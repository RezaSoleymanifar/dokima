# reviewer (plan) for #254

Run: https://github.com/dokima-dev/dokima/actions/runs/37873942151

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct  9 02:18 .
> drwxrwxrwt 18 root   root    4096 Oct  9 02:18 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 02:18 in
> -rw-r--r--  1 runner runner 14174 Oct  9 02:18 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 02:18 open_blockers.json
> -rw-r--r--  1 runner runner  4573 Oct  9 02:18 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  9 02:18 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 02:18 ..
> -rw-r--r-- 1 runner runner 5217 Oct  9 02:18 01-planner.json
> # Issue #254: A link added or removed by hand on GitHub updates the cards of both issues
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 5</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.
> 
> **Context:** The owner's answer on #231 (19:21): "a link I add or remove by hand on GitHub also updates the cards of both issues, the same as links from an approved plan." GitHub's only native link is blocked-by (read by blocked_by() in dokima/agent.py, REST repos/{repo}/issues/{n}/dependencies/blocked_by and .../blocking); relates-to has no native form, so a hand-made link here is always blocked-by. No workflow today runs when a dependency changes: card.yml runs on issues opened/edited and workflow_r

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_hand_links.py
```

> commit 70679e1f6f4e5df89599bebcd43f999e6d89386a
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:18:12 2026 +0000
> 
>     planner for #254 (run 37872687021)
> 
>  tests/test_hand_links.py | 391 +++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 391 insertions(+)
> """A blocked-by link added or removed by hand shows on both cards (#254).
> 
> Story 5 of #231.
> 
> GitHub Actions has no event for a blocked-by link being added or removed, so the cards catch up on a schedule: card.yml
> runs `python3 dokima/card.py` on a cron, and on that event (GITHUB_EVENT_NAME=schedule, no ISSUE_NUMBER) card.py
> sweeps every open issue. It reads GitHub's own blocked-by links (GET repos/o/r/issues/N/dependencies/blocked_by and
> .../blocking) and redraws the card of each issue whose blocking links, or loop of issues blocking each other, differ
> from what its card shows. Every redraw, the sweep's or card.yml's own with ISSUE_NUMBER, draws the Blocked by and
> Blocks lines from GitHub's links read right then.
> 
> Every test runs the real `python3 dokima/card.py` as a subprocess against the fake GitHub of
> tests/test_plan_links_recorded.py (a `gh` first on PATH keeping its state in one JSON file), extended here with two
> things: GitHub failing to list one issue's blocked-by links (state "unreadable": {issue: GitHub's error}), and a
> project board reached through dokima.board.Board's own GraphQL calls, as DOKIMA_BOARD="o/1" names it, whose Action
> writes are l

`3. Bash`
```
cd /home/runner/work/dokima/dokima; diff <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json')),indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/in/01-planner.json'))['handback'],indent=1,sort_keys=True))") | head; python3 -m pytest -q tests/test_hand_links.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|Error" | head -40
```

> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> E         KeyError: 'HEAD_SHA'
> E        +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3', 'dokima/card.py'], returncode=1, stdout=...                     ~~~~~~~~~~^^^^^^^^^^^^\n  File "<frozen os>", line 714, in __getitem__\nKeyError: \'HEAD_SHA\'\n').returncode
> tests/test_hand_links.py:127: AssertionError
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> E         KeyError: 'HEAD_SHA'
> E        +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3', 'dokima/card.py'], returncode=1, stdout=...                     ~~~~~~~~~~^^^^^^^^^^^^\n  File "<frozen os>", line 714, in __getitem__\nKeyError: \'HEAD_SHA\'\n').returncode
> tests/test_hand_links.py:127: AssertionError
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> E         KeyError: 'HEAD_SHA'
> E        +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3', 'dokima/card.py'], returncode=1, stdout=...                     ~~~~~~~~~~^^^^^^^^^^^^\n  File "<frozen os>", line 714, in __getitem__\nKe

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_hand_links.py 2>&1 | tail -15; python3 -m pytest -q -x 2>&1 | tail -3; cat .github/workflows/card.yml; grep -n "HEAD_SHA\|GITHUB_EVENT_NAME\|def main\|ISSUE_NUMBER" dokima/card.py | head -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b3pj0cr15). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/b3pj0cr15.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/card.yml; grep -n "HEAD_SHA\|GITHUB_EVENT_NAME\|def main\|ISSUE_NUMBER\|blocked_by\|dependencies" dokima/card.py | head -40
```

> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, or a person opens or edits an issue. These triggers always use
> # the default branch's copy of this file and of dokima/card.py, so the work being
> # judged cannot change how it is reported.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [completed]
>   issues:
>     types: [opened, edited]
> concurrency:
>   group: card
>   cancel-in-progress: false
> permissions:
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   card:
>     environment: keys
>     # The bot's own edits (the card itself) don't trigger another card.
>     if: github.event_name != 'issues' || github.event.action == 'opened' || github.event.sender.type != 'Bot'
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>       # The card is posted by the repo's Dokima app, so it shows as that app's bot.
>       - id: app
>         uses: actions/create-github-app-token@v2
>         with:
>           app-id: ${{ vars.DOKIMA_APP_ID }}
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Write the card
>         env:
>           ISSUE_NUMBER: ${{ github.event.issue.number }}
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           REPO: ${{ github.repository }}
>           HEAD_SHA: ${{ github.event.workflow_run.head_sha }}
>           PR_NUMBER: ${{ github.event.workflow_run.pull_requests[0].number }}
>           RUN_TITLE: ${{ github.event.work

**Agent:** Checking the full test run; the plan's tests look sound so far.

`6. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/b3pj0cr15.output | tail -20
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/b3pj0cr15.output tail -20. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 110 python3 -m pytest -q tests/test_hand_links.py -p no:cacheprovider 2>&1 | grep -E "^(FAILED|PASSED)|passed|failed" | cut -c1-200
```

> f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.1: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
>                                    f"failed instead of sweeping the cards: {p.stderr[-1500:]}")
> E       AssertionError: 254.2: the scheduled run of card.yml (`python3 dok

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote two acceptance criteria and three non-functional requirements, with 12 tests in tests/test_hand_links.py that run the real card.py against a fake GitHub."],
  "decided": ["Cards catch up on a schedule: card.yml runs by itself at least every 15 minutes and checks every open issue's blocked-by links, because GitHub Actions gets no event when such a link changes.",
              "A scheduled run rewrites only the cards whose links or loop changed; on autopilot a loop of issues blocking each other gets one comment mentioning the owner and the Needs you pill on each issue in it."],
  "open": ["The planner asks whether cards catching up within about 15 minutes is fine."]},
 "verdict": "approve",
 "summary": "The plan covers every ask of this story with tests that fail today because the feature is missing; its one question, a 15-minute schedule, adds a job that runs all day and is yours to decide.",
 "blockers": [],
 "notes": [
  {"text": "The loop tests check that a card's loop line names at least the issues in the loop, so a line that also named an issue outside the loop would still pass.",
   "evidence": "tests/test_hand_links.py uses numbers(line) >= {N, 301, 302}; only #303's own card is checked for no loop line."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "When a person adds a blocked-by link by hand on GitHub (#A blocked by #B), with no command, the card of #A shows #B on its Blocked by line and the card of #B shows #A on its Blocks line", "source": "https://github.com/dokima-dev/dokima/issues/254", "criterion": "254.1"},
  {"ask": "when the person removes it, neither card shows it any more. No comment is posted on either issue for the link.", "source": "https://github.com/dokima-dev/dokima/issues/254", "criterion": "254.1"},
  {"ask": "When a link added by hand makes two issues block each other, directly or through other issues, 
```

> Exit code 1
> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers every ask with tests failing today for the right reason; its 15-minute schedule adds an all-day job, so that choice is yours."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 254 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #254, but I didn't accept its one question, so it stops for you on that.

**Why it passes:**
- All seven things you asked for in the issue map to a criterion:
  - A link added by hand shows on both cards, and a removed one leaves both.
  - No comment is posted for the link.
  - A loop of issues blocking each other is named on the cards, and on autopilot it stops for you.
  - The links are read from GitHub each time a card is drawn.
  - The card says when GitHub can't list them.
  - Cards update by themselves.
- I ran the 12 new tests in `tests/test_hand_links.py`. They all fail today because the feature doesn't exist yet: `card.py` has no scheduled run, and `card.yml` has no schedule. None of them fail because of a broken test setup.

**The question I didn't accept:** GitHub Actions gets no event when a blocked-by link changes, so the planner has `card.yml` run every 15 minutes and check every open issue's links. That's about 96 runs a day, which changes both how the system works and what it costs. Your words only say the cards show the change "by themselves" and never say how late they may catch up. So whether a delay of up to about 15 minutes is fine is your call.

**One minor note:** the loop tests check that a card names at least the issues in the loop. A card that also named an issue outside the loop would still pass.

My verdict is in `/tmp/dokima-out/review.json`, and both hand-back checks pass on it.

`10. Bash`
```
grep -E "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/b3pj0cr15.output | tail -3
```

> FAILED tests/test_hand_links.py::test_the_scheduled_run_redraws_only_cards_whose_links_changed - AssertionError: 254.5: the scheduled run of card.yml (`python3 dokima/card.py`, event schedule) failed instead of sweeping the cards: Traceback (most recent call last):
> 12 failed in 3.31s
> 1 failed, 335 passed in 187.71s (0:03:07)

`11. Bash`
```
grep -E "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/b3pj0cr15.output | tail -1 | cut -c1-120
```

> FAILED tests/test_hand_links.py::test_the_scheduled_run_redraws_only_cards_whose_links_changed - AssertionError: 254.5:

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 280 python3 -m pytest -q -p no:cacheprovider --ignore=tests/test_hand_links.py 2>&1 | tail -3
```

> Exit code 143
> Terminated

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -p no:cacheprovider --ignore=tests/test_hand_links.py 2>&1 | tail -3
```

> Command running in background with ID: bnk684ue9. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/bnk684ue9.output. You will be notified when it completes. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** The test run that just finished agrees with what I reported: all 12 new tests fail because the feature isn't built yet. The full suite also showed `1 failed, 335 passed`, but that run stopped at the first failure without saying which test it was. It's most likely one of the 12 new ones. To make sure the rest of the repo still passes, I've started the suite again without the new test file. I'll report the result when it finishes.

`14. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/911e4240-b59e-4430-8824-9b890c3cba23/tasks/bnk684ue9.output
```

> ........................................................................ [ 92%]
> .............................................                            [100%]
> 621 passed in 354.09s (0:05:54)
> 
> [exited with code 0]

**Agent:** Leaving out the new test file, all 621 other tests pass. So the only failures on this branch are the 12 new tests in `tests/test_hand_links.py`, and they fail because the feature isn't built yet. My approval of the plan stands as written in `/tmp/dokima-out/review.json`. The 15-minute schedule question still stops for you.
