"""The owner's ask reads open on the issue they wrote, folded only where it is quoted from somewhere else.

Issue #237, story 4 of #230. dokima/body.py keeps the owner's part below one fixed marker. Until now every redraw
wrapped it in a closed `<details><summary>Original issue</summary>` fold. Now the ask on an issue the owner wrote
shows open below the card, byte for byte; an issue whose body is a split's story, quoted by code from the parent's
approved plan (dokima/agent.py story_body), keeps the fold. Issues saved before this change carry the fold already:
reading still accepts it, and their next redraw opens it. A redraw that would change the owner's text is still
refused, leaving the body as it was and saying why on the issue.

GitHub is faked by the same recorder tests/test_body.py uses; the card's main runs as in those tests.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent, body, plan, planner  # noqa: E402
from test_body import NUMBER, PLAN_TOP, REPO, TRICKY, github, run_card  # noqa: E402,F401

FOLD_SUMMARY = "<summary>Original issue</summary>"
OLD_FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
OLD_FOLD_END = "\n\n</details>"

OWNER_ASKS = ("Please keep my words open.\n- [ ] Goal: an old goal\n", TRICKY, "",
              "<details><summary>My own fold</summary>\n\nA detail I folded myself.\n\n</details>\n")

STORY = {"title": "Open asks", "user_story": "The owner's ask reads open.",
         "context": "dokima/body.py folds the ask.",
         "acceptance_criteria": [{"text": "The ask shows open.", "source": "https://github.com/o/r/issues/230"}],
         "non_functional": [{"text": "Refusals still say why.", "why": "the owner's words are never rewritten"}]}


def below(text):
    """Everything below the one marker."""
    assert text.count(body.MARKER) == 1, f"expected exactly one marker, found {text.count(body.MARKER)}"
    return text.split(body.MARKER, 1)[1]


def assert_open(k, new, ask):
    """Fail naming criterion k unless the owner's ask sits open below the marker, byte for byte, with no fold of code's."""
    part = below(new)
    assert body.ask(new) == ask, f"{k}: the owner's ask does not read back byte for byte"
    assert ask in part, f"{k}: the owner's text is not below the marker exactly as written"
    assert FOLD_SUMMARY not in part, f"{k}: the owner's ask is still folded under Original issue"
    assert part.count("<details") == ask.count("<details") and part.count("</details>") == ask.count("</details>"), \
        f"{k}: code wrapped the owner's ask in a fold; it should show open below the card"


def assert_folded(k, new, ask):
    """Fail naming criterion k unless the quoted ask sits below the marker inside one closed Original issue fold."""
    part = below(new)
    assert body.ask(new) == ask, f"{k}: the quoted ask does not read back byte for byte"
    head = part.lstrip()
    assert head.startswith("<details>" + FOLD_SUMMARY), f"{k}: a split's quoted story is not folded under Original issue"
    assert part.rstrip().endswith("</details>"), f"{k}: the Original issue fold is not closed after the quoted story"
    assert ask in part, f"{k}: the quoted story is not inside the fold as written"


def old_folded(top, ask):
    """A body saved before this change: the card, the marker, and the ask in the closed Original issue fold."""
    return top.rstrip("\n") + "\n\n" + body.MARKER + OLD_FOLD_START + ask + OLD_FOLD_END


# 237.1: on the issue the owner wrote, their text shows open below the card, byte for byte

def test_the_owners_ask_shows_open_below_the_card(record_property):
    """On an issue the owner wrote, their text shows open below the card, exactly as written.

    Redraws four owner asks (plain words with old checkboxes, an ask full of Windows line ends and stray markup, an
    empty ask, and an ask with the owner's own fold) and checks each sits below the one marker with no Original issue
    fold around it and reads back byte for byte."""
    record_property("proves", "237.1")
    for ask in OWNER_ASKS:
        new = body.redraw(ask, "the card")
        assert new.split(body.MARKER, 1)[0].strip() == "the card", "237.1: the card is not alone above the marker"
        assert_open("237.1", new, ask)


def test_the_open_ask_stays_byte_for_byte_after_many_redraws(record_property):
    """The open ask never changes, however many times code redraws the card above it.

    Redraws an ask the card cannot read five times with different cards and checks it stays open and every byte
    below the marker stays the same."""
    record_property("proves", "237.1")
    current = body.redraw(TRICKY, "first card")
    assert_open("237.1", current, TRICKY)
    part = below(current)
    for k in range(5):
        current = body.redraw(current, f"card {k}")
        assert below(current) == part, f"237.1: redraw {k + 1} changed the part below the marker"
        assert_open("237.1", current, TRICKY)


def test_the_card_shows_the_owners_ask_open(record_property, monkeypatch, github):
    """When the card is drawn on an issue the owner wrote, their text shows open below it.

    Runs the card's main on a fresh owner-written issue, then again on what it saved, and checks both saved bodies
    have the card on top and the owner's text open below the marker, byte for byte."""
    record_property("proves", "237.1")
    saved = run_card(monkeypatch, github, TRICKY)
    assert saved is not None, "237.1: the card saved nothing on the issue"
    assert saved.startswith(plan.CARD_START), "237.1: the card is not at the top of the issue"
    assert_open("237.1", saved, TRICKY)
    again = run_card(monkeypatch, github, saved)
    assert again is not None, "237.1: the second card run saved nothing"
    assert_open("237.1", again, TRICKY)
    assert below(again) == below(saved), "237.1: the second card run changed the part below the marker"


def test_the_planner_shows_the_owners_ask_open(record_property):
    """When the planner writes its plan into an issue the owner wrote, their text shows open below it.

    Runs the planner's render on a fresh ask and again on its own output, and checks the ask stays open and
    byte for byte below the plan."""
    record_property("proves", "237.1")
    story = {"objective": "Slow calls return a job id", "criteria": ["A slow call returns a job id within 20 s"],
             "non_goals": [], "scope": ["dokima/jobs.py"], "test_changes": {}}
    first = planner.render("9", TRICKY, story, {})
    assert_open("237.1", first, TRICKY)
    assert_open("237.1", planner.render("9", first, dict(story, objective="Again"), {}), TRICKY)


# 237.2: an issue whose ask is folded today opens on its next redraw, the owner's text unchanged

def test_an_old_folded_ask_opens_on_its_next_redraw(record_property):
    """An issue whose ask is folded today opens on its next redraw, with the owner's text unchanged.

    Builds old folded bodies for four owner asks, checks each still reads back byte for byte, then redraws each and
    checks it is saved, not refused, with the ask open below the marker and byte for byte as written; a second redraw
    leaves it open and the same."""
    record_property("proves", "237.2")
    for ask in OWNER_ASKS:
        assert body.ask(old_folded("old card", ask)) == ask, "237.2: an old folded ask no longer reads back as written"
        try:
            new = body.redraw(old_folded("old card", ask), "new card")
        except body.Refused as e:
            pytest.fail(f"237.2: opening an old folded ask was refused: {e}")
        assert new.split(body.MARKER, 1)[0].strip() == "new card", "237.2: the new card is not above the marker"
        assert_open("237.2", new, ask)
        again = body.redraw(new, "third card")
        assert_open("237.2", again, ask)
        assert below(again) == below(new), "237.2: the redraw after opening changed the part below the marker"


def test_the_card_opens_an_old_folded_ask(record_property, monkeypatch, github):
    """The next card drawn on an issue whose ask is folded today opens it, with the owner's text unchanged.

    Runs the card's main on an old folded body and checks the saved body shows the ask open, byte for byte, and no
    refusal is posted."""
    record_property("proves", "237.2")
    saved = run_card(monkeypatch, github, old_folded(PLAN_TOP, TRICKY))
    assert saved is not None, "237.2: the card saved nothing on an issue with an old folded ask"
    assert_open("237.2", saved, TRICKY)
    assert not github.comments, "237.2: opening an old folded ask posted a refusal"


# 237.3: where the owner's text is quoted from somewhere else, like a split's sub-issues, it stays folded

def test_a_split_story_stays_folded(record_property):
    """A split's sub-issue, whose text is quoted from the parent's approved plan, keeps it folded.

    Draws a story body the way code files a split's sub-issue, redraws it fresh and again, and checks the quoted
    story sits in one closed Original issue fold below the marker, byte for byte. Beside it, an owner's ask on the
    same redraw shows open."""
    record_property("proves", "237.3")
    quoted = agent.story_body(230, 4, STORY, "Cards show everything")
    new = body.redraw(quoted, "the card")
    assert_folded("237.3", new, quoted)
    again = body.redraw(new, "another card")
    assert_folded("237.3", again, quoted)
    assert below(again) == below(new), "237.3: a redraw changed the part below the marker of a split's story"
    assert_open("237.3", body.redraw("An owner's own ask.", "the card"), "An owner's own ask.")


def test_a_split_story_folded_today_stays_folded(record_property, monkeypatch, github):
    """A split's sub-issue already folded today stays folded when the card is drawn again.

    Runs the card's main on an old folded body holding a split's story and checks the saved body keeps it in the
    Original issue fold, byte for byte, with no refusal posted. Beside it, an old folded owner's ask opens."""
    record_property("proves", "237.3")
    quoted = agent.story_body(230, 2, STORY, "Cards show everything")
    saved = run_card(monkeypatch, github, old_folded(PLAN_TOP, quoted))
    assert saved is not None, "237.3: the card saved nothing on a split's story"
    assert_folded("237.3", saved, quoted)
    assert not github.comments, "237.3: redrawing a split's story posted a refusal"
    owners = run_card(monkeypatch, github, old_folded(PLAN_TOP, "An owner's own ask."))
    assert owners is not None, "237.3: the card saved nothing on an owner's ask"
    assert_open("237.3", owners, "An owner's own ask.")


def test_the_card_folds_a_fresh_split_story(record_property, monkeypatch, github):
    """The first card drawn on a freshly filed sub-issue folds its quoted story.

    Runs the card's main on a sub-issue body exactly as a split files it and checks the saved body keeps the story in
    the Original issue fold, byte for byte. Beside it, a fresh owner's ask opens."""
    record_property("proves", "237.3")
    quoted = agent.story_body(230, 3, STORY, "Cards show everything")
    saved = run_card(monkeypatch, github, quoted)
    assert saved is not None, "237.3: the card saved nothing on a fresh split story"
    assert_folded("237.3", saved, quoted)
    owners = run_card(monkeypatch, github, "An owner's own ask.")
    assert owners is not None, "237.3: the card saved nothing on an owner's ask"
    assert_open("237.3", owners, "An owner's own ask.")


# 237.4: a redraw that would change the owner's text is still refused, the body left alone and the reason on the issue

def test_a_redraw_that_would_change_the_ask_is_still_refused(record_property):
    """A redraw that would change the owner's text is still refused, open or folded, and a good one goes through.

    Draws a card that holds the marker itself on an open ask, an old folded ask and a split's story, and checks each
    is refused with a reason; the same bodies with a plain card redraw fine, the open ask staying open."""
    record_property("proves", "237.4")
    quoted = agent.story_body(230, 4, STORY, "Cards show everything")
    assert_open("237.4", body.redraw("My ask.", "old card"), "My ask.")
    for current in (body.redraw("My ask.", "old card"), old_folded("old card", "My ask."), body.redraw(quoted, "old")):
        with pytest.raises(body.Refused) as refused:
            body.redraw(current, f"a card that quotes {body.MARKER} in a criterion")
        assert str(refused.value).strip(), "237.4: the refusal gives no reason"
        body.redraw(current, "a card that quotes nothing")
    assert_open("237.4", body.redraw(old_folded("old card", "My ask."), "a card"), "My ask.")


def test_a_refused_save_leaves_the_open_body_and_says_why(record_property, github):
    """When the owner's open text would change, nothing is saved and the issue gets one comment saying why.

    Saves a bad card on an open ask and on an old folded ask: the body is never written, one comment with the reason
    is posted to this issue each time and the save reports False; a good card then saves with no comment."""
    record_property("proves", "237.4")
    for current in (body.redraw("My ask.", "old card"), old_folded("old card", "My ask.")):
        github.saves.clear()
        github.comments.clear()
        bad = f"a card that quotes {body.MARKER}"
        with pytest.raises(body.Refused) as refused:
            body.redraw(current, bad)
        assert body.save(REPO, NUMBER, current, bad) is False, "237.4: a refused save did not report False"
        assert github.saves == [], "237.4: the body was written although the owner's text would change"
        assert len(github.comments) == 1, f"237.4: expected one comment saying why, got {len(github.comments)}"
        args, text = github.comments[0]
        assert any(a == str(NUMBER) or f"issues/{NUMBER}/" in a for a in args), "237.4: the reason went somewhere other than this issue"
        assert str(refused.value) in (text or ""), "237.4: the comment does not say why the save was refused"
        assert body.save(REPO, NUMBER, current, "good card") is True, "237.4: a good save did not report True"
        assert len(github.saves) == 1 and body.ask(github.saves[0]) == "My ask.", "237.4: a good save changed the owner's text"
        assert len(github.comments) == 1, "237.4: a good save posted a refusal"
        assert_open("237.4", github.saves[0], "My ask.")


def test_the_owners_open_text_is_never_read_as_plan(record_property):
    """The owner's open text is never read as the plan: their old checkboxes never become goals or criteria.

    Writes a plan into an issue whose ask holds old plan checkboxes and checks the plan reads back with only the
    planner's one goal and criterion, the same as for an ask with no checkboxes."""
    record_property("proves", "237.5")
    story = {"objective": "Slow calls return a job id", "criteria": ["A slow call returns a job id within 20 s"],
             "non_goals": [], "scope": ["dokima/jobs.py"], "test_changes": {}}
    ask = "- [ ] Goal: an old goal\n  - [ ] Done when: an old criterion\n- [ ] Objective: another old goal\n"
    new = planner.render("9", ask, story, {})
    assert_open("237.5", new, ask)
    parsed = plan.parse(new)
    assert [g["text"] for g in parsed["goals"]] == ["Slow calls return a job id"], \
        "237.5: the owner's old checkboxes were read as plan goals"
    assert [c["text"] for c in parsed["goals"][0]["criteria"]] == ["A slow call returns a job id within 20 s"], \
        "237.5: the owner's old checkboxes were read as plan criteria"
    plain = plan.parse(planner.render("9", "No checkboxes here.", story, {}))
    assert [g["text"] for g in plain["goals"]] == ["Slow calls return a job id"], "237.5: a plain ask lost the plan's goal"
