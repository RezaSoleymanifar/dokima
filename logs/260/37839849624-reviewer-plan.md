# reviewer (plan) for #260

Run: https://github.com/dokima-dev/dokima/actions/runs/37839849624

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (33.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/582afa61-8090-4397-9c72-6619802629c7/tool-results/b4hzn32yo.txt
> 
> Preview (first 2KB):
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
> # Issue #260: The all tests check runs main's copy of its workflow, so a pull request can't rewrite its own judge
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> Dokima's app may now merge without my review once the required checks pass. "All done-whens passed" already runs main's copy of its workflow, but "all tests" runs the pull request's own copy, so a pull request that edits that workflow could make it pass no matter what.
> 
> What I want:
> - "All tests" runs main's copy of its workflow, the way "all done-whens passed" does, while still testing the pull

`2. Bash`
```
cd /tmp/pack; sed -n '/## Comments/,$p' issue.md | grep -v '^$' | cut -c1-400 | head -150
```

> ## Comments
> ### RezaSoleymanifar on issue #260 (2026-10-08T20:10:35Z)
> /autopilot start
> ### dokima-runtime on issue #260 (2026-10-08T20:10:58Z)
> Autopilot: switched on, starting plan
> ### dokima-runtime on issue #260 (2026-10-08T20:11:00Z)
> Autopilot is on for #260. Planning started for #260, which wait on nothing open.
> ### dokima-runtime on issue #260 (2026-10-08T20:11:14Z)
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> The planner planned this issue.
> **User story:** The all tests check judges every pull request by main's rules, the way all done-whens passed already does, so a pull request that edits the all tests workflow can't pass its own broken code, and its tests run with no key and no write access.
> **Acceptance criteria:**
> 1. On a pull request, GitHub runs main's copy of the all tests workflow (as it does for all done-whens passed), and that run still tests the pull request's code: a pull request whose code works passes, and one whose code is broken fails even when main's code works.
> 2. While the all tests check runs the pull request's code, that code can find no key and no GitHub token, in its environment or in any file of the checkout. The workflow names no secret and opens no keyed environment, and its token is limited to read access.
> 3. A pull request that edits the all tests workflow cannot change how its own tests are judged. If it replaces the t

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['in/02-reviewer-plan.json']:
  d=json.load(open(f)); print(json.dumps(d,indent=1)[:8000])
"
```

> [
>  {
>   "id": "B1",
>   "criterion": "260.1",
>   "test": "tests/test_all_tests_judge.py::test_all_tests_runs_mains_workflow_on_the_pull_requests_code",
>   "problem": "The owner asked that all tests run main's copy of its workflow, the way all done-whens passed does, and that one runs only main's copy. The tests only require that main's copy runs among others. A workflow that keeps the pull_request trigger and adds pull_request_target passes every test. GitHub would then still start the pull request's own copy as a second all tests check, which the pull request can rewrite to pass. That leaves a green all tests check beside main's red one, and the pull request's copy is the judge the owner wanted gone.",
>   "evidence": "I set full-suite.yml to listen on pull_request, pull_request_target and push to main, checking out github.event.pull_request.head.sha with persist-credentials: false. pytest -q tests/test_all_tests_judge.py tests/test_checks.py printed: 6 passed. tests/test_checks.py line 30 only requires 'pull_request_target:' and does not check that 'pull_request:' is gone.",
>   "fix": "In test 260.1, assert that on a pull request that leaves the workflow alone, every all tests run GitHub starts is main's copy (none is 'the pull request's copy'). The failure should name the extra run, for example '260.1: GitHub also runs the pull request's own copy of full-suite.yml'.",
>   "fixer": "planner"
>  }
> ]{
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37839417920",
>  "commit_before": "a74

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json
d=json.load(open('in/03-planner.json')); h=d['handback']; print(json.dumps({k:v for k,v in h.items()},indent=1)); print(d.get('check'))
"; diff <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json')),indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/in/03-planner.json'))['handback'],indent=1,sort_keys=True))") | head
```

> {
>  "kind": "user_story",
>  "summary": "The all tests check should run main's copy of its workflow, so a pull request that edits that workflow can't make its own tests pass.",
>  "user_story": "The all tests check judges every pull request by main's rules, the way all done-whens passed already does, so a pull request that edits the all tests workflow can't pass its own broken code, and its tests run with no key and no write access.",
>  "acceptance_criteria": [
>   {
>    "text": "On a pull request, GitHub runs only main's copy of the all tests workflow (as it does for all done-whens passed), never the pull request's own copy beside it, and that run still tests the pull request's code: a pull request whose code works passes, and one whose code is broken fails even when main's code works.",
>    "source": "https://github.com/dokima-dev/dokima/issues/260"
>   },
>   {
>    "text": "While the all tests check runs the pull request's code, that code can find no key and no GitHub token, in its environment or in any file of the checkout. The workflow names no secret and opens no keyed environment, and its token is limited to read access.",
>    "source": "https://github.com/dokima-dev/dokima/issues/260"
>   },
>   {
>    "text": "A pull request that edits the all tests workflow cannot change how its own tests are judged. If it replaces the test command with one that always passes (keeping the trigger, switching it to pull_request or to pull_request_target), or deletes the file, its broken code still gets a f

**Agent:** Now the tests.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff a746b8e HEAD --stat; git diff a746b8e HEAD; cat .github/workflows/full-suite.yml; wc -l tests/test_all_tests_judge.py
```

> tests/test_all_tests_judge.py | 8 ++++++--
>  1 file changed, 6 insertions(+), 2 deletions(-)
> diff --git a/tests/test_all_tests_judge.py b/tests/test_all_tests_judge.py
> index 6363ebc..cadb1fe 100644
> --- a/tests/test_all_tests_judge.py
> +++ b/tests/test_all_tests_judge.py
> @@ -241,12 +241,16 @@ def test_all_tests_runs_mains_workflow_on_the_pull_requests_code(record_property
>      """The all tests check runs main's copy of its workflow, and the code it tests is the pull request's.
>  
>      Plays out GitHub opening a pull request that leaves the workflow alone. Main's copy must be among the all tests
> -    runs GitHub starts. A pull request whose code is right passes; one whose code is broken fails, though main's code
> -    is right, so the check tests the pull request's code and not main's."""
> +    runs GitHub starts, and it must be the only one: GitHub may not also start the pull request's own copy, which the
> +    pull request could rewrite. A pull request whose code is right passes; one whose code is broken fails, though
> +    main's code is right, so the check tests the pull request's code and not main's."""
>      record_property("proves", "260.1")
>      runs, _ = pull_request(tmp_path / "good", APP_GOOD)
>      assert any(who.startswith("main's") for who, _, _ in runs), \
>          f"260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:\n{show(runs)}"
> +    theirs = [who for who, _, _ in runs if not who.startswith("main's")]
> +    assert not theirs, \
> + 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,240p tests/test_all_tests_judge.py
```

> """The all tests check is judged by main's copy of its workflow, so a pull request cannot rewrite its own judge (#260).
> 
> These tests play GitHub's part when a pull request is opened or updated. GitHub runs a workflow from the pull
> request's own branch when that copy listens on `pull_request`, and main's copy when main's copy listens on
> `pull_request_target`; both can run at once. Every workflow of this repo with a job named "all tests" is copied into a
> temp "main" tree, next to a tiny project (app.py and its test). The pull request's tree holds the same project, its
> code fixed or broken, and its own copy of those workflows, kept, edited or deleted. Each "all tests" job GitHub would
> start is then run step by step: `actions/checkout` copies the tree its `ref` names (main's by default on
> pull_request_target, the pull request's on pull_request) and, unless told `persist-credentials: false`, leaves the token
> in the checkout's .git/config the way the real action does; other `uses:` steps are skipped; every `run:` script runs
> with bash, its `${{ }}` filled in, with a `pip` that does nothing. The check counts as passed only when every
> "all tests" run on the pull request passed or was skipped, the same rule autopilot reads before it merges
> (dokima/agent.py, unproven()).
> """
> import json
> import os
> import re
> import shutil
> import subprocess
> 
> import test_start as ts
> 
> ROOT = ts.ROOT
> WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
> CHECK = "all tests"
> HEAD_SHA = "1111111111111111111111

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 240,339p tests/test_all_tests_judge.py; git diff 0a816b5 HEAD -- tests/test_checks.py
```

> def test_all_tests_runs_mains_workflow_on_the_pull_requests_code(record_property, tmp_path):
>     """The all tests check runs main's copy of its workflow, and the code it tests is the pull request's.
> 
>     Plays out GitHub opening a pull request that leaves the workflow alone. Main's copy must be among the all tests
>     runs GitHub starts, and it must be the only one: GitHub may not also start the pull request's own copy, which the
>     pull request could rewrite. A pull request whose code is right passes; one whose code is broken fails, though
>     main's code is right, so the check tests the pull request's code and not main's."""
>     record_property("proves", "260.1")
>     runs, _ = pull_request(tmp_path / "good", APP_GOOD)
>     assert any(who.startswith("main's") for who, _, _ in runs), \
>         f"260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:\n{show(runs)}"
>     theirs = [who for who, _, _ in runs if not who.startswith("main's")]
>     assert not theirs, \
>         f"260.1: GitHub also runs {', '.join(theirs)}, so the pull request's own copy still judges it:\n{show(runs)}"
>     assert green(runs), f"260.1: a pull request with working code did not pass all tests:\n{show(runs)}"
>     runs, _ = pull_request(tmp_path / "bad", APP_BAD)
>     assert any(who.startswith("main's") for who, _, _ in runs), \
>         f"260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:\n{show(runs)}"
>     assert not green(runs), \
> 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_all_tests_judge.py tests/test_checks.py 2>&1 | grep -E "260\.|29\.|passed|failed" | head -20
cp .github/workflows/full-suite.yml /tmp/orig.yml
mk(){ cat > .github/workflows/full-suite.yml; pytest -q tests/test_all_tests_judge.py tests/test_checks.py 2>&1 | grep -E "^E +AssertionError|passed|failed" | head -6; echo ---; }
echo "== correct"; mk <<'EOF'
name: full suite
on:
  pull_request_target:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  all-tests:
    name: all tests
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - run: pytest -q -p no:cacheprovider tests
EOF
echo "== both triggers"; mk <<'EOF'
name: full suite
on:
  pull_request:
  pull_request_target:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  all-tests:
    name: all tests
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - run: pytest -q -p no:cacheprovider tests
EOF
echo "== both triggers, if-skip on pull_request"; mk <<'EOF'
name: full suite
on:
  pull_request:
  pull_request_target:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  all-tests:
    name: all tests
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha || github.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          pyth
```

> record_property("proves", "260.1")
>             f"260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:\n{show(runs)}"
> E       AssertionError: 260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:
>         record_property("proves", "260.2")
> >       assert mains, f"260.2: GitHub would not run main's copy of the all tests workflow:\n{show(runs)}"
> E       AssertionError: 260.2: GitHub would not run main's copy of the all tests workflow:
>         record_property("proves", "260.3")
>                 f"260.3: a pull request that {how} kept main's all tests run from failing on its broken code:\n{show(runs)}"
> E           AssertionError: 260.3: a pull request that makes its copy always pass kept main's all tests run from failing on its broken code:
>         record_property("proves", "29.4")
> FAILED tests/test_all_tests_judge.py::test_all_tests_runs_mains_workflow_on_the_pull_requests_code - AssertionError: 260.1: GitHub would not run main's copy of the all tests workflow on a pull request, only:
> FAILED tests/test_all_tests_judge.py::test_all_tests_sees_no_secret_and_no_token - AssertionError: 260.2: GitHub would not run main's copy of the all tests workflow:
> FAILED tests/test_all_tests_judge.py::test_a_pull_request_cannot_rewrite_how_its_own_tests_are_judged - AssertionError: 260.3: a pull request that makes its copy always pass kept main's all tests run from failing on its broken code:
> 4 failed, 2 passed in 0.61s
> == c

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner changed criterion 260.1 so only main's copy of the all tests workflow may run on a pull request, never the pull request's own copy beside it.",
          "Test 260.1 now fails when GitHub would also start the pull request's own copy, naming that run."],
  "decided": ["The check keeps the name all tests, its workflow keeps the name full suite, and pushes to main keep running it.",
              "A pull request's own conftest.py and pytest settings stay outside this issue."],
  "open": ["The planner still raises the concern that a pull request can change how pytest judges its tests through conftest.py or pytest settings."]},
 "verdict": "approve",
 "summary": "The tests now fail if the pull request's own copy of the all tests workflow still runs beside main's, and a workflow that runs only main's copy on the pull request's code passes all of them.",
 "blockers": [],
 "notes": [
  {"text": "Plan grade item 6, still open from last round: nothing checks that pushes to main keep running all tests, which the plan promises as out of scope. The owner did not ask for it, so it is a note only.",
   "evidence": "A full-suite.yml listening only on pull_request_target would pass all six tests; the tests only simulate pull requests."},
  {"text": "I checked the tests against three versions of the workflow. Listening only on pull_request_target with the pull request's head checked out and no saved token: 6 passed. Listening on both pull_request and pull_request_target: 260.1 fails, naming the pull request's copy. Both triggers with the job skipped on pull_request: 260.1 also fails, which is right, since the pull request could remove that skip in its own copy.",
   "evidence": "pytest -q tests/test_all_tests_judge.py tests/test_checks.py against each version of .github/workflows/full-suite.yml. On today's workflow: 4 failed, 2 passed, with messages naming 260.1, 260.2, 260.
```

> rc=0

**Agent:** I approved the plan for #260. Blocker B1 from my last review is fixed, and `review.json` is in `/tmp/dokima-out`. Both checks on it pass.

**B1 (fixed):** I had blocked because the pull request's own copy of the "all tests" workflow could keep running next to main's copy and still go green. The planner now says in criterion 260.1 that only main's copy may run. Test 260.1 fails and names the extra run if GitHub would also start the pull request's copy.

**Test runs:** I ran `pytest -q tests/test_all_tests_judge.py tests/test_checks.py` against four versions of the "full suite" workflow:

| Workflow version | Result |
|---|---|
| Today's workflow | 4 failed, 2 passed; the failures name 260.1, 260.2, 260.3 and the older test 29.4, each for the right reason |
| Runs only main's copy, on the pull request's code, with no token left in the checkout | 6 passed |
| Runs on both the pull request's trigger and main's trigger | 260.1 fails and names the pull request's copy |
| Both triggers, with the job skipped for the pull request's copy | 260.1 still fails, which is right because the pull request could remove that skip from its own copy |

**Notes in the review:**
- Nothing checks that pushes to main still run "all tests". The plan says they will, but the owner didn't ask for it, so it's a note, not a blocker.
- The planner's concern is still open: a pull request can change how its tests are judged through its own `conftest.py` or pytest settings. The plan leaves this for a separate issue.

**Next:** #260 is on autopilot and the plan has no questions, so the worker should start without anyone typing `/work`.
