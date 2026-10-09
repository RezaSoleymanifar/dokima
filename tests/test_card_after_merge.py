"""A PR's card shows its true state after merge, however fast the owner merges (#322).

On #246 the owner merged twelve seconds after the tests finished; the card run that followed could no longer find the
PR (GitHub's event names no PR once it is merged, and GitHub lists only open PRs for a squash-merged commit), so the
PR card kept saying All tests was running. These tests read the real `.github/workflows/card.yml`: they work out, for
one GitHub event, whether the card job runs, its concurrency group and the env its "Write the card" step gets, the way
GitHub would, then run the real `dokima/card.py` main() with that env against a fake GitHub.

The fake GitHub (FakeGitHub below) answers `gh` the way GitHub does for these reads:
    gh api repos/o/r/commits/SHA/pulls          open PRs whose head is SHA, plus the merged PR of a commit on main
    gh api repos/o/r/pulls?head=o:BRANCH&state=open|closed|all   (any order of query parameters)
    gh api repos/o/r/pulls?state=...            every PR in that state
    gh api repos/o/r/pulls/N                    one PR
    gh api repos/o/r/issues/N/dependencies/blocked_by|blocking, .../sub_issues   none
    gh api search/issues?q=...SHA...            the PRs whose head is SHA, open or merged
    gh api graphql ... -F p=N                   the issue PR N closes (closingIssuesReferences)
    gh api -X PATCH repos/o/r/pulls/N -F body=@FILE   writes the PR's description
Anything else fails as a refused call would, and is logged in `refused`. What the card draws from (records, checks,
reviews) is faked at card.gather, so these tests prove which issue and PR get drawn and what the drawn card says.
"""
import fnmatch
import os
import re
import shlex
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import body, card, plan  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
WORKFLOW = os.path.join(ROOT, ".github/workflows/card.yml")
REPO = "o/r"
OWNER = "owner"


# ---------------------------------------------------------------- card.yml, read the way GitHub reads it

def workflow():
    """card.yml's text."""
    with open(WORKFLOW) as f:
        return f.read()


def scalar(text):
    """One plain, quoted or flow-list YAML value, as a string, a list or None."""
    text = text.strip()
    if not text or text == "~" or text == "null":
        return None
    if text.startswith("[") and text.endswith("]"):
        return [scalar(t) for t in text[1:-1].split(",") if t.strip()]
    if len(text) > 1 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1].replace("''", "'") if text[0] == "'" else text[1:-1]
    return text


def parse_yaml(text):
    """The workflow as dicts, lists and strings.

    Handles the part of YAML GitHub workflows use: mappings, `- ` lists, flow lists, quoted values, comments and
    block values (`>-`, `>`, `|`, `|-`). The repo has no YAML library, so the test reads the file itself."""
    lines = []
    for raw in text.splitlines():
        lines.append(raw.rstrip())

    def indent(line):
        return len(line) - len(line.lstrip(" "))

    def skip(i):
        while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
            i += 1
        return i

    def block_text(i, style, parent):
        """A block value's text and the line after it."""
        got, ind = [], None
        while i < len(lines) and (not lines[i].strip() or indent(lines[i]) > parent):
            if lines[i].strip():
                ind = indent(lines[i]) if ind is None else ind
                got.append(lines[i][ind:])
            else:
                got.append("")
            i += 1
        while got and not got[-1]:
            got.pop()
        joined = " ".join(g.strip() for g in got) if style.startswith(">") else "\n".join(got)
        return joined, i

    def value(rest, i, parent):
        """The value after `key:` (or `- `) and the line after it."""
        rest = rest.strip()
        if "${{" not in rest and not rest.startswith(("'", '"')):
            rest = re.sub(r"\s+#.*$", "", rest).strip()
        if rest in (">", ">-", "|", "|-", ">+", "|+"):
            return block_text(i, rest, parent)
        if rest:
            return scalar(rest), i
        j = skip(i)
        if j < len(lines) and indent(lines[j]) > parent:
            return node(j, indent(lines[j]))
        if j < len(lines) and indent(lines[j]) == parent and lines[j].lstrip().startswith("- "):
            return node(j, parent)
        return None, i

    def node(i, ind):
        i = skip(i)
        if i < len(lines) and lines[i].lstrip().startswith("- ") and indent(lines[i]) == ind:
            out = []
            while True:
                i = skip(i)
                if i >= len(lines) or indent(lines[i]) != ind or not lines[i].lstrip().startswith("- "):
                    return out, i
                inner = lines[i][ind + 2:]
                if re.match(r"[A-Za-z_][\w-]*:(\s|$)", inner):
                    lines[i] = " " * (ind + 2) + inner
                    item, i = node(i, ind + 2)
                else:
                    item, i = value(inner, i + 1, ind)
                out.append(item)
        out = {}
        while True:
            i = skip(i)
            if i >= len(lines) or indent(lines[i]) != ind or lines[i].lstrip().startswith("- "):
                return out, i
            m = re.match(r"\s*([^:]+?):(\s.*|)$", lines[i])
            if not m:
                return out, i
            out[m.group(1).strip().strip("'\"")], i = value(m.group(2), i + 1, ind)

    return node(0, 0)[0]


def parsed():
    """card.yml as dicts, lists and strings."""
    return parse_yaml(workflow())


def triggers():
    """The `on:` block of card.yml: each trigger and its settings."""
    on = parsed().get("on")
    if isinstance(on, list):
        return {t: None for t in on}
    if isinstance(on, str):
        return {on: None}
    return on or {}


def trigger_types(name):
    """The event types card.yml lists for trigger `name`.

    None without that trigger, [] when it lists no types."""
    on = triggers()
    if name not in on:
        return None
    types = (on[name] or {}).get("types") if isinstance(on[name], dict) else None
    return [types] if isinstance(types, str) else list(types or [])


def lookup(ctx, path):
    """The value at a dotted path like github.event.workflow_run.pull_requests[0].number; None when missing."""
    cur = ctx
    for part in re.findall(r"[A-Za-z_][A-Za-z0-9_-]*|\[\d+\]", path):
        if part.startswith("["):
            i = int(part[1:-1])
            cur = cur[i] if isinstance(cur, list) and i < len(cur) else None
        else:
            cur = cur.get(part) if isinstance(cur, dict) else None
    return cur


PATH = re.compile(r"\b(?:github|inputs|vars|secrets|steps|env|needs)(?:\.[A-Za-z_][A-Za-z0-9_-]*|\[\d+\])+")


def evaluate(expr, ctx):
    """The value of one GitHub expression, worked out the way GitHub does.

    Handles paths, '' strings, ==, !=, !, &&, ||, true/false/null and the common functions."""
    parts = re.split(r"('(?:[^']|'')*')", expr)
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            out.append(repr(p[1:-1].replace("''", "'")))
            continue
        p = PATH.sub(lambda m: f"_L({m.group(0)!r})", p)
        p = p.replace("&&", " and ").replace("||", " or ")
        p = re.sub(r"!(?!=)", " not ", p)
        out.append(p)

    def text(v):
        return "" if v is None else str(v).lower() if isinstance(v, bool) else str(v)

    names = {"_L": lambda path: lookup(ctx, path), "true": True, "false": False, "null": None,
             "format": lambda s, *a: re.sub(r"\{(\d+)\}", lambda m: text(a[int(m.group(1))]), s),
             "contains": lambda a, b: (b in a) if isinstance(a, list) else text(b).lower() in text(a).lower(),
             "startsWith": lambda a, b: text(a).lower().startswith(text(b).lower()),
             "endsWith": lambda a, b: text(a).lower().endswith(text(b).lower()),
             "toJSON": lambda v: __import__("json").dumps(v), "join": lambda a, s=",": s.join(map(text, a or [])),
             "always": lambda: True, "success": lambda: True, "failure": lambda: False, "cancelled": lambda: False}
    return eval("".join(out), {"__builtins__": {}}, names)


def render_value(value, ctx):
    """A workflow value with every ${{ }} rendered as GitHub renders it.

    A null renders as an empty string."""
    def one(m):
        v = evaluate(m.group(1), ctx)
        return "" if v is None else str(v).lower() if isinstance(v, bool) else str(v)
    return re.sub(r"\$\{\{(.*?)\}\}", one, str(value if value is not None else ""), flags=re.S).strip()


def condition(expr, ctx):
    """Whether a job's or step's `if:` lets this event through; no `if:` always does."""
    if expr is None:
        return True
    expr = str(expr).strip()
    inner = re.fullmatch(r"\$\{\{(.*)\}\}", expr, re.S)
    return bool(evaluate(inner.group(1) if inner else expr, ctx))


def the_job():
    """The card workflow's one job."""
    jobs = parsed().get("jobs") or {}
    assert len(jobs) == 1, f"card.yml has {len(jobs)} jobs; these tests expect one"
    return next(iter(jobs.values()))


def job_runs(ctx):
    """Whether the card job's `if:` lets this event through."""
    return condition(the_job().get("if"), ctx)


def group(ctx):
    """The card run's concurrency group for this event, and its cancel-in-progress.

    cancel-in-progress says whether a newer run cancels one already going."""
    c = parsed().get("concurrency")
    if isinstance(c, str):
        return render_value(c, ctx), "false"
    c = c or {}
    return (render_value(c.get("group"), ctx) if c.get("group") is not None else None), \
        str(c.get("cancel-in-progress") or "false")


CARD_CALL = re.compile(r"python3?\s+(?:dokima/card\.py|-m\s+dokima\.card)\b([^|;&\n]*)")


def card_steps(ctx):
    """The card.py calls the card job makes for this event, as (env, argv) in order.

    Only steps whose `if:` lets the event through count; env is rendered as GitHub renders it."""
    out = []
    for step in the_job().get("steps") or []:
        if not isinstance(step, dict) or not step.get("run") or not condition(step.get("if"), ctx):
            continue
        env = {k: render_value(v, ctx) for k, v in (step.get("env") or {}).items()}
        for m in CARD_CALL.finditer(str(step["run"])):
            out.append((env, ["card.py", *shlex.split(m.group(1))]))
    return out


def starts(ctx, files=()):
    """Whether this event starts card.yml at all.

    Checks its trigger, types, branches and paths, then the job's `if:`.

    `files` are the files a push changed, for a `paths:` filter."""
    name = ctx["github"]["event_name"]
    on = triggers()
    if name not in on:
        return False
    rules = on[name] if isinstance(on[name], dict) else {}
    action = ctx["github"]["event"].get("action")
    types = rules.get("types")
    if types and action not in ([types] if isinstance(types, str) else types):
        return False
    if name == "workflow_run":
        wanted = rules.get("workflows") or []
        if ctx["github"]["event"]["workflow_run"]["name"] not in ([wanted] if isinstance(wanted, str) else wanted):
            return False
    if name == "push":
        branch = ctx["github"]["ref"].split("refs/heads/", 1)[-1]
        branches = rules.get("branches")
        if branches and not any(fnmatch.fnmatch(branch, b) for b in ([branches] if isinstance(branches, str) else branches)):
            return False
        paths = rules.get("paths")
        if paths and not any(fnmatch.fnmatch(f, p.replace("**", "*")) for f in files
                             for p in ([paths] if isinstance(paths, str) else paths)):
            return False
    return job_runs(ctx)


# ---------------------------------------------------------------- the events

def event(name, action=None, sender="User", ref="refs/heads/main", **payload):
    """GitHub's context for one event, as its expressions see it."""
    ev = dict(payload, action=action, sender={"type": sender, "login": "dokima-runtime[bot]" if sender == "Bot" else OWNER},
              repository={"default_branch": "main", "full_name": REPO})
    inputs = payload.get("inputs") or {}
    return {"github": {"event_name": name, "event": ev, "repository": REPO, "ref": ref,
                       "sha": "m0", "run_id": "777"},
            "inputs": inputs, "vars": {"DOKIMA_APP_ID": "1"}, "secrets": {}, "steps": {"app": {"outputs": {"token": "t"}}}}


def merged_pr(pr, sender="Bot"):
    """GitHub's event when PR `pr` merges: pull_request_target (or pull_request), closed, merged."""
    payload = {"number": pr["number"], "pull_request": dict(pr), "repository": {"full_name": REPO}}
    return event("pull_request_target", "closed", sender, **payload)


def check_finished(head_sha, head_branch, pull_requests, title="full suite"):
    """GitHub's workflow_run event when a check workflow finishes on `head_sha`."""
    return event("workflow_run", "completed", "Bot",
                 workflow_run={"head_sha": head_sha, "head_branch": head_branch, "pull_requests": pull_requests,
                               "display_title": title, "name": "full suite", "id": 99, "event": "pull_request_target"})


def issue_edited(number):
    return event("issues", "edited", "User", issue={"number": number})


def pushed_to_main(files, sha="m9"):
    """GitHub's push event when a merge lands commit `sha` on main, changing `files`."""
    commit = {"id": sha, "modified": list(files), "added": [], "removed": []}
    return event("push", None, "User", ref="refs/heads/main", after=sha, commits=[commit], head_commit=commit)


# ---------------------------------------------------------------- a fake GitHub

def pr(number, issue, state="open", merged=False, sha=None, merge_commit=None, card_text=None):
    """One PR as GitHub's API gives it, closing `issue`.

    `card_text` puts an older card on top of its description, as code wrote it before."""
    text = f"Closes #{issue}"
    if card_text:
        text = f"{plan.CARD_START}\n{card_text}\n{plan.CARD_END}\n\n{text}"
    return {"number": number, "state": state, "merged": merged, "merged_at": "2026-10-08T21:36:54Z" if merged else None,
            "merged_by": {"login": OWNER} if merged else None, "body": text,
            "html_url": f"https://github.com/{REPO}/pull/{number}", "merge_commit_sha": merge_commit,
            "head": {"ref": f"try/issue-{issue}", "sha": sha or f"head{number}"}, "base": {"ref": "main"}}


class FakeGitHub:
    """GitHub with a few PRs, answering `gh` as described at the top of this file."""

    def __init__(self, prs, closes):
        self.prs, self.closes = prs, closes
        self.refused, self.pr_bodies = [], {}

    def refuse(self, args):
        self.refused.append(args)
        raise subprocess.CalledProcessError(1, ["gh", *args], "", "gh: Not Found (HTTP 404)")

    def __call__(self, *args, **kw):
        import json
        args = [str(a) for a in args]
        if args[:1] != ["api"]:
            return self.refuse(args)
        rest = args[1:]
        method = "GET"
        if "-X" in rest:
            method = rest[rest.index("-X") + 1]
        path = next((a for a in rest if a.startswith("repos/") or a.startswith("search/") or a == "graphql"), None)
        if path == "graphql":
            p = next((a.split("=", 1)[1] for a in rest if a.startswith("p=")), None)
            issue = self.closes.get(int(p)) if p else None
            nodes = [{"number": issue}] if issue else []
            return json.dumps({"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": nodes}}}}})
        if path is None:
            return self.refuse(args)
        base, _, query = path.partition("?")
        q = dict(urllib.parse.parse_qsl(query))
        m = re.fullmatch(rf"repos/{REPO}/pulls/(\d+)", base)
        if m and method == "PATCH":
            f = next(a for a in rest if a.startswith("body="))[5:]
            if f.startswith("@"):
                with open(f[1:]) as fh:
                    f = fh.read()
            self.pr_bodies[int(m.group(1))] = f
            return "{}"
        if method != "GET":
            return self.refuse(args)
        if m:
            found = [p for p in self.prs if p["number"] == int(m.group(1))]
            return json.dumps(found[0]) if found else self.refuse(args)
        if re.fullmatch(rf"repos/{REPO}/issues/\d+/(?:dependencies/blocked_by|dependencies/blocking|sub_issues)", base):
            return "[]"
        m = re.fullmatch(rf"repos/{REPO}/commits/(\w+)/pulls", base)
        if m:
            sha = m.group(1)
            # GitHub lists the merged PR that brought a commit into main, and otherwise only open PRs.
            return json.dumps([p for p in self.prs if (p["state"] == "open" and p["head"]["sha"] == sha)
                               or (p["merged"] and p["merge_commit_sha"] == sha)])
        if base == f"repos/{REPO}/pulls":
            state = q.get("state", "open")
            found = [p for p in self.prs if state == "all" or p["state"] == state]
            if "head" in q:
                found = [p for p in found if f"o:{p['head']['ref']}" == q["head"]]
            return json.dumps(found)
        if base == "search/issues":
            items = [{"number": p["number"], "state": p["state"], "pull_request": {"merged_at": p["merged_at"]}}
                     for p in self.prs if p["head"]["sha"] in q.get("q", "")]
            return json.dumps({"total_count": len(items), "items": items})
        return self.refuse(args)


MERGED = pr(5, 40, state="closed", merged=True, sha="abc", merge_commit="m1")
OPEN = pr(6, 41, sha="def")


def world(monkeypatch, tmp_path, prs=(MERGED, OPEN)):
    """Fake GitHub for card.py, recording every card it draws and writes.

    Returns the fake, the (issue, PR) pairs drawn, and the issue cards saved by number."""
    gh = FakeGitHub(list(prs), {5: 40, 6: 41, 246: 240, 312: 280, 330: 322})
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(card, "gh", gh)
    monkeypatch.setattr(plan, "gh", gh, raising=False)
    drawn, saved = [], {}

    def gather(repo, number, pr_number):
        drawn.append((number, int(pr_number) if pr_number else None))
        the_pr = next((p for p in gh.prs if pr_number and p["number"] == int(pr_number)), None)
        return found_for(number, the_pr)

    monkeypatch.setattr(card, "gather", gather)
    monkeypatch.setattr(card, "their_links", lambda *a, **k: {"relates_to": [], "blocked_by": [], "blocks": []})
    monkeypatch.setattr(plan, "fetch_issue", lambda repo, n: {
        "number": n, "url": f"https://github.com/{REPO}/issues/{n}", "title": f"issue {n}",
        "current_body": f"{body.MARKER}\n\nThe owner's ask."})

    def save(repo, number, current, top):
        saved[number] = top
        return True

    monkeypatch.setattr(body, "save", save)
    return gh, drawn, saved


def check(name, n):
    return {"name": name, "status": "completed", "conclusion": "success",
            "html_url": f"https://github.com/{REPO}/actions/runs/2/job/{n}"}


def found_for(number, the_pr):
    """What GitHub holds for an issue whose PR merged with everything passed.

    An approved plan, a build, an approving code review, every check green on the PR's head, and a code owner's
    merge."""
    src = f"https://github.com/{REPO}/issues/{number}"
    h = {"kind": "user_story", "summary": "A card.", "user_story": "Owners see a card.",
         "acceptance_criteria": [{"text": "first thing works", "source": src}], "non_functional": [],
         "scope": ["x.py"], "out_of_scope": [], "tests": {f"{number}.1": ["tests/test_a.py::test_one"]}}
    run = f"https://github.com/{REPO}/actions/runs/"
    recs = [{"role": "planner", "stage": None, "handback": h, "check": {"passed": True}, "run": run + "8"},
            {"role": "reviewer", "stage": "plan", "handback": {"verdict": "approve"}, "check": {"passed": True}, "run": run + "9"},
            {"role": "worker", "stage": None, "handback": {}, "check": {"passed": True}, "run": run + "10"},
            {"role": "reviewer", "stage": "pr", "handback": {"verdict": "approve"}, "check": {"passed": True}, "run": run + "11"}]
    checks = [check(f"{number}.1 · first thing works", 1), check(card.ALL_TESTS, 3)] if the_pr else []
    return {"recs": recs, "pr": the_pr, "check_runs": checks, "reviews": [], "owners": {OWNER}, "tests": {},
            "worker": {"status": "completed", "conclusion": "success", "html_url": run + "10"}, "children": []}


def run_card(monkeypatch, ctx):
    """Run the real card.py main() for every card.py call card.yml's job makes for this event.

    Each call gets the env and arguments card.yml gives its step, and GITHUB_EVENT_NAME as GitHub sets it. Returns
    the (env, argv) of every call."""
    calls = card_steps(ctx)
    for env, argv in calls:
        for k in ("ISSUE_NUMBER", "PR_NUMBER", "HEAD_SHA", "RUN_TITLE", "HEAD_BRANCH", "HEAD_REF"):
            monkeypatch.delenv(k, raising=False)
        for k, v in env.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("GITHUB_EVENT_NAME", ctx["github"]["event_name"])
        monkeypatch.setattr(sys, "argv", argv)
        try:
            card.main()
        except SystemExit as e:
            assert not e.code, f"card.py {' '.join(argv[1:])} failed (exit {e.code}) on a {ctx['github']['event_name']} event"
    return calls


def shows_merged_and_done(text):
    """True when a card shows Merged and its whole Definition of Done passed."""
    passed = card.icon(REPO, "passed", alt="passed")
    row = next((l for l in text.splitlines() if l.startswith("**Definition of Done:**")), "")
    return (f"{card.field_icon(REPO, 'merged')} **Merged**" in text and row.count(passed) == 3
            and "not started" not in row and "running" not in row)


# ---------------------------------------------------------------- the tests

def test_a_check_finishing_after_the_merge_still_writes_the_pr_card(record_property, monkeypatch, tmp_path):
    """A check finishing after the merge still writes the merged PR's card and its issue's.

    Proves 322.1.

    Replays #246: the full suite finishes on the PR's head after a squash merge, so GitHub's event names no PR and
    GitHub lists no open PR for that commit. The card run must still draw issue #40 with its merged PR #5 and write the
    PR's description. An open PR's check still draws its own PR, and a commit with no PR draws nothing."""
    record_property("proves", "322.1")
    gh, drawn, saved = world(monkeypatch, tmp_path)
    assert starts(check_finished("abc", "try/issue-40", [])), "322.1: the card job is skipped when a check finishes"
    run_card(monkeypatch, check_finished("abc", "try/issue-40", []))
    assert drawn == [(40, 5)], (f"322.1: a check finishing after PR #5 merged drew {drawn or 'nothing'}, "
                                "not issue #40 with its merged PR #5")
    assert 5 in gh.pr_bodies, "322.1: the merged PR #5's card was not written"
    assert shows_merged_and_done(gh.pr_bodies[5]), "322.1: the merged PR's card does not show Merged with every check passed"
    assert 40 in saved, "322.1: the issue's card was not written"

    drawn.clear()
    gh.pr_bodies.clear()
    run_card(monkeypatch, check_finished("def", "try/issue-41", [{"number": 6, "head": {"sha": "def"}}]))
    assert drawn == [(41, 6)], f"322.1: a check on open PR #6 drew {drawn or 'nothing'}, not issue #41 with PR #6"

    drawn.clear()
    gh.pr_bodies.clear()
    run_card(monkeypatch, check_finished("zzz", "main", []))
    assert drawn == [], f"322.1: a check on a commit with no PR drew {drawn}; it should draw nothing"
    assert not gh.pr_bodies, "322.1: a check on a commit with no PR wrote a PR's card"


def test_merging_a_pr_redraws_its_card_and_its_issues_card(record_property, monkeypatch, tmp_path):
    """Merging a PR redraws its card and its issue's as Merged and Done.

    Proves 322.2.

    Sends card.yml GitHub's event for PR #5 merging (by autopilot's bot, then by the owner), checks the card job runs
    for it, then runs card.py with the env card.yml gives: the PR's description and the issue's card both show Merged,
    with All tests, Code review and Owner approval passed."""
    record_property("proves", "322.2")
    types = trigger_types("pull_request_target")
    assert types is not None and "closed" in types, \
        f"322.2: card.yml does not start on a PR closing (pull_request_target types: {types})"
    for sender in ("Bot", "User"):
        gh, drawn, saved = world(monkeypatch, tmp_path)
        ctx = merged_pr(MERGED, sender)
        assert starts(ctx), f"322.2: the card job is skipped when a PR is merged by a {sender}"
        run_card(monkeypatch, ctx)
        assert drawn == [(40, 5)], f"322.2: merging PR #5 drew {drawn or 'nothing'}, not issue #40 with PR #5"
        assert 5 in gh.pr_bodies, "322.2: merging PR #5 did not write its card"
        assert shows_merged_and_done(gh.pr_bodies[5]), "322.2: the PR card after merge does not show Merged and Done"
        assert 40 in saved and shows_merged_and_done(saved[40]), \
            "322.2: the issue card after merge does not show Merged and Done"


def test_the_merges_card_run_always_has_the_last_word(record_property, monkeypatch, tmp_path):
    """The merge's card run waits for its PR's earlier runs; no other issue's drops it.

    Proves 322.3.

    Works out card.yml's concurrency group for four events: the merge of PR #5, a check finishing late on PR #5's
    branch, a check on another issue's PR and an edit of another issue. The merge and the late check share a group,
    so they run one after the other and never overlap; the other two are in other groups, so they can never replace
    the merge's waiting run; and a newer run never cancels one already going."""
    record_property("proves", "322.3")
    merge, _ = group(merged_pr(MERGED))
    late, _ = group(check_finished("abc", "try/issue-40", []))
    other_check, _ = group(check_finished("def", "try/issue-41", [{"number": 6}]))
    other_issue, cancel = group(issue_edited(9))
    assert merge and merge == late, (f"322.3: the merge's card run (group {merge!r}) and a late check's on the same PR "
                                     f"(group {late!r}) can overlap, so an older drawing can land after the merge")
    assert other_check != merge and other_issue != merge, \
        f"322.3: card runs for other issues share the merge's group {merge!r}, so they can drop its waiting run"
    assert cancel.lower() == "false", "322.3: a newer card run cancels one already going"


STALE = "**Work** · All tests running · Code review not started · Owner approval not started"
CHANGED = (".github/workflows/card.yml", "dokima/card.py")


def test_landing_this_change_redraws_246_and_312_by_itself(record_property, monkeypatch, tmp_path):
    """Landing this change redraws #246 and #312 as Merged and Done, with no click.

    Proves 322.4.

    Fakes GitHub with merged PRs #246 and #312 whose cards still say All tests is running, as they do today, and this
    change's own PR #330 merging. Sends card.yml the two events GitHub sends when that PR merges: the PR closing as
    merged, and the push of its commit (changing card.yml and card.py) to main. Runs every card.py call the card job
    makes for them, as GitHub would, and checks both PRs' cards and their issues' cards were written showing Merged
    with All tests, Code review and Owner approval passed. Nothing is run by hand: no Run workflow event is sent."""
    record_property("proves", "322.4")
    stale = [pr(246, 240, state="closed", merged=True, sha="s246", merge_commit="m246", card_text=STALE),
             pr(312, 280, state="closed", merged=True, sha="s312", merge_commit="m312", card_text=STALE)]
    this = pr(330, 322, state="closed", merged=True, sha="s330", merge_commit="m9")
    gh, drawn, saved = world(monkeypatch, tmp_path, prs=(*stale, this))
    for ctx, files in ((merged_pr(this), ()), (pushed_to_main(CHANGED), CHANGED)):
        if starts(ctx, files):
            run_card(monkeypatch, ctx)
    for number, issue in ((246, 240), (312, 280)):
        assert number in gh.pr_bodies, \
            f"322.4: PR #{number}'s stale card was not redrawn when this change landed on main (drew {drawn or 'nothing'})"
        assert shows_merged_and_done(gh.pr_bodies[number]), \
            f"322.4: PR #{number}'s redrawn card does not show Merged with every Definition of Done item passed"
        assert issue in saved, f"322.4: issue #{issue}'s card (PR #{number}'s issue) was not redrawn"
        assert shows_merged_and_done(saved[issue]), \
            f"322.4: issue #{issue}'s redrawn card does not show Merged with every Definition of Done item passed"


def test_the_merges_card_run_uses_mains_code(record_property):
    """The card run a merge starts uses main's card code, never the PR's.

    Proves 322.5.

    Reads card.yml: a PR event reaches it only as pull_request_target (which runs main's copy), never as pull_request,
    and its checkout names no PR ref or sha."""
    record_property("proves", "322.5")
    assert trigger_types("pull_request_target") is not None, "322.5: card.yml has no pull_request_target trigger"
    assert trigger_types("pull_request") is None, \
        "322.5: card.yml starts on pull_request, which runs the PR's own copy of the card"
    text = workflow()
    refs = re.findall(r"^\s+ref:\s*(.+)$", text, re.M)
    assert not [r for r in refs if "pull_request" in r or "head" in r], \
        f"322.5: card.yml checks out the PR's code ({refs}), so the work could change how it is reported"
