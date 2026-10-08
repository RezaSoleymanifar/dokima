"""The board shows what runs on autopilot: an Autopilot pill, Needs you in its place when the river stops, one view (#210).

The board is faked at the size of dokima.board.Board, so these tests read the board's end state, never the GraphQL
queries that reach it. The fake keeps, in memory, one world shared with a fake `gh`:

- cards: each card's Status and Action (the single-select field holding "Needs you" and now "Autopilot");
- labels: the labels each issue and pull request carries; `autopilot` is autopilot's state (story 1, #209);
- the open pull request of each issue (branch try/issue-N, body "Closes #N");
- the board's views by name.

What the fake Board offers, and the code is expected to use:
    Board(spec, repo, q)               the board, as today
    .fields                            {"Status": (id, {option: id}), "Action": (id, {option: id})}, as today
    .item(kind, n) -> item id          as today; kind is "issue" or "pr"
    .set(item, field, option or None)  as today: an unknown field or option is ignored, None clears
    .value(item, field) -> option      the card's current option of that field, or None
    .autopilot(kind, n) -> bool        whether that issue or pull request carries the `autopilot` label
    .open_pr(n) -> number or None      the open pull request built for issue n
    .label(kind, n, on)                put the `autopilot` label on (True) or off (False) that issue or pull request
    .views() -> [name, ...]            the board's views
    .add_view(name, layout, filter)    add a view to the board

The fake `gh` answers `pr list` (the issue's open pull request), `issue view` and `api repos/o/r/issues/N` (with
labels), `issue create`, sub-issue and blocked-by links, and labels added through `issue create --label`,
`issue edit --add-label/--remove-label` or the REST labels API, all against the same world.
"""
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, board  # noqa: E402
from test_agent import GOOD_REVIEW, SPLIT, rec  # noqa: E402

LABEL = "autopilot"
SPEC, REPO = "dokima-dev/1", "dokima-dev/dokima"
BOT, YOU = {"type": "Bot"}, {"type": "User"}


class World:
    """The GitHub the board and `gh` both see: cards, labels, open pull requests and views."""

    def __init__(self, labels=None, prs=None, cards=None, views=("Needs you",), options=("Needs you", "Autopilot")):
        self.labels = {k: set(v) for k, v in (labels or {}).items()}
        self.prs = dict(prs or {})
        self.cards = {k: dict(v) for k, v in (cards or {}).items()}
        self.view_list = [{"name": v, "layout": "table", "filter": ""} for v in views]
        self.options = options
        self.created = 200
        self.calls = []

    def action(self, kind, n):
        """The card's Action pill: "Needs you", "Autopilot" or None."""
        return self.cards.get((kind, n), {}).get("Action")

    def status(self, kind, n):
        return self.cards.get((kind, n), {}).get("Status")

    def has(self, kind, n):
        return LABEL in self.labels.get((kind, n), set())

    def put(self, kind, n, on):
        s = self.labels.setdefault((kind, n), set())
        s.add(LABEL) if on else s.discard(LABEL)


def fake_board(world):
    """A stand-in for dokima.board.Board that reads and writes the world."""

    class FakeBoard:
        def __init__(self, *a, **k):
            self.fields = {"Status": ("S", {o: "s-" + o for o in ("Backlog", "Plan", "Work", "Review", "Done")}),
                           "Action": ("W", {o: "w-" + o for o in world.options})}

        def item(self, kind, n):
            world.cards.setdefault((kind, int(n)), {})
            return (kind, int(n))

        def set(self, iid, field, option):
            if field not in self.fields:
                return
            card = world.cards.setdefault(iid, {})
            if option is None:
                card.pop(field, None)
            elif option in self.fields[field][1]:
                card[field] = option

        def value(self, iid, field):
            return world.cards.get(iid, {}).get(field)

        def autopilot(self, kind, n):
            return world.has(kind, int(n))

        def open_pr(self, n):
            return world.prs.get(int(n))

        def label(self, kind, n, on):
            world.put(kind, int(n), on)

        def views(self):
            return [v["name"] for v in world.view_list]

        def add_view(self, name, layout, filter):
            world.view_list.append({"name": name, "layout": layout, "filter": filter})

    return FakeBoard


def fake_gh(world):
    """A stand-in for agent.gh that answers from the world."""

    def gh(*args):
        world.calls.append(args)
        a = list(args)
        if a[:2] == ["pr", "list"]:
            head = a[a.index("--head") + 1]
            n = world.prs.get(int(head.rsplit("-", 1)[1]))
            return f"{n}\n" if n else "\n"
        if a[:2] == ["issue", "view"]:
            n = int(a[2])
            return json.dumps({"number": n, "title": "Parent", "body": "", "comments": [],
                               "labels": [{"name": l} for l in sorted(world.labels.get(("issue", n), set()))]})
        if a[:2] == ["issue", "create"]:
            world.created += 1
            n = world.created
            if "--label" in a and LABEL in a[a.index("--label") + 1].split(","):
                world.put("issue", n, True)
            return f"https://github.com/o/r/issues/{n}\n"
        if a[:2] == ["issue", "edit"]:
            n = int(a[2])
            if "--add-label" in a and LABEL in a[a.index("--add-label") + 1].split(","):
                world.put("issue", n, True)
            if "--remove-label" in a and LABEL in a[a.index("--remove-label") + 1].split(","):
                world.put("issue", n, False)
            return ""
        if a[:1] == ["api"]:
            path = next((x for x in a[1:] if x.lstrip("/").startswith("repos/")), "").lstrip("/")
            method = a[a.index("-X") + 1].upper() if "-X" in a else ("POST" if any(x in ("-f", "-F") for x in a) else "GET")
            m_lab = re.fullmatch(r"repos/o/r/issues/(\d+)/labels(?:/(.+))?", path)
            if m_lab:
                n = int(m_lab.group(1))
                if method == "DELETE":
                    world.put("issue", n, False)
                elif method in ("POST", "PUT") and any(x in (f"labels[]={LABEL}", f"labels={LABEL}") for x in a):
                    world.put("issue", n, True)
                return "[]"
            m_iss = re.fullmatch(r"repos/o/r/issues/(\d+)", path)
            if m_iss and method == "GET":
                n = int(m_iss.group(1))
                return json.dumps({"id": 9000 + n, "number": n,
                                   "labels": [{"name": l} for l in sorted(world.labels.get(("issue", n), set()))]})
            return "{}"
        return ""

    return gh


@pytest.fixture
def make(monkeypatch):
    """Wire a world into dokima.board.Board and dokima.agent.gh, and return it."""

    def wire(**kw):
        world = World(**kw)
        monkeypatch.setattr(board, "Board", fake_board(world))
        monkeypatch.setattr(agent, "gh", fake_gh(world))
        return world

    return wire


def label_event(action, name, labels, number=57):
    """An issues labeled/unlabeled payload; labels are the issue's labels after the change, as GitHub sends them."""
    return {"action": action, "label": {"name": name}, "issue": {"number": number, "labels": [{"name": n} for n in labels]}}


def comment_event(number, body, labels, user=BOT):
    return {"action": "created", "issue": {"number": number, "labels": [{"name": n} for n in labels]},
            "comment": {"user": user, "body": body}}


def pr_event(action, number, issue):
    return {"action": action, "pull_request": {"number": number, "body": f"Closes #{issue}", "merged": False,
                                               "head": {"ref": f"try/issue-{issue}"}, "labels": []}}


# 210.1: every card in a tree on autopilot shows the Autopilot pill, and loses it once off autopilot

def test_switching_autopilot_on_puts_the_pill_on_the_issue_and_its_pull_request(record_property, make):
    """Switching an issue on autopilot puts the Autopilot pill on its card and its open pull request's card.

    The `autopilot` label is added to #57 (open PR #60) and to #101 (no PR), as `/autopilot start` does for every issue
    in a tree; each label event reaches the board sync. Both issue cards and PR #60 show Autopilot and no card's stage
    moves. A `bug` label on #58, which is not on autopilot, puts no Autopilot pill anywhere."""
    record_property("proves", "210.1")
    w = make(labels={("issue", 57): {LABEL}, ("issue", 101): {LABEL}}, prs={57: 60},
             cards={("issue", 57): {"Status": "Plan"}, ("pr", 60): {"Status": "Review"}, ("issue", 101): {"Status": "Backlog"}})
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 101), SPEC, REPO)
    for kind, n in (("issue", 57), ("pr", 60), ("issue", 101)):
        assert w.action(kind, n) == "Autopilot", f"210.1: {kind} #{n} on autopilot shows {w.action(kind, n)!r}, not the Autopilot pill"
    assert (w.status("issue", 57), w.status("pr", 60), w.status("issue", 101)) == ("Plan", "Review", "Backlog"), \
        "210.1: switching autopilot on moved a card to another column"
    w.labels[("issue", 58)] = {"bug"}
    w.cards[("issue", 58)] = {"Status": "Plan"}
    board.sync("issues", label_event("labeled", "bug", ["bug"], 58), SPEC, REPO)
    assert w.action("issue", 58) is None, "210.1: an issue that is not on autopilot got the Autopilot pill"


def test_switching_autopilot_off_takes_the_pill_away(record_property, make):
    """Switching an issue off autopilot takes the Autopilot pill off its card and its open pull request's card.

    #57 and its PR #60 show Autopilot; the `autopilot` label is removed from #57, as `/autopilot stop` does. Both
    cards end with no pill and stay in their columns."""
    record_property("proves", "210.1")
    w = make(labels={("issue", 57): set(), ("pr", 60): {LABEL}}, prs={57: 60},
             cards={("issue", 57): {"Status": "Work", "Action": "Autopilot"}, ("pr", 60): {"Status": "Review", "Action": "Autopilot"}})
    board.sync("issues", label_event("unlabeled", LABEL, [], 57), SPEC, REPO)
    assert w.action("issue", 57) is None, f"210.1: issue #57 off autopilot still shows {w.action('issue', 57)!r}"
    assert w.action("pr", 60) is None, f"210.1: PR #60, whose issue is off autopilot, still shows {w.action('pr', 60)!r}"
    assert (w.status("issue", 57), w.status("pr", 60)) == ("Work", "Review"), "210.1: switching autopilot off moved a card"


def test_stage_moments_keep_the_pill_on_issues_on_autopilot_only(record_property, make):
    """When the board moves a card to the next stage, a card on autopilot keeps its Autopilot pill; others get none.

    Runs the board sync's stage moments (the work label, a pull request opened, changes requested) for #57, on autopilot
    with PR #60, and for #58, not on autopilot, with PR #61. Every #57 and #60 card ends in the new column with
    Autopilot; every #58 and #61 card ends in the new column with no pill."""
    record_property("proves", "210.1")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}, ("issue", 58): set()}, prs={57: 60, 58: 61})
    board.sync("issues", label_event("labeled", "work", [LABEL, "work"], 57), SPEC, REPO)
    board.sync("issues", label_event("labeled", "work", ["work"], 58), SPEC, REPO)
    assert (w.status("issue", 57), w.action("issue", 57)) == ("Work", "Autopilot"), \
        f"210.1: #57 on autopilot moved to Work shows {w.action('issue', 57)!r}, not Autopilot"
    assert (w.status("issue", 58), w.action("issue", 58)) == ("Work", None), "210.1: #58, not on autopilot, got a pill"
    board.sync("pull_request_target", pr_event("opened", 60, 57), SPEC, REPO)
    board.sync("pull_request_target", pr_event("opened", 61, 58), SPEC, REPO)
    for kind, n in (("pr", 60), ("issue", 57)):
        assert (w.status(kind, n), w.action(kind, n)) == ("Review", "Autopilot"), \
            f"210.1: {kind} #{n} on autopilot in Review shows {w.action(kind, n)!r}, not Autopilot"
    for kind, n in (("pr", 61), ("issue", 58)):
        assert (w.status(kind, n), w.action(kind, n)) == ("Review", None), f"210.1: {kind} #{n}, not on autopilot, got a pill"
    review = {"action": "submitted", "review": {"state": "changes_requested"}, "pull_request": {"number": 60, "body": "Closes #57"}}
    board.sync("pull_request_review", review, SPEC, REPO)
    assert (w.status("pr", 60), w.action("pr", 60)) == ("Work", "Autopilot"), "210.1: PR #60 sent back to Work lost its Autopilot pill"


def test_the_river_keeps_the_pill_when_it_moves_a_card_on_autopilot(record_property, make):
    """When the river starts the next stage, the issue and its pull request keep the Autopilot pill while on autopilot.

    Calls the river's card move (agent.move_card, as `agent board` does after every run) for #57, on autopilot with
    open PR #60, and for #58, not on autopilot, with open PR #61. #57 and #60 land in Review with Autopilot; #58 and
    #61 land in Review with no pill."""
    record_property("proves", "210.1")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}, ("issue", 58): set()}, prs={57: 60, 58: 61})
    agent.move_card("o/r", "57", "Review", False, "o/1")
    agent.move_card("o/r", "58", "Review", False, "o/1")
    for kind, n in (("issue", 57), ("pr", 60)):
        assert (w.status(kind, n), w.action(kind, n)) == ("Review", "Autopilot"), \
            f"210.1: the river moved {kind} #{n}, on autopilot, and it shows {w.action(kind, n)!r}, not Autopilot"
    for kind, n in (("issue", 58), ("pr", 61)):
        assert (w.status(kind, n), w.action(kind, n)) == ("Review", None), f"210.1: the river gave {kind} #{n}, not on autopilot, a pill"


# 210.2: children filed by a split under a parent on autopilot are on autopilot too

def split_main(monkeypatch, w, parent=139):
    """Run `agent split PARENT` for an approved split, the way the /work command does, against the world."""
    recs = [rec("planner", handback=SPLIT), rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})]
    monkeypatch.setattr(agent, "conversation", lambda repo, n: ({}, []))
    monkeypatch.setattr(agent, "records", lambda items: list(recs))
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("CARD_ID", "")
    return agent.main(["agent", "split", str(parent)])


def test_a_split_under_a_parent_on_autopilot_files_children_on_autopilot(record_property, make, monkeypatch):
    """Stories filed by a split under a parent on autopilot get the autopilot label and the Autopilot pill; others don't.

    Files an approved two-story split of #139, which carries the `autopilot` label, on a board. Both new issues carry
    the label, land in Backlog with Autopilot, and #139 shows Work with Autopilot. Then files the same split of a #139
    not on autopilot: no new issue carries the label and no card shows Autopilot."""
    record_property("proves", "210.2")
    w = make(labels={("issue", 139): {LABEL}})
    monkeypatch.setenv("DOKIMA_BOARD", "o/1")
    assert split_main(monkeypatch, w) == 0
    children = [n for (kind, n) in w.cards if kind == "issue" and n != 139]
    assert sorted(children) == [201, 202], f"210.2: the split's stories were not placed on the board: {children}"
    for n in (201, 202):
        assert w.has("issue", n), f"210.2: story #{n}, filed under #139 on autopilot, does not carry the autopilot label"
        assert (w.status("issue", n), w.action("issue", n)) == ("Backlog", "Autopilot"), \
            f"210.2: story #{n} landed as {w.status('issue', n)!r} with {w.action('issue', n)!r}, not Backlog with Autopilot"
    assert (w.status("issue", 139), w.action("issue", 139)) == ("Work", "Autopilot"), \
        f"210.2: parent #139 on autopilot shows {w.action('issue', 139)!r} after its split, not Autopilot"
    w = make(labels={("issue", 139): {"bug"}})
    assert split_main(monkeypatch, w) == 0
    for n in (201, 202):
        assert not w.has("issue", n), f"210.2: story #{n}, under a parent not on autopilot, was put on autopilot"
        assert (w.status("issue", n), w.action("issue", n)) == ("Backlog", None), f"210.2: story #{n}, not on autopilot, got a pill"
    assert w.action("issue", 139) is None, "210.2: parent #139, not on autopilot, got the Autopilot pill"


# 210.3: Needs you takes the Autopilot pill's place when the river stops for the owner, never both

def test_needs_you_replaces_autopilot_when_the_river_stops_and_autopilot_returns_after(record_property, make):
    """When the river stops for the owner on an issue on autopilot, its card shows Needs you instead; Autopilot returns after.

    For #57 on autopilot with PR #60: the river stops (move_card with Needs you) and both cards show Needs you; it goes
    on (move_card without) and both show Autopilot again. The board sync does the same: a planner question shows Needs
    you on #57, the work label after it shows Autopilot, and done-whens finishing on PR #60 shows Needs you on it."""
    record_property("proves", "210.3")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}}, prs={57: 60})
    agent.move_card("o/r", "57", "Plan", True, "o/1")
    for kind, n in (("issue", 57), ("pr", 60)):
        assert w.action(kind, n) == "Needs you", f"210.3: the river stopped for the owner and {kind} #{n} shows {w.action(kind, n)!r}"
    agent.move_card("o/r", "57", "Work", False, "o/1")
    for kind, n in (("issue", 57), ("pr", 60)):
        assert w.action(kind, n) == "Autopilot", f"210.3: the river went on and {kind} #{n} shows {w.action(kind, n)!r}, not Autopilot"
    board.sync("issue_comment", comment_event(57, "**Planner question**\n\nWhich?", [LABEL]), SPEC, REPO)
    assert w.action("issue", 57) == "Needs you", f"210.3: a question for the owner on #57 shows {w.action('issue', 57)!r}"
    board.sync("issues", label_event("labeled", "work", [LABEL, "work"], 57), SPEC, REPO)
    assert w.action("issue", 57) == "Autopilot", f"210.3: #57 went on after the question and shows {w.action('issue', 57)!r}"
    board.sync("workflow_run", {"action": "completed", "workflow_run": {"pull_requests": [{"number": 60}]}}, SPEC, REPO)
    assert w.action("pr", 60) == "Needs you", f"210.3: PR #60 waiting on the owner shows {w.action('pr', 60)!r}"


def test_switching_autopilot_never_hides_needs_you(record_property, make):
    """Switching autopilot on or off while the card waits on the owner leaves Needs you, so no card shows both or loses it.

    #57 and PR #60 show Needs you. Adding the `autopilot` label keeps Needs you on both; removing it keeps Needs you
    on both. A card off autopilot that shows Autopilot by mistake loses it, so the switch does act."""
    record_property("proves", "210.3")
    w = make(labels={("issue", 57): {LABEL}}, prs={57: 60},
             cards={("issue", 57): {"Status": "Plan", "Action": "Needs you"}, ("pr", 60): {"Status": "Review", "Action": "Needs you"}})
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
    for kind, n in (("issue", 57), ("pr", 60)):
        assert w.action(kind, n) == "Needs you", f"210.3: switching autopilot on replaced Needs you on {kind} #{n} with {w.action(kind, n)!r}"
    w.labels[("issue", 57)] = set()
    board.sync("issues", label_event("unlabeled", LABEL, [], 57), SPEC, REPO)
    for kind, n in (("issue", 57), ("pr", 60)):
        assert w.action(kind, n) == "Needs you", f"210.3: switching autopilot off cleared Needs you on {kind} #{n}"
    w.cards[("issue", 58)] = {"Status": "Plan", "Action": "Autopilot"}
    board.sync("issues", label_event("unlabeled", LABEL, [], 58), SPEC, REPO)
    assert w.action("issue", 58) is None, "210.3: switching autopilot off left the Autopilot pill on #58"


# 210.4: one Autopilot table view lists every issue and pull request on autopilot

def test_the_board_gets_one_autopilot_table_view(record_property, make):
    """The first issue switched on autopilot gives the board an Autopilot view, a table showing only what carries the label.

    On a board with only the Needs you view, switching #57 on autopilot adds exactly one view: named Autopilot, laid
    out as a table, filtered to label:autopilot. Switching #101 on afterwards adds no second view, and a stage moment
    on a board without the view adds none."""
    record_property("proves", "210.4")
    w = make(labels={("issue", 57): {LABEL}, ("issue", 101): {LABEL}, ("issue", 58): set()})
    board.sync("issues", label_event("labeled", "work", ["work"], 58), SPEC, REPO)
    assert [v["name"] for v in w.view_list] == ["Needs you"], "210.4: a board change unrelated to autopilot added a view"
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
    added = [v for v in w.view_list if v["name"] != "Needs you"]
    assert added == [{"name": "Autopilot", "layout": "table", "filter": f"label:{LABEL}"}], \
        f"210.4: switching autopilot on added {added}, not one Autopilot table view filtered to label:{LABEL}"
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 101), SPEC, REPO)
    assert [v["name"] for v in w.view_list].count("Autopilot") == 1, "210.4: the Autopilot view was added twice"


def test_pull_requests_on_autopilot_carry_the_label_so_the_view_lists_them(record_property, make):
    """A pull request built for an issue on autopilot carries the autopilot label, so the view lists it; it loses it after.

    Switching #57 on autopilot labels its open PR #60; switching it off removes the label. A PR opened for #57 while on
    autopilot (#62) is labeled when it opens; one opened for #58, not on autopilot (#61), is not."""
    record_property("proves", "210.4")
    w = make(labels={("issue", 57): {LABEL}, ("issue", 58): set()}, prs={57: 60, 58: 61})
    board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
    assert w.has("pr", 60), "210.4: PR #60, built for #57 on autopilot, does not carry the autopilot label"
    w.labels[("issue", 57)] = set()
    board.sync("issues", label_event("unlabeled", LABEL, [], 57), SPEC, REPO)
    assert not w.has("pr", 60), "210.4: PR #60 still carries the autopilot label after #57 went off autopilot"
    w.labels[("issue", 57)] = {LABEL}
    w.prs[57] = 62
    board.sync("pull_request_target", pr_event("opened", 62, 57), SPEC, REPO)
    board.sync("pull_request_target", pr_event("opened", 61, 58), SPEC, REPO)
    assert w.has("pr", 62), "210.4: PR #62, opened for #57 on autopilot, does not carry the autopilot label"
    assert not w.has("pr", 61), "210.4: PR #61, built for #58 not on autopilot, was labeled autopilot"


# 210.5: in a repo without a board, autopilot still works and nothing fails

def test_without_a_board_autopilot_still_works_and_nothing_fails(record_property, make, monkeypatch):
    """Without a board, the label events touch nothing and a split under a parent on autopilot still labels its stories.

    Runs the board sync for the autopilot label with no board set and a GitHub stand-in that fails on any call; then
    files a split of #139 on autopilot with no DOKIMA_BOARD, with the Board failing if built: it succeeds and both new
    issues carry the autopilot label."""
    record_property("proves", "210.5")

    def explode(*a, **k):
        raise AssertionError("210.5: the board was reached without a board set")

    for action, labels in (("labeled", [LABEL]), ("unlabeled", [])):
        assert not board.sync("issues", label_event(action, LABEL, labels), "", "o/r", q=explode)
    w = make(labels={("issue", 139): {LABEL}})
    monkeypatch.setattr(board, "Board", explode)
    monkeypatch.delenv("DOKIMA_BOARD", raising=False)
    assert split_main(monkeypatch, w) == 0, "210.5: filing a split failed without a board"
    for n in (201, 202):
        assert w.has("issue", n), f"210.5: without a board, story #{n} under #139 on autopilot was not labeled autopilot"
