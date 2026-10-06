"""An agent's hand-back is checked by code before anyone else sees it: well formed passes, every malformation is named."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, fence  # noqa: E402

GOOD_REVIEW = {"stage": "plan", "round": 1, "verdict": "block", "summary": "One test is missing.",
               "blockers": [{"id": "B1", "criterion": "9.1", "test": None, "problem": "No good-case test.",
                             "evidence": "18 passed against a stub.", "fix": "Add one."}],
               "notes": [], "outside_plan": [], "resolved": []}
GOOD_WORK = {"summary": "Cause and change.", "criteria": {"9.1": "dokima/x.py, parse()"},
             "evidence": "pytest -q: 12 passed", "replies": [{"blocker": "B1", "answer": "fixed", "why": "Added it."}]}


def test_a_good_review_passes_and_each_malformation_is_named(record_property):
    """A well-formed review has no problems; an approve with blockers, a block without, a bad stage and a bare blocker are each named."""
    record_property("proves", "agent.1")
    assert agent.problems_review(GOOD_REVIEW) == []
    assert agent.problems_review({**GOOD_REVIEW, "verdict": "approve"}) == ["an approve has no blockers"]
    assert agent.problems_review({**GOOD_REVIEW, "blockers": []}) == ["a block needs at least one blocker"]
    assert "stage must be" in agent.problems_review({**GOOD_REVIEW, "stage": "x"})[0]
    bare = agent.problems_review({**GOOD_REVIEW, "blockers": [{"id": "B1"}]})
    assert {"blocker B1 has no criterion", "blocker B1 has no evidence", "blocker B1 has no fix"} <= set(bare)
    assert agent.problems_review({**GOOD_REVIEW, "notes": [{}] * 4}) == ["at most three notes"]


def test_a_good_work_passes_and_each_malformation_is_named(record_property):
    """A well-formed work.json has no problems; missing criteria, missing evidence and a reply without a reason are each named."""
    record_property("proves", "agent.2")
    assert agent.problems_work(GOOD_WORK) == []
    assert agent.problems_work({**GOOD_WORK, "criteria": {}}) == ["criteria must give one line per criterion"]
    assert "evidence is empty" in agent.problems_work({**GOOD_WORK, "evidence": " "})[0]
    assert "reply to B1" in agent.problems_work({**GOOD_WORK, "replies": [{"blocker": "B1", "answer": "maybe"}]})[0]


def test_check_fails_closed_on_missing_or_broken_files(record_property, tmp_path, capsys):
    """A missing file or invalid JSON is a failure with its reason, never a pass; a good file passes."""
    record_property("proves", "agent.3")
    assert agent.check("review", str(tmp_path / "none.json")) == 1
    (tmp_path / "bad.json").write_text("{not json")
    assert agent.check("work", str(tmp_path / "bad.json")) == 1
    (tmp_path / "ok.json").write_text(json.dumps(GOOD_REVIEW))
    assert agent.check("review", str(tmp_path / "ok.json")) == 0
    assert "missing" in capsys.readouterr().out


def test_the_fence_reads_scope_from_plan_json(record_property, tmp_path, monkeypatch):
    """Given plan.json, the fence uses its scope list exactly."""
    record_property("proves", "agent.4")
    plan = tmp_path / "plan.json"
    plan.write_text(json.dumps({"scope": ["app.py"]}))
    seen = {}
    monkeypatch.setattr(fence, "fence", lambda base, scope: seen.setdefault("scope", scope) and [])
    fence.main(["fence", "BASE", str(plan)])
    assert seen["scope"] == ["app.py"]


def test_only_the_planner_asks_and_its_questions_are_checked(record_property):
    """A full planner question passes; a missing '?', fewer than two options or an unoffered pick is named; review and work may not ask."""
    record_property("proves", "agent.5")
    q = {"question": "Split it?", "options": ["Yes", "No"], "recommendation": "Yes"}
    assert agent.problems_questions([q]) == []
    assert agent.problems_questions([{**q, "question": "Split it."}]) == ["question 1 must be one question ending in '?'"]
    assert agent.problems_questions([{**q, "options": ["Yes"]}]) == ["question 1 needs at least two options"]
    assert agent.problems_questions([{**q, "recommendation": "Maybe"}]) == ["question 1's recommendation must be one of its options"]
    assert agent.problems_review({**GOOD_REVIEW, "questions": [q]}) == ["the reviewer never asks the owner; escalate on round three instead"]
    assert agent.problems_work({**GOOD_WORK, "questions": [q]}) == ["the worker never asks the owner; the plan is the contract"]
