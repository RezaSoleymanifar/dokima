# reviewer (plan) for #257

Run: https://github.com/dokima-dev/dokima/actions/runs/37835657489

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #257: A finished worker always opens the pull request, even with nothing new to push
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> The worker opens the PR only right after it pushes. When the planner already pushed the whole fix and the worker has nothing new, the push step quits early and the PR is never opened. That happened on #244: the fix for the red tests on main sits on its branch with no PR, code review approved it anyway, and main stays red.
> 
> What I want:
> - When the worker finishes, its PR is opened if none is open, whether or not it pushed anything.
> - A test proves it: a run where the worker has nothing new to push still ends with an open PR for the issue.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #257 (2026-10-08T19:45:53Z)
> 
> /autopilot start
> 
> ### RezaSoleymanifar on issue #257 (2026-10-08T19:46:02Z)
> 
> /plan
> 
> ### dokima-runtime on issue

`2. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python -m pytest -q tests/test_worker_pr.py 2>&1 | tail -20; grep -n "PASSED" tests/test_worker_pr.py | head; sed -n 300,340p .github/workflows/agent.yml
```

> wrong.append(f"{case}: the worker's new code never reached try/issue-{N}: {m.branch_files()}")
> >       assert not wrong, "257.1: " + "\n257.1: ".join(wrong)
> E       AssertionError: 257.1: a worker with nothing new to push: expected 1 pull request(s) opened, got 0: []
> E       assert not ['a worker with nothing new to push: expected 1 pull request(s) opened, got 0: []']
> 
> tests/test_worker_pr.py:115: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_worker_pr.py::test_a_worker_with_nothing_new_to_push_still_opens_its_pull_request - AssertionError: 257.1: the worker had nothing new to push: expected exactly one pull request opened, got 0: []
>   ## run: Copy the runtime from main before touching any branch (exit 0)
>   
>   ## run: Starting branch (exit 0)
>   
>   ## run: Push the planner's tests or the worker's code to try/issue-N (exit 0)
>   Nothing to push.
>   
> assert 0 == 1
>  +  where 0 = len([])
> FAILED tests/test_worker_pr.py::test_only_a_finished_worker_opens_a_pull_request_and_only_when_none_is_open - AssertionError: 257.1: a worker with nothing new to push: expected 1 pull request(s) opened, got 0: []
> assert not ['a worker with nothing new to push: expected 1 pull request(s) opened, got 0: []']
> 2 failed in 1.32s
> 7:from that key up to saving the conversation. The hand-back is taken as passed (PASSED=true), the way the run sets it
> 45:        job = {**job, "env": {**(job.get("env") or {}), "PASSED": "true", "STARTED": "true

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote two acceptance criteria and two tests in tests/test_worker_pr.py that run the agent workflow's real push steps against a local copy of GitHub."],
  "decided": ["A finished worker opens its pull request from try/issue-N into main whenever none is open, whether or not it pushed anything; a planner never opens one.",
              "The fix goes in .github/workflows/agent.yml, where the early exit lives, so the pull request waits for the owner's merge even on autopilot."],
  "open": ["#244 still has no pull request; the plan leaves that to the owner or a new worker run once this lands."]},
 "verdict": "approve",
 "summary": "The plan keeps both of the owner's asks, and its tests run the workflow's own push steps and fail today only because a worker with nothing new to push opens no pull request.",
 "blockers": [],
 "notes": [
  {"text": "No test covers a worker whose hand-back was rejected: the plan says such a run still pushes nothing, but a fix that opened the pull request in a step running on every outcome would pass every test. A case with PASSED=false expecting no pull request would close that gap.",
   "evidence": "tests/test_worker_pr.py:45 sets PASSED to \"true\" for every run; no case sets it false."},
  {"text": "I ran both tests on this branch: each fails only on the case the issue names, while the cases for new code, an already open pull request and the planner already pass, so they catch a fix that goes too broad.",
   "evidence": "pytest -q tests/test_worker_pr.py: 2 failed, 'a worker with nothing new to push: expected 1 pull request(s) opened, got 0'; the push step logs 'Nothing to push.' from .github/workflows/agent.yml:323."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "When the worker finishes, its PR is opened if none is open, whether or not it pushed anything.", "source": "https://github.com/doki
```

> (Bash completed with no output)

**Agent:** I approved the plan for #257. Both checks on my hand-back pass, and it is saved at `/tmp/dokima-out/review.json`.

- **Your asks:** both are covered. "Its PR is opened if none is open, whether or not it pushed anything" is criterion 257.1. "A test proves it: a run where the worker has nothing new to push still ends with an open PR" is criterion 257.2.
- **Tests:** I ran `pytest -q tests/test_worker_pr.py` on this branch. Both tests fail today, and only on the case you named: "a worker with nothing new to push: expected 1 pull request(s) opened, got 0". The push step stops early with "Nothing to push." at `.github/workflows/agent.yml:323`. The other cases already pass: new code, a pull request already open, and the planner. So a fix that opens pull requests where it shouldn't would also turn them red.
- **One gap (a note, not a blocker):** no test covers a worker whose hand-back was rejected. Every test case marks the hand-back as passed (`tests/test_worker_pr.py:45`). So a fix that opens the pull request even after a rejected hand-back would still pass. A case where the hand-back fails and no pull request is expected would close that gap.
- **You'll need to merge it yourself:** the fix has to go in `.github/workflows/agent.yml`. A pull request that changes a workflow file stops for you even on autopilot.
- **Still open:** #244 still has no pull request. The plan leaves that to you, or to a new worker run on #244 once this lands.

The plan had no questions for you, and I found no problems outside this issue.
