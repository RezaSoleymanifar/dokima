# reviewer (plan) for #251

Run: https://github.com/dokima-dev/dokima/actions/runs/37853850690

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (30.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2708626f-5f4d-4be2-9973-86bfcb784e8a/tool-results/b1gnrlznh.txt
> 
> Preview (first 2KB):
> .:
> total 48
> drwxr-xr-x  3 runner runner  4096 Oct  8 22:30 .
> drwxrwxrwt 18 root   root    4096 Oct  8 22:30 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 22:30 in
> -rw-r--r--  1 runner runner 26433 Oct  8 22:30 issue.md
> -rw-r--r--  1 runner runner  1251 Oct  8 22:30 open_blockers.json
> -rw-r--r--  1 runner runner  3251 Oct  8 22:30 plan.json
> 
> in:
> total 24
> drwxr-xr-x 2 runner runner 4096 Oct  8 22:30 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 22:30 ..
> -rw-r--r-- 1 runner runner 3151 Oct  8 22:30 01-planner.json
> -rw-r--r-- 1 runner runner 4726 Oct  8 22:30 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3875 Oct  8 22:30 03-planner.json
> # Issue #251: The issue card and the planner's run comment show the links, each kind with its own icon
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 2</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** The owner sees which issues this one is blocked by, blocks and relates to, on the card at the top of the issue and its pull request and on the planner's run comment, each kind with its own icon.
> 
> **Context:** The owner answered round one's question on #231: both cards show the links, so the planner's run comment 

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> # Issue #251: The issue card and the planner's run comment show the links, each kind with its own icon
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 2</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** The owner sees which issues this one is blocked by, blocks and relates to, on the card at the top of the issue and its pull request and on the planner's run comment, each kind with its own icon.
> 
> **Context:** The owner answered round one's question on #231: both cards show the links, so the planner's run comment mirrors the issue card. The issue card is drawn by card.render() in dokima/card.py; the run comment by render() in dokima/agent.py, whose long parts are folds drawn by the same code as the issue card (#228). Round one's tests on branch try/issue-231 (tests/test_issue_links.py, criterion 231.4: test_the_card_shows_each_kind_of_link_with_its_own_icon and test_the_card_shows_no_line_for_a_kind_with_no_links) cover the issue card and can be reused; the run comment needs its own test. The three icons are new SVG files in dokima/icons, none of them a verdict or run icon. Changing dokima/card.py needs this issue to ask for it, which it does.
> 
> **Acceptance criteria:**
> - The card at the top of the issue and of its pull request shows each kind of link the newest plan has on its own line, with its label (Blocked by, Blocks, Relates to), its issue number

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json; echo; cat in/02-reviewer-plan.json; echo; cat in/03-planner.json
```

> [
>  {
>   "id": "B1",
>   "criterion": "251.1",
>   "test": "tests/test_link_lines.py::test_the_issue_card_shows_each_kind_of_link_on_its_own_line_with_its_own_icon",
>   "problem": "The issue asks for link icons that are \"none of them a verdict or run icon\". Criterion 251.1 only says \"a different icon from the fixed icon table\", and that table also holds passed, failed, running and the other verdict and run icons. The test only checks that the three kinds use three different files from card.FIELD_ICONS. Since dokima/card.py is in scope, a worker could map \"related\" to \"passed\" in FIELD_ICONS and every test would still pass.",
>   "evidence": "Issue #251 criterion 1: \"three new SVG icons in dokima/icons, none of them a verdict or run icon\". tests/test_link_lines.py:121-122 asserts only len({card.FIELD_ICONS[f] ...}) == 3; img() at line 46 reads the icon file from FIELD_ICONS, so changing the map changes what the test expects.",
>   "fix": "Add \"none of them a verdict or run icon\" to 251.1. In the test, assert that the three kinds draw exactly blocked-by.svg, blocks.svg and related.svg, and that none of them is a verdict or run icon (card.ICON_FILE values, passed, failed, queued, running, cancelled, none).",
>   "fixer": "planner"
>  }
> ]
> {
>  "kind": "user_story",
>  "summary": "The issue card and the planner's run comment show which issues this one is blocked by, blocks and relates to, each kind with its own icon.",
>  "user_story": "The owner sees which issues this one is blocked by, b

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 -- tests/test_link_lines.py; git diff 26d548a b09b6d3 --stat; cat -n tests/test_link_lines.py; ls dokima/icons; grep -n "FIELD_ICONS\|ICON_FILE" -A12 dokima/card.py | head -60
```

> b09b6d3 planner for #251 (run 37853712537)
> 26d548a planner for #251 (run 37852116066)
>  tests/test_link_lines.py | 38 +++++++++++++++++++++++++++++++-------
>  1 file changed, 31 insertions(+), 7 deletions(-)
>      1	"""The issue card and the planner's run comment show the links, each with its icon.
>      2	
>      3	Issue #251, story 2 of #231. The planner hands back `links`: three lists of open issue numbers, `blocked_by`, `blocks` and `relates_to` (#250).
>      4	This story draws them. Each kind with at least one link gets one line: its fixed field icon from card.FIELD_ICONS
>      5	("blocked by" -> blocked-by.svg, "blocks" -> blocks.svg, "related" -> related.svg, all added by #234), right in front
>      6	of its label (Blocked by, Blocks, Relates to), then its issue numbers as #N. A kind with no links has no line, and an
>      7	older plan with no links field draws exactly as one with three empty lists.
>      8	
>      9	The issue card (dokima/card.py render, on the issue and on its pull request) draws them from the newest plan; the
>     10	planner's run comment (dokima/agent.py render) shows the very same lines, outside its folds, for a plan and for a split.
>     11	"""
>     12	import json
>     13	import os
>     14	import re
>     15	import sys
>     16	import tempfile
>     17	
>     18	import pytest
>     19	
>     20	sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
>     21	from dokima import agent, card  # noqa: E402
>     22	
>     23	REPO = "o/r"
>     24	OWNER = "boss"
>     25	BOT = "do

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_link_lines.py 2>&1 | grep -E "^E .*251|passed|failed" | head -20; python -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bagyswrgr). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/2708626f-5f4d-4be2-9973-86bfcb784e8a/tasks/bagyswrgr.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_link_lines.py 2>&1 | grep -E "^E +(Assert|.*251)|passed|failed" | head -20
```

> blocks.svg, related.svg), never a verdict or run icon such as passed, failed, queued, running or cancelled."""
> E       AssertionError: 251.1: the issue card of a user_story shows 0 link lines, not one each for ['blocked_by', 'blocks', 'relates_to']:
> E       AssertionError: 251.1: the issue card of a plan with only blocks shows 0 link lines, not one each for ['blocks']:
> E       AssertionError: 251.1: the issue card after a re-plan shows 0 link lines, not one each for ['relates_to']:
> text = '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...· 1.0 min · 3 turns · 10 tokens in, 5 out · $0.10 at API prices · [run](https://github.com/o/r/actions/runs/1)</sub>\n'
> E       AssertionError: 251.2: the planner's run comment for a user_story shows 0 link lines, not one each for ['blocked_by', 'blocks', 'relates_to']:
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> text = '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...· 1.0 min · 3 turns · 10 tokens in, 5 out · $0.10 at API prices · [run](https://github.com/o/r/actions/runs/1)</sub>\n'
> E       AssertionError: 251.2: the run comment of a plan

**Agent:** The previous blocker (B1) is fixed and all five new tests fail today for the right reason, so I'm writing the approval now.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Rewrote 251.1 so each kind of link draws its own file (blocked-by.svg, blocks.svg, related.svg), none of them a verdict or run icon, and a plan with no links field adds nothing to the card.",
          "Changed the tests to name those three files themselves, to check each link line carries only its own icon and never a verdict or run icon, and to check the link lines are the only difference from an older plan's card."],
  "decided": ["Keeps reusing the three icons #234 added instead of adding three new ones.",
              "Leaves links off a rejected planner run's comment."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves every ask of the issue, including that no link line uses a verdict or run icon, and all five tests fail today because no card or run comment draws link lines yet.",
 "blockers": [],
 "notes": [
  {"text": "The tests find a link line by the exact icon tag the card draws for that field (card.icon with the field name as its alt text), so the worker must draw the icon the way card.field_icon already does; a different alt text fails the tests even if the line looks right.",
   "evidence": "tests/test_link_lines.py:51-53 and 91-94; dokima/card.py:54."},
  {"text": "The owner's \"three new SVG icons\" is met by the three icons #234 added for exactly these kinds; they are none of the verdict or run icons, and the tests now pin those file names.",
   "evidence": "dokima/icons/blocked-by.svg, blocks.svg, related.svg; dokima/card.py:41-42; tests/test_link_lines.py:45-47, 126-129."}],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "The card at the top of the issue and of its pull request shows each kind of link the newest plan has on its own line, with its label (Blocked by, Blocks, Relates to), its issue numbers and an icon of its own", "source": "https://github.com/dokima-dev/dokima/issues/251", "criterion": "251.1"},
 
```

> rc=0

**Agent:** I approved the plan for #251. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **B1 is fixed.** Criterion 251.1 now says each kind of link uses its own icon file (`blocked-by.svg`, `blocks.svg`, `related.svg`), none of them a verdict or run icon. The tests name those three files directly instead of reading the card's icon map. They also check that each link line shows only its own icon and never passed, failed, queued, running, cancelled or none. A worker who pointed a link at the "passed" icon would now fail.
- **Last round's note is covered too.** A card with links, once its link lines are taken out, must match exactly the card of an older plan with no links. So nothing else can be added to the card.
- **All five new tests fail today for the right reason.** I ran `tests/test_link_lines.py` and each test fails with "shows 0 link lines", because no card or run comment draws link lines yet. I started the full test suite too, but it hadn't finished within two minutes when I wrote the review, so I don't have its result.
- **Every ask of the owner is covered.** I matched all five asks in the issue to 251.1 or 251.2; none is missing. The plan has no questions for the owner.
- **Two notes, neither blocking:**
  - The tests find a link line by the exact icon tag the card already draws, including its alt text. If the worker draws the icon any other way, the tests fail even when the line looks right.
  - The issue asks for "three new SVG icons". The plan reuses the three that #234 added for these same kinds instead of making new ones. Those icons are not verdict or run icons, and the tests now check the file names.

`8. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/2708626f-5f4d-4be2-9973-86bfcb784e8a/tasks/bagyswrgr.output
```

> +  where 0 = len([])
>  +  and   1 = len(['blocks'])
> 5 failed, 562 passed in 264.13s (0:04:24)
> 
> [exited with code 0]

**Agent:** The full test suite has now finished: 562 passed and 5 failed. The 5 failures are the new link tests, which are meant to fail until the worker builds the link lines. Nothing else in the repo breaks with the planner's tests in place, so the approval in `/tmp/dokima-out/review.json` stands unchanged.
