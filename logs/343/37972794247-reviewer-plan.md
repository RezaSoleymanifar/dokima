# reviewer (plan) for #343

Run: https://github.com/dokima-dev/dokima/actions/runs/37972794247

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #343: An approved plan waiting on a blocker stays in Plan; Work means it is being built
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #343](https://github.com/dokima-dev/dokima/issues/343)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> #333's plan is approved but it waits on #332, and the board put its card in Work, though nothing is being built.
> 
> What I want:
> - An issue whose plan is approved but whose worker has not started stays in Plan. That includes an issue waiting on a blocker.
> - Work means a worker is building it, or has built it and code review ha

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_work_column.py; git show HEAD -- tests/test_board_state.py
```

> commit 3eda6dcef5176da16a5cff048c7cf1fea8c1a7ea
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 18:21:55 2026 +0000
> 
>     planner for #343 (run 37971113495)
> 
>  tests/test_board_state.py |   6 +-
>  tests/test_work_column.py | 195 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 198 insertions(+), 3 deletions(-)
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
> - after the worker's record it stays in Work until the code review starts: the bot puts up the code

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_work_column.py tests/test_board_state.py 2>&1 | grep -E "343|331|passed|failed|Error" | head -40
```

> Proves 343.1.
>         record_property("proves", "343.1")
>                 f"343.1: #57's approved plan waits on #332 and no worker started, yet after {way} its card is at " \
> E           AssertionError: 343.1: #57's approved plan waits on #332 and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not in Plan with Autopilot
> tests/test_work_column.py:85: AssertionError
>         Proves 343.1.
>         record_property("proves", "343.1")
>                     f"343.1: #{n}'s plan is approved and no worker started, yet after {way} its card is at " \
> E               AssertionError: 343.1: #57's plan is approved and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not ('Plan', 'Autopilot')
> tests/test_work_column.py:115: AssertionError
>         Proves 343.2.
>         record_property("proves", "343.2")
> >               assert got == want, f"343.2: a worker started on #{n}, yet after {way} the cards are at {got}, not {want}"
> E               AssertionError: 343.2: a worker started on #57, yet after the end of a run the cards are at {'issue #57': ('Plan', None)}, not {'issue #57': ('Work', None)}
> tests/test_work_column.py:144: AssertionError
>         Proves 343.3.
>         record_property("proves", "343.3")
> >               assert got == want, f"343.3: #57's worker has built it and {name}, yet after {way} the cards are at {got}, not {want}"
> E               AssertionError: 343.3: #57's worker has built it and nothing has started the

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn '"Work"' tests/*.py | grep -v test_work_column | head -40
```

> tests/test_agent.py:399:    assert agent.board_place(rec("reviewer", "pr", GOOD_REVIEW), ("start", "worker", "")) == ("Work", False)
> tests/test_autopilot_board.py:84:            self.fields = {"Status": ("S", {o: "s-" + o for o in ("Backlog", "Plan", "Work", "Review", "Done")}),
> tests/test_autopilot_board.py:318:    assert (w.status("issue", 139), w.action("issue", 139)) == ("Work", "Autopilot"), \
> tests/test_autopilot_board.py:481:                {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Backlog", "Plan", "Work", "Review", "Done")]},
> tests/test_autopilot_board.py:633:                           ("issue", 58): {"Status": "Work", "Action": "Autopilot"}, ("issue", 59): {"Status": "Work"}})
> tests/test_board_state.py:135:            w.cards.update({("issue", issue): {"Status": "Work"}, ("pr", pr): {"Status": "Done", "Action": NEEDS},
> tests/test_board_state.py:189:    assert got == {"issue #58": ("Work", AUTO), "pr #61": ("Work", AUTO)}, \
> tests/test_board_state.py:340:             ("pr", 61): ("Done", NEEDS), ("issue", 62): ("Work", NEEDS), ("issue", 59): ("Work", None),
> tests/test_board_state.py:341:             ("issue", 63): ("Review", AUTO), ("issue", 66): ("Work", NEEDS), ("issue", 67): ("Review", NEEDS)}
> tests/test_board_state.py:355:            "issue #59": ("Work", None), "issue #63": ("Review", AUTO), "issue #67": ("Review", NEEDS)}
> tests/test_board_state.py:380:                        ("issue", 58): {"Status": "Done"}, ("issue", 59)

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 295,325p tests/test_autopilot_board.py; sed -n 175,192p tests/test_board_state.py; sed -n 330,356p tests/test_board_state.py
```

> monkeypatch.setattr(agent, "conversation", lambda repo, n: ({}, []))
>     monkeypatch.setattr(agent, "records", lambda items: list(recs))
>     monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
>     monkeypatch.setenv("CARD_ID", "")
>     return agent.main(["agent", "split", str(parent)])
> 
> 
> def test_a_split_under_a_parent_on_autopilot_files_children_on_autopilot(record_property, make, monkeypatch):
>     """Stories filed by a split under a parent on autopilot get the autopilot label and the Autopilot pill; others don't.
> 
>     Files an approved two-story split of #139, which carries the `autopilot` label, on a board. Both new issues carry
>     the label, land in Backlog with Autopilot, and #139 shows Work with Autopilot. Then files the same split of a #139
>     not on autopilot: no new issue carries the label and no card shows Autopilot."""
>     record_property("proves", "210.2")
>     w = make(labels={("issue", 139): {LABEL}})
>     monkeypatch.setenv("DOKIMA_BOARD", "o/1")
>     assert split_main(monkeypatch, w) == 0
>     children = [n for (kind, n) in w.cards if kind == "issue" and n != 139]
>     assert sorted(children) == [201, 202], f"210.2: the split's stories were not placed on the board: {children}"
>     for n in (201, 202):
>         assert w.has("issue", n), f"210.2: story #{n}, filed under #139 on autopilot, does not carry the autopilot label"
>         assert (w.status("issue", n), w.action("issue", n)) == ("Backlog", "Autopilot"), \
>             f"210.2: story #{n} landed as {w.status('issue'

**Agent:** I've run the plan's tests: all six fail today, each for the right reason. Now I'm writing the review.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned three criteria: an approved plan stays in Plan until its worker starts, even while it waits on a blocker, and its card still says Blocked by; Work starts with the code owner's /work, the bot's Autopilot start line or the worker's run card; a built issue stays in Work until the code review's run card or record is up.",
          "Added tests/test_work_column.py with five tests and changed one expectation in tests/test_board_state.py (#64, already started with /work, now goes to Work, not Plan)."],
  "decided": ["Only the bot's own lines and run cards and a code owner's /work move a card to Work or Review; the same words from anyone else move nothing.",
              "Out of scope: the stage line on the issue card (#332), cancelled worker runs, and a filed split's parent."],
  "open": ["Asks whether the code review counts as started once its run is queued, and planned on queued."]},
 "verdict": "approve",
 "summary": "The plan covers all three of the owner's asks, and every new test fails today because the board still puts an approved plan in Work and a built issue in Review.",
 "blockers": [],
 "notes": [
  {"text": "343.3 is tested only on the first build. After a code review sends the work back and the worker builds again, the issue should again stay in Work until the next code review's run card is up. Code that moves the card to Review once any code review card exists would still pass. A second-round case would close that gap.",
   "evidence": "tests/test_work_column.py::test_a_built_issue_stays_in_work_until_its_code_review_starts uses only worker_done(), which has a single worker record and no earlier code review."},
  {"text": "The Blocked by part of 343.1 already passes today, so it only guards against that line breaking. The board part of the same test is what fails today.",
   "evidence": "tests/test_work_column.py:89-96 renders card.render with blockin
```

> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`7. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan covers all three asks, and every new test fails today because the board misplaces approved and built issues."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 343 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #343, but I didn't accept its one question's assumption, so on autopilot the river will stop and ask you. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**Why it's approved:**
- **Every ask is covered.** Your three asks each match a criterion. Staying in Plan, including while waiting on a blocker, is 343.1. What Work means is 343.2 and 343.3. The card still saying what it waits on is part of 343.1.
- **Every new test fails today for the right reason.** I ran `tests/test_work_column.py` and `tests/test_board_state.py`: 6 failed and 18 passed. Each failure is the board putting a card in the wrong column, not a crash or a bad path:
  - an approved plan, or one waiting on #332, lands in Work;
  - an issue already started with `/work` stays in Plan;
  - a built issue jumps to Review before its code review starts;
  - words someone else pastes don't fail on their own today: the test goes red only because the "waiting on #332" line already puts the card in Work.
- **One existing test changes.** In `test_board_state.py`, issue #64 moves from Plan to Work because its owner already said `/work`. That matches your ask.
- **Other tests still fit.** Existing tests that expect Work after a split or after a code review sends work back agree with the new rule.

**The question I didn't accept:** does the code review count as started once its run is queued, or only once its agent is working? The planner assumed queued is enough. Your issue says only "code review hasn't started", and that doesn't settle it. The answer decides when a card moves from Work to Review, so you need to answer it.

**Notes, none of them blocking:**
- **Second build round isn't tested.** The test only covers the first build. After a code review sends work back and the worker builds again, nothing checks that the card stays in Work until the next review starts.
- **The Blocked by check doesn't fail today.** The part checking the card still says "Blocked by #332" already passes, because the card already shows it. It only guards against that line breaking later.
- **No criterion checks AGENTS.md.** Its board rule needs rewording to match, and it's in the plan's files, but no criterion checks it.
