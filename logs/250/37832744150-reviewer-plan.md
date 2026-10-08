# reviewer (plan) for #250

Run: https://github.com/dokima-dev/dokima/actions/runs/37832744150

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
> # Issue #250: The planner finds the issues this one is blocked by, blocks or relates to, and code checks them
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 1</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** Every plan names the open issues its issue is blocked by, blocks and relates to, and code refuses a plan whose links are missing, malformed or wrong.
> 
> **Context:** Split from #231 under rule R2 (seven criteria once the owner's second comment added the run comment and GitHub's own links) and R3 (the native links live in the river and autopilot code, apart from the pack and checks). Round one of #231 planned this part and its 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_issue_links.py; git show HEAD -- tests/test_fixer.py tests/test_agent.py
```

> commit 125ea334294595c03cda4b61010ea972c6f133a7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 19:32:27 2026 +0000
> 
>     planner for #250 (run 37831831978)
> 
>  tests/test_agent.py       |   5 +-
>  tests/test_fixer.py       |   5 +-
>  tests/test_issue_links.py | 250 ++++++++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 258 insertions(+), 2 deletions(-)
> """The planner finds the open issues this one is blocked by, blocks or relates to, and code checks them.
> 
> Issue #250 (story 1 of #231). The planner's starting pack holds the repo's open issues; its prompt tells it to find the
> links; its hand-back carries them in a `links` field of three lists; and the round check every planner run does
> (`python3 -m dokima.agent check-round planner FILE PACK`) rejects a missing or malformed field, a number that is not
> one of the open issues in the pack, a link to the issue itself and one issue in two of the lists.
> 
> GitHub is faked: `gh issue view` and `gh pr list` answer for issue 250, and the repo's open issues are served to both
> ways of listing them, `gh issue list` (which honours `--limit`/`-L`, 30 by default, as gh does) and
> `gh api repos/o/r/issues` (which pages at `per_page`, 30 by default, unless `--paginate` is given, and also lists pull
> requests, each with a `pull_request` key, as GitHub's API does). Any other GitHub call fails the test naming it.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> from urllib.par

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_issue_links.py 2>&1 | grep -E "^(FAILED|ERROR)|AssertionError|Error:|passed|failed" | head -40; python -m pytest -q -x 2>&1 | tail -5; grep -rn 'problems_round("planner"\|check-round", "planner"\|"planner", ""' tests/ | grep -v test_issue_links
```

> E       AssertionError: 250.1: the planner's pack has no open_issues.json listing the repo's open issues
> tests/test_issue_links.py:104: AssertionError
> E       AssertionError: 250.2: the planner's prompt never points it at the pack's open_issues.json
> tests/test_issue_links.py:127: AssertionError
> >           assert code == 1, f"250.3: a hand-back with {name} passed the round check"
> E           AssertionError: 250.3: a hand-back with no links field passed the round check
> tests/test_issue_links.py:158: AssertionError
> >               assert code == 1, f"250.3: a {kind} with {name} passed the round check"
> E               AssertionError: 250.3: a story with a link to #999, no open issue passed the round check
> tests/test_issue_links.py:181: AssertionError
> >               assert code == 1, f"250.3: a {kind} with {name} passed the round check"
> E               AssertionError: 250.3: a story with #12 blocked by and blocks passed the round check
> tests/test_issue_links.py:203: AssertionError
> >       assert code == 1 and "links" in out, f"250.3: a planner hand-back with no links passed the round check: {out}"
> E       AssertionError: 250.3: a planner hand-back with no links passed the round check: 
> tests/test_issue_links.py:225: AssertionError
> FAILED tests/test_issue_links.py::test_the_planners_pack_holds_every_open_issue_of_the_repo - AssertionError: 250.1: the planner's pack has no open_issues.json listing the repo's open issues
> FAILED tests/test_issue_links.py::test_the_planners_prompt_te

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | grep -E "^FAILED|passed|failed" | head -20; git stash list | head -2
```

> >           assert code == 1, f"250.3: a hand-back with {name} passed the round check"
> E           AssertionError: 250.3: a hand-back with no links field passed the round check
> >               assert code == 1, f"250.3: a {kind} with {name} passed the round check"
> E               AssertionError: 250.3: a story with a link to #999, no open issue passed the round check
> >               assert code == 1, f"250.3: a {kind} with {name} passed the round check"
> E               AssertionError: 250.3: a story with #12 blocked by and blocks passed the round check
> >       assert code == 1 and "links" in out, f"250.3: a planner hand-back with no links passed the round check: {out}"
> E       AssertionError: 250.3: a planner hand-back with no links passed the round check: 
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it", "criterion": "N.k" or "missing"}
> FAILED tests/test_handback_check.py::test_every_blocker_is

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git stash -u -q 2>/dev/null; git checkout -q HEAD~1 && python -m pytest -q tests/test_fixer.py tests/test_handback_check.py 2>&1 | tail -4; git checkout -q try/issue-250; git status --short
```

> +     '"the owner\'s words", "source": "a link to where they said it", '
>   +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 11 passed in 0.75s

**Agent:** Plan's 7 new tests all fail for the right reason; checking a couple of last details before writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n '# Issue #' dokima/agent.py | head; grep -n "check-round" .github/workflows/agent.yml
```

> 62:    parts = [f"# Issue #{d['number']}: {d['title']}", "", d["body"] or "", "", "## Comments"]
> 217:          CHECK="$CHECK && python3 -m dokima.agent check-round $ROLE $OUT/$FILE $PACK"

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote a plan with three criteria and one fail-closed requirement, and seven new tests in tests/test_issue_links.py.",
          "It adjusted two existing tests so the planner case in each carries empty links and the fake GitHub answers the open-issue listing."],
  "decided": ["Only the planner's round check asks for links; the worker's and the reviewer's never do.",
              "A link must name an issue that is open now and listed in the pack; a pull request or the issue itself is refused."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of this story, and each of its seven new tests fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 3 adds that the worker's and reviewer's round checks never ask for links; this is not new scope but the guard that the rule stays on the planner's hand-back the story names, so it is kept.",
   "evidence": "plan.json criterion 3, last sentence; tests/test_issue_links.py::test_only_the_planner_must_hand_back_links"},
  {"text": "The docstring of the pack test says it expects 'exactly the 250 issues' while it fakes 1050; the assertion itself checks all 1050.",
   "evidence": "tests/test_issue_links.py::test_the_planners_pack_holds_every_open_issue_of_the_repo docstring vs issues = list(range(1, 1051))"},
  {"text": "All seven new tests fail today on the right reason: no open_issues.json in the pack, no mention in the prompt, the round check accepting missing or wrong links, and the pack not failing when GitHub cannot list issues.",
   "evidence": "pytest -q tests/test_issue_links.py: 7 failed, each with its 250.N message (e.g. '250.1: the planner's pack has no open_issues.json', '250.4 ... DID NOT RAISE')"}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [
  {"title": "Three review hand-back tests fail on main because the review check now dema
```

> OK

**Agent:** I approved the plan for #250 and wrote the review to `/tmp/dokima-out/review.json`. It passes both hand-back checks.

- **Owner's asks:** the issue makes four asks, and each one maps to a part of the plan (250.1–250.3 and the fail-closed requirement, tested as 250.4). Nothing is dropped, and there are no questions to judge.
- **Tests:** I ran the seven new tests in `tests/test_issue_links.py` and all seven fail, each because the feature isn't there yet:
  - the pack has no `open_issues.json`;
  - the planner's prompt doesn't mention the file;
  - the round check lets missing links through, along with links to issue #999, a pull request, the issue itself, or one issue in two lists;
  - building the pack doesn't fail when GitHub can't list the issues.
- **Notes (none blocking):**
  - Criterion 3 adds that the worker's and reviewer's round checks never ask for links. That isn't new scope; it keeps the rule on the planner's hand-back, as the story says.
  - The pack test's docstring says "exactly the 250 issues", but the test checks all 1050.
- **Problem outside this issue:** three tests in `tests/test_fixer.py` and `tests/test_handback_check.py` also fail on main (commit 27453f2), before this plan's commit. The review check rejects their review hand-backs with "asks must list every ask in the owner's issue and comments". I listed it in `issues_found` as a proposed new issue.

On the full suite, the plan's commit gives 10 failures: those three plus the seven new tests.
