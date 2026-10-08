# reviewer (plan) for #181

Run: https://github.com/dokima-dev/dokima/actions/runs/37752231674

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (48.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/e49bad64-0a4c-4aad-8776-25df879520a2/tool-results/b77pgl165.txt
> 
> Preview (first 2KB):
> total 40
> drwxr-xr-x 2 runner runner  4096 Oct  8 08:48 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 08:48 ..
> -rw-r--r-- 1 runner runner 10309 Oct  8 08:48 01-planner.json
> -rw-r--r-- 1 runner runner  5749 Oct  8 08:48 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11521 Oct  8 08:48 03-planner.json
> # Issue #181: The card says what the issue is, where it stands, its children, and what the owner must do
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 3</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners read one sentence and one status line at the top of a card and know what the issue is, where it stands, how each child is doing if it was split, and what, if anything, is theirs to do now.
> 
> **Context:** Keeps the status line of the issue body, the planner's summary sentence of the owner's comment of 2026-10-07 20:16 and the smart shared card of the owner's comment of 2026-10-07 20:55. plan.json is checked in dokima/planner.py (from_kind(), check_stories()) and asked for in dokima/roles/planner.md ('What you hand back'); both need a new required field (suggested name: summary) for the user_story and feature kinds; the issue explicitly a

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (36.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/e49bad64-0a4c-4aad-8776-25df879520a2/tool-results/b4u2dazzb.txt
> 
> Preview (first 2KB):
> # Issue #181: The card says what the issue is, where it stands, its children, and what the owner must do
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 3</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners read one sentence and one status line at the top of a card and know what the issue is, where it stands, how each child is doing if it was split, and what, if anything, is theirs to do now.
> 
> **Context:** Keeps the status line of the issue body, the planner's summary sentence of the owner's comment of 2026-10-07 20:16 and the smart shared card of the owner's comment of 2026-10-07 20:55. plan.json is checked in dokima/planner.py (from_kind(), check_stories()) and asked for in dokima/roles/planner.md ('What you hand back'); both need a new required field (suggested name: summary) for the user_story and feature kinds; the issue explicitly asks for it, so dokima/roles/ may change here. The stage and 'needs you' already exist as code: dokima/agent.py STAGE_COLUMN, board_place() and the river's stop decisions; the card must use the same rule so the card and the board's Needs you pill never disagree. A filed split is a 'split' record wh

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/e49bad64-0a4c-4aad-8776-25df879520a2/tool-results/b4u2dazzb.txt
```

> 1	# Issue #181: The card says what the issue is, where it stands, its children, and what the owner must do
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- /dokima-card -->
> 5	
> 6	<details open><summary>From the approved plan of #143, story 3</summary>
> 7	
> 8	**Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 9	
> 10	**User story:** Owners read one sentence and one status line at the top of a card and know what the issue is, where it stands, how each child is doing if it was split, and what, if anything, is theirs to do now.
> 11	
> 12	**Context:** Keeps the status line of the issue body, the planner's summary sentence of the owner's comment of 2026-10-07 20:16 and the smart shared card of the owner's comment of 2026-10-07 20:55. plan.json is checked in dokima/planner.py (from_kind(), check_stories()) and asked for in dokima/roles/planner.md ('What you hand back'); both need a new required field (suggested name: summary) for the user_story and feature kinds; the issue explicitly asks for it, so dokima/roles/ may change here. The stage and 'needs you' already exist as code: dokima/agent.py STAGE_COLUMN, board_place() and the river's stop decisions; the card must use the same rule so the card and the board's Needs you pill never disagree. A filed split is a 'split' record whose handback.stories holds each child's issue number and title (dokima/agent.py file_split()); each child's stage comes from its own records and PR. The real-page proof sits here because on

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 0b1e968 b899b1e --stat; git diff 0b1e968 b899b1e -- tests/ | head -300
```

> tests/test_card_status.py | 82 +++++++++++++++++++++++++++++++----------------
>  1 file changed, 55 insertions(+), 27 deletions(-)
> diff --git a/tests/test_card_status.py b/tests/test_card_status.py
> index c23ea4c..d2b3b8c 100644
> --- a/tests/test_card_status.py
> +++ b/tests/test_card_status.py
> @@ -6,8 +6,10 @@ status line, never a heading:
>  
>      card.status(issue, found) -> (stage, todo)
>          stage  "Backlog", "Plan", "Work", "Review" (the board's columns) or "Merged"
> -        todo   None when nothing is the owner's to do, else the owner's to-do in words; exactly "Ready for approval"
> -               when the work waits for the owner's approval and every criterion's check and All tests passed
> +        todo   None when nothing is the owner's to do, else the owner's to-do, word for word one of TODO below:
> +               a plan with questions, an approved plan, three blocks in a row, a rejected hand-back, a run that never
> +               started, an escalation, approved work with every check green ("Ready for approval"), and approved work
> +               whose checks have not all passed
>          `found` is what card.render takes (see tests/test_card_records.py), plus
>                  "items":    the conversation the records come from (dokima.agent.conversation), oldest first
>                  "children": for a filed split, [{"number", "title", "stage"}] in the split's order
> @@ -131,8 +133,8 @@ def lines_of(text):
>  
>  
>  def bare(line):
> -    """A line without its HTML tags, '*' and

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_status.py 2>&1 | tail -60
```

> FAILED tests/test_card_status.py::test_an_issue_with_no_records_is_in_backlog_and_a_filed_split_is_in_work - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_card_opens_with_the_status_line_when_there_is_no_plan - AssertionError: 181.2: the card with no plan does not open with its status line: “### Plan: add `work` to start”
> assert (not True)
>  +  where True = <built-in method startswith of str object at 0x7f4655e08670>('#')
>  +    where <built-in method startswith of str object at 0x7f4655e08670> = '### Plan: add `work` to start'.startswith
> FAILED tests/test_card_status.py::test_a_split_lists_each_child_with_its_link_and_stage - AssertionError: 181.3: expected one line linking child #41 (https://github.com/o/r/issues/41), found 0
> assert 0 == 1
>  +  where 0 = len([])
> FAILED tests/test_card_status.py::test_the_card_reads_each_childs_stage_from_its_own_records_and_pr - AssertionError: 181.3: the children read from GitHub are [], not [(41, 'Child 41', 'Backlog'), (42, 'Child 42', 'Plan'), (43, 'Child 43', 'Review'), (44, 'Child 44', 'Merged')]
> assert [] == [(41, 'Child ...4', 'Merged')]
>   
>   Right contains 4 more items, first extra item: (41, 'Child 41', 'Backlog')
>   
>   Full diff:
>   + []
>   - [
>   -     (
>   -         41,
>   -         'Child 41',
>   -         'Backlog',
>   -     ),
>   -     (
>   -         42,
>   -         'Child 42',
>   -         'Plan',
>   -     ),
>   -     (
>   -         43,
>   -         'Child 43',
> 

**Agent:** Round 2 of the plan review: B1's fix is in, and all 41 new tests fail today. Next I'm checking that the new river cases fail because the feature is missing, not because of a broken fixture.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_status.py -k needs_you 2>&1 | grep FAILED; python3 -m pytest -q tests/ 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bfwbpnszn). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/e49bad64-0a4c-4aad-8776-25df879520a2/tasks/bfwbpnszn.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 60 python3 -m pytest -q tests/test_card_status.py -k needs_you 2>&1 | grep FAILED | cut -c1-260
```

> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a fresh plan goes to the reviewer] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a plan with questions waits for the owner] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[an approved plan waits for /work] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a blocked plan goes back to the planner] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a second block in a row still goes back] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a third block in a row waits for the owner] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not exist
> FAILED tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill[a third code block in a row waits for the owner] - Failed: 181.2: the card has no status yet: card.status(issue, found) does not e

**Agent:** All new cases get past the river's own placement and fail only because the card has no status yet. Writing the approval.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote into 181.2 the owner's exact to-do at each stop: questions, approved plan, three blocks, rejected hand-back, a run that never started, escalation, Ready for approval, and approved work whose checks have not all passed.",
          "It made the status test check that exact to-do for each case, and added cases for a third code block, a run that never started and approved work with a failed check."],
  "decided": ["The words of each to-do are the planner's own, fixed in the plan; the card must use them exactly."],
  "open": ["The owner went on with both of the planner's assumptions by saying /review."]},
 "verdict": "approve",
 "summary": "The plan now checks the exact words of the owner's to-do at every stop, and all 41 new tests fail today because the card has no status yet.",
 "blockers": [],
 "notes": [
  {"text": "The to-do wording is the planner's choice, not the owner's words; the owner can change it at /work if any phrase reads wrong.",
   "evidence": "plan.json 181.2 text; tests/test_card_status.py TODO"},
  {"text": "Three tests outside this plan failed on main in the last round, so All tests on this PR will be red whatever the worker does, until that is fixed.",
   "evidence": "previous review note; main commit 91ba938 addressed one such failure"}],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "plan.json for a user story and for a feature carries one plain sentence saying what the issue is about; the planner prompt asks for it, and the planner's check rejects a plan without it, naming the field.", "source": "https://github.com/dokima-dev/dokima/issues/181", "criterion": "181.1"},
  {"ask": "The card opens with that sentence, then a small status line (not a heading) naming the issue's current stage and what the owner needs to do, or nothing when nothing is theirs; it agrees with the board's Needs you pill.
```

> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git stash list >/dev/null; git worktree add -q /tmp/main-wt main 2>&1|tail -1; cd /tmp/main-wt && timeout 100 python3 -m pytest -q -x tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -3; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/main-wt
```

> )
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed in 0.17s

**Agent:** Main still fails there, so I'm making that note's evidence exact.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["notes"][1]["evidence"]="on main: pytest -x tests/test_fixer.py tests/test_handback_check.py -> 1 failed (stops at first)"
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 181 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #181 and wrote the result to `/tmp/dokima-out/review.json`. It passes both of Dokima's checks.

- **B1 is fixed.** Last round's blocker was that a vague to-do like "Needs you: act" would pass every test. Criterion 181.2 now gives the owner's to-do word for word at each stop:
  - a plan with questions
  - an approved plan
  - three blocks in a row
  - a rejected hand-back
  - a run that never started
  - an escalation
  - Ready for approval
  - approved work whose checks have not all passed

  The status test now checks that exact wording in the card's status and on the status line. The planner also added test cases for a third code block, a run that never started, and approved work with a failed check.
- **All 41 new tests fail today for the right reason.** Each one fails because the feature is missing (the card has no status yet, there's no child list, no gallery). None fails on a fixture problem. In every status case, the river's own code still puts the issue where the test expects before the card is checked.
- **Asks:** all six of the owner's asks map to criteria 181.1 to 181.6, and none is missing.
- **Notes for the owner:**
  - The to-do wording is the planner's own, not the owner's. If a phrase reads wrong, the owner can change it before saying `/work`.
  - Main is still red. Running `tests/test_fixer.py` and `tests/test_handback_check.py` on main stops at its first failure. Until that's fixed, the All tests check on this PR will fail whatever the worker does, so the card can never show "Ready for approval".

I started a full-suite run on this branch in the background, but it hit the 2-minute limit and I only saw that it finished, not its result.
