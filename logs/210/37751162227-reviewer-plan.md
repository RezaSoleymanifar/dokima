# reviewer (plan) for #210

Run: https://github.com/dokima-dev/dokima/actions/runs/37751162227

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (74.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tool-results/bg223bq1j.txt
> 
> Preview (first 2KB):
> .:
> total 104
> drwxr-xr-x  3 runner runner  4096 Oct  8 08:38 .
> drwxrwxrwt 18 root   root    4096 Oct  8 08:38 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 08:38 in
> -rw-r--r--  1 runner runner 75336 Oct  8 08:38 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 08:38 open_blockers.json
> -rw-r--r--  1 runner runner  9203 Oct  8 08:38 plan.json
> 
> in:
> total 92
> drwxr-xr-x 2 runner runner 4096 Oct  8 08:38 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 08:38 ..
> -rw-r--r-- 1 runner runner 5134 Oct  8 08:38 01-planner.json
> -rw-r--r-- 1 runner runner 6513 Oct  8 08:38 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8429 Oct  8 08:38 03-planner.json
> -rw-r--r-- 1 runner runner 5210 Oct  8 08:38 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2678 Oct  8 08:38 05-worker.json
> -rw-r--r-- 1 runner runner 4581 Oct  8 08:38 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 9323 Oct  8 08:38 07-planner.json
> -rw-r--r-- 1 runner runner 4765 Oct  8 08:38 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner  308 Oct  8 08:38 09-not-started.json
> -rw-r--r-- 1 runner runner 9844 Oct  8 08:38 10-planner.json
> # Issue #210: Autopilot: the owner sees on the board and on every card what is on autopilot
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #219](https://github.com/dokima-dev/dokima/pull/219) · [files 

`2. Bash`
```
cd /tmp/pack; sed -n 1,200p issue.md
```

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
> **Context:** Asked by the owner on 2026-10-08 06:24 and corrected at 06:25 (https://github.com/dokima-dev/dokima/issues/205): no separate Autopilot needs you pill, no On autopilot from #N line, and the view is a table like the Needs you view. The board is kept by dokima/board.py (sync, decide, priority) from .github/workflows/board.yml; today the single-select Action field holds 'Needs you' 

`3. Bash`
```
cd /tmp/pack; grep -n "^### \|^\*\*Next\|^\*\*block\|^\*\*approve\|^- \*\*B" issue.md | head -80
```

> 4:### Checks failing
> 42:### RezaSoleymanifar on issue #210 (2026-10-08T06:58:13Z)
> 46:### dokima-runtime on issue #210 (2026-10-08T06:58:34Z)
> 158:**Next:** @RezaSoleymanifar The plan has questions for you. Answer with `/plan` and your words, or say `/review` to go on with its assumptions.
> 161:### RezaSoleymanifar on issue #210 (2026-10-08T07:13:12Z)
> 165:### dokima-runtime on issue #210 (2026-10-08T07:13:30Z)
> 170:**block**: The plan covers every ask, but every test swaps the real board for a stand-in, so the new reads and writes to GitHub (whether an issue is on autopilot, the card's current pill, the pull request's label, the view) could do nothing and all tests would still pass.
> 171:- **B1** (210.1, the planner fixes it): All ten tests replace dokima.board.Board with an in-memory stand-in that already offers the new methods (value, autopilot, open_pr, label, views, add_view). The real Board's versions of these are never run, so a worker can write them as stubs (autopilot always False, value always None, label and add_view doing nothing) and every test passes while the board shows no Autopilot pill, overwrites Needs you when autopilot is switched, and never labels pull requests or adds a view.
> 172:- **B2** (210.4, the planner fixes it): The owner asked to check whether GitHub's API can create a project view, and to make the view a one-time manual step with a (manual) criterion if it cannot. The plan says code adds the view but names no GitHub call that does so, and its only pr

`4. Bash`
```
cd /tmp/pack; sed -n 575,640p issue.md; sed -n 980,1040p issue.md; sed -n 1150,1300p issue.md
```

> ### RezaSoleymanifar on issue #210 (2026-10-08T07:35:54Z)
> 
> /work
> 
> ### dokima-runtime on issue #210 (2026-10-08T07:36:15Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Worker**
> 
> The board only knew the Needs you pill and never looked at the autopilot label, so nothing showed what runs on autopilot. The real Board now reads labels, an issue's open PR, a card's current pill and its views, and writes the PR label and the Autopilot view; sync, the river's card move and split filing use them to show Autopilot, keep Needs you in its place, and label split stories under a parent on autopilot.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "worker",
>  "stage": null,
>  "run_id": "37744423723",
>  "commit_before": "902f106a8da35a2e1b1222c71e3b71142d34d1d9",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 363497,
>   "turns": 17,
>   "cost_usd": 1.094106,
>   "tokens_in": 987641,
>   "tokens_out": 14684
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/210/37744423723-worker.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37744423723",
>  "handback": {
>   "summary": "The board only knew the Needs you pill and never looked at the autopilot label, so nothing showed what runs on autopilot. The real Board now reads labels, an issue's open PR, a card's current pill and its views, and 

`5. Bash`
```
cd /tmp/pack; cat plan.json; python3 -c "
import json;d=json.load(open('in/10-planner.json'));h=d.get('handback',d);print(json.dumps({k:v for k,v in h.items() if k in('test_changes','concerns','questions','out_of_scope','scope')},indent=1))"; cat in/08-reviewer-plan.json | head -80
```

> {
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
>    "text": "The board has one Autopilot view, laid out as a table and filtered to

**Agent:** Reading the latest plan; now checking whether the branch merges cleanly with main and running the tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --graph; git fetch -q origin main 2>&1|tail -1; git merge-tree --write-tree HEAD origin/main >/dev/null && echo CLEAN || echo CONFLICT; git log --oneline HEAD..origin/main | head; git show --stat HEAD | head -20; grep -n "def file_split" -A25 dokima/agent.py | head -40
```

> *   6d61f3a Merge branch 'main' into try/issue-210
> |\  
> | * 4cccffe Live card: minutes and the current step while the agent works (#216)
> | * 91ba938 Main is red: the cancelled-run test's fake plan review fails the new asks check (#221)
> * | 502c0c6 planner for #210 (run 37745957667)
> * | 2302537 worker for #210 (run 37744423723)
> * | 902f106 planner for #210 (run 37742292905)
> * | b224a3a planner for #210 (run 37740601676)
> |/  
> * 60dee99 Autopilot: /autopilot start and /autopilot stop switch an issue tree on and off (#214)
> CONFLICT
> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> commit 6d61f3a0fa4be23528a9e00f8e0f9c58f3a1f42f
> Merge: 502c0c6 4cccffe
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 03:07:34 2026 -0500
> 
>     Merge branch 'main' into try/issue-210
> 
>  .github/workflows/agent.yml |  64 ++++++++--
>  dokima/agent.py             |  25 ++--
>  tests/test_cancelled_run.py |  15 ++-
>  tests/test_progress_card.py | 291 ++++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 375 insertions(+), 20 deletions(-)
> 168:def file_split(repo, parent, recs):
> 169-    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links.
> 170-
> 171-    Returns the record of what was filed. Filing twice files nothing new: the newest spli

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git merge-tree --write-tree --name-only HEAD origin/main | head -20; git diff 6d61f3a --stat; git diff 502c0c6 6d61f3a --stat; git show origin/main:dokima/agent.py | grep -n "def file_split" -A15; git show origin/main:dokima/agent.py | grep -n "file_split(" 
```

> e51cfb406b5e8fc77b22ea149b4e76cef331443a
> dokima/agent.py
> 
> Auto-merging AGENTS.md
> Auto-merging dokima/agent.py
> CONFLICT (content): Merge conflict in dokima/agent.py
>  .github/workflows/agent.yml |  64 ++++++++--
>  dokima/agent.py             |  25 ++--
>  tests/test_cancelled_run.py |  15 ++-
>  tests/test_progress_card.py | 291 ++++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 375 insertions(+), 20 deletions(-)
> 168:def file_split(repo, parent, recs, labels=()):
> 169-    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
> 170-    each created with the given labels.
> 171-
> 172-    Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
> 173-    done = latest(recs, "split", passed=True)
> 174-    if done:
> 175-        return done
> 176-    plan = latest(recs, "planner")["handback"]
> 177-    title = json.loads(gh("issue", "view", str(parent), "-R", repo, "--json", "title"))["title"]
> 178-    filed = []
> 179-    for i, st in enumerate(plan["stories"], 1):
> 180-        extra = [x for label in labels for x in ("--label", label)]
> 181-        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
> 182-        number = int(url.rstrip("/").split("/")[-1])
> 183-        node = json.loads(gh("api", f"repos/{repo}/issues/{number}"))["id"]
> 168:def file_split(repo, parent, recs, labels=()):
> 1114:        rec 

`8. Bash`
```
cd /tmp/pack; python3 - <<'E'
import json
a=json.load(open('in/07-planner.json'))['handback'];b=json.load(open('in/10-planner.json'))['handback']
for k in set(a)|set(b):
    if a.get(k)!=b.get(k): print(k); print(' OLD',json.dumps(a.get(k))[:1500]); print(' NEW',json.dumps(b.get(k))[:1500])
print(json.load(open('in/10-planner.json')).get('check'))
E
```

> out_of_scope
>  OLD ["The board workflow (.github/workflows/board.yml) is not changed: it already runs on labeled and unlabeled issue events and on pull requests opening, which is every moment this story needs.", "dokima/card.py is not touched, and the issue's card shows nothing new.", "Adding the Autopilot option to the board's Action field is a one-time step on the board, like the Needs you option, as the owner accepted with /review; code never edits the field's options, and AGENTS.md says so.", "Running a whole tree end to end on autopilot is story 3 of #205; switching the label on and off is story 1 (#209).", "Two separate /autopilot start commands on two unrelated trees, given within the same few seconds on a board that has no Autopilot view yet, are not guarded against each adding one: the board workflow's runs are not queued across issues and it is not changed here. One command switches a whole tree, so this needs two commands at once."]
>  NEW ["The board workflow (.github/workflows/board.yml) is not changed: it already runs on labeled and unlabeled issue events and on pull requests opening, which is every moment this story needs.", "dokima/card.py is not touched, and the issue's card shows nothing new.", "Adding the Autopilot option to the board's Action field is a one-time step on the board, like the Needs you option, as the owner accepted with /review; code never edits the field's options, and AGENTS.md says so.", "Running a whole tree end to end on autopilot is story 

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/main:.github/workflows/agent.yml | grep -n -i "starting branch" -A30 | head -50
```

> 129:      - name: Starting branch
> 130-        env:
> 131-          GH_TOKEN: ${{ github.token }}
> 132-        run: |
> 133-          if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
> 134-            git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
> 135-            if [ "$ROLE" = worker ]; then
> 136-              git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
> 137-            fi
> 138-          elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
> 139-            # A plan review needs no branch: a split never makes one, so it reviews from main.
> 140-            git checkout -q -B "try/issue-$N" origin/main
> 141-          else
> 142-            echo "try/issue-$N does not exist; run the planner first." > /tmp/why.txt
> 143-            echo "::error title=Nothing to $ROLE::$(cat /tmp/why.txt)"; exit 1
> 144-          fi
> 145-          echo "BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> 146-          # A plan's tests are everything the issue's branch added since it split off main, over every planning round.
> 147-          echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
> 148-          # What this run starts from: the planner may change only tests from here on.
> 149-          echo "PLANNER_RUN_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> 150-          LOG="logs/$N/${{ github.run_id }}-$ROLE${STAGE:+-$STAGE}.md"
> 151-          echo "LOG=$LOG" >> "$GITHUB_ENV"
> 152-     

`10. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q 2>&1 | tail -30
```

> Full diff:
>     (
>   -     0,
>   ?     ^
>   +     1,
>   ?     ^
>   -     '',
>   +     'asks must list every ask in the owner\'s issue and comments, each {"ask": '
>   +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'}
>   asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
>   
> assert (1, 'asks mus...r "missing"}') == (0, '')
>   
>   At index 0 diff: 1 != 0
>   
>   Full diff:
>     (
>   -     0,
>   ?     ^
>   +     1,
>   ?     ^
>   -     '',
>   +     'asks must list every ask in the owner\'s issue and comments, each {"ask": '
>   +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 6 failed, 358 passed in 104.96s (0:01:44)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q 2>&1 | grep FAILED | cut -c1-200; rm -rf /tmp/wm; git worktree add -q /tmp/wm origin/main && cd /tmp/wm && git diff --name-only $(git merge-base origin/main /home/runner/work/dokima/dokima/.git/HEAD 2>/dev/null || echo 60dee99) 502c0c6 -- tests
```

> FAILED tests/test_autopilot_board.py::test_the_real_board_reads_an_issues_parent - Failed: 210.4: the real Board has no parent yet
> FAILED tests/test_autopilot_board.py::test_switching_a_whole_tree_on_adds_the_view_once_even_when_runs_overlap - Failed: 210.4: the real Board has no parent yet
> FAILED tests/test_autopilot_board.py::test_a_sub_issue_switched_on_alone_still_gets_the_view - Failed: 210.4: the real Board has no parent yet
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the ow
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in th
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B
> tests/test_autopilot_board.py
> tests/test_board.py
> tests/test_failed_run_card.py
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Tests ran on the branch; now checking the plan's tests on top of today's main.

`12. Bash`
```
cd /tmp/wm; for f in tests/test_autopilot_board.py tests/test_board.py tests/test_failed_run_card.py; do git -C /home/runner/work/dokima/dokima show HEAD:$f > $f; done; timeout 600 python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "FAILED|passed|failed" | cut -c1-220
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bt0zze7fp). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, looking at the split test against main's `file_split`.

`13. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def test_a_split_under_a_parent_on_autopilot" -A60 tests/test_autopilot_board.py | head -80
```

> 287:def test_a_split_under_a_parent_on_autopilot_files_children_on_autopilot(record_property, make, monkeypatch):
> 288-    """Stories filed by a split under a parent on autopilot get the autopilot label and the Autopilot pill; others don't.
> 289-
> 290-    Files an approved two-story split of #139, which carries the `autopilot` label, on a board. Both new issues carry
> 291-    the label, land in Backlog with Autopilot, and #139 shows Work with Autopilot. Then files the same split of a #139
> 292-    not on autopilot: no new issue carries the label and no card shows Autopilot."""
> 293-    record_property("proves", "210.2")
> 294-    w = make(labels={("issue", 139): {LABEL}})
> 295-    monkeypatch.setenv("DOKIMA_BOARD", "o/1")
> 296-    assert split_main(monkeypatch, w) == 0
> 297-    children = [n for (kind, n) in w.cards if kind == "issue" and n != 139]
> 298-    assert sorted(children) == [201, 202], f"210.2: the split's stories were not placed on the board: {children}"
> 299-    for n in (201, 202):
> 300-        assert w.has("issue", n), f"210.2: story #{n}, filed under #139 on autopilot, does not carry the autopilot label"
> 301-        assert (w.status("issue", n), w.action("issue", n)) == ("Backlog", "Autopilot"), \
> 302-            f"210.2: story #{n} landed as {w.status('issue', n)!r} with {w.action('issue', n)!r}, not Backlog with Autopilot"
> 303-    assert (w.status("issue", 139), w.action("issue", 139)) == ("Work", "Autopilot"), \
> 304-        f"210.2: parent #139 on autopilot shows {w.actio

`14. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`15. Bash`
```
cd /tmp/pack; python3 -c "
import json;h=json.load(open('in/08-reviewer-plan.json'))['handback'];print(json.dumps(h['asks'],indent=1))"
```

> [
>  {
>   "ask": "an Autopilot pill on every card in the tree",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.1"
>  },
>  {
>   "ask": "the pill is gone once the issue is off autopilot",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.1"
>  },
>  {
>   "ask": "including children filed later by a split under a parent on autopilot",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.2"
>  },
>  {
>   "ask": "the usual Needs you pill in its place where autopilot stopped for them",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.3"
>  },
>  {
>   "ask": "no card ever shows Autopilot and Needs you at once",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.3"
>  },
>  {
>   "ask": "one table view listing it all",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.4"
>  },
>  {
>   "ask": "The board has an Autopilot view laid out as a table, like the Needs you view, listing every issue and pull request on autopilot and nothing else",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.4"
>  },
>  {
>   "ask": "check whether GitHub's API can create a project view; if it cannot, the view is a one-time setup step next to the Needs you view and its criterion is (manual) with that reason",
>   "source": "https://github.com/dokima-dev/dokima/issues/210",
>   "criterion": "210.4"
>  },
>  {
>   "ask": "In a repo

`16. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output | sed 's/ - .*//' | sort | uniq -c | sort -rn | head; tail -1 /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output; grep -o "FAILED[^-]*- [^:]*:[^:]*" /tmp/claude-1001/-home-runner-work-dokima-dokima/71b9d1c5-1da8-4187-9c6b-e4c85ed2c1f0/tasks/bt0zze7fp.output | cut -c1-200 | head -25
```

> 1 [exited with code 0]
>       1 FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named
>       1 FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests
>       1 FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner
>       1 FAILED tests/test_autopilot_board.py::test_the_river_keeps_the_pill_when_it_moves_a_card_on_autopilot
>       1 FAILED tests/test_autopilot_board.py::test_the_real_board_reads_whether_an_issue_or_pull_request_is_on_autopilot
>       1 FAILED tests/test_autopilot_board.py::test_the_real_board_reads_back_the_pill_it_sets
>       1 FAILED tests/test_autopilot_board.py::test_the_real_board_reads_an_issues_parent
>       1 FAILED tests/test_autopilot_board.py::test_the_real_board_puts_the_autopilot_label_on_and_off_a_pull_request
>       1 FAILED tests/test_autopilot_board.py::test_the_real_board_lists_its_views_and_adds_the_autopilot_table_view
> [exited with code 0]
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_on_puts_the_pill_on_the_issue_and_its_pull_request - AssertionError: 210.1
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_off_takes_the_pill_away - AssertionError: 210.1
> FAILED tests/test_autopilot_board.py::test_stage_moments_keep_the_pill_on_issues_on_autopilot_only - AssertionError: 210.1
> FAILED tests/test_autopilot_board.py::test_the_river_keeps_the_pill_when_it_moves_a_card_on_autopilot - AssertionErro

`17. Bash`
```
cd /tmp/wm; python3 -m pytest -q -p no:cacheprovider tests/test_autopilot_board.py -k split 2>&1 | grep -E "^E " | head -5; git stash -q; python3 -m pytest -q -p no:cacheprovider tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -2; git stash pop -q; cd /; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/wm
```

> E           AssertionError: 210.2: story #201 landed as 'Backlog' with None, not Backlog with Autopilot
> E           assert ('Backlog', None) == ('Backlog', 'Autopilot')
> E             
> E             At index 1 diff: None != 'Autopilot'
> E             
>     )
> 3 failed, 11 passed in 4.64s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Main is red on 3 unrelated tests; the plan holds up on today's main. Writing the hand-back.

`18. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'E'
import json
asks=json.load(open('in/08-reviewer-plan.json'))['handback']['asks']
r={"previous_step":{
 "did":["The planner re-read the plan against today's main and kept all five criteria and their 21 tests unchanged.",
        "The planner added to the plan that labelling a split's stories under a parent on autopilot is already on main since #213, so this story adds only the Autopilot pill on the stories and the parent, and drops the branch's own labelling."],
 "decided":["The branch's own change to how a split files its stories gives way to main's."],
 "open":["The planner says it cannot clear the clash in dokima/agent.py itself, since it may change only tests; until someone resolves it once on try/issue-210, the next /work stops at Starting branch again."]},
 "verdict":"approve",
 "summary":"The plan holds on today's main: all 19 new tests fail there only because the feature is missing, and the split test now asks only for the Autopilot pill since main already labels the stories; but the branch still clashes with main in dokima/agent.py, so /work will stop again until that clash is resolved by hand.",
 "blockers":[],
 "notes":[
  {"text":"The owner's '/plan ... Re-plan on top of today's main' is done in the plan, not on the branch: try/issue-210 still clashes with main, and the worker's Starting branch step merges main with no conflict handling, so /work fails the same way as run 37749690595. The planner cannot fix this (it may push only tests). Keeping main's file_split and dropping the branch's labelling hunk in it, as the plan's last out-of-scope line says, clears it.",
   "evidence":"git merge-tree --write-tree HEAD origin/main: CONFLICT (content) in dokima/agent.py; origin/main has f1b30ab (#218) not merged into try/issue-210; .github/workflows/agent.yml:136 `git merge -q --no-edit origin/main` for the worker."},
  {"text":"On today's main with the plan's three test files laid on top, every one of the 1
```

> rc=0

**Agent:** I approved the plan for #210, but your next `/work` will fail the same way the last one did. The plan itself is fine on today's main. The branch still clashes with main, and you'll need to resolve that by hand first.

- **What the planner changed:** the five criteria and their 21 tests are as before. Main already gives a split's stories the `autopilot` label (since #213). So the planner added a note that this story only adds the Autopilot pill to the stories and the parent, and it drops the branch's own labelling code in favour of main's.
- **Tested on today's main:** I put the plan's three test files on top of main and ran the suite. All 19 new tests fail, and each failure names its criterion and says the feature is missing. The split test now fails only on the missing pill ("story #201 landed as Backlog with None"), so main's labelling already passes it. The five older tests whose fake GitHub the planner extended pass.
- **What you need to do:**
  - **The clash:** `try/issue-210` still clashes with main in `dokima/agent.py`, in how a split files its stories. The worker's "Starting branch" step merges main with no conflict handling, so it stops there again, as in run 37749690595. The planner can't fix this because it may only change tests.
  - **The fix:** resolve it once on the branch. Keep main's version of `file_split` and drop the branch's own labelling change inside it.
  - **Then:** say `/work`.
- **A separate problem:** main itself is red. Three tests in `tests/test_fixer.py` and `tests/test_handback_check.py` fail on untouched main because a review must now list the owner's asks and those tests' sample reviews list none. Every PR's full-suite check will fail until that's fixed, including PR #219. I listed it as a proposed new issue.

The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.
