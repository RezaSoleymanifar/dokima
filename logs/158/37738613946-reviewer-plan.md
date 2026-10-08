# reviewer (plan) for #158

Run: https://github.com/dokima-dev/dokima/actions/runs/37738613946

`1. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; cat issue.md | head -c 20000
```

> 01-planner.json
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> 06-planner.json
> 07-reviewer-plan.json
> 08-worker.json
> 09-reviewer-pr.json
> 10-planner.json
> []# Issue #158: The reviewer lists every ask in the owner's words, and real hand-backs become test samples
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #198](https://github.com/dokima-dev/dokima/pull/198) · [files changed](https://github.com/dokima-dev/dokima/pull/198/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37737976067/job/113181788987)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 5</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing.
> 
> **Context:** The owner's answer 3 on the issue: the planner cannot check itself for dropped asks because it writes the criteria from the owner's words, so the reviewer reads the issue text on its own and lists every ask; review.json gets a field for exactly this, and the checker rejects a plan review without it. The review.json shape lives in dokima/roles/reviewer.

`2. Bash`
```
cd /tmp/pack; python3 -c "
import re;s=open('issue.md').read();i=s.find('Reviewer (pr)');print(len(s));
" ; grep -n '^### ' issue.md
```

> 63207
> 4:### Checks failing
> 31:### RezaSoleymanifar on issue #158 (2026-10-08T05:06:53Z)
> 35:### dokima-runtime on issue #158 (2026-10-08T05:17:52Z)
> 144:### RezaSoleymanifar on issue #158 (2026-10-08T05:24:21Z)
> 148:### dokima-runtime on issue #158 (2026-10-08T05:26:45Z)
> 230:### RezaSoleymanifar on issue #158 (2026-10-08T05:29:23Z)
> 234:### dokima-runtime on PR #198 (2026-10-08T05:33:27Z)
> 292:### dokima-runtime on PR #198 (2026-10-08T05:35:45Z)
> 395:### dokima-runtime on issue #158 (2026-10-08T05:38:40Z)
> 507:### dokima-runtime on issue #158 (2026-10-08T05:50:16Z)
> 511:### RezaSoleymanifar on issue #158 (2026-10-08T06:17:41Z)
> 515:### dokima-runtime on issue #158 (2026-10-08T06:17:57Z)
> 619:### dokima-runtime on issue #158 (2026-10-08T06:21:01Z)
> 712:### RezaSoleymanifar on issue #158 (2026-10-08T06:24:24Z)
> 716:### dokima-runtime on PR #198 (2026-10-08T06:24:45Z)
> 779:### dokima-runtime on PR #198 (2026-10-08T06:30:30Z)
> 869:### dokima-runtime on issue #158 (2026-10-08T06:33:32Z)
> 975:### dokima-runtime on issue #158 (2026-10-08T06:37:14Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 395,420p issue.md; sed -n 505,530p issue.md; sed -n 619,640p issue.md; sed -n 705,800p issue.md; sed -n 860,1100p issue.md | grep -v '^   *"' | head -150
```

> ### dokima-runtime on issue #158 (2026-10-08T05:38:40Z)
> 
> <!-- dokima-record -->
> **Planner** · hand-back rejected by code
> 
> - ::error title=Planner output rejected::tests/test_review_asks.py::test_a_plan_review_must_list_every_ask_well_formed is a new test that passes today (or is skipped); every new test must fail on today's code; tests/test_review_asks.py::test_a_plan_review_with_a_missing_ask_cannot_approve is a new test that passes today (or is skipped); every new test must fail on today's code; tests/test_review_asks.py::test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers is a new test that passes today (or is skipped); every new test must fail on today's code; tests/test_review_asks.py::test_the_reviewer_prompt_asks_for_every_ask_in_the_owners_words is a new test that passes today (or is skipped); every new test must fail on today's code
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37733173860",
>  "commit_before": "97f70b107aa79105d21ebab2eaf0bdc62463b681",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 141446,
>   "turns": 18,
>   "cost_usd": 0.6339026000000001,
>   "tokens_in": 825262,
>   "tokens_out": 6177
>  },
> 
> 
> ### dokima-runtime on issue #158 (2026-10-08T05:50:16Z)
> 
> Blocked by #201: the re-plan can't land until it is fixed.
> 
> ### RezaSoleymanifar on issue #158 (2026-10-08T06:17:41Z)
> 
> /plan
> 
> ### dokima-runtime on issue #158 (2026-10-08T06:17:57Z)
> 
> <!-- 

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:p[k] for k in p if k not in ('acceptance_criteria',)},indent=1))"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests/test_live_queue.py
```

> {
>  "kind": "user_story",
>  "user_story": "A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing, and real hand-backs are kept as samples that pass their checkers on every test run.",
>  "non_functional": [],
>  "scope": [
>   "dokima/agent.py",
>   "dokima/roles/reviewer.md"
>  ],
>  "out_of_scope": [
>   "Changing .github/workflows/: the review is checked by the same two commands agent.yml runs today (`agent check review FILE PLAN N`, then `agent check-round reviewer FILE PACK`), in a job whose STAGE is plan or pr; a code review's pack also holds the PR's diff.patch.",
>   "Changing the older tests in tests/test_handback_check.py and tests/test_agent.py: they check reviews with no asks list outside a plan review (no STAGE=plan) and must keep passing as they are.",
>   "Showing the asks list on the issue's card; the card is another issue.",
>   "Requiring an asks list on a code review of the pull request.",
>   "A real plan review that carries an asks list as a sample: none can exist until this change merges; it joins the samples as tests/samples/N/review-plan.json in a follow-up.",
>   "Writing the samples: the planner commits tests/samples/132/ (plan.json, work.json, review-pr.json, sources.json) itself, since the fence drops every file under tests/ the worker writes."
>  ],
>  "tests": {
>   "158.1": [
>    "tests/test_review_asks.py::test_the_reviewer_prompt_asks_for_every_ask_in_the_owners

**Agent:** Now run the tests on the branch and the new tests on main.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE timeout 900 pytest -q -x -p no:cacheprovider 2>&1 | tail -5; git diff --stat origin/main...HEAD 2>/dev/null | tail -15
```

> ........................................................................ [ 45%]
> ........................................................................ [ 68%]
> ........................................................................ [ 91%]
> ..........................                                               [100%]
> 314 passed in 114.35s (0:01:54)
>  dokima/agent.py                  |  22 ++++
>  dokima/roles/reviewer.md         |  14 ++-
>  tests/samples/132/plan.json      |  52 +++++++++
>  tests/samples/132/review-pr.json |  24 ++++
>  tests/samples/132/sources.json   |   5 +
>  tests/samples/132/work.json      |  11 ++
>  tests/test_failed_run_card.py    |   3 +-
>  tests/test_live_queue.py         |   3 +-
>  tests/test_review_asks.py        | 243 +++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py              |   7 +-
>  10 files changed, 377 insertions(+), 7 deletions(-)

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt origin/main 2>&1|tail -1; cp -r tests/test_review_asks.py tests/test_live_queue.py tests/test_start.py tests/test_failed_run_card.py /tmp/wt/tests/; cp -r tests/samples /tmp/wt/tests/; cd /tmp/wt; env -u STAGE timeout 600 pytest -q -p no:cacheprovider tests/test_review_asks.py tests/test_live_queue.py tests/test_start.py tests/test_failed_run_card.py 2>&1 | grep -E "FAILED|passed|failed|^E .*(158|Error)" | head -30
```

> E       AssertionError: 158.1: the review.json shape in reviewer.md has no asks list of {"ask": ..., "source": ..., "criterion": "N.k" | "missing"}
> E       AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> E       AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> E                   AssertionError: 158.4: tests/samples/132/review-pr.json graded as a plan review with no asks list passes; the samples are not checked in the settled format: 
> FAILED tests/test_review_asks.py::test_the_reviewer_prompt_asks_for_every_ask_in_the_owners_words - AssertionError: 158.1: the review.json shape in reviewer.md has no asks list of {"ask": ..., "source": ..., "criterion": "N.k" | "missing"}
> FAILED tests/test_review_asks.py::test_a_plan_review_must_list_every_ask_well_formed - AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> FAILED tests/test_review_asks.py::test_a_plan_review_with_a_missing_ask_cannot_approve - AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> FAILED tests/test_review_asks.py::test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers - AssertionError: 158.4: tests/samples/132/review-pr.json graded as a plan review with no asks list passes; the samples are not checked in the settled format: 
> 4 failed, 13 passed in 45.49s
> S

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added an asks entry, matched to criterion 57.1, to the fake plan review in tests/test_live_queue.py, so the two live-card tests that came from main with #203 pass again.",
          "Listed those two tests in the plan's test changes, with the reason."],
  "decided": ["Kept the four criteria, their tests and the scope unchanged."],
  "open": ["A real plan review with an asks list joins the samples in a follow-up once one is recorded."]},
 "verdict": "approve",
 "summary": "The two live-card tests the code review found failing now pass, the whole suite passes on this branch, and every criterion's test still fails on main's code for the right reason, so the build can go on.",
 "blockers": [],
 "notes": [{"text": "The change to the two live-card tests only adds an asks list to their fake plan review; what they prove is unchanged, and they pass on main as well as on this branch.",
            "evidence": "git show d8acdd9 -- tests/test_live_queue.py adds one asks entry; env -u STAGE pytest -q on the branch: 314 passed; on main with the new tests: the 4 tests of tests/test_review_asks.py fail (158.1 to 158.4, the feature missing), the other 13 pass."}],
 "resolved": ["B2"],
 "issues_found": []}
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 158 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

`8. Bash`
```
cd /home/runner/work/dokima/dokima; echo "STAGE=$STAGE"; STAGE=plan python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 158; echo rc=$?
```

> STAGE=plan
> rc=0

**Agent:** I approved the plan. The hand-back is in `/tmp/dokima-out/review.json`, and both required checks pass on it.

**What the planner did this round:** it added one entry to the fake plan review in `tests/test_live_queue.py`. That entry is an asks list matched to criterion 57.1. It also listed the two live-card tests that came from main with #203 under the plan's test changes, with a reason. The four criteria, their tests and the scope are unchanged.

**What I checked:**
- **On this branch:** the full suite passes, 314 tests (run with `env -u STAGE pytest -q`). That includes the two `test_live_queue.py` tests behind the code review's blocker B2, so I marked B2 resolved.
- **On main, with the new tests copied in:**
  - All four tests in `tests/test_review_asks.py` fail, each because the feature is missing (criteria 158.1 to 158.4).
  - The other 13 tests in the four changed files pass, so the test changes only add an asks list and don't change what those tests prove.

There were no open blockers from earlier plan reviews. I added one note recording this evidence and proposed no new issues.
