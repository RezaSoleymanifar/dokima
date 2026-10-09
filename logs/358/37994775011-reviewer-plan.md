# reviewer (plan) for #358

Run: https://github.com/dokima-dev/dokima/actions/runs/37994775011

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack /tmp/pack/in; cat /tmp/pack/plan.json; cat /tmp/pack/open_blockers.json
```

> # Issue #358: Text-only changes (AGENTS.md, README, wiki) skip the plan and tests
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #358](https://github.com/dokima-dev/dokima/issues/358)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> A pull request that changes only text files (AGENTS.md, README, the wiki, other .md files) and no code, tests or workflows takes a shortcut: no plan, no planner tests, no worker test run. The checks pass on their own when nothing but text files changed, and the owner approves and merges it like any other pull request.
> 
> Owner's words (2026

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/parent.json | head -30; git show --stat HEAD; cat tests/test_text_only.py; cat dokima/checks.py; cat .github/workflows/done-whens.yml
```

> {"number": null}commit 8765688ca8d7cba96481bb8b59845e59b0de2690
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 21:39:25 2026 +0000
> 
>     planner for #358 (run 37994079094)
> 
>  tests/test_text_only.py | 223 ++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 223 insertions(+)
> """A pull request changing only text files skips the plan and its tests (issue #358).
> 
> Most tests here run the real command the done-whens workflow runs, `python3 -m dokima.checks matrix`, from the repo
> root, with GitHub faked: a stub `gh` on PATH answers the pull request's changed files (GitHub's `pulls/N/files` list,
> split over two pages the way `gh api --paginate` prints them back to back) and finds no issue linked and no plan.
> Others run the shell of the done-whens workflow's own steps, cut out of `.github/workflows/done-whens.yml`, with a fake
> `pytest` on PATH, so the workflow GitHub runs is the thing judged. Nothing here touches the network.
> 
> Text files are `.md` files outside `dokima/roles/`, `tests/` and `.github/`: AGENTS.md, README.md, the wiki under
> docs/wiki/ and any other Markdown file. Anything else changed sends the pull request the full way.
> """
> import json
> import os
> import subprocess
> import sys
> 
> ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
> WORKFLOW = os.path.join(ROOT, ".github", "workflows", "done-whens.yml")
> SHORTCUT = "Text only: no plan needed"
> NO_ISSUE = "No approved plan found: no issue linke

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_text_only.py 2>&1 | grep -E "Error|358\.|passed|failed" | head -30; grep -n "BRANCH_RULES" -A5 dokima/manifest.py | head; cat .github/CODEOWNERS; ls docs 2>&1; grep -n "def issue_of_pr\|def conversation\|def pages" -A15 dokima/agent.py | head -70
```

> Proves 358.1.
>         record_property("proves", "358.1")
> >           assert is_shortcut(rows), (f"358.1: a pull request changing only text files ({what}) did not get the single "
> E           AssertionError: 358.1: a pull request changing only text files (AGENTS.md alone) did not get the single 'Text only: no plan needed' check: [{'id': 'none', 'name': 'No approved plan found: no issue linked', 'tests': ''}]
> tests/test_text_only.py:133: AssertionError
>         Proves 358.2.
>         record_property("proves", "358.2")
> >       assert code == 0, f"358.2: the text-only check failed in the done-whens workflow (exit {code}):\n{out}"
> E       AssertionError: 358.2: the text-only check failed in the done-whens workflow (exit 1):
> tests/test_text_only.py:147: AssertionError
>         Proves 358.3.
>         record_property("proves", "358.3")
>                 f"358.3: a pull request changing {other} took the text-only shortcut or lost its checks: {rows}\n{out}"
>             f"358.3: renaming a code file to a .md name took the text-only shortcut: {rows}\n{out}"
>             f"358.3: deleting a code file beside a text change took the text-only shortcut: {rows}\n{out}"
> >       assert is_shortcut(rows), f"358.3: a text-only pull request lost its shortcut: {rows}\n{out}"
> E       AssertionError: 358.3: a text-only pull request lost its shortcut: [{'id': 'none', 'name': 'No approved plan found: no issue linked', 'tests': ''}]
> tests/test_text_only.py:183: AssertionError
>         Proves 358.4.
>         "all 

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned a shortcut: a pull request changing only Markdown files outside dokima/roles/, tests/ and .github/ gets one check, \"Text only: no plan needed\", that passes without running tests.",
          "Wrote five tests in tests/test_text_only.py that run the real check-list command with GitHub faked and the done-whens workflow's own steps."],
  "decided": ["The river does not change; the shortcut is for pull requests the owner opens themselves, and non-Markdown text files like LICENSE do not get it.",
              "When GitHub cannot list the changed files, or lists none, the pull request goes the full way."],
  "open": ["The build must change .github/workflows/done-whens.yml, which the planner flagged as a concern."]},
 "verdict": "block",
 "summary": "The plan matches the owner's ask and its tests fail today for the right reason, but the tests only try pull requests with no linked issue, so a build that skips the shortcut whenever the pull request says \"Closes #N\" would still pass.",
 "blockers": [{"id": "B1", "criterion": "358.1",
   "test": "tests/test_text_only.py::test_a_pull_request_changing_only_text_files_gets_the_text_only_check",
   "problem": "Criterion 1 promises the text-only check \"needs no issue or plan\", but every text-only case in the tests is a pull request with no linked issue. A build that adds the shortcut only where build_matrix today returns \"No approved plan found: no issue linked\" passes every test, while a text-only pull request that says \"Closes #N\" for an issue with no plan still gets the failing \"No approved plan found for issue #N\" check. That is the usual way an owner opens a pull request for a filed issue.",
   "evidence": "tests/test_text_only.py run_matrix writes the event body as \"\" and head ref \"owner/text-edit\", and the stub's graphql answer has no closing issues, so agent.issue_of_pr and plan.pr_issue_number always 
```

> Exit code 1
> summary holds 43 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`5. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="The plan matches the ask, but its tests only try pull requests with no linked issue, so a text-only one saying \"Closes #N\" is unproven."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 358 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I've finished reviewing the plan for [#358](https://github.com/dokima-dev/dokima/issues/358) (text-only pull requests skip the plan and its tests), and I'm sending it back to the planner over one problem. The review is saved in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**The blocker (B1, criterion 358.1, fixed by the planner):** the plan says a text-only pull request gets the shortcut whether or not it has a linked issue or a plan. But every test only tries a pull request with no linked issue. That leaves the common case unproven: the owner opens a pull request that says "Closes #N" for an issue with no plan. A build could add the shortcut only where today's code says "no issue linked" and still pass every test. That pull request would then still fail with "No approved plan found for issue #N". The fix is one more test case: a text-only pull request whose body says "Closes #77", with fake GitHub answering for that issue, which must get only the "Text only" check.

**What's fine:**
- All six of your asks in the issue map to a criterion.
- All five new tests fail today because the feature is missing, not because the tests are broken.
- The tests run the real check-list command and the workflow's own steps.
- They cover renamed and deleted code files, role files, and the case where GitHub can't list the changed files.

**Notes that don't block:**
- As written, the shortcut would also replace an approved plan's criterion checks with the single "Text only" check if a pull request for that plan changes only text. That's rare today.
- The build has to change `.github/workflows/done-whens.yml`, and the bot can't push workflow changes. So the build will stop for you: it needs your hands, and the shortcut only takes effect after it merges.
