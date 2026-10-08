# reviewer (plan) for #210

Run: https://github.com/dokima-dev/dokima/actions/runs/37752726592

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (98.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tool-results/bej8wcx6h.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-worker.json
> 06-reviewer-pr.json
> 07-planner.json
> 08-reviewer-plan.json
> 09-not-started.json
> 10-planner.json
> 11-reviewer-plan.json
> 12-planner.json
> # Issue #210: Autopilot: the owner sees on the board and on every card what is on autopilot
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #219](https://github.com/dokima-dev/dokima/pull/219) · [files changed](https://github.com/dokima-dev/dokima/pull/219/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37747784556/job/113213305579)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 2</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** The owner sees at a glance what runs on autopilot: an Autopilot pill on every card in the tree, the usual Ne

`2. Bash`
```
cd /tmp/pack; cat issue.md | head -c 40000
```

> <persisted-output>
> Output too large (39.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tool-results/brpocc49n.txt
> 
> Preview (first 2KB):
> # Issue #210: Autopilot: the owner sees on the board and on every card what is on autopilot
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #219](https://github.com/dokima-dev/dokima/pull/219) · [files changed](https://github.com/dokima-dev/dokima/pull/219/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37747784556/job/113213305579)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 2</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** The owner sees at a glance what runs on autopilot: an Autopilot pill on every card in the tree, the usual Needs you pill in its place where autopilot stopped for them, and one table view listing it all.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []{
>  "kind": "user_story",
>  "user_story": "The owner sees at a glance what runs on autopilot: an Autopilot pill on every card in the tree, the usual Needs you pill in its place where autopilot stopped for them, and one Autopilot table view listing it all.",
>  "acceptance_criteria": [
>   {
>    "text": "Every card of an issue on autopilot, and of the open pull request built for it, shows an Autopilot pill on the board: it appears when the issue goes on autopilot, stays when the board or the river moves the card to another stage, and is gone once the issue goes off autopilot. Cards of issues not on autopilot never show it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/210"
>   },
>   {
>    "text": "Stories filed by a split under a parent on autopilot carry the autopilot label and land in Backlog with the Autopilot pill, and the parent shows Autopilot in Work; stories of a parent not on autopilot get neither.",
>    "source": "https://github.com/dokima-dev/dokima/issues/210"
>   },
>   {
>    "text": "When the river stops for the owner on an issue on autopilot, its card and its pull request's card show the existing Needs you pill and no Autopilot pill, and show Autopilot again once the river goes on. Switching autopilot on or off while a card shows Needs you leaves Needs you in place, so no card ever shows both or loses Needs you.",
>    "source": "https://github.com/dokima-dev/dokima/issues/210"
>   },
>   {
>    "text": "The board has one Autopilot view, laid out as a table and filtered 

`4. Bash`
```
cd /tmp/pack; sed -n '1,400p' issue.md | tail -n +30
```

> - The board has an Autopilot view laid out as a table, like the Needs you view, listing every issue and pull request on autopilot and nothing else. ([source](https://github.com/dokima-dev/dokima/issues/205))
> 
> **Non-functional:**
> - In a repo without a board, autopilot still switches on and off and nothing fails. (The board is an optional extra.)
> 
> </details>
> 
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #210 (2026-10-08T06:58:13Z)
> 
> /plan
> 
> ### dokima-runtime on issue #210 (2026-10-08T06:58:34Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**
> 
> The owner sees at a glance what runs on autopilot: an Autopilot pill on every card in the tree, the usual Needs you pill in its place where autopilot stopped for them, and one Autopilot table view listing it all.
> 
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - The Autopilot pill needs an Autopilot option on the board's Action field, next to Needs you. GitHub's API can only replace all of a field's options at once, which risks wiping every card's Needs you. Is adding that one option by hand on the board, once, fine with you? Assumed: The plan assumes yes: you add the Autopilot option to the Action field once; where it is missing, cards simply show no Autopilot pill and nothing fails.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {

`5. Bash`
```
cd /tmp/pack; sed -n '14,32p' issue.md; grep -n "^### " issue.md
```

> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 2</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** The owner sees at a glance what runs on autopilot: an Autopilot pill on every card in the tree, the usual Needs you pill in its place where autopilot stopped for them, and one table view listing it all.
> 
> **Context:** Asked by the owner on 2026-10-08 06:24 and corrected at 06:25 (https://github.com/dokima-dev/dokima/issues/205): no separate Autopilot needs you pill, no On autopilot from #N line, and the view is a table like the Needs you view. The board is kept by dokima/board.py (sync, decide, priority) from .github/workflows/board.yml; today the single-select Action field holds 'Needs you' (board.py sync sets it or clears it) and the Priority pill follows a label (#206). A simple way to keep Autopilot and Needs you off the same card: make Autopilot another option of the same single-select Action field, set to 'Needs you' when the river stops for the owner and to 'Autopilot' otherwise while the issue carries the `autopilot` label from story 1, so a card can never hold both. Children filed later by a split (file_split in dokima/agent.py) under a parent on autopilot must get the label and the pill too. The view: check whether GitHub's API can create a project view; if it cannot, the vi

`6. Bash`
```
cd /tmp/pack; for l in 577 982 1020 1291 1295; do sed -n "${l},$((l+4))p" issue.md; done; sed -n 636,700p issue.md; sed -n 986,1019p issue.md
```

> ### RezaSoleymanifar on issue #210 (2026-10-08T07:35:54Z)
> 
> /work
> 
> ### dokima-runtime on issue #210 (2026-10-08T07:36:15Z)
> ### RezaSoleymanifar on issue #210 (2026-10-08T08:24:59Z)
> 
> /work
> 
> ### dokima-runtime on PR #219 (2026-10-08T08:25:25Z)
> ### RezaSoleymanifar on issue #210 (2026-10-08T08:30:26Z)
> 
> /plan The PR clashes with main after #213 merged. Re-plan on top of today's main.
> 
> ### dokima-runtime on issue #210 (2026-10-08T08:30:48Z)
> ### dokima-runtime on PR #219 (2026-10-08T08:47:41Z)
> 
> Replaced: this branch conflicts with main after #213 merged. Re-planning #210 from fresh main, as done for #154.
> 
> ### RezaSoleymanifar on issue #210 (2026-10-08T08:47:45Z)
> ### RezaSoleymanifar on issue #210 (2026-10-08T08:47:45Z)
> 
> /plan Fresh start on today's main: the old branch is deleted because it conflicted after #213 merged.
> 
> ### dokima-runtime on issue #210 (2026-10-08T08:48:06Z)
> ### dokima-runtime on PR #219 (2026-10-08T07:43:10Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (pr)**
> 
> **block**: The pills, labels and split all work as planned, but switching a whole tree on autopilot at once can add the Autopilot view several times, and the plan's only test switches issues on one after another, so it cannot see this.
> - **B1** (210.4, the planner fixes it): The plan promises the Autopilot view is never added twice, but the code only checks for the view a

**Agent:** Reading the newest review and the planner's latest run, then running the tests.

`7. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['08-reviewer-plan.json','11-reviewer-plan.json','12-planner.json']:
  d=json.load(open(f)); h=d.get('handback',d)
  print(f, json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','resolved','notes','replies','concerns','questions','test_changes']},indent=1)[:5000]); print(d.get('check'))
"
```

> 08-reviewer-plan.json {
>  "verdict": "approve",
>  "summary": "The plan now proves that switching a whole tree on autopilot adds the Autopilot view exactly once even when its board runs overlap, and the new test turns red on today's code for exactly that reason.",
>  "blockers": [],
>  "resolved": [
>   "B1"
>  ],
>  "notes": [
>   {
>    "text": "The only duplicate left is two /autopilot start commands on unrelated trees given within seconds of each other before the board has an Autopilot view; the plan names this openly as out of scope, and it can happen only once per board.",
>    "evidence": "plan.json out_of_scope, last line; .github/workflows/board.yml groups runs per issue number, so runs for different issues are not queued."
>   },
>   {
>    "text": "The three new tests fail today because the board has no way to read an issue's parent yet. In a scratch copy, adding just that read to today's code turned the overlap test red on the right reason (three extra create-view calls from the sub-issues' runs), and adding the top-of-tree rule turned all twenty autopilot tests green with no other test changing.",
>    "evidence": "pytest -q tests/test_autopilot_board.py on try/issue-210: 3 failed ('210.4: the real Board has no parent yet'), 17 passed. Scratch copy with Board.parent only: 'AssertionError: 210.4: a sub-issue whose parent is on autopilot added the Autopilot view: [3 POST .../views]'. With the rule added: the same failures as the untouched branch outside this file (test_cancelled_run, test_fi

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 origin/main 2>/dev/null; git diff --stat main..HEAD; git merge-base --is-ancestor origin/main HEAD && echo up-to-date; timeout 600 python -m pytest -q tests/test_autopilot_board.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | head -40
```

> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> 4cccffe Live card: minutes and the current step while the agent works (#216)
>  tests/test_autopilot_board.py | 796 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_board.py           |   7 +-
>  tests/test_failed_run_card.py |   9 +-
>  3 files changed, 809 insertions(+), 3 deletions(-)
> up-to-date
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_on_puts_the_pill_on_the_issue_and_its_pull_request - AssertionError: 210.1: issue #57 on autopilot shows None, not the Autopilot pill
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_off_takes_the_pill_away - AssertionError: 210.1: issue #57 off autopilot still shows 'Autopilot'
> FAILED tests/test_autopilot_board.py::test_stage_moments_keep_the_pill_on_issues_on_autopilot_only - AssertionError: 210.1: #57 on autopilot moved to Work shows None, not Autopilot
> FAILED tests/test_autopilot_board.py::test_the_river_keeps_the_pill_when_it_moves_a_card_on_autopilot - AssertionError: 210.1: the river moved issue #57, on autopilot, and it shows None, not Autopilot
> FAILED tests/test_autopilot_board.py::test_a_split_under_a_parent_on_autopilot_files_children_on_autopilot - AssertionError: 210.2: story #201 landed as 'Backlog' with None, not Backlog with Autopilot
> FAILED tests/test_autopilot_board.py::test_needs_you_r

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | grep -v test_autopilot_board; git stash list | head -1; git checkout -q main 2>/dev/null && timeout 900 python -m pytest -q -x -p no:cacheprovider 2>&1 | tail -3; git checkout -q try/issue-210
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bm6bpilwp). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bm6bpilwp.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile I'll read the test file from the branch.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git show try/issue-210:tests/test_autopilot_board.py | sed -n 1,200p
```

> """The board shows what runs on autopilot: an Autopilot pill, Needs you in its place when the river stops, one view (#210).
> 
> The first ten tests fake dokima.board.Board itself, so they read the board's end state, never the GraphQL queries
> that reach it. The tests at the end run the real Board against a faked GitHub, so the new reads and writes below truly
> reach GitHub. The fake keeps, in memory, one world shared with a fake `gh`:
> 
> - cards: each card's Status and Action (the single-select field holding "Needs you" and now "Autopilot");
> - labels: the labels each issue and pull request carries; `autopilot` is autopilot's state (story 1, #209);
> - the open pull request of each issue (branch try/issue-N, body "Closes #N");
> - the parent issue of each sub-issue;
> - the board's views by name.
> 
> What the fake Board offers, and the code is expected to use:
>     Board(spec, repo, q)               the board, as today
>     .fields                            {"Status": (id, {option: id}), "Action": (id, {option: id})}, as today
>     .item(kind, n) -> item id          as today; kind is "issue" or "pr"
>     .set(item, field, option or None)  as today: an unknown field or option is ignored, None clears
>     .value(item, field) -> option      the card's current option of that field, or None
>     .autopilot(kind, n) -> bool        whether that issue or pull request carries the `autopilot` label
>     .open_pr(n) -> number or None      the open pull request built for issue n
>     .parent(n) -> number or Non

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main..try/issue-210 -- tests/test_board.py tests/test_failed_run_card.py
```

> diff --git a/tests/test_board.py b/tests/test_board.py
> index 3696ed0..9aa3bc3 100644
> --- a/tests/test_board.py
> +++ b/tests/test_board.py
> @@ -56,7 +56,12 @@ class FakeGitHub:
>          if query.startswith("query") and "repository" in query:
>              kind = "issue" if "issue(" in query else "pullRequest"
>              items = [{"id": "ITEM", "project": {"id": "P"}}] if self.on_board else []
> -            return {"repository": {kind: {"id": "C", "projectItems": {"nodes": items}}}}
> +            # The issue or PR carries no labels and has no open PR, as GitHub answers for them (#210).
> +            return {"repository": {kind: {"id": "C", "projectItems": {"nodes": items}, "labels": {"nodes": []}},
> +                                   "pullRequests": {"nodes": []}}}
> +        if query.startswith("query") and "node(" in query:
> +            # The card has no Action pill yet, as GitHub answers for it (#210).
> +            return {"node": {"fieldValueByName": None, "fieldValues": {"nodes": []}}}
>          if "addProjectV2ItemById" in query:
>              return {"addProjectV2ItemById": {"item": {"id": "NEW"}}}
>          return {}
> diff --git a/tests/test_failed_run_card.py b/tests/test_failed_run_card.py
> index e4a103a..efa4353 100644
> --- a/tests/test_failed_run_card.py
> +++ b/tests/test_failed_run_card.py
> @@ -36,10 +36,15 @@ if a[:2] == ["api", "graphql"]:
>          data = {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
>              {"id": "S", "name": "Status", "options": [{"i

**Agent:** Fine: no assertions changed. Waiting on the full suite.

`12. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bm6bpilwp.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bm6bpilwp.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned on today's main, as the owner asked: the branch is now main plus one commit that adds only the plan's tests.",
          "The planner kept the same four criteria, the board-free rule and the 20 tests, and kept main's labelling of a split's stories, adding only the Autopilot pill for them and their parent.",
          "The planner taught the fakes in five existing board tests to answer the board's new reads with no labels, no pull request and no pill; no assertion changed."],
  "decided": ["Two /autopilot start commands on unrelated trees within seconds, on a board with no Autopilot view yet, may still add two views; this stays out of scope."],
  "open": []},
 "verdict": "approve",
 "summary": "The re-plan on today's main holds: the branch no longer clashes with main, all 20 new tests fail there only because the feature is missing, and the five touched board tests still pass with no assertion changed.",
 "blockers": [],
 "notes": [
  {"text": "The clash with main that stopped /work last time is gone: try/issue-210 now sits on main (#218) with only the plan's tests on top.",
   "evidence": "git merge-base --is-ancestor origin/main HEAD succeeds; git diff --stat main..HEAD lists only tests/test_autopilot_board.py, tests/test_board.py and tests/test_failed_run_card.py."},
  {"text": "Every one of the 20 plan tests fails today naming its criterion because the feature is missing, for example '210.1: issue #57 on autopilot shows None, not the Autopilot pill' and '210.4: the real Board takes no rest= call yet'.",
   "evidence": "pytest -q tests/test_autopilot_board.py on try/issue-210: 20 failed in 0.60s."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "an Autopilot pill on every card in the tree", "source": "https://github.com/dokima-dev/dokima/issues/210", "criterion": "210.1"},
  {"ask": "the pill is gone once the issue is off autopil
```

> (Bash completed with no output)

`14. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json;p='review.json';d=json.load(open(p));d['asks']=d['asks'][:-1];json.dump(d,open(p,'w'),indent=1)
EOF
```

> Shell cwd was reset to /home/runner/work/dokima/dokima

`15. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`16. Bash`
```
f=/tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bm6bpilwp.output; until [ "$(cd /home/runner/work/dokima/dokima && git branch --show-current)" = try/issue-210 ] && grep -qE "passed|failed|error" $f && [ $(grep -cE " in [0-9.]+s" $f) -ge 2 ]; do sleep 3; done; cat $f
```

> Command running in background with ID: bo8dvydog. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bo8dvydog.output. You will be notified when it completes. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** I'm waiting for the full test suite to finish on the branch and on main.

`17. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/8d85e951-8fd1-4acc-b20c-ef464b635d99/tasks/bm6bpilwp.output; cd /home/runner/work/dokima/dokima; git branch --show-current; git status --short
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
> 23 failed, 368 passed in 148.40s (0:02:28)
>     )
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 162 passed in 45.89s
> 
> [exited with code 0]
> try/issue-210

`18. Bash`
```
cd /tmp && rm -rf mainwt && git -C /home/runner/work/dokima/dokima worktree add -q /tmp/mainwt main 2>&1 | tail -1; cd /tmp/mainwt && timeout 300 python -m pytest -q -p no:cacheprovider tests/test_fixer.py tests/test_handback_check.py tests/test_board.py tests/test_failed_run_card.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-120; cd /tmp; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/mainwt
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review 
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionErro
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionErro
> 3 failed, 28 passed in 10.06s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The 3 other failures happen on untouched main too. Updating the note and running the check.

`19. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json;p='review.json';d=json.load(open(p))
d['notes'][1]['evidence']+=" Full suite on the branch: 23 failed, 368 passed; the 3 others (test_fixer::test_every_review_blocker_names_the_worker_or_the_planner, two in test_handback_check.py) fail the same way on untouched main, and the five changed tests in test_board.py and test_failed_run_card.py pass."
json.dump(d,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 210 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

`20. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json;p='review.json';d=json.load(open(p))
d['issues_found']=[{"title":"Main is red: three hand-back check tests reject reviews that list no asks",
 "why":"Every pull request's full suite fails on these three tests whatever its work, so a red suite no longer says anything about the change.",
 "evidence":"On main (f1b30ab): pytest -q tests/test_fixer.py tests/test_handback_check.py -> 3 failed: test_every_review_blocker_names_the_worker_or_the_planner and test_well_formed_hand_backs_pass_and_every_malformed_field_is_named ('asks must list every ask in the owner's issue and comments'), test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests."}]
json.dump(d,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 210 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #210 and wrote the review to `/tmp/dokima-out/review.json`. It passes both hand-back checks.

- **Re-planned on today's main, as the owner asked:** the branch is now main (including #218) plus one commit, and that commit contains only the plan's tests. The clash that stopped `/work` last time is gone.
- **The plan itself is unchanged:** the same four criteria, the rule that autopilot still works without a board, and the same 20 tests. Labelling a split's stories was already added to main in #218 and is kept as it is; the split test now only checks for the Autopilot pill.
- **All 20 new tests fail today, and only because the feature isn't built yet.** Each failure names its criterion, for example `210.1: issue #57 on autopilot shows None, not the Autopilot pill`.
- **Existing tests:** the planner edited five of them only so their fake GitHub answers the board's new reads with "no labels, no pull request, no pill". No assertion changed, and all five pass.
- **Full suite on the branch:** 368 passed and 23 failed. That is the 20 plan tests plus 3 hand-back check tests in `tests/test_fixer.py` and `tests/test_handback_check.py`, which fail the same way on main without the branch.
- **Every ask from the owner** matches a criterion; none is missing. There were no open blockers to carry over.

**Proposed new issue:** main is red because those 3 tests reject reviews that list no asks. Every pull request's full suite fails on them whatever its work, so a red suite says nothing about the change. It stays a proposal until the owner files it.
