# reviewer (plan) for #182

Run: https://github.com/dokima-dev/dokima/actions/runs/37814813007

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ====; cat plan.json; echo ====; cat open_blockers.json
```

> <persisted-output>
> Output too large (32KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b03f5fce-15cf-4cdf-ad80-dbfc8c47f82e/tool-results/bpomi35wc.txt
> 
> Preview (first 2KB):
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  8 17:13 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 17:13 ..
> -rw-r--r-- 1 runner runner 5269 Oct  8 17:13 01-planner.json
> -rw-r--r-- 1 runner runner 6426 Oct  8 17:13 02-planner.json
> -rw-r--r-- 1 runner runner 6991 Oct  8 17:13 03-planner.json
> # Issue #182: Every run comment is a short card with the long parts in folds
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 4</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners skim every planner, worker and reviewer comment from one plain sentence on top, and open folds only for what they need.
> 
> **Context:** Keeps the run-card promises of the issue body and the 'run card says what the run did' and AGENTS.md principle promises of the owner's comment of 2026-10-07 20:16. Today dokima/agent.py render(rec) draws the record comment: a bold role name, the user story or verdict, blockers, issues found, questions, a 'What the previous step did' fold and the full JSON fold plus footnote(). It should use the same card-building code as stories 2 and 3. Reviewer blockers already name a criterion (problems_shape). Work hand-backs have summary, criteria, outside

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> # Issue #182: Every run comment is a short card with the long parts in folds
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 4</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners skim every planner, worker and reviewer comment from one plain sentence on top, and open folds only for what they need.
> 
> **Context:** Keeps the run-card promises of the issue body and the 'run card says what the run did' and AGENTS.md principle promises of the owner's comment of 2026-10-07 20:16. Today dokima/agent.py render(rec) draws the record comment: a bold role name, the user story or verdict, blockers, issues found, questions, a 'What the previous step did' fold and the full JSON fold plus footnote(). It should use the same card-building code as stories 2 and 3. Reviewer blockers already name a criterion (problems_shape). Work hand-backs have summary, criteria, outside_scope and suspect_tests. #164 (one live card per run, queued to done) is separate. The AGENTS.md principle goes under Principles. The owner's comment of 2026-10-07 23:54 adds: the reviewer card lists only the criteria it blocks on, passes stay on the main card; the worker card is one sentence plus the test result, the rest folded. That newer wording replaces the issue body's 'worker card: what it built, what it found, any blocker it raised' as the top of the card; those parts move into folds. Th

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; diff <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1))") <(python3 -c "import json;print(json.dumps(json.load(open('in/03-planner.json'))['handback'],indent=1))") | head; cd /home/runner/work/dokima/dokima; git diff main --stat; wc -l tests/test_run_cards.py
```

> [] .github/workflows/agent.yml     |  27 +-
>  .github/workflows/autopilot.yml |  47 ---
>  .github/workflows/commands.yml  |  20 +-
>  AGENTS.md                       |  10 +-
>  dokima/agent.py                 | 462 ++---------------------
>  dokima/board.py                 | 118 +-----
>  dokima/card.py                  | 189 ++--------
>  dokima/planner.py               |   2 -
>  dokima/roles/planner.md         |   4 +-
>  dokima/roles/reviewer.md        |  15 +-
>  tests/samples/132/plan.json     |   1 -
>  tests/test_agent.py             |   2 +-
>  tests/test_automerge.py         | 702 -----------------------------------
>  tests/test_autopilot.py         |  24 +-
>  tests/test_autopilot_board.py   | 796 ----------------------------------------
>  tests/test_autopilot_close.py   | 767 --------------------------------------
>  tests/test_autopilot_river.py   | 545 ---------------------------
>  tests/test_board.py             |   7 +-
>  tests/test_body.py              |   2 +-
>  tests/test_card.py              |  40 +-
>  tests/test_card_status.py       | 657 ---------------------------------
>  tests/test_failed_run_card.py   |   9 +-
>  tests/test_feature_check.py     |   2 +-
>  tests/test_plan_check.py        |   4 +-
>  tests/test_plan_shape.py        |   6 +-
>  tests/test_planner.py           |   2 +-
>  tests/test_questions.py         |   2 +-
>  tests/test_run_cards.py         | 340 +++++++++++++++++
>  tests/test_start.py             |   2 -
>  29 files changed, 447 insertions(+), 4357 deletions(-)
> 340 tests/test_

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff $(git merge-base HEAD main) --stat; cat tests/test_run_cards.py
```

> tests/test_run_cards.py | 340 ++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 340 insertions(+)
> """Every run comment is a short card the owner skims, with the long parts folded (issue #182).
> 
> A run comment is what code posts when a planner, worker or reviewer run ends (dokima/agent.py render). These tests draw
> those comments from records built the way the workflow builds them, then read them the way the owner does: the opening
> sentence, the short part on top (everything above the first fold), and the folds below it. The folds must come from the
> same code that folds the issue card (dokima/card.py fold), and the full JSON record must stay folded on every comment.
> """
> import json
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent, card  # noqa: E402
> 
> RECORD_FOLD = "<details><summary>Full record</summary>"
> FOLD = re.compile(r"<details>(.*?)</details>", re.S)
> 
> 
> def rec(role, stage="", handback=None, passed=True, problems=""):
>     """A record built the way the workflow builds one, from a temp hand-back folder."""
>     import tempfile
>     out = tempfile.mkdtemp()
>     json.dump(handback or {}, open(os.path.join(out, agent.HANDBACK[role]), "w"))
>     return agent.build_record(role, stage, out, problems, passed, {"run_id": "1", "run": "https://x/run/1"})
> 
> 
> def top(body):
>     """The short part the owner reads first: everything above the first fold."""
>     return body.split("<details")[

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_run_cards.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-400; grep -n "^def render\|^def not_started\|^def cancelled\|^def build_record\|^HANDBACK\|^def records\|def next\|\"next\"" dokima/agent.py
```

> E                 <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**
> E                   "passed": true,
> E                +  where '' = folds('<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w...\n  "passed": true,\n  "problems": []\n }\n}\n```\n\n</details>\n\n<sub>model unknown · [run](https://x/run/1)</sub>\n')
> E             <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**
> E           assert 'A slow call returns a job id within 2 s.' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**\n\nSlow calls return a job id at once.\n\n'
>         from code (no "built"), with a link to the pull request and no test result (no passed or failed, no test count).
> >           body = agent.render(rec("worker", handback=handback, passed=False, problems=why + "\n"), pr=PR)
> E         <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Worker**
> E           "evidence": "python3 -m pytest -q: 12 passed in 3.1s",
> E           "passed": true,
> E       assert (['<img src="https://raw.githubuser

**Agent:** Tests all fail for the right reason so far; now checking the worker summary format, the `agent next` fake, and the issue-card render call.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -i "summary" dokima/roles/worker.md dokima/agent.py | head -30; sed -n 1030,1090p dokima/agent.py; grep -n "^def render\|^def conversation\|^def gh" dokima/card.py dokima/agent.py
```

> dokima/roles/worker.md:43:  {"summary": "Two plain sentences: the cause and the change.",
> dokima/agent.py:157:             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
> dokima/agent.py:300:    """The comment that carries a record: a short readable summary, then the full record as JSON in a fold."""
> dokima/agent.py:308:        lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
> dokima/agent.py:317:        lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
> dokima/agent.py:331:        lines += ["", f"**{h.get('verdict')}**: {h.get('summary', '')}"]
> dokima/agent.py:343:        lines += ["", h.get("summary", "")]
> dokima/agent.py:350:        lines += ["", "<details><summary>What the previous step did</summary>", ""]
> dokima/agent.py:354:    lines += ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>",
> dokima/agent.py:496:    if not str(r.get("summary", "")).strip():
> dokima/agent.py:497:        bad.append("summary is empty")
> dokima/agent.py:551:    if not str(w.get("summary", "")).strip():
> dokima/agent.py:552:        bad.append("summary is empty")
> dokima/agent.py:601:        if not filled(h.get("summary")):
> dokima/agent.py:602:            bad.append("summary must be one non-empty sentence")
> dokima/agent.py:616:    if not filled(h.get("summ

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show $(git merge-base HEAD main):.github/workflows/agent.yml | grep -n -i -E "pr create|gh pr|agent next|agent post|comment.md|name:" | head -60
```

> 1:name: agent
> 2:run-name: "${{ (inputs.role || github.event.client_payload.role) }}${{ (inputs.role || github.event.client_payload.role) == 'reviewer' && format(' ({0})', (inputs.stage || github.event.client_payload.stage)) || '' }} for #${{ (inputs.issue || github.event.client_payload.issue) }}"
> 68:      - name: Copy the runtime from main before touching any branch
> 70:      - name: Only a code owner starts an agent
> 93:      - name: Put up the run's card, queued
> 101:          PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --json number -q '.[0].number' || true)
> 118:      - name: The card says setting up
> 129:      - name: Starting branch
> 153:      - name: Build the starting pack
> 167:      - name: Install pytest and Claude Code
> 172:      - name: All tests, run by code before the reviewer reads the pull request
> 177:      - name: Code checks the pack has everything this role needs
> 191:      - name: The card says working
> 202:      - name: The agent starts now
> 204:      - name: The agent (Claude Code)
> 240:      - name: The card says checking
> 251:      - name: Code checks the hand-back
> 257:      - name: Fence - only in-scope changes, the planner's tests as committed
> 262:      - name: Write this run's record
> 281:          cat "$OUT/comment.md" >> "$GITHUB_STEP_SUMMARY"
> 282:      - name: Remove secrets from the raw session files before they are uploaded
> 294:      - name: Save the hand-back and the full session log
> 298:          name: ${{ env.ROLE }}-${{ env

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import sys; sys.path.insert(0,'tests'); sys.path.insert(0,'.')
import test_run_cards as t
from dokima import card
found = {'recs': [t.rec('planner', handback=t.PLAN)], 'pr': None, 'check_runs': [], 'reviews': [], 'owners': [], 'tests': {}, 'worker': None}
print(card.render('o/r', {'number': 9, 'url': 'https://github.com/o/r/issues/9'}, found))
" | head -40; sed -n 140,186p dokima/card.py
```

> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **User story:** Slow calls return a job id at once.
> 
> **Acceptance criteria**
> 
> <table>
> <tr><td><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"></td><td>A slow call returns a job id within 2 s.</td></tr>
> <tr><td><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"></td><td>The job's result is kept for a day.</td></tr>
> </table>
> 
> <details><summary><b>Non-functional requirements</b></summary>
> 
> <table>
> <tr><td><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"></td><td>Jobs survive a restart-zq.</td></tr>
> </table>
> 
> </details>
> 
> **Scope:**
> 
> - dokima/jobs_zq.py
> 
> **Out of scope:**
> 
> - Cancelling a job-zq.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
>     return ("**Definition of Done:** "
>             f"{circle(repo, state(all_tests), all_tests 

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,80p dokima/roles/worker.md
```

> # Where you are
> You are Dokima's worker for one approved plan. A separate planner wrote the plan and its tests; a separate reviewer
> judges your pull request; you never see their reasoning, only what they handed back. You work on a fresh machine with
> the repo checked out on the issue's branch. Code commits, pushes and posts; you never do.
> No single model is reliable; several independent judgments checked against real records are. So nothing you say about
> your own work counts. The planner's tests, run by GitHub, are the only finish line.
> 
> # How you work
> 1. Orient before touching anything. Read the plan on the issue, AGENTS.md, then the code the plan's scope points to and
>    its callers. Never edit a file you have not read in this run: most wrong fixes come from guessing what code does.
> 2. Reproduce first. Run the plan's tests before changing anything and read every failure in full. They should all fail
>    today; if one already passes, say so in work.json.
> 3. Find the cause, not the symptom. Before editing, write one line for yourself: what is missing or wrong, where, and why
>    the failure follows from it. If you cannot write that line, read more; an edit without a cause is a guess.
> 4. Build exactly the behavior each criterion describes, as the owner wrote it, in the repo's existing style. Nothing
>    more: no refactors, renames, new files or dependencies the plan did not ask for. Every extra line is something the
>    reviewer must clear, and changes outside the plan's scope are 

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "asks\|source" dokima/agent.py | sed -n 1,60p | grep -i -n "ask\|comment" | head -30
```

> 2:487:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 3:524:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 4:528:def problems_asks(r, ids):
> 5:529:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 6:531:    asks = r.get("asks")
> 7:532:    if not isinstance(asks, list) or not asks:
> 8:533:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 10:535:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 11:536:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 12:564:        bad.append("the worker never asks the owner; the plan is the contract")
> 13:696:                bad += problems_asks(data, plan_criteria(plan, number))

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/ --deselect tests/test_run_cards.py 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b1xpd8raq). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/b03f5fce-15cf-4cdf-ad80-dbfc8c47f82e/tasks/b1xpd8raq.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_feature_check.py 2>&1 | tail -3
```

> +  where False = names('plan.json needs a summary: one plain sentence saying what the issue is about', 2)
>  +  and   False = names('plan.json needs a summary: one plain sentence saying what the issue is about', 3)
> 2 failed, 37 passed in 0.22s

**Agent:** Checks done: every new test fails today for the right reason. Writing the review.

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner changed the worker card so its one sentence is the worker's own words on what it changed, taken from the change sentence of the worker's summary, with a link to its pull request.",
          "The planner updated the worker-card and opening-sentence tests to check that sentence word for word, and that no generic line from code appears."],
  "decided": ["The worker card shows no test result; the cause sentence, the per-criterion lines, out-of-scope changes and suspect tests go in folds.",
              "dokima/card.py gets one shared fold helper that both the issue card and the run comments use."],
  "open": ["Two feature-check tests already fail on main, outside this plan."]},
 "verdict": "approve",
 "summary": "The plan covers every ask in the issue and both of the owner's later comments, and all 20 new tests fail today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 182.4 promises the reviewer's proposed issues on the card, but the test only checks for them on a passing review. A card that hid them on a blocking review would still pass.",
   "evidence": "tests/test_run_cards.py::test_the_reviewer_card_shows_pass_or_only_the_criteria_it_blocks_on checks 'Board ignores closed PRs' only for APPROVE; BLOCK has no issues_found"},
  {"text": "The worker's stopped-early case is tested only for a hand-back that code rejected. The planner card's cases for a run that never started or was cancelled are checked only for their opening word, not for why the run stopped.",
   "evidence": "tests/test_run_cards.py::test_the_worker_card_says_why_it_stopped_when_it_stopped_early; OPENINGS entries 'run that never started' and 'cancelled run'"}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [
  {"title": "Two feature-check tests fail on main since the plan check started requiring a summary",
   "why": "Main is red apart from any i
```

> rc=0

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i "s/The planner card's cases for a run that never started or was cancelled are checked only for their opening word, not for why the run stopped./A worker run that never started or was cancelled is checked only for its opening word, not for why it stopped./" /tmp/dokima-out/review.json; grep -c "never started or was cancelled" /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 182 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> 1
> rc=0

**Agent:** I approved the plan for #182, with no blockers. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner changed:** following the owner's comment of 2026-10-08 17:10, the worker card now opens with the worker's own words on what it changed. That sentence is the second half of the worker's two-sentence summary, and it links the pull request. There's no test result on the card. The worker's other details (the first sentence of its summary, its line for each criterion, changes outside the plan, tests it doubts) go in folds.

**Why it passes:**
- **Every request is covered.** I found nine requests: the five criteria in the issue, the full-record requirement, and three in the owner's later comments. Each one matches a criterion in the plan (182.1 to 182.6), and none is missing.
- **All 20 new tests fail today for the right reason.** I ran `tests/test_run_cards.py`, and every failure is because the feature doesn't exist yet: no opening sentence, no shared fold code in `dokima/card.py`, `render()` doesn't take a pull request link yet, and the AGENTS.md principle is missing. None fails from a crash or a bad path.
- **The first-round pull request link is plausible.** The workflow opens the pull request before the step that decides what follows runs, so that step can add the link to the comment.

**Gaps I noted but didn't block on:**
- **Proposed issues on a blocking review:** the test checks the reviewer's proposed issues only on a review that passes. A card that hid them on a blocking review would still pass.
- **Why a worker stopped:** the "why it stopped" check covers only a hand-back that code rejected. For a worker run that never started or was cancelled, the tests check only the opening word.

**Proposed new issue:** main is already red. Two tests in `tests/test_feature_check.py` fail on main because the plan check now requires a summary (2 failed, 37 passed). This is outside this plan's scope.

For each request I linked the issue itself, because the comment links weren't in the materials I had.

`15. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/b03f5fce-15cf-4cdf-ad80-dbfc8c47f82e/tasks/b1xpd8raq.output
```

> +     'asks must list every ask in the owner\'s issue and comments, each {"ask": '
>   +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 5 failed, 354 passed, 20 deselected in 142.62s (0:02:22)
> 
> [exited with code 0]

`16. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 280 python -m pytest -q -rf tests/ --deselect tests/test_run_cards.py 2>&1 | grep ^FAILED | cut -c1-200
```

> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_broken_feature_and_says_why - AssertionError: 156.1: rejected.txt does not say story 2 lacks its title: 'plan.json needs a summary:
> FAILED tests/test_feature_check.py::test_the_check_command_rejects_a_loop_and_says_why - AssertionError: 156.2: rejected.txt does not name story 2 or 3 (and only them) in the loop: 'plan.json needs a 
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the ow
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in th
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B

`17. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r["previous_step"]["open"]=["Two feature-check tests already fail on main, outside this plan (the planner's count; there are five)."]
r["issues_found"]=[
 {"title":"Two feature-check tests fail on main since the plan check started requiring a summary",
  "why":"Main is red apart from any issue, so every PR's All tests check fails on these tests.",
  "evidence":"tests/test_feature_check.py::test_the_check_command_rejects_a_broken_feature_and_says_why and ::test_the_check_command_rejects_a_loop_and_says_why fail: 'plan.json needs a summary: one plain sentence saying what the issue is about'"},
 {"title":"Three review-check tests fail on main since a plan review must list the owner's asks",
  "why":"Their sample review.json files have no asks list, so the check rejects reviews the tests expect to pass, and main stays red.",
  "evidence":"tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner, tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named and ::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests fail: 'asks must list every ask in the owner's issue and comments'"}]
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 182 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I ran the full test suite, and main fails 5 of its own tests, not just the 2 the planner mentioned. I've updated the review to say so. It's still an approval: none of the 5 are in this issue's tests, and its 20 new tests still fail only because the feature hasn't been built yet. The updated `/tmp/dokima-out/review.json` passes both checks.

The 5 failures (354 others pass) come from two newer rules that some older tests haven't caught up with:
- **Plans must now have a summary:** two tests in `tests/test_feature_check.py` fail with "plan.json needs a summary".
- **Plan reviews must now list the owner's requests:** three tests fail because their sample reviews have no such list:
  - `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner`
  - two in `tests/test_handback_check.py`

I've proposed each group as its own new issue. Until they're fixed, the "All tests" check will fail on every pull request.
