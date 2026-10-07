# reviewer (plan) for #154

Run: https://github.com/dokima-dev/dokima/actions/runs/37549770642

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #154: Plan checker: kinds, sources and named tests
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 1</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tests are real and filed under the plan's own criteria.
> 
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_kind raises TypeError). Older tests in tests/test_planner.py that hand back question.md or the old shape will need changing, with reasons. The repo comes from GITHUB_REPOSITORY. The owner's newer words (comment of 2026-10-06T20:49) settle one flow: the planner always pl

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_plan_check.py; wc -l dokima/planner.py
```

> commit b3eaad3858e02b1097fc1ac85663ddad7a05310b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Tue Oct 6 23:26:31 2026 +0000
> 
>     planner for #154 (run 37546108743)
> 
>  tests/test_plan_check.py     | 248 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py     |  14 ++-
>  tests/test_planner.py        |  39 +++----
>  tests/test_planner_prompt.py |   2 +-
>  4 files changed, 267 insertions(+), 36 deletions(-)
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
>              '    record_property("proves

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_plan_check.py 2>&1 | grep -E "FAILED|passed|failed" | sed 's/ - /\n   /' | cut -c1-300
```

> files = {'plan.json': {'kind': 'question', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A sl...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'essay', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A slow ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> p = {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, 'source': 'htt...al': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A ...comment-123456'}], 'non_functional': [{'text': 'A failed call says why.', 'why': 3, 'principle': 'fail closed'}], ...}}
> p = {'kind

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_plan_check.py -rA 2>&1 | grep PASSED; python3 -m pytest -q 2>&1 | tail -3; cat dokima/planner.py
```

> PASSED tests/test_plan_check.py::test_a_test_filed_under_a_key_that_is_not_a_criterion_is_rejected_and_named[another issue, new test]
> PASSED tests/test_plan_check.py::test_a_test_filed_under_a_key_that_is_not_a_criterion_is_rejected_and_named[past the last, new test]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[criteria not a list]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[user_story]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[scope]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[out_of_scope]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[tests]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[test_changes]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[questions]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[kind]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[plan.json a list]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[plan.json a string]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[plan.json a number]
> FAILED tests/test_plan_check.py::test_a_value_of_the_wrong_

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_plan_shape.py tests/test_planner.py tests/test_planner_prompt.py; grep -n "question\|Exactly one kind\|End with exactly" dokima/roles/planner.md; grep -n "question\|plan.json" .github/workflows/planner.yml
```

> commit b3eaad3858e02b1097fc1ac85663ddad7a05310b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Tue Oct 6 23:26:31 2026 +0000
> 
>     planner for #154 (run 37546108743)
> 
> diff --git a/tests/test_plan_shape.py b/tests/test_plan_shape.py
> index 935fcef..e067326 100644
> --- a/tests/test_plan_shape.py
> +++ b/tests/test_plan_shape.py
> @@ -1,7 +1,7 @@
>  """The planner's hand-back: one plan.json in the agreed shape, read by code, shown on the run page.
>  
> -Covers #138: the prompt teaches the agreed terms and examples, code accepts the story, feature and
> -question kinds, test labels come from what the plan declares, and every run shows what it handed back.
> +Covers #138: the prompt teaches the agreed terms and examples, code accepts the story and feature
> +kinds (#154 took the lone question away), test labels come from what the plan declares, and every run shows what it handed back.
>  """
>  import json
>  import os
> @@ -65,7 +65,7 @@ def test_a_story_is_read_with_criteria_then_non_functional(record_property, tmp_
>      (lambda s: s["non_functional"][0].pop("why"), "text and why"),
>      (lambda s: s.pop("tests"), "tests as a map"),
>      (lambda s: s.update(user_story=" "), "user_story"),
> -    (lambda s: s.update(kind="essay"), "kind must be"),
> +    (lambda s: s.update(kind="essay"), "user_story"),
>  ])
>  def test_a_story_missing_a_rule_is_rejected_with_why(record_property, tmp_path, change, why):
>      """A story with a criterion with no source, a requirement w

**Agent:** Tests run as expected: 25 fail today for the right reasons. One gap found in the prompt test. Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned four criteria and one non-functional requirement, with 8 new tests in tests/test_plan_check.py that fail today", "Changed or deleted 9 older tests that handed back question.md or the old plan shape, each with a reason"],
  "decided": ["The question kind goes away from the check, the planner's prompt and the planner workflow", "The source check covers a user_story's criteria only, not a feature's stories"],
  "open": ["Asks the owner whether a feature's stories should also have their sources checked"]},
 "verdict": "block",
 "summary": "The plan matches the ask and its tests fail today for the right reasons, but the prompt test would still pass if the prompt kept its 'One question for the owner' section, so 154.1 is not fully proven.",
 "blockers": [{"id": "B1", "criterion": "154.1",
   "test": "tests/test_plan_check.py::test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question",
   "problem": "154.1 promises the planner's prompt no longer offers ending with a lone question. The test only checks the example kinds, the 'Exactly one kind:' sentence and the 'End with exactly one of' sentence. A prompt that keeps the whole '# One question for the owner' section, which tells the planner to hand back one question with options and a recommendation, still passes.",
   "evidence": "dokima/roles/planner.md:103-106 holds '# One question for the owner / Only if you cannot plan without the owner's answer. One full question ending in \"?\", with options...'. If you edit only lines 6, 111 and 126, the test goes green with that section still there. The changed tests/test_planner_prompt.py only stops requiring the section. Nothing checks that it is gone.",
   "fix": "In the same test, assert that the prompt has no 'One question for the owner' heading (for example, no line starting with '#' that contains 'One question'), with a 154.1 message."}],
 "notes": [
  {"text": "Th
```

> (Bash completed with no output)

`7. Bash`
```
sed -i 's/with 8 new tests/with 7 new tests/' /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo ok
```

> ok

**Agent:** I'm blocking the plan for issue #154 on one gap. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

The plan covers the four criteria and the wrong-type requirement from the issue, and every source points at #154. I ran the new tests: 25 cases fail today, and each fails because the feature is missing or because the check crashes on a wrong type (the crash is the bug the requirement targets). None fails on a bad path or a missing tool. The other 25 failures in the full suite are these same cases; everything else passes (136).

**Blocker B1 (criterion 154.1):** the plan promises the planner's prompt will stop offering a lone question. The test for this (`test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question`) only checks three spots: the example kinds, the "Exactly one kind:" sentence and the "End with exactly one of" sentence. If the worker edits only those, the test passes even though the "# One question for the owner" section at `dokima/roles/planner.md:103` still tells the planner to hand back one question. The fix is one more check in that test: the prompt has no "One question" heading.

**Notes (not blocking):**
- **Split stories:** your story says owners see "a story or a split … whose sources point at their issue", which reads as covering a split's stories too. The planner checked sources on a single story only, and asked you about splits in its questions. If you say yes, the plan needs one more case and a test.
- **Leftover wording:** two other places still mention a question, and no test catches them: `dokima/roles/planner.md:135` and the header comment at `.github/workflows/planner.yml:5`.
- **Cases that already pass:** 13 of the new test cases pass today. They protect against the behaviour breaking later, and each of their test functions still fails today on its other cases.

I found no problems outside this issue worth filing.
