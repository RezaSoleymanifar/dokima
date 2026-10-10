"""An approved plan stays in Plan until its worker starts; Work means building (#343).

Before this, the board placed an issue from its newest record and the river's next step alone. On autopilot an
approved plan's next step is "start the worker", so #333, whose approved plan waits on #332, sat in Work though
nothing was being built. The other way round, an issue the owner started with `/work` stayed in Plan while its worker
built it, and a finished worker's issue jumped to Review before its code review had started.

The rule these tests hold the board to, for an open issue and its open pull request:
- an approved plan whose worker has not started is in Plan;
- a worker has started once the code owner says `/work`, the bot posts the Autopilot line that starts it
  (`Autopilot: plan approved, starting work`) or the bot puts up the worker's run card; from then the issue is in
  Work. #353 removed #253's waiting worker, so the bot's old `Autopilot: blockers closed, starting work` starts
  nothing;
- after the worker's record it stays in Work until the code review starts: the bot puts up the code review's run card
  (queued is enough) or posts its record; then it is in Review;
- only the bot's own lines and run cards, and a code owner's `/work`, count: anyone can comment on a public repo.

The tests run against test_needs_you's in-memory world, wired by test_board_state's `make` fixture: dokima.board.Board
and agent's `gh` are faked, and the history is a list where a plain string is the code owner's words, a (login,
words) pair a comment by that login, and a dict an agent record the bot posted.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import test_needs_you as tny  # noqa: E402
from test_agent import GOOD_REVIEW, GOOD_WORK, rec  # noqa: E402
from test_board_state import STRANGER, make, place, places, run_ends  # noqa: E402,F401
from dokima import agent, board, card  # noqa: E402

SPEC, REPO, LABEL = tny.SPEC, tny.REPO, tny.LABEL
NEEDS, AUTO = tny.NEEDS, tny.AUTO
STARTED = (agent.BOT, "Autopilot: plan approved, starting work")
GO = (agent.BOT, "Autopilot: blockers closed, starting work")


def bot_card(role, stage=""):
    """The run card the bot puts up for a queued run of `role`."""
    return (agent.BOT, agent.live_card(role, stage, "handoff"))


def worker_done():
    """Records up to the worker's record, before anything starts the code review."""
    return tny.plan_approved() + ["/work", rec("worker", handback=GOOD_WORK)]


def replanned_after_test_fix():
    """Records up to an approved re-plan after a code review's test blocker.

    Its criteria are unchanged.

    The river starts the worker by itself here, with no `/work` and no Autopilot line (AGENTS.md, step 5)."""
    to_planner = {**GOOD_REVIEW, "stage": "pr", "raises": [{**GOOD_REVIEW["raises"][0], "to": "planner"}]}
    return worker_done() + [rec("reviewer", "pr", to_planner)] + tny.plan_approved()


def everywhere(w, monkeypatch, tmp_path, n):
    """Run the board on issue n each way it runs: run end, event, sweep.

    Yields a name for each way, after the board ran it."""
    run_ends(n, monkeypatch, tmp_path)
    yield "the end of a run"
    board.sync("issue_comment", tny.comment(n, "Any news?", STRANGER), SPEC, REPO)
    yield "a comment on the issue"
    board.sync("schedule", {"schedule": "*/15 * * * *"}, SPEC, REPO)
    yield "the 15-minute sweep"


# 343.1: an approved plan whose worker has not started stays in Plan

def test_an_approved_plan_stays_in_plan_until_its_worker_starts(record_property, make, monkeypatch, tmp_path):
    """Every approved plan whose worker has not started is in Plan.

    Proves 343.1.
    #57 is on autopilot and its plan review has just approved, before the bot's Autopilot line that starts the worker:
    Plan with Autopilot. #58 is off autopilot and waits for the owner's `/work`: Plan with Needs you. #59 is on
    autopilot, approved, and the owner said `/plan` to plan again, so the planner's run card is up: Plan with
    Autopilot, since the planner's card is not a worker. Each card starts in Work and is checked after a run's end, a
    comment and the sweep."""
    record_property("proves", "343.1")
    cases = {57: (tny.plan_approved(), {LABEL}, AUTO),
             58: (tny.plan_approved(), set(), NEEDS),
             59: (tny.plan_approved() + ["/plan Add the error case.", bot_card("planner")], {LABEL}, AUTO)}
    for n, (history, labels, pill) in cases.items():
        w = make(labels={("issue", n): labels}, records={n: history}, cards={("issue", n): {"Status": "Work"}})
        for way in everywhere(w, monkeypatch, tmp_path, n):
            assert place(w, "issue", n) == ("Plan", pill), \
                f"343.1: #{n}'s plan is approved and no worker started, yet after {way} its card is at " \
                f"{place(w, 'issue', n)}, not ('Plan', {pill!r})"


# 343.2: Work means a worker is building it

def test_an_issue_is_in_work_once_its_worker_starts(record_property, make, monkeypatch, tmp_path):
    """Once a worker starts, the issue and its pull request are in Work.

    Proves 343.2.
    Three ways a worker starts, each from an approved plan whose card starts in Plan: the code owner says `/work` (#57,
    off autopilot: Work with no pill); the bot's `Autopilot: plan approved, starting work` (#58, on autopilot: Work with
    Autopilot); and, after a code review sent a test back to the planner and the re-plan was approved with the same criteria, the
    worker's run card the bot put up with no command and no line (#60, with its PR #70: both in Work with no pill).
    Each is checked after a run's end, a comment and the sweep."""
    record_property("proves", "343.2")
    cases = {57: (tny.plan_approved() + ["/work"], set(), None),
             58: (tny.plan_approved() + [STARTED], {LABEL}, AUTO),
             60: (replanned_after_test_fix() + [bot_card("worker")], set(), None)}
    for n, (history, labels, pill) in cases.items():
        pr = 70 if n == 60 else None
        w = make(labels={("issue", n): labels}, records={n: history}, prs={n: pr} if pr else {},
                 cards={("issue", n): {"Status": "Plan"}, **({("pr", pr): {"Status": "Review"}} if pr else {})})
        for way in everywhere(w, monkeypatch, tmp_path, n):
            got = places(w, ("issue", n), *([("pr", pr)] if pr else []))
            want = {k: ("Work", pill) for k in got}
            assert got == want, f"343.2: a worker started on #{n}, yet after {way} the cards are at {got}, not {want}"


# 343.3: after the worker has built it, it stays in Work until the code review starts

def test_a_built_issue_stays_in_work_until_its_code_review_starts(record_property, make, monkeypatch, tmp_path):
    """A built issue stays in Work until its code review starts, then Review.

    Proves 343.3.
    #57's worker has handed back and opened PR #60, and nothing has started the code review: both cards are in Work
    with no pill. Then the bot puts up the code review's queued run card: both go to Review. Then the code review's
    record approves: both stay in Review, with Needs you. Each step is checked after a run's end, a comment and the
    sweep; the cards start in Plan."""
    record_property("proves", "343.3")
    steps = [("nothing has started the code review", worker_done(), "Work", None),
             ("the code review's run card is up", worker_done() + [bot_card("reviewer", "pr")], "Review", None),
             ("the code review approved", tny.code_approved(), "Review", NEEDS)]
    for name, history, column, pill in steps:
        w = make(records={57: history}, prs={57: 60}, cards={("issue", 57): {"Status": "Plan"}, ("pr", 60): {"Status": "Plan"}})
        for way in everywhere(w, monkeypatch, tmp_path, 57):
            got = places(w, ("issue", 57), ("pr", 60))
            want = {"issue #57": (column, pill), "pr #60": (column, pill)}
            assert got == want, f"343.3: #57's worker has built it and {name}, yet after {way} the cards are at {got}, not {want}"


# 343.4: only the bot's own lines and run cards, and a code owner's /work, count

def test_words_anyone_could_paste_start_no_worker_and_no_code_review(record_property, make, monkeypatch, tmp_path):
    """Words anyone could paste never move a card to Work or Review.

    Proves 343.4.
    Beside 343.2 and 343.3's good cases, each on autopilot with an approved plan, so only the pasted words could
    move it: someone else says `/work` (#57), someone else pastes `Autopilot: plan approved, starting work` (#58),
    someone else pastes the worker's run card (#59): each stays in Plan with Autopilot. #61's worker has built PR #62
    and someone else pastes the code review's run card: both stay in Work with Autopilot."""
    record_property("proves", "343.4")
    pasted = {57: (STRANGER, "/work"), 58: (STRANGER, STARTED[1]), 59: (STRANGER, bot_card("worker")[1])}
    for n, words in pasted.items():
        w = make(labels={("issue", n): {LABEL}}, records={n: tny.plan_approved() + [words]},
                 cards={("issue", n): {"Status": "Work"}})
        for way in everywhere(w, monkeypatch, tmp_path, n):
            assert place(w, "issue", n) == ("Plan", AUTO), \
                f"343.4: on #{n} {STRANGER} wrote {words[1][:40]!r}, which starts nothing, yet after {way} its card " \
                f"is at {place(w, 'issue', n)}, not in Plan with Autopilot"
    w = make(labels={("issue", 61): {LABEL}, ("pr", 62): {LABEL}}, prs={61: 62},
             records={61: worker_done() + [(STRANGER, bot_card("reviewer", "pr")[1])]},
             cards={("issue", 61): {"Status": "Review"}, ("pr", 62): {"Status": "Review"}})
    for way in everywhere(w, monkeypatch, tmp_path, 61):
        got = places(w, ("issue", 61), ("pr", 62))
        assert got == {"issue #61": ("Work", AUTO), "pr #62": ("Work", AUTO)}, \
            f"343.4: {STRANGER} pasted a code review's run card on #61, which starts nothing, yet after {way} the " \
            f"cards are at {got}, not in Work with Autopilot"


def test_a_rebuilt_issue_stays_in_work_until_its_next_code_review_starts(record_property, make, monkeypatch, tmp_path):
    """Sent back by code review, it is in Work again until the next review starts.

    Proves 343.3.
    #57's first code review blocked with a fix for the worker, so the river started the worker again by itself: its
    run card is up, then its second record. An earlier code review record is on the issue, yet until the bot puts up
    the next code review's queued run card, #57 and its PR #60 are in Work with no pill; once that card is up, both
    are in Review. Each step is checked after a run's end, a comment and the sweep; the cards start in Review, then
    Plan, so a board that never moves them fails."""
    record_property("proves", "343.3")
    to_worker = {**GOOD_REVIEW, "stage": "pr"}
    rebuilt = worker_done() + [rec("reviewer", "pr", to_worker), bot_card("worker")]
    steps = [("the worker is building it again", rebuilt, "Work", "Review"),
             ("the worker built it again", rebuilt + [rec("worker", handback=GOOD_WORK)], "Work", "Review"),
             ("the next code review's run card is up",
              rebuilt + [rec("worker", handback=GOOD_WORK), bot_card("reviewer", "pr")], "Review", "Plan")]
    for name, history, column, start in steps:
        w = make(records={57: history}, prs={57: 60},
                 cards={("issue", 57): {"Status": start}, ("pr", 60): {"Status": start}})
        for way in everywhere(w, monkeypatch, tmp_path, 57):
            got = places(w, ("issue", 57), ("pr", 60))
            want = {"issue #57": (column, None), "pr #60": (column, None)}
            assert got == want, \
                f"343.3: #57's code review sent it back and {name}, yet after {way} the cards are at {got}, not {want}"


# 353.4: #253's waiting worker is gone, so its old line starts nothing

def test_the_old_blockers_closed_line_no_longer_starts_a_worker(record_property, make, monkeypatch, tmp_path):
    """The bot's old `Autopilot: blockers closed, starting work` no longer moves a card to Work.

    Proves 353.4.
    #57 is on autopilot with an approved plan, and the bot's own comment `Autopilot: blockers closed, starting work`
    (the line #253 started a waiting worker with) is on it: its card, started in Work, must be in Plan with Autopilot
    after a run's end, a comment and the sweep. Beside it, #58 with the bot's `Autopilot: plan approved, starting work`
    still goes to Work with Autopilot."""
    record_property("proves", "353.4")
    cases = {57: (GO, "Work", ("Plan", AUTO)), 58: (STARTED, "Plan", ("Work", AUTO))}
    for n, (line, start, want) in cases.items():
        w = make(labels={("issue", n): {LABEL}}, records={n: tny.plan_approved() + [line]},
                 cards={("issue", n): {"Status": start}})
        for way in everywhere(w, monkeypatch, tmp_path, n):
            assert place(w, "issue", n) == want, \
                f"353.4: #{n} has the bot's {line[1]!r} after its approved plan, yet after {way} its card is at " \
                f"{place(w, 'issue', n)}, not {want}"
