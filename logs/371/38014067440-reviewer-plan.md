# reviewer (plan) for #371

Run: https://github.com/dokima-dev/dokima/actions/runs/38014067440

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; cat open_blockers.json; cat plan.json
```

> total 16
> drwxr-xr-x 2 runner runner 4096 Oct 10 01:40 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 01:40 ..
> -rw-r--r-- 1 runner runner 5460 Oct 10 01:40 01-planner.json
> # Issue #371: A new issue's card shows the owner's text first, the Definition of Done below it, and no 'no plan yet' line
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 372, 373 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #371](https://github.com/dokima-dev/dokima/issues/371)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #372, #373
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" al

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_new_issue_card.py; python -m pytest -q tests/test_new_issue_card.py 2>&1 | tail -40
```

> commit 2eca89c7d2788bf14f97302e934b84a0ac12d14b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 01:40:01 2026 +0000
> 
>     planner for #371 (run 38013526732)
> 
>  tests/test_card_status.py    |   8 +-
>  tests/test_new_issue_card.py | 258 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_scan.py           |   6 +-
>  3 files changed, 265 insertions(+), 7 deletions(-)
> """A new issue shows the owner's text first, then the Definition of Done, with no "no plan yet".
> 
> Issue #371. The owner asked (2026-10-09) that when an issue is first posted and has no plan yet, the Definition of
> Done line no longer comes before the owner's original issue text: it moves below that text, and the line "This issue
> has no plan yet." goes away. Since #373 the owner's text sits in a closed fold titled Original issue below the card's
> marker, so on an issue with no plan the body reads: the card's status and link lines, the Original issue fold, then the
> Definition of Done. Once the issue has a plan, the card is drawn as before, with the Definition of Done at its bottom,
> above the fold.
> 
> The card is drawn by dokima/card.py render and saved by card.draw through dokima/body.py, which keeps the owner's text
> byte for byte or refuses. These tests run card.draw with GitHub faked by the recorder in tests/test_body.py, and read
> the body it saves the way the owner reads the issue.
> """
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_new_issue_card.py 2>&1 | grep -E "^(FAILED|E   )" | cut -c1-250 | head -30; git show HEAD -- tests/test_card_status.py tests/test_scan.py; python -m pytest -q tests/test_card_status.py tests/test_scan.py 2>&1 | tail -5
```

> E               AssertionError: 371.1: with no record, the card still says it has no plan yet
> E               assert 'no plan yet' not in '<!-- dokima...ima-card -->'
> E                 
> E                 'no plan yet' is contained here:
> E                   issue has no plan yet.
> E                   
> E                   **definition of done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> all tests · <img src="https://raw.githubusercontent.com/o/r/main/doki
> E                   
> E                   <!-- /dokima-card -->
> E       AssertionError: 371.2 (no record): the Definition of Done still comes before the owner's text:
> E         <!-- dokima-card -->
> E         <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> E         **Backlog**
> E         
> E         [issue #40](https://github.com/o/r/issues/40)
> E         
> E         This issue has no plan yet.
> E         
> E         **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/n
> E         
> E         <!-- /dokima-card -->
> E         
> E         
> E       assert '**Definition of Done:**' not in '<!-- dokima...card -->\n\n'
> E         
> E         '**Definition of Done:**' is contained here:
> E           lan yet.
> E           
> E           **Definition of Do

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_new_issue_card.py 2>&1 | grep -E "^FAILED" | cut -c1-260
```

> FAILED tests/test_new_issue_card.py::test_a_card_with_no_plan_has_no_no_plan_line - AssertionError: 371.1: with no record, the card still says it has no plan yet
> FAILED tests/test_new_issue_card.py::test_a_new_issue_shows_the_owners_text_then_the_definition_of_done - AssertionError: 371.2 (no record): the Definition of Done still comes before the owner's text:
> FAILED tests/test_new_issue_card.py::test_an_issue_showing_todays_card_moves_its_definition_of_done_below - AssertionError: 371.2: the Definition of Done still comes before the owner's text:
> FAILED tests/test_new_issue_card.py::test_a_new_issues_card_is_not_rewritten_when_nothing_changed - AssertionError: 371.2: the Definition of Done still comes before the owner's text:
> FAILED tests/test_new_issue_card.py::test_a_planned_issue_keeps_its_definition_of_done_in_the_card - AssertionError: 371.3: the Definition of Done still comes before the owner's text:
> FAILED tests/test_new_issue_card.py::test_the_owners_text_is_kept_or_the_save_refused - AssertionError: 371.4: the Definition of Done still comes before the owner's text:
> FAILED tests/test_new_issue_card.py::test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text - AssertionError: 371.5: AGENTS.md's The issue body does not say an issue with no plan shows its Definition of Done below the Original issue fol

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def \(done_row\|shows\|draw\|render\|gather\|github_links\|their_links\)" dokima/card.py; grep -n "^def \|^MARKER" dokima/body.py; grep -n "def github\|TRICKY =" -A3 tests/test_body.py | head -30; grep -n "no plan yet" -r dokima | head
```

> 100:def their_links(repo, number, sources, plans=None):
> 174:def github_links(repo, number, cache):
> 418:def done_row(repo, found, all_tests):
> 434:def render(repo, issue, found, page="issue"):
> 510:def shows(current, top):
> 599:def gather(repo, number, pr_number):
> 823:def draw(repo, number, pr_number, plans=None, noted=None, cache=None, changed_only=False):
> 12:MARKER = "<!-- dokima-ask -->"
> 22:def ask(body):
> 35:def redraw(body, top):
> 47:def gh(*args, **kw):
> 51:def save(repo, number, current, top):
> 34:TRICKY = ("\r\n\r\nPlease make the card keep my words.  \r\n"
> 35-          "- [ ] Goal: an old goal\r\n"
> 36-          "  - [ ] Done when: an old criterion\r\n"
> 37-          "    Verified by: nothing\r\n"
> --
> 99:def github(monkeypatch, tmp_path):
> 100-    """A faked GitHub for the body helper and the card, run in a temp folder."""
> 101-    fake = FakeGitHub()
> 102-    monkeypatch.chdir(tmp_path)
> dokima/card.py:475:        lines += ["This issue has no plan yet.", ""]

**Agent:** I'm checking the planner's tests against the code; all seven new tests fail today for the right reason. Next I'm looking for older tests the change would break.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "no plan yet\|has no plan" tests | grep -v test_new_issue_card | head; sed -n 1,80p dokima/body.py; sed -n 418,520p dokima/card.py
```

> tests/test_autopilot_start.py:63:    #57 has no plan, no sub-issues and nothing blocking it. After the code owner's `/autopilot start` on it, #57's
> tests/test_scan.py:444:    assert "Every card says what is true." in second and "This issue has no plan yet." not in second, \
> tests/test_card_status.py:345:    """With no plan yet, the card opens with the status line.
> tests/test_card_status.py:348:    (no heading). Since #371 the card no longer says it has no plan yet: it shows the Definition of Done instead."""
> tests/test_review_asks.py:211:        assert "plan.json" in files, f"158.4: tests/samples/{n} has no plan.json to check its other hand-backs against"
> """The issue body: code's card above one marker, the owner's ask folded below, never rewritten.
> 
> Every ask, the owner's own or a split's story quoted by code from the parent's approved plan, sits folded under
> Original issue (#373). Bodies saved between #237 and #373 show the ask open: reading still accepts it, and the next
> redraw folds it.
> 
> Every code path that redraws an issue body (the card and the planner) saves it through `save`, which keeps the
> owner's part byte for byte or refuses, leaves the body as it was and says why in a comment on the issue.
> """
> import subprocess
> 
> MARKER = "<!-- dokima-ask -->"
> FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> FOLD_END = "\n\n</details>"
> OPEN_START = "\n\n"
> 
> 
> class Refused(Exception):
>     """A redraw that would change the owner's part; its message says why."""
> 
> 
> def 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rln "FOLD_END\|endswith(.*details\|body.ask\|redraw(" tests | grep -v test_new_issue_card
```

> tests/test_plan_links_recorded.py
> tests/test_parent_sweep.py
> tests/test_open_ask.py
> tests/test_card_folds.py
> tests/test_body.py
> tests/test_scan.py
> tests/card_player.py
> tests/test_card_merge.py
> tests/test_terms.py
> tests/test_hand_links.py
> tests/test_card_running.py
> tests/test_card_records.py
> tests/test_card_queue.py
> tests/test_card_sweep.py

`8. Bash`
```
rm -rf /tmp/sim && cp -r /home/runner/work/dokima/dokima /tmp/sim && cd /tmp/sim && python3 - <<'EOF'
import re
p='dokima/body.py'; s=open(p).read()
s=s.replace('OPEN_START = "\\n\\n"\n','OPEN_START = "\\n\\n"\nBELOW = "<!-- dokima-below -->"\nTAIL = FOLD_END + "\\n\\n" + BELOW\n')
s=s.replace('''    below = body.split(MARKER, 1)[1]
    if below.startswith(FOLD_START) and below.endswith(FOLD_END)''','''    below = body.split(MARKER, 1)[1]
    if below.startswith(FOLD_START) and TAIL in below:
        return below[len(FOLD_START):below.rindex(TAIL)]
    if below.startswith(FOLD_START) and below.endswith(FOLD_END)''')
s=s.replace('''    below = FOLD_START + owner + FOLD_END
    new = top.rstrip("\\n") + "\\n\\n" + MARKER + below''','''    tail = ""
    if BELOW in top:
        top, dod = top.split(BELOW, 1)
        tail = "\\n\\n" + BELOW + "\\n" + dod.strip("\\n")
    below = FOLD_START + owner + FOLD_END + tail
    new = top.rstrip("\\n") + "\\n\\n" + MARKER + below''')
open(p,'w').write(s)
p='dokima/card.py'; s=open(p).read()
s=s.replace('''        lines += ["This issue has no plan yet.", ""]
    else:''','''        pass
    else:''')
s=s.replace('''    lines += [done_row(repo, found, all_tests), "", plan.CARD_END]
    return "\\n".join(lines)''','''    if not h:
        return "\\n".join(lines + [plan.CARD_END, "", body.BELOW, done_row(repo, found, all_tests)])
    lines += [done_row(repo, found, all_tests), "", plan.CARD_END]
    return "\\n".join(lines)''')
open(p,'w').write(s)
EOF
git diff --stat; python -m pytest -q -x tests/test_new_issue_card.py 2>&1 | tail -15
```

> dokima/body.py | 10 +++++++++-
>  dokima/card.py |  4 +++-
>  2 files changed, 12 insertions(+), 2 deletions(-)
>         sentences = [s for s in re.split(r"(?<=[.;])\s+", section) if "Definition of Done" in s]
> >       assert any("no plan" in s and "below" in s and "Original issue" in s for s in sentences), \
>             "371.5: AGENTS.md's The issue body does not say an issue with no plan shows its Definition of Done below the " \
>             "Original issue fold"
> E       AssertionError: 371.5: AGENTS.md's The issue body does not say an issue with no plan shows its Definition of Done below the Original issue fold
> E       assert False
> E        +  where False = any(<generator object test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text.<locals>.<genexpr> at 0x7f49dbcdd080>)
> 
> tests/test_new_issue_card.py:254: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_new_issue_card.py::test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text - AssertionError: 371.5: AGENTS.md's The issue body does not say an issue with no plan shows its Definition of Done below the Original issue fold
> assert False
>  +  where False = any(<generator object test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text.<locals>.<genexpr> at 0x7f49dbcdd080>)
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 6 passed in 0.14s
> Shell cwd was reset to /

**Agent:** Six pass with a rough sketch, so the tests are achievable. Now the full suite on the sketch, to see which older tests break.

`9. Bash`
```
cd /tmp/sim && python -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-220; cd /home/runner/work/dokima/dokima && python -m pytest -q -p no:cacheprovider 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b5jenrmrr). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/b5jenrmrr.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`11. Bash`
```
until grep -qE "passed|failed|error" /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/b5jenrmrr.output && [ $(grep -cE "[0-9]+ (passed|failed)" /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/b5jenrmrr.output) -ge 2 ]; do sleep 2; done; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/b5jenrmrr.output
```

> Command running in background with ID: bj05p6uph. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/bj05p6uph.output. You will be notified when it completes. To check interim output, use Read on that file path.

`12. Monitor`
```
f=/tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/bj05p6uph.output; until [ -s $f ]; do sleep 3; done; grep -E "^FAILED|passed|failed" $f | cut -c1-200
```

> Monitor started (task bmjnumk33, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.

**Agent:** The full suite is still running. Once it finishes, I'll write the review.

`13. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/f1c2957a-721a-4185-abe2-839c81925f39/tasks/b5jenrmrr.output | cut -c1-220
```

> FAILED tests/test_new_issue_card.py::test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text - AssertionError: 371.5: AGENTS.md's The issue body does not say an issue with no plan shows its Definit
> 1 failed, 831 passed, 79 skipped in 201.21s (0:03:21)
> assert False
>  +  where False = any(<generator object test_agents_md_says_a_new_issues_definition_of_done_sits_below_the_owners_text.<locals>.<genexpr> at 0x7fa0531dfc60>)
> 7 failed, 825 passed, 79 skipped in 197.87s (0:03:17)
> 
> [exited with code 0]

`14. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three acceptance criteria and two non-functional requirements, with seven new tests in tests/test_new_issue_card.py, and updated three older tests that looked for the line \"This issue has no plan yet.\"."],
  "decided": ["While an issue has no plan, the card above the owner's text keeps its status and link lines, the owner's text stays in its closed Original issue fold, and the Definition of Done line goes right below that fold.",
              "Once the issue has a plan, the card is drawn as before, with the Definition of Done as its last line above the fold."],
  "open": ["Two questions for the owner: whether the text shows open or stays folded, and whether the status and link lines also move below the text."]},
 "verdict": "approve",
 "summary": "The plan covers both things the owner asked for, removing the \"no plan yet\" line and moving the Definition of Done below the owner's text, and every new test fails today because that is not built yet.",
 "blockers": [],
 "notes": [
  {"text": "The test for 371.5 needs AGENTS.md to keep the words \"Code only writes above the marker\" while also saying the Definition of Done of an issue with no plan sits below the fold. So the worker has to word that sentence as a rule with one exception, or AGENTS.md will contradict itself.",
   "evidence": "tests/test_new_issue_card.py:255-256 asserts \"Code only writes above the marker\" is still in the section next to the new below-the-fold sentence."},
  {"text": "I checked that the plan can be built. A rough version of the change in a scratch copy (render puts the Definition of Done after a separator, and body.redraw/body.ask place it and read it after the fold) passed all six code tests, and every older test still passed. So the plan's test changes are complete.",
   "evidence": "Scratch copy: 1 failed (371.5, AGENTS.md not edited), 831 passed, 79 skipped. Branch
```

`15. TaskStop`
```
{}
```

> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

> <tool_use_error>Missing required parameter: task_id</tool_use_error>

`16. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers both asks, no \"no plan yet\" line and the Definition of Done below the owner's text, and every new test fails today."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 371 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; rm -rf /tmp/sim
```

> rc=0

**Agent:** I approved the plan for [#371](https://github.com/dokima-dev/dokima/issues/371) (new issue shows the owner's text first). The review is saved as `/tmp/dokima-out/review.json` and passes both checks, the format check and the round check.

**What I checked:**
- **Your asks:** you asked for two things. Removing "This issue has no plan yet." is criterion 371.1. Putting your text first with the Definition of Done below it is criterion 371.2. Nothing you asked for is missing.
- **New tests:** all seven fail on the branch today, each because the change isn't built yet, not because of a crash or a broken setup. The full suite there gives 7 failed and 825 passed.
- **Whether it can be built:** I sketched the change roughly in a scratch copy and threw the copy away afterwards. Six of the seven new tests passed. The seventh checks AGENTS.md, which I didn't edit. Every older test still passed (831 passed, 1 failed), so the three older tests the planner rewrote are the only ones that needed it.
- **The plan's two questions:** I accepted both assumptions, and neither changes how the system works.
  - Your text stays in the closed Original issue fold, as AGENTS.md already says.
  - The status and link lines stay above your text, because you named only the Definition of Done to move.

**Notes for the worker (they don't block):**
- The AGENTS.md test still requires the words "Code only writes above the marker". The Definition of Done will now sit below the fold, so that sentence has to be reworded as a rule with one exception, or AGENTS.md will contradict itself.
- The 15-minute sweep is only tested for leaving an unchanged new issue alone. Nothing tests that it rewrites a Definition of Done below the fold that has gone out of date.
