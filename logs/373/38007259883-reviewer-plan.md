# reviewer (plan) for #373

Run: https://github.com/dokima-dev/dokima/actions/runs/38007259883

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct 10 00:02 .
> drwxrwxrwt 18 root   root    4096 Oct 10 00:02 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 00:02 in
> -rw-r--r--  1 runner runner 10748 Oct 10 00:02 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 00:02 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 00:02 parent.json
> -rw-r--r--  1 runner runner  6991 Oct 10 00:02 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct 10 00:02 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 00:02 ..
> -rw-r--r-- 1 runner runner 7654 Oct 10 00:02 01-planner.json
> # Issue #373: Card: scope files as code on one line; original text, non-functional and out of scope folded
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #373](https://github.com/dokima-dev/dokima/issues/373)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align=

`2. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print({k:v for k,v in d.items() if k!='handback' and k!='plan'})" | head -50; cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; cat tests/test_card_folds.py
```

> {'role': 'planner', 'stage': None, 'run_id': '38006697554', 'commit_before': '39825a662f7f1107a85d897006f18f49fd757b6c', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 397159, 'turns': 30, 'cost_usd': 1.7277042000000002, 'tokens_in': 2242927, 'tokens_out': 26042}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/373/38006697554-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/38006697554', 'check': {'passed': True, 'problems': []}}
> commit 1b65f3ceece8653cb7b4047e61cdaa31e77ee15a
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 00:01:55 2026 +0000
> 
>     planner for #373 (run 38006697554)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |   8 +-
>  tests/raised_goldens/old-issue-card.md           |   8 +-
>  tests/raised_goldens/rejected-issue-card.md      |   8 +-
>  tests/test_card_folds.py                         | 241 +++++++++++++++++++++++
>  tests/test_open_ask.py                           | 159 +++------------
>  5 files changed, 279 insertions(+), 145 deletions(-)
> """Scope shows as code on one line; Out of scope, requirements and the owner's text fold.
> 
> Issue #373. The owner asked (2026-10-09) that on the issue and PR card the Scope lists its files as code fields,
> `dokima/card.py`, all on one line instead of one line per file, and that the original issue text, the non-functional
> requirements and Out of scope sit in folds, closed by default.
> 
> The

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_folds.py 2>&1 | grep -E "Error|assert|passed|failed|FAILED" | head -40; python3 -m pytest -q tests/test_open_ask.py tests/test_raised_cards.py 2>&1 | tail -15
```

> >           assert scope_lines == ["**Scope:** `dokima/card.py`, `tests/test_card.py`, `dokima/body.py::redraw`"], \
> E           AssertionError: 373.1: the issue card does not show Scope as code on one line, comma separated; its Scope lines are ['**Scope:**']
> E           assert ['**Scope:**'] == ['**Scope:** ....py::redraw`']
> tests/test_card_folds.py:88: AssertionError
> >       assert len(named) == 1, f"{k}: the {where} has {len(named)} folds titled {title!r}, expected exactly one:\n{text}"
> E       AssertionError: 373.2: the issue card has 0 folds titled 'Out of scope', expected exactly one:
> E       assert 0 == 1
> tests/test_card_folds.py:70: AssertionError
>             assert NFR[0]["text"] in inside, f"373.2: on the {where}, the requirement is not in its fold"
>             assert NFR[0]["text"] not in outside_folds(text), f"373.2: on the {where}, the requirement also shows open"
> >       assert len(named) == 1, f"{k}: the {where} has {len(named)} folds titled {title!r}, expected exactly one:\n{text}"
> E       AssertionError: 373.2: the issue card has 0 folds titled 'Out of scope', expected exactly one:
> E       assert 0 == 1
> tests/test_card_folds.py:70: AssertionError
>             assert new.split(body.MARKER, 1)[0].strip() == "the card", "373.3: the card is not alone above the marker"
> >           assert_folded("373.3", new, ask)
>     def assert_folded(k, new, ask):
>         assert new.count(body.MARKER) == 1, f"{k}: expected exactly one marker, found {new.count(body.MARKER)}"
> >     

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_folds.py 2>&1 | grep -E "^(FAILED|PASSED)|passed|failed"; python3 -m pytest -q tests/test_card_folds.py -k agents 2>&1 | grep -E "^E" | head; grep -n "Non-functional\|Out of scope\|Scope:\|Original issue" dokima/card.py dokima/body.py | head -30
```

> FAILED tests/test_card_folds.py::test_scope_shows_every_file_as_code_on_one_line - AssertionError: 373.1: the issue card does not show Scope as code on one line, comma separated; its Scope lines are ['**Scope:**']
> FAILED tests/test_card_folds.py::test_out_of_scope_sits_in_a_closed_fold - AssertionError: 373.2: the issue card has 0 folds titled 'Out of scope', expected exactly one:
> FAILED tests/test_card_folds.py::test_non_functional_requirements_sit_in_a_closed_fold_beside_out_of_scope - AssertionError: 373.2: the issue card has 0 folds titled 'Out of scope', expected exactly one:
> FAILED tests/test_card_folds.py::test_the_owners_text_is_folded_below_the_card - AssertionError: 373.3: the owner's text is not alone inside a closed Original issue fold below the card:
> FAILED tests/test_card_folds.py::test_an_open_ask_folds_on_its_next_redraw - AssertionError: 373.3: the owner's text is not alone inside a closed Original issue fold below the card:
> FAILED tests/test_card_folds.py::test_the_card_and_the_planner_fold_the_owners_text - AssertionError: 373.3: the owner's text is not alone inside a closed Original issue fold below the card:
> FAILED tests/test_card_folds.py::test_a_redraw_that_would_change_the_folded_text_is_refused - AssertionError: 373.3: the owner's text is not alone inside a closed Original issue fold below the card:
> FAILED tests/test_card_folds.py::test_agents_md_says_the_owners_text_is_folded - AssertionError: 373.4: AGENTS.md's The issue body does not say the owner'

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def pr_body" -A30 dokima/card.py; sed -n 1,40p dokima/body.py; git log --oneline -5 -- dokima/body.py; grep -rn "Original issue\|original" dokima/card.py | head
```

> 479:def pr_body(card, body):
> 480-    """The PR's description: the card, then the line linking the issue, and nothing else."""
> 481-    found = CLOSES.search(body or "")
> 482-    return card + ("\n\n" + found.group(0) if found else "")
> 483-
> 484-
> 485-def shows(current, top):
> 486-    """True when the issue body already shows `top` above its marker, as saved."""
> 487-    try:
> 488-        return body.redraw(current, top) == current
> 489-    except body.Refused:
> 490-        return False
> 491-
> 492-
> 493-def gh(*args):
> 494-    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 495-
> 496-
> 497-def issue_pr(repo, n):
> 498-    """The PR built for issue n from its try or work branch, or None."""
> 499-    owner = repo.split("/")[0]
> 500-    for branch in (f"try/issue-{n}", f"work/issue-{n}"):
> 501-        prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
> 502-        if prs:
> 503-            return prs[0]["number"]
> 504-    return None
> 505-
> 506-
> 507-def find_work(repo):
> 508-    """The issue and open PR this event is about, as (issue number, PR number or None)."""
> 509-    if os.environ.get("ISSUE_NUMBER"):
> """The issue body: code's card above one fixed marker, the owner's ask open below it, never rewritten.
> 
> A split's story, quoted by code from the parent's approved plan, stays folded under Original issue. Bodies saved
> before #237 carry the fold around every ask: reading still accepts it, and the next redraw opens an owner's ask.
> 
> Ever

**Agent:** Reviewing the plan for [#373](https://github.com/dokima-dev/dokima/issues/373) (card folds and Scope on one line): the new tests all fail today for the right reason. Now I'm writing the hand-back.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three criteria: Scope as code on one line, Out of scope and the non-functional requirements in closed folds, and the owner's text below the card in a closed Original issue fold.",
          "The planner added tests/test_card_folds.py, rewrote the open-ask checks in tests/test_open_ask.py and updated three card goldens."],
  "decided": ["The owner's text folds again, reversing the open ask from #237, and AGENTS.md's The issue body says so.",
              "Out of scope stays on the card, folded; dropping it is left out."],
  "open": ["Whether the PR card should also carry the owner's original text in an Original issue fold."]},
 "verdict": "approve",
 "summary": "The plan covers every part of the ask with tests that fail today because the feature is missing; one question, whether the PR card also gets the Original issue fold, is yours to answer.",
 "blockers": [],
 "notes": [
  {"text": "The non-functional requirements already sit in a closed fold today, so that half of 373.2 is a guard against going back, not new work; its test fails today only on the Out of scope part.",
   "evidence": "dokima/card.py:465 already draws fold(\"Non-functional requirements\", ...); tests/test_card_folds.py::test_non_functional_requirements_sit_in_a_closed_fold_beside_out_of_scope fails at the Out of scope fold check, after its requirement checks pass."},
  {"text": "The owner wrote 'non functional tests'; the plan reads this as the card's non-functional requirements section, which is the only section by that name on the card.",
   "evidence": "Issue #373 owner's words; dokima/card.py:465."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "the scope should be rendered like code fields with ` `", "source": "https://github.com/dokima-dev/dokima/issues/373", "criterion": "1.1"},
  {"ask": "all printed in a single line instead of a line per file changed", "sou
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> the ask "the scope should be rendered like code fields with ` `" is matched to 1.1, which is not a criterion of the plan (373.1, 373.2, 373.3, 373.4)
> the ask "all printed in a single line instead of a line per file changed" is matched to 1.1, which is not a criterion of the plan (373.1, 373.2, 373.3, 373.4)
> the ask "original issue should be folded" is matched to 1.3, which is not a criterion of the plan (373.1, 373.2, 373.3, 373.4)
> the ask "along with non functional tests and out of scope field" is matched to 1.2, which is not a criterion of the plan (373.1, 373.2, 373.3, 373.4)
> the ask "The owner's original issue text, the non-functional requirements and Out of scope sit in folds, closed by default." is matched to 1.2, which is not a criterion of the plan (373.1, 373.2, 373.3, 373.4)

`7. Bash`
```
cd /tmp/dokima-out; sed -i 's/"criterion": "1\./"criterion": "373./g; s/"summary": "[^"]*"/"summary": "Every part of the ask has a criterion and a test that fails today; you decide whether the PR card also gets the Original issue fold."/' review.json
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 373 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

`8. Bash`
```
cd /tmp/dokima-out; sed -i 's/"summary": "[^"]*"/"summary": "Every part of the ask has a criterion and a test that fails today; you decide whether the PR card gets the Original issue fold."/' review.json
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 373 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#373](https://github.com/dokima-dev/dokima/issues/373) (card folds and Scope on one line), but one question is held for you. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**Your question to answer:** should the PR card also carry your original issue text in an "Original issue" fold? The planner assumed not, because the PR card doesn't show that text today. I didn't accept that assumption. Your ask opens with "On the issue and PR card:" and lists the original text among the things folded there, so it can also be read as wanting the text on the PR card. Nothing you wrote settles it. Because the issue is on autopilot, this stops for you.

**Why it's approved:**
- **Every ask is covered.** Each part of your request maps to one of the plan's criteria:
  - Scope as code on one line, comma separated: 373.1.
  - Out of scope and the non-functional requirements in closed folds: 373.2.
  - Your original text folded below the card: 373.3.
- **The new tests fail for the right reason.** I ran `tests/test_card_folds.py` on this branch: all 8 fail, each because the feature isn't built yet, not because of a crash or a bad path.
- **AGENTS.md changes with it.** The plan undoes [#237](https://github.com/dokima-dev/dokima/issues/237) (shows your ask open below the card) because your newer words ask for the fold. One test checks that the "The issue body" section of AGENTS.md now says the ask is folded.
- **Old tests are updated.** The open-ask tests in `tests/test_open_ask.py` are rewritten to expect the fold. The three card examples in `tests/raised_goldens/` now show the one-line Scope and the closed Out of scope fold.

**Two notes, neither blocking:**
- The non-functional requirements are already in a closed fold today (`dokima/card.py:465`). That half of 373.2 only stops it going back, and its test fails today on the Out of scope part, not that half.
- You wrote "non functional tests". The plan reads this as the card's "Non-functional requirements" section, the only section by that name on the card.
