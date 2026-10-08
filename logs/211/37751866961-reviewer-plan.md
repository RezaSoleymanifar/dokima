# reviewer (plan) for #211

Run: https://github.com/dokima-dev/dokima/actions/runs/37751866961

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (123.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/bb9b0274-5a90-4f00-9071-0f059e2e2343/tool-results/btedifuvc.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-worker.json
> 06-reviewer-pr.json
> 07-planner.json
> 08-reviewer-plan.json
> 09-worker.json
> 10-reviewer-pr.json
> 11-planner.json
> 12-reviewer-plan.json
> 13-planner.json
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
> 
> <!-- dokima-card -->
> ### No checks yet
> [PR #220](https://github.com/dokima-dev/dokima/pull/220) · [files changed](https://github.com/dokima-dev/dokima/pull/220/files)
> 
> **User story:** On autopilot an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`; a planner's question stops only when the plan reviewer cannot match its assumption to the owner's own words; and the river still stops and mentions the owner wherever the owner must decide.
> 
> **Acceptance criteria**
> 
> <table>
> <tr><td><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"></td><td>On an issue on autopilot, a plan review that approves starts the worker by itself, and so does `/autopilot start` said on an issue whose pl

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json; cat open_blockers.json; sed -n '/dokima-card-end\|<!-- dokima-ask/,$p' issue.md | head -400
```

> 117642 issue.md
>   8529 plan.json
>      2 open_blockers.json
> 126173 total
> []<!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 3</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`, and the river still stops and mentions the owner wherever the owner must decide.
> 
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, three blocks in a row (rounds=3), a rejected hand-back and a run that failed or never started; board_place puts Needs you on every stop. 'Silent failures' in the issue reads as a run that failed or never started. The owner confirmed `/autopilot start` picks up what is already waiting, so an approved plan already waiting for `/work` starts too. The owner asked (comment of 2026-10-08 06:29) that wherever they would have typed a command, autopilot posts one short line in its place, like 

`3. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md; for f in in/*.json; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f'));h=d.get('handback',d)
print(d.get('run_id'), d.get('started_by'))
for k in ('verdict','summary'): print(k, h.get(k))
for b in h.get('blockers',[]): print(' ',b['id'],b['criterion'],b['problem'][:300])
print(' resolved',h.get('resolved'))
print(' check', d.get('check'))
"; done
```

> 4:### No checks yet
> 75:### RezaSoleymanifar on issue #211 (2026-10-08T06:56:48Z)
> 79:### RezaSoleymanifar on issue #211 (2026-10-08T06:58:15Z)
> 83:### dokima-runtime on issue #211 (2026-10-08T06:58:34Z)
> 214:### dokima-runtime on issue #211 (2026-10-08T07:13:24Z)
> 360:### dokima-runtime on issue #211 (2026-10-08T07:15:50Z)
> 508:### dokima-runtime on issue #211 (2026-10-08T07:21:58Z)
> 636:### RezaSoleymanifar on issue #211 (2026-10-08T07:27:05Z)
> 640:### dokima-runtime on issue #211 (2026-10-08T07:27:24Z)
> 702:### dokima-runtime on PR #220 (2026-10-08T07:44:08Z)
> 802:### dokima-runtime on issue #211 (2026-10-08T07:50:02Z)
> 947:### dokima-runtime on issue #211 (2026-10-08T07:55:52Z)
> 1067:### dokima-runtime on PR #220 (2026-10-08T08:03:01Z)
> 1122:### dokima-runtime on PR #220 (2026-10-08T08:07:01Z)
> 1202:### RezaSoleymanifar on issue #211 (2026-10-08T08:25:57Z)
> 1206:### dokima-runtime on issue #211 (2026-10-08T08:26:17Z)
> 1348:### dokima-runtime on issue #211 (2026-10-08T08:34:29Z)
> 1489:### dokima-runtime on PR #220 (2026-10-08T08:42:11Z)
> 1493:### RezaSoleymanifar on issue #211 (2026-10-08T08:42:14Z)
> 1497:### dokima-runtime on issue #211 (2026-10-08T08:42:34Z)
> 1635:### dokima-runtime on issue #211 (2026-10-08T08:44:37Z)
> == in/01-planner.json
> 37740603828 RezaSoleymanifar
> verdict None
> summary None
>  resolved None
>  check {'passed': True, 'problems': []}
> == in/02-reviewer-plan.json
> 37742116998 dokima-runtime[bot]
> verdict block
> summary The plan drops the owner's rule that an assumption which chang

`4. Bash`
```
cd /tmp/pack; sed -n 636,640p issue.md; sed -n 1202,1206p issue.md; sed -n 1489,1500p issue.md; sed -n 1635,1700p issue.md; python3 -c "
import json;d=json.load(open('in/12-reviewer-plan.json'));print(json.dumps(d['handback'],indent=1))"
```

> ### RezaSoleymanifar on issue #211 (2026-10-08T07:27:05Z)
> 
> /work
> 
> ### dokima-runtime on issue #211 (2026-10-08T07:27:24Z)
> ### RezaSoleymanifar on issue #211 (2026-10-08T08:25:57Z)
> 
> /plan The PR clashes with main after #213 merged. Re-plan on top of today's main.
> 
> ### dokima-runtime on issue #211 (2026-10-08T08:26:17Z)
> ### dokima-runtime on PR #220 (2026-10-08T08:42:11Z)
> 
> Replaced: this branch conflicts with main after #213 merged. Re-planning #211 from fresh main, as done for #154.
> 
> ### RezaSoleymanifar on issue #211 (2026-10-08T08:42:14Z)
> 
> /plan Fresh start on today's main: the old branch is deleted because it conflicted after #213 merged.
> 
> ### dokima-runtime on issue #211 (2026-10-08T08:42:34Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**
> ### dokima-runtime on issue #211 (2026-10-08T08:44:37Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> **Reviewer (plan)** · setting up
> 
> The machine is setting up: the branch, the starting pack and the tools. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37751866961)</sub>
> 
> {
>  "previous_step": {
>   "did": [
>    "Re-planned on today's main: 211.2 now also promises that, as `/work` on autopilot do

**Agent:** Now the newest planner record and the plan.

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/13-planner.json'));h=d['handback'];print(json.dumps({k:h[k] for k in h if k not in ('acceptance_criteria',)},indent=1))"; diff <(python3 -c "import json;print(json.dumps(json.load(open('in/11-planner.json'))['handback'],indent=1))") <(python3 -c "import json;print(json.dumps(json.load(open('in/13-planner.json'))['handback'],indent=1))"); diff <(python3 -c "import json;print(json.dumps(json.load(open('in/13-planner.json'))['handback'],indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1,sort_keys=True))") && echo SAME
```

> {
>  "kind": "user_story",
>  "user_story": "On autopilot an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`; a planner's question stops only when the plan reviewer cannot match its assumption to the owner's own words; and the river still stops and mentions the owner wherever the owner must decide.",
>  "non_functional": [
>   {
>    "text": "When GitHub cannot say whether the issue is on autopilot, the river stops for the owner, starts nothing, and the card's Next line says autopilot could not be read.",
>    "why": "A guess either way would start work the owner did not switch on, or stall it silently.",
>    "principle": "Fail closed."
>   }
>  ],
>  "scope": [
>   "dokima/agent.py",
>   "dokima/roles/reviewer.md",
>   ".github/workflows/agent.yml",
>   ".github/workflows/commands.yml",
>   "AGENTS.md"
>  ],
>  "out_of_scope": [
>   "Starting the next sibling story when a story merges, and closing a finished tree; #213 (merged in #218) already does that.",
>   "Autopilot lines for anything other than an approved plan or an approved split.",
>   "Changing how the planner writes its questions; only the plan reviewer and the river change."
>  ],
>  "tests": {
>   "211.1": [
>    "tests/test_autopilot_river.py::test_on_autopilot_an_approved_plan_starts_the_worker_with_one_autopilot_line",
>    "tests/test_autopilot_river.py::test_autopilot_start_starts_the_worker_on_a_plan_already_waiting_for_work"
>   ],
>   "211.2": [
>    "tests/te

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -1; git log --oneline -3 origin/main; git diff --stat origin/main...HEAD; git diff origin/main HEAD --stat; python3 -c "import json;[print(c['text']) for c in json.load(open('/tmp/pack/plan.json'))['acceptance_criteria']]"
```

> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> 4cccffe Live card: minutes and the current step while the agent works (#216)
>  tests/test_autopilot_river.py | 545 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py           |   2 +
>  2 files changed, 547 insertions(+)
>  tests/test_autopilot_river.py | 545 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py           |   2 +
>  2 files changed, 547 insertions(+)
> On an issue on autopilot, a plan review that approves starts the worker by itself, and so does `/autopilot start` said on an issue whose plan is already approved and waiting for `/work`. The issue gets exactly one comment reading `Autopilot: plan approved, starting work`, the review's card ends "Next: The worker starts now." with no Needs you, and no comment says no stage was started. A plan already handed to the worker, by autopilot or by the owner's `/work`, is not started again, and a code review's approval still stops for the owner.
> On an issue on autopilot, an approved split files its stories as sub-issues by itself, as `/work` would, and so does `/autopilot start` said on an issue whose split is approved and not yet filed. The issue gets one Split filed record and exactly one comment reading `Autopilot: split approved, filing its stories`, and no worker starts. As `/work` on autopilot doe

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed|^E  " | head -60
```

> assert r.agent_started() and not r.failed, f"211.1: setup: the plan review did not run:\n{r.tail()}"
> E       AssertionError: 211.1: the approved plan on autopilot did not start exactly one worker for #57: []
> E       assert [] == [('worker', '57')]
> E         
> E         Right contains one more item: ('worker', '57')
> E         
> E         Full diff:
> E         + []
> E         - [
> E         -     (
> E         -         'worker',
> E         -         '57',
> E         -     ),
> E         - ]
>         assert not m.failed, f"211.1: the listener failed on /autopilot start:\n{m.tail()}"
> E       AssertionError: 211.1: /autopilot start did not start exactly one worker for #57: []
> E       assert [] == [('worker', '57')]
> E         
> E         Right contains one more item: ('worker', '57')
> E         
> E         Full diff:
> E         + []
> E         - [
> E         -     (
> E         -         'worker',
> E         -         '57',
> E         -     ),
> E         - ]
> E       AssertionError: 211.2: the approved split on autopilot filed 0 issues, not its 2 stories
> E       assert 0 == 2
> E        +  where 0 = len([])
> E        +    where [] = created_issues()
> E        +      where created_issues = <test_start.Run object at 0x7fe9046ff230>.created_issues
> E       AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
> E       assert [] == [('worker', '57')]
> E         
> E         Right contains one more item: ('worker', '57')
> E         
> E         Full diff:
> E         + []
> E         - [

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^E   +(Assertion|[A-Za-z]+Error)|passed|failed"; timeout 900 python3 -m pytest -q -x --deselect tests/test_autopilot_river.py 2>&1 | tail -3
```

> assert r.agent_started() and not r.failed, f"211.1: setup: the plan review did not run:\n{r.tail()}"
> E       AssertionError: 211.1: the approved plan on autopilot did not start exactly one worker for #57: []
>         assert not m.failed, f"211.1: the listener failed on /autopilot start:\n{m.tail()}"
> E       AssertionError: 211.1: /autopilot start did not start exactly one worker for #57: []
> E       AssertionError: 211.2: the approved split on autopilot filed 0 issues, not its 2 stories
> E       AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
>         """On autopilot the river still stops on an escalation, three blocks in a row, a rejected hand-back and a run that failed or never started.
> E       AssertionError: 211.4: an approving plan review on autopilot did not start the worker: []
>         Decides what follows a passed plan that has two questions for the owner. On autopilot the plan reviewer must start
> E       AssertionError: 211.5: on autopilot a plan with questions did not go to the plan reviewer: 'stop'
> >           assert code != 0, f"211.5 ({case}): the check passed a plan review that does not judge every question properly"
> E           AssertionError: 211.5 (none judged): the check passed a plan review that does not judge every question properly
>         assert r.agent_started() and not r.failed, f"211.5: setup: the plan review did not pass its check:\n{r.tail()}"
> E       AssertionError: 211.5: with every assumption accepted the w

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1200 python3 -m pytest -q --deselect tests/test_autopilot_river.py 2>&1 | grep -E "^FAILED|passed|failed"
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bhzkbtqch). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/bb9b0274-5a90-4f00-9071-0f059e2e2343/tasks/bhzkbtqch.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def test_on_autopilot_an_approved_split" -A80 tests/test_autopilot_river.py; git diff origin/main HEAD -- tests/test_start.py
```

> 286:def test_on_autopilot_an_approved_split_files_its_stories_with_one_autopilot_line(record_property, tmp_path, monkeypatch):
> 287-    """On autopilot, an approved split files its stories as `/work` would, with one "Autopilot: split approved, filing its stories" line.
> 288-
> 289-    Runs the plan review of a split on #57, on autopilot, the reviewer approving: both stories must be filed as issues,
> 290-    the issue must get one "Split filed" record and exactly one comment reading the line, and no worker may start.
> 291-    As `/work` on autopilot does on main (#213), both stories must be filed on autopilot and only the first, which
> 292-    waits on nothing (the second is blocked by it), may start its planner; GitHub numbers them #900 and #901.
> 293-    Then `/autopilot start` on #57 whose split is approved and not yet filed does the same, and on a split already
> 294-    filed it files nothing and posts no line."""
> 295-    record_property("proves", "211.2")
> 296-    r = run(monkeypatch, tmp_path / "river", "reviewer", "plan", ts.SPLIT_PROPOSED, ON)
> 297-    assert r.agent_started(), f"211.2: setup: the plan review of the split did not run:\n{r.tail()}"
> 298-    assert len(r.created_issues()) == 2, f"211.2: the approved split on autopilot filed {len(r.created_issues())} issues, not its 2 stories"
> 299-    assert len(lines(r, LINE_SPLIT)) == 1, \
> 300-        f"211.2: the issue did not get exactly one {LINE_SPLIT!r} comment: {[p['body'][:120] for p in r.posted()]}"
> 301-    assert [x["role"

**Agent:** Still checking the rest of the test suite on this branch; all 11 new tests fail today because the feature is missing.

`11. Bash`
```
sleep 1; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/bb9b0274-5a90-4f00-9071-0f059e2e2343/tasks/bhzkbtqch.output | tail -5
```

> (Bash completed with no output)

`12. Bash`
```
grep -n "def assert_stories_as_work_files_them" -A25 /home/runner/work/dokima/dokima/tests/test_autopilot_river.py
```

> 275:def assert_stories_as_work_files_them(m, case):
> 276-    """The split's stories were filed as `/work` files them on autopilot: each on autopilot, and only the unblocked one planning."""
> 277-    for c in m.created_issues():
> 278-        given = [c[j + 1] for j, x in enumerate(c[:-1]) if x in ("--label", "-l")]
> 279-        assert "autopilot" in [l.strip() for v in given for l in v.split(",")], \
> 280-            f"211.2 ({case}): a story was filed off autopilot, unlike `/work` on autopilot: {c[:6]} labels {given}"
> 281-    planners = sorted(s for s in starts(m) if s[0] == "planner")
> 282-    assert planners == [("planner", "900")], (f"211.2 ({case}): the stories did not start as `/work` on autopilot starts "
> 283-                                              f"them (only #900, which waits on nothing, plans): {planners}")
> 284-
> 285-
> 286-def test_on_autopilot_an_approved_split_files_its_stories_with_one_autopilot_line(record_property, tmp_path, monkeypatch):
> 287-    """On autopilot, an approved split files its stories as `/work` would, with one "Autopilot: split approved, filing its stories" line.
> 288-
> 289-    Runs the plan review of a split on #57, on autopilot, the reviewer approving: both stories must be filed as issues,
> 290-    the issue must get one "Split filed" record and exactly one comment reading the line, and no worker may start.
> 291-    As `/work` on autopilot does on main (#213), both stories must be filed on autopilot and only the first, which
> 292-    waits on nothing 

`13. Bash`
```
until grep -qE "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/bb9b0274-5a90-4f00-9071-0f059e2e2343/tasks/bhzkbtqch.output 2>/dev/null; do sleep 10; done; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/bb9b0274-5a90-4f00-9071-0f059e2e2343/tasks/bhzkbtqch.output
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
> 3 failed, 368 passed, 11 deselected in 162.16s (0:02:42)
> 
> [exited with code 0]

`14. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree add -q /tmp/mainwt origin/main 2>&1; cd /tmp/mainwt && timeout 300 python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -4; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt
```

> +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 11 passed in 1.52s

`15. Bash`
```
env | grep -i -E "dokima|stage" ; cd /home/runner/work/dokima/dokima; env -u DOKIMA_STAGE timeout 300 python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -1
```

> GITHUB_WORKSPACE=/home/runner/work/dokima/dokima
> LOG_URL=https://github.com/dokima-dev/dokima/blob/logs/logs/211/37751866961-reviewer-plan.md
> GITHUB_TRIGGERING_ACTOR=dokima-runtime[bot]
> PWD=/home/runner/work/dokima/dokima
> STAGE=plan
> GITHUB_WORKFLOW_REF=dokima-dev/dokima/.github/workflows/agent.yml@refs/heads/main
> GITHUB_ACTOR=dokima-runtime[bot]
> GITHUB_REPOSITORY=dokima-dev/dokima
> RUNNER_WORKSPACE=/home/runner/work/dokima
> GITHUB_REPOSITORY_OWNER=dokima-dev
> OUT=/tmp/dokima-out
> 3 failed, 11 passed in 2.78s

`16. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE timeout 300 python3 -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -1
```

> 14 passed in 7.66s

**Agent:** Those 3 extra failures come from this machine's own setting, not the plan. Checking that the 11 new tests still fail the same way without it.

`17. Bash`
```
cd /home/runner/work/dokima/dokima; env -u STAGE timeout 600 python3 -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^E +AssertionError|passed|failed" | cut -c1-160
```

> assert r.agent_started() and not r.failed, f"211.1: setup: the plan review did not run:\n{r.tail()}"
> E       AssertionError: 211.1: the approved plan on autopilot did not start exactly one worker for #57: []
>         assert not m.failed, f"211.1: the listener failed on /autopilot start:\n{m.tail()}"
> E       AssertionError: 211.1: /autopilot start did not start exactly one worker for #57: []
> E       AssertionError: 211.2: the approved split on autopilot filed 0 issues, not its 2 stories
> E       AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
>         """On autopilot the river still stops on an escalation, three blocks in a row, a rejected hand-back and a run that failed or never started.
> E       AssertionError: 211.4: an approving plan review on autopilot did not start the worker: []
>         Decides what follows a passed plan that has two questions for the owner. On autopilot the plan reviewer must start
> E       AssertionError: 211.5: on autopilot a plan with questions did not go to the plan reviewer: 'stop'
> >           assert code != 0, f"211.5 ({case}): the check passed a plan review that does not judge every question properly"
> E           AssertionError: 211.5 (none judged): the check passed a plan review that does not judge every question properly
>         assert r.agent_started() and not r.failed, f"211.5: setup: the plan review did not pass its check:\n{r.tail()}"
> E       AssertionError: 211.5: with every assumption accepted the w

**Agent:** All 11 fail today because the feature is missing. Writing the review.

`18. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
prev=json.load(open('in/12-reviewer-plan.json'))['handback']
asks=prev['asks']+[{"ask":"Fresh start on today's main: the old branch is deleted because it conflicted after #213 merged.","source":"https://github.com/dokima-dev/dokima/issues/211","criterion":"211.2"}]
r={"previous_step":{
 "did":["Re-planned #211 from today's main after the old branch was deleted; the branch now holds only the tests, with no clash with main.",
        "Kept the six criteria, the scope and the eleven tests from the plan approved last round, and dropped the concern about the branch clashing with main."],
 "decided":["As before, 211.2 promises that an autopilot split files every story on autopilot and starts only the stories with nothing to wait for, as `/work` on autopilot does since #213."],
 "open":["Six criteria, one over the split limit, kept as one story because #211 is already a story of #205."]},
 "verdict":"approve",
 "summary":"The plan is unchanged from the one approved last round and now sits on a fresh branch from today's main with no clash; all 11 new tests fail today because the feature is missing.",
 "blockers":[],
 "notes":[
  {"text":"The branch is now main plus only this plan's tests, so the worker's run can merge main and start.","evidence":"git diff --stat origin/main...HEAD (f1b30ab): tests/test_autopilot_river.py +545, tests/test_start.py +2; no other file."},
  {"text":"Every new test fails today for the right reason, each naming its criterion and the missing behaviour; the rest of the suite passes.","evidence":"pytest -q tests/test_autopilot_river.py: 11 failed (e.g. '211.1: the approved plan on autopilot did not start exactly one worker for #57: []', '211.2: the approved split on autopilot filed 0 issues, not its 2 stories'). Rest of suite: 371 passed once this machine's own STAGE variable is unset; with it set, 3 tests in test_fixer.py and test_handback_check.py fail the same way on main."},
 
```

> rc=0

**Agent:** I approved the plan for #211, and the hand-back is in `/tmp/dokima-out/review.json`. Both required hand-back checks pass.

- **The plan:** it's the same as the one approved last round. The only difference is that the planner dropped its warning about the branch clashing with main, since that branch was deleted.
- **The branch:** it's now today's main plus only the plan's tests (`tests/test_autopilot_river.py` and two lines in `tests/test_start.py`). The worker's run should no longer stop on a clash with main.
- **Tests:** all 11 new tests fail today because the feature isn't built yet. Each failure names its criterion, for example "211.1: the approved plan on autopilot did not start exactly one worker for #57". The rest of the suite passes: 371 tests.
- **Three other failures:** on my first run, 3 tests in `test_fixer.py` and `test_handback_check.py` also failed, and they fail the same way on main. The cause was a `STAGE` setting on the machine I ran on. With it unset, they pass, so they say nothing about this plan.
- **Your asks:** every ask in the issue and your comments maps to a criterion, including your latest "Fresh start on today's main".
- **Before `/work`:** the plan changes `.github/workflows/agent.yml`, `.github/workflows/commands.yml` and `dokima/roles/reviewer.md`. AGENTS.md allows that only when the issue asks. The planner explains why in its concerns, so saying `/work` also approves those changes.
- **Waits for you:** one criterion (211.2) changed in the round before this one, so the worker won't start on its own. It waits for your `/work`.
