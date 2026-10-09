# reviewer (plan) for #299

Run: https://github.com/dokima-dev/dokima/actions/runs/37889866273

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (78.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/ef568e2a-3708-40cd-b188-867cd58cb4f1/tool-results/bsozi47g2.txt
> 
> Preview (first 2KB):
> .:
> total 96
> drwxr-xr-x  3 runner runner  4096 Oct  9 05:42 .
> drwxrwxrwt 18 root   root    4096 Oct  9 05:42 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 05:42 in
> -rw-r--r--  1 runner runner 72286 Oct  9 05:42 issue.md
> -rw-r--r--  1 runner runner  1695 Oct  9 05:42 open_blockers.json
> -rw-r--r--  1 runner runner  5874 Oct  9 05:42 plan.json
> 
> in:
> total 48
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:42 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:42 ..
> -rw-r--r-- 1 runner runner 5244 Oct  9 05:42 01-planner.json
> -rw-r--r-- 1 runner runner 7570 Oct  9 05:42 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6727 Oct  9 05:42 03-planner.json
> -rw-r--r-- 1 runner runner 6870 Oct  9 05:42 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6514 Oct  9 05:42 05-planner.json
> # Issue #299: Cards show what was raised and how each earlier raise was answered
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298 -->
> **Backlog**
> 
> [issue #299](https://github.com/dokima-dev/dokima/issues/299)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298
> 
> This issue has no plan yet.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; wc -c issue.md; grep -n "^## \|^### \|^---" issue.md | head -80
```

> {
>  "kind": "user_story",
>  "summary": "Run comments and the issue card show what an agent raised in one Raised section, and a review shows how it answered earlier raises.",
>  "user_story": "The owner reads every question, blocker and issue a run raised in one Raised section that says who each one is for, and on a review sees how each earlier raise was answered, without ever seeing an ID.",
>  "acceptance_criteria": [
>   {
>    "text": "A run comment shows one Raised section with every raise of the run. The issue card shows one Raised section with every raise on the issue still waiting for an answer, from every run, and a raise leaves it only once it is answered, done or disagree. Each line opens with its kind's icon (question, blocker or issue), shows its label when it has one, and says who it is for: you, the planner, the worker, or filed as an issue. A run that raised nothing shows no Raised section on its comment, and the issue card shows none only when every raise has an answer.",
>    "source": "https://github.com/dokima-dev/dokima/issues/299"
>   },
>   {
>    "text": "No card shows a raise's or an answer's ID; only the full record keeps them.",
>    "source": "https://github.com/dokima-dev/dokima/issues/299"
>   },
>   {
>    "text": "A review card shows what earlier steps raised in its own Raised earlier section, apart from what this review raises. Each earlier raise shows the reviewer's answer: done or disagree, and why. An answer given for you on autopilot quotes your words and links wher

`3. Bash`
```
cd /tmp/pack; sed -n 1,48p issue.md; sed -n 410,420p issue.md; sed -n 785,795p issue.md; sed -n 960,1100p issue.md | head -60
```

> # Issue #299: Cards show what was raised and how each earlier raise was answered
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298 -->
> **Backlog**
> 
> [issue #299](https://github.com/dokima-dev/dokima/issues/299)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 2</summary>
> 
> **Part of:** #289 Every agent raises thin

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['02-reviewer-plan.json','04-reviewer-plan.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:7000]); print('=====')
"
```

> 02-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37886599269",
>  "commit_before": "51cf1d924b6922ab3678ce35d2e4d9734968daea",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 5855,
>   "turns": 2,
>   "cost_usd": 0.7518587999999999,
>   "tokens_in": 135775,
>   "tokens_out": 312
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/299/37886599269-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37886599269",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner wrote five criteria for one Raised section, no IDs on cards, a Raised earlier section on review cards, old records kept as posted, and what code detects kept in its place.",
>     "The planner added 13 tests in tests/test_raised_cards.py and nine golden files of what today's code draws."
>    ],
>    "decided": [
>     "The issue card shows the raises of the newest run only.",
>     "A rejected hand-back shows none of its raises."
>    ],
>    "open": [
>     "Two questions for the owner: which run the issue card's Raised section draws, and whether a rejected run shows its raises."
>    ]
>   },
>   "verdict": "block",
>   "summary": "Criterion 5 drops part of the owner's list of what code detects, and no test keeps Outside the plan in place for new records.",
>   "blockers": [
>    {
>     "id": "B1",
>     "criterion": "299.5",
>     "test": "tests/test_raised_cards.py::test_what_code_detects_never_enters_the_raised_section",
>  

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; python -m pytest -q tests/test_raised_cards.py 2>&1 | tail -30
```

> commit f6753f8ed70eaff1db66d2f31164dd166fe3b31c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:42:20 2026 +0000
> 
>     planner for #299 (run 37889655207)
> 
>  tests/test_raised_cards.py | 63 ++++++++++++++++++++++++++++++----------------
>  1 file changed, 42 insertions(+), 21 deletions(-)
> 
> commit 32d5f3392d5e0de669349a6c89bb94490bb29a8e
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:34:11 2026 +0000
> 
>     planner for #299 (run 37888531909)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |  33 +++++++
>  tests/raised_goldens/merge-failed.md             |  38 ++++++++
>  tests/test_raised_cards.py                       | 114 ++++++++++++++++++++---
>  3 files changed, 170 insertions(+), 15 deletions(-)
> 
> commit 51cf1d924b6922ab3678ce35d2e4d9734968daea
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:01:10 2026 +0000
> 
>     planner for #299 (run 37884628736)
> 
>  tests/raised_goldens/cancelled.md           |  35 ++
>  tests/raised_goldens/clash.md               |  31 ++
>  tests/raised_goldens/not-started.md         |  38 +++
>  tests/raised_goldens/old-issue-card.md      |  33 ++
>  tests/raised_goldens/old-planner.md         | 122 +++++++
>  tests/raised_goldens/old-review.md          | 123 +++++++
>  tests/raised_goldens/old-worker.md          |  78 +++++
>  tests/raised_goldens/rejected-issue-card.md |  33 ++
>  tests/raised_goldens/r

**Agent:** Reviewing the planner's third plan for #299: all 23 tests fail today. Next I'm checking the rewritten issue-card test against the owner's answer.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show f6753f8 | head -200; python -m pytest -q tests/test_raised_cards.py 2>&1 | grep -E "^FAILED"
```

> commit f6753f8ed70eaff1db66d2f31164dd166fe3b31c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:42:20 2026 +0000
> 
>     planner for #299 (run 37889655207)
> 
> diff --git a/tests/test_raised_cards.py b/tests/test_raised_cards.py
> index f36d8b7..b937671 100644
> --- a/tests/test_raised_cards.py
> +++ b/tests/test_raised_cards.py
> @@ -12,7 +12,8 @@ What the code these tests run must do, as the plan pins it:
>  - `agent.render(rec, pr=None, plan=None, earlier=None)`: `earlier` is the issue's records before this one, oldest
>    first; an answer finds the raise it answers there by its ID. The workflow's record step,
>    `python3 -m dokima.agent record ROLE STAGE OUT CHECK PASSED LOGS`, passes the records in `$PACK/in/` as `earlier`.
> -- `card.render(repo, issue, found)`: the issue card shows the raises of the newest record, when its hand-back passed.
> +- `card.render(repo, issue, found)`: the issue card shows every raise on the issue still waiting for an answer, from
> +  every record whose hand-back passed; a raise leaves it once a passed record answers its ID, done or disagree.
>  - A rejected hand-back's raises are not drawn: its comment and the issue card stay as today, showing why it was
>    rejected.
>  
> @@ -269,28 +270,48 @@ def test_a_run_that_raised_nothing_shows_no_raised_section(record_property, env)
>      assert headings(agent.render(NEW_PLANNER), "Raised:"), "299.1: a planner run with raises shows no Raised section"
>  
>  
> -def test_the_is

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 20,200p tests/test_raised_cards.py
```

> How the tests read a card:
> - A section is a heading line whose bold text is exactly "Raised:" (this run's raises) or "Raised earlier:" (what
>   earlier steps raised, answered here), icons allowed in front, then its list: every line after the heading up to the
>   first non-empty line that is neither a list item ("- ") nor indented under one. An item is a "- " line with the
>   indented lines under it.
> - A raise's line opens, right after "- ", with its kind's icon: the <img> of card.field_icon for "question",
>   "blocker" or "issue found". It holds the label when there is one, the text, and exactly one of: "for you", "for the
>   planner", "for the worker", "filed as an issue".
> - An answer's item holds "Done" or "Disagree" and the why; an answer given for the owner on autopilot also holds a
>   markdown link whose text holds the owner's words and whose target is where they said them.
> - The full record fold, "<details><summary>Full record</summary>...</details>", is the record itself and is not
>   read as the card.
> 
> The golden files in tests/raised_goldens/ are what today's code draws for records posted before this change and for
> what code detects (a rejected hand-back, a clash with main, red main, a failed merge of main, a cancelled run, and the
> issue card of failing tests); they must stay byte for byte the same.
> """
> import copy
> import json
> import os
> import re
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote the owner's answer into criterion 1: the issue card shows every raise still waiting for an answer, from every run, and a raise leaves only once it is answered, done or disagree.",
          "The planner rewrote the issue card test to follow raises across a planner, a quiet run, a worker, a review that answers two, a rejected review and a review that answers the rest."],
  "decided": ["A rejected hand-back's raises are not drawn, and its answers take no raise off the issue card."],
  "open": ["One question for the owner: whether a rejected run still shows what it raised, planned as no."]},
 "verdict": "approve",
 "summary": "The plan now keeps every unanswered raise on the issue card, as the owner asked, and every test fails today because the feature is missing.",
 "blockers": [],
 "notes": [{"text": "All 23 tests fail today. The 299.4 and 299.5 goldens match today's drawing on purpose, and each of those tests then fails on the check that a newer record draws Raised, so they fail for the right reason.",
            "evidence": "pytest -q tests/test_raised_cards.py: 23 failed in 0.64s; test_the_issue_card_shows_every_raise_still_waiting_for_an_answer fails on 'after the planner's run, the issue card must have exactly one Raised section'."}],
 "outside_plan": [],
 "resolved": ["B2"],
 "issues_found": [],
 "asks": [
  {"ask": "A run comment and the issue card show one Raised section with every raise of the run. Each line opens with its kind's icon (question, blocker or issue), shows its label when it has one, and says who it is for: you, the planner, the worker, or filed as an issue.", "source": "https://github.com/dokima-dev/dokima/issues/299", "criterion": "299.1"},
  {"ask": "A run that raised nothing shows no Raised section.", "source": "https://github.com/dokima-dev/dokima/issues/299", "criterion": "299.1"},
  {"ask": "No card shows a raise's or an a
```

> rc=0

**Agent:** I approved the third plan for #299. The hand-back is in `/tmp/dokima-out/review.json` and passed both checks.

- **Blocker B2 is fixed.** You asked for the issue card to show every raise still waiting for an answer. Criterion 1 now says exactly that: raises from every run stay on the card until they get an answer, either "done" or "disagree". The planner dropped the question that asked this again.
- **The rewritten test follows the raises from one run to the next:**
  - A planner's raises stay after a later run that raised nothing.
  - The planner's and the worker's raises show together.
  - A review that answers two raises takes those two off, keeps the unanswered one, and adds its own four.
  - A review whose hand-back was rejected takes nothing off.
  - The Raised section disappears only once every raise has an answer.
- **All 23 tests fail on this branch, each because the feature isn't built yet.** None fails on a crash or a bad path. The tests that compare against today's saved drawings match them on purpose, then fail on their next check, that a newer record shows a Raised section.
- **I accepted the one remaining question:** "Should a run whose hand-back code rejected still show what it raised?" The plan says no. That matches your rule that what code detects, including a rejected hand-back, "keeps its own name, icon and place on the card, exactly as today, and never appears in the Raised section". On autopilot this goes ahead without asking you.

I matched all 11 of your asks to a criterion, including your two answers from 05:25 and 05:39, so none is missing. I linked each to the issue itself, because the pack doesn't give individual comment links.
