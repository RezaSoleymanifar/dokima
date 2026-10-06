import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import board  # noqa: E402

WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "board.yml")
BOT, YOU = {"type": "Bot"}, {"type": "User"}


def pr(action, number=7, body="Closes #5", merged=False):
    return {"action": action, "pull_request": {"number": number, "body": body, "merged": merged}}


# 116.1: every stage moment sets the stage and whose turn it is

def test_issue_stage_moments(record_property):
    record_property("proves", "116.1")
    issue = {"number": 5}
    assert board.decide("issues", {"action": "labeled", "label": {"name": "plan"}, "issue": issue}) == [("issue", 5, "Plan", False)]
    assert board.decide("issues", {"action": "labeled", "label": {"name": "work"}, "issue": issue}) == [("issue", 5, "Work", False)]
    assert board.decide("issues", {"action": "closed", "issue": issue}) == [("issue", 5, "Done", False)]
    assert board.decide("issues", {"action": "labeled", "label": {"name": "bug"}, "issue": issue}) == []


def test_plan_ready_question_or_rejection_is_your_turn(record_property):
    record_property("proves", "116.1")
    for body in ("Plan written above, tests on `work/issue-5`.", "**Planner question**\n\nWhich?", "**Plan rejected:** no tests"):
        assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": body}}) == [("issue", 5, "Plan", True)]
    assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": YOU, "body": "Plan written above"}}) == [], "116.1: a person's comment moved the board"


def test_pr_moments(record_property):
    record_property("proves", "116.1")
    assert board.decide("pull_request", pr("opened")) == [("pr", 7, "Review", False), ("issue", 5, "Review", False)]
    run = {"action": "completed", "workflow_run": {"pull_requests": [{"number": 7}]}}
    assert board.decide("workflow_run", run) == [("pr", 7, "Review", True)]
    review = {"action": "submitted", "review": {"state": "changes_requested"}, "pull_request": {"number": 7, "body": "Closes #5"}}
    assert board.decide("pull_request_review", review) == [("pr", 7, "Work", False), ("issue", 5, "Work", False)]
    assert board.decide("pull_request", pr("closed", merged=True)) == [("pr", 7, "Done", False), ("issue", 5, "Done", False)]
    assert board.decide("pull_request", pr("closed", merged=False)) == [("pr", 7, "Done", False)], "116.1: an unmerged close finished the issue"


# 116.2: PR and issue move together; new items land on top

class FakeGitHub:
    def __init__(self, on_board=False):
        self.calls, self.on_board = [], on_board

    def __call__(self, query, **v):
        self.calls.append((query.split("(")[0].split("{")[0].strip(), v))
        if "organization" in query:
            return {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
                {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Plan", "Work", "Review", "Done")]},
                {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": "Needs you"}]}]}}}}
        if query.startswith("query") and "repository" in query:
            kind = "issue" if "issue(" in query else "pullRequest"
            items = [{"id": "ITEM", "project": {"id": "P"}}] if self.on_board else []
            return {"repository": {kind: {"id": "C", "projectItems": {"nodes": items}}}}
        if "addProjectV2ItemById" in query:
            return {"addProjectV2ItemById": {"item": {"id": "NEW"}}}
        return {}


def test_pr_and_issue_move_together(record_property):
    record_property("proves", "116.2")
    gh = FakeGitHub(on_board=True)
    changed = board.sync("pull_request", pr("opened"), "dokima-dev/1", "dokima-dev/dokima", q=gh)
    assert [(k, n) for k, n, *_ in changed] == [("pr", 7), ("issue", 5)]
    sets = [v for name, v in gh.calls if name == "mutation" and "o" in v]
    assert {s["o"] for s in sets} == {"s-Review"}, f"116.2: got {sets}"
    clears = [v for name, v in gh.calls if name == "mutation" and v.get("f") == "W" and "o" not in v]
    assert len(clears) == 2, "116.2: Action was not cleared on both items while Dokima works"


def test_new_item_is_added_at_the_top(record_property):
    record_property("proves", "116.2")
    gh = FakeGitHub(on_board=False)
    board.sync("issues", {"action": "labeled", "label": {"name": "work"}, "issue": {"number": 5}}, "dokima-dev/1", "dokima-dev/dokima", q=gh)
    positions = [v for _, v in gh.calls if v.get("i") == "NEW" and set(v) == {"p", "i"}]
    assert positions, "116.2: new item was not placed"
    assert all("a" not in v for v in positions), "116.2: new item was placed after another item, not on top"


# 116.3: without a board, nothing happens and nothing fails

def test_no_board_means_no_calls(record_property):
    record_property("proves", "116.3")
    def explode(*a, **k):
        raise AssertionError("116.3: GitHub was called without a board")
    assert board.sync("issues", {"action": "closed", "issue": {"number": 5}}, "", "o/r", q=explode) == []


def test_workflow_skips_without_the_board_setting(record_property):
    record_property("proves", "116.3")
    assert "if: vars.DOKIMA_BOARD != ''" in open(WORKFLOW).read()


def test_lanes_are_needs_you_or_nothing(record_property):
    """Items that need the owner get Action = "Needs you"; everything else has no Action."""
    record_property("proves", "130.1")
    gh = FakeGitHub(on_board=True)
    board.sync("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": "**Planner question**"}}, "dokima-dev/1", "o/r", q=gh)
    assert any(v.get("o") == "w-you" for _, v in gh.calls), "130.1: a question for the owner did not land in Needs you"


# 135: the refresh button puts every card back where it belongs

def issue(state="OPEN", labels=(), prs=()):
    return {"__typename": "Issue", "number": 1, "state": state,
            "labels": {"nodes": [{"name": n} for n in labels]},
            "closedByPullRequestsReferences": {"nodes": [{"state": s} for s in prs]}}


def test_place_from_real_state():
    """Each item's column comes from its real state; closed items drop the flag."""
    assert board.place(issue("CLOSED", ["work"])) == ("Done", True), "135.1"
    assert board.place({"__typename": "PullRequest", "state": "MERGED"}) == ("Done", True), "135.2"
    assert board.place({"__typename": "PullRequest", "state": "OPEN"}) == ("Review", False), "135.1"
    assert board.place(issue(labels=["work"], prs=["OPEN"])) == ("Review", False), "135.1"
    assert board.place(issue(labels=["work"], prs=["CLOSED"])) == ("Work", False), "135.1"
    assert board.place(issue(labels=["plan"])) == ("Plan", False), "135.1"
    assert board.place(issue()) == ("Backlog", False), "135.1"
