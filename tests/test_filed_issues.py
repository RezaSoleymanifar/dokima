"""Every issue an agent finds outside its own is filed by code at the end of its run, parked and labeled (#268).

Before this, only a review could list issues it found, and they stayed proposals on its card until someone filed them
by hand (a `/issue` command was only planned). #222 showed the cost: the no-PR bug was found, never filed, and broke
main. Now the planner's plan.json, the worker's work.json and the reviewer's review.json all take the same field,
issues_found ({title, why, evidence}), and the run that hands them back files each one once its hand-back passes.

These tests run the agents through the whole agent workflow (.github/workflows/agent.yml), the way GitHub runs it,
with the machine from test_start.py and the fake GitHub of test_automerge.py, on issue #57. The "plan" machine holds
#57 planned, its plan approved and `/work` said, with no pull request; the "pr" machine holds the same story built as
pull request #60. The fake Claude Code hands back what the test chose, in the file of the run's role; a planner also
writes its one test (tests/test_x.py::test_a, failing today), so its hand-back passes the planner's check. Runs can
follow one another on the same machine, so a later run sees what an earlier one filed.

Every key the workflow makes is told apart: each app-token step gives the key `key-<its id>` (key-app for the one
made after the agent), so a test can see which key filed an issue.

The fake GitHub is taught to keep the issues code files (filed.json: number from 900 up, title, body, labels, state,
and the key and PASSED the call was made with) and the repo's labels (repo_labels.json). It answers:
  - `gh issue create` with --title/-t, --body/-b or --body-file/-F, and --label/-l (repeatable, comma-separated);
    like gh, it refuses a label the repo does not have ("could not add label: 'X' not found");
  - `gh api -X POST repos/o/r/issues` with -f/-F title=, body= (or body=@file), labels[]=, or --input JSON; like
    GitHub's REST API, it creates a label the repo does not have yet;
  - `gh api repos/o/r/issues` (GET, labels= and state= in the query string or as -f fields, --paginate allowed) and
    `gh issue list` with --label/-l, --state/-s and --json (no --jq, no --search), listing the filed issues with
    their bodies;
  - `gh label create NAME` (refused when it exists, unless --force) and `gh api -X POST repos/o/r/labels` with
    name= (422 when it exists), `gh api repos/o/r/labels` and `gh api repos/o/r/labels/NAME` (404 when missing);
  - labels added after an issue is created (`gh issue edit N --add-label`, the issue labels API) count too.
A test can make GitHub refuse every new issue (fail_create), with the message GitHub would give.
"""
import json
import os
import re
import sys

import test_automerge as tam
import test_start as ts
from dokima import agent
from test_start import N, PR, Ctx

LABEL = "filed-by-dokima"
PARKED = "parked"
EXISTING = ["autopilot", "blocker", "high"]
REFUSED = "HTTP 502: Server Error (https://api.github.com/repos/o/r/issues)"
ROLES = ("planner", "worker", "reviewer")
WORKFLOWS = ["agent.yml", "assign.yml", "autopilot.yml", "board.yml", "card.yml", "commands.yml", "done-whens.yml",
             "full-suite.yml", "planner.yml", "wiki.yml", "worker.yml"]

FIND_A = {"title": "The board drops closed pull requests", "why": "Cards for merged work go stale on the board.",
          "evidence": "dokima/board.py:121 asks only for OPEN pull requests"}
FIND_B = {"title": "A cancelled run leaves its queued card behind", "why": "The owner sees a run that never ends.",
          "evidence": "dokima/agent.py:290 queue() never removes the card"}
FIND_C = {"title": "Footnotes lose the run link on retries", "why": "The owner cannot open the retried run.",
          "evidence": "dokima/agent.py:518 footnote() reads run only once"}
FIND_D = {"title": "The wiki step skips renamed pages", "why": "A renamed page keeps its old title on the wiki.",
          "evidence": "dokima/trail.py:40 matches pages by file name only"}

PLANNER_TEST = '''def test_a(record_property):
    """The fix is in."""
    record_property("proves", "57.1")
    assert False, "57.1: the fix is not built yet"
'''

FILED_GH = r'''
FILED = jload("filed.json", [])
REPO_LABELS = jload("repo_labels.json", [])
def save_filed():
    jsave("filed.json", FILED)
    jsave("repo_labels.json", REPO_LABELS)
def filed_labels(i):
    return i["labels"] + [l for l in LABELS.get(str(i["number"]), []) if l not in i["labels"]]
def filed_obj(i):
    n = i["number"]
    return {"id": n * 10, "node_id": f"I_{n}", "number": n, "title": i["title"], "body": i["body"], "state": i["state"],
            "state_reason": None, "html_url": f"https://github.com/o/r/issues/{n}",
            "url": f"https://api.github.com/repos/o/r/issues/{n}", "labels": [{"name": l} for l in filed_labels(i)]}
def new_filed(title, body, labels):
    if opts.get("fail_create"):
        sys.stderr.write(opts["fail_create"] + "\n")
        sys.exit(1)
    i = {"number": 900 + len(FILED), "title": title or "", "body": body or "", "labels": labels, "state": "open",
         "token": KEY, "passed": os.environ.get("PASSED", "")}
    FILED.append(i)
    save_filed()
    return i
def filed_list(want, st):
    return [i for i in FILED if all(l in filed_labels(i) for l in want) and st in ("all", i["state"])]
def split_labels(vals):
    return [l.strip() for v in vals for l in v.split(",") if l.strip()]
def file_body(v):
    if v and v.startswith("@") and os.path.exists(v[1:]):
        return open(v[1:]).read()
    return v
if a[:2] == ["issue", "create"]:
    body = open(flag("--body-file", "-F")).read() if flag("--body-file", "-F") else flag("--body", "-b")
    labels = split_labels([a[k + 1] for k, x in enumerate(a[:-1]) if x in ("--label", "-l")])
    missing = [l for l in labels if l not in REPO_LABELS]
    if missing:
        sys.stderr.write(f"could not add label: '{missing[0]}' not found\n")
        sys.exit(1)
    print(filed_obj(new_filed(flag("--title", "-t"), body, labels))["html_url"])
    sys.exit(0)
if API == "repos/o/r/issues" and method() == "POST":
    f = fields()
    labels = [l["name"] if isinstance(l, dict) else l for l in (f.get("labels[]") or []) + (f.get("labels") or [])]
    REPO_LABELS += [l for l in labels if l not in REPO_LABELS]
    jq(filed_obj(new_filed(one(f, "title"), file_body(one(f, "body")), labels)))
if API == "repos/o/r/issues" and method() == "GET":
    import urllib.parse
    q = dict(urllib.parse.parse_qsl(RAW.split("?", 1)[1])) if "?" in RAW else {}
    q.update({k: v[0] for k, v in fields().items()})
    print(json.dumps([filed_obj(i) for i in filed_list(split_labels([q.get("labels") or ""]), (q.get("state") or "open").lower())]))
    sys.exit(0)
if a[:2] == ["issue", "list"]:
    want = split_labels([a[k + 1] for k, x in enumerate(a[:-1]) if x in ("--label", "-l")])
    print(json.dumps([{"number": o["number"], "title": o["title"], "body": o["body"], "state": o["state"].upper(),
                       "labels": o["labels"], "url": o["html_url"]}
                      for o in (filed_obj(i) for i in filed_list(want, (flag("--state", "-s") or "open").lower()))]))
    sys.exit(0)
if a[:2] == ["label", "create"]:
    name = a[2]
    if name in REPO_LABELS and "--force" not in a and "-f" not in a:
        sys.stderr.write(f"label with name \"{name}\" already exists; use `--force` to update its color and description\n")
        sys.exit(1)
    if name not in REPO_LABELS:
        REPO_LABELS.append(name)
    save_filed()
    sys.exit(0)
if API == "repos/o/r/labels":
    if method() == "POST":
        name = one(fields(), "name")
        if name in REPO_LABELS:
            sys.stderr.write("HTTP 422: Validation Failed (https://api.github.com/repos/o/r/labels)\nalready_exists\n")
            sys.exit(1)
        REPO_LABELS.append(name)
        save_filed()
        jq({"name": name})
    print(json.dumps([{"name": l} for l in REPO_LABELS]))
    sys.exit(0)
m_rl = re.fullmatch(r"repos/o/r/labels/([^/]+)", API or "")
if m_rl:
    import urllib.parse
    name = urllib.parse.unquote(m_rl.group(1))
    if name not in REPO_LABELS:
        sys.stderr.write("HTTP 404: Not Found (https://api.github.com/%s)\n" % API)
        sys.exit(1)
    jq({"name": name})
'''

FAKE_CLAUDE = r'''#!/usr/bin/env python3
"""A stand-in for Claude Code: hands back what the test chose, in the file of the run's role.

A planner also writes its one test, failing today, so its hand-back passes the planner's check. Like the fake of
test_start.py, it keeps its own environment (agent-env.json) and leaves a session log naming its model."""
import json, os, shutil
d = os.environ["FAKE_GH_DIR"]
json.dump(dict(os.environ), open(os.path.join(d, "agent-env.json"), "w"))
open(os.environ["FAKE_CLAUDE_MARK"], "w").write("started")
role = os.environ["ROLE"]
name = {"planner": "plan.json", "worker": "work.json", "reviewer": "review.json"}[role]
os.makedirs(os.environ["OUT"], exist_ok=True)
shutil.copy(os.environ["FAKE_REVIEW"], os.path.join(os.environ["OUT"], name))
test = os.path.join(d, "planner-test.py")
if role == "planner" and os.path.exists(test):
    os.makedirs("tests", exist_ok=True)
    shutil.copy(test, os.path.join("tests", "test_x.py"))
logs = os.path.join(os.environ["HOME"], ".claude", "projects", "p")
os.makedirs(logs, exist_ok=True)
open(os.path.join(logs, "s.jsonl"), "w").write(json.dumps({"message": {"model": os.environ["MODEL"], "role": "assistant", "content": "Done."}}) + "\n")
print(json.dumps({"num_turns": 1, "duration_ms": 1000, "usage": {}}))
'''


KEYS_GH = r'''
KEY = token
if token.startswith("key-"):
    token = os.environ["GH_TOKEN"] = "fake-token"
'''


def fake_gh():
    """test_automerge's fake GitHub, taught to file issues, list them with their bodies and keep the repo's labels.

    Every app key (`key-<step id>`) counts as Dokima's app key, as fake-token does; the one a call came with is KEY."""
    fake = tam.fake_gh()
    taught = fake
    for anchor, extra in (('token = os.environ.get("GH_TOKEN", "")\n', KEYS_GH),
                          ('API = API.split("?")[0] if API else None\n', FILED_GH)):
        before = taught
        taught = taught.replace(anchor, anchor + extra, 1)
        assert taught != before, "test setup: could not teach the fake GitHub to file issues"
    return taught


def keyed(job):
    """The job with each app-token step giving its own key, `key-<step id>`, so a filed issue shows which key made it."""
    steps = []
    for s in job["steps"]:
        if "create-github-app-token" in str(s.get("uses")):
            s = {k: v for k, v in s.items() if k not in ("uses", "with")}
            s["name"] = f"Make the key {s['id']}"
            s["run"] = (f'echo "token=key-{s["id"]}" >> "$GITHUB_OUTPUT"; '
                        f'echo "app-slug=dokima-runtime" >> "$GITHUB_OUTPUT"')
        steps.append(s)
    return {**job, "steps": steps}


def plan_handback(*found, tests=True):
    """A planner's plan for #57 (one criterion, its test tests/test_x.py::test_a) listing these issues found outside it.

    With tests=False the planner writes no test, so the planner's check rejects the plan."""
    return {**ts.STORY, "summary": "Stuck issues get unstuck.", "issues_found": [dict(f) for f in found],
            "_tests": tests}


def work_handback(*found, summary="Built it. The fix is in x.py."):
    """A worker's hand-back for #57 listing these issues found outside it; an empty summary is rejected by the check."""
    return {"summary": summary, "criteria": {"57.1": "x.py"}, "evidence": "pytest: 1 passed",
            "issues_found": [dict(f) for f in found]}


def plan_review(*found, verdict="approve"):
    """A plan review of #57's one-story plan that lists these issues found outside it."""
    return {**ts.APPROVE, "verdict": verdict, "asks": [{**ts.APPROVE["asks"][0], "criterion": "57.1"}],
            "issues_found": [dict(f) for f in found]}


def code_review(*found):
    """A code review of pull request #60 that approves it and lists these issues found outside it."""
    return {**tam.review_pr("approve"), "issues_found": [dict(f) for f in found]}


class Agents(tam.Merges, ts.Machine):
    """Issue #57, planned, its plan approved and `/work` said (and, at the pr stage, built as pull request #60), on
    which agents run through agent.yml.

    `labels` gives each issue's labels ({57: ["autopilot"]} puts #57 on autopilot); `repo_labels` the labels the
    repo has; `options` the fake GitHub's options (fail_create)."""

    def __init__(self, tmp, stage, labels=None, repo_labels=None, options=None):
        super().__init__(tmp, [], try_branch=True, options={"pr_open": stage == "pr", **(options or {})})
        t, self.stage, self.runs = self.tmp, stage, 0
        open(f"{t}/bin/gh", "w").write(fake_gh())
        open(f"{t}/bin/claude", "w").write(FAKE_CLAUDE.replace("#!/usr/bin/env python3", f"#!{sys.executable}"))
        for tool in ("gh", "claude"):
            os.chmod(f"{t}/bin/{tool}", 0o755)
        seed = tam.history(57, 60)
        if stage == "pr":
            json.dump({PR: tam.pr_state(57, tam.GREEN)}, open(f"{t}/gh/prs.json", "w"))
        else:
            seed = seed[:3]
            json.dump({}, open(f"{t}/gh/prs.json", "w"))
        json.dump(seed, open(f"{t}/gh/comments.json", "w"))
        self.seeded = len(seed)
        json.dump({str(k): list(v) for k, v in (labels or {}).items()}, open(f"{t}/gh/labels.json", "w"))
        have = list(EXISTING + [PARKED, LABEL] if repo_labels is None else repo_labels)
        json.dump(have, open(f"{t}/gh/repo_labels.json", "w"))
        json.dump([], open(f"{t}/gh/filed.json", "w"))

    def base_env(self, event_name):
        """The machine's environment, where git also pushes with the app key the workflow makes after the agent."""
        env = super().base_env(event_name)
        return {**env, "GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_1": env["GIT_CONFIG_KEY_0"],
                "GIT_CONFIG_VALUE_1": "https://x-access-token:key-app@github.com/o/r.git"}

    def run(self, role, handback):
        """One run of agent.yml by `role` (the reviewer grading this machine's stage), handing back `handback`;
        returns the job's result."""
        t = self.tmp
        self.runs += 1
        self.role = role
        self.before = len(self.comments())
        stage = self.stage if role == "reviewer" else ""
        handback = dict(handback)
        tests = handback.pop("_tests", True)
        if role == "planner" and tests:
            open(f"{t}/gh/planner-test.py", "w").write(PLANNER_TEST)
        elif os.path.exists(f"{t}/gh/planner-test.py"):
            os.remove(f"{t}/gh/planner-test.py")
        json.dump(handback, open(f"{t}/review.json", "w"))
        open(f"{t}/event.json", "w").write(json.dumps({"inputs": {"role": role, "stage": stage, "issue": N}}))
        ctx = {"inputs": Ctx(role=role, stage=stage, issue=N),
               "github": Ctx(event_name="workflow_dispatch", actor=ts.OWNER, event=Ctx(), run_id="42", run_attempt="1",
                             server_url="https://github.com", repository="o/r", token="fake-github-token"),
               "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
               "vars": Ctx(DOKIMA_APP_ID="1"), "needs": Ctx()}
        wf = ts.workflow("agent.yml")
        self.failed_step = None
        self.result, _ = self.run_job(f"{role}{self.runs}", keyed(wf["jobs"]["run"]), ctx, "workflow_dispatch",
                                      [("/tmp/", f"{t}/run{self.runs}/"), ("/home/runner/", f"{t}/home/")], wf.get("defaults"))
        return self.result

    def filed(self):
        """Every issue filed so far, oldest first: {number, title, body, labels (all it carries now), state, token, passed}."""
        later = json.load(open(f"{self.tmp}/gh/labels.json"))
        out = []
        for i in json.load(open(f"{self.tmp}/gh/filed.json")):
            extra = [l for l in later.get(str(i["number"]), []) if l not in i["labels"]]
            out.append({**i, "labels": i["labels"] + extra})
        return out

    def close_filed(self, number):
        """Filed issue `number` is closed on GitHub, as the owner would close it."""
        rows = json.load(open(f"{self.tmp}/gh/filed.json"))
        for i in rows:
            if i["number"] == number:
                i["state"] = "closed"
        json.dump(rows, open(f"{self.tmp}/gh/filed.json", "w"))

    def record(self):
        """The comment carrying the newest run's record, as it stands now: {id, kind, number, body, passed}, or None."""
        for c in self.comments()[self.before:]:
            body = c["versions"][-1]
            recs = agent.records([{"author": {"login": c["author"]}, "body": body}])
            if recs and recs[0].get("role") == self.role:
                return {"id": c["id"], "kind": c["kind"], "number": c["number"], "body": body,
                        "passed": recs[0]["check"]["passed"]}
        return None


def ran(m, crit, case):
    """The run finished, its hand-back passed and its record was posted; otherwise the test fails here saying why."""
    rec = m.record()
    assert rec, f"{crit} ({case}): the {m.role} run posted no record of its own:\n{m.tail()}"
    assert rec["passed"], f"{crit} ({case}): code rejected the {m.role}'s hand-back, so this case proves nothing:\n{rec['body']}"


def titles(m):
    """The titles of every issue filed so far, oldest first."""
    return [i["title"] for i in m.filed()]


def shown(m):
    """The newest run's record comment as the owner reads it, without its folded JSON."""
    return re.sub(r"```json\n.*?\n```", "", m.record()["body"], flags=re.S)


def every_agent(tmp_path, *found, **kw):
    """One run of each agent on its own fresh machine, each handing back these findings: [(case, machine)]."""
    out = []
    for case, role, stage, handback in (("planner", "planner", "plan", plan_handback(*found)),
                                        ("plan review", "reviewer", "plan", plan_review(*found)),
                                        ("worker", "worker", "pr", work_handback(*found)),
                                        ("code review", "reviewer", "pr", code_review(*found))):
        m = Agents(tmp_path / case.replace(" ", "-"), stage, **kw)
        m.run(role, handback)
        out.append((case, m))
    return out


def test_every_issue_any_agent_finds_is_filed_parked_and_labeled(record_property, tmp_path):
    """Each issue the planner, the worker or a review finds is filed by itself in that run, parked and labeled filed-by-dokima.

    Runs the planner, a plan review, the worker and a code review of #57, each finding two issues, with no owner
    command after any, and checks each run filed exactly one issue per finding, titled with the finding's own title,
    carrying exactly the labels parked and filed-by-dokima and nothing else. It runs the same four on a repo that has
    neither label yet, and checks the issues are filed with both all the same. Beside them, each agent handing back
    no finding files nothing. Each agent's prompt names the same field, issues_found, with a title, why and evidence."""
    record_property("proves", "268.1")
    wrong = []
    for repo, kw in (("repo with the labels", {}), ("repo without the labels", {"repo_labels": EXISTING})):
        for case, m in every_agent(tmp_path / repo.replace(" ", "-"), FIND_A, FIND_B, **kw):
            ran(m, "268.1", f"{case}, {repo}")
            if titles(m) != [FIND_A["title"], FIND_B["title"]]:
                wrong.append(f"{case} ({repo}) found two issues but did not file exactly those two by their titles; "
                             f"filed: {titles(m)}")
            wrong += [f"{case} ({repo}): filed issue #{i['number']} carries {i['labels']}, not exactly parked and {LABEL}"
                      for i in m.filed() if sorted(i["labels"]) != sorted([LABEL, PARKED])]
    for case, m in every_agent(tmp_path / "none"):
        ran(m, "268.1", f"{case}, nothing found")
        if titles(m):
            wrong.append(f"{case} found nothing yet filed issues: {titles(m)}")
    for role in ROLES:
        prompt = open(os.path.join(ts.ROOT, "dokima", "roles", f"{role}.md")).read()
        if not re.search(r'"issues_found":\s*\[\{"title":\s*"[^"]*",\s*"why":\s*"[^"]*",\s*"evidence":', prompt):
            wrong.append(f"dokima/roles/{role}.md does not give the {role}'s hand-back the field "
                         '"issues_found": [{"title": ..., "why": ..., "evidence": ...}]')
    assert not wrong, "268.1: " + "\n268.1: ".join(wrong)


def test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record(record_property, tmp_path):
    """Each filed issue names the issue (and pull request) it was found on and the agent, and links that run's record.

    Runs the planner, a plan review, the worker and a code review, each finding two issues, then reads each filed
    issue's body: it must name #57 (and #60 for the worker and the code review, which work on the pull request), name
    the agent that found it and no other agent, hold the finding's why and evidence, and link the very comment on
    GitHub that carries that run's record, by its address on the issue or pull request it is on."""
    record_property("proves", "268.2")
    wrong = []
    where = {"planner": ["#57"], "plan review": ["#57"], "worker": ["#57", "#60"], "code review": ["#57", "#60"]}
    for case, m in every_agent(tmp_path, FIND_A, FIND_B):
        ran(m, "268.2", case)
        rec = m.record()
        link = re.compile(rf"https://github\.com/o/r/(?:issues|pull)/{rec['number']}#issuecomment-{rec['id']}(?!\d)")
        if len(m.filed()) != 2:
            wrong.append(f"{case}: expected 2 filed issues, got {titles(m)}")
            continue
        for i, f in zip(m.filed(), (FIND_A, FIND_B)):
            body = i["body"]
            wrong += [f"{case}: filed issue #{i['number']} does not say it was found on {w}:\n{body}"
                      for w in where[case] if not re.search(rf"{w}(?!\d)", body)]
            if not re.search(rf"\b{m.role}\b", body, re.I):
                wrong.append(f"{case}: filed issue #{i['number']} does not say the {m.role} found it:\n{body}")
            others = [r for r in ROLES if r != m.role and re.search(rf"\b{r}\b", body, re.I)]
            if others:
                wrong.append(f"{case}: filed issue #{i['number']} names the {', '.join(others)}, not only the {m.role} "
                             f"that found it:\n{body}")
            if f["why"] not in body or f["evidence"] not in body:
                wrong.append(f"{case}: filed issue #{i['number']} lacks the finding's why or evidence:\n{body}")
            if not link.search(body):
                wrong.append(f"{case}: filed issue #{i['number']} does not link the run's record comment "
                             f"(#{rec['number']}, comment {rec['id']}):\n{body}")
    assert not wrong, "268.2: " + "\n268.2: ".join(wrong)


def test_a_filed_issue_gets_nothing_more_than_filing(record_property, tmp_path):
    """A filed issue gets no links, no autopilot and no run: it is not a sub-issue, blocks nothing, and nothing starts on it.

    Runs the planner, a plan review, the worker and a code review, each finding two issues, while #57 is on autopilot
    (so the river goes on to the next stage of #57), and checks for every run that both findings were filed, that no
    sub-issue or blocked-by link was made for any filed issue, that no stage was signalled to start on any filed
    issue, and that no filed issue carries the autopilot label."""
    record_property("proves", "268.3")
    wrong = []
    for case, m in every_agent(tmp_path, FIND_A, FIND_B, labels={57: ["autopilot"]}):
        ran(m, "268.3", f"{case} on autopilot")
        filed = {i["number"] for i in m.filed()}
        if len(filed) != 2:
            wrong.append(f"{case}: the run did not file its two findings; filed: {titles(m)}")
            continue
        ids = {str(n * 10) for n in filed} | {f"I_{n}" for n in filed}
        for call in m.calls():
            text = " ".join(call)
            if call[:1] == ["api"] and ("sub_issues" in text or "dependencies" in text):
                touched = {int(x) for x in re.findall(r"repos/o/r/issues/(\d+)/", text)}
                given = set(re.findall(r"(?:sub_issue_id|issue_id)=(\S+)", text))
                if touched & filed or given & ids:
                    wrong.append(f"{case}: a filed issue was linked into the graph: {call}")
            if call[:2] == ["issue", "edit"] and any(x in call for x in map(str, filed)) and "autopilot" in text:
                wrong.append(f"{case}: a filed issue was put on autopilot: {call}")
        started = [d for d in m.dispatches()
                   if any(re.search(rf"client_payload\[issue\]=({'|'.join(map(str, filed))})$", x) for x in d)]
        if started:
            wrong.append(f"{case}: a stage was started on a filed issue: {started}")
        wrong += [f"{case}: filed issue #{i['number']} went on autopilot: {i['labels']}"
                  for i in m.filed() if "autopilot" in i["labels"]]
    assert not wrong, "268.3: " + "\n268.3: ".join(wrong)


def test_the_same_finding_is_never_filed_twice(record_property, tmp_path):
    """The same finding is filed once: not twice in one run, and not again by a later run of any agent, even once closed.

    On one issue, the planner lists one finding twice (its title in other letter case and spacing) beside another: two
    issues are filed. The first is then closed. A plan review finds it again (case and spacing changed again, a new
    why) beside a new finding, then the worker finds the second one again beside another new one: each later run files
    only its new finding. The same is checked on a pull request, a code review finding again what the worker filed."""
    record_property("proves", "268.4")
    m = Agents(tmp_path / "issue", "plan")
    again = dict(FIND_A, title="  the BOARD drops   closed pull requests ", why="Said another way.")
    m.run("planner", plan_handback(FIND_A, again, FIND_B))
    ran(m, "268.4", "planner")
    assert titles(m) == [FIND_A["title"], FIND_B["title"]], \
        f"268.4: a planner listing a finding twice did not file it exactly once beside the other; filed: {titles(m)}"
    m.close_filed(m.filed()[0]["number"])
    m.run("reviewer", plan_review(dict(FIND_A, title="The board drops closed  PULL requests", why="Found again."), FIND_C))
    ran(m, "268.4", "plan review after the planner")
    assert titles(m) == [FIND_A["title"], FIND_B["title"], FIND_C["title"]], \
        (f"268.4: a plan review finding an already filed (and closed) issue again filed it twice, or did not file its "
         f"new finding; filed: {titles(m)}\n{m.tail()}")
    m.run("worker", work_handback(dict(FIND_B, title=FIND_B["title"].upper()), FIND_D))
    ran(m, "268.4", "worker after the plan review")
    assert titles(m) == [FIND_A["title"], FIND_B["title"], FIND_C["title"], FIND_D["title"]], \
        (f"268.4: a worker finding an issue the planner filed again filed it twice, or did not file its new finding; "
         f"filed: {titles(m)}\n{m.tail()}")

    p = Agents(tmp_path / "pr", "pr")
    p.run("worker", work_handback(FIND_A))
    ran(p, "268.4", "worker on the pull request")
    p.run("reviewer", code_review(dict(FIND_A, title=" the board DROPS closed pull requests"), FIND_C))
    ran(p, "268.4", "code review after the worker")
    assert titles(p) == [FIND_A["title"], FIND_C["title"]], \
        f"268.4: a code review finding what the worker filed filed it twice, or missed its new finding; filed: {titles(p)}"


def test_the_card_names_each_filed_issue(record_property, tmp_path):
    """The run's card names each filed issue by its number and no longer calls the findings proposals.

    Runs the planner, a plan review, the worker and a code review, each finding two issues, and reads each run's record
    comment as it ends up on GitHub, without its folded JSON: it must link each filed issue by number and must not
    say the findings are proposals."""
    record_property("proves", "268.5")
    wrong = []
    for case, m in every_agent(tmp_path, FIND_A, FIND_B):
        ran(m, "268.5", case)
        if len(m.filed()) != 2:
            wrong.append(f"{case}: the run did not file its two findings; filed: {titles(m)}")
            continue
        text = shown(m)
        wrong += [f"{case}: the card does not name filed issue #{i['number']}:\n{text}"
                  for i in m.filed() if not re.search(rf"#{i['number']}(?!\d)", text)]
        if "proposal" in text.lower():
            wrong.append(f"{case}: the card still calls the findings proposals:\n{text}")
    assert not wrong, "268.5: " + "\n268.5: ".join(wrong)


def test_a_finding_github_refuses_to_file_says_why_on_the_card(record_property, tmp_path):
    """When GitHub refuses to file a finding, the run's card still posts and names that finding with GitHub's reason.

    Runs the planner, a plan review, the worker and a code review, each finding one issue while GitHub refuses every
    new issue, and checks each run's record is still posted and, outside its folded JSON, names the finding and
    carries GitHub's error message."""
    record_property("proves", "268.5")
    wrong = []
    for case, m in every_agent(tmp_path, FIND_A, options={"fail_create": REFUSED}):
        ran(m, "268.5", f"{case}, GitHub refuses")
        assert titles(m) == [], f"test setup: GitHub refused every issue, yet some were filed: {titles(m)}"
        text = shown(m)
        if FIND_A["title"] not in text or "HTTP 502" not in text:
            wrong.append(f"{case}: the card does not say the finding was not filed and GitHub's reason:\n{text}")
    assert not wrong, "268.5: " + "\n268.5: ".join(wrong)


def test_a_rejected_handback_files_nothing(record_property, tmp_path):
    """A planner, worker or reviewer hand-back that code rejects files none of the issues it lists, and no new workflow or job is added.

    Runs a planner whose plan comes with no test, a worker whose hand-back has no summary and a plan review whose
    verdict code does not accept, each listing two issues, and checks each was rejected and filed nothing; beside each,
    the same agent with a good hand-back files both. The repo's workflows stay the ones it has today, and the agent
    workflow keeps its one job, so the filing happens in the run that checks the hand-back."""
    record_property("proves", "268.6")
    wrong = []
    for case, role, stage, bad, good in (
            ("planner", "planner", "plan", plan_handback(FIND_A, FIND_B, tests=False), plan_handback(FIND_A, FIND_B)),
            ("worker", "worker", "pr", work_handback(FIND_A, FIND_B, summary=""), work_handback(FIND_A, FIND_B)),
            ("plan review", "reviewer", "plan", plan_review(FIND_A, FIND_B, verdict="maybe"), plan_review(FIND_A, FIND_B))):
        no = Agents(tmp_path / f"{role}-{stage}-bad", stage)
        no.run(role, bad)
        rec = no.record()
        if not rec:
            wrong.append(f"{case}: the rejected run posted no record:\n{no.tail()}")
        elif rec["passed"]:
            wrong.append(f"test setup: the {case}'s bad hand-back passed its check")
        if titles(no):
            wrong.append(f"{case}: a hand-back code rejected filed issues: {titles(no)}")
        yes = Agents(tmp_path / f"{role}-{stage}-good", stage)
        yes.run(role, good)
        ran(yes, "268.6", f"good {case}")
        if titles(yes) != [FIND_A["title"], FIND_B["title"]]:
            wrong.append(f"{case}: the same agent with a good hand-back did not file its findings; filed: {titles(yes)}")
    have = sorted(os.listdir(os.path.join(ts.ROOT, ".github", "workflows")))
    if have != WORKFLOWS:
        wrong.append(f"the repo's workflows changed: {have}, not {WORKFLOWS}")
    jobs = list(ts.workflow("agent.yml")["jobs"])
    if jobs != ["run"]:
        wrong.append(f"agent.yml now has the jobs {jobs}, not its one job run")
    assert not wrong, "268.6: " + "\n268.6: ".join(wrong)


def test_the_key_that_files_is_made_only_after_the_agent_and_the_check(record_property, tmp_path):
    """Issues are filed with a key made only after the agent and the hand-back check finished, and the agent holds none.

    Runs the planner, a plan review, the worker and a code review, each finding two issues, with every key the
    workflow makes told apart by the step that made it. For every filed issue it checks the key that filed it was made
    by a step that comes after both the agent's step and the hand-back check in agent.yml, that the filing happened
    once the check had passed, and that the agent's own environment held no key at all."""
    record_property("proves", "268.7")
    steps = keyed(ts.workflow("agent.yml")["jobs"]["run"])["steps"]
    at = {s.get("id"): k for k, s in enumerate(steps) if s.get("id")}
    names = [s.get("name") for s in steps]
    after = max(names.index("The agent (Claude Code)"), names.index("Code checks the hand-back"))
    wrong = []
    for case, m in every_agent(tmp_path, FIND_A, FIND_B):
        ran(m, "268.7", case)
        if len(m.filed()) != 2:
            wrong.append(f"{case}: the run did not file its two findings; filed: {titles(m)}")
            continue
        for i in m.filed():
            made_by = i["token"][len("key-"):] if i["token"].startswith("key-") else None
            if made_by not in at or at[made_by] <= after:
                wrong.append(f"{case}: filed issue #{i['number']} was filed with {i['token']!r}, not a key made after "
                             "the agent and the hand-back check")
            if i["passed"] != "true":
                wrong.append(f"{case}: filed issue #{i['number']} was filed before the hand-back check had passed "
                             f"(PASSED={i['passed']!r})")
        env = json.load(open(f"{m.tmp}/gh/agent-env.json"))
        held = [k for k, v in env.items() if str(v).startswith("key-") or k in ("GH_TOKEN", "GITHUB_TOKEN")]
        if held:
            wrong.append(f"{case}: the agent held a key while it ran: {held}")
    assert not wrong, "268.7: " + "\n268.7: ".join(wrong)
