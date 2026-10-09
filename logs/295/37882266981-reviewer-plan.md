# reviewer (plan) for #295

Run: https://github.com/dokima-dev/dokima/actions/runs/37882266981

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (57.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/0875e1d4-f3d5-4dcb-a7ed-a9f10a99fbf3/tool-results/bbmba0hvg.txt
> 
> Preview (first 2KB):
> .:
> total 80
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:05 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:05 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:05 in
> -rw-r--r--  1 runner runner 58315 Oct  9 04:05 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 04:05 open_blockers.json
> -rw-r--r--  1 runner runner  3409 Oct  9 04:05 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:05 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:05 ..
> -rw-r--r-- 1 runner runner 3973 Oct  9 04:05 01-planner.json
> -rw-r--r-- 1 runner runner 3996 Oct  9 04:05 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3435 Oct  9 04:05 03-planner.json
> -rw-r--r-- 1 runner runner 3345 Oct  9 04:05 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1918 Oct  9 04:05 05-worker.json
> -rw-r--r-- 1 runner runner 2884 Oct  9 04:05 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4044 Oct  9 04:05 07-planner.json
> # Issue #295: The plan check re-runs when a plan is approved, so it never shows a stale failure
> 
> <!-- dokima-card -->
> An approved plan reruns the pull request's plan check on the same commit, so it never keeps a stale "No approved plan found".
> 
> **Review**
> 
> [issue #295](https://github.com/dokima-dev/dokima/issues/295) · [PR #303](https://github.com/dokima-dev/dokima/pull/303) · <img src="htt

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; for f in in/*; do echo "== $f"; cat $f; echo; done
```

> {
>  "kind": "user_story",
>  "summary": "An approved plan reruns the pull request's plan check on the same commit, so it never keeps a stale \"No approved plan found\".",
>  "user_story": "Once a plan is approved, the pull request's \"all done-whens passed\" check shows the verdict on that approved plan, without the owner re-running it by hand.",
>  "acceptance_criteria": [
>   {
>    "text": "When a plan is approved and its open pull request has no new commit, the plan check on that head reruns and passes. It reruns in full, only after the approval is posted, and leaves runs on older commits and other workflows alone.",
>    "source": "https://github.com/dokima-dev/dokima/issues/295"
>   },
>   {
>    "text": "Only an approval reruns the check. A plan review that blocks reruns nothing, and an approval with no open pull request reruns nothing and still posts its record.",
>    "source": "https://github.com/dokima-dev/dokima/issues/295"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "When the plan check cannot rerun, the pull request gets one comment from Dokima saying so, with the head's short id and why. That covers GitHub refusing and a check still running; the plan review's record is still posted.",
>    "why": "A stale red check with no explanation is exactly what stalled five pull requests.",
>    "principle": "Fail closed: a failure always says why."
>   },
>   {
>    "text": "The rerun uses Dokima's app key, minted after the agent finished. dokima/app.json and Dokima's manifest in code, dokima/manifest

`3. Bash`
```
cd /tmp/pack; grep -n "dokima-card\|^## \|^### \|^\*\*.*wrote\|RezaSoleymanifar" issue.md | head -80
```

> 3:<!-- dokima-card -->
> 48:<!-- /dokima-card -->
> 58:## Comments
> 60:### RezaSoleymanifar on issue #295 (2026-10-09T02:02:18Z)
> 64:### dokima-runtime on issue #295 (2026-10-09T02:02:41Z)
> 68:### dokima-runtime on issue #295 (2026-10-09T02:02:43Z)
> 73:### dokima-runtime on issue #295 (2026-10-09T02:02:54Z)
> 228:### dokima-runtime on issue #295 (2026-10-09T02:09:52Z)
> 347:**Next:** @RezaSoleymanifar The reviewer did not accept the plan's assumption for: "This needs a new step in .github/workflows/agent.yml after the record is posted (the river decides what follows before the approval is on GitHub, so a rerun from there would read the old records) and write access to Actions for Dokima's app, which you accept once on GitHub. AGENTS.md says workflows change only when an issue asks: may this one change agent.yml and dokima/app.json?" Answer with `/plan` and your words, or say `/work` to build it on its assumptions.
> 350:### RezaSoleymanifar on issue #295 (2026-10-09T03:44:35Z)
> 354:### dokima-runtime on issue #295 (2026-10-09T03:44:55Z)
> 410: "started_by": "RezaSoleymanifar",
> 500:### dokima-runtime on issue #295 (2026-10-09T03:46:53Z)
> 614:### dokima-runtime on issue #295 (2026-10-09T03:48:40Z)
> 619:### dokima-runtime on issue #295 (2026-10-09T03:48:42Z)
> 694:### dokima-runtime on PR #303 (2026-10-09T03:57:18Z)
> 785:### dokima-runtime on issue #295 (2026-10-09T04:03:41Z)
> 947:### dokima-runtime on issue #295 (2026-10-09T04:05:31Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 40,72p issue.md; sed -n 348,356p issue.md; sed -n 940,960p issue.md
```

> - Renaming the plan check or its workflow; that is #291.
> - Starting a plan check on a head that never had one: GitHub runs it on the next push and it reads the approval then.
> - Rerunning any other check, such as all tests.
> - Accepting the app's new Actions permission on GitHub; the owner does that once.
> 
> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37881680340/job/113662547280"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/running.svg" width="16" height="16" align="absmiddle" alt="running"></a> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The "all done-whens passed" check runs only when a pull request gets a new commit. When a plan is re-approved and the worker has nothing new to push, no commit lands, so the check keeps the failure it got before the approv

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff main --stat; grep -n '"actions"' dokima/manifest.py dokima/app.json; timeout 600 python3 -m pytest -q tests/test_plan_check_rerun.py tests/test_manifest.py 2>&1 | tail -20
```

> ea2c5b4 Merge branch 'main' into try/issue-295
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 85c0854 Merge branch 'main' into try/issue-295
>  .github/workflows/agent.yml    |   7 +
>  dokima/agent.py                |  49 +++++-
>  dokima/app.json                |   2 +-
>  tests/test_plan_check_rerun.py | 327 +++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 383 insertions(+), 2 deletions(-)
> dokima/app.json:15:    "actions": "write",
> dokima/manifest.py:62:    "actions": "read",
> dokima/manifest.py:82:    **{("run", s): ("actions", "read") for s in ("view", "list", "download", "watch")},
> dokima/manifest.py:83:    **{("run", s): ("actions", "write") for s in ("rerun", "cancel", "delete")},
> dokima/manifest.py:95:    (r"actions/", "actions"),
>   {'actions': 'read'} != {'actions': 'write'}
>   
>   Full diff:
>     {
>         'contents': 'write',
>         'pull_requests': 'write',
>         'issues': 'write',
>         'checks': 'read',
>   -     'actions': 'write',
>   ?                 - --
>   +     'actions': 'read',
>   ?                   ++
>         'statuses': 'read',
>         'metadata': 'read',
>         'workflows': 'write',
>   +     'organization_projects': 'write',
>         'administration': 'read',
>   -     'organization_projects': 'write',
>     }
> 2 failed, 63 passed in 18.45s

**Agent:** Still reviewing the plan: running its tests on the branch to see which fail and why.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_plan_check_rerun.py tests/test_manifest.py 2>&1 | grep -E "^(FAILED|E  .*295)" ; grep -n "manifest\|PERMISSIONS" tests/test_plan_check_rerun.py
```

> FAILED tests/test_manifest.py::test_the_guard_passes_settings_the_manifest_declares - AssertionError: 282.3: code or workflows in this repo rely on settings the manifest leaves out: ['dokima/agent.py: POST repos/{}/actions/runs/{}/rerun needs the app permission actions: write, and the manifest grants actions: read']
> FAILED tests/test_manifest.py::test_the_manifest_permissions_match_the_app_with_administration_read - AssertionError: 282.4: the manifest's permissions {'contents': 'write', 'pull_requests': 'write', 'issues': 'write', 'checks': 'read', 'actions': 'read', 'statuses': 'read', 'metadata': 'read', 'workflows': 'write', 'organization_projects': 'write', 'administration': 'read'} differ from dokima/app.json's {'contents': 'write', 'pull_requests': 'write', 'issues': 'write', 'checks': 'read', 'actions': 'write', 'statuses': 'read', 'metadata': 'read', 'workflows': 'write', 'administration': 'read', 'organization_projects': 'write'}
> 312:    Proves 295.4. The app's manifest must also ask GitHub for that right. Every re-run call must carry the app's key (the workflow's own token is read-only and GitHub refuses it) and come
> 313:    after the agent ran, so no agent holds a key that can run workflows. The app's manifest, dokima/app.json, must ask
> 324:    manifest = json.load(open(os.path.join(ROOT, "dokima", "app.json")))
> 325:    assert manifest["default_permissions"].get("actions") == "write", \
> 326:        f"295.4: dokima/app.json asks for actions: {manifest['default_permi

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -6 -- tests/test_plan_check_rerun.py; git log --oneline -8; sed -n 300,330p tests/test_plan_check_rerun.py; git log --all --oneline | head -5
```

> fd4037a planner for #295 (run 37872677209)
> ea2c5b4 Merge branch 'main' into try/issue-295
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 85c0854 Merge branch 'main' into try/issue-295
> 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
> 04630d5 worker for #295 (run 37880975938)
> 3961720 Merge remote-tracking branch 'origin/main' into try/issue-295
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
> fd4037a planner for #295 (run 37872677209)
>                                f"again, got {m.pr_comments()}{why(m)}"
>         assert m.try_sha[:7] in said[0] and reason in said[0], \
>             f"295.3 ({case}): the comment does not name the head {m.try_sha[:7]} and why ('{reason}'): {said[0]!r}"
>     ok = PlanReview(tmp_path / "ok", [lambda sha: plan_run(7001, sha)])
>     assert ok.runs()[7001]["conclusion"] == "success", f"295.3: the plan check did not run again when it could{why(ok)}"
>     assert not [c for c in ok.pr_comments() if "plan check" in c.lower()], \
>         f"295.3: a plan check that ran again still got a comment saying it could not: {ok.pr_comments()}"
> 
> 
> def test_the_plan_check_runs_again_only_with_the_apps_key_after_the_agent_finished(record_property, tmp_path):
>     """The plan check runs again only with Dokima's app key, after the agent finished.
> 
>     Proves 295.4. The app's manifest must also ask GitHub for that right. Every re-run call must carry the app's key (th

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git status --short; git diff HEAD --stat; git show fd4037a:tests/test_plan_check_rerun.py | grep -c "must also"; git branch -a | head; git log --all --oneline | grep -i "37882123559\|planner for #295"
```

> 1
>   main
> * try/issue-295
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
> 36b8ebc Conversation of run 37882123559
> fd4037a planner for #295 (run 37872677209)

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 origin/try/issue-295 2>&1; git show --stat 36b8ebc | head; git show 36b8ebc | grep -n -i "manifest" | head -30
```

> ea2c5b4 Merge branch 'main' into try/issue-295
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 85c0854 Merge branch 'main' into try/issue-295
> commit 36b8ebcd21bdfea62c8ec00c7668e4d37dbb8d82
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:05:22 2026 +0000
> 
>     Conversation of run 37882123559
> 
>  logs/295/37882123559-planner.md | 197 ++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 197 insertions(+)
> 65:+>   "problem": "295.4 asks dokima/app.json for write access to Actions. The manifest (dokima/manifest.py) must match app.json and must cover every GitHub call in code, so it needs actions: write too. The plan's scope leaves manifest.py out, so code dropped the worker's one-line change there, and two tests that pass on main now fail.",
> 66:+>   "evidence": "/tmp/pack/tests.txt: '2 failed, 684 passed'; FAILED tests/test_manifest.py::test_the_manifest_permissions_match_the_app_with_administration_read ({'actions': 'read'} != {'actions': 'write'}) and FAILED tests/test_manifest.py::test_the_guard_passes_settings_the_manifest_declares ('POST repos/{}/actions/runs/{}/rerun needs the app permission actions: write, and the manifest grants actions: read'). Both pass on main (pytest -q tests/test_manifest.py: 61 passed). The worker's record lists dropped_by_fence: ['dokima/manifest.py']; dokima/manifest.py:62 still says \"actions\": \"read\".",
> 67:+>   "fix": "Add dokima/manifest.py to the plan's scop

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_plan_check_rerun.py 2>&1 | tail -3; sed -n 150,175p <(git show 36b8ebc)
```

> ....                                                                     [100%]
> 4 passed in 13.25s
> +
> +**Agent:** Answering the reviewer's one blocker: I'm adding `dokima/manifest.py` to the scope and making the 295.4 test check it too.
> +
> +`6. Bash`
> +```
> +cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
> +p="tests/test_plan_check_rerun.py"
> +s=open(p).read()
> +old='''    for write access to Actions, which GitHub requires to run a workflow again; with read access it refuses."""'''
> +new='''    for write access to Actions, which GitHub requires to run a workflow again; with read access it refuses. Dokima's
> +    own manifest in code, dokima/manifest.py, must ask for the same, so the two never disagree."""'''
> +assert old in s; s=s.replace(old,new)
> +old2='''        "check again needs write"
> +'''
> +new2='''        "check again needs write"
> +    from dokima.manifest import PERMISSIONS
> +    assert PERMISSIONS.get("actions") == "write", \\
> +        f"295.4: dokima/manifest.py asks for actions: {PERMISSIONS.get('actions')!r}; it must match dokima/app.json, " \\
> +        "and running the plan check again needs write"
> +'''
> +assert s.count(old2)==1; s=s.replace(old2,new2)
> +open(p,"w").write(s)
> +EOF
> +python3 -m pytest -q tests/test_plan_check_rerun.py 2>&1 | tail -5
> +```
> +

`11. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt main && cp tests/test_plan_check_rerun.py /tmp/wt/tests/ && cd /tmp/wt && timeout 600 python3 -m pytest -q tests/test_plan_check_rerun.py 2>&1 | grep -E "^(FAILED|E +(Assertion|.*295))" | cut -c1-250; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt
```

> E       AssertionError: 295.1: the plan check on the head 7132f7d was not run again after the approval
> E       AssertionError: 295.2: an approval with the pull request open did not end with a passing plan check
> E           AssertionError: 295.3 (GitHub refused): expected one comment on PR #60 saying the plan check could not run again, got []
> E       AssertionError: 295.4: the plan check was not run again
> FAILED tests/test_plan_check_rerun.py::test_a_reapproved_plan_with_no_new_commit_ends_with_a_passing_plan_check - AssertionError: 295.1: the plan check on the head 7132f7d was not run again after the approval
> FAILED tests/test_plan_check_rerun.py::test_only_an_approval_with_an_open_pull_request_runs_the_plan_check_again - AssertionError: 295.2: an approval with the pull request open did not end with a passing plan check
> FAILED tests/test_plan_check_rerun.py::test_a_plan_check_that_cannot_run_again_says_why_on_the_pull_request - AssertionError: 295.3 (GitHub refused): expected one comment on PR #60 saying the plan check could not run again, got []
> FAILED tests/test_plan_check_rerun.py::test_the_plan_check_runs_again_only_with_the_apps_key_after_the_agent_finished - AssertionError: 295.4: the plan check was not run again

**Agent:** I've found one problem and am now writing the review file and checking it.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added dokima/manifest.py to the plan's scope and changed 295.4 to say both dokima/app.json and dokima/manifest.py ask GitHub for write access to Actions."],
  "decided": ["The 295.4 test is listed as also checking that dokima/manifest.py asks for write access to Actions."],
  "open": ["That test change is not on the branch: the 295.4 test still checks only dokima/app.json."]},
 "verdict": "block",
 "summary": "The plan now promises the manifest asks for write access to Actions, but the test change that would prove it never reached the branch, so the 295.4 test passes with the manifest still at read.",
 "blockers": [{"id": "B2", "criterion": "295.4",
   "test": "tests/test_plan_check_rerun.py::test_the_plan_check_runs_again_only_with_the_apps_key_after_the_agent_finished",
   "problem": "295.4 now promises dokima/manifest.py asks for write access to Actions, and the plan's test_changes and reply to B1 say this test checks dokima.manifest.PERMISSIONS and fails today with \"295.4: dokima/manifest.py asks for actions: 'read'\". The branch has no such check: the planner's edit was never committed, so the test proves only the app.json half and passes while the manifest still grants read.",
   "evidence": "On try/issue-295 (ea2c5b4), git log -- tests/test_plan_check_rerun.py shows only fd4037a (the first planner run); there is no commit from run 37882123559. grep -n 'PERMISSIONS\\|manifest.py' tests/test_plan_check_rerun.py finds nothing. pytest -q tests/test_plan_check_rerun.py: 4 passed, while dokima/manifest.py:62 still says \"actions\": \"read\".",
   "fix": "Commit the check the plan describes at the end of the 295.4 test (from dokima.manifest import PERMISSIONS; assert PERMISSIONS.get('actions') == 'write' with the 295.4 message), and confirm it fails on this branch before handing back.",
   "fixer": "planner"}],
 "notes": [{"text": "The three other tests still prove th
```

> summary holds 35 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";r=json.load(open(p))
r["summary"]="The 295.4 test never got its promised manifest check, so it passes while the manifest still grants read access to Actions."
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 295 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for #295 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json`, and it passes both hand-back checks.

**Why it's blocked (B2, criterion 295.4):** The planner tried to fix last round's blocker B1 in two parts, and only one reached the branch.
- **Landed:** `dokima/manifest.py` is now in the plan's scope, and 295.4 now says both `dokima/app.json` and `dokima/manifest.py` ask GitHub for write access to Actions.
- **Didn't land:** The plan says the 295.4 test now also checks the manifest and fails today because the manifest still says "read". That isn't true on `try/issue-295`:
  - The planner's log shows the edit, but that run never committed it. The test file's only commit is still from the first planner run (`fd4037a`).
  - The 295.4 test checks only `app.json`, and all 4 tests in `tests/test_plan_check_rerun.py` pass even though `dokima/manifest.py:62` still says `"actions": "read"`.

**Fix for the planner:** Commit the manifest check at the end of the 295.4 test, and confirm it fails on the branch before handing back.

**What still holds:**
- **Other tests:** I ran the branch's test file against main's code, and all four tests fail with their own criterion's message. So the other three criteria are still properly proven.
- **No wrong merge meanwhile:** `tests/test_manifest.py` already fails on this branch over the manifest mismatch (2 failures). The all-tests check would still stop a wrong merge, though the 295.4 test itself doesn't prove that part.
- **Your asks:** Each of your three asks has a criterion that covers it.

I also proposed one issue for you to consider filing: a planner's test edits can get lost even though its plan says they landed, and the plan still passes its check.
