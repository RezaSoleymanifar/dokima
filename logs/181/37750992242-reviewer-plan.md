# reviewer (plan) for #181

Run: https://github.com/dokima-dev/dokima/actions/runs/37750992242

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> **Context:** Keeps the status line of the issue body, the planner's summary sentence of the owner's comment of 2026-10-07 20:16 and the smart shared card of the owner's comment of 2026-10-07 20:55. plan.json is checked in dokima/planner.py (from_kind(), check_stories()) and asked for in dokima/roles/planner.md ('What you hand back'); both need a new required field (suggested name: summary) for the user_story and feature kinds; the issue explicitly asks for it, so dokima/roles/ may change here. The stage and 'needs you' already exist as code: dokima/agent.py STAGE_COLUMN, board_place() and the river's stop decisions; the card must use the same rule so the card and the board's Needs you pill never disagree. A filed split is a 'split' record whose handback.stories holds each child's issue number and title (dokima/agent.py file_split()); each child's stage comes from its own records and PR. 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_card_status.py dokima/card.py dokima/planner.py; grep -n "kind" dokima/planner.py | head -40
```

> commit 0b1e96850328c94d69d65cdc4974009d883e15b4
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 08:32:21 2026 +0000
> 
>     planner for #181 (run 37748531404)
> 
>  tests/samples/132/plan.json |   1 +
>  tests/test_agent.py         |   2 +-
>  tests/test_body.py          |   2 +-
>  tests/test_card.py          |  40 +--
>  tests/test_card_status.py   | 629 ++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_feature_check.py |   2 +-
>  tests/test_plan_check.py    |   4 +-
>  tests/test_plan_shape.py    |   6 +-
>  tests/test_planner.py       |   2 +-
>  tests/test_questions.py     |   2 +-
>  10 files changed, 661 insertions(+), 29 deletions(-)
>   629 tests/test_card_status.py
>   292 dokima/card.py
>   462 dokima/planner.py
>  1383 total
> 7:The planner holds no GitHub key. It ends by writing one plan.json to OUT, of kind user_story or feature (see
> 36:ALWAYS = ("the planner always hands back a plan, a plan.json of kind user_story or feature, "
> 61:    if "kind" not in p:
> 62:        raise Garbled(f"plan.json has no kind: {ALWAYS}")
> 63:    return from_kind(p, issue_link(number) if number is not None else None)
> 132:def from_kind(p, issue=None):
> 139:    kind = p["kind"]
> 140:    if kind == "feature":
> 149:    if kind != "user_story":
> 150:        raise Garbled(f"plan.json kind is {kind!r}: {ALWAYS}")
> 420:        kind, result = read_output(out, number)
> 421:        if kind == "plan":
> 446:        if kind == "feature":
> 457:    print(kind)

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_status.py
```

> <persisted-output>
> Output too large (37.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/291d7b5e-4a35-4905-b643-45ba74d476bc/tool-results/b010ymh1p.txt
> 
> Preview (first 2KB):
> """The card says what the issue is, where it stands, its children, and what the owner must do.
> 
> Issue #181 (story 3 of #143). Every plan.json carries a one-sentence "summary" of what the issue is about, and the
> planner's check rejects a plan without one. The card (`dokima/card.py`) opens with that sentence, then one small
> status line, never a heading:
> 
>     card.status(issue, found) -> (stage, todo)
>         stage  "Backlog", "Plan", "Work", "Review" (the board's columns) or "Merged"
>         todo   None when nothing is the owner's to do, else the owner's to-do in words; exactly "Ready for approval"
>                when the work waits for the owner's approval and every criterion's check and All tests passed
>         `found` is what card.render takes (see tests/test_card_records.py), plus
>                 "items":    the conversation the records come from (dokima.agent.conversation), oldest first
>                 "children": for a filed split, [{"number", "title", "stage"}] in the split's order
> 
> The stage and the Needs you pill follow the board's own rule, dokima.agent.board_place() on the newest record and
> dokima.agent.next_step() as it was decided when that record was posted (the conversation before it), so the card and
> the board never disagree. Three cases come before 

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/291d7b5e-4a35-4905-b643-45ba74d476bc/tool-results/b010ymh1p.txt
```

> 1	"""The card says what the issue is, where it stands, its children, and what the owner must do.
> 2	
> 3	Issue #181 (story 3 of #143). Every plan.json carries a one-sentence "summary" of what the issue is about, and the
> 4	planner's check rejects a plan without one. The card (`dokima/card.py`) opens with that sentence, then one small
> 5	status line, never a heading:
> 6	
> 7	    card.status(issue, found) -> (stage, todo)
> 8	        stage  "Backlog", "Plan", "Work", "Review" (the board's columns) or "Merged"
> 9	        todo   None when nothing is the owner's to do, else the owner's to-do in words; exactly "Ready for approval"
> 10	               when the work waits for the owner's approval and every criterion's check and All tests passed
> 11	        `found` is what card.render takes (see tests/test_card_records.py), plus
> 12	                "items":    the conversation the records come from (dokima.agent.conversation), oldest first
> 13	                "children": for a filed split, [{"number", "title", "stage"}] in the split's order
> 14	
> 15	The stage and the Needs you pill follow the board's own rule, dokima.agent.board_place() on the newest record and
> 16	dokima.agent.next_step() as it was decided when that record was posted (the conversation before it), so the card and
> 17	the board never disagree. Three cases come before the rule: a merged PR is Merged, an issue with no records is in
> 18	Backlog, and a filed split (its newest record is a "split") is in Work with nothing for the owner, as
> 19	`p

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_card_status.py 2>&1 | grep -E "FAILED|ERROR|passed|failed" | head -60
```

> >       assert out.returncode != 0, "181.1: the planner check passed a split with no summary"
> E       AssertionError: 181.1: the planner check passed a split with no summary
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste...nd thing works', 'source': 'https://github.com/o/r/issues/40'}], ...}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste...nd thing works', 'source': 'https://github.com/o/r/issues/40'}], ...}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste..., 'stage': 'plan', 'handback': {'verdict': 'approve', 'blockers': []}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste... {'verdict': 'block', 'blockers': [{'id': 'B1', 'fixer': 'planner'}]}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste... {'verdict': 'block', 'blockers': [{'id': 'B1', 'fixer': 'planner'}]}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 's

**Agent:** Running the planner's tests for #181; collecting the short failure reasons next.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q -rf tests/test_card_status.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-260; echo ===; python -m pytest -q -x --deselect tests/test_card_status.py 2>&1 | tail -15
```

> >       assert out.returncode != 0, "181.1: the planner check passed a split with no summary"
> E       AssertionError: 181.1: the planner check passed a split with no summary
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste...nd thing works', 'source': 'https://github.com/o/r/issues/40'}], ...}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste...nd thing works', 'source': 'https://github.com/o/r/issues/40'}], ...}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste..., 'stage': 'plan', 'handback': {'verdict': 'approve', 'blockers': []}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste... {'verdict': 'block', 'blockers': [{'id': 'B1', 'fixer': 'planner'}]}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 'summary': 'Slow calls hand back a job id inste... {'verdict': 'block', 'blockers': [{'id': 'B1', 'fixer': 'planner'}]}, 'check': {'passed': True, 'problems': []}, ...}]
> steps = [{'role': 'planner', 'stage': None, 'handback': {'kind': 'user_story', 's

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q --deselect tests/test_card_status.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-200; git diff HEAD~1 -- tests/test_card.py | head -120
```

> _____________ test_title_asks_for_approval_when_all_checks_passed ______________
>     def test_title_asks_for_approval_when_all_checks_passed(record_property):
>         """Approved work with every check passed says Ready for approval on its status line."""
> E        +    where '<!-- dokima-card -->\n### Approve the result to merge\n[latest run](https://github.com/o/r/actions/runs/1) · [PR #5](...ma/icons/none.svg" width="16" height="16" align="absmiddle
> FAILED tests/test_card.py::test_title_asks_for_approval_when_all_checks_passed - assert 'Ready for approval' in '### Approve the result to merge'
>  +    where '<!-- dokima-card -->\n### Approve the result to merge\n[latest run](https://github.com/o/r/actions/runs/1) · [PR #5](...ma/icons/none.svg" width="16" height="16" align="absmiddle" alt="n
> FAILED tests/test_card.py::test_unrelated_running_check_is_ignored - assert 'Ready for approval' in '### Approve the result to merge'
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the ow
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in th
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own crite

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git stash -q 2>/dev/null; git checkout -q HEAD~1 -- tests && python -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -3; git checkout -q HEAD -- tests; git status --short
```

> +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 11 passed in 0.99s

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def next_step\|def board_place\|def next_line\|Needs you\|needs_you" dokima/agent.py | head -30
```

> 836:def next_step(items, rec, owners, rounds=3):
> 903:def board_place(rec, step):
> 905:    the owner, and the Needs you pill exactly when the river stops for the owner (not after a cancel)."""
> 911:def move_card(repo, number, column, needs_you, spec, q=None):
> 912:    """Put the issue and its open pull request in that column, with or without the Needs you pill."""
> 922:        b.set(iid, "Action", "Needs you" if needs_you else None)
> 926:def next_line(step, owners):
> 1065:            # Deciding what follows failed, so the river stopped: the run's own stage, with Needs you.
> 1073:            print(f"board: {kind} #{n} -> {column}{' · Needs you' if needs == 'needs' else ''}")

`10. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 836,960p dokima/agent.py
```

> def next_step(items, rec, owners, rounds=3):
>     """The river: what follows the run that just finished. ("start", role, stage) or ("stop", why), decided by code.
> 
>     A planner hands to the reviewer unless it has questions for the owner. A worker hands to the reviewer. A blocking
>     review sends the work back, until three blocks in a row at that stage since the owner last spoke; then it is the
>     owner's call. An approval, a question, an escalation or a hand-back code rejected always stops for the owner. A
>     cancelled run starts nothing and mentions no one: whoever cancelled it knows."""
>     role, stage, h = rec.get("role"), rec.get("stage") or "", rec.get("handback") or {}
>     if role == "cancelled":
>         return ("cancelled", "Nothing starts by itself after a cancel. Give the command again to start this stage.")
>     if role == "not-started":
>         return ("stop", "Nothing ran, see why above. Fix the cause, then give the command again.")
>     if not rec.get("check", {}).get("passed"):
>         return ("stop", "The hand-back was rejected by code, see the problems above. Fix the cause, then start the stage again.")
>     if role == "planner":
>         if h.get("questions"):
>             return ("stop", "The plan has questions for you. Answer with `/plan` and your words, or say `/review` to go on with its assumptions.")
>         return ("start", "reviewer", "plan")
>     if role == "worker":
>         return ("start", "reviewer", "pr")
>     if role != "reviewer":
>         return ("s

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five criteria and one non-functional requirement for the card's opening sentence, status line, children list, Ready for approval and Merged, with 38 new tests that all fail today because the feature is missing.",
          "It added the summary to every sample plan the existing tests use and moved the old card tests from the heading to the status line."],
  "decided": ["The card's stage and Needs you follow the board's own rule; Ready for approval also needs an approving code review of the latest build.",
              "A `python3 dokima/card.py gallery DIR` command draws every situation's card for the owner to post on a throwaway issue and PR."],
  "open": ["The owner went on with both of the planner's assumptions by saying /review."]},
 "verdict": "block",
 "summary": "The plan is close, but nothing checks that the status line says what the owner must actually do: any words after Needs you would pass, except for Ready for approval.",
 "blockers": [
  {"id": "B1", "criterion": "181.2",
   "test": "tests/test_card_status.py::test_the_status_agrees_with_the_boards_needs_you_pill",
   "problem": "The owner asked that the status line name what the owner needs to do. The tests only check that the to-do is some non-empty text that appears on the line. A card that says 'Needs you: act' for a plan with questions, an approved plan, a third block, an escalation and a rejected hand-back would pass every test, so the to-do is never proven.",
   "evidence": "tests/test_card_status.py lines 293-298 only assert `isinstance(todo, str) and todo.strip()` and that the to-do is on the line; the only to-do pinned anywhere is 'Ready for approval' (lines 488, 491). The criterion text of 181.2 does not say what each to-do is either.",
   "fix": "Say in 181.2 what the to-do is at each stop (for example the river's own stop words from dokima.agent.next_step, or a short phrase
```

> rc=0

**Agent:** I've blocked the plan for #181 and sent it back to the planner over one problem. The review is in `/tmp/dokima-out/review.json` and passes both format checks.

**Blocker B1 (criterion 181.2):** nothing checks that the status line says what the owner actually has to do.
- The tests only check that some text follows "Needs you". The one exact to-do they check is "Ready for approval".
- So a card that said "Needs you: act" would pass for a plan with questions, an approved plan, a third block in a row, an escalation and a rejected hand-back.
- The fix is to name the to-do for each of those stops in 181.2 and check it in each case. The river already has wording for each stop in `dokima/agent.py` `next_step()` that could be reused.

**Everything else holds up:**
- Each of your six asks in the issue maps to one criterion (181.1 to 181.6); none is missing.
- I ran all 38 new tests and they fail today because the feature is missing, not because of a crash or a bad path. The gallery test exits early with a `HEAD_SHA` error because the `gallery` command doesn't exist yet.
- The old card tests the planner changed are written for the new status line, so two of them fail until the worker builds it. The planner listed both changes.

**Notes I added:**
- "Ready for approval" also needs the code review to have approved the latest build. Your words didn't say that, but it follows from the card agreeing with the board, which only stops for approval after that review.
- **Main is already failing:** three tests fail there before this plan touches anything (`tests/test_fixer.py` and `tests/test_handback_check.py`), with "asks must list every ask in the owner's…". Until they're fixed, the "All tests" check will fail on every pull request, so no work can show Ready for approval. I've proposed it as a separate issue.
