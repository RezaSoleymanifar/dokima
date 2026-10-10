# reviewer (plan) for #373

Run: https://github.com/dokima-dev/dokima/actions/runs/38011328737

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (40.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3834f1a8-a619-4306-bef4-d04c6115b390/tool-results/bh2pasc0q.txt
> 
> Preview (first 2KB):
> total 32
> drwxr-xr-x 2 runner runner  4096 Oct 10 00:59 .
> drwxr-xr-x 3 runner runner  4096 Oct 10 00:59 ..
> -rw-r--r-- 1 runner runner  7654 Oct 10 00:59 01-planner.json
> -rw-r--r-- 1 runner runner  3625 Oct 10 00:59 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10416 Oct 10 00:59 03-planner.json
> # Issue #373: Card: scope files as code on one line; original text, non-functional and out of scope folded
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 354 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> The card shows Scope as code on one line and folds Out of scope, the non-functional requirements and the owner's original text.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #373](https://github.com/dokima-dev/dokima/issues/373)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #371, #84, #230, #354
> 
> **User story:** Owners read a shorter card on every issue and pull request: Scope fits on one line as code, and the parts they rarely read (their own original text, the 

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-original/,$p' issue.md | head -300; grep -n "dokima-card-end\|<!-- dokima" issue.md | head
```

> 3:<!-- dokima-card -->
> 4:<!-- dokima-linked-from: 354 -->
> 5:<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> 56:<!-- dokima-ask -->
> 82:<!-- dokima-record -->
> 170:<!-- dokima-record -->
> 226:<!-- dokima-record -->
> 321:<!-- dokima-live -->
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 56,90p issue.md; echo ...; sed -n 300,400p issue.md
```

> <!-- dokima-ask -->
> 
> On the issue and PR card:
> - Scope lists its files as code (`dokima/card.py`, `tests/test_card.py`) on one line, separated by commas, not one line per file.
> - The owner's original issue text, the non-functional requirements and Out of scope sit in folds, closed by default.
> 
> Owner's words (2026-10-09): "the scope should be rendered like code fields with ` ` ... and all printed in a single line instead of a line per file changed. original issue should be folded along with non functional tests and out of scope field. (not sure if out of scope was pulling weight at all on the cards since it was just prose)"
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #373 (2026-10-09T23:54:27Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #373 (2026-10-09T23:54:47Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #373 (2026-10-09T23:54:49Z)
> 
> Autopilot is on for #373. Planning started for #373, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #373 (2026-10-09T23:54:59Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue and asks you 1 question.
> 
> **User story:** Owners read a shorter card on every issue and pull request: Scope fits on one line as code, 

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d,indent=1))"
```

> {
>  "kind": "user_story",
>  "summary": "The card shows Scope as code on one line and folds Out of scope, the requirements and the owner's text, on issue and PR alike.",
>  "user_story": "Owners read a shorter card on every issue and pull request: Scope fits on one line as code, and the parts they rarely read (their own original text, the non-functional requirements and Out of scope) wait in closed folds, the same on both.",
>  "acceptance_criteria": [
>   {
>    "text": "On the issue and PR cards, Scope lists every file as code on one line, separated by commas. Files keep the plan's order, e.g. **Scope:** `dokima/card.py`, `tests/test_card.py`.",
>    "source": "https://github.com/dokima-dev/dokima/issues/373"
>   },
>   {
>    "text": "On the issue and PR cards, Out of scope and the non-functional requirements each sit in their own closed fold. None of their text shows outside it, and Scope stays open.",
>    "source": "https://github.com/dokima-dev/dokima/issues/373"
>   },
>   {
>    "text": "The owner's original issue text sits below the card in a closed fold titled Original issue, byte for byte, the same on the issue and its PR. On the PR it sits between the card and the Closes line. This holds on a new issue, on an issue whose text shows open today and on a PR drawn before this change (from their next redraw), and on a split's sub-issue, whether the card or the planner saves it. A redraw that would change that text is still refused and says why.",
>    "source": "https://github.com/dokima-dev/doki

`5. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; python3 -c "
import json;d=json.load(open('in/03-planner.json'));h=d['handback'];print(d.get('started_by'));print(json.dumps(h.get('questions'),indent=1));print(json.dumps(h.get('replies'),indent=1));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1))"
```

> 67:### RezaSoleymanifar on issue #373 (2026-10-09T23:54:27Z)
> 71:### dokima-runtime on issue #373 (2026-10-09T23:54:47Z)
> 75:### dokima-runtime on issue #373 (2026-10-09T23:54:49Z)
> 80:### dokima-runtime on issue #373 (2026-10-09T23:54:59Z)
> 168:### dokima-runtime on issue #373 (2026-10-10T00:02:10Z)
> 220:### RezaSoleymanifar on issue #373 (2026-10-10T00:48:02Z)
> 224:### dokima-runtime on issue #373 (2026-10-10T00:48:21Z)
> 319:### dokima-runtime on issue #373 (2026-10-10T00:58:54Z)
> RezaSoleymanifar
> null
> []
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38010597110",
>  "commit_before": "1b65f3ceece8653cb7b4047e61cdaa31e77ee15a",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 591222,
>   "turns": 31,
>   "cost_usd": 1.7059467999999998,
>   "tokens_in": 2424462,
>   "tokens_out": 25884
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/373/38010597110-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38010597110",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> Shell cwd was reset to /home/runner/work/dokima/dokima

`6. Bash`
```
cd /tmp/pack; sed -n 168,230p issue.md
```

> ### dokima-runtime on issue #373 (2026-10-10T00:02:10Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer passed the plan.
> 
> **The plan's assumptions:**
> - Should the PR card also carry your original issue text in an Original issue fold, or is folding it on the issue enough? Not accepted: The ask opens with 'On the issue and PR card:' and lists the original issue text among what sits in folds there, so it can be read as also wanting the text on the PR card; no words of the owner say the PR card goes without it.
> 
> <details><summary><b>Details</b></summary>
> 
> - Every part of the ask has a criterion and a test that fails today; you decide whether the PR card gets the Original issue fold.
> 
> </details>
> 
> <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/note.svg" width="16" height="16" align="absmiddle" alt="note"> Notes</b></summary>
> 
> - The non-functional requirements already sit in a closed fold today, so that half of 373.2 is a guard against going back, not new work; its test fails today only on the Out of scope part. (dokima/card.py:465 already draws fold("Non-functional requirements", ...); tests/test_card_folds.py::test_non_functional_requiremen

**Agent:** Reading done; the owner answered the PR-fold question. Now running the planner's tests.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -2 | head -40; timeout 600 python3 -m pytest -q tests/test_card_folds.py 2>&1 | tail -40
```

> commit ffcfed6b0cae5cd9827436016d048a221041625c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 00:58:42 2026 +0000
> 
>     planner for #373 (run 38010597110)
> 
>  tests/test_card.py       |   5 +-
>  tests/test_card_folds.py | 144 +++++++++++++++++++++++++++++++++++++++++++----
>  tests/test_scan.py       |   3 +-
>  3 files changed, 140 insertions(+), 12 deletions(-)
> 
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
>   '\n\nMy ask.'
> assert '\n\nMy ask.' == '\n<details><...n\n</details>'
>   
>     
>   - <details><summary>Original issue</summary>
>     
>   - My ask.
>   ?        -
>   + My ask.
>   - 
>   - </details>
> FAILED tests/test_card_folds.py::test_the_pr_card_carries_the_same_original_issue_fold - AssertionError: 373.3: the owner's text is not alone inside a closed Original issue fold below the card:
>   '\n\nPlease fold my words.\n- [ ] Goal: an old goal\n'
> assert '\n\nPlease f...an old goal\n' == '\n<det

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_card_folds.py 2>&1 | grep -E "^(FAILED|E  )" | head -40; cat tests/test_card_folds.py
```

> E           AssertionError: 373.1: the issue card does not show Scope as code on one line, comma separated; its Scope lines are ['**Scope:**']
> E           assert ['**Scope:**'] == ['**Scope:** ....py::redraw`']
> E             
> E             At index 0 diff: '**Scope:**' != '**Scope:** `dokima/card.py`, `tests/test_card.py`, `dokima/body.py::redraw`'
> E             
> E             Full diff:
> E               [
> E             +     '**Scope:**',
> E             -     '**Scope:** `dokima/card.py`, `tests/test_card.py`, '
> E             -     '`dokima/body.py::redraw`',
> E               ]
> E       AssertionError: 373.2: the issue card has 0 folds titled 'Out of scope', expected exactly one:
> E         <!-- dokima-card -->
> E         Cards fold what the owner rarely reads.
> E         
> E         **Plan**
> E         
> E         [issue #40](https://github.com/o/r/issues/40)
> E         
> E         **User story:** The owner reads a short card.
> E         
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> E         
> E         - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Scope shows on one line.
> E           - <a href="https://github.com/o/r/issues/40">Source</a>
> E         
> E         <details><summary><b>Non-functional requirements</b></summary>
> E

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def story_body" -A30 dokima/agent.py | head -50; grep -n "Original issue\|def redraw\|def ask\|FOLD" dokima/body.py | head -30
```

> 228:def story_body(parent, i, story, parent_title):
> 229-    """A story's issue body, drawn by code from the approved plan, so the child planner starts from exactly what was agreed."""
> 230-    lines = ["<!-- dokima-card -->", "<!-- /dokima-card -->", "",
> 231-             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
> 232-             f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
> 233-    if story.get("context"):
> 234-        lines += [f"**Context:** {story['context']}", ""]
> 235-    lines += ["**Acceptance criteria:**"]
> 236-    lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
> 237-    if story.get("non_functional"):
> 238-        lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', '')})" for n in story["non_functional"]]
> 239-    return "\n".join(lines + ["", "</details>"]) + "\n"
> 240-
> 241-
> 242-def file_split(repo, parent, recs, labels=()):
> 243-    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
> 244-    each created with the given labels.
> 245-
> 246-    Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
> 247-    done = latest(recs, "split", passed=True)
> 248-    if done:
> 249-        return done
> 250-    plan = latest(recs, "planner")["handback"]
> 251-    title = json.loa

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -x -p no:cacheprovider tests 2>&1 | tail -5; timeout 900 python3 -m pytest -q tests 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-200
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b3ojexli7). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/3834f1a8-a619-4306-bef4-d04c6115b390/tasks/b3ojexli7.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, checking the scan/card test changes and goldens.

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 1b65f3c ffcfed6 -- tests/test_card.py tests/test_scan.py; git diff 39825a6 1b65f3c -- tests/raised_goldens/old-issue-card.md; grep -n "def pr_body" -A15 dokima/card.py
```

> diff --git a/tests/test_card.py b/tests/test_card.py
> index 8bf40a1..f23a251 100644
> --- a/tests/test_card.py
> +++ b/tests/test_card.py
> @@ -115,7 +115,10 @@ def test_card_says_criteria_and_is_read_back_as_the_plan(record_property):
>  def test_same_card_on_issue_and_pr_and_only_icons_change(record_property):
>      record_property("proves", "67.6")
>      assert render(checks=[], pr=None) != render()
> -    assert card.pr_body(render(), "Closes #40.\n\nSome prose.") == render() + "\n\nCloses #40"
> +    # Since #373 the PR also carries the owner's text in a closed Original issue fold between the card and Closes #40.
> +    pr = card.pr_body(render(), "Closes #40.\n\nSome prose.", "My ask.")
> +    assert pr.startswith(render()) and pr.endswith("\n\nCloses #40") and "Some prose." not in pr
> +    assert "\n<details><summary>Original issue</summary>\n\nMy ask.\n\n</details>" in pr
>      src = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "card.py")).read()
>      assert 'f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md"' in src
>      yml = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "card.yml")).read()
> diff --git a/tests/test_scan.py b/tests/test_scan.py
> index a616585..0b291d1 100644
> --- a/tests/test_scan.py
> +++ b/tests/test_scan.py
> @@ -313,7 +313,8 @@ def make_true(w, *items):
>      for kind, n in items:
>          text = scan.card_now(REPO, kind, n)
>          if kind == "pr":
> -            w.prs[n]["body"] = card.pr_body(text, w.prs[n]["body"])
> +       

`12. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/3834f1a8-a619-4306-bef4-d04c6115b390/tasks/b3ojexli7.output | tail -30
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/3834f1a8-a619-4306-bef4-d04c6115b390/tasks/b3ojexli7.output tail -30. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`13. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "pr_body\|ask(" dokima/scan.py dokima/card.py | head -20
```

> dokima/card.py:479:def pr_body(card, body):
> dokima/card.py:824:    if pr and not (changed_only and pr_body(top, pr.get("body")) == (pr.get("body") or "")):
> dokima/card.py:826:            f.write(pr_body(top, pr.get("body")))
> dokima/scan.py:75:        stale = card.pr_body(top, current) != current

`14. Bash`
```
f=/tmp/claude-1001/-home-runner-work-dokima-dokima/3834f1a8-a619-4306-bef4-d04c6115b390/tasks/b3ojexli7.output; until grep -qE "[0-9]+ (passed|failed)" <(tail -3 $f) && [ $(grep -cE "[0-9]+ (passed|failed)" $f) -ge 2 ]; do sleep 5; done; grep -E "^FAILED|passed|failed" $f | cut -c1-220
```

> FAILED tests/test_card.py::test_same_card_on_issue_and_pr_and_only_icons_change - TypeError: pr_body() takes 2 positional arguments but 3 were given
> 1 failed, 173 passed, 33 skipped in 47.23s
>         Draws the issue card of a pull request whose code review passed but whose criterion check and All tests failed,
>         and checks it is byte for byte today's card, kept in tests/raised_goldens/, with the failed marks and Needs you:
>         See why not every check passed. Then draws it again with the review raising one issue, and checks the Raised
>         section holds that one raise and no failing check, while the failed marks and the to-do stay as they were.
> E         - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **Acceptance criterion:** <a href="https://x/check/1">A
> E         - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Non-functional requirement:** <a href="https://x/chec
> E         **Definition of Done:** <a href="https://x/check/3"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> A
> E           **Definition of Done:** <a href="https://x/check/3"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a>
>         byte today's, with its 

**Agent:** Every new test fails today because the feature is missing (no crashes, no bad paths). The owner's answer is carried into 373.3. Writing the hand-back.

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned after the owner's answer: the PR card now carries the owner's text in the same closed Original issue fold, between the card and the Closes line (373.3).",
          "The planner added tests for the PR fold, for older PR cards gaining it on their next redraw, and for the owner's closing words on the PR closing nothing; it updated the PR checks in tests/test_card.py and tests/test_scan.py."],
  "decided": ["On the PR copy, a '#' right after a closing keyword in the owner's text is written '&#35;', so only the PR's own Closes line closes an issue (373.5).",
              "Out of scope stays on the card, folded; dropping it is left out."],
  "open": []},
 "verdict": "approve",
 "summary": "Every part of your ask, including your answer that the PR card carries the same Original issue fold, has a criterion and a test that fails today because the work is not built yet.",
 "blockers": [],
 "notes": [
  {"text": "373.5 is the planner's own safeguard, not your words: on the PR, the owner's 'fixes #99' is written 'fixes &#35;99', so the PR's copy shows the same but is not byte for byte the issue's for text with closing words. Whether GitHub ignores the escaped form can only be seen on a real merge.",
   "evidence": "plan.json non_functional[1]; tests/test_card_folds.py::test_the_owners_closing_words_on_the_pr_close_nothing expects 'This fixes &#35;99.' on the PR and the raw text on the issue."},
  {"text": "The non-functional requirements already sit in a closed fold today, so that half of 373.2 guards against going back; its test fails today only on the Out of scope fold.",
   "evidence": "dokima/card.py draws fold(\"Non-functional requirements\", ...); pytest: test_non_functional_requirements_sit_in_a_closed_fold_beside_out_of_scope fails with \"the issue card has 0 folds titled 'Out of scope'\"."},
  {"text": "All 25 failing tests on this branch fail on 
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`16. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Every part of your ask, including the PR card's Original issue fold, has a criterion and a test that fails today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 373 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#373](https://github.com/dokima-dev/dokima/issues/373) (Scope as code on one line; Original issue, non-functional requirements and Out of scope folded). The hand-back is in `/tmp/dokima-out/review.json`, and both checks on it pass.

- **The asks:** I found six things you asked for and each one has a criterion. That includes your 2026-10-10 answer: the PR card carries the same closed Original issue fold, between the card and the Closes line (373.3). There were no open blockers from the last round.
- **The tests:** the full suite on this branch gives 25 failed, 790 passed, 79 skipped. All 25 fail because the feature isn't built yet, not because something crashes or a path is wrong. The 11 new tests in `tests/test_card_folds.py` fail on their own checks. The updated checks in `tests/test_card.py` and `tests/test_scan.py` fail with a TypeError, because the function that writes the PR description doesn't take your text yet.

I left three notes, none blocking:
- **The planner added 373.5 itself; it's not in your words.** When your text is copied onto the PR, a `#` right after a closing word is escaped. So "fixes #99" is written "fixes &#35;99". It looks the same, but means the PR copy isn't byte for byte the issue's text. Only a real merge can show that GitHub then ignores it and doesn't close #99.
- **Half of 373.2 is already true.** The non-functional requirements already sit in a closed fold, so that part only stops it from coming undone. Its test fails today only because Out of scope isn't folded yet.
- **I recorded the test results above** as the third note.
