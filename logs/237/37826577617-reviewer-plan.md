# reviewer (plan) for #237

Run: https://github.com/dokima-dev/dokima/actions/runs/37826577617

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 36
> drwxr-xr-x  3 runner runner  4096 Oct  8 18:44 .
> drwxrwxrwt 18 root   root    4096 Oct  8 18:44 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 18:44 in
> -rw-r--r--  1 runner runner 12195 Oct  8 18:44 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 18:44 open_blockers.json
> -rw-r--r--  1 runner runner  4518 Oct  8 18:44 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 18:44 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 18:44 ..
> -rw-r--r-- 1 runner runner 5162 Oct  8 18:44 01-planner.json
> # Issue #237: The owner's ask reads open on the issue they wrote
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 4</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** On the issue the owner wrote, their own text shows open as the issue, folded only where it is quoted elsewhere, like a split's sub-issues.
> 
> **Context:** dokima/body.py writes the owner's part below the marker inside FOLD_START ('<details><summary>Original issue</summary>') and FOLD_END, and ask() reads it back. Existing issues already carry the fold, so reading must keep accepting it while redraws write it open. A split's stories quote the parent's story in agent.py ('<details open><summary>From the approved plan of #...'), which is the quoted-elsewhere case. AGENTS.md, 'The issue body', says the ask is folded and must be updated to match.
> 
> **Acceptance criteria:**
> - On the issue the owner wrote, thei

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat dokima/body.py; sed -n 1,90p dokima/plan.py; grep -n "From the approved plan\|def story_body" -A15 dokima/agent.py | head -60
```

> commit 213519c5c36738ca28df3d830124998a5d2095be
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 18:43:55 2026 +0000
> 
>     planner for #237 (run 37825200858)
> 
>  tests/test_body.py     |  25 +----
>  tests/test_open_ask.py | 267 +++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_planner.py  |   7 --
>  3 files changed, 270 insertions(+), 29 deletions(-)
> """The issue body: code's card above one fixed marker, the owner's ask folded below it, never rewritten.
> 
> Every code path that redraws an issue body (the card and the planner) saves it through `save`, which keeps the
> owner's part byte for byte or refuses, leaves the body as it was and says why in a comment on the issue.
> """
> import subprocess
> 
> MARKER = "<!-- dokima-ask -->"
> FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> FOLD_END = "\n\n</details>"
> 
> 
> class Refused(Exception):
>     """A redraw that would change the owner's part; its message says why."""
> 
> 
> def ask(body):
>     """The owner's part below the first marker, byte for byte; the whole body when there is no marker yet."""
>     body = body or ""
>     if MARKER not in body:
>         return body
>     below = body.split(MARKER, 1)[1]
>     if below.startswith(FOLD_START) and below.endswith(FOLD_END) and len(below) >= len(FOLD_START) + len(FOLD_END):
>         return below[len(FOLD_START):len(below) - len(FOLD_END)]
>     return below
> 
> 
> def redraw(body, top):
>     """The new body: `top` above the marker and the owner

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_open_ask.py; git show HEAD -- tests/test_body.py tests/test_planner.py
```

> """The owner's ask reads open on the issue they wrote, folded only where it is quoted from somewhere else.
> 
> Issue #237, story 4 of #230. dokima/body.py keeps the owner's part below one fixed marker. Until now every redraw
> wrapped it in a closed `<details><summary>Original issue</summary>` fold. Now the ask on an issue the owner wrote
> shows open below the card, byte for byte; an issue whose body is a split's story, quoted by code from the parent's
> approved plan (dokima/agent.py story_body), keeps the fold. Issues saved before this change carry the fold already:
> reading still accepts it, and their next redraw opens it. A redraw that would change the owner's text is still
> refused, leaving the body as it was and saying why on the issue.
> 
> GitHub is faked by the same recorder tests/test_body.py uses; the card's main runs as in those tests.
> """
> import os
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> sys.path.insert(0, os.path.dirname(__file__))
> from dokima import agent, body, plan, planner  # noqa: E402
> from test_body import NUMBER, PLAN_TOP, REPO, TRICKY, github, run_card  # noqa: E402,F401
> 
> FOLD_SUMMARY = "<summary>Original issue</summary>"
> OLD_FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> OLD_FOLD_END = "\n\n</details>"
> 
> OWNER_ASKS = ("Please keep my words open.\n- [ ] Goal: an old goal\n", TRICKY, "",
>               "<details><summary>My own fold</summary>\n\nA detail I folded myself.\n\n</details>\n")
> 
> STORY = {"ti

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_open_ask.py 2>&1 | grep -E "^(FAILED|PASSED|E  )|passed|failed" | head -60; python -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bxd2hx306). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/f4a81e3b-727f-43a8-9454-f0af97959312/tasks/bxd2hx306.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_open_ask.py -rA 2>&1 | grep -E "^(FAILED|PASSED|E   )" | head -60
```

> E       AssertionError: 237.1: the owner's ask is still folded under Original issue
> E       assert '<summary>Or...ue</summary>' not in '\n<details>...\n</details>'
> E         
> E         '<summary>Original issue</summary>' is contained here:
> E           
> E           <details><summary>Original issue</summary>
> E           
> E           Please keep my words open.
> E           - [ ] Goal: an old goal
> E           
> E           
> E           </details>
> E       AssertionError: 237.1: the owner's ask is still folded under Original issue
> E       assert '<summary>Or...ue</summary>' not in '\n<details>...\n</details>'
> E         
> E         '<summary>Original issue</summary>' is contained here:
> E           
> E           <details><summary>Original issue</summary>
> E           
> E           
> E           
> E           Please make the card keep my words.  
> E           - [ ] Goal: an old goal
> E             - [ ] Done when: an old criterion
> E               Verified by: nothing
> E           <!-- dokima-card -->
> E           </details>
> E           > quoted line
> E           **Not checked:** speed.
> E           Ünïcødé — and a trailing blank line
> E           
> E              
> E           
> E           </details>
> E       AssertionError: 237.1: the owner's ask is still folded under Original issue
> E       assert '<summary>Or...ue</summary>' not in '\n<details>...\n</details>'
> E         
> E         '<summary>Original issue</summary>' is contained here:
> E           
> E           <details><summary>Original issue</summary

**Agent:** Plan tests are running. 237.1 fails for the right reason so far (the ask is still folded); now checking the rest.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_open_ask.py -rA 2>&1 | grep -E "^(FAILED|PASSED)" ; timeout 100 python -m pytest -q tests/test_open_ask.py 2>&1 | grep -E "^E +(Assertion|Failed|[A-Za-z]+Error)" | sort | uniq -c
```

> FAILED tests/test_open_ask.py::test_the_owners_ask_shows_open_below_the_card - AssertionError: 237.1: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_the_open_ask_stays_byte_for_byte_after_many_redraws - AssertionError: 237.1: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_the_card_shows_the_owners_ask_open - AssertionError: 237.1: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_the_planner_shows_the_owners_ask_open - AssertionError: 237.1: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_an_old_folded_ask_opens_on_its_next_redraw - AssertionError: 237.2: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_the_card_opens_an_old_folded_ask - AssertionError: 237.2: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_a_split_story_stays_folded - AssertionError: 237.3: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_a_split_story_folded_today_stays_folded - AssertionError: 237.3: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_the_card_folds_a_fresh_split_story - AssertionError: 237.3: the owner's ask is still folded under Original issue
> FAILED tests/test_open_ask.py::test_a_redraw_that_would_change_the_ask_is_still_refused - AssertionError: 237.4: the owner's ask i

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "Original issue\|FOLD_START\|FOLD_END\|body\.ask\|dokima-ask" --include=*.py --include=*.yml --include=*.md . | grep -v "^./tests/test_open_ask" | head -30; grep -n "folded\|Original" AGENTS.md
```

> dokima/body.py:8:MARKER = "<!-- dokima-ask -->"
> dokima/body.py:9:FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> dokima/body.py:10:FOLD_END = "\n\n</details>"
> dokima/body.py:23:    if below.startswith(FOLD_START) and below.endswith(FOLD_END) and len(below) >= len(FOLD_START) + len(FOLD_END):
> dokima/body.py:24:        return below[len(FOLD_START):len(below) - len(FOLD_END)]
> dokima/body.py:31:    below = body.split(MARKER, 1)[1] if MARKER in body else FOLD_START + body + FOLD_END
> tests/test_body.py:214:    assert body.ask(saved) == "Please show a card.", "179.1: the owner's ask is not below the marker as written"
> tests/test_body.py:230:        assert body.ask(current) == TRICKY, f"179.2: redraw {k + 1} changed the owner's ask"
> tests/test_body.py:247:        assert body.ask(saved) == TRICKY, f"179.2: card run {k + 1} changed the owner's ask"
> tests/test_body.py:265:    assert body.ask(current) == TRICKY, "179.2: the first plan changed the owner's ask"
> tests/test_body.py:269:        assert body.ask(current) == TRICKY, f"179.2: re-plan {k + 1} changed the owner's ask"
> tests/test_body.py:287:    assert body.ask(body.redraw(current, "a card that quotes nothing")) == "My ask.", "179.3: a good redraw was refused"
> tests/test_body.py:336:    assert body.ask(github.saves[0]) == "My ask.", "179.3: a good plan post changed the owner's ask"
> tests/test_body.py:363:        assert body.ask(new) == fresh, "179.4: the whole existing body was not kept below the marker as written"
> t

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn '"issue", "create"\|issue create\|issues.*POST\|--body' dokima/*.py | head; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.keys())"
```

> dokima/agent.py:182:        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
> dokima/agent.py:1034:    gh("issue", "comment", str(number), "-R", repo, "--body", AUTOPILOT_LINE)
> dokima/agent.py:1196:        gh("issue", "comment", str(number), "-R", repo, "--body", f"Autopilot: merged PR #{pr}")
> dokima/agent.py:1211:            gh("pr", "comment", pr, "-R", repo, "--body",
> dokima/agent.py:1491:            gh("issue", "comment", parent, "-R", repo, "--body", render(rec))
> dokima/body.py:49:        gh("issue", "comment", str(number), "-R", repo, "--body",
> dokima/body.py:53:    gh("issue", "edit", str(number), "-R", repo, "--body-file", "-", input=new)
> dokima/planner.py:419:        gh("issue", "comment", number, "-R", repo, "--body", f"**Plan rejected:** {why}\n\n[See the run]({run})")
> dokima/planner.py:449:            gh("issue", "comment", number, "-R", repo, "--body", f"**Planner proposes a split**\n\n```json\n{result}\n```")
> dokima/planner.py:457:            gh("issue", "comment", number, "-R", repo, "--body",
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])

`9. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/f4a81e3b-727f-43a8-9454-f0af97959312/tasks/bxd2hx306.output
```

> E           </details>
> E       AssertionError: 237.1: the owner's ask is still folded under Original issue
> E       assert '<summary>Or...ue</summary>' not in '\n<details>...\n</details>'
> E         
> E         '<summary>Original issue</summary>' is contained here:

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned three criteria: the owner's text shows open below the card, an ask folded today opens on its next redraw, and a split's sub-issue keeps its quoted story folded.",
          "Wrote 12 tests in tests/test_open_ask.py and removed two older tests that required the ask to be folded."],
  "decided": ["Only a split's sub-issue, whose text carries 'From the approved plan of #N', counts as quoted elsewhere and stays folded.",
              "The owner's open text must never be read as the plan, so old checkboxes in it never become goals or criteria."],
  "open": ["One question to the owner: whether any issue other than a split's sub-issue counts as quoted elsewhere."]},
 "verdict": "approve",
 "summary": "The plan covers every ask of the issue with tests that each fail today because the ask is still folded, and its one question matches the owner's own words.",
 "blockers": [],
 "notes": [
  {"text": "The issue's Context says AGENTS.md, 'The issue body', must be updated to say the ask is open; AGENTS.md is in scope but no test checks it, so the code review should read that line in the diff.",
   "evidence": "AGENTS.md:84 'Below it, the owner's original ask, folded, exactly as written.'; plan.json scope lists AGENTS.md with no criterion for it"},
  {"text": "No test covers an owner's own ask that happens to mention 'From the approved plan of #'; a worker that folds on that words anywhere in the text would fold it. Folding only when the text starts with the story's fold is the safer reading.",
   "evidence": "tests/test_open_ask.py builds quoted stories only with agent.story_body (dokima/agent.py:158) and owner asks without that phrase"}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "On the issue the owner wrote, their original text shows open below the card, not folded under Original issue, and stays byte for byte as written.", "source": "https://github.com/
```

> (Bash completed with no output)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i "s/folds on that words anywhere/folds whenever those words appear anywhere/" /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 237 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo ok
```

> ok

**Agent:** I approved the plan for #237. The review is saved to `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Criteria:** Each of the issue's four asks has a criterion:
- **237.1:** the owner's text shows open below the card, byte for byte.
- **237.2:** an ask that is folded today opens on its next redraw.
- **237.3:** a split's sub-issue keeps its quoted story folded.
- **237.4:** a redraw that would change the owner's text is still refused, and the issue says why.

The plan adds one more, **237.5**: once the ask is open, old checkboxes in it must never be read as plan goals.

**Tests:** I ran the 12 new tests in `tests/test_open_ask.py` on this branch. All 12 fail for the right reason: "the owner's ask is still folded under Original issue". The 237.3 tests also check that a plain owner's ask shows open. So a change that folds everything fails them, and so does one that opens everything. The two older tests the plan deletes only required the fold, and their other checks are still covered elsewhere. I didn't wait for the full test suite to finish.

**The plan's question** was whether anything besides a split's sub-issue counts as "quoted elsewhere". I accepted the planner's answer, "only a split's sub-issue". It matches the owner's words: "Where the owner's text is quoted somewhere else, like a split's sub-issues, it stays folded." It's also the only kind of issue body code creates today (`dokima/agent.py:182`). Since #237 is on autopilot, accepting it means the issue goes on to the worker without waiting for you.

**Two notes, neither blocking:**
- The issue says AGENTS.md (line 84, which still calls the ask "folded") must be updated. AGENTS.md is in scope, but no test checks it, so the code review needs to read that line in the diff.
- No test covers an owner's ask that happens to contain the words "From the approved plan of #". A worker who folds whenever those words appear anywhere would fold that owner's text by mistake.

`12. Bash`
```
tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/f4a81e3b-727f-43a8-9454-f0af97959312/tasks/bxd2hx306.output
```

> 15 failed, 465 passed in 263.71s (0:04:23)
> 
> [exited with code 0]

`13. Bash`
```
grep -E "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/f4a81e3b-727f-43a8-9454-f0af97959312/tasks/bxd2hx306.output | grep -v test_open_ask; grep -c "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/f4a81e3b-727f-43a8-9454-f0af97959312/tasks/bxd2hx306.output
```

> 0

`14. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python -m pytest -q -p no:cacheprovider --deselect tests/test_open_ask.py -rf --ignore=tests/test_open_ask.py 2>&1 | grep -E "^FAILED|passed|failed"
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
> 3 failed, 465 passed in 266.94s (0:04:26)

`15. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat main HEAD; python3 - <<'EOF'
import json
p="/tmp/dokima-out/review.json"; r=json.load(open(p))
r["issues_found"]=[{"title":"Three hand-back check tests fail on main since the asks rule",
 "why":"The full test run is red on main for reasons unrelated to any issue, so a red run no longer tells the owner whether new work broke something.",
 "evidence":"pytest -q on try/issue-237 (which changes only test_body.py, test_planner.py and test_open_ask.py): tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner, tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named and tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests fail with 'asks must list every ask in the owner's issue and comments'"}]
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 237 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo ok
```

> tests/test_body.py     |  25 +----
>  tests/test_open_ask.py | 267 +++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_planner.py  |   7 --
>  3 files changed, 270 insertions(+), 29 deletions(-)
> ok

**Agent:** The full test run finished: 15 failed and 465 passed. The verdict on the plan is still approve.

- **12 of the 15** are the plan's own new tests in `tests/test_open_ask.py`. They fail for the right reason: the owner's ask is still folded.
- **The other 3** are tests that check the format of the reviewer's hand-back:
  - `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner`
  - `tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named`
  - `tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests`

  All three fail because the check now requires the review to list the owner's asks. This branch changes only test files, and none of these three, so they almost certainly fail on main too. I didn't run them on main to confirm.

I added these three failing tests to the review as a proposed new issue, since a full run that is always red can't show whether new work broke something. The updated `review.json` still passes both hand-back checks.
