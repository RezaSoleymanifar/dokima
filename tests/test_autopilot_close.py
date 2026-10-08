"""On autopilot, children start once their blockers merge, and the tree switches itself off when done (#213).

These tests run the workflows the way GitHub runs them, on the machine from test_start.py: every job's `if:` is
evaluated and its scripts run with bash against a fake `gh`. When an issue closes, every workflow in
.github/workflows/ that GitHub would start on `issues: closed` runs, with the event GitHub sends (github.event_name
`issues`, github.event.action `closed`, github.event.issue with its number, state, state_reason, labels and
parent_issue_url), started by the code owner who merged. The project board's variable is unset, so the board does
nothing. A command runs the listener, commands.yml, as test_autopilot.py does. Job and step `if:` expressions can use
what test_start.evaluate knows (no toJSON, no `.*` filters): read labels and the tree in a step's script.

The fake GitHub knows an issue tree and keeps it in tree.json, labels.json, states.json and deps.json:
  - `gh api repos/o/r/issues/N` gives the issue (id N*10, number, title, state, state_reason, labels,
    parent_issue_url); PATCH or POST on it with -f/-F state=closed (and state_reason=...) or --input closes it.
  - `gh api repos/o/r/issues/N/parent` gives its parent issue (404 when it has none).
  - `gh api repos/o/r/issues/N/sub_issues` lists its sub-issues; POST with sub_issue_id=ID adds one.
  - `gh api repos/o/r/issues/N/dependencies/blocked_by` lists the issues blocking it, each with its state; POST with
    issue_id=ID adds one.
  - labels change through `gh issue edit N --add-label/--remove-label` or the REST labels API, as in test_autopilot.
  - `gh issue view N` shows issue N (number, title, body, state, stateReason, labels, comments); `gh issue close N`
    closes it (--reason, -r, and --comment/-c, which posts that comment); `gh issue comment N` comments on it.
  - `gh api repos/o/r/actions/runs/ID` says whether run ID is still going (in_progress) or completed.
  - a signal to start a stage is `gh api repos/o/r/dispatches` with -f/-F event_type=... client_payload[...]=...,
    or --input with that JSON; every one is kept with the key it was sent with. Only Dokima's app key (the token an
    app-token step gives, fake-token) starts agent.yml: GitHub ignores a signal sent with the workflow's own token.
"""
import json
import os
import re

import test_autopilot as ta
import test_start as ts
from dokima import agent
from test_start import N, OWNER, Ctx, evaluate, condition

LABEL = "autopilot"
LINE = "Autopilot: blockers merged, starting plan"
WORKFLOWS = os.path.join(ts.ROOT, ".github", "workflows")

TREE_GH = r'''
def jload(name, default):
    p = os.path.join(d, name)
    return json.load(open(p)) if os.path.exists(p) else default
def jsave(name, obj):
    json.dump(obj, open(os.path.join(d, name), "w"), indent=1)
TREE, LABELS, STATES, DEPS = jload("tree.json", {}), jload("labels.json", {}), jload("states.json", {}), jload("deps.json", {})
def parent_of(n):
    return next((int(p) for p, cs in TREE.items() if int(n) in cs), None)
def issue_obj(n):
    n = int(n)
    st = STATES.get(str(n)) or {}
    p = parent_of(n)
    return {"id": n * 10, "node_id": f"I_{n}", "number": n, "title": f"Issue {n}", "state": st.get("state", "open"),
            "state_reason": st.get("reason"), "html_url": f"https://github.com/o/r/issues/{n}",
            "url": f"https://api.github.com/repos/o/r/issues/{n}",
            "parent_issue_url": f"https://api.github.com/repos/o/r/issues/{p}" if p else None,
            "labels": [{"name": l} for l in LABELS.get(str(n), [])]}
def method():
    return (flag("-X", "--method") or "GET").upper()
def fields():
    vals = {}
    for i, x in enumerate(a):
        if x in ("-f", "-F", "--field", "--raw-field") and i + 1 < len(a) and "=" in a[i + 1]:
            k, v = a[i + 1].split("=", 1)
            vals.setdefault(k, []).append(v)
    if "--input" in a:
        p = flag("--input")
        data = json.load(sys.stdin if p == "-" else open(p)) or {}
        for k, v in data.items():
            vals.setdefault(k, []).extend(v if isinstance(v, list) else [v])
    return vals
def num():
    for x in a[2:]:
        m = re.fullmatch(r"#?(\d+)|https://github.com/o/r/issues/(\d+)/?", x)
        if m:
            return m.group(1) or m.group(2)
    return ""
def one(f, k):
    v = f.get(k) or [None]
    return v[0]
def close(n, reason):
    STATES[str(n)] = {"state": "closed", "reason": reason or "completed"}
    jsave("states.json", STATES)
def jq(obj):
    q = flag("-q", "--jq")
    if q and re.fullmatch(r"\.[A-Za-z_]+", q.strip()):
        v = obj.get(q.strip()[1:], "")
        print(v if isinstance(v, str) else json.dumps(v))
    else:
        print(json.dumps(obj))
    sys.exit(0)
API = next((x.lstrip("/") for x in a[1:] if x.lstrip("/").startswith("repos/o/r/")), None) if a[:1] == ["api"] else None
API = API.split("?")[0] if API else None
if API == "repos/o/r/dispatches":
    f = fields()
    payload = {k[len("client_payload["):-1]: v[0] for k, v in f.items() if k.startswith("client_payload[")}
    if isinstance(one(f, "client_payload"), dict):
        payload.update(one(f, "client_payload"))
    open(os.path.join(d, "dispatches.jsonl"), "a").write(json.dumps(
        {"event_type": one(f, "event_type"), "payload": {k: str(v) for k, v in payload.items()}, "token": token}) + "\n")
    sys.exit(0)
m_run = re.fullmatch(r"repos/o/r/actions/runs/(\d+)", API or "")
if m_run:
    jq({"id": int(m_run.group(1)), "status": "in_progress" if m_run.group(1) in opts.get("running_runs", []) else "completed"})
m_par = re.fullmatch(r"repos/o/r/issues/(\d+)/parent", API or "")
if m_par:
    p = parent_of(m_par.group(1))
    if p is None:
        sys.stderr.write("HTTP 404: Not Found (https://api.github.com/%s)\n" % API)
        sys.exit(1)
    jq(issue_obj(p))
m_sub = re.fullmatch(r"repos/o/r/issues/(\d+)/sub_issues", API or "")
if m_sub:
    n = m_sub.group(1)
    if method() == "POST":
        TREE.setdefault(n, []).append(int(one(fields(), "sub_issue_id")) // 10)
        jsave("tree.json", TREE)
        jq(issue_obj(n))
    print(json.dumps([issue_obj(c) for c in TREE.get(n, [])]))
    sys.exit(0)
m_dep = re.fullmatch(r"repos/o/r/issues/(\d+)/dependencies/blocked_by", API or "")
if m_dep:
    n = m_dep.group(1)
    if method() == "POST":
        DEPS.setdefault(n, []).append(int(one(fields(), "issue_id")) // 10)
        jsave("deps.json", DEPS)
        jq(issue_obj(n))
    print(json.dumps([issue_obj(b) for b in DEPS.get(n, [])]))
    sys.exit(0)
m_lab = re.fullmatch(r"repos/o/r/issues/(\d+)/labels", API or "")
if m_lab:
    n = m_lab.group(1)
    if method() in ("POST", "PUT"):
        f = fields()
        new = [l["name"] if isinstance(l, dict) else l for l in (f.get("labels[]") or []) + (f.get("labels") or [])]
        have = [] if method() == "PUT" else LABELS.get(n, [])
        LABELS[n] = have + [l for l in new if l not in have]
        jsave("labels.json", LABELS)
    print(json.dumps([{"name": l} for l in LABELS.get(n, [])]))
    sys.exit(0)
m_one = re.fullmatch(r"repos/o/r/issues/(\d+)/labels/([^/]+)", API or "")
if m_one and method() == "DELETE":
    n, name = m_one.group(1), m_one.group(2)
    if name not in LABELS.get(n, []):
        sys.stderr.write("HTTP 404: Label does not exist (https://api.github.com/%s)\n" % API)
        sys.exit(1)
    LABELS[n] = [l for l in LABELS[n] if l != name]
    jsave("labels.json", LABELS)
    print(json.dumps([{"name": l} for l in LABELS.get(n, [])]))
    sys.exit(0)
m_iss = re.fullmatch(r"repos/o/r/issues/(\d+)", API or "")
if m_iss:
    n = m_iss.group(1)
    if method() in ("PATCH", "POST"):
        f = fields()
        if one(f, "state") == "closed":
            close(n, one(f, "state_reason"))
        elif one(f, "state") == "open":
            STATES.pop(n, None)
            jsave("states.json", STATES)
    jq(issue_obj(n))
if a[:2] == ["issue", "close"]:
    n = num()
    reason = (flag("--reason", "-r") or "completed").replace(" ", "_")
    close(n, reason)
    text = flag("--comment", "-c")
    if text:
        create("issue", n, text)
    sys.exit(0)
if a[:2] == ["issue", "edit"]:
    nums = []
    for x in a[2:]:
        if x.startswith("-"):
            break
        nums.append(x.rstrip("/").rsplit("/", 1)[-1].lstrip("#"))
    adds = [l.strip() for v in [a[i + 1] for i, x in enumerate(a) if x == "--add-label"] for l in v.split(",") if l.strip()]
    rems = [l.strip() for v in [a[i + 1] for i, x in enumerate(a) if x == "--remove-label"] for l in v.split(",") if l.strip()]
    for n in nums:
        have = [l for l in LABELS.get(n, []) if l not in rems]
        LABELS[n] = have + [l for l in adds if l not in have]
    jsave("labels.json", LABELS)
    print(f"https://github.com/o/r/issues/{nums[0] if nums else ''}")
    sys.exit(0)
if a[:2] == ["issue", "view"]:
    n = int(num())
    seed = json.load(open(os.path.join(d, "issue.json")))
    o = issue_obj(n)
    view = {"number": n, "title": seed["title"] if n == seed["number"] else o["title"],
            "body": seed["body"] if n == seed["number"] else "", "state": o["state"].upper(),
            "stateReason": (o["state_reason"] or "").upper(), "labels": o["labels"], "url": o["html_url"],
            "comments": (seed["comments"] if n == seed["number"] else []) + comments_on("issue", n)}
    jq(view)
'''


def fake_gh():
    """test_start's fake GitHub, taught the issue tree, states, blocked-by links, runs and signals."""
    anchor = 'if a[:2] == ["issue", "view"]:'
    fake = ts.FAKE_GH.replace(anchor, TREE_GH + anchor, 1)
    assert fake != ts.FAKE_GH, "test setup: could not teach the fake GitHub about the issue tree"
    return fake.replace("#!/usr/bin/env python3", f"#!{ts.sys.executable}")


def bot_comment(kind, number, body, cid):
    """A comment Dokima's bot already posted on an issue, as the fake GitHub keeps it."""
    return {"id": cid, "kind": kind, "number": number, "created": "2026-10-07T10:00:00.000000Z",
            "versions": [body], "author": agent.BOT}


def planned(n, cid):
    """A planner record the bot posted on issue n: the issue already has a plan."""
    return bot_comment("issue", n, agent.render(ts.planner_record(ts.STORY)), cid)


def running(n, run, cid):
    """A live card for a run still going on issue n: the planner is running there now."""
    body = f"{agent.LIVE}\n**Planner** · working\n\nThe agent is working.\n\n<sub>[run](https://github.com/o/r/actions/runs/{run})</sub>\n"
    return bot_comment("issue", n, body, cid)


def closes_on_issue_close(wf):
    """True when GitHub starts this workflow when an issue closes."""
    on = wf.get("on")
    if isinstance(on, str):
        return on == "issues"
    if isinstance(on, list):
        return "issues" in on
    if not isinstance(on, dict) or "issues" not in on:
        return False
    types = (on.get("issues") or {}).get("types") if isinstance(on.get("issues"), dict) else None
    return not types or "closed" in (types if isinstance(types, list) else [types])


class Repo(ts.Machine):
    """A repo whose fake GitHub knows one issue tree: who is under whom, labels, states, blocked-by links, comments."""

    def __init__(self, tmp, tree, labels=None, deps=None, closed=(), seed=(), history=None, running_runs=()):
        super().__init__(tmp, history or ta.HISTORY, actor=OWNER, options={"running_runs": [str(r) for r in running_runs]})
        t = self.tmp
        open(f"{t}/bin/gh", "w").write(fake_gh())
        json.dump({str(k): list(v) for k, v in tree.items()}, open(f"{t}/gh/tree.json", "w"))
        json.dump({str(k): list(v) for k, v in (labels or {}).items()}, open(f"{t}/gh/labels.json", "w"))
        json.dump({str(k): list(v) for k, v in (deps or {}).items()}, open(f"{t}/gh/deps.json", "w"))
        json.dump({str(n): {"state": "closed", "reason": "completed"} for n in closed}, open(f"{t}/gh/states.json", "w"))
        json.dump(list(seed), open(f"{t}/gh/comments.json", "w"))
        self.seeded = len(seed)
        self.runs, self.failures = 0, []

    listen = ta.Tree.listen

    def _json(self, name):
        path = f"{self.tmp}/gh/{name}"
        return json.load(open(path)) if os.path.exists(path) else {}

    def labels(self):
        """Every issue's labels now: {number: [names]}."""
        return {int(k): v for k, v in self._json("labels.json").items()}

    def on_autopilot(self):
        """The issues that carry the autopilot label now."""
        return {n for n, ls in self.labels().items() if LABEL in ls}

    def state(self, n):
        """("open", None) or ("closed", reason) for issue n, as GitHub holds it now."""
        st = self._json("states.json").get(str(n)) or {}
        return st.get("state", "open"), st.get("reason")

    def issue_event(self, n):
        """The issue as GitHub puts it in the event payload."""
        parent = next((int(p) for p, cs in self._json("tree.json").items() if int(n) in cs), None)
        state, reason = self.state(n)
        return {"number": int(n), "title": f"Issue {n}", "state": state, "state_reason": reason,
                "html_url": f"https://github.com/o/r/issues/{n}",
                "parent_issue_url": f"https://api.github.com/repos/o/r/issues/{parent}" if parent else None,
                "labels": [{"name": l} for l in self.labels().get(int(n), [])], "user": {"login": OWNER, "type": "User"}}

    def close(self, n):
        """Issue n closes as completed (its pull request merged); every workflow GitHub starts on that runs.

        Returns the names of the jobs that ran (were not skipped)."""
        states = self._json("states.json")
        states[str(n)] = {"state": "closed", "reason": "completed"}
        json.dump(states, open(f"{self.tmp}/gh/states.json", "w"))
        event = {"action": "closed", "issue": self.issue_event(n), "sender": {"login": OWNER, "type": "User"},
                 "repository": {"full_name": "o/r", "default_branch": "main", "name": "r", "owner": {"login": "o"}}}
        open(f"{self.tmp}/event.json", "w").write(json.dumps(event))
        github = Ctx(event_name="issues", actor=OWNER, event=event, run_id="42", run_attempt="1", ref="refs/heads/main",
                     server_url="https://github.com", repository="o/r", repository_owner="o", token="fake-github-token")
        ran = []
        for fname in sorted(os.listdir(WORKFLOWS)):
            if not fname.endswith((".yml", ".yaml")):
                continue
            wf = ts.load_yaml(open(os.path.join(WORKFLOWS, fname)).read())
            if not closes_on_issue_close(wf):
                continue
            jobs, results, outputs = wf.get("jobs") or {}, {}, {}
            while len(results) < len(jobs):
                progressed = False
                for name, job in jobs.items():
                    needs = job.get("needs") or []
                    needs = [needs] if isinstance(needs, str) else needs
                    if name in results or any(x not in results for x in needs):
                        continue
                    progressed = True
                    res = [results[x] for x in needs]
                    status = {"failed": "failure" in res, "success": all(r == "success" for r in res)}
                    ctx = {"github": github, "inputs": Ctx(), "vars": Ctx(DOKIMA_APP_ID="1"),
                           "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
                           "needs": Ctx({x: {"result": results[x], "outputs": outputs.get(x, {})} for x in needs})}
                    if not evaluate(condition(job.get("if")), ctx, status):
                        results[name] = "skipped"
                        continue
                    ran.append(f"{fname}:{name}")
                    if "uses" in job:
                        results[name] = "success"
                        continue
                    self.runs += 1
                    label = f"close{self.runs}-{fname}-{name}"
                    results[name], outputs[name] = self.run_job(label, job, ctx, "issues",
                                                                [("/tmp/", f"{self.tmp}/jobs/{label}/tmp/")], wf.get("defaults"))
                    if results[name] == "failure":
                        self.failures.append(f"{fname}:{name}")
                assert progressed, f"test setup: the jobs of {fname} wait on each other"
        self.failed = bool(self.failures)
        return ran

    def signals(self):
        """Every start signal sent: {event_type, payload, token}."""
        path = f"{self.tmp}/gh/dispatches.jsonl"
        return [json.loads(l) for l in open(path)] if os.path.exists(path) else []

    def planners_started(self, crit):
        """{issue number: how many times its planner was started}, counting only signals that start agent.yml."""
        started = {}
        for s in self.signals():
            p = s["payload"]
            if s["event_type"] != "dokima-next" or p.get("role") != "planner":
                continue
            assert s["token"] == "fake-token", (f"{crit}: the planner for #{p.get('issue')} was signalled with the "
                                                f"workflow's own token, which GitHub ignores; only Dokima's app key starts agent.yml")
            started[int(p["issue"])] = started.get(int(p["issue"]), 0) + 1
        return started

    def new_comments(self, n):
        """The bodies of the comments written on issue n since the test began, as they stand now."""
        return [c["versions"][-1] for c in self.comments()[self.seeded:] if c["kind"] == "issue" and c["number"] == int(n)]

    def autopilot_lines(self, n):
        """How many comments on issue n read exactly the Autopilot line."""
        return sum(1 for b in self.new_comments(n) if b.strip() == LINE)

    def any_autopilot_line(self):
        """Every new comment anywhere that starts with 'Autopilot:'."""
        return [(c["number"], c["versions"][-1]) for c in self.comments()[self.seeded:] if c["versions"][-1].strip().startswith("Autopilot:")]


def assert_started_exactly(m, crit, case, want, wont):
    """Each issue in `want` got its planner started once and one Autopilot line; no issue in `wont` got either."""
    started = m.planners_started(crit)
    for n in sorted(want):
        assert started.get(n) == 1, (f"{crit} ({case}): #{n}'s planner was started {started.get(n, 0)} times, expected "
                                     f"once; started: {started}\n{m.tail()}")
        assert m.autopilot_lines(n) == 1, (f"{crit} ({case}): #{n} got {m.autopilot_lines(n)} comments reading "
                                           f"'{LINE}', expected exactly one; its new comments: {m.new_comments(n)}")
    for n in sorted(wont):
        assert n not in started, f"{crit} ({case}): #{n}'s planner was started, though it must not be; started: {started}"
        assert m.autopilot_lines(n) == 0, f"{crit} ({case}): #{n} got an Autopilot line, though it must not start"


ALL = {57: [LABEL], 101: [LABEL], 102: [LABEL], 103: [LABEL], 104: [LABEL], 105: [LABEL]}


def test_a_close_starts_every_sibling_whose_blockers_have_all_merged(record_property, tmp_path):
    """When a child merges, every sibling it was the last blocker of starts planning, with one Autopilot line; the rest wait.

    #57 is on autopilot with sub-issues #101 to #105. #102 is blocked by #101; #105 by #101 and #110 (already
    closed, outside the tree); #103 by #101 and #104, which is still open; #104 already has a plan. When #101 closes,
    #102 and #105 must each have their planner started once by Dokima's signal and get exactly one comment reading the
    Autopilot line; #103 (still blocked), #104 (already planned), #101 and the parent #57 must not."""
    record_property("proves", "213.1")
    m = Repo(tmp_path / "close", {57: [101, 102, 103, 104, 105]}, ALL,
             deps={102: [101], 103: [101, 104], 105: [101, 110]}, closed=[110], seed=[planned(104, 4001)])
    m.close(101)
    assert not m.failed, f"213.1: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert_started_exactly(m, "213.1", "close", {102, 105}, {57, 101, 103, 104})


def test_a_split_filed_on_autopilot_starts_its_unblocked_stories(record_property, tmp_path):
    """When `/work` files a split on autopilot, each story with nothing to wait for starts planning; one that waits does not.

    Runs the listener on the code owner's `/work` on #57, whose approved split has two stories, the second blocked by
    the first. GitHub numbers them #900 and #901. With #57 on autopilot, #900 must have its planner started once and
    get one Autopilot line, and #901 neither. Beside it, the same `/work` with #57 not on autopilot starts neither
    story and posts no Autopilot line."""
    record_property("proves", "213.1")
    m = Repo(tmp_path / "on", {}, {57: [LABEL]}, history=ts.SPLIT_APPROVED)
    m.listen("/work")
    assert not m.failed, f"213.1 (split on autopilot): the listener failed on /work:\n{m.tail()}"
    assert json.load(open(f"{m.tmp}/gh/tree.json")).get("57") == [900, 901], \
        f"213.1 (split on autopilot): /work did not file the two stories as #900 and #901:\n{m.tail()}"
    assert_started_exactly(m, "213.1", "split on autopilot", {900}, {57, 901})

    m = Repo(tmp_path / "off", {}, {}, history=ts.SPLIT_APPROVED)
    m.listen("/work")
    assert not m.failed, f"213.1 (split off autopilot): the listener failed on /work:\n{m.tail()}"
    assert m.planners_started("213.1") == {}, f"213.1 (split off autopilot): a story started: {m.planners_started('213.1')}"
    assert m.any_autopilot_line() == [], f"213.1 (split off autopilot): an Autopilot line was posted: {m.any_autopilot_line()}"


def test_autopilot_start_on_a_parent_picks_up_the_children_waiting(record_property, tmp_path):
    """`/autopilot start` on a parent starts every child with no plan and nothing open to wait for; a blocked child waits.

    #57 has sub-issues #101 (no blockers), #102 (blocked by #101, still open) and #103 (blocked by #110, already
    closed), none planned. After the code owner's `/autopilot start` on #57, #101 and #103 must each have their planner
    started once and get one Autopilot line; #102 and #57 itself must not. Beside it, `/autopilot stop` on the same
    tree starts nothing and posts no Autopilot line."""
    record_property("proves", "213.1")
    tree, deps = {57: [101, 102, 103]}, {102: [101], 103: [110]}
    m = Repo(tmp_path / "start", tree, {}, deps=deps, closed=[110])
    m.listen("/autopilot start")
    assert not m.failed, f"213.1 (/autopilot start): the listener failed:\n{m.tail()}"
    assert_started_exactly(m, "213.1", "/autopilot start", {101, 103}, {57, 102})

    m = Repo(tmp_path / "stop", tree, {57: [LABEL], 101: [LABEL], 102: [LABEL], 103: [LABEL]}, deps=deps, closed=[110])
    m.listen("/autopilot stop")
    assert not m.failed, f"213.1 (/autopilot stop): the listener failed:\n{m.tail()}"
    assert m.planners_started("213.1") == {}, f"213.1 (/autopilot stop): a child started: {m.planners_started('213.1')}"
    assert m.any_autopilot_line() == [], f"213.1 (/autopilot stop): an Autopilot line was posted: {m.any_autopilot_line()}"


def test_the_parent_closes_when_its_last_sub_issue_closes(record_property, tmp_path):
    """When the last open sub-issue merges the parent closes as completed with one comment that its tree is done; before that it stays open.

    #57 is on autopilot with #101 and #102. With #102 already closed, closing #101 must close #57 as completed and
    leave exactly one new comment on #57 that says its tree is done (it names the tree and says done). With #102 still
    open, closing #101 must leave #57 open, with no new comment, and #57 and #102 still on autopilot."""
    record_property("proves", "213.2")
    labels = {57: [LABEL], 101: [LABEL], 102: [LABEL]}
    m = Repo(tmp_path / "done", {57: [101, 102]}, labels, closed=[102])
    m.close(101)
    assert not m.failed, f"213.2 (last one): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert m.state(57) == ("closed", "completed"), \
        f"213.2 (last one): #57 is {m.state(57)} after its last open sub-issue closed, expected closed as completed\n{m.tail()}"
    said = m.new_comments(57)
    assert len(said) == 1, f"213.2 (last one): #57 got {len(said)} new comments, expected one saying its tree is done: {said}"
    assert "tree" in said[0].lower() and "done" in said[0].lower(), \
        f"213.2 (last one): #57's comment does not say its whole tree is done: {said[0]!r}"

    m = Repo(tmp_path / "not-yet", {57: [101, 102]}, labels)
    m.close(101)
    assert not m.failed, f"213.2 (one left): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert m.state(57)[0] == "open", f"213.2 (one left): #57 closed while #102 is still open"
    assert m.new_comments(57) == [], f"213.2 (one left): #57 got comments while #102 is still open: {m.new_comments(57)}"
    assert {57, 102} <= m.on_autopilot(), \
        f"213.2 (one left): the tree went off autopilot while #102 is still open: on autopilot now {sorted(m.on_autopilot())}"


def test_autopilot_goes_off_for_the_whole_tree_when_it_is_done(record_property, tmp_path):
    """When the tree is done, the parent and every sub-issue go off autopilot; a lone issue goes off when it closes.

    #57 is on autopilot with #101 and #102 (#102 already closed, #101 also labelled bug); #58, outside the tree, is
    on autopilot too. Closing #101 must take #57, #101 and #102 off autopilot, keep #101's bug label and leave #58 on.
    Then #57, on autopilot with no parent and no sub-issues, closes: it must go off autopilot while #58 stays on."""
    record_property("proves", "213.3")
    m = Repo(tmp_path / "tree", {57: [101, 102]}, {57: [LABEL], 101: [LABEL, "bug"], 102: [LABEL], 58: [LABEL]}, closed=[102])
    m.close(101)
    assert not m.failed, f"213.3 (tree): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    left = m.on_autopilot() & {57, 101, 102}
    assert left == set(), f"213.3 (tree): the done tree left these issues on autopilot: {sorted(left)}\n{m.tail()}"
    assert "bug" in m.labels().get(101, []), "213.3 (tree): switching autopilot off removed #101's other label"
    assert 58 in m.on_autopilot(), "213.3 (tree): #58, outside the done tree, went off autopilot"

    m = Repo(tmp_path / "single", {}, {57: [LABEL], 58: [LABEL]})
    m.close(57)
    assert not m.failed, f"213.3 (single): a workflow failed when #57 closed: {m.failures}\n{m.tail()}"
    assert 57 not in m.on_autopilot(), f"213.3 (single): #57, with no sub-issues, stayed on autopilot after it closed\n{m.tail()}"
    assert 58 in m.on_autopilot(), "213.3 (single): #58, an unrelated issue, went off autopilot"


def test_a_close_off_autopilot_does_nothing(record_property, tmp_path):
    """Off autopilot a close starts no sibling, closes no parent and posts no Autopilot line; on autopilot the same close does.

    The same two trees as above, once with no issue on autopilot and once with all of them on. Tree one: #57 with #101
    and #102, #102 blocked by #101. Tree two: #57 with #101 and #102, #102 already closed. Closing #101 off autopilot
    must start no planner, post no comment starting 'Autopilot:', leave #57 open with no new comment, and fail no
    workflow. On autopilot, the same close starts #102 in tree one and closes #57 in tree two."""
    record_property("proves", "213.4")
    for on in (False, True):
        case = "on autopilot" if on else "off autopilot"
        labels = {57: [LABEL], 101: [LABEL], 102: [LABEL]} if on else {}
        m = Repo(tmp_path / f"blocked-{on}", {57: [101, 102]}, labels, deps={102: [101]})
        m.close(101)
        assert not m.failed, f"213.4 ({case}, sibling): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
        started = m.planners_started("213.4")
        if on:
            assert started == {102: 1}, f"213.4 ({case}, sibling): #102 should start once when #101 closes: {started}\n{m.tail()}"
        else:
            assert started == {}, f"213.4 ({case}, sibling): a close off autopilot started planners: {started}"
            assert m.any_autopilot_line() == [], f"213.4 ({case}, sibling): Autopilot lines were posted: {m.any_autopilot_line()}"

        m = Repo(tmp_path / f"last-{on}", {57: [101, 102]}, labels, closed=[102])
        m.close(101)
        assert not m.failed, f"213.4 ({case}, parent): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
        if on:
            assert m.state(57)[0] == "closed", f"213.4 ({case}, parent): #57 did not close with its last sub-issue\n{m.tail()}"
        else:
            assert m.state(57)[0] == "open", f"213.4 ({case}, parent): #57 closed though it is not on autopilot"
            assert m.new_comments(57) == [], f"213.4 ({case}, parent): #57 got comments: {m.new_comments(57)}"
            assert m.any_autopilot_line() == [], f"213.4 ({case}, parent): Autopilot lines were posted: {m.any_autopilot_line()}"


def test_a_child_planned_running_or_done_is_never_started_again(record_property, tmp_path):
    """A close never starts a child that already has a plan, a run going or is closed, and two closes start a child only once.

    #57 is on autopilot with #101, #102, #104, #106, #107 and #108, all blocked by #101. #104 already has a plan,
    #106 is already closed, #107 has a planner run still going, #108 has a plan and is about to merge, and #102 is
    waiting. Closing #101 must start #102 once and none of the others. Closing #108 right after must not start #102
    again: across both closes #102's planner starts once and #102 gets one Autopilot line."""
    record_property("proves", "213.5")
    tree = {57: [101, 102, 104, 106, 107, 108]}
    labels = {n: [LABEL] for n in (57, 101, 102, 104, 106, 107, 108)}
    deps = {n: [101] for n in (102, 104, 106, 107, 108)}
    m = Repo(tmp_path / "twice", tree, labels, deps=deps, closed=[106],
             seed=[planned(104, 4001), planned(108, 4002), running(107, 777, 4003)], running_runs=[777])
    m.close(101)
    assert not m.failed, f"213.5: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert_started_exactly(m, "213.5", "first close", {102}, {104, 106, 107, 108})
    m.close(108)
    assert not m.failed, f"213.5: a workflow failed when #108 closed: {m.failures}\n{m.tail()}"
    assert_started_exactly(m, "213.5", "second close", {102}, {104, 106, 107})
