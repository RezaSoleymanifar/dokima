"""Planner questions are a question and its assumption, nothing else (#170).

The owner asked that every question the planner puts in plan.json be exactly two fields, the question and the reading
the plan assumed; that code reject anything else; that the card show only the question and the assumption; and that
the planner's prompt stop asking for options or a recommendation. The check is run the way the workflow runs it,
through planner.main inside a temp git repo (the `check` fixture of tests/test_plan_check.py); the card is drawn with
agent.render, the code that writes every record comment.
"""
import copy
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent  # noqa: E402
from tests.test_plan_check import FEATURE, STORY, check  # noqa: E402,F401

ROOT = os.path.join(os.path.dirname(__file__), "..")
GOOD = {"question": "Should job ids be numbers?", "assumption": "The plan assumes they are strings."}
SECOND = {"question": "Should a failed run move to Needs you?", "assumption": "The plan assumes it does."}


def with_questions(base, qs):
    """A copy of the good story or feature carrying the given questions."""
    p = copy.deepcopy(base)
    p["questions"] = qs
    return p


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
def test_a_question_with_its_assumption_passes_the_check(record_property, check, base):
    """A plan whose questions each give the question and the reading it assumed passes the check.

    Hands back a good story and a good feature with no questions, with one question, and with two, each question
    exactly a question and its assumption, and checks every one passes, so the rule never blocks a good plan.
    """
    record_property("proves", "170.1")
    for qs in (None, [GOOD], [GOOD, SECOND]):
        p = copy.deepcopy(base) if qs is None else with_questions(base, qs)
        rc, why = check({"plan.json": p}, "170.1")
        assert rc == 0 and not why, f"170.1: a {base['kind']} with questions {qs} was rejected: {why!r}"


BAD = [
    (["Should job ids be numbers? I planned for strings."], 1, "assumption", "a plain string"),
    ([{"question": GOOD["question"]}], 1, "assumption", "no assumption"),
    ([{"assumption": GOOD["assumption"]}], 1, "question", "no question"),
    ([{"question": GOOD["question"], "assumption": "  "}], 1, "assumption", "an empty assumption"),
    ([{"question": "", "assumption": GOOD["assumption"]}], 1, "question", "an empty question"),
    ([{"question": GOOD["question"], "assumption": 5}], 1, "assumption", "an assumption that is not text"),
    ([{"question": "Split it.", "assumption": GOOD["assumption"]}], 1, "?", "a question that asks nothing"),
    ([GOOD, dict(SECOND, options=["(A) Needs you", "(B) Red mark only"])], 2, "options", "options"),
    ([GOOD, dict(SECOND, recommendation="(A), the owner sees it without looking")], 2, "recommendation", "a recommendation"),
    ([dict(GOOD, options=["Yes", "No"], recommendation="Yes")], 1, "options", "options and a recommendation"),
    ([5], 1, "question", "a number"),
]


@pytest.mark.parametrize("base", [STORY, FEATURE], ids=["story", "feature"])
@pytest.mark.parametrize("qs, n, word, what", BAD, ids=[b[3] for b in BAD])
def test_a_question_that_is_anything_else_is_rejected_saying_which_and_why(record_property, check, base, qs, n, word, what):
    """A question that is not exactly a question and its assumption is rejected, naming the question and what is wrong.

    Hands back a good story or feature whose questions hold one bad entry (a plain string, a missing, empty or
    non-text field, a question with no '?', or extra options or a recommendation) and checks the check fails, its
    reason names that question by number and the field at fault.
    """
    record_property("proves", "170.1")
    rc, why = check({"plan.json": with_questions(base, qs)}, "170.1")
    assert rc == 1, f"170.1: a {base['kind']} whose question {n} has {what} was accepted"
    assert f"question {n}" in why, f"170.1: the reason does not name question {n}: {why!r}"
    assert word in why, f"170.1: the reason for {what} does not name {word!r}: {why!r}"


def readable(rec):
    """The part of a record comment the owner reads: everything above the folded full record."""
    return agent.render(rec).split("<details><summary>Full record</summary>")[0]


@pytest.mark.parametrize("kind", ["user_story", "feature"])
def test_the_card_shows_each_question_with_its_assumption_and_nothing_else(record_property, tmp_path, kind):
    """The card shows each question beside the reading the plan assumed, with no options and no recommendation.

    Draws a planner card from a record with two questions and checks each question appears on one line together
    with its own assumption, never as raw data. Then draws a card from a record whose questions also carry options
    and a recommendation and checks neither appears in the part the owner reads.
    """
    record_property("proves", "170.2")
    import json
    out = tmp_path / "out"
    out.mkdir()

    def rec(qs):
        (out / "plan.json").write_text(json.dumps({"kind": kind, "user_story": "Slow calls return a job id.",
                                                   "feature": "Slow calls run as jobs.", "stories": [], "questions": qs}))
        return agent.build_record("planner", "", str(out), "", True, {"run_id": "1", "run": "https://x/run/1"})

    text = readable(rec([GOOD, SECOND]))
    for q in (GOOD, SECOND):
        lines = [l for l in text.splitlines() if q["question"] in l]
        assert lines, f"170.2: the card does not show the question {q['question']!r}:\n{text}"
        assert any(q["assumption"] in l for l in lines), f"170.2: the card does not show {q['question']!r} with its assumption {q['assumption']!r}:\n{text}"
    for raw in ("{'", "'question'", "'assumption'", '"question"', '"assumption"'):
        assert raw not in text, f"170.2: the card shows a question as raw data ({raw!r}):\n{text}"
    text = readable(rec([dict(GOOD, options=["Numbers-zq", "Strings-zq"], recommendation="Pick-strings-zq")]))
    assert GOOD["question"] in text and GOOD["assumption"] in text, f"170.2: the card lost the question or its assumption:\n{text}"
    for extra in ("Numbers-zq", "Strings-zq", "Pick-strings-zq", "options", "recommendation"):
        assert extra not in text, f"170.2: the card shows {extra!r}, an option or a recommendation:\n{text}"


def test_the_prompt_asks_for_a_question_and_its_assumption_never_options_or_a_recommendation(record_property):
    """The planner's prompt never asks for options or a recommendation, and teaches a question and its assumption.

    Reads dokima/roles/planner.md: no line shows lettered options such as (A) or (B) or the word option, the only
    line that recommends anything is the concern example, the question example names the reading it assumed, and the
    hand-back section shows each question as {"question": "...?", "assumption": "..."}.
    """
    record_property("proves", "170.3")
    text = open(os.path.join(ROOT, "dokima", "roles", "planner.md")).read()
    lines = text.splitlines()
    lettered = [l for l in lines if re.search(r"\([A-E]\)", l)]
    assert not lettered, f"170.3: the prompt still shows lettered options: {lettered}"
    options = [l for l in lines if re.search(r"\boptions?\b", l, re.I)]
    assert not options, f"170.3: the prompt still mentions options: {options}"
    recommends = [l for l in lines if re.search(r"recommend", l, re.I) and not l.lstrip().startswith("- Concern:")]
    assert not recommends, f"170.3: the prompt still asks for a recommendation: {recommends}"
    example = [l for l in lines if l.lstrip().startswith("- Question:")]
    assert example, "170.3: the prompt lost its question example"
    assert all(re.search(r"assum", l, re.I) for l in example), f"170.3: the question example does not name the reading it assumed: {example}"
    flat = " ".join(text.split())
    assert re.search(r'"questions":\s*\[\s*\{\s*"question":\s*"[^"]*\?",\s*"assumption":\s*"[^"]*"\s*\}', flat), \
        "170.3: the hand-back section does not show each question as {\"question\": \"...?\", \"assumption\": \"...\"}"
