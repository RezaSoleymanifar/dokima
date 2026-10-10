"""The board updates only when a card can change, once per burst (#380).

GitHub's GraphQL budget (5,000 calls an hour, shared by every Dokima workflow) ran out on 2026-10-09, and board.yml
alone used about 56% of it: it recomputed an issue's cards on every comment, line note, new commit and finished
check, though none of those can move a card. These tests hold the fix to the owner's words:

- `python3 -m dokima.board queue`, the step that already names each event's board queue from its payload alone,
  also writes `run=true` or `run=false` to GITHUB_OUTPUT: false exactly for an event that cannot change a card's
  column or pill, true for every other one (and for any event it cannot read). board.yml's sync job runs only on
  true, so a skipped event spends no GraphQL call at all.
- Events about one issue that arrive within a minute become one update: board.yml waits one minute in a queue of
  the issue's own that a newer event cancels, and only then syncs.
- The 15-minute sweep stays, so a card a skipped event could have put right is put right there.
- The card is saved on the issue only when what code draws differs from what the issue shows.
- Skipping changes nothing: on every history played here, today's board update on a skipped event would have left
  every card exactly where it was.

board.yml is played with tests/test_start.py's reader and evaluator: each job's `if:`, outputs and concurrency group
are evaluated the way GitHub evaluates them, with the queue step's real outputs. The board itself runs against
tests/test_needs_you.py's in-memory world, as tests/test_board_state.py does.
"""
import copy
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import test_board_state as tbs  # noqa: E402
import test_needs_you as tny  # noqa: E402
from test_agent import GOOD_WORK, rec  # noqa: E402
from test_body import github, run_card  # noqa: E402,F401  (github is the fixture run_card needs)
from test_start import Ctx, condition, evaluate, fill, load_yaml  # noqa: E402
from dokima import agent, board, body, plan  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BOARD_YML = os.path.join(ROOT, ".github", "workflows", "board.yml")
SPEC, REPO, OWNER, LABEL = tny.SPEC, tny.REPO, tny.OWNER, tny.LABEL
NEEDS, AUTO = tny.NEEDS, tny.AUTO
BOT_LOGIN = f"{agent.BOT}[bot]"
STRANGER = "someone-else" if OWNER != "someone-else" else "another-person"
ASK = "The board is updated only when it can change.\n\n- Bursts become one update.\n"


# --- payloads, as GitHub sends them -------------------------------------------------------------------------------

def issue_payload(n, action, labels=(), state="open", issue_body=ASK, **extra):
    """An `issues` event on issue n."""
    return {"action": action, "issue": {"number": n, "state": state, "body": issue_body,
                                        "labels": [{"name": x} for x in labels]}, **extra}


def labeled(n, action, name):
    """An `issues` labeled or unlabeled event for one label."""
    return issue_payload(n, action, labels=[name] if action == "labeled" else [], label={"name": name})


def comment_on_issue(n, words, login=OWNER, kind="User"):
    """A comment created on issue n."""
    return {"action": "created", "issue": {"number": n, "state": "open", "body": ASK, "labels": []},
            "comment": {"body": words, "user": {"login": login, "type": kind}}}


def comment_on_pr(pr, issue, words, login=OWNER, kind="User"):
    """A comment created on pull request `pr`, built for `issue`."""
    return {"action": "created", "issue": {"number": pr, "state": "open", "body": f"Closes #{issue}", "labels": [],
                                           "pull_request": {"url": f"https://api.github.com/repos/o/r/pulls/{pr}"}},
            "comment": {"body": words, "user": {"login": login, "type": kind}}}


def pr_payload(pr, issue, merged=False, state="open"):
    """A pull request as event payloads carry it, built for `issue` from its try branch."""
    return {"number": pr, "state": state, "merged": merged, "body": f"Closes #{issue}", "labels": [],
            "head": {"ref": f"try/issue-{issue}"}}


def pr_event(action, pr, issue, merged=False):
    """A `pull_request_target` event."""
    return {"action": action, "pull_request": pr_payload(pr, issue, merged, "closed" if action == "closed" else "open")}


def review(pr, issue, state, words, login=OWNER, kind="User"):
    """A pull request review submitted with this state and summary."""
    return {"action": "submitted", "pull_request": pr_payload(pr, issue),
            "review": {"state": state, "body": words, "user": {"login": login, "type": kind}}}


def line_note(pr, issue, words):
    """A line note created on the pull request's diff."""
    return {"action": "created", "pull_request": pr_payload(pr, issue),
            "comment": {"body": words, "path": "dokima/board.py", "line": 3, "user": {"login": OWNER, "type": "User"}}}


def checks(pr, issue, conclusion):
    """The done-whens checks finishing on the pull request."""
    return {"action": "completed", "workflow_run": {"name": "done-whens", "conclusion": conclusion, "pull_requests": [
        {"number": pr, "head": {"ref": f"try/issue-{issue}"}}]}}


def record_text(r):
    """A record comment's body, as code posts it."""
    return f"The run is done.\n\n{agent.MARK}\n<details><summary>Record</summary>\n\n```json\n{json.dumps(r)}\n```\n</details>"


def live_card(role="Worker"):
    """A run card the bot puts up when a run is queued."""
    return f"{agent.LIVE}\n**{role}** · queued\n\nThe machine is setting up."


def card_edit(n):
    """The bot redraws the card above the marker: the owner's ask below it is unchanged."""
    old = body.redraw(ASK, "<!-- dokima-card -->\nPlan\n<!-- /dokima-card -->")
    new = body.redraw(old, "<!-- dokima-card -->\nWork\n<!-- /dokima-card -->")
    return issue_payload(n, "edited", issue_body=new, changes={"body": {"from": old}})


def first_card(n):
    """The first card drawn on a fresh ask, keeping the whole ask below it."""
    return issue_payload(n, "edited", issue_body=body.redraw(ASK, "<!-- dokima-card -->\nBacklog\n<!-- /dokima-card -->"),
                         changes={"body": {"from": ASK}})


def ask_edit(n):
    """A person changes the owner's ask below the marker."""
    old = body.redraw(ASK, "<!-- dokima-card -->\nPlan\n<!-- /dokima-card -->")
    new = old.split(body.MARKER, 1)[0] + body.MARKER + "\n\n" + ASK + "\nAlso the cards.\n"
    return issue_payload(n, "edited", issue_body=new, changes={"body": {"from": old}})


SCHEDULE = ("schedule", {"schedule": "*/15 * * * *"})


def skipped_events(n=57, pr=60):
    """Every event about issue n or its PR that cannot move a card."""
    return {
        "a stranger's comment on the issue": ("issue_comment", comment_on_issue(n, "Looks right to me.", STRANGER)),
        "the code owner's comment that is no command": ("issue_comment", comment_on_issue(n, "Thanks, I'll look tomorrow.")),
        "the code owner's comment naming a command later in it": ("issue_comment", comment_on_issue(n, "Should I say /work now?")),
        "a comment on the pull request": ("issue_comment", comment_on_pr(pr, n, "A note on the diff.", STRANGER)),
        "a bot comment that is no record, run card or Autopilot line": (
            "issue_comment", comment_on_issue(n, "**Issue text not updated:** the owner's part would change.", BOT_LOGIN, "Bot")),
        "a line note": ("pull_request_review_comment", line_note(pr, n, "Rename this.")),
        "a review that only comments": ("pull_request_review", review(pr, n, "commented", "Nice.")),
        "an Approve with no summary": ("pull_request_review", review(pr, n, "approved", "")),
        "an Approve with a summary that is no command": ("pull_request_review", review(pr, n, "approved", "Looks good.")),
        "new commits on the pull request": ("pull_request_target", pr_event("synchronize", pr, n)),
        "the done-whens checks passing": ("workflow_run", checks(pr, n, "success")),
        "the done-whens checks failing": ("workflow_run", checks(pr, n, "failure")),
        "the label bug added": ("issues", labeled(n, "labeled", "bug")),
        "the label bug removed": ("issues", labeled(n, "unlabeled", "bug")),
        "the card redrawn above the marker": ("issues", card_edit(n)),
        "the first card drawn on a fresh ask": ("issues", first_card(n)),
        "the title edited": ("issues", issue_payload(n, "edited", changes={"title": {"from": "An older title"}})),
    }


def run_events(n=57, pr=60):
    """Every event about issue n or its PR that can move a card."""
    worker = rec("worker", handback=GOOD_WORK)
    out = {
        "the issue opened": ("issues", issue_payload(n, "opened")),
        "the issue closed": ("issues", issue_payload(n, "closed", state="closed")),
        "the issue reopened": ("issues", issue_payload(n, "reopened")),
        "the owner's ask edited below the marker": ("issues", ask_edit(n)),
        "an edit GitHub sends with no changes": ("issues", issue_payload(n, "edited")),
        "/plan on the issue": ("issue_comment", comment_on_issue(n, "/plan Go on with the planner's reading.")),
        "/work on the issue": ("issue_comment", comment_on_issue(n, "/work")),
        "/review on the issue": ("issue_comment", comment_on_issue(n, "/review")),
        "/autopilot start on the issue": ("issue_comment", comment_on_issue(n, "/autopilot start")),
        "/autopilot stop on the issue": ("issue_comment", comment_on_issue(n, "/autopilot stop")),
        "/review on the pull request": ("issue_comment", comment_on_pr(pr, n, "/review Look again.")),
        "a record the bot posts on the issue": ("issue_comment", comment_on_issue(n, record_text(worker), BOT_LOGIN, "Bot")),
        "a record the bot posts on the pull request": ("issue_comment", comment_on_pr(pr, n, record_text(worker), BOT_LOGIN, "Bot")),
        "a run card the bot puts up": ("issue_comment", comment_on_issue(n, live_card(), BOT_LOGIN, "Bot")),
        "a review asking for changes with /work": ("pull_request_review", review(pr, n, "changes_requested", "/work Fix the name.")),
        "a review the bot submits with its record": ("pull_request_review", review(pr, n, "commented", record_text(worker), BOT_LOGIN, "Bot")),
        "the pull request opened": ("pull_request_target", pr_event("opened", pr, n)),
        "the pull request reopened": ("pull_request_target", pr_event("reopened", pr, n)),
        "the pull request merged": ("pull_request_target", pr_event("closed", pr, n, merged=True)),
        "the pull request closed unmerged": ("pull_request_target", pr_event("closed", pr, n)),
        "an event the board does not know": ("workflow_dispatch", {"inputs": {}}),
        "the 15-minute sweep": SCHEDULE,
    }
    for name in (LABEL, "high", "parked"):
        out[f"the label {name} added"] = ("issues", labeled(n, "labeled", name))
        out[f"the label {name} removed"] = ("issues", labeled(n, "unlabeled", name))
    for line in (agent.AUTOPILOT_LINES["worker"], agent.AUTOPILOT_LINES["split"], agent.AUTOPILOT_LINE, agent.AUTOPILOT_START_LINE):
        out[f"the bot's line {line!r}"] = ("issue_comment", comment_on_issue(n, line, BOT_LOGIN, "Bot"))
    return out


# --- the queue step, run as board.yml runs it ---------------------------------------------------------------------

def queue_outputs(event, payload, monkeypatch, tmp_path, k):
    """What the queue step writes to GITHUB_OUTPUT for this event, as {key: value}."""
    d = tmp_path / f"q{len(list(tmp_path.glob('q*')))}"
    d.mkdir()
    (d / "event.json").write_text(json.dumps(payload))
    (d / "output.txt").write_text("")
    for key, value in (("GITHUB_EVENT_NAME", event), ("GITHUB_EVENT_PATH", str(d / "event.json")),
                       ("GITHUB_OUTPUT", str(d / "output.txt")), ("GITHUB_RUN_ID", "4242"), ("GITHUB_REPOSITORY", REPO)):
        monkeypatch.setenv(key, value)
    code = board.main(["board", "queue"])
    assert code == 0, f"{k}: `python3 -m dokima.board queue` exited {code} on a {event} event"
    return dict(line.split("=", 1) for line in (d / "output.txt").read_text().splitlines() if "=" in line)


def runs(event, payload, monkeypatch, tmp_path, k):
    """True when the queue step writes run=true for this event, False for run=false."""
    out = queue_outputs(event, payload, monkeypatch, tmp_path, k)
    assert out.get("run") in ("true", "false"), \
        f"{k}: the queue step wrote {out} to GITHUB_OUTPUT on a {event} event, with no run=true or run=false"
    return out["run"] == "true"


# --- board.yml, played as GitHub plays it --------------------------------------------------------------------------

def jobs_of():
    """board.yml's jobs, read."""
    return load_yaml(open(BOARD_YML).read())["jobs"]


def runs_text(job):
    """Every `run:` script of a job, joined."""
    return "\n".join(str(s.get("run", "")) for s in job.get("steps") or [] if isinstance(s, dict))


def needs_of(job):
    n = job.get("needs") or []
    return [n] if isinstance(n, str) else list(n)


def queue_job(jobs):
    found = [j for j, b in jobs.items() if "python3 -m dokima.board queue" in runs_text(b)]
    assert found, "test setup: no job in board.yml runs `python3 -m dokima.board queue`"
    return found[0]


def sync_job(jobs):
    found = [j for j, b in jobs.items() if re.search(r"(?m)^\s*python3 -m dokima\.board\s*$", runs_text(b))]
    assert found, "test setup: no job in board.yml runs `python3 -m dokima.board`"
    return found[0]


def upstream(jobs, name):
    """Every job `name` needs, directly or through others."""
    seen, todo = set(), needs_of(jobs[name])
    while todo:
        j = todo.pop()
        if j not in seen and j in jobs:
            seen.add(j)
            todo += needs_of(jobs[j])
    return seen


def play(event, payload, monkeypatch, tmp_path, k, results=None):
    """Play board.yml's jobs for one event: {job: {"ran", "group", "cancels"}}.

    The queue job's step outputs are the real queue step's for this event. A job runs when its `if:` (with GitHub's
    implied success()) holds over its needs; `results` forces a job's result (for example "cancelled", as when a
    newer event cancels it), and a job that does not run is "skipped". Each job's concurrency group and
    cancel-in-progress are filled in whether it runs or not."""
    jobs, results = jobs_of(), dict(results or {})
    q = queue_job(jobs)
    step_out = queue_outputs(event, payload, monkeypatch, tmp_path, k)
    step_ids = [s["id"] for s in jobs[q].get("steps") or [] if isinstance(s, dict) and s.get("id")]
    base = {"github": {"event_name": event, "event": payload, "run_id": "4242", "repository": REPO},
            "vars": {"DOKIMA_BOARD": SPEC, "DOKIMA_APP_ID": "1"}, "secrets": {"DOKIMA_APP_KEY": "k"}, "env": {}, "inputs": {}}
    done, outputs, got = {}, {}, {}
    while len(done) < len(jobs):
        ready = [j for j in jobs if j not in done and all(n in done for n in needs_of(jobs[j]))]
        assert ready, "test setup: board.yml's jobs need each other in a loop"
        for j in ready:
            job = jobs[j]
            ctx = Ctx({key: Ctx(v) for key, v in {**base, "needs": {n: {"result": done[n], "outputs": outputs.get(n, {})} for n in needs_of(job)},
                       "steps": {sid: {"outputs": step_out} for sid in step_ids} if j == q else {}}.items()})
            status = {"failed": any(done[n] == "failure" for n in needs_of(job)),
                      "cancelled": any(done[n] == "cancelled" for n in needs_of(job)),
                      "success": all(done[n] == "success" for n in needs_of(job))}
            cond = re.sub(r"^\$\{\{(.*)\}\}$", r"\1", str(job.get("if") or "").strip())
            ran = bool(evaluate(condition(cond), ctx, status))
            done[j] = results.get(j, "success") if ran else "skipped"
            outputs[j] = {key: fill(v, ctx, status) for key, v in (job.get("outputs") or {}).items()} if ran else {}
            conc = job.get("concurrency")
            group = fill(conc.get("group"), ctx, status) if isinstance(conc, dict) else (fill(conc, ctx, status) if conc else None)
            cancels = isinstance(conc, dict) and fill(str(conc.get("cancel-in-progress", "false")), ctx, status).strip() == "true"
            got[j] = {"ran": ran, "group": group, "cancels": cancels}
    return got


def settle_job(jobs):
    """The job the sync waits on that sleeps in a cancelling queue, or None."""
    s = sync_job(jobs)
    for j in sorted(upstream(jobs, s) - {queue_job(jobs)}):
        conc = jobs[j].get("concurrency")
        if isinstance(conc, dict) and str(conc.get("cancel-in-progress", "")).strip() not in ("", "false") \
                and re.search(r"\bsleep\s+\d+", runs_text(jobs[j])):
            return j
    return None


# --- the board's in-memory world ------------------------------------------------------------------------------------

@pytest.fixture
def make(monkeypatch):
    """Wire a world into dokima.board.Board and dokima.agent.gh, and return it (as tests/test_board_state.py does)."""

    def wire(**kw):
        world = tny.World(**kw)
        monkeypatch.setattr(board, "Board", tbs.fake_board(world))
        monkeypatch.setattr(agent, "gh", tny.fake_gh(world))
        return world

    return wire


def settle(w, n=57):
    """Put issue n's cards where its state says now, the way any board update does."""
    board.rebuild(board.Board(SPEC, REPO), REPO, plan.repo_approvers("o"), n)


# =================================================================================================================
# 380.1: an event that cannot change a card's column or pill does not run the board update

def test_events_that_cannot_move_a_card_do_not_run_the_board_update(record_property, monkeypatch, tmp_path):
    """Comments, line notes, new commits, checks and other labels skip the board update.

    Runs the queue step on each event about #57 or its PR #60 that cannot change a column or pill: a stranger's
    comment, the code owner's comment with no command, a comment on the PR, a bot comment that is no record, run card
    or Autopilot line, a line note, a review that only comments, an Approve with or without words, new commits, the
    done-whens checks passing or failing, the label bug added or removed, the card redrawn above the marker, the first
    card on a fresh ask, and a title edit. Each must write run=false. Proves 380.1."""
    record_property("proves", "380.1")
    ran = [what for what, (e, p) in skipped_events().items() if runs(e, p, monkeypatch, tmp_path, "380.1")]
    assert not ran, f"380.1: these events cannot change a card's column or pill, yet they run the board update: {ran}"


def test_events_that_can_move_a_card_still_run_the_board_update(record_property, monkeypatch, tmp_path):
    """Every event that can change a column or pill still runs the board update.

    Runs the queue step on: the issue opened, closed or reopened; the owner's ask edited, or an edit GitHub sends with
    no changes; /plan, /work, /review, /autopilot start and stop on the issue and /review on the PR; a record the bot
    posts on the issue or the PR, a run card, each Autopilot line; a review asking for changes with /work, a review the
    bot submits with its record; the PR opened, reopened, merged or closed; the labels autopilot, high and parked added
    or removed; the 15-minute sweep; and an event the board does not know. Each must write run=true. Proves 380.1."""
    record_property("proves", "380.1")
    skipped = [what for what, (e, p) in run_events().items() if not runs(e, p, monkeypatch, tmp_path, "380.1")]
    assert not skipped, f"380.1: these events can change a card's column or pill, yet the board update is skipped: {skipped}"


def test_an_event_the_queue_step_cannot_read_still_runs_the_board_update(record_property, monkeypatch, tmp_path):
    """An event the queue step cannot read still runs the board update.

    A comment event with no comment in it, a review with no review, an edit with no changes field and a label event
    with no label must each write run=true and exit 0, so a payload the step does not understand never hides an update. Proves 380.1."""
    record_property("proves", "380.1")
    odd = {"a comment event with no comment": ("issue_comment", {"action": "created", "issue": {"number": 57}}),
           "a review event with no review": ("pull_request_review", {"action": "submitted", "pull_request": pr_payload(60, 57)}),
           "an edit with no changes field": ("issues", {"action": "edited", "issue": {"number": 57, "labels": []}}),
           "a label event with no label": ("issues", {"action": "labeled", "issue": {"number": 57, "labels": []}})}
    skipped = [what for what, (e, p) in odd.items() if not runs(e, p, monkeypatch, tmp_path, "380.1")]
    assert not skipped, f"380.1: the queue step could not read these events, yet it skipped the board update: {skipped}"


def test_board_yml_syncs_the_board_only_when_the_queue_step_says_so(record_property, monkeypatch, tmp_path):
    """board.yml syncs the board only on events the queue step lets through.

    Plays board.yml's jobs, their `if:` evaluated as GitHub does with the queue step's real outputs: on every skipped
    event the job running `python3 -m dokima.board` must not run, and on every event that can change a card it must. Proves 380.1."""
    record_property("proves", "380.1")
    jobs = jobs_of()
    s = sync_job(jobs)
    wrong_run = [w for w, (e, p) in skipped_events().items() if play(e, p, monkeypatch, tmp_path, "380.1")[s]["ran"]]
    assert not wrong_run, f"380.1: board.yml's {s!r} job still syncs the board on: {wrong_run}"
    wrong_skip = [w for w, (e, p) in run_events().items() if not play(e, p, monkeypatch, tmp_path, "380.1")[s]["ran"]]
    assert not wrong_skip, f"380.1: board.yml's {s!r} job no longer syncs the board on: {wrong_skip}"


# =================================================================================================================
# 380.2: events about one issue within a minute become one board update

def test_events_about_one_issue_wait_a_minute_in_a_queue_of_their_own_that_a_newer_one_cancels(record_property, monkeypatch, tmp_path):
    """A burst about one issue becomes one update: a newer event cancels the waiting one.

    board.yml must have a job the sync job waits on that sleeps exactly 60 seconds in a concurrency group with
    cancel-in-progress true. Played for /plan on #57, a record on #57, PR #60 opened and a /work review on PR #60, that
    job runs and takes one and the same group each time; for #58 it takes another group. That group is never the sync
    job's own, so a newer event cancels only a waiting update, never a running one. Proves 380.2."""
    record_property("proves", "380.2")
    jobs = jobs_of()
    j = settle_job(jobs)
    assert j, "380.2: board.yml has no job the sync waits on that sleeps in a queue a newer event cancels"
    sleeps = [int(x) for x in re.findall(r"\bsleep\s+(\d+)", runs_text(jobs[j]))]
    assert sleeps == [60], f"380.2: the {j!r} job waits {sleeps} seconds, not one minute (sleep 60)"
    s, worker = sync_job(jobs), rec("worker", handback=GOOD_WORK)
    groups = {}
    for n, pr in ((57, 60), (58, 61)):
        for what, (e, p) in {"/plan": ("issue_comment", comment_on_issue(n, "/plan Again.")),
                             "a record": ("issue_comment", comment_on_issue(n, record_text(worker), BOT_LOGIN, "Bot")),
                             "PR opened": ("pull_request_target", pr_event("opened", pr, n)),
                             "a /work review": ("pull_request_review", review(pr, n, "changes_requested", "/work"))}.items():
            got = play(e, p, monkeypatch, tmp_path, "380.2")
            assert got[j]["ran"], f"380.2: on {what} about #{n} the {j!r} job did not run, so the update does not wait"
            assert got[j]["cancels"], f"380.2: on {what} about #{n} the {j!r} job does not cancel the one waiting before it"
            assert got[j]["group"] and got[j]["group"] != got[s]["group"], \
                f"380.2: on {what} about #{n} the waiting queue {got[j]['group']!r} is the sync job's own, so it could cancel a running update"
            groups.setdefault(n, set()).add(got[j]["group"])
    assert len(groups[57]) == 1, f"380.2: events about #57 and its PR #60 wait in different queues: {groups[57]}"
    assert len(groups[58]) == 1 and groups[57] != groups[58], \
        f"380.2: #57 and #58 share a waiting queue, so one issue's event would cancel another's update: {groups}"


def test_an_update_a_newer_event_cancelled_never_syncs(record_property, monkeypatch, tmp_path):
    """An update cancelled while it waits never syncs the board; only the newest one does.

    Plays /work on #57 with the waiting job cancelled (as a newer event about #57 cancels it): the sync job must not
    run. Played again with the waiting job finished, the sync job runs. Proves 380.2."""
    record_property("proves", "380.2")
    jobs = jobs_of()
    j, s = settle_job(jobs), sync_job(jobs)
    assert j, "380.2: board.yml has no job the sync waits on that sleeps in a queue a newer event cancels"
    e, p = "issue_comment", comment_on_issue(57, "/work")
    assert not play(e, p, monkeypatch, tmp_path, "380.2", results={j: "cancelled"})[s]["ran"], \
        f"380.2: the {j!r} job was cancelled by a newer event, yet the {s!r} job still syncs the board"
    assert play(e, p, monkeypatch, tmp_path, "380.2")[s]["ran"], f"380.2: after the {j!r} job waited, the {s!r} job did not run"


def test_a_skipped_event_never_cancels_an_update_waiting_for_its_issue(record_property, monkeypatch, tmp_path):
    """An event that skips the update never cancels one waiting for its issue.

    For each skipped event about #57 (a comment, a line note, new commits, finished checks...), the waiting job must not
    run, and its queue must not be the one /work on #57 waits in, so the record that came a second before it still
    lands on the board. Proves 380.2."""
    record_property("proves", "380.2")
    jobs = jobs_of()
    j = settle_job(jobs)
    assert j, "380.2: board.yml has no job the sync waits on that sleeps in a queue a newer event cancels"
    waiting = play("issue_comment", comment_on_issue(57, "/work"), monkeypatch, tmp_path, "380.2")[j]["group"]
    bad = []
    for what, (e, p) in skipped_events().items():
        got = play(e, p, monkeypatch, tmp_path, "380.2")[j]
        if got["ran"] or got["group"] == waiting:
            bad.append(what)
    assert not bad, f"380.2: these skipped events take #57's waiting queue {waiting!r} and would cancel its update: {bad}"


# =================================================================================================================
# 380.3: the 15-minute sweep stays as the safety net

def test_the_15_minute_sweep_still_syncs_the_board(record_property, monkeypatch, tmp_path):
    """The 15-minute sweep still runs the board update.

    board.yml must still be scheduled every 15 minutes, the queue step must write run=true for it, and played for the
    schedule, the job running `python3 -m dokima.board` runs. Proves 380.3."""
    record_property("proves", "380.3")
    text = open(BOARD_YML).read()
    assert re.search(r"cron:\s*[\"']\*/15 \* \* \* \*[\"']", text), "380.3: board.yml is no longer scheduled every 15 minutes"
    assert runs(*SCHEDULE, monkeypatch, tmp_path, "380.3"), "380.3: the queue step skips the 15-minute sweep"
    s = sync_job(jobs_of())
    assert play(*SCHEDULE, monkeypatch, tmp_path, "380.3")[s]["ran"], f"380.3: the {s!r} job does not run on the 15-minute sweep"


def test_a_card_a_skipped_event_left_wrong_is_put_right_by_the_next_sweep(record_property, make, monkeypatch, tmp_path):
    """A card left wrong after a skipped event is put right by the next sweep.

    #57's code review approved, so its card and PR #60's belong in Review with Needs you, but both sit in Work with no
    pill. A stranger's comment on #57 arrives: the queue step skips it (run=false). The next 15-minute sweep, with #57
    updated since the last good sweep, must put both cards in Review with Needs you. Proves 380.3."""
    record_property("proves", "380.3")
    w = make(prs={57: 60}, records={57: tny.code_approved()},
             cards={("issue", 57): {"Status": "Work"}, ("pr", 60): {"Status": "Work"}})
    e, p = "issue_comment", comment_on_issue(57, "Looks right to me.", STRANGER)
    assert not runs(e, p, monkeypatch, tmp_path, "380.3"), "380.3: test setup: a stranger's comment still runs the board update"
    tbs.with_github_lists(w, monkeypatch, runs=tbs.BOARD_RUNS, updated={("issue", 57): "2026-10-09T15:40:00Z"})
    board.sync(*SCHEDULE, SPEC, REPO)
    got = tbs.places(w, ("issue", 57), ("pr", 60))
    assert got == {"issue #57": ("Review", NEEDS), "pr #60": ("Review", NEEDS)}, \
        f"380.3: the sweep after a skipped event left #57's cards at {got}, not Review with Needs you"


# =================================================================================================================
# 380.4: a card is written on the issue only when what it shows changed

CARD_A = "<!-- dokima-card -->\n**Plan**\n<!-- /dokima-card -->"
CARD_B = "<!-- dokima-card -->\n**Work**\n<!-- /dokima-card -->"


class Recorder:
    """Stands in for gh: records every call, answers nothing."""

    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kw):
        self.calls.append(([str(a) for a in args], kw.get("input")))
        return ""


def test_an_issue_already_showing_its_card_is_not_saved_again(record_property, monkeypatch):
    """An issue showing its card is not saved again; a changed card is saved once.

    Saves the same card on #57 whose text already holds it: no call reaches GitHub at all (no edit, no comment). Then
    saves a different card: exactly one edit of #57, carrying the new card above the marker and the owner's ask
    unchanged below it. Proves 380.4."""
    record_property("proves", "380.4")
    fake = Recorder()
    monkeypatch.setattr(body, "gh", fake)
    current = body.redraw(ASK, CARD_A)
    body.save(REPO, 57, current, CARD_A)
    assert fake.calls == [], f"380.4: the issue already showed this card, yet it was saved again: {fake.calls}"
    body.save(REPO, 57, current, CARD_B)
    edits = [(a, i) for a, i in fake.calls if a[:2] == ["issue", "edit"]]
    assert len(fake.calls) == 1 and len(edits) == 1, f"380.4: a changed card made {fake.calls}, not one edit of the issue"
    assert edits[0][1] == body.redraw(current, CARD_B), "380.4: the changed card was not saved as drawn above the owner's ask"


def test_a_card_run_on_an_issue_already_showing_its_card_writes_nothing(record_property, monkeypatch, github):
    """A card run on an issue whose card is current writes nothing to it.

    Runs the card on a fresh ask: it saves the card above the ask. Runs it again on what it saved: nothing is saved
    and no comment is posted, because the card it draws is the one the issue already shows. Proves 380.4."""
    record_property("proves", "380.4")
    saved = run_card(monkeypatch, github, ASK)
    assert saved is not None, "380.4: the first card run on a fresh ask saved nothing"
    again = run_card(monkeypatch, github, saved)
    assert again is None, "380.4: the card run saved the issue again though its card had not changed"
    assert not github.comments, f"380.4: the card run posted a comment: {github.comments}"


# =================================================================================================================
# 380.5: the board ends up exactly as today; only the number of runs drops

def histories():
    """Board worlds to replay events on, each with issue #57 and PR #60."""
    blocked = tny.plan_blocked()
    return {"no record yet": {"records": {57: []}},
            "a plan approved, waiting for /work": {"records": {57: tny.plan_approved()}},
            "a plan sent back on autopilot": {"records": {57: blocked}, "labels": {("issue", 57): {LABEL}, ("pr", 60): {LABEL}}},
            "a code review approved, waiting to merge": {"records": {57: tny.code_approved()}},
            "a code review escalated": {"records": {57: tny.escalated("pr")}}}


def effects():
    """What each event changes on GitHub before it reaches the board, as {what: function(world)}."""
    worker = rec("worker", handback=GOOD_WORK)

    def said(words, login=OWNER):
        return lambda w: tny.said(w, 57, words, login)

    def reviewed(state, words):
        return lambda w: w.reviews.setdefault(60, []).append((state, words))

    def label(name, on):
        return lambda w: (w.labels.setdefault(("issue", 57), set()).add(name) if on
                          else w.labels.setdefault(("issue", 57), set()).discard(name))

    out = {
        "a stranger's comment on the issue": said("Looks right to me.", STRANGER),
        "the code owner's comment that is no command": said("Thanks, I'll look tomorrow."),
        "the code owner's comment naming a command later in it": said("Should I say /work now?"),
        "a comment on the pull request": said("A note on the diff.", STRANGER),
        "a bot comment that is no record, run card or Autopilot line": said("**Issue text not updated:** the owner's part would change.", agent.BOT),
        "a review that only comments": reviewed("COMMENTED", "Nice."),
        "an Approve with a summary that is no command": reviewed("APPROVED", "Looks good."),
        "the label bug added": label("bug", True),
        "the label bug removed": label("bug", False),
        "the issue closed": lambda w: w.closed.add(("issue", 57)),
        "/plan on the issue": said("/plan Go on with the planner's reading."),
        "/work on the issue": said("/work"),
        "/review on the issue": said("/review"),
        "/review on the pull request": said("/review Look again."),
        "a record the bot posts on the issue": lambda w: w.records[57].append(worker),
        "a record the bot posts on the pull request": lambda w: w.records[57].append(worker),
        "a run card the bot puts up": said(live_card(), agent.BOT),
        "a review asking for changes with /work": reviewed("CHANGES_REQUESTED", "/work Fix the name."),
        "the pull request merged": lambda w: w.closed.add(("pr", 60)),
        "the pull request closed unmerged": lambda w: w.closed.add(("pr", 60)),
        f"the label {LABEL} added": lambda w: w.put("issue", 57, True),
        f"the label {LABEL} removed": lambda w: w.put("issue", 57, False),
    }
    out[f"the bot's line {agent.AUTOPILOT_LINES['worker']!r}"] = said(agent.AUTOPILOT_LINES["worker"], agent.BOT)
    return out


# Events that move a card in at least one history above, so a filter that skipped them would be caught here.
MOVES_A_CARD = ("/plan on the issue", "/work on the issue", "a record the bot posts on the issue", "a run card the bot puts up",
                "a review asking for changes with /work", "the issue closed", "the pull request merged", f"the label {LABEL} added",
                f"the bot's line {agent.AUTOPILOT_LINES['worker']!r}")


def test_skipping_an_event_leaves_every_card_where_todays_update_would_put_it(record_property, make, monkeypatch, tmp_path):
    """Every skipped event would have left every card where it was today.

    For five histories of #57 and its PR #60 (no record; a plan waiting for /work; a plan sent back on autopilot; a code
    review waiting to merge; an escalation), with both cards first put where the state says, each event (skipped or
    not) first changes GitHub as it would (a comment, a review, a label, a record, a close), then reaches the queue
    step. For every event the step skips, today's board update is run on it anyway and must leave every card's column
    and pill exactly as they were. Events that do move a card in some history (/plan, /work, a record, a run card, a
    /work review, a close, a merge, the autopilot label, the Autopilot line) are in the replay, so a step that skipped
    one would fail here. Proves 380.5."""
    record_property("proves", "380.5")
    events = {**skipped_events(), **run_events()}
    fx, moved, wrong = effects(), set(), []
    for name, settings in histories().items():
        for what, (e, p) in events.items():
            w = make(prs={57: 60}, **copy.deepcopy(settings))
            settle(w)
            before = copy.deepcopy(w.cards)
            fx.get(what, lambda w: None)(w)
            skip = not runs(e, p, monkeypatch, tmp_path, "380.5")
            board.sync(e, p, SPEC, REPO)
            if w.cards != before:
                moved.add(what)
                if skip:
                    wrong.append(f"{what} on {name}: {before} -> {w.cards}")
    assert not wrong, "380.5: the queue step skips events that would have moved a card today:\n" + "\n".join(wrong)
    assert set(MOVES_A_CARD) <= moved, f"test setup: these events moved no card in any history: {set(MOVES_A_CARD) - moved}"
