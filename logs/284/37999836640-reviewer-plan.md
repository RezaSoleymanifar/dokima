# reviewer (plan) for #284

Run: https://github.com/dokima-dev/dokima/actions/runs/37999836640

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat open_blockers.json; wc -c issue.md plan.json in/*
```

> .:
> total 200
> drwxr-xr-x  3 runner runner   4096 Oct  9 22:33 .
> drwxrwxrwt 18 root   root     4096 Oct  9 22:33 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 22:33 in
> -rw-r--r--  1 runner runner 175861 Oct  9 22:33 issue.md
> -rw-r--r--  1 runner runner      2 Oct  9 22:33 open_blockers.json
> -rw-r--r--  1 runner runner     15 Oct  9 22:33 parent.json
> -rw-r--r--  1 runner runner   7128 Oct  9 22:33 plan.json
> 
> in:
> total 228
> drwxr-xr-x 2 runner runner 4096 Oct  9 22:33 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 22:33 ..
> -rw-r--r-- 1 runner runner 6602 Oct  9 22:33 01-planner.json
> -rw-r--r-- 1 runner runner 5347 Oct  9 22:33 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6398 Oct  9 22:33 03-planner.json
> -rw-r--r-- 1 runner runner 5011 Oct  9 22:33 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2132 Oct  9 22:33 05-worker.json
> -rw-r--r-- 1 runner runner 2668 Oct  9 22:33 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner  319 Oct  9 22:33 07-updater.json
> -rw-r--r-- 1 runner runner 7041 Oct  9 22:33 08-planner.json
> -rw-r--r-- 1 runner runner  319 Oct  9 22:33 09-updater.json
> -rw-r--r-- 1 runner runner 7037 Oct  9 22:33 10-planner.json
> -rw-r--r-- 1 runner runner  319 Oct  9 22:33 11-updater.json
> -rw-r--r-- 1 runner runner 7047 Oct  9 22:33 12-planner.json
> -rw-r--r-- 1 runner runner  319 Oct  9 22:33 13-updater.json
> -rw-r--r-- 1 runner runner 7053 Oct  9 22:33 14-planner.json
> -rw-r--r-- 1 runner runner  319 Oct  9 22:33 15-updater.json
> -rw-r--r-- 1 runner runner 6582 Oct  9 22:33 16-plann

`2. Bash`
```
cd /tmp/pack; cat plan.json; cat parent.json; echo; cat in/35-reviewer-plan.json; cat in/36-updater.json
```

> {
>  "kind": "user_story",
>  "summary": "The drift audit sets missing or wrong labels, board options and views back to what Dokima needs, and only reports app permissions and branch rules.",
>  "user_story": "Missing or wrong labels, board options and views come back by themselves, and the owner is only asked about what touches permissions or branch rules.",
>  "acceptance_criteria": [
>   {
>    "text": "A declared label, board option or view that is missing or wrong is set to the manifest's values. The Setup issue lists it as fixed. When nothing is left off, the Setup issue still lists the fixes, is not marked Needs you, and closes with the line saying nothing is off. A whole board field that is missing is never created: it is only listed as still off on the Setup issue, marked Needs you.",
>    "source": "https://github.com/dokima-dev/dokima/issues/284"
>   },
>   {
>    "text": "A difference in app permissions or branch rules is never changed by the audit. It is only read, and listed as still off on the Setup issue, marked Needs you.",
>    "source": "https://github.com/dokima-dev/dokima/issues/284"
>   },
>   {
>    "text": "A fix GitHub refuses stays on the Setup issue as still off, with GitHub's reason on its line, and the other fixes still happen.",
>    "source": "https://github.com/dokima-dev/dokima/issues/284"
>   },
>   {
>    "text": "Adding or fixing a board option keeps every other option with its id, name, color and description, and every card already set keeps its value.",
>    "source": "https:

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/34-planner.json'))['handback']; b=json.load(open('plan.json'))
for k in set(a)|set(b):
  if a.get(k)!=b.get(k): print('DIFF',k)
"; grep -n '^## \|^### \|^\*\*' issue.md | tail -40
```

> DIFF concerns
> 1353:### dokima-runtime on issue #284 (2026-10-09T21:15:57Z)
> 1358:**User story:** Missing or wrong labels, board options and views come back by themselves, and the owner is only asked about what touches permissions or branch rules.
> 1430:**Next:** The reviewer starts now.
> 1433:### dokima-runtime on issue #284 (2026-10-09T21:17:11Z)
> 1479:**Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 1482:### dokima-runtime on PR #323 (2026-10-09T21:18:25Z)
> 1486:### dokima-runtime on PR #323 (2026-10-09T21:39:45Z)
> 1490:### dokima-runtime on issue #284 (2026-10-09T21:39:47Z)
> 1505:**Next:** The planner starts now.
> 1508:### dokima-runtime on issue #284 (2026-10-09T21:40:01Z)
> 1513:**User story:** Missing or wrong labels, board options and views come back by themselves, and the owner is only asked about what touches permissions or branch rules.
> 1585:**Next:** The reviewer starts now.
> 1588:### dokima-runtime on issue #284 (2026-10-09T21:41:22Z)
> 1634:**Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 1637:### dokima-runtime on PR #323 (2026-10-09T21:42:35Z)
> 1641:### dokima-runtime on PR #323 (2026-10-09T21:45:41Z)
> 1645:### dokima-runtime on issue #284 (2026-10-09T21:45:43Z)
> 1660:**Next:** The planner starts now.
> 1663:### dokima-runtime on issue #284 (2026-10-09T21:45:57Z)
> 1668:**User story:** Missing or wrong labels, board options and views come back by themselves, and the owner is only 

`4. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md | grep -v dokima-runtime; sed -n 1951,1975p issue.md; sed -n 2057,2080p issue.md
```

> 243:### RezaSoleymanifar on issue #284 (2026-10-09T05:25:49Z)
> ### dokima-runtime on PR #323 (2026-10-09T22:03:53Z)
> 
> The plan of #284 is approved, but the plan check on b3b76ca could not run again: GitHub refused: gh: Resource not accessible by integration (HTTP 403). Re-run all its jobs once it can, so it reads the approved plan: https://github.com/dokima-dev/dokima/actions/runs/37968643310
> 
> ### dokima-runtime on PR #323 (2026-10-09T22:31:23Z)
> 
> This pull request could not be updated with `main` (b6d00ea). GitHub said: merge conflict between base and head
> 
> ### dokima-runtime on issue #284 (2026-10-09T22:31:25Z)
> 
> <!-- dokima-record -->
> Pull request #323 clashes with `main` since b6d00ea (#327) merged, so the planner re-plans against the new main. The files that clashed:
> 
> - `AGENTS.md`
> 
> <details><summary>Full record</summary>
> 
> (full record: in/36-updater.json)
> 
> </details>
> 
> <sub>Found by code, no model · [run](https://github.com/dokima-dev/dokima/actions/runs/37999658655)</sub>
> 
> **Next:** The planner starts now.
> 
> ### dokima-runtime on issue #284 (2026-10-09T22:33:09Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> **Reviewer (plan)** · setting up
> 
> The machine is setting up: the branch, the starting pack an

**Agent:** Only the concerns changed and no new owner words. Let me verify the planner's evidence and run the tests on main.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -2; git show --stat b6d00ea | tail -8; git log --oneline b3b76ca..origin/main -- AGENTS.md dokima/audit.py dokima/manifest.py tests/fake_gh.py tests/test_audit.py; git diff --stat origin/main HEAD -- tests/ | tail -5
```

> tests/raised_goldens/old-issue-card.md           |  33 ++
>  tests/raised_goldens/old-planner.md              | 122 +++++
>  tests/raised_goldens/old-review.md               | 123 +++++
>  tests/raised_goldens/old-worker.md               |  78 +++
>  tests/raised_goldens/rejected-issue-card.md      |  33 ++
>  tests/raised_goldens/rejected.md                 | 110 ++++
>  tests/test_raised_cards.py                       | 606 +++++++++++++++++++++++
>  14 files changed, 1359 insertions(+), 3 deletions(-)
> 7a2349e On autopilot, a blocked issue plans only after its blockers merge (reverses #253) (#360)
> 3ae65a6 A scan of the whole board and every card names anything that does not match its state (#361)
> 8b12495 AGENTS.md: every issue reference is a link plus a few plain words (#357)
> 5565fa5 Every 15 minutes, any card that does not match its issue's state is redrawn (#356)
> 28ccaf3 An approved plan waiting on a blocker stays in Plan; Work means it is being built (#348)
> 09881bd The board's column and pills are always computed from the issue's state right now (#339)
>  tests/test_raised_cards.py                       |  606 -------------
>  tests/test_scan.py                               |  671 --------------
>  tests/test_text_only.py                          |  233 -----
>  tests/test_work_column.py                        |  213 -----
>  36 files changed, 1368 insertions(+), 6042 deletions(-)

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat --format= b6d00ea | head -8; git log --format=%h b3b76ca..origin/main -- dokima/audit.py dokima/manifest.py tests/fake_gh.py tests/test_audit.py; echo ---; git show origin/main:AGENTS.md | grep -n "never edits\|drift audit"
```

> dokima/agent.py                                  |  43 +-
>  dokima/card.py                                   |  39 ++
>  tests/raised_goldens/cancelled.md                |  35 ++
>  tests/raised_goldens/clash.md                    |  31 ++
>  tests/raised_goldens/failing-tests-issue-card.md |  33 ++
>  tests/raised_goldens/merge-failed.md             |  38 ++
>  tests/raised_goldens/not-started.md              |  38 ++
>  tests/raised_goldens/old-issue-card.md           |  33 ++
> ---
> 21:**A stage never edits what another stage owns. It proposes, and the owner routes it with a command.**
> 91:- One Autopilot view, a table filtered to `label:autopilot is:open`, lists every open issue and pull request on autopilot; merged and closed ones keep the label but leave the view. Code adds it the first time a tree goes on autopilot, from the board run of the tree's top issue only, and a refused view fails that run naming it. The board run of a merge changes an Autopilot view still filtered to the old `label:autopilot` to `label:autopilot is:open`, leaves any other filter alone, and fails naming the view if GitHub refuses. The Autopilot option of the Action field is a one-time step on the board, like Needs you; code never edits the field's options.

**Agent:** Evidence holds. Now run the plan's tests on main.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/m && git worktree add -q /tmp/m origin/main 2>&1|tail -1; for f in tests/test_audit_fix.py tests/test_audit_fix_cli.py tests/test_audit.py tests/fake_gh.py; do cp $f /tmp/m/$f; done; cd /tmp/m && timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_audit_fix.py tests/test_audit_fix_cli.py tests/test_audit.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-220
```

> Proves 284.2. The faked app has issues: read and administration: write, main's rule lacks the all done-whens passed check, and
>                             ("main's rule", ("main", "all done-whens passed"))):
>         one_line(off, "284.2", "main's rule, still off", "main", "all done-whens passed")
> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_label_is_set_and_listed_as_fixed - AssertionError: 284.1: the plan label is None, not the manifest's {'color': '1d76db', 'description': 'Starts the planner'}
> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_board_option_is_set_and_listed_as_fixed - AssertionError: 284.1: the Autopilot option of Action is None, not the manifest's {'color': 'PURPLE', 'description': 'Ru
> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_view_is_set_and_listed_as_fixed - AssertionError: 284.1: the missing Autopilot view was not added as the manifest has it: None
> FAILED tests/test_audit_fix.py::test_a_run_that_fixes_everything_lists_the_fixes_and_closes_the_setup_issue - AssertionError: 284.1: the missing plan label was not created
> FAILED tests/test_audit_fix.py::test_a_missing_board_field_is_reported_not_created - AssertionError: 284.1: the missing Autopilot option should be listed as fixed, as 'Option `Autopilot` of the board field `Action` is mi
> FAILED tests/test_audit_fix.py::test_permissions_and_branch_rules_are_only_reported - AssertionError: 284.2: the plan label should be listed as fixed, as 'Label `plan` is missing; Dokima 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/m; mkdir -p /tmp/dokima-out; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/35-reviewer-plan.json'))['handback']
r={
 "previous_step":{
  "did":["The planner re-planned after pull request #323 clashed with main on AGENTS.md when #327 merged; the five criteria, the one non-functional rule and the 19 new tests are unchanged."],
  "decided":["The worker starts from main's AGENTS.md as it is, keeps every newer line, and replaces only the sentence saying the Autopilot option is a one-time step that code never edits.",
             "The issue stays blocked by #326."],
  "open":["The planner points out again that every merge to main starts another re-plan with nothing new while this issue waits on #326."]},
 "verdict":"approve",
 "summary":"The re-plan keeps the approved criteria and tests unchanged, every ask has a criterion, and all 19 new tests still fail on main for the right reason.",
 "blockers":[],
 "notes":[{"text":"#327 did not touch AGENTS.md or any file this plan changes, so this re-plan brings nothing new; the worker must still take main's AGENTS.md as it is and change only the Autopilot option sentence.",
  "evidence":"git show --stat b6d00ea lists dokima/agent.py, dokima/card.py, tests/raised_goldens/ and tests/test_raised_cards.py only; git log b3b76ca..origin/main -- dokima/audit.py dokima/manifest.py tests/fake_gh.py tests/test_audit.py is empty; main's AGENTS.md:91 still ends 'code never edits the field's options.' On main with the plan's test files: 19 failed, 15 passed, each failure naming its criterion."}],
 "resolved":[],
 "issues_found":prev["issues_found"],
 "asks":prev["asks"],
}
r["issues_found"][0]["why"]="Issue #284 has been re-planned and re-reviewed after each of #357, #360, #361, #362 and #327 with no change to its plan, spending a planner and a reviewer run each time and asking the owner again for /work."
r["issues_found"][0]["evidence"]="Updater records in
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r["summary"]="The re-plan keeps the approved criteria and tests, every ask has a criterion, and all 19 new tests still fail on main."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 284 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-plan for issue #284 and wrote the review to `/tmp/dokima-out/review.json`. Both hand-back checks pass.

- **What changed:** The planner re-planned because pull request #323 clashed with main on `AGENTS.md` after #327 merged. The only thing that differs from the last approved plan is its list of concerns. The five criteria, the one rule the audit must always follow (never delete, rename or touch undeclared settings) and the 19 new tests are all the same.
- **New owner comments:** None since the last review, and there were no open blockers to answer.
- **Tests on main:** I ran the plan's test files on current main. All 19 new tests fail, each naming its criterion and the missing feature, and the other 15 pass.
- **What #327 changed:** #327 didn't touch `AGENTS.md` or any file in this plan's scope. `AGENTS.md:91` on main still ends "code never edits the field's options." The note tells the worker to change only that sentence and keep everything else in main's `AGENTS.md`.
- **Repeat re-plans:** I'm proposing the same issue again. The updater keeps re-planning this approved, waiting issue on every merge to main, even when nothing the plan touches changed. That has now happened after #357, #360, #361, #362 and #327, costing a planner run and a reviewer run each time and asking you for `/work` again.

The issue is still blocked by #326, so this waits on that before any work starts.
