# reviewer (plan) for #260

Run: https://github.com/dokima-dev/dokima/actions/runs/37839417920

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner  4096 Oct  8 20:26 .
> drwxrwxrwt 18 root   root    4096 Oct  8 20:26 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 20:26 in
> -rw-r--r--  1 runner runner 10399 Oct  8 20:26 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 20:26 open_blockers.json
> -rw-r--r--  1 runner runner  3651 Oct  8 20:26 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  8 20:26 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 20:26 ..
> -rw-r--r-- 1 runner runner 4258 Oct  8 20:26 01-planner.json
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
> Dokima's app may now merge without my review once the required checks pass. "All done-whens passed" already runs main's copy of its workflow, but "all tests" runs the pull request's own copy, so a pull request

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat .github/workflows/full-suite.yml; cat .github/workflows/done-whens.yml; cat tests/test_all_tests_judge.py; git show HEAD -- tests/test_checks.py
```

> commit a746b8e9993d54cc731f7bb0f45565da6303de79
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 20:25:55 2026 +0000
> 
>     planner for #260 (run 37837527348)
> 
>  tests/test_all_tests_judge.py | 335 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_checks.py          |   2 +-
>  2 files changed, 336 insertions(+), 1 deletion(-)
> name: full suite
> # Every test in the repo, on every pull request and on main.
> on:
>   pull_request:
>   push:
>     branches: [main]
> permissions:
>   contents: read
> jobs:
>   all-tests:
>     name: all tests
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - run: pytest -q -p no:cacheprovider tests
> name: done-whens
> # One GitHub check per criterion of the PR's approved plan, plus one gate check.
> # Runs main's copy of this workflow and of Dokima's code; only the tests, and the code they judge, come from the PR.
> on:
>   pull_request_target:
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
> jobs:
>   list:
>     name: list done-whens
>     runs-on: ubuntu-24.04
>     outputs:
>       matrix: ${{ steps.m.outputs.matrix }}
>     steps:
>       - uses: actions/checkout@v5
>       - id: m
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
> 
>   check:
>     needs: list
>     if: needs.list.outputs.matrix != '[]'
>     

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q -p no:cacheprovider tests/test_all_tests_judge.py tests/test_checks.py 2>&1 | tail -60
```

> the token behind). Also checks the all tests run actually happened, so a run that saw nothing cannot pass. Then
>         reads the workflow: it may name no key and open no keyed environment, and its token must be limited to read."""
>         record_property("proves", "260.2")
>         runs, dump = pull_request(tmp_path, APP_GOOD)
>         mains = [r for r in runs if r[0].startswith("main's")]
> >       assert mains, f"260.2: GitHub would not run main's copy of the all tests workflow:\n{show(runs)}"
> E       AssertionError: 260.2: GitHub would not run main's copy of the all tests workflow:
> E         - the pull request's copy of full-suite.yml: success
> E       assert []
> 
> tests/test_all_tests_judge.py:268: AssertionError
> _______ test_a_pull_request_cannot_rewrite_how_its_own_tests_are_judged ________
> 
> record_property = <function record_property.<locals>.append_property at 0x7f0388f2c400>
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-0/test_a_pull_request_cannot_rew0')
> 
>     def test_a_pull_request_cannot_rewrite_how_its_own_tests_are_judged(record_property, tmp_path):
>         """A pull request that edits the all tests workflow to pass no matter what still fails when its tests fail.
>     
>         The pull request breaks the code its tests check, then edits its copy of the workflow four ways: every pytest
>         command replaced by `true`, the same while listening on pull_request, the same on pull_request_target, and the file
>         deleted. Each time main's all tests run must still

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def unproven" -A40 dokima/agent.py; grep -rn "all tests" dokima/*.py | head -20
```

> 1136:def unproven(repo, sha):
> 1137-    """Why the commit is not proven by every check on it, check runs and commit statuses alike, or None when every
> 1138-    check on it has passed."""
> 1139-    runs = [r for p in pages(gh("api", f"repos/{repo}/commits/{sha}/check-runs?per_page=100", "--paginate"))
> 1140-            for r in p.get("check_runs", [])]
> 1141-    statuses = [s for p in pages(gh("api", f"repos/{repo}/commits/{sha}/status?per_page=100", "--paginate"))
> 1142-                for s in p.get("statuses") or []]
> 1143-    if not runs and not statuses:
> 1144-        return f"there are no checks on its head commit {sha[:7]}"
> 1145-    red = [f"{r['name']} ({r.get('conclusion')})" for r in runs if r.get("status") == "completed" and r.get("conclusion") not in PASSING]
> 1146-    red += [f"{s.get('context')} ({s.get('state')})" for s in statuses if s.get("state") not in ("success", "pending")]
> 1147-    running = [r["name"] for r in runs if r.get("status") != "completed"]
> 1148-    running += [s.get("context") for s in statuses if s.get("state") == "pending"]
> 1149-    if red:
> 1150-        return f"not every check passed on its head commit {sha[:7]}: {', '.join(red)}"
> 1151-    if running:
> 1152-        return f"a check is still running on its head commit {sha[:7]}: {', '.join(running)}"
> 1153-    return None
> 1154-
> 1155-
> 1156-def try_merge(repo, pr):
> 1157-    """Merge the pull request at the head whose checks were read, only when it changes no workflow file and every
> 1158-    check on that

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cp .github/workflows/full-suite.yml /tmp/orig.yml
try(){ cat > .github/workflows/full-suite.yml; echo "== $1"; python -m pytest -q -p no:cacheprovider tests/test_all_tests_judge.py tests/test_checks.py 2>&1 | grep -E "FAILED|passed|failed" | cut -c1-200; }
try correct <<'EOF'
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
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - run: pytest -q -p no:cacheprovider tests
EOF
try both <<'EOF'
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
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - run: pytest -q -p no:cacheprovider tests
EOF
try persist <<'EOF'
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
          ref: ${{ github.event.pull_request.head.sha }}
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - run: pytest -q -p no:cacheprovider tests
EOF
try mainref <<'EOF'
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
 
```

> == correct
> 6 passed in 1.82s
> == both
> 6 passed in 2.67s
> == persist
> FAILED tests/test_all_tests_judge.py::test_all_tests_sees_no_secret_and_no_token - AssertionError: 260.2: the pull request's tests can read the run's GitHub token in the file /tmp/pytest-of-runner/pyt
> 1 failed, 5 passed in 1.89s
> == mainref
>             f"260.1: a pull request with broken code passed all tests, so its own code was not tested:\n{show(runs)}"
> E       AssertionError: 260.1: a pull request with broken code passed all tests, so its own code was not tested:
> E        +  where True = green([("main's copy of full-suite.yml", 'success', '$ pip install -q pytest\n\n$ pytest -q -p no:cacheprovider tests\n.                                                       
> FAILED tests/test_all_tests_judge.py::test_all_tests_runs_mains_workflow_on_the_pull_requests_code - AssertionError: 260.1: a pull request with broken code passed all tests, so its own code was not te
>  +  where True = green([("main's copy of full-suite.yml", 'success', '$ pip install -q pytest\n\n$ pytest -q -p no:cacheprovider tests\n.                                                               
> FAILED tests/test_all_tests_judge.py::test_a_pull_request_cannot_rewrite_how_its_own_tests_are_judged - AssertionError: 260.3: a pull request that makes its copy always pass kept main's all tests run 
> 2 failed, 4 passed in 0.95s
> == envtoken
> FAILED tests/test_all_tests_judge.py::test_all_tests_sees_no_secret_and_no_token - AssertionError: 260.2: the pull requ

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner wrote three criteria and three tests. The tests open a pretend pull request and run every all tests job GitHub would start for it, step by step.",
          "The planner changed the old full suite test so it requires the pull_request_target trigger instead of pull_request."],
  "decided": ["The check keeps the name all tests, its workflow keeps the name full suite, and pushes to main keep running it.",
              "A pull request's own conftest.py and pytest settings stay outside this issue."],
  "open": ["The planner raised a concern: a pull request can still change how pytest judges its tests through conftest.py or pytest settings."]
 },
 "verdict": "block",
 "summary": "The tests catch a workflow that tests main's code, leaves the token in the checkout or hands the tests a key, but still pass if the pull request's own copy of the workflow keeps running next to main's.",
 "blockers": [
  {"id": "B1", "criterion": "260.1", "test": "tests/test_all_tests_judge.py::test_all_tests_runs_mains_workflow_on_the_pull_requests_code",
   "problem": "The owner asked that all tests run main's copy of its workflow, the way all done-whens passed does, and that one runs only main's copy. The tests only require that main's copy runs among others. A workflow that keeps the pull_request trigger and adds pull_request_target passes every test. GitHub would then still start the pull request's own copy as a second all tests check, which the pull request can rewrite to pass. That leaves a green all tests check beside main's red one, and the pull request's copy is the judge the owner wanted gone.",
   "evidence": "I set full-suite.yml to listen on pull_request, pull_request_target and push to main, checking out github.event.pull_request.head.sha with persist-credentials: false. pytest -q tests/test_all_tests_judge.py tests/test_checks.py printed: 6 passed. tests/test_checks.py
```

> rc=0

**Agent:** I blocked the plan for #260. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**The one blocker (B1, for the planner):** the owner asked that "all tests" run main's copy of its workflow, the way "all done-whens passed" does. That check runs only main's copy. The plan's tests only require main's copy to run alongside any others. I wrote a workflow that keeps the old `pull_request` trigger and adds `pull_request_target`, and all 6 tests passed. With that workflow, GitHub would still start the pull request's own copy as a second "all tests" check. The pull request could rewrite that copy to pass, leaving a green "all tests" next to main's red one.

The smallest fix: test 260.1 should require that, on a pull request that leaves the workflow alone, every "all tests" run is main's copy.

**What the tests do catch:**
- On today's code, the 3 new tests and the changed full suite test fail for the right reason: main's copy of the workflow isn't run.
- A correct workflow passes all 6.
- These wrong versions are each caught:
  - testing main's code instead of the pull request's;
  - leaving the token in the checkout;
  - handing the token to the test step;
  - having no read-only permissions setting.

**Notes (not blocking):** dropping the push-to-main trigger passes every test. The plan promises pushes keep running "all tests", but the owner didn't ask for that.

All three of the owner's asks map to criteria 1, 2 and 3. Nothing is missing, and the plan has no questions to judge. I put the workflow file back as it was, and the working tree is clean.
