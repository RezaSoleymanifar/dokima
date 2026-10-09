"""Needs you shows only while the river waits on the owner; Autopilot otherwise (#297).

Before this, the board put Needs you where nothing waited on the owner: every time the done-whens checks finished on a
pull request (even one already merged), on closed issues a run stopped on after the owner had merged, and on parent
issues left with the pill from before their split was filed. A Needs you the river did set was wiped by the next new
commit, yet stayed for the whole run after the owner answered with a command. Nothing ever cleared old wrong pills.

Most tests fake dokima.board.Board and agent's `gh` against one in-memory world, so they read the board's end state:
each card's Status and Action ("Needs you", "Autopilot" or none), each item's labels and whether it is closed, each
issue's open pull request, sub-issues and Dokima records (the bot's record comments, read through `gh issue view`).
On top of test_autopilot_board's fake Board, the board offers two more reads the code is expected to use:

    .state(kind, n) -> "open" | "closed"    a merged pull request is closed; raises subprocess.CalledProcessError
                                             when GitHub cannot say
    .needs_you_items() -> [(kind, n), ...]  every issue and pull request on the board whose Action is Needs you

Whether an item is closed may also be read through `gh` (`gh api repos/o/r/issues/N`, `gh issue view N --json state`,
`gh pr view N --json state`); the fake answers all of them alike, and fails alike for an item GitHub cannot read.
Code owners are the people CODEOWNERS names (dokima.plan.repo_approvers). The last two tests run the real Board's new
reads against a faked GitHub.
"""
import json
import os
import re
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import test_autopilot_board as tab  # noqa: E402
from dokima import agent, board, card, plan  # noqa: E402
from test_agent import GOOD_REVIEW, SPLIT, rec  # noqa: E402

LABEL = "autopilot"
SPEC, REPO = "o/1", "o/r"
OWNER = sorted(plan.repo_approvers("o"))[0]
NEEDS, AUTO = "Needs you", "Autopilot"


def split_filed(stories=(201, 202)):
    """The Split filed record code posts on a parent once its stories are filed."""
    return {"role": "split", "stage": None, "check": {"passed": True, "problems": []},
            "handback": {"stories": [{"story": i, "issue": n, "title": f"Story {i}", "id": f"I_{n}", "blocked_by": []}
                                     for i, n in enumerate(stories, 1)]}}


def split_planned():
    """A parent's records up to an approved split not filed yet, waiting for `/work`."""
    return [rec("planner", handback=SPLIT), rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})]


class World(tab.World):
    """test_autopilot_board's world, plus which items are closed, which GitHub cannot read, sub-issues and records."""

    def __init__(self, closed=(), unreadable=(), subs=None, records=None, **kw):
        super().__init__(**kw)
        self.closed = set(closed)  # (kind, n)
        self.unreadable = set(unreadable)  # numbers whose state GitHub will not give
        self.subs = {k: list(v) for k, v in (subs or {}).items()}
        self.records = {k: list(v) for k, v in (records or {}).items()}

    def is_closed(self, n):
        return ("issue", n) in self.closed or ("pr", n) in self.closed

    def refuse(self, n, args):
        if n in self.unreadable:
            raise subprocess.CalledProcessError(1, ["gh", *args], output="", stderr="HTTP 502: Bad Gateway")


def fake_board(world):
    """test_autopilot_board's fake Board, reading this world, with the two new reads."""
    base = tab.fake_board(world)

    class FakeBoard(base):
        def state(self, kind, n):
            world.refuse(int(n), ["api", f"state {kind} {n}"])
            return "closed" if (kind, int(n)) in world.closed else "open"

        def needs_you_items(self):
            return sorted(k for k, c in world.cards.items() if c.get("Action") == NEEDS)

        def view_nodes(self):
            return []

        def set_view_filter(self, view_id, filter):
            pass

    return FakeBoard


def fake_gh(world):
    """agent.gh, answering from the world: pull requests, states, labels, sub-issues and records."""

    def gh(*args):
        world.calls.append(args)
        a = [str(x) for x in args]
        if a[:2] == ["pr", "list"]:
            head = a[a.index("--head") + 1]
            n = int(head.rsplit("-", 1)[1])
            pr = world.prs.get(n) if head.startswith("try/") else None
            want_open = "--state" not in a or a[a.index("--state") + 1] == "open"
            found = [pr] if pr and (not want_open or ("pr", pr) not in world.closed) else []
            if "-q" in a or "--jq" in a:
                return f"{found[0]}\n" if found else "\n"
            return json.dumps([{"number": p} for p in found])
        if a[:2] == ["issue", "view"]:
            n = int(a[2])
            world.refuse(n, a)
            items = card.as_items(world.records.get(n, []))
            comments = [{**c, "createdAt": f"2026-10-09T00:00:{i:02d}Z"} for i, c in enumerate(items)]
            return json.dumps({"number": n, "title": f"Issue {n}", "body": "", "comments": comments,
                               "state": "CLOSED" if ("issue", n) in world.closed else "OPEN",
                               "labels": [{"name": x} for x in sorted(world.labels.get(("issue", n), set()))]})
        if a[:2] == ["pr", "view"]:
            n = int(a[2])
            world.refuse(n, a)
            return json.dumps({"number": n, "state": "CLOSED" if ("pr", n) in world.closed else "OPEN",
                               "comments": [], "reviews": [],
                               "labels": [{"name": x} for x in sorted(world.labels.get(("pr", n), set()))]})
        if a[:1] == ["api"]:
            path = next((x for x in a[1:] if x.lstrip("/").startswith("repos/")), "").lstrip("/")
            method = a[a.index("-X") + 1].upper() if "-X" in a else ("POST" if any(x in ("-f", "-F") for x in a) else "GET")
            m = re.fullmatch(r"repos/o/r/(?:issues|pulls)/(\d+)(/.*)?", path.split("?")[0])
            if m:
                n, rest = int(m.group(1)), m.group(2) or ""
                kind = "pr" if ("pr", n) in world.cards or n in world.prs.values() else "issue"
                if rest == "/sub_issues":
                    return json.dumps([{"number": c, "state": "closed" if world.is_closed(c) else "open"}
                                       for c in world.subs.get(n, [])])
                if rest.startswith("/labels"):
                    if method == "DELETE":
                        world.put(kind, n, False)
                    elif LABEL in " ".join(a):
                        world.put(kind, n, True)
                    return "[]"
                if rest == "/comments":
                    return "[]"
                if rest == "" and method == "GET":
                    world.refuse(n, a)
                    return json.dumps({"id": 9000 + n, "number": n, "state": "closed" if world.is_closed(n) else "open",
                                       "merged": ("pr", n) in world.closed,
                                       "labels": [{"name": x} for x in sorted(world.labels.get((kind, n), set()))]})
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


def comment(n, body, login=OWNER, kind="User", pr_body=None, labels=(), state="open"):
    """An issue_comment payload on issue n, or on pull request n when pr_body is given."""
    issue = {"number": n, "labels": [{"name": x} for x in labels], "state": state, "body": pr_body or ""}
    if pr_body is not None:
        issue["pull_request"] = {"url": f"https://api.github.com/repos/o/r/pulls/{n}"}
    return {"action": "created", "issue": issue, "comment": {"user": {"login": login, "type": kind}, "body": body}}


def pr_event(action, number, issue, merged=False):
    return {"action": action, "pull_request": {"number": number, "body": f"Closes #{issue}", "merged": merged,
                                               "head": {"ref": f"try/issue-{issue}"}, "labels": []}}


def checks_done(*prs):
    """The done-whens checks finished on these pull requests."""
    return {"action": "completed", "workflow_run": {"pull_requests": [{"number": n} for n in prs]}}


def pills(w, *items):
    return {f"{k} #{n}": w.action(k, n) for k, n in items}


# 297.1: Needs you appears only where the river stops for the owner, and stays until it is answered

def test_a_check_finishing_never_marks_a_pull_request_for_the_owner(record_property, make):
    """Finished checks never put Needs you on a pull request.

    Proves 297.1. The done-whens checks finish on PR #60 (on autopilot, showing Autopilot), PR #61 (not on autopilot, no pill) and
    PR #62 (the river stopped on it for the owner, showing Needs you). Afterwards #60 still shows Autopilot, #61 still
    shows nothing and #62 still shows Needs you. Today a finished check puts Needs you on all three."""
    record_property("proves", "297.1")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}}, prs={57: 60, 58: 61, 59: 62},
             cards={("pr", 60): {"Status": "Review", "Action": AUTO}, ("pr", 61): {"Status": "Review"},
                    ("pr", 62): {"Status": "Review", "Action": NEEDS}})
    board.sync("workflow_run", checks_done(60, 61, 62), SPEC, REPO)
    got = pills(w, ("pr", 60), ("pr", 61), ("pr", 62))
    assert got == {"pr #60": AUTO, "pr #61": None, "pr #62": NEEDS}, \
        f"297.1: after the checks finished, the pull requests show {got}; a finished check must not mark one for the owner"


def test_needs_you_set_by_the_river_stays_through_new_commits_and_checks(record_property, make):
    """A Needs you the river set stays through new commits and finished checks.

    Proves 297.1. The good case first: the river stops for the owner on #59 (as `agent board` does after a run), so #59 and its open
    PR #62 show Needs you. Then a new commit reaches PR #62 (as when main is merged into it) and its checks finish: both
    cards must still show Needs you, because nothing answered it. Beside it, PR #60 on autopilot gets a new commit and
    keeps Autopilot, so a card never ends with neither. Today the new commit wipes Needs you off #59 and #62."""
    record_property("proves", "297.1")
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}}, prs={57: 60, 59: 62},
             cards={("pr", 60): {"Status": "Review", "Action": AUTO}, ("issue", 57): {"Status": "Review", "Action": AUTO}})
    agent.move_card(REPO, "59", "Review", True, SPEC)
    got = pills(w, ("issue", 59), ("pr", 62))
    assert got == {"issue #59": NEEDS, "pr #62": NEEDS}, f"297.1: the river stopped for the owner on #59 but the cards show {got}"
    board.sync("pull_request_target", pr_event("synchronize", 62, 59), SPEC, REPO)
    got = pills(w, ("issue", 59), ("pr", 62))
    assert got == {"issue #59": NEEDS, "pr #62": NEEDS}, \
        f"297.1: a new commit on PR #62 took Needs you away though the owner answered nothing: {got}"
    board.sync("workflow_run", checks_done(62), SPEC, REPO)
    assert w.action("pr", 62) == NEEDS, f"297.1: finished checks took Needs you off PR #62: {w.action('pr', 62)!r}"
    board.sync("pull_request_target", pr_event("synchronize", 60, 57), SPEC, REPO)
    got = pills(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": AUTO, "pr #60": AUTO}, f"297.1: a new commit on PR #60, on autopilot, left {got}, not Autopilot"


# 297.2: Needs you clears the moment a code owner answers with a command

def test_a_code_owners_command_clears_needs_you_at_once_and_nothing_else_does(record_property, make):
    """A code owner's command clears Needs you at once; no other comment does.

    Proves 297.2. #57 (on autopilot, with PR #60), #58 (with PR #61) and #59 (no PR) all show Needs you. First, comments that answer
    nothing: someone who is not a code owner says /work on #57, the bot says /work on #57, and the code owner writes a
    plain comment with no command on #57; all five cards still show Needs you. Then the code owner says /work on #57:
    #57 and PR #60 show Autopilot. The code owner says /review on PR #61 (whose description closes #58): #61 and #58
    show nothing. The code owner says /plan with an answer on #59: #59 shows nothing. Today none of these comments
    changes a pill."""
    record_property("proves", "297.2")
    every = (("issue", 57), ("pr", 60), ("issue", 58), ("pr", 61), ("issue", 59))
    w = make(labels={("issue", 57): {LABEL}, ("pr", 60): {LABEL}}, prs={57: 60, 58: 61},
             cards={k: {"Status": "Review", "Action": NEEDS} for k in every})
    stranger = "someone-else" if OWNER != "someone-else" else "another-person"
    for body, login, kind in (("/work", stranger, "User"), ("/work", "dokima-runtime[bot]", "Bot"),
                              ("Thanks, that reads right.", OWNER, "User")):
        board.sync("issue_comment", comment(57, body, login, kind, labels=[LABEL]), SPEC, REPO)
        got = pills(w, *every)
        assert set(got.values()) == {NEEDS}, \
            f"297.2: {login}'s comment {body!r} on #57 answered nothing, yet the pills changed to {got}"
    board.sync("issue_comment", comment(57, "/work", labels=[LABEL]), SPEC, REPO)
    got = pills(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": AUTO, "pr #60": AUTO}, \
        f"297.2: the code owner said /work on #57, on autopilot, and the cards show {got}, not Autopilot"
    board.sync("issue_comment", comment(61, "/review", pr_body="Closes #58"), SPEC, REPO)
    got = pills(w, ("pr", 61), ("issue", 58))
    assert got == {"pr #61": None, "issue #58": None}, f"297.2: the code owner said /review on PR #61 and the cards show {got}"
    board.sync("issue_comment", comment(59, "/plan Yes, keep the old name."), SPEC, REPO)
    assert w.action("issue", 59) is None, f"297.2: the code owner answered with /plan on #59 and it shows {w.action('issue', 59)!r}"


# 297.3: Needs you clears when the item closes and never lands on a closed item

def test_needs_you_never_lands_on_a_closed_issue_or_pull_request(record_property, make):
    """Closing clears Needs you, and nothing puts it on a closed item.

    Proves 297.3. Closing: #57 (on autopilot) closes and shows Autopilot; merged PR #60 and its #56 lose Needs you. Then the river
    stops on #57 after it closed (a run that ended after the owner merged) and #57 must keep Autopilot; it stops on
    closed #58, not on autopilot, and #58 must show nothing; and a bot comment saying a plan is ready lands on closed
    #58 and must not mark it. Beside them, the river stops on open #59 and #59 and its PR #62 show Needs you, and on
    #63, whose state GitHub cannot give, which shows Needs you so nothing waiting is hidden. Today the river and the
    bot comment put Needs you on the closed issues."""
    record_property("proves", "297.3")
    w = make(labels={("issue", 57): {LABEL}}, prs={56: 60, 59: 62}, unreadable={63},
             cards={("issue", 57): {"Status": "Review", "Action": NEEDS}, ("issue", 56): {"Status": "Review", "Action": NEEDS},
                    ("pr", 60): {"Status": "Review", "Action": NEEDS}, ("issue", 58): {"Status": "Done"}})
    w.closed |= {("issue", 57)}
    board.sync("issues", {"action": "closed", "issue": {"number": 57, "labels": [{"name": LABEL}], "state": "closed"}}, SPEC, REPO)
    assert w.action("issue", 57) == AUTO, f"297.3: #57, on autopilot, closed and shows {w.action('issue', 57)!r}, not Autopilot"
    w.closed |= {("pr", 60), ("issue", 56)}
    board.sync("pull_request_target", pr_event("closed", 60, 56, merged=True), SPEC, REPO)
    got = pills(w, ("pr", 60), ("issue", 56))
    assert got == {"pr #60": None, "issue #56": None}, f"297.3: PR #60 merged and the cards still show {got}"
    w.closed |= {("issue", 58)}
    agent.move_card(REPO, "57", "Review", True, SPEC)
    assert w.action("issue", 57) == AUTO, f"297.3: the river stopped on closed #57 and it shows {w.action('issue', 57)!r}, not Autopilot"
    agent.move_card(REPO, "58", "Review", True, SPEC)
    assert w.action("issue", 58) is None, f"297.3: the river stopped on closed #58 and it shows {w.action('issue', 58)!r}"
    board.sync("issue_comment", comment(58, "Plan written above, tests on `work/issue-58`.", "dokima-runtime[bot]", "Bot",
                                        state="closed"), SPEC, REPO)
    assert w.action("issue", 58) is None, f"297.3: a bot comment marked closed #58 with {w.action('issue', 58)!r}"
    agent.move_card(REPO, "59", "Review", True, SPEC)
    got = pills(w, ("issue", 59), ("pr", 62))
    assert got == {"issue #59": NEEDS, "pr #62": NEEDS}, f"297.3: the river stopped on open #59 and the cards show {got}"
    agent.move_card(REPO, "63", "Plan", True, SPEC)
    assert w.action("issue", 63) == NEEDS, \
        f"297.3: GitHub could not say whether #63 is closed and it shows {w.action('issue', 63)!r}; it must show Needs you"


# 297.4: a parent shows Needs you only when the parent itself waits on the owner

def test_a_parent_shows_needs_you_only_for_its_own_stop(record_property, make):
    """A parent shows Needs you only when its own split waits for /work.

    Proves 297.4. #139 (on autopilot) has its split filed into #201 and #202. #201's river stops for the owner and #202's pull
    request merges: #201 shows Needs you, #139 keeps Autopilot. #141's approved split is not filed yet, so its river
    stops for /work: #141 shows Needs you, and keeps it through another merge. Then a board left with old pills: #139
    (on autopilot) and #140 (not), both with filed splits, show Needs you; after the next merge #139 shows Autopilot,
    #140 nothing, and #141, still waiting for /work, keeps Needs you. Today the old pills on #139 and #140 stay."""
    record_property("proves", "297.4")
    parents = dict(labels={("issue", 139): {LABEL}, ("issue", 201): {LABEL}, ("issue", 141): {LABEL}},
                   subs={139: [201, 202], 140: [203]}, parents={201: 139, 202: 139, 203: 140}, prs={202: 210},
                   records={139: split_planned() + [split_filed((201, 202))], 140: split_planned() + [split_filed((203,))],
                            141: split_planned()})
    w = make(cards={("issue", 139): {"Status": "Work", "Action": AUTO}, ("issue", 201): {"Status": "Plan", "Action": AUTO},
                    ("issue", 141): {"Status": "Plan", "Action": AUTO}}, **parents)
    agent.move_card(REPO, "201", "Plan", True, SPEC)
    w.closed |= {("pr", 210), ("issue", 202)}
    board.sync("pull_request_target", pr_event("closed", 210, 202, merged=True), SPEC, REPO)
    got = pills(w, ("issue", 201), ("issue", 139))
    assert got == {"issue #201": NEEDS, "issue #139": AUTO}, f"297.4: a story stopped and another merged, and the cards show {got}"
    agent.move_card(REPO, "141", "Plan", True, SPEC)
    board.sync("pull_request_target", pr_event("closed", 211, 300, merged=True), SPEC, REPO)
    assert w.action("issue", 141) == NEEDS, \
        f"297.4: #141's own split waits for /work, yet it shows {w.action('issue', 141)!r}, not Needs you"
    w = make(cards={("issue", 139): {"Status": "Work", "Action": NEEDS}, ("issue", 140): {"Status": "Work", "Action": NEEDS},
                    ("issue", 141): {"Status": "Plan", "Action": NEEDS}}, closed={("pr", 70), ("issue", 71)}, **parents)
    board.sync("pull_request_target", pr_event("closed", 70, 71, merged=True), SPEC, REPO)
    got = pills(w, ("issue", 139), ("issue", 140), ("issue", 141))
    assert got == {"issue #139": AUTO, "issue #140": None, "issue #141": NEEDS}, \
        f"297.4: after a merge, parents with their stories in progress or waiting for /work show {got}"


# 297.5: the wrong pills already on the board are cleared

def test_a_merge_clears_the_wrong_pills_already_on_the_board(record_property, make):
    """Every merge clears old Needs you pills on closed items and keeps open ones.

    Proves 297.5. The board has old pills: closed #57 (on autopilot), closed #58, merged PR #64 (on autopilot) and closed PR #61 all
    show Needs you, and so do open #59 and its open PR #62, which wait on the owner. PR #70 (closing #71) merges.
    Afterwards #57 and #64 show Autopilot, #58 and #61 show nothing, and #59 and #62 still show Needs you. Today the
    old pills stay."""
    record_property("proves", "297.5")
    old = (("issue", 57), ("issue", 58), ("pr", 64), ("pr", 61), ("issue", 59), ("pr", 62))
    w = make(labels={("issue", 57): {LABEL}, ("pr", 64): {LABEL}}, prs={59: 62},
             closed={("issue", 57), ("issue", 58), ("pr", 64), ("pr", 61), ("pr", 70), ("issue", 71)},
             records={59: [rec("planner", handback={"kind": "user_story"}),
                           rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})]},
             cards={k: {"Status": "Review", "Action": NEEDS} for k in old})
    board.sync("pull_request_target", pr_event("closed", 70, 71, merged=True), SPEC, REPO)
    got = pills(w, *old)
    want = {"issue #57": AUTO, "issue #58": None, "pr #64": AUTO, "pr #61": None, "issue #59": NEEDS, "pr #62": NEEDS}
    assert got == want, f"297.5: after the merge the old pills read {got}, not {want}"


# The real dokima.board.Board's two new reads, against a faked GitHub

class GitHub:
    """GitHub as the real Board reads it: a two-page project, issues and pull requests.

    Every query about the organization's project answers its id, its Status and Action fields and, page by page, its
    items: each with its id, type, content (number, state, __typename), its Action value both as fieldValueByName and in
    fieldValues. The second page is answered when any variable or the query text carries the first page's endCursor.
    Every query about the repository answers the issue or pull request asked for, with its state; the REST reads of
    repos/dokima-dev/dokima/issues/N and pulls/N answer the same."""

    STATES = {("issue", 57): "CLOSED", ("issue", 58): "OPEN", ("issue", 59): "OPEN",
              ("pr", 60): "MERGED", ("pr", 61): "CLOSED", ("pr", 62): "OPEN"}

    def __init__(self):
        self.pages = [[("issue", 57, NEEDS), ("issue", 58, AUTO), ("pr", 61, None), ("draft", None, NEEDS)],
                      [("pr", 60, NEEDS), ("issue", 59, NEEDS)]]

    def node(self, kind, n, action):
        content = {"__typename": "DraftIssue", "title": "An idea"} if kind == "draft" else \
            {"__typename": "Issue" if kind == "issue" else "PullRequest", "number": n, "state": self.STATES[(kind, n)],
             "closed": self.STATES[(kind, n)] != "OPEN", "merged": self.STATES[(kind, n)] == "MERGED"}
        values = [{"name": "Review", "field": {"name": "Status"}}] + ([{"name": action, "field": {"name": "Action"}}] if action else [])
        return {"id": f"ITEM_{kind}_{n}", "type": {"issue": "ISSUE", "pr": "PULL_REQUEST", "draft": "DRAFT_ISSUE"}[kind],
                "content": content, "fieldValueByName": {"name": action} if action else None, "fieldValues": {"nodes": values}}

    def q(self, query, **v):
        text = " ".join(query.split())
        if "organization" in text:
            second = any(str(x) == "c1" for x in v.values()) or '"c1"' in text
            page = self.pages[1 if second else 0]
            return {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
                {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Backlog", "Plan", "Work", "Review", "Done")]},
                {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": NEEDS}, {"id": "w-auto", "name": AUTO}]}]},
                "items": {"totalCount": 6, "pageInfo": {"hasNextPage": not second, "endCursor": None if second else "c1"},
                          "nodes": [self.node(*x) for x in page]},
                "views": {"nodes": []}}}}
        if "repository" in text:
            n = next((x for x in v.values() if isinstance(x, int)), None)
            if n is None:
                n = int(re.search(r"(?:issue|pullRequest)\s*\(\s*number:\s*(\d+)", text).group(1))
            out = {}
            for field, kind in (("issue", "issue"), ("pullRequest", "pr")):
                if re.search(field + r"\s*\(", text):
                    st = self.STATES[(kind, n)]
                    out[field] = {"id": f"N_{n}", "number": n, "state": st, "closed": st != "OPEN", "merged": st == "MERGED",
                                  "labels": {"nodes": []}, "projectItems": {"nodes": []}}
            return {"repository": out}
        return {}

    def rest(self, method, path, **fields):
        m = re.fullmatch(r"repos/dokima-dev/dokima/(issues|pulls)/(\d+)", path.lstrip("/"))
        if m and method.upper() == "GET":
            n = int(m.group(2))
            st = self.STATES.get(("issue", n)) or self.STATES.get(("pr", n))
            return {"number": n, "state": "open" if st == "OPEN" else "closed", "merged": st == "MERGED"}
        return {}


def real(gh):
    return board.Board("dokima-dev/1", "dokima-dev/dokima", q=gh.q, rest=gh.rest)


def test_the_real_board_lists_every_card_showing_needs_you(record_property):
    """The board lists every issue and pull request showing Needs you, across pages.

    Proves 297.5. The real Board reads a project of two pages: closed #57 shows Needs you, #58 Autopilot, PR #61 nothing and a draft
    item Needs you on the first; merged PR #60 and open #59 show Needs you on the second. It must list exactly #57,
    #59 and PR #60, skipping the draft, which is no issue or pull request."""
    record_property("proves", "297.5")
    if not callable(getattr(board.Board, "needs_you_items", None)):
        pytest.fail("297.5: the real Board cannot list the cards showing Needs you yet (it has no needs_you_items)")
    got = sorted(real(GitHub()).needs_you_items())
    assert got == [("issue", 57), ("issue", 59), ("pr", 60)], \
        f"297.5: the board listed {got} as showing Needs you, not issue #57, issue #59 and PR #60 from both pages"


def test_the_real_board_tells_a_closed_item_from_an_open_one(record_property):
    """The board reads whether an issue or pull request is closed; merged counts as closed.

    Proves 297.3. The real Board reads closed #57, open #58, merged PR #60, closed PR #61 and open PR #62."""
    record_property("proves", "297.3")
    if not callable(getattr(board.Board, "state", None)):
        pytest.fail("297.3: the real Board cannot read whether an issue or pull request is closed yet (it has no state)")
    b = real(GitHub())
    got = {f"{k} #{n}": b.state(k, n) for k, n in (("issue", 57), ("issue", 58), ("pr", 60), ("pr", 61), ("pr", 62))}
    want = {"issue #57": "closed", "issue #58": "open", "pr #60": "closed", "pr #61": "closed", "pr #62": "open"}
    assert got == want, f"297.3: the board read the states as {got}, not {want}"
