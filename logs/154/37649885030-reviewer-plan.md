# reviewer (plan) for #154

Run: https://github.com/dokima-dev/dokima/actions/runs/37649885030

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (51.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/cb34b055-a2bc-4f89-8bb5-0a604bf652ba/tool-results/b49ffsf3y.txt
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
> **Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where t

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (44.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/cb34b055-a2bc-4f89-8bb5-0a604bf652ba/tool-results/bi9r2qfs6.txt
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

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/cb34b055-a2bc-4f89-8bb5-0a604bf652ba/tool-results/bi9r2qfs6.txt
```

> 1	# Issue #154: Plan checker: kinds, sources and named tests
> 2	
> 3	<!-- dokima-card -->
> 4	### Plan: add `work` to start
> 5	
> 6	
> 7	This issue has no objective and acceptance criteria yet.
> 8	
> 9	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 10	
> 11	<!-- /dokima-card -->
> 12	
> 13	<details open><summary>From the approved plan of #139, story 1</summary>
> 14	
> 15	**Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 16	
> 17	**User story:** Owners only see real plans (a story or a split, never a lone question) whose sources point at their issue and whose named tests are real and filed under the plan's own criteria.
> 18	
> 19	**Context:** dokima/planner.py read_output still accepts question.md and a plan.json with no kind (the old objective/criteria shape); from_kind only checks a source is non-empty; declared_labels ignores named tests that do not exist, and counts only added or changed tests as proof, so a criterion named against an older unchanged test is rejected as 'has no test'. A number where text belongs crashes the check (c['text'][:60] in from_kind raises TypeError). Older tests in tests/test_planner.py that hand back question.md or the old shape will need changing, with reasons. The repo comes from GITHUB_REPOSITORY. The owner's newer words (comment of 2026-10-06T20:49) settle one flow: the planner always plans on its best rea

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; ls in; cd /home/runner/work/dokima/dokima; git log --oneline -5 main 2>/dev/null; git log --oneline -3 origin/main; git merge-base HEAD origin/main; git diff --stat origin/main...HEAD; git diff --stat origin/main HEAD
```

> []01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-planner.json
> 05-reviewer-plan.json
> 06-planner.json
> 07-planner.json
> 860b40d The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue (#161)
> 4aeacaa Plan checker: features are checked (#160)
> 77c5b21 The river: each stage starts the next until it needs the owner (#162)
> a6ac00c A re-plan checks its tests against where the branch left main (#159)
> 78fe9eb /work on an approved split files its stories as sub-issues (#153)
> 860b40d The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue (#161)
> 4aeacaa Plan checker: features are checked (#160)
> 77c5b21 The river: each stage starts the next until it needs the owner (#162)
> 860b40de3ad96832391c461da1576fc7167dbc4d
>  tests/test_feature_check.py  |   8 +-
>  tests/test_plan_check.py     | 293 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py     |  14 +--
>  tests/test_planner.py        |  39 ++----
>  tests/test_planner_prompt.py |   2 +-
>  5 files changed, 316 insertions(+), 40 deletions(-)
>  tests/test_feature_check.py  |   8 +-
>  tests/test_plan_check.py     | 293 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py     |  14 +--
>  tests/test_planner.py        |  39 ++----
>  tests/test_planner_prompt.py |   2 +-
>  5 files changed, 316 insertions(+), 40 deletions(-)

**Agent:** Branch now sits on today's main. Let me look at the diff and run the tests.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff origin/main HEAD -- tests/test_feature_check.py tests/test_plan_shape.py tests/test_planner.py tests/test_planner_prompt.py; python -m pytest -q 2>&1 | tail -45
```

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
> -                         cwd=ROOT, capture_output=True, text=True, timeout=30)
> +                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
>      assert run.returncode == 0, f

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | grep FAILED | cut -d: -f1 | sort | uniq -c; python -m pytest -q tests/test_plan_check.py -rA 2>&1 | grep -E "^(PASSED|FAILED)" | grep PASSED; git diff 2dea01a HEAD --stat -- tests/test_plan_check.py; git diff 2dea01a HEAD -- tests/test_plan_check.py | head -50
```

> 33 FAILED tests/test_plan_check.py
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
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's criterion source]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[split's criteria not a list]
> PASSED tests/test_plan_check.py::test_a_value_of_the_wrong_type_is_rejected_naming_the_field[plan.json a list]
> PASSED te

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "o/r\|GITHUB_REPOSITORY\|def story\|def feature\|check_stories\|problems(" tests/test_feature_check.py | head -30; grep -rn "GITHUB_REPOSITORY" tests/test_plan_check.py | head; grep -rln "kind.*feature\|\"feature\"" tests/ 
```

> 20:SRC = "https://github.com/o/r/issues/9"
> 23:def story(title, deps):
> 29:def feature(*stories):
> 131:                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
> 138:                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
> 176:                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
> 184:                         cwd=ROOT, env=dict(os.environ, GITHUB_REPOSITORY="o/r"), capture_output=True, text=True, timeout=30)
> tests/test_plan_check.py:6:issue, is read back. GITHUB_REPOSITORY is set to o/r and the issue is #9, so this issue's link is
> tests/test_plan_check.py:65:    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
> tests/test_feature_check.py
> tests/test_plan_shape.py
> tests/test_handback_check.py
> tests/test_plan_check.py
> tests/test_agent.py

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def problems\|def proving\|def check_stories\|GITHUB_REPOSITORY\|def main" dokima/planner.py | head -20; grep -n "\"feature\"\|feature(" tests/test_split.py tests/test_plan_shape.py | head; grep -n "problems\|main(" tests/test_split.py tests/test_plan_shape.py | head
```

> 67:def check_stories(stories):
> 207:def proving(tc):
> 212:def problems(number, plan, files, tc):
> 285:def main(argv):
> 287:    repo = os.environ.get("GITHUB_REPOSITORY", "")
> ugrep: warning: tests/test_split.py: No such file or directory
> 89:    assert hand_back(tmp_path, {"kind": "feature", "feature": "f", "stories": [story, story]})[0] == "feature", "138.2: feature not read"
> 91:        hand_back(tmp_path, {"kind": "feature", "feature": "f", "stories": [story]})
> ugrep: warning: tests/test_split.py: No such file or directory
> 109:    assert planner.problems("9", p, ["tests/t.py"], tc) == [], "138.3: a declared plan was still rejected"

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "feature\|planner\b\|GITHUB_REPOSITORY\|issues/" tests/test_handback_check.py | head -20; grep -n "\"feature\"\|issues/\|planner.main\|dokima.planner" tests/test_agent.py | head -20
```

> 20:SPLIT = {"kind": "feature", "feature": "f", "stories": [
> 196:    env = {**os.environ, "PYTHONPATH": ROOT, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_REPOSITORY": "o/r", "GITHUB_RUN_ID": "42"}
> 285:SPLIT = {"kind": "feature", "feature": "f", "stories": [
> 299:            return f"https://github.com/o/r/issues/{200 + sum(1 for c in calls if c[:2] == ('issue', 'create'))}\n"
> 300:        if args[0] == "api" and args[1].startswith("repos/o/r/issues/2"):
> 309:    assert ("api", "-X", "POST", "repos/o/r/issues/139/sub_issues", "-F", "sub_issue_id=9201") in calls
> 310:    assert ("api", "-X", "POST", "repos/o/r/issues/202/dependencies/blocked_by", "-F", "issue_id=9201") in calls

`10. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 15,40p tests/test_handback_check.py; grep -n "SPLIT" tests/test_handback_check.py
```

> STORY = {"kind": "user_story", "user_story": "u",
>          "acceptance_criteria": [{"text": "a", "source": "https://x/9"}, {"text": "b", "source": "https://x/9"}],
>          "non_functional": [{"text": "c", "why": "w", "principle": "Fail closed"}],
>          "scope": ["dokima/x.py"], "out_of_scope": [],
>          "tests": {"9.1": ["tests/test_x.py::test_a"], "9.2": ["tests/test_x.py::test_b"], "9.3": ["tests/test_x.py::test_c"]}}
> SPLIT = {"kind": "feature", "feature": "f", "stories": [
>     {"title": "One", "user_story": "u1", "acceptance_criteria": [{"text": "a", "source": "https://x/9"}],
>      "non_functional": [{"text": "n", "why": "w"}], "depends_on": []},
>     {"title": "Two", "user_story": "u2", "acceptance_criteria": [{"text": "b", "source": "https://x/9"}],
>      "non_functional": [], "depends_on": [0]}]}
> 
> REVIEW = {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []},
>           "verdict": "block", "summary": "One proof is missing.",
>           "blockers": [{"id": "B1", "criterion": "9.1", "test": None, "problem": "No test.", "evidence": "plan.json", "fix": "Add one."}],
>           "notes": [{"text": "A note.", "evidence": "x.py:1"}], "outside_plan": [{"file": "a.py", "change": "c"}],
>           "resolved": ["B0"], "issues_found": [{"title": "t", "why": "w", "evidence": "e"}]}
> WORK = {"summary": "Cause and change.", "criteria": {"9.1": "x.py, a()", "9.2": "x.py, b()", "9.3": "x.py, c()"},
>         "evidence": "pytest -q: 3 passed", "outside_scope": [{"

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "planner\.\|read_output\|problems" dokima/agent.py | head
```

> 6:The plan's own check lives in dokima/planner.py; this module adds review.json and work.json.
> 111:def problems_round(role, h, pack_dir):
> 172:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> 183:           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()] if not passed else []}}
> 196:        lines += [""] + [f"- {p}" for p in rec["check"]["problems"]]
> 336:def problems_questions(qs):
> 344:def problems_review(r):
> 381:def problems_work(w):
> 406:def problems_items(h, field, keys, name=None):
> 423:def problems_shape(kind, h):

**Agent:** Status: the branch now sits on today's main, the new tests are the same ones I approved last round, and they fail today for the right reasons. I'm writing the approval now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Rebuilt the approved plan on today's main after #156 merged, with the same four criteria, one non-functional requirement and the same new tests",
          "Kept #156's story with a sourced criterion in tests/test_plan_shape.py, so that file no longer conflicts with main",
          "Set the repo to o/r in two #156 tests that run the check, so their split's sources point at the issue they check"],
  "decided": ["What the criteria promise and what the new tests check stay as approved"],
  "open": []},
 "verdict": "approve",
 "summary": "The plan is the one approved before, now on today's main: the new tests are unchanged and still fail today because the feature is missing, and the two older #156 tests it changes keep checking the same thing.",
 "blockers": [],
 "notes": [
  {"text": "The two #156 tests now run the check as if the repo were o/r. Without that change, the split's sources would be rejected once 154.2 lands, because CI runs as dokima-dev/dokima. What they check is unchanged.",
   "evidence": "git diff origin/main HEAD -- tests/test_feature_check.py: only env=dict(os.environ, GITHUB_REPOSITORY=\"o/r\") is added at lines 131, 138, 176 and 184"},
  {"text": "The new tests in tests/test_plan_check.py match the approved round exactly. 15 cases already pass today, for example a new test filed under another issue's key and several wrong-type fields. Each of their test functions still fails today on its other cases.",
   "evidence": "git diff 2dea01a HEAD -- tests/test_plan_check.py is empty; pytest -q: 33 failed (all in tests/test_plan_check.py), 189 passed"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 154 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> exit 0

**Agent:** I approved the refreshed plan for #154 and saved the review to `/tmp/dokima-out/review.json`. It passes both checks it has to pass before handing back.

**What changed since the last approval:** you asked the planner to refresh the plan after #156 merged. The criteria and the new tests in `tests/test_plan_check.py` are exactly the ones I approved last round. The only edits are to older tests, so the branch fits on today's main again:
- `tests/test_plan_shape.py` now keeps #156's version of the conflicting test, with a criterion and its source.
- Two #156 tests in `tests/test_feature_check.py` now run the check as if the repo were `o/r`. Without that, once the check starts looking at a split's sources, those tests would fail in CI. CI runs as `dokima-dev/dokima`, so their `o/r` sources would be rejected. What the two tests check is unchanged.

**What I ran:** the full suite on this branch gave 33 failed and 189 passed. All 33 failures are the new tests in `tests/test_plan_check.py`, and each fails because the feature isn't built yet, not because of a crash or a broken path. 15 of the new cases already pass today, such as a new test filed under another issue's number and some wrong-type fields. That's acceptable because every test function those cases belong to still fails on its other cases.

There were no open blockers to carry over, and I found no problems outside this issue.
