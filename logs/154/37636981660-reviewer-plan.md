# reviewer (plan) for #154

Run: https://github.com/dokima-dev/dokima/actions/runs/37636981660

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (38.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9ab49eee-49ef-4828-80f8-9fd762437c07/tool-results/beueiw2n7.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-planner.json
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
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_

`2. Bash`
```
cd /tmp/pack; cat issue.md; echo ====; cat open_blockers.json
```

> <persisted-output>
> Output too large (32.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9ab49eee-49ef-4828-80f8-9fd762437c07/tool-results/b4tfqylys.txt
> 
> Preview (first 2KB):
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
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_kind raises TypeError). Older tests in tests/test_planner.py that hand back question.md or the old shape will need changi

`3. Bash`
```
cd /tmp/pack; cat plan.json; echo; for f in in/*; do echo "== $f"; python3 -c "import json,sys;d=json.load(open('$f'));print(json.dumps(d,indent=1)[:6000])"; done
```

> {
>  "kind": "user_story",
>  "user_story": "Owners only ever see real plans (a story or a split, never a lone question) whose sources point at their own issue and whose named tests are real and filed under the plan's own criteria.",
>  "acceptance_criteria": [
>   {
>    "text": "A hand-back that is not a plan.json of kind user_story or feature (nothing at all, a question.md, a plan.json with no kind, or one of kind question or any other kind) is rejected, and the reason says the planner always hands back a plan, a user_story or a feature, with its questions listed inside it; a good user_story, a good feature and a story carrying its questions still pass. The planner's prompt no longer offers the question kind, ending with a lone question, or a section on asking the owner one question, and no longer says a question is shown as handed back; the planner workflow no longer looks for question.md or says the planner may end with one question.",
>    "source": "https://github.com/dokima-dev/dokima/issues/154"
>   },
>   {
>    "text": "A criterion whose source is anything other than this issue's link or a link to one of its comments (#issuecomment-...) is rejected, and the reason names the source; this issue's link and its comment links pass. Another issue, a longer number that starts with this one, another repo, a pull request, another host and plain prose are all rejected. A split is no exception: the criteria inside every story of a feature are checked the same way.",
>    "source": "https://githu

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/04-planner.json'));print(d['handback'].get('questions'));print(d['check']);print(d['handback'].get('replies'))
d=json.load(open('in/03-planner.json'));print(d['handback'].get('questions'));print(d['check'])
d=json.load(open('in/01-planner.json'));print(d['handback'].get('questions'))"; sed -n '/Acceptance criteria/,$p' issue.md | head -400
```

> [
>  {
>   "id": "B1",
>   "criterion": "154.1",
>   "test": "tests/test_plan_check.py::test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question",
>   "problem": "154.1 promises the planner's prompt no longer offers ending with a lone question. The test only checks the example kinds, the 'Exactly one kind:' sentence and the 'End with exactly one of' sentence. A prompt that keeps the whole '# One question for the owner' section, which tells the planner to hand back one question with options and a recommendation, still passes.",
>   "evidence": "dokima/roles/planner.md:103-106 holds '# One question for the owner / Only if you cannot plan without the owner's answer. One full question ending in \"?\", with options...'. If you edit only lines 6, 111 and 126, the test goes green with that section still there. The changed tests/test_planner_prompt.py only stops requiring the section. Nothing checks that it is gone.",
>   "fix": "In the same test, assert that the prompt has no 'One question for the owner' heading (for example, no line starting with '#' that contains 'One question'), with a 154.1 message."
>  }
> ]None
> {'passed': True, 'problems': []}
> [{'blocker': 'B1', 'answer': 'fixed', 'why': "Fixed in the previous round and kept: tests/test_plan_check.py::test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question fails while any heading of dokima/roles/planner.md contains 'one question' (the '# One question for the owner' section), with its own 154.1 message; editing only prompt lines

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; wc -l tests/test_plan_check.py; python -m pytest -q tests/test_plan_check.py 2>&1 | tail -40; python -m pytest -q 2>&1 | tail -3
```

> commit 2dea01a37bc0b9e24d40db48b5b15154d4449c6b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 01:46:05 2026 +0000
> 
>     planner for #154 (run 37558599360)
> 
>  tests/test_plan_check.py | 44 +++++++++++++++++++++++++++++++++++++++++---
>  1 file changed, 41 insertions(+), 3 deletions(-)
> 
> commit a15fe3e85f8cd41d23d1424324c4b4e303bab185
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 00:19:42 2026 +0000
> 
>     planner for #154 (run 37551203491)
> 
>  tests/test_plan_check.py | 27 +++++++++++++++++----------
>  1 file changed, 17 insertions(+), 10 deletions(-)
> 
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
> 293 tests/test_plan_check.py
> assert 0 == 1
> FAILED tests/test_plan_check.py::test_a_source_outside_this_issue_inside_a_split_is_rejected_and_named[longer number] - AssertionError: 154.2: a split whose story 2 has a criterion sourced to 'https://github.com/o/r/issues/91' was accepted on issue #9
> assert 0 == 1
> FAILED tests/test_plan_check.py::test_a_source_outside_this_i

**Agent:** Let me read the test file to check B1 and the new split test.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_plan_check.py; python -m pytest -q tests/test_plan_check.py 2>&1 | grep -E "lone_question|split|^FAILED.*anything" | head -20
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
> NEW_TESTS = ('def test_id(record_property):\n    """A slow call returns a job id."""\n'
>              '    record_property("proves", "9.1")\n    assert True\n\n\n'
>              'def test_unique(record_property):\n    """Job ids never repeat."""\n'
>              '    record_property("proves", "9.2")\n    assert True\n')
> STORY = {"kind": "user_story", "user_story": "Slow calls return a job id.",
>          "acceptance_criteria": [{"text":

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_plan_check.py -k "lone_question or anything" 2>&1 | grep -E "^E " | head; python -m pytest -q tests/test_plan_check.py -rA 2>&1 | grep PASSED
```

> E           AssertionError: 154.1: the reason does not say the planner always hands back a user_story or a feature with its questions inside ('always hands back' missing): 'the planner must hand back exactly one of plan.json or question.md, found neither'
> E           assert 'always hands back' in 'the planner must hand back exactly one of plan.json or question.md, found neither'
> E       AssertionError: 154.1: ['question.md'] was accepted; only a user_story or a feature may pass
> E       assert 0 == 1
> E       AssertionError: 154.1: ['plan.json'] was accepted; only a user_story or a feature may pass
> E       assert 0 == 1
> E       AssertionError: 154.1: ['plan.json'] was accepted; only a user_story or a feature may pass
> E       assert 0 == 1
> E       AssertionError: 154.1: ['plan.json'] was accepted; only a user_story or a feature may pass
> E       assert 0 == 1
> PASSED tests/test_plan_check.py::test_a_test_filed_under_a_key_that_is_not_a_criterion_is_rejected_and_named[another issue, new test]
> PASSED tests/test_plan_check.py::test_a_test_filed_under_a_key_that_is_not_a_criterion_is_rejected_and_named[past the last, new test]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[criteria not a list]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[user_story]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[scope]
> PASSED tests/test_plan_check.py::test_a_value

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q "tests/test_plan_check.py::test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question" 2>&1 | grep -E "^E " | head -3; grep -n "source" dokima/planner.py | head -30
```

> E       AssertionError: 154.1: the prompt shows the kinds ['feature', 'question', 'user_story'], not exactly user_story and feature
> E       assert {'feature', '... 'user_story'} == {'feature', 'user_story'}
> E         
> 98:        if not str(c.get("source", "")).strip():
> 99:            raise Garbled(f"acceptance criterion '{c['text'][:60]}' has no source link")
> 130:    """Each test function in a file: name -> (its source, the criterion keys it proves)."""

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added the owner's answer to criterion 154.2: the criteria inside every story of a split have their sources checked the same way",
          "Added a test that puts a wrong source on each story of a split, one at a time, and a wrong-type source and criteria list inside a split's story to 154.5"],
  "decided": ["Kept the test change from the last round that fails while the planner's prompt still has a section offering one question for the owner"],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now covers the owner's answer (a split's stories have their sources checked too), the earlier gap in the prompt test is closed, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "The new split sentence in 154.2 comes from the owner's comment, but the criterion still cites only the issue link. Citing that comment would trace it to the owner's words exactly.",
   "evidence": "plan.json acceptance_criteria[1].source is https://github.com/dokima-dev/dokima/issues/154; the owner's answer is the /plan comment of 2026-10-07T01:44:35Z"},
  {"text": "13 parametrized cases already pass today, for example a new test filed under another issue's key and several wrong-type fields. They guard against the behavior getting worse later, and each of their test functions still fails today on its other cases.",
   "evidence": "pytest -q tests/test_plan_check.py -rA: 35 failed, 13 passed; full suite: 35 failed, 136 passed"}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for issue #154 and wrote the verdict to `/tmp/dokima-out/review.json`. It passed both hand-back checks.

- **Your answer is in the plan.** You said a split's stories need their sources checked too, and criterion 154.2 now says so. A new test puts a wrong source on each story of a split, one at a time, and expects it to be rejected and named. Criterion 154.5 also gained cases for a wrong-type source and a criteria field that isn't a list inside a split's story.
- **Last round's blocker (B1) is fixed.** The prompt test now fails while the planner's prompt still has a section offering one question for you. It fails today on the prompt still showing a question kind.
- **The new tests fail for the right reason.** In the full suite, 35 tests fail and 136 pass. Each failure comes from the missing feature, not a crash or a bad path. For example, a question.md hand-back is still accepted, and an older unchanged test is still called "has no test".

Two notes, neither blocking:
- The sentence added from your comment is still sourced to the issue link, not to your comment of 2026-10-07 01:44. Citing the comment would trace it to your words exactly.
- 13 of the new test cases already pass today, mostly wrong-type fields. They protect against regressions later, and every one of those test functions still fails on its other cases.

The plan has no open questions left.
