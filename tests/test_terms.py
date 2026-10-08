import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import body, plan  # noqa: E402

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


def test_old_and_new_words_read_as_the_same_plan(record_property):
    record_property("proves", "93.2")
    old, new = plan.parse(OLD), plan.parse(NEW)
    assert old["goals"] == new["goals"], "93.2: old and new words give different plans"
    assert [c["text"] for c in new["goals"][0]["criteria"]] == ["first thing works", "second thing works"]
    assert new["goals"][0]["text"] == "show a card", "93.2: 'Objective:' was not stripped from the objective"


def test_context_fold_is_kept_and_never_read_as_plan(record_property):
    record_property("proves", "93.3")
    fold = NEW + "\n" + CONTEXT
    words = plan.parse(fold)
    assert len(words["goals"]) == 1 and len(words["goals"][0]["criteria"]) == 2, "93.3: the Context fold was read as plan"
    rewritten = body.redraw(body.redraw(fold, "card one"), "card two")
    assert CONTEXT in body.ask(rewritten), "93.3: the Context fold changed when the card was rewritten"
    assert plan.parse(body.ask(rewritten))["goals"] == words["goals"], "93.3: the fold drifts after a second rewrite"
