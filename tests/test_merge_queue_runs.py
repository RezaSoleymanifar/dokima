"""Runs after the merge queue's own test runs touch no card and never fail (#377).

When a pull request sits in the merge queue, GitHub runs done-whens and full suite on the queued commit, a `merge_group`
event with no pull request: its workflow_run payload has event `merge_group`, no pull_requests and head branch
`gh-readonly-queue/main/pr-N-SHA`. card.yml and board.yml start after those runs. Before this, card.yml's card job went
on to look the commit's pull request up and draw its cards, and board.yml's sync job read the board, so either could
touch a card or fail on a run that is about no card at all. A pull request's own done-whens and full suite runs must
still redraw and place its cards and its issue's, as they do today.

These tests play card.yml and board.yml with tests/card_player.py against its fake GitHub (issue #246 with PR #260,
issue #312 with PR #314, each with a stale card). The fake answers no board query, as when GitHub cannot be read, so a
board.yml run that reads the board fails. board.yml is played with DOKIMA_BOARD set to a board, as on a repo that has
one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from card_player import OWNER, REPOSITORY, STALE_CARD, Hub, Run, checks_finished, load_yaml, must_redraw, sender, \
    stale_again  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BOARD_YML = os.path.join(ROOT, ".github", "workflows", "board.yml")
PAIRS = ((246, 260), (312, 314))
# The workflows card.yml and board.yml start after that run in the merge queue.
QUEUE_RUNS = ("done-whens", "full suite")


def queue_finished(n, p, workflow, conclusion="success", sha=None):
    """A workflow_run event: `workflow` finished on the merge queue's commit for PR p.

    As GitHub sends it for a merge_group run: event merge_group, no pull requests, head branch
    gh-readonly-queue/main/pr-p-SHA. `sha` is the queued commit; given the PR's own head, GitHub lists the PR for it."""
    run = {"name": workflow, "head_sha": sha or f"queue{p}", "head_branch": f"gh-readonly-queue/main/pr-{p}-mainsha",
           "display_title": f"Merge pull request #{p} from o/try/issue-{n}", "event": "merge_group",
           "status": "completed", "conclusion": conclusion, "pull_requests": [],
           "actor": sender(OWNER), "triggering_actor": sender(OWNER)}
    return "workflow_run", {"action": "completed", "workflow": {"name": workflow}, "workflow_run": run,
                            "sender": sender(OWNER), "repository": REPOSITORY}


def board_workflow():
    """board.yml, read, as on a repo whose DOKIMA_BOARD variable names a board."""
    text = open(BOARD_YML).read()
    assert "vars.DOKIMA_BOARD" in text, "test setup: board.yml no longer reads vars.DOKIMA_BOARD"
    return load_yaml(text.replace("vars.DOKIMA_BOARD", "format('o/1')"))


def play_board(hub, event):
    """Play board.yml for one event against the fake GitHub; returns its Run."""
    return Run(hub, *event, wf=board_workflow())


def bodies(hub):
    """Every issue's and PR's body on the fake GitHub, keyed '#n'."""
    s = hub.load()
    return {**{f"#{n}": i["body"] for n, i in s["issues"].items()}, **{f"#{p}": x["body"] for p, x in s["prs"].items()}}


def test_a_merge_queue_run_makes_card_yml_change_nothing_and_never_fail(tmp_path, record_property):
    """Merge-queue runs make card.yml change nothing and never fail; a PR's run still redraws.

    Proves 377.1. Plays card.yml for done-whens and full suite finishing, passed and failed, on the merge queue's commit for PR #260
    (issue #246) and PR #314 (issue #312), with every card stale. GitHub lists the pull request for the queued commit,
    so a card job that looks it up would redraw its cards: no issue or PR body and no comment may be written, every
    card must still be the stale one, and no job may fail. Then the same runs with GitHub refusing to read or write
    the issue and its PR: still no job may fail. Beside it, the same workflows finishing on the pull request itself
    must still redraw the issue's and the PR's cards, so card.yml was not simply switched off after those runs."""
    record_property("proves", "377.1")
    hub = Hub(tmp_path)
    for workflow in QUEUE_RUNS:
        for n, p in PAIRS:
            stale_again(hub)
            must_redraw(hub, checks_finished(n, p, workflow), "377.1")
            wrote = {(x["op"], x["n"]) for x in hub.writes()}
            assert ("issue-body", n) in wrote and ("pr-body", p) in wrote, \
                f"377.1: {workflow} finishing on PR #{p} itself redrew only {sorted(wrote)}, not issue #{n} and PR #{p}"
        for conclusion in ("success", "failure"):
            for n, p in PAIRS:
                what = f"{workflow} {conclusion} in the merge queue for PR #{p}"
                stale_again(hub)
                before = bodies(hub)
                r = hub.run(*queue_finished(n, p, workflow, conclusion, sha=f"sha{p}"), "377.1")
                assert not r.failed(), f"377.1: card.yml's run after {what} failed:\n{r.log[-3000:]}"
                assert not hub.writes(), f"377.1: card.yml's run after {what} wrote {hub.writes()}\n{r.log[-2000:]}"
                assert bodies(hub) == before, f"377.1: card.yml's run after {what} changed a card"
                for op, k in (("read-issue", n), ("write-issue", n), ("write-pr", p)):
                    hub.refuse(op, k)
                r = hub.run(*queue_finished(n, p, workflow, conclusion, sha=f"sha{p}"), "377.1")
                s = hub.load()
                s["refuse"] = []
                hub.save()
                assert not r.failed(), \
                    f"377.1: card.yml's run after {what} failed when GitHub could not read #{n}:\n{r.log[-3000:]}"
                assert not hub.writes(), f"377.1: card.yml's run after {what} wrote {hub.writes()}"


def test_a_merge_queue_run_makes_board_yml_change_nothing_and_never_fail(tmp_path, record_property):
    """Merge-queue runs make board.yml change nothing and never fail; a PR's run still syncs.

    Proves 377.1. Plays board.yml, on a repo with a board, for done-whens and full suite finishing, passed and failed, on the merge
    queue's commit for PR #260 and PR #314. The fake GitHub answers no board query, as when GitHub cannot be read, so
    a run that reads or moves a card fails: no job may fail and nothing may be written. Beside it, done-whens
    finishing on the pull request itself must still run the sync step in the issue's board queue (board-246,
    board-312), so board.yml was not simply switched off after those runs."""
    record_property("proves", "377.1")
    hub = Hub(tmp_path)
    for n, p in PAIRS:
        r = play_board(hub, checks_finished(n, p, "done-whens"))
        assert r.groups.get("sync") == f"board-{n}" and "## sync: Sync the board" in r.log, \
            f"377.1: done-whens finishing on PR #{p} itself no longer syncs the board in board-{n}:\n{r.log[-2000:]}"
    for workflow in QUEUE_RUNS:
        for conclusion in ("success", "failure"):
            for n, p in PAIRS:
                what = f"{workflow} {conclusion} in the merge queue for PR #{p}"
                stale_again(hub)
                before = bodies(hub)
                r = play_board(hub, queue_finished(n, p, workflow, conclusion))
                assert not r.failed(), f"377.1: board.yml's run after {what} failed:\n{r.log[-3000:]}"
                assert not hub.writes() and bodies(hub) == before, f"377.1: board.yml's run after {what} changed a card"
