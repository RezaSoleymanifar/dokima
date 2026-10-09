"""The board's column and pills are always computed from the issue's state right now (#331).

Before this, each board update trusted the one event that started it: board.decide() mapped each event to a column,
agent.move_card() put the card where the finished run said, and a dropped, late or out-of-order event left a card
wrong for good (#231 stuck in Work, about 40 closed cards still showing a pill). Now every event about an issue or its
pull request, the end of every agent run and a sweep every 15 minutes set the cards from GitHub as it is.

The rule these tests hold the board to, for an issue and the pull requests built for it:
- closed issue, merged or closed pull request: Done, no Action pill, whatever its labels;
- open issue with no agent record yet: Backlog;
- otherwise the column the river placed it in after its newest record (agent.board_place on that record and the
  river's next step: the stage now running, or the stage that stopped for the owner; a filed split is Work);
- Needs you while the issue waits on the owner (agent.waits_on_owner), else Autopilot while the item carries the
  autopilot label, else no pill. An open pull request goes with the issue it was built for.

Most tests run against test_needs_you's in-memory world: dokima.board.Board and agent's `gh` are faked, so the tests
read the board's end state. On top of that fake Board, cards() also gives each card's column:

    .cards() -> [{"kind", "number", "status", "action", "closed", "autopilot"}, ...]

and the history (the bot's records, everyone's words, pull request reviews) is read through `gh issue view`,
`gh pr list`, `gh pr view` and `gh api`, as agent.conversation does. A history entry that is a (login, words) pair is
a comment by that person; a plain string is the code owner's words.
"""
import json
import os
import re
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import test_needs_you as tny  # noqa: E402
from dokima import agent, board  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "board.yml")
LABEL, SPEC, REPO, OWNER = tny.LABEL, tny.SPEC, tny.REPO, tny.OWNER
NEEDS, AUTO = tny.NEEDS, tny.AUTO
BOT = "dokima-runtime[bot]"
STRANGER = "someone-else" if OWNER != "someone-else" else "another-person"


def fake_board(world):
    """test_needs_you's fake Board, whose cards() also gives each card's column."""
    base = tny.fake_board(world)

    class FakeBoard(base):
        def cards(self):
            return [{**c, "status": world.status(c["kind"], c["number"])} for c in super().cards()]

    return FakeBoard


@pytest.fixture
def make(monkeypatch):
    """Wire a world into dokima.board.Board and dokima.agent.gh, and return it."""

    def wire(**kw):
        world = tny.World(**kw)
        monkeypatch.setattr(board, "Board", fake_board(world))
        monkeypatch.setattr(agent, "gh", tny.fake_gh(world))
        return world

    return wire


def place(w, kind, n):
    """(column, pill) of one card."""
    return w.status(kind, n), w.action(kind, n)


def places(w, *items):
    """Each card's (column, pill), keyed "issue #N" or "pr #N"."""
    return {f"{k} #{n}": place(w, k, n) for k, n in items}


def run_ends(n, monkeypatch, tmp_path, board_txt=None):
    """Run the end of a run's board step on issue n: `agent board N OUT`.

    board_txt, when given, is what the run itself decided (OUT/board.txt), which must not count."""
    monkeypatch.setenv("DOKIMA_BOARD", SPEC)
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
    if board_txt:
        (tmp_path / "board.txt").write_text(board_txt)
    return agent.main(["agent", "board", str(n), str(tmp_path)])


def pr_payload(number, issue):
    """A pull request as event payloads carry it, built for `issue` (no issue when None)."""
    return {"number": number, "body": f"Closes #{issue}" if issue else "", "merged": False, "labels": [],
            "head": {"ref": f"try/issue-{issue}" if issue else f"feature-{number}"}}


def events_about(issue, pr):
    """One event of every kind about an issue or its PR, none a command."""
    return [
        ("issues", {"action": "labeled", "label": {"name": "bug"},
                    "issue": {"number": issue, "state": "open", "labels": [{"name": "bug"}]}}),
        ("issues", {"action": "edited", "issue": {"number": issue, "state": "open", "labels": []}}),
        ("issue_comment", tny.comment(issue, "Looks right to me.", STRANGER)),
        ("issue_comment", tny.comment(pr, "A note on the diff.", STRANGER, pr_body=f"Closes #{issue}")),
        ("pull_request_target", {"action": "synchronize", "pull_request": pr_payload(pr, issue)}),
        ("pull_request_review", {"action": "submitted", "pull_request": pr_payload(pr, issue),
                                 "review": {"state": "commented", "body": "Nice.", "user": {"login": STRANGER, "type": "User"}}}),
        ("pull_request_review_comment", {"action": "created", "pull_request": pr_payload(pr, issue),
                                         "comment": {"body": "Rename this.", "user": {"login": STRANGER, "type": "User"}}}),
        ("workflow_run", {"action": "completed", "workflow_run": {"name": "done-whens", "pull_requests": [
            {"number": pr, "head": {"ref": f"try/issue-{issue}"}}]}}),
    ]


# 331.1: any event about an issue or its pull request, and the end of every run, set both cards from state now

def test_any_event_puts_both_cards_where_the_issues_state_says(record_property, make):
    """Any event about an issue or its PR puts both cards where its state says.

    Proves 331.1. #57's code review approved, so it waits on the owner to merge: its card and its PR #60's belong in Review with
    Needs you. #58 (on autopilot), whose plan review sent it back to the planner, belongs in Plan with Autopilot, and
    so does its PR #61. Before each event both pairs of cards are put in the wrong place (Work with no pill, and Done
    with Needs you). Then one event of every kind arrives, none of them a command: a label, an edit, a comment on the
    issue, a comment on the PR, a new commit, a review, a line note and finished checks. After each one about #57,
    #57 and PR #60 must be in Review with Needs you; after each one about #58, #58 and PR #61 in Plan with Autopilot.
    #59's wrong card, which no event is about, is left as it was."""
    record_property("proves", "331.1")
    w = make(labels={("issue", 58): {LABEL}, ("pr", 61): {LABEL}}, prs={57: 60, 58: 61},
             records={57: tny.code_approved(), 58: tny.plan_blocked(), 59: tny.code_approved()})
    want = {57: {"issue #57": ("Review", NEEDS), "pr #60": ("Review", NEEDS)},
            58: {"issue #58": ("Plan", AUTO), "pr #61": ("Plan", AUTO)}}
    for issue, pr in ((57, 60), (58, 61)):
        for event, payload in events_about(issue, pr):
            w.cards.update({("issue", issue): {"Status": "Work"}, ("pr", pr): {"Status": "Done", "Action": NEEDS},
                            ("issue", 59): {"Status": "Done", "Action": AUTO}})
            board.sync(event, payload, SPEC, REPO)
            got = places(w, ("issue", issue), ("pr", pr))
            assert got == want[issue], \
                f"331.1: after a {event} {payload.get('action')} event about #{issue}, the cards are at {got}, not {want[issue]}"
            assert place(w, "issue", 59) == ("Done", AUTO), \
                f"331.1: a {event} event about #{issue} moved #59's card, which it is not about, to {place(w, 'issue', 59)}"


def test_the_next_event_fixes_what_a_dropped_or_late_event_left_wrong(record_property, make):
    """The next event fixes a card left wrong by a dropped or late event.

    Proves 331.1. #57 closed and its PR #60 merged on GitHub, but those events were dropped: both cards still sit in Review with
    Needs you. A plain comment on #57 arrives: both cards move to Done with no pill. Then the PR's old "opened" event
    arrives late: both stay in Done with no pill. #58 was moved to Done by hand though it is open with no record yet;
    a label on it puts it back in Backlog."""
    record_property("proves", "331.1")
    w = make(prs={57: 60}, records={57: tny.code_approved()}, closed={("issue", 57), ("pr", 60)},
             cards={("issue", 57): {"Status": "Review", "Action": NEEDS}, ("pr", 60): {"Status": "Review", "Action": NEEDS},
                    ("issue", 58): {"Status": "Done"}})
    board.sync("issue_comment", tny.comment(57, "Thanks, all good.", STRANGER, state="closed"), SPEC, REPO)
    got = places(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": ("Done", None), "pr #60": ("Done", None)}, \
        f"331.1: the close and merge events were dropped and the next event left the cards at {got}, not Done with no pill"
    board.sync("pull_request_target", {"action": "opened", "pull_request": pr_payload(60, 57)}, SPEC, REPO)
    got = places(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": ("Done", None), "pr #60": ("Done", None)}, \
        f"331.1: PR #60's opened event arrived after the merge and moved the cards to {got}"
    board.sync("issues", {"action": "labeled", "label": {"name": "bug"},
                          "issue": {"number": 58, "state": "open", "labels": [{"name": "bug"}]}}, SPEC, REPO)
    assert place(w, "issue", 58) == ("Backlog", None), \
        f"331.1: open #58 with no record was in Done and a label left it at {place(w, 'issue', 58)}, not Backlog"


def test_the_end_of_a_run_places_the_cards_from_state_not_from_the_run(record_property, make, monkeypatch, tmp_path):
    """A run's end places the cards from GitHub's state, not from the run.

    Proves 331.1. A run ends on #57, whose plan was approved and waits for the owner's /work, and the run's own board.txt says
    "Work none": #57 must be in Plan with Needs you. A run ends on #58 (on autopilot, with PR #61), whose code review
    sent it back to the worker, while board.txt says "Review needs": #58 and PR #61 must be in Work with Autopilot.
    Both runs' board steps exit 0."""
    record_property("proves", "331.1")
    blocked = tny.code_approved()[:-1] + [tny.rec("reviewer", "pr", {**tny.GOOD_REVIEW, "stage": "pr"})]
    w = make(labels={("issue", 58): {LABEL}, ("pr", 61): {LABEL}}, prs={58: 61},
             records={57: tny.plan_approved(), 58: blocked},
             cards={("issue", 57): {"Status": "Backlog"}, ("issue", 58): {"Status": "Done"}, ("pr", 61): {"Status": "Plan"}})
    code = run_ends(57, monkeypatch, tmp_path, "Work none\n")
    assert code == 0, f"331.1: the end of the run on #57 exited {code}, not 0"
    assert place(w, "issue", 57) == ("Plan", NEEDS), \
        f"331.1: #57's approved plan waits for /work, yet the end of its run put it at {place(w, 'issue', 57)}"
    code = run_ends(58, monkeypatch, tmp_path, "Review needs\n")
    assert code == 0, f"331.1: the end of the run on #58 exited {code}, not 0"
    got = places(w, ("issue", 58), ("pr", 61))
    assert got == {"issue #58": ("Work", AUTO), "pr #61": ("Work", AUTO)}, \
        f"331.1: #58's code review sent it back to the worker, yet the end of its run put the cards at {got}"


def test_needs_you_and_autopilot_follow_the_history_whichever_event_comes(record_property, make, monkeypatch, tmp_path):
    """Needs you shows exactly while the issue waits on you; Autopilot otherwise on autopilot.

    Proves 331.1. #57 (on autopilot, with PR #60) has a plan sent back to the planner: a run ends and both cards show Autopilot.
    Its reviewer then escalates and a run ends: both show Needs you. Switching autopilot off and on again leaves Needs
    you on both. The code owner says /plan: both show Autopilot again. #58, not waiting, is switched on autopilot and
    shows Autopilot, then off and shows nothing."""
    record_property("proves", "331.1")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}}, prs={57: 60}, records={57: tny.plan_blocked()})
    both = (("issue", 57), ("pr", 60))
    run_ends(57, monkeypatch, tmp_path)
    assert {k: p for k, (_, p) in places(w, *both).items()} == {"issue #57": AUTO, "pr #60": AUTO}, \
        f"331.1: #57 on autopilot goes on, yet its cards show {places(w, *both)}"
    w.records[57] = tny.escalated("plan")
    run_ends(57, monkeypatch, tmp_path)
    assert {k: p for k, (_, p) in places(w, *both).items()} == {"issue #57": NEEDS, "pr #60": NEEDS}, \
        f"331.1: #57's reviewer escalated, yet its cards show {places(w, *both)}"
    for action, on in (("unlabeled", False), ("labeled", True)):
        w.put("issue", 57, on)
        board.sync("issues", {"action": action, "label": {"name": LABEL},
                              "issue": {"number": 57, "state": "open", "labels": [{"name": LABEL}] if on else []}}, SPEC, REPO)
        assert {k: p for k, (_, p) in places(w, *both).items()} == {"issue #57": NEEDS, "pr #60": NEEDS}, \
            f"331.1: switching autopilot {'on' if on else 'off'} while #57 waits on the owner left {places(w, *both)}"
    w.records[57].append("/plan Go on with the planner's reading.")
    board.sync("issue_comment", tny.comment(57, "/plan Go on with the planner's reading.", labels=[LABEL]), SPEC, REPO)
    assert {k: p for k, (_, p) in places(w, *both).items()} == {"issue #57": AUTO, "pr #60": AUTO}, \
        f"331.1: the code owner answered #57 with /plan, yet its cards show {places(w, *both)}"
    for action, on, pill in (("labeled", True, AUTO), ("unlabeled", False, None)):
        w.put("issue", 58, on)
        board.sync("issues", {"action": action, "label": {"name": LABEL},
                              "issue": {"number": 58, "state": "open", "labels": [{"name": LABEL}] if on else []}}, SPEC, REPO)
        assert w.action("issue", 58) == pill, f"331.1: #58 switched {'on' if on else 'off'} autopilot shows {w.action('issue', 58)!r}"


def test_the_board_runs_on_every_event_about_an_issue_or_its_pull_request(record_property):
    """The board workflow runs on every event about an issue or its PR.

    Proves 331.1. Reads .github/workflows/board.yml's triggers: issues opened, edited, closed, reopened, labeled and unlabeled; a
    comment created; a pull request opened, reopened, synchronized and closed; a review submitted; a line note created;
    the done-whens checks completed; and the schedule */15 * * * *."""
    record_property("proves", "331.1")
    on = triggers(open(WORKFLOW).read())
    want = {"issues": {"opened", "edited", "closed", "reopened", "labeled", "unlabeled"}, "issue_comment": {"created"},
            "pull_request_target": {"opened", "reopened", "synchronize", "closed"}, "pull_request_review": {"submitted"},
            "pull_request_review_comment": {"created"}, "workflow_run": {"completed"}}
    missing = {e: sorted(t - on.get(e, set())) for e, t in want.items() if not t <= on.get(e, set())}
    assert not missing, f"331.1: board.yml does not run on these events about an issue or its pull request: {missing}"
    assert re.search(r"cron:\s*[\"']\*/15 \* \* \* \*[\"']", open(WORKFLOW).read()), "331.1: board.yml has no 15-minute schedule"


def triggers(text):
    """{event: {type, ...}} from a workflow's on: block."""
    block = re.split(r"(?m)^\S", text.split("\non:\n", 1)[1], maxsplit=1)[0]
    out = {}
    for m in re.finditer(r"(?m)^  (\w+):[^\n]*\n((?:    [^\n]*\n?)*)", block):
        types = re.search(r"types:\s*\[([^\]]*)\]", m.group(2))
        out[m.group(1)] = {t.strip() for t in types.group(1).split(",")} if types else set()
    return out


# 331.2: every 15 minutes a sweep sets every issue and pull request card on the board

def test_the_15_minute_sweep_puts_every_card_where_its_state_says(record_property, make):
    """Every 15 minutes, every card on the board goes where its state says.

    Proves 331.2. The scheduled run finds a board where every card is wrong: #57 (code review approved, waits for the merge) and its
    PR #60 in Plan with no pill; #58 (on autopilot, plan sent back to the planner) in Done with Needs you; #59 (no
    record yet) in Work with Needs you; #62 (split filed) in Plan with Needs you; #64 (plan approved, the code owner
    already said /work) in Review with Needs you; closed #63 in Plan with Needs you. After the run: #57 and PR #60 in
    Review with Needs you, #58 in Plan with Autopilot, #59 in Backlog, #62 in Work, #64 in Plan, #63 in Done, the last
    four with no pill."""
    record_property("proves", "331.2")
    wrong = {("issue", 57): ("Plan", None), ("pr", 60): ("Plan", None), ("issue", 58): ("Done", NEEDS),
             ("issue", 59): ("Work", NEEDS), ("issue", 62): ("Plan", NEEDS), ("issue", 64): ("Review", NEEDS),
             ("issue", 63): ("Plan", NEEDS)}
    w = make(labels={("issue", 58): {LABEL}}, prs={57: 60}, closed={("issue", 63)},
             records={57: tny.code_approved(), 58: tny.plan_blocked(), 62: tny.split_planned() + [tny.split_filed((201, 202))],
                      64: tny.plan_approved() + ["/work"], 63: tny.code_approved()},
             cards={k: {"Status": s, **({"Action": a} if a else {})} for k, (s, a) in wrong.items()})
    board.sync("schedule", {"schedule": "*/15 * * * *"}, SPEC, REPO)
    want = {"issue #57": ("Review", NEEDS), "pr #60": ("Review", NEEDS), "issue #58": ("Plan", AUTO),
            "issue #59": ("Backlog", None), "issue #62": ("Work", None), "issue #64": ("Plan", None), "issue #63": ("Done", None)}
    got = places(w, *wrong)
    bad = {k: f"{got[k]}, not {want[k]}" for k in want if got[k] != want[k]}
    assert not bad, f"331.2: after the 15-minute sweep these cards are in the wrong place: {bad}"


class Project:
    """GitHub's project as the real Board reads it: cards with Status and Action.

    Any fieldValueByName(name: "X") the query asks for, under an alias or not, is answered with that card's X, and
    fieldValues lists every field the card has set."""

    CARDS = [("Issue", 57, "OPEN", "Review", NEEDS, []), ("Issue", 58, "OPEN", "Plan", None, [LABEL]),
             ("PullRequest", 60, "MERGED", "Done", None, []), ("Issue", 59, "OPEN", None, None, [])]

    def q(self, query, **v):
        text = " ".join(query.split())
        asked = re.findall(r"(?:(\w+)\s*:\s*)?fieldValueByName\s*\(\s*name\s*:\s*\"(\w+)\"\s*\)", text)
        nodes = []
        for typename, n, state, status, action, labels in self.CARDS:
            fields = {"Status": status, "Action": action}
            node = {"id": f"ITEM_{n}", "content": {"__typename": typename, "number": n, "state": state,
                                                    "closed": state != "OPEN", "merged": state == "MERGED",
                                                    "labels": {"nodes": [{"name": x} for x in labels]}},
                    "fieldValues": {"nodes": [{"name": o, "field": {"name": f}} for f, o in fields.items() if o]}}
            for alias, field in asked:
                node[alias or "fieldValueByName"] = {"name": fields[field]} if fields.get(field) else None
            nodes.append(node)
        return {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
            {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Backlog", "Plan", "Work", "Review", "Done")]},
            {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": NEEDS}, {"id": "w-auto", "name": AUTO}]}]},
            "items": {"totalCount": len(nodes), "pageInfo": {"hasNextPage": False, "endCursor": None}, "nodes": nodes},
            "views": {"nodes": []}}}}

    def rest(self, method, path, **fields):
        return {}


def test_the_real_board_reads_each_cards_column_for_the_sweep(record_property):
    """The board reads every card's column, so the sweep knows what to fix.

    Proves 331.2. The real Board reads a project holding #57 in Review with Needs you, #58 (on autopilot) in Plan, merged PR #60 in
    Done and #59 in no column yet; each card it lists must carry that column as "status"."""
    record_property("proves", "331.2")
    got = board.Board("dokima-dev/1", "dokima-dev/dokima", q=Project().q, rest=Project().rest).cards()
    got = {(c["kind"], c["number"]): c.get("status") for c in got}
    want = {("issue", 57): "Review", ("issue", 58): "Plan", ("pr", 60): "Done", ("issue", 59): None}
    assert got == want, f"331.2: the board read the cards' columns as {got}, not {want}"


# 331.3: a closed issue, and a merged or closed pull request, sits in Done with no pill, whatever its labels

def test_closed_items_sit_in_done_with_no_pill_whatever_their_labels(record_property, make):
    """A closed issue or PR sits in Done with no pill, whatever its labels.

    Proves 331.3. #57 (labeled autopilot and high, its code review approved, so its history still reads as waiting on the owner)
    closes, and its PR #60 (labeled autopilot) merges: both must sit in Done with no pill. PR #61, built for open #58
    (plan sent back to the planner), is closed without merging: PR #61 must sit in Done with no pill while #58 stays in
    Plan. Beside them, open #59 on autopilot with no record sits in Backlog with Autopilot, so the rule does not reach
    open items."""
    record_property("proves", "331.3")
    w = make(labels={("issue", 57): {LABEL, "high"}, ("pr", 60): {LABEL}, ("issue", 59): {LABEL}}, prs={57: 60, 58: 61},
             records={57: tny.code_approved(), 58: tny.plan_blocked()},
             cards={("issue", 57): {"Status": "Review", "Action": NEEDS}, ("pr", 60): {"Status": "Review", "Action": AUTO},
                    ("pr", 61): {"Status": "Plan", "Action": NEEDS}, ("issue", 58): {"Status": "Plan"}})
    w.closed |= {("issue", 57), ("pr", 60)}
    board.sync("issues", {"action": "closed", "issue": {"number": 57, "state": "closed",
                                                         "labels": [{"name": LABEL}, {"name": "high"}]}}, SPEC, REPO)
    board.sync("pull_request_target", tny.pr_event("closed", 60, 57, merged=True), SPEC, REPO)
    got = places(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": ("Done", None), "pr #60": ("Done", None)}, \
        f"331.3: closed #57 and merged PR #60, both labeled autopilot, are at {got}, not Done with no pill"
    w.closed |= {("pr", 61)}
    board.sync("pull_request_target", tny.pr_event("closed", 61, 58), SPEC, REPO)
    got = places(w, ("pr", 61), ("issue", 58))
    assert got == {"pr #61": ("Done", None), "issue #58": ("Plan", None)}, \
        f"331.3: PR #61 closed unmerged and the cards are at {got}; the PR belongs in Done, its open issue in Plan"
    board.sync("issues", {"action": "labeled", "label": {"name": LABEL},
                          "issue": {"number": 59, "state": "open", "labels": [{"name": LABEL}]}}, SPEC, REPO)
    assert place(w, "issue", 59) == ("Backlog", AUTO), f"331.3: open #59 on autopilot is at {place(w, 'issue', 59)}"


def test_the_sweep_puts_closed_items_in_done_with_no_pill(record_property, make):
    """The 15-minute sweep puts every closed card in Done with no pill.

    Proves 331.3. The board holds about forty closed cards in the wrong place: closed issues #100 to #119, half on autopilot, in
    Work with Needs you or Autopilot, and merged PRs #120 to #139, half on autopilot, in Review with Needs you. After
    the scheduled run every one of them is in Done with no pill, while open #57 on autopilot (no record) stays in
    Backlog with Autopilot."""
    record_property("proves", "331.3")
    closed = [("issue", n) for n in range(100, 120)] + [("pr", n) for n in range(120, 140)]
    w = make(labels={**{k: {LABEL} for k in closed[::2]}, ("issue", 57): {LABEL}}, closed=set(closed),
             cards={**{k: {"Status": "Work" if k[0] == "issue" else "Review", "Action": NEEDS if k[1] % 4 else AUTO}
                       for k in closed}, ("issue", 57): {"Status": "Backlog", "Action": AUTO}})
    board.sync("schedule", {"schedule": "*/15 * * * *"}, SPEC, REPO)
    wrong = {f"{k} #{n}": place(w, k, n) for k, n in closed if place(w, k, n) != ("Done", None)}
    assert not wrong, f"331.3: after the sweep these closed cards are not in Done with no pill: {wrong}"
    assert place(w, "issue", 57) == ("Backlog", AUTO), f"331.3: the sweep moved open #57 to {place(w, 'issue', 57)}"


# 331.4: an issue and its pull request share one board queue that keeps the newest recompute

def queue_of(event, payload, tmp_path):
    """The board queue `python3 -m dokima.board queue` names for this event, read from GITHUB_OUTPUT's group=."""
    path, out = tmp_path / "event.json", tmp_path / "output.txt"
    path.write_text(json.dumps(payload))
    out.write_text("")
    env = {k: v for k, v in os.environ.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN", "DOKIMA_BOARD")}
    env.update(GITHUB_EVENT_NAME=event, GITHUB_EVENT_PATH=str(path), GITHUB_OUTPUT=str(out), GITHUB_REPOSITORY=REPO,
               PYTHONPATH=os.path.abspath(ROOT))
    done = subprocess.run([sys.executable, "-m", "dokima.board", "queue"], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=30)
    assert done.returncode == 0, f"331.4: `python3 -m dokima.board queue` failed on a {event} event: {done.stderr or done.stdout}"
    groups = re.findall(r"(?m)^group=(.+)$", out.read_text())
    assert len(groups) == 1, f"331.4: the queue step wrote {out.read_text()!r} to GITHUB_OUTPUT, not one group=..."
    return groups[0].strip()


def test_an_issue_and_its_pull_request_share_one_board_queue(record_property, tmp_path):
    """An issue and its PR share one board queue, and another issue never shares it.

    Proves 331.4. Names the queue, without reaching GitHub, for every event about #57 or its PR #60 (each kind events_about lists,
    plus the PR opening and merging and a code owner's command on the PR): all must name one and the same queue. The
    same events about #58 and its PR #61 must name one queue too, different from #57's, and the 15-minute schedule a
    queue of its own."""
    record_property("proves", "331.4")
    seen = {}
    for issue, pr in ((57, 60), (58, 61)):
        evs = events_about(issue, pr) + [
            ("pull_request_target", {"action": "opened", "pull_request": pr_payload(pr, issue)}),
            ("pull_request_target", {"action": "closed", "pull_request": {**pr_payload(pr, issue), "merged": True}}),
            ("issue_comment", tny.comment(pr, "/review", pr_body=f"Closes #{issue}"))]
        seen[issue] = {f"{e} {p.get('action')}": queue_of(e, p, tmp_path) for e, p in evs}
        assert len(set(seen[issue].values())) == 1, \
            f"331.4: events about #{issue} and its PR #{pr} landed in different queues: {seen[issue]}"
    q57, q58 = next(iter(seen[57].values())), next(iter(seen[58].values()))
    assert q57 != q58, f"331.4: #57 and #58 share the queue {q57!r}, so one issue's run can wait on or replace another's"
    sweep = queue_of("schedule", {"schedule": "*/15 * * * *"}, tmp_path)
    assert sweep not in (q57, q58), f"331.4: the 15-minute sweep shares the queue {sweep!r} of an issue"


def jobs(text):
    """{job id: its block of text} from a workflow's jobs: section."""
    body = text.split("\njobs:\n", 1)[1]
    parts = re.split(r"(?m)^  (\w[\w-]*):\s*\n", body)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def test_the_board_workflow_joins_that_queue_and_never_cancels_a_running_recompute(record_property):
    """The board workflow queues each recompute by issue and never cancels one.

    Proves 331.4. Reads .github/workflows/board.yml: one job runs `python3 -m dokima.board queue` in a step with an id and exposes
    that step's group output; the job that syncs the board needs that job, takes its concurrency group from that
    output, and sets cancel-in-progress to false, so GitHub keeps the running recompute and only the newest waiting
    one. No workflow-wide concurrency group keyed by the event's issue or pull request number is left."""
    record_property("proves", "331.4")
    text = open(WORKFLOW).read()
    head = text.split("\njobs:\n", 1)[0]
    assert "github.event.issue.number" not in head and "github.event.pull_request.number" not in head, \
        "331.4: board.yml still queues runs by the event's issue or pull request number, so an issue and its PR run apart"
    found = jobs(text)
    queue = next((j for j, b in found.items() if "python3 -m dokima.board queue" in b), None)
    assert queue, f"331.4: no job in board.yml runs `python3 -m dokima.board queue` (jobs: {sorted(found)})"
    step = re.search(r"-\s*id:\s*([\w-]+)\s*\n(?:\s+[^\n]*\n)*?\s+run:[^\n]*python3 -m dokima\.board queue", found[queue]) or \
        re.search(r"id:\s*([\w-]+)[^\n]*\n(?:[^\n]*\n){0,8}?[^\n]*python3 -m dokima\.board queue", found[queue])
    assert step, f"331.4: the step running `python3 -m dokima.board queue` in job {queue!r} has no id"
    assert re.search(r"outputs:\s*\n\s+group:\s*\$\{\{\s*steps\." + re.escape(step.group(1)) + r"\.outputs\.group\s*\}\}",
                     found[queue]), f"331.4: job {queue!r} does not expose its queue step's group output as outputs.group"
    sync = next((j for j, b in found.items() if re.search(r"run:\s*python3 -m dokima\.board\s*$", b, re.M)), None)
    assert sync, "331.4: no job in board.yml runs `python3 -m dokima.board` to sync the board"
    block = found[sync]
    assert re.search(r"needs:\s*\[?\s*[\w\-, ]*\b" + re.escape(queue) + r"\b", block), \
        f"331.4: the sync job {sync!r} does not need the queue job {queue!r}"
    group = re.search(r"concurrency:\s*\n\s+group:\s*([^\n]+)\n\s+cancel-in-progress:\s*(\w+)", block)
    assert group, f"331.4: the sync job {sync!r} has no concurrency group with cancel-in-progress"
    assert re.search(r"\$\{\{\s*needs\." + re.escape(queue) + r"\.outputs\.group\s*\}\}", group.group(1)), \
        f"331.4: the sync job's concurrency group is {group.group(1)!r}, not the queue job's group output"
    assert group.group(2) == "false", "331.4: the sync job cancels a running recompute (cancel-in-progress is not false)"


# 331.5: the per-event board rules this replaces are removed, and the board code is smaller

def test_the_per_event_board_rules_are_removed(record_property):
    """The rules that set the board from the event alone are gone.

    Proves 331.5. dokima/board.py no longer has decide() (an event to a column), keeps() (events that keep Needs you), answered()
    (a command clearing the pill from the event) or YOUR_TURN (bot comment texts that meant Needs you), and
    dokima/agent.py no longer has move_card() (the card put where the run said)."""
    record_property("proves", "331.5")
    left = [f"board.{n}" for n in ("decide", "keeps", "answered", "YOUR_TURN") if hasattr(board, n)] + \
        [f"agent.{n}" for n in ("move_card",) if hasattr(agent, n)]
    assert not left, f"331.5: these per-event board rules are still there: {', '.join(left)}"


def test_the_board_code_is_shorter_than_before(record_property):
    """The board code has fewer lines than before.

    Proves 331.5. Counts lines: dokima/board.py must have fewer than its 446 before this, and dokima/board.py and dokima/agent.py
    together fewer than their 2516 (446 and 2070), so nothing is just moved into agent.py."""
    record_property("proves", "331.5")
    count = lambda p: len(open(os.path.join(ROOT, p)).read().splitlines())
    b, a = count("dokima/board.py"), count("dokima/agent.py")
    assert b < 446, f"331.5: dokima/board.py has {b} lines, not fewer than the 446 it had before"
    assert a + b < 2516, f"331.5: dokima/board.py and dokima/agent.py have {a + b} lines together, not fewer than 2516"


# 331.6: a card whose state GitHub cannot give keeps its column and pill, and the run fails naming it

def test_an_unreadable_card_keeps_its_place_and_the_run_fails_naming_it(record_property, make, monkeypatch, tmp_path, capsys):
    """A card GitHub cannot read keeps its place, and the run fails naming it.

    Proves 331.6. GitHub answers nothing about #63 (HTTP 502); its card is in Plan with Needs you. A comment on #63 reaches the
    board: the run must fail with a reason naming #63, and the card stays in Plan with Needs you. The end of a run on
    #63 exits 1 with an ::error line naming #63, the card again unchanged. Beside it, the same comment on readable
    #57 (no record, card in Work) succeeds and moves it to Backlog, so the run does not fail on everything."""
    record_property("proves", "331.6")
    w = make(unreadable={63}, cards={("issue", 63): {"Status": "Plan", "Action": NEEDS}, ("issue", 57): {"Status": "Work"}})
    board.sync("issue_comment", tny.comment(57, "Any news?", STRANGER), SPEC, REPO)
    assert place(w, "issue", 57) == ("Backlog", None), f"331.6: readable #57 ended at {place(w, 'issue', 57)}, not Backlog"
    with pytest.raises(RuntimeError) as e:
        board.sync("issue_comment", tny.comment(63, "Any news?", STRANGER), SPEC, REPO)
    assert "#63" in str(e.value), f"331.6: the board run failed without naming #63: {e.value}"
    assert place(w, "issue", 63) == ("Plan", NEEDS), f"331.6: GitHub could not read #63, yet its card moved to {place(w, 'issue', 63)}"
    capsys.readouterr()
    code = run_ends(63, monkeypatch, tmp_path)
    out = capsys.readouterr()
    assert code == 1, f"331.6: the end of a run on unreadable #63 exited {code}, not 1"
    assert re.search(r"::error[^\n]*#63", out.out + out.err), f"331.6: the end of the run did not say ::error naming #63: {out.out + out.err!r}"
    assert place(w, "issue", 63) == ("Plan", NEEDS), f"331.6: the end of a run moved unreadable #63 to {place(w, 'issue', 63)}"


def test_the_sweep_fixes_the_rest_and_fails_naming_the_unreadable_card(record_property, make):
    """The sweep fixes every readable card and fails naming the unreadable one.

    Proves 331.6. The scheduled run finds #63 (unreadable) in Review with Autopilot, #59 (no record) in Work with Needs you and
    closed #64 in Plan. #59 must end in Backlog with no pill and #64 in Done with no pill, #63 must stay in Review with
    Autopilot, and the run must fail with a reason naming #63 but not #59 or #64."""
    record_property("proves", "331.6")
    w = make(unreadable={63}, closed={("issue", 64)},
             cards={("issue", 63): {"Status": "Review", "Action": AUTO}, ("issue", 59): {"Status": "Work", "Action": NEEDS},
                    ("issue", 64): {"Status": "Plan"}})
    with pytest.raises(RuntimeError) as e:
        board.sync("schedule", {"schedule": "*/15 * * * *"}, SPEC, REPO)
    assert "#63" in str(e.value) and "#59" not in str(e.value) and "#64" not in str(e.value), \
        f"331.6: the sweep's failure must name #63 and only it: {e.value}"
    got = places(w, ("issue", 63), ("issue", 59), ("issue", 64))
    want = {"issue #63": ("Review", AUTO), "issue #59": ("Backlog", None), "issue #64": ("Done", None)}
    assert got == want, f"331.6: after a sweep that could not read #63, the cards are at {got}, not {want}"
