"""An approved plan runs every check on its pull request's head again by itself (#440).

GitHub runs a pull request's checks only when it gets a new commit, so a plan approved with nothing new to push keeps
the checks that ran before the approval. agent.yml's step "Run the plan check again once the plan is approved" calls
`python3 -m dokima.agent recheck N OUT` once the plan review's record is up; these tests run that command, as the
workflow does, against a fake `gh` on PATH that keeps GitHub in one JSON file.

The fake GitHub holds issue #57, whose pull request #60 is open on try/issue-57 (unless the test closes it), and the
GitHub Actions runs on its head. It answers the calls Dokima may use for this, logging every call and every call it
does not understand:
  - the pull request: `gh pr list` (with --head, --state, --json, -q), `gh pr view 60|try/issue-57`,
    `gh api repos/o/r/pulls[?head=..&state=..]` and `gh api repos/o/r/pulls/60`;
  - the runs: `gh api repos/o/r/actions/runs[?head_sha=..&event=..&status=..]`,
    `gh api repos/o/r/actions/workflows/FILE/runs[?...]`, `gh api repos/o/r/actions/runs/ID`, `gh run list` and
    `gh run view ID`; a run still going finishes by itself after it was read three times, as GitHub's would;
  - stopping and re-running: `gh api -X POST repos/o/r/actions/runs/ID/cancel|rerun|rerun-failed-jobs`,
    `gh run cancel ID` and `gh run rerun ID [--failed]`. GitHub refuses to re-run a run that is still going
    ("This workflow is already running (HTTP 403)"), and a run the test listed under "refuse" with the reason given;
  - comments: `gh pr comment 60 --body|--body-file` and `gh api repos/o/r/issues/N/comments -f body=..`;
  - the repo's owner: `gh api repos/o/r`, `gh api users/o` and `gh api orgs/o` (404 for a personal account).
-q/--jq takes a plain path like `.[0].number`, `.head.sha` or `.workflow_runs[].id`.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
N, PR = 57, 60
HEAD = "a" * 40
OLD = "b" * 40
PERMISSION = "gh: Resource not accessible by integration (HTTP 403)"
OTHER = "gh: Unable to retry this workflow run because it was created over a month ago (HTTP 403)"

FAKE_GH = r'''#!@@PYTHON@@
import json, os, re, sys
STATE = os.environ["FAKE_GH_STATE"]
s = json.load(open(STATE))
a = sys.argv[1:]
s["calls"].append(a)

def save():
    json.dump(s, open(STATE, "w"), indent=1)

def fail(msg, code=1):
    save()
    sys.stderr.write(msg + "\n")
    sys.exit(code)

def unsupported():
    s["unsupported"].append(a)
    fail("fake gh does not support this call (HTTP 400)")

def flag(*names):
    for i, x in enumerate(a):
        if x in names and i + 1 < len(a):
            return a[i + 1]
        for n in names:
            if n.startswith("--") and x.startswith(n + "="):
                return x.split("=", 1)[1]
    return None

def jq(obj, q):
    out = [obj]
    for name, idx in re.findall(r"\.([A-Za-z_]\w*)|\[(\d*)\]", q):
        nxt = []
        for o in out:
            if name:
                nxt.append(o.get(name) if isinstance(o, dict) else None)
            elif idx == "":
                nxt.extend(o if isinstance(o, list) else [])
            else:
                nxt.append(o[int(idx)] if isinstance(o, list) and int(idx) < len(o) else None)
        out = nxt
    return out

def reply(obj):
    q = flag("-q", "--jq")
    save()
    if q is None:
        print(json.dumps(obj))
    else:
        if not re.fullmatch(r"(\.([A-Za-z_]\w*)?|\[\d*\])+", q.strip()):
            unsupported()
        for v in jq(obj, q.strip()):
            if v is not None:
                print(v if not isinstance(v, (dict, list)) else json.dumps(v))
    sys.exit(0)

def pr_json():
    return {"number": 60, "headRefName": "try/issue-57", "headRefOid": s["head"], "body": "Closes #57",
            "state": "OPEN" if s["pr_open"] else "CLOSED", "url": "https://github.com/o/r/pull/60"}

def pr_rest():
    return {"number": 60, "state": "open" if s["pr_open"] else "closed", "body": "Closes #57",
            "head": {"sha": s["head"], "ref": "try/issue-57"}, "html_url": "https://github.com/o/r/pull/60"}

def rest_run(r):
    return {"id": r["id"], "name": r["name"], "path": r["path"], "event": r["event"], "head_sha": r["head_sha"],
            "head_branch": "try/issue-57", "status": r["status"], "conclusion": r["conclusion"],
            "run_attempt": r["run_attempt"], "workflow_id": abs(hash(r["path"])) % 100000,
            "html_url": f"https://github.com/o/r/actions/runs/{r['id']}"}

def seen(r):
    if r["status"] == "completed" or r.get("rerun_started"):
        return
    r["reads"] = r.get("reads", 0) + 1
    if r["reads"] > 3:
        r.update(status="completed", conclusion="success")

def find(rid):
    r = next((r for r in s["runs"] if r["id"] == int(rid)), None)
    if r is None:
        fail("gh: Not Found (HTTP 404)")
    return r

def listed(workflow, q):
    out = [r for r in s["runs"] if not workflow or r["path"].endswith("/" + workflow.split("/")[-1]) or r["name"] == workflow]
    for key, field in (("head_sha", "head_sha"), ("event", "event")):
        if q.get(key):
            out = [r for r in out if r[field] == q[key]]
    if q.get("branch"):
        out = [r for r in out if q["branch"] == "try/issue-57"]
    if q.get("status"):
        out = [r for r in out if r["status"] == q["status"] or r["conclusion"] == q["status"]]
    for r in out:
        seen(r)
    return sorted(out, key=lambda r: -r["id"])

def query(path):
    q = {}
    if "?" in path:
        for part in path.split("?", 1)[1].split("&"):
            k, _, v = part.partition("=")
            q[k] = v
    for i, x in enumerate(a):
        if x in ("-f", "-F", "--raw-field", "--field") and i + 1 < len(a) and "=" in a[i + 1]:
            k, _, v = a[i + 1].partition("=")
            q[k] = v
    return q

def cancel(rid):
    r = find(rid)
    s["log"].append(["cancel", r["id"]])
    if r["status"] != "completed":
        r.update(status="completed", conclusion="cancelled")

def rerun(rid, failed_only):
    r = find(rid)
    if str(r["id"]) in s["refuse"]:
        fail(s["refuse"][str(r["id"])])
    if r["status"] != "completed":
        fail("gh: This workflow is already running (HTTP 403)")
    s["log"].append(["rerun", r["id"]])
    r["reruns"].append({"failed_only": failed_only})
    r.update(status="queued", conclusion=None, run_attempt=r["run_attempt"] + 1, rerun_started=True)

def comment(n, body):
    s["comments"].append({"number": int(n), "body": body})

def body_arg():
    b = flag("--body", "-b")
    if b is not None:
        return b
    f = flag("--body-file", "-F")
    if f is not None:
        return sys.stdin.read() if f == "-" else open(f).read()
    unsupported()

if a[:2] == ["pr", "list"]:
    head = flag("--head", "-H")
    state = (flag("--state", "-s") or "open").lower()
    prs = [pr_json()] if (head in (None, "try/issue-57") and (state == "all" or (state == "open") == s["pr_open"])) else []
    reply(prs)
if a[:2] == ["pr", "view"]:
    if not s["pr_open"] and "try/issue-57" in a:
        fail('no pull requests found for branch "try/issue-57"')
    reply(pr_json())
if a[:2] == ["pr", "comment"]:
    comment(60, body_arg())
    save()
    print("https://github.com/o/r/pull/60#issuecomment-1")
    sys.exit(0)
if a[:2] == ["run", "list"]:
    rs = listed(flag("--workflow", "-w"), {"head_sha": flag("--commit", "-c"), "branch": flag("--branch", "-b"),
                                           "status": flag("--status", "-s"), "event": flag("--event", "-e")})
    rs = rs[: int(flag("-L", "--limit") or 20)]
    reply([{"databaseId": r["id"], "headSha": r["head_sha"], "status": r["status"], "conclusion": r["conclusion"] or "",
            "workflowName": r["name"], "name": r["name"], "event": r["event"], "number": r["id"],
            "attempt": r["run_attempt"], "headBranch": "try/issue-57",
            "url": f"https://github.com/o/r/actions/runs/{r['id']}"} for r in rs])
if a[:2] == ["run", "view"]:
    r = find(next(x for x in a[2:] if x.isdigit()))
    seen(r)
    reply({"databaseId": r["id"], "status": r["status"], "conclusion": r["conclusion"] or "", "headSha": r["head_sha"],
           "workflowName": r["name"], "event": r["event"], "attempt": r["run_attempt"]})
if a[:2] == ["run", "cancel"]:
    cancel(next(x for x in a[2:] if x.isdigit()))
    save()
    sys.exit(0)
if a[:2] == ["run", "rerun"]:
    rerun(next(x for x in a[2:] if x.isdigit()), "--failed" in a)
    save()
    sys.exit(0)
if a[:1] == ["api"]:
    path = next((x.lstrip("/") for x in a[1:] if re.match(r"/?(repos|users|orgs)/", x)), "")
    bare = path.split("?", 1)[0]
    if bare == "repos/o/r":
        reply({"full_name": "o/r", "name": "r", "owner": {"login": "o", "type": s["owner_type"]}})
    if bare == "users/o":
        reply({"login": "o", "type": s["owner_type"]})
    if bare == "orgs/o":
        if s["owner_type"] != "Organization":
            fail("gh: Not Found (HTTP 404)")
        reply({"login": "o"})
    if bare == "repos/o/r/pulls":
        q = query(path)
        open_ = q.get("state", "open") in ("open", "all") and s["pr_open"] or q.get("state") in ("closed", "all") and not s["pr_open"]
        reply([pr_rest()] if open_ and q.get("head", "o:try/issue-57") == "o:try/issue-57" else [])
    if bare == "repos/o/r/pulls/60":
        reply(pr_rest())
    m = re.fullmatch(r"repos/o/r/actions/runs/(\d+)/(cancel|rerun|rerun-failed-jobs|force-cancel)", bare)
    if m:
        if m.group(2) in ("cancel", "force-cancel"):
            cancel(m.group(1))
        else:
            rerun(m.group(1), m.group(2) == "rerun-failed-jobs")
        save()
        print("{}")
        sys.exit(0)
    m = re.fullmatch(r"repos/o/r/actions/runs/(\d+)", bare)
    if m:
        r = find(m.group(1))
        seen(r)
        reply(rest_run(r))
    m = re.fullmatch(r"repos/o/r/actions/(?:workflows/([^/]+)/)?runs", bare)
    if m:
        rs = [rest_run(r) for r in listed(m.group(1), query(path))]
        reply({"total_count": len(rs), "workflow_runs": rs})
    m = re.fullmatch(r"repos/o/r/issues/(\d+)/comments", bare)
    if m and ("POST" in a or any(x in ("-f", "-F", "--raw-field", "--field", "--input") for x in a)):
        q = query(path)
        body = q.get("body", "")
        if body.startswith("@"):
            body = sys.stdin.read() if body == "@-" else open(body[1:]).read()
        if not body and "--input" in a:
            f = flag("--input")
            body = json.load(sys.stdin if f == "-" else open(f)).get("body", "")
        comment(m.group(1), body)
        save()
        print("{}")
        sys.exit(0)
unsupported()
'''


def run(rid, name, path, sha=HEAD, event="pull_request_target", status="completed", conclusion="failure"):
    """One GitHub Actions run, as the fake GitHub keeps it."""
    return {"id": rid, "name": name, "path": f".github/workflows/{path}", "event": event, "head_sha": sha,
            "status": status, "conclusion": conclusion if status == "completed" else None, "run_attempt": 1,
            "reruns": []}


def plan_check(rid, **kw):
    """A run of the plan check (done-whens.yml)."""
    return run(rid, "done-whens", "done-whens.yml", **kw)


def all_tests(rid, **kw):
    """A run of All tests (full-suite.yml)."""
    return run(rid, "full suite", "full-suite.yml", **kw)


class Recheck:
    """`python3 -m dokima.agent recheck 57 OUT` after an approved plan review, against the fake GitHub.

    `runs` are on GitHub, `refuse` maps a run id to the reason GitHub gives when asked to run it again, `pr_open` says
    whether pull request #60 is open and `owner_type` is the repo owner's kind (Organization or User)."""

    def __init__(self, tmp, runs, refuse=None, pr_open=True, owner_type="Organization"):
        os.makedirs(tmp / "bin")
        os.makedirs(tmp / "out")
        self.state_file = tmp / "gh.json"
        json.dump({"head": HEAD, "pr_open": pr_open, "owner_type": owner_type, "runs": runs,
                   "refuse": {str(k): v for k, v in (refuse or {}).items()}, "calls": [], "unsupported": [],
                   "comments": [], "log": []}, open(self.state_file, "w"))
        gh = tmp / "bin" / "gh"
        gh.write_text(FAKE_GH.replace("@@PYTHON@@", sys.executable))
        os.chmod(gh, 0o755)
        record = {"role": "reviewer", "stage": "plan", "issue": N, "check": {"passed": True, "problems": []},
                  "handback": {"verdict": "approve", "summary": "The plan proves every criterion."}}
        (tmp / "out" / "record.json").write_text(json.dumps(record))
        env = {**os.environ, "PATH": f"{tmp / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}",
               "FAKE_GH_STATE": str(self.state_file), "GITHUB_REPOSITORY": "o/r", "GITHUB_REPOSITORY_OWNER": "o",
               "GH_TOKEN": "fake-token", "PYTHONPATH": ROOT}
        self.proc = subprocess.run([sys.executable, "-m", "dokima.agent", "recheck", str(N), str(tmp / "out")],
                                   cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        self.state = json.load(open(self.state_file))

    def runs(self):
        """Every run as GitHub holds it now, by id."""
        return {r["id"]: r for r in self.state["runs"]}

    def rerun(self, rid):
        """True when run `rid` was run again in full (all its jobs), at least once."""
        return any(not x["failed_only"] for x in self.runs()[rid]["reruns"])

    def comments(self):
        """Every comment posted, on the pull request or anywhere else."""
        return self.state["comments"]

    def why(self):
        """What the command saw and did, for a failure message."""
        return (f"\nexit {self.proc.returncode}\nstdout: {self.proc.stdout[-1500:]}\nstderr: {self.proc.stderr[-1500:]}"
                f"\ncalls the fake GitHub does not support: {self.state['unsupported']}"
                f"\ncomments: {self.comments()}\nruns: {json.dumps(self.state['runs'], indent=1)[-2500:]}")


def test_every_check_on_the_head_runs_again_with_no_comment(record_property, tmp_path):
    """Every check on the head runs again by itself, even one still running.

    Proves 440.1. Approves the plan with three checks on the pull request's head: the plan check and All tests, both finished and
    red, and the board's run still going from the last push. Each must be run again in full (not only its failed
    jobs); the one still running is stopped or waited for and then run again, after its earlier run ended, since a
    run that started before the approval may have read the plan before it. Nothing is posted anywhere: no comment and
    no step for the owner."""
    record_property("proves", "440.1")
    m = Recheck(tmp_path, [plan_check(7001), all_tests(7002),
                           run(7003, "board", "board.yml", status="in_progress")])
    assert m.proc.returncode == 0, f"440.1: the recheck command failed{m.why()}"
    for rid, name in ((7001, "the plan check"), (7002, "All tests"), (7003, "the board's run still going")):
        assert m.rerun(rid), f"440.1: {name} (run {rid}) on the head {HEAD[:7]} was not run again in full{m.why()}"
    assert ["rerun", 7003] in m.state["log"], f"440.1: the run still going was never run again{m.why()}"
    assert not m.comments(), f"440.1: the checks ran again, yet something was posted: {m.comments()}{m.why()}"


def test_a_refusal_for_lack_of_permission_names_the_setting_once(record_property, tmp_path):
    """A refusal for lack of permission gets one comment naming the setting, with its link.

    Proves 440.2. GitHub refuses both checks on the head with "Resource not accessible by integration (HTTP 403)", the answer an
    installation gives when it has not accepted Actions: Read and write. The pull request must get exactly one comment
    (not one per check) saying Dokima's GitHub App needs Actions set to Read and write, accepted on its installation,
    with the link to the installations page: the organization's for a repo an organization owns, the account's own
    for a personal repo. Both owners are tried, so a link that fits only one fails."""
    record_property("proves", "440.2")
    links = {"Organization": "https://github.com/organizations/o/settings/installations",
             "User": "https://github.com/settings/installations"}
    for owner_type, link in links.items():
        m = Recheck(tmp_path / owner_type, [plan_check(7001), all_tests(7002)],
                    refuse={7001: PERMISSION, 7002: PERMISSION}, owner_type=owner_type)
        assert m.proc.returncode == 0, f"440.2 ({owner_type}): the recheck command failed{m.why()}"
        on_pr = [c["body"] for c in m.comments() if c["number"] == PR]
        assert len(m.comments()) == 1 and len(on_pr) == 1, \
            f"440.2 ({owner_type}): expected one comment on PR #60, got {m.comments()}{m.why()}"
        text = on_pr[0].lower()
        for words in ("dokima", "github app", "actions", "read and write", "accept"):
            assert words in text, f"440.2 ({owner_type}): the comment does not say '{words}': {on_pr[0]!r}"
        assert link in on_pr[0], f"440.2 ({owner_type}): the comment does not link {link}: {on_pr[0]!r}"
        other = [l for t, l in links.items() if t != owner_type][0]
        assert other not in on_pr[0], f"440.2 ({owner_type}): the comment links the wrong owner's page {other}: {on_pr[0]!r}"


def test_with_no_open_pull_request_nothing_runs_and_nothing_is_posted(record_property, tmp_path):
    """With no open pull request, nothing runs and nothing is posted.

    Proves 440.3. The branch try/issue-57 still has red checks from a pull request that was closed. Approving the plan must ask
    GitHub to stop or run nothing and post nothing. The same checks with the pull request open do all run again, so
    this does not pass by doing nothing at all."""
    record_property("proves", "440.3")
    m = Recheck(tmp_path / "closed", [plan_check(7001), all_tests(7002)], pr_open=False)
    assert m.proc.returncode == 0, f"440.3: the recheck command failed with no open pull request{m.why()}"
    assert not m.state["log"], f"440.3: with no open pull request, runs were stopped or run again: {m.state['log']}{m.why()}"
    assert not m.comments(), f"440.3: with no open pull request, something was posted: {m.comments()}{m.why()}"
    opened = Recheck(tmp_path / "open", [plan_check(7001), all_tests(7002)])
    assert opened.rerun(7001) and opened.rerun(7002), \
        f"440.3: with the pull request open, its checks did not all run again{opened.why()}"


def test_a_rerun_refused_for_another_reason_says_githubs_reason(record_property, tmp_path):
    """A re-run refused for another reason says why, in GitHub's own words.

    Proves 440.4. GitHub refuses to run All tests again for a reason that is not permission. The pull request must get one comment
    carrying GitHub's own reason, and it must not send the owner to the permission setting, which would not help. The
    plan check, which GitHub accepts, still runs again."""
    record_property("proves", "440.4")
    m = Recheck(tmp_path, [plan_check(7001), all_tests(7002)], refuse={7002: OTHER})
    assert m.proc.returncode == 0, f"440.4: the recheck command failed{m.why()}"
    on_pr = [c["body"] for c in m.comments() if c["number"] == PR]
    assert len(on_pr) == 1, f"440.4: expected one comment on PR #60 saying why All tests could not run again, got {m.comments()}{m.why()}"
    assert "Unable to retry this workflow run because it was created over a month ago" in on_pr[0], \
        f"440.4: the comment does not carry GitHub's own reason: {on_pr[0]!r}"
    assert "read and write" not in on_pr[0].lower(), \
        f"440.4: a refusal that is not about permission sent the owner to the permission setting: {on_pr[0]!r}"
    assert m.rerun(7001), f"440.4: the plan check, which GitHub accepted, did not run again{m.why()}"


def test_only_the_newest_run_of_each_check_from_a_push_runs_again(record_property, tmp_path):
    """Only the newest run of each check a push started runs again, once.

    Proves 440.5. Nothing else is stopped or run again. On the head: two runs of the plan check (only the newer is the check the pull request shows), All tests, and
    runs a review, a comment and a finished check started, which a re-run would repeat (a command run would start an
    agent again). On an older commit: a plan check. Exactly the newer plan check and All tests run again, each once,
    and every other run is left as it was."""
    record_property("proves", "440.5")
    runs = [plan_check(7000, sha=OLD), plan_check(7001), plan_check(7002), all_tests(7003),
            run(7004, "commands", "commands.yml", event="pull_request_review"),
            run(7005, "reviews", "reviews.yml", event="pull_request_review"),
            run(7006, "commands", "commands.yml", event="issue_comment"),
            run(7007, "board", "board.yml", event="workflow_run")]
    m = Recheck(tmp_path, runs)
    assert m.proc.returncode == 0, f"440.5: the recheck command failed{m.why()}"
    now = m.runs()
    for rid in (7002, 7003):
        assert len(now[rid]["reruns"]) == 1 and m.rerun(rid), \
            f"440.5: run {rid}, the newest of its check on the head, did not run again exactly once{m.why()}"
    for rid, what in ((7000, "the plan check on an older commit"), (7001, "an older run of the plan check on the head"),
                      (7004, "a run a review started (commands)"), (7005, "a run a review started (reviews)"),
                      (7006, "a run a comment started"), (7007, "a run another check's end started")):
        assert not now[rid]["reruns"] and ["cancel", rid] not in m.state["log"], \
            f"440.5: {what}, run {rid}, was stopped or run again{m.why()}"
