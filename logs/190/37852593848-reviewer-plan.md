# reviewer (plan) for #190

Run: https://github.com/dokima-dev/dokima/actions/runs/37852593848

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
> # Issue #190: A clash with main goes to the planner, on the record
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #57, story 2</summary>
> 
> **Part of:** #57 Keep PRs up to date with main automatically
> 
> **User story:** When a PR clashes with main after a merge, the issue gets a record naming the merge that caused it and the files that clashed, and the planner re-plans right away against the new main; for a PR Dokima didn't build, the owner is pinged instead.
> 
> **Context:** The owner corrected the first split: a clash goes to the planner, not the worker, because the plan may not fit main anymore (comments of 2026-10-07 22:10:09, 22:10:44 and 22:21:16). Story 1 detects the clash (update-branch answers 422 'merge conflict') and hands the PR and the merge commit (the push's head sha on main, and the PR it merged if any, from GET /commits/{sha}/pulls) to this story. GitHub's 422 does not list files: code finds them with a trial merge in a checkout (git merge --no-commit origin/main on the PR head, then git diff --name-only --diff-filter=U), with a git user.name and user.email set. A Dokima PR's branch is try/issue-N (dokima/agent.py issue_of_pr). The record must be a bot comment carrying the record marker (MARK, '<!-- dokima-record -->') with a JSON record folded below, since only the bot's records count (dokima/agent.py records()); give it its own role (e.g. 'updater') an

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_clash.py; timeout 600 python -m pytest -q tests/test_clash.py 2>&1 | tail -40
```

> commit 5d6b5a6f798a52c049ec36af2f73903d7b46b4ea
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 22:17:53 2026 +0000
> 
>     planner for #190 (run 37851463011)
> 
>  tests/test_clash.py | 505 ++++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 505 insertions(+)
> 505 tests/test_clash.py
>   Auto-merging app.py
>   CONFLICT (content): Merge conflict in app.py
>   Auto-merging lib.py
>   CONFLICT (content): Merge conflict in lib.py
>   Automatic merge failed; fix conflicts and then commit the result.
>   
> assert 'failure' == 'success'
>   
>   - success
>   + failure
> FAILED tests/test_clash.py::test_the_fence_keeps_mains_changes_and_drops_only_the_workers_out_of_scope_ones - AssertionError: 190.5: the clashing worker run failed at 'Starting branch':
>   ## run: Starting branch (exit 1)
>   Auto-merging app.py
>   CONFLICT (content): Merge conflict in app.py
>   Auto-merging lib.py
>   CONFLICT (content): Merge conflict in lib.py
>   Automatic merge failed; fix conflicts and then commit the result.
>   
>   ## run: Copy the runtime from main before touching any branch (exit 0)
>   
>   ## run: Starting branch (exit 1)
>   Auto-merging app.py
>   CONFLICT (content): Merge conflict in app.py
>   Auto-merging lib.py
>   CONFLICT (content): Merge conflict in lib.py
>   Automatic merge failed; fix conflicts and then commit the result.
>   
> assert 'failure' == 'success'
>   
>   - success
>   + failure
> FAILED tests/test_clash.py::test_a_second_clash_while_the_planner_waits_reco

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_clash.py 2>&1 | grep -E "^FAILED|^E " | head -40; cat tests/test_clash.py
```

> <persisted-output>
> Output too large (31.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/af9b5fc0-974b-484b-ae79-f4f205c3e658/tool-results/bfljaraj3.txt
> 
> Preview (first 2KB):
> E           Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> E           Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> E           Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> E           Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> E           Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> E       AssertionError: 190.4: a worker on a branch that clashes with main failed at 'Starting branch':
> E         ## run: Starting branch (exit 1)
> E         Auto-merging app.py
> E         CONFLICT (content): Merge conflict in app.py
> E         Auto-merging lib.py
> E         CONFLICT (content): Merge conflict in lib.py
> E         Automatic merge failed; fix conflicts and then commit the result.
> E         
> E         ## run: Copy the runtime from main before touching any branch (exit 0)
> E         
> E         ## run: Starting branch (exit 1)
> E         Auto-merging app.py
> E         CONFLICT (content): Merge conflict in app.py
> E         Auto-merging lib.py
> E         CONFLICT (content): Merge conflict in lib.py
> E         Automatic merge failed; fix conflicts and then commit the result.

`4. Read`
```
/home/runner/work/dokima/dokima/tests/test_clash.py
```

> 1	"""A clash with main goes to the planner, on the record (#190).
> 2	
> 3	After a merge to main, `dokima.uptodate.run(repo, base, sha, rest=..., on_clash=...)` calls `on_clash(pr, sha)` for
> 4	every PR GitHub refuses to update with a merge conflict (#189). This story fills that hook with
> 5	`dokima.uptodate.clash(repo, base, sha, pr, rest=api, files=None, owners=None)`, and `python3 -m dokima.uptodate`
> 6	wires it in:
> 7	  - `pr` is the PR as GitHub lists it; `sha` is the merge on main (the push's head sha);
> 8	  - `files(pr, sha)` returns the paths that clashed; by default a trial merge in the git checkout the module runs in,
> 9	    fetching what it needs from its `origin` remote;
> 10	  - `owners` are the code owners' logins; by default those of the checkout's CODEOWNERS;
> 11	  - every GitHub call goes through `rest(method, path, **fields)`, shaped like `dokima.board.api`.
> 12	
> 13	A Dokima PR is one whose branch is try/issue-N in this same repo. Its clash leaves a record on issue N (a bot comment
> 14	carrying agent.MARK with the JSON record folded below, role "updater") and starts the planner for N with the river's
> 15	own `dokima-next` signal, unless a clash record is already waiting for its planner. Any other PR gets a comment that
> 16	mentions the owners and starts nothing.
> 17	
> 18	The worker side runs the real steps of .github/workflows/agent.yml on the machine from test_start.py: a temp origin
> 19	where main and try/issue-57 clash, the worker's edits, the fence and the push.
> 20	
> 21	The 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_clash.py 2>&1 | grep -E "^(FAILED|ERROR)"; grep -n "def status" -A60 dokima/card.py | head -90
```

> FAILED tests/test_clash.py::test_a_clash_leaves_one_record_naming_the_merge_its_pr_and_every_clashed_file - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> FAILED tests/test_clash.py::test_the_clash_record_reaches_the_planner_through_its_pack - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> FAILED tests/test_clash.py::test_right_after_the_record_the_planner_starts_and_no_worker - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> FAILED tests/test_clash.py::test_the_issue_card_shows_plan_and_not_needs_you_after_a_clash_record - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> FAILED tests/test_clash.py::test_a_clash_on_a_pr_dokima_did_not_build_pings_the_owner_and_starts_nothing - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, rest, files, owners) is missing
> FAILED tests/test_clash.py::test_a_worker_on_a_branch_that_clashes_starts_and_pushes_main_merged_with_no_markers - AssertionError: 190.4: a worker on a branch that clashes with main failed at 'Starting branch':
> FAILED tests/test_clash.py::test_the_fence_keeps_mains_changes_and_drops_only_the_workers_out_of_scope_ones - AssertionError: 190.5: the clashing worker run failed at 'Starting branch':
> FAILED tests/test_clash.py::test_a_second_clash_while_the_planner_waits_records_but_starts_no_second_planner - Failed: 190: dokima.uptodate.clash(repo, base, sha, pr, r

**Agent:** Tests all fail today for the right reasons (the clash handler missing, the worker's start failing on the clash). Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["The planner wrote three criteria and three non-functional requirements, with ten new tests in tests/test_clash.py.", "The tests fake GitHub, run a real trial merge and run the real steps of the agent workflow for a worker on a clashing branch."],
  "decided": ["A clash record is a bot record with role 'updater' on issue N, and the planner starts with the river's dokima-next signal.", "A pull request Dokima didn't build, a fork's included, gets one comment mentioning the code owners and starts nothing.", "The work changes .github/workflows/agent.yml, so the pull request will wait for the owner's approval on GitHub."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask from #57 and each test fails today because the feature is missing, so it is ready for the owner's /work.",
 "blockers": [],
 "notes": [
  {"text": "Reading the code owners from CODEOWNERS by default is only exercised for a Dokima pull request; the ping on a pull request Dokima didn't build is tested with owners passed in. The worker should make sure the default reaches that comment too.", "evidence": "tests/test_clash.py:126 passes owners=list(OWNERS); only test_the_real_module_records_the_files_a_trial_merge_finds_and_starts_the_planner uses the checkout's CODEOWNERS, and on try/issue-7."},
  {"text": "The issue card test relies on dokima/agent.py (next_step, board_place), which is in scope; dokima/card.py, which is off limits, needs no change for it.", "evidence": "dokima/card.py:147 calls agent.board_place(rec, agent.next_step(...)) for every role but split."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "post a record on the issue naming the merge that caused it and what clashed", "source": "https://github.com/dokima-dev/dokima/issues/190", "criterion": "190.1"},
  {"ask": "A clash goes to the planner, not the worker", "source": "https://gith
```

> rc=0

**Agent:** I approved the plan for #190. Both checks on my review passed, and the review is saved at `/tmp/dokima-out/review.json`.

**Why it passes:**
- **Every ask is covered.** The four asks quoted from the owner's comments on #57 and the three requirements from the story each map to a criterion (190.1 to 190.6). None are missing.
- **The tests fail today for the right reason.** I ran all 10 tests in `tests/test_clash.py` and all 10 fail. In 7 the cause is that the code that handles a clash (`dokima.uptodate.clash`) doesn't exist yet. In 2, the agent workflow's real steps fail at "Starting branch" on the conflict, which is the dead end the issue describes. The last one runs the real module with a fake `gh` and gets no record on the issue.
- **The tests catch mistakes in both directions.** Each one that rejects something has a matching case that should pass:
  - A branch that merges cleanly sits beside the clashing one.
  - Main's own files are checked as kept, and the worker's out-of-scope file as dropped.
  - "No second planner while one is waiting" is paired with "it starts again after the planner answered", and a record pasted by someone else doesn't count.
  - Pull requests Dokima didn't build, including a fork whose branch is named `try/issue-7`, sit beside Dokima's own pull request.
- **The plan changes `.github/workflows/agent.yml`.** That file is normally off limits, but the issue names its "Starting branch" step as the dead end to fix, so I accepted it. The pull request will wait for your approval on GitHub because it touches a workflow file.

**Two notes, neither blocking:**
- The ping on a pull request Dokima didn't build is only tested with the code owners passed in by the test. Reading them from CODEOWNERS by default is only tested on a Dokima pull request.
- The issue-card test needs no change to the off-limits `dokima/card.py`. The card reads its stage from `dokima/agent.py`, which is in scope.

The plan has no questions for you. The next step is your `/work`.
