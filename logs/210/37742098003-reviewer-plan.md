# reviewer (plan) for #210

Run: https://github.com/dokima-dev/dokima/actions/runs/37742098003

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in/; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #210: Autopilot: the owner sees on the board and on every card what is on autopilot
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
> **Context:** Asked by the owner on 2026-10-08 06:24 and corrected at 06:25 (https://github.com/dokima-dev/dokima/issues/205): no separate Autopilot needs you pill, no On autopilot from #N line, and the view is a table like the Needs you view. The board is kept by dokima/board.py (sync, decide, priority) from .github/workflows/board.yml; today the single-select Action field holds 'Needs you' (board.py sync sets it or clears it) and the Priority pill follows a label (#206). A simple way to keep Autopilot and Needs you off the same card: make Autopilot another option of the same single-select Action field, set to 'Needs you' when the river stops for the owner and to 'Autopilot' otherwise while the issue carries the `autopilot` label from story 1, so a card can never hold both. Children filed later by a split (file_split in dokima/agent.py) under a parent on autopilot must get the label and the pill too. The view: check whether GitHub's AP

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_autopilot_board.py; python -m pytest -q tests/test_autopilot_board.py 2>&1 | tail -40
```

> commit b224a3a1ddf269b2e60ee1bfdc60146203ac954f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 07:08:55 2026 +0000
> 
>     planner for #210 (run 37740601676)
> 
>  tests/test_autopilot_board.py | 410 ++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 410 insertions(+)
> """The board shows what runs on autopilot: an Autopilot pill, Needs you in its place when the river stops, one view (#210).
> 
> The board is faked at the size of dokima.board.Board, so these tests read the board's end state, never the GraphQL
> queries that reach it. The fake keeps, in memory, one world shared with a fake `gh`:
> 
> - cards: each card's Status and Action (the single-select field holding "Needs you" and now "Autopilot");
> - labels: the labels each issue and pull request carries; `autopilot` is autopilot's state (story 1, #209);
> - the open pull request of each issue (branch try/issue-N, body "Closes #N");
> - the board's views by name.
> 
> What the fake Board offers, and the code is expected to use:
>     Board(spec, repo, q)               the board, as today
>     .fields                            {"Status": (id, {option: id}), "Action": (id, {option: id})}, as today
>     .item(kind, n) -> item id          as today; kind is "issue" or "pr"
>     .set(item, field, option or None)  as today: an unknown field or option is ignored, None clears
>     .value(item, field) -> option      the card's current option of that field, or None
>     .autopilot(kind, n) -> bool   

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_autopilot_board.py 2>&1 | grep -E "^(FAILED|E  )" | head -40; wc -l dokima/board.py; grep -n "def \|class " dokima/board.py; grep -rn "Board(" tests/*.py | grep -v test_autopilot_board | head; grep -n "def move_card\|def file_split" -A30 dokima/agent.py | head -90
```

> E           AssertionError: 210.1: issue #57 on autopilot shows None, not the Autopilot pill
> E           assert None == 'Autopilot'
> E            +  where None = action('issue', 57)
> E            +    where action = <test_autopilot_board.World object at 0x7fc8183afe60>.action
> E       AssertionError: 210.1: issue #57 off autopilot still shows 'Autopilot'
> E       assert 'Autopilot' is None
> E        +  where 'Autopilot' = action('issue', 57)
> E        +    where action = <test_autopilot_board.World object at 0x7fc8183718b0>.action
> E       AssertionError: 210.1: #57 on autopilot moved to Work shows None, not Autopilot
> E       assert ('Work', None) == ('Work', 'Autopilot')
> E         
> E         At index 1 diff: None != 'Autopilot'
> E         
> E         Full diff:
> E           (
> E               'Work',
> E         -     'Autopilot',
> E         +     None,
> E           )
> E           AssertionError: 210.1: the river moved issue #57, on autopilot, and it shows None, not Autopilot
> E           assert ('Review', None) == ('Review', 'Autopilot')
> E             
> E             At index 1 diff: None != 'Autopilot'
> E             
> E             Full diff:
> E               (
> E                   'Review',
> E             -     'Autopilot',
> E             +     None,
> E               )
> E           AssertionError: 210.2: story #201, filed under #139 on autopilot, does not carry the autopilot label
> E           assert False
> E            +  where False = has('issue', 201)
> E            +    where has = <test_autopilo

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 55,125p dokima/board.py; grep -rn "board\.\|Board" tests/test_board*.py 2>/dev/null | head -20; ls tests
```

> if event != "issues" or p["action"] not in ("labeled", "unlabeled") or p["label"]["name"] not in PRIORITY:
>         return None
>     names = {label["name"] for label in p["issue"].get("labels") or []}
>     return p["issue"]["number"], next((option for label, option in PRIORITY.items() if label in names), None)
> 
> 
> def gql(query, **variables):
>     args = ["gh", "api", "graphql", "-f", f"query={query}"]
>     for k, v in variables.items():
>         args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
>     return json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)["data"]
> 
> 
> class Board:
>     def __init__(self, spec, repo, q=gql):
>         self.q = q
>         owner, number = spec.split("/")
>         self.repo_owner, self.repo_name = repo.split("/")
>         p = q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}', o=owner, n=int(number))["organization"]["projectV2"]
>         self.id = p["id"]
>         self.fields = {f["name"]: (f["id"], {o["name"]: o["id"] for o in f["options"]}) for f in p["fields"]["nodes"] if f}
> 
>     def item(self, kind, number):
>         """The board item for an issue or PR, added at the top if it is not on the board yet."""
>         field = "issue" if kind == "issue" else "pullRequest"
>         node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{id projectItems(first:20){{nodes{

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,30p .github/workflows/board.yml; sed -n 55,110p tests/test_board.py
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
>                 {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": "Needs you"}]}]}}}}
>         if query.startswith("query") and "repository" in query:
>             kind = "issue" if "issue(" in query else "pullRequest"
>             items = [{"id": "ITEM", "project": {"id": "P"}}] if self.on_board else []
>             return {"repository": {kind: {"id": "C", "projectItems": {"nodes": items}}}}
>         if "addProjectV2ItemById" in query:
>             return {"addProjectV2ItemById": {"item": {"id": "NEW"}

**Agent:** Checking line numbers for the hand-back, then writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "monkeypatch.setattr(board, \"Board\"\|def add_view\|def autopilot\|def value\|def label\|def test_the_board_gets_one\|def test_pull_requests_on" tests/test_autopilot_board.py; grep -n "createProjectV2View\|View" -r dokima | head
```

> 91:        def value(self, iid, field):
> 94:        def autopilot(self, kind, n):
> 100:        def label(self, kind, n, on):
> 106:        def add_view(self, name, layout, filter):
> 167:        monkeypatch.setattr(board, "Board", fake_board(world))
> 174:def label_event(action, name, labels, number=57):
> 352:def test_the_board_gets_one_autopilot_table_view(record_property, make):
> 370:def test_pull_requests_on_autopilot_carry_the_label_so_the_view_lists_them(record_property, make):
> 406:    monkeypatch.setattr(board, "Board", explode)

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote four criteria and one board-free rule: the Autopilot pill on every card of an issue on autopilot and its pull request, stories of a split on autopilot, Needs you in the pill's place, and one Autopilot table view.",
          "The planner wrote ten tests in tests/test_autopilot_board.py; all ten fail today because the feature is missing."],
  "decided": ["Autopilot is a second option of the board's Action field next to Needs you, so a card holds one or the other; the owner adds that option by hand once.",
              "Code adds the Autopilot view itself, and pull requests carry the autopilot label so the view lists them; board.yml stays unchanged."],
  "open": ["The owner went on with /review on the planner's reading that the Autopilot option is added by hand."]},
 "verdict": "block",
 "summary": "The plan covers every ask, but every test swaps the real board for a stand-in, so the new reads and writes to GitHub (whether an issue is on autopilot, the card's current pill, the pull request's label, the view) could do nothing and all tests would still pass.",
 "blockers": [
  {"id": "B1", "criterion": "210.1", "test": "tests/test_autopilot_board.py::test_switching_autopilot_on_puts_the_pill_on_the_issue_and_its_pull_request",
   "problem": "All ten tests replace dokima.board.Board with an in-memory stand-in that already offers the new methods (value, autopilot, open_pr, label, views, add_view). The real Board's versions of these are never run, so a worker can write them as stubs (autopilot always False, value always None, label and add_view doing nothing) and every test passes while the board shows no Autopilot pill, overwrites Needs you when autopilot is switched, and never labels pull requests or adds a view.",
   "evidence": "tests/test_autopilot_board.py:167 monkeypatch.setattr(board, \"Board\", fake_board(world)); the methods at lines 91-107 exist 
```

> rc=0

**Agent:** I blocked the plan for #210. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

**What's fine:** every ask in the issue maps to a criterion (210.1 to 210.5), so no ask is missing. All ten new tests fail today, and each fails because the feature isn't built yet. Leaving `board.yml` unchanged is right too: it already runs on labeled and unlabeled issue events.

**Blockers (both go back to the planner):**
- **B1 (criterion 210.1, and also 210.3 and 210.4):** every test swaps the real board for an in-memory stand-in (`tests/test_autopilot_board.py:167`). The board's new GitHub reads and writes are therefore never run:
  - checking whether an issue is on autopilot
  - reading a card's current pill
  - labelling the pull request
  - adding the view

  A worker could leave all four doing nothing and every test would still pass. On the real board there would be no Autopilot pill, Needs you would be overwritten when autopilot is switched, and the view would never appear. The fix is to test these against a faked GitHub connection, the way `tests/test_board.py` already does for the existing board code.
- **B2 (criterion 210.4):** the owner asked the planner to check whether GitHub's API can create a project view, and to make the view a one-time manual step if it can't. The plan says code adds the view but doesn't name a GitHub call that does it, and its only proof is the stand-in. As far as I know, GitHub's project API has no call to create a view, though I couldn't confirm that from the sandbox. The fix is to name the call and test it, or else follow the owner's fallback: a one-time setup step in AGENTS.md next to the Needs you view, with that part of 210.4 marked (manual).
