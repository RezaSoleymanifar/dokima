# reviewer (plan) for #417

Run: https://github.com/dokima-dev/dokima/actions/runs/38080811936

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (37.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b245e24f-3936-4ec2-ad0f-0100160da73d/tool-results/b1jvqwtut.txt
> 
> Preview (first 2KB):
> total 40
> drwxr-xr-x 2 runner runner 4096 Oct 10 19:42 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 19:42 ..
> -rw-r--r-- 1 runner runner 3461 Oct 10 19:42 01-planner.json
> -rw-r--r-- 1 runner runner 3990 Oct 10 19:42 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4554 Oct 10 19:42 03-planner.json
> -rw-r--r-- 1 runner runner 2069 Oct 10 19:42 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2341 Oct 10 19:42 05-worker.json
> -rw-r--r-- 1 runner runner 3557 Oct 10 19:42 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 1964 Oct 10 19:42 07-worker.json
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
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/

`2. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b245e24f-3936-4ec2-ad0f-0100160da73d/tool-results/b1jvqwtut.txt | sed -n 20,400p
```

> <persisted-output>
> Output too large (32.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b245e24f-3936-4ec2-ad0f-0100160da73d/tool-results/bejz5adgs.txt
> 
> Preview (first 2KB):
> https://github.com/dokima-dev/dokima/issues/417 · https://github.com/dokima-dev/dokima/pull/447 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/447/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #429, #368, #380, #425
> 
> **User story:** On autopilot no step is lost silently: when deciding what runs next fails, the record says why, and when GitHub's rate limit ran out the step waits for it to reset and starts what it would have started.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **<a href="https://github.com/dokima-dev/dokima/actions/runs/38079411100/job/114293094586">Acceptance criterion</a>:** When GitHub refuses a call while deciding what runs next, the record says so i

**Agent:** Let me read the files in pieces with the Read tool.

`3. Read`
```
/tmp/pack/issue.md
```

> 1	# Issue #417: Autopilot sometimes never starts the next step, and says nothing
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-linked-from: 368, 425 -->
> 5	<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> 6	When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.
> 7	
> 8	**Review**
> 9	
> 10	https://github.com/dokima-dev/dokima/issues/417 · https://github.com/dokima-dev/dokima/pull/447 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/447/files)
> 11	
> 12	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #429, #368, #380, #425
> 13	
> 14	**User story:** On autopilot no step is lost silently: when deciding what runs next fails, the record says why, and when GitHub's rate limit ran out the step waits for it to reset and starts what it would have started.
> 15	
> 16	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 17	
> 18	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **<a href="https://github

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; ls; cat in/04-reviewer-plan.json | head -50; cd /home/runner/work/dokima/dokima; git log --oneline -8; git diff main --stat
```

> {
>  "kind": "user_story",
>  "summary": "When deciding what runs next fails, the record says GitHub's reason; a rate limit is waited out, then the step goes on.",
>  "user_story": "On autopilot no step is lost silently: when deciding what runs next fails, the record says why, and when GitHub's rate limit ran out the step waits for it to reset and starts what it would have started.",
>  "acceptance_criteria": [
>   {
>    "text": "When GitHub refuses a call while deciding what runs next, the record says so in one line with GitHub's reason. No stage starts, and runs GitHub answers get no such line.",
>    "source": "https://github.com/dokima-dev/dokima/issues/417"
>   },
>   {
>    "text": "When the refusal is GitHub's rate limit, GraphQL or REST, the step waits until that limit's reported reset, then starts what it would have started. The Next line is the same as a run that never hit the limit, and any other refusal is said at once, with no wait.",
>    "source": "https://github.com/dokima-dev/dokima/issues/417"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "A decision that still fails stops for the owner: the record's one Next line mentions the owner and the card shows Needs you.",
>    "why": "Nothing starts by itself after a failed decision, so only the owner can move the issue on.",
>    "principle": "Fail closed"
>   },
>   {
>    "text": "A run waits for the rate limit at most once. If GitHub still refuses after the reset, the step says so and stops, never retrying in a loop.",
>    "why": "The run's GitH

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 -- dokima/agent.py tests/test_next_rate_limit.py; echo $PYTHONPATH; PYTHONPATH=. python3 -m pytest -q tests/test_next_rate_limit.py tests/test_failed_run_card.py 2>&1 | tail -30
```

> 190fae3 Merge branch 'main' into try/issue-417
> 566dbf7 When a plan is approved, its pull request's checks run again by themselves (#448)
> 9397d35 worker for #417 (run 38077321070)
> /tmp/runtime
> >           assert got == want, (f"132.1: {name}: the card ended at {got} (column, Needs you), expected {want}; "
>                                  f"the run stopped at '{r.failed_step}':\n{r.tail()}")
> E           AssertionError: 132.1: plan review passed but deciding what follows failed: the card ended at None (column, Needs you), expected ('Plan', True); the run stopped at 'None':
> E             ## run: Run the plan check again once the plan is approved (exit 0)
> E             No open pull request: no check to run again.
> E             
> E             ## run: Move the card on the board (exit 0)
> E             ::error::Could not read the state of #57 (HTTP 502: Bad Gateway (https://api.github.com/graphql)), so its cards were left as they were.
> E             ::warning title=Board not moved::the card could not be moved
> E             
> E             ## run: Fail closed on a bad hand-back or the wrong model (exit 0)
> E             models: ['claude-opus-5-5']
> E             
> E           assert None == ('Plan', True)
> 
> tests/test_failed_run_card.py:134: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_failed_run_card.py::test_a_failed_run_lands_in_its_stage_column_with_needs_you - AssertionError: 132.1: plan review passed but deciding wha

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_next_rate_limit.py
```

> """Deciding what runs next says why GitHub failed, and waits out its rate limit (#417).
> 
> agent.yml runs `python3 -m dokima.agent next N OUT` as `NEXT=$(...) || NEXT=stop`, so before #417 a GitHub call that
> failed inside it (on 10-10, "GraphQL: API rate limit already exceeded for installation ID ...") became a stop with no
> Next line and no word on the issue. These tests run the same `next` command in-process on a passed planner record,
> whose decision is to start the plan reviewer, against a fake GitHub that stands in for `dokima.agent.gh`:
> 
> - `gh issue view` gives the issue and its comments, `gh pr list` gives no pull requests, and `gh api rate_limit`
>   gives GitHub's rate limit answer (`resources.graphql.reset` and `resources.core.reset`, epoch seconds), the one
>   call GitHub answers even when the limit has run out.
> - A fake clock replaces `time.time`, and `time.sleep` only moves it forward, so a wait of an hour takes no time.
> - Every other call fails, the way gh fails (CalledProcessError with GitHub's words on stderr), while the fake clock
>   is before the reset of the limit that ran out, or always, or never, as each test says.
> 
> What the run decided is what `next` printed (the workflow reads it as NEXT) and the Next line it added to the
> record (OUT/comment.md, which the workflow posts on the issue); OUT/board.txt says whether the card shows Needs you.
> So the fakes reach the code, `next` reads GitHub only through `dokima.agent.gh` and reads the clock and waits only
> through `ti

`7. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1|tail -1; cp tests/test_next_rate_limit.py /tmp/mainwt/tests/; cd /tmp/mainwt; PYTHONPATH=. python3 -m pytest -q tests/test_next_rate_limit.py 2>&1 | grep -E "^(FAILED|E  .*41[0-9]\.|[0-9]+ (passed|failed))" | head -30
```

> E       AssertionError: 417.1: GitHub refused a call while deciding what runs next, and the record holds 0 lines with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)', not one (the error escaped the step: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)):
> E       AssertionError: 417.2: the rate-limited decision was never tried again; GitHub's error escaped: GraphQL: API rate limit already exceeded for installation ID 168252268
> E       AssertionError: 417.2: the rate-limited decision was never tried again; GitHub's error escaped: API rate limit exceeded for installation ID 168252268. (HTTP 403)
> E       AssertionError: 417.2: the server error was not said on the record:
> E       AssertionError: 417.3: the error escaped the step, so the record has no Next line: GraphQL: API rate limit already exceeded for installation ID 168252268
> E       AssertionError: 417.3: the error escaped the step, so the record has no Next line: HTTP 502: Server Error (https://api.github.com/repos/o/r/issues/57)
> E       AssertionError: 417.4: the rate-limited run did not end with a decision: GraphQL: API rate limit already exceeded for installation ID 168252268
> E       AssertionError: 417.2: after GitHub's rate limit on 'api repos/o/r/issues/57' reset, the run printed 'stop', not 'start worker' (it waited 0 s for a reset 300 s away); its Next lines: ['**Next:** @owner-person Autopilot could not be read from GitHub, so nothing starts by itself. The pl

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "undecided" dokima/agent.py | head; sed -n 1,40p tests/test_failed_run_card.py; grep -n "deciding what follows" -A8 tests/test_failed_run_card.py; git worktree remove --force /tmp/mainwt
```

> """A failed run puts its card in Needs you, in the column of the stage that ran (#132).
> 
> Two layers. The first runs the agent workflow (.github/workflows/agent.yml) step by step the way GitHub runs it, using
> the machine from tests/test_start.py, with a board set (vars.DOKIMA_BOARD), so its "Move the card on the board" step
> really runs `python3 -m dokima.agent board`. The fake `gh` also answers the board's GraphQL calls and records every
> field it sets, so each test reads back where the card ended up: its Status column and whether it shows Needs you. The
> fake Claude Code can be told to crash, and the fake `gh` can be told to fail every read of the issue once the agent
> has started, which is how the run's own "Decide what follows" step fails in real life (GitHub answering 502).
> 
> The second layer runs `python3 -m dokima.agent board N OUT` alone, the way the board step does, with a fake `gh` on
> PATH: when the run left no decision behind (no board.txt, or nothing at all in OUT), the card must still land in the
> column of the stage the run was for, with Needs you.
> """
> import json
> import os
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.dirname(__file__))
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> import test_start as T  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> 
> # Answers the board's GraphQL calls and records every field set or cleared; fails reads of the issue after the agent.
> GH_EXTRA = r'''
> if os.path.exists

**Agent:** Plan's tests all fail on main for the right reasons; one weakness found in the 417.3 test. Writing the hand-back now.

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Kept the plan of round two: two criteria, two requirements, ten tests in tests/test_next_rate_limit.py, scope dokima/agent.py and that test file."],
  "decided": ["A failed decision stops for the owner, proven by the run's board line ending in 'needs'."],
  "open": ["The test for 417.3 checks the board line the run writes, not the card the owner sees."]},
 "verdict": "block",
 "summary": "Every test fails today for the right reason, but the test for 417.3 passed on a build whose card lost Needs you, so it does not prove the card shows Needs you.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "417.3: weak test",
   "text": "417.3 promises the card shows Needs you when a decision still fails. Its test, test_a_failed_decision_stops_for_the_owner, only checks that OUT/board.txt ends in ' needs'. The worker's first build passed it while the real card lost Needs you: writing board.txt sends the board step to rebuild the card from GitHub, which is still refusing, so the card is left as it was. The code review caught this only through an older test (132.1), not through this plan's proof. Smallest fix: make the 417.3 test follow the run through to the card. For example, after `next` fails on a rate limit that does not lift, and on a server error, run `python3 -m dokima.agent board 57 OUT` (or the agent workflow, as tests/test_failed_run_card.py's BoardRun does) with GitHub still refusing reads of the issue, and check the card ends in its stage's column (Plan for a planner record) with Needs you. Add tests/test_failed_run_card.py to the scope if the test reuses its machine.",
   "evidence": "On commit 9397d35 (the worker's first build, now on try/issue-417): PYTHONPATH=. pytest -q tests/test_next_rate_limit.py passes test_a_failed_decision_stops_for_the_owner[rate-limit-again] and [server-error], while tests/test_failed_run_card.py::test_a_failed_run_lands_in_its
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every test fails today for the right reason, but the 417.3 test passed on a build whose card lost Needs you."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 417 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I've blocked the plan for [#417](https://github.com/dokima-dev/dokima/issues/417) (autopilot losing a step when GitHub refuses a call) and sent one blocker back to the planner. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What holds up:**
- All three of your asks map to a criterion: the reason goes on the record (417.1), the step tries again after the rate limit resets (417.2), and no step is lost (417.2).
- I ran the plan's ten tests against main and all ten fail because the feature is missing, not because of a crash or a bad path. That includes the case where autopilot was read after the plan review passed, which is your 15:12Z failure.

**The blocker (417.3 test is too weak):** 417.3 promises that when a decision still fails, the card shows Needs you. Its test, `test_a_failed_decision_stops_for_the_owner` (`tests/test_next_rate_limit.py:242`), only checks the board line the run writes, not the card itself.
- On the worker's first build, which is what this branch still holds, that test passes. Meanwhile the older test `tests/test_failed_run_card.py::test_a_failed_run_lands_in_its_stage_column_with_needs_you` (from issue 132) fails, with the card ending in no column and without Needs you.
- The cause: writing that board line makes the board step rebuild the card from GitHub. GitHub is still refusing, so the card is left as it was.
- The fix I asked for: make the 417.3 test follow the run through to the card, with GitHub still refusing, and check the card lands in its stage's column with Needs you. If it reuses the older test's setup, `tests/test_failed_run_card.py` joins the scope.

The plan's criteria don't change, so once the plan review passes again, the fix should go straight to the worker without waiting for `/work`.

The worker's second fix, which adds an "undecided" marker, isn't on this branch, so I couldn't check it. That's for the code review of [#447](https://github.com/dokima-dev/dokima/pull/447) (the pull request for #417).
