# reviewer (plan) for #168

Run: https://github.com/dokima-dev/dokima/actions/runs/37687957234

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (51KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6d634efd-0a67-47eb-9428-b433f6e33cd8/tool-results/bii5penrg.txt
> 
> Preview (first 2KB):
> total 56
> drwxr-xr-x 2 runner runner 4096 Oct  7 21:14 .
> drwxr-xr-x 3 runner runner 4096 Oct  7 21:14 ..
> -rw-r--r-- 1 runner runner 5423 Oct  7 21:14 01-planner.json
> -rw-r--r-- 1 runner runner 5165 Oct  7 21:14 02-planner.json
> -rw-r--r-- 1 runner runner 3834 Oct  7 21:14 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5953 Oct  7 21:14 04-planner.json
> -rw-r--r-- 1 runner runner 2239 Oct  7 21:14 05-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2412 Oct  7 21:14 06-worker.json
> -rw-r--r-- 1 runner runner 2781 Oct  7 21:14 07-reviewer-pr.json
> -rw-r--r-- 1 runner runner 6512 Oct  7 21:14 08-planner.json
> # Issue #168: Merge check reads the criteria from the approved plan, not the issue text
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #171](https://github.com/dokima-dev/dokima/pull/171) · [files changed](https://github.com/dokima-dev/dokima/pull/171/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37684793898/job/113009715719)
> 
> <!-- /dokima-card -->
> 
> The merge check "all done-whens passed" fails on every pull request from the new flow,

`2. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; 
```

> 4:### Approve the result to merge
> 19:### RezaSoleymanifar on issue #168 (2026-10-07T19:16:59Z)
> 24:### dokima-runtime on issue #168 (2026-10-07T19:20:55Z)
> 133:### RezaSoleymanifar on issue #168 (2026-10-07T20:21:24Z)
> 137:### dokima-runtime on issue #168 (2026-10-07T20:22:43Z)
> 241:### dokima-runtime on issue #168 (2026-10-07T20:24:09Z)
> 343:### dokima-runtime on issue #168 (2026-10-07T20:25:59Z)
> 453:### dokima-runtime on issue #168 (2026-10-07T20:27:02Z)
> 541:### RezaSoleymanifar on issue #168 (2026-10-07T20:46:20Z)
> 545:### dokima-runtime on PR #171 (2026-10-07T20:48:16Z)
> 599:### dokima-runtime on PR #171 (2026-10-07T20:50:38Z)
> 688:### RezaSoleymanifar on issue #168 (2026-10-07T21:10:36Z)
> 692:### dokima-runtime on issue #168 (2026-10-07T21:14:10Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 130,140p issue.md; sed -n 538,800p issue.md
```

> **Next:** @RezaSoleymanifar The plan has questions for you. Answer with `/plan` and your words, or say `/review` to go on with its assumptions.
> 
> 
> ### RezaSoleymanifar on issue #168 (2026-10-07T20:21:24Z)
> 
> /plan B. If a newer plan isn't approved yet the merge check fails until it is. Nothing merges on an old plan.
> 
> ### dokima-runtime on issue #168 (2026-10-07T20:22:43Z)
> 
> <!-- dokima-record -->
> **Planner**
> **Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 
> 
> ### RezaSoleymanifar on issue #168 (2026-10-07T20:46:20Z)
> 
> /work
> 
> ### dokima-runtime on PR #171 (2026-10-07T20:48:16Z)
> 
> <!-- dokima-record -->
> **Worker**
> 
> The merge check built its checks from criteria written in the issue's text, which plans from the new flow no longer have, so it found nothing and the gate failed every pull request. dokima/checks.py now reads the bot's record comments on the issue (and its pull requests), takes the newest passed plan only when the newest plan review after it approves, and makes one check per criterion running that plan's tests, or one failing 'No approved plan found' check.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "worker",
>  "stage": null,
>  "run_id": "37684569757",
>  "commit_before": "295a29d978dee9f20eab7aab049aeb57dfadbe51",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 76267,
>   "turns": 15,
>   "cost_usd": 0.6363786,
>   "tokens_in": 675278,
>   "tokens_out": 6865
>  },
>  

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['03-reviewer-plan.json','05-reviewer-plan.json']:
  d=json.load(open('in/'+f)); print(f, json.dumps(d.get('handback',d),indent=1)[:2500])
"; cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; cat .github/workflows/done-whens.yml
```

> []03-reviewer-plan.json {
>  "previous_step": {
>   "did": [
>    "Re-planned after the owner's answer B: when a newer plan is handed back, the merge check fails until that plan is approved.",
>    "Added that case to 168.1 and 168.3 and to their tests (a newer plan not yet reviewed, and a newer plan blocked)."
>   ],
>   "decided": [
>    "Only dokima/checks.py changes; the done-whens workflow stays as it is.",
>    "Three old tests that read criteria from the issue's text are deleted, each replaced by a 168 test."
>   ],
>   "open": [
>    "The planner flags that a pull request changing dokima/checks.py also changes the check that judges it, and suggests a separate issue."
>   ]
>  },
>  "verdict": "block",
>  "summary": "The plan follows the owner's answer, but no test has the records an issue really holds at merge time (the worker's and the code review's after the plan approval), so a check that still fails every real pull request would pass these tests.",
>  "blockers": [
>   {
>    "id": "B1",
>    "criterion": "168.1",
>    "test": "tests/test_merge_check.py::test_one_check_per_criterion_of_the_approved_plan_running_exactly_its_tests",
>    "problem": "Every passing case ends with the plan review approval as the very last record. On a real issue the worker's record, and code-stage reviewer records, come after the approval (agent.yml posts the worker's record on the issue when no PR is open yet). A check that takes 'the newest record must be a plan approval', or treats a code-stage block as overturning the plan

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show 34e9ff3 -- tests/test_merge_check.py | head -120
```

> commit 34e9ff3ecad2160c19c26dcb5ffbe01c732e46d6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:14:00 2026 +0000
> 
>     planner for #168 (run 37687521078)
> 
> diff --git a/tests/test_merge_check.py b/tests/test_merge_check.py
> index d6dcdc5..9e47d0d 100644
> --- a/tests/test_merge_check.py
> +++ b/tests/test_merge_check.py
> @@ -4,9 +4,13 @@ Every test here runs the real command the "done-whens" workflow runs, `python3 -
>  root, with GitHub faked: a stub `gh` on PATH answers from a JSON file in a temp folder, and the pull request event is a
>  temp file. The issue's records are real record comments, drawn by dokima.agent.render, so the check reads exactly what
>  the bot posts. Nothing here touches the network.
> +
> +The last test reads the done-whens workflow itself (issue #168, the owner's later comment): the merge check must run
> +main's copy of its workflow and of Dokima's code, so a pull request can never change the check that judges it.
>  """
>  import json
>  import os
> +import re
>  import subprocess
>  import sys
>  
> @@ -225,3 +229,70 @@ def test_records_pasted_by_anyone_but_the_bot_do_not_count(record_property, tmp_
>      code, rows, out = run_matrix(tmp_path, [planned(PLAN), reviewed(APPROVE)])
>      assert rows is not None and len(rows) == 3, f"168.4: the bot's own records did not count: {rows}\n{out}"
>  
> +
> +
> +def workflow_jobs(text):
> +    """Each job of a workflow as (name, job-level text before its steps, [step texts]), read without a YAML 

**Agent:** Reviewing the plan for #168: running the planner's tests now, then writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_merge_check.py 2>&1 | tail -15; python3 -m pytest -q 2>&1 | tail -3; git diff main --stat
```

> on = re.split(r"(?m)^[a-z]", text.split("\non:\n", 1)[1], 1)[0]
> >       assert re.search(r"(?m)^  pull_request_target:", on), \
>             "168.5: the merge check is not triggered by pull_request_target, so GitHub runs the pull request's copy of it"
> E       AssertionError: 168.5: the merge check is not triggered by pull_request_target, so GitHub runs the pull request's copy of it
> E       assert None
> E        +  where None = <function search at 0x7f5ee7ff3060>('(?m)^  pull_request_target:', '  pull_request:\n')
> E        +    where <function search at 0x7f5ee7ff3060> = re.search
> 
> tests/test_merge_check.py:266: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code - AssertionError: 168.5: the merge check is not triggered by pull_request_target, so GitHub runs the pull request's copy of it
> assert None
>  +  where None = <function search at 0x7f5ee7ff3060>('(?m)^  pull_request_target:', '  pull_request:\n')
>  +    where <function search at 0x7f5ee7ff3060> = re.search
> 1 failed, 6 passed in 1.98s
>  +  where None = <function search at 0x7f42befef060>('(?m)^  pull_request_target:', '  pull_request:\n')
>  +    where <function search at 0x7f42befef060> = re.search
> 1 failed, 183 passed in 5.25s
>  dokima/checks.py          |  45 ++++---
>  tests/test_checks.py      |  42 +------
>  tests/test_merge_check.py | 298 ++++++++++++++++++++++++++++++++++++++++

**Agent:** Testing whether the 168.5 test catches a workflow that drops its permissions block.

`7. Bash`
```
rm -rf /tmp/mut && cp -r /home/runner/work/dokima/dokima /tmp/mut && cd /tmp/mut && cat > .github/workflows/done-whens.yml <<'EOF'
name: done-whens
on:
  pull_request_target:
jobs:
  list:
    name: list done-whens
    runs-on: ubuntu-24.04
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
    steps:
      - uses: actions/checkout@v5
      - id: m
        env:
          GH_TOKEN: ${{ github.token }}
        run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
  check:
    needs: list
    name: ${{ matrix.name }}
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          path: main
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          path: pr
      - name: Run
        working-directory: pr
        run: |
          pytest -rA $TESTS
      - name: Annotate
        working-directory: main
        run: python3 -m dokima.checks annotate ../pr/r.xml
EOF
python3 -m pytest -q tests/test_merge_check.py -k mains_code 2>&1 | tail -2
```

> .                                                                        [100%]
> 1 passed, 6 deselected in 0.04s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`8. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Added criterion 168.5 from the owner's latest comment: the merge check runs main's copy of its workflow and of Dokima's code, and only the tests and the code they judge come from the pull request.",
   "Added the done-whens workflow to the scope and one test that reads the workflow step by step."
  ],
  "decided": [
   "The check must name no key and ask for no write permission, since it runs the pull request's code; other pull request workflows (full suite) stay as they are."
  ],
  "open": [
   "Pull request #171 is judged by main's old check once this runs, so it needs the owner's override one last time."
  ]
 },
 "verdict": "block",
 "summary": "The plan folds in the owner's ask, but the 168.5 test passes a merge check that drops its permissions list, which on pull_request_target can hand the pull request's tests a token that can write to the repo.",
 "blockers": [
  {
   "id": "B2",
   "criterion": "168.5",
   "test": "tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code",
   "problem": "168.5 promises the merge check asks for no write permission. The test only looks for a line that says 'write'; a workflow with no permissions list at all passes. On pull_request_target the token then gets the repository's default permissions, which can be read and write, while the job runs the pull request's own tests and setup files (and actions/checkout leaves the token in the checkout). That is the exact hole moving to pull_request_target opens, and the test would not catch it.",
   "evidence": "Copied the repo to /tmp/mut and replaced done-whens.yml with a workflow on pull_request_target, main's checkout for the Dokima steps, the pull request's checkout for pytest, and no permissions list: `pytest -q tests/test_merge_check.py -k mains_code` gives 1 passed. On this branch the same test fails today for the right reason (still 
```

> (Bash completed with no output)

**Agent:** I blocked the plan for #168. The planner added what you asked for in your last comment, but the test for it misses one way the change can go wrong. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the planner did:** It added criterion 168.5. The merge check must run main's copy of its workflow and of Dokima's code, and only the tests (plus the code they judge) come from the pull request. It must also name no key and ask for no write permission. The planner added `.github/workflows/done-whens.yml` to the scope and wrote one test that reads that workflow step by step.

**Blocker B2 (criterion 168.5):**
- **The gap:** the test only looks for a line saying "write". A workflow with no permissions list at all passes it.
- **Why it matters:** with no list, the check's built-in GitHub token gets the repo's default permissions, which can include write. The check would run the pull request's own tests and setup files with that token, and checking out the pull request's code leaves the token in that folder. Moving the check to run main's copy opens exactly this hole.
- **How I confirmed it:** I copied the repo to `/tmp/mut` and replaced `done-whens.yml` with a version that is correct apart from having no permissions list. The 168.5 test passed against it.
- **Smallest fix:** the test should also require a top-level permissions list where every entry is "read" or "none", and allow no job-level permissions other than read or none.

**Test runs:**
- **168.5:** fails today for the right reason: the check still runs the pull request's own copy of the workflow.
- **168.1 to 168.4:** all six tests already pass with the worker's earlier code.
- **Full suite:** 183 passed, 1 failed (the 168.5 test).

**Notes (not blockers):**
- Dokima's bot can't push workflow changes, and the pause for workflow changes isn't built yet. You may need to push or approve `done-whens.yml` yourself.
- 168.5 says the check "names no key", but one step still needs GitHub's built-in read-only token to look up the issue's records. The test allows that token, which is the right reading, but the criterion's wording could say so.

The planner also raised that pull request #171 will be judged by main's old check once this lands, so it will need your override one last time.
