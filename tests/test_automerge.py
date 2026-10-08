"""On autopilot, a pull request the reviewer approved merges by itself once every check is green (#212).

These tests run the real workflows the way GitHub runs them, on the machine from test_start.py: the agent workflow
(.github/workflows/agent.yml) for the code review of pull request #60, built for issue #57, and the command listener
(.github/workflows/commands.yml) for `/autopilot start`. Every step's `if:` is evaluated and its script run with bash
against a fake `gh`, which here also knows issue #57's labels (the issue tree and label calls of test_autopilot.py) and
pull request #60 as GitHub would show it:

- its head commit, the tip of try/issue-57, and the checks GitHub reports on each commit;
- the files it changes;
- whether it is merged, and every merge call.

A test can add more open pull requests, each built for another issue of the tree on its own real try/issue-N branch,
with that issue's history (`gh issue view N`, or GET on repos/o/r/issues/N/comments); comments posted on such a pull
request are kept on it. Without a selector, a `gh pr` call means #60.

GitHub answers about a pull request through any of: `gh pr view` (a number, URL or branch, `--json` with every field: number,
headRefName, headRefOid, body, state, mergeable, mergeStateStatus, files, statusCheckRollup, comments, reviews),
`gh pr list` (open, merged or all, with --head or --search head:...), `gh pr checks` (with or without --required; with --json, or as text exiting 1 on a
failed check and 8 on a pending one), `gh pr diff --name-only`, and the REST API: repos/o/r/pulls (with head=),
repos/o/r/pulls/N, repos/o/r/pulls/N/files, repos/o/r/commits/SHA/check-runs and repos/o/r/commits/SHA/status (no commit statuses: its
combined state is pending with total_count 0, as GitHub says when a repo uses only check runs). `-q`/`--jq` is
understood only as a plain `.field`, `.[0].field` or `.[].field`. GraphQL is not answered. The repo has no branch
protection unless a test says so: like GitHub on such a repo, the fake merges whatever it is asked to merge, red or
pending checks included, so only Dokima's own code can keep a red pull request out. A merge is `gh pr merge` with
--merge, --squash or --rebase (without one gh refuses, as it does when not interactive; --auto only turns on
auto-merge and merges nothing; --admin is noted so a test can refuse it), or PUT repos/o/r/pulls/60/merge; both honour
the commit they are pinned to (--match-head-commit, or the sha field) and fail with GitHub's "Head branch was
modified" when the head has moved. A test can make GitHub refuse every merge with its own reason (a conflict, branch
protection), and can push a new commit to the pull request, with its checks still running, the moment code first
reads the head or the checks.
"""
import json
import os
import re

import test_start as ts
from test_autopilot import TREE_GH, Tree
from test_start import N, OWNER, PR, Ctx, Machine, sh, workflow
from dokima import agent

LABEL = "autopilot"
MERGED_LINE = f"Autopilot: merged PR #{PR}"
GREEN = [{"name": "All tests", "state": "SUCCESS"}, {"name": "Lint", "state": "SUCCESS"}]
RED_NAME = "Unit tests (3.12)"
RED = [{"name": "All tests", "state": "SUCCESS"}, {"name": RED_NAME, "state": "FAILURE"}]
PENDING = [{"name": "All tests", "state": "SUCCESS"}, {"name": "Slow suite", "state": "PENDING"}]
CONFLICT = "Pull Request is not mergeable: the merge commit cannot be cleanly created"
PROTECTED = "At least 1 approving review is required by reviewers with write access"

PR_GH = r'''
PR_FILE = os.path.join(d, "pr.json")
PRS = json.load(open(PR_FILE)) if os.path.exists(PR_FILE) else None
HIST_FILE = os.path.join(d, "issues.json")
HIST = json.load(open(HIST_FILE)) if os.path.exists(HIST_FILE) else {}
def save_pr():
    json.dump(PRS, open(PR_FILE, "w"), indent=1)
ISSUE_FILE = os.path.join(d, "issue.json")
if os.path.exists(ISSUE_FILE) and os.path.exists(LABELS_FILE):
    _iss = json.load(open(ISSUE_FILE))
    _iss["labels"] = [{"name": l} for l in LABELS.get(str(_iss["number"]), [])]
    json.dump(_iss, open(ISSUE_FILE, "w"))
def num_of(x):
    """The number a selector names (60, #60, a URL), or None."""
    m = re.fullmatch(r"#?(\d+)|.*/(?:pull|pulls|issues)/(\d+)/?", str(x or ""))
    return (m.group(1) or m.group(2)) if m else None
def pr_by_branch(ref):
    ref = re.sub(r"^(?:refs/heads/|[^:/]+:)", "", str(ref or ""))
    return next((n for n, p in PRS.items() if p["branch"] == ref), None)
def selected(start):
    """The pull request a `gh pr ...` call names (number, URL or branch); with none, #60."""
    sel = a[start] if len(a) > start and not a[start].startswith("-") else None
    if sel is None:
        return "60"
    n = num_of(sel)
    if n is not None:
        return n if n in PRS else None
    return pr_by_branch(sel)
def checks_of(n, sha):
    return PRS[n]["checks"].get(sha, [])
def reveal(n):
    """Code has now seen the head or its checks: a commit pushed meanwhile becomes the head, its checks running."""
    p = PRS[n]
    if p.get("moves_to") and not p.get("moved"):
        p["moved"] = True
        p["head"] = p["moves_to"]
        save_pr()
def rollup(n, sha):
    out = []
    for c in checks_of(n, sha):
        done = c["state"] != "PENDING"
        out.append({"__typename": "CheckRun", "name": c["name"], "workflowName": c["name"],
                    "status": "COMPLETED" if done else "IN_PROGRESS", "conclusion": c["state"] if done else "",
                    "detailsUrl": "https://github.com/o/r/actions/runs/7"})
    return out
def pr_obj(n):
    p = PRS[n]
    merged = bool(p.get("merged"))
    return {"number": int(n), "url": f"https://github.com/o/r/pull/{n}", "headRefName": p["branch"], "baseRefName": "main",
            "headRefOid": p["head"], "body": f"Closes #{p['issue']}", "title": f"Issue {p['issue']}",
            "state": "MERGED" if merged else "OPEN", "merged": merged, "mergeable": "UNKNOWN",
            "mergeStateStatus": "UNKNOWN", "isDraft": False,
            "files": [{"path": f, "additions": 1, "deletions": 0} for f in p["files"]],
            "statusCheckRollup": rollup(n, p["head"]), "comments": comments_on("pr", n), "reviews": [],
            "commits": [{"oid": p["head"]}], "labels": [], "closingIssuesReferences": [{"number": p["issue"]}]}
def jq_pick(obj, q):
    q = (q or "").strip()
    m = re.fullmatch(r"\.\[(?:0)?\]\.([A-Za-z_]+)", q)
    if m and isinstance(obj, list):
        vals = [x.get(m.group(1), "") for x in obj]
        return "\n".join(str(v) for v in (vals[:1] if "[0]" in q else vals))
    m = re.fullmatch(r"\.([A-Za-z_]+)", q)
    if m and isinstance(obj, dict):
        v = obj.get(m.group(1), "")
        return json.dumps(v) if isinstance(v, (dict, list)) else str(v).lower() if isinstance(v, bool) else str(v)
    return json.dumps(obj)
def emit(obj):
    q = flag("-q", "--jq")
    print(jq_pick(obj, q) if q else json.dumps(obj))
def json_fields():
    return (flag("--json") or "").split(",")
def merge_now(n, sha_pin, how):
    p = PRS[n]
    if p.get("merged"):
        return "Pull Request is not mergeable: it is already merged"
    if sha_pin and sha_pin != p["head"]:
        return "Head branch was modified. Review and try the merge again."
    if p.get("refuse"):
        return p["refuse"]
    p["merged"] = {"sha": p["head"], "how": how}
    save_pr()
    return None
def no_pr():
    sys.stderr.write("no pull requests found\n")
    sys.exit(1)
ISSUE_ARG = (a[2] if len(a) > 2 else "") if a[:2] == ["issue", "view"] else ""
if HIST and num_of(ISSUE_ARG) in HIST:
    n = num_of(ISSUE_ARG)
    obj = {"number": int(n), "title": f"Issue {n}", "body": "Fix it.", "state": "OPEN",
           "labels": [{"name": l} for l in LABELS.get(n, [])], "comments": HIST[n] + comments_on("issue", n)}
    emit(obj)
    sys.exit(0)
C_PATH = next((x for x in a[1:] if re.fullmatch(r"/?repos/o/r/issues/\d+/comments(?:\?.*)?", x)), None) if a[:1] == ["api"] else None
if PRS is not None and C_PATH:
    n = re.search(r"issues/(\d+)/comments", C_PATH).group(1)
    body = api_body()
    if body is not None or (flag("-X", "--method") or "GET").upper() != "GET":
        out(shown(create("pr" if n in PRS else "issue", n, body)))
        sys.exit(0)
    if n in HIST:
        old = [{"id": 100 + i, "body": c["body"], "user": {"login": c["author"]["login"]},
                "author": {"login": c["author"]["login"]}, "created_at": c["createdAt"], "createdAt": c["createdAt"]}
               for i, c in enumerate(HIST[n])]
        print(json.dumps(old + [shown(c) for c in load() if c["number"] == int(n)]))
        sys.exit(0)
if PRS is not None and a[:2] == ["pr", "view"]:
    n = selected(2)
    if n is None:
        no_pr()
    obj = pr_obj(n)
    if any(f in json_fields() for f in ("headRefOid", "statusCheckRollup", "commits")) or not flag("--json"):
        reveal(n)
    emit(obj)
    sys.exit(0)
if PRS is not None and a[:2] == ["pr", "list"]:
    state = (flag("--state", "-s") or "open").lower()
    head = flag("--head", "-H")
    search = flag("--search", "-S") or ""
    m_head = re.search(r"head:(\S+)", search)
    head = head or (m_head.group(1) if m_head else None)
    items = []
    for n, p in sorted(PRS.items(), key=lambda kv: int(kv[0])):
        merged = bool(p.get("merged"))
        show = state == "all" or (state == "open" and not merged) or (state in ("merged", "closed") and merged)
        if show and (head is None or p["branch"] == head):
            items.append(pr_obj(n))
            if any(f in json_fields() for f in ("headRefOid", "statusCheckRollup")):
                reveal(n)
    emit(items)
    sys.exit(0)
if PRS is not None and a[:2] == ["pr", "checks"]:
    n = selected(2)
    if n is None:
        no_pr()
    checks = checks_of(n, PRS[n]["head"])
    reveal(n)
    if not checks:
        sys.stderr.write(f"no checks reported on the '{PRS[n]['branch']}' branch\n")
        sys.exit(1)
    bucket = {"SUCCESS": "pass", "FAILURE": "fail", "PENDING": "pending"}
    rows = [{"name": c["name"], "state": "IN_PROGRESS" if c["state"] == "PENDING" else c["state"],
             "bucket": bucket[c["state"]], "workflow": c["name"], "link": "https://github.com/o/r/actions/runs/7",
             "description": "", "event": "pull_request"} for c in checks]
    if flag("--json"):
        emit(rows)
        sys.exit(0)
    for r in rows:
        print(f"{r['name']}\t{r['bucket']}\t1m\t{r['link']}")
    sys.exit(1 if any(r["bucket"] == "fail" for r in rows) else 8 if any(r["bucket"] == "pending" for r in rows) else 0)
if PRS is not None and a[:2] == ["pr", "diff"]:
    n = selected(2)
    if n is None:
        no_pr()
    print("\n".join(PRS[n]["files"]))
    sys.exit(0)
if PRS is not None and a[:2] == ["pr", "merge"]:
    n = selected(2)
    if n is None:
        no_pr()
    PRS[n].setdefault("calls", []).append(a)
    save_pr()
    if "--admin" in a:
        sys.stderr.write("the bot may not bypass branch protection\n")
        sys.exit(1)
    if "--auto" in a:
        print(f"Pull request o/r#{n} will be automatically merged when all requirements are met")
        sys.exit(0)
    how = next((x[2:] for x in a if x in ("--merge", "--squash", "--rebase")), None)
    if not how:
        sys.stderr.write("--merge, --rebase, or --squash required when not running interactively\n")
        sys.exit(1)
    why = merge_now(n, flag("--match-head-commit"), how)
    if why:
        sys.stderr.write(f"X Pull request o/r#{n} was not merged: {why}\n")
        sys.exit(1)
    print(f"Merged pull request o/r#{n} (Issue {PRS[n]['issue']})")
    sys.exit(0)
API = next((x for x in a[1:] if x.startswith(("repos/o/r/pulls", "/repos/o/r/pulls", "repos/o/r/commits", "/repos/o/r/commits"))), None) if a[:1] == ["api"] else None
if PRS is not None and API:
    path, _, query = API.lstrip("/").partition("?")
    m = re.fullmatch(r"repos/o/r/pulls/(\d+)/merge", path)
    if m:
        n = m.group(1)
        if n not in PRS:
            sys.stderr.write("HTTP 404: Not Found\n")
            sys.exit(1)
        PRS[n].setdefault("calls", []).append(a)
        save_pr()
        sha = (fields("sha") or [None])[0]
        how = (fields("merge_method") or ["merge"])[0]
        if "--input" in a:
            body = json.load(open(flag("--input")))
            sha, how = body.get("sha", sha), body.get("merge_method", how)
        why = merge_now(n, sha, how)
        if why:
            code = 409 if "Head branch was modified" in why else 405
            sys.stderr.write(f"HTTP {code}: {why} (https://api.github.com/repos/o/r/pulls/{n}/merge)\n")
            sys.exit(1)
        emit({"sha": "m" * 40, "merged": True, "message": "Pull Request successfully merged"})
        sys.exit(0)
    m = re.fullmatch(r"repos/o/r/pulls/(\d+)/files", path)
    if m and m.group(1) in PRS:
        emit([{"filename": f, "status": "modified"} for f in PRS[m.group(1)]["files"]])
        sys.exit(0)
    def rest(n):
        o = pr_obj(n)
        return {"number": int(n), "state": "closed" if o["merged"] else "open", "merged": o["merged"], "mergeable": None,
                "mergeable_state": "unknown", "head": {"sha": o["headRefOid"], "ref": PRS[n]["branch"]},
                "base": {"ref": "main"}, "body": o["body"], "html_url": o["url"]}
    m = re.fullmatch(r"repos/o/r/pulls/(\d+)", path)
    if m and m.group(1) in PRS:
        obj = rest(m.group(1))
        reveal(m.group(1))
        emit(obj)
        sys.exit(0)
    if path == "repos/o/r/pulls":
        hm = re.search(r"head=([^&]+)", query)
        head = flag("head") or (hm.group(1) if hm else None)
        for i, x in enumerate(a):
            if x in ("-f", "-F", "--field", "--raw-field") and i + 1 < len(a) and a[i + 1].startswith("head="):
                head = a[i + 1][5:]
        st = re.search(r"state=(\w+)", query)
        st = st.group(1) if st else "open"
        items = [rest(n) for n, p in sorted(PRS.items(), key=lambda kv: int(kv[0]))
                 if (head is None or pr_by_branch(head) == n) and (st == "all" or (st == "open") != bool(p.get("merged")))]
        for i in items:
            reveal(str(i["number"]))
        emit(items)
        sys.exit(0)
    m = re.fullmatch(r"repos/o/r/commits/([^/]+(?:/[^/]+)*?)/(check-runs|status)", path)
    if m:
        ref, kind = m.group(1), m.group(2)
        n = pr_by_branch(ref) or next((k for k, p in PRS.items() if ref in p["checks"]), None)
        sha = PRS[n]["head"] if n and pr_by_branch(ref) else ref
        if kind == "status":
            if n:
                reveal(n)
            emit({"state": "pending", "total_count": 0, "statuses": [], "sha": sha})
            sys.exit(0)
        runs = [{"name": c["name"], "head_sha": sha, "status": "in_progress" if c["state"] == "PENDING" else "completed",
                 "conclusion": None if c["state"] == "PENDING" else c["state"].lower()} for c in (checks_of(n, sha) if n else [])]
        if n:
            reveal(n)
        emit({"total_count": len(runs), "check_runs": runs})
        sys.exit(0)
if PRS is not None and a[:2] == ["run", "download"]:
    dest = flag("-D", "--dir") or "."
    os.makedirs(os.path.join(dest, "p"), exist_ok=True)
    open(os.path.join(dest, "p", "s.jsonl"), "w").write(json.dumps({"message": {"role": "assistant", "content": "Built."}}) + "\n")
    sys.exit(0)
'''


def fake_gh():
    """The fake gh of test_start.py taught the issue tree, its labels, and pull request #60 with any others a test adds."""
    fake = ts.FAKE_GH.replace('if a[:2] == ["issue", "view"]:', TREE_GH + PR_GH + 'if a[:2] == ["issue", "view"]:', 1)
    assert fake != ts.FAKE_GH, "test setup: could not teach the fake GitHub about the pull request"
    return fake.replace("#!/usr/bin/env python3", f"#!{ts.sys.executable}")


WORK = {"summary": "Built it.", "criteria": {"57.1": "x.py"}, "evidence": "pytest -q: 1 passed"}
PR_APPROVE = {"previous_step": {"did": ["Built x.py."], "decided": [], "open": []}, "stage": "pr", "round": 1,
              "verdict": "approve", "summary": "Every criterion has its proof.", "blockers": [], "notes": [],
              "outside_plan": [], "resolved": [],
              "asks": [{"ask": "Fix it.", "source": "https://github.com/o/r/issues/57", "criterion": "57.1"}]}
PR_BLOCK = {**PR_APPROVE, "verdict": "block", "summary": "One proof is missing.",
            "blockers": [{"id": "B1", "criterion": "57.1", "test": None, "problem": "No proof.", "evidence": "x.py",
                          "fix": "Add it.", "fixer": "worker"}]}


def worker_record():
    """A passed worker record, the way the workflow writes one, from run 3."""
    return {"role": "worker", "stage": None, "run_id": "3", "run": "https://github.com/o/r/actions/runs/3",
            "models": ["claude-opus-5-5"], "handback": WORK, "check": {"passed": True, "problems": []}}


def pr_review_record(review):
    """A passed code review record from run 4."""
    return {"role": "reviewer", "stage": "pr", "run_id": "4", "run": "https://github.com/o/r/actions/runs/4",
            "models": ["claude-opus-5-5"], "handback": review, "check": {"passed": True, "problems": []}}


BUILT = ts.STORY_APPROVED + [ts.record_comment(worker_record(), "2026-10-07T11:00:00Z")]
APPROVED = BUILT + [ts.record_comment(pr_review_record(PR_APPROVE), "2026-10-07T11:30:00Z")]
BLOCKED = BUILT + [ts.record_comment(pr_review_record(PR_BLOCK), "2026-10-07T11:30:00Z")]


def set_pr(m, checks, workflow_file=False, refuse="", moves=False):
    """Give the machine's pull request #60 its head (the try branch's tip), checks and files, and what GitHub refuses.

    With workflow_file, the try branch first gets a commit that changes .github/workflows/extra.yml, so the branch and
    GitHub's file list agree. With moves, a new commit with its checks still running becomes the head the moment code
    first reads the head or its checks."""
    src = f"{m.tmp}/src"
    if workflow_file:
        os.makedirs(f"{src}/.github/workflows", exist_ok=True)
        open(f"{src}/.github/workflows/extra.yml", "w").write("name: extra\non: push\njobs: {}\n")
        sh(src, "git", "add", "-A")
        sh(src, "git", "commit", "-qm", "workflow")
        sh(src, "git", "push", "-q", "origin", f"try/issue-{N}")
        m.try_sha = sh(src, "git", "rev-parse", "HEAD")
    files = sh(src, "git", "diff", "--name-only", f"main...try/issue-{N}").split()
    later = "b" * 40
    state = {"issue": int(N), "branch": f"try/issue-{N}", "head": m.try_sha,
             "checks": {m.try_sha: checks, later: [{"name": "All tests", "state": "PENDING"}]},
             "files": files, "refuse": refuse, "merged": None}
    if moves:
        state["moves_to"] = later
    json.dump({PR: state}, open(f"{m.tmp}/gh/pr.json", "w"))


def history(issue, comments):
    """Issue #57's history, retold for another issue: its criteria and links name that issue instead."""
    return json.loads(json.dumps(comments).replace("57.1", f"{issue}.1").replace("issues/57", f"issues/{issue}"))


def add_pr(m, number, issue, comments, checks):
    """Give the fake GitHub another open pull request, built for another issue on its own try branch, and that issue's history.

    The branch try/issue-ISSUE is a real commit off main that adds one file, pushed to the machine's origin; GitHub
    reports the given checks on it. The issue's comments are the given history, retold for that issue."""
    src = f"{m.tmp}/src"
    sh(src, "git", "checkout", "-q", "-B", f"try/issue-{issue}", "main")
    open(f"{src}/x{issue}.py", "w").write(f'"""Issue {issue}."""\n')
    sh(src, "git", "add", "-A")
    sh(src, "git", "commit", "-qm", f"issue {issue}")
    sh(src, "git", "push", "-q", "origin", f"try/issue-{issue}")
    sha = sh(src, "git", "rev-parse", "HEAD")
    sh(src, "git", "checkout", "-q", f"try/issue-{N}")
    prs = json.load(open(f"{m.tmp}/gh/pr.json"))
    prs[str(number)] = {"issue": issue, "branch": f"try/issue-{issue}", "head": sha, "checks": {sha: checks},
                        "files": [f"x{issue}.py"], "refuse": "", "merged": None}
    json.dump(prs, open(f"{m.tmp}/gh/pr.json", "w"))
    path = f"{m.tmp}/gh/issues.json"
    hist = json.load(open(path)) if os.path.exists(path) else {}
    hist[str(issue)] = history(issue, comments)
    json.dump(hist, open(path, "w"))
    return sha


def pr_state(m, pr=PR):
    """A pull request (#60 unless named) as the fake GitHub holds it now."""
    return json.load(open(f"{m.tmp}/gh/pr.json"))[str(pr)]


class Review(Machine):
    """The agent workflow's code review of pull request #60, its reviewer handing back the review given."""

    def __init__(self, tmp, review, labels, checks, comments=BUILT, **pr):
        super().__init__(tmp, comments, try_branch=True, options={"pr_open": True})
        t = self.tmp
        open(f"{t}/bin/gh", "w").write(fake_gh())
        json.dump({str(k): list(v) for k, v in labels.items()}, open(f"{t}/gh/labels.json", "w"))
        json.dump(review, open(f"{t}/review.json", "w"))
        set_pr(self, checks, **pr)
        open(f"{t}/event.json", "w").write(json.dumps({"inputs": {"role": "reviewer", "stage": "pr", "issue": N}}))
        ctx = {"inputs": Ctx(role="reviewer", stage="pr", issue=N),
               "github": Ctx(event_name="workflow_dispatch", actor=OWNER, event=Ctx(), run_id="42", run_attempt="1",
                             server_url="https://github.com", repository="o/r", token="fake-github-token"),
               "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
               "vars": Ctx(DOKIMA_APP_ID="1"), "needs": Ctx()}
        wf = workflow("agent.yml")
        self.result, _ = self.run_job("run", wf["jobs"]["run"], ctx, "workflow_dispatch",
                                      [("/tmp/", f"{t}/"), ("/home/runner/", f"{t}/home/")], wf.get("defaults"))
        self.failed = self.result == "failure"

    def board(self):
        """Where the run put the card ('Review needs'), or '' when it wrote nothing."""
        out = self.env.get("OUT", "")
        path = os.path.join(out, "board.txt")
        return open(path).read().strip() if out and os.path.exists(path) else ""


class Command(Tree):
    """The command listener on a code owner's comment, with the fake GitHub also knowing pull request #60."""

    def __init__(self, tmp, comments, labels, checks, **pr):
        super().__init__(tmp, labels)
        t = self.tmp
        issue = json.load(open(f"{t}/gh/issue.json"))
        issue["comments"] = comments
        json.dump(issue, open(f"{t}/gh/issue.json", "w"))
        open(f"{t}/bin/gh", "w").write(fake_gh())
        set_pr(self, checks, **pr)


def merged(m, pr=PR):
    """The commit GitHub merged for a pull request (#60 unless named), or None."""
    return (pr_state(m, pr).get("merged") or {}).get("sha")


def autopilot_lines(m):
    """Every comment, anywhere, whose whole text is the Autopilot line, as (kind, number)."""
    return [(p["where"][0], p["where"][2]) for p in m.posted() if p["body"].strip() == MERGED_LINE]


def review_card(m):
    """The code review's record as posted (on the pull request or the issue): its body, or ''."""
    for p in m.posted():
        recs = agent.records([{"author": {"login": agent.BOT}, "body": p["body"]}])
        if recs and recs[0].get("role") == "reviewer":
            return p["body"]
    return ""


def next_line(body):
    """The card's Next line, or ''."""
    return next((l for l in body.splitlines() if l.startswith("**Next:**")), "")


def no_bypass(m, crit, case):
    """No merge call, on any pull request, tried to bypass branch protection."""
    for c in [c for p in json.load(open(f"{m.tmp}/gh/pr.json")).values() for c in p.get("calls", [])]:
        assert "--admin" not in c, f"{crit} ({case}): the merge tried to bypass branch protection with --admin: {c}"


def assert_merged(m, crit, case):
    """The pull request was merged at its green head, the issue got exactly one Autopilot line, and nothing else started."""
    assert merged(m) == m.try_sha, \
        f"{crit} ({case}): the approved pull request with green checks was not merged at its head " \
        f"(merged: {merged(m)}, merge calls: {pr_state(m).get('calls', [])}):\n{m.tail()}"
    lines = autopilot_lines(m)
    assert lines == [("issue", N)], \
        f"{crit} ({case}): expected exactly one comment reading '{MERGED_LINE}' on issue #{N}, found {lines}: " \
        f"{[p['body'][:200] for p in m.posted()]}"
    assert m.dispatches() == [], f"{crit} ({case}): merging also started another stage: {m.dispatches()}"
    no_bypass(m, crit, case)


def assert_waits(m, crit, case, reason=None):
    """Nothing merged, no Autopilot line, and a comment on the pull request mentions the owner (with the reason)."""
    assert merged(m) is None, f"{crit} ({case}): the pull request was merged at {merged(m)}, but it should wait for the owner"
    assert autopilot_lines(m) == [], f"{crit} ({case}): an Autopilot line was posted though nothing merged"
    on_pr = [p["body"] for p in m.posted() if p["where"][0] == "pr" and p["where"][2] == PR]
    told = [b for b in on_pr if f"@{OWNER}" in b and (reason is None or reason.lower() in b.lower())]
    assert told, f"{crit} ({case}): no comment on pull request #{PR} mentions @{OWNER}" + \
        (f" and says why ({reason!r})" if reason else "") + f": {[b[-500:] for b in on_pr]}\n{m.tail()}"
    no_bypass(m, crit, case)


def test_on_autopilot_an_approved_pull_request_with_green_checks_merges_and_says_so(record_property, tmp_path):
    """On autopilot, the code review's approval with every check green merges the pull request and the issue says `Autopilot: merged PR #60`.

    Runs the agent workflow's code review of pull request #60 on issue #57, which carries the autopilot label, the
    reviewer approving and both checks on the head green. GitHub must have merged #60 at that head, issue #57 must
    carry exactly one comment reading `Autopilot: merged PR #60`, the review's card must end with a Next line saying it
    merged without mentioning the owner, the board must not show Needs you, and no other stage may start."""
    record_property("proves", "212.1")
    m = Review(tmp_path / "river", PR_APPROVE, {57: [LABEL]}, GREEN)
    assert m.agent_started(), f"212.1: test setup: the code review never ran; it stopped at '{m.failed_step}':\n{m.tail()}"
    assert_merged(m, "212.1", "code review")
    card = review_card(m)
    assert card, f"212.1: the code review posted no record: {[p['body'][:200] for p in m.posted()]}"
    line = next_line(card)
    assert "merged" in line.lower(), f"212.1: the review's card does not say the pull request merged; its Next line is {line!r}"
    assert f"@{OWNER}" not in line, f"212.1: the merged pull request still mentions the owner: {line!r}"
    assert not m.board().endswith("needs"), f"212.1: the board shows Needs you after the merge: {m.board()!r}"


def test_autopilot_start_merges_a_pull_request_already_approved(record_property, tmp_path):
    """`/autopilot start` on an issue, or on its pull request, merges a pull request the reviewer already approved with green checks.

    Issue #57's newest record is the code review's approval and both checks on #60's head are green; the issue is not
    yet on autopilot. The code owner says `/autopilot start` on #57, then (on a fresh machine) on #60. Each time GitHub
    must have merged #60 at its head, issue #57 must carry exactly one comment reading `Autopilot: merged PR #60`, and
    no planner, worker or reviewer may start. Beside them, a newest code review that blocks merges nothing."""
    record_property("proves", "212.1")
    for case, on_pr in (("on the issue", False), ("on the pull request", True)):
        m = Command(tmp_path / case.replace(" ", "-"), APPROVED, {}, GREEN)
        called = m.listen("/autopilot start", on_pr=on_pr)
        assert not m.failed, f"212.1 ({case}): the listener failed on /autopilot start:\n{m.tail()}"
        assert not called, f"212.1 ({case}): /autopilot start started an agent"
        assert_merged(m, "212.1", f"/autopilot start {case}")
    m = Command(tmp_path / "blocked", BLOCKED, {}, GREEN)
    m.listen("/autopilot start")
    assert merged(m) is None and autopilot_lines(m) == [], \
        f"212.1 (blocked): /autopilot start merged a pull request whose newest code review blocks it"


def test_autopilot_start_merges_the_approved_pull_requests_of_the_whole_tree(record_property, tmp_path):
    """`/autopilot start` merges every already-approved pull request with green checks anywhere under the issue, and nothing outside it.

    Issue #57's tree is #101 and #102 under it, #103 under #101 and #104 under #103; #58 is its sibling. Pull requests
    wait on each: #60 (#57) and #61 (#101) and #63 (#104, three levels down) approved by the code review with green
    checks; #62 (#102) whose newest code review blocks; #64 (#103) approved but with a red check; #65 (#58, outside the
    tree) approved and green. After the code owner's `/autopilot start` on #57, exactly #60, #61 and #63 must be merged,
    each at its head; issues #57, #101 and #104 must each carry exactly one comment reading `Autopilot: merged PR #N`
    for their own pull request and no other issue any; #64 must say on itself which check is red and mention the
    owner; and no planner, worker or reviewer may start."""
    record_property("proves", "212.1")
    m = Command(tmp_path / "tree", APPROVED, {}, GREEN)
    heads = {PR: m.try_sha}
    waiting = ((61, 101, APPROVED, GREEN), (62, 102, BLOCKED, GREEN), (63, 104, APPROVED, GREEN),
               (64, 103, APPROVED, RED), (65, 58, APPROVED, GREEN))
    for number, issue, comments, checks in waiting:
        heads[str(number)] = add_pr(m, number, issue, comments, checks)
    called = m.listen("/autopilot start")
    assert not m.failed, f"212.1 (tree): the listener failed on /autopilot start:\n{m.tail()}"
    assert not called and m.dispatches() == [], "212.1 (tree): /autopilot start started a stage"
    done = {pr for pr in heads if merged(m, pr)}
    assert done == {PR, "61", "63"}, \
        f"212.1 (tree): /autopilot start on #57 should merge exactly #60, #61 and #63 (approved, green, inside the " \
        f"tree); it merged {sorted(done, key=int)}:\n{m.tail()}"
    for pr in done:
        assert merged(m, pr) == heads[pr], f"212.1 (tree): #{pr} was merged at {merged(m, pr)}, not its head {heads[pr]}"
    lines = sorted((p["where"][0], p["where"][2], p["body"].strip()) for p in m.posted()
                   if p["body"].strip().startswith("Autopilot: merged"))
    want = sorted([("issue", N, MERGED_LINE), ("issue", "101", "Autopilot: merged PR #61"),
                   ("issue", "104", "Autopilot: merged PR #63")])
    assert lines == want, f"212.1 (tree): expected one Autopilot line on each of #57, #101 and #104 for its own " \
        f"pull request, found {lines}"
    on_64 = [p["body"] for p in m.posted() if p["where"][0] == "pr" and p["where"][2] == "64"]
    assert any(f"@{OWNER}" in b and RED_NAME.lower() in b.lower() for b in on_64), \
        f"212.1 (tree): #64, approved with a red check, does not say which check is red and mention the owner: {on_64}"
    no_bypass(m, "212.1", "tree")


def test_without_autopilot_an_approved_pull_request_waits_for_the_owner(record_property, tmp_path):
    """Off autopilot, an approved pull request with green checks still waits for the owner to merge it, as today.

    Runs the code review of #60, approving with green checks, on issue #57 without the autopilot label (it carries only
    "bug"). Nothing may be merged and no merge tried, no Autopilot line posted, the card must still say "Merge the pull
    request" and mention the owner, and the board must show Needs you. The same pull request after `/autopilot stop`
    is not merged either. Beside them, the same review on autopilot does merge."""
    record_property("proves", "212.2")
    m = Review(tmp_path / "off", PR_APPROVE, {57: ["bug"]}, GREEN)
    assert m.agent_started(), f"212.2: test setup: the code review never ran; it stopped at '{m.failed_step}':\n{m.tail()}"
    assert merged(m) is None and pr_state(m).get("calls", []) == [], \
        f"212.2: off autopilot the pull request was merged or a merge was tried: {pr_state(m).get('calls')}"
    assert autopilot_lines(m) == [], "212.2: an Autopilot line was posted for an issue not on autopilot"
    line = next_line(review_card(m))
    assert "Merge the pull request" in line and f"@{OWNER}" in line, \
        f"212.2: off autopilot the card no longer asks the owner to merge: {line!r}"
    assert m.board().endswith("needs"), f"212.2: off autopilot the board does not show Needs you: {m.board()!r}"

    m = Command(tmp_path / "stop", APPROVED, {57: [LABEL]}, GREEN)
    m.listen("/autopilot stop")
    assert merged(m) is None and autopilot_lines(m) == [], "212.2: /autopilot stop merged the approved pull request"

    m = Review(tmp_path / "on", PR_APPROVE, {57: ["bug", LABEL]}, GREEN)
    assert merged(m) == m.try_sha, f"212.2: test control: on autopilot the same review did not merge:\n{m.tail()}"


def test_a_refused_merge_stops_for_the_owner_and_says_why(record_property, tmp_path):
    """A merge that cannot happen stops for the owner: the pull request says why, mentions the owner and the card shows Needs you.

    Runs the code review of #60 on autopilot, approving, four ways: a red check (its name must be on the pull
    request), no checks at all (the pull request must say there are no checks), GitHub refusing for a conflict, and
    GitHub refusing for branch protection (its words must be on the pull request). Each must leave #60 unmerged, post
    no Autopilot line, mention the owner on #60 with the reason, show Needs you on the board and start nothing else.
    `/autopilot start` on an approved pull request with a red check must likewise merge nothing and say on #60 which
    check is red, mentioning the owner."""
    record_property("proves", "212.3")
    cases = (("red check", RED, "", RED_NAME), ("no checks", [], "", "no checks"),
             ("conflict", GREEN, CONFLICT, CONFLICT), ("branch protection", GREEN, PROTECTED, PROTECTED))
    for case, checks, refuse, reason in cases:
        m = Review(tmp_path / case.replace(" ", "-"), PR_APPROVE, {57: [LABEL]}, checks, refuse=refuse)
        assert m.agent_started(), f"212.3 ({case}): test setup: the code review never ran:\n{m.tail()}"
        assert_waits(m, "212.3", case, reason)
        assert m.board().endswith("needs"), f"212.3 ({case}): the board does not show Needs you: {m.board()!r}"
        assert m.dispatches() == [], f"212.3 ({case}): a refused merge started another stage: {m.dispatches()}"
    m = Command(tmp_path / "command-red", APPROVED, {}, RED)
    m.listen("/autopilot start")
    assert_waits(m, "212.3", "/autopilot start, red check", RED_NAME)


def test_agents_md_says_autopilot_merges_what_the_reviewer_approved(record_property):
    """AGENTS.md's flow says that on autopilot the reviewer's approval with green checks merges by itself.

    Reads AGENTS.md: step 6 of The flow (the Merge step, which today says only that the owner approves and merges)
    must mention autopilot."""
    record_property("proves", "212.4")
    text = open(os.path.join(ts.ROOT, "AGENTS.md")).read()
    sections = {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M)}
    flow = next((v for k, v in sections.items() if k.startswith("The flow")), "")
    step = next((l for l in flow.splitlines() if l.startswith("6.")), "")
    assert step, "212.4: AGENTS.md's The flow has no step 6"
    assert "merge" in step.lower() and "autopilot" in step.lower(), \
        f"212.4: step 6 of AGENTS.md's The flow does not say that autopilot merges an approved pull request: {step!r}"


def test_a_pull_request_changing_a_workflow_file_never_merges_by_autopilot(record_property, tmp_path):
    """A pull request that changes a workflow file waits for the owner even on autopilot with every check green.

    Runs the code review of #60 on autopilot, approving with green checks, where the pull request also changes
    .github/workflows/extra.yml; then `/autopilot start` on the same approved pull request. Neither may merge it or post
    an Autopilot line, and a comment on #60 must mention the owner. Beside them, the same review without the workflow
    file merges."""
    record_property("proves", "212.5")
    m = Review(tmp_path / "river", PR_APPROVE, {57: [LABEL]}, GREEN, workflow_file=True)
    assert m.agent_started(), f"212.5: test setup: the code review never ran:\n{m.tail()}"
    assert_waits(m, "212.5", "code review")
    assert m.board().endswith("needs"), f"212.5: the board does not show Needs you: {m.board()!r}"
    m = Command(tmp_path / "command", APPROVED, {}, GREEN, workflow_file=True)
    m.listen("/autopilot start")
    assert_waits(m, "212.5", "/autopilot start")
    m = Review(tmp_path / "control", PR_APPROVE, {57: [LABEL]}, GREEN)
    assert merged(m) == m.try_sha, f"212.5: test control: without a workflow file the review did not merge:\n{m.tail()}"


def test_nothing_merges_unless_every_check_on_the_merging_commit_is_green(record_property, tmp_path):
    """Nothing merges by autopilot unless every check on the very commit that merges has passed.

    On a repo where GitHub itself would merge anything, runs the code review of #60 on autopilot, approving, with: one
    red check beside a green one, one check still running, no checks at all, and green checks on the reviewed head but
    a new commit (its checks still running) pushed the moment code first looks. None may be merged. `/autopilot start`
    with a check still running merges nothing either. Beside them, every check green merges at that head."""
    record_property("proves", "212.6")
    cases = (("one red", RED, False), ("one running", PENDING, False), ("none", [], False), ("head moved", GREEN, True))
    for case, checks, moves in cases:
        m = Review(tmp_path / case.replace(" ", "-"), PR_APPROVE, {57: [LABEL]}, checks, moves=moves)
        assert m.agent_started(), f"212.6 ({case}): test setup: the code review never ran:\n{m.tail()}"
        assert merged(m) is None, \
            f"212.6 ({case}): merged commit {merged(m)} though not every check on it had passed: {pr_state(m)['checks']}"
        assert autopilot_lines(m) == [], f"212.6 ({case}): an Autopilot line was posted though nothing should merge"
        no_bypass(m, "212.6", case)
    m = Command(tmp_path / "command-running", APPROVED, {}, PENDING)
    m.listen("/autopilot start")
    assert merged(m) is None, "212.6 (/autopilot start, running): merged though a check was still running"
    m = Review(tmp_path / "green", PR_APPROVE, {57: [LABEL]}, GREEN)
    assert merged(m) == m.try_sha, f"212.6: test control: every check green did not merge at the head:\n{m.tail()}"
