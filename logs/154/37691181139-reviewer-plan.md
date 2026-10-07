# reviewer (plan) for #154

Run: https://github.com/dokima-dev/dokima/actions/runs/37691181139

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (124.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b9b2d57f-5f5b-4493-8f80-5c7d1ad724c1/tool-results/b980g9sr6.txt
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
> 17-reviewer-plan.json
> 18-planner.json
> 19-reviewer-plan.json
> 20-planner.json
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
> **User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tes

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (117.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b9b2d57f-5f5b-4493-8f80-5c7d1ad724c1/tool-results/blnc3hm9f.txt
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
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has 

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; grep -n '^## \|^### \|^\*\*.*commented\|^---' issue.md | head -100
```

> []
> 4:### Approve the result to merge
> 32:## Comments
> 34:### RezaSoleymanifar on issue #154 (2026-10-06T23:21:30Z)
> 38:### dokima-runtime on issue #154 (2026-10-06T23:26:36Z)
> 154:### dokima-runtime on issue #154 (2026-10-07T00:03:40Z)
> 249:### dokima-runtime on issue #154 (2026-10-07T00:19:47Z)
> 378:### RezaSoleymanifar on issue #154 (2026-10-07T01:44:35Z)
> 383:### dokima-runtime on issue #154 (2026-10-07T01:46:10Z)
> 500:### dokima-runtime on issue #154 (2026-10-07T14:29:40Z)
> 578:### RezaSoleymanifar on issue #154 (2026-10-07T16:00:27Z)
> 582:### RezaSoleymanifar on issue #154 (2026-10-07T16:05:36Z)
> 587:### dokima-runtime on issue #154 (2026-10-07T16:07:26Z)
> 628:### dokima-runtime on issue #154 (2026-10-07T16:09:46Z)
> 749:### dokima-runtime on issue #154 (2026-10-07T16:11:07Z)
> 829:### RezaSoleymanifar on issue #154 (2026-10-07T16:29:04Z)
> 833:### dokima-runtime on PR #165 (2026-10-07T16:32:49Z)
> 890:### dokima-runtime on PR #165 (2026-10-07T16:35:42Z)
> 993:### dokima-runtime on PR #165 (2026-10-07T16:36:54Z)
> 1054:### dokima-runtime on PR #165 (2026-10-07T16:38:45Z)
> 1138:### dokima-runtime on PR #165 (2026-10-07T16:40:07Z)
> 1205:### dokima-runtime on PR #165 (2026-10-07T16:41:33Z)
> 1290:### RezaSoleymanifar on issue #154 (2026-10-07T16:47:45Z)
> 1295:### dokima-runtime on issue #154 (2026-10-07T16:51:24Z)
> 1424:### RezaSoleymanifar on issue #154 (2026-10-07T18:23:21Z)
> 1429:### dokima-runtime on issue #154 (2026-10-07T18:24:53Z)
> 1550:### dokima-runtime on issue #154 (2026-10-07T18:26:17Z)
> 1624:#

`4. Bash`
```
cd /tmp/pack; sed -n 1,37p issue.md; for l in 378 578 582 829 1290 1424 1624 1820 1824 1828; do sed -n "${l},$((l+4))p" issue.md; done
```

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
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_kind raises TypeError). Older tests in tests/test_planner.py that hand back question.md or the old shape will need changing, with reasons

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['in/19-reviewer-plan.json','in/20-planner.json']:
  d=json.load(open(f)); print(f); print(json.dumps(d,indent=1)[:6000])
"; sed -n 1832,2000p issue.md
```

> in/19-reviewer-plan.json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37681564270",
>  "commit_before": "eac2d11423f7147f1917b8515498cfac19136b52",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 32233,
>   "turns": 8,
>   "cost_usd": 0.3330532,
>   "tokens_in": 273205,
>   "tokens_out": 2388
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/154/37681564270-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37681564270",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "Handed back the same plan as the last approved round, with no change to criteria, tests or files"
>    ],
>    "decided": [
>     "Treated the two split story cases the owner asked for on 154.5 as already present: a story's non-functional requirements set to text, and a requirement whose text is a number"
>    ],
>    "open": []
>   },
>   "verdict": "approve",
>   "summary": "The two split story cases the owner asked for on 154.5 are in the test, and they fail when the check they prove is removed; no criteria changed, as the owner said.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "The owner's newest /plan asked for the two cases from the pull request review: a split story's non-functional requirements given as text, and a requirement whose text is a number. Both were already added in the previous round, along with two more (a requirement that is not an object, and a why that is a number). The planner changed nothing this

**Agent:** I'm checking the re-plan against the last approved plan and running its tests on this branch.

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/16-planner.json'))['handback']; b=json.load(open('plan.json'))
for k in set(a)|set(b):
  if a.get(k)!=b.get(k): print('DIFF',k); print(' old',json.dumps(a.get(k))[:1500]); print(' new',json.dumps(b.get(k))[:1500])
"; cd /home/runner/work/dokima/dokima; git log --oneline -3; git show --stat HEAD
```

> DIFF replies
>  old [{"blocker": "B2", "answer": "fixed", "why": "tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field now has four split cases: a story's non_functional set to a string (reason must name 'non_functional'), set to [5] ('non-functional requirement 1'), an item whose text is a number ('its text is not') and one whose why is a number ('its why is not'). With the non_functional block of check_stories removed from dokima/planner.py on the branch, exactly these four fail with a 154.5 message; with the worker's code all 226 tests pass."}]
>  new []
> b178e36 planner for #154 (run 37690922194)
> acfbaa7 AGENTS.md: the conventions we settled (#163)
> 6672bda A re-plan is judged only on what the planner changed in its own run (#167)
> commit b178e368132acc728e4e60efbdf15d3f8f041cb0
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:41:20 2026 +0000
> 
>     planner for #154 (run 37690922194)
> 
>  tests/test_feature_check.py  |   8 +-
>  tests/test_plan_check.py     | 300 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py     |  14 +-
>  tests/test_planner.py        |  39 ++----
>  tests/test_planner_prompt.py |   2 +-
>  5 files changed, 323 insertions(+), 40 deletions(-)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_plan_check.py 2>&1 | grep -E "FAILED|passed|failed" | cut -c1-300; python3 -m pytest -q 2>&1 | tail -25 | cut -c1-300
```

> files = {'plan.json': {'kind': 'question', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A sl...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'essay', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A slow ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> p = {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, 'source': 'htt...al': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 5, ...l': [{'text': 'A failed call says why.', 'why': 'the owner is never left guessing', 'principle': 'fail closed'}], ...}}
> files = {'plan.json': {'kind': 'user_story', 'user_story': 'Slow calls return a job id.', 'acceptance_criteria': [{'text': 'A ...comment-123456'}], 'non_functional': [{'text': 'A failed call says why.', 'why': 3, 'principle': 'fail closed'}], ...}}
> p = {'kind

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q 2>&1 | grep ^FAILED | grep -v test_plan_check | head; git cat-file -t eac2d11 2>&1; git diff eac2d11 HEAD --stat -- tests/ 2>&1 | tail -8
```

> fatal: Not a valid object name eac2d11
> fatal: bad revision 'eac2d11'

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_feature_check.py tests/test_planner_prompt.py tests/test_plan_shape.py | head -120; python3 -m pytest -q tests/test_plan_check.py 2>&1 | grep -c PASSED; python3 -m pytest -q tests/test_plan_check.py -rA 2>&1 | grep ^PASSED
```

> commit b178e368132acc728e4e60efbdf15d3f8f041cb0
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:41:20 2026 +0000
> 
>     planner for #154 (run 37690922194)
> 
> diff --git a/tests/test_feature_check.py b/tests/test_feature_check.py
> index eccce7b..8a90201 100644
> --- a/tests/test_feature_check.py
> +++ b/tests/test_feature_check.py
> @@ -128,14 +128,14 @@ def test_the_check_command_rejects_a_broken_feature_and_says_why(record_property
>      bad["stories"][1].pop("title")
>      (tmp_path / "plan.json").write_text(json.dumps(bad))
>      run = subprocess.run([sys.executable, "-m", "dokima.planner", "check", "9", str(tmp_path)],
> -                         cwd=ROOT, capture_output=True, text=True, timeout=30)
> +                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
>      assert run.returncode == 1, f"156.1: the check passed a story with no title (exit {run.returncode}): {run.stdout}{run.stderr}"
>      why = (tmp_path / "rejected.txt").read_text() if (tmp_path / "rejected.txt").exists() else ""
>      assert names(why, 2) and "title" in why, f"156.1: rejected.txt does not say story 2 lacks its title: {why!r}"
>      (tmp_path / "rejected.txt").unlink()
>      (tmp_path / "plan.json").write_text(json.dumps(feature(story("First", []), story("Second", [0]))))
>      run = subprocess.run([sys.executable, "-m", "dokima.planner", "check", "9", str(tmp_path)],
> -                         cwd

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned #154 from today's main after the earlier draft no longer merged, with the same criteria and tests as the last approved plan"],
  "decided": ["Kept the split story cases for 154.5 the owner asked for, and pinned the repo for two older split checks so their sources point at their own issue"],
  "open": []},
 "verdict": "approve",
 "summary": "The re-plan on fresh main is the plan you approved before, word for word, and its tests still fail today only because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Nothing in the plan changed since the last approved round except the old reply to B2 that no longer applies; the tests were laid again on today's main, which now includes #163 and #167.",
   "evidence": "plan.json compared with the 16-planner hand-back: only 'replies' differs. Branch try/issue-154 is main acfbaa7 plus the planner commit b178e36."},
  {"text": "Every new test fails today for the right reason, and every older test the planner changed still passes, so the rest of the suite is untouched.",
   "evidence": "pytest -q: 37 failed, 190 passed; all 37 failures are in tests/test_plan_check.py with messages like '154.4: a criterion proven by an older test was called 'has no test'' and '154.2: a criterion sourced to 'https://github.com/o/r/issues/91' was accepted on issue #9'. No failure in test_planner.py, test_plan_shape.py, test_feature_check.py or test_planner_prompt.py."}
 ],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 154 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for #154. The new plan is the one you approved before, word for word, now rebuilt on today's main. No blockers, and both checks on my review passed.

- **What changed:** Only the old answer to blocker B2 was dropped, because it no longer applies. The criteria, tests, files in scope and changes to older tests are the same as the last approved round. The branch is today's main plus the planner's one commit.
- **Your earlier ask is still in:** The 154.5 test still has the cases you asked for on a split story's non-functional requirements.
- **Two older tests changed:** Two tests for a split's check now set the repo name for their run. Once a split's sources are checked, their sample split would otherwise be rejected for pointing at another repo. What they check is unchanged.
- **Tests today:** The full suite gives 37 failed and 190 passed. All 37 failures are in the new test file, and each fails because the feature isn't built yet, not because of a crash or a bad path. For example: "154.4: a criterion proven by an older test was called 'has no test'". Every older test the planner changed still passes.

**Next:** it's your call, `/work` to start the build.
