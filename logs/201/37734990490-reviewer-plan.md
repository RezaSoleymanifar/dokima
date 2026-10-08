# reviewer (plan) for #201

Run: https://github.com/dokima-dev/dokima/actions/runs/37734990490

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
> # Issue #201: A re-plan after the worker built is rejected: new tests are judged against the branch, not main
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: a re-plan made after the worker built can still land, so a review block owned by the planner can always be fixed**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: on a re-plan, the plan checker judges "a new test must fail first" against main's code, not the branch that already holds the worker's code
> *Verified by: a test where a branch already has the worker's code that makes a new test pass, and the re-plan with that test is accepted because the test fails on main*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: a new test that already passes on main is still rejected, on a first plan and on a re-plan
> *Verified by: a test that a re-plan adding a test that passes on main is rejected with that test named*
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
> Found o

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_replan_check.py; grep -n "PLANNER_BASE\|def \|fail first\|passes today\|worktree\|stash" dokima/planner.py | head -80
```

> commit b93f64efc9c2e744c870f433465d9ec85870c2ee
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:53:49 2026 +0000
> 
>     planner for #201 (run 37734395961)
> 
>  tests/test_replan_check.py | 156 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 156 insertions(+)
> """The planner check on a re-plan (#201): a new test must fail on main's code, not on the branch's.
> 
> On a re-plan the issue's branch may already hold the worker's code, so a new test that proves that code passes on the
> branch even though the feature is missing on main. Every test here runs `python3 -m dokima.planner check 9 OUT`
> through planner.main, inside the temp git repo of the `check` fixture of tests/test_plan_check.py, set up like a real
> re-plan: main is the fixture's starting commit (PLANNER_BASE), the branch adds the planner's first-round test and then
> the worker's code (jobs.py, at PLANNER_RUN_BASE), and the re-plan writes its tests on top.
> """
> import os
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from tests.test_plan_check import STORY, check  # noqa: E402,F401
> 
> # The worker's code: on the branch only, never on main.
> WORKER_CODE = 'def make_job_id():\n    return "job-1"\n\n\ndef job_ids(n):\n    return ["job-%d" % i for i in range(n)]\n'
> 
> TEST_ID = ('import os\nimport sys\n\n\ndef test_id(record_property):\n    """A slow call returns a job id."""\n'
>            '    record_proper

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 300,460p dokima/planner.py; grep -n "def check\b\|def check(" -A40 tests/test_plan_check.py | head -70
```

> """True when the line is one sentence ending in '.', '?' or '!', with no other sentence end inside it."""
>     return bool(line) and line[-1] in ".?!" and not re.search(r"[.?!]\s", line)
> 
> 
> def unsummarized(added):
>     """The new tests (path::name) whose docstring's first line is not one sentence on one line."""
>     out = []
>     for path in sorted({t.partition("::")[0] for t in added}):
>         with open(path, encoding="utf-8") as f:
>             tree = ast.parse(f.read(), path)
>         for node in tree.body:
>             t = f"{path}::{getattr(node, 'name', '')}"
>             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and t in added:
>                 doc = ast.get_docstring(node, clean=False) or ""
>                 if not one_sentence(doc.split("\n")[0].strip()):
>                     out.append(f"{t} is a new test with no one-sentence summary: the first line of its docstring must "
>                                f"be one sentence on one line, ending in '.', '?' or '!'")
>     return out
> 
> 
> def passing_today(added):
>     """Run each new test (path::name) on today's code; the ones that pass or are skipped, or run past the limit."""
>     out = []
>     for t in sorted(added):
>         try:
>             r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", t],
>                                capture_output=True, text=True, timeout=NEW_TEST_TIMEOUT)
>         except subprocess.TimeoutExpired:
>             out.append(f"{t} is a new test still running aft

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_replan_check.py 2>&1 | tail -30; python -m pytest -q 2>&1 | tail -3
```

> E           assert (1 == 1 and 'test_unique' in "tests/test_jobs.py::test_id is a new test that passes today (or is skipped); every new test must fail on today's code...ts/test_jobs.py::test_unique is a new test that passes today (or is skipped); every new test must fail on today's code" and 'test_id' not in "tests/test_...today's code"
> E             
> E             'test_id' is contained here:
> E             ?                     ^^^^^^^^^^^^^^
> E               tests/test_jobs.py::test_id is a new test that passes today (or is skipped); every new test must fail on today's code; tests/test_jobs.py::test_unique is a new test that passes today (or is skipped); every new test must fail on today's code
> E             ?                     ^^^^^^^^^^^^^^^^^^^^^)
> 
> /home/runner/work/dokima/dokima/tests/test_replan_check.py:148: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> ::error title=Planner output rejected::tests/test_jobs.py::test_id is a new test that passes today (or is skipped); every new test must fail on today's code; tests/test_jobs.py::test_unique is a new test that passes today (or is skipped); every new test must fail on today's code
> =========================== short test summary info ============================
> FAILED tests/test_replan_check.py::test_a_replan_whose_new_tests_pass_only_thanks_to_the_workers_code_is_accepted - AssertionError: 201.1: a re-plan whose new tests fail on main (they pass only thanks to the worker

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "PLANNER_BASE\|PLANNER_RUN_BASE" .github/ dokima/ | grep -v "^dokima/planner.py"
```

> .github/workflows/planner.yml:59:          echo "PLANNER_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> .github/workflows/agent.yml:117:          echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
> .github/workflows/agent.yml:119:          echo "PLANNER_RUN_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"

**Agent:** I've read the plan and run its tests; the plan looks sound, so I'm writing the approval now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote three tests in tests/test_replan_check.py: a re-plan whose new tests pass only thanks to the worker's code is accepted (201.1), a new test that passes on main is rejected by name on a first plan and a re-plan (201.2), and the check leaves the branch and files as it found them (201.3)."],
  "decided": ["The check keeps using PLANNER_BASE, where the branch left main, as \"main\"; only dokima/planner.py changes.", "Refusing worker scope under tests/ goes to its own issue, as the owner accepted with /review."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers both asks of the issue, and every new test fails today for the right reason: the check still judges new tests against the branch.",
 "blockers": [],
 "notes": [
  {"text": "The reviewer's proposal to refuse worker scope under tests/ is left for its own issue; the owner accepted that assumption with /review, so it is worth filing.", "evidence": "issue #201 Context and the owner's /review comment of 2026-10-08T05:57:13Z"},
  {"text": "Today the first-plan half of 201.2 already passes; the test goes red only on its re-plan half, which is the new behavior, so it still guards against a fix that skips the check on re-plans.", "evidence": "pytest -q tests/test_replan_check.py: 4 failed, each with 'passes today' naming test_id, which passes only on the worker's branch"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [
  {"title": "Plan checker refuses a plan that puts files under tests/ in the worker's scope", "why": "The fence always drops worker changes under tests/, so such a plan can never be delivered and the issue gets stuck, as #158 did.", "evidence": "Issue #201 Context: code review blocked 158.4 because test samples sit under tests/, which only the planner may write."}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/
```

> rc=0

**Agent:** I approved the plan for #201. It covers what the issue asks for, and all its new tests fail today for the right reason. The hand-back is at `/tmp/dokima-out/review.json` and passed both hand-back checks.

**What the plan promises** (all in `tests/test_replan_check.py`, with only `dokima/planner.py` to change):
- **201.1:** When the planner re-plans after the worker has built, the plan checker runs each new test against main, not the branch. A re-plan whose new tests pass only because the worker's code is on the branch is accepted.
- **201.2:** A new test that already passes on main is still rejected by name, on a first plan and on a re-plan.
- **201.3:** Running the check leaves the branch, its latest commit, its worktrees and every file exactly as it found them, whether the re-plan is accepted or rejected.

**Test run:**
- All 4 new tests fail today because the checker still judges against the branch. On a re-plan, it reports `test_id` as "passes today" even though that test fails on main.
- The rest of the suite passes: 295 tests.
- The first-plan half of 201.2 already passes today, as it should. The test goes red on its re-plan half, so a fix that just skips the check on re-plans would still be caught.
- "Main" here means where the branch left main. `.github/workflows/agent.yml` already sets this with `git merge-base HEAD origin/main`.

The plan leaves one thing out. The other reviewer's proposal, to refuse a plan that puts files under `tests/` in the worker's scope, is left for a separate issue. You accepted that when you replied `/review`. I listed it in the review as a proposed issue so it can be filed.

**Next:** the plan is waiting for you to approve it with `/work`.
