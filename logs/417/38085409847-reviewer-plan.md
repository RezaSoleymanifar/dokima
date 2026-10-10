# reviewer (plan) for #417

Run: https://github.com/dokima-dev/dokima/actions/runs/38085409847

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (57.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fc729a68-69b5-443a-aedd-7ba5b5c7af31/tool-results/b4n53fs3a.txt
> 
> Preview (first 2KB):
> # Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 368, 425 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/417 · https://github.com/dokima-dev/dokima/pull/447 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/447/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Test cannot pass:** On GitHub the tests of all four criteria, not only 417.4's, run against main's code, not this branch's. tests/test_next_rate_limit.py does `from dokima import agent` without putting the checkout first on sys.path, so where PYTHONPATH points at the runtime copy of Dokima (/tmp/runtime, main's code) a plain `pytest` imports that copy, and no change to dokima/agent.py can reach the test. Smallest fix: insert the repo root at 

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-3000
```

> <persisted-output>
> Output too large (33.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fc729a68-69b5-443a-aedd-7ba5b5c7af31/tool-results/bvi9v1yxx.txt
> 
> Preview (first 2KB):
> # Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 368, 425 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/417 · https://github.com/dokima-dev/dokima/pull/447 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/447/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Test cannot pass:** On GitHub the tests of all four criteria, not only 417.4's, run against main's code, not this branch's. tests/test_next_rate_limit.py does `from dokima import agent` without putting the checkout first on sys.path, so where PYTHONPATH points at the runtime copy of Dokima (/tmp/runtime, main's code) a plain `pytest` imports that copy, and no change to dokima/agent.py can reach the test. Smallest fix: insert the repo root at 

`3. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; cat plan.json
```

> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-worker.json
> 06-reviewer-pr.json
> 07-worker.json
> 08-reviewer-plan.json
> 09-planner.json
> 10-reviewer-plan.json
> 11-worker.json
> 12-reviewer-pr.json
> 13-worker.json
> 14-planner.json
> [
>  {
>   "kind": "blocker",
>   "to": "planner",
>   "label": "Test cannot pass",
>   "text": "On GitHub the tests of all four criteria, not only 417.4's, run against main's code, not this branch's. tests/test_next_rate_limit.py does `from dokima import agent` without putting the checkout first on sys.path, so where PYTHONPATH points at the runtime copy of Dokima (/tmp/runtime, main's code) a plain `pytest` imports that copy, and no change to dokima/agent.py can reach the test. Smallest fix: insert the repo root at the front of sys.path before `from dokima import agent`, as tests/test_budget_retry.py:30-31 does. Nothing the tests check changes.",
>   "evidence": "On 0bc639c, the head, GitHub's check runs 417.1, 417.2, 417.3 and 417.4 all failed at the step \"Run this done-when's tests\" (exit codes 1 and 4), while All tests passed and #446's criterion checks passed (GET /repos/dokima-dev/dokima/commits/0bc639c/check-runs). Here, with PYTHONPATH=/tmp/runtime: `pytest -q tests/test_next_rate_limit.py` gives 10 failed, and /tmp/runtime/dokima/agent.py has no rate_limit_waited_once. A throwaway copy of the same test file with `sys.path.insert(0, <repo root>)` added gives 10 passed under the same plain `pytest`, and so does `PYTHONPATH=. pytho

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests | head -60; python3 -c "
import json;d=json.load(open('/tmp/pack/in/14-planner.json'));print(json.dumps(d,indent=1)[:4000])"
```

> commit d3f94c8a262cd038580d72ec16629d690d5cb699
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 20:51:39 2026 +0000
> 
>     planner for #417 (run 38083776600)
> 
>  tests/test_next_rate_limit.py | 5 ++++-
>  1 file changed, 4 insertions(+), 1 deletion(-)
> commit d3f94c8a262cd038580d72ec16629d690d5cb699
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 20:51:39 2026 +0000
> 
>     planner for #417 (run 38083776600)
> 
> diff --git a/tests/test_next_rate_limit.py b/tests/test_next_rate_limit.py
> index b7a5d0b..820faff 100644
> --- a/tests/test_next_rate_limit.py
> +++ b/tests/test_next_rate_limit.py
> @@ -22,11 +22,14 @@ through `time.time()` and `time.sleep()`.
>  import json
>  import os
>  import subprocess
> +import sys
>  import time
>  
>  import pytest
>  
> -from dokima import agent
> +sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> +sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
> +from dokima import agent  # noqa: E402
>  
>  N = "57"
>  OWNER = "owner-person"
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38083776600",
>  "commit_before": "f97ea00936cd2e6ce0ae8466887877d1395141e8",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 534921,
>   "turns": 16,
>   "cost_usd": 0.8252757999999999,
>   "tokens_in": 1044952,
>   "tokens_out": 5762
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/417/3808377660

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -12; git diff main --stat; grep -n "rate_limit_waited_once" dokima/agent.py | head
```

> d3f94c8 planner for #417 (run 38083776600)
> f97ea00 Merge branch 'main' into try/issue-417
> d270c52 A play-through on a real sandbox repo checks the card after every step from issue to merge (#451)
> 413a926 Merge branch 'main' into try/issue-417
> 3d9fa7b The checks are named All tests and Acceptance criteria, with no done-whens left (#450)
> 0bc639c Merge branch 'main' into try/issue-417
> 24de857 Merge branch 'main' into try/issue-417
> 093a506 A board or card update the budget stopped is retried once the budget is back (#446)
> f036ee8 Run comments show only what has something, in the owner's words, with no codes (#287)
> b263ecb worker for #417 (run 38081230980)
> d99ad64 planner for #417 (run 38080950433)
> 190fae3 Merge branch 'main' into try/issue-417
>  dokima/agent.py               | 178 ++++++++++++++-------
>  tests/test_next_rate_limit.py | 352 ++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 471 insertions(+), 59 deletions(-)
> 1538:def rate_limit_waited_once():
> 2504:            with rate_limit_waited_once():

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainrt; git worktree add -f /tmp/mainrt main -q 2>&1|tail -1; python3 -m pytest -q tests/test_next_rate_limit.py 2>&1|tail -3; PYTHONPATH=/tmp/mainrt python3 -m pytest -q -p no:cacheprovider tests/test_next_rate_limit.py 2>&1|tail -3; PYTHONPATH=/tmp/mainrt pytest -q -p no:cacheprovider tests/test_next_rate_limit.py 2>&1|tail -3
cp tests/test_next_rate_limit.py /tmp/mainrt/tests/; cd /tmp/mainrt; python3 -m pytest -q -p no:cacheprovider tests/test_next_rate_limit.py 2>&1|tail -15
```

> ..........                                                               [100%]
> 10 passed in 0.57s
> ..........                                                               [100%]
> 10 passed in 0.47s
> ..........                                                               [100%]
> 10 passed in 0.47s
>    },
>    "check": {
>     "passed": true,
>     "problems": []
>    }
>   }
>   ```
>   
>   </details>
>   
>   **Next:** @owner-person Autopilot could not be read from GitHub, so nothing starts by itself. The plan is approved. Say `/work` to build it, or `/plan` with changes.
>   
> assert 0 == 1
>  +  where 0 = len([])
> 10 failed in 0.19s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`7. Bash`
```
cd /tmp/mainrt; python3 -m pytest -q -p no:cacheprovider tests/test_next_rate_limit.py 2>&1|grep -E "^(FAILED|E  )" | cut -c1-250 | head -30; cd -; rm /tmp/mainrt/tests/test_next_rate_limit.py; git worktree remove --force /tmp/mainrt
python3 -c "
import json;d=json.load(open('/tmp/pack/in/10-reviewer-plan.json'));print(d.get('posted_at'),json.dumps(d['handback'].get('asks'),indent=1))"; grep -n "^## \|^### \|Comment by\|^\*\*@" /tmp/pack/issue.md | tail -40
```

> E       AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)', not one (the error escaped the step: HTTP 502
> E         <!-- dokima-record -->
> E         <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" 
> E         
> E         <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Stats</b></summary>
> E         
> E         Opus 5.5 · [run](https://github.com/o/r/actions/runs/1)
> E         
> E         </details>
> E         
> E         <details><summary>Full record</summary>
> E         
> E         ```json
> E         {
> E          "role": "planner",
> E          "stage": null,
> E          "run_id": "1",
> E          "run": "https://github.com/o/r/actions/runs/1",
> E          "models": [
> E           "claude-opus-5-5"
> E          ],
> E          "handback": {
> E           "kind": "user_story",
> E           "summary": "s",
> E           "user_story": "u",
> E           "acceptance_criteria": [
> E            {
> E             "text": "a",
> E             "source": "https://github.com/o/r/issues/57"
> E            }
> /home/runner/work/dokima/dokima
> None [
>  {
>   "ask": "When deciding wh

`8. Bash`
```
sed -n 40,80p /tmp/pack/issue.md | cut -c1-1500; for l in 390 597 630; do sed -n "$l,$((l+3))p" /tmp/pack/issue.md|cut -c1-1500; done; sed -n 634,660p /tmp/pack/issue.md | cut -c1-600
```

> **Scope:** `dokima/agent.py`, `tests/test_next_rate_limit.py`
> 
> <details><summary><b>Out of scope</b></summary>
> 
> - agent.yml stays as it is: its `|| NEXT=stop` remains the last resort, and the fix lives in `python3 -m dokima.agent next`.
> - Using less of GitHub's allowance, and tracking it; that is #380 and #368.
> - Retrying board and card updates the rate limit stopped; that is #429.
> - Failures that are not GitHub refusing a call, such as a malformed record file.
> 
> </details>
> 
> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/38084763104/job/114308868020"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> On autop

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 25,35p tests/test_budget_retry.py; cd /tmp && env -u PYTHONPATH pytest -q -p no:cacheprovider /home/runner/work/dokima/dokima/tests/test_next_rate_limit.py 2>&1|tail -2; cd /home/runner/work/dokima/dokima && pytest -q 2>&1|tail -2
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b7x1uwm2y). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/fc729a68-69b5-443a-aedd-7ba5b5c7af31/tasks/b7x1uwm2y.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
head -c 3000 /tmp/claude-1001/-home-runner-work-dokima-dokima/fc729a68-69b5-443a-aedd-7ba5b5c7af31/tasks/b7x1uwm2y.output
```

> import sys
> import time
> 
> import pytest
> 
> sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
> import test_needs_you as tny  # noqa: E402
> from dokima import agent, board, card  # noqa: E402
> 
> SPEC, REPO, NEEDS = tny.SPEC, tny.REPO, tny.NEEDS
> ..........                                                               [100%]
> 10 passed in 0.46s

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner made tests/test_next_rate_limit.py put the repo's own folder first when it imports dokima, the way tests/test_budget_retry.py does, as the owner asked on 20:26."],
  "decided": ["The criteria, the tests and the scope stay as they were; only the test file's import changed.", "Where the runner points Python at the runtime copy of Dokima is left to #449."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan is unchanged except that its test file now imports this branch's Dokima, so each criterion's check tests this branch's code and not main's; it is ready for /work.",
 "raises": [],
 "answers": [
  {"raise": "W2", "answer": "done", "why": "tests/test_next_rate_limit.py:30-32 now puts the repo root first on sys.path before `from dokima import agent`, as tests/test_budget_retry.py:30-31 does. With PYTHONPATH pointed at a checkout of main, plain `pytest -q tests/test_next_rate_limit.py` on this branch gives 10 passed, so the checks now test this branch's code. Run from /tmp with no PYTHONPATH it also gives 10 passed, so 'No module named dokima' is gone. The same file run against main's dokima/agent.py gives 10 failed, each naming its criterion, e.g. '417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason ... (the error escaped the step: HTTP 502'."}
 ],
 "asks": [
  {"ask": "When deciding what runs next fails, the record says so on the issue in one line, with GitHub's reason, instead of stopping silently.", "source": "https://github.com/dokima-dev/dokima/issues/417", "criterion": "417.1"},
  {"ask": "When the failure is GitHub's rate limit, the step is tried again after the limit resets, and starts what it would have started.", "source": "https://github.com/dokima-dev/dokima/issues/417", "criterion": "417.2"},
  {"ask": "this issue is about never losing a step when it runs out.", "source": "https://
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

**Agent:** The summary is over the 25-word cap, so I'm shortening it and running the check again.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The test file now imports this branch's Dokima, so each criterion's check tests this branch's code; nothing else changed, and the plan is ready for /work."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The test file now imports this branch's Dokima, so each criterion's check tests this branch's code; nothing else changed, and the plan is ready."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#417](https://github.com/dokima-dev/dokima/issues/417) (Autopilot sometimes never starts the next step, and says nothing). The approval is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner changed this round:** one thing, as you asked in your 20:26 `/plan` comment. `tests/test_next_rate_limit.py` now puts the repo's own folder first before it imports Dokima, the same way `tests/test_budget_retry.py` does. The criteria, tests and scope are unchanged.

**What I checked:**
- **The worker's blocker W2 (marked done):** the worker raised that every criterion's check was testing main's code instead of this branch's. I pointed Python at a copy of main, the way the runner does, and ran the file on this branch: all 10 tests pass. So each check now tests this branch's code.
- **"No module named dokima":** running the file from outside the repo with no Python path set also passes all 10. That error is gone.
- **Tests fail today for the right reason:** against main's code all 10 fail, and each failure names its criterion and the missing behavior. For example, 417.1 reports that GitHub refused a call and the record holds no line with GitHub's reason.
- **Your asks:** I found three in the issue. They map to 417.1 and 417.2, and none is missing.

I started the full test suite, but it didn't finish within the two-minute limit and kept running in the background. I approved without waiting for it, so I can't say it passes.

**Next:** this is a plan approval, so the river stops for you. Say `/work` to build it, or `/plan` with changes.

`14. Bash`
```
tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/fc729a68-69b5-443a-aedd-7ba5b5c7af31/tasks/b7x1uwm2y.output
```

> 947 passed, 77 skipped in 223.41s (0:03:43)
> 
> [exited with code 0]

**Agent:** The full test suite has now finished on this branch: 947 passed, 77 skipped and none failed. My plan approval for [#417](https://github.com/dokima-dev/dokima/issues/417) (Autopilot sometimes never starts the next step, and says nothing) stays as it was.

**Next:** it's still yours to say `/work` to build it, or `/plan` with changes.
