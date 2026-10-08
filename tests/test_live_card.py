"""Each agent run has one live card that turns from working into its result (#185).

These tests run the agent workflow (.github/workflows/agent.yml) the way GitHub runs it, with the machine from
test_start.py: a fake GitHub that keeps every comment the run writes and every version of it, a fake Claude Code that
notes what GitHub showed the moment it started, and nothing leaving the machine. Each scenario runs once per module
and the tests read what it left behind: which comments exist, what each said at each moment, and which key made each
call.
"""
import calendar
import json
import os
import re
import time

import pytest

import test_start as ts
from test_start import N, OWNER, PR, PIP_BROKEN, STORY_APPROVED, STORY_PLANNED, Run

from dokima import agent

ROOT = ts.ROOT
ICON = re.compile(r'<img[^>]*src="https://raw\.githubusercontent\.com/[^/"]+/[^/"]+/main/dokima/icons/([A-Za-z0-9_-]+)\.svg"')
TIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?(?:\.\d+)?\s*(?:UTC|Z)(?!\w)")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‼⁉ℹ⌚-⏿Ⓜ"
                   "▪-◾〰〽㊗㊙]")
SHORTCODE = re.compile(r"(?<![\w/]):[a-z_+-][a-z0-9_+-]*:(?![\w/])")
NEXT_STEP_FIX = "Fix the cause, then give the command again."
BAD_REVIEW = {"verdict": "maybe"}


class Scenario:
    """One finished run of the agent workflow, with the time just before it started."""

    def __init__(self, tmp, *args, **kw):
        self.t0 = time.time()
        self.run = Run(tmp, *args, **kw)
        gh = os.path.join(self.run.tmp, "gh")
        p = os.path.join(gh, "at-agent-start.json")
        self.at_start = json.load(open(p)) if os.path.exists(p) else None
        p = os.path.join(gh, "agent-env.json")
        self.agent_env = json.load(open(p)) if os.path.exists(p) else None
        p = os.path.join(gh, "agent-started-at")
        self.agent_at = float(open(p).read()) if os.path.exists(p) else None
        p = os.path.join(gh, "calls-meta.jsonl")
        self.meta = [json.loads(l) for l in open(p)] if os.path.exists(p) else []
        self.comments = self.run.comments()

    def tail(self):
        """The run's own log, for a failure message."""
        return self.run.tail()


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    """Every scenario these tests read, each run once through the whole agent workflow."""
    t = tmp_path_factory.mktemp("live")
    return {
        "pass": Scenario(t / "pass", "reviewer", "plan", STORY_PLANNED, try_branch=True),
        "fail": Scenario(t / "fail", "reviewer", "plan", STORY_PLANNED, try_branch=True, review=BAD_REVIEW),
        "pr": Scenario(t / "pr", "worker", "", STORY_APPROVED, try_branch=True, options={"pr_open": True}),
        "branch": Scenario(t / "branch", "worker", "", STORY_APPROVED),
        "pack": Scenario(t / "pack", "worker", "", STORY_PLANNED, try_branch=True),
        "install": Scenario(t / "install", "worker", "", STORY_APPROVED, try_branch=True, broken={"pip": PIP_BROKEN}),
        "gate": Scenario(t / "gate", "worker", "", STORY_APPROVED, try_branch=True, actor="stranger"),
        "no-edit": Scenario(t / "no-edit", "reviewer", "plan", STORY_PLANNED, try_branch=True, options={"fail_edits": True}),
        "no-card": Scenario(t / "no-card", "reviewer", "plan", STORY_PLANNED, try_branch=True, options={"fail_card": True}),
    }


def as_comment(body):
    """A body as a comment the bot posted, the way records() and is_record() read comments."""
    return {"author": {"login": agent.BOT}, "body": body, "createdAt": "2026-10-08T00:00:00Z"}


def recs_of(body):
    """The records a body holds when the bot posted it."""
    return agent.records([as_comment(body)])


def icons(body):
    """The names of Dokima's icons a body shows, in order."""
    return ICON.findall(body)


def visible(body):
    """A body without its folded JSON record: the part the owner reads."""
    return re.sub(r"```json\n.*?\n```", "", body, flags=re.S)


def is_edit(args):
    """True when a gh call edits a comment."""
    method = next((args[i + 1] for i, x in enumerate(args[:-1]) if x in ("-X", "--method")), "").upper()
    return "--edit-last" in args or (args[:1] == ["api"] and method in ("PATCH", "POST")
                                     and any(re.fullmatch(r"/?repos/o/r/issues/comments/\d+", x) for x in args))


def is_new_comment(args):
    """True when a gh call posts a new comment."""
    return (args[:2] in (["issue", "comment"], ["pr", "comment"]) and "--edit-last" not in args) or \
        (args[:1] == ["api"] and any(re.fullmatch(r"/?repos/o/r/issues/\d+/comments", x) for x in args)
         and any(x.startswith("body=") for x in args) or "--input" in args)


def where(c):
    """Where a fake GitHub comment is, in words."""
    return f"{'PR' if c['kind'] == 'pr' else 'issue'} #{c['number']}"


def working_card(s, crit, kind="issue", number=N):
    """The one comment GitHub showed when the agent started, checked to be the run's card in the right place."""
    assert s.run.agent_started(), f"{crit}: setup: the agent never started; the run stopped at '{s.run.failed_step}':\n{s.tail()}"
    cards = s.at_start or []
    assert len(cards) == 1, (f"{crit}: when the agent started, the run had {len(cards)} comments on GitHub, expected its one "
                             f"card: {[(where(c), c['versions'][-1][:200]) for c in cards]}\n{s.tail()}")
    c = cards[0]
    assert (c["kind"], str(c["number"])) == (kind, str(number)), \
        f"{crit}: the card is on {where(c)}, expected {kind} #{number}"
    return c


def test_the_card_says_working_with_its_start_time_when_the_agent_starts(record_property, runs):
    """When the agent starts, its card on the issue says working, with the running icon and the time it started.

    Runs a plan review and reads what GitHub showed the moment the fake agent started: exactly one comment for the run,
    on issue #57, that says working, shows the running icon and gives a UTC time no earlier than the minute the run
    began and no later than the agent's start. A worker run whose issue already has open pull request #60 must show
    the same working card on the pull request instead."""
    record_property("proves", "185.1")
    s = runs["pass"]
    c = working_card(s, "185.1")
    body = c["versions"][-1]
    assert "working" in body.lower(), f"185.1: the card does not say working when the agent starts:\n{body[:800]}"
    assert "running" in icons(body), f"185.1: the working card does not show the running icon, it shows {icons(body)}:\n{body[:800]}"
    m = TIME.search(visible(body))
    assert m, f"185.1: the working card gives no start time in UTC (like 2026-10-08 05:03 UTC):\n{body[:800]}"
    y, mo, d, h, mi, sec = (int(x or 0) for x in m.groups())
    started = calendar.timegm((y, mo, d, h, mi, sec))
    assert s.t0 // 60 * 60 <= started <= s.agent_at + 1, \
        (f"185.1: the card's start time {m.group(0)} is not when the run started: the run began at "
         f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s.t0))} UTC and the agent at "
         f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s.agent_at))} UTC")

    s = runs["pr"]
    c = working_card(s, "185.1", "pr", PR)
    body = c["versions"][-1]
    assert "working" in body.lower() and "running" in icons(body), \
        f"185.1: the card on pull request #60 does not say working with the running icon:\n{body[:800]}"


def test_the_same_comment_becomes_the_result_and_is_the_runs_only_comment(record_property, runs):
    """At the end of the run its card, edited in place, becomes its record: done, or failed with why.

    A plan review that passes, one whose hand-back code rejects, and a worker run on an issue with an open pull request
    each leave exactly one comment: the very comment that said working when the agent started, now edited (not a new
    one), posted by Dokima's bot, holding exactly the run's own record and its Next line. The passed run shows the
    passed icon; the rejected run shows the failed icon and lists the check's problems; neither still shows the
    running icon."""
    record_property("proves", "185.2")
    for name, kind, number, role, passed in (("pass", "issue", N, "reviewer", True), ("fail", "issue", N, "reviewer", False),
                                              ("pr", "pr", PR, "worker", False)):
        s = runs[name]
        card = working_card(s, f"185.2 ({name})", kind, number)
        cs = s.comments
        assert len(cs) == 1, (f"185.2 ({name}): the run left {len(cs)} comments, expected exactly one: "
                              f"{[(where(c), c['versions'][-1][:150]) for c in cs]}")
        c = cs[0]
        assert c["id"] == card["id"], f"185.2 ({name}): the result is a new comment, not the working card edited in place"
        assert len(c["versions"]) > len(card["versions"]), f"185.2 ({name}): the working card was never edited into the result"
        assert c["author"] == agent.BOT, f"185.2 ({name}): the run's comment was posted by {c['author']}, not Dokima's bot"
        final = c["versions"][-1]
        recs = recs_of(final)
        assert len(recs) == 1, f"185.2 ({name}): the final comment does not hold exactly one record:\n{final[:800]}"
        assert (recs[0]["role"], recs[0]["check"]["passed"]) == (role, passed), \
            f"185.2 ({name}): the final comment holds the wrong record: {recs[0]['role']}, passed={recs[0]['check']['passed']}"
        assert "**Next:**" in final, f"185.2 ({name}): the result has no Next line:\n{final[-600:]}"
        shown = icons(final)
        assert "running" not in shown, f"185.2 ({name}): the result still shows the running icon: {shown}"
        if passed:
            assert "passed" in shown and "failed" not in shown, f"185.2 ({name}): a done run does not show the passed icon: {shown}"
        else:
            assert "failed" in shown and "passed" not in shown, f"185.2 ({name}): a failed run does not show the failed icon: {shown}"
            problems = recs[0]["check"]["problems"]
            assert problems and problems[0] in visible(final), \
                f"185.2 ({name}): the failed result does not say why (the check's problems):\n{final[:800]}"


def test_a_run_that_stops_before_its_agent_edits_its_card_into_why_and_what_to_do(record_property, runs):
    """A run that stops before its agent starts turns its card into why it stopped and what the owner can do.

    Three runs stop after their card is up: a worker with no try branch, a worker whose plan nobody approved, and a
    worker whose tools fail to install. Each leaves exactly one comment, first a card that is not yet a record, then
    that same comment edited into the run's failed record naming its reason and saying what to do. A run that a
    stranger starts stops before anything else and still leaves exactly one comment saying why."""
    record_property("proves", "185.3")
    for name, reason in (("branch", f"try/issue-{N}"), ("pack", "no passed plan"), ("install", "Install pytest and Claude Code"),
                         ("gate", "not a code owner")):
        s = runs[name]
        assert not s.run.agent_started(), f"185.3 ({name}): setup: the agent started though the run should stop before it"
        cs = s.comments
        assert len(cs) == 1, (f"185.3 ({name}): the run that stopped before its agent left {len(cs)} comments, expected one: "
                              f"{[(where(c), c['versions'][-1][:150]) for c in cs]}\n{s.tail()}")
        c = cs[0]
        if name != "gate":
            assert len(c["versions"]) >= 2 and not recs_of(c["versions"][0]) and icons(c["versions"][0]), \
                (f"185.3 ({name}): no card was up before the run stopped, so none was updated; the comment's first "
                 f"version was:\n{c['versions'][0][:600]}")
        final = c["versions"][-1]
        recs = recs_of(final)
        assert len(recs) == 1 and recs[0]["role"] == "not-started", \
            f"185.3 ({name}): the card did not become the run's not-started record:\n{final[:800]}"
        assert reason.lower() in visible(final).lower(), f"185.3 ({name}): the card does not say why ({reason!r}):\n{final[:800]}"
        assert NEXT_STEP_FIX in final, f"185.3 ({name}): the card does not say what the owner can do:\n{final[-600:]}"
        assert "failed" in icons(final), f"185.3 ({name}): the stopped run's card does not show the failed icon: {icons(final)}"


def test_every_state_of_the_card_shows_one_of_dokimas_own_icons_and_no_emoji(record_property, runs):
    """Every version of every card shows an icon from dokima/icons/, and nothing anywhere adds an emoji or a reaction.

    Reads every version of every comment from all the runs (working, done, failed, stopped before the agent): each
    shows at least one icon, every icon it shows is a file in dokima/icons/, and the part the owner reads holds no
    emoji character and no :shortcode:. No run asks GitHub for a reaction."""
    record_property("proves", "185.4")
    own = {f[:-4] for f in os.listdir(os.path.join(ROOT, "dokima", "icons")) if f.endswith(".svg")}
    seen = 0
    for name in ("pass", "fail", "pr", "branch", "pack", "install", "gate"):
        s = runs[name]
        for c in s.comments:
            for i, body in enumerate(c["versions"]):
                seen += 1
                shown = icons(body)
                assert shown, f"185.4 ({name}): version {i + 1} of the card shows no icon from dokima/icons/:\n{body[:600]}"
                assert set(shown) <= own, f"185.4 ({name}): the card shows icons not in dokima/icons/: {sorted(set(shown) - own)}"
                text = visible(body)
                assert not EMOJI.search(text) and not SHORTCODE.search(text), \
                    f"185.4 ({name}): the card holds an emoji: {EMOJI.findall(text) + SHORTCODE.findall(text)}"
        reactions = [m["args"] for m in s.meta if any("reactions" in str(x) for x in m["args"])]
        assert not reactions, f"185.4 ({name}): the run added a reaction: {reactions}"
    assert seen >= 10, f"185.4: setup: only {seen} card versions were written, too few to check every state"


def test_a_card_still_running_is_never_read_as_a_record(record_property, runs):
    """Packs, the river and approvals see only finished results: a card still running never reads as a record.

    Every version of every card before its last (the card before the agent and the working card) must not read as a
    record, posted by the bot or not, while the last version of each reads as exactly one. The pack the agent of a
    plan review got holds only the one earlier record of the issue, not its own card."""
    record_property("proves", "185.5")
    earlier = 0
    for name in ("pass", "fail", "pr", "branch", "pack", "install"):
        for c in runs[name].comments:
            for body in c["versions"][:-1]:
                earlier += 1
                assert recs_of(body) == [] and not agent.is_record(as_comment(body)), \
                    f"185.5 ({name}): a card still running reads as a record:\n{body[:600]}"
            assert len(recs_of(c["versions"][-1])) == 1, f"185.5 ({name}): the finished card does not read as one record"
    assert earlier >= 6, f"185.5: only {earlier} versions of a card were written before its result: the runs put up no live card"
    s = runs["pass"]
    pack_in = os.path.join(s.run.env.get("PACK", ""), "in")
    got = sorted(os.listdir(pack_in)) if os.path.isdir(pack_in) else None
    assert got is not None and len(got) == 1, f"185.5: the plan review's pack should hold the issue's one earlier record, got {got}"
    assert json.load(open(os.path.join(pack_in, got[0])))["role"] == "planner", "185.5: the pack's record is not the planner's"


def test_a_card_that_cannot_be_posted_or_edited_never_loses_the_result(record_property, runs):
    """If the card cannot be posted or edited, the run still goes on and posts its result as a record.

    Runs a plan review twice: once with GitHub refusing every edit of a comment, and once with GitHub refusing every
    new comment until the agent has started. Both times the agent still runs and, among the comments the run leaves,
    Dokima's bot posted exactly one record: the review's passed record."""
    record_property("proves", "185.6")
    for name in ("no-edit", "no-card"):
        s = runs[name]
        tried = [m["args"] for m in s.meta if is_edit(m["args"])] if name == "no-edit" else \
            [m["args"] for m in s.meta if not m["agent_started"] and is_new_comment(m["args"])]
        assert tried, f"185.6 ({name}): the run never tried to {'edit' if name == 'no-edit' else 'put up'} a live card, so there is none"
        assert s.run.agent_started(), f"185.6 ({name}): the agent never started once the card failed; stopped at '{s.run.failed_step}':\n{s.tail()}"
        recs = [r for c in s.comments if c["author"] == agent.BOT for r in recs_of(c["versions"][-1])]
        assert [(r["role"], r["check"]["passed"]) for r in recs] == [("reviewer", True)], \
            f"185.6 ({name}): the run's result was not posted as exactly one record: {[(r['role'], r['check']['passed']) for r in recs]}\n{s.tail()}"


def test_no_bot_key_is_live_while_the_agent_works(record_property, runs):
    """The bot's key that put the card up is revoked before the agent starts, and the agent's environment holds none.

    Reads every call the plan review made to GitHub before its agent started: the card went up with Dokima's bot key,
    and the last call made with that key before the agent is the call that revokes it (DELETE installation/token). The
    fake agent's own environment holds no bot key. After the agent, the run still posts its result (185.2)."""
    record_property("proves", "185.7")
    s = runs["pass"]
    before = [m for m in s.meta if not m["agent_started"] and m["token"] == "fake-token"]
    assert before, "185.7: no call before the agent used Dokima's bot key: the bot never put up a live card"
    last = before[-1]["args"]
    method = next((last[i + 1] for i, x in enumerate(last[:-1]) if x in ("-X", "--method")), "").upper()
    assert last[:1] == ["api"] and method == "DELETE" and any(re.fullmatch(r"/?installation/token", x) for x in last), \
        f"185.7: the bot's key was still live when the agent started; its last call before the agent was {last}"
    leaked = sorted(k for k, v in (s.agent_env or {}).items() if "fake-token" in v and k != "GIT_CONFIG_VALUE_0")
    assert s.agent_env is not None and not leaked, f"185.7: the agent's environment holds the bot's key in {leaked}"
