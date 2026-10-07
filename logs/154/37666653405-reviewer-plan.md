# reviewer (plan) for #154

Run: https://github.com/dokima-dev/dokima/actions/runs/37666653405

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (102.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/977ca8fc-9fdd-43a1-87d5-5b0128beb65e/tool-results/b4v2obne4.txt
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
> 05-reviewer-plan.json
> 06-planner.json
> 07-planner.json
> 08-reviewer-plan.json
> 09-worker.json
> 10-reviewer-pr.json
> 11-worker.json
> 12-reviewer-pr.json
> 13-worker.json
> 14-reviewer-pr.json
> 15-planner.json
> 16-planner.json
> # Issue #154: Plan checker: kinds, sources and named tests
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #165](https://github.com/dokima-dev/dokima/pull/165) · [files changed](https://github.com/dokima-dev/dokima/pull/165/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37653427992/job/112902365682)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 1</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tests are real and filed under the plan's own criteria.
> 
> ...
> </persisted-output

`2. Bash`
```
cd /tmp/pack; cat issue.md | head -c 40000
```

> <persisted-output>
> Output too large (39.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/977ca8fc-9fdd-43a1-87d5-5b0128beb65e/tool-results/bdm4uh8yj.txt
> 
> Preview (first 2KB):
> # Issue #154: Plan checker: kinds, sources and named tests
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #165](https://github.com/dokima-dev/dokima/pull/165) · [files changed](https://github.com/dokima-dev/dokima/pull/165/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37653427992/job/112902365682)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 1</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tests are real and filed under the plan's own criteria.
> 
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has n

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/977ca8fc-9fdd-43a1-87d5-5b0128beb65e/tool-results/bdm4uh8yj.txt
```

> 1	# Issue #154: Plan checker: kinds, sources and named tests
> 2	
> 3	<!-- dokima-card -->
> 4	### Approve the result to merge
> 5	[PR #165](https://github.com/dokima-dev/dokima/pull/165) · [files changed](https://github.com/dokima-dev/dokima/pull/165/files)
> 6	
> 7	This issue has no objective and acceptance criteria yet.
> 8	
> 9	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37653427992/job/112902365682)
> 10	
> 11	<!-- /dokima-card -->
> 12	
> 13	<details open><summary>From the approved plan of #139, story 1</summary>
> 14	
> 15	**Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 16	
> 17	**User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tests are real and filed under the plan's own criteria.
> 18	
> 19	**Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_kind raises TypeError). Older tests in tests/test_planner.py that hand back question.md o

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/977ca8fc-9fdd-43a1-87d5-5b0128beb65e/tool-results/b4v2obne4.txt
```

> 700	  "non_functional": [
> 701	   {
> 702	    "text": "A plan.json with a value of the wrong type (a number where text belongs, a string where a list belongs, inside a story or a split's story, or a plan.json that is not an object) is rejected with a reason naming the field, never a crash.",
> 703	    "why": "a crash posts nothing and leaves the owner guessing",
> 704	    "principle": "Fail closed: a failure always says why on the issue."
> 705	   }
> 706	  ],
> 707	  "scope": [
> 708	   "dokima/planner.py",
> 709	   "dokima/roles/planner.md",
> 710	   ".github/workflows/planner.yml"
> 711	  ],
> 712	  "out_of_scope": [
> 713	   "The board's 'Planner question' match in dokima/board.py and the agent card's question line in dokima/agent.py; they become unused but stay.",
> 714	   "Renaming the planner workflow's steps.",
> 715	   "What the reviewer and the worker hand back; only the planner's check changes."
> 716	  ],
> 717	  "tests": {
> 718	   "154.1": [
> 719	    "tests/test_plan_check.py::test_anything_but_a_story_or_a_feature_is_rejected_saying_the_planner_always_hands_back_a_plan",
> 720	    "tests/test_plan_check.py::test_the_prompt_and_the_workflow_no_longer_offer_a_lone_question"
> 721	   ],
> 722	   "154.2": [
> 723	    "tests/test_plan_check.py::test_a_source_outside_this_issue_is_rejected_and_named",
> 724	    "tests/test_plan_check.py::test_a_source_outside_this_issue_inside_a_split_is_rejected_and_named"
> 725	   ],
> 726	   "154.3": [
> 727	    "tests/test_plan_check.py::test_a_named_test_that_is_not_in_the_repo_i

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 84864f4 eac2d11 --stat; git diff 84864f4 eac2d11 -- tests; python3 -m pytest -q 2>&1 | tail -3; sed -n 70,110p dokima/planner.py
```

> tests/test_plan_check.py | 7 ++++++-
>  1 file changed, 6 insertions(+), 1 deletion(-)
> diff --git a/tests/test_plan_check.py b/tests/test_plan_check.py
> index bf362c1..7ee7fe3 100644
> --- a/tests/test_plan_check.py
> +++ b/tests/test_plan_check.py
> @@ -272,12 +272,17 @@ def test_a_criterion_proven_only_by_an_older_test_counts_as_proven(record_proper
>      (lambda s: s.update(kind=5), "kind"),
>      (feature(lambda f: f["stories"][1]["acceptance_criteria"][0].update(source=9)), "source"),
>      (feature(lambda f: f["stories"][0].update(acceptance_criteria="A job id.")), "acceptance_criteria"),
> +    (feature(lambda f: f["stories"][1].update(non_functional="none")), "non_functional"),
> +    (feature(lambda f: f["stories"][1].update(non_functional=[5])), "non-functional requirement 1"),
> +    (feature(lambda f: f["stories"][1].update(non_functional=[{"text": 3, "why": "w"}])), "its text is not"),
> +    (feature(lambda f: f["stories"][1].update(non_functional=[{"text": "t", "why": 3}])), "its why is not"),
>      ([], "plan.json"),
>      ("a plan", "plan.json"),
>      (5, "plan.json"),
>  ], ids=["criterion text", "criterion source", "requirement text", "requirement why", "criteria not a list",
>          "requirements not a list", "user_story", "scope", "out_of_scope", "tests", "test_changes", "questions", "kind",
> -        "split's criterion source", "split's criteria not a list", "plan.json a list", "plan.json a string", "plan.json a number"])
> +        "split's criterion source", "split's criteria n

**Agent:** Checking that the four new test cases go red when the worker's check is removed, and that they also fail on main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 288,310p tests/test_plan_check.py; rm -rf /tmp/mut && git worktree add -q /tmp/mut HEAD && cd /tmp/mut && python3 - <<'E'
p='dokima/planner.py';s=open(p).read()
a=s.index('        nfr = s.get("non_functional", [])');b=s.index('        if not isinstance(s.get("depends_on"), list):')
open(p,'w').write(s[:a]+s[b:])
E
python3 -m pytest -q 2>&1 | grep -E "FAILED|passed|failed"; git checkout -q dokima/planner.py
git checkout -q origin/main -- dokima .github 2>/dev/null; python3 -m pytest -q tests/test_plan_check.py -k "split" 2>&1 | grep -E "FAILED|passed|failed"; cd /; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/mut
```

> Breaks one field's type at a time in a good story or a split's story (or makes the whole plan.json a list, a string
>     or a number), runs the check, and checks it fails with a reason naming that field (or plan.json); a crash fails the
>     test instead.
>     """
>     record_property("proves", "154.5")
>     rc, why = check({"plan.json": story(change) if callable(change) else json.dumps(change)}, "154.5")
>     assert rc == 1, f"154.5: a wrong type in {field} was accepted"
>     assert field in why, f"154.5: the reason does not name the field {field}: {why!r}"
> 
> 
> FAILED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's requirements not a list] - AssertionError: 154.5: a wrong type in non_functional was accepted
> FAILED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's requirement not an object] - AssertionError: 154.5: a wrong type in non-functional requirement 1 was accepted
> FAILED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's requirement text] - AssertionError: 154.5: a wrong type in its text is not was accepted
> FAILED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's requirement why] - AssertionError: 154.5: a wrong type in its why is not was accepted
> 4 failed, 222 passed in 5.02s
> FAILED tests/test_plan_check.py::test_a_source_outside_this_issue_inside_a_split_is_rejected_and_named[parent issue] - Assertion

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {"did": ["Added four cases to the 154.5 test that break a split story's non-functional requirements: a string instead of a list, an item that is not an object, an item whose text is a number, and an item whose why is a number", "Widened the 154.5 wording to name a split story's non-functional requirements"], "decided": ["Changed no other criterion, test or file; the code that passes the new cases is already on the branch"], "open": []},
 "verdict": "approve",
 "summary": "The planner did what the owner asked: the 154.5 test now proves a split story's broken non-functional requirements are rejected, naming the field, and those four cases go red when the check is removed.",
 "blockers": [],
 "notes": [{"text": "The four new cases are the proof B2 on the pull request asked for. With the worker's check in place all 226 tests pass; with it removed exactly these four fail, each with a 154.5 message. On main's code they fail the same way, because the feature is missing there.", "evidence": "git diff 84864f4 eac2d11 touches only tests/test_plan_check.py (+6/-1). Deleting the non_functional block of check_stories (dokima/planner.py:91-100) on a copy: 4 failed, 222 passed, e.g. \"[split's requirement why] - 154.5: a wrong type in its why is not was accepted\". With main's dokima/: same four fail, plus the 154.2 split cases."}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
E
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 154 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the refreshed plan for #154. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

**What the planner did:** It added four cases to the 154.5 test. Each one breaks a split story's non-functional requirements a different way: a string instead of a list, an item that isn't an object, an item whose text is a number, and an item whose why is a number. It also widened the 154.5 wording to name these requirements. Only `tests/test_plan_check.py` changed, by six lines. This is the missing test that the pull-request reviewer's B2 asked for and that you sent back with `/plan`.

**What I checked:**
- **On the branch:** all 226 tests pass.
- **With the worker's check removed:** only these four new cases fail, each saying "154.5" and which field was let through. So they really prove that a split story's non-functional requirements are checked.
- **With main's code:** the same four cases fail, because the check doesn't exist there yet.

There are no blockers, and no earlier plan-stage blockers were left open. B2 belongs to the pull-request review, so the reviewer there should mark it resolved next round.
