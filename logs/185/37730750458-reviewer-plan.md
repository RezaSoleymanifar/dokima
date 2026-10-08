# reviewer (plan) for #185

Run: https://github.com/dokima-dev/dokima/actions/runs/37730750458

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #185: Live card: one card per run, updated in place from working to its result
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #164, story 1</summary>
> 
> **Part of:** #164 Visibility: one live card per run, from queued to done
> 
> **User story:** Each agent run has one card on the issue or PR that turns from working into its result, so the owner no longer waits in silence for a comment to appear.
> 
> **Context:** Today a run posts its one record comment only at the very end (agent.yml, step 'Post the record as a comment'). render() in dokima/agent.py draws it, with the full JSON in a fold under the <!-- dokima-record --> marker. records() and is_record() treat every bot comment with that marker and a JSON fold as a permanent record, and every pack, next_step and approved() reads them. So a card that is still running must never parse as a record: give it its own marker, or no JSON fold, until it becomes the result. The step 'The agent starts now' is the moment the machine is ready. A run that fails before it, through not_started(), already writes why. That record has to edit the same card instead of posting a n

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_live_card.py; cat tests/test_live_card.py
```

> commit 9d7fd0307a3e6baa7499a5e5be61eecf0479b640
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:05:20 2026 +0000
> 
>     planner for #185 (run 37729962175)
> 
>  tests/test_live_card.py | 298 ++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py     | 169 +++++++++++++++++++++++----
>  2 files changed, 447 insertions(+), 20 deletions(-)
> 298 tests/test_live_card.py
> """Each agent run has one live card that turns from working into its result (#185).
> 
> These tests run the agent workflow (.github/workflows/agent.yml) the way GitHub runs it, with the machine from
> test_start.py: a fake GitHub that keeps every comment the run writes and every version of it, a fake Claude Code that
> notes what GitHub showed the moment it started, and nothing leaving the machine. Each scenario runs once per module
> and the tests read what it left behind: which comments exist, what each said at each moment, and which key made each
> call.
> """
> import calendar
> import json
> import os
> import re
> import time
> 
> import pytest
> 
> import test_start as ts
> from test_start import N, OWNER, PR, PIP_BROKEN, STORY_APPROVED, STORY_PLANNED, Run
> 
> from dokima import agent
> 
> ROOT = ts.ROOT
> ICON = re.compile(r'<img[^>]*src="https://raw\.githubusercontent\.com/[^/"]+/[^/"]+/main/dokima/icons/([A-Za-z0-9_-]+)\.svg"')
> TIME = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?(?:\.\d+)?\s*(?:UTC|Z)(?!\w)")
> EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‼⁉ℹ

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_start.py
```

> commit 9d7fd0307a3e6baa7499a5e5be61eecf0479b640
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:05:20 2026 +0000
> 
>     planner for #185 (run 37729962175)
> 
> diff --git a/tests/test_start.py b/tests/test_start.py
> index a7a5937..8c0a9f5 100644
> --- a/tests/test_start.py
> +++ b/tests/test_start.py
> @@ -3,9 +3,10 @@
>  These tests run the workflows' own steps, read from .github/workflows/agent.yml and commands.yml, the way GitHub runs
>  them: each job's and step's `if:` is evaluated, its `${{ }}` expressions filled in, and its script run with bash in a
>  clone of a temp git repo whose origin is a local bare repo. Jobs run in the order their `needs` allow, each on its own
> -fresh clone and its own /tmp. Nothing leaves the machine: a fake `gh` answers from a fake issue and records every
> -comment, dispatch and issue it is asked to create (and can be told to fail one call, the way GitHub does); a fake
> -`claude` hands back a review; `pip` and `npm` do nothing unless a test breaks them; pushes to github.com are redirected
> +fresh clone and its own /tmp. Nothing leaves the machine: a fake `gh` answers from a fake issue, keeps every comment
> +with each version of it as it is edited in place, and records every call, dispatch and issue it is asked to create
> +(and can be told to fail one call, the way GitHub does); a fake `claude` hands back a review and notes what GitHub
> +showed when it started; `pip` and `npm` do nothing unless a test breaks th

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_live_card.py 2>&1 | grep -E "^(FAILED|ERROR|E  )|passed|failed" | head -40; timeout 900 python -m pytest -q 2>&1 | tail -5
```

> assert s.run.agent_started(), f"{crit}: setup: the agent never started; the run stopped at '{s.run.failed_step}':\n{s.tail()}"
> E       AssertionError: 185.1: when the agent started, the run had 0 comments on GitHub, expected its one card: []
> E         ## run: Decide what follows, and say it on the card (exit 0)
> E         stop
> E         
> E         ## run: Post the record as a comment, on the PR once there is one (exit 0)
> E         https://github.com/o/r/issues/57#issuecomment-5001
> E         
> E         ## run: Fail closed on a bad hand-back or the wrong model (exit 0)
> E         models: ['claude-opus-5-5']
> E         
> E       assert 0 == 1
> E        +  where 0 = len([])
>         """At the end of the run its card, edited in place, becomes its record: done, or failed with why.
>         one), posted by Dokima's bot, holding exactly the run's own record and its Next line. The passed run shows the
>         passed icon; the rejected run shows the failed icon and lists the check's problems; neither still shows the
>         for name, kind, number, role, passed in (("pass", "issue", N, "reviewer", True), ("fail", "issue", N, "reviewer", False),
>         assert s.run.agent_started(), f"{crit}: setup: the agent never started; the run stopped at '{s.run.failed_step}':\n{s.tail()}"
> E       AssertionError: 185.2 (pass): when the agent started, the run had 0 comments on GitHub, expected its one card: []
> E         ## run: Decide what follows, and say it on the card (exit 0)
> E         stop
> E         
> E

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_live_card.py 2>&1 | grep -E "^(FAILED|E  +AssertionError)"; git stash list; git diff HEAD~1 --stat; timeout 600 python -m pytest -q tests/test_start.py 2>&1|tail -2; git checkout -q HEAD~1 -- tests/test_start.py 2>/dev/null; git show HEAD~1:tests/test_start.py > /tmp/old_start.py; 
```

> E       AssertionError: 185.1: when the agent started, the run had 0 comments on GitHub, expected its one card: []
> E       AssertionError: 185.2 (pass): when the agent started, the run had 0 comments on GitHub, expected its one card: []
> E               AssertionError: 185.3 (branch): no card was up before the run stopped, so none was updated; the comment's first version was:
> E                   AssertionError: 185.4 (pass): version 1 of the card shows no icon from dokima/icons/:
> E       AssertionError: 185.5: only 0 versions of a card were written before its result: the runs put up no live card
> E           AssertionError: 185.6 (no-edit): the run never tried to edit a live card, so there is none
> E       AssertionError: 185.7: no call before the agent used Dokima's bot key: the bot never put up a live card
> FAILED tests/test_live_card.py::test_the_card_says_working_with_its_start_time_when_the_agent_starts - AssertionError: 185.1: when the agent started, the run had 0 comments on GitHub, expected its one card: []
> FAILED tests/test_live_card.py::test_the_same_comment_becomes_the_result_and_is_the_runs_only_comment - AssertionError: 185.2 (pass): when the agent started, the run had 0 comments on GitHub, expected its one card: []
> FAILED tests/test_live_card.py::test_a_run_that_stops_before_its_agent_edits_its_card_into_why_and_what_to_do - AssertionError: 185.3 (branch): no card was up before the run stopped, so none was updated; the comment's first version was:
> FAILED tests/test_

**Agent:** The new tests all fail for the right reason. I briefly overwrote `tests/test_start.py` by mistake, so I'm restoring it now and then going on with the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git checkout -q HEAD -- tests/test_start.py; git status --short; echo ok
```

> ok

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "GIT_CONFIG\|name:\|if:\|token" .github/workflows/agent.yml | head -120
```

> 1:name: agent
> 2:run-name: "${{ (inputs.role || github.event.client_payload.role) }}${{ (inputs.role || github.event.client_payload.role) == 'reviewer' && format(' ({0})', (inputs.stage || github.event.client_payload.stage)) || '' }} for #${{ (inputs.issue || github.event.client_payload.issue) }}"
> 63:      - name: Copy the runtime from main before touching any branch
> 65:      - name: Only a code owner starts an agent
> 75:      - name: Starting branch
> 77:          GH_TOKEN: ${{ github.token }}
> 99:      - name: Build the starting pack
> 101:          GH_TOKEN: ${{ github.token }}
> 113:      - name: Install pytest and Claude Code
> 118:      - name: All tests, run by code before the reviewer reads the pull request
> 119:        if: env.STAGE == 'pr'
> 123:      - name: Code checks the pack has everything this role needs
> 128:      - name: The agent starts now
> 130:      - name: The agent (Claude Code)
> 157:      - name: Code checks the hand-back
> 158:        if: always() && env.STARTED == 'true'
> 163:      - name: Fence - only in-scope changes, the planner's tests as committed
> 164:        if: env.ROLE == 'worker'
> 168:      - name: Write this run's record
> 169:        if: always()
> 171:          GH_TOKEN: ${{ github.token }}
> 183:      - name: Remove secrets from the raw session files before they are uploaded
> 184:        if: always()
> 187:          SCRUB_GITHUB: ${{ github.token }}
> 195:      - name: Save the hand-back and the full session log
> 196:        if: always()
> 199:          name: ${{ env.ROLE

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "GIT_CONFIG\|fake-token" tests/test_start.py | head; grep -rn "GIT_CONFIG" .github dokima | head
```

> 103:         "author": "dokima-runtime" if token == "fake-token" else "github-actions"}
> 461:                        "RUNNER_TEMP": f"{t}/runner-temp", "GIT_CONFIG_COUNT": "1",
> 462:                        "GIT_CONFIG_KEY_0": f"url.file://{t}/origin.git.insteadOf",
> 463:                        "GIT_CONFIG_VALUE_0": "https://x-access-token:fake-token@github.com/o/r.git"})
> 511:                outputs = {"token": "fake-token", "app-slug": "dokima-runtime"}

`9. Bash`
```
cd /home/runner/work/dokima/dokima/tests; mkdir -p /tmp/rv; cat > /tmp/rv/g.py <<'EOF'
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'..')
import test_start as ts, tempfile
t=tempfile.mkdtemp()
r=ts.Run(t+"/g","worker","",ts.STORY_APPROVED,try_branch=True,actor="stranger")
for c in r.comments(): print(c["author"], len(c["versions"]), c["versions"][-1][:300])
EOF
timeout 300 python /tmp/rv/g.py
```

> dokima-runtime 1 <!-- dokima-record -->
> **Worker** · stopped before any agent started
> 
> - stranger is not a code owner, so they cannot start an agent.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "not-started",
>  "attempt": "worker",
>  "stage": null,
>  "run_id": "42",
>  "started_by": "stranger",
>  "run": "

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan with four acceptance criteria and three non-functional promises, each with one test in tests/test_live_card.py, and taught the test machine's fake GitHub to keep every version of an edited comment."],
  "decided": ["The card goes up right after the code-owner gate, so a run that stops while getting ready edits that same card (the owner went on with this assumption via /review).",
              "The bot's key used for the early card is revoked before the agent starts; a cancelled state, commands that fail in the listener, and the issue's top card stay out of scope."],
  "open": ["The worker's change touches .github/workflows/agent.yml, which the bot cannot push; the owner may have to land that file by hand."]},
 "verdict": "approve",
 "summary": "The plan covers every promise of the story with a test that runs the real workflow, and all seven new tests fail today because no live card exists yet.",
 "blockers": [],
 "notes": [
  {"text": "Every failed run in the tests ends with the agent finishing and code rejecting its hand-back; none has the agent itself crash or time out, so a card left saying working after a crash is not tested directly. The record step runs on every outcome, so the risk is small.",
   "evidence": "tests/test_live_card.py::runs: the 'fail' scenario uses review={'verdict': 'maybe'}; .github/workflows/agent.yml:157,168,256 run with always()."},
  {"text": "Out of scope says the worker's first run keeps its card on the issue even after it opens the pull request. Today that run's record is posted on the new pull request, so the record moves for that one run.",
   "evidence": ".github/workflows/agent.yml:256 'Post the record as a comment, on the PR once there is one'; plan.json out_of_scope item 4."},
  {"text": "All seven new tests fail today for the right reason (no card is up when the agent starts, no edit is tried, no bot call is made bef
```

> (Bash completed with no output)

**Agent:** I approved the plan for #185. The hand-back is in `/tmp/dokima-out/review.json`, and both of Dokima's checks on it pass.

**Why it's approved:** each of the four acceptance criteria and three non-functional promises has its own test in `tests/test_live_card.py`. Those tests run the real `agent.yml` against a fake GitHub that keeps every version of an edited comment. Every promise is checked both ways: a run that passes, one that's rejected, one on an open pull request, three that stop before the agent starts, and one where GitHub refuses the card. All seven new tests fail today because no live card exists yet (for example, "185.1: when the agent started, the run had 0 comments on GitHub"). The rest of the suite still passes against the new fake GitHub: 7 failed, 270 passed. There were no earlier blockers to answer.

**Notes for the owner (none of them blockers):**
1. Every failed run in the tests is one where the agent finishes and code then rejects what it handed back. No test has the agent itself crash or time out, so nothing directly proves a card can't be left saying "working". The risk is small, because the record step runs whatever the outcome.
2. The plan keeps the worker's first card on the issue even after it opens a pull request. Today that run's record goes on the new pull request, so for that one run the record moves.
3. The open point carried over from the planner still stands: the work changes `.github/workflows/agent.yml`, which the bot can't push, so you may have to land that file yourself.

During the review I overwrote `tests/test_start.py` with its version from before the planner's commit by mistake. I put it back straight away, and the working tree is clean.
