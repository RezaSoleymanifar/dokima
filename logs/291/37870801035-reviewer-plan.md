# reviewer (plan) for #291

Run: https://github.com/dokima-dev/dokima/actions/runs/37870801035

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (36.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tool-results/bd9egy0b3.txt
> 
> Preview (first 2KB):
> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #291](https://github.com/dokima-dev/dokima/issues/291)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #262, story 1</summary>
> 
> **Part of:** #262 The 

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n '20,400p'
```

> <details open><summary>From the approved plan of #262, story 1</summary>
> 
> **Part of:** #262 The checks on a pull request read exactly like its Definition of Done
> 
> **User story:** The owner sees a pull request's checks named All tests and Acceptance criteria, the same words as its Definition of Done, finds no done-when anywhere they read, and is told plainly how to switch the branch rule when the rename merges.
> 
> **Context:** Today the PR shows two workflows. `.github/workflows/full-suite.yml` is named `full suite` and its job (the check) is `all tests`; `dokima/card.py` finds it by the exact name `ALL_TESTS = "all tests"` (card.py line 24, used in `checks_passed` and `render`). `.github/workflows/done-whens.yml` is named `done-whens`: a job `list done-whens`, one job per criterion named `N.k · <criterion>` (built by `dokima/checks.py` `check_name`, parsed back by card.py `checks_by_key`, so keep that shape), and a gate job `all done-whens passed`. Every place the old word survives today (grep -rni 'done.when'): done-whens.yml lines 1, 12, 45 (step `Run this done-when's tests`), 51 (`No test verifies this done-when yet.`), 61 and 71 (`No done-whens`, `Link an issue with done-whens`); `dokima/checks.py` line 69 (`annotations(..., done_when)`); `.github/workflows/card.yml` line 8 (`workflows: [done-whens, full suite, worker]`) and `.github/workflows/board.yml` line 16 (`workflows: [done-whens]`), which start the card and the board through `workflow_run` by workflow name, so renam

`3. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> 01-planner.json
> []{
>  "kind": "user_story",
>  "summary": "The pull request checks take the Definition of Done's names, All tests and Acceptance criteria, and the word done-when disappears.",
>  "user_story": "The owner sees a pull request's checks named All tests and Acceptance criteria, the same words as its Definition of Done, finds no done-when anywhere they read, and is told plainly how to switch the branch rule when the rename merges.",
>  "acceptance_criteria": [
>   {
>    "text": "The check that runs every test in the repo, and its workflow, are named All tests, in plain words with no number. The card still shows that check's verdict in its Definition of Done row and redraws when it finishes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/291"
>   },
>   {
>    "text": "The check that passes only when every criterion's tests passed, and its workflow, are named Acceptance criteria, with no number. Each criterion keeps its own check, named by its number and words. The card and the board still update when these checks finish.",
>    "source": "https://github.com/dokima-dev/dokima/issues/291"
>   },
>   {
>    "text": "No text a person reads says done-when or done-whens. That covers workflow file names, workflow, job and step names, error messages and test annotations. It also covers names, comments, docstrings and messages in Dokima's code and tests, AGENTS.md and the README. The only exceptions are the owner's older \"Done when:\" plan lines that Dokima still reads (dokima/plan.py

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_check_names.py
```

> commit 885417eaa325704290f64eea5a5629c816172513
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 01:38:51 2026 +0000
> 
>     planner for #291 (run 37870112685)
> 
>  tests/test_all_tests_judge.py |  12 +-
>  tests/test_automerge.py       |  11 +-
>  tests/test_autopilot_board.py |   2 +-
>  tests/test_card.py            |   2 +-
>  tests/test_card_bullets.py    |   2 +-
>  tests/test_card_records.py    |  16 +--
>  tests/test_card_status.py     |   6 +-
>  tests/test_check_names.py     | 325 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_checks.py          |   5 +-
>  tests/test_field_icons.py     |   2 +-
>  tests/test_merge_check.py     |  12 +-
>  11 files changed, 361 insertions(+), 34 deletions(-)
> """The pull request checks are named All tests and Acceptance criteria, with no done-whens (#291).
> 
> Story 1 of #262. The check that runs every test, and its workflow, are named All tests; the check that passes only when
> every criterion's check passed, and its workflow, are named Acceptance criteria; each criterion keeps its own check
> named "N.k · <words>". The card and the board start through `workflow_run` by workflow name, so the tests read those
> names out of card.yml and board.yml and match them against the workflows the repo really has. The card is drawn with
> the new and the old check names, and autopilot's merge is played through the fake GitHub of test_automerge.py with
> heads that lack either check. One test reads every file in the repo 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/ ':!tests/test_check_names.py'
```

> commit 885417eaa325704290f64eea5a5629c816172513
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 01:38:51 2026 +0000
> 
>     planner for #291 (run 37870112685)
> 
> diff --git a/tests/test_all_tests_judge.py b/tests/test_all_tests_judge.py
> index cadb1fe..3929973 100644
> --- a/tests/test_all_tests_judge.py
> +++ b/tests/test_all_tests_judge.py
> @@ -2,14 +2,14 @@
>  
>  These tests play GitHub's part when a pull request is opened or updated. GitHub runs a workflow from the pull
>  request's own branch when that copy listens on `pull_request`, and main's copy when main's copy listens on
> -`pull_request_target`; both can run at once. Every workflow of this repo with a job named "all tests" is copied into a
> +`pull_request_target`; both can run at once. Every workflow of this repo with a job named "All tests" is copied into a
>  temp "main" tree, next to a tiny project (app.py and its test). The pull request's tree holds the same project, its
> -code fixed or broken, and its own copy of those workflows, kept, edited or deleted. Each "all tests" job GitHub would
> +code fixed or broken, and its own copy of those workflows, kept, edited or deleted. Each "All tests" job GitHub would
>  start is then run step by step: `actions/checkout` copies the tree its `ref` names (main's by default on
>  pull_request_target, the pull request's on pull_request) and, unless told `persist-credentials: false`, leaves the token
>  in the checkout's .git/config the way the real a

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_check_names.py 2>&1 | grep -E "^(FAILED|ERROR|E  .*29[0-9]\.)|passed|failed" | head -40
```

> E       AssertionError: 291.1: expected one workflow named 'All tests', found []; the workflows are named ['agent', 'assign', 'autopilot', 'board', 'card', 'commands', 'done-whens', 'full suite', 'planner', 'uptodate', 'wiki', 'worker']
>         Proves 291.1. Draws the card with a check named All tests passed, then failed: the row's first circle says passed, then failed.
>         as passed."""
>         for conclusion, want in (("success", "passed"), ("failure", "failed")):
> E           AssertionError: 291.1: a check named All tests that ended success shows ['not started']
> E           assert ['not started'] == ['passed']
> E             At index 0 diff: 'not started' != 'passed'
> E             -     'passed',
> E       AssertionError: 291.1: the card does not redraw when All tests finishes; it waits on ['done-whens', 'full suite', 'worker']
> E       AssertionError: 291.2: expected one workflow named 'Acceptance criteria', found []; the workflows are named ['agent', 'assign', 'autopilot', 'board', 'card', 'commands', 'done-whens', 'full suite', 'planner', 'uptodate', 'wiki', 'worker']
> E           AssertionError: 291.2: card.yml does not start when Acceptance criteria finishes; it waits on ['done-whens', 'full suite', 'worker']
>         exactly one mention of the old check all done-whens passed. Each leftover is listed with its file and line. The
> E       AssertionError: 291.3: the old word done-when is still where a person reads it:
> E         .github/workflows/done-whens.yml line 61: name:

**Agent:** I've confirmed all 9 new tests fail today for the right reason (the rename is missing). Now checking the test helpers exist and running the full suite.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -nE "^(def|class) (Review|Command|pr_state|assert_waits|visible)|def (new_comments|merged|listen|agent_started|tail)" tests/test_automerge.py; grep -nE "^def (run|dod|draw|alts)|^RECS" tests/test_card_records.py; timeout 900 python3 -m pytest -q -x -p no:cacheprovider tests 2>&1 | tail -15
```

> 89:def pr_state(p):
> 344:def pr_state(issue, checks, files=None, refuse="", moves=False):
> 362:    def merged(self, pr=PR):
> 372:    def new_comments(self, kind, n):
> 382:class Review(Merges, ts.Machine):
> 427:class Command(Merges, tac.Repo):
> 445:    def listen(self, body, on_pr=None):
> 485:def visible(body):
> 512:def assert_waits(m, crit, case, reason, pr=PR, issue=N):
> 79:RECS = [PLANNED, PLAN_OK, BUILT, CODE_OK]
> 91:def run(name, status="completed", conclusion="success", n=7):
> 108:def draw(page="issue", **kw):
> 150:def alts(html):
> 165:def dod(text, k):
> 315:def run_ids(recs):
>         for name in sorted(os.listdir(WORKFLOWS)):
>             if name.endswith((".yml", ".yaml")):
>                 jobs = ts.load_yaml(open(os.path.join(WORKFLOWS, name)).read()).get("jobs") or {}
>                 if any(isinstance(j, dict) and j.get("name") == CHECK for j in jobs.values()):
>                     out.append(name)
> >       assert out, "the repo has no workflow with a job named 'All tests'"
> E       AssertionError: the repo has no workflow with a job named 'All tests'
> E       assert []
> 
> tests/test_all_tests_judge.py:71: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_all_tests_judge.py::test_all_tests_runs_mains_workflow_on_the_pull_requests_code - AssertionError: the repo has no workflow with a job named 'All tests'
> assert []
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 27 passed in 1.31s

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -p no:cacheprovider tests 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-200
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b6lk5h6mc). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python3 -m pytest -q -p no:cacheprovider "tests/test_check_names.py::test_no_text_a_person_reads_says_done_when" 2>&1 | grep -A40 "still where" | head -50
```

> >       assert not left, "291.3: the old word done-when is still where a person reads it:\n" + "\n".join(left)
> E       AssertionError: 291.3: the old word done-when is still where a person reads it:
> E         .github/workflows/board.yml line 16: workflows: [done-whens]
> E         .github/workflows/card.yml line 8: workflows: [done-whens, full suite, worker]
> E         .github/workflows/done-whens.yml: the file's name
> E         .github/workflows/done-whens.yml line 1: name: done-whens
> E         .github/workflows/done-whens.yml line 12: name: list done-whens
> E         .github/workflows/done-whens.yml line 45: - name: Run this done-when's tests
> E         .github/workflows/done-whens.yml line 51: if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi
> E         .github/workflows/done-whens.yml line 61: name: all done-whens passed
> E         .github/workflows/done-whens.yml line 71: echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
> E         .github/workflows/done-whens.yml line 71: echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
> E         dokima/checks.py line 69: def annotations(junit_xml, repo, sha, done_when):
> E         dokima/checks.py line 77: lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"
> E       assert not ['.github/workflows/board.yml line 16: workflows: [done-whens]', '.github/workflows/

`10. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output | cut -c1-200
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output cut -c1-200. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Meanwhile I'll draft the review.

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote nine new tests in tests/test_check_names.py, one or more for each of the four criteria and the non-functional requirement, and switched older tests' fake checks from all tests to All tests.",
          "The planner renamed one older test and cleaned the old word out of older tests' docstrings."],
  "decided": ["The criteria workflow file becomes acceptance-criteria.yml; full-suite.yml keeps its file name and only its workflow and check names change.",
              "Autopilot requires checks named All tests and Acceptance criteria on the head and stops for the owner, naming the missing one, when either is absent."],
  "open": ["The owner switches main's branch rule in GitHub's settings when the rename merges."]},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the story, and each of its nine new tests fails today because the rename is missing, while a good case beside each one keeps it honest.",
 "blockers": [],
 "notes": [
  {"text": "tests/test_card_bullets.py and tests/test_field_icons.py were changed (their fake all tests check now reads All tests) but have no line in test_changes, so the owner sees no reason for those two edits.",
   "evidence": "git show HEAD --stat lists both files; plan.json test_changes has no key in either file."},
  {"text": "Besides the rename, the 291.1 test also requires that the card no longer counts a check under the old name all tests; this follows the non-functional requirement's fail-closed rule rather than adding a new ask.",
   "evidence": "tests/test_check_names.py::test_the_card_shows_the_all_tests_verdict_in_its_definition_of_done_row, the old-name case at its end."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The check that runs every test in the repo, and its workflow, are named All tests, in plain words with no number. The card still shows that check's
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The plan keeps every ask of the story, and all nine new tests fail today only because the rename is missing."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 291 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output | cut -c1-200
```

> rc=0

**Agent:** The full test suite is still running, so I'll wait for it before finishing.

`13. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`14. Bash`
```
f=/tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output; until grep -qE "passed|failed" $f; do sleep 3; done; cut -c1-180 $f
```

> Command running in background with ID: b25d3ffgb. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b25d3ffgb.output. You will be notified when it completes. To check interim output, use Read on that file path.

**Agent:** Waiting for the full suite to finish.

`15. Bash`
```
cut -c1-200 /tmp/claude-1001/-home-runner-work-dokima-dokima/bcd2cc45-bebd-4ded-8797-dbe8ecdc18b2/tasks/b6lk5h6mc.output
```

> _____________ test_title_asks_for_approval_when_all_checks_passed ______________
>     def test_title_asks_for_approval_when_all_checks_passed(record_property):
>         """Approved work with every check passed says Ready for approval on its status line."""
> E       assert 'Ready for approval' in '**Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs y
> E        +  where '**Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See why not every
> E        +    where '<!-- dokima-card -->\n**Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" w...r-approval.svg" width="16" height="16" align="absmiddle" a
> E       assert 'Ready for approval' in '**Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs y
> E        +  where '**Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See why not every
>         Draws the card with the all tests check missing, queued, in progress, passed and failed, and checks the row's first
>                  (run("All tests", "in_progress", None, n=4), "running"), (run("All tests", n=4), "passed"),
>             

**Agent:** I approved the plan for issue #291 and wrote the review to `/tmp/dokima-out/review.json`. Both hand-back checks pass.

**The plan:** it covers what the story asks:
- The check that runs every test, and its workflow, are named All tests.
- The gate check and its workflow are named Acceptance criteria. The file becomes `acceptance-criteria.yml`, and each criterion keeps its own check named by its number and words.
- The words done-when and done-whens are gone everywhere a person reads. The only exceptions are the owner's older "Done when:" lines, copies of past records in `tests/samples`, and the one AGENTS.md sentence naming the old check.
- AGENTS.md lists the checks in Definition of Done order and says in one sentence how main's branch rule switches when the rename merges.
- Autopilot merges only when both All tests and Acceptance criteria passed on the pull request's head. If either is missing, it stops for the owner and says which one.

None of the owner's asks is missing from the plan.

**The tests:** all nine new tests in `tests/test_check_names.py` fail today, and each fails only because the rename hasn't been done yet. Each test that checks a bad case has a good case beside it: the word scan first tries lines it must flag and lines it must let through, and the autopilot test also checks that a head with both checks green does merge. I listed every leftover use of the old word. All of them are in files the worker is allowed to change, so the scan can pass.

**The full test suite:** 590 passed and 22 failed. The 22 are the 9 new tests and 13 older tests the planner edited to use the new names. Every one fails because the rename is missing, not because of a crash or a bad path.

**Notes in the review (not blockers):**
- `tests/test_card_bullets.py` and `tests/test_field_icons.py` were also switched from all tests to All tests, but neither has a line in the plan's test changes. The owner sees no reason for those two edits.
- One test for the All tests criterion also requires that the card stops counting a check still named all tests. I read this as part of the fail-closed requirement, not a new ask.
