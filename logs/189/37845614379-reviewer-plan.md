# reviewer (plan) for #189

Run: https://github.com/dokima-dev/dokima/actions/runs/37845614379

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #189: Open PRs are brought up to date after every merge to main
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
> <details open><summary>From the approved plan of #57, story 1</summary>
> 
> **Part of:** #57 Keep PRs up to date with main automatically
> 
> **User story:** After every merge to main, each open PR that fell behind is updated by GitHub's own Update branch, so the owner never taps it and the PR's timeline records it.
> 
> **Context:** Today nothing updates PRs: the owner taps Update branch by hand (issue #57). No workflow runs on push to main except full-suite.yml (tests only). The update must use the Dokima app's token (actions/create-github-app-token in the keys environment, as board.yml and agent.yml do): an update made with github.token starts no workflows, so the PR's checks would not rerun. GitHub's API: GET /repos/{repo}/pulls?state=open, GET /repos/{repo}/compare/{base}...{head} (behind_by), PUT /repos/{repo}/pulls/{n}/update-branch with expected_head_sha; a clash answers 422 'merge conflict'. The app can't push workflow files (AGENTS.md, Identity and safety), so GitHub may refuse an update that brings in a workflow change from main; that failure must say why on the PR. Put the decisions in a small Python modu

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_uptodate.py
```

> commit 7fe22d5dd5b0fa0c02ba93614317a78fd44f0474
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:16:20 2026 +0000
> 
>     planner for #189 (run 37844024824)
> 
>  tests/test_uptodate.py | 274 +++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 274 insertions(+)
> """Open PRs are brought up to date after every merge to main (#189).
> 
> After a merge to main, `.github/workflows/uptodate.yml` runs `python3 -m dokima.uptodate`, which calls GitHub's own
> Update branch for every open PR whose branch fell behind main. The rules live in `dokima.uptodate.run(repo, base, sha,
> rest=...)`, where `rest(method, path, **fields)` is one GitHub REST call shaped like `dokima.board.api`: it returns the
> parsed JSON and raises `subprocess.CalledProcessError` (GitHub's answer as JSON on `output`, gh's one-line message on
> `stderr`) when GitHub refuses. These tests fake GitHub through that seam, one test runs the real module from outside
> against a fake `gh` on PATH, and the workflow is read as text.
> 
> The fake GitHub answers:
>   - GET .../pulls (any query or fields; an empty page past the first): the open PRs, drafts included;
>   - GET .../compare/BASE...HEAD, where HEAD is a PR's head sha, its ref or its "owner:ref" label: behind_by, ahead_by;
>   - PUT .../pulls/N/update-branch (expected_head_sha): 202, or GitHub's refusal for that PR, 422 with its message;
>   - POST .../issues/N/comments (body): a comment on PR N.
> """
> import json
> import os
> impo

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_uptodate.py 2>&1 | grep -E "^(FAILED|E  .*189)|passed|failed" | head -30; grep -n -B1 -A3 "create-github-app-token\|environment\|branches" .github/workflows/board.yml .github/workflows/full-suite.yml | head -40
```

> E           Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> E       AssertionError: 189.1: .github/workflows/uptodate.yml is missing
> E       AssertionError: 189.1: dokima/uptodate.py is missing
> E           Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> E           Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> E           Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> E       AssertionError: 189.4: .github/workflows/uptodate.yml is missing
> E           Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> FAILED tests/test_uptodate.py::test_every_open_pr_behind_main_is_updated_drafts_included - Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> FAILED tests/test_uptodate.py::test_the_workflow_runs_the_update_on_every_push_to_main - AssertionError: 189.1: .github/workflows/uptodate.yml is missing
> FAILED tests/test_uptodate.py::test_the_real_module_updates_behind_prs_through_gh - AssertionError: 189.1: dokima/uptodate.py is missing
> FAILED tests/test_uptodate.py::test_prs_up_to_date_with_main_get_no_update_call - Failed: 189: dokima/uptodate.py is missing (cannot import name 'uptodate' from 'dokima' (unknown location))
> FAILED tests/

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three criteria and two requirements (app token, expected head) for updating open PRs that fell behind main, with eight tests in tests/test_uptodate.py."],
  "decided": ["The rules live in dokima/uptodate.py with GitHub's calls faked in tests; the workflow is .github/workflows/uptodate.yml, run on every push to main.",
              "PRs into branches other than main are left alone, and a successful update posts no comment.",
              "The hook for story 2 is an on_clash argument to run(), called with the clashing PR and the merge commit."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every criterion of this story, each with tests that fail today only because the module and workflow are missing.",
 "blockers": [],
 "notes": [
  {"text": "The story's context asks for one clear hook for story 2 (a function receiving the clashing PR and the merge commit); the plan names it (run(on_clash=...)) only in out of scope, and no test checks it is called on a clash.", "evidence": "plan.json out_of_scope[0]; tests/test_uptodate.py never passes on_clash"},
  {"text": "The plan says PRs into branches other than main are left alone, but every fake PR targets main, so a module updating PRs into other branches would still pass.", "evidence": "tests/test_uptodate.py pr() always sets base.ref to main"},
  {"text": "The workflow tests read fixed YAML shapes (branches: [main], `- id: NAME` above `uses: actions/create-github-app-token`), matching board.yml and full-suite.yml, so the worker must follow that style.", "evidence": "tests/test_uptodate.py::test_the_workflow_runs_the_update_on_every_push_to_main and ::test_the_workflow_updates_with_the_apps_token; .github/workflows/board.yml:36-40"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "When main changes, a workflow calls GitHub's Update branch (PUT /pulls/{
```

> (Bash completed with no output)

**Agent:** I approved the plan for #189 and wrote the review to `/tmp/dokima-out/review.json`. Both hand-back checks ran without errors.

- **Asks:** I counted five things the owner asked for in the issue: the three acceptance criteria and the two requirements (use the Dokima app's token, and pass the PR head it read). Each one maps to a criterion, 189.1 to 189.5, and none is missing.
- **Tests:** All 8 tests in `tests/test_uptodate.py` fail today, and only because `dokima/uptodate.py` and `.github/workflows/uptodate.yml` don't exist yet.
- **Proof:** The tests run the update against a fake GitHub and check each outcome the plan promises:
  - drafts are updated;
  - PRs already up to date get no call;
  - each refused PR gets one comment with GitHub's reason, and the other PRs still update;
  - every update carries the PR head it read;
  - the workflow runs on a push to main and uses the app's token, never github.token.

  One test also runs the real module from outside against a fake `gh`.

The plan asks the owner no questions and there were no earlier blockers. I added three notes, none of them blocking:
1. **Hook for story 2 is untested.** The issue asks this story to leave one hook for story 2, which receives the clashing PR and the merge commit. The plan names it (`run(on_clash=...)`), but only under "out of scope", and no test checks that it is called on a clash.
2. **The "main only" rule is untested.** The plan says PRs into branches other than main are left alone, but every fake PR targets main, so code that also updated those PRs would still pass.
3. **The workflow tests expect one exact layout.** They look for `branches: [main]`, and for `- id: NAME` on the line above the step that creates the app token. That matches the style of `board.yml` and `full-suite.yml`, so the worker has to write it the same way.
