# reviewer (plan) for #284

Run: https://github.com/dokima-dev/dokima/actions/runs/37886911155

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #284: The audit fixes harmless gaps itself and only reports permissions and branch rules
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 283, 285 -->
> **Backlog**
> 
> [issue #284](https://github.com/dokima-dev/dokima/issues/284)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #283
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #285
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><su

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l dokima/audit.py tests/test_audit*.py tests/fake_gh.py; grep -n "Action field\|one-time step\|audit" AGENTS.md
```

> commit c65dfbe262f1e47b74f248f31d7e55424671b482
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:05:10 2026 +0000
> 
>     planner for #284 (run 37885351778)
> 
>  tests/fake_gh.py            | 281 ++++++++++++++++++++++++++++-
>  tests/test_audit.py         |  91 ++++++++--
>  tests/test_audit_fix.py     | 420 ++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_audit_fix_cli.py | 228 ++++++++++++++++++++++++
>  4 files changed, 1006 insertions(+), 14 deletions(-)
>    290 dokima/audit.py
>    549 tests/test_audit.py
>    293 tests/test_audit_cli.py
>    420 tests/test_audit_fix.py
>    228 tests/test_audit_fix_cli.py
>    652 tests/fake_gh.py
>   2432 total
> 79:- One Autopilot view, a table filtered to `label:autopilot is:open`, lists every open issue and pull request on autopilot; merged and closed ones keep the label but leave the view. Code adds it the first time a tree goes on autopilot, from the board run of the tree's top issue only, and a refused view fails that run naming it. The board run of a merge changes an Autopilot view still filtered to the old `label:autopilot` to `label:autopilot is:open`, leaves any other filter alone, and fails naming the view if GitHub refuses. The Autopilot option of the Action field is a one-time step on the board, like Needs you; code never edits the field's options.

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_audit_fix.py tests/test_audit_fix_cli.py tests/test_audit.py 2>&1 | tail -40
```

> assert ({'create_issue', 'needs_you', 'pin_issue'} & {'create_label', 'create_view', 'set_options', 'update_label', 'update_view'})
> FAILED tests/test_audit_fix_cli.py::test_the_command_fixes_labels_options_and_views_and_lists_them_as_fixed - AssertionError: 284.1: the plan label is None on GitHub, not the manifest's
>   unsupported calls: []
>   writes: [{'kind': 'create', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'pin', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'board', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'board', 'repo': 'acme/widgets', 'number': 101}]
> assert None == {'color': '1d76db', 'description': 'Starts the planner'}
>  +  where None = <built-in method get of dict object at 0x7f68bbeceb00>('plan')
>  +    where <built-in method get of dict object at 0x7f68bbeceb00> = {'work': {'color': '0e8a16', 'description': 'Old words'}, 'autopilot': {'color': '8250df', 'description': 'Running on ...205', 'description': 'Priority: blocks other work'}, 'high': {'color': 'd93f0b', 'description': 'Priority: high'}, ...}.get
> FAILED tests/test_audit_fix_cli.py::test_the_command_adds_a_missing_view_and_closes_once_all_is_fixed - AssertionError: 284.1: the missing Autopilot view was not added: {}
>   unsupported calls: []
>   writes: [{'kind': 'create', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'pin', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'board', 'repo': 'acme/widgets', 'number': 101}, {'kind': 'board', 'repo': 'acme/widgets', 'number': 101}]
> assert None 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_audit_fix.py tests/test_audit_fix_cli.py tests/test_audit.py 2>&1 | grep -E "^(FAILED|ERROR)" ; cat dokima/audit.py
```

> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_label_is_set_and_listed_as_fixed - AssertionError: 284.1: the plan label is None, not the manifest's {'color': '1d76db', 'description': 'Starts the planner'}
> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_board_option_is_set_and_listed_as_fixed - AssertionError: 284.1: the Autopilot option of Action is None, not the manifest's {'color': 'PURPLE', 'description': 'Running on its own'}
> FAILED tests/test_audit_fix.py::test_a_missing_or_changed_view_is_set_and_listed_as_fixed - AssertionError: 284.1: the missing Autopilot view was not added as the manifest has it: None
> FAILED tests/test_audit_fix.py::test_a_run_that_fixes_everything_lists_the_fixes_and_closes_the_setup_issue - AssertionError: 284.1: the missing plan label was not created
> FAILED tests/test_audit_fix.py::test_a_missing_board_field_is_reported_not_created - AssertionError: 284.1: the missing Autopilot option should be listed as fixed, as 'Option `Autopilot` of the board field `Action` is missing; Dokima needs it with color `PURPLE` and description `Running on its own`.'; fixed part: []
> FAILED tests/test_audit_fix.py::test_permissions_and_branch_rules_are_only_reported - AssertionError: 284.2: the plan label should be listed as fixed, as 'Label `plan` is missing; Dokima needs it with color `1d76db` and description `Starts the planner`.'; fixed part: []
> FAILED tests/test_audit_fix.py::test_a_missing_branch_rule_is_only_reported - AssertionError: 284.2

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_audit_fix.py
```

> """Tests for #284: the audit fixes declared labels, options and views, and only reports the rest.
> 
> The audit (`dokima/audit.py`, from #283) compares the manifest with the live repo and reports on one Setup issue. These
> tests run `audit.run` against the in-memory faked GitHub of tests/test_audit.py, whose docstring lists every read and
> write the audit is expected to use: since #284 it may create and update labels, replace a board field's options and
> create and update views. It has no write for branch rules or app permissions at all.
> 
> How the Setup issue is expected to read: first what is still off, one line each; then one line holding the word
> "fixed" (nothing before it says fixed); then each setting this run fixed, on its own line, worded exactly as the
> audit's compare() line for it. parts() below splits a body that way. When everything off was fixed, the Setup issue
> still lists the fixes, is not marked Needs you, and is closed with the one line saying nothing is off.
> """
> import copy
> import os
> import re
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> sys.path.insert(0, ROOT)
> sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> from dokima import manifest  # noqa: E402
> from test_audit import (BOARD, FORBIDDEN, BROKEN, REPO, GitHub, audit, body_lines, codeowners,  # noqa: E402
>                         one_line, open_setup)
> 
> ISSUE_WRITES = {"create_issue", "edit_issue", "comment", "close_issue", "pin_issue", "needs_you"}
> FIX_WRITES = {"

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_audit.py | head -250
```

> commit c65dfbe262f1e47b74f248f31d7e55424671b482
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:05:10 2026 +0000
> 
>     planner for #284 (run 37885351778)
> 
> diff --git a/tests/test_audit.py b/tests/test_audit.py
> index ce7d4bf..29f9d8a 100644
> --- a/tests/test_audit.py
> +++ b/tests/test_audit.py
> @@ -25,6 +25,17 @@ What the faked GitHub offers, and the audit is expected to use (a read may raise
>      close_issue(repo, n)
>      pin_issue(repo, n)
>      needs_you(repo, n)        marks the issue's card Needs you on the board
> +
> +Since #284 the audit also fixes declared labels, board options and views itself, through these (a write may raise
> +subprocess.CalledProcessError too, when GitHub refuses it):
> +    create_label(repo, name, color, description)
> +    update_label(repo, name, color, description)
> +    set_options(field, options)   replaces the field's options with the list given, as GitHub does: each option is
> +                                  {"id": id or None, "name", "color", "description"}; one passed with its id keeps it,
> +                                  one without gets a new id, and one left out is deleted, clearing every card on it
> +    create_view(name, layout, filter)
> +    update_view(name, layout, filter)
> +fields() gives each option its "id" too. Board writes are kept with BOARD in place of a repo: the board is the org's.
>  """
>  import copy
>  import importlib
> @@ -41,6 +52,7 @@ from dokima import manifest  # noqa: E402
> 

**Agent:** Grading the plan for #284: the 19 new tests fail today as they should. Now checking the faked GitHub, the command-line tests and the asks.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "updateProjectV2Field\|singleSelectOptions\|createProjectV2View\|ProjectV2View" dokima/ | head; git show HEAD -- tests/fake_gh.py | grep -n "^+.*def \|updateProjectV2\|singleSelect\|View\|labels" | head -60
```

> dokima/board.py:148:        self.q('mutation($v:ID!,$f:String!){updateProjectV2View(input:{viewId:$v,filter:$f}){projectV2View{id}}}', v=view_id, f=filter)
> 15:+    gh api -X POST repos/OWNER/REPO/labels -f name=.. -f color=.. -f description=..   creates a label
> 16:+    gh api -X PATCH repos/OWNER/REPO/labels/NAME [-f new_name=..] -f color=.. -f description=..   edits it
> 17:+    gh api -X DELETE repos/OWNER/REPO/labels/NAME                                      deletes it
> 23:-        updateProjectV2ItemPosition, updateProjectV2ItemFieldValue and pinIssue.
> 24:+        updateProjectV2ItemPosition, updateProjectV2ItemFieldValue and pinIssue;
> 25:+        updateProjectV2Field(input:{fieldId:, singleSelectOptions:[{id:, name:, color:, description:}]}), with the
> 29:+        deleted, clearing every card that had it; updateProjectV2View(input:{viewId:, filter:, layout:, name:});
> 30:+        and deleteProjectV2Field / deleteProjectV2View, which delete.
> 32:+Writes to labels, fields and views are logged under "writes" as kinds label, label_delete, field, field_delete, view
> 35:-O_<Field>_<Option with spaces as _>, the project PVT_1. Views come back with GitHub's layouts (TABLE_LAYOUT, ...).
> 37:+the project PVT_1, a view PVTV_<name with spaces as _>. A card's value is state["items"][item][Field] = option id. Views come back with GitHub's layouts (TABLE_LAYOUT, ...).
> 52:+def view_id(name):
> 57:+def write(state, kind):
> 58:+    """Log one write to the repo's labels or the board."""
> 62:+def refus

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p tests/fake_gh.py; grep -n "def add_view" -A30 tests/fake_gh.py; grep -n "add_view\|views" tests/fake_gh.py | head -30
```

> """A fake `gh` for the drift audit's command tests, keeping GitHub in one JSON file.
> 
> tests/test_audit_cli.py copies this file onto PATH as `gh` and runs `python3 -m dokima.audit OWNER/REPO` against it.
> The state lives in the file named by FAKE_GH_STATE; every call is logged there under "calls", every write under
> "writes" (kind, repo, number), and every call this fake does not understand under "unsupported", where it also exits 1
> so the audit sees a refused call. A read listed under "fail" answers as GitHub does when it refuses: GitHub's reason on
> stderr ("gh: ... (HTTP 403)") and exit 1.
> 
> What it answers (OWNER/REPO is the state's repo; any other repo is logged as unsupported):
>     gh api [-X GET] repos/OWNER/REPO/labels[?...]                       labels, as GitHub's REST list
>     gh api [-X GET] repos/OWNER/REPO/branches/main/protection[/required_status_checks]
>                                                                         main's rule; 404 "Branch not protected" if none
>     gh api [-X GET] repos/OWNER/REPO/installation                       the app's {"permissions": {...}}
>     gh api [-X GET] repos/OWNER/REPO/issues[?state=...&labels=...]      issues (open unless state says otherwise)
>     gh api [-X GET] repos/OWNER/REPO/issues/N[/comments]
>     gh api [-X POST] repos/OWNER/REPO/issues -f title=.. -f body=.. [-f labels[]=..]   opens an issue
>     gh api -X PATCH repos/OWNER/REPO/issues/N -f body=.. | -f state=closed            edits or closes it
>     gh api [-X POST]

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "projectsV2\|/views" dokima/ | head; sed -n 1,80p tests/test_audit_fix_cli.py
```

> dokima/board.py:151:        self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)
> dokima/manifest.py:101:    (r"orgs/[^/]+/projectsV2(/|$)", "organization_projects"),
> """Tests for #284: `python3 -m dokima.audit OWNER/REPO` fixes declared labels, options and views through `gh`.
> 
> The in-memory tests in tests/test_audit_fix.py prove what the audit decides; these prove it really writes GitHub the
> way GitHub works. Each runs the command from outside, as tests/test_audit_cli.py does, against the fake `gh` in
> tests/fake_gh.py, whose docstring lists every call it answers. The fake replaces a field's options the way GitHub's
> updateProjectV2Field does: an option passed without its id gets a new one, and an option left out is deleted, which
> clears every card on it. So keeping the owner's options and cards can only pass by sending each kept option back with
> its id.
> 
> How the command is expected to fix things (any one way the fake answers):
>     a label             gh api -X POST repos/OWNER/REPO/labels or -X PATCH repos/OWNER/REPO/labels/NAME
>                         (or gh label create / gh label edit)
>     a board option      gh api graphql, updateProjectV2Field with every option of the field, kept ones with their ids
>     a view              gh api -X POST orgs/OWNER/projectsV2/1/views to add it, updateProjectV2View to change it
> The Setup issue reads as tests/test_audit_fix.py describes: what is still off, then a line holding the wo

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python -m pytest -q -x --deselect tests/test_audit_fix.py --deselect tests/test_audit_fix_cli.py 2>&1 | tail -3; grep -n "def check_review\|asks\|criterion" dokima/agent.py | head -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bsh7oolj6). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, I'll write the hand-back.

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote five criteria and one non-functional rule, with 19 new tests: in-memory tests of the audit and tests that run the command against a fake gh.",
   "It changed two tests of #283 so they report through permissions and branch rules, which the audit now only reports."
  ],
  "decided": [
   "The Setup issue lists every fix; when nothing is left off it is closed with the line saying nothing is off and is never marked Needs you.",
   "A whole missing board field is only reported, not created."
  ],
  "open": [
   "Two questions for the owner: what happens when a run fixes everything, and whether a missing board field is created."
  ]
 },
 "verdict": "approve",
 "summary": "The plan keeps every ask of the issue and each test fails today because the audit cannot fix anything yet; the question on a missing board field needs the owner's answer.",
 "blockers": [],
 "notes": [
  {
   "text": "The tests prove option ids are kept only against a fake that accepts an id on each option it is given. If GitHub's updateProjectV2Field drops ids in practice, cards could lose their values on the real board even with every test green, so the worker should check this against GitHub before shipping.",
   "evidence": "tests/fake_gh.py docstring: 'an option passed with its id keeps it'; tests/test_audit.py GitHub.set_options does the same; no code in dokima/ calls updateProjectV2Field yet (grep finds none)."
  },
  {
   "text": "If the owner answers the field question with 'create it', the test test_a_missing_board_field_is_reported_not_created would have to be turned around, and the out-of-scope line about missing fields removed.",
   "evidence": "tests/test_audit_fix.py::test_a_missing_board_field_is_reported_not_created asserts 'Priority' not in g.field_map after the run."
  }
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "A declared label, board option 
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`12. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every ask has a criterion and every new test fails today for the right reason; the missing-field question needs the owner."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 284 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

`13. Bash`
```
sleep 100; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output
```

> <tool_use_error>Blocked: sleep 100 followed by: tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** I'll wait for the full test run to finish before closing.

`14. Bash`
```
until grep -qE "passed|failed|error" /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output; do sleep 5; done; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output
```

> 910:        if not isinstance(b, dict) or not filled(b.get("criterion")):
> 
> [exited with code 0]

`15. Bash`
```
head -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/78b0a1c0-8908-409e-b493-3e664dc85731/tasks/bsh7oolj6.output
```

> ........................................................................ [ 97%]
> ...............                                                          [100%]
> 735 passed, 19 deselected in 271.02s (0:04:31)
> 410:                   + bullets(h.get("blockers"), lambda b: f"{b.get('id')} on {b.get('criterion')}: {b.get('problem', '')} "
> 415:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]

**Agent:** I approved the plan for #284, with no blockers. One of its two questions has to go to you before the work starts. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What I checked**
- **Your asks:** each of the seven asks in the issue has its own criterion (284.1 to 284.6). Nothing was dropped, added or narrowed.
- **New tests:** all 19 new tests fail on the current code for the right reason: the audit can't fix anything yet, and AGENTS.md still has the old line saying the Autopilot option is a one-time step code never edits. None of them fail from a crash or a bad path.
- **The rest of the suite:** the other 735 tests pass, including the two #283 tests the planner changed.

**The planner's two questions**
- **Accepted:** when a run fixes everything, the Setup issue still lists the fixes, then closes without Needs you. This follows your words "The Setup issue lists it as fixed." It adds nothing new to build or pay for.
- **Not accepted:** the planner assumed a whole missing board field (Status, Action or Priority) is only reported, never created. Your issue names labels, options and views, but it also says you should "only be asked about what touches permissions or branch rules", and reporting a missing field breaks that. Creating a field or not also changes what the audit writes on the board. Because #284 is on autopilot, this question now stops for your answer.

**Notes for the worker (not blockers)**
- **Keeping cards:** the tests that prove options keep their ids and cards keep their values run against a fake GitHub that accepts an id on each option. If GitHub's real call that replaces a field's options drops those ids, cards could lose their values on the real board while every test passes. The worker should check this against GitHub.
- **If you answer "create the field":** the test that asserts the field stays missing would have to be turned around, and the out-of-scope line about missing fields removed.
