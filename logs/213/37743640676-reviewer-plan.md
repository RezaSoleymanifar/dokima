# reviewer (plan) for #213

Run: https://github.com/dokima-dev/dokima/actions/runs/37743640676

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (36.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d881b54e-ce56-4c6e-b22a-f18d5dba08ba/tool-results/bhrcigtg3.txt
> 
> Preview (first 2KB):
> .:
> total 60
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:28 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:28 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:28 in
> -rw-r--r--  1 runner runner 34584 Oct  8 07:28 issue.md
> -rw-r--r--  1 runner runner  1635 Oct  8 07:28 open_blockers.json
> -rw-r--r--  1 runner runner  6606 Oct  8 07:28 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:28 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:28 ..
> -rw-r--r-- 1 runner runner 5442 Oct  8 07:28 01-planner.json
> -rw-r--r-- 1 runner runner 5491 Oct  8 07:28 02-planner.json
> -rw-r--r-- 1 runner runner 7124 Oct  8 07:28 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7246 Oct  8 07:28 04-planner.json
> # Issue #213: Autopilot: children start once their blockers merge, and the tree switches itself off when done
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
> <details open><summary>From the approved plan of #205, story 5</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (33.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d881b54e-ce56-4c6e-b22a-f18d5dba08ba/tool-results/buwy4b70s.txt
> 
> Preview (first 2KB):
> # Issue #213: Autopilot: children start once their blockers merge, and the tree switches itself off when done
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
> <details open><summary>From the approved plan of #205, story 5</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, each child of a split starts planning by itself as soon as everything it waits on has merged, with one Autopilot line where the owner would have typed `/plan`, and when the whole tree is done the parent closes and autopilot ends, with no one switching it off.
> 
> **Context:** Both halves react to the same event, an issue closing when its pull request merges, which needs a workflow trigger, so this story must say so explicitly. Overlaps #86 (start children when blockers merge); fold #86 in or close it as a duplicate of this story, per AGENTS.md Changing scope. AGENTS.md Splitting already says 'When a child merges, every sibling whose needs h

`3. Read`
```
/tmp/pack/issue.md
```

> 1	# Issue #213: Autopilot: children start once their blockers merge, and the tree switches itself off when done
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
> 13	<details open><summary>From the approved plan of #205, story 5</summary>
> 14	
> 15	**Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 16	
> 17	**User story:** On autopilot, each child of a split starts planning by itself as soon as everything it waits on has merged, with one Autopilot line where the owner would have typed `/plan`, and when the whole tree is done the parent closes and autopilot ends, with no one switching it off.
> 18	
> 19	**Context:** Both halves react to the same event, an issue closing when its pull request merges, which needs a workflow trigger, so this story must say so explicitly. Overlaps #86 (start children when blockers merge); fold #86 in or close it as a duplicate of this story, per AGENTS.md Changing scope. AGENTS.md Splitting already says 'When a child merges, every sibling whose needs have landed starts'. Blocked-by links are native GitHub issue dependencies (repos/{repo}/issues/N/dependencies/blocked_by, filed by file_split in dokima/agent.py). The p

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff cc3b648 HEAD -- tests | head -400
```

> commit 73f8fd776d03647f6109a84a2a23f24add3eff75
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:28:14 2026 +0000
> 
>     planner for #213 (run 37742731881)
> 
>  tests/test_autopilot_close.py | 140 ++++++++++++++++++++++++++++++++++++++++--
>  1 file changed, 134 insertions(+), 6 deletions(-)
> diff --git a/tests/test_autopilot_close.py b/tests/test_autopilot_close.py
> index 0ce7e87..671d781 100644
> --- a/tests/test_autopilot_close.py
> +++ b/tests/test_autopilot_close.py
> @@ -18,6 +18,8 @@ The fake GitHub knows an issue tree and keeps it in tree.json, labels.json, stat
>    - labels change through `gh issue edit N --add-label/--remove-label` or the REST labels API, as in test_autopilot.
>    - `gh issue view N` shows issue N (number, title, body, state, stateReason, labels, comments); `gh issue close N`
>      closes it (--reason, -r, and --comment/-c, which posts that comment); `gh issue comment N` comments on it.
> +  - `gh api repos/o/r/issues` (GET, with labels= and state= in the query string or as -f fields) and
> +    `gh issue list --label L --state S --json ...` list the issues it knows, filtered the same way (no --jq).
>    - `gh api repos/o/r/actions/runs/ID` says whether run ID is still going (in_progress) or completed.
>    - a signal to start a stage is `gh api repos/o/r/dispatches` with -f/-F event_type=... client_payload[...]=...,
>      or --input with that JSON; every one is kept with the key it was sent with. Only Dokima's app key 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_autopilot_close.py tests/test_autopilot.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|^E  .*21[3]" | head -60
```

> assert not m.failed, f"213.1: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E           AssertionError: 213.1 (close): #102's planner was started 0 times, expected once; started: {}
>         assert not m.failed, f"213.1 (split on autopilot): the listener failed on /work:\n{m.tail()}"
> E           AssertionError: 213.1 (split on autopilot): #900's planner was started 0 times, expected once; started: {}
>         assert not m.failed, f"213.1 (/autopilot start): the listener failed:\n{m.tail()}"
> E           AssertionError: 213.1 (/autopilot start): #101's planner was started 0 times, expected once; started: {}
>         assert not m.failed, f"213.2 (last one): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E       AssertionError: 213.2 (last one): #57 is ('open', None) after its last open sub-issue closed, expected closed as completed
>         assert not m.failed, f"213.3 (tree): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E       AssertionError: 213.3 (tree): the done tree left these issues on autopilot: [57, 101, 102]
>             assert not m.failed, f"213.4 ({case}, sibling): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E               AssertionError: 213.4 (on autopilot, sibling): #102 should start once when #101 closes: {}
>         assert not m.failed, f"213.5: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E           AssertionError: 213.5 (first close): #102's planner was started 0 times, expected on

**Agent:** Twelve new tests fail today because the feature is missing. Next I'm checking which existing workflows already run when an issue closes, since the queue test covers every job that acts.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -n -A4 "^on:" .github/workflows/*.yml | grep -n -i -E "issues|closed|types" ; grep -n "concurrency" -A3 .github/workflows/*.yml
```

> agent.yml
> assign.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> wiki.yml
> worker.yml
> 2:.github/workflows/assign.yml-5-  issues:
> 3:.github/workflows/assign.yml-6-    types: [opened]
> 8:.github/workflows/agent.yml-14-    types: [dokima-next]
> 15:.github/workflows/done-whens.yml-8-  issues: read
> 17:.github/workflows/worker.yml-8-  issues:
> 18:.github/workflows/worker.yml-9-    types: [labeled, unlabeled]
> 23:.github/workflows/commands.yml-14-    types: [created]
> 25:.github/workflows/commands.yml-16-    types: [submitted]
> 32:.github/workflows/board.yml-7-  issues:
> 33:.github/workflows/board.yml-8-    types: [labeled, unlabeled, closed]
> 35:.github/workflows/board.yml-10-    types: [created]
> 39:.github/workflows/card.yml-9-    types: [completed]
> 40:.github/workflows/card.yml-10-  issues:
> 47:.github/workflows/planner.yml-9-  issues:
> 48:.github/workflows/planner.yml-10-    types: [labeled]
> .github/workflows/agent.yml:36:concurrency:
> .github/workflows/agent.yml-37-  group: agent-${{ (inputs.issue || github.event.client_payload.issue) }}
> .github/workflows/agent.yml-38-  cancel-in-progress: false
> .github/workflows/agent.yml-39-permissions:
> .github/workflows/board.yml:20:concurrency:
> .github/workflows/board.yml-21-  group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
> .github/workflows/board.yml-22-  cancel-in-progress: false
> .github/workflows/board.yml-23-jobs:
> .github/workflows/card.yml:12:concurrency:
> .github/work

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,20p .github/workflows/card.yml; mkdir -p /tmp/rv && cat > /tmp/rv/probe.py <<'EOF'
import sys; sys.path.insert(0, "tests"); sys.path.insert(0, ".")
import test_autopilot_close as t, pathlib, tempfile
d = pathlib.Path(tempfile.mkdtemp())
m = t.Repo(d / "q", {57: [101, 102], 58: [201]}, {n: [t.LABEL] for n in (57, 101, 102)}, deps={102: [101]})
print(m.close(101)); print([(a[0], a[1]) for a in m.acted]); print(m.failures)
EOF
python /tmp/rv/probe.py 2>&1 | tail -5
```

> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, or a person opens or edits an issue. These triggers always use
> # the default branch's copy of this file and of dokima/card.py, so the work being
> # judged cannot change how it is reported.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [completed]
>   issues:
>     types: [opened, edited]
> concurrency:
>   group: card
>   cancel-in-progress: false
> permissions:
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> []
> []
> []

**Agent:** The new tests fail for the right reason, and none of today's jobs that run on a close would interfere with the queue test. Writing the review now.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner put 'two merges that close together' back into 213.5 and added two tests for it.",
   "One test requires every job that acts on a close to wait in one queue for the whole repo, which a newer run never cancels.",
   "The other test drops the queued runs of two closes, as GitHub does, and requires the next run to still do their work."
  ],
  "decided": [
   "Closes are handled one at a time through GitHub's own queue, and each run catches up on any close whose run was dropped."
  ],
  "open": [
   "A command said at the same moment a merge closes is not in that queue; the plan lists this as out of scope."
  ]
 },
 "verdict": "approve",
 "summary": "The plan now proves that two merges closing together start a waiting child only once, and all twelve new tests fail today because the feature is missing.",
 "blockers": [],
 "notes": [
  {
   "text": "The queue test checks only the jobs that changed something when #101 closed. A job that reads the tree outside the queue and passes its choice to a job inside the queue would still pass, though it could act on a stale reading.",
   "evidence": "tests/test_autopilot_close.py::test_closes_that_land_together_are_handled_one_at_a_time loops over m.acted only. Repo.close adds a job to m.acted only when _effects() changed."
  },
  {
   "text": "The owner's rule says a child is never started again by a close. The plan leaves `/autopilot start` and filing a split outside the queue, so a close at the same second as one of those commands could start the same child twice. The plan says so openly, and the window is a few seconds.",
   "evidence": "plan.json out_of_scope[2]."
  },
  {
   "text": "The planner's concern still holds: tests/test_cancelled_run.py (188.3) fails on main, so the full suite is red before any work starts here.",
   "evidence": "plan.json concerns[0]."
  }
 ],
 "outside_plan": [],
 "resolved": ["B1"],

```

> rc=0

**Agent:** I approved the plan for #213; the review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**My blocker from last round (B1) is fixed.** You wrote that two merges closing together must not start the same planner twice. Last round the plan only tested two closes one after the other. The planner put "together" back into criterion 213.5 and added two tests for it:
- **One queue for the whole repo:** every job that acts on a close must wait in one GitHub queue shared by the whole repo, which a newer run never cancels. So two closes are handled one at a time, never at once.
- **Dropped runs still count:** GitHub keeps only one run waiting in a queue and cancels it when a newer one arrives. The test drops the runs for two closes and requires the next run to still do their work. That means starting the waiting child once, closing the finished parent with one "tree done" comment, and taking finished issues off autopilot.

**Tests:** I ran `tests/test_autopilot_close.py` and `tests/test_autopilot.py`. All 12 new tests fail today, each because the feature is missing (no planner started, parent still open, labels still on). None fail on a crash or a setup problem. The 5 tests in `test_autopilot.py`, including the one the plan changes, pass. No workflow that runs on a close today trips the queue test.

I left three notes, none blocking:
- **Queue test gap:** the test only checks jobs that actually changed something. A build could read the tree outside the queue and act on it inside, and still pass, so it could act on an out-of-date reading.
- **Commands outside the queue:** `/autopilot start` and `/work` filing a split are not in the queue. A close in the same few seconds as one of those commands could start a child twice. The plan states this openly as out of scope.
- **Suite already red:** as the planner reported, `tests/test_cancelled_run.py` (criterion 188.3) already fails on main, so the full suite is red before any work starts here.

Every ask in the issue and your 07:13 comment ("every level", "test at least two levels") maps to a criterion. Closing #86 as a duplicate is still a step for you to take on GitHub.
