# reviewer (plan) for #313

Run: https://github.com/dokima-dev/dokima/actions/runs/37891094297

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (116.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/53143d22-7e98-4bdd-bad5-3e75bfe8e9e1/tool-results/btu1fisyt.txt
> 
> Preview (first 2KB):
> .:
> total 136
> drwxr-xr-x  3 runner runner   4096 Oct  9 05:58 .
> drwxrwxrwt 18 root   root     4096 Oct  9 05:58 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 05:58 in
> -rw-r--r--  1 runner runner 111029 Oct  9 05:58 issue.md
> -rw-r--r--  1 runner runner      2 Oct  9 05:58 open_blockers.json
> -rw-r--r--  1 runner runner   7625 Oct  9 05:58 plan.json
> 
> in:
> total 76
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:58 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:58 ..
> -rw-r--r-- 1 runner runner 7593 Oct  9 05:58 01-planner.json
> -rw-r--r-- 1 runner runner 4705 Oct  9 05:58 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8933 Oct  9 05:58 03-planner.json
> -rw-r--r-- 1 runner runner 5623 Oct  9 05:58 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 9301 Oct  9 05:58 05-planner.json
> -rw-r--r-- 1 runner runner 4165 Oct  9 05:58 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8272 Oct  9 05:58 07-planner.json
> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json; echo; wc -l issue.md; grep -n "^## \|^### \|^\*\*.*commented\|^---" issue.md | head -80
```

> []
> {
>  "kind": "user_story",
>  "summary": "On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.",
>  "user_story": "On autopilot, every story starts planning the moment it is in the tree, blocked or not, whether Dokima filed it or you attached it by hand, so only building waits for blockers and a stuck story like #311 gets going.",
>  "acceptance_criteria": [
>   {
>    "text": "When a split is filed on autopilot (by `/work`, by autopilot itself or by `/autopilot start`), every story starts planning at once, blocked or not. An unblocked story gets `Autopilot: blockers merged, starting plan` as today; a blocked story gets one line naming its open blockers, `Autopilot: starting plan, its worker waits for #A and #B to close`.",
>    "source": "https://github.com/dokima-dev/dokima/issues/313"
>   },
>   {
>    "text": "`/autopilot start` starts planning every issue in the tree that has no sub-issues and nothing started on it, blocked or not, the issue itself included. A blocked one gets the line naming its open blockers, and the comment naming what was switched no longer says the started issues wait on nothing open.",
>    "source": "https://github.com/dokima-dev/dokima/issues/313"
>   },
>   {
>    "text": "Every open story on autopilot that was never started begins planning, blocked or not, with no command. This happens when this merges and #313 closes (so #311 gets going), at every later close, and at autopilot's regular look ever

`3. Bash`
```
cd /tmp/pack; sed -n 1,82p issue.md; sed -n 418,424p issue.md; sed -n 1144,1150p issue.md; sed -n 1340,1354p issue.md
```

> # Issue #313: On autopilot, a blocked story starts planning right away instead of waiting for its blockers
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> On autopilot, a blocked story waits to plan until its blockers close; it should plan at once and only its worker should wait.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #313](https://github.com/dokima-dev/dokima/issues/313)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #311, #86
> 
> **User story:** On autopilot, every story starts planning the moment it is in the tree, blocked or not, whether Dokima filed it or you attached it by hand, so only building waits for blockers and a stuck story like #311 gets going.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** When a split is filed on autopilot (by `/work`, by autopilot itself or by `/autopilot start`), every story starts plann

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['06-reviewer-plan.json','07-planner.json']:
    d=json.load(open(f)); print(f); print(json.dumps(d,indent=1)[:6000])
"
```

> 06-reviewer-plan.json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37890092330",
>  "commit_before": "253bf7a6d4d34f20a50adedc5911e4e1bc475f25",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 44453,
>   "turns": 9,
>   "cost_usd": 0.3314698,
>   "tokens_in": 338596,
>   "tokens_out": 3883
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/313/37890092330-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37890092330",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner turned the 5-minute check into a question for the owner, naming its cost: about 288 short runs a day, sometimes late, and a failed check says why only in its run log."
>    ],
>    "decided": [
>     "It plans on the 5-minute check: autopilot.yml also runs every 5 minutes and whenever an issue opens. The criteria and tests stay as they were."
>    ],
>    "open": [
>     "Whether a story attached by hand waits for a 5-minute check, for the next close or `/autopilot start`, or something else is the owner's to answer."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The plan now asks you about the 5-minute check instead of choosing it, and every test fails today for the right reason.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "When someone uses GitHub's 'create sub-issue' button, the issue may open before GitHub links it to its parent. The 'opened' look could then miss it, and it would start at the next schedu

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff HEAD~1 -- tests | head -150; grep -n "15\|cron\|\*/" tests/test_blocked_plans.py | head -40
```

> commit f4a3e3f3624763013410802e893dcd9f49da4bb8
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:57:37 2026 +0000
> 
>     planner for #313 (run 37890761063)
> 
>  tests/test_blocked_plans.py | 49 ++++++++++++++++++++++++++++++++++++---------
>  1 file changed, 40 insertions(+), 9 deletions(-)
> diff --git a/tests/test_blocked_plans.py b/tests/test_blocked_plans.py
> index f6acb5e..b0bed6e 100644
> --- a/tests/test_blocked_plans.py
> +++ b/tests/test_blocked_plans.py
> @@ -11,7 +11,7 @@ river's decision between two stages matters, the journey runs `python3 -m dokima
>  stage's record, against the same fake GitHub, as agent.yml does after every run.
>  
>  A sub-issue someone attaches by hand to a tree on autopilot joins it and plans too. GitHub sends no event when an
> -existing issue is attached, so autopilot also looks on a schedule, every 5 minutes, and when an issue opens; an issue
> +existing issue is attached, so autopilot also looks on a schedule, every 15 minutes, and when an issue opens; an issue
>  someone took off autopilot is never put back on it.
>  
>  A blocked issue that starts planning gets one line naming its open blockers, `Autopilot: starting plan, its worker
> @@ -310,7 +310,7 @@ def test_agents_md_says_every_story_on_autopilot_plans_as_soon_as_it_exists(reco
>      The flow section must say "starts planning as soon as it exists, blocked or not" and name the line
>      `Autopilot: starting plan, its worker waits for #A and #B to close`, an

**Agent:** Reviewing the plan for #313: it now uses the owner's 15-minute check. Running the new tests to confirm they fail today for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "cron" .github/workflows/; timeout 600 python3 -m pytest -q tests/test_blocked_plans.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|AssertionError: 313" | head -40
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
> E       AssertionError: 313.3: no workflow runs every 15 minutes to find sub-issues attached by hand; schedules: []
> E           AssertionError: 313.3 (free): #130, opened under #57 on autopilot, should start planning once: {}
>         assert not m.failed, f"313.7: a workflow failed on the schedule: {m.failures}\n{m.tail()}"
> E       AssertionErro

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import sys; sys.path.insert(0,'tests')
from test_blocked_plans import minute_gaps as g
for c in ['*/15 * * * *','0,15,30,45 * * * *','*/5 * * * *','7 * * * *','*/15 3 * * *','0-59/15 * * * *']: print(c, g(c))"; timeout 900 python3 -m pytest -q -x tests 2>&1 | tail -5
```

> */15 * * * * {15}
> 0,15,30,45 * * * * {15}
> */5 * * * * {5}
> 7 * * * * {60}
> */15 3 * * * None
> 0-59/15 * * * * {15}
>  +    where <built-in method get of dict object at 0x7f8f178cc5c0> = {102: 1, 105: 1}.get
>  +      where {102: 1, 105: 1} = planners_started('213.1')
>  +        where planners_started = <test_autopilot_close.Repo object at 0x7f8f1795ea80>.planners_started
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 75 passed in 83.57s (0:01:23)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1200 python3 -m pytest -q tests 2>&1 | grep -E "^FAILED|passed|failed" | head -30
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
>         assert not m.failed, f"313.7: a workflow failed on the schedule: {m.failures}\n{m.tail()}"
> FAILED tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged - AssertionError: 213.1 (close): #103, still blocked, should start planning once without the blockers-merged line: []
> FAILED tests/test_autopilot_close.py::test_a_split_filed_on_autopilot_s

`9. Bash`
```
cd /tmp/pack; grep -o "https://github.com/dokima-dev/dokima/issues/313#issuecomment-[0-9]*" issue.md | sort -u; sed -n 1144,1149p issue.md
```

> ### RezaSoleymanifar on issue #313 (2026-10-09T05:53:44Z)
> 
> /plan Check every 15 minutes.
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner set autopilot's regular look to every 15 minutes, as the owner asked, in the plan, AGENTS.md's promised wording and the tests.",
          "The tests now require a workflow that runs every 15 minutes, and none that runs more often."],
  "decided": ["The plan has no questions left for the owner; the criteria are otherwise unchanged."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now checks every 15 minutes as you asked, every new test fails today because the feature is missing, and it is ready for /work.",
 "blockers": [],
 "notes": [
  {"text": "The issue's card on top still says 5 minutes; it was drawn from the earlier plan and should change to 15 on its next redraw.",
   "evidence": "/tmp/pack/issue.md card text reads 'every 5 minutes', while plan.json 313.3, 313.6 and out_of_scope say 15 minutes."},
  {"text": "When someone uses GitHub's 'create sub-issue' button, the issue may open before GitHub links it to its parent; it would then start at the next 15-minute look instead of the moment it opens.",
   "evidence": "tests/test_blocked_plans.py::test_a_sub_issue_created_under_an_issue_on_autopilot_plans_right_away builds the tree before firing issues: opened."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "On autopilot, every story starts planning as soon as it exists, blocked or not: when a split files its stories", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.1"},
  {"ask": "on `/autopilot start`", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.2"},
  {"ask": "and when a story is added to a tree on autopilot", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.3"},
  {"ask": "Only its worker waits for its blockers, as #253 already does.", "source": "https://github.com/dokima-dev/dokima/issues/313", "criterion": "313.4"},
  {"ask
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`11. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"summary": "The plan now checks every 15 minutes as you asked, every new test fails today because the feature is missing, and it is ready for \/work."/"summary": "The plan now checks every 15 minutes as you asked, and every new test fails today because the feature is missing; it is ready for \/work."/' /tmp/dokima-out/review.json; sed -i 's/, and every new test fails today because the feature is missing; it is ready/; every new test fails today for the missing feature; ready/' /tmp/dokima-out/review.json; grep summary /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 313 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> "summary": "The plan now checks every 15 minutes as you asked; every new test fails today for the missing feature; ready for /work.",
> rc=0

**Agent:** I approved the plan for #313. It now checks the tree every 15 minutes, as the owner asked in their last comment ("Check every 15 minutes."), and it has no questions left for them.

- **Every ask is covered.** The issue's asks and both owner comments each match a criterion, and none is missing.
- **The new tests fail today because the feature isn't built.** All 9 tests in `tests/test_blocked_plans.py` fail with their own criterion message, none from a crash or a bad path. In the full suite, 16 tests fail and 705 pass. The other 7 failures are the existing tests the plan lists as changed, and each now expects the blocked story to start planning.
- **The schedule test is strict both ways.** It requires a workflow that runs every 15 minutes and fails if any workflow runs more often. I checked how it reads schedules: every-15-minute schedules like `*/15` or `0,15,30,45` count, while `*/5` counts as too often.
- **No earlier blockers:** none were open.

I added two notes, neither blocking:
- The card at the top of the issue still says "every 5 minutes"; it should show 15 when it's next redrawn.
- When someone uses GitHub's "create sub-issue" button, the issue may open before GitHub links it to its parent. If so, it starts planning at the next 15-minute check instead of the moment it opens.

The hand-back is in `/tmp/dokima-out/review.json` and passes both checks. Next step: the owner says `/work`.
