# reviewer (plan) for #343

Run: https://github.com/dokima-dev/dokima/actions/runs/37975523092

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #343: An approved plan waiting on a blocker stays in Plan; Work means it is being built
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> The board keeps an approved plan in Plan until its worker starts, and shows Work only while a worker builds it.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #343](https://github.com/dokima-dev/dokima/issues/343)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #332, #333, #313
> 
> **User story:** The owner sees in Work only the issues a worker is actually building, and an approved plan that waits for its worker, or for a blocker, stays in Plan with its card saying what it waits on.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** An approved plan whose worker has not started stays in Plan, also while it waits on a blocker. Its issue card still says Blocked by with the issues it waits on.
>   -

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_work_column.py; git diff 3eda6dc d05f215 --stat; timeout 600 python -m pytest -q tests/test_work_column.py 2>&1 | tail -30
```

> """An approved plan stays in Plan until its worker starts; Work means building (#343).
> 
> Before this, the board placed an issue from its newest record and the river's next step alone. On autopilot an
> approved plan's next step is "start the worker", so #333, whose approved plan waits on #332, sat in Work though
> nothing was being built. The other way round, an issue the owner started with `/work` stayed in Plan while its worker
> built it, and a finished worker's issue jumped to Review before its code review had started.
> 
> The rule these tests hold the board to, for an open issue and its open pull request:
> - an approved plan whose worker has not started is in Plan, also while it waits on a blocker, and its card still
>   names what it waits on;
> - a worker has started once the code owner says `/work`, the bot posts the Autopilot line that starts it
>   (`Autopilot: plan approved, starting work` or `Autopilot: blockers closed, starting work`) or the bot puts up the
>   worker's run card; from then the issue is in Work;
> - after the worker's record it stays in Work until the code review starts: the bot puts up the code review's run card
>   (queued is enough) or posts its record; then it is in Review;
> - only the bot's own lines and run cards, and a code owner's `/work`, count: anyone can comment on a public repo.
> 
> The tests run against test_needs_you's in-memory world, wired by test_board_state's `make` fixture: dokima.board.Board
> and agent's `gh` are faked, and the history is a list where a p

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_work_column.py 2>&1 | grep -E "^(FAILED|ERROR)"; git diff main -- tests/test_board_state.py | head -40; timeout 900 python -m pytest -q -x tests/test_board_state.py 2>&1 | tail -5
```

> FAILED tests/test_work_column.py::test_an_approved_plan_waiting_on_a_blocker_stays_in_plan_and_its_card_names_the_blocker - AssertionError: 343.1: #57's approved plan waits on #332 and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not in Plan with Autopilot
> FAILED tests/test_work_column.py::test_an_approved_plan_stays_in_plan_until_its_worker_starts - AssertionError: 343.1: #57's plan is approved and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not ('Plan', 'Autopilot')
> FAILED tests/test_work_column.py::test_an_issue_is_in_work_once_its_worker_starts - AssertionError: 343.2: a worker started on #57, yet after the end of a run the cards are at {'issue #57': ('Plan', None)}, not {'issue #57': ('Work', None)}
> FAILED tests/test_work_column.py::test_a_built_issue_stays_in_work_until_its_code_review_starts - AssertionError: 343.3: #57's worker has built it and nothing has started the code review, yet after the end of a run the cards are at {'issue #57': ('Review', None), 'pr #60': ('Review', None)}, not {'issue #57': ('Work', None), 'pr #60': ('Work', None)}
> FAILED tests/test_work_column.py::test_words_anyone_could_paste_start_no_worker_and_no_code_review - AssertionError: 343.4: on #57 someone-else wrote '/work', which starts nothing, yet after the end of a run its card is at ('Work', 'Autopilot'), not in Plan with Autopilot
> FAILED tests/test_work_column.py::test_a_rebuilt_issue_stays_in_work_until_its_ne

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["Re-planned after the owner's answer: a code review has started once its run card is up, even queued, and the issue then sits in Review.",
  "Added a test that an issue sent back by code review stays in Work through the rebuild until the next code review's run card is up."],
 "decided": ["Kept the three criteria and the rule that only the bot's own lines and run cards and a code owner's /work move a card to Work or Review."],
 "open": []},
 "verdict": "approve",
 "summary": "The plan now follows the owner's answer that a queued code review counts as started, covers a rebuild, and all six new tests fail today because the board misplaces the cards.",
 "blockers": [],
 "notes": [
  {"text": "The Blocked by part of 343.1 already passes today, so that half of the test only guards against the line breaking; the board half is what fails today.",
   "evidence": "tests/test_work_column.py: card.render with blocking {'blocked_by': [332]} asserts '**Blocked by:** #332'; the test fails earlier, on the board place ('Work', 'Autopilot')."},
  {"text": "AGENTS.md's board rule ('in the column the river placed it in after its newest record') is in scope and should be reworded to the new rule; no test checks it.",
   "evidence": "AGENTS.md, The board, first bullet; plan.json scope lists AGENTS.md."}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "An issue whose plan is approved but whose worker has not started stays in Plan. That includes an issue waiting on a blocker.", "source": "https://github.com/dokima-dev/dokima/issues/343", "criterion": "343.1"},
  {"ask": "Work means a worker is building it, or has built it and code review hasn't started.", "source": "https://github.com/dokima-dev/dokima/issues/343", "criterion": "343.2"},
  {"ask": "The card still says what it waits on.", "source": "https://github.com/dokima-dev/dokima/issues/343", "criterion": "343.1"},
  {"ask": "Co
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan follows the owner's answer that a queued code review counts as started, covers a rebuild, and every new test fails today."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 343 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #343. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What changed since the last round:** the owner answered the open question with "Code review counts as started as soon as its run is queued: the card moves to Review then." The plan now says this in criterion 343.3. It also covers the case from my earlier note: when a code review sends the work back, the issue stays in Work through the rebuild until the next code review is queued. There's a new test for that.

**Tests:** I ran the six new tests on this branch and they all fail today, each because the board puts the card in the wrong column:
- approved plans sit in Work when they should be in Plan;
- an issue started with `/work` stays in Plan;
- built issues jump to Review before their code review is queued.

The one changed expectation in `tests/test_board_state.py` (issue #64 moves to Work instead of Plan) also fails today for that reason.

**Owner's asks:** I found four, and each one maps to a criterion: three from the issue text (343.1, 343.2, 343.1) and the owner's `/plan` answer (343.3). The plan has no open questions this round, so I didn't need to judge any assumptions. There were no open blockers to resolve.

**Notes I left (not blockers):**
- The "Blocked by" half of 343.1's first test already passes today, so it only guards that line against breaking. The board half is what fails.
- The board rule in `AGENTS.md` still describes the old placement ("in the column the river placed it in after its newest record"). The file is in scope and should be reworded, but no test checks it.
