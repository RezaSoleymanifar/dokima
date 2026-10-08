# reviewer (plan) for #188

Run: https://github.com/dokima-dev/dokima/actions/runs/37736030675

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
> 02-reviewer-plan.json
> 03-planner.json
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
> - When code rejects an agent's hand-back, the card mentions the owner. ([source](https:

**Agent:** Verify the fix in the test file.

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff b647f32 f7ebfe6 --stat; git diff b647f32 f7ebfe6 -- tests/ | head -80; grep -n "ICON\|failed\|Next" tests/test_cancelled_run.py | head -40
```

> tests/test_cancelled_run.py | 11 +++++++----
>  1 file changed, 7 insertions(+), 4 deletions(-)
> diff --git a/tests/test_cancelled_run.py b/tests/test_cancelled_run.py
> index 4e3b85b..5d9abca 100644
> --- a/tests/test_cancelled_run.py
> +++ b/tests/test_cancelled_run.py
> @@ -85,7 +85,8 @@ def test_a_cancelled_run_says_so_on_its_card_and_mentions_no_one(record_property
>      Cancels runs at the code-owner gate, while the tools install, while the planner, the plan reviewer and the worker
>      (whose card is on its open pull request) work, and after a review's hand-back passed code's check. Each must leave
>      exactly one comment, in the right place, that says it was cancelled, no longer says getting ready or working,
> -    names no one with an @, does not say any hand-back was rejected or that a step failed, and ends with a Next line.
> +    names no one with an @, shows no running, queued or failed icon, does not say any hand-back was rejected or that a
> +    step failed, and ends with a Next line.
>      Runs that end without a cancel (a rejected hand-back, a failed install, a blocking review) must never say
>      cancelled."""
>      record_property("proves", "188.1")
> @@ -100,12 +101,14 @@ def test_a_cancelled_run_says_so_on_its_card_and_mentions_no_one(record_property
>          assert re.search(r"\bcancell?ed\b", body, re.I), f"188.1 ({name}): the card does not say the run was cancelled:\n{body[:900]}"
>          assert LIVE not in body and "working since" not in body and "getting ready" not in

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_cancelled_run.py 2>&1 | grep -E "^(FAILED|E  +(assert|AssertionError)?.{0,200}188)|passed|failed" | head -20; timeout 900 python -m pytest -q --deselect tests/test_cancelled_run.py 2>&1 | tail -3
```

> ugrep: error: error at position 96
> x80-\xbf]*){0,200}188)|passed|failed
>        exceeds complexity limits___/
> 
> 
> ........................................................................ [ 97%]
> .......                                                                  [100%]
> 295 passed, 4 deselected in 83.77s (0:01:23)

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q tests/test_cancelled_run.py 2>&1 | grep -E "^E .*188\.|FAILED|passed|failed in" | cut -c1-250 | head -20
```

> (whose card is on its open pull request) work, and after a review's hand-back passed code's check. Each must leave
>         Runs that end without a cancel (a rejected hand-back, a failed install, a blocking review) must never say
> E           AssertionError: 188.1 (gate): the card does not say the run was cancelled:
> E           AssertionError: 188.2 (planner): a run cancelled while its agent worked mentions ['@owner-person']:
>         Every cancelled run (including one cancelled after its blocking review had passed code's check, which the river
> E           AssertionError: 188.3 (after-check): after a cancel the run started another run by itself: [['api', '-X', 'POST', 'repos/o/r/dispatches', '-f', 'event_type=dokima-next', '-f', 'client_payload[role]=planner', '-f', 'client_payload[stage]=p
> E           AssertionError: 188.4 (gate): a cancelled run left its card as 'Plan needs', expected no Needs you
> FAILED tests/test_cancelled_run.py::test_a_cancelled_run_says_so_on_its_card_and_mentions_no_one - AssertionError: 188.1 (gate): the card does not say the run was cancelled:
> FAILED tests/test_cancelled_run.py::test_the_owner_is_mentioned_on_a_real_rejection_and_not_on_a_cancel - AssertionError: 188.2 (planner): a run cancelled while its agent worked mentions ['@owner-person']:
> FAILED tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure - AssertionError: 188.3 (after-check): after a cancel the run started another run by itself: [['api', '-X', 'POST', 

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Made the 188.1 test also rule out the failed icon on a cancelled run's card, beside the running and queued icons.",
          "Made the 188.1 test check that the cancelled run's card ends with its Next line, not only that one is somewhere in it."],
  "decided": ["188.1 now says outright that a cancelled card shows no failed icon and no word failed."],
  "open": ["The question on a cancel after the hand-back passed code's check stands on its assumption (a cancel starts nothing); the owner went on with /review."]},
 "verdict": "approve",
 "summary": "The one blocker is fixed: the test for 188.1 now turns red if a cancelled run's card keeps the failed icon, and all four new tests fail today for the right reasons while the 295 older tests pass.",
 "blockers": [],
 "notes": [],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 188 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for #188. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Earlier blocker B1 is fixed:** The test for 188.1 now also rules out the failed icon on a cancelled run's card (`tests/test_cancelled_run.py:104`). A cancelled card that keeps the red failed icon would now fail the test.
- **Earlier note is fixed:** The same test now checks that the cancelled card's last line is its Next line, not just that one appears somewhere.
- **New tests fail today for the right reason:** I ran all four new tests and each fails because the feature is missing:
  - **188.1:** a run cancelled at the code-owner gate leaves a card that doesn't say cancelled.
  - **188.2:** a planner run cancelled while it works mentions `@owner-person`.
  - **188.3:** a run cancelled after its hand-back passed code's check still starts the next stage.
  - **188.4:** a run cancelled at the gate puts its card in Needs you.
- **Older tests still pass:** all 295 of them.
- **The planner's open question:** whether a cancel that lands after the hand-back passed code's check should still start the next stage. The planner assumed it starts nothing, and the owner went on with that assumption by saying `/review`.

The review has no new blockers, notes or proposed issues.
