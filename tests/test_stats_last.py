"""Every run comment Dokima posts ends with its stats line, right below its Next line.

Issue #454, story 3 of #416; the owner's /plan comment of 2026-10-10T20:04:51Z: "In every run comment, the stats line
(tokens used and the like) is the very last line, below Next." Before it, `agent render` (dokima/agent.py) put the
stats in a Stats fold right above the Full record fold, and the Next line was added after the whole comment: by
`agent next` for agent runs (agent.py, after `render`), and by dokima/uptodate.py for a clash record.

These tests post each kind of run comment the way the workflows do: `agent render` writes comment.md, then
`agent next N OUT` adds the Next line, GitHub faked so nothing leaves the machine. A filed split is posted as
`render` draws it, and a clash record as dokima/uptodate.py posts it (faked as in tests/test_clash.py). Each comment
is then read the way the owner reads it, from the bottom up.
"""
import copy
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent, card  # noqa: E402
from test_run_comment_fields import BLOCK, META, PLAN, REPO, WORK, rec  # noqa: E402

RECORD_FOLD = "<details><summary>Full record</summary>"
STATS = ("Opus 5.5", "4.0 min", "23 turns", "401K", "18K", "$3.20")
LINKS = ("https://g/log.md", "https://github.com/o/r/actions/runs/1")
QUIET = {**BLOCK, "raises": [r for r in BLOCK["raises"] if r["kind"] != "issue"]}


@pytest.fixture
def post(tmp_path, monkeypatch):
    """Posts a record's comment as agent.yml does, and returns the body.

    `agent render` writes it, then `agent next` adds the Next line."""
    for k, v in {"GITHUB_REPOSITORY": REPO, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_RUN_ID": "1",
                 "OWNERS": "owner"}.items():
        monkeypatch.setenv(k, v)

    def gh(*args, **kw):
        if args[:2] == ("pr", "list"):
            return "7\n"
        return "[]"
    monkeypatch.setattr(agent, "gh", gh)
    monkeypatch.setattr(agent, "conversation", lambda repo, number: ({}, []))
    monkeypatch.setattr(agent, "on_autopilot", lambda repo, number: False)
    count = [0]

    def run(r):
        count[0] += 1
        out = tmp_path / f"out{count[0]}"
        out.mkdir()
        (out / "record.json").write_text(json.dumps(r))
        (out / "comment.md").write_text(agent.render(r))
        agent.main(["agent", "next", "77", str(out)])
        return (out / "comment.md").read_text()
    return run


def lines_of(body):
    """The comment's lines that show something, in order."""
    return [l for l in body.splitlines() if l.strip()]


def is_stats(line):
    """True when the line is a stats line, opening with the stats icon."""
    return re.sub(r"^\s*<sub>\s*", "", line).startswith(card.field_icon(REPO, "stats"))


def assert_stats_last(k, what, body, next_above=True):
    """Fail naming k unless the comment ends with one full stats line.

    The stats line holds every stat and link, with the Next line right above it (when `next_above`), no Stats
    fold, and the Full record still the last fold."""
    lines = lines_of(body)
    last = lines[-1] if lines else ""
    assert is_stats(last), f"{k} ({what}): the comment's last line is not its stats line: {last!r}\n{body[-900:]}"
    for said in STATS + LINKS:
        assert said in last, f"{k} ({what}): the stats line does not hold {said!r}: {last!r}"
    assert sum(1 for l in lines if is_stats(l)) == 1, f"{k} ({what}): the stats show on more than one line:\n{body}"
    assert not re.search(r"<summary>[^<]*(<img[^>]*>)?\s*Stats\s*</summary>", body), \
        f"{k} ({what}): the stats are still in a Stats fold:\n{body}"
    if next_above:
        assert len(lines) > 1 and lines[-2].startswith("**Next:**"), \
            f"{k} ({what}): the line right above the stats line is not the Next line: {lines[-2:]!r}"
    assert RECORD_FOLD in body, f"{k} ({what}): the comment lost its Full record fold"
    after = body.partition(RECORD_FOLD)[2].partition("</details>")[2]
    assert "<details" not in after, f"{k} ({what}): a fold follows the Full record fold:\n{after}"


def test_every_agent_run_comment_ends_with_its_stats_line_below_next(record_property, post):
    """In every agent run's comment, the stats line is last, right below Next.

    Proves 454.2.

    Posts the comments of a planner, a worker, a blocking plan review, a blocking code review, a rejected plan and a
    run cancelled after its agent started, as the workflow posts them, and checks each ends with one stats line (the
    stats icon, model, time, turns, tokens, cost, conversation and run links) right below its Next line, with no
    Stats fold left, and still reads back as the same record."""
    record_property("proves", "454.2")
    cases = [("planner", rec("planner", "", PLAN)), ("worker", rec("worker", "", WORK)),
             ("plan review", rec("reviewer", "plan", QUIET)), ("code review", rec("reviewer", "pr", QUIET)),
             ("rejected plan", rec("planner", "", PLAN, passed=False, problems=["a problem"])),
             ("cancelled while working", agent.cancelled("worker", "", True, copy.deepcopy(META)))]
    for what, r in cases:
        body = post(r)
        assert_stats_last("454.2", what, body)
        back = agent.records([{"author": {"login": agent.BOT}, "body": body, "createdAt": "2026-10-10T10:00:00Z"}])
        assert back == [r], f"454.2 ({what}): the posted comment no longer reads back as its record: {back}"


def test_runs_with_no_model_end_with_their_stats_line_too(record_property, post, monkeypatch):
    """Runs no model worked in end with their own stats line too.

    Proves 454.2.

    Posts a run that stopped before its agent started and one cancelled before it, and checks each ends with its
    line saying no agent ran, linking the run, right below Next. Then draws a filed split, which says no model ran
    and links its run on its last line, and posts a clash record as dokima/uptodate.py does, whose last line, below
    its Next line, says code found it and links the run."""
    record_property("proves", "454.2")
    run = "https://github.com/o/r/actions/runs/1"
    for what, r in (("never started", agent.not_started("worker", "", "main is red", copy.deepcopy(META))),
                    ("cancelled before it started", agent.cancelled("worker", "", False, copy.deepcopy(META)))):
        lines = lines_of(post(r))
        assert "No agent ran" in lines[-1] and run in lines[-1], \
            f"454.2 ({what}): the last line does not say no agent ran with the run's link: {lines[-1]!r}"
        assert lines[-2].startswith("**Next:**"), f"454.2 ({what}): the Next line is not right above the last line: {lines[-2:]!r}"
    split = {"role": "split", "stage": None, "run": run, "check": {"passed": True, "problems": []},
             "handback": {"stories": [{"story": 1, "issue": 201, "title": "First", "blocked_by": []}]}}
    last = lines_of(agent.render(split))[-1]
    assert is_stats(last) and "no model" in last.lower() and run in last, \
        f"454.2 (split): a filed split's last line is not its stats line saying no model ran: {last!r}"
    import test_clash as tc
    gh = tc.FakeGitHub(merged=(300,))
    monkeypatch.setenv("GITHUB_RUN_ID", "1")
    tc.clash(gh, tc.pr(70, "try/issue-7"))
    posted = [b for n, b in gh.posted() if n == 7]
    assert len(posted) == 1, f"454.2 (clash): expected one clash record on issue #7, got {gh.posted()}"
    lines = lines_of(posted[0])
    assert "Found by code" in lines[-1] and "actions/runs/1" in lines[-1], \
        f"454.2 (clash): the clash record's last line is not its stats line: {lines[-1]!r}"
    assert lines[-2].startswith("**Next:**"), f"454.2 (clash): the Next line is not right above the stats line: {lines[-2:]!r}"


def test_agents_md_says_the_stats_line_is_last_below_next(record_property):
    """AGENTS.md says a run comment's stats line is its last line, below Next.

    Proves 454.2.

    Reads the Agent records and cards section and checks it no longer describes a Stats fold, and that it names the
    stats line as the last line, below the Next line."""
    record_property("proves", "454.2")
    text = open(os.path.join(os.path.dirname(__file__), "..", "AGENTS.md")).read()
    section = text.split("## Agent records and cards", 1)[1].split("\n## ", 1)[0]
    assert "a Stats fold" not in section, "454.2: AGENTS.md still describes a Stats fold in run comments"
    assert re.search(r"stats line[^.]*last[^.]*below[^.]*Next|stats line[^.]*below[^.]*Next[^.]*last", section, re.I), \
        f"454.2: AGENTS.md does not say the stats line is the last line, below Next:\n{section}"
