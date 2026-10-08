# reviewer (plan) for #257

Run: https://github.com/dokima-dev/dokima/actions/runs/37835444461

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json 2>/dev/null
```

> .:
> total 36
> drwxr-xr-x  3 runner runner  4096 Oct  8 19:56 .
> drwxrwxrwt 18 root   root    4096 Oct  8 19:56 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 19:56 in
> -rw-r--r--  1 runner runner 13600 Oct  8 19:56 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 19:56 open_blockers.json
> -rw-r--r--  1 runner runner  2297 Oct  8 19:56 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 19:56 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 19:56 ..
> -rw-r--r-- 1 runner runner 2886 Oct  8 19:56 01-planner.json
> -rw-r--r-- 1 runner runner 2889 Oct  8 19:56 02-planner.json
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
> The worker opens the PR only right after it pushes. When the planner already pushed the whole fix and the worker has nothing new, the push step quits early and the PR is

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_worker_pr.py; git show --stat HEAD; sed -n 280,360p .github/workflows/agent.yml
```

> """A finished worker always ends with its pull request open, even when it has nothing new to push (#257).
> 
> On #244 the planner had already pushed the whole fix, the worker had nothing new, the push step quit early and the
> pull request was never opened. These tests run the real steps of .github/workflows/agent.yml that take a finished
> run's work to GitHub, with the machine from test_start.py (a temp repo whose origin is a local bare repo, a fake
> `gh` that records every call): copying the runtime, checking out try/issue-57, minting the app's key, then every step
> from that key up to saving the conversation. The hand-back is taken as passed (PASSED=true), the way the run sets it
> once the code's check accepts it. A pull request is opened when the fake `gh` is asked `gh pr create` for the head
> try/issue-57; options.json's pr_open makes #60 already open for it.
> """
> 
> import test_start as ts
> from test_start import N, OWNER, Ctx
> 
> 
> def push_steps(change=None):
>     """The steps of agent.yml that take a finished run's work to GitHub, with a step making `change` (a shell line)
>     in the worker's checkout right after the branch is checked out, as the agent would."""
>     wf = ts.workflow("agent.yml")
>     job = wf["jobs"]["run"]
>     steps = job["steps"]
>     named = {s.get("name"): s for s in steps}
>     app = next(i for i, s in enumerate(steps) if s.get("id") == "app")
>     end = next(i for i, s in enumerate(steps) if str(s.get("name", "")).startswith("Save the conversation"))
>     picked = [na

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_worker_pr.py 2>&1 | tail -60
```

> E         ## run: Push the planner's tests or the worker's code to try/issue-N (exit 0)
> E         Nothing to push.
> E         
> E       assert 0 == 1
> E        +  where 0 = len([])
> 
> tests/test_worker_pr.py:68: AssertionError
> _ test_only_a_finished_worker_opens_a_pull_request_and_only_when_none_is_open __
> 
> record_property = <function record_property.<locals>.append_property at 0x7f32d96618a0>
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_only_a_finished_worker_op0')
> 
>     def test_only_a_finished_worker_opens_a_pull_request_and_only_when_none_is_open(record_property, tmp_path):
>         """Only a finished worker opens a pull request, once, whether or not it pushed anything.
>     
>         Six runs of the agent workflow's real push steps: a worker with nothing new and a worker with new code, with no
>         pull request open (each must open exactly one from try/issue-57 into main, and the new code must reach the branch);
>         the same two with #60 already open (neither may open another); and a planner with nothing new and with a new test
>         (neither may open one). Every case is run and every one that goes wrong is named."""
>         record_property("proves", "257.1")
>         fix, new_test = "echo 'x = 1' > fix.py", "printf 'def test_b():\\n    pass\\n' > tests/test_y.py"
>         wrong = []
>         for case, role, change, pr_open, want in (
>                 ("a worker with nothing new to push", "worker", None, False, 1),
>                 ("a worker that pushed new code

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote two acceptance criteria and two tests in tests/test_worker_pr.py that run the agent workflow's real push steps against a local copy of GitHub."],
  "decided": ["A finished worker opens its pull request from try/issue-N into main whenever none is open, whether or not it pushed anything; a planner never opens one.",
              "The fix goes in .github/workflows/agent.yml, the only place the early exit lives, so the pull request will wait for the owner's merge even on autopilot."],
  "open": ["#244 still has no pull request; the plan leaves that to the owner or a new worker run once this lands."]},
 "verdict": "approve",
 "summary": "The plan covers both asks, and its tests run the workflow's own push steps and fail today only because a worker with nothing new to push opens no pull request.",
 "blockers": [],
 "notes": [
  {"text": "No test covers a worker whose hand-back was rejected: the plan's out-of-scope says such a run pushes nothing, but a fix that opened the pull request in a step running on every outcome would pass every test. Worth a case with PASSED=false expecting no pull request.",
   "evidence": "tests/test_worker_pr.py:44 sets PASSED to \"true\" for every Finish run; no case sets it false."},
  {"text": "I ran both tests on this branch: each fails only on the case the issue names, 'a worker with nothing new to push: expected 1 pull request(s) opened, got 0', while the other five cases (new code, an already open #60, the planner) already pass, so they guard against the fix going too broad.",
   "evidence": "pytest -q tests/test_worker_pr.py: 2 failed; the push step log shows 'Nothing to push.' from .github/workflows/agent.yml:323."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "When the worker finishes, its PR is opened if none is open, whether or not it pushed anything.", "source": "https://github.com/dokima-dev/dokima
```

> Exit code 1
> the ask "When the worker finishes, its PR is opened if none is open, whether or not it pushed anything." is matched to 1.1, which is not a criterion of the plan (257.1, 257.2)
> the ask "A test proves it: a run where the worker has nothing new to push still ends with an open PR for the issue." is matched to 1.2, which is not a criterion of the plan (257.1, 257.2)

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"criterion": "1.1"/"criterion": "257.1"/; s/"criterion": "1.2"/"criterion": "257.2"/' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 257 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #257. The hand-back is written to `/tmp/dokima-out/review.json` and passes both checks.

- **Both asks are covered.** The owner's first ask is criterion 257.1: when the worker finishes, its pull request is opened if none is open, whether or not it pushed anything. The test ask is criterion 257.2. Neither is missing.
- **Both new tests fail today for the right reason.** I ran `tests/test_worker_pr.py` on this branch. Each fails only on the case the issue describes: "a worker with nothing new to push: expected 1 pull request(s) opened, got 0". The run logs "Nothing to push." from the early exit at `.github/workflows/agent.yml:323`.
- **The tests also catch a fix that goes too far.** The other five cases already pass: a worker with new code, a pull request already open as #60, and a planner with or without a new test. So a fix that opened a second pull request, opened one for the planner, or stopped pushing new code would turn a test red.
- **One gap, left as a note rather than a blocker.** Every test run treats the worker's hand-back as accepted, so none covers a rejected one. A fix that opened the pull request on every outcome would still pass. Adding one case where the hand-back is rejected and no pull request is expected would close it.

The plan has no questions for the owner and no earlier blockers. The fix has to change a workflow file, so even on autopilot the pull request will wait for the owner to merge it.
