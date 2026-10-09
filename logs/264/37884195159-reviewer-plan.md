# reviewer (plan) for #264

Run: https://github.com/dokima-dev/dokima/actions/runs/37884195159

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
> # Issue #264: A pull request can't change how its own tests are judged through test setup files
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
> Found by the code review of #263. Even with "all tests" running main's copy of its workflow, a pull request can still change how its tests run through files it ships, like conftest.py or pytest settings, and so rig its own judge.
> 
> What I want:
> - The test setup and settings that decide how tests are judged come from main, not from the pull request, or a change to them always waits for me.
> - A test proves a pull request that edits those files cannot make a failing test pass.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #264 (2026-10-09T04:23:39Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #264 (2026-10-09T04:24:15Z)
> 
> Autopilot: switched on, starting

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_test_setup_judge.py; ls; ls .github/workflows
```

> commit 402b276b44d9e19740215ac11dfeba2f878a7d38
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:30:13 2026 +0000
> 
>     planner for #264 (run 37883717477)
> 
>  tests/test_test_setup_judge.py | 259 +++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 259 insertions(+)
> """A pull request cannot change how its tests are judged through test setup files (#264).
> 
> Even with the all tests check running main's copy of its workflow (#263), pytest still reads setup and settings from
> the files in the tree it runs in: every conftest.py, and pytest's settings in pytest.ini, .pytest.ini, pyproject.toml,
> setup.cfg and tox.ini. A pull request that ships its own copy of one of them could make a failing test pass. These
> tests play GitHub's part the way tests/test_all_tests_judge.py does (same tiny project, same step-by-step run of the
> workflow): main's tree and the pull request's tree are written to temp folders, then every "all tests" job GitHub would
> start, and the acceptance criteria check's per-criterion job of done-whens.yml, are run on the pull request. The
> pull request's code is broken (its one test fails) and it adds, edits or deletes a setup file so that pytest would
> report success; the check must still fail. A pull request with working code whose setup edits change nothing must pass, without its copies being read, and
> main's own setup must still apply, so throwing every setup file away does not pass either.
> 
> The run is simulate

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_test_setup_judge.py 2>&1 | tail -80
```

> cases = [(how, j.APP_BAD, {}, files) for how, files in ATTACKS.items()]
>         cases.append(("deletes main's pytest.ini", APP_WARNS, STRICT, DELETES_STRICT))
>         for i, (how, app, main_files, pr_files) in enumerate(cases):
>             end, log = criterion_check(tmp_path / f"c{i}", app, main_files, pr_files, monkeypatch)
> >           assert end == "failure", \
>                 f"264.4: a pull request with a failing test that {how} passed the acceptance criteria check " \
>                 f"({end}):\n{log[-1500:]}"
> E           AssertionError: 264.4: a pull request with a failing test that adds a conftest.py at the root that turns the run's exit code to 0 passed the acceptance criteria check (success):
> E                     [100%]
> E             
> E             =================================== FAILURES ===================================
> E             __________________________________ test_value __________________________________
> E             
> E                 def test_value():
> E                     with open('/tmp/pytest-of-runner/pytest-0/test_setup_files_cannot_make_f0/c0/seen.jsonl', "a") as f:
> E                         f.write(json.dumps(seen()) + "\n")
> E             >       assert app.value() == 1
> E             E       assert 2 == 1
> E             E        +  where 2 = <function value at 0x7f9cad860720>()
> E             E        +    where <function value at 0x7f9cad860720> = app.value
> E             
> E             tests/test_app.py:26: AssertionError
> E             ====

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/full-suite.yml; sed -n 1,200p .github/workflows/done-whens.yml | grep -n "merge_group\|on:\|ref:\|pytest\|checkout" ; grep -n "ref" tests/test_merge_queue.py | head -30
```

> name: full suite
> # Every test in the repo, on every pull request, in the merge queue and on main.
> # Runs main's copy of this workflow, so a pull request can't rewrite its own judge; only the code it tests comes from
> # the pull request, checked out with no token left behind, and the run holds no secret and only read access.
> on:
>   pull_request_target:
>   push:
>     branches: [main]
>   merge_group:
> permissions:
>   contents: read
> jobs:
>   all-tests:
>     name: all tests
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.pull_request.head.sha || github.sha }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - run: pytest -q -p no:cacheprovider tests
> 5:on:
> 7:  merge_group:
> 15:    runs-on: ubuntu-24.04
> 19:      - uses: actions/checkout@v5
> 33:    runs-on: ubuntu-24.04
> 35:      - uses: actions/checkout@v5
> 38:      - uses: actions/checkout@v5
> 40:          ref: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
> 45:          python-version: "3.12"
> 46:      - run: pip install -q pytest
> 54:          pytest -rA -p no:cacheprovider -o junit_family=xunit1 --junitxml=r.xml $TESTS
> 59:          HEAD_SHA: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
> 66:    runs-on: ubuntu-24.04
> 6:queue's branch (refs/heads/gh-readonly-queue/<base>/pr-<N>-<sha>) and lists the same c

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 255,280p tests/test_merge_queue.py; sed -n 350,375p tests/test_merge_queue.py; find . -name conftest.py -not -path ./node_modules; ls -a | head; git log --oneline -3 -- tests/test_merge_queue.py
```

> def test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit(record_property):
>     """Both required workflows run in the merge queue, testing the queued commit.
> 
>     Proves 191.1. Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
>     the done-whens check checks out and the commit its annotations link to for a merge_group event, and checks both are
>     the queue's commit (the pull request on top of the latest main), not empty and not main's; and does the same for
>     the commit the all tests check checks out."""
>     record_property("proves", "191.1")
>     for name in ("full-suite.yml", "done-whens.yml"):
>         assert "merge_group" in triggers(workflow(name)), \
>             f"191.1: {name} does not run on the merge queue's merge_group event; its `on:` is {sorted(triggers(workflow(name)))}"
>     for expr in suite_refs():
>         got = evaluate(expr, queue_event(12), QUEUE_SHA)
>         assert got == QUEUE_SHA, \
>             f"191.1: in the merge queue the all tests checkout `{expr}` gives {got!r}, not the queued commit {QUEUE_SHA}"
>     refs, heads = commit_expressions()
>     assert refs and heads, "191.1: done-whens.yml has no `ref:` on the checkout with `path: pr` or no HEAD_SHA"
>     for what, exprs in (("checkout ref", refs), ("HEAD_SHA", heads)):
>         for expr in exprs:
>             got = evaluate(expr, queue_event(12), QUEUE_SHA)
>             assert got is not None, f"191.1: done-whens.yml {what} 

**Agent:** Still reviewing the plan: the four new tests fail today for the right reason. Now I'm checking that the fix can actually pass them without breaking the existing merge-queue tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def run_job" -A60 tests/test_all_tests_judge.py | head -90
```

> 125:def run_job(job, wf, event, base, head, ws, bin_dir):
> 126-    """Run one job the way GitHub would; returns 'success', 'failure' or 'skipped', and the log."""
> 127-    ctx = context(event)
> 128-    status = {"failed": False}
> 129-    cond = str(job.get("if") or "").replace("${{", "").replace("}}", "").strip()
> 130-    if not ts.evaluate(ts.condition(cond), ctx, status):
> 131-        return "skipped", ""
> 132-    assert "strategy" not in job, "the tests do not run matrix jobs"
> 133-    shutil.rmtree(ws, ignore_errors=True)
> 134-    os.makedirs(ws)
> 135-    env = {**(wf.get("env") or {}), **(job.get("env") or {})}
> 136-    workdir = ((job.get("defaults") or {}).get("run") or {}).get("working-directory") or \
> 137-        ((wf.get("defaults") or {}).get("run") or {}).get("working-directory") or "."
> 138-    log = []
> 139-    for step in job.get("steps") or []:
> 140-        scond = str(step.get("if") or "").replace("${{", "").replace("}}", "").strip()
> 141-        if not ts.evaluate(ts.condition(scond), ctx, status):
> 142-            continue
> 143-        uses = str(step.get("uses") or "")
> 144-        if uses.startswith("actions/checkout"):
> 145-            w = {k: ts.fill(v, ctx, status) for k, v in (step.get("with") or {}).items()}
> 146-            dest = os.path.join(ws, w.get("path") or ".")
> 147-            if os.path.abspath(dest) == os.path.abspath(ws):
> 148-                for n in os.listdir(ws):
> 149-                    p = os.path.join(ws, n)
> 150-                    shutil.rmtree(p) if o

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 25,70p .github/workflows/done-whens.yml; grep -n "def tree_for" -A12 tests/test_all_tests_judge.py
```

> check:
>     needs: list
>     if: needs.list.outputs.matrix != '[]'
>     name: ${{ matrix.name }}
>     strategy:
>       fail-fast: false
>       matrix:
>         include: ${{ fromJSON(needs.list.outputs.matrix) }}
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           persist-credentials: false
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
>           path: pr
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - name: Run this done-when's tests
>         working-directory: pr
>         env:
>           TESTS: ${{ matrix.tests }}
>           ID: ${{ matrix.id }}
>         run: |
>           if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi
>           pytest -rA -p no:cacheprovider -o junit_family=xunit1 --junitxml=r.xml $TESTS
>       - name: Annotate the tests that ran
>         if: always() && matrix.tests != ''
>         env:
>           ID: ${{ matrix.id }}
>           HEAD_SHA: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
>         run: python3 -m dokima.checks annotate pr/r.xml
> 
>   gate:
>     name: all done-whens passed
>     needs: [list, check]
>     if: always()
>     runs-on: ubuntu-24.04
>     steps:
>       - env:
>           MATRIX: ${{ needs.list.outputs.matrix }}
>           

**Agent:** Let me prototype a fix in a scratch copy to confirm the tests can pass.

`8. Bash`
```
rm -rf /tmp/proto && cp -r /home/runner/work/dokima/dokima /tmp/proto && cd /tmp/proto && python3 - <<'EOF'
swap = '''          rm -f pytest.ini .pytest.ini pyproject.toml setup.cfg tox.ini
          find . -name conftest.py -not -path './.git/*' -delete
          find . -path ./.git -prune -o \\( -name pytest.ini -o -name .pytest.ini -o -name tox.ini -o -name setup.cfg -o -name pyproject.toml \\) -print -delete
          (cd "$MAIN" && find . -path ./.git -prune -o \\( -name conftest.py -o -name pytest.ini -o -name .pytest.ini -o -name pyproject.toml -o -name setup.cfg -o -name tox.ini \\) -print) | while read f; do mkdir -p "$(dirname "$f")"; cp "$MAIN/$f" "$f"; done
'''
p='.github/workflows/full-suite.yml'; s=open(p).read()
s=s.replace('''      - uses: actions/setup-python@v6''','''      - uses: actions/checkout@v5
        with:
          path: .main
          persist-credentials: false
      - name: Use main's test setup
        env:
          MAIN: .main
        run: |
'''+swap+'''          rm -rf .main
      - uses: actions/setup-python@v6''')
open(p,'w').write(s)
p='.github/workflows/done-whens.yml'; s=open(p).read()
s=s.replace('''      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - name: Run this''','''      - name: Use main's test setup
        working-directory: pr
        env:
          MAIN: ..
        run: |
'''+swap.replace("find . -name conftest.py -not -path './.git/*' -delete","find . -name conftest.py -not -path './.git/*' -delete").replace("(cd \"$MAIN\" && find . -path ./.git -prune","(cd \"$MAIN\" && find . -path ./.git -prune -o -path ./pr -prune")+'''      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - name: Run this''')
open(p,'w').write(s)
EOF
git diff --stat; timeout 900 python -m pytest -q -x tests/test_test_setup_judge.py tests/test_merge_queue.py tests/test_all_tests_judge.py 2>&1 | tail -
```

> .github/workflows/done-whens.yml |  9 +++++++++
>  .github/workflows/full-suite.yml | 13 +++++++++++++
>  2 files changed, 22 insertions(+)
> =========================== short test summary info ============================
> FAILED tests/test_test_setup_judge.py::test_main_test_setup_judges_and_the_pull_requests_copies_are_not_read - AssertionError: 264.1: a pull request with working code that only edits test setup did not pass all tests:
>   - main's copy of full-suite.yml: failure
>   $ rm -f pytest.ini .pytest.ini pyproject.toml setup.cfg tox.ini
>   find . -name conftest.py -not -path './.git/*' -delete
>   find . -path ./.git -prune -o \( -name pytest.ini -o -name .pytest.ini -o -name tox.ini -o -name setup.cfg -o -name pyproject.toml \) -print -delete
>   (cd "$MAIN" && find . -path ./.git -prune -o \( -name conftest.py -o -name pytest.ini -o -name .pytest.ini -o -name pyproject.toml -o -name setup.cfg -o -name tox.ini \) -print) | while read f; do mkdir -p "$(dirname "$f")"; cp "$MAIN/$f" "$f"; done
>   rm -rf .main
>   find: The -delete action automatically turns on -depth, but -prune does nothing when -depth is in effect.  If you want to carry on anyway, just explicitly use the -depth option.
>   
> assert False
>  +  where False = <function green at 0x7f22c0f86660>([("main's copy of full-suite.yml", 'failure', "$ rm -f pytest.ini .pytest.ini pyproject.toml setup.cfg tox.ini\nfind ....une does nothing when -depth is in effect.  If you want to carry on anyway, just explicitly use the -depth opti

`9. Bash`
```
cd /tmp/proto && git checkout -q .github && python3 - <<'EOF'
py = '''          python3 - <<'PY'
          import os, shutil
          names = {"conftest.py", "pytest.ini", ".pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini"}
          main = os.environ["MAIN"]
          skip = {".git", os.path.basename(main.rstrip("/"))} if main != ".." else {".git"}
          for root, dirs, files in os.walk("."):
              dirs[:] = [d for d in dirs if d not in skip]
              for f in files:
                  if f in names:
                      os.remove(os.path.join(root, f))
          for root, dirs, files in os.walk(main):
              dirs[:] = [d for d in dirs if d not in (".git", "pr", ".main")]
              for f in files:
                  if f in names:
                      rel = os.path.relpath(os.path.join(root, f), main)
                      os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
                      shutil.copy(os.path.join(root, f), rel)
          PY
'''
p='.github/workflows/full-suite.yml'; s=open(p).read()
s=s.replace('''      - uses: actions/setup-python@v6''','''      - uses: actions/checkout@v5
        with:
          path: .main
          persist-credentials: false
      - name: Use main's test setup
        env:
          MAIN: .main
        run: |
'''+py+'''          rm -rf .main
      - uses: actions/setup-python@v6''')
open(p,'w').write(s)
p='.github/workflows/done-whens.yml'; s=open(p).read()
s=s.replace('''      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - name: Run this''','''      - name: Use main's test setup
        working-directory: pr
        env:
          MAIN: ..
        run: |
'''+py+'''      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -q pytest
      - name: Run this''')
open(p,'w').write(s)
EOF
timeout 900 python -m pytest -q tests/test_test_setup_judge.py tests/test_merg
```

> ..............                                                           [100%]
> 14 passed in 10.83s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /tmp/proto && timeout 900 python -m pytest -q -x -p no:cacheprovider tests 2>&1 | tail -5; cd /home/runner/work/dokima/dokima && cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(list(d.keys()))"
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bzbs09zkw). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/1f7bac0f-b6c2-445d-b2d7-fb8cf87972ee/tasks/bzbs09zkw.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`11. Bash`
```
sleep 100; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/1f7bac0f-b6c2-445d-b2d7-fb8cf87972ee/tasks/bzbs09zkw.output
```

> <tool_use_error>Blocked: sleep 100 followed by: tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/1f7bac0f-b6c2-445d-b2d7-fb8cf87972ee/tasks/bzbs09zkw.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** While the full suite runs on the prototype, I'll write the review.

`12. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Planned four criteria: both checks use main's conftest.py files and pytest settings, and a pull request that adds, edits or deletes them cannot turn a failing test green.",
   "Wrote four tests in tests/test_test_setup_judge.py that run the all tests and acceptance criteria jobs on a pull request that ships rigged setup files."
  ],
  "decided": [
   "Takes setup from main rather than stopping for the owner, so a change to test setup takes effect only once it merges.",
   "Leaves the merge queue run, other test runners and code that ends the test process itself out of scope."
  ],
  "open": [
   "Code that ends the test process with exit code 0 can still turn both checks green; raised as a concern for a later issue."
  ]
 },
 "verdict": "approve",
 "summary": "The plan covers both of the owner's asks, and each of its four tests fails today because the checks still read the pull request's own setup files; a trial fix passes them.",
 "blockers": [],
 "notes": [
  {
   "text": "Taking setup from main means a pull request can change conftest.py or pytest settings without stopping for the owner. Once merged, those files become main's and judge every later pull request. On autopilot that merge needs no owner. The owner allowed this route (\"come from main ... or a change to them always waits for me\"), but should know the trade-off.",
   "evidence": "plan.json out_of_scope[1]; AGENTS.md step 6 stops only for a workflow file change."
  },
  {
   "text": "No attack edits a pytest settings file that main already has; only main's tests/conftest.py is edited. Any fix that restores main's copies covers this, so it is a gap in coverage, not a hole in the proof.",
   "evidence": "tests/test_test_setup_judge.py ATTACKS: main has no settings file in those cases; STRICT appears only with deletion (264.3, 264.4)."
  },
  {
   "text": "The tests can be passed by a small change th
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> the ask "The test setup and settings that decide how tests are judged come from main, not from the pull request, or a change to them always waits for me." is matched to 1, which is not a criterion of the plan (264.1, 264.2, 264.3, 264.4)
> the ask "A test proves a pull request that edits those files cannot make a failing test pass." is matched to 2, which is not a criterion of the plan (264.1, 264.2, 264.3, 264.4)

`13. Bash`
```
cd /tmp/dokima-out && python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['summary']="The plan covers both asks; its four tests fail today because the checks still read the pull request's setup files, and a trial fix passes them."
d['asks'][0]['criterion']="264.1"; d['asks'][1]['criterion']="264.2"
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 264 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/1f7bac0f-b6c2-445d-b2d7-fb8cf87972ee/tasks/bzbs09zkw.output
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

**Agent:** I approved the plan for #264, and the review is saved at `/tmp/dokima-out/review.json`. Both of its checks pass.

**What I checked**
- **Your asks:** both are kept. Taking test setup from main is criterion 264.1. Proving a pull request can't make a failing test pass by editing setup files is criterion 264.2, backed up by 264.3 and 264.4.
- **The tests fail today for the right reason:** I ran all four. Each fails because the checks still read the pull request's own setup files, not because of a crash or a broken path. For example, a pull request with a failing test plus a rigged root `conftest.py` comes out green on main's copy of the "all tests" check.
- **The tests can be passed:** I wrote a trial fix in a scratch copy, touching only the two workflow files the plan names (check out main, remove the pull request's setup files, copy in main's). The new tests, the merge-queue tests and the existing all-tests tests then pass: 14 passed. A full test run on that copy was still going when I finished, so I haven't seen its result.
- **Shortcuts are caught:** a fix that skips every `conftest.py`, keeps setup files the pull request added, or drops main's settings would fail at least one test.

**Notes (not blockers)**
- The planner took your first option: setup comes from main, rather than stopping for you. The cost is that a pull request can change `conftest.py` or pytest settings without stopping for you. If its code works, it passes and can merge on autopilot, and from then on its files judge every later pull request.
- No test edits a pytest settings file that main already has; only main's `tests/conftest.py` gets edited. Any fix that restores main's copies covers this, so it's a gap in coverage, not a hole in the proof.

**Proposed new issues**
- **A pull request that changes `conftest.py` or pytest settings should stop for you,** for the reason in the first note.
- **The merge-queue retest from #270 still uses the queued pull request's own setup.** A pull request that breaks on the latest main could pass that retest by shipping a `conftest.py` that reports success. The plan leaves the merge queue out on purpose. The existing merge-queue test also requires every `ref:` in `full-suite.yml` to name the queued commit, so closing this needs that test changed.

`14. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/1f7bac0f-b6c2-445d-b2d7-fb8cf87972ee/tasks/bzbs09zkw.output | tail -8
```

> ........................................................................ [ 72%]
> ........................................................................ [ 82%]
> ........................................................................ [ 92%]
> ....................................................                     [100%]
> 700 passed in 365.28s (0:06:05)
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> 
> [exited with code 0]

`15. Bash`
```
cd /tmp/dokima-out && python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['notes'][2]['evidence']=d['notes'][2]['evidence'].replace("gives 14 passed;","gives 14 passed, and the whole suite gives 700 passed;")
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 264 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

**Agent:** The full test run on my scratch copy with the trial fix finished: all 700 tests pass. So the plan's fix can be made by changing only its two workflow files without breaking anything else.

I added that result to the review in `/tmp/dokima-out/review.json`, and the review still passes both of its checks. The verdict is still to approve the plan.
