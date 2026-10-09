# reviewer (plan) for #291

Run: https://github.com/dokima-dev/dokima/actions/runs/37884870942

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (115.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/862b6f54-7c58-46cb-be31-d3596b1194df/tool-results/bb414gqpo.txt
> 
> Preview (first 2KB):
> .:
> total 136
> drwxr-xr-x  3 runner runner   4096 Oct  9 04:39 .
> drwxrwxrwt 18 root   root     4096 Oct  9 04:39 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 04:39 in
> -rw-r--r--  1 runner runner 114143 Oct  9 04:39 issue.md
> -rw-r--r--  1 runner runner   2711 Oct  9 04:39 open_blockers.json
> -rw-r--r--  1 runner runner   7921 Oct  9 04:39 plan.json
> 
> in:
> total 80
> drwxr-xr-x 2 runner runner  4096 Oct  9 04:39 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 04:39 ..
> -rw-r--r-- 1 runner runner 10086 Oct  9 04:39 01-planner.json
> -rw-r--r-- 1 runner runner  3892 Oct  9 04:39 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  1844 Oct  9 04:39 03-worker.json
> -rw-r--r-- 1 runner runner  2573 Oct  9 04:39 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 12310 Oct  9 04:39 05-planner.json
> -rw-r--r-- 1 runner runner   342 Oct  9 04:39 06-updater.json
> -rw-r--r-- 1 runner runner  7842 Oct  9 04:39 07-reviewer-plan.json
> -rw-r--r-- 1 runner runner  8573 Oct  9 04:39 08-planner.json
> -rw-r--r-- 1 runner runner   342 Oct  9 04:39 09-updater.json
> -rw-r--r-- 1 runner runner   342 Oct  9 04:39 10-updater.json
> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 264, 282, 295, 305 -->
> The criteria workflow is r

`2. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|dokima-original\|Original issue" issue.md | head -80; wc -l issue.md
```

> 53:<details><summary>Original issue</summary>
> 80:## Comments
> 82:### dokima-runtime on issue #291 (2026-10-09T01:30:31Z)
> 86:### dokima-runtime on issue #291 (2026-10-09T01:30:45Z)
> 304:### dokima-runtime on issue #291 (2026-10-09T01:39:02Z)
> 435:### dokima-runtime on issue #291 (2026-10-09T01:45:21Z)
> 440:### dokima-runtime on issue #291 (2026-10-09T01:45:23Z)
> 504:### dokima-runtime on PR #293 (2026-10-09T01:52:04Z)
> 597:### RezaSoleymanifar on issue #291 (2026-10-09T03:57:11Z)
> 601:### dokima-runtime on issue #291 (2026-10-09T03:57:32Z)
> 852:### dokima-runtime on PR #293 (2026-10-09T04:04:33Z)
> 856:### dokima-runtime on issue #291 (2026-10-09T04:04:35Z)
> 893:### dokima-runtime on issue #291 (2026-10-09T04:08:50Z)
> 1092:### RezaSoleymanifar on issue #291 (2026-10-09T04:26:34Z)
> 1096:### dokima-runtime on issue #291 (2026-10-09T04:26:56Z)
> 1285:### dokima-runtime on PR #293 (2026-10-09T04:29:16Z)
> 1289:### dokima-runtime on issue #291 (2026-10-09T04:29:19Z)
> 1326:### dokima-runtime on PR #293 (2026-10-09T04:34:36Z)
> 1330:### dokima-runtime on issue #291 (2026-10-09T04:34:38Z)
> 1367:### dokima-runtime on issue #291 (2026-10-09T04:39:03Z)
> 1375 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 1,80p issue.md; sed -n 595,600p issue.md; sed -n 1090,1096p issue.md; sed -n 1280,1375p issue.md
```

> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 264, 282, 295, 305 -->
> The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.
> 
> **Plan**
> 
> [issue #291](https://github.com/dokima-dev/dokima/issues/291) · [PR #293](https://github.com/dokima-dev/dokima/pull/293) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/293/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #262, #292, #264, #282, #295, #305
> 
> **User story:** The owner sees the criteria checks under a workflow named Acceptance criteria and finds no done-when anywhere they read except in the names of checks #262 renames, while main's branch rule stays exactly as it is.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** The workflow that

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; python3 -c "
import json;d=json.load(open('in/07-reviewer-plan.json'));print(json.dumps(d,indent=1))"
```

> {
>  "kind": "user_story",
>  "summary": "The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.",
>  "user_story": "The owner sees the criteria checks under a workflow named Acceptance criteria and finds no done-when anywhere they read except in the names of checks #262 renames, while main's branch rule stays exactly as it is.",
>  "acceptance_criteria": [
>   {
>    "text": "The workflow that holds the criteria checks is named Acceptance criteria, with no number, in the file .github/workflows/acceptance-criteria.yml; done-whens.yml is gone. It still runs on every pull request and in the merge queue, each criterion keeps its own check named by its number and words, and the gate still passes only when every criterion's check passed. The card and the board still update when it finishes, and the card still redraws when the all tests check finishes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/291"
>   },
>   {
>    "text": "No check changes its name, so main's branch rule stays as it is until #262. The check running every test is still all tests, in the workflow full suite. The criteria workflow's checks are still list done-whens and all done-whens passed. The manifest still requires all tests and all done-whens passed on main, and the card still shows the all tests verdict. AGENTS.md does not tell the owner to switch the branch rule.",
>    "source": "https://github.com/dokima-dev/dokima/issue

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --graph; git merge-base --is-ancestor d99847b HEAD && echo has270; ls tests/test_merge_queue.py; git fetch -q origin main 2>&1|tail -1; git log --oneline -5 origin/main; git merge-base HEAD origin/main
```

> * 355128a planner for #291 (run 37883897217)
> *   46e839b Merge branch 'main' into try/issue-291
> |\  
> | * 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
> * | 6ac9bf9 Merge branch 'main' into try/issue-291
> |\| 
> | * fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
> * | 016d6af Merge branch 'main' into try/issue-291
> |\| 
> | * bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
> * | c610eb4 worker for #291 (run 37871310094)
> ls: cannot access 'tests/test_merge_queue.py': No such file or directory
> e1a21e7 Three kinds of raise and one table of who raises to whom, checked by code (#304)
> 436b3e8 The plan check re-runs when a plan is approved, so it never shows a stale failure (#303)
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
> 5261412e0a8b066c19ecc4d8c067f036f65427f7

**Agent:** I'm checking the plan's tests on the branch and comparing them with today's main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_check_names.py 2>&1 | tail -15; python -m pytest -q 2>&1 | tail -3; git diff --stat HEAD origin/main -- tests | tail -5; git grep -nic 'done.when' origin/main -- tests/test_merge_queue.py dokima .github | head -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: brl5vfiyp). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/862b6f54-7c58-46cb-be31-d3596b1194df/tasks/brl5vfiyp.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python -m pytest -q -p no:cacheprovider tests/test_check_names.py 2>&1 | grep -E "FAILED|passed|failed|Error" | head -20
```

> E       AssertionError: 291.1: the Acceptance criteria workflow no longer runs on pull requests and in the merge queue: ['pull_request_target']
> tests/test_check_names.py:76: AssertionError
> E       AssertionError: 291.1: the card no longer redraws when the all tests check finishes; card.yml waits on ['Acceptance criteria', 'All tests', 'worker']
> tests/test_check_names.py:111: AssertionError
>         criteria workflow's checks are still named list done-whens and all done-whens passed; that no workflow has a check
>         named All tests or Acceptance criteria; that the manifest still requires all tests and all done-whens passed on
> E       AssertionError: 291.2: full-suite.yml is no longer the workflow full suite with the one check all tests: {'name': 'All tests', 'on': {'pull_request_target': '', 'push': {'branches': ['main']}}, 'permissions': {'contents': 'read'}, 'jobs': {'all-tests': {'name': 'All tests', 'runs-on': 'ubuntu-24.04', 'steps': [{'uses': 'actions/checkout@v5', 'with': {'ref': '${{ github.event.pull_request.head.sha || github.sha }}', 'persist-credentials': 'false'}}, {'uses': 'actions/setup-python@v6', 'with': {'python-version': '3.12'}}, {'run': 'pip install -q pytest'}, {'run': 'pytest -q -p no:cacheprovider tests'}]}}}
> tests/test_check_names.py:127: AssertionError
> FAILED tests/test_check_names.py::test_the_criteria_workflow_is_named_acceptance_criteria_in_its_own_file - AssertionError: 291.1: the Acceptance criteria workflow no longer runs on pull requests and

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,400p tests/test_check_names.py
```

> """The criteria workflow becomes Acceptance criteria, no check is renamed, and done-when is gone.
> 
> Story 1 of #262. The owner left every check rename, all tests included, to #262, so main's branch rule only changes
> once. This story renames only the workflow that holds the criteria checks, from done-whens in done-whens.yml to
> Acceptance criteria in acceptance-criteria.yml, and takes the word done-when out of every other place a person reads.
> The card and the board start through `workflow_run` by workflow name, so the tests read those names out of card.yml and
> board.yml and match them against the workflows the repo really has. One test reads every file in the repo for the old
> word; the exceptions are the names of the checks that keep them until #262 (all done-whens passed and list done-whens),
> the owner's older "Done when:" plan lines Dokima still reads, and copies of past records in tests/samples.
> """
> import os
> import re
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent, card, checks, manifest  # noqa: E402
> 
> import test_card_records as tcr  # noqa: E402
> import test_start as ts  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
> CRITERIA = "Acceptance criteria"
> ALL_TESTS, GATE, LIST = "all tests", "all done-whens passed", "list done-whens"
> OLD_WORD = re.compile(r"done[\s_-]*whens?", re.I)
> 
> 
> def workflows():
>     """Every w

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git diff origin/main HEAD --stat | tail -30; git show origin/main:AGENTS.md | grep -n "rename\|Definition of Done, in order" ; for f in $(git diff --name-only HEAD origin/main); do git show origin/main:$f 2>/dev/null | grep -nic 'done.when' | sed "s|^|$f: |"; done | grep -v ": 0$"
```

> .../{done-whens.yml => acceptance-criteria.yml}    |  18 +-
>  .github/workflows/agent.yml                        |   7 -
>  .github/workflows/board.yml                        |   2 +-
>  .github/workflows/card.yml                         |   2 +-
>  .github/workflows/full-suite.yml                   |   7 +-
>  AGENTS.md                                          |   5 +
>  dokima/agent.py                                    |  58 +---
>  dokima/app.json                                    |   2 +-
>  dokima/card.py                                     |   2 +-
>  dokima/checks.py                                   |  21 +-
>  dokima/manifest.py                                 |   2 +-
>  dokima/raises.py                                   | 117 -------
>  tests/test_autopilot_board.py                      |   2 +-
>  tests/test_check_names.py                          | 225 +++++++++++++
>  tests/test_checks.py                               |   2 +-
>  tests/test_manifest.py                             |   6 +-
>  tests/test_merge_check.py                          |  12 +-
>  tests/test_merge_queue.py                          | 366 ---------------------
>  tests/test_plan_check_rerun.py                     | 332 -------------------
>  tests/test_raises.py                               | 329 ------------------
>  20 files changed, 270 insertions(+), 1247 deletions(-)
> .github/workflows/board.yml: 1
> .github/workflows/card.yml: 1
> .github/workflows/done-whens.yml: 6
> dokima/agent.py: 1
> dokima/checks.py: 2
> dokima/manifest.py: 2

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/main:tests/test_plan_check_rerun.py | grep -ni 'done.when\|full suite\|all tests'; git show origin/main:tests/test_merge_queue.py | grep -ni 'done.when\|done-whens.yml' | head -30; git show origin/main:dokima/manifest.py | grep -ni 'done.when'
```

> 3:The plan check is the done-whens workflow (.github/workflows/done-whens.yml): its `list` job reads the issue's records
> 4:and builds one check per criterion of the approved plan, and its gate, "all done-whens passed", fails with "No approved
> 17:  - the runs: `gh api repos/o/r/actions/runs` and `repos/o/r/actions/workflows/done-whens.yml/runs` (the file name or
> 166:    return {"id": rid, "name": "done-whens", "path": ".github/workflows/done-whens.yml", "event": "pull_request_target",
> 5:done-whens.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> 177:    """The pull_request_target payload done-whens.yml gets for pull request n."""
> 240:    lines = workflow("done-whens.yml")
> 260:    Proves 191.1. Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
> 261:    the done-whens check checks out and the commit its annotations link to for a merge_group event, and checks both are
> 265:    for name in ("full-suite.yml", "done-whens.yml"):
> 273:    assert refs and heads, "191.1: done-whens.yml has no `ref:` on the checkout with `path: pr` or no HEAD_SHA"
> 277:            assert got is not None, f"191.1: done-whens.yml {what} `{expr}` is not `${{{{ a || b }}}}` of github.sha / github.event paths"
> 279:                f"191.1: in the merge queue the done-whens {what} `{expr}` gives {got!r}, not the queued commit {QUEUE_SHA}"
> 285:    """In the queue, the done-whens find the PR's issue 

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git grep -n 'done-whens' origin/main -- dokima .github | grep -v "all done-whens passed\|list done-whens"
```

> origin/main:.github/workflows/board.yml:16:    workflows: [done-whens]
> origin/main:.github/workflows/card.yml:8:    workflows: [done-whens, full suite, worker]
> origin/main:.github/workflows/done-whens.yml:1:name: done-whens
> origin/main:.github/workflows/done-whens.yml:73:            echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
> origin/main:dokima/agent.py:1235:PLAN_CHECK = "done-whens.yml"

**Agent:** Round three still has the main-merge blocker, so I'm writing an escalation.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner rewrote the plan so no check changes its name: only the criteria workflow is renamed Acceptance criteria, in acceptance-criteria.yml.",
   "The planner committed the plan's four tests in tests/test_check_names.py and its six test changes to the branch."
  ],
  "decided": [
   "The workflow full suite, the AGENTS.md list of checks with its branch rule sentence, and autopilot requiring the new check names all move to #262 with the check renames."
  ],
  "open": [
   "The planner says it cannot change tests/test_merge_queue.py, because that file is on main but not on this branch, and asks code to merge main into the branch first.",
   "No open story under #262 renames the checks yet."
  ]
 },
 "verdict": "escalate",
 "summary": "The plan follows your answer and its tests are now on the branch, but it still cannot pass: tests on today's main open done-whens.yml and say done-when, and the planner cannot change them until main is merged into this branch.",
 "blockers": [
  {
   "id": "B2",
   "criterion": "291.1",
   "test": "tests/test_check_names.py::test_no_text_a_person_reads_says_done_when",
   "problem": "Today's main has tests that this plan breaks, and the plan's test changes leave them out. tests/test_merge_queue.py (#270) opens done-whens.yml by path and says done-whens in its docstrings and messages. tests/test_plan_check_rerun.py (#303, new since the last review) says done-whens.yml and the done-whens workflow, and fakes a run at that path. main's dokima/agent.py also finds the plan check by the file name done-whens.yml. When the worker merges main, renaming the file breaks All tests, and 291.3 fails on both test files, which the worker cannot change. The planner agrees and says it cannot change files that are not on its branch. The reviewer and the planner disagree only on who unblocks it: the reviewer holds that the plan cannot pass as it stan
```

> Exit code 1
> summary holds 40 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> blocker B2 names tests/test_check_names.py::test_no_text_a_person_reads_says_done_when, which is not one of the plan's tests for 291.1

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; d=json.load(open(p))
d["summary"]="The plan follows your answer, but it cannot pass until main is merged into this branch, because main's newer tests still use done-whens.yml."
d["blockers"][0]["criterion"]="291.3"
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 291 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I escalated this plan review to you. The plan follows your answer, but it can't pass until `main` is merged into `try/issue-291`.

- **B1, the plan's tests weren't on the branch: resolved.** The planner committed its four tests in `tests/test_check_names.py` and its six changes to older tests. They match the plan: only the criteria workflow is renamed Acceptance criteria, in `acceptance-criteria.yml`, no check changes its name, and done-when disappears everywhere else. Three of the four tests fail today for the right reason. The done-when scan passes only because the earlier worker's commit (`c610eb4`) is still on the branch and already removed the word. On `main` the scan fails.
- **B2, today's `main` breaks this plan: still open, and worse than last round.** The branch was built from `5261412`, so it doesn't have three later changes on `main`:
  - `tests/test_merge_queue.py` (#270) opens `done-whens.yml` by path and uses the old word on 22 lines.
  - `tests/test_plan_check_rerun.py` (#303, new since the last review) uses the old word on 4 lines and points its fake run at `done-whens.yml`.
  - `dokima/agent.py:1235` on `main` finds the plan check by the file name: `PLAN_CHECK = "done-whens.yml"`.

  When the worker merges `main`, renaming the file turns All tests red and the done-when scan fails. The worker can't change test files, and the planner can't change files that aren't on its branch.
- **Why it's an escalation.** This is round three. The planner agrees about the clash, but says code has to merge `main` into the branch first. I hold that the plan can't pass as it stands.
- **What unblocks it.** Merge `main` (`e1a21e7` or later) into `try/issue-291`, or have code do it before the planner runs. The planner then re-plans with changes to both test files. It should also add a test that the plan check re-run still finds the renamed workflow.

Two more things:
- **Moved scope has no home yet.** The AGENTS.md list of checks and the autopilot rule moved to #262, but no open story under #262 holds them. They need one, with a short note on each issue.
- **Proposed issue.** The planner always plans on an old copy of `main`, so it can never update tests that `main` added since. I proposed this as its own issue.

The review is in `/tmp/dokima-out/review.json` and passes both checks.

`14. Bash`
```
tail -40 /tmp/claude-1001/-home-runner-work-dokima-dokima/862b6f54-7c58-46cb-be31-d3596b1194df/tasks/brl5vfiyp.output | grep -E "passed|failed|FAILED" | head
```

> FAILED tests/test_check_names.py::test_the_card_and_the_board_update_when_the_acceptance_criteria_workflow_finishes - AssertionError: 291.1: the card no longer redraws when the all tests check finishes; card.yml waits on ['Acceptance criteria', 'All tests', 'worker']
> FAILED tests/test_check_names.py::test_no_check_changes_its_name_so_the_branch_rule_stays_as_it_is - AssertionError: 291.2: full-suite.yml is no longer the workflow full suite with the one check all tests: {'name': 'All tests', 'on': {'pull_request_target': '', 'push': {'branches': ['main']}}, 'permissions': {'contents': 'read'}, 'jobs': {'all-tests': {'name': 'All tests', 'runs-on': 'ubuntu-24.04', 'steps': [{'uses': 'actions/checkout@v5', 'with': {'ref': '${{ github.event.pull_request.head.sha || github.sha }}', 'persist-credentials': 'false'}}, {'uses': 'actions/setup-python@v6', 'with': {'python-version': '3.12'}}, {'run': 'pip install -q pytest'}, {'run': 'pytest -q -p no:cacheprovider tests'}]}}}
> 3 failed, 1 passed in 0.26s
> 26 failed, 667 passed in 283.10s (0:04:43)

**Agent:** The full test run I started in the background has finished, and it doesn't change the review. On `try/issue-291`, 26 of 693 tests fail. That's what I'd expect: the branch still has the earlier worker's commit, which renamed the checks to All tests. The new plan's tests now expect those names to stay as they are, and older tests on the branch were written for the old names too.

The three failing tests in `tests/test_check_names.py` are the same three I reported, and they fail for the right reason. The verdict stays an escalation: merge `main` into the branch, then let the planner re-plan. `/tmp/dokima-out/review.json` is unchanged.
