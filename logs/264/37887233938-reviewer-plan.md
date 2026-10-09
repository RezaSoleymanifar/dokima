# reviewer (plan) for #264

Run: https://github.com/dokima-dev/dokima/actions/runs/37887233938

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (52.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/e4e024d6-e3b9-485e-8729-47b4c550892a/tool-results/b79cofjw2.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  9 05:09 .
> drwxrwxrwt 18 root   root    4096 Oct  9 05:10 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 05:09 in
> -rw-r--r--  1 runner runner 48277 Oct  9 05:09 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 05:09 open_blockers.json
> -rw-r--r--  1 runner runner  5034 Oct  9 05:09 plan.json
> 
> in:
> total 44
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:09 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:09 ..
> -rw-r--r-- 1 runner runner 4112 Oct  9 05:09 01-planner.json
> -rw-r--r-- 1 runner runner 4492 Oct  9 05:09 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1761 Oct  9 05:09 03-worker.json
> -rw-r--r-- 1 runner runner 4168 Oct  9 05:09 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5674 Oct  9 05:09 05-planner.json
> # Issue #264: A pull request can't change how its own tests are judged through test setup files
> 
> <!-- dokima-card -->
> A pull request can no longer make its failing tests pass by shipping its own conftest.py or pytest settings.
> 
> **Plan**
> 
> [issue #264](https://github.com/dokima-dev/dokima/issues/264)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #291
> 
> **User story:** The owner can trust a green All t

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; for f in in/*; do echo "== $f"; cat $f; echo; done
```

> {
>  "kind": "user_story",
>  "summary": "A pull request can no longer make its failing tests pass by shipping its own conftest.py or pytest settings.",
>  "user_story": "The owner can trust a green All tests or Acceptance criteria check, because the test setup and pytest settings that judge a pull request always come from main, never from the pull request.",
>  "acceptance_criteria": [
>   {
>    "text": "All tests and Acceptance criteria judge a pull request with main's conftest.py files and pytest settings, never the pull request's copies. This holds whether it ships them as files or as links to files of its own. Settings means pytest.toml, .pytest.toml, pytest.ini, .pytest.ini, pyproject.toml, setup.cfg and tox.ini. The pull request's code and tests still run, so working code passes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/264"
>   },
>   {
>    "text": "A pull request whose test fails still fails All tests when it adds or edits a conftest.py or pytest settings file to report success. This holds for files and for links to files of its own, at the root, in a folder under tests, and for main's own conftest.py.",
>    "source": "https://github.com/dokima-dev/dokima/issues/264"
>   },
>   {
>    "text": "A pull request that deletes main's pytest settings is still judged by them in All tests: code that main's settings fail still fails.",
>    "source": "https://github.com/dokima-dev/dokima/issues/264"
>   },
>   {
>    "text": "The Acceptance criteria check fails a criterion whose test fail

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|<!-- dokima-card -->\|Original\|marker" issue.md | head -50; wc -l issue.md
```

> 3:<!-- dokima-card -->
> 53:## Comments
> 55:### RezaSoleymanifar on issue #264 (2026-10-09T04:23:39Z)
> 59:### dokima-runtime on issue #264 (2026-10-09T04:24:15Z)
> 63:### dokima-runtime on issue #264 (2026-10-09T04:24:17Z)
> 68:### dokima-runtime on issue #264 (2026-10-09T04:24:28Z)
> 212:### dokima-runtime on issue #264 (2026-10-09T04:30:24Z)
> 345:### dokima-runtime on issue #264 (2026-10-09T04:39:19Z)
> 350:### dokima-runtime on issue #264 (2026-10-09T04:39:21Z)
> 414:### dokima-runtime on PR #314 (2026-10-09T04:47:07Z)
> 524:### dokima-runtime on issue #264 (2026-10-09T04:53:34Z)
> 680:### dokima-runtime on issue #264 (2026-10-09T05:09:35Z)
> 688 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 1,25p issue.md; sed -n 60,140p issue.md
```

> # Issue #264: A pull request can't change how its own tests are judged through test setup files
> 
> <!-- dokima-card -->
> A pull request can no longer make its failing tests pass by shipping its own conftest.py or pytest settings.
> 
> **Plan**
> 
> [issue #264](https://github.com/dokima-dev/dokima/issues/264)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #291
> 
> **User story:** The owner can trust a green All tests or Acceptance criteria check, because the test setup and pytest settings that judge a pull request always come from main, never from the pull request.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** All tests and Acceptance criteria judge a pull request with main's conftest.py files and pytest settings, never the pull request's copies. Settings means pytest.ini, .pytest.ini, pyproject.toml, setup.cfg and tox.ini. The pull request's code and tests still run, so working code passes.
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-264/tests/test_test_setup_judge.py#L173"><img src="https://raw.githubusercontent.com/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 25,60p issue.md; sed -n 680,688p issue.md
```

> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** The Acceptance criteria check fails a criterion whose test fails, whatever test setup or pytest settings files the pull request adds, edits or deletes.
>   - *<a href="https://github.com/dokima-dev/dokima/blob/try/issue-264/tests/test_test_setup_judge.py#L244"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: A failing criterion still fails its check, whatever setup files the pull request ships.*
>   - <a href="https://github.com/dokima-dev/dokima/issues/264">Source</a>
> 
> **Scope:**
> 
> - .github/workflows/full-suite.yml
> - .github/workflows/done-whens.yml
> 
> **Out of scope:**
> 
> - The merge queue run: there GitHub runs the queued commit's own copy of the workflows, as #263 left it, so its setup comes from the queued commit; the pull request has already passed with main's setup by then.
> - A pull request that changes test setup does not stop for the owner; the owner allowed either way, and main's copy is used instead, so such a change takes effect only once it merges.
> - Code under test that ends the test process itself (see the concern).
> - Test runners other than pytest.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -5 -- tests/test_test_setup_judge.py; git status --short; cat tests/test_test_setup_judge.py
```

> 402b276 planner for #264 (run 37883717477)
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
> The run is simulated the way tests/test_all_tests_judge.py does it: `actions/checkout` copies the tree its `ref` names
> (with `path:` honoured) and every `run:` script runs with bash; the checkouts hold no git history. Note that
> tests/test_merge_queue.py also requires every `ref:` in full-suite.yml to n

**Agent:** I'm checking whether the re-plan's updated tests are actually on this branch; the file here looks unchanged.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git log --all --oneline -10; grep -rn "pytest.toml\|symlinks=True" tests/test_test_setup_judge.py tests/test_all_tests_judge.py | head; grep -n "pytest.toml\|-type" .github/workflows/full-suite.yml .github/workflows/done-whens.yml
```

> d3a2b19 Conversation of run 37885989547
> 0c133d2 Merge branch 'main' into try/issue-236
> 96eb8ef Merge branch 'main' into try/issue-254
> 94e604d Conversation of run 37886228614
> 6e74b92 Merge branch 'main' into try/issue-264
> 747e1ec Merge branch 'main' into try/issue-308
> 208a31e worker for #285 (run 37886228614)
> 504aa2d Conversation of run 37886603651
> 4701372 worker for #308 (run 37886603651)
> 930523a The Blocker pill is computed from blocked-by links, not set by hand (#317)
> .github/workflows/full-suite.yml:36:          find . -path ./.git -prune -o -type f "${setup[@]}" -print0 | xargs -0 -r rm -f
> .github/workflows/full-suite.yml:37:          (cd .. && find . -path ./pr -prune -o -path ./.git -prune -o -type f "${setup[@]}" -print0 | xargs -0 -r cp --parents -t pr)
> .github/workflows/done-whens.yml:52:          find . -path ./.git -prune -o -type f "${setup[@]}" -print0 | xargs -0 -r rm -f
> .github/workflows/done-whens.yml:53:          (cd .. && find . -path ./pr -prune -o -path ./.git -prune -o -type f "${setup[@]}" -print0 | xargs -0 -r cp --parents -t pr)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git log --all --oneline -- tests/test_test_setup_judge.py; git branch -a | head -30; git show --stat d3a2b19 | head
```

> 402b276 planner for #264 (run 37883717477)
>   main
> * try/issue-264
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
>   remotes/origin/issue-116-board-sync
>   remotes/origin/issue-121-needs-you
>   remotes/origin/issue-126-keys-from-main
>   remotes/origin/issue-138-prompt
>   remotes/origin/issue-40-app
>   remotes/origin/issue-46-approve
>   remotes/origin/issue-54-plan
>   remotes/origin/issue-60-wrap
>   remotes/origin/issue-63-latest
>   remotes/origin/issue-67-label
>   remotes/origin/issue-74-layout
>   remotes/origin/issue-78-design
>   remotes/origin/issue-80-planner
>   remotes/origin/issue-81-build-on-main
>   remotes/origin/issue-89-planner-prompt
>   remotes/origin/issue-90-assign
>   remotes/origin/issue-93-terms
>   remotes/origin/logs
>   remotes/origin/main
>   remotes/origin/opus-everywhere
> commit d3a2b19c7cf8afef6cbcec19660c5a2f323e29ca
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:09:25 2026 +0000
> 
>     Conversation of run 37885989547
> 
>  logs/264/37885989547-planner.md | 448 ++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 448 insertions(+)

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git show d3a2b19:logs/264/37885989547-planner.md | grep -n -i "edit\|write\|commit\|symlinks\|pytest.toml" | head -40; git show d3a2b19:logs/264/37885989547-planner.md | tail -30
```

> 92:> - A test proves a pull request that edits those files cannot make a failing test pass.
> 134:> nothing to commit, working tree clean
> 143:> pull request's code is broken (its one test fails) and it adds, edits or deletes a setup file so that pytest would
> 144:> report success; the check must still fail. A pull request with working code whose setup edits change nothing must pass, without its copies being read, and
> 149:**Agent:** Answering the reviewer's two blockers (pytest.toml files and symlinked setup files): checking how the test harness simulates checkout.
> 221:> 2.38s call     tests/test_test_setup_judge.py::test_editing_setup_files_cannot_make_failing_tests_pass_all_tests
> 242:setup.cfg and tox.ini.""","""the files in the tree it runs in: every conftest.py, and pytest's settings in pytest.toml, .pytest.toml, pytest.ini,
> 276:>         tests/conftest.py edited to report every test as passed, and pytest.ini, .pytest.ini, pyproject.toml, setup.cfg,
> 278:> E           AssertionError: 264.2: a pull request with a failing test that adds a pytest.toml that runs no test passed all tests:
> 280:> E           AssertionError: 264.4: a pull request with a failing test that adds a pytest.toml that runs no test passed the acceptance criteria check (success):
> 281:> FAILED tests/test_test_setup_judge.py::test_editing_setup_files_cannot_make_failing_tests_pass_all_tests - AssertionError: 264.2: a pull request with a failing test that adds a pytest.toml that runs no test passed all tests:
> 282

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_test_setup_judge.py 2>&1 | tail -3; git rev-parse HEAD; git diff main --stat | tail -5
```

> ....                                                                     [100%]
> 4 passed in 7.14s
> 6e74b92cfa82928f073b4c8ead62070a096a5101
>  .github/workflows/done-whens.yml |   7 ++
>  .github/workflows/full-suite.yml |  13 ++
>  tests/test_test_setup_judge.py   | 259 +++++++++++++++++++++++++++++++++++++++
>  3 files changed, 279 insertions(+)

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": [
   "Added pytest.toml and .pytest.toml to the settings files main must supply, in criterion 264.1.",
   "Said in 264.1 and 264.2 that a setup file shipped as a link to a file of the pull request's own counts too.",
   "Answered the code review's two blockers as fixed, describing new attacks and a link-keeping checkout in tests/test_test_setup_judge.py."
  ],
  "decided": [
   "Extended the concern: a test module that loads its own hook with pytest_plugins can still turn a failing run green; left for a later issue."
  ],
  "open": [
   "The test changes the planner describes are not on the branch; the tests there are the first round's."
  ]},
 "verdict": "block",
 "summary": "The plan now promises that pytest.toml, .pytest.toml and linked setup files cannot rig the checks, but the tests on the branch were never updated, so all four still pass against the code the last review blocked.",
 "blockers": [
  {"id": "B3", "criterion": "264.1",
   "test": "tests/test_test_setup_judge.py::test_main_test_setup_judges_and_the_pull_requests_copies_are_not_read",
   "problem": "264.1 now names pytest.toml and .pytest.toml and says links count, but the test on the branch checks neither: it has no pytest.toml case and no linked conftest.py. The planner's reply says these were added, but its edit never reached the branch.",
   "evidence": "On try/issue-264 (HEAD 6e74b92) `git log --all -- tests/test_test_setup_judge.py` shows only 402b276, the first plan; `grep -n 'pytest.toml\\|symlinks=True' tests/test_test_setup_judge.py tests/test_all_tests_judge.py` finds nothing. `pytest -q tests/test_test_setup_judge.py` gives 4 passed, against workflows whose 'Use main's test setup' step still lists neither pytest.toml nor .pytest.toml and uses `find ... -type f` (full-suite.yml:36, done-whens.yml:52). The planner's own log (run 37885989547) ends with `M tests/test_test_setup_judge.py` uncommit
```

> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan promises pytest.toml and linked setup files cannot rig the checks, but its updated tests never reached the branch, so nothing proves it."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 264 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the re-plan for #264. The plan's new promises have no tests behind them. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner changed:** to answer the code review, it added `pytest.toml` and `.pytest.toml` to the settings files in criterion 264.1. It also wrote into 264.1 and 264.2 that a setup file shipped as a link to one of the pull request's own files counts too. Its replies say it added matching attacks to `tests/test_test_setup_judge.py` and made the fake checkout keep links.

**Why it's blocked:** those test changes are not on the branch.
- No commit after the first plan (402b276) touches `tests/test_test_setup_judge.py`, on this branch or any other.
- The planner's own run log (run 37885989547) ends with the file still modified and not committed.
- On the branch, `pytest -q tests/test_test_setup_judge.py` gives **4 passed**. That's against workflows whose cleanup step still skips `pytest.toml`, `.pytest.toml` and links (`.github/workflows/full-suite.yml:36`, `.github/workflows/done-whens.yml:52`). So both holes the code review found are still open, and nothing would catch them.

**Blockers, both for the planner:**
- **B3 (264.1):** put the `pytest.toml` and linked `conftest.py` cases on the branch, with the fake checkout keeping links, and show the test fails today.
- **B4 (264.2, which also covers 264.4):** put the new attacks on the branch (the `pytest.toml` and `.pytest.toml` files, and the linked setup files) and show both tests fail today.

**Asks:** both of your asks map to the plan: settings from main → 264.1, a test proving edits can't rig the result → 264.2. The plan has no questions for you, so there are no assumptions to judge.

**Proposed issue:** the planner's checks passed even though its test edits never got onto the branch, so a plan and its proof can disagree without any check noticing. I've proposed tracking that separately. I also noted that the planner's new concern is real but outside this issue: a test file can load its own pytest plugin and still turn a failing run green.
