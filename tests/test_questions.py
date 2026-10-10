"""A plan record's questions show each with its assumption, nothing else (#170).

Since #300 a planner raises its questions as raises, and code rejects the old questions field; plans posted before
that still carry it, and their comments are still drawn by agent.render, the code that writes every record comment.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
GOOD = {"question": "Should job ids be numbers?", "assumption": "The plan assumes they are strings."}
SECOND = {"question": "Should a failed run move to Needs you?", "assumption": "The plan assumes it does."}


def readable(rec):
    """The part of a record comment the owner reads: everything above the folded full record."""
    # The field icons code draws (issue #234) are not words; their alt text names the field, as in alt="question".
    return re.sub(r"<img [^>]*>", "", agent.render(rec).split("<details><summary>Full record</summary>")[0])


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
        (out / "plan.json").write_text(json.dumps({"kind": kind, "summary": "Slow calls hand back a job id.", "user_story": "Slow calls return a job id.",
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
