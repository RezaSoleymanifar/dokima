"""On autopilot, a blocked issue plans, but its worker waits for every blocker (#253).

Story 4 of #231. Two moments matter, and each runs the real code against a fake GitHub:

- The plan review approves. `python3 -m dokima.agent next N OUT` (the step of agent.yml that decides what follows a
  run) runs on the review's record, on the fake GitHub of test_plan_links_recorded.py (issue #252 there). An issue on
  autopilot that GitHub still has blocked by an open issue must not start its worker: it gets one line naming the
  open issues it waits on, and the card's Next line mentions no one.
- An issue closes. autopilot.yml runs the way GitHub runs it, on the machine of test_autopilot_close.py (issue #57
  there). When the last open blocker of an issue on autopilot closes, and its newest plan is approved and no worker
  has started on it, its worker starts once, with one line `Autopilot: blockers closed, starting work`.

Where GitHub cannot list an issue's blockers, the fake answers that read with "HTTP 502: Server Error" and the worker
must not start, with the reason on the issue.
"""
import json
import os
import re

import test_autopilot_close as tc
import test_autopilot_river as ar
import test_plan_links_recorded as pl
import test_start as ts
from dokima import agent

WAIT = "Autopilot: plan approved, waiting for {} to close"
GO = "Autopilot: blockers closed, starting work"
LABEL = "autopilot"
ERROR = "HTTP 502: Server Error (blocked_by)"


# The plan review approves: `agent next` on #252 ---------------------------------------------------------------------

def hub(tmp, closed=(), autopilot=True, deps=None, fail_read=False):
    """The fake GitHub of test_plan_links_recorded, with these issues closed.

    With fail_read, every read of #252's blocker list fails."""
    h = pl.Hub(tmp, deps=deps, autopilot=autopilot)
    s = h.load()
    for n in closed:
        s["issues"][str(n)]["state"] = "closed"
    s["fail_read"] = [pl.N] if fail_read else []
    h.save()
    src = 'if method == "GET":\n            out([obj(b) for b in deps(n)])'
    fake = pl.FAKE_GH.replace(src, 'if method == "GET":\n            if n in S.get("fail_read", []):\n'
                                   f'                fail({ERROR!r})\n            out([obj(b) for b in deps(n)])', 1)
    assert fake != pl.FAKE_GH, "test setup: could not teach the fake GitHub to fail a read of the blockers"
    gh = os.path.join(h.dir, "bin", "gh")
    open(gh, "w").write(f"#!{pl.sys.executable}\nBOT_LOGIN = {pl.BOT!r}\nOWNER_LOGIN = {pl.OWNER!r}\n" + fake)
    return h


def new_comments(h):
    """The comments the commands wrote on #252, apart from records.

    The run's own record is posted later, by the workflow."""
    return [c["body"].strip() for c in h.comments(pl.N) if agent.MARK not in c["body"]]


def next_line(comment):
    """The card's Next line."""
    return next((l for l in comment.splitlines() if l.startswith("**Next:**")), "")


def approve_on(h, links, crit, case):
    """The river runs on a plan with these links, then on its approving review.

    Asserts the plan goes to the plan review as usual; returns what the river said on the approval."""
    rec = pl.plan(links)
    step, _, _ = h.next(rec)
    assert step == "start reviewer plan", \
        f"{crit} ({case}): the plan of a blocked issue did not go to the plan review as usual, the river said {step!r}"
    h.post(rec)
    return h.next(pl.review())


def test_on_autopilot_a_blocked_plan_waits_with_one_line_and_mentions_no_one(tmp_path, record_property):
    """On autopilot, a blocked approved plan starts no worker; one line names its open blockers.

    #252 is on autopilot. Its plan says blocked by #301 (open) and #302 (closed), and GitHub already has #252 blocked
    by #304 (open) by hand. The plan goes to its review as usual; when the review approves, no stage starts, no
    `/work` stand-in line is written, #252 gets exactly one comment, `Autopilot: plan approved, waiting for #301 and
    #304 to close`, the card's Next line mentions no one and the card is not marked Needs you. With #301 the only
    blocker the line reads `... waiting for #301 to close`. Beside them: with every blocker closed the worker starts
    and no waiting line is written, and off autopilot the blocked plan stops for the owner as before, with no line. Proves 253.1."""
    record_property("proves", "253.1")
    h = hub(tmp_path / "blocked", closed=[302], deps={pl.N: [304]})
    step, comment, out = approve_on(h, pl.links([301, 302]), "253.1", "blocked")
    assert not step.startswith("start"), f"253.1: a blocked plan on autopilot started {step!r}"
    assert not os.path.exists(os.path.join(out, "autopilot.md")), "253.1: the worker's Autopilot line was still written"
    assert h.writes("dispatch") == [], f"253.1: a stage was signalled: {h.writes('dispatch')}"
    said = new_comments(h)
    assert said == [WAIT.format("#301 and #304")], \
        f"253.1: #252 should get exactly one line naming the open issues it waits on (#301 and #304), got {said}"
    nxt = next_line(comment)
    assert nxt and "@" not in nxt, f"253.1: the card's Next line should mention no one while it waits: {nxt!r}"
    assert open(os.path.join(out, "board.txt")).read().split()[1] == "none", \
        "253.1: the card is marked Needs you while the issue only waits on its blockers"

    h = hub(tmp_path / "one")
    step, comment, out = approve_on(h, pl.links([301]), "253.1", "one blocker")
    assert not step.startswith("start"), f"253.1 (one blocker): the worker started: {step!r}"
    assert new_comments(h) == [WAIT.format("#301")], f"253.1 (one blocker): the line is {new_comments(h)}"

    h = hub(tmp_path / "all-closed", closed=[301, 302])
    step, comment, out = approve_on(h, pl.links([301, 302]), "253.1", "all closed")
    assert step == "start worker", f"253.1 (all closed): with every blocker closed the worker should start, not {step!r}"
    assert os.path.exists(os.path.join(out, "autopilot.md")), "253.1 (all closed): the Autopilot line is missing"
    assert new_comments(h) == [], f"253.1 (all closed): a waiting line was written: {new_comments(h)}"

    h = hub(tmp_path / "off", autopilot=False)
    step, comment, out = approve_on(h, pl.links([301]), "253.1", "off autopilot")
    assert step == "stop" and f"@{pl.OWNER}" in next_line(comment), \
        f"253.1 (off autopilot): the approval should stop for the owner: {step!r} {next_line(comment)!r}"
    assert new_comments(h) == [], f"253.1 (off autopilot): a waiting line was written: {new_comments(h)}"


def test_when_github_cannot_list_the_blockers_the_worker_waits_and_the_issue_says_why(tmp_path, record_property):
    """When GitHub cannot list the blockers, no worker starts and the card says why.

    #252 is on autopilot with a plan that has no links, and every read of #252's blocked-by list fails with
    "HTTP 502: Server Error (blocked_by)". When the review approves, no stage starts, no Autopilot line is written,
    and the record's comment, which the workflow posts on the issue, quotes GitHub's error. Beside it, the same plan
    with the list readable starts the worker. Proves 253.4."""
    record_property("proves", "253.4")
    h = hub(tmp_path / "readable")
    step, _, _ = approve_on(h, pl.links(), "253.4", "readable")
    assert step == "start worker", f"253.4 (readable): with nothing blocking it the worker should start, not {step!r}"

    h = hub(tmp_path / "unreadable", fail_read=True)
    step, comment, out = approve_on(h, pl.links(), "253.4", "unreadable")
    assert not step.startswith("start"), f"253.4: the worker started though GitHub could not list the blockers: {step!r}"
    assert not os.path.exists(os.path.join(out, "autopilot.md")), "253.4: the worker's Autopilot line was still written"
    assert h.writes("dispatch") == [], f"253.4: a stage was signalled: {h.writes('dispatch')}"
    assert ERROR in comment, f"253.4: the issue does not say why the worker did not start (GitHub's error): {comment[-800:]!r}"


# An issue closes: autopilot.yml on #57 ------------------------------------------------------------------------------

def bot_line(text, t):
    """An Autopilot line the bot posted on #57, as GitHub returns it."""
    return {"author": {"login": agent.BOT}, "body": text, "createdAt": t}


APPROVED = ts.STORY_PLANNED + [ts.record_comment(ts.review_record(ar.APPROVE), "2026-10-07T10:20:00Z")]
WAITING = APPROVED + [bot_line(WAIT.format("#101 and #102"), "2026-10-07T10:21:00Z")]
WORKER = {"role": "worker", "stage": None, "run_id": "3", "run": "https://github.com/o/r/actions/runs/3",
          "models": ["claude-opus-5-5"], "handback": {"summary": "Built it."}, "check": {"passed": True, "problems": []}}


def repo(tmp, history, closed=(102,), on=True, fail_read=False):
    """#57, blocked by #101 and #102, with this history and on autopilot unless told.

    With fail_read, every read of #57's blocker list fails."""
    m = tc.Repo(tmp, {}, {57: [LABEL]} if on else {}, deps={57: [101, 102]}, closed=closed, history=history)
    if fail_read:
        anchor = 'm_dep = re.fullmatch(r"repos/o/r/issues/(\\d+)/dependencies/blocked_by", API or "")\nif m_dep:\n    n = m_dep.group(1)\n'
        fake = tc.fake_gh()
        patched = fake.replace(anchor, anchor + '    if method() == "GET" and n in opts.get("fail_deps", []):\n'
                                                f'        sys.stderr.write({ERROR!r} + "\\n")\n        sys.exit(1)\n', 1)
        assert patched != fake, "test setup: could not teach the fake GitHub to fail a read of the blockers"
        open(f"{m.tmp}/bin/gh", "w").write(patched)
        json.dump({"running_runs": [], "fail_deps": ["57"]}, open(f"{m.tmp}/gh/options.json", "w"))
    return m


def workers(m, crit):
    """How many times #57's worker was started by a signal that starts agent.yml."""
    n = 0
    for s in m.signals():
        p = s["payload"]
        if s["event_type"] == "dokima-next" and p.get("role") == "worker" and p.get("issue") == "57":
            assert s["token"] == "fake-token", f"{crit}: #57's worker was signalled with the workflow's own token, which GitHub ignores"
            n += 1
    return n


def go_lines(m):
    """How many new comments on #57 read exactly the line that starts its worker."""
    return sum(1 for b in m.new_comments(57) if b.strip() == GO)


def assert_starts_once(m, crit, case):
    """#57's worker started exactly once with exactly one line, and its planner did not start."""
    assert not m.failed, f"{crit} ({case}): a workflow failed: {m.failures}\n{m.tail()}"
    assert workers(m, crit) == 1, f"{crit} ({case}): #57's worker started {workers(m, crit)} times, expected once\n{m.tail()}"
    assert go_lines(m) == 1, f"{crit} ({case}): #57 should get exactly one {GO!r} comment: {m.new_comments(57)}"
    assert 57 not in m.planners_started(crit), f"{crit} ({case}): #57's planner was started again"


def assert_starts_nothing(m, crit, case):
    """#57's worker did not start and no line starts it."""
    assert not m.failed, f"{crit} ({case}): a workflow failed: {m.failures}\n{m.tail()}"
    assert workers(m, crit) == 0, f"{crit} ({case}): #57's worker started, though it must not"
    assert go_lines(m) == 0, f"{crit} ({case}): #57 got a {GO!r} line, though nothing may start: {m.new_comments(57)}"


def test_the_last_blocker_closing_starts_the_waiting_worker_once(tmp_path, record_property):
    """The last open blocker closing starts the waiting worker once, with its line.

    #57 is on autopilot, its plan approved and waiting on #101 and #102. With #102 already closed, closing #101
    starts #57's worker exactly once, by Dokima's own signal, with exactly one comment reading `Autopilot: blockers
    closed, starting work`, and does not start its planner. Another close right after starts nothing more. With #102
    still open, closing #101 starts nothing; and off autopilot the same last close starts nothing. Proves 253.2."""
    record_property("proves", "253.2")
    m = repo(tmp_path / "last", WAITING)
    m.close(101)
    assert_starts_once(m, "253.2", "last blocker closed")
    m.close(110)
    assert_starts_once(m, "253.2", "a later close")

    for case, kw in (("one still open", dict(closed=())), ("off autopilot", dict(on=False))):
        m = repo(tmp_path / case.replace(" ", "-"), WAITING, **kw)
        m.close(101)
        assert_starts_nothing(m, "253.2", case)


def test_a_worker_already_started_is_never_started_again(tmp_path, record_property):
    """A close never starts a worker again once it has started.

    #57 is on autopilot, its plan approved, blocked by #101 and #102 (#102 closed). When #101 closes, #57's worker
    starts once; but not when, after the approval, the owner already said `/work`, a worker record is on the issue,
    or the bot already wrote `Autopilot: blockers closed, starting work`. Proves 253.2."""
    record_property("proves", "253.2")
    m = repo(tmp_path / "waiting", WAITING)
    m.close(101)
    assert_starts_once(m, "253.2", "waiting")
    for case, extra in (("owner said /work", ts.owner_comment("/work", "2026-10-07T10:30:00Z")),
                        ("worker record", ts.record_comment(WORKER, "2026-10-07T10:30:00Z")),
                        ("already started by a close", bot_line(GO, "2026-10-07T10:30:00Z"))):
        m = repo(tmp_path / case.replace(" ", "-").replace("/", ""), WAITING + [extra])
        m.close(101)
        assert_starts_nothing(m, "253.2", case)


def test_only_an_approved_newest_plan_starts_its_worker(tmp_path, record_property):
    """The last blocker closing starts the worker only when the issue's newest plan is approved.

    #57 is on autopilot, blocked by #101 and #102 (#102 closed). Closing #101 starts #57's worker when its newest
    plan is approved; it starts nothing when the plan is still under review, or when a newer plan came after the
    approval and is not reviewed yet. Proves 253.2."""
    record_property("proves", "253.2")
    m = repo(tmp_path / "approved", APPROVED)
    m.close(101)
    assert_starts_once(m, "253.2", "approved, no waiting line")
    replan = ts.record_comment(ts.planner_record(ts.STORY), "2026-10-07T10:40:00Z")
    for case, history in (("under review", ts.STORY_PLANNED), ("re-plan not reviewed", WAITING + [replan])):
        m = repo(tmp_path / case.replace(" ", "-"), history)
        m.close(101)
        assert_starts_nothing(m, "253.2", case)


def test_a_close_that_cannot_list_the_blockers_starts_no_worker_and_says_why(tmp_path, record_property):
    """When a close cannot list the blockers, no worker starts and the issue says why.

    #57 is on autopilot, its plan approved and waiting, blocked by #101 and #102 (#102 closed), and every read of
    #57's blocked-by list fails with "HTTP 502: Server Error (blocked_by)". Closing #101 starts no worker and leaves
    a new comment on #57 quoting GitHub's error. Beside it, the same close with the list readable starts the worker.
    Proves 253.4."""
    record_property("proves", "253.4")
    m = repo(tmp_path / "readable", WAITING)
    m.close(101)
    assert_starts_once(m, "253.4", "readable")

    m = repo(tmp_path / "unreadable", WAITING, fail_read=True)
    m.close(101)
    assert workers(m, "253.4") == 0, "253.4: #57's worker started though GitHub could not list its blockers"
    assert go_lines(m) == 0, f"253.4: #57 got a {GO!r} line though its blockers could not be listed"
    assert any(ERROR in b for b in m.new_comments(57)), \
        f"253.4: #57 does not say why its worker did not start (GitHub's error): {m.new_comments(57)}\n{m.tail()}"


# AGENTS.md ----------------------------------------------------------------------------------------------------------

def test_agents_md_says_a_blocked_issue_plans_and_its_worker_waits(record_property):
    """AGENTS.md's flow says a blocked issue still plans and its worker waits.

    Reads the section of AGENTS.md whose heading starts "The flow". One paragraph of it must say that on autopilot
    "a blocked issue still plans", that "its worker waits until every blocker closes", that it "then starts by
    itself", and name the line `Autopilot: blockers closed, starting work`. Proves 253.3."""
    record_property("proves", "253.3")
    text = open(os.path.join(ts.ROOT, "AGENTS.md")).read()
    sections = {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M)}
    flow = next((v for k, v in sections.items() if k.startswith("The flow")), "")
    assert flow, "253.3: AGENTS.md has no The flow section"
    want = ("autopilot", "a blocked issue still plans", "its worker waits until every blocker closes",
            "then starts by itself", f"`{GO}`")
    best = max(flow.split("\n\n"), key=lambda p: sum(w in p for w in want))
    missing = [w for w in want if w not in best]
    assert not missing, f"253.3: no paragraph of AGENTS.md's The flow says the new rule; the closest misses {missing}"
