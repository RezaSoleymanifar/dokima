# reviewer (plan) for #282

Run: https://github.com/dokima-dev/dokima/actions/runs/37858760814

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (48.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4b570aac-ce40-4c2e-b264-89a3c2767152/tool-results/b1r1k1hlb.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct  8 23:19 .
> drwxrwxrwt 18 root   root    4096 Oct  8 23:19 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 23:19 in
> -rw-r--r--  1 runner runner 40226 Oct  8 23:19 issue.md
> -rw-r--r--  1 runner runner  1599 Oct  8 23:19 open_blockers.json
> -rw-r--r--  1 runner runner  6750 Oct  8 23:19 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  8 23:19 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 23:19 ..
> -rw-r--r-- 1 runner runner 5771 Oct  8 23:19 01-planner.json
> -rw-r--r-- 1 runner runner 5335 Oct  8 23:19 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7410 Oct  8 23:19 03-planner.json
> # Issue #282: Everything Dokima needs from GitHub is declared in one manifest in code
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #282](https://github.com/dokima-dev/dokima/issues/282)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" 

`2. Bash`
```
cd /tmp/pack; sed -n 20,400p issue.md | cut -c1-2000
```

> <details open><summary>From the approved plan of #280, story 1</summary>
> 
> **Part of:** #280 A drift audit compares the repo's settings with what Dokima needs and tells me what's off
> 
> **User story:** The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a test catches code that relies on anything left out.
> 
> **Acceptance criteria:**
> - One manifest module in `dokima/` declares the labels, board fields and their options, views, required check names, branch rules and app permissions Dokima needs. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - The manifest declares the Autopilot option as purple, described "Running on its own". It declares the Autopilot view's filter as `label:autopilot is:open`. The board code reads that filter from the manifest. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - A test fails when code or a workflow relies on a setting the manifest leaves out. It names the setting and the file. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - The manifest's app permissions match `dokima/app.json` exactly. Both ask for Administration read, never write, so the app can read branch rules but never change them. ([source](https://github.com/dokima-dev/dokima/issues/280))
> 
> **Non-functional:**
> - The manifest is plain data with no GitHub calls, so tests and the audit read it without a network. (Tests run on a clean machine with no secrets.)
> 
> </det

`3. Bash`
```
cd /tmp/pack; sed -n 400,700p issue.md | grep -v '^\s*$' | head -150; cat open_blockers.json; python3 -c "import json;d=json.load(open('plan.json'));print(json.dumps({k:v for k,v in d.items() if k not in()},indent=1))" | head -150
```

> - tests/test_manifest.py
> - tests/test_app.py
> - tests/test_autopilot_board.py
> </details>
> <details><summary><b>Out of scope</b></summary>
> - Comparing the manifest with the live repo, the Setup issue, fixing gaps and the daily run; those are #283, #284 and #285.
> - Changing the Autopilot view already on the board; only views the board adds from now on use the new filter. The audit (#284) or #278 fixes the existing one.
> - Moving other code (the autopilot label name, the priority labels) to read from the manifest; only the view's filter does.
> - Granting the new Administration read permission on the installed app; the owner accepts it on GitHub.
> - Working out app permissions from every GitHub call the code makes; the guard sees only a workflow's app token asking for a permission and code reading or changing a branch's rule.
> </details>
> <details><summary><b>Tests</b></summary>
> - 282.1: tests/test_manifest.py::test_the_manifest_declares_every_label_dokima_uses, tests/test_manifest.py::test_the_manifest_declares_the_board_fields_and_their_options, tests/test_manifest.py::test_the_manifest_declares_views_checks_and_branch_rules, tests/test_manifest.py::test_the_manifest_declares_the_app_permissions
> - 282.2: tests/test_manifest.py::test_the_autopilot_option_is_purple_running_on_its_own, tests/test_manifest.py::test_the_board_adds_the_autopilot_view_with_the_manifests_filter
> - 282.3: tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file, tests/test_manifest.py::te

**Agent:** Now the tests.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat 4913f5c HEAD; wc -l tests/test_manifest.py; cat tests/test_manifest.py
```

> tests/test_manifest.py | 122 ++++++++++++++++++++++++++++++++++++++++++++++---
>  1 file changed, 115 insertions(+), 7 deletions(-)
> 445 tests/test_manifest.py
> """Tests for #282: one manifest in code declares everything Dokima needs from GitHub.
> 
> The manifest is `dokima/manifest.py`, plain data read without a network:
>     LABELS        {label name: {"color": "rrggbb", "description": str}}
>     FIELDS        {board field name: {option name: {"color": GitHub option color, "description": str}}}
>     VIEWS         {view name: {"layout": "table" | "board" | "roadmap", "filter": str}}
>     CHECKS        [required check name, ...]
>     BRANCH_RULES  {branch name: {"required_checks": [check name, ...], ...}}
>     PERMISSIONS   {app permission: "read" | "write"}, the same as dokima/app.json's default_permissions
>     undeclared(root) -> [str, ...]: one line per setting the code or workflows under `root` rely on that the manifest
>         leaves out, naming the setting and the file (path relative to root, with forward slashes). It reads the
>         manifest's data when called, so a test can take an entry out and see the guard report it.
> 
> What counts as relying on a setting:
>     label       a workflow started by it (github.event.label.name == '...'), or code adding it ("labels[]": "...",
>                 labels[]=...)
>     field       code setting it: board.set(iid, "Field", "Option"); the option counts too
>     view        code adding it: add_view("Name", ...)
>     check       code looking a check r

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n 'ALL_TESTS\|DONE_WHEN\|\["name"\] ==' dokima/*.py | head -20; grep -rn "label.name\|labels\[\]\|permission-\|/protection\|rules/branches\|add_view\|\.set(" .github/workflows dokima/*.py | head -40; python -m pytest -q tests/test_manifest.py tests/test_app.py tests/test_autopilot_board.py 2>&1 | tail -30
```

> dokima/card.py:24:ALL_TESTS = "all tests"
> dokima/card.py:103:    runs.append(next((r for r in check_runs if r["name"] == ALL_TESTS), None))
> dokima/card.py:247:    all_tests = next((r for r in check_runs if r["name"] == ALL_TESTS), None)
> dokima/card.py:421:             f"{number}.3 · A failed job says why", ALL_TESTS]
> dokima/board.py:28:        if action == "labeled" and p["label"]["name"] == "plan":
> dokima/board.py:30:        elif action == "labeled" and p["label"]["name"] == "work":
> dokima/board.py:152:    if event == "issues" and p["action"] in ("labeled", "unlabeled") and p["label"]["name"] == AUTOPILOT:
> .github/workflows/worker.yml:2:run-name: "worker for #${{ github.event.issue.number }}${{ github.event.label.name != 'work' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> .github/workflows/worker.yml:13:  group: work-${{ github.event.issue.number }}-${{ github.event.label.name }}
> .github/workflows/worker.yml:21:    if: github.event.action == 'labeled' && github.event.label.name == 'work'
> .github/workflows/planner.yml:2:run-name: "planner for #${{ github.event.issue.number }}${{ github.event.label.name != 'plan' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> .github/workflows/planner.yml:12:  group: plan-${{ github.event.issue.number }}-${{ github.event.label.name }}
> .github/workflows/planner.yml:20:    if: github.event.label.name == 'plan'
> dokima/board.py:133:            self.rest("POST", path, **{"labels[]": AUTOPILOT})
> dokima

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_manifest.py 2>&1 | grep -E "^FAILED|passed|failed" | sed 's/ - .*manifest module.*/ [no manifest]/' | sort | uniq -c | head -40; python -m pytest -q 2>&1 | tail -2; grep -n "organization\|default_permissions" -A12 dokima/app.json | head -20
```

> Command did not complete within its 120s timeout and was moved to the background (ID: btpg6spga). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/4b570aac-ce40-4c2e-b264-89a3c2767152/tasks/btpg6spga.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_manifest.py 2>&1 | grep -E "^FAILED|passed|failed" | sed 's/ - .*manifest module.*/ [no manifest]/'; cat dokima/app.json | head -30
```

> Proves 282.1. The required checks are the two Dokima's merge waits on, "all tests" and "all done-whens passed", each the name of
>         "all tests" and "all done-whens passed" by name and through a constant, and reading main's branch rule both ways,
> FAILED tests/test_manifest.py::test_the_manifest_declares_every_label_dokima_uses [no manifest]
> FAILED tests/test_manifest.py::test_the_manifest_declares_the_board_fields_and_their_options [no manifest]
> FAILED tests/test_manifest.py::test_the_manifest_declares_views_checks_and_branch_rules [no manifest]
> FAILED tests/test_manifest.py::test_the_manifest_declares_the_app_permissions [no manifest]
> FAILED tests/test_manifest.py::test_the_autopilot_option_is_purple_running_on_its_own [no manifest]
> FAILED tests/test_manifest.py::test_the_board_adds_the_autopilot_view_with_the_manifests_filter [no manifest]
> FAILED tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file[.github/workflows/deploy.yml] [no manifest]
> FAILED tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file[dokima/ship.py] [no manifest]
> FAILED tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file[dokima/stage.py] [no manifest]
> FAILED tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file[dokima/mine.py] [no manifest]
> FAILED tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file[dokima/rest_label.py] [no manifest]
> FAILED tests/test_manifest.py::test_

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "^    name:" .github/workflows | head; pkill -f "pytest -q$" ; true
```

> .github/workflows/full-suite.yml:13:    name: all tests
> .github/workflows/done-whens.yml:12:    name: list done-whens
> .github/workflows/done-whens.yml:26:    name: ${{ matrix.name }}
> .github/workflows/done-whens.yml:61:    name: all done-whens passed

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner widened criterion 3 so the guard also names a required check, a branch rule or an app permission the manifest leaves out, with the file relying on it.",
          "The planner added tests that take \"all tests\" out of the manifest and expect the guard to name it and dokima/card.py, and take main or administration out and expect them named."],
  "decided": ["The guard works out app permissions only from a workflow's app token and from reading or changing a branch's rule, not from every GitHub call."],
  "open": ["The planner asks the owner whether the guard should work out the permission behind every GitHub call the code makes."]},
 "verdict": "approve",
 "summary": "The plan now covers every kind of setting the owner named, including required checks, branch rules and app permissions, and every new test fails today because the manifest does not exist yet; one question about how far the permission check reaches waits for the owner.",
 "blockers": [],
 "notes": [
  {"text": "Every new test fails today because dokima/manifest.py is missing, and the three changed Autopilot view tests fail because the board still adds the filter label:autopilot.",
   "evidence": "pytest -q tests/test_manifest.py: 26 failed, each 'there is no manifest module, dokima/manifest.py'; tests/test_autopilot_board.py: filter 'label:autopilot' vs 'label:autopilot is:open'."},
  {"text": "The check test runs against the real repo: dokima/card.py looks up \"all tests\" through its constant ALL_TESTS, which is the case the plan names.",
   "evidence": "dokima/card.py:24 ALL_TESTS = \"all tests\"; dokima/card.py:103 r[\"name\"] == ALL_TESTS; tests/test_manifest.py::test_the_guard_catches_a_check_taken_out_of_the_manifest"},
  {"text": "The planner's question is backed by evidence: the board calls organization projects, a permission dokima/app.json does not list, so a guard that maps every cal
```

> (Bash completed with no output)

**Agent:** I approved the plan for #282. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Earlier blocker B1 is fixed.** Criterion 3 now covers required checks, branch rules and app permissions, not just labels, board fields, options and views. One new test takes "all tests" out of the manifest and expects the guard to name it along with `dokima/card.py`. That file really does look the check up by name (`dokima/card.py:103`). Other tests do the same for the `main` branch rule and the Administration permission.
- **The new tests fail for the right reason.** All 26 tests in `tests/test_manifest.py` fail with "there is no manifest module". Separately, the board still adds the old Autopilot view filter, `label:autopilot` instead of `label:autopilot is:open`, so some of the existing tests the plan changed fail today too.
- **I did not accept the planner's one question,** so it will stop for you even though the issue is on autopilot. The question asks whether the test should work out the app permission behind every GitHub call the code makes. The planner assumes it shouldn't. That narrows your words, "a test fails when code or a workflow relies on a setting the manifest leaves out", and nothing you wrote backs the narrower reading. The planner's reason holds up: the board already uses organization projects, which `dokima/app.json` doesn't list, so mapping every call would fail on the repo as it is today.

All six of your asks from the issue map to a criterion; none is missing.
