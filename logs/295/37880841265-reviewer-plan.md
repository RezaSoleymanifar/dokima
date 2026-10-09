# reviewer (plan) for #295

Run: https://github.com/dokima-dev/dokima/actions/runs/37880841265

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (31.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a36fee24-2d88-4265-81fa-741d91442adc/tool-results/bku2or8sd.txt
> 
> Preview (first 2KB):
> .:
> total 52
> drwxr-xr-x  3 runner runner  4096 Oct  9 03:47 .
> drwxrwxrwt 18 root   root    4096 Oct  9 03:47 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 03:47 in
> -rw-r--r--  1 runner runner 31662 Oct  9 03:47 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 03:47 open_blockers.json
> -rw-r--r--  1 runner runner  2812 Oct  9 03:47 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner 4096 Oct  9 03:47 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 03:47 ..
> -rw-r--r-- 1 runner runner 3973 Oct  9 03:47 01-planner.json
> -rw-r--r-- 1 runner runner 3996 Oct  9 03:47 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3435 Oct  9 03:47 03-planner.json
> # Issue #295: The plan check re-runs when a plan is approved, so it never shows a stale failure
> 
> <!-- dokima-card -->
> An approved plan reruns the pull request's plan check on the same commit, so it never keeps a stale "No approved plan found".
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #295](https://github.com/dokima-dev/dokima/issues/295)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-card-end\|<!-- dokima-ask/,$p' issue.md | head -50; echo ----; grep -n "^## \|^### \|Comment\|@" issue.md | head -60
```

> <!-- dokima-ask -->
> 
> The "all done-whens passed" check runs only when a pull request gets a new commit. When a plan is re-approved and the worker has nothing new to push, no commit lands, so the check keeps the failure it got before the approval ("No approved plan found"). That stalled #290, #287, #274, #255 and #288 tonight until they were re-run by hand.
> 
> What I want:
> - When a plan is approved, the pull request's plan check runs again on its current head.
> - A test proves a re-approved plan with no new commit ends with a passing plan check.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #295 (2026-10-09T02:02:18Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #295 (2026-10-09T02:02:41Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #295 (2026-10-09T02:02:43Z)
> 
> Autopilot is on for #295. Planning started for #295, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #295 (2026-10-09T02:02:54Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue and asks you 1 question.
> 
> **User story:** Once a plan is approved, the pull request's "all done-whens passed" check shows the verdict on that approved plan, without the owner re-running it by hand.
> 
> <img src="https://r

`3. Bash`
```
cd /tmp/pack; sed -n 228,360p issue.md; sed -n 500,700p issue.md
```

> ### dokima-runtime on issue #295 (2026-10-09T02:09:52Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer passed the plan.
> 
> **The plan's assumptions:**
> - This needs a new step in .github/workflows/agent.yml after the record is posted (the river decides what follows before the approval is on GitHub, so a rerun from there would read the old records) and write access to Actions for Dokima's app, which you accept once on GitHub. AGENTS.md says workflows change only when an issue asks: may this one change agent.yml and dokima/app.json? Not accepted: Saying yes changes a workflow and gives Dokima's app new write access to Actions, which the owner must accept on GitHub. That changes how the system works and what the bot may do. The owner's issue never mentions changing a workflow or the app's access, and AGENTS.md forbids workflow changes unless the issue explicitly asks, so the owner has to decide this.
> 
> <details><summary><b>Details</b></summary>
> 
> - The plan covers both of the owner's asks, and all four of its tests fail today because nothing reruns the plan check yet.
> 
> </details>
> 
> <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/note.svg" width

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1));print(json.dumps(d.get('handback'),indent=1)[:3000])"; cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40
```

> {
>  "kind": "user_story",
>  "summary": "An approved plan reruns the pull request's plan check on the same commit, so it never keeps a stale \"No approved plan found\".",
>  "user_story": "Once a plan is approved, the pull request's \"all done-whens passed\" check shows the verdict on that approved plan, without the owner re-running it by hand.",
>  "acceptance_criteria": [
>   {
>    "text": "When a plan is approved and its open pull request has no new commit, the plan check on that head reruns and passes. It reruns in full, only after the approval is posted, and leaves runs on older commits and other workflows alone.",
>    "source": "https://github.com/dokima-dev/dokima/issues/295"
>   },
>   {
>    "text": "Only an approval reruns the check. A plan review that blocks reruns nothing, and an approval with no open pull request reruns nothing and still posts its record.",
>    "source": "https://github.com/dokima-dev/dokima/issues/295"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "When the plan check cannot rerun, the pull request gets one comment from Dokima saying so, with the head's short id and why. That covers GitHub refusing and a check still running; the plan review's record is still posted.",
>    "why": "A stale red check with no explanation is exactly what stalled five pull requests.",
>    "principle": "Fail closed: a failure always says why."
>   },
>   {
>    "text": "The rerun uses Dokima's app key, minted after the agent finished. dokima/app.json asks GitHub for write access to Actions, which

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_plan_check_rerun.py; python -m pytest -q tests/test_plan_check_rerun.py 2>&1 | tail -15
```

> """An approved plan runs the pull request's plan check again on its current head (#295).
> 
> The plan check is the done-whens workflow (.github/workflows/done-whens.yml): its `list` job reads the issue's records
> and builds one check per criterion of the approved plan, and its gate, "all done-whens passed", fails with "No approved
> plan found" while the newest plan has no approving review. It runs only when the pull request gets a new commit, so a
> plan re-approved with nothing new to push kept its stale failure.
> 
> These tests run the whole agent workflow (agent.yml) for the plan reviewer on issue #57, whose pull request #60 is
> open on try/issue-57, on the machine of test_start.py: every step's `if:` is evaluated and its script runs with bash
> against a fake `gh`. The fake Claude Code hands back the review the test chose. Nothing is pushed by a plan review, so
> the pull request's head stays the commit the test made: a re-approval with no new commit.
> 
> The fake GitHub of test_start.py is taught pull request #60 and GitHub Actions runs. Runs live in runs.json, each
> {id, name, path, event, head_sha, head_branch, status, conclusion, run_attempt, matrix, reruns}. It answers:
>   - `gh pr view 60|try/issue-57 --json ...` (number, headRefName, headRefOid, body, state, url, comments, reviews) and
>     `gh api repos/o/r/pulls/60` (number, state, body, head.sha, head.ref), with -q/--jq a plain `.field` or `.head.sha`;
>   - the runs: `gh api repos/o/r/actions/runs` and `repos/o/r/actions/workflows/do

**Agent:** Checking the plan for #295: tests fail today as expected; confirming each fails for the right reason, then writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_plan_check_rerun.py 2>&1 | grep -E "^E +(AssertionError: )?29|^FAILED|AssertionError: 295" | cut -c1-200
```

> E       AssertionError: 295.1: the plan check on the head 4fc342d was not run again after the approval
> E       AssertionError: 295.2: an approval with the pull request open did not end with a passing plan check
> E           AssertionError: 295.3 (GitHub refused): expected one comment on PR #60 saying the plan check could not run again, got []
> E       AssertionError: 295.4: the plan check was not run again
> FAILED tests/test_plan_check_rerun.py::test_a_reapproved_plan_with_no_new_commit_ends_with_a_passing_plan_check - AssertionError: 295.1: the plan check on the head 4fc342d was not run again after the 
> FAILED tests/test_plan_check_rerun.py::test_only_an_approval_with_an_open_pull_request_runs_the_plan_check_again - AssertionError: 295.2: an approval with the pull request open did not end with a pass
> FAILED tests/test_plan_check_rerun.py::test_a_plan_check_that_cannot_run_again_says_why_on_the_pull_request - AssertionError: 295.3 (GitHub refused): expected one comment on PR #60 saying the plan che
> FAILED tests/test_plan_check_rerun.py::test_the_plan_check_runs_again_only_with_the_apps_key_after_the_agent_finished - AssertionError: 295.4: the plan check was not run again

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned after the owner's answer: the same two acceptance criteria, two non-functional requirements and four tests, with the question about agent.yml and dokima/app.json removed."],
  "decided": ["The rerun happens in a new step of agent.yml after the plan review's record is posted, using Dokima's app key, with write access to Actions added to dokima/app.json.",
              "When the check cannot rerun (GitHub refuses, or it is still running), the pull request gets one comment saying so, with the head's short id and why."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now does what the owner allowed (changing agent.yml and dokima/app.json and giving the app write access to Actions), covers both asks, and all four tests fail today because nothing reruns the plan check yet.",
 "blockers": [],
 "notes": [
  {"text": "When the plan check from the planner's push is still running at approval, the plan only comments on the pull request instead of rerunning once the check finishes, so that check may still end with the stale failure and need a manual rerun. This should be rare, since the plan review takes minutes and the check's list job takes seconds.",
   "evidence": "tests/test_plan_check_rerun.py::test_a_plan_check_that_cannot_run_again_says_why_on_the_pull_request, the 'running' case expects one comment and no rerun."},
  {"text": "The fake GitHub reruns the check by running Dokima's real `python3 -m dokima.checks matrix` against the issue's records at that moment, so 295.1 passes only on a full rerun, after the approval is posted, on the current head; rerunning only failed jobs, too early, or another commit's run each turns it red.",
   "evidence": "Ran pytest -q tests/test_plan_check_rerun.py on try/issue-295: 4 failed, each with its criterion's message ('295.1: the plan check on the head 4fc342d was not run again after the approval', '295.2: an appro
```

> Exit code 1
> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan uses the owner's permission to change agent.yml and app.json, covers both asks, and its four tests fail today as they should."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 295 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #295 and wrote the review to `/tmp/dokima-out/review.json`. Both required checks on the hand-back pass.

- **What changed since the last round:** The planner re-planned after your `/plan` answer. The plan is the same as before (two acceptance criteria, two non-functional requirements and four tests), minus the question about changing `agent.yml` and `dokima/app.json`. That question is now covered by your own permission.
- **Your asks:** All three are covered by a criterion:
  - Rerunning the plan check on the current head maps to 295.1.
  - The test that a re-approved plan with no new commit ends with a passing check also maps to 295.1.
  - Your permission to give the app write access to Actions maps to 295.4.
- **Tests:** I ran `pytest -q tests/test_plan_check_rerun.py` on `try/issue-295`. All 4 tests fail for the right reason: nothing reruns the plan check yet, and each failure names its criterion. None fail on a crash or a setup problem.
- **Open blockers:** There were none to carry over, and I found no new ones.
- **Two notes, not blockers:**
  - If the plan check from the planner's push is still running when the plan is approved, the plan only comments on the pull request; it doesn't wait and rerun. That check could still end with the stale failure and need a manual rerun. This should be rare, because the plan review takes minutes and the check's list job takes seconds.
  - The fake GitHub reruns the check with Dokima's real check code against the issue's records at that moment. So 295.1 only passes on a full rerun of the head's check, after the approval is posted. Rerunning only the failed jobs, rerunning too early, or rerunning another commit's run each fails it.

The plan changes a workflow file, so on autopilot the pull request will still stop for you to merge. You'll also need to accept the app's new Actions permission once on GitHub.
