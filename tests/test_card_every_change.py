"""Every change on an issue or its PR redraws both cards from card.yml alone (#438).

Story 2 of #425.

#419: the code review had passed, yet the card said Code review running for 30 minutes. card.yml picked its moments:
it skipped the bot's own edits and comments (except a code review's run card on a pull request) and redrew on a run's
start only for the full suite. The review's record is the bot's edit of its run card, so nothing redrew. Beside
card.yml, the old planner (dokima/planner.py, `post`) saved its own plan above the marker, and the plan approval
(`python3 -m dokima.agent next`, dokima/agent.py record_links) drew the cards of the issues its links touched.

These tests play card.yml one event at a time on the fake GitHub of tests/card_player.py, run the play-through's
steps there and judge them with dokima/playthrough.py's own judge, run the old planner's post and the plan approval
against fakes, read .github/workflows/playthrough.yml, and run `python3 -m dokima.playthrough` with a temp git repo
standing in for a pull request. Nothing calls real GitHub.
"""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from card_player import (BOT, MAINS_COPY, OWNER, REPOSITORY, STALE_CARD, Hub, checks_finished,  # noqa: E402
                         issue_comment, issue_event, line_note, plan_record, pr_comment, pr_event, record,
                         review_event, review_record, schedule, sender, stale_again, worker_finished, worker_record)
import card_player  # noqa: E402
from test_start import Ctx, condition, evaluate, fill, load_yaml  # noqa: E402
from dokima import agent, body  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLAYTHROUGH_YML = os.path.join(ROOT, ".github", "workflows", "playthrough.yml")
N, P = 246, 260
# The activity types GitHub starts a workflow on when its `on:` names the event with no `types:`.
DEFAULT_TYPES = {"pull_request_target": ("opened", "synchronize", "reopened"),
                 "pull_request": ("opened", "synchronize", "reopened"),
                 "workflow_run": ("requested", "completed")}
SETTING = "Require status checks to pass before merging"


# --- helpers -------------------------------------------------------------------------------------------------------

def github_starts(wf, event_name, event):
    """True when GitHub itself would start `wf` on this event, default activity types included.

    tests/card_player.py starts a workflow on any action when its `on:` lists no types; GitHub does not for
    pull_request_target and workflow_run, so this checks the types GitHub really uses."""
    if not card_player.starts(wf, event_name, event):
        return False
    t = card_player.triggers(wf)[event_name]
    types = card_player.listed(t.get("types")) if isinstance(t, dict) else []
    action = event.get("action")
    return bool(types) or event_name not in DEFAULT_TYPES or action in DEFAULT_TYPES[event_name]


def reaches_card(event_name, event):
    """True when GitHub starts card.yml on this event, itself or through a relay."""
    if github_starts(card_player.workflow(), event_name, event):
        return True
    return any(github_starts(wf, event_name, event) for _, wf in card_player.relays(event_name, event))


def run_started(n, p, workflow, state):
    """A workflow_run event: `workflow` on PR p started (in_progress) or was requested."""
    name, event = checks_finished(n, p, workflow)
    event["action"] = state
    event["workflow_run"].update(status="in_progress" if state == "in_progress" else "queued", conclusion=None)
    return name, event


def every_change(n=N, p=P):
    """Every change GitHub announces on issue n or its pull request p.

    As {what: (event name, payload)}.

    Edits, comments and labels by a person and by the bot, a run's start and its result, the pull request's own
    changes, reviews and line notes. The merge is last, so the ones before it find the pull request open."""
    live = agent.live_card("reviewer", "pr", "queued")
    return {
        "the owner opens the issue": issue_event(n, "opened"),
        "the owner edits the issue": issue_event(n, "edited"),
        "the bot edits the issue": issue_event(n, "edited", who="bot"),
        "the bot labels the issue": issue_event(n, "labeled", who="bot"),
        "the owner unlabels the issue": issue_event(n, "unlabeled"),
        "the owner closes the issue": issue_event(n, "closed"),
        "the owner reopens the issue": issue_event(n, "reopened"),
        "the owner comments on the issue": issue_comment(n),
        "the bot comments on the issue": issue_comment(n, who="bot", text="Autopilot: plan approved, starting work"),
        "the bot edits its comment on the issue": issue_comment(n, who="bot", action="edited", text="A record."),
        "the owner deletes a comment on the issue": issue_comment(n, action="deleted"),
        "the owner comments on the pull request": pr_comment(n, p),
        "the bot puts up a run card on the pull request": pr_comment(n, p, who="bot", text=live),
        "the bot posts a plain comment on the pull request": pr_comment(n, p, who="bot", text="A note from the bot."),
        "the bot edits its run card into a record on the pull request": pr_comment(n, p, who="bot", action="edited",
                                                                                   text="A record."),
        "the bot opens the pull request": pr_event(n, p, "opened"),
        "the owner edits the pull request": pr_event(n, p, "edited", who=OWNER),
        "the bot pushes a commit to the pull request": pr_event(n, p, "synchronize"),
        "the owner closes the pull request unmerged": pr_event(n, p, "closed", who=OWNER),
        "the owner reopens the pull request": pr_event(n, p, "reopened", who=OWNER),
        "the owner reviews the pull request": review_event(n, p),
        "the owner writes a note on a line": line_note(n, p),
        "the Acceptance criteria run starts": run_started(n, p, "Acceptance criteria", "in_progress"),
        "the Acceptance criteria run ends": checks_finished(n, p, "Acceptance criteria"),
        "the full suite starts": run_started(n, p, "full suite", "in_progress"),
        "the full suite ends": checks_finished(n, p, "full suite"),
        "the worker run ends": worker_finished(n),
        "the bot merges the pull request": pr_event(n, p, "closed", who="bot", merged=True),
    }


def both_redrawn(hub, n=N, p=P):
    """The cards that still hold the old card, by name; empty when both were redrawn."""
    old = "An old card, drawn before the last event."
    return [where for where, text in ((f"issue #{n}", hub.issue_body(n)), (f"PR #{p}", hub.pr_body(p))) if old in text]


def play_change(hub, what, event, k):
    """Play one change with both cards stale; card.yml's run, once it redrew both."""
    stale_again(hub)
    assert reaches_card(*event), f"{k}: card.yml does not start when {what}, so its cards keep what they showed"
    r = hub.run(*event, k)
    assert r.started and r.card_ran(), f"{k}: card.yml started when {what} but its card job did not run"
    assert not r.failed(), f"{k}: card.yml's run when {what} failed:\n{r.log[-3000:]}"
    left = both_redrawn(hub)
    assert not left, f"{k}: when {what}, card.yml left the old card on {', '.join(left)}"
    return r


def playthrough(k):
    """dokima/playthrough.py; fails naming criterion k when it cannot be imported."""
    try:
        from dokima import playthrough as p
    except ImportError as e:
        raise AssertionError(f"{k}: dokima/playthrough.py cannot be imported: {e}")
    return p


# --- 438.1: every change on an issue or its pull request redraws both cards --------------------------------------

def test_every_change_on_an_issue_or_its_pull_request_redraws_both_cards(tmp_path, record_property):
    """Every change on an issue or its pull request redraws both cards.

    Proves 438.1.
    Plays card.yml on the fake GitHub for every change GitHub announces about issue #246 or its PR #260, with both
    cards stale each time: the issue opened, edited (by the owner and by the bot), labeled, closed and reopened; a
    comment posted, edited and deleted on the issue and on the pull request, the bot's included; a run card going up
    and being edited into its record; the pull request opened, edited, pushed to, closed, reopened, reviewed, noted on
    a line and merged; the Acceptance criteria and full suite runs starting and ending; the worker run ending. GitHub
    must start card.yml for each (counting only the activity types GitHub really sends), and the run must leave
    neither card old. One missed change turns it red, naming it."""
    record_property("proves", "438.1")
    hub = Hub(tmp_path)
    missed = []
    for what, event in every_change().items():
        if what == "the bot merges the pull request":
            hub.merge(N, P, by=BOT)
        try:
            play_change(hub, what, event, "438.1")
        except AssertionError as e:
            missed.append(str(e).splitlines()[0])
    assert not missed, "438.1: not every change redraws both cards:\n" + "\n".join(missed)


def test_a_run_start_and_its_result_each_redraw_the_card_to_show_it(tmp_path, record_property):
    """A run's start and its result each redraw both cards to show it.

    Proves 438.1.
    The #419 moment on the fake GitHub: the bot puts the code review's run card up on PR #260 and both cards must
    show Code review running; then the bot edits that same comment into the approving record, and both cards must
    show Code review passed, never running. A card left on running after the record turns it red."""
    record_property("proves", "438.1")
    hub = Hub(tmp_path)
    s = hub.load()
    s["issues"][str(N)]["comments"] = [c for c in s["issues"][str(N)]["comments"]
                                       if not ('"role": "reviewer"' in c["body"] and '"stage": "pr"' in c["body"])]
    live = agent.live_card("reviewer", "pr", "queued")
    s["prs"][str(P)]["comments"].append({"login": BOT, "body": live, "at": "2026-10-09T05:00:00Z"})
    hub.save()
    play_change(hub, "the bot puts up the code review's run card", pr_comment(N, P, who="bot", text=live), "438.1")
    for where, text in ((f"issue #{N}", hub.issue_body(N)), (f"PR #{P}", hub.pr_body(P))):
        got = card_player.done_of(text).get("Code review")
        assert got == "running", f"438.1: with the code review's run card up, {where}'s card shows Code review {got!r}"
    s = hub.load()
    card_comment = next(c for c in s["prs"][str(P)]["comments"] if c["body"] == live)
    card_comment["body"] = record(review_record("pr"), card_comment["at"])["body"]
    hub.save()
    play_change(hub, "the bot edits the run card into the code review's record",
                pr_comment(N, P, who="bot", action="edited", text=card_comment["body"]), "438.1")
    for where, text in ((f"issue #{N}", hub.issue_body(N)), (f"PR #{P}", hub.pr_body(P))):
        got = card_player.done_of(text).get("Code review")
        assert got == "passed", (f"438.1: the code review's record is posted, but {where}'s card shows Code review "
                                 f"{got!r}, not passed")


# --- 438.2: only card.yml's run writes the card ------------------------------------------------------------------

def test_approving_a_plan_saves_no_card_and_card_yml_then_shows_its_links_on_every_card(tmp_path, record_property):
    """Approving a plan saves no card; card.yml's redraw then shows its links on every card.

    Proves 438.2.
    Runs the plan approval (`python3 -m dokima.agent next` on an approving plan review) on the fake GitHub of
    tests/test_plan_links_recorded.py, for a plan that says #252 is blocked by #301, blocks #302 and relates to #303.
    The approval must still record the blocking links on GitHub, and must write no issue body at all. Then card.yml's
    own redraw of #252 (`python3 dokima/card.py`, as on the record's comment) must leave #252's card showing all three
    links and #301, #302 and #303 each showing its link from its own side, with every owner's ask kept."""
    record_property("proves", "438.2")
    import test_plan_links_recorded as tl
    hub = tl.Hub(tmp_path)
    hub.post(tl.plan(tl.links([301], [302], [303])))
    rec = tl.review("approve")
    hub.next(rec)
    saved = sorted({w["issue"] for w in hub.writes("body")})
    assert not saved, f"438.2: the plan approval saved the card of {', '.join(f'#{n}' for n in saved)} itself"
    assert hub.blocked_by(tl.N) == [301] and hub.blocked_by(302) == [tl.N], \
        f"438.2: the plan approval no longer records its blocking links: {hub.load()['deps']}"
    hub.post(rec)
    hub.redraw(tl.N)
    assert hub.card_links(tl.N) == {"blocked_by": {301}, "blocks": {302}, "relates_to": {303}}, \
        f"438.2: after card.yml's redraw, #{tl.N}'s card does not show its links: {hub.card_links(tl.N)}"
    expected = {301: {"blocked_by": set(), "blocks": {tl.N}, "relates_to": set()},
                302: {"blocked_by": {tl.N}, "blocks": set(), "relates_to": set()},
                303: {"blocked_by": set(), "blocks": set(), "relates_to": {tl.N}}}
    for n, want in expected.items():
        assert hub.card_links(n) == want, \
            f"438.2: after card.yml's redraw of #{tl.N}, #{n}'s card should show {want}, shows {hub.card_links(n)}"
        assert body.ask(hub.body(n)) == hub.asks[n], f"438.2: the owner's ask on #{n} changed"


def test_the_planner_saves_no_card_of_its_own(record_property, monkeypatch, tmp_path):
    """The planner saves no card of its own; it still says it planned.

    Proves 438.2.
    Runs the old planner's post (`dokima/planner.py`, as planner.yml does) for a good plan on an issue that already
    has a card, against tests/test_body.py's fake GitHub. It must save no issue body, and must still finish without
    error and post its comment on the issue, so the post did run."""
    record_property("proves", "438.2")
    import test_body as tb
    from dokima import card, planner
    fake = tb.FakeGitHub()
    monkeypatch.setenv("REPO", tb.REPO)
    monkeypatch.setattr(body, "gh", fake)
    monkeypatch.setattr(card, "gh", fake)
    monkeypatch.setattr(planner, "gh", fake)
    current = body.redraw("My ask.", tb.PLAN_TOP)
    raised = tb.run_planner_post(monkeypatch, tmp_path, fake, current)
    assert raised is None, f"438.2: the planner's post failed on a good plan: {raised!r}"
    assert fake.saves == [], f"438.2: the planner saved a card of its own above the marker: {fake.saves[0][:300]!r}"
    assert fake.comments, "438.2: the planner's post said nothing on the issue, so it did not run"


# --- 438.3: the play-through passes every step on this story's code ----------------------------------------------

class Played:
    """The play-through's steps, played on the fake GitHub as dokima/playthrough.py plays them on the sandbox."""

    def __init__(self, hub, n=500, p=501):
        self.hub, self.n, self.p, self.k = hub, n, p, 0
        s = hub.load()
        s["issues"][str(n)] = {"title": f"Issue {n}", "state": "open", "labels": [], "updated_at": self.at(),
                               "body": f"The play-through's issue {n}.", "comments": []}
        hub.save()
        self.worker_card = self.review_card = None

    def at(self):
        """A later time for each thing posted."""
        self.k += 1
        return f"2026-10-10T{10 + self.k // 60:02d}:{self.k % 60:02d}:00Z"

    def post(self, text, on_pr=False):
        """The bot posts a comment on the issue or its PR; the event."""
        s = self.hub.load()
        holder = s["prs"][str(self.p)] if on_pr else s["issues"][str(self.n)]
        holder.setdefault("comments", []).append({"login": BOT, "body": text, "at": self.at()})
        self.hub.save()
        return pr_comment(self.n, self.p, who="bot", text=text) if on_pr else issue_comment(self.n, who="bot", text=text)

    def edit(self, old, new, on_pr=False):
        """The bot edits one of its comments; returns the event GitHub sends."""
        s = self.hub.load()
        holder = s["prs"][str(self.p)] if on_pr else s["issues"][str(self.n)]
        c = next(c for c in holder["comments"] if c["body"] == old)
        c["body"] = new
        self.hub.save()
        if on_pr:
            return pr_comment(self.n, self.p, who="bot", action="edited", text=new)
        return issue_comment(self.n, who="bot", action="edited", text=new)

    def open_pr(self):
        """The worker's pull request appears, every check on its head green; returns the event."""
        s = self.hub.load()
        sha = f"sha{self.p}"
        s["prs"][str(self.p)] = {"title": f"Issue {self.n}", "state": "open", "merged": False, "merged_by": None,
                                 "head_ref": f"try/issue-{self.n}", "sha": sha, "closes": self.n,
                                 "body": f"Closes https://github.com/o/r/issues/{self.n}", "comments": [],
                                 "reviews": [], "updated_at": self.at()}
        s["checks"][sha] = [{"name": f"{self.n}.1 · Criterion one", "status": "completed", "conclusion": "success",
                             "head_sha": sha, "html_url": f"https://github.com/o/r/runs/{self.p}1"},
                            {"name": "all tests", "status": "completed", "conclusion": "success", "head_sha": sha,
                             "html_url": f"https://github.com/o/r/runs/{self.p}2"}]
        self.hub.save()
        return pr_event(self.n, self.p, "opened")

    def do(self, step):
        """Play one step; returns the events GitHub sends for it, in order."""
        n, p = self.n, self.p
        if step == "issue opened":
            return [issue_event(n, "opened")]
        if step == "plan posted":
            return [self.post(record(plan_record(n, f"The owner sees issue {n} done."), "")["body"])]
        if step == "plan approved":
            return [self.post(record(review_record("plan"), "")["body"])]
        if step == "build started":
            self.worker_card = agent.live_card("worker", "", "working")
            return [self.post("Autopilot: plan approved, starting work"), self.post(self.worker_card)]
        if step == "pull request opened":
            return [self.open_pr(), self.edit(self.worker_card, record(worker_record(), "")["body"])]
        if step == "code review started":
            self.review_card = agent.live_card("reviewer", "pr", "queued")
            return [self.post(self.review_card, on_pr=True)]
        if step == "code review record posted":
            return [self.edit(self.review_card, record(review_record("pr"), "")["body"], on_pr=True)]
        if step == "merged":
            self.hub.merge(n, p, by=BOT)
            return [pr_event(n, p, "closed", who="bot", merged=True)]
        raise AssertionError(f"test setup: no such step {step!r}")


def test_the_play_through_passes_every_step_from_a_new_issue_to_a_merge(tmp_path, record_property):
    """The play-through passes every step from a new issue to a merge.

    Proves 438.3.
    Plays every step of dokima/playthrough.py's STEPS on the fake GitHub as the play-through plays them on the
    sandbox: the issue opened, the planner's record, the plan review's record, the Autopilot line and the worker's run
    card, the pull request opened and the worker's card edited into its record, the code review's run card, its edit
    into the approving record, and the merge. Each event GitHub would send goes through card.yml, and after each step
    the play-through's own judge() must say `PASS: <step>`, including the moment the build started and the moment the
    code review's record is posted, when both cards must show Code review passed. Every FAIL line is reported."""
    record_property("proves", "438.3")
    p = playthrough("438.3")
    hub = Hub(tmp_path)
    played = Played(hub)
    lines = []
    for step in p.STEPS:
        for event in played.do(step):
            if reaches_card(*event):
                r = hub.run(*event, "438.3")
                assert not r.failed(), f"438.3: card.yml's run at {step!r} failed:\n{r.log[-3000:]}"
        issue_text = hub.issue_body(played.n)
        pr_text = hub.load()["prs"].get(str(played.p), {}).get("body")
        lines.append(p.judge(step, issue_text, pr_text))
    failed = [l for l in lines if not l.startswith("PASS: ")]
    assert not failed, "438.3: the play-through does not pass every step:\n" + "\n".join(lines)
    assert [l[len("PASS: "):] for l in lines] == list(p.STEPS), f"438.3: not every step was judged: {lines}"


# --- 438.4 and 438.5: the play-through as a check on every pull request ------------------------------------------

def playthrough_yml(k):
    """playthrough.yml as nested dicts; fails naming criterion k when it is missing."""
    assert os.path.exists(PLAYTHROUGH_YML), f"{k}: .github/workflows/playthrough.yml does not exist"
    return load_yaml(open(PLAYTHROUGH_YML).read())


def pr_target_event(action="opened"):
    """A pull_request_target event for PR #7, head headsha7, base basesha7."""
    pr = {"number": 7, "title": "A change", "state": "open", "merged": False,
          "head": {"ref": "try/issue-6", "sha": "headsha7"}, "base": {"ref": "main", "sha": "basesha7"},
          "user": {"login": BOT + "[bot]", "type": "Bot"}}
    return "pull_request_target", {"action": action, "number": 7, "pull_request": pr, "sender": sender("bot"),
                                   "repository": dict(REPOSITORY, full_name="dokima-dev/dokima")}


def merge_group_event():
    """A merge_group event: the queued commit queuesha8 on base basesha8."""
    return "merge_group", {"action": "checks_requested",
                           "merge_group": {"head_sha": "queuesha8", "head_ref": "gh-readonly-queue/main/pr-7-x",
                                           "base_sha": "basesha8", "base_ref": "refs/heads/main"},
                           "sender": sender("bot"), "repository": dict(REPOSITORY, full_name="dokima-dev/dokima")}


def dispatch_event(commit="abc1234"):
    """The Run workflow button with commit `commit`."""
    return "workflow_dispatch", {"inputs": {"commit": commit}, "sender": sender(OWNER),
                                 "repository": dict(REPOSITORY, full_name="dokima-dev/dokima")}


def ctx_for(event_name, event):
    """The expression context GitHub gives playthrough.yml for one event."""
    g = card_player.github_ctx(event_name, event)
    inputs = card_player.wrap(event.get("inputs") or {})
    return {"github": g, "vars": Ctx(), "secrets": Ctx(), "inputs": inputs, "env": Ctx(), "needs": Ctx(),
            "steps": Ctx(), "job": Ctx(status="success"), "matrix": Ctx()}


def jobs_for(wf, event_name, event, k):
    """The jobs of `wf` GitHub runs for this event, as [(check name, job)].

    Fails naming k when the workflow never starts on it."""
    assert github_starts(wf, event_name, event), \
        f"{k}: playthrough.yml does not start on {event_name} {event.get('action') or ''}".rstrip()
    ctx, out = ctx_for(event_name, event), []
    for key, job in (wf.get("jobs") or {}).items():
        if card_player.listed(job.get("needs")):
            continue
        if evaluate(condition(job.get("if")), ctx, {"failed": False}):
            out.append((fill(job.get("name") or key, ctx, {"failed": False}), job))
    return out


def play_step(job, ctx):
    """The step of `job` running the play-through, with its env filled in."""
    for step in job.get("steps") or []:
        if "dokima.playthrough" in str(step.get("run") or ""):
            env = {**(job.get("env") or {}), **(step.get("env") or {})}
            return step, {k: fill(v, ctx, {"failed": False}) for k, v in env.items()}
    raise AssertionError("no step runs python3 -m dokima.playthrough")


def played_checkout(job, ctx):
    """The checkout of the played commit (path `played`): its ref and fetch-depth, filled in."""
    for step in job.get("steps") or []:
        w = step.get("with") or {}
        if "actions/checkout" in str(step.get("uses") or "") and str(w.get("path") or "") == "played":
            return fill(w.get("ref") or "", ctx, {"failed": False}), fill(w.get("fetch-depth") or "1", ctx, {"failed": False})
    raise AssertionError("no checkout has path `played`")


def the_check(k):
    """The play-through's check on a pull request: (its name, its job).

    Fails naming k unless there is exactly one."""
    wf = playthrough_yml(k)
    found = jobs_for(wf, *pr_target_event(), k)
    assert len(found) == 1, (f"{k}: on a pull request playthrough.yml should run exactly one job, its one check, "
                             f"not {[name for name, _ in found]}")
    return found[0]


def test_every_pull_request_gets_the_play_through_as_one_check_on_its_head(record_property):
    """Every pull request gets the play-through as one check, played on its head.

    Proves 438.4.
    Reads .github/workflows/playthrough.yml with the workflow evaluator of tests/test_start.py. It must start on a
    pull request opened, pushed to and reopened (pull_request_target, so main's copy judges it) and still on the Run
    workflow button. On a pull request it runs exactly one job, the check; that job checks out the pull request's head
    commit as `played` with its whole history (fetch-depth 0), and runs `python3 -m dokima.playthrough` with
    PLAYED_COMMIT set to the head and PLAYED_BASE to the base, so the module can tell what the pull request changed.
    From the button, PLAYED_COMMIT is the commit given and PLAYED_BASE is empty, so it always plays."""
    record_property("proves", "438.4")
    wf = playthrough_yml("438.4")
    for action in ("opened", "synchronize", "reopened"):
        found = jobs_for(wf, *pr_target_event(action), "438.4")
        assert len(found) == 1, f"438.4: a pull request {action} runs {len(found)} play-through jobs, not one check"
    name, job = the_check("438.4")
    ctx = ctx_for(*pr_target_event())
    ref, depth = played_checkout(job, ctx)
    assert ref == "headsha7", f"438.4: the check plays {ref!r}, not the pull request's head commit headsha7"
    assert depth == "0", f"438.4: the played checkout has fetch-depth {depth!r}, not 0, so the base is not there"
    _, env = play_step(job, ctx)
    assert env.get("PLAYED_COMMIT") == "headsha7", f"438.4: PLAYED_COMMIT is {env.get('PLAYED_COMMIT')!r}, not the head"
    assert env.get("PLAYED_BASE") == "basesha7", f"438.4: PLAYED_BASE is {env.get('PLAYED_BASE')!r}, not the base"
    found = jobs_for(wf, *dispatch_event(), "438.4")
    assert found, "438.4: the Run workflow button no longer runs the play-through"
    _, env = play_step(found[0][1], ctx_for(*dispatch_event()))
    assert env.get("PLAYED_COMMIT") == "abc1234", f"438.4: from the button PLAYED_COMMIT is {env.get('PLAYED_COMMIT')!r}"
    assert not env.get("PLAYED_BASE"), f"438.4: from the button PLAYED_BASE is {env.get('PLAYED_BASE')!r}, not empty"


def git(cwd, *args):
    """Run git in `cwd` as a test user; its output."""
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()


def pull_request(tmp_path, files):
    """A temp git repo standing in for a pull request that changes `files`.

    Returns (folder, base sha, head sha)."""
    repo = tmp_path / "played"
    (repo / "dokima").mkdir(parents=True)
    (repo / "dokima" / "__init__.py").write_text("")
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")
    base = git(repo, "rev-parse", "HEAD")
    for f in files:
        path = repo / f
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"changed {f}\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "head")
    return str(repo), base, git(repo, "rev-parse", "HEAD")


def run_module(tmp_path, played, base, head):
    """Run the play-through module for a pull request, with no sandbox key.

    Returns (exit code, output, gh calls).

    gh is a stub that logs and fails, so a play that reaches GitHub shows in the calls."""
    stub = tmp_path / "bin"
    stub.mkdir(exist_ok=True)
    log = tmp_path / "gh-calls.txt"
    (stub / "gh").write_text(f"#!/bin/sh\necho \"$@\" >> {log}\nexit 1\n")
    (stub / "gh").chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k not in ("SANDBOX_TOKEN", "PLAYTHROUGH_WAIT")}
    env.update(PATH=f"{stub}{os.pathsep}{os.environ['PATH']}", REPO="dokima-dev/card-gallery", PLAYED=played,
               PLAYED_COMMIT=head, PLAYED_BASE=base, GH_TOKEN="fake", PYTHONPATH=ROOT)
    p = subprocess.run([sys.executable, "-m", "dokima.playthrough"], cwd=ROOT, env=env, capture_output=True,
                       text=True, timeout=60)
    return p.returncode, p.stdout + p.stderr, log.read_text() if log.exists() else ""


CARD_CODE = [".github/workflows/card.yml", ".github/workflows/board.yml", "dokima/card.py", "dokima/body.py",
             "dokima/board.py"]
OTHER_CODE = ["README.md", "dokima/agent.py", "dokima/cards.py", "tests/test_card.py", "tests/test_board.py",
              ".github/CODEOWNERS", "docs/dokima/card.py"]


def test_only_a_pull_request_changing_card_board_or_workflow_code_is_played(tmp_path, record_property):
    """Only card, board or workflow changes are played; others pass without playing.

    Proves 438.4.
    Runs `python3 -m dokima.playthrough` with PLAYED_BASE and PLAYED_COMMIT naming a temp git repo's base and head
    commits, with no sandbox key and a gh that fails. A pull request changing only other files (the README,
    dokima/agent.py, a near name like dokima/cards.py, tests, .github/CODEOWNERS, docs/dokima/card.py) must exit 0,
    say it passed without playing and call no gh. One changing any of .github/workflows/, dokima/card.py,
    dokima/body.py or dokima/board.py, beside other files, must try to play: with no sandbox key it fails at install,
    exit 1."""
    record_property("proves", "438.4")
    for k, f in enumerate(OTHER_CODE):
        played, base, head = pull_request(tmp_path / f"other{k}", [f])
        code, out, calls = run_module(tmp_path / f"other{k}", played, base, head)
        assert code == 0 and "without playing" in out, \
            f"438.4: a pull request changing only {f} should pass without playing, exit 0; it exited {code}: {out[-500:]}"
        assert not calls, f"438.4: a pull request changing only {f} still called GitHub: {calls}"
    for k, f in enumerate(CARD_CODE):
        played, base, head = pull_request(tmp_path / f"card{k}", ["README.md", f])
        code, out, _ = run_module(tmp_path / f"card{k}", played, base, head)
        assert code == 1 and "FAIL: install" in out and "without playing" not in out, \
            f"438.4: a pull request changing {f} should be played (and fail at install with no key); it exited {code}: {out[-500:]}"


def test_making_the_play_through_required_and_autopilot_waits_for_it(record_property, monkeypatch):
    """Autopilot waits for a green play-through, and the required setting is named.

    Proves 438.5.
    Reads the play-through's check name as GitHub shows it from playthrough.yml's one job on a pull request. The
    file's header must name the branch protection setting on main, `Require status checks to pass before merging`,
    and that check name in backticks. Then autopilot's merge (dokima/agent.py try_merge) runs on a fake GitHub for a
    pull request changing dokima/card.py with All tests green: with the play-through check failed, or still running,
    it must not merge and must name the check; with it passed, it must merge that head."""
    record_property("proves", "438.5")
    name, _ = the_check("438.5")
    header = "\n".join(l for l in open(PLAYTHROUGH_YML).read().splitlines() if l.startswith("#"))
    assert SETTING in header and "main" in header, \
        f"438.5: playthrough.yml's header does not name the setting {SETTING!r} on main:\n{header}"
    assert f"`{name}`" in header, f"438.5: playthrough.yml's header does not name the check `{name}` as GitHub shows it"
    for state, conclusion, merges in (("completed", "failure", False), ("in_progress", None, False),
                                      ("completed", "success", True)):
        calls = []

        def gh(*args, **kw):
            calls.append(args)
            a = " ".join(args)
            if "/files" in a:
                return json.dumps([{"filename": "dokima/card.py"}])
            if args[:2] == ("pr", "view"):
                return "headsha9\n"
            if "check-runs" in a:
                return json.dumps({"check_runs": [
                    {"name": "all tests", "status": "completed", "conclusion": "success"},
                    {"name": name, "status": state, "conclusion": conclusion}]})
            if "/status" in a:
                return json.dumps({"statuses": []})
            if args[:2] == ("pr", "merge"):
                return ""
            raise AssertionError(f"test setup: unexpected gh call {args}")

        monkeypatch.setattr(agent, "gh", gh)
        ok, why = agent.try_merge("o/r", "9")
        merged = any(c[:2] == ("pr", "merge") for c in calls)
        assert ok is merges and merged is merges, \
            f"438.5: with the play-through check {conclusion or state}, autopilot merged={merged}, said {why!r}"
        if not merges:
            assert name in why, f"438.5: autopilot did not merge but did not name the play-through check: {why!r}"


# --- 438.6: a redraw that finds both cards current writes nothing -------------------------------------------------

def test_the_bots_own_card_save_redraws_and_writes_nothing(tmp_path, record_property):
    """The bot's own card save starts a redraw that writes nothing, so the chain ends.

    Proves 438.6.
    After the owner's comment redraws issue #246 and PR #260, plays the events GitHub sends for the bot's own saves
    of those cards: the issue edited by the bot and the pull request edited by the bot. Each must start card.yml and
    run its card job (every change redraws), and must write no issue or PR body. Beside it, the same bot edit with
    both cards stale must write both, so the run is not simply doing nothing."""
    record_property("proves", "438.6")
    hub = Hub(tmp_path)
    play_change(hub, "the owner comments on the issue", issue_comment(N), "438.6")
    for what, event in (("the bot saves the issue's card", issue_event(N, "edited", who="bot")),
                        ("the bot saves the PR's card", pr_event(N, P, "edited"))):
        hub.clear_writes()
        assert reaches_card(*event), f"438.6: card.yml does not start when {what}"
        r = hub.run(*event, "438.6")
        assert r.started and r.card_ran() and not r.failed(), f"438.6: card.yml's card job did not run cleanly when {what}"
        wrote = [f"{w['op']} #{w['n']}" for w in hub.writes() if w["op"] in ("issue-body", "pr-body")]
        assert not wrote, f"438.6: when {what} with both cards current, the redraw wrote {wrote}, so it never ends"
    play_change(hub, "the bot saves the issue's card while both are stale", issue_event(N, "edited", who="bot"), "438.6")


# --- 438.7: every redraw runs main's copy -------------------------------------------------------------------------

def test_every_redraw_runs_mains_copy_of_card_yml_and_card_py(tmp_path, record_property):
    """Every redraw runs main's copy of card.yml and dokima/card.py, never a pull request's.

    Proves 438.7.
    For every change of 438.1, the card job that redraws must belong to a card.yml run started by an event GitHub runs
    from the default branch's copy (issues, issue_comment, pull_request_target, workflow_run, schedule), and every
    checkout in it must take the default branch, never the pull request's head or merge ref. A relay that runs from a
    pull request's own copy (for a review or a line note) must not run dokima/card.py itself."""
    record_property("proves", "438.7")
    hub = Hub(tmp_path)
    for what, event in every_change().items():
        if what == "the bot merges the pull request":
            hub.merge(N, P, by=BOT)
        r = play_change(hub, what, event, "438.7")
        assert r.event_name in MAINS_COPY, f"438.7: when {what}, card.yml ran on {r.event_name}, from the PR's own copy"
        bad = [c for c in r.checkouts if c not in ("", "refs/heads/main", "main")]
        assert not bad, f"438.7: when {what}, card.yml checked out {bad}, not main's copy"
        for relay in getattr(r, "relays", []):
            assert not relay.card_ran(), f"438.7: when {what}, a relay run from the PR's own copy ran dokima/card.py"


# --- 438.8: a card that cannot be redrawn fails its run, and the next change or the sweep redraws it ----------------

def test_a_card_that_cannot_be_redrawn_fails_naming_the_issue_and_the_next_change_or_sweep_redraws_it(tmp_path, record_property):
    """A card GitHub refuses fails its run naming the issue; a later redraw fixes it.

    Proves 438.8.
    GitHub refuses to save issue #246's body while the bot comments on it: card.yml must start, and its run must fail
    with an error line naming #246. GitHub then takes saves again, and the bot's next edit of its comment must redraw
    both cards. The same refusal once more, then the 15-minute sweep with GitHub answering, must redraw issue #246's
    card too."""
    record_property("proves", "438.8")
    hub = Hub(tmp_path)

    def refused_then(event, what):
        stale_again(hub)
        hub.refuse("write-issue", N)
        assert reaches_card(*event), f"438.8: card.yml does not start when {what}"
        r = hub.run(*event, "438.8")
        assert r.started and r.failed(), f"438.8: GitHub refused #{N}'s card when {what}, yet the run did not fail"
        assert any(f"#{N}" in e for e in r.errors()), f"438.8: the failed run does not name #{N}: {r.errors()}"
        s = hub.load()
        s["refuse"] = []
        hub.save()

    refused_then(issue_comment(N, who="bot", text="Autopilot: plan approved, starting work"), "the bot comments")
    play_change(hub, "the bot edits its comment next", issue_comment(N, who="bot", action="edited", text="A record."),
                "438.8")
    refused_then(issue_comment(N, who="bot", text="Another bot line."), "the bot comments again")
    r = hub.run(*schedule(), "438.8")
    assert not r.failed(), f"438.8: the sweep failed with GitHub answering:\n{r.log[-2000:]}"
    assert STALE_CARD not in hub.issue_body(N), f"438.8: the sweep left #{N}'s old card in place"


# --- 438.9: the check reports in the merge queue too --------------------------------------------------------------

def test_the_play_through_check_also_reports_in_the_merge_queue(record_property):
    """The play-through check also reports in the merge queue, on the queued commit.

    Proves 438.9.
    Reads playthrough.yml for a merge_group event: it must start, run the same one check (the same name as on a pull
    request), check out the queued commit as `played` with its whole history, and run `python3 -m dokima.playthrough`
    with PLAYED_COMMIT the queued commit and PLAYED_BASE the queue's base, so a required check never leaves a queued
    pull request waiting."""
    record_property("proves", "438.9")
    name, _ = the_check("438.9")
    wf = playthrough_yml("438.9")
    found = jobs_for(wf, *merge_group_event(), "438.9")
    assert [n for n, _ in found] == [name], \
        f"438.9: in the merge queue playthrough.yml runs {[n for n, _ in found]}, not the one check `{name}`"
    ctx = ctx_for(*merge_group_event())
    ref, depth = played_checkout(found[0][1], ctx)
    assert ref == "queuesha8" and depth == "0", \
        f"438.9: in the merge queue it plays {ref!r} with fetch-depth {depth!r}, not queuesha8 with 0"
    _, env = play_step(found[0][1], ctx)
    assert (env.get("PLAYED_COMMIT"), env.get("PLAYED_BASE")) == ("queuesha8", "basesha8"), \
        f"438.9: in the merge queue PLAYED_COMMIT/PLAYED_BASE are {env.get('PLAYED_COMMIT')!r}/{env.get('PLAYED_BASE')!r}"
