# reviewer (plan) for #285

Run: https://github.com/dokima-dev/dokima/actions/runs/37885605414

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #285: The audit runs once a day in the background, and on the Run workflow button
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 283 -->
> **Backlog**
> 
> [issue #285](https://github.com/dokima-dev/dokima/issues/285)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #283
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approve

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_audit_workflow.py; ls .github/workflows; grep -n "audit\|workflow" dokima/manifest.py | head -40
```

> commit d223955c0172d3384484c644d69d97c69d50ebbd
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:48:27 2026 +0000
> 
>     planner for #285 (run 37885355622)
> 
>  tests/test_audit_workflow.py | 263 +++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 263 insertions(+)
> """Tests for #285: one workflow runs the drift audit daily and on Run workflow.
> 
> The audit itself (`python3 -m dokima.audit OWNER/REPO`, #283) is proven in tests/test_audit.py and
> tests/test_audit_cli.py. These prove the workflow that runs it: `.github/workflows/audit.yml`, read with the repo's
> own YAML reader (tests/test_start.py's load_yaml, no YAML library). The workflow's own audit step is run the way GitHub
> would run it: its `${{ }}` filled in, its env set, its script run with `bash -e` against the fake `gh` of
> tests/fake_gh.py, from a folder holding .github/CODEOWNERS, with the dokima package on PYTHONPATH.
> """
> import copy
> import json
> import os
> import re
> import subprocess
> import sys
> 
> import pytest
> 
> HERE = os.path.dirname(os.path.abspath(__file__))
> ROOT = os.path.abspath(os.path.join(HERE, ".."))
> sys.path.insert(0, ROOT)
> sys.path.insert(0, HERE)
> import test_start as ts  # noqa: E402
> from dokima import agent, manifest  # noqa: E402
> 
> WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
> AUDIT = os.path.join(WORKFLOWS, "audit.yml")
> REPO = "acme/widgets"
> TOKEN = "fake-app-token"
> 
> 
> def workflow(criterion):
>     """The audit workflow, read; fails naming th

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_audit_workflow.py 2>&1 | tail -20; grep -rn "undeclared" tests/*.py | head -5; sed -n 1,30p dokima/manifest.py
```

> tests/test_audit_workflow.py:250: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> 
> criterion = '285.5'
> 
>     def workflow(criterion):
>         """The audit workflow, read; fails naming the criterion when it is missing."""
>         if not os.path.exists(AUDIT):
> >           pytest.fail(f"{criterion}: there is no .github/workflows/audit.yml to run the audit")
> E           Failed: 285.5: there is no .github/workflows/audit.yml to run the audit
> 
> tests/test_audit_workflow.py:34: Failed
> =========================== short test summary info ============================
> FAILED tests/test_audit_workflow.py::test_one_workflow_runs_the_audit_once_a_day - Failed: 285.1: there is no .github/workflows/audit.yml to run the audit
> FAILED tests/test_audit_workflow.py::test_the_audit_runs_on_a_schedule_or_the_run_workflow_button_and_nothing_else - Failed: 285.2: there is no .github/workflows/audit.yml to run the audit
> FAILED tests/test_audit_workflow.py::test_the_workflow_reports_a_missing_branch_rule_on_a_new_setup_issue - Failed: 285.3: there is no .github/workflows/audit.yml to run the audit
> FAILED tests/test_audit_workflow.py::test_the_workflow_posts_nothing_on_a_clean_repo - Failed: 285.3: there is no .github/workflows/audit.yml to run the audit
> FAILED tests/test_audit_workflow.py::test_audit_runs_wait_in_one_queue_for_the_repo - Failed: 285.4: there is no .github/workflows/audit.yml to run the audit
> FAILED tests/test_audit_workflow.py::test_the_audit_acts_as_the

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "from dokima import agent; print(agent.COMMANDS); print(agent.route('/audit', False, '5'))"; sed -n 1,80p .github/workflows/board.yml; grep -n "environment\|concurrency\|group" .github/workflows/*.yml; sed -n 1,40p dokima/audit.py; grep -n "argv\|def main" dokima/audit.py
```

> {'/plan': 'planner', '/work': 'worker', '/review': 'reviewer'}
> None
> name: board
> # Keeps the project board's Status and "Waiting on" current at every stage moment,
> # and its Priority in step with the blocker, high and parked labels.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [labeled, unlabeled, closed]
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   workflow_run:
>     workflows: [done-whens]
>     types: [completed]
> permissions:
>   contents: read
> concurrency:
>   group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
>   cancel-in-progress: false
> jobs:
>   sync:
>     environment: keys
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.repository.default_branch }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - id: app
>         uses: actions/create-github-app-token@v2
>         with:
>           app-id: ${{ vars.DOKIMA_APP_ID }}
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Sync the board
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }

`5. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && cat > .github/workflows/audit.yml <<'EOF'
name: audit
# Runs the drift audit once a day, and on the Run workflow button.
on:
  schedule:
    - cron: "17 6 * * *"
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: audit
  cancel-in-progress: false
jobs:
  audit:
    environment: keys
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - id: app
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.DOKIMA_APP_ID }}
          private-key: ${{ secrets.DOKIMA_APP_KEY }}
      - name: Audit the settings
        env:
          GH_TOKEN: ${{ steps.app.outputs.token }}
          DOKIMA_BOARD: ${{ vars.DOKIMA_BOARD }}
        run: python3 -m dokima.audit "${{ github.repository }}"
EOF
python -m pytest -q tests/test_audit_workflow.py 2>&1 | tail -15; python -m pytest -q -x 2>&1 | tail -5; python3 -m dokima.manifest .
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b876y3k22). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/1d5845c8-3335-4ba0-aac2-bb889e174022/tasks/b876y3k22.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** I'm checking the plan's tests against a sample workflow in a copy of the repo. The full suite is still running.

`6. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/1d5845c8-3335-4ba0-aac2-bb889e174022/tasks/b876y3k22.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/1d5845c8-3335-4ba0-aac2-bb889e174022/tasks/b876y3k22.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`7. Read`
```
/tmp/claude-1001/-home-runner-work-dokima-dokima/1d5845c8-3335-4ba0-aac2-bb889e174022/tasks/b876y3k22.output
```

> 1	......                                                                   [100%]
> 2	6 passed in 0.70s
> 3

`8. Bash`
```
cd /tmp/rv; cp .github/workflows/audit.yml /tmp/good.yml
t(){ python -m pytest -q tests/test_audit_workflow.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-200; cp /tmp/good.yml .github/workflows/audit.yml; echo ---; }
sed -i 's/  workflow_dispatch:/  workflow_dispatch:\n  issue_comment:\n    types: [created]/' .github/workflows/audit.yml; t
sed -i 's/17 6 \* \* \*/0 *\/6 * * */' .github/workflows/audit.yml; t
sed -i 's/cancel-in-progress: false/cancel-in-progress: true/' .github/workflows/audit.yml; t
sed -i 's/steps.app.outputs.token/github.token/' .github/workflows/audit.yml; t
sed -i 's/"\${{ github.repository }}"/acme\/other/' .github/workflows/audit.yml; t
sed -i 's/          DOKIMA_BOARD: \${{ vars.DOKIMA_BOARD }}//' .github/workflows/audit.yml; t
sed -i 's/group: audit/group: autopilot/' .github/workflows/audit.yml; t
sed -i 's/  workflow_dispatch:/  workflow_dispatch:\n    inputs:\n      x:\n        required: true/' .github/workflows/audit.yml; t
```

> FAILED tests/test_audit_workflow.py::test_the_audit_runs_on_a_schedule_or_the_run_workflow_button_and_nothing_else - AssertionError: 285.2: audit.yml should start only on schedule and workflow_dispatc
> 1 failed, 5 passed in 0.63s
> ---
> FAILED tests/test_audit_workflow.py::test_one_workflow_runs_the_audit_once_a_day - AssertionError: 285.1: the cron line '0 */6 * * *' does not fire exactly once every day
> 1 failed, 5 passed in 0.62s
> ---
> FAILED tests/test_audit_workflow.py::test_audit_runs_wait_in_one_queue_for_the_repo - AssertionError: 285.4: cancel-in-progress is 'true'; a second run must wait, not cancel
> 1 failed, 5 passed in 0.62s
> ---
> FAILED tests/test_audit_workflow.py::test_the_audit_acts_as_the_dokima_app - AssertionError: 285.5: the audit step's GH_TOKEN is '${{ github.token }}', not the app token of an earlier step
> 1 failed, 5 passed in 0.64s
> ---
> >       assert p.returncode == 0, f"285.3: the workflow's audit step failed ({p.returncode}):\n{p.stdout}\n{p.stderr}"
> E       AssertionError: 285.3: the workflow's audit step failed (1):
> >       assert p.returncode == 0, f"285.3: the workflow's audit step failed ({p.returncode}):\n{p.stdout}\n{p.stderr}"
> E       AssertionError: 285.3: the workflow's audit step failed (1):
> FAILED tests/test_audit_workflow.py::test_the_workflow_reports_a_missing_branch_rule_on_a_new_setup_issue - AssertionError: 285.3: the workflow's audit step failed (1):
> FAILED tests/test_audit_workflow.py::test_the_workflow_posts_nothing_on_a_clean_repo - Asser

`9. Bash`
```
cd /tmp/rv; timeout 110 python3 -m dokima.manifest . ; echo rc=$?; timeout 100 python -m pytest -q tests/test_manifest.py 2>&1 | tail -3
```

> Everything the code and workflows rely on is in the manifest.
> rc=0
> .............................................................            [100%]
> 61 passed in 4.88s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned one workflow, .github/workflows/audit.yml, that runs the drift audit once a day and on the Run workflow button.",
          "Wrote six tests that read the workflow and run its audit step against a fake GitHub, for a missing branch rule and for a clean repo."],
  "decided": ["Audit runs wait in one queue that no other workflow shares, and never cancel each other.",
              "The audit acts as the Dokima app with a token minted in its job, and reads the board from DOKIMA_BOARD."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers every part of story 4 of #280, and each test fails today only because audit.yml does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "I tried the tests against a sample audit.yml in a copy of the repo. A correct one passes all six. Each wrong version I tried turned a test red: an extra comment trigger, a cron every six hours, cancel-in-progress true, the workflow's own token, a wrong repo argument, no DOKIMA_BOARD, a group shared with autopilot.yml, and a required input on the button.",
   "evidence": "pytest -q tests/test_audit_workflow.py in /tmp/rv: 6 passed with the sample workflow, then 1 to 3 failed for each wrong version; python3 -m dokima.manifest . printed 'Everything the code and workflows rely on is in the manifest.'"},
  {"text": "The workflow's audit step runs from a checkout, but no test proves the job checks out the repo first. If the checkout step were missing, the module would not be found on GitHub. The tests would not catch that.",
   "evidence": "tests/test_audit_workflow.py::run_the_step sets PYTHONPATH=ROOT, so the dokima package is found without a checkout step"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "One workflow runs the audit once a day on a schedule.", "source": "https://github.com/dokima-dev/dokima/issues/285", "criterion": "285.1"},
  {"ask": "The same w
```

> rc=0

**Agent:** I approved the plan for #285. The review is in `/tmp/dokima-out/review.json`, and it passes both of Dokima's hand-back checks.

**What the plan covers:** one workflow, `.github/workflows/audit.yml`, that runs the drift audit once a day and on the Run workflow button. It has no other trigger. It runs the audit as the Dokima app and reads the board setting. Runs wait in one queue that no other workflow shares, and a second run never cancels the first. All four things the issue asks for are covered: the three acceptance criteria plus the requirement that runs never overlap.

**Today's tests:** all six new tests fail for the right reason, because `audit.yml` doesn't exist yet. None fails from a crash or a bad path.

**Would they catch a wrong workflow?** I wrote a sample `audit.yml` in a scratch copy of the repo; the real repo is unchanged.
- **Correct version:** a correct workflow passes all six tests.
- **Repo settings:** Dokima's settings list still covers everything the workflows rely on, so the planned change to it may not be needed.
- **Wrong versions:** each wrong version I tried turned a test red:
  - an extra comment trigger
  - a cron that fires every six hours
  - a second run that cancels the first
  - the workflow's own token instead of the app's
  - the wrong repo passed to the audit
  - no board setting
  - a queue shared with `autopilot.yml`
  - a required input on the Run workflow button

**One gap, left as a note rather than a blocker:** no test proves the workflow checks out the repo before running the audit. The tests point Python at the repo directly. So a workflow missing that step would pass the tests and then fail on GitHub.

`11. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/1d5845c8-3335-4ba0-aac2-bb889e174022/tasks/b876y3k22.output
```

> ......                                                                   [100%]
> 6 passed in 0.70s
> ........................................................................ [ 77%]
> ........................................................................ [ 87%]
> ........................................................................ [ 97%]
> .....................                                                    [100%]
> 741 passed in 384.51s (0:06:24)
> Everything the code and workflows rely on is in the manifest.
> 
> [exited with code 0]

**Agent:** The full test suite has now finished in the scratch copy, with my sample workflow in place: all 741 tests pass. So adding a correct `audit.yml` breaks nothing else in the repo. Dokima's settings list also still covers everything the workflows need. That supports the approval, and the review file stays as it is.
