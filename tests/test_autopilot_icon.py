"""Cards on autopilot show the autopilot icon and the word Autopilot on their status line.

Issue #454, story 3 of #416, folding in #394: `FIELD_ICONS` in dokima/card.py has had an `autopilot` icon
(dokima/icons/autopilot.svg) that no code drew; the status line showed the stage and Needs you only. Now, on an issue
on autopilot (its `autopilot` label) and on its pull request, the status line shows the autopilot icon and the word
Autopilot beside the stage, never while it shows Needs you, as on the board's pills; a card not on autopilot shows
neither.

The cards are drawn the way Dokima draws them, by dokima.card.draw and by the board scan's dokima.scan.card_now, against
tests/test_scan.py's fake GitHub (its World): issues with their labels, records, pull requests and checks, answering
the REST and `gh` reads the card code makes, and failing loudly on a call it does not know.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dokima import card  # noqa: E402
from test_agent import rec  # noqa: E402
from test_scan import REPO, drawn, plan_approved, world  # noqa: E402,F401

from dokima import scan  # noqa: E402

LABEL = "autopilot"
STATUS = re.compile(r"^(?:<img[^>]*>\s*)?\*\*(Backlog|Plan|Work|Review|Merged)\*\*")


def plain(text):
    """Text as plain words: no tags or bold."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text).replace("**", "")).strip()


def status_line(k, top, what):
    """The card's status line: the one line that opens with its stage."""
    found = [l for l in top.splitlines() if STATUS.match(l)]
    assert len(found) == 1, f"{k} ({what}): expected one status line on the card, found {found}:\n{top}"
    return found[0]


def icon():
    return card.field_icon(REPO, "autopilot")


def assert_autopilot(k, top, what):
    """Fail unless the status line shows the autopilot icon, then Autopilot, and no Needs you."""
    line = status_line(k, top, what)
    assert icon() in line, f"{k} ({what}): the status line of a card on autopilot has no autopilot icon: {line}"
    assert re.search(re.escape(icon()) + r"\s*(?:\*\*)?Autopilot\b", line), \
        f"{k} ({what}): the autopilot icon on the status line is not followed by the word Autopilot: {line}"
    assert "Needs you" not in line, f"{k} ({what}): setup: this card should not need the owner: {line}"


def assert_no_autopilot(k, top, what):
    """Fail if the card shows the autopilot icon, or its status line says Autopilot."""
    line = status_line(k, top, what)
    assert icon() not in top, f"{k} ({what}): the card shows the autopilot icon: {line}"
    assert "Autopilot" not in plain(line), f"{k} ({what}): the status line says Autopilot: {line}"


def planned():
    """A plan its review has not judged yet: Plan, needing no one."""
    return [rec("planner", handback={"kind": "user_story", "summary": "Draw the autopilot icon."})]


def test_a_card_on_autopilot_shows_the_autopilot_icon_and_word(record_property, world, monkeypatch, tmp_path):
    """A card on autopilot shows its icon and Autopilot, on the issue and PR.

    Proves 454.3.

    Labels #5 (no record, Backlog) and #6 (planned, Plan, with open pull request #60) autopilot, draws their cards
    with Dokima's card code, and checks each issue card's status line and the pull request's own description show the
    icon followed by Autopilot; the board scan's card for each says the same."""
    record_property("proves", "454.3")
    world.issue(5, labels=(LABEL,))
    world.issue(6, records=planned(), labels=(LABEL,))
    world.pr(60, 6)
    assert_autopilot("454.3", drawn(world, 5, None, monkeypatch, tmp_path), "issue #5 in Backlog")
    assert_autopilot("454.3", drawn(world, 6, 60, monkeypatch, tmp_path), "issue #6 in Plan")
    pr_md = tmp_path / "pr.md"
    assert pr_md.exists(), "454.3: setup: the card code wrote no description for pull request #60"
    assert_autopilot("454.3", pr_md.read_text().split("<!-- dokima-ask -->")[0], "pull request #60")
    assert_autopilot("454.3", scan.card_now(REPO, "issue", 5), "the scan's card of issue #5")
    assert_autopilot("454.3", scan.card_now(REPO, "pr", 60), "the scan's card of pull request #60")


def test_needs_you_hides_the_autopilot_icon_and_a_card_off_autopilot_shows_neither(record_property, world, monkeypatch,
                                                                                    tmp_path):
    """Needs you hides the autopilot icon, and a card off autopilot shows neither.

    Proves 454.3.

    Draws #7, on autopilot with an approved plan waiting for the owner, and checks its status line shows Needs you
    and no autopilot icon or word. Then draws #8 (no record) and #9 (planned) with no autopilot label and checks
    neither shows the icon or the word. Beside them, #10, on autopilot and planned, does show it."""
    record_property("proves", "454.3")
    world.issue(7, records=plan_approved(), labels=(LABEL,))
    world.issue(8)
    world.issue(9, records=planned(), labels=("high",))
    world.issue(10, records=planned(), labels=(LABEL,))
    top = drawn(world, 7, None, monkeypatch, tmp_path)
    assert "Needs you" in status_line("454.3", top, "issue #7"), \
        f"454.3: setup: the approved plan of #7 should show Needs you:\n{top}"
    assert_no_autopilot("454.3", top, "issue #7 while Needs you shows")
    assert_no_autopilot("454.3", scan.card_now(REPO, "issue", 7), "the scan's card of issue #7")
    assert_no_autopilot("454.3", drawn(world, 8, None, monkeypatch, tmp_path), "issue #8 off autopilot")
    assert_no_autopilot("454.3", drawn(world, 9, None, monkeypatch, tmp_path), "issue #9 off autopilot")
    assert_autopilot("454.3", drawn(world, 10, None, monkeypatch, tmp_path), "issue #10 on autopilot")
