# reviewer (plan) for #313

Run: https://github.com/dokima-dev/dokima/actions/runs/37887367837

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
> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #313](https://github.com/dokima-dev/dokima/issues/313)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> #253 made an approved plan's worker wait until its blockers close, but the step that starts planning still skips any issue with an open blocker. So a split on autopilot starts only its unblocked stories, and a blocked one (for example #311, blocked by #309) sits unplanned until its blocker closes.
> 
> What I want:
> - On a

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_blocked_plans.py; cat tests/test_blocked_plans.py
```

> commit 0fb503ce382b78b7fbee99fd5bd9bcd46e7c51e5
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:11:01 2026 +0000
> 
>     planner for #313 (run 37884977913)
> 
>  tests/test_autopilot_close.py |  56 +++++---
>  tests/test_autopilot_river.py |  11 +-
>  tests/test_autopilot_start.py |  25 ++--
>  tests/test_blocked_plans.py   | 322 ++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 373 insertions(+), 41 deletions(-)
> 322 tests/test_blocked_plans.py
> """On autopilot, a blocked story plans at once; only its worker waits (#313).
> 
> Before this, every step that starts a planner on autopilot skipped an issue with an open blocker: a split filed only
> its unblocked stories' planners, `/autopilot start` left blocked issues alone, and a close started only the issues
> whose blockers had all closed. So a blocked story (such as #311, blocked by #309) sat unplanned until its blocker
> closed, though #253 already makes the worker the one that waits.
> 
> These tests run the workflows the way GitHub runs them, on the machine of test_start.py, against the fake GitHub of
> test_autopilot_close.py (issue tree, labels, states, blocked-by links, comments and start signals). Where only the
> river's decision between two stages matters, the journey runs `python3 -m dokima.agent next N OUT` on the finished
> stage's record, against the same fake GitHub, as agent.yml does after every run.
> 
> A blocked issue that starts planning gets one line naming its open blockers,

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_blocked_plans.py -x -q 2>&1 | tail -5; timeout 900 python3 -m pytest -q tests/test_blocked_plans.py 2>&1 | grep -E "^E .*31[3]\.|passed|failed" | head -30
```

> {
>         900: 1,
>   -     901: 1,
>     }
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
>             assert not m.failed, f"313.1 ({case}): the listener failed:\n{m.tail()}"
> E           AssertionError: 313.1 (/work on autopilot): every story should start planning once, the blocked #901 too; planners started: {900: 1}
>         assert not m.failed, f"313.2 (blocked issue): the listener failed:\n{m.tail()}"
> E       AssertionError: 313.2 (blocked issue): #57, blocked by #110, should start planning once: {}
>         assert not m.failed, f"313.3: a workflow failed when #313 closed: {m.failures}\n{m.tail()}"
> E       AssertionError: 313.3: #311 and #312, stuck on autopilot with no plan, should each start planning once, and nothing else: {}
>         assert not m.failed, f"313.4: the listener failed on /work:\n{m.tail()}"
> E       AssertionError: 313.4: the journey stopped at the split: blocked #901's planner did not start once: {900: 1}
> E        +      where {900: 1} = planners_started('313.4')
>         assert not m.failed, f"313.5: a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 313.5: #101 and blocked #102 should each have started planning exactly once: {101: 1}
> E           AssertionError: 313.6: AGENTS.md's The flow does not say 'starts planning as soon as it exists, blocked or not'
> 6 failed in 6.96s

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_autopilot_close.py tests/test_autopilot_river.py tests/test_autopilot_start.py | head -300
```

> commit 0fb503ce382b78b7fbee99fd5bd9bcd46e7c51e5
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:11:01 2026 +0000
> 
>     planner for #313 (run 37884977913)
> 
> diff --git a/tests/test_autopilot_close.py b/tests/test_autopilot_close.py
> index 671d781..d3b10b1 100644
> --- a/tests/test_autopilot_close.py
> +++ b/tests/test_autopilot_close.py
> @@ -449,13 +449,16 @@ def test_a_close_starts_every_sibling_whose_blockers_have_all_merged(record_prop
>      #57 is on autopilot with sub-issues #101 to #105. #102 is blocked by #101; #105 by #101 and #110 (already
>      closed, outside the tree); #103 by #101 and #104, which is still open; #104 already has a plan. When #101 closes,
>      #102 and #105 must each have their planner started once by Dokima's signal and get exactly one comment reading the
> -    Autopilot line; #103 (still blocked), #104 (already planned), #101 and the parent #57 must not."""
> +    Autopilot line; #104 (already planned), #101 and the parent #57 must not. #103, still blocked by #104, starts
> +    planning too (#313: on autopilot a blocked story plans at once), once, but not with the blockers-merged line."""
>      record_property("proves", "213.1")
>      m = Repo(tmp_path / "close", {57: [101, 102, 103, 104, 105]}, ALL,
>               deps={102: [101], 103: [101, 104], 105: [101, 110]}, closed=[110], seed=[planned(104, 4001)])
>      m.close(101)
>      assert not m.failed, f"213.1: a workflow failed when #101 closed: {m.failures}

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1500 python3 -m pytest -q -x -p no:cacheprovider tests/ --deselect tests/test_blocked_plans.py 2>&1 | tail -3; timeout 1500 python3 -m pytest -q tests/test_autopilot_close.py tests/test_autopilot_river.py tests/test_autopilot_start.py 2>&1 | grep -E "^FAILED|passed|failed"
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bnrcqv5p1). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bnrcqv5p1.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "blockers merged, starting plan\|def .*start.*plan\|def file_split\|nothing open" dokima/agent.py | head -40
```

> 232:def file_split(repo, parent, recs, labels=()):
> 1110:        said += f" Planning started for {', '.join(f'#{n}' for n in started)}, which wait on nothing open."
> 1116:AUTOPILOT_LINE = "Autopilot: blockers merged, starting plan"
> 1285:def start_planner(repo, number, line=AUTOPILOT_LINE):
> 1295:    """Start the planner of every open issue among `numbers` with no sub-issues, nothing open blocking it and nothing
> 1952:            # The issue itself starts its planner when it waits on nothing open and nothing started on it yet.
> 1954:            # `/autopilot start` picks up every issue under the issue, at every level, that waits on nothing open.

**Agent:** Still reviewing the plan for #313. The new tests fail for the right reason, and the full test suite is running now.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1280,1330p dokima/agent.py; grep -n "start_unblocked\|start_planners\|def autopilot_split\|file_split(" dokima/agent.py | head
```

> MARK in body or LIVE in body or body.strip() in (AUTOPILOT_LINE, AUTOPILOT_START_LINE)):
>             return True
>     return False
> 
> 
> def start_planner(repo, number, line=AUTOPILOT_LINE):
>     """Start the issue's planner with the river's own signal, after one Autopilot line where the owner would have said /plan.
> 
>     The line goes first: it is the record that this issue was started, so no later close starts it again."""
>     gh("issue", "comment", str(number), "-R", repo, "--body", line)
>     gh("api", "-X", "POST", f"repos/{repo}/dispatches", "-f", "event_type=dokima-next", "-f", "client_payload[role]=planner",
>        "-f", "client_payload[stage]=plan", "-f", f"client_payload[issue]={number}")
> 
> 
> def start_waiting(repo, numbers, need_blocker=False, line=AUTOPILOT_LINE):
>     """Start the planner of every open issue among `numbers` with no sub-issues, nothing open blocking it and nothing
>     started on it yet; with need_blocker, only those blocked by at least one issue (all now closed). Returns those started."""
>     started = []
>     for n in numbers:
>         if json.loads(gh("api", f"repos/{repo}/issues/{n}")).get("state") != "open" or sub_issues(repo, n):
>             continue
>         blockers = blocked_by(repo, n)
>         if (need_blocker and not blockers) or any(b.get("state") != "closed" for b in blockers):
>             continue
>         if started_before(repo, n):
>             continue
>         start_planner(repo, n, line)
>         started.append(n)
>     return started
> 
> 
> WAIT_LINE = 

`8. Bash`
```
sleep 200; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bnrcqv5p1.output | tail -15
```

> <tool_use_error>Blocked: sleep 200 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bnrcqv5p1.output tail -15. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`9. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bnrcqv5p1.output | tail -15
```

> +        where planners_started = <test_autopilot_close.Repo object at 0x7f402c609100>.planners_started
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 75 passed, 6 deselected in 95.24s (0:01:35)

**Agent:** I'll wait for the rest of the suite to finish before writing the review.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1500 python3 -m pytest -q -p no:cacheprovider tests/ 2>&1 | grep -E "^FAILED|passed|failed"
```

> Command running in background with ID: bprcko0xg. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bprcko0xg.output. You will be notified when it completes. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner wrote four criteria and two requirements: every story on autopilot starts planning at once, blocked or not, when a split is filed, on `/autopilot start` and at every close, and only its worker waits for its blockers.",
          "It wrote six new tests in tests/test_blocked_plans.py and changed nine existing tests that said a blocked story must not start planning."],
  "decided": ["A blocked story that starts planning gets its own line, `Autopilot: starting plan, its worker waits for #A and #B to close`, and is never started twice.",
              "AGENTS.md is updated, and the header comment of autopilot.yml stays as it is because workflow files are off limits."],
  "open": ["A sub-issue a person attaches by hand on GitHub starts planning at the next close or `/autopilot start`, not the minute it is added. This is the owner's call."]
 },
 "verdict": "approve",
 "summary": "The plan covers every ask, each test fails today because the feature is missing, and only the question about stories attached by hand is left for you.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 313.1 names three ways a split is filed. The 313.1 test covers `/work` and `/autopilot start`. The third way, the plan review approving the split on autopilot, is covered only by the changed river test. That test checks that #901 starts planning but not its waiting line. All three ways use the same filing code, so the risk is small.",
   "evidence": "tests/test_blocked_plans.py::test_a_split_on_autopilot_starts_planning_every_story_blocked_or_not runs only '/work' and '/autopilot start'; tests/test_autopilot_river.py::assert_stories_as_work_files_them checks only the planners; dokima/agent.py:1817 is the only file_split call."},
  {"text": "Today the record that an issue has started is only the two existing Autopilot lines. The new waiting line must be added to that record, or every cl
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`12. Bash`
```
cd /home/runner/work/dokima/dokima; tail -12 /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bnrcqv5p1.output; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers every ask and each new test fails today because the feature is missing; the question about stories attached by hand goes to you."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> assert not m.failed, f"245.3 (plan waiting): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"245.3 (children): the listener failed:\n{m.tail()}"
> FAILED tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged - AssertionError: 213.1 (close): #103, still blocked, should start planning once without the blockers-merged line: []
> FAILED tests/test_autopilot_close.py::test_a_split_filed_on_autopilot_starts_its_unblocked_stories - AssertionError: 213.1 (split on autopilot): blocked #901 should start planning once without the blockers-merged line: []
> FAILED tests/test_autopilot_close.py::test_autopilot_start_on_a_parent_picks_up_the_children_waiting - AssertionError: 213.1 (/autopilot start): blocked #102 should start planning once without the blockers-merged line: []
> FAILED tests/test_autopilot_close.py::test_autopilot_start_picks_up_waiting_issues_at_every_level - AssertionError: 213.1 (/autopilot start, every level): blocked #202 and #302 should each start planning once: {102: 1, 301: 1}
> FAILED tests/test_autopilot_close.py::test_a_close_deep_in_the_tree_starts_its_waiting_siblings - AssertionError: 213.1 (deep close): blocked #202 should start planning once: {302: 1}
> FAILED tests/test_autopilot_river.py::test_on_autopilot_an_approved_split_files_its_stories_with_one_autopilot_line - AssertionError: 211.2 (the river): the stories did not start as `/work` on autopilot starts them (each plans once, the blocked #901 too): [('pla

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers every ask and each new test fails today for the right reason; the question about stories attached by hand goes to you."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #313. One question still needs your answer: how a story that someone attaches by hand on GitHub should start.

**What the plan does:** On autopilot, every story starts planning right away, blocked or not. That happens when a split files its stories, on `/autopilot start`, and at every issue close. When this merges and #313 closes, the stuck stories like #311 start planning. A blocked story gets one new line, `Autopilot: starting plan, its worker waits for #A and #B to close`, and is never started twice. Only its worker waits for its blockers, as #253 already does. AGENTS.md gets updated to match.

**Test runs:**
- All six new tests in `tests/test_blocked_plans.py` fail today because the feature is missing, not because of a crash or bad setup.
- The planner changed nine existing tests. Seven now fail because each expects a blocked story to start planning, which it doesn't yet.
- One changed test passes today. It was rewritten to accept that the blocked story starts at the first close, and the old code also starts it later in that test, so it can't tell old from new.
- I started a run of the whole suite; it hadn't finished when I wrote this. Before that, an earlier run stopped at its first failure (one of the changed tests above), with 75 tests passed.

**Your question:** You wrote that every story starts planning "as soon as it exists", including "when a story is added to a tree on autopilot". The plan reads that as stories Dokima files. A sub-issue someone attaches by hand would only start at the next close or `/autopilot start`, not the same minute. Doing it the same minute would need a workflow file change, and only you can allow that. I did not accept this assumption, so it stops for you.
- Answer with `/plan` and your words to change it.
- Or say `/review` to go on with the planner's reading.

**Two minor gaps (neither blocks):**
- When the plan review approves a split on its own, the tests check that the blocked story starts planning, but not its waiting line. All three ways of filing a split use the same code, so the risk is small.
- The new waiting line has to count as "already started", or every later close would start the blocked story again. Today only the two existing Autopilot lines count. The tests for criterion 313.5 check this.

The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

`14. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/89491b9f-3725-4839-9faa-2dbca3fbcedd/tasks/bprcko0xg.output
```

> assert not m.failed, f"213.1: a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
>         assert not m.failed, f"213.1 (split on autopilot): the listener failed on /work:\n{m.tail()}"
>         assert not m.failed, f"213.1 (/autopilot start): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"213.1 (/autopilot start, every level): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"213.1 (deep close): a workflow failed when #301 closed: {m.failures}\n{m.tail()}"
>         assert not m.failed, f"245.3 (plan waiting): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"245.3 (children): the listener failed:\n{m.tail()}"
>             assert not m.failed, f"313.1 ({case}): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"313.2 (blocked issue): the listener failed:\n{m.tail()}"
>         assert not m.failed, f"313.3: a workflow failed when #313 closed: {m.failures}\n{m.tail()}"
>         assert not m.failed, f"313.4: the listener failed on /work:\n{m.tail()}"
>         assert not m.failed, f"313.5: a workflow failed: {m.failures}\n{m.tail()}"
> FAILED tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged - AssertionError: 213.1 (close): #103, still blocked, should start planning once without the blockers-merged line: []
> FAILED tests/test_autopilot_close.py::test_a_split_filed_on_autopilot_starts_its_unblocked_stories - AssertionError: 213.1 (split on autopilot): blocked #901 should start

**Agent:** The full test suite has finished: 705 tests pass and 13 fail. All 13 are tests the planner wrote or changed for #313. They fail because blocked stories don't start planning yet, and AGENTS.md doesn't say they should yet.

- **New tests:** all 6 in `tests/test_blocked_plans.py` fail.
- **Changed tests:** 7 of the 9 fail. Six expect a blocked story to start planning. The seventh, the plan-review test, checks that a split filed by the plan review starts the blocked story's planner too.

No test the planner left alone fails, so the plan breaks nothing else. My approval stands. The question about stories someone attaches by hand on GitHub is still yours: answer with `/plan` and your words to change it, or `/review` to go on with the planner's reading. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.
