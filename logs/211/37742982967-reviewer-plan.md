# reviewer (plan) for #211

Run: https://github.com/dokima-dev/dokima/actions/runs/37742982967

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (46.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a2343899-e96b-4a79-88fd-494beb6478df/tool-results/bdkdso8h2.txt
> 
> Preview (first 2KB):
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
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
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, three blocks in a row (rounds=3), a rejected hand-back and a run that failed or never started; board_place puts Needs you on every stop. 'Silent failures' in the issue reads as a run that failed or never started. The owner confirmed `/autopilot start` picks up what is already waiting, so an app

`2. Bash`
```
cd /tmp/pack; cat issue.md; ls in
```

> <persisted-output>
> Output too large (34.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a2343899-e96b-4a79-88fd-494beb6478df/tool-results/bb3q8ddfz.txt
> 
> Preview (first 2KB):
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
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
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, three blocks in a row (rounds=3), a rejected hand-back and a run that failed or never started; board_place puts Needs you on every stop. 'Silent failures' in the issue reads as a run that failed or never started. The owner confirmed `/autopilot start` picks up what is already waiting, so an app

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; cat plan.json
```

> [
>  {
>   "id": "B1",
>   "criterion": "211.5",
>   "test": "tests/test_autopilot_river.py::test_on_autopilot_an_accepted_assumption_goes_on_and_one_not_accepted_stops",
>   "problem": "The owner said an assumption that changes how the system works or what it costs stops for them. 211.5 only says the reviewer accepts an assumption when it has the owner's words; nothing in the criterion or its tests says an assumption that changes how the system works or what it costs is never accepted. The test even requires the opposite: it accepts the assumption that the board gets a cost column priced per run and expects the worker to start.",
>   "evidence": "Owner's comment on #211 (2026-10-08T06:56:48Z): 'If it changes how the system works, what it costs, or isn't backed by my words, it stops for me.' tests/test_autopilot_river.py:35-36 (question 'Should the board show a cost column?', assumption 'priced per run') and :46-47, :426-430 (ACCEPT_2 accepted, worker must start). The only check on the reviewer's prompt (:413-415) looks for the words 'assumptions' and 'matched'.",
>   "fix": "Add the owner's rule to 211.5: an assumption that changes how the system works or what it costs is never accepted. Make it observable, e.g. each judgement says whether it changes how the system works or what it costs, code rejects an accepted one that does, and the river stops on it; test both ways (accepted with no change goes on, accepted with a cost change is rejected or stops). Use a question that does not change 

`4. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500 | head -c 34000 | tail -c 30000
```

> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
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
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, three blocks in a row (rounds=3), a rejected hand-back and a run that failed or never started; board_place puts Needs you on every stop. 'Silent failures' in the issue reads as a run that failed or never started. The owner confirmed `/autopilot start` picks up what is already waiting, so an approved plan already waiting for `/work` starts too. The owner asked (comment of 2026-10-08 06:29) that wherever they would have typed a command, autopilot posts one short line in its place, like 'Autopilot: plan appro

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat 3ad0991 HEAD; wc -l tests/test_autopilot_river.py; git diff 3ad0991 HEAD -- tests/ | head -400
```

> tests/test_autopilot_river.py | 95 +++++++++++++++++++++++++++++++++++--------
>  1 file changed, 78 insertions(+), 17 deletions(-)
> 530 tests/test_autopilot_river.py
> diff --git a/tests/test_autopilot_river.py b/tests/test_autopilot_river.py
> index 24b7f8c..1b7d864 100644
> --- a/tests/test_autopilot_river.py
> +++ b/tests/test_autopilot_river.py
> @@ -32,8 +32,8 @@ ISSUE = "https://github.com/o/r/issues/57"
>  
>  QUESTIONS = [{"question": "Should a failed run move its card to Needs you?",
>                "assumption": "It does, so the owner sees it without looking."},
> -             {"question": "Should the board show a cost column?",
> -              "assumption": "It does, priced per run."}]
> +             {"question": "Should the card name the step that failed?",
> +              "assumption": "It does, so the owner sees where it broke."}]
>  STORY_Q = {**ts.STORY, "questions": QUESTIONS}
>  APPROVE = {**ts.APPROVE, "previous_step": {"did": ["Planned one story."], "decided": [], "open": []},
>             "summary": "Every ask has a criterion and every criterion a test that breaks on any deviation.",
> @@ -41,16 +41,21 @@ APPROVE = {**ts.APPROVE, "previous_step": {"did": ["Planned one story."], "decid
>  BLOCK = {**APPROVE, "verdict": "block", "summary": "The test for 57.1 proves nothing.",
>           "blockers": [{"id": "B1", "criterion": "57.1", "problem": "The test passes against a stub.",
>                         "evidence": "tests/test_x.py::test_a", "fix": "Run the real thing.", "test": None, "fix

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | cut -c1-400 | head -60
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
> E        +      where created_issues = <test_start.Run object at 0x7f60f538d850>.created_issues
> E       AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
> E       assert [] == [('worker', '57')]
> E         
> E         Right contains one more item: ('worker', '57')
> E         
> E         Full diff:
> E         + []
> E         - [

**Agent:** Running the plan's tests; checking each new test fails for the right reason.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^E  +[A-Za-z]*Error|^FAILED|passed|failed" | cut -c1-300
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

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added to 211.5 the owner's rule that an assumption which changes how the system works or what it costs is never accepted: each judgement says so, and code rejects an accepted one that does.",
          "Added a check that the owner's matched words appear word for word in the source named, from the issue's text, a code owner's comment on the issue or AGENTS.md, and a test that the river stops otherwise.",
          "Replaced the cost-column question in the tests with one that changes nothing, backed by a real owner comment."],
  "decided": ["A matched word found only in a comment by someone who is not a code owner, the bot included, counts as not accepted."],
  "open": ["Six criteria, one over the split limit, kept as one story because #211 is already a story of #205."]},
 "verdict": "approve",
 "summary": "Both earlier blockers are fixed: an assumption that changes how the system works or what it costs is never accepted, and code checks the owner really said the matched words where the review says; every ask has a criterion and all eleven tests fail today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "The plan changes .github/workflows/agent.yml, .github/workflows/commands.yml and dokima/roles/reviewer.md, which AGENTS.md allows only when the issue asks. The issue names commands.yml and the owner's comment asks the plan reviewer to judge assumptions, and the planner says why in its concerns, so the owner should confirm this when saying /work.",
   "evidence": "AGENTS.md 'Working in this repo'; plan.json scope and first concern."},
  {"text": "211.3 says 'even when its parent is' on autopilot, but the fake GitHub's tree is not shown to link #57 under #50, so the test may not prove that a parent's label is ignored.",
   "evidence": "tests/test_autopilot_river.py off = {50: ['autopilot'], 57: ['bug']}."}
 ],
 "outside_plan": [],
 "resolved": ["
```

> 0

**Agent:** I approved the plan for #211. Both blockers from my last review are fixed, and the hand-back passed both code checks.

- **B1 (fixed):** The owner said an assumption that changes how the system works or what it costs must stop for them. The plan now has this rule. Each judgement says whether the assumption changes either one, and code rejects an approval that accepts one that does. The test that accepted a priced cost column now uses a question about naming the failed step, which changes nothing. A new case checks that an assumption accepted even though it changes things is rejected and the river stops.
- **B2 (fixed):** Code now checks that the owner's matched words appear word for word in the place the review names: the issue's text, a code owner's comment on the issue, or AGENTS.md. The river goes on when the words are in the owner's comment, in AGENTS.md or in the issue text. It stops and names the question when:
  - the words are not in the comment the review names;
  - the comment is a stranger's or the bot's;
  - the comment does not exist;
  - the words are not in the issue text or not in AGENTS.md.

  A source on another issue is also rejected.

All 11 tests in `tests/test_autopilot_river.py` fail today, each because the feature is missing (no worker starts, nothing is filed, no check exists yet). None fail on a crash or a bad setup. The owner made no new comments since my last review. All eight of their asks map to a criterion, and the last one ("If it changes how the system works, what it costs…") now maps to 211.5.

I left two notes, not blockers:
- **Protected files:** the plan changes `.github/workflows/agent.yml`, `.github/workflows/commands.yml` and `dokima/roles/reviewer.md`. AGENTS.md allows that only when the issue asks, so the owner should confirm it when saying `/work`.
- **Parent on autopilot:** criterion 211.3 says an issue off autopilot stops even when its parent is on autopilot. The test's fake GitHub may not actually place #57 under #50, so it may not prove the parent's label is ignored.

The review is in `/tmp/dokima-out/review.json`.
