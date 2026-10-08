# reviewer (plan) for #202

Run: https://github.com/dokima-dev/dokima/actions/runs/37735485467

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #202: Board: the Priority pill follows the issue's priority label
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: an issue's priority label and its board Priority pill always agree**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: adding or removing the blocker, high or parked label sets the board's Priority field to match (Blocker, High, Parked, or empty)
> *Verified by: a test that a labeled and an unlabeled event set and clear the Priority field*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: an issue filed with a priority label shows the matching pill as soon as it lands on the board
> *Verified by: a test that a new issue with the blocker label gets Priority Blocker*
> 
> </dd></dl>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> Requested by Reza in chat, 2026-10-08.
> 
> <details><summary><b>Context</b></summary>
> 
> #201 was filed with the blocker label but its board card had no Blocker pill; the pill was set by hand. Nothing syncs labels to the board's Priority field today. Relates to #68 (auto-Blocker pil

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat .github/workflows/board.yml; wc -l dokima/board.py; git diff HEAD~1 -- tests/test_board.py
```

> commit be99c643b1868a098f85901476b65f61c17172b0
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:58:43 2026 +0000
> 
>     planner for #202 (run 37734795472)
> 
>  tests/test_board.py | 125 ++++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 125 insertions(+)
> name: board
> # Keeps the project board's Status and "Waiting on" current at every stage moment.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [labeled, closed]
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
>          

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat dokima/board.py; sed -n 1,100p tests/test_board.py; python -m pytest -q tests/test_board.py 2>&1 | tail -30
```

> """Keep the project board's Status and Action ("Needs you") current, from GitHub events.
> 
>     python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")
> 
> Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.I)
> YOUR_TURN = ("Plan written above", "**Planner question**", "**Plan rejected:**")
> 
> 
> def linked(body):
>     return [int(n) for n in CLOSES.findall(body or "")]
> 
> 
> def decide(event, p):
>     """[(kind, number, status, needs_you)]: kind is "issue" or "pr"; needs_you True marks it for the owner."""
>     out = []
>     if event == "issues":
>         n, action = p["issue"]["number"], p["action"]
>         if action == "labeled" and p["label"]["name"] == "plan":
>             out.append(("issue", n, "Plan", False))
>         elif action == "labeled" and p["label"]["name"] == "work":
>             out.append(("issue", n, "Work", False))
>         elif action == "closed":
>             out.append(("issue", n, "Done", False))
>     elif event == "issue_comment" and p["action"] == "created":
>         if p["comment"]["user"]["type"] == "Bot" and p["comment"]["body"].startswith(YOUR_TURN):
>             out.append(("issue", p["issue"]["number"], "Plan", True))
>     elif event in ("pull_request", "pull_request_target"):
>         pr, action = p["pull_request"], p["action"]
>       

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["Planned two criteria and one quality rule: priority labels set and clear the board's Priority pill, a newly filed issue lands with its pill, and a repo without a board or Priority field is left alone.",
          "Wrote six tests in tests/test_board.py; all six fail today because the feature is missing."],
  "decided": ["Adds unlabeled to the board workflow's issue triggers, which the owner accepted with /review.",
              "With two priority labels the higher one wins: Blocker, then High, then Parked."],
  "open": ["The worker is to update the AGENTS.md line that says priority is a field, not a label."]
 },
 "verdict": "approve",
 "summary": "The plan covers both of the owner's asks, the tests break if the pill is missing, wrong or left behind after a label is removed, and all six fail today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 202.1 adds a rule the owner did not state: other labels must never write the pill. Because of it, a design that re-syncs the pill on every issue event, which would also fix cards whose pill is already wrong, fails the tests. The rule keeps the change small, so this is a note, not a block.",
   "evidence": "tests/test_board.py::test_adding_a_priority_label_sets_the_matching_pill asserts priority_calls(gh) == [] for labeled/unlabeled bug and plan on an issue labeled blocker."},
  {"text": "The trigger test checks that labeled and unlabeled are present but not that closed stays. A worker who rewrote the line could drop closed, and no new test would catch it.",
   "evidence": "tests/test_board.py::test_workflow_runs_on_label_removal only asserts 'labeled' in types and 'unlabeled' in types; .github/workflows/board.yml line 7 today is types: [labeled, closed]."},
  {"text": "Removing a priority label from an issue that is not on the board would, through Board.item, add the issue to the board only
```

> (Bash completed with no output)

**Agent:** I approved the plan for #202 and wrote the review to `/tmp/dokima-out/review.json`. Both of Dokima's checks on the review file pass.

**Why it's approved:**
- **Both asks are covered.** Adding the blocker, high or parked label sets the board's Priority pill to match, and removing it clears the pill. An issue filed with a priority label (the #201 case) lands on the board with its pill already set. The planner asked about the two places your words left open, and your `/review` accepted its assumptions:
  - The board workflow also runs when a label is removed.
  - With two priority labels, the higher one wins.
- **The tests catch it if the feature is wrong.** They fail if:
  - the pill is wrong, or still set after its label is removed;
  - the lower of two priority labels wins;
  - a priority label moves the card or changes its Needs you pill;
  - a board with no Priority field gets written to.
- **They fail today for the right reason.** I ran `pytest -q tests/test_board.py`: the six new tests fail because the feature is missing, not because of a crash or a bad path. The eight existing tests pass.

**Notes (not blocking):**
- The plan adds a rule you didn't ask for: other labels must never write the pill. That keeps the change small, but it also rules out re-syncing the pill on every issue event, which would fix cards whose pill is already wrong.
- The workflow test checks that "labeled" and "unlabeled" are in the trigger list, but not that "closed" stays there.
- No test covers removing a priority label from an issue that isn't on the board yet. As the code stands, that would add the issue to the board just to clear its pill.

**Proposed new issue:** new cards land with no Status rather than in Backlog, which is what AGENTS.md says should happen. The code that adds a card to the board never sets its column.
