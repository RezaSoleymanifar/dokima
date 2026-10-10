# reviewer (plan) for #354

Run: https://github.com/dokima-dev/dokima/actions/runs/38007332385

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #354: The words Acceptance criterion carry the link, not the criterion's text
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #354](https://github.com/dokima-dev/dokima/issues/354)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> On every card, the label "Acceptance criterion" is the link to the check that proves it; the criterion's own text after it is plain, unlinked text.
> 
> Owner's words (2026-10-09): "the acceptance criterion text itself, little the word acceptance criterion shou

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_card_criterion_label.py; git show HEAD -- tests/test_card_bullets.py tests/test_card_records.py tests/raised_goldens | head -300
```

> commit 4ae60baa844c9102085961331fccc37685837fbb
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 00:02:56 2026 +0000
> 
>     planner for #354 (run 38006702494)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |   4 +-
>  tests/test_card_bullets.py                       |  43 +++---
>  tests/test_card_criterion_label.py               | 158 +++++++++++++++++++++++
>  tests/test_card_records.py                       |  21 ++-
>  4 files changed, 197 insertions(+), 29 deletions(-)
> """On every card, a criterion's label links to its check; its text stays plain.
> 
> Issue #354. The owner: "the word acceptance criterion should get the hyperlink, not the description in front of it."
> 
> The card is drawn by `dokima/card.py` (render, from `found`). Each criterion is one bullet:
> 
>     - <status icon> **<a href="check">Acceptance criterion</a>:** the criterion's text
> 
> The status icon is never inside a link, the only link on the bullet sits on the label's words (with or without its
> colon), and the criterion's text after it is plain. With no check there is no link at all. Non-functional
> requirements, in their fold, read the same with the label Non-functional requirement. Markdown links `[text](url)` and
> HTML links `<a href="url">text</a>` are read alike.
> """
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import card, plan  # noqa: E402
> 
> REPO = "o/r"
> ISSUE = {"number": 40, "u

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py 2>&1 | tail -30; grep -n "Acceptance criterion\|Non-functional requirement" dokima/*.py | head -30
```

> </details>
>   
>   **Scope:**
>   
>   - dokima/agent.py
>   
>   **Out of scope:**
>   
>   - The board.
>   
>   **Definition of Done:** <a href="https://x/check/3"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> All tests · <a href="https://github.com/o/r/actions/runs/7"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
>   
>   <!-- /dokima-card -->
> assert '<!-- dokima-...kima-card -->' == '<!-- dokima-...kima-card -->'
>   
>   Skipping 1047 identical leading characters in diff, use -v to show
>   Skipping 934 identical trailing characters in diff, use -v to show
>   - ailed"> **<a href="https://x/check/1">Acceptance criterion</a>:** A slow call returns a job id.
>   + ailed"> **Acceptance criterion:** <a href="https://x/check/1">A slow call returns a job id.</a>
>       - <a href="https://github.com/o/r/issues/299">Source</a>
>     
>     <details><summary><b>Non-functional requirements<

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py 2>&1 | grep -E "^(FAILED|E  .*(354|235|180))" | head -40; grep -n "def criteria_list" -A30 dokima/card.py
```

> E       AssertionError: 354.1: the link on the bullet of “First thing works” is on “First thing works”, not on the words Acceptance criterion: - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** <a href="https://github.com/o/r/actions/runs/2/job/1">First thing works</a>
> E       AssertionError: 354.1: the link on the bullet of “First thing works” is on “First thing works”, not on the words Acceptance criterion: - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/running.svg" width="16" height="16" align="absmiddle" alt="running"> **Acceptance criterion:** <a href="https://github.com/o/r/actions/runs/2/job/1">First thing works</a>
> E       AssertionError: 354.1: the link on the bullet of “First thing works” is on “First thing works”, not on the words Acceptance criterion: - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Acceptance criterion:** <a href="https://github.com/o/r/actions/runs/2/job/1">First thing works</a>
> E       AssertionError: 354.1: the link on the bullet of “First thing works” is on “First thing works”, not on the words Acceptance criterion: - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **Acceptance criterion:** <a href="https://github.com/o/r/actions/runs/2/job/

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def criterion_item" -A25 dokima/card.py; grep -rn "render(" dokima/*.py | grep -v "def render" | head; grep -rn "criterion" dokima/*.py | grep -v "^dokima/card.py" | grep -i "href\|link" | head
```

> 353:def criterion_item(repo, label, c, check, tests):
> 354-    """One criterion as a bullet: its status circle, its label and its words, linked to its check when there is one;
> 355-    under it one italic Verified by line per test with a docstring, only the words Verified by linking to the test,
> 356-    then Source linking to where the owner asked for it, when it has one."""
> 357-    words = escape(c.get("text"))
> 358-    if check:
> 359-        words = f'<a href="{check["html_url"]}">{words}</a>'
> 360-    out = [f"- {circle(repo, state(check))} **{label}:** {words}"]
> 361-    for t in tests:
> 362-        if t and t.get("verified_by"):
> 363-            out.append(f'  - *<a href="{t["url"]}">{field_icon(repo, "verified by")} Verified by</a>: '
> 364-                       f'{escape(t["verified_by"])}*')
> 365-    if c.get("source"):
> 366-        out.append(f'  - <a href="{c["source"]}">Source</a>')
> 367-    return out
> 368-
> 369-
> 370-def criteria_list(repo, number, start, label, criteria, plan_tests, by_key, tests):
> 371-    """The bullet list of criteria numbered from `start`, each with its own check and tests."""
> 372-    out = []
> 373-    for k, c in enumerate(criteria, start):
> 374-        key = f"{number}.{k}"
> 375-        out += criterion_item(repo, label, c, by_key.get(key), [tests.get(t) for t in plan_tests.get(key, [])])
> 376-    return out
> 377-
> 378-
> dokima/agent.py:1921:        open(os.path.join(out, "comment.md"), "w").write(render(rec, plan=plan if isinstance(plan, dict) else None,
> dokima

**Agent:** I'm checking the planner's tests and the card code; next I'll write the review.

`6. Bash`
```
cd /tmp/pack; cat parent.json | head -20; python3 -c "import json;d=json.load(open('in/01-planner.json'));print(d.get('check'))"; cd /home/runner/work/dokima/dokima; python3 -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b96noe06d). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/9ab112fb-5422-4833-ad18-11af8ce8aba1/tasks/b96noe06d.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
head -30 /tmp/claude-1001/-home-runner-work-dokima-dokima/9ab112fb-5422-4833-ad18-11af8ce8aba1/tasks/b96noe06d.output
```

> {"number": 230}{'passed': True, 'problems': []}

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned two criteria: the words Acceptance criterion link to the criterion's check with its text plain, and the same for Non-functional requirement.",
          "Wrote three new tests in tests/test_card_criterion_label.py and updated the link helpers of tests/test_card_bullets.py, tests/test_card_records.py and one golden card to read the link on the label."],
  "decided": ["The status icon is never linked, and a criterion with no check has no link at all.",
              "The Verified by and Source lines stay as they are; cards on GitHub change on their next redraw, with no backfill."],
  "open": ["Asks whether Non-functional requirement bullets move the link to their label too; it planned that they do (354.2)."]},
 "verdict": "approve",
 "summary": "The plan moves the link from each criterion's text to the words Acceptance criterion, and its new tests fail today because the text still carries the link; one question, on the Non-functional requirement bullets, is the owner's to answer.",
 "blockers": [],
 "notes": [
  {"text": "Every new and updated test fails today for the right reason: the link is still on the criterion's text, not on its label.",
   "evidence": "pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py: 17 failed, 45 passed; each failure reads e.g. '354.1: the link on the bullet of “First thing works” is on “First thing works”, not on the words Acceptance criterion'."},
  {"text": "Both issue and pull request cards are drawn by the same criterion_item in dokima/card.py, so one change there covers 'every card'; the issue asks for this card change, so editing card.py is in bounds.",
   "evidence": "dokima/card.py:353-367 builds '**{label}:** <a href=check>{words}</a>' for both labels; scan.py and card.py main both call card.render."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": 
```

> Exit code 1
> summary holds 39 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan moves each criterion's link onto the words Acceptance criterion, its tests fail today for that reason, and its one question goes to the owner."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 354 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

**Agent:** I approved the plan for [#354](https://github.com/dokima-dev/dokima/issues/354) (put the link on the words "Acceptance criterion", not on the criterion's text) with no blockers. Both checks on my review pass. My review is in `/tmp/dokima-out/review.json`.

- **The plan:** criterion 354.1 moves each criterion's link off its text and onto the words "Acceptance criterion". The status icon is never linked, and a criterion with no check has no link at all. Criterion 354.2 does the same for "Non-functional requirement". The planner also updated the older card tests and one saved example card that expected the link on the text.
- **The tests:** I ran the four card test files: 17 failed and 45 passed. Every failure is for the right reason: the link is still on the criterion's text. The new tests would also fail if the icon or the text stayed linked. Issue cards and pull request cards are drawn by the same code in `dokima/card.py:353`, so one change covers "every card". I didn't wait for the full test suite to finish.
- **Your asks:** I found three places where you asked for this, and all of them map to 354.1. None is missing.
- **The question goes to you:** the planner asked whether the "Non-functional requirement" bullets should move their link to the label too, and planned that they do. I didn't accept that assumption. Your words only name "Acceptance criterion", so whether 354.2 belongs in this issue is your call. Because the issue is on autopilot, the river will stop and wait for you. Reply `/plan` with your answer, or `/review` to go ahead with the planner's reading.

`10. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/9ab112fb-5422-4833-ad18-11af8ce8aba1/tasks/b96noe06d.output
```

> </detai
> 17 failed, 799 passed, 79 skipped in 139.53s (0:02:19)
> 
> [exited with code 0]

**Agent:** The full test suite has now finished: 17 failed, 799 passed and 79 skipped. That's the same 17 failures I got from the four card test files on their own. All of them fail only because the link is still on the criterion's text, so nothing else in the repo breaks on the planner's branch. My approval stands.
