"""The 15-minute card sweep closes every open parent whose sub-issues are all closed (#367).

A parent closes when its last sub-issue closes, but a close event GitHub drops or a run that never went would leave a
finished parent sitting in Work, as #330 did. The owner asked that the 15-minute card sweep from #347 doubles as the
safety net: on each sweep, any open parent whose sub-issues are all closed is closed the same way.

These tests play card.yml's 15-minute schedule with the player of tests/card_player.py, running the real
`python3 dokima/card.py` against the fake GitHub of tests/test_card_sweep.py, extended here with issue trees:
- `gh api repos/o/r/issues/N/sub_issues` lists N's sub-issues (each with its state and state_reason), and
  `gh api repos/o/r/issues/N/parent` gives N's parent (404 when it has none).
- Every issue GitHub gives carries `state_reason`, `parent_issue_url` and `sub_issues_summary` (total, and completed:
  the sub-issues closed as completed; one closed as not planned is not counted there, so code that trusts that count
  alone misses it).
- `gh issue close N` (--reason/-r, --comment/-c) closes N, and `gh api repos/o/r/issues/N` with -X PATCH and
  state=closed (state_reason=...) does too.
Every tree's closes happened at 01:00, before the last sweep that succeeded (05:00), and nothing was updated since: the
missed close is old, as #330's was, so the sweep must look at every open parent, not only the ones updated lately.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_player import must_redraw, schedule  # noqa: E402
from dokima import agent  # noqa: E402
from test_card_sweep import DEFS_AT, CALL_AT, SweepHub  # noqa: E402

TREE_DEFS = r'''
def tree_parent(n):
    return next((int(p) for p, cs in S.get("tree", {}).items() if int(n) in cs), None)


_plain_issue_rest = issue_rest


def issue_rest(n):
    i = _plain_issue_rest(n)
    if str(n) in S["prs"]:
        return i
    kids = S.get("tree", {}).get(str(n), [])
    p = tree_parent(n)
    i["state_reason"] = S["issues"][str(n)].get("state_reason")
    i["parent_issue_url"] = f"https://api.github.com/repos/{REPO}/issues/{p}" if p else None
    i["sub_issues_summary"] = {
        "total": len(kids),
        "completed": sum(1 for c in kids if S["issues"][str(c)]["state"] == "closed"
                         and S["issues"][str(c)].get("state_reason") == "completed"),
        "percent_completed": 0}
    return i


_plain_issue_gh = issue_gh


def issue_gh(n):
    i = _plain_issue_gh(n)
    reason = S["issues"][str(n)].get("state_reason")
    i["stateReason"] = (reason or "").upper()
    return i


def close_issue(n, reason, comment=None):
    i = issue(n)
    reason = (reason or "completed").lower().replace(" ", "_")
    if reason not in ("completed", "not_planned"):
        fail(f"fake gh: no such close reason {reason!r}")
    i["state"], i["state_reason"] = "closed", reason
    i["closed_at"] = i["updated_at"] = tick()
    write("close", n)
    if comment:
        i.setdefault("comments", []).append({"login": BOT_LOGIN, "body": comment, "at": tick()})
        write("comment", n)
    save()


def tree_calls(route, params, method, f):
    """Sub-issues, parents and closes over REST, as GitHub answers them."""
    r = route[len(f"repos/{REPO}/"):] if route.startswith(f"repos/{REPO}/") else None
    if r is None:
        return
    m = re.fullmatch(r"issues/(\d+)/sub_issues", r)
    if m and method == "GET":
        refuse("read-issue", int(m.group(1)))
        issue(int(m.group(1)))
        out([issue_rest(c) for c in S.get("tree", {}).get(m.group(1), [])])
        sys.exit(0)
    m = re.fullmatch(r"issues/(\d+)/parent", r)
    if m and method == "GET":
        p = tree_parent(int(m.group(1)))
        if p is None:
            fail(f"HTTP 404: Not Found (https://api.github.com/{route})")
        out(issue_rest(p))
        sys.exit(0)
    m = re.fullmatch(r"issues/(\d+)", r)
    if m and method in ("PATCH", "POST") and f.get("state") == "closed":
        close_issue(int(m.group(1)), f.get("state_reason"))
        out(issue_rest(int(m.group(1))))
        sys.exit(0)


if a[:2] == ["issue", "close"]:
    close_issue(number(positional()[1]), flag("--reason", "-r"), flag("--comment", "-c"))
    sys.exit(0)
'''


class TreeHub(SweepHub):
    """The sweep's fake GitHub, plus issue trees, closes and each issue's close reason."""

    def __init__(self, tmp):
        super().__init__(tmp)
        gh = os.path.join(self.dir, "bin", "gh")
        text = open(gh).read()
        assert text.count(DEFS_AT) == 1 and text.count(CALL_AT) == 1, \
            "test setup: the fake GitHub of tests/test_card_sweep.py changed shape"
        text = text.replace(DEFS_AT, TREE_DEFS + DEFS_AT).replace(
            CALL_AT, CALL_AT + "    tree_calls(route, params, method, f)\n")
        open(gh, "w").write(text)
        self.last_sweep("2026-10-09T05:00:00Z")

    def tree(self, tree, closed=(), not_planned=()):
        """Add the tree's issues, open, then close the listed ones before the last sweep."""
        for n in sorted({int(p) for p in tree} | {c for cs in tree.values() for c in cs}):
            self.add_issue(n, records=False)
        self.save()
        s = self.load()
        s.setdefault("tree", {}).update({str(p): list(cs) for p, cs in tree.items()})
        for n in closed:
            s["issues"][str(n)].update(state="closed", state_reason="completed", closed_at="2026-10-09T01:00:00Z")
        for n in not_planned:
            s["issues"][str(n)].update(state="closed", state_reason="not_planned", closed_at="2026-10-09T01:00:00Z")
        self.save()
        self.comments_at_start = {k: len(v.get("comments", [])) for k, v in s["issues"].items()}

    def state_of(self, n):
        """Issue n's state and close reason on GitHub now."""
        i = self.load()["issues"][str(n)]
        return i["state"], i.get("state_reason")

    def new_comments(self, n):
        """The comments on issue n since the tree was set up."""
        cs = self.load()["issues"][str(n)].get("comments", [])
        return [c["body"] for c in cs[self.comments_at_start.get(str(n), 0):]]


def closed_saying_why(hub, n, crit, case):
    """Fail naming crit unless issue n closed as completed with the autopilot close's line."""
    assert hub.state_of(n) == ("closed", "completed"), (
        f"{crit} ({case}): the sweep left #{n} {hub.state_of(n)} though all its sub-issues are closed, expected it "
        f"closed as completed\n{hub.log[-3000:]}")
    said = hub.new_comments(n)
    want = agent.tree_done_comment(n).strip()
    assert [c.strip() for c in said] == [want], \
        f"{crit} ({case}): #{n} got {said!r} when the sweep closed it, expected exactly one comment {want!r}"


def test_the_sweep_closes_an_open_parent_whose_sub_issues_are_all_closed(record_property, tmp_path):
    """Each 15-minute sweep closes an open parent whose sub-issues are all closed, saying why.

    Proves 367.5. #57 has #101 and #102, both closed at 01:00 and nothing on autopilot; the close event never closed #57. One
    scheduled run must close #57 as completed with exactly one comment, the autopilot close's one line. Beside it,
    #58 has #103 closed and #104 still open: it must stay open with no comment. Neither was updated since the last
    sweep."""
    record_property("proves", "367.5")
    hub = TreeHub(tmp_path)
    hub.tree({57: [101, 102], 58: [103, 104]}, closed=[101, 102, 103])
    must_redraw(hub, schedule(), "367.5")
    closed_saying_why(hub, 57, "367.5", "all closed")
    assert hub.state_of(58)[0] == "open", "367.5 (one open): the sweep closed #58 while its sub-issue #104 is open"
    assert hub.new_comments(58) == [], f"367.5 (one open): #58 got comments while #104 is open: {hub.new_comments(58)}"
    assert hub.state_of(104)[0] == "open", "367.5 (one open): the sweep closed #104, a sub-issue, not a parent"


def test_the_sweep_counts_a_sub_issue_closed_as_not_planned_as_done(record_property, tmp_path):
    """The sweep counts a sub-issue closed as not planned as done.

    Proves 367.5. #57 has #101 closed as completed and #102 closed as not planned; #58 has #103 and #104 both closed as not
    planned. One scheduled run must close #57 and #58, each as completed with the one line. #59 has #105 closed as
    not planned and #106 open: it must stay open with no comment."""
    record_property("proves", "367.5")
    hub = TreeHub(tmp_path)
    hub.tree({57: [101, 102], 58: [103, 104], 59: [105, 106]}, closed=[101], not_planned=[102, 103, 104, 105])
    must_redraw(hub, schedule(), "367.5")
    closed_saying_why(hub, 57, "367.5", "one not planned")
    closed_saying_why(hub, 58, "367.5", "all not planned")
    assert hub.state_of(59)[0] == "open", "367.5 (not planned, one open): the sweep closed #59 while #106 is open"
    assert hub.new_comments(59) == [], f"367.5 (not planned, one open): #59 got comments: {hub.new_comments(59)}"


def test_the_sweep_closes_one_level_up_in_turn(record_property, tmp_path):
    """The sweep closes a grandparent once the parent it closed was its last.

    Proves 367.5. #57 has #101 and #102; #101 has #201 and #202. #201, #202 and #102 closed at 01:00, but #101 and #57 are still
    open. One scheduled run must close #101 and then #57, each as completed with the one line. Beside it, #60 has
    #110 and #111, #110 has #210 closed, and #111 is open: the run must close #110 and leave #60 open, no comment."""
    record_property("proves", "367.5")
    hub = TreeHub(tmp_path)
    hub.tree({57: [101, 102], 101: [201, 202], 60: [110, 111], 110: [210]}, closed=[201, 202, 102, 210])
    must_redraw(hub, schedule(), "367.5")
    closed_saying_why(hub, 101, "367.5", "two levels, #101")
    closed_saying_why(hub, 57, "367.5", "two levels, #57")
    closed_saying_why(hub, 110, "367.5", "two levels, #110")
    assert hub.state_of(60)[0] == "open", "367.5 (two levels, one open): the sweep closed #60 while #111 is open"
    assert hub.new_comments(60) == [], f"367.5 (two levels, one open): #60 got comments: {hub.new_comments(60)}"


def test_the_sweep_leaves_a_closed_parent_alone_and_closes_nothing_twice(record_property, tmp_path):
    """The sweep never closes or comments on a parent twice, nor on one already closed.

    Proves 367.6. #57 was closed by hand as not planned with both #101 and #102 closed; #58 is open with #103 and #104 closed.
    The first scheduled run must leave #57 closed as not planned with no comment and close #58 with its one line.
    A second scheduled run must change neither and post no comment anywhere."""
    record_property("proves", "367.6")
    hub = TreeHub(tmp_path)
    hub.tree({57: [101, 102], 58: [103, 104]}, closed=[101, 102, 103, 104])
    s = hub.load()
    s["issues"]["57"].update(state="closed", state_reason="not_planned", closed_at="2026-10-09T01:00:00Z")
    hub.save()
    must_redraw(hub, schedule(), "367.6")
    assert hub.state_of(57) == ("closed", "not_planned"), \
        f"367.6 (already closed): the sweep closed #57 again: it is now {hub.state_of(57)}, expected closed as not planned"
    assert hub.new_comments(57) == [], f"367.6 (already closed): the sweep commented on #57: {hub.new_comments(57)}"
    closed_saying_why(hub, 58, "367.6", "open parent, first sweep")
    hub.last_sweep("2026-10-09T23:00:00Z")
    hub.clear_writes()
    must_redraw(hub, schedule(), "367.6")
    again = [w for w in hub.writes() if w["op"] in ("close", "comment")]
    assert again == [], f"367.6 (second sweep): the sweep closed or commented again: {again}"
    assert len(hub.new_comments(58)) == 1, \
        f"367.6 (second sweep): #58 now has {hub.new_comments(58)!r}, expected its one line only"
