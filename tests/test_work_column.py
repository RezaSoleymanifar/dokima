"""An approved plan stays in Plan until its worker starts; Work means building (#343).

Before this, the board placed an issue from its newest record and the river's next step alone. On autopilot an
approved plan's next step is "start the worker", so #333, whose approved plan waits on #332, sat in Work though
nothing was being built. The other way round, an issue the owner started with `/work` stayed in Plan while its worker
built it, and a finished worker's issue jumped to Review before its code review had started.

The rule these tests hold the board to, for an open issue and its open pull request:
- an approved plan whose worker has not started is in Plan, also while it waits on a blocker, and its card still
  names what it waits on;
- a worker has started once the code owner says `/work`, the bot posts the Autopilot line that starts it
  (`Autopilot: plan approved, starting work` or `Autopilot: blockers closed, starting work`) or the bot puts up the
  worker's run card; from then the issue is in Work;
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
WAIT = (agent.BOT, "Autopilot: plan approved, waiting for #332 to close")
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
    to_planner = {**GOOD_REVIEW, "stage": "pr", "blockers": [{**GOOD_REVIEW["blockers"][0], "fixer": "planner"}]}
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


# 343.1: an approved plan whose worker has not started stays in Plan, also while it waits on a blocker

def test_an_approved_plan_waiting_on_a_blocker_stays_in_plan_and_its_card_names_the_blocker(record_property, make, monkeypatch, tmp_path):
    """An approved plan waiting on a blocker stays in Plan; its card names the blocker.

    Proves 343.1.
    #333's case. #57 is on autopilot; its plan is approved and the bot said `Autopilot: plan approved, waiting for
    #332 to close`. Its card starts in Work with Autopilot, where today's board puts it. After a run's end, a comment
    and the 15-minute sweep, it must be in Plan with Autopilot each time. Its issue card, drawn with GitHub's links
    (#332 blocks it), must still say Blocked by #332."""
    record_property("proves", "343.1")
    w = make(labels={("issue", 57): {LABEL}}, records={57: tny.plan_approved() + [WAIT]},
             cards={("issue", 57): {"Status": "Work", "Action": AUTO}})
    for way in everywhere(w, monkeypatch, tmp_path, 57):
        assert place(w, "issue", 57) == ("Plan", AUTO), \
            f"343.1: #57's approved plan waits on #332 and no worker started, yet after {way} its card is at " \
            f"{place(w, 'issue', 57)}, not in Plan with Autopilot"
    # Drawn the way card.draw() draws it: GitHub's blocked-by links, read now, are the card's Blocked by line.
    items = card.as_items(tny.plan_approved(), tny.OWNER)
    found = {"recs": agent.records(items), "items": items, "pr": None, "check_runs": [], "reviews": [],
             "owners": {tny.OWNER}, "tests": {}, "worker": None, "children": [],
             "blocking": {"blocked_by": [332], "blocks": [], "loop": []},
             "linked": {"relates_to": [], "blocked_by": [332], "blocks": []}}
    drawn = card.render(REPO, {"number": 57, "title": "Issue 57", "url": "https://github.com/o/r/issues/57"}, found)
    assert "**Blocked by:** #332" in drawn, \
        f"343.1: #57 waits on #332, yet its card no longer says Blocked by #332:\n{drawn}"


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
    Four ways a worker starts, each from an approved plan whose card starts in Plan: the code owner says `/work` (#57,
    off autopilot: Work with no pill); the bot's `Autopilot: plan approved, starting work` (#58, on autopilot: Work with
    Autopilot); the bot's `Autopilot: blockers closed, starting work` after the waiting line (#59: Work with Autopilot);
    and, after a code review sent a test back to the planner and the re-plan was approved with the same criteria, the
    worker's run card the bot put up with no command and no line (#60, with its PR #70: both in Work with no pill).
    Each is checked after a run's end, a comment and the sweep."""
    record_property("proves", "343.2")
    cases = {57: (tny.plan_approved() + ["/work"], set(), None),
             58: (tny.plan_approved() + [STARTED], {LABEL}, AUTO),
             59: (tny.plan_approved() + [WAIT, GO], {LABEL}, AUTO),
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
    Beside 343.2 and 343.3's good cases, each on autopilot after the waiting line, so only the pasted words could
    move it: someone else says `/work` (#57), someone else pastes `Autopilot: blockers closed, starting work` (#58),
    someone else pastes the worker's run card (#59): each stays in Plan with Autopilot. #61's worker has built PR #62
    and someone else pastes the code review's run card: both stay in Work with Autopilot."""
    record_property("proves", "343.4")
    pasted = {57: (STRANGER, "/work"), 58: (STRANGER, GO[1]), 59: (STRANGER, bot_card("worker")[1])}
    for n, words in pasted.items():
        w = make(labels={("issue", n): {LABEL}}, records={n: tny.plan_approved() + [WAIT, words]},
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
