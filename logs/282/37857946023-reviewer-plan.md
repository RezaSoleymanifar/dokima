# reviewer (plan) for #282

Run: https://github.com/dokima-dev/dokima/actions/runs/37857946023

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #280, story 1</summary>
> 
> **Part of:** #280 A drift audit compares the repo's settings with what Dokima needs and tells me what's off
> 
> **User story:** The owner can read in one file every label, board fiel

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_manifest.py; git show HEAD -- tests/test_app.py tests/test_autopilot_board.py; cat dokima/app.json
```

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
> """
> import importlib
> import json
> import os
> import subprocess
> import sys
> import textwrap
> 
> import py

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_manifest.py 2>&1 | tail -30; python -m pytest -q tests/test_app.py tests/test_autopilot_board.py 2>&1 | tail -8; ls .github/workflows; grep -rn "name:" .github/workflows/*.yml | grep -i "all " ; grep -rn "label.name\|labels\[\]\|add_view\|\"Needs you\"" .github/workflows dokima --include=*.py --include=*.yml | head -40
```

> def manifest(criterion):
>         """The manifest module, or a failure naming the criterion when it is missing."""
>         try:
>             return importlib.import_module("dokima.manifest")
>         except ModuleNotFoundError as e:
>             if e.name != "dokima.manifest":
>                 raise
> >           pytest.fail(f"{criterion}: there is no manifest module, dokima/manifest.py")
> E           Failed: 282.5: there is no manifest module, dokima/manifest.py
> 
> tests/test_manifest.py:34: Failed
> =========================== short test summary info ============================
> FAILED tests/test_manifest.py::test_the_manifest_declares_every_label_dokima_uses - Failed: 282.1: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_manifest_declares_the_board_fields_and_their_options - Failed: 282.1: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_manifest_declares_views_checks_and_branch_rules - Failed: 282.1: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_manifest_declares_the_app_permissions - Failed: 282.1: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_autopilot_option_is_purple_running_on_its_own - Failed: 282.2: there is no manifest module, dokima/manifest.py
> FAILED tests/test_manifest.py::test_the_board_adds_the_autopilot_view_with_the_manifests_filter - Failed: 282.2: there is no manifest module, dokima/manifest.py
> FAILED test

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "all tests\|done-whens passed\|required_status\|branches/.*protection\|administration" dokima .github/workflows --include=*.py --include=*.yml | grep -v "^tests" | head -20; grep -rn "labels\|label" dokima/*.py | grep -iv "autopilot\|AUTOPILOT" | grep -n "\"[a-z]*\"" | head -30; gh 2>/dev/null; grep -rn "permissions:" -A6 .github/workflows/board.yml | head
```

> dokima/fence.py:3:The judges (all tests, each criterion's check) run on fresh machines from what gets pushed, so nothing the worker does to
> .github/workflows/done-whens.yml:61:    name: all done-whens passed
> .github/workflows/agent.yml:227:          - $PACK/diff.patch: the work against main. $PACK/tests.txt and tests.xml: all tests, run by code on this machine.
> .github/workflows/full-suite.yml:13:    name: all tests
> dokima/card.py:24:ALL_TESTS = "all tests"
> 2:dokima/card.py:180:    """One criterion as a bullet: its status circle, its label and its words, linked to its check when there is one;
> 6:dokima/board.py:28:        if action == "labeled" and p["label"]["name"] == "plan":
> 7:dokima/board.py:30:        elif action == "labeled" and p["label"]["name"] == "work":
> 8:dokima/board.py:55:    """(number, option) when a priority label was added or removed: the highest priority label left, or None to clear."""
> 9:dokima/board.py:56:    if event != "issues" or p["action"] not in ("labeled", "unlabeled") or p["label"]["name"] not in PRIORITY:
> 10:dokima/board.py:58:    names = {label["name"] for label in p["issue"].get("labels") or []}
> 11:dokima/board.py:59:    return p["issue"]["number"], next((option for label, option in PRIORITY.items() if label in names), None)
> 12:dokima/board.py:116:        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{labels(first:100){{nodes{{name}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=int(numb

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "labels\[\]\|--add-label\|--label\|issues/.*labels\|LABEL *=" dokima .github/workflows | head -20; grep -rn "label.name ==\|contains(github.event" .github/workflows | head
```

> dokima/board.py:131:        path = f"repos/{self.repo_owner}/{self.repo_name}/issues/{number}/labels"
> dokima/board.py:133:            self.rest("POST", path, **{"labels[]": AUTOPILOT})
> dokima/agent.py:225:        extra = [x for label in labels for x in ("--label", label)]
> dokima/agent.py:1053:        labels = {l["name"] for l in json.loads(gh("api", f"repos/{repo}/issues/{n}")).get("labels", [])}
> dokima/agent.py:1056:            gh("api", "-X", "POST", f"repos/{repo}/issues/{n}/labels", "-f", f"labels[]={AUTOPILOT}")
> dokima/agent.py:1059:            gh("api", "-X", "DELETE", f"repos/{repo}/issues/{n}/labels/{AUTOPILOT}")
> dokima/agent.py:1177:        labels = json.loads(gh("api", f"repos/{repo}/issues/{number}")).get("labels")
> dokima/agent.py:1566:        on = AUTOPILOT in {l["name"] for l in json.loads(gh("api", f"repos/{repo}/issues/{parent}")).get("labels", [])}
> dokima/plan.py:22:LABEL = "work"
> .github/workflows/worker.yml:21:    if: github.event.action == 'labeled' && github.event.label.name == 'work'
> .github/workflows/planner.yml:20:    if: github.event.label.name == 'plan'

**Agent:** I'm checking which labels Dokima's code adds, then I'll write the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 215,232p dokima/agent.py; grep -n "pr_open\|labels=" dokima/agent.py | head
```

> each created with the given labels.
> 
>     Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
>     done = latest(recs, "split", passed=True)
>     if done:
>         return done
>     plan = latest(recs, "planner")["handback"]
>     title = json.loads(gh("issue", "view", str(parent), "-R", repo, "--json", "title"))["title"]
>     filed = []
>     for i, st in enumerate(plan["stories"], 1):
>         extra = [x for label in labels for x in ("--label", label)]
>         url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
>         number = int(url.rstrip("/").split("/")[-1])
>         node = json.loads(gh("api", f"repos/{repo}/issues/{number}"))["id"]
>         gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues", "-F", f"sub_issue_id={node}")
>         filed.append({"story": i, "issue": number, "title": st["title"], "id": node,
>                       "blocked_by": [d + 1 for d in st.get("depends_on", [])]})
>     by_story = {f["story"]: f for f in filed}
> 213:def file_split(repo, parent, recs, labels=()):
> 1148:            "api", f"repos/{repo}/issues?labels={AUTOPILOT}&state=all&per_page=100", "--paginate") or "[]")

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote four criteria and a no-network requirement, with 17 new tests in tests/test_manifest.py.",
   "The planner changed three Autopilot view tests to expect the filter label:autopilot is:open, and the app test to allow Administration read."
  ],
  "decided": [
   "The guard that catches undeclared settings covers labels, board fields, options and views only.",
   "Only the Autopilot view's filter is read from the manifest; other code keeps its own names for now."
  ],
  "open": []
 },
 "verdict": "block",
 "summary": "The plan narrows the owner's \"a setting the manifest leaves out\" to labels, board fields, options and views, so code relying on a required check that the manifest drops would pass; the rest of the plan is sound and its tests fail today for the right reason.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "282.3",
   "test": "tests/test_manifest.py::test_the_guard_names_an_undeclared_setting_and_its_file",
   "problem": "The owner asked that a test fail when code or a workflow relies on any setting the manifest leaves out, and the manifest's settings include required check names, branch rules and app permissions. Criterion 3 and its tests cover only labels, board fields, options and views, and the plan raises no question about the narrower reading. Code already relies on a required check by name, so leaving it out of the manifest would go unnoticed.",
   "evidence": "Issue #282: \"A test fails when code or a workflow relies on a setting the manifest leaves out. It names the setting and the file.\" Criterion 3 says \"relies on a label, board field, option or view\". dokima/card.py:24 has ALL_TESTS = \"all tests\", the name of a required check. No test in tests/test_manifest.py takes a check out of CHECKS (or a permission out of PERMISSIONS) and expects the guard to name it, and none of the UNDECLARED cases is a check, branch rule or
```

> rc=0

**Agent:** I blocked the plan for #282 and sent it back to the planner. It narrows one of the owner's asks without asking them first. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks passed.

**The blocker (B1, criterion 282.3, for the planner):** The owner asked for a test that fails when code or a workflow relies on "a setting the manifest leaves out". The plan only covers labels, board fields, options and views. It leaves out required check names, branch rules and app permissions, and the plan has no question asking the owner about that. This is already a real gap: `dokima/card.py:24` uses the required check name "all tests", so if the manifest dropped that check, no test would notice. The smallest fix is to cover required check names, with a test in each direction. Any kind that can't be found in code, like branch rules or app permissions, should go to the owner as a question.

**What holds up:**
- **Owner's asks:** each of the six maps to a criterion, and none is missing.
- **New tests:** all 17 tests in `tests/test_manifest.py` fail today for the right reason: there is no `dokima/manifest.py` yet.
- **Changed tests:**
  - The three Autopilot view tests now fail, as expected, because the board still uses the filter `label:autopilot` instead of `label:autopilot is:open`.
  - The app test now allows Administration read but still refuses write, which matches criterion 4.

I found no problems outside this issue.
