# reviewer (plan) for #282

Run: https://github.com/dokima-dev/dokima/actions/runs/37862304071

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (69.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/96b89f2e-e815-488c-86e0-59b34e850c82/tool-results/b3zbu28aa.txt
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
> 05-planner.json
> # Issue #282: Everything Dokima needs from GitHub is declared in one manifest in code
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #282](https://github.com/dokima-dev/dokima/issues/282)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- 

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | tail -n +20
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
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []
> {
>  "kind": "user_story",
>  "summary": "Every label, board field and option, view, required check, branch rule and app permission Dokima relies on is declared in one manifest file, and a test catches code that relies on anything left out.",
>  "user_story": "The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a test catches code that relies on anything left out.",
>  "acceptance_criteria": [
>   {
>    "text": "One manifest, `dokima/manifest.py`, declares the labels, board fields and options, views, required checks, branch rules and app permissions Dokima needs. Labels: plan, work, autopilot, blocker, high, parked. Fields: Status (Backlog, Plan, Work, Review, Done), Action (Needs you, Autopilot), Priority (Blocker, High, Parked). View: Autopilot, a table. Required checks: \"all tests\" and \"all done-whens passed\", which main's branch rule requires. Every label and option has a color and description.",
>    "source": "https://github.com/dokima-dev/dokima/issues/282"
>   },
>   {
>    "text": "The manifest declares the Autopilot option as purple, described \"Running on its own\", and the Autopilot view's filter as `label:autopilot is:open`. The board takes that filter from the manifest when it adds the view, so changing the manifest changes the view it adds.",
>    "source": "https://github.com/dokima-dev/dokima/issues/282"
>   },
>   {
>    "text": "A test fails when a workflow or Dokima's code relies on a s

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; python3 -c "
import json
for f in ['in/04-reviewer-plan.json','in/05-planner.json']:
  d=json.load(open(f)); h=d.get('handback',d)
  print(f); print(json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','resolved','notes','assumptions','questions','replies']},indent=1)[:6000])
"
```

> 42:### dokima-runtime on issue #282 (2026-10-08T23:01:40Z)
> 46:### dokima-runtime on issue #282 (2026-10-08T23:01:52Z)
> 225:### dokima-runtime on issue #282 (2026-10-08T23:10:36Z)
> 372:### dokima-runtime on issue #282 (2026-10-08T23:12:01Z)
> 571:### dokima-runtime on issue #282 (2026-10-08T23:19:09Z)
> 725:### RezaSoleymanifar on issue #282 (2026-10-08T23:48:30Z)
> 729:### dokima-runtime on issue #282 (2026-10-08T23:48:50Z)
> 917:### dokima-runtime on issue #282 (2026-10-08T23:57:59Z)
> in/04-reviewer-plan.json
> {
>  "verdict": "approve",
>  "summary": "The plan now covers every kind of setting the owner named, including required checks, branch rules and app permissions, and every new test fails today because the manifest does not exist yet; one question about how far the permission check reaches waits for the owner.",
>  "blockers": [],
>  "resolved": [
>   "B1"
>  ],
>  "notes": [
>   {
>    "text": "Every new test fails today because dokima/manifest.py is missing, and the three changed Autopilot view tests fail because the board still adds the filter label:autopilot.",
>    "evidence": "pytest -q tests/test_manifest.py: 26 failed, each 'there is no manifest module, dokima/manifest.py'; tests/test_autopilot_board.py: filter 'label:autopilot' vs 'label:autopilot is:open'."
>   },
>   {
>    "text": "The check test runs against the real repo: dokima/card.py looks up \"all tests\" through its constant ALL_TESTS, which is the case the plan names.",
>    "evidence": "dokima/card.py:24 ALL_TESTS = \"all tests\"; dokima/

`5. Bash`
```
cd /tmp/pack; sed -n 720,740p issue.md; sed -n 917,960p issue.md
```

> <sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 2.8 min · 10 turns · 473,788 tokens in, 4,241 out · $0.56 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/282/37858760814-reviewer-plan.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37858760814)</sub>
> 
> **Next:** @RezaSoleymanifar The reviewer did not accept the plan's assumption for: "Should the test work out the app permission behind every GitHub call the code makes, not only branch rules and a workflow's app token?" Answer with `/plan` and your words, or say `/work` to build it on its assumptions.
> 
> 
> ### RezaSoleymanifar on issue #282 (2026-10-08T23:48:30Z)
> 
> /plan Answer: yes, the test confirms the app has the permission behind every GitHub call the code makes, not only branch rules and the workflow token.
> 
> ### dokima-runtime on issue #282 (2026-10-08T23:48:50Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; wc -l tests/test_manifest.py; timeout 600 python -m pytest -q tests/test_manifest.py tests/test_app.py tests/test_autopilot_board.py 2>&1 | tail -45
```

> commit 099f0e042e6224f96b649806e67df671a3c10bac
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:57:48 2026 +0000
> 
>     planner for #282 (run 37861463546)
> 
>  tests/test_manifest.py | 172 ++++++++++++++++++++++++++++++++++++++++++++++++-
>  1 file changed, 169 insertions(+), 3 deletions(-)
> 
> commit 35c46755ffc651abd71dbf04a68aaa4ae01b11b7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:18:57 2026 +0000
> 
>     planner for #282 (run 37858075382)
> 
>  tests/test_manifest.py | 122 ++++++++++++++++++++++++++++++++++++++++++++++---
>  1 file changed, 115 insertions(+), 7 deletions(-)
> 
> commit 4913f5c1736889269bc04b7d070501e922bce8cb
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:10:25 2026 +0000
> 
>     planner for #282 (run 37857074700)
> 
>  tests/test_app.py             |   3 +-
>  tests/test_autopilot_board.py |  16 +-
>  tests/test_manifest.py        | 337 ++++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 347 insertions(+), 9 deletions(-)
> 611 tests/test_manifest.py
> FAILED tests/test_manifest.py::test_the_guard_catches_a_permission_this_repos_calls_need[issues-read-.github/workflows/agent.yml] - Failed: 282.4: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_manifest_is_read_with_no_network_and_no_github_calls - Failed: 282.5: there is no manifest module, dokima/manifest.py
> FAILED t

**Agent:** Round three of the plan review for #282: the new tests fail today for the right reason (no manifest yet). Now reading the new permission tests that cover the owner's 23:48 answer.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show 099f0e0 -- tests/test_manifest.py | head -260
```

> commit 099f0e042e6224f96b649806e67df671a3c10bac
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:57:48 2026 +0000
> 
>     planner for #282 (run 37861463546)
> 
> diff --git a/tests/test_manifest.py b/tests/test_manifest.py
> index c49d1f9..6f53c3a 100644
> --- a/tests/test_manifest.py
> +++ b/tests/test_manifest.py
> @@ -22,6 +22,18 @@ What counts as relying on a setting:
>      permission  a workflow asking an app token for it (permission-<name>: <level>), or code calling
>                  branches/<branch>/protection, which needs administration: read to read it, write to change it
>                  (-X PUT/POST/PATCH/DELETE, or rest("PUT", ...)); a level higher than the manifest's is left out too
> +
> +The app's permission behind every GitHub call (282.4): the guard also names every GitHub call whose app permission, at
> +the level it needs, the manifest leaves out, with the permission and the file. The calls it sees:
> +    in Python under dokima/: gh("api", [-X METHOD,] PATH, ...) and rest/api/self.rest(METHOD, PATH, ...), where PATH is
> +        written in the call (a string or f-string); without -X, a gh api call with -f/-F fields is POST, else GET;
> +        gh("<command>", "<subcommand>", ...) for gh's other commands; and every GraphQL query or mutation written in
> +        the code (a string starting "query" or "mutation"). A wrapper passing on a path it was given is not a call.
> +    in workflows: gh and git push in a step whose GH_TOKEN (

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "undeclared(ROOT)" tests/test_manifest.py; grep -n "def test_the_guard_passes_settings" -A25 tests/test_manifest.py | head -40; cat dokima/app.json
```

> 361:    assert m.undeclared(ROOT) == [], f"282.3: code or workflows in this repo rely on settings the manifest leaves out: {m.undeclared(ROOT)}"
> 373:    lines = m.undeclared(ROOT)
> 386:    lines = m.undeclared(ROOT)
> 581:    lines = m.undeclared(ROOT)
> 319:def test_the_guard_passes_settings_the_manifest_declares(record_property, tmp_path):
> 320-    """The guard stays quiet for declared settings, and the repo as it is passes.
> 321-
> 322-    Proves 282.3. A workflow keyed on the label plan and asking an app token for issues write and administration read, and code
> 323-    setting Status to Done, adding the Autopilot view, adding the label autopilot both ways, looking up the checks
> 324-    "all tests" and "all done-whens passed" by name and through a constant, and reading main's branch rule both ways,
> 325-    gets no line from the guard, and neither does the repo as it is."""
> 326-    record_property("proves", "282.3")
> 327-    m = manifest("282.3")
> 328-    write(str(tmp_path), ".github/workflows/plan.yml", """\
> 329-        on:
> 330-          issues:
> 331-            types: [labeled]
> 332-        jobs:
> 333-          go:
> 334-            if: github.event.label.name == 'plan'
> 335-            runs-on: ubuntu-24.04
> 336-            steps:
> 337-              - uses: actions/create-github-app-token@v2
> 338-                id: app
> 339-                with:
> 340-                  app-id: ${{ vars.DOKIMA_APP_ID }}
> 341-                  private-key: ${{ secrets.DOKIMA_APP_KEY }}
> 342-                  perm

`9. Bash`
```
cd /tmp/pack; grep -o "https://github.com/dokima-dev/dokima/issues/282#issuecomment-[0-9]*" issue.md | sort -u; grep -rho "issuecomment-[0-9]*" in | sort -u | head
```

> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner widened criterion 4 so a test checks the app permission, and its level, behind every gh command, REST or GraphQL call and git push in Dokima's code and in workflow steps on the app's key, as the owner answered.",
          "The planner added tests that name a missing or too-low permission with its file, stay quiet for calls needing no permission or on Actions' own key, and name any call they cannot tie to a permission."],
  "decided": ["The app and the manifest ask for Organization projects write, which the board's calls need, as well as Administration read.",
              "Workflow steps on Actions' own key are left out, since they never use the app's permissions."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now does what the owner answered: a test ties every GitHub call the code makes to the app permission it needs, and every new test fails today because the manifest does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "Every new test fails today for the right reason, and the three changed Autopilot view tests fail because the board still adds the filter label:autopilot.",
   "evidence": "pytest -q tests/test_manifest.py tests/test_app.py tests/test_autopilot_board.py: 63 failed, 20 passed; manifest tests fail with '282.N: there is no manifest module, dokima/manifest.py'; view tests with 'label:autopilot' vs 'label:autopilot is:open'."},
  {"text": "Each permission test runs both ways: the permission left out (or cut to read for a write call) is named with its file, and granted at the needed level the guard is quiet, so a guard tying a call to the wrong permission fails.",
   "evidence": "tests/test_manifest.py::test_the_guard_names_the_app_permission_behind_a_github_call, 22 cases; test_the_guard_catches_a_permission_this_repos_calls_need runs on this repo for board.py, body.py, card.py, agent.py, uptodate.py, worker.yml and a
```

> Exit code 1
> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`11. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan now ties every GitHub call the code makes to the app permission it needs, and every new test fails today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 282 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

`12. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan now ties every GitHub call the code makes to the app permission it needs, and every new test fails today as it should."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 282 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #282, round three. The review is saved to `/tmp/dokima-out/review.json` and passes both checks.

- **Your answer is built in:** You replied with `/plan` that the test should confirm the app has the permission behind every GitHub call the code makes. Criterion 4 now does that. It covers `gh` commands, direct GitHub API calls (REST and GraphQL) and `git push`, both in Dokima's code and in workflow steps that use the app's key.
- **The permission tests check both ways:**
  - A permission that is missing, or set to read where a call writes, is reported with the permission's name and the file.
  - With the right permission granted, the check stays quiet.
  - Calls that need no permission, or that run on Actions' own key, are not reported.
  - A call it can't link to a permission is reported, not let through.
  - Run on this repo, it finds the files that need each permission the app now has.
- **The tests fail today for the right reason:** the three test files gave 63 failures and 20 passes. The new tests fail because `dokima/manifest.py` doesn't exist yet. The three changed Autopilot view tests fail because the board still sets the filter to `label:autopilot` rather than `label:autopilot is:open`.
- **All seven of your asks are covered,** including your answer, and no earlier blockers were left open.

**For you to do on GitHub:** the plan adds Organization projects write to the app's permissions (`dokima/app.json`), because the board's calls need it, alongside Administration read. Neither is granted to the installed app until you accept them there.
