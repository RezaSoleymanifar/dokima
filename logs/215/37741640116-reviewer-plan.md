# reviewer (plan) for #215

Run: https://github.com/dokima-dev/dokima/actions/runs/37741640116

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

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
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> - [ ] Goal: main's full suite is green again
>   - [ ] Done when: tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure passes on main, with its fake plan review's asks matched to a criterion the fake plan actually has
>     Verified by: the full suite on main passes
> 
> Filed by the overnight watch, 2026-10-08.
> 
> <details><summary><b>Context</b></summary>
> 
> Main has been red since 06:54 UTC (runs 37740214354, 37740586001): 1 failed, 338 passed. #188 (PR #208) and #158 (PR #198) each passed alone; together, #158's asks check rejects the fake plan review in #188's test because it matches the ask to

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_cancelled_run_fakes.py; grep -n "BLOCK\|asks\|S1.1\|57.1" tests/test_cancelled_run.py | head -40; python -m pytest -q tests/test_cancelled_run.py tests/test_cancelled_run_fakes.py 2>&1 | tail -30
```

> commit fdac0dd816e166c8d85d9df26be85745c3f69f6f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:08:28 2026 +0000
> 
>     planner for #215 (run 37741108425)
> 
>  tests/test_cancelled_run_fakes.py | 56 +++++++++++++++++++++++++++++++++++++++
>  1 file changed, 56 insertions(+)
> """The fake plan review the cancelled-run tests feed is one code's check accepts, so they test what they say (#215).
> 
> tests/test_cancelled_run.py feeds a blocking plan review (BLOCK) to runs on a one-story plan for issue 57, whose only
> criterion is 57.1. BLOCK was built from test_start.APPROVE, whose ask names S1.1, a criterion only a split has; once
> #158's asks check landed, code rejected that hand-back, so the "blocked" run no longer sent the plan back to the
> planner and main went red. These tests run the real check the workflow runs on a plan review
> (`python3 -m dokima.agent check review FILE PLAN N`, with STAGE=plan) against the fake plan those runs use.
> """
> import json
> import os
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> sys.path.insert(0, os.path.dirname(__file__))
> 
> import test_cancelled_run as tcr  # noqa: E402
> from test_start import N, STORY  # noqa: E402
> 
> from dokima import agent  # noqa: E402
> 
> 
> def check_review(tmp_path, review, name):
>     """Run code's plan-review check on a review against the cancelled-run tests' fake plan; (exit code, output)."""
>     path, plan = tmp_path / f"{name}.json

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q -x -p no:cacheprovider 2>&1 | tail -5; python -m pytest -q 2>&1 | tail -4; grep -n "which is not a criterion of the plan" dokima/agent.py; sed -n 1,40p tests/test_cancelled_run.py; grep -n "^APPROVE\|^STORY\b\|^STORY =" -A12 tests/test_start.py | head -50
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bbpwv39t3). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "which is not a criterion of the plan" dokima/agent.py; sed -n 1,40p tests/test_cancelled_run.py; grep -n "^APPROVE\|^STORY =" -A12 tests/test_start.py | head -50
```

> 533:            bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
> 653:            bad.append(f"blocker {b.get('id')} names {c}, which is not a criterion of the plan ({', '.join(ids) or 'none'})")
> """A cancelled run says so quietly, the owner is mentioned on a real rejection, and nothing restarts by itself (#188).
> 
> These tests run the agent workflow (.github/workflows/agent.yml) the way GitHub runs it, with the machine from
> test_start.py, and cancel some runs part way, the way the Cancel button on the Actions page does: at the code-owner
> gate (before the run's card is up), while the tools install (card up, no agent yet), while the agent works, and after
> the agent's hand-back passed code's check. Other runs are not cancelled and end the usual ways: a hand-back code
> rejects, a step that fails before the agent, and a blocking plan review that the river sends back to the planner.
> Each scenario runs once per module and the tests read what it left on the fake GitHub: its comments, and every call
> that could start a run.
> """
> import os
> import re
> 
> import pytest
> 
> import test_start as ts
> from test_start import APPROVE, N, OWNER, PIP_BROKEN, PR, STORY_APPROVED, STORY_PLANNED, Run, owner_comment
> 
> from dokima import agent
> 
> LIVE = "<!-- dokima-live -->"
> MENTION = re.compile(r"(?<![\w/@.`])@[A-Za-z0-9][A-Za-z0-9-]*")
> ICON = re.compile(r"/dokima/icons/([A-Za-z0-9_-]+)\.svg")
> BAD_REVIEW = {"verdict": "maybe"}
> BLOCK = dict(APPROVE, verdict="block", summ

`5. Bash`
```
sleep 100; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output
```

> <tool_use_error>Blocked: sleep 100 followed by: tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** I'm waiting for the full test suite to finish. Meanwhile I'll write the review: the plan checks out, and both new tests fail today for the right reason.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan with two criteria: the cancelled-run test passes again, and its fake blocking plan review matches its asks to 57.1, the fake plan's only criterion.",
          "Added tests/test_cancelled_run_fakes.py, which runs code's real plan-review check on the fake review."],
  "decided": ["The fix goes in the fake review in tests/test_cancelled_run.py; code's asks check in dokima/agent.py stays exactly as it is."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan fixes main by correcting the fake plan review rather than loosening the check, and both tests fail today for the right reason.",
 "blockers": [],
 "notes": [{"text": "215.2 also checks that code still rejects an ask matched to S1.1 on the one-story plan. If the worker made main green by loosening the asks check, this test would turn red.",
            "evidence": "tests/test_cancelled_run_fakes.py:54-56; dokima/agent.py:533 holds the message it expects"}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "main's full suite is green again", "source": "https://github.com/dokima-dev/dokima/issues/215", "criterion": "215.1"},
  {"ask": "tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure passes on main", "source": "https://github.com/dokima-dev/dokima/issues/215", "criterion": "215.1"},
  {"ask": "with its fake plan review's asks matched to a criterion the fake plan actually has", "source": "https://github.com/dokima-dev/dokima/issues/215", "criterion": "215.2"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 215 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

`7. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`8. Bash`
```
until grep -qE "passed|failed|error" /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output 2>/dev/null; do sleep 5; done; tail -8 /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output
```

> Command running in background with ID: bi4tbvb9h. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bi4tbvb9h.output. You will be notified when it completes. To check interim output, use Read on that file path.

**Agent:** I'll wait for the full suite to confirm the cancelled-run test is the only test failing on the branch.

`9. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bi4tbvb9h.output | grep -E "FAILED|passed|failed" 
```

> 1 failed, 68 passed in 16.10s

`10. Bash`
```
grep -E "FAILED|passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/f48aaecc-83a9-423e-b51d-fda2cbf78fd1/tasks/bbpwv39t3.output | cut -c1-200
```

> 1 failed, 68 passed in 16.10s
> 5 failed, 335 passed in 121.59s (0:02:01)
> the agent's hand-back passed code's check. Other runs are not cancelled and end the usual ways: a hand-back code

**Agent:** The full suite shows 5 failures, not the 2 I expected. I'm checking which tests they are.

`11. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 500 python -m pytest -q -rf 2>&1 | grep -E "^FAILED|passed" | cut -c1-250
```

> Every cancelled run (including one cancelled after its blocking review had passed code's check, which the river
> E         ,\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"block\",\n  \"summary\": \"
> FAILED tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure - AssertionError: 188.3: a blocking plan review that nobody cancelled no longer starts the planner: []
>   ,\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"block\",\n  \"summary\": \"57.1 has
> FAILED tests/test_cancelled_run_fakes.py::test_the_fake_blocking_review_matches_its_asks_to_the_fake_plan - AssertionError: 215.2: the fake blocking review matches asks to criteria the fake plan does not have (it has ['57.1']): [{'ask': 'Fix it.', 's
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner'
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list ev

**Agent:** Three more tests fail here that the issue doesn't mention. I'm checking whether something in my environment is causing them.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; env | grep -iE "^STAGE|DOKIMA|ROLE" ; env -u STAGE python -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -2
```

> GITHUB_WORKSPACE=/home/runner/work/dokima/dokima
> LOG_URL=https://github.com/dokima-dev/dokima/blob/logs/logs/215/37741640116-reviewer-plan.md
> GITHUB_TRIGGERING_ACTOR=dokima-runtime[bot]
> PWD=/home/runner/work/dokima/dokima
> STAGE=plan
> GITHUB_WORKFLOW_REF=dokima-dev/dokima/.github/workflows/agent.yml@refs/heads/main
> GITHUB_ACTOR=dokima-runtime[bot]
> ROLE=reviewer
> GITHUB_REPOSITORY=dokima-dev/dokima
> RUNNER_WORKSPACE=/home/runner/work/dokima
> GITHUB_REPOSITORY_OWNER=dokima-dev
> OUT=/tmp/dokima-out
> OLDPWD=/home/runner/work/dokima/dokima
> ..............                                                           [100%]
> 14 passed in 4.10s

**Agent:** Those three failures come from my sandbox: it sets `STAGE=plan`, and the tests pick it up. With `STAGE` unset they all pass. I'll add that to the review as a separate issue and rerun the check.

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";r=json.load(open(p))
r["issues_found"]=[{"title":"Some tests change result when the STAGE environment variable is set","why":"Inside an agent run, where STAGE=plan is set, the full suite shows three extra failures that do not happen on main's CI. So an agent checking the suite sees red that isn't real.","evidence":"With STAGE=plan: tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner and two tests in tests/test_handback_check.py fail with 'asks must list every ask'. With `env -u STAGE pytest -q tests/test_fixer.py tests/test_handback_check.py`: 14 passed."}]
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 215 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #215. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

The fix goes in the right place. The cancelled-run test's fake plan review matches its ask to S1.1, a criterion only a split plan has. The plan corrects that fake review to use 57.1, the fake plan's only criterion. Code's asks check in `dokima/agent.py` stays as it is.

- **Tests fail today for the right reason.**
  - `tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure` (215.1) still fails: code rejects the fake review's ask "matched to S1.1".
  - The planner's new test `tests/test_cancelled_run_fakes.py::test_the_fake_blocking_review_matches_its_asks_to_the_fake_plan` (215.2) fails because the fake review still names S1.1.
- **The check can't be loosened to make main green.** Test 215.2 also confirms that code still rejects an ask matched to S1.1 on a one-story plan. If the worker made main green by loosening the check, that test would turn red.
- **Every ask is covered.** I listed the three asks in the issue. "Main's full suite is green again" and "the test passes on main" map to 215.1; "the fake review's asks matched to a criterion the fake plan has" maps to 215.2. None is missing.

**Separate problem:** in my sandbox the full suite showed 5 failures, not 2. The other three (one in `tests/test_fixer.py`, two in `tests/test_handback_check.py`) fail only because the agent machine sets `STAGE=plan` and those tests pick it up. With `STAGE` unset they all pass (14 passed). Their failures fit the issue's main count (1 failed, 338 passed), so they aren't red on main. But any agent running the suite will see failures that aren't real, so I proposed it as its own issue in the review.
