"""`/autopilot start` on an issue with no plan starts its planner, and the issue then runs to merged by itself (#245).

Before this, `/autopilot start` switched the issue on and said "No stage was started": it only started planning for
issues under the one switched on, never that issue itself, so nothing happened until the owner typed `/plan`.

These tests run the command listener (.github/workflows/commands.yml) the way GitHub runs it, on the machine from
test_start.py, against the fake GitHub of test_autopilot_close.py (issue tree, labels, states, blocked-by links,
comments, signals) and, for the journey, test_automerge.py's (pull requests, checks, merging). Where only the river's
decision between two stages matters, the journey runs `python3 -m dokima.agent next 57` on the finished stage's record,
against the same fake GitHub, as agent.yml does after every run.
"""
import json
import os
import subprocess
import sys

import test_automerge as tam
import test_autopilot_close as tac
import test_start as ts
from dokima import agent
from test_start import N, OWNER, PR

LABEL = "autopilot"
LINE = "Autopilot: switched on, starting plan"
LINE_BLOCKERS = "Autopilot: blockers merged, starting plan"
LINE_WORK = "Autopilot: plan approved, starting work"
ISSUE = int(N)


def lines(m, n, text):
    """How many comments written on issue n since the test began read exactly this line."""
    return sum(1 for b in on_issue(m, n) if b.strip() == text)


def on_issue(m, n):
    """The bodies of the comments written on issue n since the test began, as they stand now."""
    return [c["versions"][-1] for c in m.comments()[m.seeded:] if c["kind"] == "issue" and c["number"] == int(n)]


def said_where_commanded(m):
    """The one comment `/autopilot start` left on #57 naming what it switched: the one that starts 'Autopilot is'."""
    said = [b for b in on_issue(m, ISSUE) if b.strip().startswith(("Autopilot is", f"#{N} and every issue"))]
    assert len(said) == 1, f"test setup: /autopilot start left {len(said)} switch comments on #{N}: {said}"
    return said[0]


def assert_a_new_issue_starts(tmp, crit, deps=None, closed=()):
    """The good case beside every "does not start" case: `/autopilot start` on #57 with no plan starts its planner once.

    Without it, code that never starts the issue's planner would pass every check that it must not start."""
    m = tac.Repo(tmp, {}, {}, deps=deps, closed=closed)
    m.listen("/autopilot start")
    assert not m.failed, f"{crit} (new issue): the listener failed on /autopilot start:\n{m.tail()}"
    started = m.planners_started(crit)
    assert started == {ISSUE: 1} and lines(m, ISSUE, LINE) == 1, \
        (f"{crit} (new issue): /autopilot start on #{N} with no plan and nothing open to wait for did not start its planner "
         f"once with one {LINE!r}; planners started: {started}, its comments: {on_issue(m, ISSUE)}")


def test_autopilot_start_on_an_issue_with_no_plan_starts_its_planner(record_property, tmp_path):
    """`/autopilot start` on a new issue starts its planner once, with one Autopilot line where the owner would have said /plan.

    #57 has no plan, no sub-issues and nothing blocking it. After the code owner's `/autopilot start` on it, #57's
    planner must be started exactly once by Dokima's signal, #57 must get exactly one comment reading
    `Autopilot: switched on, starting plan`, and the comment naming what was switched must say planning started for
    #57 and must no longer say "No stage was started"."""
    record_property("proves", "245.1")
    m = tac.Repo(tmp_path / "new", {}, {})
    m.listen("/autopilot start")
    assert not m.failed, f"245.1: the listener failed on /autopilot start:\n{m.tail()}"
    started = m.planners_started("245.1")
    assert started == {ISSUE: 1}, (f"245.1: /autopilot start on #{N}, a new issue with no plan, did not start its planner "
                                   f"exactly once; planners started: {started}\n{m.tail()}")
    assert lines(m, ISSUE, LINE) == 1, \
        f"245.1: #{N} did not get exactly one comment reading {LINE!r}; its new comments: {on_issue(m, ISSUE)}"
    said = said_where_commanded(m)
    assert "No stage was started" not in said, f"245.1: the switch comment still says no stage was started:\n{said}"
    assert f"Planning started for #{N}" in said, f"245.1: the switch comment does not say planning started for #{N}:\n{said}"


def test_autopilot_start_never_starts_the_issue_itself_where_it_must_not(record_property, tmp_path):
    """`/autopilot start` leaves the issue itself alone when it is already planned or planning, split, or blocked by an open issue.

    Four issues #57 that must not get their planner started nor the Autopilot line: one already planned (a planner
    record on it), one whose planner is running now (a live card), one split into sub-issues (#101 waits on nothing,
    so #101 starts instead), and one blocked by #110, still open. The blocked one must then start, once, when #110
    closes, with the line autopilot gives every issue whose blockers merged. Beside them, the same #57 with no plan and
    its only blocker already closed must start at once."""
    record_property("proves", "245.2")
    assert_a_new_issue_starts(tmp_path / "unblocked", "245.2", deps={ISSUE: [110]}, closed=[110])
    cases = (("planned", {}, {}, [tac.planned(ISSUE, 4001)], {}),
             ("running", {}, {}, [tac.running(ISSUE, 77, 4002)], {}),
             ("split", {ISSUE: [101]}, {}, [], {101: 1}),
             ("blocked", {}, {ISSUE: [110]}, [], {}))
    for case, tree, deps, seed, want in cases:
        m = tac.Repo(tmp_path / case, tree, {}, deps=deps, seed=seed, running_runs=[77])
        m.listen("/autopilot start")
        assert not m.failed, f"245.2 ({case}): the listener failed on /autopilot start:\n{m.tail()}"
        started = m.planners_started("245.2")
        assert started == want, f"245.2 ({case}): /autopilot start started planners {started}, expected {want}\n{m.tail()}"
        assert lines(m, ISSUE, LINE) == 0, f"245.2 ({case}): #{N} got {LINE!r} though it must not start: {on_issue(m, ISSUE)}"
        if case == "blocked":
            m.close(110)
            assert not m.failed, f"245.2 (blocked): a workflow failed when #110 closed: {m.failures}\n{m.tail()}"
            started = m.planners_started("245.2")
            assert started == {ISSUE: 1}, f"245.2 (blocked): #{N} did not start once when its blocker #110 closed: {started}"
            assert lines(m, ISSUE, LINE_BLOCKERS) == 1, \
                f"245.2 (blocked): #{N} did not get one {LINE_BLOCKERS!r} when #110 closed: {on_issue(m, ISSUE)}"


def test_autopilot_start_still_picks_up_what_waits_in_the_tree(record_property, tmp_path):
    """`/autopilot start` still picks up what already waits anywhere in the tree, and never starts a planner on top of it.

    Three trees: #57 with an approved plan waiting for `/work` (its worker starts with one `Autopilot: plan approved,
    starting work` line, and no planner starts); #57 split into #101 and #102, #102 under #101's blocker (#101's
    planner starts, #57's and #102's do not); and #57 whose pull request #60 its code review approved with every check
    green (#60 merges, and no planner starts). Beside them, #57 with no plan and nothing waiting must start its planner,
    so code that never starts one cannot pass."""
    record_property("proves", "245.3")
    assert_a_new_issue_starts(tmp_path / "new", "245.3")
    m = tam.Command(tmp_path / "waiting", {}, {}, tree={ISSUE: []})
    for i, c in enumerate(ts.STORY_PLANNED[1:] + [ts.record_comment(ts.review_record(ts.APPROVE), "2026-10-07T10:20:00Z")]):
        seed = json.load(open(f"{m.tmp}/gh/comments.json"))
        seed.append(tam.stored("issue", ISSUE, c["body"], 5000 + i, minute=10 + i))
        json.dump(seed, open(f"{m.tmp}/gh/comments.json", "w"))
        m.seeded += 1
    m.listen("/autopilot start")
    assert not m.failed, f"245.3 (plan waiting): the listener failed:\n{m.tail()}"
    workers = [s for s in m.signals() if s["payload"].get("role") == "worker" and s["payload"].get("issue") == N]
    assert len(workers) == 1, f"245.3 (plan waiting): the waiting plan's worker did not start once: {m.signals()}"
    assert m.planners_started("245.3") == {}, f"245.3 (plan waiting): a planner started too: {m.planners_started('245.3')}"
    assert lines(m, ISSUE, LINE_WORK) == 1 and lines(m, ISSUE, LINE) == 0, \
        f"245.3 (plan waiting): #{N} did not get exactly the work line and no plan line: {on_issue(m, ISSUE)}"

    m = tac.Repo(tmp_path / "children", {ISSUE: [101, 102]}, {}, deps={102: [101]})
    m.listen("/autopilot start")
    assert not m.failed, f"245.3 (children): the listener failed:\n{m.tail()}"
    assert m.planners_started("245.3") == {101: 1}, f"245.3 (children): planners started: {m.planners_started('245.3')}"
    assert lines(m, ISSUE, LINE) == 0, f"245.3 (children): #{N}, a parent, got {LINE!r}"

    m = tam.Command(tmp_path / "approved", {int(PR): tam.pr_state(ISSUE, tam.GREEN)}, {ISSUE: "approve"}, tree={ISSUE: []})
    m.listen("/autopilot start")
    assert not m.failed, f"245.3 (approved pull request): the listener failed:\n{m.tail()}"
    assert m.merged(PR) == tam.HEAD, f"245.3 (approved pull request): #{PR} did not merge: {m.tried()}\n{m.tail()}"
    assert m.planners_started("245.3") == {}, f"245.3 (approved pull request): a planner started: {m.planners_started('245.3')}"


def test_saying_autopilot_start_twice_starts_the_planner_once(record_property, tmp_path):
    """Saying `/autopilot start` twice on a new issue starts its planner once and leaves one Autopilot line.

    Runs the code owner's `/autopilot start` on #57, a new issue, then again (as after a `/autopilot stop`, which
    starts nothing). The Autopilot line the first one left is the record that #57 started, so the second must start
    no planner and post no second line."""
    record_property("proves", "245.5")
    m = tam.Command(tmp_path / "twice", {}, {}, tree={ISSUE: []})
    m.listen("/autopilot start")
    m.listen("/autopilot stop")
    m.listen("/autopilot start")
    assert not m.failed, f"245.5: the listener failed:\n{m.tail()}"
    started = m.planners_started("245.5")
    assert started == {ISSUE: 1}, f"245.5: saying /autopilot start twice started #{N}'s planner {started.get(ISSUE, 0)} times, not once"
    assert lines(m, ISSUE, LINE) == 1, f"245.5: #{N} got {lines(m, ISSUE, LINE)} lines reading {LINE!r}, not one"


def river(m, rec, kind, number):
    """A stage finished: its record goes on GitHub where the workflow posts it, then the river decides what follows.

    Runs `python3 -m dokima.agent next 57` with Dokima's app key against the same fake GitHub, as agent.yml does. An
    Autopilot line it writes goes on the issue, as the workflow posts it. Returns what it printed."""
    t = m.tmp
    store = json.load(open(f"{t}/gh/comments.json"))
    store.append(tam.stored(kind, number, agent.render(rec), 9000 + len(store), minute=min(59, 10 + len(store))))
    json.dump(store, open(f"{t}/gh/comments.json", "w"))
    out = f"{t}/out-{len(store)}"
    os.makedirs(out)
    json.dump(rec, open(f"{out}/record.json", "w"))
    open(f"{out}/comment.md", "w").write(agent.render(rec))
    env = {**m.base_env("workflow_dispatch"), "GH_TOKEN": "fake-token", "OWNERS": OWNER, "PYTHONPATH": ts.ROOT}
    p = subprocess.run([sys.executable, "-m", "dokima.agent", "next", N, out], cwd=ts.ROOT, env=env,
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, f"245.4: the river failed after the {rec['role']} {rec.get('stage') or ''}:\n{p.stderr[-2000:]}"
    if os.path.exists(f"{out}/autopilot.md"):
        subprocess.run(["gh", "issue", "comment", N, "-R", "o/r", "--body-file", f"{out}/autopilot.md"], env=env, check=True)
    return p.stdout.strip()


def test_a_new_issue_on_autopilot_ends_merged_with_no_command_from_the_owner(record_property, tmp_path):
    """A new issue the owner puts on autopilot is planned, reviewed, built, reviewed and merged with no other command from the owner.

    #57 is a new issue. The code owner says `/autopilot start` and nothing else. Each stage then follows from the one
    before by itself: `/autopilot start` must start the planner; the plan must go to the plan reviewer; its approval
    must start the worker with one `Autopilot: plan approved, starting work` line; the worker's pull request #60 must go
    to the code reviewer; and its approval, every check green, must merge #60 with one `Autopilot: merged PR #60` line.
    The owner wrote no comment along the way."""
    record_property("proves", "245.4")
    m = tam.Command(tmp_path / "journey", {}, {}, tree={ISSUE: []})
    m.listen("/autopilot start")
    assert not m.failed, f"245.4: the listener failed on /autopilot start:\n{m.tail()}"
    assert m.planners_started("245.4") == {ISSUE: 1}, \
        f"245.4: the journey stopped at the start: /autopilot start did not start #{N}'s planner: {m.signals()}\n{m.tail()}"

    step = river(m, ts.planner_record(ts.STORY), "issue", ISSUE)
    assert step == "start reviewer plan", f"245.4: after the plan, the river did not start the plan review: {step!r}"
    step = river(m, ts.review_record({**ts.APPROVE, "asks": [{**ts.APPROVE["asks"][0], "criterion": "57.1"}]}), "issue", ISSUE)
    assert step.startswith("start worker"), f"245.4: after the plan review approved, the worker did not start: {step!r}"
    assert lines(m, ISSUE, LINE_WORK) == 1, f"245.4: #{N} did not get one {LINE_WORK!r}: {on_issue(m, ISSUE)}"

    json.dump({PR: tam.pr_state(ISSUE, tam.GREEN)}, open(f"{m.tmp}/gh/prs.json", "w"))
    step = river(m, tam.worker_record(), "pr", int(PR))
    assert step == "start reviewer pr", f"245.4: after the worker opened #{PR}, the code review did not start: {step!r}"
    river(m, tam.code_review_record("approve"), "pr", int(PR))
    assert m.merged(PR) == tam.HEAD, f"245.4: the approved pull request #{PR} did not merge: {m.tried()}"
    assert [x for x in m.autopilot_lines(ISSUE)] == [("issue", ISSUE, f"Autopilot: merged PR #{PR}")], \
        f"245.4: #{N} did not get one 'Autopilot: merged PR #{PR}' line: {m.autopilot_lines(ISSUE)}"

    by_owner = [c["versions"][-1] for c in m.comments() if c["author"] == OWNER]
    assert by_owner == [], f"245.4: the owner had to write along the way: {by_owner}"
