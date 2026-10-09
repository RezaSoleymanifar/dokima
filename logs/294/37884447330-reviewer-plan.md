# reviewer (plan) for #294

Run: https://github.com/dokima-dev/dokima/actions/runs/37884447330

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #294: The Blocker pill is computed from blocked-by links, not set by hand
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 253, 254, 282 -->
> **Backlog**
> 
> [issue #294](https://github.com/dokima-dev/dokima/issues/294)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #253, #254, #282
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Today the Blocker priority on the board follows a blocker label that someone sets by hand. Now that issues carry real 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_blocker_pill.py; cat tests/test_blocker_pill.py; cat .github/workflows/board.yml; git show HEAD -- tests/test_board.py tests/test_manifest.py
```

> <persisted-output>
> Output too large (38KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/19d0c074-63d0-4263-9838-10bc39cf00e4/tool-results/b51gm6w62.txt
> 
> Preview (first 2KB):
> commit 27a1d7093fe94f7885adcaa538f93746cdfcdcda
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:33:23 2026 +0000
> 
>     planner for #294 (run 37883641801)
> 
>  tests/test_blocker_pill.py | 463 +++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_board.py        |  55 +++---
>  tests/test_manifest.py     |  10 +-
>  3 files changed, 496 insertions(+), 32 deletions(-)
> 463 tests/test_blocker_pill.py
> """The board's Blocker pill is computed from blocked-by links, never set by hand (#294).
> 
> An open issue that blocks at least one other open issue shows Priority Blocker. The board sync recomputes it when an
> issue closes or reopens and on a schedule every 15 minutes (GitHub starts no workflow when a link is added or removed),
> and the blocker label no longer moves the pill. Without Blocker, the pill follows the high or parked label as before.
> 
> Most tests fake dokima.board.Board itself and read the board's end state. What the fake Board offers, and the code is
> expected to use (the first group exists today; the second is new):
>     Board(spec, repo, q, rest)          the board
>     .fields                             {"Status": ..., "Action": ..., "Priority": (id, {option: id})}
>     .item(kind, n) / .set(item, field, option or

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_blocker_pill.py
```

> """The board's Blocker pill is computed from blocked-by links, never set by hand (#294).
> 
> An open issue that blocks at least one other open issue shows Priority Blocker. The board sync recomputes it when an
> issue closes or reopens and on a schedule every 15 minutes (GitHub starts no workflow when a link is added or removed),
> and the blocker label no longer moves the pill. Without Blocker, the pill follows the high or parked label as before.
> 
> Most tests fake dokima.board.Board itself and read the board's end state. What the fake Board offers, and the code is
> expected to use (the first group exists today; the second is new):
>     Board(spec, repo, q, rest)          the board
>     .fields                             {"Status": ..., "Action": ..., "Priority": (id, {option: id})}
>     .item(kind, n) / .set(item, field, option or None) / .value(item, field)
>     .autopilot(kind, n) / .open_pr(n) / .parent(n) / .label(kind, n, on) / .views() / .add_view(...)
> 
>     .blocking(n) -> [{"number", "state"}]     the issues n blocks, each with its state ("open" or "closed")
>     .blocked_by(n) -> [{"number", "state"}]   the issues blocking n, each with its state
>     .open_issues() -> [n, ...]                every open issue of the repo, pull requests left out
>     .labels(kind, n) -> {name, ...}           the labels the issue carries
> 
> The new reads raise subprocess.CalledProcessError when GitHub refuses, as Board's REST calls do today. The last tests
> run the real Board against a faked GitHub, so t

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/board.yml; wc -l dokima/board.py; grep -n "def \|PRIORITY\|blocker" dokima/board.py | head -80; grep -n "blocker" dokima/manifest.py
```

> name: board
> # Keeps the project board's Status and "Waiting on" current at every stage moment,
> # and its Priority in step with the blocker, high and parked labels.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [labeled, unlabeled, closed]
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   workflow_run:
>     workflows: [done-whens]
>     types: [completed]
> permissions:
>   contents: read
> concurrency:
>   group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
>   cancel-in-progress: false
> jobs:
>   sync:
>     environment: keys
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.repository.default_branch }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - id: app
>         uses: actions/create-github-app-token@v2
>         with:
>           app-id: ${{ vars.DOKIMA_APP_ID }}
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Sync the board
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           DOKIMA_BOARD: ${{ vars.DOKIMA_BOARD }}
>         run: pyth

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_blocker_pill.py 2>&1 | grep -E "Error|assert|passed|failed|^FAILED" | head -60; python -m pytest -q tests/test_board.py tests/test_manifest.py 2>&1 | tail -8; python -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bma2biug8). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/19d0c074-63d0-4263-9838-10bc39cf00e4/tasks/bma2biug8.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q -p no:cacheprovider tests/test_blocker_pill.py -rA 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed" | head -30
```

> FAILED tests/test_blocker_pill.py::test_an_issue_blocking_an_open_issue_gets_the_blocker_pill - AssertionError: 294.1: after the scheduled sync the pills are {10: None, 12: None, 14: None, 15: None, 16: None}; only open issues blocking an open issue show Blocker, and the rest follow their high or parked label
> FAILED tests/test_blocker_pill.py::test_the_scheduled_sync_writes_only_pills_that_change - AssertionError: 294.1: with only #22 wrong, the scheduled sync wrote [], not Blocker on #22 alone
> FAILED tests/test_blocker_pill.py::test_closing_the_last_blocked_issue_clears_the_pill - AssertionError: 294.2: after #31 closed the pills are {30: 'Blocker', 32: 'Blocker', 34: 'Blocker'}; #30 should lose Blocker, #32 keep it and #34 fall back to Parked
> FAILED tests/test_blocker_pill.py::test_a_closed_issue_loses_its_own_blocker_pill - AssertionError: 294.2: the closed issue #40 still shows Blocker
> FAILED tests/test_blocker_pill.py::test_reopening_an_issue_brings_the_pill_back - AssertionError: 294.2: after #51 reopened the pills are {50: None, 51: None}, not Blocker on both
> FAILED tests/test_blocker_pill.py::test_the_workflow_runs_on_close_and_reopen - AssertionError: 294.2: the board workflow's issue triggers are ['labeled', 'unlabeled', 'closed']; a close or reopen never reaches the pill
> FAILED tests/test_blocker_pill.py::test_a_link_added_or_removed_reaches_the_pill_on_the_next_scheduled_run - AssertionError: 294.3: after the link was added, #60 shows None, not Blocker
> FAILED test

**Agent:** Reading done; the 16 new tests all fail today for the right reasons. Checking the edited old tests next, then writing the review.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q -p no:cacheprovider tests/test_board.py tests/test_manifest.py 2>&1 | grep -E "^FAILED|passed|failed"; grep -n "15 min\|schedule" AGENTS.md | head
```

> FAILED tests/test_board.py::test_two_priority_labels_show_the_highest - AssertionError: 202.1: labeled parked with labels ['blocker', 'parked'] wrote ['p-Blocker'], not p-Parked
> FAILED tests/test_manifest.py::test_the_manifest_declares_every_label_dokima_uses - AssertionError: 282.1: the manifest declares the labels ['autopilot', 'blocker', 'high', 'parked', 'plan', 'work'], not plan, work, autopilot, high, parked
> 2 failed, 73 passed in 2.58s

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote four criteria and one fail-closed requirement for a Blocker pill that follows GitHub's blocked-by links, with 16 new tests and 7 changed ones."],
  "decided": ["The board run recomputes every open issue's pill on close, on reopen and on a schedule every 15 minutes; the blocker label stops counting and leaves the manifest.",
              "When GitHub cannot list an issue's links, that issue's pill stays as it is and the run fails with exit code 1 naming the issue."],
  "open": ["Whether a 15-minute delay is acceptable for a link changed by hand.", "Whether Dokima stops declaring the blocker label altogether."]},
 "verdict": "approve",
 "summary": "The plan covers all three of your asks with tests that fail today for the right reason; both of its questions change how the board works, so they are yours to answer.",
 "blockers": [],
 "notes": [
  {"text": "The work adds a reopened trigger and a 15-minute schedule to the board workflow. AGENTS.md says to change workflows only when the issue explicitly asks, and the bot cannot push workflow changes, so the owner's answer to the first question is what authorizes this change.",
   "evidence": ".github/workflows/board.yml:7 has types [labeled, unlabeled, closed] and no schedule; tests/test_blocker_pill.py::test_the_workflow_runs_every_15_minutes and ::test_the_workflow_runs_on_close_and_reopen require both."},
  {"text": "Every new test fails today on the missing feature, not on a crash: 16 failed, each naming its criterion. Of the changed old tests, two fail on the blocker label that still counts and the rest pass.",
   "evidence": "pytest -q tests/test_blocker_pill.py: 16 failed; pytest -q tests/test_board.py tests/test_manifest.py: test_two_priority_labels_show_the_highest and test_the_manifest_declares_every_label_dokima_uses fail, 73 passed."}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": 
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The plan covers your three asks with tests that fail today for the right reason; both questions change how the board works, so you decide."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 294 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #294, but did not accept either of its two questions, so on autopilot the river stops for you on those. The review is written to `/tmp/dokima-out/review.json`, and both checks on it pass.

**Coverage:** each of your three asks maps to one criterion:
- An open issue that blocks another open issue shows Blocker, computed from its links → 294.1
- The pill goes away by itself when the last blocked issue closes or the link is removed → 294.2
- No one sets or clears it by hand → 294.4

**Tests:** all 16 new tests in `tests/test_blocker_pill.py` fail today because the feature is missing, not because of a crash, and each failure names its criterion. Of the 7 old tests the plan changed, 2 fail because the blocker label still sets the pill; the other 5 pass. I couldn't get a full `pytest -q` run to finish, so I ran only those three test files.

**Questions not accepted:** both change how the board works, and your words don't settle either one.
1. **The 15-minute delay for a link changed by hand.** It adds a board run every 15 minutes, which costs Actions minutes. It also changes `.github/workflows/board.yml` by adding a reopen trigger and the schedule. AGENTS.md allows workflow changes only when the issue asks for them, so your answer here is what allows that edit.
2. **Dropping the blocker label from the manifest.** That changes which labels onboarding creates in every repo. Your issue talks about the pill, not the label.

I left no blockers and found no problems that need their own issue.

`10. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/19d0c074-63d0-4263-9838-10bc39cf00e4/tasks/bma2biug8.output
```

> 'work',
>     }
> 18 failed, 694 passed in 237.85s (0:03:57)
> 
> [exited with code 0]

**Agent:** The full test run finished: 18 failed and 694 passed. The 18 failures are the 16 new tests plus the 2 changed old tests I'd already found failing, so nothing else in the repo breaks. The review stays as it is: plan approved, both of its questions left for you to answer.
