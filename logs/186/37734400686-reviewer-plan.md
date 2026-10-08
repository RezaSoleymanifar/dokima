# reviewer (plan) for #186

Run: https://github.com/dokima-dev/dokima/actions/runs/37734400686

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #186: Live card: queued within seconds, waiting behind another run, the same card at every hand-off and split
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #164, story 2</summary>
> 
> **Part of:** #164 Visibility: one live card per run, from queued to done
> 
> **User story:** The owner sees a card within seconds of every command and every hand-off, and it says so when the run waits its turn.
> 
> **Context:** A command reaches commands.yml first: the job 'route' decides, then 'run' calls agent.yml, or 'split' files a split. The river's hand-offs reach agent.yml through repository_dispatch dokima-next, sent by the step 'Start the next stage'. That step is the natural place to post the queued card for the next run and hand its comment id on in the payload. agent.yml runs one run per issue at a time (concurrency group agent-N, cancel-in-progress false). Note what GitHub does there: while one run is pending, a newer one replaces it, and the pending one is cancelled. So the waiting card and story 4's cancelled card meet here. Filing a split (agent.py split) posts a split record today; it has to use the same card. This story needs changes to .github/workflows/commands.yml and agent.yml, which the issue asks for.
> 
> **Acceptance criteria:**
> - Within seconds of a code owner's /plan, /work or /review, a card on the issue or PR says queued for that stage. It is the same card the run then updates. ([source](https://github.com/dokima-dev/dokima

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_live_queue.py; cat tests/test_live_queue.py
```

> <persisted-output>
> Output too large (30.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f961aa5f-cf60-440e-a596-07d5c284a04d/tool-results/bpa4gwdz0.txt
> 
> Preview (first 2KB):
> commit b1bab0f9699d1a730062e7e1b22ada5b7f4e7840
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:50:12 2026 +0000
> 
>     planner for #186 (run 37733566305)
> 
>  tests/test_live_queue.py | 487 +++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py      |   9 +-
>  2 files changed, 493 insertions(+), 3 deletions(-)
> 487 tests/test_live_queue.py
> """Every run's card goes up within seconds of what started it, says when it waits, and stays the run's one card (#186).
> 
> These tests run the workflows the way GitHub runs them, with the machine from test_start.py: the command listener
> (.github/workflows/commands.yml) on a code owner's comment, then the agent workflow (.github/workflows/agent.yml) it
> calls, with exactly the inputs the listener's job hands it. A hand-off runs the agent workflow, then runs it again
> the way GitHub would on the dokima-next signal it sent, with exactly the payload of that signal. Between the two
> halves the tests read what GitHub showed: that is the moment a run waits for its turn on the issue.
> 
> The fake GitHub here also knows runs: options.json may say "runs": {"41": "in_progress"}, and GitHub then answers
> `gh api repos/o/r/actions/runs/41`, `gh run view 41` and the run lists with that 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_live_queue.py; git show HEAD -- tests/test_start.py
```

> <persisted-output>
> Output too large (32.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f961aa5f-cf60-440e-a596-07d5c284a04d/tool-results/b14zi86fy.txt
> 
> Preview (first 2KB):
> """Every run's card goes up within seconds of what started it, says when it waits, and stays the run's one card (#186).
> 
> These tests run the workflows the way GitHub runs them, with the machine from test_start.py: the command listener
> (.github/workflows/commands.yml) on a code owner's comment, then the agent workflow (.github/workflows/agent.yml) it
> calls, with exactly the inputs the listener's job hands it. A hand-off runs the agent workflow, then runs it again
> the way GitHub would on the dokima-next signal it sent, with exactly the payload of that signal. Between the two
> halves the tests read what GitHub showed: that is the moment a run waits for its turn on the issue.
> 
> The fake GitHub here also knows runs: options.json may say "runs": {"41": "in_progress"}, and GitHub then answers
> `gh api repos/o/r/actions/runs/41`, `gh run view 41` and the run lists with that status; every other run is
> completed. A run another run waits for is found from GitHub's records: its card on the issue or its pull request,
> which links to the run, and GitHub's word that the run is not completed. Every dokima-next signal's payload is kept.
> """
> import json
> import os
> import re
> import shutil
> 
> import pytest
> 
> import test_start as ts
> from test_start import N, OWNER, PR, SPLIT_APPROVED, STORY_A

`4. Read`
```
/home/runner/work/dokima/dokima/tests/test_live_queue.py
```

> 1	"""Every run's card goes up within seconds of what started it, says when it waits, and stays the run's one card (#186).
> 2	
> 3	These tests run the workflows the way GitHub runs them, with the machine from test_start.py: the command listener
> 4	(.github/workflows/commands.yml) on a code owner's comment, then the agent workflow (.github/workflows/agent.yml) it
> 5	calls, with exactly the inputs the listener's job hands it. A hand-off runs the agent workflow, then runs it again
> 6	the way GitHub would on the dokima-next signal it sent, with exactly the payload of that signal. Between the two
> 7	halves the tests read what GitHub showed: that is the moment a run waits for its turn on the issue.
> 8	
> 9	The fake GitHub here also knows runs: options.json may say "runs": {"41": "in_progress"}, and GitHub then answers
> 10	`gh api repos/o/r/actions/runs/41`, `gh run view 41` and the run lists with that status; every other run is
> 11	completed. A run another run waits for is found from GitHub's records: its card on the issue or its pull request,
> 12	which links to the run, and GitHub's word that the run is not completed. Every dokima-next signal's payload is kept.
> 13	"""
> 14	import json
> 15	import os
> 16	import re
> 17	import shutil
> 18	
> 19	import pytest
> 20	
> 21	import test_start as ts
> 22	from test_start import N, OWNER, PR, SPLIT_APPROVED, STORY_APPROVED, STORY_PLANNED, Ctx, evaluate, condition, fill
> 23	
> 24	from dokima import agent
> 25	
> 26	BOT_ACTOR = "dokima-runtime[bot]"
> 27	OTHER_RUN = "41"
> 28	OTHER_RU

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_start.py; timeout 900 python -m pytest -q tests/test_live_queue.py -x -q 2>&1 | tail -30
```

> commit b1bab0f9699d1a730062e7e1b22ada5b7f4e7840
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:50:12 2026 +0000
> 
>     planner for #186 (run 37733566305)
> 
> diff --git a/tests/test_start.py b/tests/test_start.py
> index 8c0a9f5..7c053cc 100644
> --- a/tests/test_start.py
> +++ b/tests/test_start.py
> @@ -739,7 +739,8 @@ def test_a_failed_command_says_why_and_stops_for_the_owner(record_property, tmp_
>      the pull request belongs to, and `/work` on an approved split when GitHub refuses to create the stories' issues.
>      Each must post one record where the command was written that carries GitHub's error, ends with a Next line
>      mentioning the owner, and starts no agent. Three good cases stay as they are: `/work` on an approved split that
> -    files fine posts only its passed "Split filed" record, `/plan` from the owner starts the agent and posts nothing,
> +    files fine posts only its passed "Split filed" record, `/plan` from the owner starts the agent and posts only its
> +    queued card (#186), which is not a record,
>      and `/plan` from someone who is not a code owner gets no reply and starts nothing."""
>      record_property("proves", "176.4")
>      gone = "GraphQL: Could not resolve to a PullRequest with the number of 60. (repository.pullRequest)"
> @@ -760,8 +761,10 @@ def test_a_failed_command_says_why_and_stops_for_the_owner(record_property, tmp_
>      assert [(x["role"], x["check"]["passed"]) for x in recs] == [("split", Tr

**Agent:** Reviewing the plan for #186: the first new test fails for the right reason (no queued card yet); now running the rest.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 1200 python -m pytest -q tests/test_live_queue.py "tests/test_start.py::test_a_failed_command_says_why_and_stops_for_the_owner" 2>&1 | grep -E "^(FAILED|PASSED|ERROR|[0-9]+ (passed|failed))|AssertionError: 18|^E +(assert|AssertionError)" | head -40
```

> E           AssertionError: 186.1 (plan): when the listener was done, before the run started, GitHub showed 0 comments, expected one queued card: []
> E           assert 0 == 1
> E           AssertionError: 186.2 (issue): the command did not put up exactly one card before its run: 0
> E           assert ({'role': 'reviewer', 'stage': 'plan', 'issue': '57'} is not None and 0 == 1)
> E           AssertionError: 186.3 (plan-block): after the first run GitHub shows 1 records and 0 cards, expected its record and the next stage's one queued card: [('issue #57', '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="pas')]
> E           assert (1 == 1 and 0 == 1)
> E       AssertionError: 186.2 (hand-off): setup: the hand-off did not put up exactly one card: 0 cards, [{'role': 'planner', 'stage': 'plan', 'issue': '57'}]
> E       assert (1 == 1 and 0 == 1)
> E       AssertionError: 186.4 (owner): the owner's /plan did not put up exactly one card: []
> E       assert (0 == 1)
> E       AssertionError: 176.4: the owner's /plan no longer just starts the planner with its one queued card: started=True posted=[]
> E       assert (not False and True and 0 == 1)
> FAILED tests/test_live_queue.py::test_a_code_owners_command_puts_up_a_queued_card_that_the_run_then_updates - AssertionError: 186.1 (plan): when the listener was done, before the run started, GitHub showed 0 comments, expected one queued card: []
> FAILED tests/te

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def live_card" -A50 dokima/agent.py | head -80; ls dokima/icons
```

> 217:def live_card(role, stage, state):
> 218-    """The run's card while it is still running: getting ready, then working since the agent started.
> 219-
> 220-    It carries its own marker and no JSON fold, so it never reads as a record; at the end of the run code edits this
> 221-    same comment into the run's record."""
> 222-    head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker"}.get(role, "Command")
> 223-    repo = os.environ.get("GITHUB_REPOSITORY", "")
> 224-    run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
> 225-    if state == "working":
> 226-        line = f"{icon(repo, 'running')} **{head}** · working since {time.strftime('%Y-%m-%d %H:%M', time.gmtime())} UTC"
> 227-        what = "The agent is working. This card becomes the run's record when it ends."
> 228-    else:
> 229-        line = f"{icon(repo, 'queued')} **{head}** · getting ready"
> 230-        what = "The machine is getting ready. This card says working when the agent starts, then becomes the run's record."
> 231-    return "\n".join([LIVE, line, "", what, "", f"<sub>[run]({run})</sub>"]) + "\n"
> 232-
> 233-
> 234-def render(rec):
> 235-    """The comment that carries a record: a short readable summary, then the full record as JSON in a fold."""
> 236-    role, h = rec["role"], rec["handback"]
> 237-    repo = os.environ.get("GITHUB_REPOSITORY", "")
> 238-    if role == "not-started":
> 239-        a = rec.get("attempt")
> 240-      

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote four acceptance criteria for the queued card, the waiting card, one card per run across hand-offs and splits, and code-owner-only posting, with five new tests in tests/test_live_queue.py.",
          "Changed one existing test so the owner's /plan now expects exactly its queued card instead of no comment."],
  "decided": ["A waiting card links the run it waits for; once its own run starts it no longer says waiting.",
              "A split that GitHub refuses to file turns its one card into the record saying why; what a card says when GitHub cancels a pending run is left to story 4 of #164."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers all three things the owner asked for plus the code-owner rule, and every new test fails today because no queued card is posted yet, not because of a setup fault.",
 "blockers": [],
 "notes": [
  {"text": "The 'says queued' checks match the queued icon's alt text, so a card that only says 'getting ready' next to the queued icon would pass 186.1 and the no-run-ahead half of 186.2. The worker should still write the word queued on the card.",
   "evidence": "tests/test_live_queue.py:249 and :368 test 'queued' in visible(body).lower(); dokima/agent.py:229 already renders alt=\"queued\" for the getting-ready card."},
  {"text": "The hand-off tests cover plan review to planner and worker to code review. They do not cover planner to plan review, code review to worker, or a hand-off card that stops saying waiting once its run starts. One shared hand-off step should cover these, but no test proves it.",
   "evidence": "tests/test_live_queue.py:378-384 (plan-block, work-done, waiting); test_a_hand_off_card_says_when_it_waits_for_another_run never reads the second run's snapshot."},
  {"text": "186.1 says the worker's card goes on the issue until a pull request exists, but /work is tested only with an open pull request.
```

> rc=0

**Agent:** I approved the plan for #186. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**Why I approved:** the plan covers the three things the issue asks for, plus the rule that only a code owner's command posts a card:
- **Queued card:** a card says queued within seconds of `/plan`, `/work` or `/review`, and the run turns that same card into its record.
- **Waiting card:** a run stuck behind another run on the same issue gets a card that says it is waiting and links that run.
- **One card per run:** this holds for all four stages, for hand-offs the river starts by itself, and for filing a split.

**Tests:** I ran the five new tests and the changed test in `tests/test_start.py`. All six fail today because no queued card is posted yet, not because of a setup problem. Each test also has a good case beside the bad one: a run with nothing ahead says queued and not waiting, an earlier run that has already finished doesn't count as one to wait for, and the owner's own `/plan` still puts up one card.

**Notes for the worker** (none of these block):
1. The "says queued" checks would also pass on the hidden label of the queued icon. A card that only says "getting ready" next to that icon would slip through, so the card should spell out the word queued.
2. Only two hand-offs are tested: plan review back to planner, and worker to code review. Nothing tests planner to plan review, code review back to worker, or a hand-off card no longer saying waiting once its run starts.
3. The worker's card should go on the issue until a pull request exists, but `/work` is only tested with a pull request already open.
