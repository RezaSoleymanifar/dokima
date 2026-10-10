"""Tests for #428: issue and pull request reads use REST, and GraphQL reads left are listed.

GitHub gives REST and GraphQL separate budgets, and on 2026-10-09 GraphQL ran out while REST had most of its budget
left. `gh issue view`, `gh pr view` and `gh pr list` all run as GraphQL, as does every `gh api graphql` query. These
tests prove three things:

- Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through REST. Each read is
  run against a fake `gh` put first on PATH. The fake answers GitHub's REST paths only and refuses `gh issue`,
  `gh pr` and `gh api graphql`, logging every call. A static scan names every GraphQL read left in dokima/ and
  .github/workflows/.
- What those reads feed comes out exactly as today: the same conversation (same comments, reviews and line notes, in
  the same order, with the bot named as `dokima-runtime` the way GraphQL names it), the same pull request, labels,
  parent and issue text.
- The GraphQL reads left are listed in one place, `GRAPHQL_READS` in dokima/manifest.py, each with why REST cannot
  answer it, and the scan checks that list against every GraphQL read in the code.

A read moved to REST that GitHub refuses must still fail as the GraphQL read did, naming GitHub's reason; the fake
refuses every REST read when the state says so.
"""
import ast
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import textwrap

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from dokima import agent, audit, board, manifest  # noqa: E402

REPO = "o/r"
REFUSED = "Resource not accessible by integration (HTTP 403)"

# The GraphQL reads expected to stay, each keyed by file::function (or file::CONSTANT for a module-level query).
EXPECTED_LEFT = {
    "dokima/plan.py::fetch_issue",
    "dokima/plan.py::pr_issue_number",
    "dokima/agent.py::merge_outcome",
    "dokima/board.py::Board.__init__",
    "dokima/board.py::Board.item",
    "dokima/board.py::Board.value",
    "dokima/board.py::Board.cards",
    "dokima/board.py::Board.view_nodes",
    "dokima/audit.py::BOARD_QUERY",
}

FAKE_GH = r'''#!/usr/bin/env python3
"""A fake gh that answers GitHub's REST reads from a JSON state and refuses everything else."""
import json, os, re, subprocess, sys
from urllib.parse import parse_qsl

STATE = os.environ["FAKE_GH_STATE"]
state = json.load(open(STATE))
argv = sys.argv[1:]


def save():
    json.dump(state, open(STATE, "w"), indent=1)


def refuse(kind, reason):
    state["calls"].append({"kind": kind, "argv": argv, "refused": reason})
    save()
    print(f"gh: {reason}", file=sys.stderr)
    sys.exit(1)


if not argv or argv[0] != "api":
    refuse("graphql", "this fake GitHub answers REST reads only, and gh issue/pr run as GraphQL (HTTP 400)")
method, path, paginate, jq, fields, i = "GET", None, False, None, {}, 1
while i < len(argv):
    a = argv[i]
    if a in ("-X", "--method"):
        method = argv[i + 1].upper(); i += 2; continue
    if a in ("-q", "--jq"):
        jq = argv[i + 1]; i += 2; continue
    if a in ("-f", "-F", "--field", "--raw-field"):
        k, _, v = argv[i + 1].partition("="); fields[k] = v; i += 2; continue
    if a in ("-H", "--header", "--cache", "-t", "--template", "--hostname", "-p", "--preview"):
        i += 2; continue
    if a == "--paginate":
        paginate = True; i += 1; continue
    if a.startswith("-"):
        i += 1; continue
    if path is None:
        path = a
    i += 1
if path == "graphql":
    refuse("graphql", "this fake GitHub answers REST reads only (HTTP 400)")
if method != "GET":
    refuse("write", "this fake GitHub answers reads only (HTTP 400)")
path, _, query = path.lstrip("/").partition("?")
params = dict(parse_qsl(query))
params.update(fields)
if state.get("refuse"):
    refuse("rest", state["refuse"])
state["calls"].append({"kind": "rest", "argv": argv, "path": path, "params": params})
save()
prefix = f"repos/{state['repo']}/"
if not path.startswith(prefix):
    refuse("rest", "Not Found (HTTP 404)")
rest = path[len(prefix):].rstrip("/")
issues = state["issues"]


def listing(items):
    per = min(int(params.get("per_page", 30)), 100)
    pages = [items[k:k + per] for k in range(0, len(items), per)] or [[]]
    if paginate:
        return pages
    page = int(params.get("page", 1))
    return [pages[page - 1] if page <= len(pages) else []]


def obj(x):
    return [x]


m = re.fullmatch(r"issues/(\d+)(/comments|/labels|/parent)?", rest)
p = re.fullmatch(r"pulls/(\d+)(/reviews|/comments)?", rest)
if rest == "issues":
    want = params.get("state", "open")
    out = listing(sorted((x for x in issues.values() if want == "all" or x["state"] == want),
                         key=lambda x: -x["number"]))
elif m:
    n, sub = m.group(1), m.group(2)
    if n not in issues:
        refuse("rest", "Not Found (HTTP 404)")
    if sub == "/comments":
        out = listing(state["comments"].get(n, []))
    elif sub == "/labels":
        out = listing(issues[n]["labels"])
    elif sub == "/parent":
        up = state["parents"].get(n)
        if up is None:
            refuse("rest", "Not Found (HTTP 404)")
        out = obj(issues[str(up)])
    else:
        out = obj(issues[n])
elif rest == "pulls":
    want, head = params.get("state", "open"), params.get("head")
    found = [x for x in state["pulls"].values() if want == "all" or x["state"] == want]
    if head is not None:
        found = [x for x in found if f"{state['repo'].split('/')[0]}:{x['head']['ref']}" == head]
    out = listing(sorted(found, key=lambda x: -x["number"]))
elif p:
    n, sub = p.group(1), p.group(2)
    if n not in state["pulls"]:
        refuse("rest", "Not Found (HTTP 404)")
    out = listing(state["reviews"].get(n, [])) if sub == "/reviews" else \
        listing(state["notes"].get(n, [])) if sub == "/comments" else obj(state["pulls"][n])
elif re.fullmatch(r"actions/workflows/[^/]+/runs", rest):
    out = obj({"total_count": 0, "workflow_runs": []})
else:
    refuse("rest", "Not Found (HTTP 404)")
for page in out:
    text = json.dumps(page)
    if jq is not None:
        text = subprocess.run(["jq", "-r", "-c", jq], input=text, capture_output=True, text=True, check=True).stdout
        sys.stdout.write(text)
    else:
        print(text)
'''


def comment(cid, login, body, at, bot=False, where="issues/7"):
    """A comment as GitHub's REST API returns it."""
    return {"id": cid, "node_id": f"IC_{cid}", "html_url": f"https://github.com/{REPO}/{where}#issuecomment-{cid}",
            "user": {"login": f"{login}[bot]" if bot else login, "type": "Bot" if bot else "User"},
            "body": body, "created_at": at, "updated_at": at, "author_association": "OWNER"}


def at(k):
    """A distinct time, k minutes after 2026-10-01 00:00 UTC."""
    return f"2026-10-01T{k // 60:02d}:{k % 60:02d}:00Z"


def issue(n, title, body, state="open", labels=(), pr=False):
    """An issue (or a pull request's issue side) as GitHub's REST API returns it."""
    x = {"number": n, "node_id": f"I_{n}", "title": title, "body": body, "state": state,
         "labels": [{"name": name} for name in labels], "html_url": f"https://github.com/{REPO}/issues/{n}"}
    if pr:
        x["pull_request"] = {"url": f"https://api.github.com/repos/{REPO}/pulls/{n}"}
    return x


def pull(n, ref, state="open", sha=None, body=""):
    """A pull request as GitHub's REST API returns it."""
    return {"number": n, "state": state, "head": {"ref": ref, "sha": sha or f"{n:040d}"}, "body": body,
            "title": f"PR {n}", "html_url": f"https://github.com/{REPO}/pull/{n}"}


def world():
    """Issue 7 with 105 comments, its pull requests, its parent 5 and neighbours.

    Issue #7 has 105 comments, so a read that does not page past 100 misses the newest. Its pull requests are #11
    (closed) and #12 (open) on try/issue-7 and #14 (open) on work/issue-7; #13 on try/issue-8 belongs to issue 8.
    Comment 103 is the bot's record."""
    comments7 = [comment(1000 + k, "alice", f"comment {k}", at(k)) for k in range(105)]
    comments7[103] = comment(1103, "dokima-runtime", f"{agent.MARK}\nthe record", at(103), bot=True)
    return {
        "repo": REPO, "calls": [], "refuse": None,
        "issues": {str(x["number"]): x for x in [
            issue(5, "Five", "Parent ask"), issue(7, "Seven", "Ask", labels=("autopilot", "high")),
            issue(8, "Eight", "Other"), issue(9, "Nine", "No parent, no pull request"),
            issue(11, "PR 11", "", state="closed", pr=True), issue(12, "PR 12", "Closes #7", labels=("autopilot",), pr=True),
            issue(13, "PR 13", "", pr=True), issue(14, "PR 14", "", pr=True)]},
        "comments": {
            "5": [comment(500, "alice", "parent words", at(1), where="issues/5"),
                  comment(501, "dokima-runtime", "parent record", at(2), bot=True, where="issues/5")],
            "7": comments7,
            "9": [comment(900, "alice", f"{agent.MARK} quoted by a person", at(3), where="issues/9")],
            "11": [comment(1100, "bob", "on the closed PR", at(200), where="pull/11")],
            "12": [comment(1200, "bob", "on the open PR", at(201), where="pull/12"),
                   comment(1201, "dokima-runtime", "PR record", at(203), bot=True, where="pull/12")],
            "13": [comment(1300, "bob", "belongs to issue 8", at(204), where="pull/13")],
        },
        "pulls": {"11": pull(11, "try/issue-7", state="closed"), "12": pull(12, "try/issue-7", sha="abcdef1234567890"),
                  "13": pull(13, "try/issue-8"), "14": pull(14, "work/issue-7")},
        "reviews": {"12": [{"id": 1, "user": {"login": "carol", "type": "User"}, "body": "looks right",
                            "state": "APPROVED", "submitted_at": at(202)},
                           {"id": 2, "user": {"login": "carol", "type": "User"}, "body": "",
                            "state": "COMMENTED", "submitted_at": at(205)},
                           {"id": 3, "user": {"login": "dokima-runtime[bot]", "type": "Bot"}, "body": "blocks",
                            "state": "CHANGES_REQUESTED", "submitted_at": at(206)}],
                    "14": [{"id": 4, "user": {"login": "carol", "type": "User"}, "body": "on the work PR",
                            "state": "COMMENTED", "submitted_at": at(207)}]},
        "notes": {"12": [{"id": 9, "user": {"login": "carol", "type": "User"}, "body": "a line note",
                          "created_at": at(208), "path": "dokima/x.py", "line": 3}]},
        "parents": {"7": 5, "8": 5},
    }


@pytest.fixture
def fake(tmp_path, monkeypatch):
    """Put the fake gh first on PATH, with the world as its state.

    Returns a handle to read and change the state."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    exe = bin_dir / "gh"
    exe.write_text(FAKE_GH)
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    path = tmp_path / "state.json"
    path.write_text(json.dumps(world()))
    monkeypatch.setenv("FAKE_GH_STATE", str(path))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)

    class Fake:
        dir = bin_dir

        def state(self):
            return json.loads(path.read_text())

        def change(self, **kw):
            s = self.state()
            s.update(kw)
            path.write_text(json.dumps(s))

        def graphql_calls(self):
            return [c["argv"] for c in self.state()["calls"] if c["kind"] != "rest"]

        def rest_reads(self):
            return [c for c in self.state()["calls"] if c["kind"] == "rest"]

    return Fake()


def run(fake, what, fn):
    """Run a read, failing in plain words when it still reads through GraphQL."""
    try:
        out = fn()
    except Exception as e:  # noqa: BLE001 - every failure is reported with the calls that caused it
        raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
                             f"{fake.graphql_calls()}") from e
    assert not fake.graphql_calls(), f"{what} still reads through GraphQL: {fake.graphql_calls()}"
    return out


def new_board():
    """A Board with its project already read, so only issue reads run."""
    b = board.Board.__new__(board.Board)
    b.q, b.rest = board.gql, board.api
    b.owner, b.number, b.repo_owner, b.repo_name = "o", 1, "o", "r"
    b.id, b.fields = "PVT_1", {}
    return b


def view(c):
    """What the cards and records read from a conversation item."""
    return (c["author"]["login"], c["body"], c["createdAt"], c["where"], c.get("url"))


# 428.1: every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through REST

def test_river_reads_only_rest(fake, record_property):
    """The river reads an issue, its comments and its pull requests only through REST.

    Proves 428.1.
    Runs the conversation, the linked and open pull request lookups, the started check, the parent's words and the
    plan check rerun against a GitHub that answers REST only, and fails naming every call that went through
    GraphQL."""
    record_property("proves", "428.1")
    run(fake, "agent.conversation", lambda: agent.conversation(REPO, 7))
    run(fake, "agent.linked_prs", lambda: agent.linked_prs(REPO, 7))
    run(fake, "agent.open_pr", lambda: agent.open_pr(REPO, 7))
    run(fake, "agent.started_before", lambda: agent.started_before(REPO, 7))
    run(fake, "agent.parent_words", lambda: agent.parent_words(REPO, 7))
    run(fake, "agent.rerun_plan_check", lambda: agent.rerun_plan_check(REPO, 7))
    assert fake.rest_reads(), "428.1: no read reached GitHub's REST API"


def test_board_and_audit_read_issues_only_through_rest(fake, record_property):
    """The board and the drift audit read issues and pull requests only through REST.

    Proves 428.1.
    Runs the board's labels, open pull request, parent and pull-request-to-issue reads and the audit's open issue
    list against a GitHub that answers REST only, and fails naming every call that went through GraphQL."""
    record_property("proves", "428.1")
    b = new_board()
    run(fake, "Board.labels", lambda: b.labels("issue", 7))
    run(fake, "Board.labels of a pull request", lambda: b.labels("pr", 12))
    run(fake, "Board.open_pr", lambda: b.open_pr(7))
    run(fake, "Board.parent", lambda: b.parent(7))
    run(fake, "board.issue_of", lambda: board.issue_of(REPO, 12))
    run(fake, "audit setup_issue", lambda: audit.GitHub("o/1").setup_issue(REPO))


# The scan of GraphQL reads left in the code

GH_READS = {("issue", "view"), ("issue", "list"), ("issue", "status"),
            ("pr", "view"), ("pr", "list"), ("pr", "status"), ("pr", "checks")}
WORKFLOW_READ = re.compile(r"\bgh\s+(?:(?:issue)\s+(?:view|list|status)|(?:pr)\s+(?:view|list|status|checks)"
                           r"|api\s+graphql\b)")


def python_reads(path, source):
    """{file::where: what} for every GraphQL read in a Python file.

    A read is a GraphQL query string (a mutation is a write) or a call to gh's issue/pr read commands, which gh runs
    as GraphQL. Where is the innermost function, as Class.method inside a class, or the name a module-level string
    is assigned to."""
    found = {}

    def visit(node, where):
        for child in ast.iter_child_nodes(node):
            here = where
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                here = f"{where}.{child.name}" if where and isinstance(node, ast.ClassDef) else child.name
            elif isinstance(child, ast.Assign) and not where and len(child.targets) == 1 \
                    and isinstance(child.targets[0], ast.Name):
                here = child.targets[0].id
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                m = manifest.GRAPHQL_OP.match(child.value)
                if m and m.group(1) == "query":
                    found.setdefault(f"{path}::{here}", child.value[:60])
            if isinstance(child, ast.JoinedStr):
                head = "".join(v.value for v in child.values if isinstance(v, ast.Constant))
                m = manifest.GRAPHQL_OP.match(head)
                if m and m.group(1) == "query":
                    found.setdefault(f"{path}::{here}", head[:60])
                continue
            if isinstance(child, ast.Call):
                args = [a.value if isinstance(a, ast.Constant) and isinstance(a.value, str) else None
                        for a in child.args[:2]]
                if isinstance(child.args[0] if child.args else None, ast.List):
                    elts = child.args[0].elts
                    args = [e.value if isinstance(e, ast.Constant) and isinstance(e.value, str) else None
                            for e in elts[:3]]
                    args = args[1:] if args and args[0] == "gh" else [None, None]
                if len(args) >= 2 and tuple(args[:2]) in GH_READS:
                    found.setdefault(f"{path}::{here}", f"gh {args[0]} {args[1]}")
            visit(child, here)

    visit(ast.parse(source), "")
    return found


def workflow_reads(path, source):
    """{file::step name: the line} for every GraphQL read in a workflow."""
    found = {}
    for block in manifest.steps(source.splitlines()):
        name = re.match(r"\s*- (?:name:\s*(.*))?", block[0]).group(1) or block[0].strip()
        for line in block:
            if line.strip().startswith("#"):
                continue
            if WORKFLOW_READ.search(line):
                found.setdefault(f"{path}::{name.strip()}", line.strip()[:80])
    return found


def graphql_reads(root):
    """Every GraphQL read under root's dokima/ and .github/workflows/."""
    found = {}
    for folder, dirs, files in sorted(os.walk(os.path.join(root, "dokima"))):
        dirs.sort()
        for f in sorted(files):
            if f.endswith(".py"):
                full = os.path.join(folder, f)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                found.update(python_reads(rel, open(full).read()))
    flows = os.path.join(root, ".github", "workflows")
    for f in sorted(os.listdir(flows)) if os.path.isdir(flows) else []:
        if f.endswith((".yml", ".yaml")):
            found.update(workflow_reads(f".github/workflows/{f}", open(os.path.join(flows, f)).read()))
    return found


def listed(criterion):
    """GRAPHQL_READS from dokima/manifest.py, or a failure naming the criterion and saying it is missing."""
    reads = getattr(manifest, "GRAPHQL_READS", None)
    assert isinstance(reads, dict), \
        f"{criterion}: dokima/manifest.py has no GRAPHQL_READS dict listing the GraphQL reads left"
    return reads


def test_no_graphql_read_of_issues_or_pull_requests_is_left(record_property):
    """No GraphQL read of an issue, pull request or comment is left anywhere.

    Proves 428.1.
    Scans dokima/ and .github/workflows/ for gh issue/pr read commands, `gh api graphql` and GraphQL query strings,
    and fails naming every one outside the reads REST cannot answer (the board's project reads, the edit history,
    a pull request's closing issues and its merge state)."""
    record_property("proves", "428.1")
    extra = {k: v for k, v in graphql_reads(ROOT).items() if k not in EXPECTED_LEFT}
    assert not extra, "428.1: these still read through GraphQL:\n" + "\n".join(f"  {k}: {v}" for k, v in extra.items())


# 428.2: the cards and board those reads feed show exactly what they show today

def test_conversation_is_the_same_as_today(fake, record_property):
    """The issue's conversation comes out the same as today, in the same order.

    Proves 428.2.
    Issue #7 has 105 comments, a bot record among them, and three pull requests (closed, open, and one from its work
    branch), with comments, reviews (one with no text, left out as today) and a line note; a pull request of another
    issue must not show. The bot is named `dokima-runtime`, as GraphQL names it, and each comment keeps its link."""
    record_property("proves", "428.2")
    d, items = run(fake, "agent.conversation", lambda: agent.conversation(REPO, 7))
    assert (d["number"], d["title"], d["body"]) == (7, "Seven", "Ask"), f"428.2: the issue read as {d!r}"
    s = world()
    want = []
    for c in s["comments"]["7"]:
        login = c["user"]["login"].removesuffix("[bot]")
        want.append((login, c["body"], c["created_at"], "issue #7", c["html_url"]))
    for n in ("11", "12"):
        want += [(c["user"]["login"].removesuffix("[bot]"), c["body"], c["created_at"], f"PR #{n}", c["html_url"])
                 for c in s["comments"].get(n, [])]
    want += [("carol", "looks right", at(202), "PR #12 review (approved)", None),
             ("dokima-runtime", "blocks", at(206), "PR #12 review (changes_requested)", None),
             ("carol", "a line note", at(208), "PR #12 line note on dokima/x.py:3", None),
             ("carol", "on the work PR", at(207), "PR #14 review (commented)", None)]
    want.sort(key=lambda w: w[2])
    got = [view(c) for c in items]
    assert got == want, ("428.2: the conversation differs from today's.\nmissing: "
                         f"{[w for w in want if w not in got][:5]}\nunexpected: {[g for g in got if g not in want][:5]}"
                         f"\nfirst difference at {next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), len(got))}")
    text = agent.issue_text(d, items)
    assert text.startswith("# Issue #7: Seven\n\nAsk\n\n## Comments\n"), f"428.2: the issue text starts {text[:80]!r}"
    assert f"### dokima-runtime on issue #7 ({at(103)})" in text, "428.2: the bot's record is not named dokima-runtime"


def test_pull_request_lookups_are_the_same_as_today(fake, record_property):
    """The issue's pull requests, and its open one, are found as today.

    Proves 428.2.
    Expects #11, #12 and #14 for issue 7 (never #13 of issue 8), #12 as its open pull request, none for issue 9,
    and the plan check rerun naming #12's head commit."""
    record_property("proves", "428.2")
    assert run(fake, "agent.linked_prs", lambda: agent.linked_prs(REPO, 7)) == [11, 12, 14], "428.2: wrong pull requests"
    assert run(fake, "agent.open_pr", lambda: agent.open_pr(REPO, 7)) == "12", "428.2: wrong open pull request of #7"
    assert run(fake, "agent.open_pr", lambda: agent.open_pr(REPO, 8)) == "13", "428.2: wrong open pull request of #8"
    assert run(fake, "agent.open_pr", lambda: agent.open_pr(REPO, 9)) == "", "428.2: #9 has no open pull request"
    said = run(fake, "agent.rerun_plan_check", lambda: agent.rerun_plan_check(REPO, 7))
    assert said == "PR #12 has no plan check on abcdef1 yet: GitHub runs it on the next push.", f"428.2: said {said!r}"
    assert run(fake, "agent.rerun_plan_check", lambda: agent.rerun_plan_check(REPO, 9)) == \
        "No open pull request: no plan check to run again.", "428.2: #9 has no open pull request"


def test_started_and_parent_words_are_the_same_as_today(fake, record_property):
    """Whether something started, and the parent's words, come out as today.

    Proves 428.2.
    Issue 7's bot record is its 104th comment, past the first page of 100, so it counts as started; issue 9 has only a
    person's comment quoting the marker, so it does not. The parent's words are #5's text and both its comments, each
    with its author (the bot as `dokima-runtime`), text, time and link."""
    record_property("proves", "428.2")
    assert run(fake, "started_before", lambda: agent.started_before(REPO, 7)) is True, "428.2: #7's record was missed"
    assert run(fake, "started_before", lambda: agent.started_before(REPO, 9)) is False, "428.2: #9 never started"
    up = run(fake, "parent_words", lambda: agent.parent_words(REPO, 7))
    assert (up["number"], up["body"]) == (5, "Parent ask"), f"428.2: the parent read as {up!r}"
    got = [(c["author"]["login"], c["body"], c["createdAt"], c["url"]) for c in up["comments"]]
    assert got == [("alice", "parent words", at(1), f"https://github.com/{REPO}/issues/5#issuecomment-500"),
                   ("dokima-runtime", "parent record", at(2), f"https://github.com/{REPO}/issues/5#issuecomment-501")], \
        f"428.2: the parent's comments read as {got!r}"


def test_board_reads_are_the_same_as_today(fake, record_property):
    """The board reads the same labels, open pull request, parent and issue as today.

    Proves 428.2.
    Expects #7's labels autopilot and high, #12's autopilot, #12 as #7's open pull request and none for #9, #5 as
    #7's parent and none for #9 (GitHub answers 404 when an issue has no parent), and #7 as #12's issue."""
    record_property("proves", "428.2")
    b = new_board()
    assert run(fake, "labels", lambda: b.labels("issue", 7)) == {"autopilot", "high"}, "428.2: #7's labels"
    assert run(fake, "labels", lambda: b.labels("pr", 12)) == {"autopilot"}, "428.2: #12's labels"
    assert run(fake, "open_pr", lambda: b.open_pr(7)) == 12, "428.2: #7's open pull request"
    assert run(fake, "open_pr", lambda: b.open_pr(9)) is None, "428.2: #9 has no open pull request"
    assert run(fake, "parent", lambda: b.parent(7)) == 5, "428.2: #7's parent"
    assert run(fake, "parent", lambda: b.parent(9)) is None, "428.2: #9 has no parent"
    assert run(fake, "issue_of", lambda: board.issue_of(REPO, 12)) == 7, "428.2: #12 was built for #7"


def test_audit_finds_the_same_setup_issue_past_100(fake, record_property):
    """The drift audit finds its Setup issue past 100 open issues, as today.

    Proves 428.2.
    The marker is on open issues #250 and #260 and on pull request #3, with 160 open issues in all; the audit must
    pick #250, the oldest issue, past the first page of 100."""
    record_property("proves", "428.2")
    s = fake.state()
    many = {str(n): issue(n, f"Issue {n}", "plain") for n in range(101, 261)}
    many["250"]["body"] = many["260"]["body"] = f"{audit.MARK}\nSetup"
    many["3"] = issue(3, "PR 3", f"{audit.MARK}\nnot an issue", pr=True)
    fake.change(issues={**s["issues"], **many})
    got = run(fake, "audit setup_issue", lambda: audit.GitHub("o/1").setup_issue(REPO))
    assert got == {"number": 250, "body": f"{audit.MARK}\nSetup"}, f"428.2: the audit found {got!r}"


def substitutions(text):
    """Every `$( ... )` command substitution in a shell text, quotes and nesting respected."""
    out, i = [], 0
    while (i := text.find("$(", i)) != -1:
        depth, j, quote = 1, i + 2, None
        while j < len(text) and depth:
            ch = text[j]
            if quote:
                if ch == quote:
                    quote = None
                elif quote == '"' and text.startswith("$(", j):
                    depth += 1
                    j += 1
            elif ch in "'\"":
                quote = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            j += 1
        out.append(text[i + 2:j - 1])
        i += 2
    return out


def workflow(name):
    return open(os.path.join(ROOT, ".github", "workflows", name)).read()


def read_lookups(name):
    """The gh reads a workflow runs inside `$( ... )`: no writes, no user lookups."""
    return [s.strip() for s in substitutions(workflow(name)) if s.strip().startswith("gh ")
            and not re.search(r"-X\s*(POST|PATCH|PUT|DELETE)|--method|users/", s)]


def shell(cmd, env_extra=None, **kw):
    env = {**os.environ, "N": "7", "GITHUB_REPOSITORY": REPO, **(env_extra or {})}
    return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, env=env, **kw)


def test_workflow_lookups_find_the_same_as_today(fake, record_property, tmp_path):
    """The workflows find the same pull request and issue text as today.

    Proves 428.2.
    Runs each read the agent and worker workflows make inside `$( ... )` with N=7: one for try/issue-7 must print 12,
    one for work/issue-7 must print 14, and the title read must print Seven. Then runs planner.yml's line that writes
    /tmp/issue.md and checks the file is `Issue #7: Seven`, a blank line and the issue's text."""
    record_property("proves", "428.2")
    seen = {"try": 0, "work": 0, "title": 0}
    for name in ("agent.yml", "worker.yml"):
        for cmd in read_lookups(name):
            r = shell(cmd)
            kind = "try" if "try/issue-" in cmd else "work" if "work/issue-" in cmd else "title"
            want = {"try": "12", "work": "14", "title": "Seven"}[kind]
            assert r.returncode == 0 and r.stdout.strip() == want, \
                f"428.2: {name} `{cmd}` printed {r.stdout.strip()!r} (exit {r.returncode}, {r.stderr.strip()}), not {want}"
            seen[kind] += 1
    assert seen["try"] >= 3 and seen["work"] >= 1 and seen["title"] >= 1, f"428.2: the workflows' lookups were {seen}"
    line = next(l.strip() for l in workflow("planner.yml").splitlines() if "> /tmp/issue.md" in l)
    out = tmp_path / "issue.md"
    r = shell(line.replace("/tmp/issue.md", str(out)))
    assert r.returncode == 0, f"428.2: planner.yml's issue read failed: {r.stderr.strip()}"
    assert out.read_text() == "Issue #7: Seven\n\nAsk\n", f"428.2: planner.yml wrote {out.read_text()!r}"
    assert not fake.graphql_calls(), f"428.2: the workflows still read through GraphQL: {fake.graphql_calls()}"


# 428.3 and 428.4: the GraphQL reads left are listed in one place, and a test checks the list

def test_graphql_list_names_exactly_the_reads_rest_cannot_answer(record_property):
    """GRAPHQL_READS in dokima/manifest.py lists exactly the reads REST cannot answer.

    Proves 428.3.
    Expects the board's project reads, the drift audit's board read, an issue's edit history, a pull request's
    closing issues and its merge state, and no other; every reason is a sentence of at least five words."""
    record_property("proves", "428.3")
    reads = listed("428.3")
    assert set(reads) == EXPECTED_LEFT, (f"428.3: GRAPHQL_READS lists {sorted(set(reads) - EXPECTED_LEFT)} it should "
                                         f"not and misses {sorted(EXPECTED_LEFT - set(reads))}")
    thin = [k for k, why in reads.items() if not isinstance(why, str) or len(why.split()) < 5]
    assert not thin, f"428.3: these GraphQL reads have no reason why REST cannot answer them: {thin}"


def test_graphql_list_matches_every_graphql_read_in_the_code(record_property):
    """The list of GraphQL reads matches every GraphQL read in the code.

    Proves 428.4.
    Scans dokima/ and .github/workflows/ and fails naming each GraphQL read the list leaves out and each entry no
    read in the code matches."""
    record_property("proves", "428.4")
    reads, found = listed("428.4"), graphql_reads(ROOT)
    unlisted = sorted(set(found) - set(reads))
    stale = sorted(set(reads) - set(found))
    assert not unlisted, "428.4: GraphQL reads not in GRAPHQL_READS:\n" + "\n".join(f"  {k}: {found[k]}" for k in unlisted)
    assert not stale, f"428.4: GRAPHQL_READS entries no GraphQL read in the code matches: {stale}"


def test_the_list_check_catches_a_new_graphql_read(tmp_path, record_property):
    """A new GraphQL read added anywhere is caught and named.

    Proves 428.4.
    Copies the code, adds one GraphQL query in Python, one `gh pr view` call and one `gh issue view` in a workflow,
    and checks the scan finds all three while the list names none of them; and that the copy's own reads match
    the list otherwise."""
    record_property("proves", "428.4")
    reads = listed("428.4")
    shutil.copytree(os.path.join(ROOT, "dokima"), tmp_path / "dokima")
    shutil.copytree(os.path.join(ROOT, ".github", "workflows"), tmp_path / ".github" / "workflows")
    (tmp_path / "dokima" / "extra.py").write_text(textwrap.dedent('''
        def sneaky(gh):
            gh("pr", "view", "1", "--json", "title")
            return "query($n:Int!){repository(owner:\\"o\\",name:\\"r\\"){issue(number:$n){title}}}"
        '''))
    (tmp_path / ".github" / "workflows" / "extra.yml").write_text(textwrap.dedent('''
        jobs:
          j:
            steps:
              - name: Read the title
                run: |
                  T=$(gh issue view 1 --json title -q .title)
        '''))
    found = graphql_reads(str(tmp_path))
    new = {"dokima/extra.py::sneaky", ".github/workflows/extra.yml::Read the title"}
    assert new <= set(found), f"428.4: the scan missed a new GraphQL read: {sorted(new - set(found))}"
    assert not new & set(reads), "428.4: the list names a read that does not exist in the real code"
    assert set(found) - new == set(reads), f"428.4: the copy's reads differ from the list: {sorted(set(found) ^ set(reads))}"


# 428.5: a read moved to REST that GitHub refuses fails as the GraphQL read did, naming GitHub's reason

def refused_rest(fake):
    """The REST reads the fake refused."""
    return [c for c in fake.state()["calls"] if c["kind"] == "rest" and c.get("refused")]


def test_refused_river_and_board_reads_fail_naming_githubs_reason(fake, record_property):
    """A refused REST read fails loudly with GitHub's reason, never reading as nothing.

    Proves 428.5.
    With GitHub refusing every REST read, the conversation, the open pull request lookup, the started check, the
    board's labels and parent and the audit's issue list each raise with GitHub's reason, and the pull request's
    issue lookup says it could not read the pull request and why, as each did on GraphQL."""
    record_property("proves", "428.5")
    fake.change(refuse=REFUSED)
    b = new_board()
    for what, fn in [("conversation", lambda: agent.conversation(REPO, 7)), ("open_pr", lambda: agent.open_pr(REPO, 7)),
                     ("started_before", lambda: agent.started_before(REPO, 7)),
                     ("Board.labels", lambda: b.labels("issue", 7)), ("Board.parent", lambda: b.parent(7)),
                     ("Board.open_pr", lambda: b.open_pr(7)),
                     ("audit setup_issue", lambda: audit.GitHub("o/1").setup_issue(REPO))]:
        before = len(refused_rest(fake))
        with pytest.raises(subprocess.CalledProcessError) as e:
            fn()
        assert REFUSED in (e.value.stderr or ""), f"428.5: {what} failed without GitHub's reason: {e.value.stderr!r}"
        assert len(refused_rest(fake)) > before, f"428.5: {what} did not read through REST: {fake.graphql_calls()}"
    with pytest.raises(RuntimeError, match=re.escape(REFUSED)) as e:
        board.issue_of(REPO, 12)
    assert "Could not read PR #12" in str(e.value), f"428.5: issue_of said {e.value}"
    assert not fake.graphql_calls(), f"428.5: these reads still went through GraphQL: {fake.graphql_calls()}"


def step(name, flow="agent.yml"):
    """The run script of the workflow step with that name."""
    for block in manifest.steps(workflow(flow).splitlines()):
        if re.match(rf"\s*- name:\s*{re.escape(name)}\s*$", block[0]):
            return "\n".join(block)
    raise AssertionError(f"428.5: {flow} has no step named {name!r}")


def test_refused_workflow_lookups_fail_as_today(fake, record_property):
    """A refused pull request lookup in a workflow behaves as today.

    Proves 428.5. The queued card goes on; the record step fails naming GitHub's reason.
    With GitHub refusing every REST read, the queued card's lookup reads a refused lookup as no pull request and the
    step goes on, as it does today; the record step's lookup stops the step, naming GitHub's reason."""
    record_property("proves", "428.5")
    fake.change(refuse=REFUSED)
    queued = next(l.strip() for l in step("Put up the run's card, queued").splitlines() if l.strip().startswith("PR=$("))
    r = shell(f"set -eo pipefail\n{queued}\necho \"after:[$PR]\"")
    assert r.returncode == 0 and r.stdout.strip() == "after:[]", \
        f"428.5: the queued card's lookup did not read a refusal as none: exit {r.returncode}, {r.stdout!r} {r.stderr!r}"
    record = next(l.strip() for l in step("Post the record as a comment, on the PR once there is one").splitlines()
                  if l.strip().startswith("PR=$("))
    r = shell(f"set -eo pipefail\n{record}\necho \"after:[$PR]\"")
    assert r.returncode != 0 and "after:" not in r.stdout, "428.5: the record step went on after GitHub refused"
    assert REFUSED in r.stderr, f"428.5: the record step failed without GitHub's reason: {r.stderr!r}"
    assert len(refused_rest(fake)) == 2 and not fake.graphql_calls(), \
        f"428.5: the lookups did not read through REST: {fake.graphql_calls()}"
