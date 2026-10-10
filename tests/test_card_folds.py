"""Scope shows as code on one line; Out of scope, requirements and the owner's text fold.

Issue #373. The owner asked (2026-10-09) that on the issue and PR card the Scope lists its files as code fields,
`dokima/card.py`, all on one line instead of one line per file, and that the original issue text, the non-functional
requirements and Out of scope sit in folds, closed by default.

The card is drawn by dokima/card.py render (the same card on the issue and the PR, which card.pr_body saves on the PR);
the owner's text below the card's marker is kept by dokima/body.py redraw and saved by the card's main and the planner.
These tests draw the card from records the way tests/test_card_records.py does and redraw bodies the way
tests/test_body.py does, with GitHub faked by its recorder.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent, body, card, planner  # noqa: E402
from test_body import PLAN_TOP, TRICKY, github, run_card  # noqa: E402,F401

ROOT = os.path.join(os.path.dirname(__file__), "..")
REPO = "o/r"
ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40"}
SRC = "https://github.com/o/r/issues/40"
SCOPE = ["dokima/card.py", "tests/test_card.py", "dokima/body.py::redraw"]
OUT = ["The journey diagram; that's another issue.", "Run comments keep their own folds."]
NFR = [{"text": "A refused save says why.", "why": "nothing fails silently", "principle": "Fail closed"}]


def plan_of(scope=SCOPE, out=OUT, nfr=NFR):
    return {"kind": "user_story", "summary": "Cards fold what the owner rarely reads.",
            "user_story": "The owner reads a short card.",
            "acceptance_criteria": [{"text": "Scope shows on one line.", "source": SRC}],
            "non_functional": nfr, "scope": scope, "out_of_scope": out, "tests": {}}


def rec(role, stage=None, **handback):
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
            "run": "https://github.com/o/r/actions/runs/1"}


def cards(**kw):
    """The issue card and the PR description, for a plan with `kw` replaced."""
    found = {"recs": [rec("planner", **plan_of(**kw))], "pr": None, "check_runs": [], "reviews": [],
             "owners": {"boss"}, "tests": {}, "worker": None}
    issue_card = card.render(REPO, ISSUE, found, page="issue")
    pr_card = card.pr_body(card.render(REPO, ISSUE, dict(found, pr={"number": 5, "merged": False, "state": "open"}),
                                       page="pr"), "Closes #40")
    return {"issue card": issue_card, "PR card": pr_card}


def outside_folds(text):
    """The card's text with every fold (<details> ... </details>) taken out."""
    return re.sub(r"<details[^>]*>.*?</details>", "", text, flags=re.S)


def folds(text):
    """Every fold in the card as (opening tag, summary text, the lines inside it)."""
    found = []
    for m in re.finditer(r"(<details[^>]*>)<summary>(.*?)</summary>(.*?)</details>", text, flags=re.S):
        found.append((m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip(), m.group(3)))
    return found


def fold_named(k, where, text, title):
    """The one fold titled `title`, closed by default; fails naming criterion k otherwise."""
    named = [f for f in folds(text) if f[1] == title]
    assert len(named) == 1, f"{k}: the {where} has {len(named)} folds titled {title!r}, expected exactly one:\n{text}"
    tag, _, inside = named[0]
    assert tag == "<details>", f"{k}: the {title} fold on the {where} is not closed by default: {tag}"
    return inside


# 373.1: Scope lists its files as code on one line, separated by commas

def test_scope_shows_every_file_as_code_on_one_line(record_property):
    """Scope lists every file as code on one line, comma separated, on both cards.

    Proves 373.1. Draws the card of a plan with three scope entries and checks both cards hold exactly the line
    **Scope:** `dokima/card.py`, `tests/test_card.py`, `dokima/body.py::redraw`, in the plan's order, and no line
    per file anywhere; a plan with one file shows just that file as code."""
    record_property("proves", "373.1")
    for where, text in cards().items():
        lines = text.splitlines()
        scope_lines = [ln for ln in lines if "Scope:" in ln and "Out of scope" not in ln]
        assert scope_lines == ["**Scope:** `dokima/card.py`, `tests/test_card.py`, `dokima/body.py::redraw`"], \
            f"373.1: the {where} does not show Scope as code on one line, comma separated; its Scope lines are {scope_lines}"
        for path in SCOPE:
            assert sum(path in ln for ln in lines) == 1, f"373.1: on the {where}, {path} shows on more than one line"
            assert not any(re.match(rf"\s*-\s*`?{re.escape(path)}`?\s*$", ln) for ln in lines), \
                f"373.1: on the {where}, {path} still has a line of its own"
    for where, text in cards(scope=["app/jobs.py"]).items():
        assert "**Scope:** `app/jobs.py`" in text.splitlines(), \
            f"373.1: the {where} does not show a one-file Scope as **Scope:** `app/jobs.py`"


# 373.2: Out of scope and the non-functional requirements sit in folds, closed by default

def test_out_of_scope_sits_in_a_closed_fold(record_property):
    """Out of scope sits in a closed fold on the issue card and the PR card.

    Proves 373.2. Draws the card of a plan with two Out of scope sentences and checks each sits inside one closed
    fold titled Out of scope, with no Out of scope heading or sentence left open on the card; Scope stays open
    beside it."""
    record_property("proves", "373.2")
    for where, text in cards().items():
        inside = fold_named("373.2", where, text, "Out of scope")
        for sentence in OUT:
            assert sentence in inside, f"373.2: on the {where}, {sentence!r} is not inside the Out of scope fold"
        rest = outside_folds(text)
        assert "Out of scope" not in rest, f"373.2: the {where} still shows an Out of scope heading outside its fold"
        assert not any(s in rest for s in OUT), f"373.2: the {where} still shows an Out of scope sentence open"
        assert "**Scope:** `dokima/card.py`" in rest, f"373.2: the {where} folded Scope too; it should stay open"


def test_non_functional_requirements_sit_in_a_closed_fold_beside_out_of_scope(record_property):
    """The non-functional requirements sit in their own closed fold on both cards.

    Proves 373.2. Draws the card of a plan with a non-functional requirement and checks it is inside one closed fold
    titled Non-functional requirements and nowhere open on the card, and that Out of scope has its own closed fold."""
    record_property("proves", "373.2")
    for where, text in cards().items():
        inside = fold_named("373.2", where, text, "Non-functional requirements")
        assert NFR[0]["text"] in inside, f"373.2: on the {where}, the requirement is not in its fold"
        assert NFR[0]["text"] not in outside_folds(text), f"373.2: on the {where}, the requirement also shows open"
        fold_named("373.2", where, text, "Out of scope")


# 373.3: the owner's original issue text sits in a fold titled Original issue, closed by default

ASKS = ("Please fold my words.\n- [ ] Goal: an old goal\n", TRICKY, "",
        "<details><summary>My own fold</summary>\n\nA detail I folded myself.\n\n</details>\n")
FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
FOLD_END = "\n\n</details>"


def assert_folded(k, new, ask):
    """Fail naming criterion k unless the owner's text sits alone in one closed Original issue fold.

    It must sit below the one marker, byte for byte, and read back as written."""
    assert new.count(body.MARKER) == 1, f"{k}: expected exactly one marker, found {new.count(body.MARKER)}"
    below = new.split(body.MARKER, 1)[1]
    assert below == FOLD_START + ask + FOLD_END, \
        f"{k}: the owner's text is not alone inside a closed Original issue fold below the card:\n{below!r}"
    assert body.ask(new) == ask, f"{k}: the owner's text does not read back byte for byte"


def open_body(top, ask):
    """A body saved before this change, the owner's text open below the marker."""
    return top.rstrip("\n") + "\n\n" + body.MARKER + "\n\n" + ask


def test_the_owners_text_is_folded_below_the_card(record_property):
    """The owner's text sits below the card in a closed fold titled Original issue.

    Proves 373.3. Redraws four asks (plain words, one full of Windows line ends and stray markup, an empty one and
    one with the owner's own fold) fresh and again, and checks each sits byte for byte inside one closed Original
    issue fold below the card, the same after every redraw."""
    record_property("proves", "373.3")
    for ask in ASKS:
        new = body.redraw(ask, "the card")
        assert new.split(body.MARKER, 1)[0].strip() == "the card", "373.3: the card is not alone above the marker"
        assert_folded("373.3", new, ask)
        again = body.redraw(new, "another card")
        assert_folded("373.3", again, ask)


def test_an_open_ask_folds_on_its_next_redraw(record_property):
    """An ask that shows open today folds under Original issue on its next redraw.

    Proves 373.3. Builds bodies with the owner's text open below the marker, as saved before this change, redraws
    each and checks it is saved, not refused, with the text byte for byte in the closed Original issue fold."""
    record_property("proves", "373.3")
    for ask in ASKS:
        try:
            new = body.redraw(open_body("old card", ask), "new card")
        except body.Refused as e:
            pytest.fail(f"373.3: folding an open ask was refused: {e}")
        assert_folded("373.3", new, ask)


def test_the_card_and_the_planner_fold_the_owners_text(record_property, monkeypatch, github):
    """The card and the planner both save the owner's text folded under Original issue.

    Proves 373.3. Runs the card's main on a fresh ask and on an ask open today, and the planner's render on a fresh
    ask, and checks every saved body keeps the owner's text byte for byte in the closed Original issue fold with no
    refusal posted; a split's quoted story stays folded the same way."""
    record_property("proves", "373.3")
    for current in (TRICKY, open_body(PLAN_TOP, TRICKY)):
        saved = run_card(monkeypatch, github, current)
        assert saved is not None, "373.3: the card saved nothing on the issue"
        assert_folded("373.3", saved, TRICKY)
    assert not github.comments, "373.3: folding the owner's text posted a refusal"
    story = {"objective": "Fold the ask", "criteria": ["The ask is folded"], "non_goals": [],
             "scope": ["dokima/body.py"], "test_changes": {}}
    assert_folded("373.3", planner.render("9", "My own words.", story, {}), "My own words.")
    quoted = agent.story_body(230, 4, {"title": "Folds", "user_story": "Folded.", "context": "c",
                                       "acceptance_criteria": [{"text": "Folded.", "source": SRC}],
                                       "non_functional": []}, "Cards show everything")
    assert_folded("373.3", body.redraw(quoted, "the card"), quoted)


def test_a_redraw_that_would_change_the_folded_text_is_refused(record_property):
    """A redraw that would change the owner's folded text is still refused.

    Proves 373.3. A good one goes through. Draws a card that holds the marker itself on a folded ask and on an ask
    open today, and checks each is refused with a reason, while a plain card on the same bodies folds the text as
    written."""
    record_property("proves", "373.3")
    for current in (body.redraw("My ask.", "old card"), open_body("old card", "My ask.")):
        with pytest.raises(body.Refused) as refused:
            body.redraw(current, f"a card that quotes {body.MARKER} in a criterion")
        assert str(refused.value).strip(), "373.3: the refusal gives no reason"
        assert_folded("373.3", body.redraw(current, "a card"), "My ask.")


# 373.4: AGENTS.md says the owner's text is folded, so every agent reads the decision

def issue_body_section():
    text = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
    m = re.search(r"^## The issue body\n(.*?)(?=^## )", text, flags=re.S | re.M)
    assert m, "373.4: AGENTS.md has no '## The issue body' section"
    return m.group(1)


def test_agents_md_says_the_owners_text_is_folded(record_property):
    """AGENTS.md says the owner's ask is folded under Original issue, closed by default.

    Proves 373.4. Reads AGENTS.md's The issue body section and checks it names the Original issue fold, closed by
    default, no longer says the ask is open or that a folded ask opens, and still says code writes only above the
    marker."""
    record_property("proves", "373.4")
    section = issue_body_section()
    assert "Original issue" in section and "closed by default" in section, \
        "373.4: AGENTS.md's The issue body does not say the owner's ask is folded under Original issue, closed by default"
    for stale in ("open, exactly as written", "opens on its next redraw", "keeps it folded under Original issue"):
        assert stale not in section, f"373.4: AGENTS.md's The issue body still says {stale!r}"
    assert "Code only writes above the marker" in section, \
        "373.4: AGENTS.md's The issue body no longer says code only writes above the marker"
