# reviewer (plan) for #191

Run: https://github.com/dokima-dev/dokima/actions/runs/37861532365

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (66.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a8fa23ee-5b4d-4e0b-ae01-2c4f080866e3/tool-results/b7sjrsa6z.txt
> 
> Preview (first 2KB):
> .:
> total 84
> drwxr-xr-x  3 runner runner  4096 Oct  8 23:49 .
> drwxrwxrwt 18 root   root    4096 Oct  8 23:49 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 23:49 in
> -rw-r--r--  1 runner runner 62774 Oct  8 23:49 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 23:49 open_blockers.json
> -rw-r--r--  1 runner runner  4035 Oct  8 23:49 plan.json
> 
> in:
> total 56
> drwxr-xr-x 2 runner runner 4096 Oct  8 23:49 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 23:49 ..
> -rw-r--r-- 1 runner runner 3078 Oct  8 23:49 01-planner.json
> -rw-r--r-- 1 runner runner 3621 Oct  8 23:49 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2107 Oct  8 23:49 03-worker.json
> -rw-r--r-- 1 runner runner 5091 Oct  8 23:49 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4766 Oct  8 23:49 05-planner.json
> -rw-r--r-- 1 runner runner 3832 Oct  8 23:49 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner  333 Oct  8 23:49 07-not-started.json
> -rw-r--r-- 1 runner runner  342 Oct  8 23:49 08-updater.json
> -rw-r--r-- 1 runner runner 4674 Oct  8 23:49 09-planner.json
> # Issue #191: Queued PRs are retested on the latest main before merging
> 
> <!-- dokima-card -->
> Make the required checks run in GitHub's merge queue, so a queued pull request is retested on the latest main before it merges.
> 
> **Work** · Needs you: Fix why nothing ran
> 
> [

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> <persisted-output>
> Output too large (31.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a8fa23ee-5b4d-4e0b-ae01-2c4f080866e3/tool-results/bx4bxdp8b.txt
> 
> Preview (first 2KB):
> {
>  "kind": "user_story",
>  "summary": "Make the required checks run in GitHub's merge queue, so a queued pull request is retested on the latest main before it merges.",
>  "user_story": "With GitHub's merge queue on, every pull request is retested against the latest main, with the all-tests check and every criterion's check, before it merges.",
>  "acceptance_criteria": [
>   {
>    "text": "The all-tests and done-whens checks also run in the merge queue, on the queued commit: the pull request on top of the latest main.",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   },
>   {
>    "text": "In the merge queue, the done-whens find the pull request's issue from the queue's branch and list the same checks as on the pull request.",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   },
>   {
>    "text": "A queued pull request with no linked issue fails 'all done-whens passed' as on a pull request: 'No approved plan found: no issue linked'.",
>    "source": "https://github.com/dokima-dev/dokima/issues/191"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Pull request checks behave exactly as before: same triggers, same check names, same check list, same commit tested; repos without a merge queue are unaffected.",
>    "why": "The merge queue is an optional extra

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/a8fa23ee-5b4d-4e0b-ae01-2c4f080866e3/tool-results/bx4bxdp8b.txt
```

> 1	{
> 2	 "kind": "user_story",
> 3	 "summary": "Make the required checks run in GitHub's merge queue, so a queued pull request is retested on the latest main before it merges.",
> 4	 "user_story": "With GitHub's merge queue on, every pull request is retested against the latest main, with the all-tests check and every criterion's check, before it merges.",
> 5	 "acceptance_criteria": [
> 6	  {
> 7	   "text": "The all-tests and done-whens checks also run in the merge queue, on the queued commit: the pull request on top of the latest main.",
> 8	   "source": "https://github.com/dokima-dev/dokima/issues/191"
> 9	  },
> 10	  {
> 11	   "text": "In the merge queue, the done-whens find the pull request's issue from the queue's branch and list the same checks as on the pull request.",
> 12	   "source": "https://github.com/dokima-dev/dokima/issues/191"
> 13	  },
> 14	  {
> 15	   "text": "A queued pull request with no linked issue fails 'all done-whens passed' as on a pull request: 'No approved plan found: no issue linked'.",
> 16	   "source": "https://github.com/dokima-dev/dokima/issues/191"
> 17	  }
> 18	 ],
> 19	 "non_functional": [
> 20	  {
> 21	   "text": "Pull request checks behave exactly as before: same triggers, same check names, same check list, same commit tested; repos without a merge queue are unaffected.",
> 22	   "why": "The merge queue is an optional extra and must not change how pull requests are judged.",
> 23	   "principle": "Small and lean: extras are optional and never required."
> 24	  }
> 25	 ],
> 26	 "scope": [
> 

`4. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^\*\*.*commented\|^---" issue.md | head -80; wc -l issue.md
```

> 47:### Plan: add `work` to start
> 74:## Comments
> 76:### dokima-runtime on issue #191 (2026-10-08T21:03:21Z)
> 80:### dokima-runtime on issue #191 (2026-10-08T21:03:38Z)
> 211:### dokima-runtime on issue #191 (2026-10-08T21:19:36Z)
> 337:### dokima-runtime on issue #191 (2026-10-08T21:21:08Z)
> 342:### dokima-runtime on issue #191 (2026-10-08T21:21:11Z)
> 404:### dokima-runtime on PR #270 (2026-10-08T21:27:36Z)
> 531:### dokima-runtime on issue #191 (2026-10-08T21:32:44Z)
> 691:### dokima-runtime on issue #191 (2026-10-08T21:34:29Z)
> 820:### dokima-runtime on issue #191 (2026-10-08T21:36:00Z)
> 825:### dokima-runtime on PR #270 (2026-10-08T21:36:03Z)
> 859:### dokima-runtime on PR #270 (2026-10-08T22:07:29Z)
> 863:### dokima-runtime on PR #270 (2026-10-08T22:13:25Z)
> 867:### dokima-runtime on PR #270 (2026-10-08T22:19:17Z)
> 871:### dokima-runtime on PR #270 (2026-10-08T22:52:25Z)
> 875:### dokima-runtime on PR #270 (2026-10-08T23:47:08Z)
> 879:### dokima-runtime on issue #191 (2026-10-08T23:47:10Z)
> 916:### dokima-runtime on issue #191 (2026-10-08T23:47:22Z)
> 1079:### dokima-runtime on issue #191 (2026-10-08T23:49:19Z)
> 1087 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 40,80p issue.md; sed -n 815,916p issue.md; sed -n 1075,1087p issue.md
```

> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37847723412/job/113552673597"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> All tests · <a href="https://github.com/dokima-dev/dokima/actions/runs/37846928015"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
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
> **Context:** The required checks come from full-suite.yml ('all tests') and done-whens.yml (one check per criterion plus 'all done-whens passed'). Neither runs on the merge_group event today, so a 

**Agent:** I'm checking the re-plan: the plan is unchanged apart from shorter wording. Next I'll run its tests against the current main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -1; git log --oneline -1 origin/main; git diff --stat origin/main...HEAD; git diff --stat HEAD origin/main -- .github dokima/checks.py tests/test_merge_queue.py; git show origin/main:.github/workflows/full-suite.yml | head -30
```

> 209ae2f A clash with main goes to the planner, on the record (#279)
>  .github/workflows/done-whens.yml |   6 +-
>  .github/workflows/full-suite.yml |   3 +-
>  dokima/checks.py                 |  17 +-
>  tests/test_merge_queue.py        | 366 +++++++++++++++++++++++++++++++++++++++
>  4 files changed, 387 insertions(+), 5 deletions(-)
>  .github/workflows/agent.yml      |  18 +-
>  .github/workflows/done-whens.yml |   6 +-
>  .github/workflows/full-suite.yml |  10 +-
>  .github/workflows/uptodate.yml   |  34 ++++
>  dokima/checks.py                 |  17 +-
>  tests/test_merge_queue.py        | 366 ---------------------------------------
>  6 files changed, 60 insertions(+), 391 deletions(-)
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

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff b642384 HEAD --stat; rm -rf /tmp/wt; git worktree add -q /tmp/wt origin/main 2>&1|tail -1; cp tests/test_merge_queue.py /tmp/wt/tests/; cd /tmp/wt && python -m pytest -q tests/test_merge_queue.py 2>&1 | grep -E "Error|passed|failed" | head -20
```

> tests/test_merge_queue.py | 24 +++++++++++++-----------
>  1 file changed, 13 insertions(+), 11 deletions(-)
> E           AssertionError: 191.1: full-suite.yml does not run on the merge queue's merge_group event; its `on:` is ['pull_request_target', 'push']
> tests/test_merge_queue.py:266: AssertionError
>         assert code == 0, f"191.2: on pull request #{pr}, `dokima.checks matrix` failed:\n{err}"
> >       assert code == 0, f"191.2: in the merge queue (pull request #{pr}), `dokima.checks matrix` failed:\n{err}"
> E       AssertionError: 191.2: in the merge queue (pull request #12), `dokima.checks matrix` failed:
> E         KeyError: 'pull_request'
> tests/test_merge_queue.py:295: AssertionError
>         assert code == 0, f"191.2: on pull request #{pr}, `dokima.checks matrix` failed:\n{err}"
> >       assert code == 0, f"191.2: in the merge queue (pull request #{pr}), `dokima.checks matrix` failed:\n{err}"
> E       AssertionError: 191.2: in the merge queue (pull request #34), `dokima.checks matrix` failed:
> E         KeyError: 'pull_request'
> tests/test_merge_queue.py:295: AssertionError
>         assert code == 0, f"191.2: on pull request #{pr}, `dokima.checks matrix` failed:\n{err}"
> >       assert code == 0, f"191.2: in the merge queue (pull request #{pr}), `dokima.checks matrix` failed:\n{err}"
> E       AssertionError: 191.2: in the merge queue (pull request #56), `dokima.checks matrix` failed:
> E         KeyError: 'pull_request'
> tests/test_merge_queue.py:295: AssertionError
> >       assert co

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git diff b642384 HEAD -- tests/test_merge_queue.py; cd /tmp/wt && python -m pytest -q tests/test_merge_queue.py 2>&1 | tail -9
```

> diff --git a/tests/test_merge_queue.py b/tests/test_merge_queue.py
> index 471fe4c..4ad6501 100644
> --- a/tests/test_merge_queue.py
> +++ b/tests/test_merge_queue.py
> @@ -215,7 +215,9 @@ def triggers(lines):
>  
>  
>  def evaluate(expr, event, sha):
> -    """Evaluate a `${{ a || b }}` commit expression for an event, the way GitHub would; None when not understood."""
> +    """Evaluate a `${{ a || b }}` commit expression the way GitHub would.
> +
> +    Returns None when the expression is not understood."""
>      m = re.fullmatch(r"\$\{\{\s*(.*?)\s*\}\}", expr.strip().strip("'\""))
>      if not m:
>          return None
> @@ -253,9 +255,9 @@ def suite_refs():
>  
>  
>  def test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit(record_property):
> -    """The all-tests and done-whens workflows run on the merge queue's event, testing the queued commit.
> +    """Both required workflows run in the merge queue, testing the queued commit.
>  
> -    Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
> +    Proves 191.1. Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
>      the done-whens check checks out and the commit its annotations link to for a merge_group event, and checks both are
>      the queue's commit (the pull request on top of the latest main), not empty and not main's; and does the same for
>      the commit the all tests check checks out."""
> @@ -280,9 +282,9 @@ def 

**Agent:** Only docstrings changed. Now the good case: main plus `merge_group` and the worker's two files.

`9. Bash`
```
cd /tmp/wt; sed -i 's/^  pull_request_target:$/  pull_request_target:\n  merge_group:/' .github/workflows/full-suite.yml; head -9 .github/workflows/full-suite.yml; cd /home/runner/work/dokima/dokima; git show HEAD:.github/workflows/done-whens.yml > /tmp/wt/.github/workflows/done-whens.yml; git show HEAD:dokima/checks.py > /tmp/wt/dokima/checks.py; cd /tmp/wt; python -m pytest -q tests/test_merge_queue.py tests/test_all_tests_judge.py $(ls tests/test_checks*.py 2>/dev/null) 2>&1 | tail -3; git checkout -q .github/workflows/full-suite.yml; python -m pytest -q tests/test_merge_queue.py 2>&1|tail -1
```

> name: full suite
> # Every test in the repo, on every pull request and on main.
> # Runs main's copy of this workflow, so a pull request can't rewrite its own judge; only the code it tests comes from
> # the pull request, checked out with no token left behind, and the run holds no secret and only read access.
> on:
>   pull_request_target:
>   merge_group:
>   push:
>     branches: [main]
> .............                                                            [100%]
> 13 passed in 3.14s
> 2 failed, 5 passed in 1.15s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Re-planned after #279 merged into main: the three criteria, the non-functional requirement, the scope and the tests are the same as the approved plan, with shorter wording and test descriptions.",
   "Checked that #279 did not touch the files this work changes; the clash with main is still the old one in the all tests workflow (#263)."
  ],
  "decided": [
   "The worker rebuilds on the current main: it keeps main's all tests workflow and only adds the merge queue to its triggers."
  ],
  "open": [
   "In the merge queue, a pull request that edits the check workflows or dokima/checks.py would be judged by its own copy; the planner leaves this to its own issue."
  ]
 },
 "verdict": "approve",
 "summary": "The plan is unchanged and still fits the current main: all 7 test runs fail on main because the merge queue isn't supported, and pass once main's all tests workflow gains the merge queue trigger with the worker's earlier done-whens and check list changes.",
 "blockers": [],
 "notes": [
  {
   "text": "191.1 still would not catch a job-level `if:` that skips a check on the merge queue's event. The triggers and the checked-out commits are proven; that the job actually runs there is not.",
   "evidence": "tests/test_merge_queue.py::test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit reads only `on:`, the checkout `ref:` lines and HEAD_SHA"
  },
  {
   "text": "The worker's branch still carries the old all tests workflow and must be rebuilt on main; the tests hold the worker to that. On main with `merge_group:` added to full-suite.yml and the branch's done-whens.yml and dokima/checks.py, everything passes. Leave that one line out and 191.1 and 191.4 fail.",
   "evidence": "Worktree at origin/main 209ae2f with tests/test_merge_queue.py: 7 failed (missing merge_group trigger; K
```

> rc=0

**Agent:** I approved the re-plan for #191. It's the same plan as the one I approved before main changed; only the wording of the criteria and the test descriptions got shorter.

- **Nothing new to act on:** there are no owner comments since the last review and no open blockers. All five of the owner's asks still map to a criterion (191.1 to 191.4), and the plan has no questions for the owner.
- **The tests fail today:** on current main (209ae2f, #279), all 7 test runs fail. The reasons are the expected ones: the all tests workflow doesn't run in the merge queue, and the check list breaks when there is no pull request in the event.
- **The tests pass with the right fix:** I added the merge queue trigger to main's all tests workflow and used the worker's earlier done-whens workflow and `dokima/checks.py`. The merge queue tests plus the all tests workflow's own tests then pass (13 passed). Without that one trigger line, 2 tests fail (191.1 and 191.4), so the tests force the worker to rebuild on the current main.

I left two notes, neither blocking:
- 191.1 still wouldn't catch a job-level `if:` that skips a check in the merge queue.
- The worker's branch still has the old all tests workflow and has to be rebuilt on main.

The worker's last attempt stopped before its agent started, and the issue is waiting on the owner to fix that cause. The plan doesn't change that. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.
