# reviewer (plan) for #231

Run: https://github.com/dokima-dev/dokima/actions/runs/37824213007

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #231: The planner finds the issues this one blocks, is blocked by, or relates to
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
> Today nothing finds links between this issue and the ones already open. Blocking is only tracked between sibling stories of one split, and the reviewer's issues found are new issues, not links to existing ones.
> 
> What I want:
> - The planner's starter pack includes the repo's open issues.
> - The planner's prompt tells it explicitly to find which existing issues this one is blocked by, blocks, or relates to.
> - Its hand-back has a field for those three lists.
> - The checker validates that field like everything else, so there are no holes: real issue numbers, no issue linked to itself.
> - The card shows them with their own icons.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #231 (2026-10-08T18:05:49Z)
> 
> /autopilot start
> 
> ### dokima-r

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_issue_links.py; git show HEAD -- tests/test_fixer.py tests/conftest.py tests/helpers* | head -80
```

> commit 7b130ade45e79f6b9155411e43aa89587cdb6d88
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 18:25:39 2026 +0000
> 
>     planner for #231 (run 37822609938)
> 
>  tests/test_fixer.py       |   3 +
>  tests/test_issue_links.py | 290 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 293 insertions(+)
> """The planner finds the open issues this one is blocked by, blocks or relates to, and the owner sees them on the card.
> 
> Issue #231. The planner's starting pack holds the repo's open issues; its prompt tells it to find the links; its
> hand-back carries them in a `links` field of three lists; the round check every planner run does
> (`python3 -m dokima.agent check-round planner FILE PACK`) rejects a missing or malformed field, a number that is not
> one of the open issues in the pack, and a link to the issue itself; and the issue card shows each list with its own icon.
> 
> GitHub is faked: `gh issue view` and `gh pr list` answer for issue 231, and the repo's open issues are served to both
> ways of listing them, `gh issue list` (which honours `--limit`/`-L`, 30 by default, as gh does) and
> `gh api repos/o/r/issues` (which pages at `per_page`, 30 by default, unless `--paginate` is given, and also lists pull
> requests, each with a `pull_request` key, as GitHub's API does). Any other GitHub call fails the test naming it.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> import xml.etree.ElementTree as ET
> from urllib.pars

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 pytest -q tests/test_issue_links.py 2>&1 | grep -E "^(FAILED|E  |[0-9]+ (passed|failed))|AssertionError|Error" | head -40; timeout 900 pytest -q -x 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b7enpkk8l). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/5710172a-5192-4c5d-bff3-cab1b71fc936/tasks/b7enpkk8l.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "check-round\|check_round\|def check\b\|def check_\|\"check\"" dokima/*.py .github/workflows/*.yml | head -40
```

> dokima/card.py:100:    if not rec.get("check", {}).get("passed"):
> dokima/card.py:188:    reviews = [r for r in after if r.get("role") == "reviewer" and r.get("stage") == "pr" and r.get("check", {}).get("passed")]
> dokima/card.py:370:        return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
> dokima/planner.py:70:def check_source(where, source, issue):
> dokima/planner.py:76:def check_stories(stories, issue=None):
> .github/workflows/agent.yml:217:          CHECK="$CHECK && python3 -m dokima.agent check-round $ROLE $OUT/$FILE $PACK"
> dokima/checks.py:40:def check_name(key, text, limit=60):
> dokima/trail.py:20:def check_note(text):
> dokima/agent.py:86:        if r.get("role") == role and (r.get("check", {}).get("passed") or not passed):
> dokima/agent.py:93:    plans = [i for i, r in enumerate(recs) if r.get("role") == "planner" and r.get("check", {}).get("passed")]
> dokima/agent.py:97:               and r.get("check", {}).get("passed")]
> dokima/agent.py:112:        if r.get("role") == "reviewer" and (r.get("stage") or "") == stage and r.get("check", {}).get("passed"):
> dokima/agent.py:123:        if r.get("role") == "reviewer" and r.get("check", {}).get("passed"):
> dokima/agent.py:195:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> dokima/agent.py:206:           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()] if not passed else [

`5. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/5710172a-5192-4c5d-bff3-cab1b71fc936/tasks/b7enpkk8l.output; cd /home/runner/work/dokima/dokima; sed -n 205,225p .github/workflows/agent.yml
```

> E       AssertionError: 231.1: the planner's pack has no open_issues.json listing the repo's open issues
> E       assert False
> E        +  where False = <function isfile at 0x7f5fda7182c0>('/tmp/pytest-of-runner/pytest-0/test_the_planners_pack_holds_e0/pack/open_issues.json')
> E        +    where <function isfile at 0x7f5fda7182c0> = <module 'posixpath' (frozen)>.isfile
> E        +      where <module 'posixpath' (frozen)> = os.path
> tests/test_issue_links.py:107: AssertionError
> E       AssertionError: 231.2: the planner's prompt never points it at the pack's open_issues.json
> E       assert 'open_issues.json' in "# Where you are\nYou are Dokima's planner for one GitHub issue. In Dokima nothing merges until it is proven. You plan...heck; otherwise fix it.\nOnly the user_story kind is built on today; a feature is shown to the owner as handed back.\n"
> tests/test_issue_links.py:130: AssertionError
> E           AssertionError: 231.3: a hand-back with no links field passed the round check
> E           assert 0 == 1
> tests/test_issue_links.py:161: AssertionError
> E               AssertionError: 231.3: a story with a link to #999, no open issue passed the round check
> E               assert 0 == 1
> tests/test_issue_links.py:184: AssertionError
> E               AssertionError: 231.4: the issue card shows #12 (blocked by) on 0 lines, not one:
> E                 <!-- dokima-card -->
> E                 Links between issues.
> E                 
> E                 **Plan**
> E                 
> E            

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 pytest -q tests/test_issue_links.py 2>&1 | grep -E "^(FAILED|PASSED)|passed|failed"; timeout 300 pytest -q tests/test_issue_links.py -k "no_line or never_plans" 2>&1 | grep -E "^E  " | head -8; timeout 600 pytest -q 2>&1 | grep -E "^FAILED|passed|failed"
```

> >           assert code == 1, f"231.3: a hand-back with {name} passed the round check"
> E           AssertionError: 231.3: a hand-back with no links field passed the round check
> >               assert code == 1, f"231.3: a {kind} with {name} passed the round check"
> E               AssertionError: 231.3: a story with a link to #999, no open issue passed the round check
> FAILED tests/test_issue_links.py::test_the_planners_pack_holds_every_open_issue_of_the_repo - AssertionError: 231.1: the planner's pack has no open_issues.json listing the repo's open issues
> FAILED tests/test_issue_links.py::test_the_planners_prompt_tells_it_to_find_and_hand_back_the_links - AssertionError: 231.2: the planner's prompt never points it at the pack's open_issues.json
> FAILED tests/test_issue_links.py::test_the_links_field_must_be_there_and_well_formed - AssertionError: 231.3: a hand-back with no links field passed the round check
> FAILED tests/test_issue_links.py::test_links_name_only_real_open_issues_and_never_the_issue_itself - AssertionError: 231.3: a story with a link to #999, no open issue passed the round check
> FAILED tests/test_issue_links.py::test_the_card_shows_each_kind_of_link_with_its_own_icon - AssertionError: 231.4: the issue card shows #12 (blocked by) on 0 lines, not one:
> FAILED tests/test_issue_links.py::test_the_card_shows_no_line_for_a_kind_with_no_links - AssertionError: 231.4: the card for a plan blocking #15 draws no Blocks line with its own icon:
> FAILED tests/test_issue_links.py

**Agent:** Reviewing the plan for #231: all seven new tests fail for the right reason. I'm now checking whether three unrelated failures already happen without this commit.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git stash -q 2>/dev/null; git checkout -q HEAD~1 -- tests/test_fixer.py; timeout 300 pytest -q tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner tests/test_handback_check.py 2>&1 | tail -3; git checkout -q HEAD -- tests/test_fixer.py; git status --short
```

> +     '"criterion": "N.k" or "missing"}',
>     )
> 3 failed, 5 passed in 0.98s

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote four criteria: the planner's pack lists every open issue, its prompt asks for the three kinds of link, the round check validates the links field, and the issue card shows each kind with its own icon.",
          "It wrote seven tests in tests/test_issue_links.py and taught one helper in tests/test_fixer.py to answer the new open-issues listing."],
  "decided": ["A link must name an open issue listed in the pack, never a pull request or the issue itself.",
              "If GitHub cannot list the open issues, the planner's pack fails and the hand-back is refused."],
  "open": ["It asks whether the planner's run comment should also show the links; it planned for the issue card only."]},
 "verdict": "approve",
 "summary": "The plan covers all five asks, and each of its seven new tests fails today because the feature is missing; one question about which card shows the links goes to the owner.",
 "blockers": [],
 "notes": [
  {"text": "The owner wrote \"real issue numbers\"; the plan accepts only issues that are open now, so a link to a closed issue is refused. This matches the ask, since the pack holds only open issues, but a plan can never say it relates to a closed issue.",
   "evidence": "plan.json criterion 3; tests/test_issue_links.py::test_links_name_only_real_open_issues_and_never_the_issue_itself"},
  {"text": "The round check that validates links runs in every planner run's CHECK, so a bad links field fails the planner's record like any other check problem.",
   "evidence": ".github/workflows/agent.yml:217 appends `dokima.agent check-round $ROLE` to every role's CHECK"}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [
  {"title": "Three review-check tests fail on main since plan reviews must list asks",
   "why": "Tests that are already red hide new failures and make every run of the suite noisy.",
   "evidence": "Run on main (without t
```

> OK

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git status --short; git stash list | head -2
```

> (Bash completed with no output)

**Agent:** I approved the plan for #231, but its one question about which card shows the links goes back to you. The review is saved in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**The plan:** It has four criteria:
1. The planner's starting pack lists every open issue in the repo.
2. The planner's prompt asks which issues this one is blocked by, blocks and relates to.
3. The round check rejects a missing or malformed links field, a number that isn't an open issue (including a pull request), and the issue linked to itself.
4. The issue card shows each kind of link on its own line with its own icon, on the issue and on its pull request.

There is also an extra rule: if GitHub can't list the open issues, building the pack fails and the planner's hand-back is refused.

**The tests:** I ran all seven new tests in `tests/test_issue_links.py` and each fails today because the feature is missing, not because of a crash or a bad path. The links check runs in every planner run's check (`.github/workflows/agent.yml:217`), so a bad links field fails the planner's run.

**Your five asks:** Each one maps to a criterion: the pack to 1, the prompt to 2, the field and the checker to 3, and the card to 4. None is missing.

**The question I didn't accept:** "The card shows them" could mean the card at the top of the issue, or the planner's run comment, which is now also a short card (#228). The planner chose the top card only. That's a reasonable reading and doesn't change how the system works or what it costs. But neither your words nor AGENTS.md settles which you meant, so on autopilot the plan stops here for your answer.

**Notes:**
- The plan reads "real issue numbers" as "open now", so a plan can never link to a closed issue.
- Outside this issue, three existing tests already fail on main without this commit: `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner` and two in `tests/test_handback_check.py`. Each says review hand-backs must list asks. The rest of the suite passes (467 tests). I proposed a separate issue for these.
