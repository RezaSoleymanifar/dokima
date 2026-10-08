# reviewer (plan) for #188

Run: https://github.com/dokima-dev/dokima/actions/runs/37734991512

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json; ls in
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #188: Live card: cancelled runs and who gets pinged
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
> <details open><summary>From the approved plan of #164, story 4</summary>
> 
> **Part of:** #164 Visibility: one live card per run, from queued to done
> 
> **User story:** A cancelled run says so quietly, and the owner is pinged only when there is a real rejection to look at.
> 
> **Context:** Today next_step() in dokima/agent.py stops on any hand-back code rejected and mentions the owner (next_line). A run that is cancelled (from the Actions page, or a pending run GitHub replaces in the agent-N concurrency group) gets no record at all, or a not-started one. Telling them apart in agent.yml needs the job status: cancelled() in a step condition, or the run's conclusion. Nothing retries today; keep it that way. This story needs changes to .github/workflows/agent.yml, which the issue asks for.
> 
> **Acceptance criteria:**
> - A cancelled run's card says it was cancelled and mentions no one. ([source](https://github.com/dokima-dev/dokima/issues/164))
> - When code rejects an agent's hand-back, the card mentions the owner. ([source](https://github.com/dokima-dev/dokima/issues/

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests/test_start.py | head -300
```

> commit b647f3210b775e0ece7a5e822f5d74b7d671cf77
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:52:03 2026 +0000
> 
>     planner for #188 (run 37733571399)
> 
>  tests/test_cancelled_run.py | 177 ++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py         |  46 ++++++++----
>  2 files changed, 209 insertions(+), 14 deletions(-)
> commit b647f3210b775e0ece7a5e822f5d74b7d671cf77
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:52:03 2026 +0000
> 
>     planner for #188 (run 37733571399)
> 
> diff --git a/tests/test_start.py b/tests/test_start.py
> index 8c0a9f5..961fae5 100644
> --- a/tests/test_start.py
> +++ b/tests/test_start.py
> @@ -188,14 +188,17 @@ FAKE_CLAUDE = r'''#!/usr/bin/env python3
>  
>  When it starts it keeps what GitHub showed at that moment (every comment and every version, at-agent-start.json),
>  its own environment (agent-env.json) and the time it started (agent-started-at), so a test can see the run as the
> -agent found it."""
> -import json, os, shutil, time
> +agent found it. With FAKE_CANCELLED set, the run is being cancelled: it stops there, as Claude Code does when its step
> +is stopped, and hands back nothing."""
> +import json, os, shutil, sys, time
>  d = os.environ["FAKE_GH_DIR"]
>  store = os.path.join(d, "comments.json")
>  json.dump(json.load(open(store)) if os.path.exists(store) else [], open(os.path.join(d, "at-agent-start.json"), "w"))
>  json.dump(dict(os.envir

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_cancelled_run.py
```

> """A cancelled run says so quietly, the owner is mentioned on a real rejection, and nothing restarts by itself (#188).
> 
> These tests run the agent workflow (.github/workflows/agent.yml) the way GitHub runs it, with the machine from
> test_start.py, and cancel some runs part way, the way the Cancel button on the Actions page does: at the code-owner
> gate (before the run's card is up), while the tools install (card up, no agent yet), while the agent works, and after
> the agent's hand-back passed code's check. Other runs are not cancelled and end the usual ways: a hand-back code
> rejects, a step that fails before the agent, and a blocking plan review that the river sends back to the planner.
> Each scenario runs once per module and the tests read what it left on the fake GitHub: its comments, and every call
> that could start a run.
> """
> import os
> import re
> 
> import pytest
> 
> import test_start as ts
> from test_start import APPROVE, N, OWNER, PIP_BROKEN, PR, STORY_APPROVED, STORY_PLANNED, Run, owner_comment
> 
> from dokima import agent
> 
> LIVE = "<!-- dokima-live -->"
> MENTION = re.compile(r"(?<![\w/@.`])@[A-Za-z0-9][A-Za-z0-9-]*")
> ICON = re.compile(r"/dokima/icons/([A-Za-z0-9_-]+)\.svg")
> BAD_REVIEW = {"verdict": "maybe"}
> BLOCK = dict(APPROVE, verdict="block", summary="57.1 has no test that would fail without the work.",
>              blockers=[{"id": "B1", "criterion": "57.1", "problem": "The test only checks a file exists.",
>                         "evidence": "tests/test_x.py::test_a", "fix": "Run 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_cancelled_run.py 2>&1 | tail -60
```

> </details>
>   
>   <sub>No agent ran · [run](https://github.com/o/r/actions/runs/42)</sub>
>   
>   **Next:** @owner-person Nothing ran, see why above. Fix the cause, then give the command again.
>   
> assert None
>  +  where None = <function search at 0x7f738ffef060>('\\bcancell?ed\\b', '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" heig...ns/runs/42)</sub>\n\n**Next:** @owner-person Nothing ran, see why above. Fix the cause, then give the command again.\n', re.IGNORECASE)
>  +    where <function search at 0x7f738ffef060> = re.search
>  +    and   re.IGNORECASE = re.I
> FAILED tests/test_cancelled_run.py::test_the_owner_is_mentioned_on_a_real_rejection_and_not_on_a_cancel - AssertionError: 188.2 (planner): a run cancelled while its agent worked mentions ['@owner-person']:
>   okima-record -->
>   <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **Planner** · hand-back rejected by code
>   
>   - ::error title=Planner output rejected::found no plan.json: the planner always hands back a plan, a plan.json of kind user_story or feature, with its questions listed inside it
>   
>   <details><summary>Full record</summary>
>   
>   
>   
>   </details>
>   
>   <sub>model unknown · [conversation](https://github.com/o/r/blob/logs/logs/57/42-planner.md) · [run](https://github.com/o/r/actions/runs/42)</sub>
>   
>   **Next:** @owner-person The hand-back was rejected by code, see th

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_cancelled_run.py 2>&1 | grep -E "^(FAILED|E  +AssertionError)" | cut -c1-300; timeout 1200 python -m pytest -q -x tests 2>&1 | tail -3
```

> E           AssertionError: 188.1 (gate): the card does not say the run was cancelled:
> E           AssertionError: 188.2 (planner): a run cancelled while its agent worked mentions ['@owner-person']:
> E           AssertionError: 188.3 (after-check): after a cancel the run started another run by itself: [['api', '-X', 'POST', 'repos/o/r/dispatches', '-f', 'event_type=dokima-next', '-f', 'client_payload[role]=planner', '-f', 'client_payload[stage]=plan', '-f', 'client_payload[issue]=57']]
> E           AssertionError: 188.4 (gate): a cancelled run left its card as 'Plan needs', expected no Needs you
> FAILED tests/test_cancelled_run.py::test_a_cancelled_run_says_so_on_its_card_and_mentions_no_one - AssertionError: 188.1 (gate): the card does not say the run was cancelled:
> FAILED tests/test_cancelled_run.py::test_the_owner_is_mentioned_on_a_real_rejection_and_not_on_a_cancel - AssertionError: 188.2 (planner): a run cancelled while its agent worked mentions ['@owner-person']:
> FAILED tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure - AssertionError: 188.3 (after-check): after a cancel the run started another run by itself: [['api', '-X', 'POST', 'repos/o/r/dispatches', '-f', 'event_type=dokima-next', '-f', 'client_payload[role]=planne
> FAILED tests/test_cancelled_run.py::test_a_cancelled_run_does_not_put_needs_you_on_the_board - AssertionError: 188.4 (gate): a cancelled run left its card as 'Plan needs', expected no Needs you
>  +    and   re.IGNORECAS

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -E "^  [a-z-]+:|concurrency|group:|cancel-in-progress|needs:|^\s+- name:|if:" .github/workflows/agent.yml | head -120
```

> 4:# starts with /plan, /work or /review. Code gathers everything the agent needs: the issue and its PR as one
> 34:concurrency:
> 35:  group: agent-${{ (inputs.issue || github.event.client_payload.issue) }}
> 36:  cancel-in-progress: false
> 38:  contents: read
> 39:  issues: read
> 40:  pull-requests: read
> 41:  actions: read
> 43:  run:
> 64:      - name: Copy the runtime from main before touching any branch
> 66:      - name: Only a code owner starts an agent
> 85:      - name: Put up the run's card, getting ready
> 99:      - name: Starting branch
> 123:      - name: Build the starting pack
> 137:      - name: Install pytest and Claude Code
> 142:      - name: All tests, run by code before the reviewer reads the pull request
> 143:        if: env.STAGE == 'pr'
> 147:      - name: Code checks the pack has everything this role needs
> 154:        if: env.CARD_ID != ''
> 161:      - name: The card says working
> 162:        if: env.CARD_ID != ''
> 170:      - name: The agent starts now
> 172:      - name: The agent (Claude Code)
> 199:      - name: Code checks the hand-back
> 200:        if: always() && env.STARTED == 'true'
> 205:      - name: Fence - only in-scope changes, the planner's tests as committed
> 206:        if: env.ROLE == 'worker'
> 210:      - name: Write this run's record
> 211:        if: always()
> 225:      - name: Remove secrets from the raw session files before they are uploaded
> 226:        if: always()
> 237:      - name: Save the hand-back and the full session log
> 238:        if: always()
> 249:        if: alwa

**Agent:** The four new tests fail today for the right reasons. Now I'm checking whether the "not shown as a failure" check also covers the card's icon.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima/icons; grep -n "def board\|def failed\|def condition" -A6 tests/test_start.py | head -40; timeout 1200 python -m pytest -q tests --deselect tests/test_cancelled_run.py 2>&1 | tail -2
```

> failed.svg
> none.svg
> passed.svg
> queued.svg
> running.svg
> 269:def condition(cond):
> 270-    """A job's or step's `if:` the way GitHub reads it: without a status function it also needs success()."""
> 271-    cond = str(cond or "success()")
> 272-    return cond if re.search(r"\b(always|failure|success|cancelled)\(\)", cond) else f"success() && ({cond})"
> 273-
> 274-
> 275-def load_yaml(text):
> --
> 590:    def board(self):
> 591-        """Where the run put the card, as written for the board step ('Plan needs'), or '' when it wrote nothing."""
> 592-        out = self.env.get("OUT", "")
> 593-        path = os.path.join(out, "board.txt")
> 594-        return open(path).read().strip() if out and os.path.exists(path) else ""
> 595-
> 596-
> .......                                                                  [100%]
> 295 passed, 4 deselected in 78.87s (0:01:18)

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote four tests that cancel runs at the code-owner gate, during install, while the agent works and after code's check, and compare them with runs that are rejected, fail or block without a cancel.",
          "Taught the workflow simulator to cancel a run at a named step; all 295 older tests still pass."],
  "decided": ["A cancel starts nothing, even one that lands after the hand-back passed code's check (the owner went on with this assumption via /review).",
              "A pending run GitHub replaces in the concurrency group, which never starts, leaves no card and is out of scope."],
  "open": ["A cancelled run's card must not carry the Needs you pill, added from the board rule."]},
 "verdict": "block",
 "summary": "The plan and its tests are sound and fail today for the right reasons, but the test for 188.1 would still pass if a cancelled run's card kept the red failed icon, so it does not prove the card is not shown as a failure.",
 "blockers": [{"id": "B1", "criterion": "188.1",
   "test": "tests/test_cancelled_run.py::test_a_cancelled_run_says_so_on_its_card_and_mentions_no_one",
   "problem": "188.1 promises the cancelled card 'is not shown as a failure', but the test removes every icon before it looks for 'failed' and only rules out the running and queued icons. A card that adds the word cancelled but keeps the failed icon (failed.svg, alt=\"failed\"), as every failed or rejected card does today, would pass.",
   "evidence": "tests/test_cancelled_run.py: `assert not {\"running\", \"queued\"} & set(ICON.findall(body))` and `\"failed\" not in re.sub(r\"<img[^>]*>\", \"\", body).lower()`; dokima/icons/ holds failed.svg, and today's rejected card begins with `icons/failed.svg ... alt=\"failed\"` (pytest output for 188.2, planner case).",
   "fix": "Add \"failed\" to the icons ruled out for a cancelled card: `assert not {\"running\", \"queued\", \"failed\"} & set(
```

> 0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['previous_step']['decided'].append("A cancelled run's card does not carry the Needs you pill, a promise taken from the board rule.")
r['previous_step']['open']=[]
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 188 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I blocked the plan for #188 on one gap in a test. The fix is a one-line change for the planner. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What holds up:**
- I ran the four new tests and they all fail today for the right reasons:
  - **188.1:** a run cancelled at the code-owner gate gets a "Nothing ran" failure card instead of one that says cancelled.
  - **188.2:** a planner cancelled while it works is shown as "hand-back rejected" and mentions @owner.
  - **188.3:** a review cancelled after it passed code's check still starts the planner.
  - **188.4:** a cancelled run puts its card in Needs you.
- The other 295 tests still pass with the planner's changes to the workflow simulator in `tests/test_start.py`.
- Leaving out a pending run that GitHub replaces is correct. The concurrency group covers the whole workflow, so a replaced run never starts and can't post a card.
- The plan's one question (a cancel starts nothing, even after code's check) was settled when the owner gave `/review`.

**Blocker B1 (criterion 188.1, for the planner):** 188.1 says a cancelled run's card "is not shown as a failure", but the test doesn't fully check that. It removes the icons before looking for the word "failed", and it only rules out the running and queued icons. So a card that adds the word "cancelled" but keeps the red failed icon, like today's failed and rejected cards, would pass.
- **Fix:** add `"failed"` to the icons ruled out for a cancelled card.
- If the plan intends to use the new `dokima/icons/cancelled.svg` (it's in scope), 188.1 should say so and the test should check that icon is the one shown.

**Note (doesn't block):** 188.1 says the card "ends with a Next line", but the test only checks that a Next line appears somewhere in the card.
