# reviewer (plan) for #291

Run: https://github.com/dokima-dev/dokima/actions/runs/38076451926

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (136.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2c2e7341-e7ef-422f-a750-ab7c7d0ec5dd/tool-results/b8ve132ok.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> 06-updater.json
> 07-reviewer-plan.json
> 08-planner.json
> 09-updater.json
> 10-updater.json
> 11-reviewer-plan.json
> 12-updater.json
> 13-updater.json
> 14-updater.json
> 15-updater.json
> 16-updater.json
> 17-updater.json
> 18-updater.json
> 19-updater.json
> 20-updater.json
> 21-updater.json
> 22-updater.json
> 23-updater.json
> 24-updater.json
> 25-updater.json
> 26-updater.json
> 27-updater.json
> 28-updater.json
> 29-updater.json
> 30-updater.json
> 31-updater.json
> 32-updater.json
> 33-planner.json
> 34-planner.json
> 35-planner.json
> 36-planner.json
> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 264, 282, 295, 305, 308, 358, 388 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [292, 416], "loop": []} -->
> The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See the newest record below
> 
> https://github.

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json parent.json; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1)[:30000])"
```

> 130979 issue.md
>   8038 plan.json
>    498 open_blockers.json
>     15 parent.json
> 139530 total
> [
>  {
>   "kind": "issue",
>   "label": "Branch pushed back",
>   "text": "A planner run that is still going pushes try/issue-N when it ends, even if the owner deleted the branch while it ran. The owner's cleanup is silently undone, and the next /plan starts from the old base again.",
>   "evidence": "Issue #291: branch deleted before the owner's /plan at 2026-10-10T17:54:55Z; run 38073387921 pushed 740b91f to try/issue-291 at 18:04:39Z.",
>   "raised_by": "planner",
>   "id": "P4",
>   "to": "reviewer"
>  }
> ]{
>  "kind": "user_story",
>  "summary": "The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.",
>  "user_story": "The owner sees the criteria checks under a workflow named Acceptance criteria and finds no done-when anywhere they read except in the names of checks #262 renames, while main's branch rule stays exactly as it is.",
>  "acceptance_criteria": [
>   {
>    "text": "The workflow that holds the criteria checks is named Acceptance criteria, with no number, in the file .github/workflows/acceptance-criteria.yml; done-whens.yml is gone. It still runs on every pull request and in the merge queue, each criterion keeps its own check named by its number and words, run by a step named Run this criterion's tests, and the gate still passes only when every criterion's check passed. The card and the board still update when i

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^---\|^\*\*@\|^> \*\*" issue.md | head -100; cat parent.json
```

> 82:## Comments
> 84:### dokima-runtime on issue #291 (2026-10-09T01:30:31Z)
> 88:### dokima-runtime on issue #291 (2026-10-09T01:30:45Z)
> 180:### dokima-runtime on issue #291 (2026-10-09T01:39:02Z)
> 229:### dokima-runtime on issue #291 (2026-10-09T01:45:21Z)
> 234:### dokima-runtime on issue #291 (2026-10-09T01:45:23Z)
> 261:### dokima-runtime on PR #293 (2026-10-09T01:52:04Z)
> 300:### RezaSoleymanifar on issue #291 (2026-10-09T03:57:11Z)
> 304:### dokima-runtime on issue #291 (2026-10-09T03:57:32Z)
> 410:### dokima-runtime on PR #293 (2026-10-09T04:04:33Z)
> 414:### dokima-runtime on issue #291 (2026-10-09T04:04:35Z)
> 432:### dokima-runtime on issue #291 (2026-10-09T04:08:50Z)
> 496:### RezaSoleymanifar on issue #291 (2026-10-09T04:26:34Z)
> 500:### dokima-runtime on issue #291 (2026-10-09T04:26:56Z)
> 576:### dokima-runtime on PR #293 (2026-10-09T04:29:16Z)
> 580:### dokima-runtime on issue #291 (2026-10-09T04:29:19Z)
> 598:### dokima-runtime on PR #293 (2026-10-09T04:34:36Z)
> 602:### dokima-runtime on issue #291 (2026-10-09T04:34:38Z)
> 620:### dokima-runtime on issue #291 (2026-10-09T04:39:03Z)
> 678:### dokima-runtime on PR #293 (2026-10-09T04:44:24Z)
> 682:### dokima-runtime on issue #291 (2026-10-09T04:44:26Z)
> 700:### dokima-runtime on PR #293 (2026-10-09T05:08:20Z)
> 704:### dokima-runtime on issue #291 (2026-10-09T05:08:22Z)
> 722:### dokima-runtime on PR #293 (2026-10-09T05:29:33Z)
> 726:### dokima-runtime on issue #291 (2026-10-09T05:29:35Z)
> 744:### dokima-runtime on PR #293 (2026-10-09T05:50:59Z)
> 748:###

`4. Bash`
```
cd /tmp/pack; sed -n 1,82p issue.md; for l in 300 496 1211 1215 1299 1379 1461 1540; do sed -n "${l},$((l+4))p" issue.md; done
```

> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 264, 282, 295, 305, 308, 358, 388 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [292, 416], "loop": []} -->
> The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See the newest record below
> 
> https://github.com/dokima-dev/dokima/issues/291 · https://github.com/dokima-dev/dokima/pull/293 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/293/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Old branch:** This plan cannot be built on try/issue-291 as it stands. The branch splits off main at 5261412, and main has since added tests that read done-whens.yml by path or wait on the workflow named done-whens; renaming it turns All tests red there, and only a planner can change a test, but this planner run cannot reach them. #393 is that problem, so this issue is now blocked by it. Recomm

`5. Bash`
```
cd /tmp/pack/in; for f in 33 34 35 36; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f-planner.json'));print(list(d.keys()));h=d.get('handback',d);print(json.dumps({k:v for k,v in (h.items() if isinstance(h,dict) else []) if k in ('raises','answers','test_changes','summary')},indent=1)[:4000]); print(json.dumps(d.get('verdict',d.get('check')))[:800]); print(d.get('run'))"; done
```

> == 33
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> {
>  "summary": "The criteria workflow is renamed Acceptance criteria, no check changes its name, and done-when disappears from every other place a person reads.",
>  "test_changes": {
>   "tests/test_checks.py::test_long_done_whens_get_short_check_names": "Renamed test_long_criteria_get_short_check_names, since no test name may say done-whens (291.3); the test itself is unchanged.",
>   "tests/test_merge_check.py::test_the_newest_plan_is_checked_only_once_approved_and_issue_text_is_ignored": "Its docstring said the old done-when format; it now says an older format (291.3). The test itself is unchanged.",
>   "tests/test_merge_check.py::test_a_criterion_without_tests_gets_a_check_that_can_only_fail": "It reads the criteria workflow by path, and done-whens.yml becomes acceptance-criteria.yml (291.1, 291.3).",
>   "tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code": "It reads the criteria workflow by path, and done-whens.yml becomes acceptance-criteria.yml (291.1, 291.3); its docstring no longer says done-whens.",
>   "tests/test_manifest.py::test_the_guard_passes_settings_the_manifest_declares": "Its fake code's constant DONE_WHENS is now GATE, since no name may say done-whens (291.3); the check name all done-whens passed stays, as the owner asked."
>  },
>  "raises": [
>   {
>    "kind": "blocker",
>    "to": "owner",
>    "label": "Old

**Agent:** Reading the newest plan and its records; next I check the branch base and run the plan's tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git merge-base HEAD origin/main 2>/dev/null; git rev-list --count HEAD..origin/main 2>/dev/null; git diff --stat HEAD~1; python3 -c "
import json;d=json.load(open('/tmp/pack/in/36-planner.json'));print(json.dumps(d['handback'].get('raises'),indent=1));print(d['handback'].get('answers'))"
```

> 7bb77cd planner for #291 (run 38074876376)
> da897bc AGENTS.md records the raise design, and the shared prompt section teaches it with many examples (#419)
> f7340db board.yml runs the pull request's own copy of itself, with the keys, on a review (#418)
> da897bc1861cfb03502c1a4c1b9ebdd3ac11d00c
> 2
>  tests/card_player.py           |   2 +-
>  tests/test_board_state.py      |   4 +-
>  tests/test_card_merge.py       |   2 +-
>  tests/test_card_queue.py       |   6 +-
>  tests/test_check_names.py      | 229 +++++++++++++++++++++++++++++++++++++++++
>  tests/test_checks.py           |   2 +-
>  tests/test_manifest.py         |   4 +-
>  tests/test_merge_check.py      |  12 +--
>  tests/test_merge_queue.py      |  36 +++----
>  tests/test_needs_you.py        |   6 +-
>  tests/test_plan_check_rerun.py |   6 +-
>  tests/test_review_relay.py     |   2 +-
>  tests/test_text_only.py        |  18 ++--
>  13 files changed, 279 insertions(+), 50 deletions(-)
> null
> None

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 -- tests/card_player.py tests/test_card_merge.py tests/test_plan_check_rerun.py tests/test_text_only.py tests/test_review_relay.py; cat tests/test_check_names.py
```

> diff --git a/tests/card_player.py b/tests/card_player.py
> index 7b24463..08659a4 100644
> --- a/tests/card_player.py
> +++ b/tests/card_player.py
> @@ -629,7 +629,7 @@ def line_note(n, p, who=OWNER, action="created"):
>                                             "repository": REPOSITORY}
>  
>  
> -def checks_finished(n, p, workflow="done-whens"):
> +def checks_finished(n, p, workflow="Acceptance criteria"):
>      """A workflow_run event: the checks of PR p finished."""
>      run = {"name": workflow, "head_sha": f"sha{p}", "head_branch": f"try/issue-{n}", "display_title": f"Issue {n}",
>             "event": "pull_request_target", "status": "completed", "conclusion": "success",
> diff --git a/tests/test_card_merge.py b/tests/test_card_merge.py
> index 1a94022..8200417 100644
> --- a/tests/test_card_merge.py
> +++ b/tests/test_card_merge.py
> @@ -634,7 +634,7 @@ def line_note(n, p, who=OWNER, action="created"):
>                                             "repository": REPOSITORY}
>  
>  
> -def checks_finished(n, p, workflow="done-whens"):
> +def checks_finished(n, p, workflow="Acceptance criteria"):
>      """A workflow_run event: the checks of PR p finished."""
>      run = {"name": workflow, "head_sha": f"sha{p}", "head_branch": f"try/issue-{n}", "display_title": f"Issue {n}",
>             "event": "pull_request_target", "status": "completed", "conclusion": "success",
> diff --git a/tests/test_plan_check_rerun.py b/tests/test_plan_check_rerun.py
> index 8a8f193..c7ce830 100644
> --- a/tests/test_plan_check_rerun.py
> +++ b/

`8. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows/; timeout 600 python3 -m pytest -q tests/test_check_names.py 2>&1 | tail -30
```

> agent.yml
> assign.yml
> audit.yml
> autopilot.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> reviews.yml
> uptodate.yml
> wiki.yml
> worker.yml
> E         dokima/checks.py line 104: lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"
> E       assert not ['.github/workflows/board.yml line 26: workflows: [done-whens, reviews]', '.github/workflows/card.yml line 16: workflo... if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi', ...]
> 
> tests/test_check_names.py:229: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_check_names.py::test_the_criteria_workflow_is_named_acceptance_criteria_in_its_own_file - AssertionError: 291.1: .github/workflows/acceptance-criteria.yml does not exist; the workflow files are ['agent.yml', 'assign.yml', 'audit.yml', 'autopilot.yml', 'board.yml', 'card.yml', 'commands.yml', 'done-whens.yml', 'full-suite.yml', 'planner.yml', 'reviews.yml', 'uptodate.yml', 'wiki.yml', 'worker.yml']
> assert False
>  +  where False = <function exists at 0x7fc815307600>('/home/runner/work/dokima/dokima/.github/workflows/acceptance-criteria.yml')
>  +    where <function exists at 0x7fc815307600> = <module 'posixpath' (frozen)>.exists
>  +      where <module 'posixpath' (frozen)> = os.path
> FAILED tests/test_check_names.py::test_the_card_and_the_board_update_when_the_acceptance_criteria_workflow_finishes - AssertionE

**Agent:** All four new tests fail today for the right reason. Now the full suite, to see the edited older tests fail only on the missing rename.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -x -p no:cacheprovider -n auto 2>/dev/null | tail -3 || true; timeout 900 python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-220
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bgeadc0eu). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/2c2e7341-e7ef-422f-a750-ab7c7d0ec5dd/tasks/bgeadc0eu.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 -- tests/test_merge_queue.py | grep '^[-+]' | head -80; python3 -c "
import json;d=json.load(open('/tmp/pack/in/11-reviewer-plan.json'));h=d['handback'];print(h['verdict'],h['summary']);print(json.dumps(h.get('asks'),indent=1))"
```

> --- a/tests/test_merge_queue.py
> +++ b/tests/test_merge_queue.py
> -done-whens.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> +acceptance-criteria.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> -    """The pull_request_target payload done-whens.yml gets for pull request n."""
> +    """The pull_request_target payload acceptance-criteria.yml gets for pull request n."""
> -    lines = workflow("done-whens.yml")
> +    lines = workflow("acceptance-criteria.yml")
> -    Proves 191.1. Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
> -    the done-whens check checks out and the commit its annotations link to for a merge_group event, and checks both are
> +    Proves 191.1. Reads the `on:` of full-suite.yml and acceptance-criteria.yml and checks each lists merge_group; then evaluates the commit
> +    the criteria check checks out and the commit its annotations link to for a merge_group event, and checks both are
> -    for name in ("full-suite.yml", "done-whens.yml"):
> +    for name in ("full-suite.yml", "acceptance-criteria.yml"):
> -    assert refs and heads, "191.1: done-whens.yml has no `ref:` on the checkout with `path: pr` or no HEAD_SHA"
> +    assert refs and heads, "191.1: acceptance-criteria.yml has no `ref:` on the checkout with `path: pr` or no HEAD_SHA"
> -            assert got is not None, f"191.1: done-whens.yml {wh

`11. Bash`
```
cd /tmp/pack; grep -o "https://github.com/dokima-dev/dokima/issues/291#issuecomment-[0-9]*" issue.md | sort -u | head; grep -rho "issuecomment-[0-9]*" in/*.json | sort -u | head -20
```

> Shell cwd was reset to /home/runner/work/dokima/dokima

`12. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/2c2e7341-e7ef-422f-a750-ab7c7d0ec5dd/tasks/bgeadc0eu.output
```

> """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
>         criteria workflow's checks are still named list done-whens and all done-whens passed; that no workflow has a check
>         named All tests or Acceptance criteria; that the manifest still requires all tests and all done-whens passed on
>         tests/samples, and this test. Allowed: the names of the checks all done-whens passed and list done-whens, which keep
>         assert code == 0, f"191.3: on pull request #90, `dokima.checks matrix` failed:\n{err}"
>         assert code == 0, f"191.3: in the merge queue (pull request #90), `dokima.checks matrix` failed:\n{err}"
>         added beyond the queue; that the required check names 'all tests' and 'all done-whens passed' are unchanged; that
>         "all done-whens passed" gate still waits on it and fails when it fails), main's branch rule still requires
>         "all tests" and "all done-whens passed", and CODEOWNERS still names a code owner for every file, whose approving
> FAILED tests/test_card_queue.py::test_every_redraw_about_an_issue_or_its_pr_waits_in_a_queue_of_its_own_that_keeps_the_newest - AssertionError: 346.1: card.yml does not start on workflow_run completed, so the cards are n
> FAILED tests/test_card_queue.py::test_a_redraw_for_one_issue_never_shares_a_queue_with_another_issue_or_the_sweep - AssertionError: 3

`13. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree add -q /tmp/mainwt origin/main 2>&1|tail -1; cd /tmp/mainwt && timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_card_queue.py tests/test_board_state.py tests/test_needs_you.py tests/test_plan_check_rerun.py tests/test_card_merge.py 2>&1 | tail -2; cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_card_queue.py 2>&1 | grep -B2 -A8 "346.1" | head -30; git worktree remove --force /tmp/mainwt
```

> ...................................ssss......                            [100%]
> 41 passed, 4 skipped in 14.13s
>         """Redraws about an issue or its PR wait in its own queue, keeping the newest.
>     
>         Proves 346.1.     Plays card.yml for each event card.yml redraws on about #246 or its PR #260 (the issue edited, a comment on it, the
>         merge by the owner and by the bot, the Acceptance criteria and full suite checks finishing, the worker finishing), and the
>         same for #312 and PR #314. Every run must redraw, the job that writes the cards must wait in a named queue, all of
>         one issue's runs in the same one, and that queue must be its own: #312's redraws wait in a different one. No queue
>         any run takes a place in may cancel the run already in it, so GitHub lets the running redraw finish and keeps the
>         newest waiting one. The events that draw no card today (the bot's own comment, a comment on a pull request, a pull
>         request closed unmerged) must still draw none."""
>         record_property("proves", "346.1")
>         hub = Hub(tmp_path)
>         own = {}
>         for n, p in ((246, 260), (312, 314)):
>             queues = {}
>             for what, event in events_about(n, p).items():
> >               card, _, cancelling = play(hub, event, "346.1")
>                                       ^^^^^^^^^^^^^^^^^^^^^^^^^
> 
> tests/test_card_queue.py:58: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_card_qu

**Agent:** The plan holds up, so I'm approving it. Writing the hand-back now.

`14. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner started this round from today's main and kept the plan from earlier rounds.",
   "It changed main's older tests that read done-whens.yml by path or wait on the workflow named done-whens, so they now expect acceptance-criteria.yml and the workflow Acceptance criteria."
  ],
  "decided": [
   "No check changes its name. all tests, list done-whens and all done-whens passed keep their names until #262, so main's branch rule stays as it is."
  ],
  "open": [
   "The worker renames the workflow and its file, updates card.yml, board.yml, dokima/agent.py and dokima/checks.py, and rewords the remaining done-when lines."
  ]
 },
 "verdict": "approve",
 "summary": "The plan now starts from today's main, keeps what PR #293 built, and every new or changed test fails today only because the workflow is not renamed yet.",
 "raises": [],
 "answers": [
  {"raise": "P4", "answer": "done", "why": "Confirmed from this issue's history. The owner deleted try/issue-291 before their /plan at 2026-10-10T17:54:55Z. Planner run 38073387921, which was still running, pushed 740b91f to the branch at 18:04:39Z, and the next run started from that old base again (planner record 35, PLANNER_RUN_BASE=740b91f). The cause sits in .github/workflows/agent.yml, not in this issue, so it is worth its own issue."}
 ],
 "asks": [
  {"ask": "The check that passes only when every criterion's tests passed, and its workflow, are named Acceptance criteria, with no number.", "source": "https://github.com/dokima-dev/dokima/issues/291", "criterion": "291.1"},
  {"ask": "Each criterion keeps its own check, named by its number and words. The card and the board still update when these checks finish.", "source": "https://github.com/dokima-dev/dokima/issues/291", "criterion": "291.1"},
  {"ask": "The card still shows that check's verdict in its Definition of Done row and redraws when it finishes.", "source":
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> exit 0

`15. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan now starts from today's main, and every new or changed test fails today only because the workflow is not renamed yet."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 291 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo exit $?
```

> exit 0

**Agent:** I approved the plan for issue #291 (renaming the criteria workflow to Acceptance criteria). The approval is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Starts from today's main:** the branch now splits off main 2 commits back, not 35. The planner updated main's newer tests that read `done-whens.yml` by path or wait on the workflow named done-whens. Each test it renamed or reworded is listed with a reason.
- **New tests fail for the right reason:** all four new tests in `tests/test_check_names.py` fail today only because the rename isn't done yet. Nothing crashes and no path is bad. The text scan names exactly the places the worker still has to change: `card.yml`, `board.yml`, `done-whens.yml`, `dokima/agent.py` and `dokima/checks.py`.
- **Full suite:** 848 passed, 78 skipped, and 14 failed. All 14 failures are the planned tests waiting for the rename: a missing `acceptance-criteria.yml`, or `card.yml` and `board.yml` not yet listening for Acceptance criteria. I ran the affected older test files on main and they pass there (41 passed, 4 skipped).
- **Your asks:** each one maps to a criterion, including your comments to leave every check rename to [#262](https://github.com/dokima-dev/dokima/issues/262) (the check renames themselves), to keep what [PR #293](https://github.com/dokima-dev/dokima/pull/293) (the earlier build of this issue) built, and to edit the old tests.
- **Branch pushed back:** I confirmed the planner's report. A planner run that was still going when you deleted `try/issue-291` pushed the branch back. The cause is in `agent.yml`, outside this issue, so it's worth its own issue.

One gap, not a blocker: the planner also edited a few test helpers and one docstring (`tests/card_player.py`, `tests/test_card_merge.py`, `tests/test_plan_check_rerun.py`) but didn't list them in its record of changed tests. Through the shared helper, another test in `tests/test_card_queue.py` that isn't listed now also waits for the rename. These edits are on the branch already, so the worker doesn't need to touch them.
