# reviewer (plan) for #283

Run: https://github.com/dokima-dev/dokima/actions/runs/37880727190

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> - The Setup issue mentions only the repo's own code owners from CODEOWNERS, and the audit posts nowhere outside the repo it runs on. ([source](https://github.com/dokima-dev/dokima/issues/280))
> - Each setting the app cannot read gets its own line saying it could not be verified and why. It is never shown as 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat dokima/manifest.py; ls dokima; cat tests/test_audit.py
```

> <persisted-output>
> Output too large (41.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/cb6f7ce5-8d6a-4365-a928-883f36e1e6ac/tool-results/bqr7g4hkp.txt
> 
> Preview (first 2KB):
> commit 9246d363d461dcbd35e77ae941176ccca538de6f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 03:45:12 2026 +0000
> 
>     planner for #283 (run 37880298813)
> 
>  tests/test_audit.py | 456 ++++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 456 insertions(+)
> """Everything Dokima needs from GitHub, declared in one place.
> 
> Labels, board fields and options, views, required checks, branch rules and the app's permissions. Plain data; nothing
> here calls GitHub.
> 
>     python3 -m dokima.manifest [root]   # prints every setting the code or workflows rely on that is left out here
> 
> undeclared(root) reads the Python under dokima/ and the workflows under .github/workflows/ and names, with the file,
> every label, field, option, view, check or branch rule they rely on that is not declared below, and every GitHub call
> made as the app whose permission, at the level it needs, is not granted below. A call it cannot tie to a permission is
> named too, so a new kind of call never slips through.
> """
> import ast
> import os
> import re
> import sys
> 
> LABELS = {
>     "plan": {"color": "1d76db", "description": "Starts the planner"},
>     "work": {"color": "0e8a16", "description": "Starts the worker on the approved plan"},
>     "autopilo

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,140p dokima/manifest.py; ls dokima; ls dokima/audit.py 2>&1
```

> Exit code 2
> """Everything Dokima needs from GitHub, declared in one place.
> 
> Labels, board fields and options, views, required checks, branch rules and the app's permissions. Plain data; nothing
> here calls GitHub.
> 
>     python3 -m dokima.manifest [root]   # prints every setting the code or workflows rely on that is left out here
> 
> undeclared(root) reads the Python under dokima/ and the workflows under .github/workflows/ and names, with the file,
> every label, field, option, view, check or branch rule they rely on that is not declared below, and every GitHub call
> made as the app whose permission, at the level it needs, is not granted below. A call it cannot tie to a permission is
> named too, so a new kind of call never slips through.
> """
> import ast
> import os
> import re
> import sys
> 
> LABELS = {
>     "plan": {"color": "1d76db", "description": "Starts the planner"},
>     "work": {"color": "0e8a16", "description": "Starts the worker on the approved plan"},
>     "autopilot": {"color": "8250df", "description": "Running on its own"},
>     "blocker": {"color": "b60205", "description": "Priority: blocks other work"},
>     "high": {"color": "d93f0b", "description": "Priority: high"},
>     "parked": {"color": "c5c5c5", "description": "Priority: parked for later"},
> }
> 
> FIELDS = {
>     "Status": {
>         "Backlog": {"color": "GRAY", "description": "Not started"},
>         "Plan": {"color": "BLUE", "description": "Being planned"},
>         "Work": {"color": "YELLOW", "description": "Being built"},
>         "

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_audit.py
```

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
>     fields()                  the board's {field: {option: {"color": COLOR, "description": str}}}
>     views()                   the board's {view: {"layout": str, "filter": str}}
>     branch_rule(repo, branch) {"required_checks": [name, ...]}, or None when the branch has no

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_audit.py 2>&1 | tail -20; python3 -m pytest -q 2>&1 | tail -3; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.keys()); print(json.dumps(d.get('check'),indent=1))"
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bgiv67f7r). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/cb6f7ce5-8d6a-4365-a928-883f36e1e6ac/tasks/bgiv67f7r.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 60 python3 -m pytest -q tests/test_audit.py 2>&1 | grep -E "Failed|passed|failed|Error" | head -30
```

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
> E           Failed: 283.2: there is no audit module, dokima/audit.py
> tests/test_audit.py:54: Failed
> E   ModuleNotFoundError: No module named 'dokima.audit'
> <frozen importlib._bootstrap>:1324: ModuleNotFoundError

**Agent:** Tests all fail today for the right reason (no `dokima/audit.py`). Now checking whether the plan proves the audit talks to the real GitHub, and how CODEOWNERS is read elsewhere.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "CODEOWNERS\|def code_owners\|def owners" -r dokima | head; grep -n "^def \|^class " dokima/board.py | head -60; grep -n "Needs you\|needs_you" dokima/*.py | head -20
```

> dokima/card.py:447:    owners = plan.approvers(file_at(repo, ".github/CODEOWNERS") or "", repo.split("/")[0])
> dokima/plan.py:5:are the code owners in CODEOWNERS (the owners of `*`), or the repository owner
> dokima/plan.py:128:    """The people whose approval counts: the owners of `*` in CODEOWNERS, else the repository owner."""
> dokima/plan.py:137:    path = os.path.join(root, ".github", "CODEOWNERS")
> 21:def linked(body):
> 25:def decide(event, p):
> 56:def priority(event, p):
> 64:def gql(query, **variables):
> 71:def api(method, path, **fields):
> 80:class Board:
> 154:def action(board, kind, number, needs_you):
> 159:def switched(event, p):
> 166:def opened(event, p):
> 173:def switch(board, number):
> 199:def fix_view(board):
> 210:def sync(event, payload, spec, repo, q=gql, rest=api):
> 234:def main():
> dokima/board.py:1:"""Keep the project board's Status, Action ("Needs you" or "Autopilot") and Priority current, from GitHub events.
> dokima/board.py:26:    """[(kind, number, status, needs_you)]: kind is "issue" or "pr"; needs_you True marks it for the owner."""
> dokima/board.py:154:def action(board, kind, number, needs_you):
> dokima/board.py:155:    """The Action pill: Needs you when the river stops for the owner, else Autopilot while on autopilot, else none."""
> dokima/board.py:156:    return "Needs you" if needs_you else "Autopilot" if board.autopilot(kind, number) else None
> dokima/board.py:174:    """Follow the issue's autopilot label on its card, its open PR's card and the PR's label, never touchi

**Agent:** Tests check out and `*` owners matches how `plan.py` already reads CODEOWNERS. Writing the review now.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Planned a drift audit in dokima/audit.py with five criteria and one non-functional rule, and wrote 14 tests in tests/test_audit.py against a GitHub faked in memory.",
   "Asked the owner whether a permission broader than the manifest's counts as off."
  ],
  "decided": [
   "The audit is handed one GitHub object for every read and write; the tests hand it a fake.",
   "Only the code owners of `*` in CODEOWNERS are mentioned; fixes, the daily workflow and AGENTS.md are left to #284 and #285."
  ],
  "open": [
   "Nothing in the plan says which code reads the repo's live settings from GitHub."
  ]
 },
 "verdict": "block",
 "summary": "The plan is right about what to report, but every test runs against a fake GitHub, so an audit that never reads the repo's live settings, pins an issue or marks Needs you on the real board would pass; and drift in a label's or option's description, or a view's layout, is never tested.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "283.1",
   "test": null,
   "problem": "Criterion 1 promises the audit compares the manifest with the repo's live settings, and 2 promises a pinned issue marked Needs you on the board, but no test touches anything except the in-memory fake. A worker could ship compare() and run() with no code that reads labels, board fields and views, main's rule or the app's permissions from GitHub, and no code that pins or sets the Action field, and all 14 tests would pass. The scope lists no place for that code either, and #285 only adds the workflow that runs the audit.",
   "evidence": "tests/test_audit.py: every test passes `GitHub()` from the test file itself (class GitHub, lines ~62-130) into audit.compare or audit.run; `grep -n 'gh\\b\\|subprocess.run\\|PATH' tests/test_audit.py` finds no call to the real tool. Plan out_of_scope: \"The workflow that runs the audit daily ... that is #285\".",
   "fix": "Add a c
```

> Exit code 1
> summary holds 54 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`9. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every test runs on a fake GitHub, so an audit that never reads live settings would pass; description and layout drift are untested."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 283 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #283 and sent it back to the planner with two blockers. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

I ran the 14 new tests in `tests/test_audit.py` and they all fail today for the right reason: `dokima/audit.py` doesn't exist yet. I started a full `pytest -q` too, but it didn't finish within two minutes, so I have no result for the rest of the suite.

**Blockers (both for the planner):**
- **B1, criterion 1:** Every test runs on a fake GitHub that lives inside the test file. An audit could pass all 14 tests without ever reading the repo's real labels, board, main's branch rule or app permissions, and without pinning the Setup issue or marking it Needs you. Nothing in the scope says which code talks to GitHub, and #285 only adds the workflow that runs the audit. The fix is a test that runs `python3 -m dokima.audit` with a fake `gh` and checks it makes those reads and writes on that repo.
- **B2, criterion 1:** The manifest sets a description for every label and board option and a layout for every view, but the tests only ever change colors, filters and missing items. An audit that ignores descriptions and layouts would still pass. The fix is to add those three kinds of drift to the test repo.

**One note:** the lines for the missing Autopilot option and the missing view aren't checked for saying what Dokima needs.

**What checks out:**
- All seven asks in the issue map to a criterion; none is missing.
- Mentioning only the code owners of `*` matches how `dokima/plan.py` already reads CODEOWNERS.
- I accepted the planner's one assumption, that a broader permission counts as off. It matches "Each difference gets one plain line saying what is off and what Dokima needs" in the issue, and it changes neither how the system works nor what it costs.

`10. Bash`
```
tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/cb6f7ce5-8d6a-4365-a928-883f36e1e6ac/tasks/bgiv67f7r.output
```

> FAILED tests/test_audit.py::test_the_audit_posts_only_on_the_repo_it_runs_on - Failed: 283.4: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_an_unreadable_branch_rule_is_never_shown_as_fine - Failed: 283.5: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_each_unreadable_setting_gets_its_own_line - Failed: 283.5: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_a_failed_github_call_is_reported_as_not_verified - Failed: 283.6: there is no audit module, dokima/audit.py
> 14 failed in 0.31s
> FAILED tests/test_audit.py::test_each_unreadable_setting_gets_its_own_line - Failed: 283.5: there is no audit module, dokima/audit.py
> FAILED tests/test_audit.py::test_a_failed_github_call_is_reported_as_not_verified - Failed: 283.6: there is no audit module, dokima/audit.py
> 14 failed, 682 passed in 272.70s (0:04:32)
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> {
>  "passed": true,
>  "problems": []
> }
> 
> [exited with code 0]

**Agent:** The full test suite has now finished: 682 tests pass and 14 fail. The 14 failures are exactly the planner's new audit tests, and each one fails because `dokima/audit.py` doesn't exist yet. Nothing that worked before is broken.

The review stays as I handed it back: blocked, with B1 and B2 going to the planner.
