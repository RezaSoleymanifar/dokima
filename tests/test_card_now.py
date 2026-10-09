"""Every issue card and PR card is drawn from GitHub's state right now (#332).

Story 2 of #330. A card used to trust the one event that started its run: card.yml never ran when a pull request was
merged, closed or reviewed, so #246's PR card kept its open card after the merge, and #312's PR card missed a dropped
redraw for good. Now any event about an issue or its pull request, and a sweep every 15 minutes, redraws both cards from
GitHub as it is, each issue in its own queue.

These tests play card.yml the way GitHub runs it, for one event at a time, against a fake GitHub:
- The event starts the workflow when card.yml's `on:` lists it (and its activity type, and for workflow_run the
  workflow that finished). Then every job runs in the order its `needs` allow: a job's `if:` and every `${{ }}` are
  evaluated with tests/test_start.py's evaluator (github, vars, secrets, needs, steps, env); `uses:` steps are skipped
  (checkout is noted with the ref it would check out, and the app token step gives a fake token); `run:` steps run with
  bash, from a copy of this repo's dokima/ and .github/, with a fake `gh` first on PATH. Values a step writes to
  GITHUB_OUTPUT or GITHUB_ENV are read as KEY=value lines, and a job's `outputs:` reach later jobs through `needs`.
- Every concurrency group card.yml declares (the workflow's and each job's that runs) is evaluated for the event.
- Pull request events reach card.yml as pull_request_target (main's copy of the workflow), pull_request_review and
  pull_request_review_comment; on a review GitHub's own ref is the pull request's merge ref.

The fake GitHub (repo o/r, code owner `boss` through CODEOWNERS, Dokima's bot `dokima-runtime`) keeps its state in one
JSON file and answers: `gh issue view|edit|comment|list`, `gh pr view|edit|list`, and `gh api` for
repos/o/r/issues[?state=..] (pull requests included, as GitHub lists them), issues/N (GET, PATCH body), issues/N/
comments|events|timeline|sub_issues, issues/N/dependencies/blocked_by|blocking, pulls[?head=..&state=..], pulls/P (GET,
PATCH body), pulls/P/reviews|comments|files, commits/SHA/check-runs|pulls|status|check-suites, contents (only
.github/CODEOWNERS exists), actions/workflows/X/runs, and the GraphQL issue and closing-issue queries of dokima/plan.py.
`--paginate` prints one page; `--json` keeps only the fields asked for; `-q/--jq` takes a plain path like
`.[0].number`. It can be told to refuse reading an issue,
or writing an issue's or a pull request's body, the way GitHub refuses (HTTP 502 on stderr, exit 1). Any other call
fails as an unknown GitHub path does.

The two pull requests the owner named are the fixtures: issue #246 with PR #260 from try/issue-246, and issue #312
with PR #314 from try/issue-312. Each issue has a plan, its approval, a build and an approving code review.
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from test_start import Ctx, Nil, condition, evaluate, fill, github_shell, load_yaml  # noqa: E402
from dokima import agent, body  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARD_YML = os.path.join(ROOT, ".github", "workflows", "card.yml")
CARD_PY = os.path.join(ROOT, "dokima", "card.py")
OWNER = "boss"
BOT = agent.BOT
# dokima/card.py's length on main when this story was planned; the owner asked for the card code to get smaller.
CARD_PY_LINES_BEFORE = 721
STAGES = ("Backlog", "Plan", "Work", "Review", "Merged")

FAKE_GH = r'''
import json, os, re, sys
D = os.environ["FAKE_GH_DIR"]
STATE = os.path.join(D, "state.json")
S = json.load(open(STATE))
a = sys.argv[1:]
open(os.path.join(D, "calls.jsonl"), "a").write(json.dumps(a) + "\n")
REPO = "o/r"
WITH_VALUE = {"-X", "--method", "-f", "-F", "--raw-field", "--field", "-H", "--header", "--input", "-q", "--jq",
              "-R", "--repo", "--json", "--body", "--body-file", "--head", "--state", "--title", "--label", "-t",
              "--template", "--limit", "-L", "--search", "--base", "--reason", "--comment"}


def save():
    json.dump(S, open(STATE, "w"), indent=1)


def flag(*names):
    for i, x in enumerate(a):
        if x in names and i + 1 < len(a):
            return a[i + 1]
    return None


def fields():
    out = {}
    for i, x in enumerate(a):
        if x in ("-f", "-F", "--raw-field", "--field") and i + 1 < len(a):
            k, _, v = a[i + 1].partition("=")
            if x in ("-F", "--field") and v.startswith("@"):
                v = sys.stdin.read() if v == "@-" else open(v[1:]).read()
            out[k] = v
        if x == "--input" and i + 1 < len(a):
            out.update(json.load(sys.stdin if a[i + 1] == "-" else open(a[i + 1])))
    return out


def positional():
    out, skip = [], False
    for x in a[1:]:
        if skip:
            skip = False
            continue
        if x in WITH_VALUE:
            skip = True
            continue
        if x.startswith("-"):
            continue
        out.append(x)
    return out


def fail(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def refuse(op, n):
    for r in S.get("refuse", []):
        if r["op"] == op and int(r["n"]) == int(n):
            fail(r.get("error") or f"HTTP 502: Server Error (https://api.github.com/repos/{REPO}/issues/{n})")


def tick():
    S["clock"] = S.get("clock", 0) + 1
    return "2026-10-09T%02d:%02d:00Z" % (12 + S["clock"] // 60, S["clock"] % 60)


def write(op, n):
    S.setdefault("writes", []).append({"op": op, "n": int(n)})


def jq(value, q):
    if q in (".", None):
        return value
    for part in re.findall(r"\.\w+|\[\d*\]", q):
        if part == "[]":
            continue
        try:
            value = value[int(part[1:-1])] if part.startswith("[") else (
                [v.get(part[1:]) for v in value] if isinstance(value, list) else value[part[1:]])
        except (KeyError, IndexError, TypeError, ValueError):
            return None
    return value


def only(value):
    """Keep only the fields `--json` asked for, as gh does."""
    want = flag("--json")
    if not want or a[:1] == ["api"]:
        return value
    keep = [k.strip() for k in want.split(",")]
    pick = lambda d: {k: d.get(k) for k in keep} if isinstance(d, dict) else d
    return [pick(v) for v in value] if isinstance(value, list) else pick(value)


def out(value):
    value = only(value)
    q = flag("-q", "--jq")
    if q:
        value = jq(value, q)
        if isinstance(value, list) and ".[]" in q:
            print("\n".join("" if v is None else v if isinstance(v, str) else json.dumps(v) for v in value))
            return
        print("" if value is None else value if isinstance(value, (str, int)) else json.dumps(value))
    else:
        print(value if isinstance(value, str) else json.dumps(value))


def number(x):
    return int(str(x).rstrip("/").rsplit("/", 1)[-1].lstrip("#"))


def issue(n):
    i = S["issues"].get(str(n))
    if i is None:
        fail(f"GraphQL: Could not resolve to an issue with the number of {n}. (repository.issue)")
    return i


def pr(p):
    x = S["prs"].get(str(p))
    if x is None:
        fail(f"HTTP 404: Not Found (https://api.github.com/repos/{REPO}/pulls/{p})")
    return x


def pr_state(x):
    return "closed" if x["merged"] or x["state"] == "closed" else "open"


def issue_rest(n):
    if str(n) in S["prs"]:
        x = S["prs"][str(n)]
        return {"number": int(n), "id": 800000 + int(n), "node_id": f"PR_{n}", "title": x["title"], "body": x["body"],
                "state": pr_state(x), "labels": [], "user": {"login": BOT_LOGIN, "type": "Bot"},
                "updated_at": x["updated_at"], "closed_at": x.get("closed_at"), "comments": len(x.get("comments", [])),
                "html_url": f"https://github.com/{REPO}/pull/{n}",
                "pull_request": {"url": f"https://api.github.com/repos/{REPO}/pulls/{n}",
                                 "merged_at": x.get("merged_at")}}
    i = issue(n)
    return {"number": int(n), "id": 900000 + int(n), "node_id": f"I_{n}", "title": i["title"], "body": i["body"],
            "state": i["state"], "labels": [{"name": l} for l in i.get("labels", [])],
            "user": {"login": OWNER_LOGIN, "type": "User"}, "updated_at": i["updated_at"],
            "comments": len(i.get("comments", [])),
            "closed_at": i.get("closed_at"), "html_url": f"https://github.com/{REPO}/issues/{n}"}


def comments_rest(cs):
    return [{"id": k + 1, "user": {"login": c["login"], "type": "Bot" if c["login"] == BOT_LOGIN else "User"},
             "body": c["body"], "created_at": c["at"], "updated_at": c["at"]} for k, c in enumerate(cs)]


def comments_gh(cs):
    return [{"author": {"login": c["login"]}, "body": c["body"], "createdAt": c["at"]} for c in cs]


def pr_rest(p):
    x = pr(p)
    return {"number": int(p), "id": 800000 + int(p), "node_id": f"PR_{p}", "title": x["title"], "body": x["body"],
            "state": pr_state(x), "merged": x["merged"], "merged_at": x.get("merged_at"),
            "merged_by": {"login": x["merged_by"]} if x.get("merged_by") else None, "closed_at": x.get("closed_at"),
            "head": {"ref": x["head_ref"], "sha": x["sha"]}, "base": {"ref": "main"}, "draft": False,
            "user": {"login": BOT_LOGIN, "type": "Bot"}, "updated_at": x["updated_at"],
            "html_url": f"https://github.com/{REPO}/pull/{p}"}


def pr_gh(p):
    x = pr(p)
    return {"number": int(p), "title": x["title"], "body": x["body"],
            "state": "MERGED" if x["merged"] else pr_state(x).upper(), "headRefName": x["head_ref"],
            "headRefOid": x["sha"], "baseRefName": "main", "mergedAt": x.get("merged_at"), "closed": pr_state(x) == "closed",
            "url": f"https://github.com/{REPO}/pull/{p}", "updatedAt": x["updated_at"],
            "comments": comments_gh(x.get("comments", [])),
            "reviews": [{"author": {"login": r["login"]}, "body": r["body"], "state": r["state"], "submittedAt": r["at"]}
                        for r in x.get("reviews", [])],
            "closingIssuesReferences": [{"number": x["closes"]}] if x.get("closes") else []}


def issue_gh(n):
    i = issue(n)
    return {"number": int(n), "title": i["title"], "body": i["body"], "state": i["state"].upper(),
            "comments": comments_gh(i.get("comments", [])), "labels": [{"name": l} for l in i.get("labels", [])],
            "url": f"https://github.com/{REPO}/issues/{n}", "updatedAt": i["updated_at"], "closedAt": i.get("closed_at")}


def prs(head=None, state="open"):
    found = []
    for k in sorted(S["prs"], key=int):
        x = S["prs"][k]
        if head and x["head_ref"] != head.split(":", 1)[-1]:
            continue
        st = pr_state(x)
        if state in ("all", None) or state == st or (state == "merged" and x["merged"]):
            found.append(int(k))
    return found


def text_arg():
    t = flag("--body")
    if t is None:
        p = flag("--body-file", "-F")
        t = sys.stdin.read() if p == "-" else open(p).read()
    return t


def set_issue_body(n, text):
    if str(n) in S["prs"]:
        return set_pr_body(n, text)
    refuse("write-issue", n)
    issue(n)["body"] = text
    issue(n)["updated_at"] = tick()
    write("issue-body", n)
    save()


def set_pr_body(p, text):
    refuse("write-pr", p)
    pr(p)["body"] = text
    pr(p)["updated_at"] = tick()
    write("pr-body", p)
    save()


if a[:2] == ["issue", "view"]:
    n = number(positional()[1])
    refuse("read-issue", n)
    out(issue_gh(n))
    sys.exit(0)
if a[:2] == ["issue", "edit"]:
    set_issue_body(number(positional()[1]), text_arg())
    sys.exit(0)
if a[:2] == ["issue", "comment"]:
    n = number(positional()[1])
    issue(n).setdefault("comments", []).append({"login": BOT_LOGIN, "body": text_arg(), "at": tick()})
    write("comment", n)
    save()
    sys.exit(0)
if a[:2] == ["issue", "list"]:
    st = (flag("--state", "-s") or "open").lower()
    out([issue_gh(int(k)) for k in sorted(S["issues"], key=int) if st == "all" or S["issues"][k]["state"] == st])
    sys.exit(0)
if a[:2] == ["pr", "list"]:
    out([pr_gh(p) for p in prs(flag("--head"), (flag("--state", "-s") or "open").lower())])
    sys.exit(0)
if a[:2] == ["pr", "view"]:
    out(pr_gh(number(positional()[1])))
    sys.exit(0)
if a[:2] == ["pr", "edit"]:
    set_pr_body(number(positional()[1]), text_arg())
    sys.exit(0)
if a[:1] == ["api"]:
    pos = positional()
    path = (pos[0] if pos else "").lstrip("/")
    route, _, query = path.partition("?")
    params = dict(p.partition("=")[::2] for p in query.split("&") if p)
    f = fields()
    method = (flag("-X", "--method") or ("POST" if f and route != "graphql" else "GET")).upper()
    if route == "graphql":
        q = f.get("query", "")
        if "userContentEdits" in q and "issue(" in q:
            n = int(f["i"])
            refuse("read-issue", n)
            i = issue(n)
            out({"data": {"repository": {"issue": {"number": n, "title": i["title"], "body": i["body"],
                                                   "url": f"https://github.com/{REPO}/issues/{n}",
                                                   "userContentEdits": {"nodes": []}}}}})
            sys.exit(0)
        if "closingIssuesReferences" in q:
            x = pr(int(f["p"]))
            nodes = [{"number": x["closes"]}] if x.get("closes") else []
            out({"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": nodes}}}}})
            sys.exit(0)
        fail(f"fake gh: no such GraphQL query {q[:200]!r}")
    p = f"repos/{REPO}/"
    if not route.startswith(p):
        fail(f"fake gh: no such call {a}")
    r = route[len(p):]
    if r == "issues" and method == "GET":
        st = params.get("state", "open")
        nums = sorted({int(k) for k in S["issues"]} | {int(k) for k in S["prs"]})
        out([issue_rest(n) for n in nums if st == "all" or issue_rest(n)["state"] == st])
        sys.exit(0)
    m = re.fullmatch(r"issues/(\d+)", r)
    if m:
        n = int(m.group(1))
        if method == "PATCH":
            if "body" not in f:
                fail(f"fake gh: no such call {a}")
            set_issue_body(n, f["body"])
        elif str(n) not in S["prs"]:
            refuse("read-issue", n)
        out(issue_rest(n))
        sys.exit(0)
    m = re.fullmatch(r"issues/(\d+)/(comments|events|timeline|sub_issues)", r)
    if m:
        n = int(m.group(1))
        if str(n) not in S["prs"]:
            refuse("read-issue", n)
        holder = S["prs"].get(str(n)) or issue(n)
        if m.group(2) == "comments" and method == "POST":
            holder.setdefault("comments", []).append({"login": BOT_LOGIN, "body": f["body"], "at": tick()})
            write("comment", n)
            save()
            out({"id": 1})
        else:
            out(comments_rest(holder.get("comments", [])) if m.group(2) == "comments" else [])
        sys.exit(0)
    m = re.fullmatch(r"issues/(\d+)/dependencies/(blocked_by|blocking)", r)
    if m and method == "GET":
        issue(int(m.group(1)))
        out([])
        sys.exit(0)
    if r == "pulls" and method == "GET":
        out([pr_rest(n) for n in prs(params.get("head"), params.get("state", "open"))])
        sys.exit(0)
    m = re.fullmatch(r"pulls/(\d+)", r)
    if m:
        n = int(m.group(1))
        if method == "PATCH":
            if "body" not in f:
                fail(f"fake gh: no such call {a}")
            set_pr_body(n, f["body"])
        out(pr_rest(n))
        sys.exit(0)
    m = re.fullmatch(r"pulls/(\d+)/(reviews|comments|files|commits)", r)
    if m and method == "GET":
        x = pr(int(m.group(1)))
        if m.group(2) == "reviews":
            out([{"id": k + 1, "user": {"login": v["login"]}, "state": v["state"], "body": v["body"],
                  "submitted_at": v["at"], "html_url": f"https://github.com/{REPO}/pull/{m.group(1)}#review-{k + 1}"}
                 for k, v in enumerate(x.get("reviews", []))])
        else:
            out([])
        sys.exit(0)
    m = re.fullmatch(r"commits/([^/]+)/(check-runs|pulls|status|check-suites)", r)
    if m and method == "GET":
        sha, what = m.group(1), m.group(2)
        if what == "check-runs":
            runs = S.get("checks", {}).get(sha, [])
            out({"total_count": len(runs), "check_runs": runs})
        elif what == "pulls":
            out([pr_rest(int(k)) for k, x in sorted(S["prs"].items()) if x["sha"] == sha])
        elif what == "status":
            out({"state": "success", "statuses": []})
        else:
            out({"total_count": 0, "check_suites": []})
        sys.exit(0)
    if r == "contents/.github/CODEOWNERS":
        print("* @" + OWNER_LOGIN)
        sys.exit(0)
    if r.startswith("contents/"):
        fail(f"HTTP 404: Not Found (https://api.github.com/{route})")
    if r.startswith("actions/"):
        out({"total_count": 0, "workflow_runs": []})
        sys.exit(0)
fail(f"fake gh: no such call {a}")
'''


# --- the fake GitHub ---------------------------------------------------------------------------------------------

def record(rec, at):
    """A comment the bot posted holding one agent record."""
    return {"login": BOT, "body": f"{agent.MARK}\n**Record**\n\n```json\n{json.dumps(rec)}\n```\n", "at": at}


def plan_record(n, story):
    """A planner record of issue n that passed its check: one criterion and its test."""
    h = {"kind": "user_story", "summary": f"Issue {n} is planned.", "user_story": story,
         "acceptance_criteria": [{"text": f"Criterion one of #{n}.", "source": f"https://github.com/o/r/issues/{n}"}],
         "non_functional": [], "scope": ["dokima/x.py"], "out_of_scope": ["Nothing else."],
         "tests": {f"{n}.1": ["tests/test_x.py::test_one"]}, "test_changes": {},
         "links": {"blocked_by": [], "blocks": [], "relates_to": []}}
    return {"role": "planner", "stage": None, "handback": h, "check": {"passed": True, "problems": []},
            "run": "https://github.com/o/r/actions/runs/1", "run_id": "1"}


def review_record(stage):
    """An approving review record at `stage` (plan or pr) that passed its check."""
    return {"role": "reviewer", "stage": stage, "handback": {"verdict": "approve", "summary": "Approved.",
                                                             "blockers": [], "resolved": []},
            "check": {"passed": True, "problems": []}, "run": "https://github.com/o/r/actions/runs/2", "run_id": "2"}


def worker_record():
    """A worker record that passed its check."""
    return {"role": "worker", "stage": None, "handback": {"summary": "Built it.", "changed": ["dokima/x.py"]},
            "check": {"passed": True, "problems": []}, "run": "https://github.com/o/r/actions/runs/3", "run_id": "3"}


def card_of(text):
    """The card block in a body, between its two marks; None when there is none."""
    m = re.search(r"<!-- dokima-card -->.*?<!-- /dokima-card -->", text or "", re.S)
    return m.group(0) if m else None


def stage_of(text):
    """The stage a card's status line shows (Backlog, Plan, Work, Review or Merged), or None."""
    for line in (card_of(text) or "").splitlines():
        m = re.search(r"\*\*(" + "|".join(STAGES) + r")\*\*", line)
        if m and "Definition of Done" not in line:
            return m.group(1)
    return None


def done_of(text):
    """The Definition of Done a card shows: {All tests, Code review, Owner approval: passed/failed/...}."""
    line = next((l for l in (card_of(text) or "").splitlines() if l.startswith("**Definition of Done:**")), "")
    found = {}
    for part in line.split(" · "):
        alt = re.search(r'alt="([^"]+)"', part)
        for name in ("All tests", "Code review", "Owner approval"):
            if part.rstrip().endswith(name) and alt:
                found[name] = alt.group(1)
    return found


STALE_CARD = "<!-- dokima-card -->\n**Review**\n\nAn old card, drawn before the last event.\n\n<!-- /dokima-card -->"


class Hub:
    """A fake GitHub holding issues #246 and #312 and their PRs #260 and #314."""

    def __init__(self, tmp):
        self.dir = str(tmp)
        os.makedirs(os.path.join(self.dir, "bin"))
        gh = os.path.join(self.dir, "bin", "gh")
        open(gh, "w").write(f"#!{sys.executable}\nBOT_LOGIN = {BOT!r}\nOWNER_LOGIN = {OWNER!r}\n" + FAKE_GH)
        os.chmod(gh, 0o755)
        self.ws = os.path.join(self.dir, "ws")
        shutil.copytree(os.path.join(ROOT, "dokima"), os.path.join(self.ws, "dokima"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(os.path.join(ROOT, ".github"), os.path.join(self.ws, ".github"))
        self.state = {"issues": {}, "prs": {}, "checks": {}, "refuse": [], "writes": [], "clock": 0}
        for n, p in ((246, 260), (312, 314)):
            self.add_issue(n, p)
        self.save()
        self.log = ""

    def add_issue(self, n, p=None, records=True):
        """Add open issue n with a stale card and, given p, its open PR."""
        ask = f"Issue {n}: the owner's own words, kept as written."
        recs = [plan_record(n, f"The owner sees issue {n} done."), review_record("plan")]
        if p:
            recs += [worker_record(), review_record("pr")]
        self.state["issues"][str(n)] = {
            "title": f"Issue {n}", "state": "open", "labels": [], "updated_at": "2026-10-09T01:00:00Z",
            "body": f"{STALE_CARD}\n\n{body.MARKER}\n\n{ask}",
            "comments": [record(r, f"2026-10-09T0{k + 1}:00:00Z") for k, r in enumerate(recs)] if records else []}
        if p:
            sha = f"sha{p}"
            self.state["prs"][str(p)] = {
                "title": f"Issue {n}", "state": "open", "merged": False, "merged_by": None, "head_ref": f"try/issue-{n}",
                "sha": sha, "closes": n, "body": f"{STALE_CARD}\n\nCloses #{n}", "comments": [], "reviews": [],
                "updated_at": "2026-10-09T01:00:00Z"}
            self.state["checks"][sha] = [
                {"name": f"{n}.1 · Criterion one", "status": "completed", "conclusion": "success", "head_sha": sha,
                 "html_url": f"https://github.com/o/r/runs/{p}1"},
                {"name": "all tests", "status": "completed", "conclusion": "success", "head_sha": sha,
                 "html_url": f"https://github.com/o/r/runs/{p}2"}]

    def save(self):
        """Write the fake GitHub's state to its file."""
        json.dump(self.state, open(os.path.join(self.dir, "state.json"), "w"), indent=1)

    def load(self):
        """Read the fake GitHub's state back, as the run left it."""
        self.state = json.load(open(os.path.join(self.dir, "state.json")))
        return self.state

    def merge(self, n, p, by=OWNER):
        """Merge PR p and close issue n on GitHub, redrawing no card."""
        s = self.load()
        s["prs"][str(p)].update(state="closed", merged=True, merged_by=by, merged_at="2026-10-09T09:00:00Z",
                                closed_at="2026-10-09T09:00:00Z", updated_at="2026-10-09T09:00:00Z")
        s["issues"][str(n)].update(state="closed", closed_at="2026-10-09T09:00:00Z", updated_at="2026-10-09T09:00:00Z")
        self.save()

    def no_pr_card(self, p, n):
        """Leave PR p with only its closing line, as after a dropped redraw."""
        s = self.load()
        s["prs"][str(p)]["body"] = f"Closes #{n}"
        self.save()

    def refuse(self, op, n):
        """GitHub refuses `op` (read-issue, write-issue or write-pr) on n with HTTP 502."""
        s = self.load()
        s["refuse"].append({"op": op, "n": n, "error": f"HTTP 502: Server Error (https://api.github.com/repos/o/r/{n})"})
        self.save()

    def issue_body(self, n):
        """Issue n's body as it stands on GitHub."""
        return self.load()["issues"][str(n)]["body"]

    def pr_body(self, p):
        """PR p's body as it stands on GitHub."""
        return self.load()["prs"][str(p)]["body"]

    def writes(self, op=None):
        """Every body or comment the run wrote, of one kind when given."""
        return [w for w in self.load()["writes"] if op is None or w["op"] == op]

    def clear_writes(self):
        """Forget the writes so far."""
        s = self.load()
        s["writes"] = []
        self.save()

    def run(self, event_name, event, k):
        """Play card.yml for one event and return the Run."""
        r = Run(self, event_name, event)
        self.log = r.log
        return r


# --- the events GitHub sends -------------------------------------------------------------------------------------

REPOSITORY = {"full_name": "o/r", "name": "r", "owner": {"login": "o"}, "default_branch": "main"}


def sender(who):
    """The sender of an event: the owner, or Dokima's bot."""
    return {"login": BOT + "[bot]", "type": "Bot"} if who == "bot" else {"login": who, "type": "User"}


def issue_event(n, action, who=OWNER):
    """An issues event on issue n."""
    return "issues", {"action": action, "issue": {"number": n, "title": f"Issue {n}", "state": "open"},
                      "sender": sender(who), "repository": REPOSITORY}


def issue_comment(n, who=OWNER, action="created", text="A thought."):
    """A comment on issue n."""
    return "issue_comment", {"action": action, "issue": {"number": n, "title": f"Issue {n}"},
                             "comment": {"body": text, "user": {"login": sender(who)["login"]}},
                             "sender": sender(who), "repository": REPOSITORY}


def pr_payload(n, p, merged=False, state="open"):
    """The pull_request object GitHub puts in a pull request event."""
    return {"number": p, "title": f"Issue {n}", "state": state, "merged": merged, "body": f"Closes #{n}",
            "head": {"ref": f"try/issue-{n}", "sha": f"sha{p}"}, "base": {"ref": "main"},
            "user": {"login": BOT + "[bot]", "type": "Bot"}, "html_url": f"https://github.com/o/r/pull/{p}"}


def pr_comment(n, p, who=OWNER, action="created", text="A thought."):
    """A comment on PR p, which GitHub sends as an issue_comment."""
    return "issue_comment", {"action": action, "issue": {"number": p, "title": f"Issue {n}",
                                                         "pull_request": {"url": f"https://api.github.com/repos/o/r/pulls/{p}"}},
                             "comment": {"body": text, "user": {"login": sender(who)["login"]}},
                             "sender": sender(who), "repository": REPOSITORY}


def pr_event(n, p, action, who="bot", merged=False):
    """A pull_request_target event on PR p."""
    state = "closed" if action == "closed" else "open"
    return "pull_request_target", {"action": action, "number": p, "pull_request": pr_payload(n, p, merged, state),
                                   "sender": sender(who), "repository": REPOSITORY}


def review_event(n, p, who=OWNER, action="submitted", state="approved"):
    """A pull_request_review event on PR p."""
    return "pull_request_review", {"action": action, "review": {"state": state, "body": "", "user": {"login": who}},
                                   "pull_request": pr_payload(n, p), "sender": sender(who), "repository": REPOSITORY}


def line_note(n, p, who=OWNER, action="created"):
    """A pull_request_review_comment event (a note on a line) on PR p."""
    return "pull_request_review_comment", {"action": action, "comment": {"body": "Here.", "user": {"login": who}},
                                           "pull_request": pr_payload(n, p), "sender": sender(who),
                                           "repository": REPOSITORY}


def checks_finished(n, p, workflow="done-whens"):
    """A workflow_run event: the checks of PR p finished."""
    run = {"name": workflow, "head_sha": f"sha{p}", "head_branch": f"try/issue-{n}", "display_title": f"Issue {n}",
           "event": "pull_request_target", "status": "completed", "conclusion": "success",
           "pull_requests": [{"number": p, "head": {"ref": f"try/issue-{n}", "sha": f"sha{p}"}, "base": {"ref": "main"}}]}
    return "workflow_run", {"action": "completed", "workflow": {"name": workflow}, "workflow_run": run,
                            "sender": sender("bot"), "repository": REPOSITORY}


def schedule():
    """The 15-minute schedule."""
    return "schedule", {"schedule": "*/15 * * * *"}


# --- playing card.yml --------------------------------------------------------------------------------------------

class Null(Nil):
    """A missing value in an expression: null, and null for anything read from it."""

    def __getattr__(self, k):
        return NIL

    def __getitem__(self, k):
        return NIL


NIL = Null()


class Context(Ctx):
    """An expression context read with dots, where a missing name is null."""

    def __getattr__(self, k):
        v = self.get(k, NIL)
        return Context(v) if isinstance(v, dict) and not isinstance(v, Ctx) else v

    def __getitem__(self, k):
        return self.__getattr__(k)


class List(list):
    """A list in an expression, where an index past its end is null."""

    def __getitem__(self, i):
        try:
            return wrap(list.__getitem__(self, i))
        except (IndexError, TypeError):
            return NIL


def wrap(v):
    """A JSON value turned into an expression context."""
    if isinstance(v, dict) and not isinstance(v, Ctx):
        return Context({k: wrap(x) for k, x in v.items()})
    if isinstance(v, list) and not isinstance(v, List):
        return List(wrap(x) for x in v)
    return v


def github_ctx(event_name, event):
    """The `github` context GitHub gives card.yml for one event."""
    ref = "refs/heads/main"
    if event_name in ("pull_request", "pull_request_review", "pull_request_review_comment"):
        ref = f"refs/pull/{event['pull_request']['number']}/merge"
    return wrap({"event_name": event_name, "event": event, "repository": "o/r", "repository_owner": "o", "ref": ref,
                 "sha": "mainsha", "run_id": "42", "run_number": "7", "server_url": "https://github.com",
                 "actor": (event.get("sender") or {}).get("login", "github"), "workflow": "card",
                 "token": "fake-workflow-token"})


def workflow():
    """card.yml, read."""
    return load_yaml(open(CARD_YML).read())


def triggers(wf):
    """card.yml's `on:` as {event name: its settings or ''}."""
    on = wf.get("on")
    if isinstance(on, str):
        return {on: ""}
    if isinstance(on, list):
        return {e: "" for e in on}
    return on or {}


def listed(value):
    """A YAML value that may be one string or a list, as a list."""
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def starts(wf, event_name, event):
    """True when card.yml's `on:` starts a run for this event."""
    on = triggers(wf)
    if event_name not in on:
        return False
    t = on[event_name] if isinstance(on[event_name], dict) else {}
    types = listed(t.get("types"))
    if types and event.get("action") not in types:
        return False
    if event_name == "workflow_run" and event["workflow"]["name"] not in listed(t.get("workflows")):
        return False
    return True


def group_of(conc, ctx, status):
    """The concurrency group a `concurrency:` setting gives, filled in; None when there is none."""
    if not conc:
        return None
    g = conc.get("group") if isinstance(conc, dict) else conc
    return fill(g, ctx, status) if g else None


def order(jobs):
    """Job names in an order their `needs` allow."""
    done, out = set(), []
    while len(out) < len(jobs):
        ready = [j for j in jobs if j not in done and set(listed(jobs[j].get("needs"))) <= done]
        assert ready, "test setup: card.yml's jobs need each other in a loop"
        for j in ready:
            done.add(j)
            out.append(j)
    return out


class Run:
    """One run of card.yml for one event, played as GitHub plays it."""

    def __init__(self, hub, event_name, event):
        self.hub, self.event_name, self.event = hub, event_name, event
        wf = workflow()
        self.wf = wf
        self.started = starts(wf, event_name, event)
        self.jobs, self.log, self.checkouts = {}, "", []
        self.groups = {}
        if not self.started:
            return
        base_ctx = {"github": github_ctx(event_name, event), "vars": Context(), "secrets": Context(), "inputs": Context()}
        self.groups["workflow"] = group_of(wf.get("concurrency"), {**base_ctx, "env": Context()}, {"failed": False})
        wf_env = {k: fill(v, {**base_ctx, "env": Context()}, {"failed": False}) for k, v in (wf.get("env") or {}).items()}
        open(os.path.join(hub.dir, "event.json"), "w").write(json.dumps(event))
        jobs = wf.get("jobs") or {}
        for name in order(jobs):
            job = jobs[name]
            assert "strategy" not in job, "test setup: this player cannot run a job with a matrix"
            needs = {j: self.jobs[j] for j in listed(job.get("needs"))}
            ctx = {**base_ctx, "needs": wrap({j: {"result": v["result"], "outputs": v["outputs"]} for j, v in needs.items()}),
                   "env": Context(wf_env)}
            status = {"failed": any(v["result"] == "failure" for v in needs.values()),
                      "cancelled": False}
            cond = condition(job.get("if"))
            skipped_need = any(v["result"] == "skipped" for v in needs.values())
            if (skipped_need and "always()" not in cond) or not evaluate(cond, ctx, status):
                self.jobs[name] = {"result": "skipped", "outputs": {}, "ran_card": False, "wrote": False}
                continue
            self.groups[name] = group_of(job.get("concurrency"), ctx, status)
            self.jobs[name] = self.run_job(name, job, ctx, wf_env)

    def run_job(self, name, job, ctx, wf_env):
        """Run one job's steps in order; returns its result, outputs and whether it ran dokima/card.py."""
        hub, status, steps, added = self.hub, {"failed": False}, {}, {}
        job_env = {k: fill(v, {**ctx, "env": Context(wf_env)}, status) for k, v in (job.get("env") or {}).items()}
        base = {"PATH": os.path.join(hub.dir, "bin") + os.pathsep + os.environ["PATH"], "HOME": os.environ.get("HOME", hub.dir),
                "FAKE_GH_DIR": hub.dir, "GITHUB_EVENT_NAME": self.event_name, "GITHUB_REPOSITORY": "o/r",
                "GITHUB_REPOSITORY_OWNER": "o", "GITHUB_RUN_ID": "42", "GITHUB_SERVER_URL": "https://github.com",
                "GITHUB_EVENT_PATH": os.path.join(hub.dir, "event.json"), "GITHUB_WORKSPACE": hub.ws,
                "GITHUB_STEP_SUMMARY": os.path.join(hub.dir, "summary.md"), "RUNNER_TEMP": hub.dir,
                "GITHUB_REF": str(ctx["github"].ref), "CI": "true", "GITHUB_ACTIONS": "true"}
        ran_card, writes = False, len(hub.writes())
        for step in job.get("steps") or []:
            sctx = {**ctx, "steps": wrap(steps), "env": Context({**wf_env, **job_env, **added}),
                    "job": Context(status="failure" if status["failed"] else "success")}
            if not evaluate(condition(step.get("if")), sctx, status):
                continue
            outputs = {}
            uses = str(step.get("uses") or "")
            if "run" in step:
                env = {**base, **wf_env, **job_env, **added}
                env.update({k: fill(v, sctx, status) for k, v in (step.get("env") or {}).items()})
                env["GITHUB_ENV"], env["GITHUB_OUTPUT"] = os.path.join(hub.dir, "step-env"), os.path.join(hub.dir, "step-out")
                for f in (env["GITHUB_ENV"], env["GITHUB_OUTPUT"]):
                    open(f, "w").close()
                script = fill(step["run"], sctx, status)
                ran_card = ran_card or "dokima/card.py" in script or "dokima.card" in script
                open(os.path.join(hub.dir, "step.sh"), "w").write(script)
                p = subprocess.run(github_shell(step, job, self.wf.get("defaults")) + [os.path.join(hub.dir, "step.sh")],
                                   cwd=hub.ws, env=env, capture_output=True, text=True, timeout=300)
                self.log += f"## {name}: {step.get('name') or 'run'} (exit {p.returncode})\n{p.stdout}{p.stderr}\n"
                for path, into in ((env["GITHUB_ENV"], added), (env["GITHUB_OUTPUT"], outputs)):
                    for line in open(path).read().splitlines():
                        if "=" in line:
                            k, v = line.split("=", 1)
                            into[k] = v
                if p.returncode != 0:
                    status["failed"] = True
            elif "actions/checkout" in uses:
                ref = fill((step.get("with") or {}).get("ref") or "", sctx, status) or str(ctx["github"].ref)
                self.checkouts.append(ref)
            elif "create-github-app-token" in uses:
                outputs = {"token": "fake-token", "app-slug": "dokima-runtime"}
            if step.get("id"):
                steps[step["id"]] = {"outputs": outputs, "outcome": "failure" if status["failed"] else "success",
                                     "conclusion": "failure" if status["failed"] else "success"}
        outs = {k: fill(v, {**ctx, "steps": wrap(steps), "env": Context({**wf_env, **job_env, **added})}, status)
                for k, v in (job.get("outputs") or {}).items()}
        wrote = any(w["op"] in ("issue-body", "pr-body") for w in hub.writes()[writes:])
        return {"result": "failure" if status["failed"] else "success", "outputs": outs, "ran_card": ran_card,
                "wrote": wrote}

    def card_ran(self):
        """True when a job that runs dokima/card.py ran for this event."""
        return any(j["ran_card"] for j in self.jobs.values())

    def failed(self):
        """True when any job of the run failed."""
        return any(j["result"] == "failure" for j in self.jobs.values())

    def card_groups(self):
        """The queue each job that wrote a card waited in."""
        return {self.groups.get(name) or self.groups.get("workflow") for name, j in self.jobs.items() if j["wrote"]}

    def all_groups(self):
        """Every concurrency group this run took a place in, the workflow's and each job's."""
        return {g for g in self.groups.values() if g}

    def errors(self):
        """The ::error lines the run printed, where GitHub names what failed."""
        return [l for l in self.log.splitlines() if l.startswith("::error")]


def must_redraw(hub, event, k):
    """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
    r = hub.run(*event, k)
    what = f"{event[0]} {event[1].get('action') or ''}".strip()
    assert r.started, f"{k}: card.yml does not start on {what}, so the cards are not redrawn"
    assert r.card_ran(), f"{k}: card.yml started on {what} but its card job was skipped"
    assert not r.failed(), f"{k}: card.yml's run on {what} failed:\n{r.log[-3000:]}"
    return r


# 332.1 -----------------------------------------------------------------------------------------------------------

MERGE_EVENTS = [
    ("the merge, by the bot on autopilot", lambda: pr_event(246, 260, "closed", "bot", merged=True)),
    ("the merge, by the owner", lambda: pr_event(246, 260, "closed", OWNER, merged=True)),
    ("the issue closing", lambda: issue_event(246, "closed")),
    ("a comment on the issue", lambda: issue_comment(246)),
    ("a comment on the pull request", lambda: pr_comment(246, 260)),
    ("an Approve review", lambda: review_event(246, 260)),
    ("a review by the bot's reviewer", lambda: review_event(246, 260, who="bot", state="commented")),
    ("a note on a line", lambda: line_note(246, 260)),
    ("the checks finishing", lambda: checks_finished(246, 260)),
]


def test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now(tmp_path, record_property):
    """Any event about an issue or its PR redraws both cards as GitHub is now.

    PR #260 is merged and #246 closed on GitHub while both cards still show the old Review card. For each of nine
    events (the merge by the bot or the owner, the issue closing, a comment on the issue or the PR, an Approve, the
    bot's review, a note on a line, the checks finishing), on a fresh GitHub, card.yml runs and afterwards #246's card
    and #260's card are the same card, saying Merged, and the PR keeps its closing line. Proves 332.1."""
    record_property("proves", "332.1")
    for what, make in MERGE_EVENTS:
        hub = Hub(tmp_path / re.sub(r"\W+", "-", what))
        hub.merge(246, 260)
        must_redraw(hub, make(), "332.1")
        issue_card, pr_card = card_of(hub.issue_body(246)), card_of(hub.pr_body(260))
        assert stage_of(hub.issue_body(246)) == "Merged", \
            f"332.1: after {what}, #246's card does not say Merged, as GitHub is now: {issue_card!r}"
        assert stage_of(hub.pr_body(260)) == "Merged", \
            f"332.1: after {what}, PR #260's card does not say Merged, as GitHub is now: {pr_card!r}"
        assert issue_card == pr_card, f"332.1: after {what}, #246 and PR #260 show different cards"
        assert hub.pr_body(260).rstrip().endswith("Closes #246"), \
            f"332.1: after {what}, PR #260 lost its closing line: {hub.pr_body(260)[-200:]!r}"


def test_an_event_redraws_an_open_issue_and_its_pr_from_the_records_now(tmp_path, record_property):
    """An event redraws an open issue's stale card and its missing PR card.

    #312's card still shows an old card that predates its plan, and PR #314 holds only `Closes #312` (a dropped
    redraw). A person's comment on #312 (and, on a fresh GitHub, a new commit pushed to #314) redraws both: each shows
    #312's plan, the same card, not Merged, and the PR keeps its closing line. An event on another issue leaves #312
    and #314 as they were. Proves 332.1."""
    record_property("proves", "332.1")
    for what, make in (("a comment on the issue", lambda: issue_comment(312)),
                       ("new commits on the pull request", lambda: pr_event(312, 314, "synchronize"))):
        hub = Hub(tmp_path / re.sub(r"\W+", "-", what))
        hub.no_pr_card(314, 312)
        must_redraw(hub, make(), "332.1")
        assert "The owner sees issue 312 done." in (card_of(hub.issue_body(312)) or ""), \
            f"332.1: after {what}, #312's card does not show its plan: {card_of(hub.issue_body(312))!r}"
        assert card_of(hub.pr_body(314)) == card_of(hub.issue_body(312)), \
            f"332.1: after {what}, PR #314 does not show #312's card: {hub.pr_body(314)!r}"
        assert stage_of(hub.pr_body(314)) not in (None, "Merged"), \
            f"332.1: after {what}, PR #314's open card shows {stage_of(hub.pr_body(314))!r}"
        assert hub.pr_body(314).rstrip().endswith("Closes #312"), f"332.1: PR #314 lost its closing line"
    hub = Hub(tmp_path / "other")
    hub.no_pr_card(314, 312)
    before = (hub.issue_body(312), hub.pr_body(314))
    must_redraw(hub, issue_comment(246), "332.1")
    assert (hub.issue_body(312), hub.pr_body(314)) == before, \
        "332.1: a comment on #246 redrew #312 or PR #314, which it is not about"


def stale_again(hub):
    """Put the old card back on every issue and PR."""
    s = hub.load()
    for n, p in ((246, 260), (312, 314)):
        s["issues"][str(n)]["body"] = f"{STALE_CARD}\n\n{body.MARKER}\n\nIssue {n}: the owner's own words."
        s["prs"][str(p)]["body"] = f"{STALE_CARD}\n\nCloses #{n}"
    s["writes"] = []
    hub.save()


def test_records_redraw_the_cards_and_the_cards_own_writes_redraw_nothing(tmp_path, record_property):
    """An agent's record redraws the cards, and the cards' own writes never start another redraw.

    With every card stale before each event: the bot posting a record, or editing its live card into a record, on
    #246 or on PR #260, redraws #246's and #260's cards. The bot editing #246's or #260's text (the card itself), and
    the bot's comments that hold no record, on either, write no card. The bot opening PR #260 draws its card. Proves 332.1."""
    record_property("proves", "332.1")
    hub = Hub(tmp_path)
    rec = record(review_record("pr"), "2026-10-09T08:00:00Z")["body"]
    for what, event in (("the bot posting a record on #246", issue_comment(246, "bot", text=rec)),
                        ("the bot editing its live card into a record on #246", issue_comment(246, "bot", "edited", rec)),
                        ("the bot posting a record on PR #260", pr_comment(246, 260, "bot", text=rec)),
                        ("the bot editing its live card into a record on PR #260", pr_comment(246, 260, "bot", "edited", rec))):
        stale_again(hub)
        must_redraw(hub, event, "332.1")
        assert card_of(hub.issue_body(246)) != STALE_CARD and card_of(hub.pr_body(260)) != STALE_CARD, \
            f"332.1: {what} did not redraw #246's and PR #260's cards"
    for what, event in (("the bot editing #246's text", issue_event(246, "edited", "bot")),
                        ("the bot editing PR #260's text", pr_event(246, 260, "edited", "bot")),
                        ("the bot's comment with no record on #246", issue_comment(246, "bot", text="Autopilot: merged PR #260")),
                        ("the bot's comment with no record on PR #260", pr_comment(246, 260, "bot", text="A live card.")),
                        ("the bot editing a live card on #246", issue_comment(246, "bot", "edited", "<!-- dokima-live -->"))):
        stale_again(hub)
        hub.run(*event, "332.1")
        assert not [w for w in hub.writes() if w["op"] in ("issue-body", "pr-body")], \
            f"332.1: {what} wrote a card, so every card the bot writes could start another run: {hub.writes()}"
    stale_again(hub)
    hub.no_pr_card(260, 246)
    must_redraw(hub, pr_event(246, 260, "opened", "bot"), "332.1")
    assert card_of(hub.pr_body(260)), "332.1: the bot opening PR #260 did not draw its card"


def test_card_yml_starts_on_every_kind_of_event_about_an_issue_or_its_pr(record_property):
    """card.yml starts on every kind of event about an issue or its pull request.

    Reads card.yml's `on:`: issues and issue comments of every kind, pull_request_target opened, edited, reopened,
    synchronize and closed, reviews submitted, edited and dismissed, line notes created, edited and deleted, the checks
    and the worker finishing, and the schedule. Proves 332.1."""
    record_property("proves", "332.1")
    wf = workflow()
    want = [issue_event(246, a) for a in ("opened", "edited", "closed", "reopened", "labeled", "unlabeled")]
    want += [issue_comment(246, action=a) for a in ("created", "edited", "deleted")]
    want += [pr_comment(246, 260, action=a) for a in ("created", "edited", "deleted")]
    want += [pr_event(246, 260, a, OWNER) for a in ("opened", "edited", "reopened", "synchronize", "closed")]
    want += [review_event(246, 260, action=a) for a in ("submitted", "edited", "dismissed")]
    want += [line_note(246, 260, action=a) for a in ("created", "edited", "deleted")]
    want += [checks_finished(246, 260, w) for w in ("done-whens", "full suite", "worker")]
    want += [schedule()]
    missing = [f"{e} {p.get('action') or p.get('workflow', {}).get('name', '')}" for e, p in want if not starts(wf, e, p)]
    assert not missing, f"332.1: card.yml does not start on: {missing}"


# 332.2 -----------------------------------------------------------------------------------------------------------

def stale_repo(tmp):
    """A fake GitHub where three issues' cards are out of date.

    #246 is closed with PR #260 merged, both cards still the old open card; #312 is open with PR #314 holding no
    card; #320 is open with a plan its card does not show yet."""
    hub = Hub(tmp)
    hub.merge(246, 260)
    hub.no_pr_card(314, 312)
    s = hub.load()
    hub.state = s
    hub.add_issue(320)
    hub.state["issues"]["320"]["comments"] = hub.state["issues"]["320"]["comments"][:1]
    hub.save()
    return hub


def every_minutes():
    """The longest gap in minutes between two scheduled runs of card.yml, or None."""
    t = triggers(workflow()).get("schedule")
    best = None
    for cron in [c.get("cron") for c in listed(t) if isinstance(c, dict)]:
        f = (cron or "").split()
        if len(f) == 5 and f[1:] == ["*"] * 4:
            mins = set()
            for part in f[0].split(","):
                rng, _, step = part.partition("/")
                lo, hi = (0, 59) if rng == "*" else (int(rng.split("-")[0]), int(rng.split("-")[-1]) if "-" in rng else (59 if step else int(rng)))
                mins |= set(range(lo, hi + 1, int(step) if step else 1))
            ms = sorted(mins)
            gap = max((ms[(i + 1) % len(ms)] - ms[i]) % 60 or 60 for i in range(len(ms)))
            best = gap if best is None else min(best, gap)
    return best


def test_the_sweep_puts_right_every_stale_issue_card_and_pr_card_open_or_closed(tmp_path, record_property):
    """Every 15 minutes a sweep puts right every stale card, open or closed.

    card.yml's schedule fires at least every 15 minutes, every hour. #246 is closed with PR #260 merged and both cards still show the old open card; PR #314 has no card; #320's card
    predates its plan. After one scheduled run of card.yml, #246's and #260's cards say Merged, #314 shows #312's card,
    and #320's card shows its plan. Then a person's event on each issue changes no card: the sweep left each one as
    GitHub's state draws it. Proves 332.2."""
    record_property("proves", "332.2")
    gap = every_minutes()
    assert gap is not None and gap <= 15, f"332.2: card.yml's schedule leaves {gap} minutes between sweeps, not 15 or less"
    hub = stale_repo(tmp_path)
    must_redraw(hub, schedule(), "332.2")
    assert stage_of(hub.issue_body(246)) == "Merged" and stage_of(hub.pr_body(260)) == "Merged", \
        f"332.2: the sweep left closed #246 or merged PR #260 showing an old card: " \
        f"{stage_of(hub.issue_body(246))!r}, {stage_of(hub.pr_body(260))!r}"
    assert card_of(hub.pr_body(314)) and card_of(hub.pr_body(314)) == card_of(hub.issue_body(312)), \
        f"332.2: the sweep did not write #312's card on PR #314: {hub.pr_body(314)!r}"
    assert "The owner sees issue 320 done." in (card_of(hub.issue_body(320)) or ""), \
        f"332.2: the sweep left #320's card without its plan: {card_of(hub.issue_body(320))!r}"
    swept = {n: hub.issue_body(n) for n in (246, 312, 320)}
    swept_prs = {p: hub.pr_body(p) for p in (260, 314)}
    for n in (246, 312, 320):
        must_redraw(hub, issue_comment(n), "332.2")
    assert {n: hub.issue_body(n) for n in (246, 312, 320)} == swept, \
        "332.2: a redraw after the sweep changed an issue card, so the sweep did not leave it as GitHub's state draws it"
    assert {p: hub.pr_body(p) for p in (260, 314)} == swept_prs, \
        "332.2: a redraw after the sweep changed a PR card, so the sweep did not leave it as GitHub's state draws it"


# 332.3 -----------------------------------------------------------------------------------------------------------

def test_the_merge_rewrites_the_pr_card_as_merged_with_the_true_definition_of_done(tmp_path, record_property):
    """After the merge the PR card shows Merged with its true Definition of Done.

    PR #260 has every check passed and an approving code review, and the owner merges it: the merge event leaves
    #260's card saying Merged with All tests, Code review and Owner approval passed. On a fresh GitHub where All tests
    failed on the PR's last commit and the bot merged it, the merge leaves Merged with All tests failed and Owner
    approval not passed. Proves 332.3."""
    record_property("proves", "332.3")
    hub = Hub(tmp_path / "green")
    hub.merge(246, 260)
    must_redraw(hub, pr_event(246, 260, "closed", OWNER, merged=True), "332.3")
    assert stage_of(hub.pr_body(260)) == "Merged", f"332.3: PR #260's card does not say Merged: {hub.pr_body(260)!r}"
    done = done_of(hub.pr_body(260))
    assert done == {"All tests": "passed", "Code review": "passed", "Owner approval": "passed"}, \
        f"332.3: merged PR #260's Definition of Done is not every check passed: {done}"
    hub = Hub(tmp_path / "red")
    s = hub.load()
    s["checks"]["sha260"][1].update(conclusion="failure")
    hub.save()
    hub.merge(246, 260, by=BOT)
    must_redraw(hub, pr_event(246, 260, "closed", "bot", merged=True), "332.3")
    done = done_of(hub.pr_body(260))
    assert stage_of(hub.pr_body(260)) == "Merged" and done.get("All tests") == "failed", \
        f"332.3: the merged PR's card does not show its failed All tests: {done}"
    assert done.get("Owner approval") != "passed", f"332.3: a bot's merge shows as the owner's approval: {done}"


def test_a_pr_card_is_written_while_the_pr_is_open(tmp_path, record_property):
    """A pull request's card is written while it is open, the moment it opens.

    PR #314 is opened by the bot with only its closing line; that event writes #312's card on it, not Merged, with
    the checks passed so far, and the closing line kept. Proves 332.3."""
    record_property("proves", "332.3")
    hub = Hub(tmp_path)
    hub.no_pr_card(314, 312)
    must_redraw(hub, pr_event(312, 314, "opened", "bot"), "332.3")
    assert card_of(hub.pr_body(314)), f"332.3: open PR #314 got no card: {hub.pr_body(314)!r}"
    assert stage_of(hub.pr_body(314)) not in (None, "Merged"), \
        f"332.3: open PR #314's card shows {stage_of(hub.pr_body(314))!r}"
    assert done_of(hub.pr_body(314)).get("All tests") == "passed", \
        f"332.3: open PR #314's card does not show All tests passed: {done_of(hub.pr_body(314))}"
    assert hub.pr_body(314).rstrip().endswith("Closes #312"), "332.3: PR #314 lost its closing line"


# 332.4 -----------------------------------------------------------------------------------------------------------

def test_each_issue_has_its_own_queue_and_one_issue_never_cancels_another(tmp_path, record_property):
    """Each issue's card runs share one queue, and one issue's run never cancels another's.

    Before each event every card is made stale again. For seven events about #246 or PR #260 (the issue changing, a
    comment on either, the merge, a review, a line note, the checks finishing) the job that writes the cards waits in
    one and the same concurrency group, and never with no group. For two events about #312 or PR #314 it waits in another group, and no group any #246 run takes
    a place in is one a #312 run or the sweep takes a place in. Proves 332.4."""
    record_property("proves", "332.4")
    hub = Hub(tmp_path)
    about = {246: [issue_event(246, "edited"), issue_comment(246), pr_comment(246, 260),
                   pr_event(246, 260, "closed", OWNER, merged=True), review_event(246, 260), line_note(246, 260),
                   checks_finished(246, 260)],
             312: [issue_comment(312), pr_event(312, 314, "synchronize")],
             "sweep": [schedule()]}
    queues, places = {}, {}
    for who, events in about.items():
        for event in events:
            stale_again(hub)
            r = must_redraw(hub, event, "332.4")
            what = f"{event[0]} {event[1].get('action') or ''}"
            groups = r.card_groups()
            assert groups, f"332.4: on {what} no job of card.yml wrote the stale cards"
            assert None not in groups, f"332.4: on {what} the job that writes the cards waits in no queue at all"
            queues.setdefault(who, set()).update(groups)
            places.setdefault(who, set()).update(r.all_groups())
    for n in (246, 312):
        assert len(queues[n]) == 1, f"332.4: #{n}'s card runs wait in more than one queue: {sorted(queues[n])}"
    shared = places[246] & (places[312] | places["sweep"])
    assert not shared, f"332.4: #246's runs share a queue with #312's or the sweep's, so one cancels the other: {shared}"
    assert not places[312] & places["sweep"], \
        f"332.4: #312's runs share a queue with the sweep: {places[312] & places['sweep']}"


# 332.5 -----------------------------------------------------------------------------------------------------------

def test_the_card_code_is_smaller_than_before(record_property):
    """The card code has fewer lines than before.

    Counts dokima/card.py's lines: fewer than the 721 it had when this story was planned, once the per-event rules
    are gone. Proves 332.5."""
    record_property("proves", "332.5")
    lines = len(open(CARD_PY).read().splitlines())
    assert lines < CARD_PY_LINES_BEFORE, \
        f"332.5: dokima/card.py has {lines} lines, not fewer than the {CARD_PY_LINES_BEFORE} before this story"


# 332.6 -----------------------------------------------------------------------------------------------------------

def test_the_sweep_names_a_card_it_cannot_redraw_fails_and_puts_the_rest_right(tmp_path, record_property):
    """The sweep names a card it cannot redraw, fails, and fixes the rest.

    GitHub refuses every read of #312. The scheduled run fails with an error line naming #312, and still leaves #246
    and #260 saying Merged and #320 showing its plan; no error line names #246, #260 or #320. Proves 332.6."""
    record_property("proves", "332.6")
    hub = stale_repo(tmp_path)
    hub.refuse("read-issue", 312)
    r = hub.run(*schedule(), "332.6")
    assert r.card_ran(), "332.6: the scheduled run did not run the card job"
    assert r.failed(), f"332.6: the scheduled run passed although #312's card could not be redrawn:\n{r.log[-2000:]}"
    errors = r.errors()
    assert any("#312" in e for e in errors), f"332.6: no error line names #312: {errors}\n{r.log[-2000:]}"
    assert not [e for e in errors if re.search(r"#(246|260|320)\b", e)], f"332.6: an error names a card that was fine: {errors}"
    assert stage_of(hub.issue_body(246)) == "Merged" and stage_of(hub.pr_body(260)) == "Merged", \
        "332.6: one unreadable issue kept #246 and PR #260 from being put right"
    assert "The owner sees issue 320 done." in (card_of(hub.issue_body(320)) or ""), \
        "332.6: one unreadable issue kept #320's card from being put right"


def test_an_event_names_the_card_it_cannot_write_fails_and_writes_the_other(tmp_path, record_property):
    """A card that cannot be written is named, the run fails, the other is written.

    GitHub refuses writing PR #260's body: a comment on #246 still writes #246's card, and the run fails with an error
    line naming #260. On a fresh GitHub that refuses writing #246's body, PR #260's card is still written and the
    error line names #246. Proves 332.6."""
    record_property("proves", "332.6")
    for refused, named, other in (("write-pr", 260, "issue"), ("write-issue", 246, "pr")):
        hub = Hub(tmp_path / refused)
        hub.merge(246, 260)
        hub.refuse(refused, named)
        r = hub.run(*issue_comment(246), "332.6")
        assert r.card_ran(), "332.6: card.yml did not run its card job on a comment on #246"
        assert r.failed(), f"332.6: the run passed although #{named}'s card could not be written"
        assert any(f"#{named}" in e for e in r.errors()), \
            f"332.6: no error line names #{named}, whose card could not be written: {r.errors()}\n{r.log[-2000:]}"
        written = hub.issue_body(246) if other == "issue" else hub.pr_body(260)
        assert stage_of(written) == "Merged", \
            f"332.6: #{named}'s refused card kept the other card ({other}) from being written: {written[:300]!r}"


# 332.7 -----------------------------------------------------------------------------------------------------------

def test_runs_started_by_a_pull_request_run_mains_code(tmp_path, record_property):
    """Runs started by a pull request use main's card code, never the PR's.

    card.yml has no pull_request trigger (which runs a PR's own copy of the workflow with the keys), and for a merge,
    new commits, a review and a line note on PR #260 every checkout step of the run checks out main. Proves 332.7."""
    record_property("proves", "332.7")
    assert "pull_request" not in triggers(workflow()), \
        "332.7: card.yml starts on pull_request, which runs the pull request's own copy of the workflow"
    hub = Hub(tmp_path)
    for event in (pr_event(246, 260, "closed", OWNER, merged=True), pr_event(246, 260, "synchronize"),
                  review_event(246, 260), line_note(246, 260)):
        r = must_redraw(hub, event, "332.7")
        what = f"{event[0]} {event[1]['action']}"
        assert r.checkouts, f"332.7: the run on {what} checks out no code"
        wrong = [ref for ref in r.checkouts if ref not in ("main", "refs/heads/main")]
        assert not wrong, f"332.7: the run on {what} checks out {wrong}, the pull request's code, not main"


# 332.8 -----------------------------------------------------------------------------------------------------------

def test_a_sweep_with_nothing_to_put_right_makes_few_github_calls(tmp_path, record_property):
    """A sweep with nothing to fix writes nothing and makes few GitHub calls.

    Thirty closed issues (#246 and #400 to #428), each with its merged pull request, and the open #312 with its open
    PR #314 and the open #320 with none. The first scheduled run puts every card right: all thirty closed issues and
    their PRs say Merged. The second, with nothing changed, writes nothing and makes at most 10 GitHub calls plus one
    per open issue and two per open pull request (14 here), however many closed issues there are. Proves 332.8."""
    record_property("proves", "332.8")
    hub = stale_repo(tmp_path)
    closed = [(246, 260)] + [(n, n + 100) for n in range(400, 429)]
    for n, p in closed[1:]:
        hub.add_issue(n, p)
    hub.save()
    for n, p in closed[1:]:
        hub.merge(n, p)
    must_redraw(hub, schedule(), "332.8")
    stale = [n for n, p in closed if stage_of(hub.issue_body(n)) != "Merged" or stage_of(hub.pr_body(p)) != "Merged"]
    assert not stale, f"332.8: the first sweep left closed issues or their merged PRs not saying Merged: {stale}"
    hub.clear_writes()
    calls = os.path.join(hub.dir, "calls.jsonl")
    open(calls, "w").close()
    must_redraw(hub, schedule(), "332.8")
    made = [json.loads(l) for l in open(calls)]
    budget = 10 + 2 + 2 * 1
    assert not [w for w in hub.writes() if w["op"] in ("issue-body", "pr-body")], \
        f"332.8: a sweep with nothing changed wrote cards: {hub.writes()}"
    assert len(made) <= budget, \
        f"332.8: a sweep with nothing to put right made {len(made)} GitHub calls, more than {budget}: " \
        f"{[' '.join(c[:3]) for c in made][:40]}"
