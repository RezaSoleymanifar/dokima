# reviewer (plan) for #278

Run: https://github.com/dokima-dev/dokima/actions/runs/37858123186

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (34.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/82df4ac5-e871-46c2-8931-214a0aa3745f/tool-results/boms5nvkm.txt
> 
> Preview (first 2KB):
> # Issue #278: The Autopilot view shows only open issues and pull requests
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The Autopilot tab on the board still lists pull requests that merged and issues that closed. Its filter is only the autopilot label, and merged or closed items keep that label.
> 
> What I want:
> - The Autopilot view lists only open issues and pull requests on autopilot.

`2. Bash`
```
cd /tmp/pack; sed -n 30,400p issue.md | grep -v '^$' | cut -c1-600 | head -150; ls in
```

> ### dokima-runtime on issue #278 (2026-10-08T22:28:07Z)
> Autopilot is on for #278. Planning started for #278, which wait on nothing open.
> ### dokima-runtime on issue #278 (2026-10-08T22:28:18Z)
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue and asks you 1 question.
> **User story:** The Autopilot view on the board lists only open issues and pull requests on autopilot, on new boards and on the board that already has the view.
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 1. A new Autopilot view is filtered to label:autopilot is:open, so merged pull requests and closed issues never show in it.
> 2. An Autopilot view still filtered to label:autopilot is changed to label:autopilot is:open the next time a tree goes on autopilot. No second view is added, and a view already right is left alone.
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or l

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(json.dumps(d.get('handback',d),indent=1)[:8000])"; grep -n "^### " issue.md
```

> [
>  {
>   "id": "B1",
>   "criterion": "278.2",
>   "test": "tests/test_autopilot_board.py::test_the_existing_autopilot_view_is_fixed_to_open_items_only",
>   "problem": "The fix depends on reading each view's id and filter from GitHub. On real GitHub, a query returns only the fields it asks for. The faked GitHub returns id, name, layout and filter for every view whatever the query asks. Code that keeps today's query (views{nodes{name}}) and then reads the id or filter would pass every 278.2 and 278.3 test, but on the real board it would get no id or filter. The existing view would then never be fixed, or the run would crash.",
>   "evidence": "tests/test_autopilot_board.py:509 answers every organization query with `[dict(x) for x in self.views]` (all keys) without looking at which fields the query names; dokima/board.py:138 today asks only `nodes{name}`. GitHub's schema (docs.github.com/public/fpt/schema.docs.graphql) confirms ProjectV2View has `id` and `filter`, and updateProjectV2View takes `viewId` and `filter`, so the plan's approach is real. Only the fake is too forgiving.",
>   "fix": "In FakeGitHub.q, return for each view only the fields the query names: include `id` only if the query text contains `id`, and `filter` only if it contains `filter` (for example, check the `nodes{...}` selection under `views`). That way a query that does not ask for them turns 278.2 and 278.3 red.",
>   "fixer": "planner"
>  }
> ]{
>  "kind": "user_story",
>  "summary": "The board's Autopilot view still lists m

`4. Bash`
```
cd /tmp/pack; sed -n 318,340p issue.md; sed -n 485,500p issue.md | cut -c1-400; diff <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1))") <(python3 -c "import json;d=json.load(open('in/03-planner.json'));print(json.dumps(d.get('handback',d),indent=1))") | head; cd /home/runner/work/dokima/dokima; git show --stat HEAD HEAD~1 | head -30
```

> ### RezaSoleymanifar on issue #278 (2026-10-08T22:51:33Z)
> 
> I set the existing Autopilot view's filter by hand to `label:autopilot is:open`. Code should create new views with that same filter and leave this one as is.
> 
> ### RezaSoleymanifar on issue #278 (2026-10-08T22:57:20Z)
> 
> /plan Answer: the existing view is fixed right after this merges. If it is already correct, like now since I fixed it by hand, the code leaves it alone.
> 
> ### dokima-runtime on issue #278 (2026-10-08T22:57:41Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** The Autopilot view on the board lists only open issues and pull requests on autopilot: new views are made that way, and an old view is fixed right after this merges unless it is already right.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 
> 1. A new Autopilot view is filtered to label:autopilot is:open, so merged pull requests and closed issues never show in it.
> 2. The next pull request merge changes an Autopilot view still filtered to label:autopilot into label:autopilot is:open, so t

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/board.yml | head -80; grep -n "def \|views\|filter" dokima/board.py | head -80
```

> name: board
> # Keeps the project board's Status and "Waiting on" current at every stage moment,
> # and its Priority in step with the blocker, high and parked labels.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [labeled, unlabeled, closed]
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   workflow_run:
>     workflows: [done-whens]
>     types: [completed]
> permissions:
>   contents: read
> concurrency:
>   group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
>   cancel-in-progress: false
> jobs:
>   sync:
>     environment: keys
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.repository.default_branch }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - id: app
>         uses: actions/create-github-app-token@v2
>         with:
>           app-id: ${{ vars.DOKIMA_APP_ID }}
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Sync the board
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           DOKIMA_BOARD: ${{ vars.DOKIMA_BOARD }}
>         run: pyth

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff accfe36~1 HEAD -- tests/test_autopilot_board.py
```

> diff --git a/tests/test_autopilot_board.py b/tests/test_autopilot_board.py
> index db8486a..dad8573 100644
> --- a/tests/test_autopilot_board.py
> +++ b/tests/test_autopilot_board.py
> @@ -360,7 +360,7 @@ def test_the_board_gets_one_autopilot_table_view(record_property, make):
>      """The first issue switched on autopilot gives the board an Autopilot view, a table showing only what carries the label.
>  
>      On a board with only the Needs you view, switching #57 on autopilot adds exactly one view: named Autopilot, laid
> -    out as a table, filtered to label:autopilot. Switching #101 on afterwards adds no second view, and a stage moment
> +    out as a table, filtered to label:autopilot is:open (#278). Switching #101 on afterwards adds no second view, and a stage moment
>      on a board without the view adds none."""
>      record_property("proves", "210.4")
>      w = make(labels={("issue", 57): {LABEL}, ("issue", 101): {LABEL}, ("issue", 58): set()})
> @@ -368,8 +368,8 @@ def test_the_board_gets_one_autopilot_table_view(record_property, make):
>      assert [v["name"] for v in w.view_list] == ["Needs you"], "210.4: a board change unrelated to autopilot added a view"
>      board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
>      added = [v for v in w.view_list if v["name"] != "Needs you"]
> -    assert added == [{"name": "Autopilot", "layout": "table", "filter": f"label:{LABEL}"}], \
> -        f"210.4: switching autopilot on added {added}, not one Autopilot table view filter

**Agent:** Plan review round 2: checking the planner's fix for B1 and the owner's new answer, then running the tests.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_autopilot_board.py 2>&1 | tail -25; sed -n 137,210p dokima/board.py
```

> Right contains one more item: ('PVTV_1', 'label:autopilot is:open')
>   
>   Full diff:
>   + []
>   - [
>   -     (
>   -         'PVTV_1',
>   -         'label:autopilot is:open',
>   -     ),
>   - ])
> FAILED tests/test_autopilot_board.py::test_a_view_already_right_is_left_alone - AssertionError: 278.3: a merge never fixed a view still on label:autopilot (sent []), so leaving right views alone proves nothing
> assert [] == [('PVTV_1', '...lot is:open')]
>   
>   Right contains one more item: ('PVTV_1', 'label:autopilot is:open')
>   
>   Full diff:
>   + []
>   - [
>   -     (
>   -         'PVTV_1',
>   -         'label:autopilot is:open',
>   -     ),
>   - ]
> FAILED tests/test_autopilot_board.py::test_a_refused_fix_still_moves_the_cards_and_says_why - Failed: DID NOT RAISE Exception
> 8 failed, 17 passed in 0.36s
>     def views(self):
>         p = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){views(first:50){nodes{name}}}}}', o=self.owner, n=self.number)["organization"]["projectV2"]
>         return [v["name"] for v in p["views"]["nodes"]]
> 
>     def add_view(self, name, layout, filter):
>         self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)
> 
> 
> def action(board, kind, number, needs_you):
>     """The Action pill: Needs you when the river stops for the owner, else Autopilot while on autopilot, else none."""
>     return "Needs you" if needs_you else "Autopilot" if board.autopilot(kind, number) else None
> 
> 
> def switched(event, p):
>   

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_autopilot_board.py 2>&1 | grep -E "^FAILED"; python3 -m pytest -q 2>&1 | tail -3; sed -n 19,55p dokima/board.py
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bdngbo3iu). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/82df4ac5-e871-46c2-8931-214a0aa3745f/tasks/bdngbo3iu.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 60 python3 -m pytest -q tests/test_autopilot_board.py 2>&1 | grep -E "^FAILED" | cut -c1-250; sed -n 19,55p dokima/board.py
```

> FAILED tests/test_autopilot_board.py::test_the_board_gets_one_autopilot_table_view - AssertionError: 210.4: switching autopilot on added [{'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'}], not one Autopilot table view filtered to
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_on_reaches_github_end_to_end - AssertionError: 210.4: the Autopilot view is {'id': 'PVTV_1', 'name': 'Autopilot', 'layout': 'TABLE_LAYOUT', 'filter': 'label:autopilot'}
> FAILED tests/test_autopilot_board.py::test_switching_a_whole_tree_on_adds_the_view_once_even_when_runs_overlap - AssertionError: 210.4: the top of the tree added {'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'}, not the Autopilot
> FAILED tests/test_autopilot_board.py::test_a_new_autopilot_view_lists_only_open_issues_and_pull_requests - AssertionError: 278.1: switching autopilot on sent [('POST', 'orgs/dokima-dev/projectsV2/1/views', {'name': 'Autopilot', 'layout': 'table', 'fi
> FAILED tests/test_autopilot_board.py::test_merging_a_pull_request_fixes_the_old_autopilot_view - AssertionError: 278.2: the merge run sent [], not one change of the Autopilot view (PVTV_1, label:autopilot) to label:autopilot is:open
> FAILED tests/test_autopilot_board.py::test_the_fix_is_made_once_across_merges - AssertionError: 278.2: two merges sent updates [] and creates [], not one fix to label:autopilot is:open
> FAILED tests/test_autopilot_board.py::test_a_view_already_right_is_left_alone - AssertionError: 2

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "label:autopilot" AGENTS.md; grep -n "issuecomment\|html_url" /tmp/pack/issue.md | head; python3 -c "import json;print(json.load(open('/tmp/pack/plan.json')).get('questions'))"
```

> 79:- One Autopilot view, a table filtered to `label:autopilot`, lists everything on autopilot. Code adds it the first time a tree goes on autopilot, from the board run of the tree's top issue only, and a refused view fails that run naming it. The Autopilot option of the Action field is a one-time step on the board, like Needs you; code never edits the field's options.
> None

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote the plan after the owner's answer: the old Autopilot view is fixed by the board run of the next pull request merge, so the merge of this work fixes it.",
          "It made the faked GitHub answer a views query with only the fields the query names, and added a test that a view already right is left alone."],
  "decided": ["A view already on label:autopilot is:open, or on any other filter the owner chose, is never changed, and a merge never adds a view.",
              "If GitHub refuses the change, the merged cards still move to Done and the board run fails naming the Autopilot view."],
  "open": ["Nothing is left for the owner; the plan has no questions."]},
 "verdict": "approve",
 "summary": "The plan now fixes the old Autopilot view right after this merges and leaves a view already right alone, as the owner answered, and its tests would catch code that never reads the view's filter from GitHub.",
 "blockers": [],
 "notes": [
  {"text": "AGENTS.md still says the view is a table filtered to label:autopilot. AGENTS.md is in scope; the worker should change it to label:autopilot is:open and say an old view is fixed on the next merge.", "evidence": "AGENTS.md:79"},
  {"text": "All eight new and changed tests fail today for the right reason: the view is still made with label:autopilot and no merge run changes a view (the refused-fix test fails with DID NOT RAISE). The other 17 tests in the file pass.", "evidence": "python3 -m pytest -q tests/test_autopilot_board.py: 8 failed, 17 passed"}
 ],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "The Autopilot view lists only open issues and pull requests on autopilot. Anything merged or closed leaves it.", "source": "https://github.com/dokima-dev/dokima/issues/278", "criterion": "278.1"},
  {"ask": "The existing view is fixed too, not only new ones.", "source": "https://github.com/dokima-dev/do
```

> (Bash completed with no output)

**Agent:** I approved the plan for #278 on this second round, and the review is in `/tmp/dokima-out/review.json`. Both hand-back checks pass.

- **Last round's blocker (B1) is fixed.** The fake GitHub in the tests used to return every view's id and filter whether or not the query asked for them. Now it returns only the fields the query names, as real GitHub does. Code that still asks GitHub only for view names would fail the tests for fixing the old view.
- **The owner's answer is in the plan.** The old Autopilot view is fixed by the board run for the next merge, and that will be the merge of this work. A view that is already `label:autopilot is:open`, like the one the owner set by hand, is left alone. So is any other filter the owner chose, and a merge never adds a view.
- **Every request the owner made maps to a criterion.** There are five, from the issue text and the owner's two comments, and none is missing. The plan has no questions left, so there was nothing to judge on that front.
- **The tests fail today for the right reason.** In `tests/test_autopilot_board.py`, the 8 new and changed tests fail and the other 17 pass. New views still get the old filter, no merge changes a view, and the test for a refused change fails because nothing raises an error.

I added one note for the worker: `AGENTS.md:79` still says the view is filtered to `label:autopilot`. `AGENTS.md` is in the plan's scope, so the worker should change it to `label:autopilot is:open`.

The full test suite didn't finish within two minutes. I only ran `tests/test_autopilot_board.py`.

`12. Bash`
```
grep -E "passed|failed|^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/82df4ac5-e871-46c2-8931-214a0aa3745f/tasks/bdngbo3iu.output | cut -c1-160
```

> FAILED tests/test_autopilot_board.py::test_the_board_gets_one_autopilot_table_view - AssertionError: 210.4: switching autopilot on added [{'name': 'Autopilot', 
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_on_reaches_github_end_to_end - AssertionError: 210.4: the Autopilot view is {'id': 'PVTV_1', 'nam
> FAILED tests/test_autopilot_board.py::test_switching_a_whole_tree_on_adds_the_view_once_even_when_runs_overlap - AssertionError: 210.4: the top of the tree adde
> FAILED tests/test_autopilot_board.py::test_a_new_autopilot_view_lists_only_open_issues_and_pull_requests - AssertionError: 278.1: switching autopilot on sent [(
> FAILED tests/test_autopilot_board.py::test_merging_a_pull_request_fixes_the_old_autopilot_view - AssertionError: 278.2: the merge run sent [], not one change of
> FAILED tests/test_autopilot_board.py::test_the_fix_is_made_once_across_merges - AssertionError: 278.2: two merges sent updates [] and creates [], not one fix to
> FAILED tests/test_autopilot_board.py::test_a_view_already_right_is_left_alone - AssertionError: 278.3: a merge never fixed a view still on label:autopilot (sent
> FAILED tests/test_autopilot_board.py::test_a_refused_fix_still_moves_the_cards_and_says_why - Failed: DID NOT RAISE Exception
> FAILED tests/test_autopilot_board.py::test_a_refused_fix_still_moves_the_cards_and_says_why - Failed: DID NOT RAISE Exception
> 8 failed, 562 passed in 266.74s (0:04:26)

**Agent:** The full test suite has now finished: 8 failed and 562 passed. The 8 failures are the plan's new and changed tests in `tests/test_autopilot_board.py`, and they fail for the same reasons as when I ran that file alone. Nothing else in the repo fails, so my approval of the plan stands. I didn't change `review.json`.
