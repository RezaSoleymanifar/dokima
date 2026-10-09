"""A parent closes when its last sub-issue closes, on autopilot or not (#367).

Today only a parent on autopilot closes itself, so #330 sat in Work with every sub-issue closed until it was closed by
hand. These tests run the workflows GitHub starts when an issue closes, on the fake GitHub of test_autopilot_close.py,
with no issue on autopilot unless a test says so. `settle` also closes in turn every issue the workflows closed, the
way GitHub tells of a close made by Dokima's app, so a grandparent can close one level up in turn.
"""
import json

from test_autopilot_close import LABEL, Repo


class NotPlannedRepo(Repo):
    """A repo where the issue closed in the test closes as not planned."""

    def close_quietly(self, n):
        """Issue n closes as not planned; its close workflows have not run yet."""
        states = self._json("states.json")
        states[str(n)] = {"state": "closed", "reason": "not_planned"}
        json.dump(states, open(f"{self.tmp}/gh/states.json", "w"))


def closed_not_planned(m, *numbers):
    """Mark issues as already closed as not planned before the test's close."""
    states = m._json("states.json")
    for n in numbers:
        states[str(n)] = {"state": "closed", "reason": "not_planned"}
    json.dump(states, open(f"{m.tmp}/gh/states.json", "w"))
    m.closed_at_start |= {int(n) for n in numbers}


def tree_done_said(m, n, crit, case):
    """The one new comment on issue n, checked to say its tree is done."""
    said = m.new_comments(n)
    assert len(said) == 1, f"{crit} ({case}): #{n} got {len(said)} new comments, expected exactly one saying why it closed: {said}"
    text = said[0].strip()
    assert text and "\n" not in text, f"{crit} ({case}): #{n}'s comment is not one line: {said[0]!r}"
    assert "tree" in text.lower() and "done" in text.lower(), \
        f"{crit} ({case}): #{n}'s comment does not say its tree is done: {said[0]!r}"
    return text


def test_a_parent_off_autopilot_closes_when_its_last_sub_issue_closes(record_property, tmp_path):
    """A parent off autopilot closes as completed when its last open sub-issue closes.

    Proves 367.1. #57 has #101 and #102; nothing is on autopilot. With #102 already closed, closing #101 must close #57 as completed,
    in the run that #101's close starts, with no workflow failing. With #102 still open, closing #101 must leave #57
    open with no new comment."""
    record_property("proves", "367.1")
    m = Repo(tmp_path / "last", {57: [101, 102]}, {}, closed=[102])
    m.close(101)
    assert not m.failed, f"367.1 (last one): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert m.state(57) == ("closed", "completed"), (
        f"367.1 (last one): #57 is {m.state(57)} after its last open sub-issue closed off autopilot, expected closed "
        f"as completed\n{m.tail()}")

    m = Repo(tmp_path / "one-left", {57: [101, 102]}, {})
    m.close(101)
    assert not m.failed, f"367.1 (one left): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert m.state(57)[0] == "open", "367.1 (one left): #57 closed while its sub-issue #102 is still open"
    assert m.new_comments(57) == [], f"367.1 (one left): #57 got comments while #102 is still open: {m.new_comments(57)}"


def test_a_sub_issue_closed_as_not_planned_counts_as_done(record_property, tmp_path):
    """A sub-issue closed as not planned counts as done, so the parent still closes.

    Proves 367.2. #57 has #101 and #102, nothing on autopilot. Case one: #102 was closed as not planned and #101 closes as completed;
    #57 must close as completed. Case two: #102 is closed as completed and #101, the last one, closes as not planned;
    #57 must close as completed. Case three: #102 is still open and #101 closes as not planned; #57 must stay open."""
    record_property("proves", "367.2")
    m = Repo(tmp_path / "sibling", {57: [101, 102]}, {})
    closed_not_planned(m, 102)
    m.close(101)
    assert not m.failed, f"367.2 (sibling not planned): a workflow failed: {m.failures}\n{m.tail()}"
    assert m.state(57) == ("closed", "completed"), (
        f"367.2 (sibling not planned): #57 is {m.state(57)} though #102 was closed as not planned and #101 as "
        f"completed, expected closed as completed\n{m.tail()}")

    m = NotPlannedRepo(tmp_path / "last", {57: [101, 102]}, {}, closed=[102])
    m.close(101)
    assert not m.failed, f"367.2 (last not planned): a workflow failed: {m.failures}\n{m.tail()}"
    assert m.state(101) == ("closed", "not_planned"), "test setup: #101 should be closed as not planned"
    assert m.state(57) == ("closed", "completed"), (
        f"367.2 (last not planned): #57 is {m.state(57)} after its last sub-issue closed as not planned, expected "
        f"closed as completed\n{m.tail()}")

    m = NotPlannedRepo(tmp_path / "one-left", {57: [101, 102]}, {})
    m.close(101)
    assert not m.failed, f"367.2 (one left): a workflow failed: {m.failures}\n{m.tail()}"
    assert m.state(57)[0] == "open", "367.2 (one left): #57 closed while #102 is still open"


def test_a_grandparent_off_autopilot_closes_one_level_up_in_turn(record_property, tmp_path):
    """A grandparent closes in turn when its last child closes with its own tree.

    Proves 367.3. #57 has #101 and #102; #101 has #201 and #202; #201 is closed; nothing is on autopilot. When #202 closes, #101 must
    close as completed and #57 must stay open, because #102 is still open. When #102 closes, #57 must close as
    completed. Case two: #102 is already closed, so closing #202 must close #101 and then #57, each as completed."""
    record_property("proves", "367.3")
    tree = {57: [101, 102], 101: [201, 202]}
    m = Repo(tmp_path / "in-turn", tree, {}, closed=[201])
    m.settle(202)
    assert not m.failed, f"367.3 (in turn): a workflow failed when #202 closed: {m.failures}\n{m.tail()}"
    assert m.state(101) == ("closed", "completed"), \
        f"367.3 (in turn): #101 is {m.state(101)} after its last sub-issue #202 closed, expected closed as completed\n{m.tail()}"
    assert m.state(57)[0] == "open", "367.3 (in turn): #57 closed while its sub-issue #102 is still open"
    m.settle(102)
    assert not m.failed, f"367.3 (in turn): a workflow failed when #102 closed: {m.failures}\n{m.tail()}"
    assert m.state(57) == ("closed", "completed"), \
        f"367.3 (in turn): #57 is {m.state(57)} after both its sub-issues closed, expected closed as completed\n{m.tail()}"

    m = Repo(tmp_path / "chain", tree, {}, closed=[201, 102])
    m.settle(202)
    assert not m.failed, f"367.3 (chain): a workflow failed when #202 closed: {m.failures}\n{m.tail()}"
    assert m.state(101) == ("closed", "completed"), f"367.3 (chain): #101 is {m.state(101)}, expected closed as completed\n{m.tail()}"
    assert m.state(57) == ("closed", "completed"), (
        f"367.3 (chain): #57 is {m.state(57)} after #101, its last open child, closed with its tree, expected closed "
        f"as completed\n{m.tail()}")


def test_the_parent_says_why_it_closed_in_one_line_as_on_autopilot(record_property, tmp_path):
    """The parent gets one one-line comment saying its tree is done, as on autopilot.

    Proves 367.4. #57 has #101 and #102, #102 closed. Off autopilot, closing #101 must leave exactly one new comment on #57: one line
    saying its tree is done, not starting with 'Autopilot:', and no comment starting 'Autopilot:' anywhere. The same
    tree on autopilot must give #57 the very same comment. In a two-level tree off autopilot, #101 and #57 must each
    get exactly one such comment, even though each close is told to the workflows again."""
    record_property("proves", "367.4")
    off = Repo(tmp_path / "off", {57: [101, 102]}, {}, closed=[102])
    off.close(101)
    assert not off.failed, f"367.4 (off): a workflow failed when #101 closed: {off.failures}\n{off.tail()}"
    said_off = tree_done_said(off, 57, "367.4", "off autopilot")
    assert off.any_autopilot_line() == [], \
        f"367.4 (off): a comment starting 'Autopilot:' was posted off autopilot: {off.any_autopilot_line()}"

    on = Repo(tmp_path / "on", {57: [101, 102]}, {57: [LABEL], 101: [LABEL], 102: [LABEL]}, closed=[102])
    on.close(101)
    assert not on.failed, f"367.4 (on): a workflow failed when #101 closed: {on.failures}\n{on.tail()}"
    said_on = tree_done_said(on, 57, "367.4", "on autopilot")
    assert said_off == said_on, \
        f"367.4: the parent's comment off autopilot {said_off!r} differs from the one on autopilot {said_on!r}"

    m = Repo(tmp_path / "levels", {57: [101, 102], 101: [201, 202]}, {}, closed=[201, 102])
    m.settle(202)
    assert not m.failed, f"367.4 (levels): a workflow failed when #202 closed: {m.failures}\n{m.tail()}"
    tree_done_said(m, 101, "367.4", "two levels, #101")
    tree_done_said(m, 57, "367.4", "two levels, #57")


def test_a_parent_already_closed_is_left_alone(record_property, tmp_path):
    """A parent closed before its last sub-issue is never closed again or commented on.

    Proves 367.5. #57 has #101 and #102, nothing on autopilot; #57 was closed by hand as not planned and #102 is closed. Closing #101
    must leave #57 closed as not planned with no new comment and fail no workflow. Beside it, the same tree with #57
    open must close #57, so the run does act on an open parent."""
    record_property("proves", "367.5")
    m = Repo(tmp_path / "already", {57: [101, 102]}, {}, closed=[102])
    closed_not_planned(m, 57)
    m.close(101)
    assert not m.failed, f"367.5 (already closed): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
    assert m.state(57) == ("closed", "not_planned"), \
        f"367.5 (already closed): #57 was closed again: it is now {m.state(57)}, expected closed as not planned"
    assert m.new_comments(57) == [], f"367.5 (already closed): #57 got comments: {m.new_comments(57)}"

    m = Repo(tmp_path / "open", {57: [101, 102]}, {}, closed=[102])
    m.close(101)
    assert m.state(57) == ("closed", "completed"), \
        f"367.5 (open parent): #57 is {m.state(57)} after its last sub-issue closed, expected closed as completed\n{m.tail()}"
