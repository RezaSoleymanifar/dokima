"""On autopilot, a blocked story plans at once; only its worker waits (#313).

Before this, every step that starts a planner on autopilot skipped an issue with an open blocker: a split filed only
its unblocked stories' planners, `/autopilot start` left blocked issues alone, and a close started only the issues
whose blockers had all closed. So a blocked story (such as #311, blocked by #309) sat unplanned until its blocker
closed, though #253 already makes the worker the one that waits.

These tests run the workflows the way GitHub runs them, on the machine of test_start.py, against the fake GitHub of
test_autopilot_close.py (issue tree, labels, states, blocked-by links, comments and start signals). Where only the
river's decision between two stages matters, the journey runs `python3 -m dokima.agent next N OUT` on the finished
stage's record, against the same fake GitHub, as agent.yml does after every run.

A blocked issue that starts planning gets one line naming its open blockers, `Autopilot: starting plan, its worker
waits for #A and #B to close`, where the owner would have said `/plan`.
"""
import json
import os
import re
import subprocess
import sys

import test_automerge as tam
import test_autopilot_close as tac
import test_start as ts
from dokima import agent
from test_start import OWNER

LABEL = "autopilot"
MERGED = "Autopilot: blockers merged, starting plan"
SWITCHED = "Autopilot: switched on, starting plan"
WAITS = "Autopilot: starting plan, its worker waits for {} to close"
WAITING = "Autopilot: plan approved, waiting for {} to close"
GO = "Autopilot: blockers closed, starting work"


def said(m, n):
    """The comments written on issue n since the test began, as they stand now, stripped."""
    return [b.strip() for b in m.new_comments(n)]


def autopilot_said(m, n):
    """The comments written on issue n since the test began that start with 'Autopilot:'."""
    return [b for b in said(m, n) if b.startswith("Autopilot:")]


def switch_comment(m):
    """The one comment `/autopilot start` left on #57 naming what it switched."""
    found = [b for b in said(m, 57) if b.startswith(("Autopilot is", "#57 and every issue"))]
    assert len(found) == 1, f"test setup: /autopilot start left {len(found)} switch comments on #57: {found}"
    return found[0]


def label(m, numbers):
    """Put these issues on autopilot on the fake GitHub.

    GitHub keeps the labels a new issue is created with; this fake keeps only those added later, so a story filed
    with the autopilot label is written here the way GitHub would hold it."""
    labels = m._json("labels.json")
    for n in numbers:
        labels[str(n)] = sorted(set(labels.get(str(n), [])) | {LABEL})
    json.dump(labels, open(f"{m.tmp}/gh/labels.json", "w"))


# 313.1: a split on autopilot ----------------------------------------------------------------------------------------

def test_a_split_on_autopilot_starts_planning_every_story_blocked_or_not(record_property, tmp_path):
    """A split filed on autopilot starts planning every story at once, the blocked one too.

    #57's approved split has two stories, the second blocked by the first; GitHub numbers them #900 and #901. When the
    code owner says `/work` on #57, which is on autopilot, both stories must have their planner started exactly once:
    #900 with one `Autopilot: blockers merged, starting plan` line as before, and #901, still blocked by #900, with
    exactly one line `Autopilot: starting plan, its worker waits for #900 to close`. The same holds when the split is
    filed by `/autopilot start` on #57 picking up the approved split. Beside them, `/work` with #57 off autopilot
    starts no story and posts no Autopilot line. Proves 313.1."""
    record_property("proves", "313.1")
    for case, labels, command in (("/work on autopilot", {57: [LABEL]}, "/work"),
                                  ("/autopilot start", {}, "/autopilot start")):
        m = tac.Repo(tmp_path / case.replace("/", "").replace(" ", "-"), {}, labels, history=ts.SPLIT_APPROVED)
        m.listen(command)
        assert not m.failed, f"313.1 ({case}): the listener failed:\n{m.tail()}"
        assert json.load(open(f"{m.tmp}/gh/tree.json")).get("57") == [900, 901], \
            f"313.1 ({case}): the split was not filed as #900 and #901:\n{m.tail()}"
        assert json.load(open(f"{m.tmp}/gh/deps.json")).get("901") == [900], \
            f"313.1 ({case}): #901 is not blocked by #900 on GitHub, so this does not test a blocked story"
        started = m.planners_started("313.1")
        assert started == {900: 1, 901: 1}, (f"313.1 ({case}): every story should start planning once, the blocked "
                                             f"#901 too; planners started: {started}\n{m.tail()}")
        assert autopilot_said(m, 900) == [MERGED], \
            f"313.1 ({case}): #900 should get exactly one {MERGED!r} line: {said(m, 900)}"
        assert autopilot_said(m, 901) == [WAITS.format("#900")], \
            f"313.1 ({case}): #901 should get exactly one {WAITS.format('#900')!r} line: {said(m, 901)}"

    m = tac.Repo(tmp_path / "off", {}, {}, history=ts.SPLIT_APPROVED)
    m.listen("/work")
    assert not m.failed, f"313.1 (off autopilot): the listener failed:\n{m.tail()}"
    assert m.planners_started("313.1") == {}, f"313.1 (off autopilot): a story started: {m.planners_started('313.1')}"
    assert m.any_autopilot_line() == [], f"313.1 (off autopilot): an Autopilot line was posted: {m.any_autopilot_line()}"


# 313.2: /autopilot start --------------------------------------------------------------------------------------------

def test_autopilot_start_starts_planning_blocked_issues_too(record_property, tmp_path):
    """`/autopilot start` starts planning every issue in the tree with no plan, blocked or not.

    #57 alone, blocked by #110 (open), with no plan: `/autopilot start` must start its planner once, with one line
    `Autopilot: starting plan, its worker waits for #110 to close`, and the switch comment must name #57 as started and
    no longer claim it waits on nothing open. A tree: #57 with #101 (no blockers), #102 (blocked by #101 and #104,
    both open), #103 (blocked by #110, closed) and #104 (already planned): #101, #102 and #103 must each start once,
    #102 with one `... waits for #101 and #104 to close`, #101 and #103 with `Autopilot: blockers merged, starting
    plan`; #104 (planned) and #57 (a parent) must not start. Beside them, #57 alone and unblocked still starts with
    `Autopilot: switched on, starting plan`, and `/autopilot stop` starts nothing. Proves 313.2."""
    record_property("proves", "313.2")
    m = tac.Repo(tmp_path / "alone-blocked", {}, {}, deps={57: [110]})
    m.listen("/autopilot start")
    assert not m.failed, f"313.2 (blocked issue): the listener failed:\n{m.tail()}"
    assert m.planners_started("313.2") == {57: 1}, \
        f"313.2 (blocked issue): #57, blocked by #110, should start planning once: {m.planners_started('313.2')}\n{m.tail()}"
    assert autopilot_said(m, 57) == [WAITS.format("#110")], \
        f"313.2 (blocked issue): #57 should get exactly one {WAITS.format('#110')!r} line: {said(m, 57)}"
    words = switch_comment(m)
    assert "Planning started for #57" in words and "nothing open" not in words, \
        f"313.2 (blocked issue): the switch comment should say planning started for #57 without claiming it waits on nothing open: {words}"

    m = tac.Repo(tmp_path / "alone-free", {}, {})
    m.listen("/autopilot start")
    assert not m.failed, f"313.2 (free issue): the listener failed:\n{m.tail()}"
    assert m.planners_started("313.2") == {57: 1} and autopilot_said(m, 57) == [SWITCHED], \
        f"313.2 (free issue): #57 should start once with {SWITCHED!r}: {m.planners_started('313.2')} {said(m, 57)}"

    tree, deps = {57: [101, 102, 103, 104]}, {102: [101, 104], 103: [110]}
    m = tac.Repo(tmp_path / "tree", tree, {}, deps=deps, closed=[110], seed=[tac.planned(104, 4001)])
    m.listen("/autopilot start")
    assert not m.failed, f"313.2 (tree): the listener failed:\n{m.tail()}"
    started = m.planners_started("313.2")
    assert started == {101: 1, 102: 1, 103: 1}, \
        f"313.2 (tree): #101, #102 (blocked) and #103 should each start once, and not #57 or #104: {started}\n{m.tail()}"
    assert autopilot_said(m, 102) == [WAITS.format("#101 and #104")], \
        f"313.2 (tree): #102 should get exactly one {WAITS.format('#101 and #104')!r} line: {said(m, 102)}"
    for n in (101, 103):
        assert autopilot_said(m, n) == [MERGED], f"313.2 (tree): #{n} should get exactly one {MERGED!r} line: {said(m, n)}"
    for n in (57, 104):
        assert autopilot_said(m, n) == [], f"313.2 (tree): #{n} got an Autopilot line though it must not start: {said(m, n)}"

    m = tac.Repo(tmp_path / "stop", tree, {n: [LABEL] for n in (57, 101, 102, 103, 104)}, deps=deps, closed=[110])
    m.listen("/autopilot stop")
    assert not m.failed, f"313.2 (/autopilot stop): the listener failed:\n{m.tail()}"
    assert m.planners_started("313.2") == {}, f"313.2 (/autopilot stop): something started: {m.planners_started('313.2')}"
    assert m.any_autopilot_line() == [], f"313.2 (/autopilot stop): an Autopilot line was posted: {m.any_autopilot_line()}"


# 313.3: the issues already stuck start when this merges -------------------------------------------------------------

STUCK_TREE = {305: [309, 311, 312], 306: [320]}
STUCK_LABELS = {n: [LABEL] for n in (305, 309, 311, 312, 313)}


def stuck_repo(tmp):
    """The repo as this merges: a blocked story never planned, and #313 about to close.

    #305 is on autopilot with #309 (planned), #311 (blocked by #309, still open, no plan) and #312 (on autopilot, no
    plan, never blocked: a story added by hand to the tree). #306 is not on autopilot and holds #320 (no plan,
    blocked by #309). #313 is on autopilot, alone."""
    return tac.Repo(tmp, STUCK_TREE, STUCK_LABELS, deps={311: [309], 320: [309]}, seed=[tac.planned(309, 4001)])


def test_when_this_merges_every_stuck_story_on_autopilot_starts_planning(record_property, tmp_path):
    """When this issue closes, every unplanned story on autopilot starts planning, blocked or not.

    Runs autopilot.yml the way GitHub does when #313 closes (its pull request merged). #311, blocked by #309 and never
    planned, must start its planner once with one line `Autopilot: starting plan, its worker waits for #309 to close`;
    #312, on autopilot with no plan and no blockers, must start once with exactly one Autopilot line that says it is
    starting its plan. #309 (planned), #305 (a parent), #306 and #320 (not on autopilot) must not start. Beside it, a
    repo where every story on autopilot already has a plan starts nothing when #313 closes. Proves 313.3."""
    record_property("proves", "313.3")
    m = stuck_repo(tmp_path / "stuck")
    m.close(313)
    assert not m.failed, f"313.3: a workflow failed when #313 closed: {m.failures}\n{m.tail()}"
    started = m.planners_started("313.3")
    assert started == {311: 1, 312: 1}, \
        f"313.3: #311 and #312, stuck on autopilot with no plan, should each start planning once, and nothing else: {started}\n{m.tail()}"
    assert autopilot_said(m, 311) == [WAITS.format("#309")], \
        f"313.3: #311 should get exactly one {WAITS.format('#309')!r} line: {said(m, 311)}"
    lines = autopilot_said(m, 312)
    assert len(lines) == 1 and "starting plan" in lines[0], \
        f"313.3: #312 should get exactly one Autopilot line saying it is starting its plan: {said(m, 312)}"
    for n in (305, 306, 309, 320):
        assert autopilot_said(m, n) == [], f"313.3: #{n} got an Autopilot line though it must not start: {said(m, n)}"

    m = tac.Repo(tmp_path / "all-planned", STUCK_TREE, STUCK_LABELS, deps={311: [309], 320: [309]},
                 seed=[tac.planned(n, 4001 + i) for i, n in enumerate((309, 311, 312))])
    m.close(313)
    assert not m.failed, f"313.3 (all planned): a workflow failed when #313 closed: {m.failures}\n{m.tail()}"
    assert m.planners_started("313.3") == {}, f"313.3 (all planned): something started: {m.planners_started('313.3')}"
    assert m.any_autopilot_line() == [], f"313.3 (all planned): an Autopilot line was posted: {m.any_autopilot_line()}"


# 313.4: the whole journey -------------------------------------------------------------------------------------------

def river(m, rec, number):
    """A stage on issue `number` finished: its record is posted, then the river decides.

    Runs `python3 -m dokima.agent next N OUT` with Dokima's app key against the same fake GitHub, as agent.yml does,
    and posts on the issue the Autopilot line it writes for the workflow. Returns what it printed."""
    t = m.tmp
    store = json.load(open(f"{t}/gh/comments.json"))
    store.append(tam.stored("issue", number, agent.render(rec), 9000 + len(store), minute=min(59, 10 + len(store))))
    json.dump(store, open(f"{t}/gh/comments.json", "w"))
    out = f"{t}/out-{len(store)}"
    os.makedirs(out)
    json.dump(rec, open(f"{out}/record.json", "w"))
    open(f"{out}/comment.md", "w").write(agent.render(rec))
    env = {**m.base_env("workflow_dispatch"), "GH_TOKEN": "fake-token", "OWNERS": OWNER, "PYTHONPATH": ts.ROOT}
    p = subprocess.run([sys.executable, "-m", "dokima.agent", "next", str(number), out], cwd=ts.ROOT, env=env,
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, f"313.4: the river failed after the {rec['role']} on #{number}:\n{p.stderr[-2000:]}"
    if os.path.exists(f"{out}/autopilot.md"):
        subprocess.run(["gh", "issue", "comment", str(number), "-R", "o/r", "--body-file", f"{out}/autopilot.md"],
                       env=env, check=True)
    return p.stdout.strip()


def workers_started(m, n):
    """How many times issue n's worker was started by Dokima's own signal."""
    return sum(1 for s in m.signals() if s["event_type"] == "dokima-next" and s["token"] == "fake-token"
               and s["payload"].get("role") == "worker" and s["payload"].get("issue") == str(n))


def test_a_split_on_autopilot_plans_its_blocked_story_and_builds_it_once_the_blocker_closes(record_property, tmp_path):
    """A blocked story plans at once, its worker waits, then builds when the blocker closes.

    #57 is on autopilot with an approved split; `/work` files #900 and #901 (#901 blocked by #900). #901's planner
    must start at once. Its plan then goes to the plan review by itself; the review's approval must start no worker
    and leave one line `Autopilot: plan approved, waiting for #900 to close`. When #900 closes, #901's worker must
    start exactly once, with one line `Autopilot: blockers closed, starting work`, and #901's planner must not start
    again. The owner writes nothing after `/work`. Proves 313.4."""
    record_property("proves", "313.4")
    m = tac.Repo(tmp_path / "journey", {}, {57: [LABEL]}, history=ts.SPLIT_APPROVED)
    m.listen("/work")
    assert not m.failed, f"313.4: the listener failed on /work:\n{m.tail()}"
    assert m.planners_started("313.4").get(901) == 1, \
        f"313.4: the journey stopped at the split: blocked #901's planner did not start once: {m.planners_started('313.4')}\n{m.tail()}"
    label(m, [900, 901])

    plan = {**ts.STORY, "acceptance_criteria": [{"text": "a", "source": "https://github.com/o/r/issues/901"}],
            "tests": {"901.1": ["tests/test_x.py::test_a"]}}
    step = river(m, ts.planner_record(plan), 901)
    assert step == "start reviewer plan", f"313.4: after #901's plan, the river did not start the plan review: {step!r}"
    review = {**ts.APPROVE, "asks": [{**ts.APPROVE["asks"][0], "source": "https://github.com/o/r/issues/901",
                                      "criterion": "901.1"}]}
    step = river(m, ts.review_record(review), 901)
    assert not step.startswith("start"), f"313.4: #901's worker started while #900 is still open: {step!r}"
    assert workers_started(m, 901) == 0, "313.4: #901's worker was signalled while #900 is still open"
    assert WAITING.format("#900") in said(m, 901), \
        f"313.4: #901 should say {WAITING.format('#900')!r} once its plan is approved: {said(m, 901)}"

    m.close(900)
    assert not m.failed, f"313.4: a workflow failed when #900 closed: {m.failures}\n{m.tail()}"
    assert workers_started(m, 901) == 1, f"313.4: #901's worker should start once when #900 closes:\n{m.tail()}"
    assert said(m, 901).count(GO) == 1, f"313.4: #901 should get exactly one {GO!r} line: {said(m, 901)}"
    assert m.planners_started("313.4").get(901) == 1, \
        f"313.4: #901's planner was started again: {m.planners_started('313.4')}"
    by_owner = [c["versions"][-1] for c in m.comments()[m.seeded:] if c["author"] == OWNER and c["versions"][-1].strip() != "/work"]
    assert by_owner == [], f"313.4: the owner had to write along the way: {by_owner}"


# 313.5: nothing starts twice ----------------------------------------------------------------------------------------

def test_a_blocked_story_that_started_planning_never_starts_again(record_property, tmp_path):
    """A blocked story that started planning is never started again by a later close.

    #57 has #101 and #102 (#102 blocked by #101, open; neither planned). `/autopilot start` starts #102 once with its
    line; closing the unrelated issues #120, then #121, must not start #102 again nor post a second line. The same for
    the stuck repo: closing #313, then #120, starts #311 once. Proves 313.5."""
    record_property("proves", "313.5")
    m = tac.Repo(tmp_path / "twice", {57: [101, 102]}, {}, deps={102: [101]})
    m.listen("/autopilot start")
    m.close(120)
    m.close(121)
    assert not m.failed, f"313.5: a workflow failed: {m.failures}\n{m.tail()}"
    started = m.planners_started("313.5")
    assert started.get(102) == 1 and started.get(101) == 1, \
        f"313.5: #101 and blocked #102 should each have started planning exactly once: {started}\n{m.tail()}"
    assert autopilot_said(m, 102) == [WAITS.format("#101")], \
        f"313.5: #102 should have exactly one {WAITS.format('#101')!r} line: {said(m, 102)}"

    m = stuck_repo(tmp_path / "stuck")
    m.close(313)
    m.close(120)
    assert not m.failed, f"313.5 (stuck): a workflow failed: {m.failures}\n{m.tail()}"
    assert m.planners_started("313.5").get(311) == 1, \
        f"313.5 (stuck): #311 should start planning once across two closes: {m.planners_started('313.5')}"
    assert len(autopilot_said(m, 311)) == 1, f"313.5 (stuck): #311 got more than one Autopilot line: {said(m, 311)}"


# 313.6: AGENTS.md says it -------------------------------------------------------------------------------------------

def section(text, heading):
    """The body of the AGENTS.md section whose heading starts with `heading`."""
    found = {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.S | re.M)}
    return next((v for k, v in found.items() if k.startswith(heading)), "")


def test_agents_md_says_every_story_on_autopilot_plans_as_soon_as_it_exists(record_property):
    """AGENTS.md says every story on autopilot plans at once, and no longer says otherwise.

    The flow section must say "starts planning as soon as it exists, blocked or not" and name the line
    `Autopilot: starting plan, its worker waits for #A and #B to close`, and still say a blocked issue's worker waits
    until every blocker closes. Neither The flow nor Commands may still say an issue starts its planner only when its
    blockers have closed ("whose blocked-by issues have now all closed starts its planner") or that `/autopilot start`
    starts only issues with "nothing open to wait for". Proves 313.6."""
    record_property("proves", "313.6")
    text = open(os.path.join(ts.ROOT, "AGENTS.md")).read()
    flow, commands = section(text, "The flow"), section(text, "Commands")
    assert flow and commands, "313.6: AGENTS.md has no The flow or no Commands section"
    for words in ("starts planning as soon as it exists, blocked or not",
                  "`Autopilot: starting plan, its worker waits for #A and #B to close`",
                  "its worker waits until every blocker closes"):
        assert words in " ".join(flow.split()), f"313.6: AGENTS.md's The flow does not say {words!r}"
    for name, body in (("The flow", flow), ("Commands", commands)):
        flat = " ".join(body.split())
        for old in ("whose blocked-by issues have now all closed starts its planner", "nothing open to wait for"):
            assert old not in flat, f"313.6: AGENTS.md's {name} still says {old!r}, which is no longer how autopilot works"
