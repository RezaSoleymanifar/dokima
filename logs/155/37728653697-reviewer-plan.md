# reviewer (plan) for #155

Run: https://github.com/dokima-dev/dokima/actions/runs/37728653697

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null; ls in
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #155: Plan checker: new tests are checked as new, renames as changes
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 2</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** Every new test in a plan has a one-sentence summary and fails today, and renaming an older test is treated as a change with a reason.
> 
> **Context:** dokima/planner.py test_changes sees a rename as one deleted plus one added test (the false rejection on #138). Nothing reads docstrings or runs the new tests today. A rename is decided by code, not guessed from labels: a test whose source is unchanged apart from its name is a rename. The planner only writes tests, so the working tree is today's code. Builds on story 1's handling of named tests. The owner confirmed (answer 2 on the issue) that a new test which fails because the code it needs does not exist yet counts as failing today. Changed and deleted older tests already need a reason (dokima/planner.py problems, the 'older' list); that check stays as it is.
> 
> **Acceptance criteria:**
> - A new test with no docstring, or whose docstring's first line is not one plain sentence on one line (one sentence, ending in '.', '?' or '!'), is rejected, and the reason names the test. ([source](https://github.com/dokima-dev/dokima/issues/139))
> - Every new test is run on today's 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_new_test_check.py; git show HEAD -- tests/test_plan_check.py
```

> commit 53370c71aef3835c80e049dc788bf2e563f022b4
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 04:40:52 2026 +0000
> 
>     planner for #155 (run 37728033587)
> 
>  tests/test_new_test_check.py | 216 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_check.py     |   5 +-
>  2 files changed, 219 insertions(+), 2 deletions(-)
> """The planner check (#155): new tests need a one-sentence summary and must fail today; a rename is a change.
> 
> Every test here runs `python3 -m dokima.planner check 9 OUT` through planner.main, inside the temp git repo of the
> `check` fixture of tests/test_plan_check.py: one older test at the starting commit, the planner's tests on top, and the
> good story STORY, which names tests/test_jobs.py::test_id and ::test_unique. Each test rewrites the planner's files in
> that repo, runs the check, and reads back the exit code and the reason saved for the issue.
> """
> import json
> import os
> import signal
> import subprocess
> import sys
> import time
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import planner  # noqa: E402
> from tests.test_plan_check import ROOT, STORY, check  # noqa: E402,F401
> 
> 
> def jobs(id_doc='"""A slow call returns a job id."""', id_body='assert False, "9.1: no job id yet"',
>          unique_doc='"""Job ids never repeat."""', unique_body='assert False, "9.2: no job ids yet"', top=""):
>     """The planner's tests/test_jobs.py, with the two tests STORY name

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,120p tests/test_plan_check.py; wc -l dokima/planner.py; grep -n "def \|older\|test_changes\|NEW_TEST\|subprocess\|pytest" dokima/planner.py | head -80
```

> """The planner check (#154): only real plans, sources on this issue, named tests that exist under this plan's criteria.
> 
> Every test here runs the check the way the agent workflow runs it, `python3 -m dokima.planner check N OUT`, through
> planner.main, inside a temp git repo that holds one older test at the starting commit and the planner's new tests on
> top. A good plan passes (exit 0); each broken one fails (exit 1) and its reason, saved to OUT/rejected.txt for the
> issue, is read back. GITHUB_REPOSITORY is set to o/r and the issue is #9, so this issue's link is
> https://github.com/o/r/issues/9.
> """
> import copy
> import json
> import os
> import re
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import planner  # noqa: E402
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> ISSUE = "https://github.com/o/r/issues/9"
> OLD_TESTS = ('def test_old(record_property):\n    """An older test, already in the repo."""\n'
>              '    record_property("proves", "50.1")\n    assert True\n')
> # The planner's new tests fail today, as every new test must (#155): the job code they need does not exist yet.
> NEW_TESTS = ('def test_id(record_property):\n    """A slow call returns a job id."""\n'
>              '    record_property("proves", "9.1")\n    assert False, "9.1: no job id yet"\n\n\n'
>              'def test_unique(record_property):\n    """Job ids never repeat."""\n'
>              '    record_property("proves", "9.2")\n  

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_new_test_check.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|passed|failed" ; timeout 600 python -m pytest -q 2>&1 | tail -5
```

> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> FAILED tests/test_new_test_check.py::test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it[no docstring] - AssertionError: 155.1: a new test with the docstring None was accepted; it needs a one-sentence first line
> FAILED tests/test_new_test_check.py::test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it[empty] - AssertionError: 155.1: a new test with the docstring '""""""' was accepted; it needs a one-sentence first line
> FAILED tests/test_new_test_check.py::test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it[no end mark] - AssertionError: 155.1: a new test with the docstring '"""A slow call returns a job id"""' was accepted; it needs a one-sentence first line
> FAILED tests/test_new_test_check.py::test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it[two sentences] - AssertionError: 155.1: a new test with the docstring '"""Job ids never repeat. They are unique."""' was accepted; it needs a one-sentence first line
> FAILED tests/te

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "assert True\|write_text\|check(" tests/test_plan_check.py tests/test_questions.py | grep -v "^.*#" | head -60; grep -rln "planner.main\|from tests.test_plan_check" tests/
```

> tests/test_questions.py:33:def test_a_question_with_its_assumption_passes_the_check(record_property, check, base):
> tests/test_questions.py:42:        rc, why = check({"plan.json": p}, "170.1")
> tests/test_questions.py:71:    rc, why = check({"plan.json": with_questions(base, qs)}, "170.1")
> tests/test_questions.py:96:        (out / "plan.json").write_text(json.dumps({"kind": kind, "user_story": "Slow calls return a job id.",
> tests/test_plan_check.py:24:             '    record_property("proves", "50.1")\n    assert True\n')
> tests/test_plan_check.py:49:def check(tmp_path, monkeypatch):
> tests/test_plan_check.py:62:    (repo / "tests" / "test_old.py").write_text(OLD_TESTS)
> tests/test_plan_check.py:69:    (repo / "tests" / "test_jobs.py").write_text(NEW_TESTS)
> tests/test_plan_check.py:76:            (out / name).write_text(content if isinstance(content, str) else json.dumps(content))
> tests/test_plan_check.py:120:        rc, why = check({"plan.json": good}, "154.1")
> tests/test_plan_check.py:122:    rc, why = check(files, "154.1")
> tests/test_plan_check.py:177:        rc, why = check({"plan.json": good}, "154.2")
> tests/test_plan_check.py:179:    rc, why = check({"plan.json": story(lambda s: s["acceptance_criteria"][1].update(source=source))}, "154.2")
> tests/test_plan_check.py:204:        rc, why = check({"plan.json": good}, "154.2")
> tests/test_plan_check.py:207:        rc, why = check({"plan.json": feature(lambda f: f["stories"][k]["acceptance_criteria"][0].update(source=source))}, "1

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "planner.main\|planner\.problems\|test_changes(\|def test_\|assert True\|\"check\"" tests/test_planner.py tests/test_agent.py | head -60; sed -n 195,270p dokima/planner.py; sed -n 300,371p dokima/planner.py
```

> tests/test_planner.py:32:def test_plan_is_written_into_the_issue_as_goal_criteria_and_scope(record_property):
> tests/test_planner.py:44:def test_owner_text_is_folded_and_never_read_as_plan(record_property):
> tests/test_planner.py:51:def test_planning_again_keeps_the_owner_text_once(record_property):
> tests/test_planner.py:58:def test_without_non_goals_there_is_no_non_goals_line(record_property):
> tests/test_planner.py:63:def test_only_a_code_owners_plan_label_starts_it_and_the_planner_holds_no_key(record_property):
> tests/test_planner.py:81:def test_good_plan_with_a_test_per_criterion_passes(record_property):
> tests/test_planner.py:83:    assert planner.problems("9", dict(PLAN, test_changes={}), ["tests/test_jobs.py"], tc()) == []
> tests/test_planner.py:86:def test_criterion_without_a_test_is_rejected(record_property):
> tests/test_planner.py:88:    bad = planner.problems("9", dict(PLAN, test_changes={}), ["tests/test_jobs.py"], tc({"tests/test_jobs.py::test_id": ["9.1"]}))
> tests/test_planner.py:92:def test_test_for_a_criterion_not_in_the_plan_is_rejected(record_property):
> tests/test_planner.py:94:    bad = planner.problems("9", dict(PLAN, test_changes={}), ["tests/test_jobs.py"], tc(dict(TAGS, **{"tests/test_jobs.py::test_x": ["9.3", "4.1"]})))
> tests/test_planner.py:99:def test_changes_outside_tests_or_no_tests_are_rejected(record_property):
> tests/test_planner.py:102:    assert "dokima/jobs.py is outside tests/; the planner may only write tests" in planner.problems("9", plan_, ["test

**Agent:** I'm checking whether the planner's new rules would break older tests that the worker isn't allowed to change, and then I'll write the review.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 85,120p tests/test_questions.py; sed -n 225,245p tests/test_planner.py; grep -n "TEST_DEF\|PROVES =" dokima/planner.py
```

> Draws a planner card from a record with two questions and checks each question appears on one line together
>     with its own assumption, never as raw data. Then draws a card from a record whose questions also carry options
>     and a recommendation and checks neither appears in the part the owner reads.
>     """
>     record_property("proves", "170.2")
>     import json
>     out = tmp_path / "out"
>     out.mkdir()
> 
>     def rec(qs):
>         (out / "plan.json").write_text(json.dumps({"kind": kind, "user_story": "Slow calls return a job id.",
>                                                    "feature": "Slow calls run as jobs.", "stories": [], "questions": qs}))
>         return agent.build_record("planner", "", str(out), "", True, {"run_id": "1", "run": "https://x/run/1"})
> 
>     text = readable(rec([GOOD, SECOND]))
>     for q in (GOOD, SECOND):
>         lines = [l for l in text.splitlines() if q["question"] in l]
>         assert lines, f"170.2: the card does not show the question {q['question']!r}:\n{text}"
>         assert any(q["assumption"] in l for l in lines), f"170.2: the card does not show {q['question']!r} with its assumption {q['assumption']!r}:\n{text}"
>     for raw in ("{'", "'question'", "'assumption'", '"question"', '"assumption"'):
>         assert raw not in text, f"170.2: the card shows a question as raw data ({raw!r}):\n{text}"
>     text = readable(rec([dict(GOOD, options=["Numbers-zq", "Strings-zq"], recommendation="Pick-strings-zq")]))
>     assert GOOD["question"] in text and GO

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned three criteria (a one-sentence summary on every new test, every new test fails today, a rename is a change with a reason under its old name) and two limits (an unreadable test file is rejected by name, a test still running after 60 s is stopped and rejected).",
          "Wrote tests/test_new_test_check.py, one test file covering all five, and made the sample new tests in tests/test_plan_check.py fail today, giving a reason."],
  "decided": ["A test that is renamed and also rewritten counts as new; a test moved to another file is not a rename.",
              "Changed or deleted older tests keep today's rule and are not held to the new-test rules."],
  "open": []},
 "verdict": "block",
 "summary": "The tests prove new tests are held to the new rules, but none proves a changed older test is left alone, so a check that also rejects every changed older test that passes today or has no summary would pass them.",
 "blockers": [{"id": "B1", "criterion": "155.2",
   "test": "tests/test_new_test_check.py::test_a_new_test_that_passes_or_skips_today_is_rejected_saying_so",
   "problem": "155.1 and 155.2 apply only to new tests, and the plan's out_of_scope says changed older tests are not held to these rules. No test has a changed older test (with its reason) that passes today or has no docstring. A check that also runs or reads changed older tests would reject good plans that touch an older test, and every 155 test would still pass. That is the 'too broad' direction of the one question.",
   "evidence": "dokima/planner.py:234 proving(tc) returns added and changed tests together. It is the helper a worker would most likely use to pick 'the new tests', and it would sweep in changed older tests. In the `check` and `legacy` fixtures the only older tests that change are renamed ones (155.3); the existing tests that touch changed older tests (tests/test_planner.py:198, :208) c
```

> (Bash completed with no output)

**Agent:** I blocked the plan for #155 and sent it back to the planner. Both hand-back checks pass on `/tmp/dokima-out/review.json`.

**What holds up:** I ran the planner's new tests on today's code: 15 of them fail, and each fails because the feature is missing, not because of a crash or a bad path. The three criteria and two limits match the issue. The planner also changed the sample tests in `tests/test_plan_check.py` so they fail today, and gave its reason. That change is needed, because once this lands a plan whose new tests already pass will be rejected.

**Blocker B1 (planner to fix, under 155.2):** Nothing tests that a changed older test is left alone. The plan says only new tests must have a one-sentence summary and fail today, and that changed older tests keep today's rule. But no test has a changed older test that passes today or has no summary. A check that also judged changed older tests would wrongly reject good plans and still pass every test here. This is a real risk: the helper that lists the planner's tests (`dokima/planner.py:234`) returns new and changed tests together, so a worker reusing it would likely sweep in changed older tests. The fix is one more case: change the body of an older test (keeping its name, with no summary, still passing) and give a reason. The check should pass.

**Notes, not blockers (both on the 60-second limit test):**
- A limit written into the code under 40 seconds, ignoring the 60-second setting, would still pass the test.
- The test doesn't check that the quick-failing test is left out of the reason, so a check that names every new test when time runs out would pass.
