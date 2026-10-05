import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card, plan  # noqa: E402

REPO = "o/r"
ISSUE = {"number": 93, "url": "https://github.com/o/r/issues/93", "approved_at": None, "changes": []}
OLD = ("- [ ] Goal: show a card\n"
       "  - [ ] Done when: first thing works\n"
       "    Verified by: a test that runs the first thing\n"
       "  - [ ] Done when: second thing works\n"
       "    Verified by: another test\n")
NEW = ("- [ ] Objective: show a card\n"
       "  - [ ] Acceptance criteria: first thing works\n"
       "    Verified by: a test that runs the first thing\n"
       "  - [ ] Acceptance criteria: second thing works\n"
       "    Verified by: another test\n")
CONTEXT = ("<details><summary><b>Context</b></summary>\n\n"
           "From the [design chat](https://claude.ai/chat/x):\n\n"
           "- [turn 5] the owner wants **Goal: nothing** to stay a note, not a plan\n"
           "- [ ] Acceptance criteria: a line that looks like a criterion but sits inside the fold\n\n"
           "</details>")


def render(body):
    return card.render(REPO, ISSUE, plan.parse(body), None, [], None)


def test_card_says_objective_and_acceptance_criteria(record_property):
    record_property("proves", "93.1")
    out = render(NEW)
    assert "**Objective: show a card**" in out, "93.1: the card does not label the objective"
    assert "Acceptance criteria: first thing works" in out, "93.1: criteria are not labelled Acceptance criteria"
    assert "**Goal:" not in out and " Criteria:" not in out, "93.1: the card still uses the old words"


def test_old_and_new_words_read_as_the_same_plan(record_property):
    record_property("proves", "93.2")
    old, new = plan.parse(OLD), plan.parse(NEW)
    assert old["goals"] == new["goals"], "93.2: old and new words give different plans"
    assert [c["text"] for c in new["goals"][0]["criteria"]] == ["first thing works", "second thing works"]
    assert new["goals"][0]["text"] == "show a card", "93.2: 'Objective:' was not stripped from the objective"
    # A card the new code wrote reads back as the same plan.
    assert plan.parse(render(NEW))["goals"] == new["goals"], "93.2: a new card does not read back"


def test_context_fold_is_kept_and_never_read_as_plan(record_property):
    record_property("proves", "93.3")
    body = NEW + "\n" + CONTEXT
    words = plan.parse(body)
    assert len(words["goals"]) == 1 and len(words["goals"][0]["criteria"]) == 2, "93.3: the Context fold was read as plan"
    rewritten = card.issue_body(render(body), words["notes"])
    assert CONTEXT in rewritten, "93.3: the Context fold changed when the card was rewritten"
    again = plan.parse(rewritten)
    assert again["goals"] == words["goals"] and CONTEXT in card.issue_body(render(rewritten), again["notes"]), \
        "93.3: the fold drifts after a second rewrite"
