"""A planned issue reads: the card, the Original issue fold, then the Definition of Done.

Issue #454, story 3 of #416. Before it, a planned issue's Definition of Done was the card's last line, above the marker,
and the owner's Original issue fold came after it, at the very bottom (dokima/card.py render, dokima/body.py redraw).
Now, once planned, the body reads: the card, then the Original issue fold, then the Definition of Done, last. The
owner's part stays byte for byte, a body saved the old way is redrawn this way next time, and a redraw that would
change the owner's part is still refused with the body left as it was.

The card's main runs as tests/test_body.py runs it: GitHub faked by its recorder, the issue planned by one planner
record, no pull request and no worker run.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent, body, card, plan  # noqa: E402
from test_body import NUMBER, REPO, TRICKY, github, run_card  # noqa: E402,F401

FOLD_HEAD = "<details><summary>Original issue</summary>"
DONE_LINE = re.compile(r"\*\*Definition of Done:\*\*[^\n]*")
OLD_CARD = ("<!-- dokima-card -->\n**Plan**\n\n**User story:** Owners see a card.\n\n"
            "**Definition of Done:** All tests · Code review · Owner approval\n\n<!-- /dokima-card -->")
STORY = {"title": "Done last", "user_story": "The owner reads the Definition of Done last.",
         "context": "dokima/body.py places the fold.",
         "acceptance_criteria": [{"text": "The fold sits above the Definition of Done.",
                                  "source": "https://github.com/o/r/issues/416"}],
         "non_functional": []}
PLANNED = {"role": "planner", "stage": None, "check": {"passed": True}, "run": "https://github.com/o/r/actions/runs/1",
           "handback": {"kind": "user_story", "user_story": "Owners see a card.", "non_functional": [],
                        "acceptance_criteria": [{"text": "first thing works", "source": f"https://github.com/{REPO}/issues/{NUMBER}"}],
                        "scope": ["dokima/card.py"], "out_of_scope": [], "tests": {}}}


def old_saved(ask):
    """A planned body saved the old way, the Definition of Done inside the card."""
    return OLD_CARD + "\n\n" + body.MARKER + "\n" + FOLD_HEAD + "\n\n" + ask + "\n\n</details>"


def assert_done_last(k, saved, ask, what):
    """Fail naming k unless `saved` is the card, the fold, then the Definition of Done.

    The Definition of Done must be the body's one and last line."""
    assert saved is not None, f"{k} ({what}): the card saved nothing"
    assert saved.count(body.MARKER) == 1, f"{k} ({what}): the body holds {saved.count(body.MARKER)} markers, expected one"
    above, below = saved.split(body.MARKER, 1)
    assert body.ask(saved) == ask, f"{k} ({what}): the owner's words do not read back byte for byte"
    assert "Definition of Done" not in above, \
        f"{k} ({what}): the Definition of Done is still in the card, above the Original issue fold:\n{saved}"
    assert above.rstrip().endswith(plan.CARD_END), f"{k} ({what}): something other than the card sits above the marker:\n{above}"
    assert below.lstrip("\n").startswith(FOLD_HEAD), \
        f"{k} ({what}): the Original issue fold does not come right after the card:\n{below[:300]}"
    start = below.index(FOLD_HEAD) + len(FOLD_HEAD)
    rest = below[below.find(ask, start) + len(ask):]
    m = re.fullmatch(r"\s*</details>\s*(?:<!--[^\n]*?-->\s*)*(" + DONE_LINE.pattern + r")\s*", rest)
    assert m, (f"{k} ({what}): after the Original issue fold the body does not end with the Definition of Done "
               f"as its only, last line:\n{rest}")
    assert "All tests" in m.group(1) and "Owner approval" in m.group(1), \
        f"{k} ({what}): the last line is not the card's Definition of Done: {m.group(1)}"
    assert len(DONE_LINE.findall(saved)) == 1, f"{k} ({what}): the Definition of Done shows more than once:\n{saved}"


def test_a_planned_issue_ends_with_its_definition_of_done_right_below_the_fold(record_property, monkeypatch, github):
    """A planned issue ends with its Definition of Done, right below the Original issue fold.

    Proves 454.1.

    Runs the card on a planned issue whose ask is fresh, an ask the card cannot read, and a split's story quoted
    from its parent, and checks each saved body: the card, the marker, the Original issue fold holding the owner's
    words byte for byte, then the Definition of Done as the one and last line, and nowhere in the card. Beside it,
    the same card with no plan record keeps the ask open with the Definition of Done below it, so only planned issues
    moved."""
    record_property("proves", "454.1")
    quoted = agent.story_body(416, 3, STORY, "Card links show as GitHub's own references")
    for what, ask in (("a fresh ask", "My ask."), ("an ask the card cannot read", TRICKY), ("a split's story", quoted)):
        assert_done_last("454.1", run_card(monkeypatch, github, ask), ask, what)
    saved = unplanned_save(monkeypatch, github, "My ask.")
    assert body.ask(saved) == "My ask.", "454.1: the unplanned issue's ask does not read back byte for byte"
    assert FOLD_HEAD not in saved, f"454.1: an unplanned issue's ask is folded:\n{saved}"
    assert DONE_LINE.fullmatch(saved.rstrip().splitlines()[-1]), \
        f"454.1: an unplanned issue no longer ends with its Definition of Done:\n{saved}"


def unplanned_save(monkeypatch, github, current):
    """Run the card's main on an issue with no plan record; the body it saved."""
    monkeypatch.setattr(card, "gather", lambda repo, n, pr: {"recs": [], "pr": None, "check_runs": [], "reviews": [],
                                                              "owners": set(), "tests": {}, "worker": None})
    issue = {"number": NUMBER, "title": "t", "url": f"https://github.com/{REPO}/issues/{NUMBER}", "approved_at": None,
             "changes": [], "plan": plan.parse(current), "current_body": current, "body": current}
    monkeypatch.setattr(card, "find_work", lambda repo: (NUMBER, None))
    monkeypatch.setattr(card, "latest_worker_run", lambda repo, n: None)
    monkeypatch.setattr(plan, "fetch_issue", lambda repo, n: issue)
    before = len(github.saves)
    try:
        card.main()
    except (SystemExit, Exception):
        pass
    assert len(github.saves) > before, "454.1: the card saved nothing on an unplanned issue"
    return github.saves[-1]


def test_a_planned_issue_saved_the_old_way_is_redrawn_the_new_way(record_property, monkeypatch, github):
    """An issue saved the old way is redrawn the new way next time.

    Proves 454.1.

    Runs the card on a planned body saved before this change (the Definition of Done last in the card, the fold at
    the bottom), and on a body saved before it was planned (the ask open, the Definition of Done below it), and checks
    each is saved as the card, the fold, then the Definition of Done last, the owner's words unchanged; drawing it
    once more saves the very same body."""
    record_property("proves", "454.1")
    unplanned = body.redraw("My ask.", "<!-- dokima-card -->\n**Backlog**\n<!-- /dokima-card -->\n\n" + body.DONE
                            + "\n**Definition of Done:** All tests · Code review · Owner approval")
    for what, current, ask in (("saved the old way", old_saved("My ask."), "My ask."),
                               ("saved the old way, an ask the card cannot read", old_saved(TRICKY), TRICKY),
                               ("saved before its plan", unplanned, "My ask.")):
        saved = run_card(monkeypatch, github, current)
        assert_done_last("454.1", saved, ask, what)
        again = run_card(monkeypatch, github, saved)
        assert again == saved, f"454.1 ({what}): drawing the card once more changed the body:\n{saved}\n---\n{again}"


def test_agents_md_says_the_definition_of_done_comes_last_below_the_fold(record_property):
    """AGENTS.md says the Definition of Done comes last, below the Original issue fold.

    Proves 454.1.

    Reads The issue body section of AGENTS.md and checks it no longer says the Definition of Done is the card's last
    line once planned, and says it sits below the Original issue fold."""
    record_property("proves", "454.1")
    text = open(os.path.join(os.path.dirname(__file__), "..", "AGENTS.md")).read()
    section = text.split("## The issue body", 1)[1].split("\n## ", 1)[0]
    assert "the Definition of Done is the card's last line again" not in section, \
        "454.1: AGENTS.md still says a planned issue's Definition of Done is the card's last line"
    assert re.search(r"Original issue[^.]*(above|before)[^.]*Definition of Done|Definition of Done[^.]*(below|after)[^.]*"
                     r"(Original issue|fold)", section), \
        f"454.1: AGENTS.md's issue body section does not say the Definition of Done comes below the fold:\n{section}"


def planned_top():
    """The card Dokima draws for the planned issue the card's main runs on."""
    issue = {"number": NUMBER, "url": f"https://github.com/{REPO}/issues/{NUMBER}"}
    return card.render(REPO, issue, {"recs": [PLANNED], "pr": None, "check_runs": [], "reviews": [], "owners": set(),
                                     "tests": {}, "worker": None})


def test_a_redraw_that_would_change_the_owners_part_is_still_refused(record_property, monkeypatch, github):
    """A redraw that would change the owner's words is still refused, the body unchanged.

    Proves 454.5.

    Saves the planned card on an owner's ask that ends with its own copy of the fold's end, the Definition of Done
    marker and a Definition of Done line, and checks it goes through with the words kept byte for byte and the
    Definition of Done last. Then saves a planned card that holds the marker itself and checks nothing is written, the
    save reports False and one comment on the issue says why."""
    record_property("proves", "454.5")
    ask = "My ask.\n\n</details>\n\n" + body.DONE + "\n**Definition of Done:** my own line"
    saved = run_card(monkeypatch, github, ask)
    assert saved is not None and body.ask(saved) == ask, "454.5: a good redraw changed or dropped the owner's words"
    above, below = saved.split(body.MARKER, 1)
    assert "Definition of Done" not in above and saved.rstrip().splitlines()[-1].startswith("**Definition of Done:** "), \
        f"454.5: the good redraw does not end with the card's Definition of Done below the fold:\n{saved}"
    assert "my own line" not in saved.rstrip().splitlines()[-1], \
        f"454.5: the owner's own Definition of Done line was taken as the card's:\n{saved}"
    github.saves.clear()
    github.comments.clear()
    bad = planned_top().replace(plan.CARD_END, f"A criterion quoting {body.MARKER}\n" + plan.CARD_END)
    with pytest.raises(body.Refused) as refused:
        body.redraw(saved, bad)
    assert body.save(REPO, NUMBER, saved, bad) is False, "454.5: a refused save did not report False"
    assert github.saves == [], "454.5: the body was written although the owner's words would change"
    assert len(github.comments) == 1 and str(refused.value) in (github.comments[0][1] or ""), \
        f"454.5: the refusal was not said once on the issue: {github.comments}"
