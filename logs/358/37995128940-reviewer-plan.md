# reviewer (plan) for #358

Run: https://github.com/dokima-dev/dokima/actions/runs/37995128940

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
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
> A pull request that changes only text files (AGENTS.md, README, the wiki, other .md files) and no code, tests or workflows takes a shortcut: no plan, no planner tests, no worker test run. The checks pass on their own when n

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_text_only.py; git diff 8765688 ec5eaed --stat
```

> """A pull request changing only text files skips the plan and its tests (issue #358).
> 
> Most tests here run the real command the done-whens workflow runs, `python3 -m dokima.checks matrix`, from the repo
> root, with GitHub faked: a stub `gh` on PATH answers the pull request's changed files (GitHub's `pulls/N/files` list,
> split over two pages the way `gh api --paginate` prints them back to back) and finds no plan: either no issue is
> linked, or the description says "Closes #77" and issue #77 has no comments and no pull requests.
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
> NO_ISSUE = "No approved plan found: no issue linked"
> PR = 900
> 
> STUB_GH = '''#!/usr/bin/env python3
> """A stand-in for the GitHub CLI: answers from $STUB_DATA and logs every call."""
> import json, os, sys
> data = json.load(open(os.environ["STUB_DATA"]))
> a = sys.argv[1:]
> with open(os.environ["STUB_DAT

`3. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_text_only.py 2>&1 | grep -E "358\.|passed|failed|Error" | head -30; grep -n "def build_matrix" -A60 dokima/checks.py | head -90
```

> Proves 358.1.
>         record_property("proves", "358.1")
> >           assert is_shortcut(rows), (f"358.1: a pull request changing only text files ({what}) did not get the single "
> E           AssertionError: 358.1: a pull request changing only text files (AGENTS.md alone) did not get the single 'Text only: no plan needed' check: [{'id': 'none', 'name': 'No approved plan found: no issue linked', 'tests': ''}]
> tests/test_text_only.py:136: AssertionError
>         Proves 358.2.
>         record_property("proves", "358.2")
> >       assert code == 0, f"358.2: the text-only check failed in the done-whens workflow (exit {code}):\n{out}"
> E       AssertionError: 358.2: the text-only check failed in the done-whens workflow (exit 1):
> tests/test_text_only.py:153: AssertionError
>         Proves 358.3.
>         record_property("proves", "358.3")
>                 f"358.3: a pull request changing {other} took the text-only shortcut or lost its checks: {rows}\n{out}"
>             f"358.3: renaming a code file to a .md name took the text-only shortcut: {rows}\n{out}"
>             f"358.3: deleting a code file beside a text change took the text-only shortcut: {rows}\n{out}"
>             f"358.3: a code change saying 'Closes #77', for an issue with no plan, took the text-only shortcut: {rows}\n{out}"
> >       assert is_shortcut(rows), f"358.3: a text-only pull request lost its shortcut: {rows}\n{out}"
> E       AssertionError: 358.3: a text-only pull request lost its shortcut: [{'id': 'none', 'name': 'No appro

`4. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_text_only.py -k "passes_without or cannot_list" 2>&1 | grep -E "^E " | head; pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b172vjivn). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/8b3e52a4-c0c2-47b5-b779-b8843fde030b/tasks/b172vjivn.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_text_only.py -k "passes_without or cannot_list" 2>&1 | grep -E "^E " | head
```

> E       AssertionError: 358.2: the text-only check failed in the done-whens workflow (exit 1):
> E         ::error title=text-only has no test::No test verifies this done-when yet.
> E         
> E       assert 1 == 0
> E       AssertionError: 358.5: the merge check never asked GitHub for the pull request's files:
> E         ["api", "graphql", "-f", "query=query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p){closingIssuesReferences(first:1){nodes{number}}}}}", "-f", "o=o", "-f", "n=r", "-F", "p=900"]
> E         
> E       assert 'pulls/900/files' in '["api", "graphql", "-f", "query=query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p){closingIssuesReferences(first:1){nodes{number}}}}}", "-f", "o=o", "-f", "n=r", "-F", "p=900"]\n'

**Agent:** Still on the plan review: every new test fails today for the right reason, and the earlier blocker is fixed, so I'm writing the approval now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["Added a case to the 358.1 test: a text-only pull request saying \"Closes #77\", for an issue with no plan, must get the single \"Text only: no plan needed\" check.", "Added the mirror case to the 358.3 test: a code change saying \"Closes #77\" keeps \"No approved plan found for issue #77\"."],
  "decided": ["Criterion 1 now says the shortcut holds both with no issue linked and when the pull request names an issue with no plan."],
  "open": ["The build must change .github/workflows/done-whens.yml, which the planner flagged as a concern."]},
 "verdict": "approve",
 "summary": "The plan covers every ask, the missing \"Closes #N\" case is now tested, and all five new tests fail today because the shortcut does not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 1 does not say what happens to a text-only pull request whose issue has an approved plan; as the suggested build reads, it would get the one text-only check in place of that plan's criterion checks. That only matters when such a plan has no test files, so it is rare.", "evidence": "plan.json criterion 1; dokima/checks.py build_matrix lines 56-67"},
  {"text": "The bot cannot push workflow changes, so the change to done-whens.yml needs the owner's hands, and because done-whens runs main's copy the shortcut only works after this merges.", "evidence": ".github/workflows/done-whens.yml; AGENTS.md Identity and safety"}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "A pull request that changes only text files (AGENTS.md, README, the wiki, other .md files) and no code, tests or workflows takes a shortcut: no plan, no planner tests, no worker test run.", "source": "https://github.com/dokima-dev/dokima/issues/358", "criterion": "358.1"},
  {"ask": "The checks pass on their own when nothing but text files changed", "source": "https://github.com/dokima-dev/dokima/issues/358
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> 0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers every ask, now tests the \"Closes #N\" case, and all five new tests fail today because the shortcut is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 358 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for [#358](https://github.com/dokima-dev/dokima/issues/358) (a shortcut for pull requests that change only text files), and the hand-back is in `/tmp/dokima-out/review.json`. It passes both checks with no errors.

- **The earlier blocker is fixed.** The 358.1 test now also tries a text-only pull request that says "Closes #77" for an issue with no plan, and expects it to get only the "Text only: no plan needed" check. The 358.3 test now has the opposite case: a code change that says "Closes #77" must still get "No approved plan found for issue #77".
- **All five new tests fail today for the right reason.** 358.1, 358.3 and 358.4 still get "No approved plan found: no issue linked". 358.2 fails because the workflow step reports "text-only has no test". 358.5 fails because nothing asks GitHub for the pull request's files yet. The new "Closes #77" code-change case in 358.3 already passes, so the fake GitHub in the tests does reach the "issue with no plan" path.
- **Every ask in the issue maps to a criterion.** None are missing, and the plan has no questions for you.

Two notes, neither of them a blocker:
- The plan doesn't say what happens to a text-only pull request whose issue already has an approved plan. Built as suggested, it would get the one text-only check instead of that plan's own checks. That only matters when such a plan has no tests, so it should be rare.
- The build has to change `.github/workflows/done-whens.yml`. The bot can't push workflow changes, so that change needs you. And because that workflow runs from main, the shortcut only starts working after this merges.

I also started the full `pytest -q` run, but it hit the two-minute limit and moved to the background before finishing, so I don't have its result.

`8. Bash`
```
tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/8b3e52a4-c0c2-47b5-b779-b8843fde030b/tasks/b172vjivn.output
```

> assert 'pulls/900/files' in '["api", "graphql", "-f", "query=query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p){closingIssuesReferences(first:1){nodes{number}}}}}", "-f", "o=o", "-f", "n=r", "-F", "p=900"]\n'
> 5 failed, 752 passed, 83 skipped in 188.81s (0:03:08)
> 
> [exited with code 0]

**Agent:** The full test run has finished: 752 passed, 83 skipped and 5 failed. The 5 failures are the five new tests for [#358](https://github.com/dokima-dev/dokima/issues/358) (a shortcut for pull requests that change only text files); they fail because the shortcut isn't built yet. No other test fails, and the approval stands.
