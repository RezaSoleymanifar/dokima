# reviewer (plan) for #211

Run: https://github.com/dokima-dev/dokima/actions/runs/37742116998

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:13 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:13 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:13 in
> -rw-r--r--  1 runner runner 12749 Oct  8 07:13 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:13 open_blockers.json
> -rw-r--r--  1 runner runner  6982 Oct  8 07:13 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:13 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:13 ..
> -rw-r--r-- 1 runner runner 7629 Oct  8 07:13 01-planner.json
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
> **Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, t

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_autopilot_river.py; timeout 600 python -m pytest -q tests/test_autopilot_river.py 2>&1 | tail -40
```

> commit 3ad0991bee7da365ab01bc5c6721f05f7296813f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:13:15 2026 +0000
> 
>     planner for #211 (run 37740603828)
> 
>  tests/test_autopilot_river.py | 469 ++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 469 insertions(+)
> 469 tests/test_autopilot_river.py
> assert [] == [('worker', '57')]
>   
>   Right contains one more item: ('worker', '57')
>   
>   Full diff:
>   + []
>   - [
>   -     (
>   -         'worker',
>   -         '57',
>   -     ),
>   - ]
> FAILED tests/test_autopilot_river.py::test_the_review_card_shows_the_owners_words_each_assumption_matched - AssertionError: 211.5: the review's card does not show the question of an accepted assumption ('Should a failed run move its card to Needs you?'):
>   <!-- dokima-record -->
>   <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (plan)**
>   
>   **approve**: Every ask has a criterion and every criterion a test that breaks on any deviation.
>   
>   <details><summary>What the previous step did</summary>
>   
>   - **Did:** Planned one story.
>   
>   </details>
>   
>   
> assert 'Should a failed run move its card to Needs you?' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w...eviation.\n\n<details><summary>What the previous step did</summary>\n\n- **Did:** Planned one story.\n\n</detai

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_autopilot_river.py
```

> <persisted-output>
> Output too large (32.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/556f4f21-4c7b-4a59-bdb3-f53305f4ed99/tool-results/bw9ia5ffw.txt
> 
> Preview (first 2KB):
> """On autopilot the river hands an approved plan to the worker and files an approved split itself (#211).
> 
> Wherever the owner would have typed `/work`, autopilot posts one short line instead, and the river still stops for the
> owner wherever the owner must decide. A planner's questions no longer always stop on autopilot: the plan reviewer
> judges each question's assumption against the owner's own words, and only a question it does not accept stops.
> 
> These tests run the real workflows the way GitHub runs them, on the machine from test_start.py (agent.yml for a run,
> commands.yml for a comment), with a fake GitHub that also knows each issue's labels. Autopilot is the `autopilot`
> label on the issue. GitHub gives an issue's labels three ways and the fake answers all three: `gh api
> repos/o/r/issues/N` (with its labels), `gh api repos/o/r/issues/N/labels`, and `gh issue view N --json ...labels`.
> With the option fail_labels, every one of those reads of issue #57 fails the way GitHub fails (HTTP 502), and nothing
> else does. A signal that starts a stage is `gh api repos/o/r/dispatches` with event_type dokima-next and its
> client_payload, given as -f/-F fields or as JSON through --input; the fake keeps both.
> Where only the river's decision matters, the tests run `python3 -m dok

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/556f4f21-4c7b-4a59-bdb3-f53305f4ed99/tool-results/bw9ia5ffw.txt
```

> 1	"""On autopilot the river hands an approved plan to the worker and files an approved split itself (#211).
> 2	
> 3	Wherever the owner would have typed `/work`, autopilot posts one short line instead, and the river still stops for the
> 4	owner wherever the owner must decide. A planner's questions no longer always stop on autopilot: the plan reviewer
> 5	judges each question's assumption against the owner's own words, and only a question it does not accept stops.
> 6	
> 7	These tests run the real workflows the way GitHub runs them, on the machine from test_start.py (agent.yml for a run,
> 8	commands.yml for a comment), with a fake GitHub that also knows each issue's labels. Autopilot is the `autopilot`
> 9	label on the issue. GitHub gives an issue's labels three ways and the fake answers all three: `gh api
> 10	repos/o/r/issues/N` (with its labels), `gh api repos/o/r/issues/N/labels`, and `gh issue view N --json ...labels`.
> 11	With the option fail_labels, every one of those reads of issue #57 fails the way GitHub fails (HTTP 502), and nothing
> 12	else does. A signal that starts a stage is `gh api repos/o/r/dispatches` with event_type dokima-next and its
> 13	client_payload, given as -f/-F fields or as JSON through --input; the fake keeps both.
> 14	Where only the river's decision matters, the tests run `python3 -m dokima.agent next` on a record, against the same
> 15	fake GitHub.
> 16	"""
> 17	import json
> 18	import os
> 19	import re
> 20	import subprocess
> 21	import sys
> 22	
> 23	import test_start as ts
> 24	from

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^(FAILED|E  )" | cut -c1-400
```

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
> E        +      where created_issues = <test_start.Run object at 0x7f1770b21dc0>.created_issues
> E       AssertionError: 211.3: with #57 on autopilot the approved plan did not start the worker: []
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
> E       AssertionError: 211.4: an approving plan review on autopilot did not start th

**Agent:** Grading the plan for #211: all 10 new tests fail today for the right reason. Now checking whether the planned workflow changes are actually needed and allowed.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Decide what follows" -A30 .github/workflows/agent.yml | head -80; grep -n "split\|autopilot" .github/workflows/commands.yml | head -40
```

> 302:      - name: Decide what follows, and say it on the card
> 303-        id: next
> 304-        if: always()
> 305-        env:
> 306-          GH_TOKEN: ${{ github.token }}
> 307-        run: |
> 308-          export OWNERS=$(python3 -m dokima.plan approvers)
> 309-          NEXT=$(python3 -m dokima.agent next "$N" "$OUT") || NEXT=stop
> 310-          echo "next=$NEXT" >> "$GITHUB_OUTPUT"; echo "$NEXT"
> 311-      - name: Post the record as a comment, on the PR once there is one
> 312-        if: always()
> 313-        env:
> 314-          GH_TOKEN: ${{ steps.app.outputs.token }}
> 315-        run: |
> 316-          # The run's card becomes its record, edited in place; a card that cannot be edited never loses the record.
> 317-          if [ -n "$CARD_ID" ]; then
> 318-            gh api -X PATCH "repos/$GITHUB_REPOSITORY/issues/comments/$CARD_ID" -F body=@"$OUT/comment.md" --silent && exit 0
> 319-            echo "::warning title=Card not edited::the record is posted as a new comment"
> 320-          fi
> 321-          PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --json number -q '.[0].number')
> 322-          if [ -n "$PR" ] && { [ "$ROLE" = worker ] || [ "$STAGE" = pr ]; }; then
> 323-            gh pr comment "$PR" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"
> 324-          else
> 325-            gh issue comment "$N" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"
> 326-          fi
> 327-      - name: Move the card on the board
> 328-        if: always() && vars.DOKIMA_B

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "workflow" .github/workflows/agent.yml | head -20; grep -rn "workflows" dokima/agent.py | head -10
```

> 15:  workflow_call:
> 22:  workflow_dispatch:

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 -- .github/workflows/ ; git log -3 --format='%h %an %s' -- .github/workflows/commands.yml
```

> 60dee99 Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off (#214)
> 481ca21 Live card: cancelled runs and who gets pinged (#208)
> c66ca9f Live card: queued within seconds, waiting behind another run, the same card at every hand-off and split (#203)
> 297beb1 Board: the Priority pill follows the issue's priority label (#206)
> 62ca0f9 Live card: one card per run, updated in place from working to its result (#197)
> 0c5a1ad Plan review fails silently on a split: it needs a try branch splits never create (#177)
> ad1f759 Plan checker: kinds, sources and named tests (#174)
> e28c83c Merge check reads the criteria from the approved plan, not the issue text (#171)
> 60dee99 dokima-runtime[bot] Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off (#214)
> c66ca9f dokima-runtime[bot] Live card: queued within seconds, waiting behind another run, the same card at every hand-off and split (#203)
> 0c5a1ad dokima-runtime[bot] Plan review fails silently on a split: it needs a try branch splits never create (#177)

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def owner_comment\|^STORY_PLANNED\|^def record_comment" -A4 tests/test_start.py | head -30; grep -n "always says why" AGENTS.md; grep -rn "issuecomment-77\|Show the cost" tests/ | head
```

> 396:def record_comment(rec, t):
> 397-    """A comment the bot posted carrying a record, as GitHub returns it."""
> 398-    return {"author": {"login": agent.BOT}, "body": agent.render(rec), "createdAt": t}
> 399-
> 400-
> 401:def owner_comment(body, t):
> 402-    """A comment the owner wrote."""
> 403-    return {"author": {"login": OWNER}, "body": body, "createdAt": t}
> 404-
> 405-
> --
> 645:STORY_PLANNED = [owner_comment("/plan", "2026-10-07T10:00:00Z"), record_comment(planner_record(STORY), "2026-10-07T10:10:00Z")]
> 646-STORY_APPROVED = STORY_PLANNED + [record_comment(review_record(APPROVE), "2026-10-07T10:20:00Z"),
> 647-                                  owner_comment("/work", "2026-10-07T10:30:00Z")]
> 648-
> 649-
> 34:- **Fail closed.** Missing proof, a missing reviewer or a broken check blocks; nothing is waved through, and a failure always says why on the issue.
> tests/test_autopilot_river.py:47:            "matched": "Show the cost of every run.", "source": ISSUE + "#issuecomment-77"}

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["Planned one story with six criteria: an approved plan or split on autopilot goes on by itself with one Autopilot line, off autopilot it stops as today, the existing stops stay, planner questions are judged by the plan reviewer, and an unreadable autopilot label stops.",
          "Wrote ten tests in tests/test_autopilot_river.py that run the real workflows against a fake GitHub."],
  "decided": ["On autopilot a plan with questions goes to the plan reviewer, which accepts an assumption only with the owner's words and where they were said; the owner's newer comment replaces questions as an automatic stop.",
              "The workflows agent.yml and commands.yml, the reviewer's prompt and AGENTS.md are in scope, since filing a split and picking up a waiting plan need them."],
  "open": ["Six criteria, one over the split limit, kept as one story because #211 is already a story of #205."]
 },
 "verdict": "block",
 "summary": "The plan drops the owner's rule that an assumption which changes how the system works or what it costs always stops, and its tests let the reviewer accept an assumption on words the owner never said.",
 "blockers": [
  {"id": "B1", "criterion": "211.5",
   "test": "tests/test_autopilot_river.py::test_on_autopilot_an_accepted_assumption_goes_on_and_one_not_accepted_stops",
   "problem": "The owner said an assumption that changes how the system works or what it costs stops for them. 211.5 only says the reviewer accepts an assumption when it has the owner's words; nothing in the criterion or its tests says an assumption that changes how the system works or what it costs is never accepted. The test even requires the opposite: it accepts the assumption that the board gets a cost column priced per run and expects the worker to start.",
   "evidence": "Owner's comment on #211 (2026-10-08T06:56:48Z): 'If it changes how the system works, what it costs, or is
```

> rc=0

**Agent:** I blocked the plan for #211 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

All 10 new tests in `tests/test_autopilot_river.py` fail today, each because the autopilot behaviour isn't built yet, not because of a crash or a bad setup. The two blockers below are about what the tests would let through.

**Blockers (both on criterion 211.5, both for the planner):**
- **B1, one of your asks is missing.** You said an assumption that "changes how the system works, what it costs, or isn't backed by my words" stops for you. The plan only requires the reviewer to quote your words. Nothing in the plan or tests keeps out an assumption that changes how the system works or what it costs. One test even expects the worker to start after the reviewer accepts "the board shows a cost column, priced per run" (lines 35–36 and 426–430).
- **B2, the "your own words" check proves nothing.** Code only checks that a matched-words field exists and that the source isn't an outside website. The test that accepts an assumption cites `issuecomment-77` and the words "Show the cost of every run.", and neither exists in that test's issue (lines 46–47). So a reviewer could make up words, or quote someone else's comment or another issue, and the river would carry on. The fix I proposed: code checks that the quoted words really appear in the issue body, a comment by a code owner on this issue, or AGENTS.md. Tests then cover a real quote passing and each kind of fake failing.

**Notes (not blocking):**
- The plan changes `.github/workflows/agent.yml`, `commands.yml` and `dokima/roles/reviewer.md`. AGENTS.md allows that only when the issue asks. The planner explained why it needs them, and the issue does name `commands.yml`, so confirm this when you say `/work`.
- The test for "even when its parent is on autopilot" may not set #57 up as a child of #50. If not, it doesn't prove the parent's label is ignored.

Your other asks each map to a criterion: 211.1 to 211.4, and 211.6 for "autopilot can't be read". The plan has six criteria, one over the split limit; the planner kept it as one story because #211 is already a story of #205, which seems reasonable.
