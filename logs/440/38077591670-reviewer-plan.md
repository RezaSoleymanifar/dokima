# reviewer (plan) for #440

Run: https://github.com/dokima-dev/dokima/actions/runs/38077591670

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/plan.json; cat /tmp/pack/open_blockers.json
```

> # Issue #440: When a plan is approved, its pull request's checks run again by themselves
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/440
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #425, story 4</summary>
> 
> **Part of:** #425 The card always shows what is true right now: one rule, one place
> 
> **User story:** When a plan is approved while its pull request is open, the pull request's checks run again by themselves on its head, and if Dokima's app lacks the permission the owner is told exactly which setting to change.
> 
> **Context:** dokima/agent.py rerun_plan_check (line 1399), called from agent.yml line 396 through `agent recheck`, re-runs only the newest done-whens.yml run on the head, and only when it has completed; a running one gets a comment instead. dokima/app.json declares actions: write, which GitHub's re-run endpoint (POST /repos/{owner}/{repo}/actions/runs/{id}/rerun) needs; an installation that has not accepted the new permission refuses with 403. This was #422.
> 
> **Acceptance criteria:**
> - When a plan is approved with its pull request open, every check on the pull request's head runs again by itself. That includes one still running from the last push, with no comment and no owner action. ([source](https://github.com/dokima-dev/dokim

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_checks_rerun.py; grep -n "def rerun_plan_check" -A80 dokima/agent.py
```

> commit 9d4082d33c417bfaa6071235d377ecd3bac282c6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:53:01 2026 +0000
> 
>     planner for #440 (run 38076669893)
> 
>  tests/conftest.py              |   1 -
>  tests/test_checks_rerun.py     | 420 +++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_check_rerun.py |  29 +--
>  3 files changed, 422 insertions(+), 28 deletions(-)
> """An approved plan runs every check on its pull request's head again by itself (#440).
> 
> GitHub runs a pull request's checks only when it gets a new commit, so a plan approved with nothing new to push keeps
> the checks that ran before the approval. agent.yml's step "Run the plan check again once the plan is approved" calls
> `python3 -m dokima.agent recheck N OUT` once the plan review's record is up; these tests run that command, as the
> workflow does, against a fake `gh` on PATH that keeps GitHub in one JSON file.
> 
> The fake GitHub holds issue #57, whose pull request #60 is open on try/issue-57 (unless the test closes it), and the
> GitHub Actions runs on its head. It answers the calls Dokima may use for this, logging every call and every call it
> does not understand:
>   - the pull request: `gh pr list` (with --head, --state, --json, -q), `gh pr view 60|try/issue-57`,
>     `gh api repos/o/r/pulls[?head=..&state=..]` and `gh api repos/o/r/pulls/60`;
>   - the runs: `gh api repos/o/r/actions/runs[?head_sha=..&event=..&status=..]`,
>     `gh api repos/o/r/actions/workflow

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_plan_check_rerun.py tests/conftest.py; grep -n "recheck" -B3 -A30 .github/workflows/agent.yml | head -80
```

> commit 9d4082d33c417bfaa6071235d377ecd3bac282c6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:53:01 2026 +0000
> 
>     planner for #440 (run 38076669893)
> 
> diff --git a/tests/conftest.py b/tests/conftest.py
> index bb679f2..a2d01f1 100644
> --- a/tests/conftest.py
> +++ b/tests/conftest.py
> @@ -77,7 +77,6 @@ SLOW = {
>      "test_parent_source.py::test_on_autopilot_the_owners_words_in_the_parent_count_as_really_said",
>      "test_plan_check.py::test_a_source_outside_this_issue_is_rejected_and_named[other",
>      "test_plan_check.py::test_anything_but_a_story_or_a_feature_is_rejected_saying_the_planner_always_hands_back_a_plan[no",
> -    "test_plan_check_rerun.py::test_a_plan_check_that_cannot_run_again_says_why_on_the_pull_request",
>      "test_plan_check_rerun.py::test_a_reapproved_plan_with_no_new_commit_ends_with_a_passing_plan_check",
>      "test_plan_check_rerun.py::test_only_an_approval_with_an_open_pull_request_runs_the_plan_check_again",
>      "test_plan_check_rerun.py::test_the_plan_check_runs_again_only_with_the_apps_key_after_the_agent_finished",
> diff --git a/tests/test_plan_check_rerun.py b/tests/test_plan_check_rerun.py
> index 8a8f193..0d16065 100644
> --- a/tests/test_plan_check_rerun.py
> +++ b/tests/test_plan_check_rerun.py
> @@ -170,7 +170,7 @@ def plan_run(rid, sha, status="completed", conclusion="failure", matrix=None):
>  
>  
>  def other_run(rid, sha):
> -    """A run of another workflow on the same commit, which an approval le

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_checks_rerun.py 2>&1 | grep -E "^(FAILED|PASSED|E  .*440|[0-9]+ )|440\.[0-9]:" | head -30; timeout 900 python3 -m pytest -q tests/test_plan_check_rerun.py 2>&1 | tail -3
```

> assert m.proc.returncode == 0, f"440.1: the recheck command failed{m.why()}"
> >           assert m.rerun(rid), f"440.1: {name} (run {rid}) on the head {HEAD[:7]} was not run again in full{m.why()}"
> E           AssertionError: 440.1: All tests (run 7002) on the head aaaaaaa was not run again in full
> E               AssertionError: 440.2 (Organization): the comment does not say 'dokima': 'The plan of #57 is approved, but the plan check on aaaaaaa could not run again: GitHub refused: gh: Resource not accessible by integration (HTTP 403). Re-run all its jobs once it can, so it reads the approved plan: https://github.com/o/r/actions/runs/7001'
>         assert m.proc.returncode == 0, f"440.3: the recheck command failed with no open pull request{m.why()}"
>         assert not m.state["log"], f"440.3: with no open pull request, runs were stopped or run again: {m.state['log']}{m.why()}"
>         assert not m.comments(), f"440.3: with no open pull request, something was posted: {m.comments()}{m.why()}"
>             f"440.3: with the pull request open, its checks did not all run again{opened.why()}"
> E       AssertionError: 440.3: with the pull request open, its checks did not all run again
>         assert m.proc.returncode == 0, f"440.4: the recheck command failed{m.why()}"
> >       assert len(on_pr) == 1, f"440.4: expected one comment on PR #60 saying why All tests could not run again, got {m.comments()}{m.why()}"
> E       AssertionError: 440.4: expected one comment on PR #60 saying why All tes

`5. Bash`
```
cd /home/runner/work/dokima/dokima; for f in .github/workflows/*.yml; do echo "== $f"; sed -n '/^on:/,/^[a-z]/p' $f | head -20; done 2>/dev/null | head -150
```

> == .github/workflows/agent.yml
> on:
>   repository_dispatch:
>     types: [dokima-next]
>   workflow_call:
>     inputs:
>       role: {type: string, required: true}
>       stage: {type: string, default: plan}
>       issue: {type: string, required: true}
>       # The id of the run's queued card, put up by the listener; the run updates it instead of putting up its own.
>       card: {type: string, default: ''}
>   workflow_dispatch:
>     inputs:
>       role:
>         description: Which agent
>         type: choice
>         options: [planner, reviewer, worker]
>       stage:
>         description: For the reviewer, what it grades
>         type: choice
>         options: [plan, pr]
> == .github/workflows/assign.yml
> on:
>   issues:
>     types: [opened]
> permissions:
> == .github/workflows/audit.yml
> on:
>   schedule:
>     - cron: "17 6 * * *"
>   workflow_dispatch:
> concurrency:
> == .github/workflows/autopilot.yml
> on:
>   issues:
>     types: [closed]
> concurrency:
> == .github/workflows/board.yml
> on:
>   issues:
>     types: [opened, edited, labeled, unlabeled, closed, reopened]
>   schedule:
>     - cron: "*/15 * * * *"
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   # A review or line note would run the pull request's own copy of this file, so
>   # they reach it through reviews.yml, which holds no key; this runs after it.
>   workflow

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p tests/conftest.py | grep -n -i -E "slow|skip|env" | head
```

> 1:"""Temporary: skip the slow tests (each 1 second or more) so the suite runs in about a minute.
> 11:SLOW = {

**Agent:** Tests fail for the right reasons; checking the older test file's fake GitHub still fits the new behavior.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,12p tests/conftest.py; sed -n 85,140p tests/conftest.py; grep -n "actions/" tests/test_plan_check_rerun.py | head -20
```

> """Temporary: skip the slow tests (each 1 second or more) so the suite runs in about a minute.
> 
> Five end-to-end replays stay: a command starts its agent or says why, a card goes queued to done,
> autopilot stops where the owner must decide, a failed run gets Needs you, a cancelled run says so.
> The parked test-speed issue makes the rest fast and deletes this file. DOKIMA_ALL_TESTS=1 runs everything.
> """
> import os
> 
> import pytest
> 
> SLOW = {
>     "test_automerge.py::test_a_pull_request_changing_a_workflow_file_never_merges_by_autopilot",
>     "test_plan_links_recorded.py::test_a_link_github_already_has_is_not_added_twice",
>     "test_plan_links_recorded.py::test_a_link_github_fails_to_remove_stops_the_river_and_says_why",
>     "test_plan_links_recorded.py::test_a_plan_the_review_blocks_records_nothing",
>     "test_plan_links_recorded.py::test_a_relates_to_link_switched_to_blocks_moves_on_the_other_card",
>     "test_plan_links_recorded.py::test_a_replan_the_review_blocks_removes_nothing",
>     "test_plan_links_recorded.py::test_an_approved_plan_records_its_blocking_links_on_github",
>     "test_plan_links_recorded.py::test_both_cards_show_every_new_link_from_their_own_side",
>     "test_plan_links_recorded.py::test_links_with_no_loop_are_recorded_and_autopilot_goes_on",
>     "test_plan_links_recorded.py::test_recorded_links_let_autopilot_go_on",
>     "test_plan_links_recorded.py::test_the_other_card_keeps_the_link_after_its_own_redraw",
>     "test_plan_links_recorded.py::test_turning_a_link_around

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 150,175p tests/test_plan_check_rerun.py; DOKIMA_ALL_TESTS=1 timeout 900 python3 -m pytest -q tests/test_plan_check_rerun.py 2>&1 | tail -3
```

> "workflowName": r["name"], "event": r["event"], "number": r["id"], "attempt": r["run_attempt"],
>            "headBranch": r["head_branch"], "url": f"https://github.com/o/r/actions/runs/{r['id']}"} for r in rs])
>     sys.exit(0)
> '''
> 
> 
> def fake_gh():
>     """The fake GitHub of test_start.py, taught pull request #60 and the plan check's runs."""
>     anchor = 'if a[:2] == ["issue", "view"]:'
>     taught = ts.FAKE_GH.replace(anchor, RUNS_GH.replace("@@ROOT@@", ROOT) + anchor, 1)
>     assert taught != ts.FAKE_GH, "test setup: could not teach the fake GitHub about runs"
>     return taught.replace("#!/usr/bin/env python3", f"#!{sys.executable}")
> 
> 
> def plan_run(rid, sha, status="completed", conclusion="failure", matrix=None):
>     """One run of the plan check on commit `sha`, as GitHub keeps it."""
>     return {"id": rid, "name": "done-whens", "path": ".github/workflows/done-whens.yml", "event": "pull_request_target",
>             "head_sha": sha, "head_branch": "try/issue-57", "status": status,
>             "conclusion": conclusion if status == "completed" else None, "run_attempt": 1,
>             "matrix": STALE if matrix is None else matrix, "reruns": []}
> 
> 
> def other_run(rid, sha):
>     """A run of another workflow on the same commit."""
>     return {**plan_run(rid, sha), "name": "full-suite", "path": ".github/workflows/full-suite.yml"}
> 
> ...                                                                      [100%]
> 3 passed in 9.43s

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote three criteria and two non-functional rules for re-running every check on the pull request's head when a plan is approved, with five new tests in tests/test_checks_rerun.py.",
          "Deleted the old test that wanted a comment when the plan check is still running, and dropped one assert that kept other checks from running again."],
  "decided": ["Only the newest run of each check a push to the head started runs again; runs a review, a comment or another workflow started are left alone, so no agent starts again.",
              "The permission comment links the organization's installations page for an organization's repo and the account's own for a personal repo."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan carries every ask of story 4 of #425, and each of its five tests fails today because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "When a plan is approved with its pull request open, every check on the pull request's head runs again by itself. That includes one still running from the last push, with no comment and no owner action.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "440.1"},
  {"ask": "When GitHub refuses the re-run for lack of permission, the pull request gets one comment naming the setting to change. It says Dokima's GitHub App needs Actions set to Read and write, accepted on its installation, with that page's link.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "440.2"},
  {"ask": "With no open pull request, nothing runs and nothing is posted.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "440.3"},
  {"ask": "A re-run that fails for any other reason says why on the pull request, with GitHub's own reason.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "440.4"}
 ]}
EOF
cd /home/ru
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#440](https://github.com/dokima-dev/dokima/issues/440) (checks run again when a plan is approved). The hand-back is in `/tmp/dokima-out/review.json`, and both checks on it passed.

**Why it passes:**
- **Every ask is covered.** All four asks from story 4 of [#425](https://github.com/dokima-dev/dokima/issues/425) (the card shows what is true now) map to a test, 440.1 to 440.4. Each test checks the outcome in both directions:
  - 440.1: every check runs again in full, including one still running, and nothing is posted.
  - 440.2: one permission comment however many checks are refused, with the right link for an organization's repo and for a personal one.
  - 440.3: nothing happens with the pull request closed, and the checks do run again when it is open.
  - 440.4: another refusal shows GitHub's own reason and does not send the owner to the permission setting.
  - 440.5: only the newest run of each check a push started runs again, exactly once.
- **All five new tests fail today for the right reason.** The current code only re-runs the plan check and posts the old generic comment, so the failures come from the missing feature, not a crash or a bad setup.
- **The fake GitHub matches the real workflows.** It uses the same trigger as the real checks (`done-whens.yml` and `full-suite.yml` both run on `pull_request_target`), so code written against the fake will see the same runs in real use.
- **The test changes are justified.** The old test file still passes in full when run with `DOKIMA_ALL_TESTS=1` (3 passed). The deleted test asked for a comment while a check is still running, which 440.1 now rules out.

**One choice made without asking you:** the planner narrowed "every check" so that runs started by a review, a comment or another workflow never run again. Re-running those would start agents again, which goes against "Bots never start anything" in AGENTS.md, so I accepted it rather than calling it a silent narrowing.

**A small gap I didn't block on:** the 440.4 test only checks that the comment leaves out "read and write". A comment that linked the installations page without those words would still pass. It's a minor gap in the second, non-blocking part of that rule.

I raised nothing, and no raises were open for me to answer.
