"""Every issue the reviewer finds outside the one it reviews is filed by code right away, parked and labeled (#265).

Before this, an issue the reviewer found stayed a proposal on its card until someone filed it by hand (a `/issue`
command was only planned). #222 showed the cost: the no-PR bug was found, never filed, and broke main.

These tests run a review through the whole agent workflow (.github/workflows/agent.yml), the way GitHub runs it, with
the machine from test_start.py and the fake GitHub of test_automerge.py, on issue #57 (a plan review) or its pull
request #60 (a code review). The fake Claude Code hands back the review the test chose. Two reviews can run one after
the other on the same machine, so a later review sees what an earlier one filed.

The fake GitHub is taught to keep the issues code files (filed.json: number from 900 up, title, body, labels, state)
and the repo's labels (repo_labels.json). It answers:
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

import test_automerge as tam
import test_start as ts
from dokima import agent
from test_start import N, PR, Ctx

LABEL = "filed-by-dokima"
PARKED = "parked"
EXISTING = ["autopilot", "blocker", "high"]
REFUSED = "HTTP 502: Server Error (https://api.github.com/repos/o/r/issues)"

FIND_A = {"title": "The board drops closed pull requests", "why": "Cards for merged work go stale on the board.",
          "evidence": "dokima/board.py:121 asks only for OPEN pull requests"}
FIND_B = {"title": "A cancelled run leaves its queued card behind", "why": "The owner sees a run that never ends.",
          "evidence": "dokima/agent.py:290 queue() never removes the card"}
FIND_C = {"title": "Footnotes lose the run link on retries", "why": "The owner cannot open the retried run.",
          "evidence": "dokima/agent.py:518 footnote() reads run only once"}

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
    i = {"number": 900 + len(FILED), "title": title or "", "body": body or "", "labels": labels, "state": "open"}
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


def fake_gh():
    """test_automerge's fake GitHub, taught to file issues, list them with their bodies and keep the repo's labels."""
    anchor = 'API = API.split("?")[0] if API else None\n'
    fake = tam.fake_gh()
    taught = fake.replace(anchor, anchor + FILED_GH, 1)
    assert taught != fake, "test setup: could not teach the fake GitHub to file issues"
    return taught


def plan_review(*found, verdict="approve"):
    """A plan review of #57's one-story plan that lists these issues found outside it."""
    return {**ts.APPROVE, "verdict": verdict, "asks": [{**ts.APPROVE["asks"][0], "criterion": "57.1"}],
            "issues_found": [dict(f) for f in found]}


def code_review(*found):
    """A code review of pull request #60 that approves it and lists these issues found outside it."""
    return {**tam.review_pr("approve"), "issues_found": [dict(f) for f in found]}


class Reviews(tam.Merges, ts.Machine):
    """Issue #57, planned (and, at the pr stage, built as pull request #60), on which reviews run through agent.yml.

    `labels` gives each issue's labels ({57: ["autopilot"]} puts #57 on autopilot); `repo_labels` the labels the
    repo has; `options` the fake GitHub's options (fail_create)."""

    def __init__(self, tmp, stage, labels=None, repo_labels=None, options=None):
        super().__init__(tmp, [], try_branch=True, options={"pr_open": stage == "pr", **(options or {})})
        t, self.stage, self.runs = self.tmp, stage, 0
        open(f"{t}/bin/gh", "w").write(fake_gh())
        os.chmod(f"{t}/bin/gh", 0o755)
        if stage == "pr":
            seed = tam.history(57, 60)
            json.dump({PR: tam.pr_state(57, tam.GREEN)}, open(f"{t}/gh/prs.json", "w"))
        else:
            seed = [tam.stored("issue", 57, agent.render(ts.planner_record(ts.STORY)), 1, minute=1)]
            json.dump({}, open(f"{t}/gh/prs.json", "w"))
        json.dump(seed, open(f"{t}/gh/comments.json", "w"))
        self.seeded = len(seed)
        json.dump({str(k): list(v) for k, v in (labels or {}).items()}, open(f"{t}/gh/labels.json", "w"))
        have = list(EXISTING + [PARKED, LABEL] if repo_labels is None else repo_labels)
        json.dump(have, open(f"{t}/gh/repo_labels.json", "w"))
        json.dump([], open(f"{t}/gh/filed.json", "w"))

    def review(self, handback):
        """One review run of agent.yml at this machine's stage, handing back `handback`; returns the job's result."""
        t = self.tmp
        self.runs += 1
        self.before = len(self.comments())
        json.dump(handback, open(f"{t}/review.json", "w"))
        open(f"{t}/event.json", "w").write(json.dumps({"inputs": {"role": "reviewer", "stage": self.stage, "issue": N}}))
        ctx = {"inputs": Ctx(role="reviewer", stage=self.stage, issue=N),
               "github": Ctx(event_name="workflow_dispatch", actor=ts.OWNER, event=Ctx(), run_id="42", run_attempt="1",
                             server_url="https://github.com", repository="o/r", token="fake-github-token"),
               "secrets": Ctx(CLAUDE_CODE_OAUTH_TOKEN="fake-claude-token", DOKIMA_APP_KEY="k"),
               "vars": Ctx(DOKIMA_APP_ID="1"), "needs": Ctx()}
        wf = ts.workflow("agent.yml")
        self.result, _ = self.run_job(f"review{self.runs}", wf["jobs"]["run"], ctx, "workflow_dispatch",
                                      [("/tmp/", f"{t}/run{self.runs}/"), ("/home/runner/", f"{t}/home/")], wf.get("defaults"))
        return self.result

    def filed(self):
        """Every issue filed so far, oldest first: {number, title, body, labels (all it carries now), state}."""
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
        """The comment carrying the newest run's review record, as it stands now: {id, kind, number, body}, or None."""
        for c in self.comments()[self.before:]:
            body = c["versions"][-1]
            recs = agent.records([{"author": {"login": c["author"]}, "body": body}])
            if recs and recs[0].get("role") == "reviewer":
                return {"id": c["id"], "kind": c["kind"], "number": c["number"], "body": body}
        return None


def ran(m, crit, case):
    """The review run finished and posted its record; otherwise the test fails here saying why."""
    assert m.result != "failure" or m.record(), f"{crit} ({case}): the review run failed:\n{m.tail()}"
    assert m.record(), f"{crit} ({case}): the review run posted no review record:\n{m.tail()}"


def titles(m):
    """The titles of every issue filed so far, oldest first."""
    return [i["title"] for i in m.filed()]


def test_every_issue_a_review_finds_is_filed_parked_and_labeled(record_property, tmp_path):
    """Each issue a plan review or a code review finds is filed by itself in the review's own run, parked and labeled filed-by-dokima.

    Runs a plan review of #57 that finds two issues and a code review of pull request #60 that finds one, with no
    owner command after either, and checks each run filed exactly one issue per finding, titled with the finding's own
    title, carrying exactly the labels parked and filed-by-dokima and nothing else. It also runs the same plan review
    on a repo that has neither label yet, and checks the issues are filed with both all the same. Beside them, a review
    that finds nothing files nothing."""
    record_property("proves", "265.1")
    m = Reviews(tmp_path / "plan", "plan")
    m.review(plan_review(FIND_A, FIND_B))
    ran(m, "265.1", "plan review")
    assert titles(m) == [FIND_A["title"], FIND_B["title"]], \
        f"265.1: a plan review that found two issues did not file exactly those two, by their titles; filed: {titles(m)}"
    for i in m.filed():
        assert sorted(i["labels"]) == sorted([LABEL, PARKED]), \
            f"265.1: filed issue #{i['number']} carries {i['labels']}, not exactly parked and {LABEL}"

    c = Reviews(tmp_path / "pr", "pr")
    c.review(code_review(FIND_C))
    ran(c, "265.1", "code review")
    assert titles(c) == [FIND_C["title"]], \
        f"265.1: a code review that found one issue did not file exactly it; filed: {titles(c)}"
    assert sorted(c.filed()[0]["labels"]) == sorted([LABEL, PARKED]), \
        f"265.1: the code review's filed issue carries {c.filed()[0]['labels']}, not exactly parked and {LABEL}"

    fresh = Reviews(tmp_path / "fresh", "plan", repo_labels=EXISTING)
    fresh.review(plan_review(FIND_A, FIND_B))
    ran(fresh, "265.1", "repo without the labels")
    assert titles(fresh) == [FIND_A["title"], FIND_B["title"]], \
        (f"265.1: on a repo without the parked and {LABEL} labels the findings were not filed; filed: {titles(fresh)}"
         f"\n{fresh.tail()}")
    for i in fresh.filed():
        assert sorted(i["labels"]) == sorted([LABEL, PARKED]), \
            f"265.1: on a repo without the labels, filed issue #{i['number']} carries {i['labels']}"

    none = Reviews(tmp_path / "none", "plan")
    none.review(plan_review())
    ran(none, "265.1", "nothing found")
    assert titles(none) == [], f"265.1: a review that found nothing filed issues: {titles(none)}"


def test_a_filed_issue_says_where_it_was_found_and_links_the_review(record_property, tmp_path):
    """Each filed issue says which issue (and pull request) was under review and links the comment that holds the review.

    Runs a plan review of #57 and a code review of pull request #60, each finding issues, then reads each filed
    issue's body: it must name #57 (and #60 for the code review), hold the finding's why and evidence, and link the
    very comment on GitHub that carries that review's record, by its address on the issue or pull request it is on."""
    record_property("proves", "265.2")
    for stage, handback, where in (("plan", plan_review(FIND_A, FIND_B), ["#57"]),
                                   ("pr", code_review(FIND_C), ["#57", "#60"])):
        m = Reviews(tmp_path / stage, stage)
        m.review(handback)
        ran(m, "265.2", f"{stage} review")
        rec = m.record()
        link = re.compile(rf"https://github\.com/o/r/(?:issues|pull)/{rec['number']}#issuecomment-{rec['id']}(?!\d)")
        assert len(m.filed()) == len(handback["issues_found"]), \
            f"265.2 ({stage} review): expected {len(handback['issues_found'])} filed issues, got {titles(m)}"
        for i, f in zip(m.filed(), handback["issues_found"]):
            body = i["body"]
            for w in where:
                assert re.search(rf"{w}(?!\d)", body), \
                    f"265.2 ({stage} review): filed issue #{i['number']} does not say it was found on {w}:\n{body}"
            assert f["why"] in body and f["evidence"] in body, \
                f"265.2 ({stage} review): filed issue #{i['number']} lacks the finding's why or evidence:\n{body}"
            assert link.search(body), \
                (f"265.2 ({stage} review): filed issue #{i['number']} does not link the review's comment "
                 f"(#{rec['number']}, comment {rec['id']}):\n{body}")


def test_a_filed_issue_gets_nothing_more_than_filing(record_property, tmp_path):
    """A filed issue gets no links, no plan and no run: it is not a sub-issue, blocks nothing, and nothing starts on it.

    Runs a plan review that finds two issues on #57 while #57 is on autopilot (so the river starts #57's worker), and
    checks that no sub-issue or blocked-by link was made for any filed issue, that no stage was signalled to start on
    any filed issue, and that no filed issue carries the autopilot label."""
    record_property("proves", "265.3")
    m = Reviews(tmp_path / "auto", "plan", labels={57: ["autopilot"]})
    m.review(plan_review(FIND_A, FIND_B))
    ran(m, "265.3", "on autopilot")
    filed = {i["number"] for i in m.filed()}
    assert len(filed) == 2, f"265.3: the review did not file its two findings; filed: {titles(m)}"
    ids = {str(n * 10) for n in filed} | {f"I_{n}" for n in filed}
    for call in m.calls():
        if call[:1] != ["api"]:
            continue
        text = " ".join(call)
        if "sub_issues" in text or "dependencies" in text:
            touched = {int(x) for x in re.findall(r"repos/o/r/issues/(\d+)/", text)}
            given = set(re.findall(r"(?:sub_issue_id|issue_id)=(\S+)", text))
            assert not (touched & filed) and not (given & ids), f"265.3: a filed issue was linked into the graph: {call}"
    started = [d for d in m.dispatches() if any(re.search(rf"client_payload\[issue\]=({'|'.join(map(str, filed))})$", x) for x in d)]
    assert started == [], f"265.3: a stage was started on a filed issue: {started}"
    for i in m.filed():
        assert "autopilot" not in i["labels"], f"265.3: filed issue #{i['number']} went on autopilot: {i['labels']}"


def test_the_same_finding_is_never_filed_twice(record_property, tmp_path):
    """The same finding is filed once: not twice in one review, and not again by a later review, even once it is closed.

    A plan review lists one finding twice (its title in other letter case and spacing) and one other: two issues are
    filed. The first filed issue is then closed, and a second review on the same issue finds it again (case and spacing
    changed again, a new why) beside a new finding: only the new one is filed."""
    record_property("proves", "265.4")
    m = Reviews(tmp_path / "twice", "plan")
    again = dict(FIND_A, title="  the BOARD drops   closed pull requests ", why="Said another way.")
    m.review(plan_review(FIND_A, again, FIND_B))
    ran(m, "265.4", "first review")
    assert titles(m) == [FIND_A["title"], FIND_B["title"]], \
        f"265.4: one review listing a finding twice did not file it exactly once beside the other; filed: {titles(m)}"
    m.close_filed(m.filed()[0]["number"])
    later = dict(FIND_A, title="The board drops closed  PULL requests", why="Found again.")
    m.review(plan_review(later, FIND_C, verdict="block") | {"blockers": [
        {"id": "B1", "criterion": "57.1", "problem": "The test only checks a file exists.", "evidence": "tests/test_x.py::test_a",
         "fix": "Run the thing.", "test": "tests/test_x.py::test_a", "fixer": "planner"}]})
    ran(m, "265.4", "second review")
    assert titles(m) == [FIND_A["title"], FIND_B["title"], FIND_C["title"]], \
        (f"265.4: a later review finding an already filed (and closed) issue again filed it twice, or did not file "
         f"its new finding; filed: {titles(m)}\n{m.tail()}")


def test_the_review_card_names_each_filed_issue(record_property, tmp_path):
    """The review's card names each filed issue by its number and no longer calls them proposals.

    Runs a plan review that finds two issues and reads the review's record comment as it ends up on GitHub, without its
    folded JSON: it must link each filed issue by number and must not say the findings are proposals."""
    record_property("proves", "265.5")
    m = Reviews(tmp_path / "card", "plan")
    m.review(plan_review(FIND_A, FIND_B))
    ran(m, "265.5", "plan review")
    shown = re.sub(r"```json\n.*?\n```", "", m.record()["body"], flags=re.S)
    assert len(m.filed()) == 2, f"265.5: the review did not file its two findings; filed: {titles(m)}"
    for i in m.filed():
        assert re.search(rf"#{i['number']}(?!\d)", shown), \
            f"265.5: the review's card does not name filed issue #{i['number']}:\n{shown}"
    assert "proposal" not in shown.lower(), f"265.5: the review's card still calls the findings proposals:\n{shown}"


def test_a_rejected_review_files_nothing(record_property, tmp_path):
    """A review whose hand-back code rejects files none of the issues it lists.

    Runs a plan review whose verdict is not one code accepts, listing two issues, and checks nothing was filed; beside
    it, the same review with a good verdict files both."""
    record_property("proves", "265.6")
    bad = Reviews(tmp_path / "bad", "plan")
    bad.review(plan_review(FIND_A, FIND_B, verdict="maybe"))
    assert bad.record(), f"265.6: the rejected review posted no record:\n{bad.tail()}"
    assert titles(bad) == [], f"265.6: a review code rejected filed issues: {titles(bad)}"
    good = Reviews(tmp_path / "good", "plan")
    good.review(plan_review(FIND_A, FIND_B))
    ran(good, "265.6", "good review")
    assert titles(good) == [FIND_A["title"], FIND_B["title"]], \
        f"265.6: the same review with a good verdict did not file its findings; filed: {titles(good)}"


def test_a_finding_github_refuses_to_file_says_why_on_the_review_card(record_property, tmp_path):
    """When GitHub refuses to file a finding, the review's card says which one was not filed and GitHub's reason.

    Runs a plan review that finds an issue while GitHub refuses every new issue, and checks the review's record is
    still posted and, outside its folded JSON, names the finding and carries GitHub's error message."""
    record_property("proves", "265.7")
    m = Reviews(tmp_path / "refused", "plan", options={"fail_create": REFUSED})
    m.review(plan_review(FIND_A))
    ran(m, "265.7", "GitHub refuses")
    shown = re.sub(r"```json\n.*?\n```", "", m.record()["body"], flags=re.S)
    assert titles(m) == [], f"test setup: GitHub refused every issue, yet some were filed: {titles(m)}"
    assert FIND_A["title"] in shown and "HTTP 502" in shown, \
        f"265.7: the review's card does not say the finding was not filed and why:\n{shown}"
