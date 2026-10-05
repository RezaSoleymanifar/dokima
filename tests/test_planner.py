import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import plan, planner  # noqa: E402

WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github/workflows/planner.yml")
PLAN = {"objective": "Slow calls return a job id", "criteria": ["A slow call returns a job id within 20 s", "The job id is unique"],
        "non_goals": ["No retries"], "scope": ["dokima/jobs.py"]}
TAGS = {"tests/test_jobs.py::test_id": ["9.1"], "tests/test_jobs.py::test_unique": ["9.2"]}


def write(tmp_path, name, content):
    (tmp_path / name).write_text(content if isinstance(content, str) else json.dumps(content))
    return str(tmp_path)


def steps():
    text = open(WORKFLOW).read()
    return text, text.split("      - ")


# 80.1: the plan lands in the issue in the format the rest of Dokima reads

def test_plan_is_written_into_the_issue_as_goal_criteria_and_scope(record_property):
    record_property("proves", "80.1")
    body = planner.render("9", "Make slow calls async.\n- [ ] Goal: old goal", PLAN, TAGS)
    assert body.startswith("- [ ] Objective: Slow calls return a job id\n  - [ ] Acceptance criteria: "), "80.1: not in the Objective / Acceptance criteria format"
    parsed = plan.parse(body)
    assert [g["text"] for g in parsed["goals"]] == ["Slow calls return a job id"], "80.1: goal not read back"
    crits = parsed["goals"][0]["criteria"]
    assert [c["text"] for c in crits] == PLAN["criteria"], "80.1: criteria not read back in order"
    assert crits[0]["verified_by"] == "`tests/test_jobs.py::test_id`", "80.1: criterion 1 not linked to its test"
    assert "**Non-goals:** No retries" in parsed["notes"] and "- `dokima/jobs.py`" in parsed["notes"], "80.1: non-goals or scope missing"


def test_owner_text_is_folded_and_never_read_as_plan(record_property):
    record_property("proves", "80.1")
    body = planner.render("9", "- [ ] Goal: old goal\n  - [ ] Done when: old", PLAN, TAGS)
    assert "<details><summary>Original issue</summary>" in body
    assert len(plan.parse(body)["goals"]) == 1, "80.1: the owner's old checkboxes were read as a second goal"


def test_planning_again_keeps_the_owner_text_once(record_property):
    record_property("proves", "80.1")
    first = planner.render("9", "Make slow calls async.", PLAN, TAGS)
    second = planner.render("9", first, PLAN, TAGS)
    assert second == first, "80.1: a second plan nested or lost the owner's original text"


def test_without_non_goals_there_is_no_non_goals_line(record_property):
    record_property("proves", "80.1")
    assert "Non-goals" not in planner.render("9", "x", dict(PLAN, non_goals=[]), TAGS)


def test_only_a_code_owners_plan_label_starts_it_and_the_planner_holds_no_key(record_property):
    record_property("proves", "80.1")
    text, parts = steps()
    assert "if: github.event.label.name == 'plan'" in text
    assert "only a code owner's label starts the planner" in text
    agent = next(p for p in parts if p.startswith("name: Planner"))
    assert "GH_TOKEN" not in agent and "DOKIMA_APP_KEY" not in agent, "80.1: the planner step can reach GitHub"
    names = [p.split("\n")[0] for p in parts]
    assert names.index("name: Check what the planner handed back") < names.index("id: app"), "80.1: key minted before the check"
    assert names.index("name: Planner (Claude Code)") < names.index("id: app"), "80.1: key minted before the planner ran"


# 80.2: tests come with the plan, each tagged with a criterion of the plan

def test_good_plan_with_a_test_per_criterion_passes(record_property):
    record_property("proves", "80.2")
    assert planner.problems("9", PLAN, ["tests/test_jobs.py"], TAGS) == []


def test_criterion_without_a_test_is_rejected(record_property):
    record_property("proves", "80.2")
    bad = planner.problems("9", PLAN, ["tests/test_jobs.py"], {"tests/test_jobs.py::test_id": ["9.1"]})
    assert bad == ["criterion 9.2 has no test"], f"80.2: got {bad}"


def test_test_for_a_criterion_not_in_the_plan_is_rejected(record_property):
    record_property("proves", "80.2")
    bad = planner.problems("9", PLAN, ["tests/test_jobs.py"], dict(TAGS, **{"tests/test_jobs.py::test_x": ["9.3", "4.1"]}))
    assert "tests/test_jobs.py::test_x proves 9.3, which is not a criterion of this plan" in bad
    assert "tests/test_jobs.py::test_x proves 4.1, which is not a criterion of this plan" in bad


def test_changes_outside_tests_or_no_tests_are_rejected(record_property):
    record_property("proves", "80.2")
    assert "dokima/jobs.py is outside tests/; the planner may only write tests" in planner.problems("9", PLAN, ["tests/t.py", "dokima/jobs.py"], TAGS)
    assert "the plan came with no tests" in planner.problems("9", PLAN, [], {})


def test_tags_are_read_from_each_test(record_property):
    record_property("proves", "80.2")
    src = 'def test_a(record_property):\n    record_property("proves", "9.1")\n\ndef test_b(record_property):\n    record_property("proves", "9.2")\n'
    assert planner.test_tags(["tests/t.py"], read=lambda p: src) == {"tests/t.py::test_a": ["9.1"], "tests/t.py::test_b": ["9.2"]}


def test_changed_files_counts_committed_and_new_files_since_the_start(record_property, tmp_path, monkeypatch):
    record_property("proves", "80.2")
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout
    git("init", "-q"); git("config", "user.name", "t"); git("config", "user.email", "t@t")
    (tmp_path / "a.py").write_text("x"); git("add", "-A"); git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD").strip()
    (tmp_path / "tests").mkdir(); (tmp_path / "tests/t1.py").write_text("x"); git("add", "-A"); git("commit", "-qm", "c")
    (tmp_path / "tests/t2.py").write_text("x")
    monkeypatch.chdir(tmp_path)
    assert planner.changed_files(base) == ["tests/t1.py", "tests/t2.py"], "80.2: committed or new test files missed"


# 80.3: the planner ends with exactly one of a plan or a question; anything else posts nothing

def test_a_question_is_read_as_a_question(record_property, tmp_path):
    record_property("proves", "80.3")
    assert planner.read_output(write(tmp_path, "question.md", "Split into two issues, yes or no?\n")) == ("question", "Split into two issues, yes or no?")


def test_a_plan_is_read_as_a_plan(record_property, tmp_path):
    record_property("proves", "80.3")
    kind, p = planner.read_output(write(tmp_path, "plan.json", {k: v for k, v in PLAN.items() if k != "non_goals"}))
    assert kind == "plan" and p["non_goals"] == [], "80.3: optional non-goals not defaulted"


@pytest.mark.parametrize("files, why", [
    ({}, "neither"),
    ({"plan.json": PLAN, "question.md": "Why?"}, "both"),
    ({"question.md": "I am not sure."}, "ending in '?'"),
    ({"plan.json": "{not json"}, "not valid JSON"),
    ({"plan.json": dict(PLAN, criteria=[])}, "criteria"),
    ({"plan.json": dict(PLAN, scope="dokima/jobs.py")}, "scope"),
    ({"plan.json": dict(PLAN, objective=" ")}, "objective"),
])
def test_garbled_output_is_rejected_with_its_reason(record_property, tmp_path, files, why):
    record_property("proves", "80.3")
    for name, content in files.items():
        write(tmp_path, name, content)
    with pytest.raises(planner.Garbled, match=why):
        planner.read_output(str(tmp_path))


def test_rejected_output_fails_the_run_and_posts_nothing(record_property, tmp_path, monkeypatch, capsys):
    record_property("proves", "80.3")
    calls = []
    monkeypatch.setattr(planner, "gh", lambda *a, **k: calls.append(a))
    assert planner.main(["x", "post", "9", write(tmp_path, "question.md", "no question here")]) == 1
    assert calls == [], "80.3: something was posted for rejected output"
    assert "::error title=Planner output rejected::" in capsys.readouterr().out


def test_a_question_is_posted_as_a_comment_and_the_body_is_untouched(record_property, tmp_path, monkeypatch):
    record_property("proves", "80.3")
    calls = []
    monkeypatch.setattr(planner, "gh", lambda *a, **k: calls.append(a) or "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    assert planner.main(["x", "post", "9", write(tmp_path, "question.md", "Which way?")]) == 0
    assert [c[:2] for c in calls] == [("issue", "comment")], f"80.3: expected one comment, got {calls}"
    assert calls[0][-1].endswith("Which way?")
