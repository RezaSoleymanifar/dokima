# reviewer (plan) for #135

Run: https://github.com/dokima-dev/dokima/actions/runs/37729561137

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 36
> drwxr-xr-x  3 runner runner 4096 Oct  8 04:52 .
> drwxrwxrwt 18 root   root   4096 Oct  8 04:52 ..
> drwxr-xr-x  2 runner runner 4096 Oct  8 04:52 in
> -rw-r--r--  1 runner runner 9375 Oct  8 04:52 issue.md
> -rw-r--r--  1 runner runner    2 Oct  8 04:52 open_blockers.json
> -rw-r--r--  1 runner runner 4655 Oct  8 04:52 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 04:52 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 04:52 ..
> -rw-r--r-- 1 runner runner 5294 Oct  8 04:52 01-planner.json
> # Issue #135: Board: a refresh button puts every card back where it belongs
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #136](https://github.com/dokima-dev/dokima/pull/136) · [files changed](https://github.com/dokima-dev/dokima/pull/136/files)
> 
> **Objective: Running the board workflow by hand (the "Run workflow" button) moves every card on the board to the column its real state says: closed is Done, an open pull request is Review, the `work` label is Work, the `plan` label is Plan, anything else is Backlog.**
> 
> <dl><dd>
> 
> </dd></dl>
> 
> **Objective: Closed items lose their Needs you flag; open items keep whatever flag they have.**
> 
> <dl><dd>
> 
> </dd></dl>
> 
> **Objective: The board's description links to the button.**
> 
> <dl><dd>
> 
> </dd></dl>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37415656886/job/112113581599)
> 
> <!

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l dokima/board.py dokima/agent.py tests/test_board.py; cat .github/workflows/board.yml; grep -rn -i "needs you" --include=*.py dokima | head -40
```

> commit 5662336fdb9cb7670bb2c2f21e2ef4930392a350
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 04:37:39 2026 +0000
> 
>     planner for #135 (run 37727796467)
> 
>  tests/test_board.py | 404 ++++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 404 insertions(+)
>   113 dokima/board.py
>   881 dokima/agent.py
>   508 tests/test_board.py
>  1502 total
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
>       

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat dokima/board.py; sed -n 680,881p dokima/agent.py
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
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_board.py | sed -n 1,480p
```

> commit 5662336fdb9cb7670bb2c2f21e2ef4930392a350
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 04:37:39 2026 +0000
> 
>     planner for #135 (run 37727796467)
> 
> diff --git a/tests/test_board.py b/tests/test_board.py
> index 5549900..3e2380b 100644
> --- a/tests/test_board.py
> +++ b/tests/test_board.py
> @@ -1,4 +1,8 @@
> +"""Tests for the project board: stage moves from GitHub events, the refresh button, and the Needs you pill.
> +
> +The board is never real here: either a fake GraphQL function or a fake `gh` on PATH stands in for GitHub."""
>  import os
> +import re
>  import sys
>  
>  sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> @@ -102,3 +106,403 @@ def test_lanes_are_needs_you_or_nothing(record_property):
>      gh = FakeGitHub(on_board=True)
>      board.sync("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": "**Planner question**"}}, "dokima-dev/1", "o/r", q=gh)
>      assert any(v.get("o") == "w-you" for _, v in gh.calls), "130.1: a question for the owner did not land in Needs you"
> +
> +
> +# 135: the board's own button puts every card back where its records say, and every board update
> +# recomputes each card's Needs you from its latest record.
> +#
> +# These tests run Dokima the way the workflows do (`python3 -m dokima.board`, `python3 -m dokima.agent board|split`)
> +# with a fake `gh` first on PATH. The fake keeps a whole small repo and board in one JSON file: issues, pull requests,
> +# t

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,30p tests/test_board.py; python -m pytest -q tests/test_board.py 2>&1 | grep -E "Error|assert|passed|failed|135\." | head -60
```

> """Tests for the project board: stage moves from GitHub events, the refresh button, and the Needs you pill.
> 
> The board is never real here: either a fake GraphQL function or a fake `gh` on PATH stands in for GitHub."""
> import os
> import re
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import board  # noqa: E402
> 
> WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "board.yml")
> BOT, YOU = {"type": "Bot"}, {"type": "User"}
> 
> 
> def pr(action, number=7, body="Closes #5", merged=False):
>     return {"action": action, "pull_request": {"number": number, "body": body, "merged": merged}}
> 
> 
> # 116.1: every stage moment sets the stage and whose turn it is
> 
> def test_issue_stage_moments(record_property):
>     record_property("proves", "116.1")
>     issue = {"number": 5}
>     assert board.decide("issues", {"action": "labeled", "label": {"name": "plan"}, "issue": issue}) == [("issue", 5, "Plan", False)]
>     assert board.decide("issues", {"action": "labeled", "label": {"name": "work"}, "issue": issue}) == [("issue", 5, "Work", False)]
>     assert board.decide("issues", {"action": "closed", "issue": issue}) == [("issue", 5, "Done", False)]
>     assert board.decide("issues", {"action": "labeled", "label": {"name": "bug"}, "issue": issue}) == []
> 
> 
> def test_plan_ready_question_or_rejection_is_your_turn(record_property):
>         record_property("proves", "135.1")
>         assert p.returncode == 0, f"135.1: the button's run failed: {p.std

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | tail -12; grep -rn -i "needs you list\|the table\|needs-you" --include=*.py --include=*.md --include=*.yml . | grep -v "^./tests/test_board" | head
```

> FAILED tests/test_board.py::test_only_the_bots_records_set_needs_you - AssertionError: 135.5: a record pasted by a person cleared Needs you: ('Plan', None)
> assert ('Plan', None) == ('Plan', 'Needs you')
>   
>   At index 1 diff: None != 'Needs you'
>   
>   Full diff:
>     (
>         'Plan',
>   -     'Needs you',
>   +     None,
>     )
> 8 failed, 270 passed in 18.66s

**Agent:** Every new test fails today for the right reason and the old tests pass. Now I'm checking how the existing code tells a bot's record from a pasted one, for the 135.5 test.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def records\|def is_record\|dokima-runtime\|BOT_LOGIN\|def conversation" -A8 dokima/agent.py | head -70
```

> 27:BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
> 28-HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 29-
> 30-
> 31-def linked_prs(repo, number):
> 32-    """Pull requests built for the issue: from its work or try branch."""
> 33-    found = []
> 34-    for head in (f"work/issue-{number}", f"try/issue-{number}"):
> 35-        found += json.loads(gh("pr", "list", "-R", repo, "--head", head, "--state", "all", "--json", "number"))
> --
> 39:def conversation(repo, number):
> 40-    """The issue and its pull requests as one list of comments, oldest first, each saying where it was written."""
> 41-    d = json.loads(gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,comments"))
> 42-    items = [{**c, "where": f"issue #{number}"} for c in d["comments"]]
> 43-    for pr in linked_prs(repo, number):
> 44-        p = json.loads(gh("pr", "view", str(pr), "-R", repo, "--json", "comments,reviews"))
> 45-        items += [{**c, "where": f"PR #{pr}"} for c in p["comments"]]
> 46-        items += [{"author": r["author"], "body": r["body"], "createdAt": r["submittedAt"], "where": f"PR #{pr} review ({r['state'].lower()})"}
> 47-                  for r in p["reviews"] if r.get("body")]
> --
> 63:def records(items):
> 64-    """Every agent record in the conversation, oldest first. Only comments the bot posted count: anyone can paste text."""
> 65-    out = []
> 66-    for c in items:
> 67-        body = c.get("body") or ""
> 68-        if (c.get("author") or {}).get("login"

**Agent:** The plan holds up; I'm writing the review and running its check.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned the board refresh as four criteria and one safety rule, with eight new tests in tests/test_board.py that run Dokima against a fake GitHub."],
  "decided": ["The button places cards by their latest bot record, not by the plan and work labels.",
              "Every board update recomputes the Needs you pill on every card; a reviewer-approved PR and its issue need you until merged."],
  "open": ["Three questions, which the owner answered with /review, so the planner's assumptions stand."]},
 "verdict": "approve",
 "summary": "The plan covers everything you asked for, including the two additions from your last comment. Every criterion has a test that runs Dokima end to end, and each test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 135.2 promises a recount on each GitHub event the board handles, but the test only closes an issue. A build that recounts only on that one event would still pass. Adding a second event, such as a pull request opened or a comment, would close that gap.",
   "evidence": "tests/test_board.py::test_an_event_update_recomputes_every_cards_needs_you sends only event=issues, action=closed. dokima/board.py sync() returns early when decide() finds no changes, so recounting on events that change nothing is a separate piece of work."},
  {"text": "Criterion 135.1 needs a new manual trigger in .github/workflows/board.yml. The bot cannot push workflow changes, so this step may need you to push or approve it.",
   "evidence": "AGENTS.md, Identity and safety: 'The bot can't ... push workflow changes'; the pause for owner approval is still marked (planned). tests/test_board.py::test_the_board_workflow_has_the_button checks for workflow_dispatch in board.yml."},
  {"text": "Every new test fails today for the right reason and the 270 existing tests still pass.",
   "evidence": "pytest -q: 8 failed, 27
```

> rc=0

**Agent:** I approved the plan for #135, with three notes. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Why it's approved:**
- **Your asks are all there.** The plan has the refresh button, the board description linking to the button, and closed items losing the pill. It also has the two additions from your last `/plan` comment: every board update recounts each card's Needs you from its latest record, and a pull request the reviewer approved needs you until it merges.
- **Its three assumptions stand.** You answered with `/review`, so the planner's readings apply:
  - Cards are placed by their latest record, not by the plan and work labels.
  - "Approved" means the reviewer's approval, not your own Approve on GitHub.
  - Every card's pill is recounted on every update, not just the cards that move.
- **Each criterion has a test that runs Dokima end to end** against a fake GitHub. They check both ways: cards that should get the pill do, and cards that shouldn't don't. That includes a record someone pastes that would fake or clear the pill.
- **The new tests fail today for the right reason.** Running `pytest -q` gives 8 failed and 270 passed. All 8 failures are the new tests, and each fails because the feature is missing (cards in the wrong column, stale pills, no button, no link), not because of a crash or a bad path.

**Notes (not blockers):**
1. **One gap in the 135.2 tests (the pill recount):** the plan promises a recount on every GitHub event the board workflow handles, but the test only covers closing an issue. A build that recounts only on that event would still pass. Testing a second event, such as a pull request opened, would close the gap.
2. **The button needs a change to `.github/workflows/board.yml`, and the bot can't push workflow changes.** The step that would pause for your approval isn't built yet, so you may have to push or approve that change yourself.
3. The existing tests still pass alongside the new ones.
