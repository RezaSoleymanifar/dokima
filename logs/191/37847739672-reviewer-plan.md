# reviewer (plan) for #191

Run: https://github.com/dokima-dev/dokima/actions/runs/37847739672

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (43.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f1d83620-c543-4dd0-9703-e06fd39ac490/tool-results/bu8b6mo58.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct  8 21:34 .
> drwxrwxrwt 18 root   root    4096 Oct  8 21:34 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 21:34 in
> -rw-r--r--  1 runner runner 43601 Oct  8 21:34 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 21:34 open_blockers.json
> -rw-r--r--  1 runner runner  4135 Oct  8 21:34 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  8 21:34 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 21:34 ..
> -rw-r--r-- 1 runner runner 3078 Oct  8 21:34 01-planner.json
> -rw-r--r-- 1 runner runner 3621 Oct  8 21:34 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2107 Oct  8 21:34 03-worker.json
> -rw-r--r-- 1 runner runner 5091 Oct  8 21:34 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4766 Oct  8 21:34 05-planner.json
> # Issue #191: Queued PRs are retested on the latest main before merging
> 
> <!-- dokima-card -->
> Make the required checks run in GitHub's merge queue, so a queued pull request is retested on the latest main before it merges.
> 
> **Review**
> 
> [PR #270](https://github.com/dokima-dev/dokima/pull/270) · [files changed](https://github.com/dokima-dev/dokima/pull/270/files)
> 
> **User story:** With GitHub's merge queue on, every pull request is retested against the latest main, with the all-tests check and every criterion's check, b

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> {
>  "kind": "user_story",
>  "summary": "Make the required checks run in GitHub's merge queue, so a queued pull request is retested on the latest main before it merges.",
>  "user_story": "With GitHub's merge queue on, every pull request is retested against the latest main, with the all-tests check and every criterion's check, before it merges.",
>  "acceptance_criteria": [
>   {
>    "text": "The all-tests check and the done-whens checks also run when a pull request enters the merge queue, and there they test the queued commit (the pull request on top of the latest main).",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   },
>   {
>    "text": "In the merge queue, the done-whens find the pull request's issue from the queue's branch and list the same one-check-per-criterion checks as on the pull request.",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   },
>   {
>    "text": "A queued pull request with no linked issue fails 'all done-whens passed' with the same reason it gives on a pull request: 'No approved plan found: no issue linked'.",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Pull request checks behave exactly as before: same triggers, same check names, same check list, same commit tested; repos without a merge queue are unaffected.",
>    "why": "The merge queue is an optional extra and must not change how pull requests are judged.",
>    "principle": "Small and lean: extras are optional and nev

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|dokima-ask\|^---" issue.md | head -50; grep -n "Original\|<details" issue.md | head
```

> 44:<!-- dokima-ask -->
> 48:### Plan: add `work` to start
> 77:## Comments
> 79:### dokima-runtime on issue #191 (2026-10-08T21:03:21Z)
> 83:### dokima-runtime on issue #191 (2026-10-08T21:03:38Z)
> 214:### dokima-runtime on issue #191 (2026-10-08T21:19:36Z)
> 340:### dokima-runtime on issue #191 (2026-10-08T21:21:08Z)
> 345:### dokima-runtime on issue #191 (2026-10-08T21:21:11Z)
> 407:### dokima-runtime on PR #270 (2026-10-08T21:27:36Z)
> 534:### dokima-runtime on issue #191 (2026-10-08T21:32:44Z)
> 694:### dokima-runtime on issue #191 (2026-10-08T21:34:29Z)
> 20:<details><summary><b>Non-functional requirements</b></summary>
> 45:<details><summary>Original issue</summary>
> 57:<details open><summary>From the approved plan of #57, story 3</summary>
> 96:<details><summary><b>Non-functional requirements</b></summary>
> 102:<details><summary><b>Scope</b></summary>
> 110:<details><summary><b>Out of scope</b></summary>
> 118:<details><summary><b>Tests</b></summary>
> 127:<details><summary>Full record</summary>
> 219:<details><summary><b>Details</b></summary>
> 225:<details><summary><b>Notes</b></summary>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 40,95p issue.md; sed -n 690,720p issue.md
```

> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37846904956/job/113549914214"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #57, story 3</summary>
> 
> **Part of:** #57 Keep PRs up to date with main automatically
> 
> **User story:** With GitHub's merge queue on, every PR is retested against the latest main, with every criterion's check, before it merges.
> 
> **Context:** The required checks come from full-suite.yml ('all tests') and done-whens.yml (one check per criterion plus 'all done-whens passed'). Neither runs on the merge_group event today, so a queue would wait for checks th

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -5 main; git diff --stat main...HEAD; git show b642384 --stat; cat tests/test_merge_queue.py
```

> 50765e4 The owner's ask reads open on the issue they wrote (#249)
> ab2dcaa The all tests check runs main's copy of its workflow, so a pull request can't rewrite its own judge (#263)
> 79e34d6 planner for #244 (run 37827165425) (#266)
> 772791d A finished worker always opens the pull request, even with nothing new to push (#259)
> 0a816b5 /autopilot start turns autopilot on but never starts the work (#247)
>  .github/workflows/done-whens.yml |   6 +-
>  .github/workflows/full-suite.yml |   3 +-
>  dokima/checks.py                 |  17 +-
>  tests/test_merge_queue.py        | 364 +++++++++++++++++++++++++++++++++++++++
>  4 files changed, 385 insertions(+), 5 deletions(-)
> commit b6423840ca1af32031a2cdc5351f5840c4edb5b2
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:34:18 2026 +0000
> 
>     planner for #191 (run 37847537372)
> 
>  tests/test_merge_queue.py | 34 ++++++++++++++++++++++++++--------
>  1 file changed, 26 insertions(+), 8 deletions(-)
> """Queued pull requests are retested on the latest main, with every criterion's check, before they merge.
> 
> GitHub's merge queue tests each pull request on top of the latest main in a temporary commit and sends the
> `merge_group` event, not `pull_request`. These tests prove the two required workflows (full-suite.yml and
> done-whens.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> queue's branch (refs/heads/gh-readonly-queue/<base>/pr-<N>-<sha>) and list

**Agent:** I'm checking the planner's revised tests: running them against main and against the branch.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt main 2>&1|tail -1; cp tests/test_merge_queue.py /tmp/wt/tests/; cd /tmp/wt; cat .github/workflows/full-suite.yml | head -40; python3 -m pytest -q tests/test_merge_queue.py 2>&1 | grep -E "AssertionError|passed|failed" | head -20
```

> name: full suite
> # Every test in the repo, on every pull request and on main.
> # Runs main's copy of this workflow, so a pull request can't rewrite its own judge; only the code it tests comes from
> # the pull request, checked out with no token left behind, and the run holds no secret and only read access.
> on:
>   pull_request_target:
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
>         with:
>           ref: ${{ github.event.pull_request.head.sha || github.sha }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - run: pytest -q -p no:cacheprovider tests
> E           AssertionError: 191.1: full-suite.yml does not run on the merge queue's merge_group event; its `on:` is ['pull_request_target', 'push']
> tests/test_merge_queue.py:264: AssertionError
>         assert code == 0, f"191.2: on pull request #{pr}, `dokima.checks matrix` failed:\n{err}"
> >       assert code == 0, f"191.2: in the merge queue (pull request #{pr}), `dokima.checks matrix` failed:\n{err}"
> E       AssertionError: 191.2: in the merge queue (pull request #12), `dokima.checks matrix` failed:
> tests/test_merge_queue.py:293: AssertionError
>         assert code == 0, f"191.2: on pull request #{pr}, `dokima.checks matrix` failed:\n{err}"
> >       assert code == 0, f"191.2: in the merge queue (pul

`7. Bash`
```
cd /tmp/wt; python3 -m pytest -q tests/test_merge_queue.py 2>&1 | tail -12; python3 -m pytest -q tests/test_merge_queue.py -k "queue_branch" 2>&1 | grep -A8 "failed:" | head -15
```

> assert {'pull_reques...rget', 'push'} == {'merge_group...rget', 'push'}
>   
>   Extra items in the right set:
>   'merge_group'
>   
>   Full diff:
>     {
>   -     'merge_group',
>         'pull_request_target',
>         'push',
>     }
> 7 failed in 0.67s
> >       assert code == 0, f"191.2: in the merge queue on release/2.0, `dokima.checks matrix` failed:\n{err}"
> E       AssertionError: 191.2: in the merge queue on release/2.0, `dokima.checks matrix` failed:
> E         Traceback (most recent call last):
> E           File "<frozen runpy>", line 198, in _run_module_as_main
> E           File "<frozen runpy>", line 88, in _run_code
> E           File "/tmp/wt/dokima/checks.py", line 95, in <module>
> E             main(sys.argv)
> E           File "/tmp/wt/dokima/checks.py", line 85, in main
> E             pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]
> E                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
> --
> FAILED tests/test_merge_queue.py::test_queue_branch_on_another_base_still_finds_the_pr - AssertionError: 191.2: in the merge queue on release/2.0, `dokima.checks matrix` failed:
>   Traceback (most recent call last):
>     File "<frozen runpy>", line 198, in _run_module_as_main
>     File "<frozen runpy>", line 88, in _run_code
> Shell cwd was reset to /home/runner/work/dokima/dokima

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 772791d main --stat -- .github dokima/checks.py; cd /tmp/wt; git checkout -q try/issue-191 -- .github/workflows/done-whens.yml dokima/checks.py 2>&1; python3 - <<'E'
p='.github/workflows/full-suite.yml';s=open(p).read();s=s.replace("    branches: [main]\n","    branches: [main]\n  merge_group:\n",1);open(p,'w').write(s)
E
git diff --stat; python3 -m pytest -q tests/test_merge_queue.py tests/test_all_tests_judge.py 2>&1 | tail -3
```

> .github/workflows/full-suite.yml | 7 ++++++-
>  1 file changed, 6 insertions(+), 1 deletion(-)
>  .github/workflows/full-suite.yml | 1 +
>  1 file changed, 1 insertion(+)
> ..........                                                               [100%]
> 10 passed in 2.68s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_merge_queue.py 2>&1 | tail -2; git worktree remove --force /tmp/wt
```

> }
> 1 failed, 6 passed in 1.07s

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{
 "previous_step": {
  "did": [
   "Rewrote the test for 191.4 against the current main: the all tests check runs on pull_request_target and pushes to main (#263) plus the merge queue, and still checks out the pull request's head on a pull request and main's commit on a push.",
   "Extended the test for 191.1 so it also checks the all tests check tests the queued commit in the merge queue."
  ],
  "decided": [
   "Kept the three criteria, the non-functional requirement and the scope unchanged."
  ],
  "open": [
   "In the merge queue, a pull request that edits the check workflows or dokima/checks.py would be judged by its own copy; the planner leaves this to its own issue."
  ]
 },
 "verdict": "approve",
 "summary": "The plan now matches the current main: all 7 new test runs fail on main because the queue isn't supported, and pass once main's all tests workflow gains the merge queue trigger with the worker's done-whens and check list changes.",
 "blockers": [],
 "notes": [
  {
   "text": "191.1 still would not catch a job-level `if:` that skips a check on the merge queue's event; the triggers and checked-out commits are proven, the job actually running there is not.",
   "evidence": "tests/test_merge_queue.py::test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit reads only `on:`, the checkout `ref:` lines and HEAD_SHA"
  },
  {
   "text": "The worker's branch must be rebuilt on the current main: as it stands, its full-suite.yml is the old pull_request version and 191.4 fails on it (1 failed, 6 passed), which is the plan working as intended.",
   "evidence": "On try/issue-191: `pytest -q tests/test_merge_queue.py` gives 1 failed, 6 passed. On main with `merge_group:` added to full-suite.yml and the branch's done-whens.yml and dokima/checks.py: `pytest -q tests/test_merge_queue.py tests/test_all_tests_judge.py` gives 10 passed. On main alone: 7 failed, each on a missing merge_group 
```

> rc=0

**Agent:** I approved the revised plan for #191. Both checks on my hand-back passed with nothing to fix.

**What the planner changed:** the earlier code review blocked because one test still expected the "all tests" workflow to start on plain pull requests. Since #263, main starts it a different way (`pull_request_target`). The planner rewrote that test to expect main's current triggers plus the merge queue. The test also still checks that the pull request's own commit is tested on a pull request, and main's commit on a push to main. The planner also extended the 191.1 test to check that "all tests" runs on the queued commit in the queue. The criteria and the files in scope are unchanged.

**What I ran:**

| Where | Result |
|---|---|
| Current main with the new tests | 7 failed, each for the right reason: no merge queue trigger, or the check list fails because it only knows how to read a pull request |
| Main plus the merge queue trigger, with the worker's done-whens and check list changes | 10 passed (this file and `tests/test_all_tests_judge.py`) |
| The worker's branch as it stands | 1 failed, 6 passed |

The one failure on the branch is expected. The branch still has the old version of the "all tests" workflow from before #263, so the worker has to rebuild on the current main.

**Notes (not blocking):**
- The 191.1 test still wouldn't catch a condition inside a workflow that skips a check in the queue. It proves the trigger and the commit tested, not that the job actually runs there.
- The planner raised a gap outside this issue: in the queue, a pull request that edits the check workflows or `dokima/checks.py` would be judged by its own edited copy. It's best filed as its own issue, and the earlier code review already proposed it, so I didn't propose it again.

The plan has no questions for you. The hand-back is in `/tmp/dokima-out/review.json`.
