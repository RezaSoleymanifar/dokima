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
    """Plain questions pass; anything that is not a plain question is named; review and work may not ask."""
    record_property("proves", "agent.5")
    q = "Should a failed run move its card to Needs you? I planned for yes."
    assert agent.problems_questions([q, "Which board view?"]) == []
    assert agent.problems_questions(["Split it."]) == ["question 1 must be a plain question with a '?'"]
    assert agent.problems_questions([{"question": "Split it?"}]) == ["question 1 must be a plain question with a '?'"]
    assert agent.problems_review({**GOOD_REVIEW, "questions": [q]}) == ["the reviewer never asks the owner; escalate on round three instead"]
    assert agent.problems_work({**GOOD_WORK, "questions": [q]}) == ["the worker never asks the owner; the plan is the contract"]


def test_records_are_numbered_kept_and_only_passed_plans_count(record_property, tmp_path, monkeypatch):
    """Each run adds the next numbered record; a rejected plan is kept as history but the newest passed plan is the plan."""
    record_property("proves", "agent.6")
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "plan.json").write_text(json.dumps({"kind": "user_story", "user_story": "first"}))
    p1 = agent.record(7, "planner", "", str(out), "", True, {"run_id": "1"})
    (out / "plan.json").write_text(json.dumps({"kind": "user_story", "user_story": "second, rejected"}))
    p2 = agent.record(7, "planner", "", str(out), "criterion 7.2 has no test\n", False, {"run_id": "2"})
    (out / "review.json").write_text(json.dumps(GOOD_REVIEW))
    p3 = agent.record(7, "reviewer", "plan", str(out), "", True, {"run_id": "3"})
    assert [os.path.basename(p) for p in (p1, p2, p3)] == ["01-planner.json", "02-planner.json", "03-reviewer-plan.json"]
    assert [r["run_id"] for _, r in agent.records(7)] == ["1", "2", "3"]
    assert agent.latest(7, "planner")["handback"]["user_story"] == "first", "a rejected plan was treated as the plan"
    assert agent.latest(7, "planner", passed=False)["check"]["problems"] == ["criterion 7.2 has no test"]
    assert agent.latest(7, "worker") is None


def test_a_missing_hand_back_is_recorded_as_missing(record_property, tmp_path, monkeypatch):
    """A run that handed back nothing still leaves a record saying so, never an empty or invented hand-back."""
    record_property("proves", "agent.7")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "out").mkdir()
    path = agent.record(7, "worker", "", str(tmp_path / "out"), "work.json is missing\n", False, {})
    r = json.load(open(path))
    assert "work.json" in r["handback"]["missing"] and r["check"] == {"passed": False, "problems": ["work.json is missing"]}


def test_the_models_used_come_from_the_session_log(record_property, tmp_path):
    """The record names every model that appears in the run's session log, so a wrong model is visible and can fail the run."""
    record_property("proves", "agent.8")
    log = tmp_path / "logs" / "proj"
    log.mkdir(parents=True)
    (log / "s.jsonl").write_text("\n".join(json.dumps(x) for x in [
        {"message": {"model": "claude-opus-5-5"}}, {"type": "user"}, {"message": {"model": "claude-sonnet-5-5"}}]) + "\nnot json\n")
    assert agent.models_used(str(tmp_path / "logs")) == ["claude-opus-5-5", "claude-sonnet-5-5"]
    assert agent.models_used(str(tmp_path / "none")) == []


def test_the_worker_starts_only_on_a_plan_the_reviewer_approved(record_property, tmp_path, monkeypatch):
    """No review, a blocking review, or an approval of an older plan keeps the worker out; an approval of the newest plan lets it in."""
    record_property("proves", "agent.9")
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "plan.json").write_text(json.dumps({"kind": "user_story"}))
    agent.record(8, "planner", "", str(out), "", True, {})
    assert not agent.approved(8), "a plan with no review let the worker in"
    (out / "review.json").write_text(json.dumps(GOOD_REVIEW))
    agent.record(8, "reviewer", "plan", str(out), "", True, {})
    assert not agent.approved(8), "a blocking review let the worker in"
    (out / "review.json").write_text(json.dumps({**GOOD_REVIEW, "verdict": "approve", "blockers": []}))
    agent.record(8, "reviewer", "plan", str(out), "", True, {})
    assert agent.approved(8), "an approved newest plan kept the worker out"
    agent.record(8, "planner", "", str(out), "", True, {})
    assert not agent.approved(8), "an approval of an older plan let the worker in on a newer one"
