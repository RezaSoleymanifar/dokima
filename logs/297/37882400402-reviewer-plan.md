# reviewer (plan) for #297

Run: https://github.com/dokima-dev/dokima/actions/runs/37882400402

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:07 .
> drwxrwxrwt 19 root   root    4096 Oct  9 04:07 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:07 in
> -rw-r--r--  1 runner runner 16192 Oct  9 04:07 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 04:07 open_blockers.json
> -rw-r--r--  1 runner runner  5276 Oct  9 04:07 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:07 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:07 ..
> -rw-r--r-- 1 runner runner 5917 Oct  9 04:07 01-planner.json
> # Issue #297: The board shows Needs you only when something truly waits on me, and Autopilot otherwise
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #297](https://github.com/dokima-dev/dokima/issues/297)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" wid

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git show --stat HEAD | head -20; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print({k:v for k,v in d.items() if k!='handback'})"
```

> ef4930a planner for #297 (run 37880701207)
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
> bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
> commit ef4930ab447929341459d2b552858bed660ef2e4
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:07:09 2026 +0000
> 
>     planner for #297 (run 37880701207)
> 
>  tests/test_autopilot_board.py |   8 +-
>  tests/test_board.py           |   2 -
>  tests/test_needs_you.py       | 441 ++++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 445 insertions(+), 6 deletions(-)
> {'role': 'planner', 'stage': None, 'run_id': '37880701207', 'commit_before': 'fd83ff52ff633ce5098b2194e40439cb440e30a5', 'started_by': 'dokima-runtime[bot]', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 1289311, 'turns': 42, 'cost_usd': 3.22745, 'tokens_in': 4184720, 'tokens_out': 61771}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/297/37880701207-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/37880701207', 'check': {'passed': True, 'problems': []}}

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_needs_you.py; git show HEAD -- tests/test_autopilot_board.py tests/test_board.py
```

> <persisted-output>
> Output too large (30.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d1a8fdc9-a713-4191-803a-819056a9adc0/tool-results/b01b6kyi7.txt
> 
> Preview (first 2KB):
> """Needs you shows only while the river waits on the owner; Autopilot otherwise (#297).
> 
> Before this, the board put Needs you where nothing waited on the owner: every time the done-whens checks finished on a
> pull request (even one already merged), on closed issues a run stopped on after the owner had merged, and on parent
> issues left with the pill from before their split was filed. A Needs you the river did set was wiped by the next new
> commit, yet stayed for the whole run after the owner answered with a command. Nothing ever cleared old wrong pills.
> 
> Most tests fake dokima.board.Board and agent's `gh` against one in-memory world, so they read the board's end state:
> each card's Status and Action ("Needs you", "Autopilot" or none), each item's labels and whether it is closed, each
> issue's open pull request, sub-issues and Dokima records (the bot's record comments, read through `gh issue view`).
> On top of test_autopilot_board's fake Board, the board offers two more reads the code is expected to use:
> 
>     .state(kind, n) -> "open" | "closed"    a merged pull request is closed; raises subprocess.CalledProcessError
>                                              when GitHub cannot say
>     .needs_you_items() -> [(kind, n), ...]  every issue and pull request on the board wh

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 25,460p tests/test_needs_you.py
```

> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> import test_autopilot_board as tab  # noqa: E402
> from dokima import agent, board, card, plan  # noqa: E402
> from test_agent import GOOD_REVIEW, SPLIT, rec  # noqa: E402
> 
> LABEL = "autopilot"
> SPEC, REPO = "o/1", "o/r"
> OWNER = sorted(plan.repo_approvers("o"))[0]
> NEEDS, AUTO = "Needs you", "Autopilot"
> 
> 
> def split_filed(stories=(201, 202)):
>     """The Split filed record code posts on a parent once its stories are filed."""
>     return {"role": "split", "stage": None, "check": {"passed": True, "problems": []},
>             "handback": {"stories": [{"story": i, "issue": n, "title": f"Story {i}", "id": f"I_{n}", "blocked_by": []}
>                                      for i, n in enumerate(stories, 1)]}}
> 
> 
> def split_planned():
>     """A parent's records up to an approved split not filed yet, waiting for `/work`."""
>     return [rec("planner", handback=SPLIT), rec("reviewer", "plan", {**GOOD_REVIEW, "verdict": "approve", "blockers": []})]
> 
> 
> class World(tab.World):
>     """test_autopilot_board's world, plus which items are closed, which GitHub cannot read, sub-issues and records."""
> 
>     def __init__(self, closed=(), unreadable=(), subs=None, records=None, **kw):
>         super().__init__(**kw)
>         self.closed = set(closed)  # (kind, n)
>         self.unreadable = set(unreadable)  # numbers whose state GitHub will not give
>         self.subs = {k: list(v) for k, v in (subs or {}).item

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_needs_you.py 2>&1 | grep -E "^(FAILED|E  .*29[7]|[0-9]+ )|297\." | head -40; python -m pytest -q 2>&1 | tail -15
```

> Command did not complete within its 120s timeout and was moved to the background (ID: byw2b5oza). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/d1a8fdc9-a713-4191-803a-819056a9adc0/tasks/byw2b5oza.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Running the full test suite in the background; meanwhile checking how the board code finds a pull request when a run stops for the owner.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def move_card" -A45 dokima/agent.py | head -80
```

> 1591:def move_card(repo, number, column, needs_you, spec, q=None):
> 1592-    """Put the issue and its open pull request in that column, with the Needs you pill when the river stops for the
> 1593-    owner, else the Autopilot pill while the issue is on autopilot."""
> 1594-    from dokima import board
> 1595-    b = board.Board(spec, repo, q or board.gql)
> 1596-    targets = [("issue", int(number))]
> 1597-    pr = gh("pr", "list", "-R", repo, "--head", f"try/issue-{number}", "--state", "open", "--json", "number", "-q", ".[0].number").strip()
> 1598-    if pr:
> 1599-        targets.append(("pr", int(pr)))
> 1600-    pill = "Needs you" if needs_you else "Autopilot" if b.autopilot("issue", int(number)) else None
> 1601-    for kind, n in targets:
> 1602-        iid = b.item(kind, n)
> 1603-        b.set(iid, "Status", column)
> 1604-        b.set(iid, "Action", pill)
> 1605-    return targets
> 1606-
> 1607-
> 1608-def next_line(step, owners):
> 1609-    """The last line of a card: what happens next, mentioning the owner when it is their turn."""
> 1610-    if step[0] == "start" and step[1] == "split":
> 1611-        return "**Next:** The split's stories are filed now."
> 1612-    if step[0] == "start":
> 1613-        who = {"planner": "The planner", "worker": "The worker", "reviewer": "The reviewer"}[step[1]]
> 1614-        return f"**Next:** {who} starts now."
> 1615-    if step[0] in ("cancelled", "merged"):
> 1616-        return f"**Next:** {step[1]}"
> 1617-    mention = " ".join(f"@{o}" for o in owners)
> 1618-    return 

`7. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d1a8fdc9-a713-4191-803a-819056a9adc0/tasks/byw2b5oza.output | tail -40
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d1a8fdc9-a713-4191-803a-819056a9adc0/tasks/byw2b5oza.output tail -40. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 110 python -m pytest -q -x --timeout=20 tests/test_needs_you.py 2>&1 | tail -30 || true
```

> ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
> python -m pytest: error: unrecognized arguments: --timeout=20
>   inifile: None
>   rootdir: /home/runner/work/dokima/dokima

`9. Bash`
```
cd /home/runner/work/dokima/dokima; for t in test_a_check_finishing_never_marks_a_pull_request_for_the_owner test_needs_you_set_by_the_river_stays_through_new_commits_and_checks test_a_code_owners_command_clears_needs_you_at_once_and_nothing_else_does test_needs_you_never_lands_on_a_closed_issue_or_pull_request test_a_parent_shows_needs_you_only_for_its_own_stop test_a_merge_clears_the_wrong_pills_already_on_the_board test_the_real_board_lists_every_card_showing_needs_you test_the_real_board_tells_a_closed_item_from_an_open_one; do echo "== $t"; timeout 25 python -m pytest -q "tests/test_needs_you.py::$t" 2>&1 | grep -E "^E .*29|passed|failed|Timeout|Error" | head -4; echo "rc=$?"; done
```

> == test_a_check_finishing_never_marks_a_pull_request_for_the_owner
> E       AssertionError: 297.1: after the checks finished, the pull requests show {'pr #60': 'Needs you', 'pr #61': 'Needs you', 'pr #62': 'Needs you'}; a finished check must not mark one for the owner
> tests/test_needs_you.py:199: AssertionError
> FAILED tests/test_needs_you.py::test_a_check_finishing_never_marks_a_pull_request_for_the_owner - AssertionError: 297.1: after the checks finished, the pull requests show {'pr #60': 'Needs you', 'pr #61': 'Needs you', 'pr #62': 'Needs you'}; a finished check must not mark one for the owner
> 1 failed in 0.04s
> rc=0
> == test_needs_you_set_by_the_river_stays_through_new_commits_and_checks
> E       AssertionError: 297.1: a new commit on PR #62 took Needs you away though the owner answered nothing: {'issue #59': None, 'pr #62': None}
> tests/test_needs_you.py:218: AssertionError
> FAILED tests/test_needs_you.py::test_needs_you_set_by_the_river_stays_through_new_commits_and_checks - AssertionError: 297.1: a new commit on PR #62 took Needs you away though the owner answered nothing: {'issue #59': None, 'pr #62': None}
> 1 failed in 0.19s
> rc=0
> == test_a_code_owners_command_clears_needs_you_at_once_and_nothing_else_does
> E       AssertionError: 297.2: the code owner said /work on #57, on autopilot, and the cards show {'issue #57': 'Needs you', 'pr #60': 'Needs you'}, not Autopilot
> tests/test_needs_you.py:251: AssertionError
> FAILED tests/test_needs_you.py::test_a_code_owners_command_clears_

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q tests/test_board.py tests/test_autopilot_board.py 2>&1 | tail -5; grep -n "PR_NUMBER\|issue_comment\|pull_request_review\|on:" -A3 .github/workflows/board.yml | head -30
```

> .......................................                                  [100%]
> 39 passed in 0.05s
> 6:on:
> 7-  issues:
> 8-    types: [labeled, unlabeled, closed]
> 9:  issue_comment:
> 10-    types: [created]
> 11-  # pull_request_target runs main's copy of this file, so the keys environment opens;
> 12-  # this job only checks out main's code, never the PR's.
> --
> 27:    runs-on: ubuntu-24.04
> 28-    steps:
> 29-      - uses: actions/checkout@v5
> 30-        with:
> --
> 35:          python-version: "3.12"
> 36-      - id: app
> 37-        uses: actions/create-github-app-token@v2
> 38-        with:

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner wrote five criteria for Needs you on the board, with eight tests in tests/test_needs_you.py that all fail today because the feature is missing, and edited two old tests that expected finished checks to set Needs you."],
  "decided": ["Finished checks never set Needs you, a code owner's command comment clears it at once, and closed items never get it.", "The board run of every merge clears Needs you on closed items and on parents whose split is filed."],
  "open": ["Whether a command in a pull request review's summary clears Needs you at once (assumed no, so no workflow file changes).", "This plan was written before the owner's /plan comment at 03:52 and does not take it in yet."]
 },
 "verdict": "block",
 "summary": "The plan does not include the one-time sweep of every board item that the owner asked for in their /plan comment, and no criterion states that an item on autopilot always shows exactly one of Autopilot or Needs you.",
 "blockers": [
  {"id": "B1", "criterion": "297.5", "test": "tests/test_needs_you.py::test_a_merge_clears_the_wrong_pills_already_on_the_board",
   "problem": "The owner asked for a one-time sweep, right after this merges, that goes over every item on the board and sets each pill to what it should be by these rules. Criterion 297.5 is narrower. It only takes Needs you off closed items, at every merge. An open item with a wrong Needs you that nothing waits on (other than a parent with a filed split), and an open item on autopilot that shows no pill, are left as they are. Nothing in the plan runs once right after this merges.",
   "evidence": "Owner's /plan comment on #297 (2026-10-09T03:52:03Z): 'Right after this merges, a one-time sweep goes over every item on the board and sets each pill to what it should be by these rules, so the backlog of wrong pills is cleared once.' The test's board holds only closed items and open items t
```

> summary holds 39 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

**Agent:** Shortening the summary to pass the hand-back check.

`12. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan misses the owner's one-time sweep of every board item and the rule that autopilot items show exactly one pill."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 297 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for #297, and the review is in `/tmp/dokima-out/review.json`. It passes both hand-back checks.

The planner wrote this plan before the owner's `/plan` comment at 03:52, so the plan doesn't include the asks in that comment yet. A second planner run is already queued.

**Blockers (both for the planner):**
- **B1:** The owner asked for a one-time sweep, right after this merges, that sets every pill on the board by the new rules. Criterion 297.5 does less: at every merge it only takes Needs you off closed items. Open items that show Needs you while nothing waits on the owner keep it, and open items on autopilot that show no pill stay that way. The test for 297.5 would pass with code that only clears closed items.
- **B2:** The owner's rule "never both and never neither" (an item on autopilot shows exactly one of Autopilot or Needs you) is not stated anywhere as a criterion. It only appears as side clauses in particular moments, and no test checks it in general.

**The plan's one question:** I did not accept its assumption that a command in a pull request review's summary keeps Needs you until the run ends. The owner wrote that Needs you "clears the moment that is answered", and AGENTS.md counts a command in a review's summary as an answer. Since the issue is on autopilot, this question stops for the owner.

**Notes:**
- Criterion 297.3 shows Needs you when GitHub can't say whether an item is closed. That fails safe, but the owner wrote that a closed item "can never get Needs you", so the re-plan should check that it still matches their words, or ask.
- All eight new tests fail today for the right reason: the feature is missing. The two edited test files still pass (39 passed).

`13. Bash`
```
tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/d1a8fdc9-a713-4191-803a-819056a9adc0/tasks/byw2b5oza.output
```

> FAILED tests/test_needs_you.py::test_the_real_board_lists_every_card_showing_needs_you - Failed: 297.5: the real Board cannot list the cards showing Needs you yet (it has no needs_you_items)
> FAILED tests/test_needs_you.py::test_the_real_board_tells_a_closed_item_from_an_open_one - Failed: 297.3: the real Board cannot read whether an issue or pull request is closed yet (it has no state)
> FAILED tests/test_plan_links_recorded.py::test_links_with_no_loop_are_recorded_and_autopilot_goes_on - AssertionError: 252.3: autopilot should start the worker, the river said 'stop'
> assert 'stop' == 'start worker'
>   
>   - start worker
>   + stop
> FAILED tests/test_plan_links_recorded.py::test_recorded_links_let_autopilot_go_on - AssertionError: 252.5: autopilot should start the worker, the river said 'stop'
> assert 'stop' == 'start worker'
>   
>   - start worker
>   + stop
> 10 failed, 680 passed in 243.61s (0:04:03)
> 
> [exited with code 0]

`14. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "import\|tab\." tests/test_plan_links_recorded.py | head; git stash list; git worktree add -q /tmp/mainwt main 2>&1; cd /tmp/mainwt && timeout 200 python -m pytest -q tests/test_plan_links_recorded.py 2>&1 | tail -3
```

> 25:import json
> 26:import os
> 27:import re
> 28:import subprocess
> 29:import sys
> 31:import pytest
> 35:from dokima import agent, body  # noqa: E402
> 46:import json, os, re, sys
> ..................                                                       [100%]
> 18 passed in 13.95s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`15. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 200 python -m pytest -q tests/test_plan_links_recorded.py 2>&1 | tail -3; git diff main --stat
```

> - start worker
>   + stop
> 2 failed, 16 passed in 13.81s
>  .github/workflows/done-whens.yml  |   6 +-
>  .github/workflows/full-suite.yml  |   3 +-
>  AGENTS.md                         |   2 +-
>  dokima/agent.py                   |  81 +------
>  dokima/checks.py                  |  17 +-
>  tests/test_autopilot_board.py     |   8 +-
>  tests/test_blocked_worker.py      | 290 -------------------------
>  tests/test_board.py               |   2 -
>  tests/test_merge_queue.py         | 366 -------------------------------
>  tests/test_needs_you.py           | 441 ++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_links_recorded.py |  10 +-
>  11 files changed, 455 insertions(+), 771 deletions(-)

`16. Bash`
```
cd /tmp/mainwt && git checkout -q fd83ff5 && timeout 200 python -m pytest -q tests/test_plan_links_recorded.py 2>&1 | tail -2; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt
```

> + stop
> 2 failed, 16 passed in 25.99s

**Agent:** I checked the whole test suite after the review was already written, and nothing in it changes. The review still blocks the plan for #297 on the same two points, and I didn't edit `review.json`.

On the branch, 10 tests fail out of 690:

- **Eight are the new tests in `tests/test_needs_you.py`.** Each fails because the feature is missing, which is what the plan expects at this stage.
- **Two are in `tests/test_plan_links_recorded.py`.** They expect autopilot to start the worker, but the river answers "stop". These fail on the commit the branch started from too, and pass on the current `main`, so a later commit on `main` fixed them. They have nothing to do with this plan.
