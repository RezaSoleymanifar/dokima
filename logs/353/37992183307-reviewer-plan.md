# reviewer (plan) for #353

Run: https://github.com/dokima-dev/dokima/actions/runs/37992183307

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #353: On autopilot, a blocked issue plans only after its blockers merge (reverses #253)
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #353](https://github.com/dokima-dev/dokima/issues/353)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> On autopilot, a blocked issue does not get a plan until every issue blocking it has merged. This reverses #253 (PR #296), where a blocked issue planned early and only its build waited.
> 
> Owner's words (2026-10-09): "Yes, don't plan a blocked issue until its blockers merge. And it, I think, honestly, default was that way. I ch

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -20; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> commit 7f3ac14e8aa6fded6d24140df6bcc496eddba0be
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 21:13:56 2026 +0000
> 
>     planner for #353 (run 37991030499)
> 
>  tests/test_blocked_worker.py | 300 +++++++++++++++++++++++--------------------
>  tests/test_work_column.py    |  72 +++++------
>  2 files changed, 194 insertions(+), 178 deletions(-)
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37991030499",
>  "commit_before": "c16b878087f2d2822a08ec3cb6ec7d85c072fc54",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 1622,
>   "turns": 1,
>   "cost_usd": 2.675190000000001,
>   "tokens_in": 147730,
>   "tokens_out": 91
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/353/37991030499-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37991030499",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 pytest -q -p no:cacheprovider tests/test_blocked_worker.py tests/test_work_column.py tests/test_autopilot_start.py tests/test_autopilot_close.py 2>&1 | tail -40
```

> tests/test_work_column.py:211: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> board: issue #57 -> Work · Autopilot
> =========================== short test summary info ============================
> FAILED tests/test_blocked_worker.py::test_an_approved_plan_with_an_open_blocker_builds_nothing_and_says_what_it_waits_for - AssertionError: 353.2: #253's waiting-worker lines were posted: ['Autopilot: plan approved, waiting for #301 and #304 to close']
> assert ['Autopilot: ...304 to close'] == []
>   
>   Left contains one more item: 'Autopilot: plan approved, waiting for #301 and #304 to close'
>   
>   Full diff:
>   - []
>   + [
>   +     'Autopilot: plan approved, waiting for #301 and #304 to close',
>   + ]
> FAILED tests/test_blocked_worker.py::test_the_last_blocker_closing_starts_a_fresh_plan_never_the_old_plans_worker - AssertionError: 353.3 (last blocker closed): #57's worker started on its old plan, though only a fresh plan may follow
> assert 1 == 0
>  +  where 1 = workers(<test_autopilot_close.Repo object at 0x7ffa68c7a840>, '353.3')
> FAILED tests/test_blocked_worker.py::test_a_command_the_owner_types_while_it_waits_runs_and_no_close_overrides_it - AssertionError: 353.3 (the owner said /plan): #57's worker started, though nothing may start
> assert 1 == 0
>  +  where 1 = workers(<test_autopilot_close.Repo object at 0x7ffa68b4c410>, '353.3')
> FAILED tests/test_blocked_worker.py::test_a_close_that_cannot_list_the_blockers_starts_nothing_and_says_why - As

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 pytest -q -p no:cacheprovider -rs tests/test_blocked_worker.py tests/test_work_column.py tests/test_autopilot_start.py tests/test_autopilot_close.py -v 2>&1 | grep -E "PASS|SKIP|FAIL" | head -40
```

> =================================== FAILURES ===================================
> SKIPPED [4] tests/test_autopilot_start.py: slow, parked until the test-speed issue
> SKIPPED [11] tests/test_autopilot_close.py: slow, parked until the test-speed issue

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "parked\|skip" tests/test_autopilot_start.py tests/test_autopilot_close.py tests/conftest.py 2>/dev/null | head; grep -rn "slow, parked" --include=*.py --include=*.yml --include=*.toml --include=*.ini --include=*.cfg . | head
```

> tests/conftest.py:1:"""Temporary: skip the slow tests (each 1 second or more) so the suite runs in about a minute.
> tests/conftest.py:5:The parked test-speed issue makes the rest fast and deletes this file. DOKIMA_ALL_TESTS=1 runs everything.
> tests/conftest.py:68:    "test_new_test_check.py::test_a_new_test_that_passes_or_skips_today_is_rejected_saying_so[marked",
> tests/conftest.py:69:    "test_new_test_check.py::test_a_new_test_that_passes_or_skips_today_is_rejected_saying_so[passes]",
> tests/conftest.py:70:    "test_new_test_check.py::test_a_new_test_that_passes_or_skips_today_is_rejected_saying_so[skips",
> tests/conftest.py:116:    skip = pytest.mark.skip(reason="slow, parked until the test-speed issue")
> tests/conftest.py:119:            item.add_marker(skip)
> tests/test_autopilot_close.py:330:        Returns the names of the jobs that ran (were not skipped). Every job that changed something on GitHub (sent a
> tests/test_autopilot_close.py:358:                        results[name] = "skipped"
> tests/conftest.py:116:    skip = pytest.mark.skip(reason="slow, parked until the test-speed issue")

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,30p tests/conftest.py; sed -n 100,125p tests/conftest.py; grep -n "autopilot_start\|autopilot_close\|blocked_worker\|work_column" tests/conftest.py; grep -rn "DOKIMA_ALL_TESTS" .github dokima | head
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
>     "test_automerge.py::test_a_refused_merge_stops_for_the_owner_and_says_why",
>     "test_automerge.py::test_autopilot_start_merges_a_pull_request_already_approved",
>     "test_automerge.py::test_autopilot_start_merges_the_approved_pull_requests_of_the_whole_tree",
>     "test_automerge.py::test_nothing_merges_unless_every_check_on_the_merging_commit_is_green",
>     "test_automerge.py::test_on_autopilot_an_approved_pull_request_with_green_checks_merges_and_says_so",
>     "test_automerge.py::test_without_autopilot_an_approved_pull_request_waits_for_the_owner",
>     "test_autopilot.py::test_autopilot_start_puts_the_issue_and_every_sub_issue_at_every_level_on_autopilot",
>     "test_autopilot.py::test_autopilot_starts_no_stage_and_says_which_issues_it_switched",
>     "test_autopilot.py::test_autopilot_stop_takes_the_same_tree_off_autopilot",
>     "test_autopilot.py::test_only_a_code_owners_autopilot_counts",
>     "test_autopilot_close.py::test_a_child_planned_runn

**Agent:** Round one of the plan review. Most of the new tests fail today for the right reason. Now I'm checking whether the tests for criterion 1 actually run in CI, since the default suite skips them as slow.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "DOKIMA_ALL_TESTS\|pytest" .github/workflows | head; DOKIMA_ALL_TESTS=1 timeout 600 pytest -q -p no:cacheprovider tests/test_autopilot_start.py::test_autopilot_start_never_starts_the_issue_itself_where_it_must_not tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged tests/test_autopilot_close.py::test_a_split_filed_on_autopilot_starts_its_unblocked_stories 2>&1 | tail -3
```

> .github/workflows/full-suite.yml:24:      - run: pip install -q pytest
> .github/workflows/full-suite.yml:25:      - run: pytest -q -p no:cacheprovider tests
> .github/workflows/planner.yml:60:      - name: Install pytest and Claude Code
> .github/workflows/planner.yml:62:        run: pip install pytest && npm install -g @anthropic-ai/claude-code
> .github/workflows/done-whens.yml:46:      - run: pip install -q pytest
> .github/workflows/done-whens.yml:54:          pytest -rA -p no:cacheprovider -o junit_family=xunit1 --junitxml=r.xml $TESTS
> .github/workflows/agent.yml:177:      - name: Install pytest and Claude Code
> .github/workflows/agent.yml:180:          { pip install pytest && npm install -g @anthropic-ai/claude-code; } 2>&1 | tee /tmp/install.txt \
> .github/workflows/agent.yml:181:            || { echo "The step 'Install pytest and Claude Code' failed: $(tail -3 /tmp/install.txt | paste -sd' ')" > /tmp/why.txt; exit 1; }
> .github/workflows/agent.yml:185:          PYTHONPATH= PYTHONSAFEPATH= python3 -m pytest -q -rA --junitxml="$PACK/tests.xml" > "$PACK/tests.txt" 2>&1 || true
> ...                                                                      [100%]
> 3 passed in 6.20s

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 30,80p .github/workflows/done-whens.yml
```

> fail-fast: false
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
>           RESULT: ${{ needs.check.result }}
>         run: |
>           if [ -z "$MATRIX" ] || [ "$MATRIX" = "[]" ]; then
>      

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "skip" dokima/checks.py | head -20
```

> (Bash completed with no output)

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_blocked_worker.py | grep "^+" | head -300
```

> +++ b/tests/test_blocked_worker.py
> +"""On autopilot, a blocked issue plans only after its blockers merge (#353, which reverses #253).
> +Before #353 a blocked issue on autopilot planned early, and its approved plan waited for its blockers with the bot's
> +line `Autopilot: plan approved, waiting for #A to close`; when they closed, its worker built that old plan, with
> +`Autopilot: blockers closed, starting work`. A plan written while its blockers are still open goes stale when they
> +merge, so now nothing waits with an approved plan. Each moment runs the real code against a fake GitHub:
> +  autopilot that GitHub still has blocked by an open issue builds nothing: no worker starts, no line stands in for
> +  `/work`, and the card's Next line names the open issues it waits for and says it plans again, mentioning no one.
> +  there). When the last open blocker of such an issue closes, autopilot starts a fresh planner run once, with
> +  `Autopilot: blockers merged, starting plan`, and never the worker of the old plan.
> +- A command the owner types by hand runs as today, through commands.yml, and a later close never overrides it.
> +Where GitHub cannot list an issue's blockers, the fake answers that read with "HTTP 502: Server Error" and nothing
> +may start, with GitHub's reason on the issue.
> +OLD_WAIT = "Autopilot: plan approved, waiting for"
> +OLD_GO = "Autopilot: blockers closed, starting work"
> +LINE = "Autopilot: blockers merged, starting plan"
> +def old_lines(said):
> +    """The lines #253 poste

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git show 28ccaf3 --stat; git show 28ccaf3 -- dokima/ | head -80
```

> commit 28ccaf37553659a8dfb29b807f13895dfe1d6e7f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 14:18:44 2026 -0500
> 
>     An approved plan waiting on a blocker stays in Plan; Work means it is being built (#348)
>     
>     * planner for #343 (run 37971113495)
>     
>     * planner for #343 (run 37975290781)
>     
>     * worker for #343 (run 37978005258)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
> 
>  AGENTS.md                 |   2 +-
>  dokima/agent.py           |  16 ++--
>  dokima/board.py           |  10 +--
>  tests/test_board_state.py |   6 +-
>  tests/test_work_column.py | 221 ++++++++++++++++++++++++++++++++++++++++++++++
>  5 files changed, 241 insertions(+), 14 deletions(-)
> commit 28ccaf37553659a8dfb29b807f13895dfe1d6e7f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 14:18:44 2026 -0500
> 
>     An approved plan waiting on a blocker stays in Plan; Work means it is being built (#348)
>     
>     * planner for #343 (run 37971113495)
>     
>     * planner for #343 (run 37975290781)
>     
>     * worker for #343 (run 37978005258)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
> 
> diff --git a/dokima/agent.py b/dokima/agent.py
> ind

`12. Bash`
```
cd /home/runner/work/dokima/dokima; git show 28ccaf3 -- AGENTS.md | grep "^[-+]" | cut -c1-900
```

> --- a/AGENTS.md
> +++ b/AGENTS.md
> -- Columns are stages: Backlog, Plan, Work, Review, Done. Every new item lands in Backlog. Each card's column and pill are computed from its issue's state on GitHub now, never from the event that started the board run: every event about an issue or its pull request and the end of every run that did not fail put both cards there, so the next event fixes a dropped or late one, and an issue and its pull requests share one board queue that keeps the newest recompute. An open issue with no record is in Backlog, otherwise in the column the river placed it in after its newest record, and an open pull request goes with its issue. A closed issue, and a merged or closed pull request, sits in Done with no pill, whatever its labels. Every 15 minutes a sweep rechecks the issues and pull requests updated since the last sweep that succeeded, each with its pull request or issue, and every card when GitH
> +- Columns are stages: Backlog, Plan, Work, Review, Done. Every new item lands in Backlog. Each card's column and pill are computed from its issue's state on GitHub now, never from the event that started the board run: every event about an issue or its pull request and the end of every run that did not fail put both cards there, so the next event fixes a dropped or late one, and an issue and its pull requests share one board queue that keeps the newest recompute. An open issue with no record is in Backlog. Otherwise it is in the column of the newest stage start

**Agent:** I'm writing the review now. Criterion 1's three tests are all on the skip list for slow tests in `tests/conftest.py`, so the per-criterion check would pass on a skip. I'm blocking on that.

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned four criteria: a blocked issue on autopilot never starts its planner by itself, a plan approved while blocked builds nothing, the last blocker closing starts a fresh plan, and #253's waiting-worker code and wording are gone.",
          "Wrote new tests for criteria 2 to 5, deleted six #253 and #343 tests, and changed two board tests."],
  "decided": ["A plan approved while blocked waits in Plan, with a Next line that names its open blockers, mentions no one and shows no Needs you.",
              "The board's general rule that an approved plan stays in Plan until its worker starts is kept; only the blocked-plan clause of #343 goes."],
  "open": ["Recommends closing #313 as replaced by #353, since it asks for the opposite."]},
 "verdict": "block",
 "summary": "The plan follows the owner's ask, but criterion 1's three tests are all on the skip list for slow tests, so its check would pass without running anything.",
 "blockers": [{"id": "B1", "criterion": "353.1", "test": "tests/test_autopilot_start.py::test_autopilot_start_never_starts_the_issue_itself_where_it_must_not",
   "problem": "All three tests named for 353.1 are skipped in every normal run, including the per-criterion check (done-whens.yml runs plain pytest). A skipped test counts as passed, so a worker that breaks 'a blocked issue never starts its planner' while removing #253's code (for example, the waiting branch in main or start_blocked_workers in the close path) would still get a green 353.1.",
   "evidence": "tests/conftest.py SLOW lists test_autopilot_start.py::test_autopilot_start_never_starts_the_issue_itself_where_it_must_not (line 42), test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged (line 26) and test_a_split_filed_on_autopilot_starts_its_unblocked_stories (line 28). `pytest -q tests/test_autopilot_start.py tests/test_autopilot_close.py` shows them a
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan follows the owner's ask, but criterion 1's tests are all skipped as slow, so its check passes without running them."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 353 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #353 on one problem with its tests. The plan itself matches what you asked for, and the review is in `/tmp/dokima-out/review.json`, which passes both hand-back checks.

**Blocker B1, for the planner (criterion 1):** criterion 1's three tests never actually run. All three are on the slow-test skip list in `tests/conftest.py`. The check that proves each criterion (`done-whens.yml`) doesn't turn that list off, and a skipped test counts as passed. So criterion 1 ("an issue with an open blocker never starts its planner by itself") would show green with nothing checked. That matters here because removing #253's code touches the same paths and could break it. The three tests do pass when run with the full suite turned on. The fix is to take them off the skip list or add a fast test that covers all three moments: autopilot switched on, a split filed, and a close that leaves a blocker open.

**What I checked:**
- Every one of your asks maps to a criterion; none is missing.
- The seven new tests for criteria 2 to 5 all fail today for the right reason. For example, the waiting line is still posted, the old plan's worker still starts, #253's code is still there, AGENTS.md doesn't state the new rule yet, and the old "blockers closed" line still moves a card to Work.

**Notes, not blockers:**
- The issue says the blocked issue "stops after plan review". The plan reads that as waiting on its blockers, with no Needs you and no mention of you. That fits "the card says it waits for those issues", but you may want to confirm it.
- #348 changed two things: a general rule that an approved plan stays in Plan until its worker starts, and a clause for the blocked case. The plan removes only the blocked clause and keeps the general rule, and says so in its Out of scope section.

**Proposed new issue:** the per-criterion check accepts skipped tests as proof. This isn't specific to #353: any criterion whose tests are all on the skip list passes without running anything.
