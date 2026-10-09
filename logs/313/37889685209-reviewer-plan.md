# reviewer (plan) for #313

Run: https://github.com/dokima-dev/dokima/actions/runs/37889685209

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (52.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7cbb40f3-ce9a-4635-83e0-b837319d782b/tool-results/bophzinr1.txt
> 
> Preview (first 2KB):
> .:
> total 80
> drwxr-xr-x  3 runner runner  4096 Oct  9 05:40 .
> drwxrwxrwt 18 root   root    4096 Oct  9 05:40 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 05:40 in
> -rw-r--r--  1 runner runner 53021 Oct  9 05:40 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 05:40 open_blockers.json
> -rw-r--r--  1 runner runner  8269 Oct  9 05:40 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:40 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:40 ..
> -rw-r--r-- 1 runner runner 7593 Oct  9 05:40 01-planner.json
> -rw-r--r-- 1 runner runner 4705 Oct  9 05:40 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8933 Oct  9 05:40 03-planner.json
> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #313](https://github.com/dokima-dev/dokima/issues/313)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16"

`2. Bash`
```
cd /tmp/pack; sed -n '/Original issue\|dokima-card-end\|<!-- dokima-ask/,$p' issue.md | head -300; grep -n "^##\|^---\|^\*\*@\|^### " issue.md | head -80
```

> <!-- dokima-ask -->
> 
> #253 made an approved plan's worker wait until its blockers close, but the step that starts planning still skips any issue with an open blocker. So a split on autopilot starts only its unblocked stories, and a blocked one (for example #311, blocked by #309) sits unplanned until its blocker closes.
> 
> What I want:
> - On autopilot, every story starts planning as soon as it exists, blocked or not: when a split files its stories, on `/autopilot start`, and when a story is added to a tree on autopilot. Only its worker waits for its blockers, as #253 already does.
> - Right after this merges, every open story on autopilot that has no plan yet starts planning, so the ones already stuck (like #311) get going.
> - A test proves the whole journey: a split on autopilot with one blocked story ends with that story planned and its worker waiting, then building once the blocker closes.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #313 (2026-10-09T04:40:02Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #313 (2026-10-09T04:40:25Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #313 (2026-10-09T04:40:27Z)
> 
> Autopilot is on for #313. Planning started for #313, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #313 (2026-10-09T04:40:39Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/doki

`3. Bash`
```
cd /tmp/pack; sed -n 414,425p issue.md; sed -n 626,700p issue.md; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> ### RezaSoleymanifar on issue #313 (2026-10-09T05:25:50Z)
> 
> /plan Both: stories Dokima files in a split, and sub-issues I attach by hand on GitHub. Anything in a tree on autopilot starts planning right away.
> 
> ### dokima-runtime on issue #313 (2026-10-09T05:26:48Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** On autopilot, every story starts planning the moment it is in the tree, blocked or not, whether Dokima filed it or you attached it by hand, so only building waits for blockers and a stuck story like #311 gets going.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> ### dokima-runtime on issue #313 (2026-10-09T05:40:14Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> **Reviewer (plan)** · setting up
> 
> The machine is setting up: the bra

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; wc -l tests/test_blocked_plans.py; git diff 0fb503c HEAD --stat; cat .github/workflows/autopilot.yml
```

> commit 253bf7a6d4d34f20a50adedc5911e4e1bc475f25
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:40:03 2026 +0000
> 
>     planner for #313 (run 37888536409)
> 
>  tests/test_blocked_plans.py | 230 +++++++++++++++++++++++++++++++++++++++++++-
>  1 file changed, 228 insertions(+), 2 deletions(-)
> 
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
> 
> commit e1a21e7925afcc148c291b29387671276d399726
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:34:17 2026 -0500
> 
>     Three kinds of raise and one table of who raises to whom, checked by code (#304)
>     
>     * planner for #298 (run 37881386661)
>     
>     * worker for #298 (run 37881925855)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  dokima/raises.py     | 117 ++++++++++++++++++
>  tests/test_r

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 0fb503c HEAD; 
```

> diff --git a/tests/test_blocked_plans.py b/tests/test_blocked_plans.py
> index 4f61fae..f6acb5e 100644
> --- a/tests/test_blocked_plans.py
> +++ b/tests/test_blocked_plans.py
> @@ -10,6 +10,10 @@ test_autopilot_close.py (issue tree, labels, states, blocked-by links, comments
>  river's decision between two stages matters, the journey runs `python3 -m dokima.agent next N OUT` on the finished
>  stage's record, against the same fake GitHub, as agent.yml does after every run.
>  
> +A sub-issue someone attaches by hand to a tree on autopilot joins it and plans too. GitHub sends no event when an
> +existing issue is attached, so autopilot also looks on a schedule, every 5 minutes, and when an issue opens; an issue
> +someone took off autopilot is never put back on it.
> +
>  A blocked issue that starts planning gets one line naming its open blockers, `Autopilot: starting plan, its worker
>  waits for #A and #B to close`, where the owner would have said `/plan`.
>  """
> @@ -305,7 +309,8 @@ def test_agents_md_says_every_story_on_autopilot_plans_as_soon_as_it_exists(reco
>  
>      The flow section must say "starts planning as soon as it exists, blocked or not" and name the line
>      `Autopilot: starting plan, its worker waits for #A and #B to close`, and still say a blocked issue's worker waits
> -    until every blocker closes. Neither The flow nor Commands may still say an issue starts its planner only when its
> +    until every blocker closes. It must also say a sub-issue "attached by hand" to a tree on autopilot 

**Agent:** I'm reviewing the re-plan for #313 and running its tests now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_blocked_plans.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|AssertionError|^E " | head -60
```

> assert not m.failed, f"313.1 ({case}): the listener failed:\n{m.tail()}"
> E           AssertionError: 313.1 (/work on autopilot): every story should start planning once, the blocked #901 too; planners started: {900: 1}
> E             ## route: r (exit 0)
> E             role=worker
> E             stage=
> E             issue=57
> E             
> E             ## queue: Put up the run's queued card (exit 0)
> E             
> E             ## split: File the approved split's stories as sub-issues (exit 0)
> E             
> E           assert {900: 1} == {900: 1, 901: 1}
> E             
> E             Omitting 1 identical items, use -vv to show
> E             Right contains 1 more item:
> E             {901: 1}
> E             
> E             Full diff:
> E               {
> E                   900: 1,
> E             -     901: 1,
> E               }
> tests/test_blocked_plans.py:90: AssertionError
>         assert not m.failed, f"313.2 (blocked issue): the listener failed:\n{m.tail()}"
> E       AssertionError: 313.2 (blocked issue): #57, blocked by #110, should start planning once: {}
> E         ## route: r (exit 0)
> E         autopilot=start
> E         issue=57
> E         
> E         ## autopilot: Switch the issue tree on or off autopilot, and say which issues, where it was written (exit 0)
> E         https://github.com/o/r/issues/57#issuecomment-5001
> E         
> E       assert {} == {57: 1}
> E         
> E         Right contains 1 more item:
> E         {57: 1}
> E         
> E         Full diff:
> E         + {}
> E         - {
> E

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_blocked_plans.py 2>&1 | grep -E "^E   +AssertionError|^FAILED|passed|failed" | head -30; timeout 900 python3 -m pytest -q tests/test_autopilot_close.py tests/test_autopilot_river.py tests/test_autopilot_start.py 2>&1 | grep -E "^E   +AssertionError|^FAILED|passed|failed"|head
```

> assert not m.failed, f"313.1 ({case}): the listener failed:\n{m.tail()}"
> E           AssertionError: 313.1 (/work on autopilot): every story should start planning once, the blocked #901 too; planners started: {900: 1}
>         assert not m.failed, f"313.2 (blocked issue): the listener failed:\n{m.tail()}"
> E       AssertionError: 313.2 (blocked issue): #57, blocked by #110, should start planning once: {}
>         assert not m.failed, f"313.3: a workflow failed when #313 closed: {m.failures}\n{m.tail()}"
> E       AssertionError: 313.3: #311 and #312, stuck on autopilot with no plan, should each start planning once, and nothing else: {}
>         assert not m.failed, f"313.4: the listener failed on /work:\n{m.tail()}"
> E       AssertionError: 313.4: the journey stopped at the split: blocked #901's planner did not start once: {900: 1}
>         assert not m.failed, f"313.5: a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 313.5: #101 and blocked #102 should each have started planning exactly once: {101: 1}
> E           AssertionError: 313.6: AGENTS.md's The flow does not say 'starts planning as soon as it exists, blocked or not'
> E       AssertionError: 313.3: no workflow runs every 5 minutes to find sub-issues attached by hand; schedules: []
> E           AssertionError: 313.3 (free): #130, opened under #57 on autopilot, should start planning once: {}
>         assert not m.failed, f"313.7: a workflow failed on the schedule: {m.failures}\n{m.tail()}"
> E       AssertionError

`8. Bash`
```
cd /tmp/pack; cat open_blockers.json; grep -o "issuecomment-[0-9]*" issue.md | sort -u; grep -n "issuecomment\|05:25:50" issue.md | head; python3 -c "import json;d=json.load(open('in/03-planner.json'));print(d.keys(), json.dumps(d.get('handback',{}).get('concerns'),indent=1))"; ls in; head -c 600 in/02-reviewer-plan.json
```

> []414:### RezaSoleymanifar on issue #313 (2026-10-09T05:25:50Z)
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']) [
>  {
>   "text": "GitHub sends no event when an existing issue is attached as a sub-issue, so \"right away\" for a hand-attached issue can only mean the next scheduled look (every 5 minutes, the shortest GitHub allows). An issue created as a sub-issue starts the moment it opens. Both need a change to .github/workflows/autopilot.yml, which your answer asks for; on autopilot that pull request stops for you before merging.",
>   "evidence": "https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows lists no sub-issue event; .github/workflows/autopilot.yml runs only on issues: closed."
>  }
> ]
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37887367837",
>  "commit_before": "0fb503ce382b78b7fbee99fd5bd9bcd46e7c51e5",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 6215,
>   "turns": 2,
>   "cost_usd": 0.7388139999999999,
>   "tokens_in": 130059,
>   "tokens_out": 442
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/313/37887367837-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37887367837",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner wrote four criteria and two req
> Shell cwd was reset to /hom

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner added the owner's answer to 313.3: a sub-issue attached by hand under an issue on autopilot gets the `autopilot` label and starts planning, blocked or not.",
   "It added three tests (attached by hand, created as a sub-issue, taken off autopilot) and a seventh promise: an issue taken off autopilot stays off while its parent stays on."
  ],
  "decided": [
   "Autopilot looks every 5 minutes on a schedule and whenever an issue opens, which changes .github/workflows/autopilot.yml.",
   "A story attached by hand starts at the next look, at most about 5 minutes later, because GitHub sends no event when an issue is attached."
  ],
  "open": [
   "The owner asked for 'right away'. A schedule that runs every 5 minutes, all day, was chosen without asking them."
  ]
 },
 "verdict": "block",
 "summary": "The plan covers every ask and its new tests fail today for the right reason. But you asked for attached stories to start 'right away', and the plan changes that to a new schedule that runs every 5 minutes, all day, without asking you, so it goes back to the planner to put that to you as a question.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "313.3",
   "test": "tests/test_blocked_plans.py::test_a_sub_issue_attached_by_hand_joins_autopilot_and_plans_at_the_next_look",
   "problem": "The owner asked that a sub-issue attached by hand start planning 'right away'. The plan says that can't be done and changes it to 'at the next look', from a new schedule that runs about 288 times a day for good. That changes how the system works and what it costs, and the owner never chose it. The plan raises it only as a concern, so the owner never decides. On autopilot, approving this plan would start the worker on that choice.",
   "evidence": "Owner's comment on #313 (2026-10-09T05:25:50Z): 'sub-issues I attach by hand on GitHub. Anything in a tree on autopilot starts pla
```

> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> rc=1

`10. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The tests are sound, but the plan swaps your 'right away' for a new 5-minute schedule without asking you, so it goes back to the planner."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`11. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The tests are sound, but the plan swaps your 'right away' for a 5-minute schedule without asking you, so it goes back to the planner."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the new plan for #313 and sent it back to the planner. The review is saved in `/tmp/dokima-out/review.json` and passes both checks.

**What's sound:**
- **Asks:** each of your seven asks, including your comment "sub-issues I attach by hand… starts planning right away", is covered by a criterion.
- **Tests:** I ran all nine new tests and all nine fail today for the right reason: the feature isn't there yet, not a crash or a setup problem. The nine older tests the plan changes also fail on the blocked stories that should now start planning.

**Why it's blocked:** You asked for stories you attach by hand to start "right away". GitHub sends no event when an existing issue is attached as a sub-issue, so the plan replaces that with two things:
- a new check that runs every 5 minutes, about 288 runs a day, which can run late;
- a change to `.github/workflows/autopilot.yml` so the check also runs when an issue opens.

That changes how the system works and what it costs, and you never chose it. The plan raised it as a concern, not a question. Because #313 is on autopilot, approving the plan would have started the worker on that choice. The fix is for the planner to ask you, assume the 5-minute check, and keep the criteria and tests as they are.

**Two notes for your answer:**
- If a scheduled check fails, there's no issue for it to report on, so the reason stays in the run's log. That bends the rule that a failure always says why on the issue.
- When you use GitHub's "create sub-issue" button, the issue may open before GitHub links it to its parent. The check that runs when an issue opens could then miss it, and it would start at the next scheduled check. The test assumes the link is already there.
