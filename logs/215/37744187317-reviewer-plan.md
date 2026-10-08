# reviewer (plan) for #215

Run: https://github.com/dokima-dev/dokima/actions/runs/37744187317

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:33 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:34 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:33 in
> -rw-r--r--  1 runner runner 23073 Oct  8 07:33 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:33 open_blockers.json
> -rw-r--r--  1 runner runner  3459 Oct  8 07:33 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:33 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:33 ..
> -rw-r--r-- 1 runner runner 2146 Oct  8 07:33 01-planner.json
> -rw-r--r-- 1 runner runner 2791 Oct  8 07:33 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1512 Oct  8 07:33 03-worker.json
> -rw-r--r-- 1 runner runner 4002 Oct  8 07:33 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4070 Oct  8 07:33 05-planner.json
> # Issue #215: Main is red: the cancelled-run test's fake plan review fails the new asks check
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: main's full suite is green again**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure passes on main, with its fake plan review's asks matched to a criterion the fake plan actually has
> *Verified by: the full suite on main passes*
> 
> </dd></dl>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="ab

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; git diff main --stat; git diff main -- tests/; ls tests/test_cancelled_run_fakes.py 2>&1
```

> Exit code 2
> commit 9187da3c447dfe9d65c8fbc2b30354a131d6338d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:33:29 2026 +0000
> 
>     planner for #215 (run 37743621270)
> 
>  tests/test_cancelled_run.py       | 15 +++++++++--
>  tests/test_cancelled_run_fakes.py | 56 ---------------------------------------
>  2 files changed, 13 insertions(+), 58 deletions(-)
> 
> commit fdac0dd816e166c8d85d9df26be85745c3f69f6f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:08:28 2026 +0000
> 
>     planner for #215 (run 37741108425)
> 
>  tests/test_cancelled_run_fakes.py | 56 +++++++++++++++++++++++++++++++++++++++
>  1 file changed, 56 insertions(+)
> 
> commit 60dee993eef1d5ed4463d19badcd4f91ea281b6a
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 01:58:03 2026 -0500
> 
>     Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off (#214)
>     
>     * planner for #209 (run 37738831571)
>     
>     * worker for #209 (run 37739600049)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
> 
>  .github/workflows/commands.yml |  44 ++++++-
>  AGENTS.md                      |   3 +
>  dokima/agent.py                |  67 +++++++++-
>  tests/test_autopilot.py        | 281 +++++++++++++++++++++++++++++++++++++++++
>  4 files cha

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 25,120p tests/test_cancelled_run.py; grep -n "^STORY\b\|^STORY =\|^APPROVE\|^N =" tests/test_start.py; grep -n "def plan_criteria" -A12 dokima/agent.py
```

> # A blocking review of the one-story plan (only criterion: 57.1), so every ask it lists is matched to 57.1 (#215).
> BLOCK = dict(APPROVE, verdict="block", summary="57.1 has no test that would fail without the work.",
>              asks=[dict(a, criterion="57.1") for a in APPROVE["asks"]],
>              blockers=[{"id": "B1", "criterion": "57.1", "problem": "The test only checks a file exists.",
>                         "evidence": "tests/test_x.py::test_a", "fix": "Run the thing and check its output.",
>                         "test": "tests/test_x.py::test_a", "fixer": "planner"}])
> AGENT = "The agent (Claude Code)"
> 
> # Runs cancelled part way: name -> (role, stage, history, options, review, the step it is cancelled at, where its card is).
> CANCELLED = {
>     "gate": ("reviewer", "plan", STORY_PLANNED, None, None, "Only a code owner starts an agent", ("issue", N)),
>     "install": ("worker", "", STORY_APPROVED, None, None, "Install pytest and Claude Code", ("issue", N)),
>     "planner": ("planner", "", [owner_comment("/plan", "2026-10-07T10:00:00Z")], None, None, AGENT, ("issue", N)),
>     "reviewer": ("reviewer", "plan", STORY_PLANNED, None, None, AGENT, ("issue", N)),
>     "worker": ("worker", "", STORY_APPROVED, {"pr_open": True}, None, AGENT, ("pr", PR)),
>     "after-check": ("reviewer", "plan", STORY_PLANNED, None, BLOCK, "Code checks the hand-back", ("issue", N)),
> }
> 
> 
> @pytest.fixture(scope="module")
> def runs(tmp_path_factory):
>     """Every scenario these tests read, each run once th

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^STORY_PLANNED" -A3 tests/test_start.py | head; env -u STAGE python -m pytest -q tests/test_cancelled_run.py 2>&1 | tail -3; cp tests/test_cancelled_run.py /tmp/branch.py; git show main:tests/test_cancelled_run.py > /tmp/main.py; # revert only BLOCK asks line
grep -v 'asks=\[dict(a, criterion="57.1")' /tmp/branch.py > tests/test_cancelled_run.py; env -u STAGE python -m pytest -q tests/test_cancelled_run.py 2>&1 | grep -E "Error|passed|failed" | head -5; cp /tmp/branch.py tests/test_cancelled_run.py; git status --short
```

> 645:STORY_PLANNED = [owner_comment("/plan", "2026-10-07T10:00:00Z"), record_comment(planner_record(STORY), "2026-10-07T10:10:00Z")]
> 646-STORY_APPROVED = STORY_PLANNED + [record_comment(review_record(APPROVE), "2026-10-07T10:20:00Z"),
> 647-                                  owner_comment("/work", "2026-10-07T10:30:00Z")]
> 648-
> ....                                                                     [100%]
> 4 passed in 7.92s
>         Every cancelled run (including one cancelled after its blocking review had passed code's check, which the river
>         would otherwise send back to the planner), a review code rejected and a run whose tools failed to install must
>         make no call that starts or re-runs a run, and each must still have been seen as cancelled or failed. Beside them,
>             assert r.failed, f"188.3 ({name}): setup: the run did not fail:\n{r.tail()}"
> E       AssertionError: 215.1: the fake blocking review matches asks to criteria its fake plan does not have (['57.1']): [{'ask': 'Fix it.', 'source': 'https://github.com/o/r/issues/57', 'criterion': 'S1.1'}]

`5. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE timeout 500 python -m pytest -q -x -n auto 2>&1 | tail -3 || true
```

> inifile: None
>   rootdir: /home/runner/work/dokima/dokima

**Agent:** Running the full suite on the plan branch now (it takes about two minutes), to confirm main would be green.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE timeout 500 python -m pytest -q 2>&1 | tail -3
```

> ........................................................................ [ 84%]
> ...................................................                      [100%]
> 339 passed in 125.07s (0:02:05)

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Changed the fake blocking plan review in tests/test_cancelled_run.py itself, so every ask it lists names 57.1, the fake plan's only criterion.",
          "Added to the cancelled-run test a check that the fake review's asks all name the fake plan's criteria and that code accepts its hand-back.",
          "Removed tests/test_cancelled_run_fakes.py and folded its proof into the cancelled-run test."],
  "decided": ["Merged the two criteria into one, 215.1; the worker has no code left to write, and the plan needs /work again."],
  "open": []},
 "verdict": "approve",
 "summary": "The fix is now in the plan itself, the cancelled-run test passes with it and fails without it for the reason the issue names, and the full suite is green.",
 "blockers": [],
 "notes": [
  {"text": "The fix is already on the branch, so the worker has nothing to change; after /work the pull request holds only the planner's change to tests/test_cancelled_run.py.",
   "evidence": "git diff main --stat: tests/test_cancelled_run.py | 15 +++++++++++++-- (1 file changed)"},
  {"text": "Without the one-line fix the test fails with the issue's reason, not a crash; with it the full suite passes.",
   "evidence": "Removing the asks=[dict(a, criterion=\"57.1\") ...] line: 'AssertionError: 215.1: the fake blocking review matches asks to criteria its fake plan does not have (['57.1']): [... 'criterion': 'S1.1'}]'. env -u STAGE python -m pytest -q on the branch: 339 passed."},
  {"text": "The round-one check that code still rejects an ask matched to S1.1 is gone; the owner did not ask for it, and dokima/agent.py is not in this plan's scope.",
   "evidence": "Commit 9187da3 deletes tests/test_cancelled_run_fakes.py; plan scope is ['tests/test_cancelled_run.py']."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "main's full suite is green again", "source": "https://github.com/do
```

> 0

**Agent:** I approved the new plan for #215. My review is in `/tmp/dokima-out/review.json`, and both hand-back checks passed it.

- **What changed since the last round:** the planner made the fix itself, in `tests/test_cancelled_run.py`. Last round the worker's fix was thrown away because the worker may never change test files. The fake blocking plan review now matches every ask to 57.1, the fake plan's only criterion, instead of S1.1.
- **One criterion now:** the planner merged the two criteria into one, 215.1. The cancelled-run test now also checks two things: that every ask in the fake review names a criterion the fake plan has, and that code accepts that review's hand-back. The separate test file from round one is deleted.
- **It fails without the fix for the right reason:** I took the one-line fix out and the test failed with "215.1: the fake blocking review matches asks to criteria its fake plan does not have", naming S1.1. That is the problem the issue describes, not a crash.
- **The full suite passes on the branch:** 339 passed. I ran it with the `STAGE` variable unset, because it causes unrelated failures inside agent runs.
- **Your three asks** (full suite green, the named test passes, the fake review's asks matched to a real criterion) all map to 215.1.

Three things to know before you say `/work`:
- The fix is already on the branch, so the worker has nothing to build. The pull request will hold only the planner's change to `tests/test_cancelled_run.py`.
- Round one also tested that code still rejects an ask matched to S1.1. That test is gone. You didn't ask for it, and the code that runs that check is outside this plan's scope.
- The last code review raised two blockers. I left them off my resolved list because they belong to the code-review stage, not the plan stage. The fix for both is the change above.
