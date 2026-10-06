# reviewer (plan) for #139

Run: https://github.com/dokima-dev/dokima/actions/runs/37539760996

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (77.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fa731eb7-b2da-4d25-a297-bdb232a1fc2a/tool-results/bph22n21w.txt
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
> 05-planner.json
> # Issue #139: Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> - [ ] Objective: When the planner hands back a plan, code alone decides from plan.json whether it can be posted, and a rejection says exactly why on the issue.
>   - [ ] Acceptance criteria: A criterion whose source link points at another issue, another repo or anything other than this issue or one of its comments is rejected, and the reason names the source.
>     Verified by: `tests/test_plan_check.py::test_a_source_must_point_at_this_issue`, `tests/test_plan_check.py::test_the_issue_and_its_comments_are_valid_sources`
>   - [ ] Acceptance criteria: A test the plan names that is not in the repo, or that is filed under a criterion this plan does not have, is rejected, and the reason names the test or the criterion.
>     Verified by: `tests/test_plan_check.py::test_every_named_test_must_exist_and_prove_a_criterion_of_this_plan`
>   - [ ] Acceptance criteria: A new test whose docstring is missing, or whose first line is not one plain sentence, is rejected, and the reason names the test.
>     Verified by: `tests/test_plan_check.py::test_a_new_test

`2. Bash`
```
cd /tmp/pack; wc -c issue.md in/* plan.json open_blockers.json; cat open_blockers.json
```

> 62409 issue.md
>  12779 in/01-planner.json
>   1908 in/02-reviewer-plan.json
>  16003 in/03-planner.json
>   2105 in/04-reviewer-plan.json
>  17345 in/05-planner.json
>  16605 plan.json
>      2 open_blockers.json
> 129156 total
> []
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; cat issue.md | head -c 30000
```

> <persisted-output>
> Output too large (29.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fa731eb7-b2da-4d25-a297-bdb232a1fc2a/tool-results/toolu_01M9H4XCC8jq1PBbYTfvSsJ5.txt
> 
> Preview (first 2KB):
> # Issue #139: Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> - [ ] Objective: When the planner hands back a plan, code alone decides from plan.json whether it can be posted, and a rejection says exactly why on the issue.
>   - [ ] Acceptance criteria: A criterion whose source link points at another issue, another repo or anything other than this issue or one of its comments is rejected, and the reason names the source.
>     Verified by: `tests/test_plan_check.py::test_a_source_must_point_at_this_issue`, `tests/test_plan_check.py::test_the_issue_and_its_comments_are_valid_sources`
>   - [ ] Acceptance criteria: A test the plan names that is not in the repo, or that is filed under a criterion this plan does not have, is rejected, and the reason names the test or the criterion.
>     Verified by: `tests/test_plan_check.py::test_every_named_test_must_exist_and_prove_a_criterion_of_this_plan`
>   - [ ] Acceptance criteria: A new test whose docstring is missing, or whose first line is not one plain sentence, is rejected, and the reason names the test.
>     Verified by: `tests/test_plan_check.py::test_a_new_test_needs_a_one_sentence_docstring`
>   - [ ] Acceptance criteria: A new test that passes on today's code, or cannot run at all

`4. Read`
```
/tmp/pack/issue.md
```

> 1	# Issue #139: Agent hand-backs: one deterministic checker that reads only the JSON files
> 2	
> 3	- [ ] Objective: When the planner hands back a plan, code alone decides from plan.json whether it can be posted, and a rejection says exactly why on the issue.
> 4	  - [ ] Acceptance criteria: A criterion whose source link points at another issue, another repo or anything other than this issue or one of its comments is rejected, and the reason names the source.
> 5	    Verified by: `tests/test_plan_check.py::test_a_source_must_point_at_this_issue`, `tests/test_plan_check.py::test_the_issue_and_its_comments_are_valid_sources`
> 6	  - [ ] Acceptance criteria: A test the plan names that is not in the repo, or that is filed under a criterion this plan does not have, is rejected, and the reason names the test or the criterion.
> 7	    Verified by: `tests/test_plan_check.py::test_every_named_test_must_exist_and_prove_a_criterion_of_this_plan`
> 8	  - [ ] Acceptance criteria: A new test whose docstring is missing, or whose first line is not one plain sentence, is rejected, and the reason names the test.
> 9	    Verified by: `tests/test_plan_check.py::test_a_new_test_needs_a_one_sentence_docstring`
> 10	  - [ ] Acceptance criteria: A new test that passes on today's code, or cannot run at all, is rejected, and the reason names the test and says which.
> 11	    Verified by: `tests/test_plan_check.py::test_a_new_test_must_fail_on_todays_code`
> 12	  - [ ] Acceptance criteria: A renamed older test counts as a c

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('plan.json')); b=json.load(open('in/05-planner.json'))
print(b.keys()); print(a==b.get('handback')); print(json.dumps(b.get('check'),indent=1)); print(b.get('run_id'))
"; cat in/04-reviewer-plan.json | head -50; ls /home/runner/work/dokima/dokima/.dokima/139/ 2>/dev/null; git -C /home/runner/work/dokima/dokima log --oneline -3 --stat
```

> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> True
> {
>  "passed": true,
>  "problems": []
> }
> 37539173410
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37523877217",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37523877217",
>  "handback": {
>   "stage": "plan",
>   "round": 2,
>   "verdict": "approve",
>   "summary": "The revised split now carries all three of your answers: real hand-backs kept as test samples (story 5), a test that fails because the code is missing counts as failing (story 2), and every blocker names a criterion while the reviewer lists your asks in a new review.json field the checker requires (stories 4 and 5); every ask is owned by exactly one story or shown to be already built.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "All three notes from round 1 are taken up: a blocker in a review of a split names a story's criterion as S<s>.<k> (story 3 context, story 4 criterion 3); changed and deleted older tests stay covered by the existing check (story 2 context); and 'one plain sentence' now accepts an ending in '.', '?' or '!' (story 2 criterion 1).",
>     "evidence": "plan.json stories[1].context and acceptance_criteria[0]; stories[2].context; stories[3].acceptance_criteria[2]"
>    },
>    {
>     "text": "Story 5 waits for stories 1 to 4, but only its last criterion (real hand-backs as samples) needs the

**Agent:** Reading the plan record is done; now checking the repo for how question-only hand-backs and the reviewer's skip work today, to judge the owner's "one flow" comment.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -i "question" .github/workflows/*.yml dokima/*.py | head -60; git status --short; git diff main --stat | tail -3
```

> .github/workflows/planner.yml:5:# or one question for the owner. Only a code owner's label counts. The planner
> .github/workflows/planner.yml:86:          for f in /tmp/dokima-out/plan.json /tmp/dokima-out/question.md; do
> .github/workflows/planner.yml:115:      - name: Write the plan into the issue, or post the question
> dokima/board.py:14:YOUR_TURN = ("Plan written above", "**Planner question**", "**Plan rejected:**")
> dokima/agent.py:125:def problems_questions(qs):
> dokima/agent.py:126:    """Everything wrong with the planner's questions for the owner: a list of plain questions, each asking something ('?')."""
> dokima/agent.py:128:        return ["questions must be a list of plain questions"]
> dokima/agent.py:129:    return [f"question {i} must be a plain question with a '?'" for i, q in enumerate(qs, 1)
> dokima/agent.py:163:    if "questions" in r:
> dokima/agent.py:183:    if "questions" in w:
> dokima/planner.py:3:    python3 -m dokima.planner check N OUT   # fail loudly unless OUT holds a well-formed plan or question
> dokima/planner.py:4:    python3 -m dokima.planner post N OUT    # write the plan into issue N, or post the question
> dokima/planner.py:12:  question.md  one question for the owner, ending in "?"
> dokima/planner.py:22:from dokima.agent import problems_questions  # noqa: E402
> dokima/planner.py:33:    """('plan', dict) or ('question', str); Garbled if OUT holds anything else."""
> dokima/planner.py:35:    has_q = os.path.exists(os.path.join(out, "question.md"))
> dokima/planne

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main...HEAD --stat; grep -n -i "question\|review" .github/workflows/planner.yml | head -30; ls .github/workflows
```

> .dokima/139/01-planner.json       | 170 ++++++++++++++++++++++++++++++++
>  .dokima/139/02-reviewer-plan.json |  38 +++++++
>  .dokima/139/03-planner.json       | 201 ++++++++++++++++++++++++++++++++++++++
>  .dokima/139/04-reviewer-plan.json |  38 +++++++
>  4 files changed, 447 insertions(+)
> 5:# or one question for the owner. Only a code owner's label counts. The planner
> 86:          for f in /tmp/dokima-out/plan.json /tmp/dokima-out/question.md; do
> 115:      - name: Write the plan into the issue, or post the question
> agent.yml
> assign.yml
> board.yml
> card.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> wiki.yml
> worker.yml

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p .github/workflows/agent.yml; grep -n "reviewer\|question\|kind" .github/workflows/planner.yml dokima/runtime*.py dokima/*.py 2>/dev/null | grep -v "^dokima/agent.py:1[0-9][0-9]" | head -40
```

> name: agent
> run-name: "${{ inputs.role }}${{ inputs.role == 'reviewer' && format(' ({0})', inputs.stage) || '' }} for #${{ inputs.issue }}"
> # Runs one agent on a fresh GitHub machine: the components of Dokima's flow, before the pipeline wires them.
> # Everything the agent needs is gathered by code: the issue with every comment, and every earlier record in
> # .dokima/N/ on try/issue-N. The agent runs its own deterministic check before it finishes; code runs it again,
> # then writes this run's record (hand-back, check verdict, run, models) into .dokima/N/ and pushes it. Records never
> # expire: they are the data the cards will be drawn from. Session logs stay on the run page.
> on:
>   workflow_dispatch:
>     inputs:
>       role:
>         description: Which agent
>         type: choice
>         options: [planner, reviewer, worker]
>       stage:
>         description: For the reviewer, what it grades
>         type: choice
>         options: [plan, pr]
>         default: plan
>       issue:
>         description: Issue number
>         required: true
> concurrency:
>   group: agent-${{ inputs.issue }}
>   cancel-in-progress: false
> permissions:
>   contents: read
>   issues: read
>   actions: read
> jobs:
>   run:
>     environment: keys
>     runs-on: ubuntu-24.04
>     env:
>       N: ${{ inputs.issue }}
>       ROLE: ${{ inputs.role }}
>       STAGE: ${{ inputs.role == 'reviewer' && inputs.stage || '' }}
>       GH_TOKEN: ${{ github.token }}
>       PACK: /tmp/pack
>       OUT: /tmp/dokima-out
>       MODEL: claude-opus-5-5
>     steps:
>      

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Kept the five-story split and took up the owner's 'one flow only' comment: story 1 now rejects a plan of kind question, and story 3 no longer checks questions."],
  "decided": ["A planner hand-back is always a plan (one story or a split) with its questions listed inside; a question.md, a plan.json with no kind or a plan of kind question is rejected.",
              "Removing the question kind also changes the planner's prompt and the planner workflow, which waits for the owner's approval."],
  "open": ["Asked whether a missing ask alone stops the plan; the owner has since answered yes, which matches story 5's third criterion as written."]},
 "stage": "plan",
 "round": 3,
 "verdict": "approve",
 "summary": "The split now follows your 'one flow only' comment (the question kind goes away in story 1 and story 3 drops its question checks), and your latest answer that a missing ask alone stops the plan is already story 5's third criterion.",
 "blockers": [],
 "notes": [
  {"text": "Your words 'the reviewer always reviews' and 'the questions wait for me at approval' get no criterion of their own; they follow from story 1 (every hand-back is now a plan the reviewer can grade, with its questions inside it) and from the planner's comment, which already lists 'Questions for you'. Nothing is dropped, but nothing tests it beyond story 1.",
   "evidence": "issue #139, comment of 2026-10-06T20:49:48Z; plan.json stories[0].acceptance_criteria[0]; dokima/planner.py lines 74-82 and 268-269 hold the question path story 1 removes"},
  {"text": "Story 5's open question is now answered (comment of 2026-10-06T22:18:39Z: a missing ask alone stops the plan). Its child planner should cite that comment as the source of story 5's third criterion and drop the question.",
   "evidence": "plan.json questions[0]; stories[4].acceptance_criteria[2]"},
  {"text": "dokima/board.py still marks '**Planner 
```

> 0

**Agent:** I approved the plan for issue #139 (round 3) with no blockers. The hand-back is in `/tmp/dokima-out/review.json`, and both required checks on it pass.

**What the planner changed:** it kept the five-story split and applied your "one flow only" comment:
- Story 1 now rejects any hand-back that isn't a plan. That covers a `question.md`, a `plan.json` with no kind, and a plan of kind question.
- Story 3 no longer checks questions.

Your latest answer, that a missing ask alone stops the plan, already matches story 5's third criterion as written.

Because this plan is a split, the tests come later, when each story gets its own plan. There were no new tests to run this round, and no earlier blockers were open.

**Notes in the review (not blocking):**
1. You wrote "the reviewer always reviews" and "the questions wait for me at approval". Neither has its own criterion. Both follow from story 1 and from how the planner's comment already lists "Questions for you", so nothing is dropped. But nothing beyond story 1 tests them.
2. Your 22:18 comment answers story 5's open question. Its planner should cite that comment as the source and drop the question.
3. `dokima/board.py` (line 14) still treats "**Planner question**" comments as waiting on you. Story 1 removes those comments, so its plan should probably include `board.py` in scope.

Removing the question kind also means editing the planner's prompt and `planner.yml`. That workflow change waits for your approval, as the planner flagged.
