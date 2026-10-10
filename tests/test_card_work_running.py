"""The card stops asking for /work once the build has started or finished.

Issue #410. The card's status (`dokima.card.status`) looked only at the newest record: after a plan approval it said
"Needs you: Say /work to build the plan" even once a code owner had said `/work`, the bot had posted its Autopilot line
or the worker's run card was up, and kept saying it while the pull request's tests failed. The board
(`dokima.board.where`) already counts a stage started since the newest record; the card must follow the same rule.

These tests draw the card from a conversation built here (owner comments, bot records and run cards) with
`dokima.card.status` and `dokima.card.render`, and compare it with the board's own `dokima.board.where` on the same
conversation, faked in place of GitHub. Nothing reaches GitHub.
"""
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, board, card, plan  # noqa: E402

REPO = "o/r"
ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40"}
SRC = "https://github.com/o/r/issues/40"
BOT = "dokima-runtime"
OWNER = "boss"
STRANGER = "passerby"
SAY_WORK = "Say /work"
PLAN = {"kind": "user_story", "summary": "Slow calls hand back a job id instead of timing out.",
        "user_story": "Callers get a job id for a slow call.",
        "acceptance_criteria": [{"text": "First thing works", "source": SRC},
                                {"text": "Second thing works", "source": SRC}],
        "non_functional": [{"text": "Nothing leaks out", "why": "safety", "principle": "Fail closed"}],
        "scope": ["app/a.py"], "out_of_scope": ["Nothing else."],
        "tests": {"40.1": ["tests/test_a.py::test_one"], "40.2": ["tests/test_a.py::test_two"],
                  "40.3": ["tests/test_a.py::test_three"]},
        "test_changes": {}}
PLAN2 = dict(PLAN, acceptance_criteria=PLAN["acceptance_criteria"] + [{"text": "Third thing works", "source": SRC}])
PR = {"number": 5, "merged": False, "state": "open", "body": "Closes #40"}
DONE = {"status": "completed", "conclusion": "success", "html_url": "https://github.com/o/r/actions/runs/1"}


def rec(role, stage=None, passed=True, n=1, **handback):
    """One agent record, as dokima.agent.records reads it from a bot comment."""
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": passed, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}", "run_id": str(n)}


PLANNED = rec("planner", n=11, **PLAN)
REPLANNED = rec("planner", n=21, **PLAN2)
PLAN_OK = rec("reviewer", "plan", n=12, verdict="approve", blockers=[])
BUILT = rec("worker", n=13)
BUILD_REJECTED = rec("worker", passed=False, n=13)
CODE_OK = rec("reviewer", "pr", n=14, verdict="approve", blockers=[])
CODE_BLOCK_TEST = rec("reviewer", "pr", n=14, verdict="block", blockers=[{"id": "B1", "fixer": "planner"}])


def run(name, status="completed", conclusion="success", n=7):
    """One GitHub check run on the PR's latest commit."""
    return {"name": name, "status": status, "conclusion": conclusion,
            "html_url": f"https://github.com/o/r/actions/runs/2/job/{n}"}


NAMES = ["40.1 · First thing works", "40.2 · Second thing works", "40.3 · Nothing leaks out", "all tests"]
GREEN = [run(x, n=i) for i, x in enumerate(NAMES, 1)]
RED_2 = [dict(r, conclusion="failure") if r["name"].startswith("40.2") else r for r in GREEN]
RED_2_ALL = [dict(r, conclusion="failure") if r["name"].startswith(("40.2", "all tests")) else r for r in GREEN]
RED_1_RUNNING_3 = [dict(r, conclusion="failure") if r["name"].startswith("40.1") else
                   dict(r, status="in_progress", conclusion=None) if r["name"].startswith("40.3") else r for r in GREEN]
RUNNING = [dict(r, status="in_progress", conclusion=None) for r in GREEN]

# Who says what: (login, body, where). A dict is a bot record.
WORK = (OWNER, "/work", "issue #40")
WORK_BY_STRANGER = (STRANGER, "/work", "issue #40")
WORK_IN_APPROVE = (OWNER, "/work", "PR #5 review (approved)")
AUTOPILOT_WORK = (BOT, None, "issue #40")  # body filled in at run time: agent.AUTOPILOT_LINES["worker"]
WORKER_CARD = (BOT, "live-worker", "issue #40")  # body: the worker's run card, queued
WORKER_CARD_WORKING = (BOT, "live-worker-working", "issue #40")


def body_of(s):
    if s[1] is None:
        return agent.AUTOPILOT_LINES["worker"]
    if s[1] == "live-worker":
        return agent.live_card("worker", "", "queued")
    if s[1] == "live-worker-working":
        return agent.live_card("worker", "", "working")
    return s[1]


def said(*steps):
    """The conversation of a run of records and comments, oldest first, one hour apart."""
    items = []
    for i, s in enumerate(steps):
        at = f"2026-10-08T{i:02d}:00:00Z"
        if isinstance(s, dict):
            items.append({"author": {"login": BOT}, "body": f"{agent.MARK}\n**Card**\n\n```json\n{json.dumps(s)}\n```\n",
                          "createdAt": at, "where": "issue #40"})
        else:
            items.append({"author": {"login": s[0]}, "body": body_of(s), "createdAt": at, "where": s[2]})
    return items


def found_for(steps, pr=None, check_runs=()):
    """What the card is drawn from for issue #40 after these steps."""
    items = said(*steps)
    return {"recs": agent.records(items), "items": items, "pr": pr, "check_runs": list(check_runs), "reviews": [],
            "owners": {OWNER}, "tests": {}, "worker": DONE, "children": []}


def lines_of(text):
    """The card's non-empty lines between its markers."""
    inside = text[text.index(plan.CARD_START) + len(plan.CARD_START):text.index(plan.CARD_END)]
    return [l.strip() for l in inside.splitlines() if l.strip()]


def bare(line):
    """A line without its HTML tags, '*', '_' and backticks."""
    return re.sub(r"[*_`]", "", re.sub(r"<[^>]+>", "", line)).strip()


def status_line(found, page="issue"):
    """The card's status line (the line after the plan's summary), without its markup."""
    return bare(lines_of(card.render(REPO, ISSUE, found, page=page))[1])


def failing(line):
    """The checks named after "Failing:" on a status line, or None."""
    m = re.search(r"Failing:\s*([^·]*)", line)
    return None if not m else {x.strip() for x in m.group(1).split(",") if x.strip()}


@pytest.fixture(autouse=True)
def bot(monkeypatch):
    monkeypatch.setattr(agent, "BOT", BOT)


RUNNING_CASES = [
    ("the owner said /work, no pull request yet", [PLANNED, PLAN_OK, WORK], None, ()),
    ("the owner said /work and the worker's card is queued", [PLANNED, PLAN_OK, WORK, WORKER_CARD], None, ()),
    ("the worker's card says working", [PLANNED, PLAN_OK, WORK, WORKER_CARD_WORKING], None, ()),
    ("the Autopilot line started the worker", [PLANNED, PLAN_OK, AUTOPILOT_WORK], None, ()),
    ("only the worker's run card is up", [PLANNED, PLAN_OK, WORKER_CARD], None, ()),
    ("a re-plan's build runs while the pull request's checks run",
     [PLANNED, PLAN_OK, WORK, BUILT, CODE_BLOCK_TEST, REPLANNED, PLAN_OK, WORK], PR, RUNNING),
    ("a re-plan's build runs while a test on the pull request fails",
     [PLANNED, PLAN_OK, WORK, BUILT, CODE_BLOCK_TEST, REPLANNED, PLAN_OK, WORK, WORKER_CARD_WORKING], PR, RED_2_ALL),
]


@pytest.mark.parametrize("name,steps,pr,checks", RUNNING_CASES, ids=[c[0] for c in RUNNING_CASES])
def test_a_running_build_shows_work_and_no_needs_you(record_property, name, steps, pr, checks):
    """A card whose build is running shows Work and no Needs you.

    Proves 410.1. First checks the good case: an approved plan nobody started still shows Plan and Needs you: Say
    /work, so the fix cannot simply drop the to-do. Then, for a build started by a code owner's /work, the bot's
    Autopilot line or the worker's run card, with and without a pull request whose tests run or fail, checks that
    card.status says Work with nothing for the owner, and that the status line on the issue and the pull request
    starts with Work and says neither Needs you nor Say /work."""
    record_property("proves", "410.1")
    waiting = found_for([PLANNED, PLAN_OK])
    got = card.status(ISSUE, waiting)
    assert got[0] == "Plan" and got[1] and SAY_WORK in bare(got[1]), \
        f"410.1: an approved plan nobody started no longer asks for /work: the card says {got}"
    line = status_line(waiting)
    assert line.startswith("Plan") and "Needs you" in line and SAY_WORK in line, \
        f"410.1: an approved plan nobody started does not show Plan and Needs you: Say /work: “{line}”"
    f = found_for(steps, pr=pr, check_runs=checks)
    got = card.status(ISSUE, f)
    assert got == ("Work", None), f"410.1: {name}: the card says {got}, not the Work stage with nothing for you"
    for page in ("issue", "pr"):
        line = status_line(f, page)
        assert line.startswith("Work"), f"410.1: {name}: the {page} card's status line does not show Work: “{line}”"
        assert "Needs you" not in line and SAY_WORK not in line, \
            f"410.1: {name}: the {page} card asks for you while the build runs: “{line}”"


FINISHED_CASES = [
    ("a finished build with one failing criterion", [PLANNED, PLAN_OK, WORK, WORKER_CARD, BUILT], RED_2, {"40.2"}),
    ("a finished build with a failing criterion and All tests", [PLANNED, PLAN_OK, WORK, BUILT], RED_2_ALL,
     {"40.2", "All tests"}),
    ("a finished build its check rejected", [PLANNED, PLAN_OK, WORK, BUILD_REJECTED], RED_2_ALL, {"40.2", "All tests"}),
    ("a finished build with one check failed and one still running", [PLANNED, PLAN_OK, WORK, BUILT],
     RED_1_RUNNING_3, {"40.1"}),
    ("approved work with a failing check", [PLANNED, PLAN_OK, WORK, BUILT, CODE_OK], RED_2, {"40.2"}),
]


@pytest.mark.parametrize("name,steps,checks,want", FINISHED_CASES, ids=[c[0] for c in FINISHED_CASES])
def test_a_finished_build_with_a_failing_test_names_what_failed(record_property, name, steps, checks, want):
    """A finished build with a failing test names each failing check, not Say /work.

    Proves 410.2. First checks the good case: the same history with every check green names nothing as failing, so
    the card cannot say Failing all the time. Then, with the worker's record in and a check on the pull request's
    latest commit failed, checks that the status line on the issue and the pull request names, after "Failing:",
    exactly the failed checks (the criterion number, or All tests), none that passed or are still running, and never
    says Say /work."""
    record_property("proves", "410.2")
    green = status_line(found_for(steps, pr=PR, check_runs=GREEN))
    assert "Failing" not in green, f"410.2: {name}: with every check green the card still says something fails: “{green}”"
    f = found_for(steps, pr=PR, check_runs=checks)
    for page in ("issue", "pr"):
        line = status_line(f, page)
        assert SAY_WORK not in line, f"410.2: {name}: the {page} card asks for /work after the build: “{line}”"
        assert failing(line) == want, \
            f"410.2: {name}: the {page} card's status line names failing {failing(line)}, not {want}: “{line}”"


AGREE_CASES = [
    ("approved, nobody started", [PLANNED, PLAN_OK], False),
    ("the owner said /work", [PLANNED, PLAN_OK, WORK], False),
    ("the worker's card is up", [PLANNED, PLAN_OK, WORK, WORKER_CARD_WORKING], False),
    ("the Autopilot line started the worker", [PLANNED, PLAN_OK, AUTOPILOT_WORK], True),
    ("a stranger said /work", [PLANNED, PLAN_OK, WORK_BY_STRANGER], False),
    ("a re-plan's build runs", [PLANNED, PLAN_OK, WORK, BUILT, CODE_BLOCK_TEST, REPLANNED, PLAN_OK, WORK], False),
]


@pytest.mark.parametrize("name,steps,on", AGREE_CASES, ids=[c[0] for c in AGREE_CASES])
def test_the_card_and_the_board_agree_on_a_started_build(record_property, monkeypatch, name, steps, on):
    """The card's stage and Needs you match the board's for the same history.

    Proves 410.3. Hands the same conversation to the board's own placing code (dokima.board.where, GitHub faked) and to the card,
    for an approval nobody started, builds started each way and a stranger's /work, and checks both give the same
    column and both show, or both don't show, Needs you."""
    record_property("proves", "410.3")
    f = found_for(steps)
    monkeypatch.setattr(agent, "conversation", lambda repo, n: ({"body": ""}, f["items"]))
    column, pill = board.where(REPO, {OWNER}, 40, on)
    stage, todo = card.status(ISSUE, f)
    assert (stage, todo is not None) == (column, pill == "Needs you"), \
        f"410.3: {name}: the card says {stage} with to-do {todo!r}; the board has {column} with pill {pill!r}"


@pytest.mark.parametrize("name,said_by", [("someone who is not a code owner", WORK_BY_STRANGER),
                                          ("an Approve review", WORK_IN_APPROVE)],
                         ids=["stranger", "approve"])
def test_only_a_code_owners_work_moves_the_card_to_work(record_property, name, said_by):
    """Only a code owner's /work moves the card to Work, never anyone else's.

    Proves 410.4. After an approved plan, /work from someone who is not a code owner, or as an Approve review's summary, leaves the
    card in Plan asking the owner to say /work, while the code owner's own /work moves it to Work with nothing to do."""
    record_property("proves", "410.4")
    got = card.status(ISSUE, found_for([PLANNED, PLAN_OK, said_by]))
    assert got[0] == "Plan" and got[1] and SAY_WORK in bare(got[1]), \
        f"410.4: /work from {name} changed the card: it says {got}, not Plan with Say /work"
    owner = card.status(ISSUE, found_for([PLANNED, PLAN_OK, WORK]))
    assert owner == ("Work", None), f"410.4: the code owner's /work does not move the card to Work: it says {owner}"
