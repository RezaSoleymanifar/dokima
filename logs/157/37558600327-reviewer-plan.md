# reviewer (plan) for #157

Run: https://github.com/dokima-dev/dokima/actions/runs/37558600327

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (29.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/648062c6-40f9-487b-86e3-f9215bc370f0/tool-results/b5h5ib1hz.txt
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
> # Issue #157: The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 4</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** The worker's and the reviewer's hand-backs reach the owner only in the shape their prompts define, every blocker is about one of the plan's criteria, and a rejected run says why on the issue.
> 
> **Context:** dokima/agent.py problems_review and problems_work check a few fields, crash on a string where an object belongs (blockers: ['B1'] raises AttributeError) or a number where a list belongs (notes: 5 raises TypeError), never check work.json gives a line for every plan criterion, and only check that a blocker's criterion is non-empty. `agent check` does not get the plan or the issue number today, so .github/workflows/agent.yml must pass them; agent.yml also only writes a record on rejection and posts nothing on the issue (planner.yml does, through `planner rejected`). The prompts' shapes are in dokima/roles/reviewer.md and dokima/roles/w

`2. Bash`
```
cd /tmp/pack; cat issue.md; echo ====; cat open_blockers.json
```

> # Issue #157: The worker's and reviewer's hand-backs are checked, and a rejection says why on the issue
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 4</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** The worker's and the reviewer's hand-backs reach the owner only in the shape their prompts define, every blocker is about one of the plan's criteria, and a rejected run says why on the issue.
> 
> **Context:** dokima/agent.py problems_review and problems_work check a few fields, crash on a string where an object belongs (blockers: ['B1'] raises AttributeError) or a number where a list belongs (notes: 5 raises TypeError), never check work.json gives a line for every plan criterion, and only check that a blocker's criterion is non-empty. `agent check` does not get the plan or the issue number today, so .github/workflows/agent.yml must pass them; agent.yml also only writes a record on rejection and posts nothing on the issue (planner.yml does, through `planner rejected`). The prompts' shapes are in dokima/roles/reviewer.md and dokima/roles/worker.md (work.json says empty lists may be left out). The real files from #142 are not in the repo (no branch holds them); they live in GitHub run artifacts. The owner answered (answer 3) that every blocker names a criterion, with no exception; dropped asks are caught by story 5 instead. A plan-stage review of a split 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; diff <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json')),indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/in/03-planner.json'))['handback'],indent=1,sort_keys=True))") | head; git show --stat HEAD; cat tests/test_handback_check.py
```

> commit aa5175c410718bb2e20cf1b6c0244e7f668c0171
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 00:19:40 2026 +0000
> 
>     planner for #157 (run 37551206405)
> 
>  tests/test_handback_check.py | 58 +++++++++++++++++++++++++++++---------------
>  1 file changed, 39 insertions(+), 19 deletions(-)
> """The worker's and reviewer's hand-backs are checked against their prompt's shape and the approved plan, from outside.
> 
> Every test runs the real command the workflow runs, `python3 -m dokima.agent check review|work FILE PLAN N`, on files in
> a temp folder, so it proves what a run sees: the exit code, the reasons printed, and never a crash. A plan for issue 9
> with two acceptance criteria and one non-functional requirement (9.1, 9.2, 9.3) stands in for the approved plan.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> 
> STORY = {"kind": "user_story", "user_story": "u",
>          "acceptance_criteria": [{"text": "a", "source": "https://x/9"}, {"text": "b", "source": "https://x/9"}],
>          "non_functional": [{"text": "c", "why": "w", "principle": "Fail closed"}],
>          "scope": ["dokima/x.py"], "out_of_scope": [],
>          "tests": {"9.1": ["tests/test_x.py::test_a"], "9.2": ["tests/test_x.py::test_b"], "9.3": ["tests/test_x.py::test_c"]}}
> SPLIT = {"kind": "feature", "feature": "f", "stories": [
>     {"title": "One", "user_story": "u1", "acceptance_crite

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_handback_check.py 2>&1 | grep -E "^(E  .*157|FAILED|[0-9]+ )" | head -30; python3 -m pytest -q 2>&1 | tail -3
```

> E       AssertionError: 157.1: the review check passed (exit 0) a hand-back it should reject: {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []}, "verdict": "block", "summary": 5, "blockers": [{"id": "B1", "criterion": "9.1",
> E           AssertionError: 157.1: the round check crashed on {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []}, "verdict": "block", "summary": "One proof is missing.", "blockers": ["B1"], "no:
> E       AssertionError: 157.2: the work check passed (exit 0) a hand-back it should reject: {"summary": "Cause and change.", "criteria": {"9.1": "x.py, a()", "9.3": "x.py, c()"}, "evidence": "pytest -q: 3 passed", "outside_scope": [{"file": "b.py", "wh
> E       AssertionError: 157.3: the review check passed (exit 0) a hand-back it should reject: {"previous_step": {"did": ["Wrote three criteria."], "decided": [], "open": []}, "verdict": "block", "summary": "One proof is missing.", "blockers": [{"id": "B1
> E               AssertionError: 157.4: the work check gave no reason naming 9.2:
> E               AssertionError: 157.5: the work check passed with plan.json missing
> E           AssertionError: 157.5: the reviewerplan run does not check against the plan and issue number: reviewerplan) GRADE=plan-grade;   FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json" ;;
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 15

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "notes" tests/test_agent.py | head; grep -n "comment" .github/workflows/agent.yml | head
```

> 13:               "notes": [], "outside_plan": [], "resolved": []}
> 30:    assert agent.problems_review({**GOOD_REVIEW, "notes": [{"text": "n", "evidence": "e"}] * 4}) == ["at most three notes"]
> 173:    """Comments from the issue, its PR, PR reviews and line notes on the code arrive in time order, each labeled with where it was written; records come from both."""
> 205:    assert agent.route("/WORK fix the line notes", True, 150, "feature-x", "Closes #42") == {"role": "worker", "stage": "", "issue": "42"}
> 3:# Runs one agent on a fresh GitHub machine. Started by hand here, or by commands.yml when a code owner's comment
> 5:# conversation (comments, reviews, line notes) and every earlier agent record. The agent runs its own check before it
> 6:# finishes; code runs it again, then posts this run's record as a comment: a card on top, the full JSON folded below.
> 7:# Those comments are the permanent records the cards are built from. Session logs stay on the run page.
> 121:          - $PACK/issue.md: issue #$N as it stands, with every comment (the owner's words and answers are here).
> 147:          cat "$OUT/comment.md" >> "$GITHUB_STEP_SUMMARY"
> 212:      - name: Post the record as a comment, on the PR once there is one
> 219:            gh pr comment "$PR" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"
> 221:            gh issue comment "$N" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"

**Agent:** Still checking the plan for issue #157. All seven new tests fail today because the feature is missing, and the earlier blocker is fixed. Writing my review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added the missing shape cases to 157.1's tests (objects missing one of their fields in notes, outside_plan, outside_scope, suspect_tests, issues_found and blockers) and a worker round check that must not crash.",
          "Made 157.2's test also check as issue 8, and added smaller cases to 157.3, 157.4 and 157.5."],
  "decided": ["Kept the plan that a rejected hand-back posts its comment on the pull request once one is open."],
  "open": ["Asked the owner where the rejection comment goes; the owner has since answered: on the pull request once one is open."]},
 "verdict": "approve",
 "summary": "The plan is ready: every criterion has tests that run the real check, all seven fail today because the feature is missing, and the earlier gap in 157.1's tests is closed.",
 "blockers": [],
 "notes": [{"text": "The owner confirmed the planner's reading of 157.4: once a pull request is open, the rejection comment goes there. The plan's criterion already says 'the run posts one comment', and the test checks the one posting step that picks the pull request or the issue.",
            "evidence": "owner's /review comment of 2026-10-07T01:44:36Z; .github/workflows/agent.yml lines 212-221"}],
 "resolved": ["B1"],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for issue #157, and my review in `/tmp/dokima-out/review.json` passes both of Dokima's own checks.

- **Tests fail today for the right reason:** I ran all seven new tests in `tests/test_handback_check.py`. Each one fails because the feature isn't built yet, not because of a crash or a bad path. The other 128 tests in the repo pass.
- **My earlier blocker B1 is fixed:** the tests for criterion 157.1 now also try items that are objects missing one of their fields, not just bare strings. The worker's round check is now tested as well as the reviewer's. I marked B1 as resolved.
- **Your answer is in the plan:** you said that once a pull request is open, a rejection posts its comment there. Criterion 157.4 already says the run "posts one comment", and its test checks the single step in `.github/workflows/agent.yml` that posts on the pull request if there is one, otherwise on the issue. I recorded that as a note, not a blocker.

There are no blockers left and no issues found outside this one, so the plan is ready for `/work`.
