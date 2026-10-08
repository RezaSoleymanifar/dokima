# reviewer (plan) for #155

Run: https://github.com/dokima-dev/dokima/actions/runs/37728974109

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; cat open_blockers.json; cat plan.json
```

> total 24
> drwxr-xr-x 2 runner runner 4096 Oct  8 04:45 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 04:45 ..
> -rw-r--r-- 1 runner runner 3961 Oct  8 04:45 01-planner.json
> -rw-r--r-- 1 runner runner 3864 Oct  8 04:45 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4682 Oct  8 04:45 03-planner.json
> # Issue #155: Plan checker: new tests are checked as new, renames as changes
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 2</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** Every new test in a plan has a one-sentence summary and fails today, and renaming an older test is treated as a change with a reason.
> 
> **Context:** dokima/planner.py test_changes sees a rename as one deleted plus one added test (the false rejection on #138). Nothing reads docstrings or runs the new tests today. A rename is decided by code, not guessed from labels: a test whose source is unchanged apart from its name is a rename. The planner only writes tests, so the working tree is today's code. Builds on story 1's handling of named tests. The owner confirmed (answer 2 on the issue) that a new test which fails because the code it needs does not exist yet counts as failing today. Changed and deleted older tests already need a reason (dokima/planner.py problems, the 'older' list); that check stays as it is.
> 
> **Acceptance criteria:**
> - A new test with no docstring, or whose docstring's first

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 53370c7 6094949 --stat; git diff 53370c7 6094949; cat tests/test_new_test_check.py
```

> tests/test_new_test_check.py | 58 +++++++++++++++++++++++++++++++-------------
>  1 file changed, 41 insertions(+), 17 deletions(-)
> diff --git a/tests/test_new_test_check.py b/tests/test_new_test_check.py
> index 16d1515..4d35ded 100644
> --- a/tests/test_new_test_check.py
> +++ b/tests/test_new_test_check.py
> @@ -56,6 +56,17 @@ def legacy(check, monkeypatch):
>      return check
>  
>  
> +CHANGED = "tests/test_legacy.py::test_legacy"
> +
> +
> +def change_legacy():
> +    """Change the body of the older test_legacy, keeping its name, no docstring, and a pass today: a changed test, not
> +    a new one, so neither new-test rule may reject it. Returns the plan with its reason under test_changes."""
> +    with open("tests/test_legacy.py", "w") as f:
> +        f.write(LEGACY.replace("assert True", "assert 1 == 1"))
> +    return dict(STORY, test_changes={CHANGED: "asserts a value instead of True"})
> +
> +
>  # 155.1: a new test needs a docstring whose first line is one plain sentence on one line
>  
>  @pytest.mark.parametrize("doc", [
> @@ -68,24 +79,29 @@ def legacy(check, monkeypatch):
>      '"""\n    \n    """',
>  ], ids=["no docstring", "empty", "no end mark", "two sentences", "two sentences ending in ?", "wrapped over two lines",
>          "blank"])
> -def test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it(record_property, check, doc):
> +def test_a_new_test_without_a_one_sentence_summary_is_rejected_naming_it(record_property, legacy, doc):
>      """A new test with no docstring, or whose first line is n

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def check" -A45 tests/test_plan_check.py | head -80; timeout 600 python -m pytest -q tests/test_new_test_check.py 2>&1 | tail -30
```

> 49:def check(tmp_path, monkeypatch):
> 50-    """A function that hands back the given files and runs the check on issue #9: returns (exit code, reason).
> 51-
> 52-    Each call empties the hand-back folder first, so one test can run the check on a good plan and then a broken one.
> 53-    """
> 54-    repo, out = tmp_path / "repo", tmp_path / "out"
> 55-    repo.mkdir()
> 56-    out.mkdir()
> 57-    git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True).stdout
> 58-    git("init", "-q")
> 59-    git("config", "user.name", "t")
> 60-    git("config", "user.email", "t@t")
> 61-    (repo / "tests").mkdir()
> 62-    (repo / "tests" / "test_old.py").write_text(OLD_TESTS)
> 63-    git("add", "-A")
> 64-    git("commit", "-qm", "base")
> 65-    # The planner's run starts at this commit too, so the check sees the new tests as its own (as a real run does).
> 66-    monkeypatch.setenv("PLANNER_BASE", git("rev-parse", "HEAD").strip())
> 67-    monkeypatch.setenv("PLANNER_RUN_BASE", git("rev-parse", "HEAD").strip())
> 68-    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
> 69-    (repo / "tests" / "test_jobs.py").write_text(NEW_TESTS)
> 70-    monkeypatch.chdir(repo)
> 71-
> 72-    def run(files, crit):
> 73-        for old in out.iterdir():
> 74-            old.unlink()
> 75-        for name, content in files.items():
> 76-            (out / name).write_text(content if isinstance(content, str) else json.dumps(content))
> 77-        try:
> 78-            rc = planner.main(["x", "check", "9", str(out)

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q 2>&1 | tail -5; git diff main --stat
```

> FAILED tests/test_new_test_check.py::test_a_new_test_file_that_cannot_be_parsed_is_rejected_naming_it[not utf-8] - Failed: 155.4: the check crashed with UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 55: invalid start byte, instead of rejecting with a reason
> FAILED tests/test_new_test_check.py::test_a_new_test_that_hangs_is_stopped_and_rejected_naming_it - AssertionError: 155.5: the check has no 60 s limit for one new test (planner.NEW_TEST_TIMEOUT)
> assert None == 60
>  +  where None = getattr(planner, 'NEW_TEST_TIMEOUT', None)
> 15 failed, 270 passed in 16.96s
>  tests/test_new_test_check.py | 240 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_check.py     |   5 +-
>  2 files changed, 243 insertions(+), 2 deletions(-)

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Changed the summary and must-fail tests so that, throughout, an older test is changed (same name, new body, no summary, passes today) with its reason, and the check must neither reject nor name it.",
          "Tightened the hang test: with a 2 s limit the check must stop within 15 s, and the reason must not name the test that failed at once."],
  "decided": ["A changed older test is held to neither new-test rule; criteria 155.1 and 155.2 now say so."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves a changed older test is left alone by the new-test rules, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [],
 "resolved": ["B1"],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 155 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #155 and wrote the review to `/tmp/dokima-out/review.json`. Both hand-back checks passed.

**The earlier blocker (B1) is fixed.** The tests for the summary rule (155.1) and the must-fail rule (155.2) now run against an older test that has been changed but kept its name. It has no summary, still passes today, and has its reason in `test_changes`. The good cases must pass with it present, and the bad cases must not name it. A check that also applied the new-test rules to changed older tests would now fail these tests.

**Both earlier notes were taken up too.** The hang test (155.5) sets a 2 s limit and requires the check to stop within 15 s, not 40 s. It also now requires that the reason leaves out the test that failed straight away.

**Test runs on `try/issue-155`:**
- `tests/test_new_test_check.py`: all 15 new tests fail, each because the feature isn't built yet. One of them (the not-valid-text file in 155.4) fails by crashing the check, which is the missing behaviour that test is meant to catch.
- Whole suite: 270 passed, and only those 15 new tests failed.

I found no other blockers and no notes, so the plan now waits for the owner's `/work`.
