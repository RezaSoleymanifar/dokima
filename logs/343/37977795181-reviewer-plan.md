# reviewer (plan) for #343

Run: https://github.com/dokima-dev/dokima/actions/runs/37977795181

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> .:
> total 52
> drwxr-xr-x  3 runner runner  4096 Oct  9 19:05 .
> drwxrwxrwt 18 root   root    4096 Oct  9 19:06 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 19:05 in
> -rw-r--r--  1 runner runner 26147 Oct  9 19:05 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 19:05 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct  9 19:05 parent.json
> -rw-r--r--  1 runner runner  3129 Oct  9 19:05 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner 4096 Oct  9 19:05 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 19:05 ..
> -rw-r--r-- 1 runner runner 3921 Oct  9 19:05 01-planner.json
> -rw-r--r-- 1 runner runner 4079 Oct  9 19:05 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3754 Oct  9 19:05 03-planner.json
> -rw-r--r-- 1 runner runner  563 Oct  9 19:05 04-cancelled-plan.json
> -rw-r--r-- 1 runner runner 3756 Oct  9 19:05 05-planner.json
> # Issue #343: An approved plan waiting on a blocker stays in Plan; Work means it is being built
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> The board keeps an approved plan in Plan until its worker starts, and shows Work only while a worker builds it.
> 
> **Plan**
> 
> [issue #343](https://github.com/dokima-dev/dokima/issues/343)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #332, #333, #313
> 
> **User story:** The owner sees in Work only the issues a worker is actually building, and an approved plan that wait

`2. Bash`
```
cd /tmp/pack; cat plan.json; cat parent.json; cat in/05-planner.json | head -c 4000; cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; cat tests/test_work_column.py
```

> {
>  "kind": "user_story",
>  "summary": "The board keeps an approved plan in Plan until its worker starts, and shows Work only while a worker builds it.",
>  "user_story": "The owner sees in Work only the issues a worker is actually building, and an approved plan that waits for its worker, or for a blocker, stays in Plan with its card saying what it waits on.",
>  "acceptance_criteria": [
>   {
>    "text": "An approved plan whose worker has not started stays in Plan, also while it waits on a blocker. Its issue card still says Blocked by with the issues it waits on.",
>    "source": "https://github.com/dokima-dev/dokima/issues/343"
>   },
>   {
>    "text": "Once a worker starts, the issue and its pull request sit in Work. It starts with the code owner's `/work`, the bot's Autopilot line that starts the worker, or the worker's run card.",
>    "source": "https://github.com/dokima-dev/dokima/issues/343"
>   },
>   {
>    "text": "After the worker has built it, the issue and its pull request stay in Work until the code review starts, also after a rebuild. A review has started once its run card is up, even queued, or its record is; then they sit in Review.",
>    "source": "https://github.com/dokima-dev/dokima/issues/343"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Only the bot's own Autopilot lines and run cards, and a code owner's `/work`, move a card to Work or Review. The same words from anyone else move nothing.",
>    "why": "Anyone can comment on a public repo, and a pasted line must not move the owne

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_work_column.py 2>&1 | grep -E "^(FAILED|PASSED|E   .*343)|passed|failed" | head -30; git diff HEAD~2 -- tests/test_board_state.py
```

> E           AssertionError: 343.1: #57's approved plan waits on #332 and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not in Plan with Autopilot
> E               AssertionError: 343.1: #57's plan is approved and no worker started, yet after the end of a run its card is at ('Work', 'Autopilot'), not ('Plan', 'Autopilot')
> E               AssertionError: 343.2: a worker started on #57, yet after the end of a run the cards are at {'issue #57': ('Plan', None)}, not {'issue #57': ('Work', None)}
> E               AssertionError: 343.3: #57's worker has built it and nothing has started the code review, yet after the end of a run the cards are at {'issue #57': ('Review', None), 'pr #60': ('Review', None)}, not {'issue #57': ('Work', None), 'pr #60': ('Work', None)}
> E               AssertionError: 343.4: on #57 someone-else wrote '/work', which starts nothing, yet after the end of a run its card is at ('Work', 'Autopilot'), not in Plan with Autopilot
> E               AssertionError: 343.3: #57's code review sent it back and the worker built it again, yet after the end of a run the cards are at {'issue #57': ('Review', None), 'pr #60': ('Review', None)}, not {'issue #57': ('Work', None), 'pr #60': ('Work', None)}
> FAILED tests/test_work_column.py::test_an_approved_plan_waiting_on_a_blocker_stays_in_plan_and_its_card_names_the_blocker - AssertionError: 343.1: #57's approved plan waits on #332 and no worker started, yet after the end of a run its card is

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def live_card" -A25 dokima/agent.py | head -40
```

> 290:def live_card(role, stage, state, ahead=None):
> 291-    """The run's card while it is still running: queued (or waiting for the run `ahead` of it), setting up, agent
> 292-    working since the agent started, then checking the hand-back.
> 293-
> 294-    It carries its own marker and no JSON fold, so it never reads as a record; at the end of the run code edits this
> 295-    same comment into the run's record. A hand-off's queued card is put up before its run exists, so it links none.
> 296-    While the agent works the card is not edited, so it links the run's live page for detail."""
> 297-    head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker",
> 298-            "split": "Filing the split"}.get(role, "Command")
> 299-    repo = os.environ.get("GITHUB_REPOSITORY", "")
> 300-    run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
> 301-    head = role_icon(repo, role, stage) + f"**{head}**"
> 302-    if state in ("queued", "handoff"):
> 303-        if ahead:
> 304-            line = f"{icon(repo, 'queued')} {head} · waiting for [this run]({ahead})"
> 305-            what = (f"Queued, and waiting for [this run]({ahead}) on the same issue to end; this run starts after it. "
> 306-                    "This card says working when the agent starts, then becomes the run's record.")
> 307-        else:
> 308-            line = f"{icon(repo, 'queued')} {head} · queued"
> 309-            what = "Queued: the run

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["Re-planned after the owner's answer: a code review counts as started once its run card is up, even queued, and the issue then moves to Review.", "Added a test that a rebuilt issue, sent back by code review, stays in Work until the next code review's run card is up."],
  "decided": ["An approved plan stays in Plan until a code owner's /work, the bot's Autopilot start line or the worker's run card; only those move a card to Work or Review.", "Out of scope: the stage line on the issue card, cancelled worker runs, and a filed split's parent."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now builds on the owner's answer that a queued code review counts as started, and every new test fails today because the board misplaces approved, started and built issues.",
 "blockers": [],
 "notes": [
  {"text": "The Blocked by part of 343.1 already passes today, so it only guards against that line breaking; the board part of the same test is what fails today.", "evidence": "tests/test_work_column.py:89-96 checks '**Blocked by:** #332' on card.render; the test fails earlier, on the board place (Work instead of Plan)."},
  {"text": "AGENTS.md's board rule ('in the column the river placed it in after its newest record') is in scope and needs rewording to the new rule; no criterion checks it, so the code review should read it.", "evidence": "AGENTS.md, The board, first bullet; plan.json scope lists AGENTS.md."},
  {"text": "The rebuild test's first step (worker building again) already passes today; its second step, after the worker's second record, is the one that fails, which is the case the owner's rule changes.", "evidence": "pytest -q tests/test_work_column.py: test_a_rebuilt_issue_stays_in_work_until_its_next_code_review_starts fails with 'the worker built it again ... Review, not Work'."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask":
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** The check says the summary is too long, so I'm shortening it and running the check again.

`6. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";r=json.load(open(p))
r["summary"]="The plan follows the owner's answer that a queued code review counts as started, and every new test fails today for the right reason."
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 343 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #343 and saved the review to `/tmp/dokima-out/review.json`; both of the repo's checks on it pass.

**What the plan promises:**
- An approved plan stays in Plan until its worker starts, including while it waits on a blocker, and its card still says what it waits on.
- An issue moves to Work once its worker starts: your `/work`, the bot's Autopilot line that starts the worker, or the worker's run card.
- A built issue and its pull request stay in Work until the code review's run card is up, even queued, as you asked in your `/plan` comment. Then they move to Review. This also holds after a code review sends the work back and the worker builds it again.
- Only the bot's own lines and run cards, and your `/work`, move a card. The same words pasted by anyone else move nothing.

**Tests:** All six new tests in `tests/test_work_column.py` fail on today's code because the board puts cards in the wrong column, which is the right reason. The planner also changed one expectation in `tests/test_board_state.py`: an issue you already started with `/work` now goes to Work instead of Plan.

All four of your asks map to a criterion, and the plan has no open questions this round.

**Notes (not blocking):**
- The "Blocked by" check on the card already passes today, so it only guards that line against breaking. The part of that test that fails today is where the card sits on the board.
- The board rule in `AGENTS.md` is in scope and needs rewording to the new rule, but no test checks it. The code review should read it.
- In the rebuild test, the first step (the worker building again) already passes today. The step that fails is after the worker's second hand-back, which is the case your new rule changes.
