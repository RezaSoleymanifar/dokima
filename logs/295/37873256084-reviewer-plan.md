# reviewer (plan) for #295

Run: https://github.com/dokima-dev/dokima/actions/runs/37873256084

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #295: The plan check re-runs when a plan is approved, so it never shows a stale failure
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #295](https://github.com/dokima-dev/dokima/issues/295)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The "all done-whens passed" check runs only when a pull request gets a new commit. When a plan is re-approved and the worker has nothing new to push, no commit lands, so the check keeps the failure it got before the approval ("No approved plan found"). That stalled #290, #287, #274, #255 and #288 tonight until they were re-run by hand.
> 
> What I want:
> - When a plan is approved, the pull request's

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_plan_check_rerun.py; ls .github/workflows; cat dokima/app.json
```

> commit fd4037ad86d36553c34fef2891a2f900bcdb1733
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:09:41 2026 +0000
> 
>     planner for #295 (run 37872677209)
> 
>  tests/test_plan_check_rerun.py | 327 +++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 327 insertions(+)
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
> {id, name, path, event, head_sha, head_branch, status, conclusion, run_attempt, matrix, reruns}. It ans

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_plan_check_rerun.py -x -q 2>&1 | tail -40; grep -n "started\b\|^token\|calls-meta\|def comments_on\|def flag\|^opts\|token =" tests/test_start.py | head -30
```

> "matrix": [
>      {
>       "id": "none",
>       "name": "No approved plan found for issue #57",
>       "tests": ""
>      }
>     ],
>     "reruns": []
>    },
>    "7002": {
>     "id": 7002,
>     "name": "full-suite",
>     "path": ".github/workflows/full-suite.yml",
>     "event": "pull_request_target",
>     "head_sha": "69759178140593647bbcd3833c796fff76e01997",
>     "head_branch": "try/issue-57",
>     "status": "completed",
>     "conclusion": "failure",
>     "run_attempt": 1,
>     "matrix": [
>      {
>       "id": "none",
>       "name": "No approved plan found for issue #57",
>       "tests": ""
>      }
>     ],
>     "reruns": []
>    }
>   }
>   ## run: Decide what follows, merge on autopilot, and say it on the card (exit 0)
>   stop
>   
>   ## run: Post the record as a comment, on the PR once there is one (exit 0)
>   on_ms\": 1000,\n  \"turns\": 1,\n  \"cost_usd\": null,\n  \"tokens_in\": 0,\n  \"tokens_out\": null\n },\n \"log\": \"https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md\",\n \"run\": \"https://github.com/o/r/actions/runs/42\",\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"approve\",\n  \"summary\": \"The split keeps every promise once.\",\n  \"blockers\": [],\n  \"notes\": [],\n  \"outside_plan\": [],\n  \"resolved\": [],\n  \"asks\": [\n   {\n    \"ask\": \"Fix it.\",\n    \"source\": \"https://github.com/o/r/issues/57\",\n    \"cr

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_plan_check_rerun.py 2>&1 | grep -E "^E +(Assertion|assert)|AssertionError: 29|passed|failed" | head -20
```

> Proves 295.1. The plan check on the pull request's head failed with "No approved plan found" after the re-plan. The plan reviewer
>         assert not m.failed, f"295.1: the plan review's run failed at '{m.failed_step}'{why(m)}"
> E       AssertionError: 295.1: the plan check on the head ce5f036 was not run again after the approval
> E         on_ms\": 1000,\n  \"turns\": 1,\n  \"cost_usd\": null,\n  \"tokens_in\": 0,\n  \"tokens_out\": null\n },\n \"log\": \"https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md\",\n \"run\": \"https://github.com/o/r/actions/runs/42\",\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"approve\",\n  \"summary\": \"The split keeps every promise once.\",\n  \"blockers\": [],\n  \"notes\": [],\n  \"outside_plan\": [],\n  \"resolved\": [],\n  \"asks\": [\n   {\n    \"ask\": \"Fix it.\",\n    \"source\": \"https://github.com/o/r/issues/57\",\n    \"criterion\": \"57.1\"\n   }\n  ]\n },\n \"check\": {\n  \"passed\": true,\n  \"problems\": []\n }\n}\n```\n\n</details>\n\n<sub><img src=\"https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg\" width=\"16\" height=\"16\" align=\"absmiddle\" alt=\"stats\"> Opus 5.5 \u00b7 0.0 min \u00b7 1 turns \u00b7 [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md) \u00b7 [run](https://github.com/o/r/actions/runs/42)</sub

`5. Bash`
```
cd /home/runner/work/dokima/dokima; head -30 .github/workflows/done-whens.yml; grep -n "def matrix\|\"matrix\"\|'matrix'" dokima/checks.py | head; grep -n "permissions" -A6 .github/workflows/agent.yml | head -20
```

> name: done-whens
> # One GitHub check per criterion of the PR's approved plan, plus one gate check.
> # Runs main's copy of this workflow and of Dokima's code; only the tests, and the code they judge, come from the PR.
> on:
>   pull_request_target:
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
> jobs:
>   list:
>     name: list done-whens
>     runs-on: ubuntu-24.04
>     outputs:
>       matrix: ${{ steps.m.outputs.matrix }}
>     steps:
>       - uses: actions/checkout@v5
>       - id: m
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
> 
>   check:
>     needs: list
>     if: needs.list.outputs.matrix != '[]'
>     name: ${{ matrix.name }}
>     strategy:
>       fail-fast: false
>       matrix:
>         include: ${{ fromJSON(needs.list.outputs.matrix) }}
> 84:    if argv[1] == "matrix":
> 40:permissions:
> 41-  contents: read
> 42-  issues: read
> 43-  pull-requests: read
> 44-  actions: read
> 45-jobs:
> 46-  run:
> --
> 240:            --model "$MODEL" --dangerously-skip-permissions --max-turns 60 --output-format json > "$OUT/claude.json"
> 241-      # The card says checking, with a key made for this one edit and revoked before code checks the hand-back.
> 242-      - id: checking-key
> 243-        if: always() && !cancelled() && env.STARTED == 'true' && env.CARD_ID != ''
> 244-        continue-on-error: true
> 245-        uses: actions/create-github-app-token@v2
> 246-        with:

**Agent:** The four new tests all fail today for the right reason, since nothing reruns the check yet. Now I'm writing the review.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned two acceptance criteria and two non-functional requirements for rerunning the pull request's plan check once a plan is approved, with one test each in tests/test_plan_check_rerun.py."],
  "decided": ["The rerun happens in a new step of agent.yml after the plan review's record is posted, using Dokima's app key with write access to Actions added to dokima/app.json.",
              "When the check cannot rerun (GitHub refuses, or it is still running), the pull request gets one comment saying so, with the head's short id and why."],
  "open": ["Asks the owner whether this issue may change agent.yml and dokima/app.json; it assumed yes."]},
 "verdict": "approve",
 "summary": "The plan covers both of the owner's asks, and each of its four tests runs the whole agent workflow against a fake GitHub and fails today because nothing reruns the plan check yet.",
 "blockers": [],
 "notes": [
  {"text": "When the plan check from the planner's push is still running at approval, the plan only comments on the pull request instead of rerunning once the check finishes. That check may still end with the stale failure, and someone would have to rerun it by hand. The plan review usually takes minutes and the check's list job takes seconds, so this case should be rare.",
   "evidence": "tests/test_plan_check_rerun.py::test_a_plan_check_that_cannot_run_again_says_why_on_the_pull_request, the 'running' case expects one comment and no rerun."},
  {"text": "The fake GitHub reruns the check by running Dokima's real `python3 -m dokima.checks matrix` against the issue's records as they are at that moment. So 295.1 passes only when the whole check reruns, after the approval is posted, on the current head. Rerunning only failed jobs, rerunning too early or rerunning another commit's run each turns it red.",
   "evidence": "Ran pytest -q tests/test_plan_check_rerun.py on try/issue-295: 4 failed,
```

> Exit code 1
> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";r=json.load(open(p))
r["summary"]="The plan covers both of the owner's asks, and all four of its tests fail today because nothing reruns the plan check yet."
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 295 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #295 with no blockers, but on autopilot it will still stop for you because I didn't accept the planner's one assumption.

**Why it passes:** both things you asked for are in criterion 1:
- When a plan is approved, the pull request's plan check runs again on its current head.
- A test proves a re-approved plan with no new commit ends with a passing plan check.

I ran the four new tests and all four fail for the right reason: nothing reruns the check yet. They aren't shallow. Each one runs the whole agent workflow against a fake GitHub, and the fake builds the check from your issue's history at the moment it's rerun. So the main test turns red if the check reruns only its failed parts, reruns before the approval is posted, or reruns on another commit or workflow.

**Not accepted:** the planner asked whether this issue may change `.github/workflows/agent.yml` and `dokima/app.json`, and assumed yes. Saying yes changes a workflow and gives Dokima's app write access to Actions, which you'd have to accept once on GitHub. Your issue doesn't ask for either change, and AGENTS.md forbids workflow changes unless the issue explicitly asks. That's your call, not something to assume.

**One weak spot (a note, not a blocker):** sometimes the check from the planner's push is still running when the plan is approved. The plan then only comments on the pull request saying it couldn't rerun, rather than rerunning once that check finishes. That check may still end with the old "No approved plan found" failure, and someone would rerun it by hand. It should be rare, since a plan review takes minutes and that check's first job takes seconds.

The hand-back is in `/tmp/dokima-out/review.json` and passes both required checks.
