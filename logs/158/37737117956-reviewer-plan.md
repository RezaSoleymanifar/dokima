# reviewer (plan) for #158

Run: https://github.com/dokima-dev/dokima/actions/runs/37737117956

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (45.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7255609f-ce26-4835-979f-a285823b1a92/tool-results/bjoyqt7xa.txt
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
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> 06-planner.json
> # Issue #158: The reviewer lists every ask in the owner's words, and real hand-backs become test samples
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #198](https://github.com/dokima-dev/dokima/pull/198) · [files changed](https://github.com/dokima-dev/dokima/pull/198/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37732974669/job/113166076961)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 5</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (39.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7255609f-ce26-4835-979f-a285823b1a92/tool-results/b5fsftwja.txt
> 
> Preview (first 2KB):
> # Issue #158: The reviewer lists every ask in the owner's words, and real hand-backs become test samples
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #198](https://github.com/dokima-dev/dokima/pull/198) · [files changed](https://github.com/dokima-dev/dokima/pull/198/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37732974669/job/113166076961)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 5</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing.
> 
> **Context:** The owner's answer 3 on the issue: the planner cannot check itself for dropped asks because it writes the criteria from the owner's words, so the reviewer reads the issue text on its own and lists every ask; review.json gets a field for exactly this, and the checker rejects a plan review without it. The review.json s

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/7255609f-ce26-4835-979f-a285823b1a92/tool-results/b5fsftwja.txt
```

> 1	# Issue #158: The reviewer lists every ask in the owner's words, and real hand-backs become test samples
> 2	
> 3	<!-- dokima-card -->
> 4	### Checks failing
> 5	[PR #198](https://github.com/dokima-dev/dokima/pull/198) · [files changed](https://github.com/dokima-dev/dokima/pull/198/files)
> 6	
> 7	This issue has no objective and acceptance criteria yet.
> 8	
> 9	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37732974669/job/113166076961)
> 10	
> 11	<!-- /dokima-card -->
> 12	
> 13	<details open><summary>From the approved plan of #139, story 5</summary>
> 14	
> 15	**Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 16	
> 17	**User story:** A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing.
> 18	
> 19	**Context:** The owner's answer 3 on the issue: the planner cannot check itself for dropped asks because it writes the criteria from the owner's words, so the reviewer reads the issue text on its own and lists every ask; review.json gets a field for exactly this, and the checker rejects a plan review without it. The review.json shape lives in dokima/roles/reviewer.md (the owner asks for this change, so editing dokima/roles/ is allowed here) and is checked by dokima/agent.py problems_review. Pro

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; cd /home/runner/work/dokima/dokima; git log --stat -3 | head -50; ls tests/samples/*; cat tests/samples/132/sources.json
```

> []commit 2efae88c0cc6297c46f6436af9e9adf681c14cb7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 06:20:47 2026 +0000
> 
>     planner for #158 (run 37736816524)
> 
>  tests/samples/132/plan.json      | 52 ++++++++++++++++++++++++++++++++++++++++
>  tests/samples/132/review-pr.json | 24 +++++++++++++++++++
>  tests/samples/132/sources.json   |  5 ++++
>  tests/samples/132/work.json      | 11 +++++++++
>  tests/test_review_asks.py        | 10 +++++++-
>  5 files changed, 101 insertions(+), 1 deletion(-)
> 
> commit 97f70b107aa79105d21ebab2eaf0bdc62463b681
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:33:20 2026 +0000
> 
>     worker for #158 (run 37732627127)
> 
>  dokima/agent.py          | 22 ++++++++++++++++++++++
>  dokima/roles/reviewer.md | 12 ++++++++++--
>  2 files changed, 32 insertions(+), 2 deletions(-)
> 
> commit c8a58d91b659ccfae721afe9740c886d25d00c07
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:17:46 2026 +0000
> 
>     planner for #158 (run 37730752132)
> 
>  tests/test_failed_run_card.py |   3 +-
>  tests/test_review_asks.py     | 235 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py           |   7 +-
>  3 files changed, 242 insertions(+), 3 deletions(-)
> plan.json
> review-pr.json
> sources.json
> work.json
> {
>  "plan.json": "https://github.com/dokima-dev/dokima/issues/132#issuecomment-6052521274",
>  "work.json": "https://github.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 97f70b1 2efae88 -- tests/test_review_asks.py; cat tests/test_review_asks.py
```

> diff --git a/tests/test_review_asks.py b/tests/test_review_asks.py
> index e52618a..45fe5f8 100644
> --- a/tests/test_review_asks.py
> +++ b/tests/test_review_asks.py
> @@ -192,7 +192,8 @@ def test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers(record_prop
>      to the record comment on GitHub it was copied from. Across all folders there is at least one plan, one work and
>      one review. Each plan passes the plan checker's reading of plan.json for issue N in dokima-dev/dokima, with its
>      questions; each work.json passes `agent check work` against its plan; each review passes the workflow's review
> -    check in the pack and STAGE of its stage, a plan review's or a code review's."""
> +    check in the pack and STAGE of its stage, a plan review's or a code review's. The format is the settled one: each
> +    review sample, graded as a review of its plan with its asks list taken away, is rejected for the missing list."""
>      record_property("proves", "158.4")
>      folders = sorted(d for d in os.listdir(SAMPLES) if os.path.isdir(os.path.join(SAMPLES, d))) if os.path.isdir(SAMPLES) else []
>      assert folders, "158.4: tests/samples/ holds no samples: keep real hand-backs there, one folder per issue"
> @@ -231,5 +232,12 @@ def test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers(record_prop
>                  assert (code, out.strip()) == (0, ""), \
>                      f"158.4: the sample tests/samples/{n}/review-{stage}.json fails its checker: {out}{err[-400:]}"
>     

**Agent:** I'm reviewing the planner's new plan for #158 now. Next I'll run its tests on this branch and against main's code.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_review_asks.py 2>&1 | tail -5; rm -rf /tmp/mainck && mkdir /tmp/mainck && git worktree add -q /tmp/mainck/w HEAD && cd /tmp/mainck/w && git checkout -q main -- dokima/ && pytest -q tests/test_review_asks.py 2>&1 | grep -E "^(FAILED|E .*158|[0-9]+ (passed|failed))" | head -20
```

> ....                                                                     [100%]
> 4 passed in 1.20s
> E       AssertionError: 158.1: the review.json shape in reviewer.md has no asks list of {"ask": ..., "source": ..., "criterion": "N.k" | "missing"}
> E       AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> E       AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> E                   AssertionError: 158.4: tests/samples/132/review-pr.json graded as a plan review with no asks list passes; the samples are not checked in the settled format: 
> FAILED tests/test_review_asks.py::test_the_reviewer_prompt_asks_for_every_ask_in_the_owners_words - AssertionError: 158.1: the review.json shape in reviewer.md has no asks list of {"ask": ..., "source": ..., "criterion": "N.k" | "missing"}
> FAILED tests/test_review_asks.py::test_a_plan_review_must_list_every_ask_well_formed - AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> FAILED tests/test_review_asks.py::test_a_plan_review_with_a_missing_ask_cannot_approve - AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> FAILED tests/test_review_asks.py::test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers - AssertionError: 158.4: tests/samples/132/review-pr.json graded as a plan review with no ask

**Agent:** All four tests fail on main's code for the right reason and pass on the branch. Next I'll check the samples against the GitHub records they link to.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainck/w; for id in 6052521274 6052566514 6052592541; do curl -s -m 15 https://api.github.com/repos/dokima-dev/dokima/issues/comments/$id > /tmp/mainck/$id.json; python3 -I - /tmp/mainck/$id.json <<'E'
import json,sys,re
b=json.load(open(sys.argv[1])).get('body','')
m=re.search(r"```json\n(.*?)\n```",b,re.S)
print(sys.argv[1], bool(m))
if m: json.dump(json.loads(m.group(1))['handback'],open(sys.argv[1]+'.hb','w'))
E
done
python3 -I - <<'E'
import json
for f,id in [("plan.json",6052521274),("work.json",6052566514),("review-pr.json",6052592541)]:
    try: print(f, json.load(open(f"/home/runner/work/dokima/dokima/tests/samples/132/{f}"))==json.load(open(f"/tmp/mainck/{id}.json.hb")))
    except Exception as e: print(f,e)
E
```

> /tmp/mainck/6052521274.json True
> /tmp/mainck/6052566514.json True
> /tmp/mainck/6052592541.json True
> plan.json True
> work.json True
> review-pr.json True

**Agent:** The three samples match their linked GitHub records exactly. Now running the full test suite.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q -x 2>&1 | tail -3
```

> )
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 103 passed in 7.73s

`9. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q 2>&1 | grep -E "FAILED|passed|failed" | tail; git stash list | head -1; git status --short
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
> 3 failed, 289 passed in 68.48s (0:01:08)

**Agent:** Three older tests fail. I'm checking whether that comes from this sandbox's own STAGE setting rather than the plan.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; echo "STAGE=$STAGE"; env -u STAGE pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -2; git checkout -q main -- dokima/ 2>/dev/null; git stash -q; echo; STAGE=plan pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1|tail -1; git stash pop -q 2>/dev/null; git checkout -q HEAD -- dokima/; git status --short
```

> STAGE=plan
> ..............                                                           [100%]
> 14 passed in 3.06s
> 
> 3 failed, 11 passed in 1.16s
> A  dokima/icons/queued.svg

**Agent:** I left a stray file from my main-vs-branch comparison. Restoring the working tree before going on.

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git stash list; git ls-tree HEAD dokima/icons/queued.svg; git rm -q --cached dokima/icons/queued.svg; rm -f dokima/icons/queued.svg; git status --short; git diff HEAD --stat
```

> (Bash completed with no output)

**Agent:** The tree is clean again. The three failures only happen when STAGE=plan is set in the environment. Checking whether CI ever runs the suite that way.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "STAGE" .github/workflows/*.yml | head -20; grep -n "pytest" .github/workflows/*.yml | head
```

> .github/workflows/agent.yml:48:      STAGE: ${{ (inputs.role || github.event.client_payload.role) == 'reviewer' && (inputs.stage || github.event.client_payload.stage) || '' }}
> .github/workflows/agent.yml:84:          elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
> .github/workflows/agent.yml:96:          LOG="logs/$N/${{ github.run_id }}-$ROLE${STAGE:+-$STAGE}.md"
> .github/workflows/agent.yml:104:          python3 -m dokima.agent pack "$N" "$ROLE" "$STAGE" "$PACK" 2> /tmp/pack-err.txt || {
> .github/workflows/agent.yml:111:          if [ "$STAGE" = pr ]; then git diff origin/main...HEAD > "$PACK/diff.patch"; fi
> .github/workflows/agent.yml:119:        if: env.STAGE == 'pr'
> .github/workflows/agent.yml:125:          python3 -m dokima.agent check-pack "$ROLE" "$STAGE" "$PACK" > /tmp/pack-check.txt \
> .github/workflows/agent.yml:135:          case "$ROLE$STAGE" in
> .github/workflows/agent.yml:150:          - $PACK/open_blockers.json: the open blockers from the newest review at your stage. Answer every one by id.$( [ "$STAGE" = pr ] && echo "
> .github/workflows/agent.yml:153:          You are on branch try/issue-$N. Your stage is: ${STAGE:-$ROLE}.
> .github/workflows/agent.yml:174:            python3 -m dokima.agent record "$ROLE" "$STAGE" "$OUT" "$OUT/check.txt" "${PASSED:-false}" /home/runner/.claude/projects
> .github/workflows/agent.yml:180:            python3 -m dokima.agent not-started "$ROLE" "$STAGE" "$OUT" /tmp/why.txt
> .github/workflows/agent.yml:241:          { echo "# ${RO

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["Committed three real hand-backs (issue #132's plan, PR #192's work and code review) under tests/samples/132/, with sources.json linking each record comment, and took them out of the worker's scope.",
          "Added a check to the samples test (158.4): each review sample, graded as a plan review with its asks list taken away, must be rejected."],
  "decided": ["Kept the four criteria and their tests unchanged; only the samples test grew."],
  "open": ["A real plan review with an asks list joins the samples in a follow-up once one is recorded."]},
 "verdict": "approve",
 "summary": "The samples the code review found missing are now on the branch, copied exactly from the records they link to, and every criterion's test fails on main's code for the right reason and passes on this branch, so the plan can go back to work.",
 "blockers": [],
 "notes": [
  {"text": "The samples match their records exactly: each of the three files equals the hand-back in the bot comment that sources.json links to.",
   "evidence": "Fetched issues/comments 6052521274, 6052566514 and 6052592541 from the GitHub API and compared each record's handback with tests/samples/132/plan.json, work.json and review-pr.json: all three equal."},
  {"text": "The new part of the 158.4 test proves the checker requires asks on a plan review (158.2's promise) more than it proves anything about the samples; it is harmless and gives the samples test a real failure on main.",
   "evidence": "With main's dokima/, tests/test_review_asks.py: 4 failed, 158.4 with 'tests/samples/132/review-pr.json graded as a plan review with no asks list passes'; on this branch: 4 passed."},
  {"text": "Three older tests fail when the suite runs with STAGE=plan already set, as in a plan reviewer's machine; CI's full run sets STAGE=pr or none, where they pass.",
   "evidence": "STAGE=plan pytest -q: 3 failed (tests/test_fixer.py::test_ever
```

> rc=0

**Agent:** The check passed even though my review has no asks list and STAGE=plan is set. I'm checking why before I rely on it.

`14. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "asks\|STAGE" dokima/agent.py | head -20; git log -1 --format=%h; env | grep -i pythonpath
```

> 390:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 427:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 431:def problems_asks(r, ids):
> 432:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 434:    asks = r.get("asks")
> 435:    if not isinstance(asks, list) or not asks:
> 436:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 438:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 439:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 467:        bad.append("the worker never asks the owner; the plan is the contract")
> 598:            if kind == "review" and os.environ.get("STAGE") == "plan":
> 599:                bad += problems_asks(data, plan_criteria(plan, number))
> 747:STAGE_COLUMN = {("planner", ""): "Plan", ("reviewer", "plan"): "Plan", ("worker", ""): "Work", ("reviewer", "pr"): "Review"}
> 754:        return STAGE_COLUMN[(step[1], step[2] if step[1] == "reviewer" else "")], False
> 755:    return STAGE_COLUMN.get((rec.get("attempt") or rec.get("role"), rec.get("stage") or ""), "Plan"), True
> 783:    """agent pack N ROLE STAGE DIR | agent check-pack ROLE STAGE DIR | agent check review|work FILE PLAN N |
> 784:    agent record ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR  (writes OUT/record.j

**Agent:** The check ran main's copy of the checker (PYTHONPATH points at /tmp/runtime), and main has no asks rule yet. That is the intended setup, so my review passes. The hand-back is written and passes both checks.

I approved the plan for #158. The samples that the code review found missing are now on the branch.

- **The open blocker is fixed.** The missing samples were B1, from the code review. The planner committed three real hand-backs under `tests/samples/132/`: issue #132's plan, and PR #192's work and code review. I fetched each linked comment from GitHub, and each file matches its record exactly. The samples are out of the worker's scope now.
- **The tests fail on main's code for the right reason.** With main's code, all four tests fail because the feature is missing. On the branch, all four pass. The criteria haven't changed. The planner only added one check to the samples test.

**Notes in the review:**
- The new check in the samples test (158.4) really tests that the checker requires an asks list, not the samples themselves. It's harmless.
- Three older tests fail if the whole suite runs with `STAGE=plan` set, as it is on a plan reviewer's machine. They pass with `STAGE` unset. The workflow only runs the full suite in the code-review job, where `STAGE=pr`, so this doesn't block the plan. I proposed it as a separate issue: those older tests should clear `STAGE` the way `tests/test_review_asks.py` already does.

While comparing against main, I briefly left a stray file in the working tree. I removed it, and `git status` is clean.

The review is in `/tmp/dokima-out/review.json`.
