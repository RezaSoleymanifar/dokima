# reviewer (plan) for #210

Run: https://github.com/dokima-dev/dokima/actions/runs/37743334055

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (38.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tool-results/buex0tzs6.txt
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
> **Context:** Asked by the owner on 2026-10-08 06:24 and corrected at 06:25 (https://github.com/dokima-dev/dokima/issues/205): no separate Autopilot needs you pill, no On autopilot from #N line, and the view is a table like the Needs you view. The board is kept by dokima/board.py (sync, decide, priority) from .github/workflows/board.yml; today the single-select Action field holds 'Needs you' (board.py sync sets it or clears it) and the Priority pill follows a label (#206). A simple way to keep Autopilot and Needs you off the same card: make Autopilot another option of the same single-select Action field, set to 'Needs you

`2. Bash`
```
cd /tmp/pack; cat issue.md
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

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['in/02-reviewer-plan.json']:
  d=json.load(open(f)); print(json.dumps(d,indent=1)[:12000])
"
```

> [
>  {
>   "id": "B1",
>   "criterion": "210.1",
>   "test": "tests/test_autopilot_board.py::test_switching_autopilot_on_puts_the_pill_on_the_issue_and_its_pull_request",
>   "problem": "All ten tests replace dokima.board.Board with an in-memory stand-in that already offers the new methods (value, autopilot, open_pr, label, views, add_view). The real Board's versions of these are never run, so a worker can write them as stubs (autopilot always False, value always None, label and add_view doing nothing) and every test passes while the board shows no Autopilot pill, overwrites Needs you when autopilot is switched, and never labels pull requests or adds a view.",
>   "evidence": "tests/test_autopilot_board.py:167 monkeypatch.setattr(board, \"Board\", fake_board(world)); the methods at lines 91-107 exist only in the stand-in. The existing board tests (tests/test_board.py::test_pr_and_issue_move_together) instead fake only the GraphQL call q and run the real Board.",
>   "fix": "Add tests that run the real Board's new methods against a faked GitHub (the q GraphQL stand-in, and a fake gh for labels), asserting the call and its result: reading an issue's labels gives autopilot True/False, reading a card's Action gives Needs you/Autopilot/None, labelling and unlabelling a pull request sends the label change, and adding the view sends the view's name, table layout and label:autopilot filter. Name them under 210.1, 210.3 and 210.4.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "210.4",
> 

`4. Bash`
```
cd /tmp/pack; cat plan.json; python3 -c "
import json
d=json.load(open('in/03-planner.json')); print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); print(list(d.keys()))
"
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

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat main...HEAD; wc -l tests/test_autopilot_board.py; python -m pytest -q tests/test_autopilot_board.py 2>&1 | tail -25; python -m pytest -q 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bdwomu36o). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tasks/bdwomu36o.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tasks/bdwomu36o.output; cat tests/test_autopilot_board.py
```

> <persisted-output>
> Output too large (42.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tool-results/bczi20w3v.txt
> 
> Preview (first 2KB):
>  tests/test_autopilot_board.py | 679 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_board.py           |   7 +-
>  tests/test_failed_run_card.py |   9 +-
>  3 files changed, 692 insertions(+), 3 deletions(-)
> 679 tests/test_autopilot_board.py
>   Full diff:
>   + []
>   - [
>   -     {
>   -         'name': 'Autopilot',
>   -         'layout': 'table',
>   -         'filter': 'label:autopilot',
>   -     },
>   - ]
> FAILED tests/test_autopilot_board.py::test_pull_requests_on_autopilot_carry_the_label_so_the_view_lists_them - AssertionError: 210.4: PR #60, built for #57 on autopilot, does not carry the autopilot label
> assert False
>  +  where False = has('pr', 60)
>  +    where has = <test_autopilot_board.World object at 0x7f74da333710>.has
> FAILED tests/test_autopilot_board.py::test_without_a_board_autopilot_still_works_and_nothing_fails - AssertionError: 210.5: without a board, story #201 under #139 on autopilot was not labeled autopilot
> assert False
>  +  where False = has('issue', 201)
>  +    where has = <test_autopilot_board.World object at 0x7f74da331070>.has
> FAILED tests/test_autopilot_board.py::test_the_real_board_reads_whether_an_issue_or_pull_request_is_on_autopilot - Failed: 210.1: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_au

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -E "passed|failed|FAILED|ERROR" /home/runner/.claude/projects/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tool-results/bczi20w3v.txt | grep -v "^  " | cut -c1-250
```

> tests/test_failed_run_card.py |   9 +-
> FAILED tests/test_autopilot_board.py::test_pull_requests_on_autopilot_carry_the_label_so_the_view_lists_them - AssertionError: 210.4: PR #60, built for #57 on autopilot, does not carry the autopilot label
> FAILED tests/test_autopilot_board.py::test_without_a_board_autopilot_still_works_and_nothing_fails - AssertionError: 210.5: without a board, story #201 under #139 on autopilot was not labeled autopilot
> FAILED tests/test_autopilot_board.py::test_the_real_board_reads_whether_an_issue_or_pull_request_is_on_autopilot - Failed: 210.1: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_autopilot_board.py::test_the_real_board_finds_the_open_pull_request_of_an_issue - Failed: 210.1: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_autopilot_board.py::test_the_real_board_reads_back_the_pill_it_sets - Failed: 210.3: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_autopilot_board.py::test_the_real_board_puts_the_autopilot_label_on_and_off_a_pull_request - Failed: 210.4: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_autopilot_board.py::test_the_real_board_lists_its_views_and_adds_the_autopilot_table_view - Failed: 210.4: the real Board takes no rest= call yet, so it cannot reach GitHub's REST API
> FAILED tests/test_autopilot_board.py::test_switching_autopilot_on_reac

**Agent:** I've confirmed all 17 of the planner's new tests fail today because the feature is missing. Next I'm reading the tests to check they actually prove each promise.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,330p tests/test_autopilot_board.py
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
>     .label(kind, n, on)                put the `autopilot` label on (

`9. Bash`
```
cd /home/runner/work/dokima/dokima; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tasks/bdwomu36o.output | cut -c1-300; sed -n 330,679p tests/test_autopilot_board.py
```

> +     '"criterion": "N.k" or "missing"}',
>     )
> 21 failed, 335 passed in 123.27s (0:02:03)
> 
> [exited with code 0]
> 
> def test_switching_autopilot_never_hides_needs_you(record_property, make):
>     """Switching autopilot on or off while the card waits on the owner leaves Needs you, so no card shows both or loses it.
> 
>     #57 and PR #60 show Needs you. Adding the `autopilot` label keeps Needs you on both; removing it keeps Needs you
>     on both. A card off autopilot that shows Autopilot by mistake loses it, so the switch does act."""
>     record_property("proves", "210.3")
>     w = make(labels={("issue", 57): {LABEL}}, prs={57: 60},
>              cards={("issue", 57): {"Status": "Plan", "Action": "Needs you"}, ("pr", 60): {"Status": "Review", "Action": "Needs you"}})
>     board.sync("issues", label_event("labeled", LABEL, [LABEL], 57), SPEC, REPO)
>     for kind, n in (("issue", 57), ("pr", 60)):
>         assert w.action(kind, n) == "Needs you", f"210.3: switching autopilot on replaced Needs you on {kind} #{n} with {w.action(kind, n)!r}"
>     w.labels[("issue", 57)] = set()
>     board.sync("issues", label_event("unlabeled", LABEL, [], 57), SPEC, REPO)
>     for kind, n in (("issue", 57), ("pr", 60)):
>         assert w.action(kind, n) == "Needs you", f"210.3: switching autopilot off cleared Needs you on {kind} #{n}"
>     w.cards[("issue", 58)] = {"Status": "Plan", "Action": "Autopilot"}
>     board.sync("issues", label_event("unlabeled", LABEL, [], 58), SPEC, REPO)
>     assert w.action("issue", 58)

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -E "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tasks/bdwomu36o.output | grep -v test_autopilot_board | cut -c1-300; git diff main...HEAD -- tests/test_board.py tests/test_failed_run_card.py
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

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -E "FAILED|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/40f7b6b7-2e4e-4843-a031-acc9776ed76f/tasks/bdwomu36o.output | cut -c1-200 | grep -v autopilot_board | head -20
```

> tests/test_failed_run_card.py |   9 +-
> 17 failed in 0.60s
> 21 failed, 335 passed in 123.27s (0:02:03)

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 500 python -m pytest -q -rf --deselect tests/test_autopilot_board.py -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-250
```

> Every cancelled run (including one cancelled after its blocking review had passed code's check, which the river
>         would otherwise send back to the planner), a review code rejected and a run whose tools failed to install must
>         make no call that starts or re-runs a run, and each must still have been seen as cancelled or failed. Beside them,
>             assert r.failed, f"188.3 ({name}): setup: the run did not fail:\n{r.tail()}"
> E         ,\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"block\",\n  \"summary\": \"
> FAILED tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure - AssertionError: 188.3: a blocking plan review that nobody cancelled no longer starts the planner: []
>   ,\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Proposed a split into two stories.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"plan\",\n  \"round\": 1,\n  \"verdict\": \"block\",\n  \"summary\": \"57.1 has
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner'
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - 

`13. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree add -q /tmp/mainwt main 2>&1; cd /tmp/mainwt && timeout 300 python -m pytest -q -p no:cacheprovider tests/test_fixer.py tests/test_handback_check.py tests/test_cancelled_run.py 2>&1 | tail -3 | cut -c1-200; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt
```

> assert (0 == 1)
>  +  where 0 = len([])
> 4 failed, 14 passed in 8.87s

**Agent:** The 4 other failing tests fail on main too, so they're unrelated. Now checking that the GitHub create-view call the plan relies on actually exists.

`14. ToolSearch`
```
{"query": "select:WebFetch", "max_results": 1}
```

> 

`15. WebFetch`
```
{"url": "https://docs.github.com/en/rest/projects/views", "prompt": "Does this page document an endpoint to create a project view? Give the exact method, path, body parameters (name, layout values, filter), and required token permissions."}
```

> Yes. The page documents creating a project view with:
> 
> - **Method and paths:** `POST /orgs/{org}/projectsV2/{project_number}/views` for organization-owned projects, or `POST /users/{user_id}/projectsV2/{project_number}/views` for user-owned projects.
> - **Body parameters:**
>   - `name` (string, required): the view's name.
>   - `layout` (string, required): the view's layout. The page says it "Can be one of: `table`, `board`, `roadmap`".
>   - `filter` (string, optional): a filter query for the view. The page refers to a separate "Filtering projects" article for syntax.
>   - Other optional fields are `visible_fields`, `sort_by`, `group_by`, and `vertical_group_by`.
> - **Token permissions:** The page does not list required token permissions or scopes. It only says most endpoints use an `Authorization: Bearer <YOUR-TOKEN>` header, so you'll need to check GitHub's authentication documentation for the scopes this endpoint requires.

`16. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added seven tests that run the real board against a stand-in GitHub: reading autopilot from labels, finding an issue's open pull request, reading back the card's pill, labelling a pull request, and adding the view.",
          "The planner named GitHub's call for adding a view (POST /orgs/{org}/projectsV2/{number}/views) in 210.4, with a test for when GitHub refuses it.",
          "The planner taught five existing board tests' stand-in GitHub the new reads, with no assertion changed."],
  "decided": ["When GitHub refuses the Autopilot view, the pills and labels are still set and the board run fails with a message naming the view.",
              "The owner adds the Autopilot option to the Action field once by hand, and AGENTS.md says so."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves each promise against the real board, and GitHub does have a call that adds a table view, so code can add the Autopilot view.",
 "blockers": [],
 "notes": [
  {"text": "The four tests failing outside this plan (test_fixer, test_handback_check, test_cancelled_run) fail the same way on main, so they are not this plan's doing.",
   "evidence": "pytest -q on main in a separate checkout: 4 failed, 14 passed in tests/test_fixer.py, tests/test_handback_check.py and tests/test_cancelled_run.py; on this branch: 21 failed = these 4 + the 17 new tests"},
  {"text": "All 17 new tests fail today because the feature is missing: the real Board takes no rest= call yet, there is no pill, and no label or view is added.",
   "evidence": "pytest -q tests/test_autopilot_board.py: 17 failed, e.g. '210.4: PR #60, built for #57 on autopilot, does not carry the autopilot label' and '210.1: the real Board takes no rest= call yet'"},
  {"text": "The GitHub App may need the organization projects write permission for the view call. If it lacks it, 210.4 makes the board run fail a
```

> rc=0

**Agent:** I approved the plan for #210. Both blockers from the last round are fixed, and the hand-back passed both checks.

- **B1 (tests only used a stand-in board): fixed.** Seven new tests run the real board, with only GitHub faked. They check that the board:
  - tells whether an issue or pull request is on autopilot;
  - finds an issue's open pull request;
  - reads back the pill on a card;
  - puts the autopilot label on and off a pull request;
  - adds the view.

  A version that does nothing turns these tests red.
- **B2 (no named way to create the view): fixed.** I checked GitHub's docs, and the call exists: `POST /orgs/{org}/projectsV2/{project_number}/views` takes a name, a `table` layout and a filter. So code can add the Autopilot view, and that criterion doesn't need to be a manual setup step. If GitHub refuses the call, the pills and labels are still set and the board run fails with a message naming the view.

**Tests:** all 17 new tests fail today because the feature is missing, which is what should happen before any code exists. The plan is also clean on scope:
- All eight of your asks map to a criterion.
- The board workflow (`board.yml`) is explicitly left unchanged.
- `dokima/card.py` is untouched.

**Two things to know:**
- **Unrelated failing tests:** four tests already fail on main, in `test_fixer.py`, `test_handback_check.py` and `test_cancelled_run.py`. Two of them say "asks must list every ask". I proposed this as a separate issue, because those red tests hide real failures on every run.
- **Possible permission gap:** the GitHub App may need permission to write to the organization's projects for the view call. If it lacks it, the board run fails and says why, as the plan intends.

The review is in `/tmp/dokima-out/review.json`.
