# reviewer (plan) for #297

Run: https://github.com/dokima-dev/dokima/actions/runs/37884936324

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (59.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4e0e66bd-a2aa-44f3-b742-f4fbd0f65ade/tool-results/bcw3comew.txt
> 
> Preview (first 2KB):
> .:
> total 84
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:40 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:40 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:40 in
> -rw-r--r--  1 runner runner 57292 Oct  9 04:40 issue.md
> -rw-r--r--  1 runner runner  2744 Oct  9 04:40 open_blockers.json
> -rw-r--r--  1 runner runner  8742 Oct  9 04:40 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:40 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:40 ..
> -rw-r--r-- 1 runner runner 5917 Oct  9 04:40 01-planner.json
> -rw-r--r-- 1 runner runner 7502 Oct  9 04:40 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 9417 Oct  9 04:40 03-planner.json
> # Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> The board's Needs you pill shows only while something truly waits on the owner, and Autopilot shows otherwise.
> 
> **Plan**
> 
> [issue #297](https://github.com/dokima-dev/dokima/issues/297)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #135, #294
> 
> **User story:** The owner trusts Needs you on the board: it shows only on items that truly wait on them, leaves the moment the

`2. Bash`
```
cd /tmp/pack; grep -n "dokima-card\|^## \|^### \|Original\|<!-- dokima" issue.md | head -50; wc -l issue.md
```

> 3:<!-- dokima-card -->
> 4:<!-- dokima-linked-from: 294 -->
> 53:<!-- /dokima-card -->
> 55:<!-- dokima-ask -->
> 65:## Comments
> 67:### RezaSoleymanifar on issue #297 (2026-10-09T03:44:40Z)
> 71:### dokima-runtime on issue #297 (2026-10-09T03:45:04Z)
> 75:### dokima-runtime on issue #297 (2026-10-09T03:45:07Z)
> 80:### dokima-runtime on issue #297 (2026-10-09T03:45:18Z)
> 82:<!-- dokima-record -->
> 263:### RezaSoleymanifar on issue #297 (2026-10-09T03:52:03Z)
> 269:### dokima-runtime on issue #297 (2026-10-09T03:52:23Z)
> 271:<!-- dokima-live -->
> 279:### dokima-runtime on issue #297 (2026-10-09T04:07:18Z)
> 281:<!-- dokima-record -->
> 463:### RezaSoleymanifar on issue #297 (2026-10-09T04:26:33Z)
> 467:### dokima-runtime on issue #297 (2026-10-09T04:26:55Z)
> 469:<!-- dokima-record -->
> 697:### dokima-runtime on issue #297 (2026-10-09T04:39:53Z)
> 699:<!-- dokima-live -->
> 705 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 53,80p issue.md; sed -n 263,280p issue.md; sed -n 463,468p issue.md; sed -n 697,705p issue.md
```

> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The board shows Needs you where nothing needs me: on done and closed issues and pull requests, and on parent issues whose children are simply in progress.
> 
> What I want:
> - Needs you shows only while the flow is actually stopped waiting for me on that item: a question, an approval, a merge, an escalation. It clears the moment that is answered, and always when the item closes.
> - A parent issue shows Needs you only when the parent itself waits on me (for example its split before it is filed, or its end-to-end test hitting a blocker), never just because its children are in progress.
> - Autopilot and Needs you are complementary: an item on autopilot shows Autopilot unless it needs me, then Needs you, never both and never neither.
> - The existing wrong pills are cleared too.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #297 (2026-10-09T03:44:40Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #297 (2026-10-09T03:45:04Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #297 (2026-10-09T03:45:07Z)
> 
> Autopilot is on for #297. Planning started for #297, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #297 (2026-10-09T03:45:18Z)
> ### RezaSoleymanifar on issue #297 (2026-10-09T03:52:03Z)
> 
> /plan Making two things explicit:
> - A closed issue or merged or closed pull request can never get Needs you, whichever job runs last. Today the job that sets "waiting for you to merge" can finish after the close and put the pill back.
> - 

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d,indent=1))"
```

> {
>  "kind": "user_story",
>  "summary": "The board's Needs you pill shows only while something truly waits on the owner, and Autopilot shows otherwise.",
>  "user_story": "The owner trusts Needs you on the board: it shows only on items that truly wait on them, leaves the moment they answer or the item closes, Autopilot shows in its place on everything else that runs by itself, and the wrong pills on the board today are put right.",
>  "acceptance_criteria": [
>   {
>    "text": "Needs you appears only where the river stops for the owner. Finished checks never set it, and a Needs you the river set stays through new commits and checks until answered.",
>    "source": "https://github.com/dokima-dev/dokima/issues/297"
>   },
>   {
>    "text": "Needs you clears the moment the owner answers. A code owner's `/plan`, `/work` or `/review`, as a comment on the issue or its pull request or as the summary of a pull request review submitted as a comment or a change request, takes it off both cards at once, with Autopilot in its place on autopilot. An Approve, and a comment or review from anyone else, from a bot, or with no command, leaves it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/297"
>   },
>   {
>    "text": "A closed issue or a merged or closed pull request never gets Needs you, whichever job runs last. Closing clears it; a run that stops after the owner merged, or checks that finish after the merge, leave a closed item on autopilot with Autopilot and any other with no pill. When GitHub 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff ef4930a HEAD --stat; wc -l tests/test_needs_you.py; python3 -c "
import json;d=json.load(open('/tmp/pack/in/03-planner.json'));print(json.dumps(d['check'],indent=1))"
```

> commit df29d01145888f67d2622dc86f6168395e515b11
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:39:41 2026 +0000
> 
>     planner for #297 (run 37883896574)
> 
>  tests/test_needs_you.py | 271 ++++++++++++++++++++++++++++++++++++++++--------
>  1 file changed, 225 insertions(+), 46 deletions(-)
>  tests/test_needs_you.py | 271 ++++++++++++++++++++++++++++++++++++++++--------
>  1 file changed, 225 insertions(+), 46 deletions(-)
> 620 tests/test_needs_you.py
> {
>  "passed": true,
>  "problems": []
> }

**Agent:** I'm reviewing the re-plan for #297. Next I'll read its tests and run them.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_needs_you.py
```

> <persisted-output>
> Output too large (39.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4e0e66bd-a2aa-44f3-b742-f4fbd0f65ade/tool-results/baz9yii1f.txt
> 
> Preview (first 2KB):
> """Needs you shows only while the river waits on the owner; Autopilot otherwise (#297).
> 
> Before this, the board put Needs you where nothing waited on the owner: every time the done-whens checks finished on a
> pull request (even one already merged), on closed issues a run stopped on after the owner had merged, and on parent
> issues left with the pill from before their split was filed. A Needs you the river did set was wiped by the next new
> commit, yet stayed for the whole run after the owner answered with a command. Nothing ever cleared old wrong pills.
> 
> Most tests fake dokima.board.Board and agent's `gh` against one in-memory world, so they read the board's end state:
> each card's Status and Action ("Needs you", "Autopilot" or none), each item's labels and whether it is closed, each
> issue's open pull request, sub-issues and history (the bot's records and the owner's words, read through
> `gh issue view`). On top of test_autopilot_board's fake Board, the board offers two more reads the code is expected
> to use:
> 
>     .state(kind, n) -> "open" | "closed"    a merged pull request is closed; raises subprocess.CalledProcessError
>                                              when GitHub cannot say
>     .cards() -> [{"kind", "number", "action", "closed", "autopilot"}, ...]
>       

`7. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/4e0e66bd-a2aa-44f3-b742-f4fbd0f65ade/tool-results/baz9yii1f.txt
```

> 1	"""Needs you shows only while the river waits on the owner; Autopilot otherwise (#297).
> 2	
> 3	Before this, the board put Needs you where nothing waited on the owner: every time the done-whens checks finished on a
> 4	pull request (even one already merged), on closed issues a run stopped on after the owner had merged, and on parent
> 5	issues left with the pill from before their split was filed. A Needs you the river did set was wiped by the next new
> 6	commit, yet stayed for the whole run after the owner answered with a command. Nothing ever cleared old wrong pills.
> 7	
> 8	Most tests fake dokima.board.Board and agent's `gh` against one in-memory world, so they read the board's end state:
> 9	each card's Status and Action ("Needs you", "Autopilot" or none), each item's labels and whether it is closed, each
> 10	issue's open pull request, sub-issues and history (the bot's records and the owner's words, read through
> 11	`gh issue view`). On top of test_autopilot_board's fake Board, the board offers two more reads the code is expected
> 12	to use:
> 13	
> 14	    .state(kind, n) -> "open" | "closed"    a merged pull request is closed; raises subprocess.CalledProcessError
> 15	                                             when GitHub cannot say
> 16	    .cards() -> [{"kind", "number", "action", "closed", "autopilot"}, ...]
> 17	                                             every issue and pull request on the board: its Action ("Needs you",
> 18	                                             "Autopilot" or None

`8. Bash`
```
cd /home/runner/work/dokima/dokima; for t in $(grep -o '^def test_[a-z_]*' tests/test_needs_you.py | cut -c5-); do echo "== $t"; timeout 120 python3 -m pytest -q -x "tests/test_needs_you.py::$t" 2>&1 | grep -E "^E  |passed|failed" | head -4; done; python3 -m pytest -q tests/test_board.py tests/test_autopilot_board.py 2>&1 | tail -2
```

> == test_a_check_finishing_never_marks_a_pull_request_for_the_owner
> E       AssertionError: 297.1: after the checks finished, the pull requests show {'pr #60': 'Needs you', 'pr #61': 'Needs you', 'pr #62': 'Needs you'}; a finished check must not mark one for the owner
> E       assert {'pr #60': 'N...: 'Needs you'} == {'pr #60': 'A...: 'Needs you'}
> E         
> E         Omitting 1 identical items, use -vv to show
> == test_needs_you_set_by_the_river_stays_through_new_commits_and_checks
> E       AssertionError: 297.1: a new commit on PR #62 took Needs you away though the owner answered nothing: {'issue #59': None, 'pr #62': None}
> E       assert {'issue #59':...pr #62': None} == {'issue #59':...: 'Needs you'}
> E         
> E         Differing items:
> == test_a_code_owners_command_clears_needs_you_at_once_and_nothing_else_does
> E       AssertionError: 297.2: the code owner said /work on #57, on autopilot, and the cards show {'issue #57': 'Needs you', 'pr #60': 'Needs you'}, not Autopilot
> E       assert {'issue #57':...: 'Needs you'} == {'issue #57':...: 'Autopilot'}
> E         
> E         Differing items:
> == test_a_code_owners_command_in_a_review_summary_clears_needs_you_at_once
> E           AssertionError: 297.2: RezaSoleymanifar's changes_requested review 'Please rename the helper.' on PR #61 answered nothing, yet the pills changed to {'issue #58': None, 'pr #61': None, 'issue #57': 'Needs you', 'pr #60': 'Needs you'}
> E           assert {None, 'Needs you'} == {'Needs you'}
> E             
> E  

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote the plan to seven criteria with thirteen tests in tests/test_needs_you.py, all failing today because the feature is missing, and adds board.yml runs on pull request reviews."],
  "decided": ["A code owner's command in a pull request review's summary clears Needs you at once, as the owner answered.",
              "The board run of this change's merge sweeps every card on the board, and so does the board run of every later merge.",
              "An item on autopilot shows Autopilot or Needs you, never both and never neither, after every board moment."],
  "open": ["Whether the sweep runs only once, as the owner wrote, or at every merge (planned for every merge)."]},
 "verdict": "block",
 "summary": "The plan now covers the full sweep and the one-pill rule, but it sweeps at every merge where the owner asked for a one-time sweep.",
 "blockers": [
  {"id": "B3", "criterion": "297.5", "test": "tests/test_needs_you.py::test_a_merge_sweeps_every_pill_on_the_board_to_what_it_should_be",
   "problem": "The owner asked for a one-time sweep that clears the backlog of wrong pills once. Criterion 297.5 adds 'Every later merge's board run sweeps the same way', and 297.4 leans on it ('loses an old Needs you at the next merge'). That adds work the owner did not ask for: every merge reads the history of every issue on the board. The owner's words leave only one reading, so the planner should plan for it and offer every-merge sweeps as the alternative in the question, not the other way round.",
   "evidence": "Owner's /plan comment on #297 (2026-10-09T03:52:03Z): 'Right after this merges, a one-time sweep goes over every item on the board and sets each pill to what it should be by these rules, so the backlog of wrong pills is cleared once.' plan.json criteria 4 and 5; the plan's own question says 'Each merge then also reads the history of every open issue on the boa
```

> (Bash completed with no output)

**Agent:** I've blocked the re-plan for #297 and sent it back to the planner. Both checks on the hand-back passed, and it's saved as `/tmp/dokima-out/review.json`.

**Why it's blocked:** you asked for "a one-time sweep… so the backlog of wrong pills is cleared once." The plan sweeps the whole board at every merge instead (criterion 297.5). Criterion 297.4 relies on that: a parent loses an old Needs you "at the next merge". The planner raised this as a question, but planned against your words, and the plan itself says each merge would then also read the history of every open issue on the board. I didn't accept that assumption, so on autopilot this stops for you rather than going ahead. The fix I asked for:
- Plan the sweep to run once, right after this change merges.
- Add a test showing a later merge doesn't sweep again.
- Keep "sweep at every merge" as an option in the question, so you can still choose it.

**Earlier blockers, now fixed:**
- **B1:** the sweep now sets every card to the right pill, and the test covers every kind of wrong pill alongside cards that should keep theirs.
- **B2:** "Autopilot or Needs you, never both and never neither" is now its own criterion, 297.6, with a test that walks two items through every board moment.

**Every ask is covered.** All nine things you asked for, including your answer that a command in a review summary clears Needs you at once, map to a criterion. Nothing is missing.

**Tests:** I ran each of the 13 new tests on its own. All fail today because the feature isn't built yet, not because of a crash or a broken setup. The two existing board test files the plan changes still pass (39 tests).

**One thing that needs your approval later:** clearing Needs you from a review summary means changing `.github/workflows/board.yml`. A bot can't push a workflow change, so that build will pause until you approve it on GitHub. The plan says this in its concerns.
