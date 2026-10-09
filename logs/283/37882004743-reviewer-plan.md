# reviewer (plan) for #283

Run: https://github.com/dokima-dev/dokima/actions/runs/37882004743

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (48.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tool-results/bt5ucbtxp.txt
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
> # Issue #283: A drift audit reports what is off on one pinned Setup issue, and stays silent otherwise
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #280, story 2</summary>
> 
> **Part of:** #280 A drift audit compares the repo's settings with what Dokima needs and tells me what's off
> 
> **User story:** When a setting drifts, the owner sees it on one pinned Setup issue, marked Needs you, one plain line per setting; when nothing is off, the audit leaves no trace.
> 
> **Acceptance criteria:**
> - The audit compares the manifest with the repo's live settings. Each difference gets one plain line saying what is off and what Dokima needs. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - Drift goes on one pinned Setup issue, marked Needs you on the board. Later runs update that same issue instead of opening another. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - A run that finds nothing off posts nothing. A Setup issue left open by an earlier run is closed with one line saying nothing is off. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - The Setup issue mentions only the repo's own code ow

`2. Bash`
```
cd /tmp/pack; sed -n 30,400p issue.md | cut -c1-3000
```

> ### dokima-runtime on issue #283 (2026-10-09T03:40:00Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue and asks you 1 question.
> 
> **User story:** When a setting drifts, the owner sees it on one pinned Setup issue marked Needs you, one plain line per setting; when nothing is off, the audit leaves no trace.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 
> 1. The audit compares the manifest with the repo's live labels, board options and views, branch rules and app permissions. Each difference, including a missing setting, a missing or extra required check and a broader permission, gets one plain line naming the setting, what it is now and what Dokima needs. Settings that match, and labels, options and views the manifest does not declare, get no line.
> 2. When something is off, it is listed on one Setup issue, pinned and marked Needs you on the board. Later runs update that same open issue with what is off now instead of opening another.
> 3. A run that finds nothing off, with no Setup issue open, writes nothing to GitHub. A Setup issu

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('plan.json'));print(json.dumps({k:v for k,v in d.items()},indent=1))" | head -150; cd /home/runner/work/dokima/dokima; git show --stat HEAD HEAD~1 | cat
```

> [
>  {
>   "id": "B1",
>   "criterion": "283.1",
>   "test": null,
>   "problem": "Criterion 1 promises the audit compares the manifest with the repo's live settings, and 2 promises a pinned issue marked Needs you on the board, but no test touches anything except the in-memory fake. A worker could ship compare() and run() with no code that reads labels, board fields and views, main's rule or the app's permissions from GitHub, and no code that pins or sets the Action field, and all 14 tests would pass. The scope lists no place for that code either, and #285 only adds the workflow that runs the audit.",
>   "evidence": "tests/test_audit.py: every test passes `GitHub()` from the test file itself (class GitHub, lines ~62-130) into audit.compare or audit.run; `grep -n 'gh\\b\\|subprocess.run\\|PATH' tests/test_audit.py` finds no call to the real tool. Plan out_of_scope: \"The workflow that runs the audit daily ... that is #285\".",
>   "fix": "Add a criterion (or extend 1 and 2) that `python3 -m dokima.audit <repo>` runs the audit against GitHub itself, and a test that runs it with a fake `gh` on PATH: it must read the labels, the board's fields and views, main's rule and the app's permissions through `gh`, and on drift create, pin and mark the Setup issue Needs you through `gh`, all on that repo, failing with the criterion number when any of those calls is missing.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "283.1",
>   "test": "tests/test_audit.py::test_each_difference_gets_one_

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_audit_cli.py; cat tests/fake_gh.py
```

> <persisted-output>
> Output too large (32.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tool-results/b1fk6xmqf.txt
> 
> Preview (first 2KB):
> """Tests for #283: `python3 -m dokima.audit OWNER/REPO` audits the live repo through `gh`.
> 
> The in-memory tests in tests/test_audit.py prove what the audit decides. These prove it really reads and writes GitHub:
> each runs the command from outside, the way a workflow does, with a fake `gh` (tests/fake_gh.py) first on PATH that
> keeps GitHub in a JSON file and logs every call. The command is run from a folder holding .github/CODEOWNERS, with
> DOKIMA_BOARD naming the org's board ("acme/1") and the dokima package on PYTHONPATH. The fake's docstring lists every
> call it answers; any other call is logged as unsupported and refused, and the failure message shows it.
> 
> How the command is expected to read GitHub:
>     labels              gh api repos/OWNER/REPO/labels
>     board fields, views gh api graphql, organization(login:){projectV2(number:){fields views}}
>     main's rule         gh api repos/OWNER/REPO/branches/main/protection (404 "Branch not protected": no rule)
>     the app's permissions  gh api repos/OWNER/REPO/installation, its "permissions"
> and to write only the Setup issue: open, edit, comment, close and pin it (gh api or gh issue), and mark its card Needs
> you through GraphQL (addProjectV2ItemById, then updateProjectV2ItemFieldValue on the Action field).
> """
> import 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_audit.py; cat dokima/manifest.py | head -150; ls dokima
```

> <persisted-output>
> Output too large (31KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tool-results/bhis4n4d0.txt
> 
> Preview (first 2KB):
> """Tests for #283: the drift audit reports on one pinned Setup issue, else stays silent.
> 
> The audit is `dokima/audit.py`. It compares the manifest (`dokima/manifest.py`) with the repo's live settings and
> reports the difference on one Setup issue. Everything it reads from or writes to GitHub goes through one object it is
> given, so these tests hand it a faked GitHub kept in memory. What the audit is expected to offer:
> 
>     audit.compare(github, repo) -> [str, ...]
>         one plain line per setting that differs from the manifest or could not be read; empty when all match
>     audit.run(github, repo, root=".") -> issue number or None
>         compares, then reports on the Setup issue: opens it (pinned, Needs you) or updates the open one when something
>         is off; closes an open one with one line when nothing is; does nothing at all when nothing is off and none is
>         open. Code owners are read from root/.github/CODEOWNERS. Returns the Setup issue it touched, or None.
> 
> What the faked GitHub offers, and the audit is expected to use (a read may raise subprocess.CalledProcessError, as
> `gh` does, carrying GitHub's reason in stderr):
>     labels(repo)              {name: {"color": "rrggbb", "description": str}}
>     fields()                  the board's {field: {option: 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 40,300p tests/test_audit_cli.py
```

> "protection": {b: list(r["required_checks"]) for b, r in manifest.BRANCH_RULES.items()},
>             "permissions": copy.deepcopy(manifest.PERMISSIONS), "fail": {}, "issues": {}, "next": 100,
>             "items": {}, "calls": [], "writes": []}
> 
> 
> def drifted():
>     """A fake GitHub off in one setting of each kind the audit reads."""
>     s = clean()
>     del s["labels"]["plan"]
>     s["labels"]["work"]["description"] = "Old words"
>     del s["fields"]["Action"]["Autopilot"]
>     s["fields"]["Priority"]["High"]["color"] = "RED"
>     s["views"]["Autopilot"]["filter"] = "label:autopilot"
>     s["protection"]["main"] = ["all tests"]
>     s["permissions"]["issues"] = "read"
>     return s
> 
> 
> class Audit:
>     """One repo root with CODEOWNERS and a fake gh, where the audit command runs."""
> 
>     def __init__(self, tmp_path, state, owners="* @alice\n"):
>         self.root = tmp_path / "repo"
>         (self.root / ".github").mkdir(parents=True)
>         (self.root / ".github" / "CODEOWNERS").write_text(owners)
>         self.bin = tmp_path / "bin"
>         self.bin.mkdir()
>         gh = self.bin / "gh"
>         gh.write_text(f"#!{sys.executable}\n" + open(os.path.join(ROOT, "tests", "fake_gh.py")).read())
>         gh.chmod(0o755)
>         self.file = tmp_path / "github.json"
>         self.save(state)
> 
>     def save(self, state):
>         """Replace the fake GitHub's state."""
>         self.file.write_text(json.dumps(state))
> 
>     def state(self):
>         """The fake GitHub's state now."""
>         return json.loa

**Agent:** Reviewing the revised plan for #283: I've read the new command tests and am now checking the fake gh and running the tests.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/fake_gh.py | head -380
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

`8. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima/audit.py 2>&1; python3 -m pytest -q tests/test_audit.py tests/test_audit_cli.py 2>&1 | grep -E "Failed|FAILED|passed|failed|Error" | cut -c1-250 | head -50
```

> ls: cannot access 'dokima/audit.py': No such file or directory
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError
>         rule lacks the all done-whens passed check, and the app has issues: read. The audit returns seven single lines, one
>         except ModuleNotFoundError as e:
> E           Failed: 283.1: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError
>         except ModuleNotFoundError as e:
> E           Failed: 283.1: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError
>         except ModuleNotFoundError as e:
> E           Failed: 283.1: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError
>         except ModuleNotFoundError as e:
> E           Failed: 283.1: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError
>         except ModuleNotFoundError as e:
> E           Failed: 283.1: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -rf tests/test_audit.py tests/test_audit_cli.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-220; python3 -m pytest -q 2>&1 | tail -2; git diff HEAD~1 -- tests/test_audit.py
```

> Command did not complete within its 120s timeout and was moved to the background (ID: baqsdlb9f). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 -- tests/test_audit.py; grep -n "Needs you\|PURPLE\|layout\|PERMISSIONS\|BRANCH_RULES" dokima/manifest.py | head -30
```

> diff --git a/tests/test_audit.py b/tests/test_audit.py
> index dda0c7b..ce7d4bf 100644
> --- a/tests/test_audit.py
> +++ b/tests/test_audit.py
> @@ -177,14 +177,15 @@ def test_each_difference_gets_one_line_saying_what_is_off_and_what_dokima_needs(
>      Proves 283.1. The faked repo differs in seven ways: the plan label is missing, the work label's color is 000000, the Action field
>      has no Autopilot option, the High priority option is RED, the Autopilot view filters on label:autopilot, main's
>      rule lacks the all done-whens passed check, and the app has issues: read. The audit returns seven single lines, one
> -    per difference, each naming the setting and the value Dokima needs (with the live value where there is one)."""
> +    per difference, each naming the setting and the value Dokima needs (with the live value where there is one; a
> +    missing option's line gives the color Dokima needs)."""
>      record_property("proves", "283.1")
>      a = audit("283.1")
>      lines = a.compare(drifted(), REPO)
>      assert all("\n" not in l and l.strip() for l in lines), f"283.1: every difference must be one plain line: {lines}"
>      one_line(lines, "283.1", "the missing plan label", "plan", "1d76db")
>      one_line(lines, "283.1", "the work label's color", "work", "000000", "0e8a16")
> -    one_line(lines, "283.1", "the missing Autopilot option of the Action field", "Action", "Autopilot")
> +    one_line(lines, "283.1", "the missing Autopilot option of the Action field", "Action", "Autopilot", "P

`11. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output | cut -c1-220
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output cut -c1-220. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`12. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output | cut -c1-220
```

> rule lacks the all done-whens passed check, and the app has issues: read. The audit returns seven single lines, one
> ____________ test_a_failed_github_call_is_reported_as_not_verified _____________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-1/test_a_failed_github_call_is_r0')
>     def test_a_failed_github_call_is_reported_as_not_verified(record_property, tmp_path):
>         """A failed GitHub call is reported as not verified with GitHub's reason, never skipped.
> _________ test_the_audit_command_reports_failed_calls_as_not_verified __________
>     def test_the_audit_command_reports_failed_calls_as_not_verified(record_property, tmp_path):
> FAILED tests/test_audit.py::test_each_difference_gets_one_line_saying_what_is_off_and_what_dokima_needs - Failed: 283.1: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_too_much_is_a_difference_too - Failed: 283.1: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_a_missing_branch_rule_and_a_missing_view_are_reported - Failed: 283.1: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_descriptions_and_layouts_are_compared_too - Failed: 283.1: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_matching_and_undeclared_settings_get_no_line - Failed: 283.1: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_drift_opens_one_pinned_setup_issue_marked_needs_you - Failed: 283.2: there is no audit module, dokima/audit.py
> FAILED 

**Agent:** All 23 new tests fail for the right reason: the audit doesn't exist yet. Both earlier blockers look fixed. Writing the hand-back now.

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Made criterion 1 promise a command, `python3 -m dokima.audit OWNER/REPO`, that reads labels, board options and views, main's rule and the app's permissions from GitHub through gh.",
          "Added tests/test_audit_cli.py: 8 tests that run the command against a fake gh (tests/fake_gh.py) and check pinning, Needs you on the board, updating the same issue, closing it once clean, code owners, staying on the repo and could-not-be-verified lines.",
          "Added a test where a label description, an option description and a view layout drift, each expected as its own line."],
  "decided": ["Reading the app's own permissions needs a key the workflow lacks; that key is left to #285, and until then the permissions line says they could not be verified."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now proves the audit command really reads and writes GitHub, and compares descriptions and layouts; all 23 new tests fail today only because the audit is missing.",
 "blockers": [],
 "notes": [
  {"text": "With the key the workflow has today, GitHub always refuses to say what the app's permissions are, so per criterion 5 the Setup issue never closes on a real repo until #285 gives the workflow a key that can read them. The owner should check that #285 really carries this.",
   "evidence": "plan.json out_of_scope: \"Giving the workflow a key that can read the app's own permissions (GET repos/OWNER/REPO/installation needs one); #285 runs the audit, and until then the permissions line says they could not be verified\"; criterion 5: unreadable settings open or keep open the Setup issue."},
  {"text": "The command tests only check a view's layout through the in-memory tests. The fake gh sends layouts the way GitHub does (TABLE_LAYOUT), so on a clean repo the command test fails if the audit reads them wrong, but no command test checks a layout that has really drifted.",

```

> summary holds 29 words, over its cap of 25 (up to 30 passes)

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now proves the audit command really reads and writes GitHub; all 23 new tests fail today only because the audit is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 283 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the revised plan for #283. Both blockers from my last review are fixed, and the hand-back is in `/tmp/dokima-out/review.json`. It passes both checks.

- **B1 (fixed):** the tests only ever ran against a fake GitHub kept in memory, so an audit that never reads the real settings could pass. Criterion 1 now promises a command, `python3 -m dokima.audit OWNER/REPO`, that reads everything from GitHub through `gh`. The 8 new tests in `tests/test_audit_cli.py` run that command from outside, against a fake `gh` that logs every call. Every kind of drift they plant can only be found by actually reading it through `gh`. They also check that the Setup issue is pinned and marked Needs you, that a later run updates the same issue, that a clean run writes nothing or closes a leftover issue, that only the code owners are mentioned, that no call goes to another repo, and that refused or failed calls become "could not be verified" lines.
- **B2 (fixed):** a new test changes a label's description, a board option's description and a view's layout, and expects one line for each.

I ran both test files: all 23 tests fail, every one with "there is no audit module" or "there is no audit command", not a crash or a bad path. I also started the full test suite, but it was still running when I finished, so I didn't wait for its result.

Every ask in the issue maps to a criterion. The plan no longer has questions for you.

Two notes, neither blocking:
- **The Setup issue can't close on a real repo yet.** With the key the workflow has today, GitHub won't say what the app's permissions are. Criterion 5 then keeps the Setup issue open with a "could not be verified" line. The plan leaves the fix, a key that can read them, to #285. It's worth checking that #285 really includes this.
- **One gap in the command tests.** No command test plants a drifted view layout; only the in-memory tests cover that.

`15. Bash`
```
grep -E "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output | tail -3 | cut -c1-300
```

> rule lacks the all done-whens passed check, and the app has issues: read. The audit returns seven single lines, one
>      one_line(lines, "283.1", "main's missing required check", "main", "all done-whens passed")
>      one_line(lines, "283.1", "main's missing rule", "main", "all tests", "all done-whens passed")

`16. Bash`
```
grep -nE "[0-9]+ (passed|failed)" /tmp/claude-1001/-home-runner-work-dokima-dokima/d840c2d1-794f-4427-bd01-2f233cf17cc1/tasks/baqsdlb9f.output | cut -c1-300
```

> 31:23 failed in 0.49s
> 33:25 failed, 680 passed in 296.54s (0:04:56)

**Agent:** The full suite finished with 25 failures, but the plan only adds 23 tests. I'm checking what the other 2 are.

`17. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python3 -m pytest -q -rf --deselect tests/test_audit.py --deselect tests/test_audit_cli.py -x -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-300
```

> FAILED tests/test_plan_links_recorded.py::test_links_with_no_loop_are_recorded_and_autopilot_goes_on - AssertionError: 252.3: autopilot should start the worker, the river said 'stop'
> 1 failed, 535 passed, 23 deselected in 236.52s (0:03:56)

`18. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python3 -m pytest -q -rf --deselect tests/test_audit.py --deselect tests/test_audit_cli.py -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-300; git diff --stat fd83ff5 HEAD
```

> FAILED tests/test_plan_links_recorded.py::test_links_with_no_loop_are_recorded_and_autopilot_goes_on - AssertionError: 252.3: autopilot should start the worker, the river said 'stop'
> FAILED tests/test_plan_links_recorded.py::test_recorded_links_let_autopilot_go_on - AssertionError: 252.5: autopilot should start the worker, the river said 'stop'
> 2 failed, 680 passed, 23 deselected in 284.87s (0:04:44)
>  tests/fake_gh.py        | 379 ++++++++++++++++++++++++++++++++++++++
>  tests/test_audit.py     | 478 ++++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_audit_cli.py | 293 +++++++++++++++++++++++++++++
>  3 files changed, 1150 insertions(+)

**Agent:** The 2 extra failures are in `tests/test_plan_links_recorded.py`, an older file the planner didn't touch. I'm checking whether they also fail without the planner's commits.

`19. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -p no:cacheprovider tests/test_plan_links_recorded.py 2>&1 | tail -1; git worktree add -q /tmp/wt-main fd83ff5 2>&1; cd /tmp/wt-main && python3 -m pytest -q -p no:cacheprovider tests/test_plan_links_recorded.py 2>&1 | tail -1; cd /; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/wt-main
```

> 2 failed, 16 passed in 28.55s
> 2 failed, 16 passed in 26.02s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** They fail on main too, so the planner didn't cause them. A quick look at why:

`20. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -p no:cacheprovider tests/test_plan_links_recorded.py -k "no_loop_are_recorded" 2>&1 | grep -E "^E |river|def test" | head -20 | cut -c1-300
```

> def test_links_with_no_loop_are_recorded_and_autopilot_goes_on(tmp_path, record_property):
> >       assert step == "start worker", f"252.3: autopilot should start the worker, the river said {step!r}"
> E       AssertionError: 252.3: autopilot should start the worker, the river said 'stop'
> E       assert 'stop' == 'start worker'
> E         
> E         - start worker
> E         + stop
> FAILED tests/test_plan_links_recorded.py::test_links_with_no_loop_are_recorded_and_autopilot_goes_on - AssertionError: 252.3: autopilot should start the worker, the river said 'stop'

**Agent:** Adding this to the review as a proposed issue, outside this plan:

`21. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["issues_found"]=[{"title":"Two plan-links tests fail on main: autopilot stops instead of starting the worker",
 "why":"Main's test suite is red, so every pull request starts with two failures that are not its own, and the autopilot promise of #252 (an approved plan with recorded links starts the worker) is not holding.",
 "evidence":"On fd83ff5 (main before this issue) `pytest -q tests/test_plan_links_recorded.py` gives 2 failed, 16 passed: test_links_with_no_loop_are_recorded_and_autopilot_goes_on (\"252.3: autopilot should start the worker, the river said 'stop'\") and test_recorded_links_let_autopilot_go_on (252.5, same message). The same 2 fail on try/issue-283, which adds only new test files."}]
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 283 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** The full test suite finished: 25 failed, 680 passed. The plan for #283 is still approved.

- **23 failures are the plan's own new tests.** They fail as they should, because the audit hasn't been built yet.
- **The other 2 fail on main too.** Both are in `tests/test_plan_links_recorded.py`: `test_links_with_no_loop_are_recorded_and_autopilot_goes_on` and `test_recorded_links_let_autopilot_go_on`. Both expect autopilot to start the worker once a plan is approved, but it stops instead ("252.3: autopilot should start the worker, the river said 'stop'"). I ran that file on main from before this issue and got the same 2 failures. This branch only adds new test files, so it didn't cause them.

I added those 2 failures to the review as a proposed issue, since they're outside this plan. Until someone fixes them, every pull request will start with 2 failures that aren't its own, including the one for #283. The updated `review.json` still passes both checks.
