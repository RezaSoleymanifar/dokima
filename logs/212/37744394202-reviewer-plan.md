# reviewer (plan) for #212

Run: https://github.com/dokima-dev/dokima/actions/runs/37744394202

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (44.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4d52d1bf-77ca-4d55-abcd-16df8e21d68e/tool-results/by6gmkszy.txt
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
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 4</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, a pull request the reviewer approved merges on its own once every check is green, and the issue says so in one Autopilot line, so the owner no longer merges by hand.
> 
> **Context:** The owner confirmed that on autopilot the reviewer's approval with green checks stands in for theirs. Today the code review's approve stops with 'Merge the pull request' (next_step in dokima/agent.py) and AGENTS.md flow step 6 says the owner approves and merges; AGENTS.md gets a short entry for the autopilot exception. The bot cannot approve, so where branch protection req

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (36.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4d52d1bf-77ca-4d55-abcd-16df8e21d68e/tool-results/bfash551g.txt
> 
> Preview (first 2KB):
> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 4</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, a pull request the reviewer approved merges on its own once every check is green, and the issue says so in one Autopilot line, so the owner no longer merges by hand.
> 
> **Context:** The owner confirmed that on autopilot the reviewer's approval with green checks stands in for theirs. Today the code review's approve stops with 'Merge the pull request' (next_step in dokima/agent.py) and AGENTS.md flow step 6 says the owner approves and merges; AGENTS.md gets a short entry for the autopilot exception. The bot cannot approve, so where branch protection requires a code owner's review the merge is refused and stops for the owner. Workflow-file changes already pause for the own

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/03-reviewer-plan.json'));print(json.dumps(d,indent=1)[:8000])"
```

> [
>  {
>   "id": "B1",
>   "criterion": "212.3",
>   "test": "tests/test_automerge.py::test_a_refused_merge_stops_for_the_owner_and_says_why",
>   "problem": "The criterion promises that a merge GitHub refuses after `/autopilot start` says why on the pull request and mentions the owner. The test covers `/autopilot start` only with a red check, which Dokima catches before it asks GitHub to merge. It never has GitHub refuse the merge on that path. Code that ignores GitHub's refusal after `/autopilot start`, posting nothing, would pass.",
>   "evidence": "tests/test_automerge.py line 612: the only `/autopilot start` case is `Command(..., APPROVED, {}, RED)`. The conflict and branch-protection cases (refuse=CONFLICT/PROTECTED, line 607) run only through `Review`.",
>   "fix": "Add a `/autopilot start` case with green checks where GitHub refuses (for example `Command(tmp_path / \"command-conflict\", APPROVED, {}, GREEN, refuse=CONFLICT)`), and assert `assert_waits(m, \"212.3\", \"/autopilot start, conflict\", CONFLICT)`.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "212.6",
>   "test": "tests/test_automerge.py::test_nothing_merges_unless_every_check_on_the_merging_commit_is_green",
>   "problem": "The rule that nothing merges unless every check on the very commit that merges has passed also covers `/autopilot start`. On that path the test tries only a running check. A new commit pushed after the checks were read, and no checks at all, are tested only through the code review. A `/autop

**Agent:** Now see the newest planner reply and the issue comments since review.

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/04-planner.json'));h=d['handback'];print(json.dumps({k:v for k,v in h.items() if k not in ('plan',)},indent=1)[:6000]); print(d.get('check'))"; sed -n '/Comments/,$p' issue.md | grep -n "^###\|^\*\*\|^## " | tail -40
```

> {
>  "kind": "user_story",
>  "user_story": "On autopilot, a pull request the reviewer approved merges by itself once every check on it is green, and the issue says so in one line, so the owner no longer merges by hand.",
>  "acceptance_criteria": [
>   {
>    "text": "On an issue on autopilot, when the code review approves and every check on the pull request's head has passed, the pull request is merged at that head, the issue it was built for gets exactly one comment reading `Autopilot: merged PR #N` (N the pull request's number), the review's card ends with a Next line saying it merged without mentioning the owner, the board shows no Needs you, and no other stage starts. `/autopilot start`, said on an issue or on its pull request, merges the same way every pull request already approved by its code review with every check green anywhere in that issue's tree: the issue's own and those of its sub-issues at every level, each issue getting its own Autopilot line. It merges nothing outside the tree, nothing whose newest code review blocks, and a pull request in the tree with a red check says on itself which check is red and mentions the owner.",
>    "source": "https://github.com/dokima-dev/dokima/issues/212"
>   },
>   {
>    "text": "On an issue not on autopilot, an approved pull request still waits for the owner exactly as today: no merge is tried, no Autopilot line is posted, the card still says \"Merge the pull request\" and mentions the owner, and the board shows Needs you. `/autopilot stop

`5. Bash`
```
cd /tmp/pack; sed -n '/^## Comments/,$p' issue.md | sed -n '1,6p;140,146p'; sed -n '/^## Comments/,$p' issue.md | sed -n '557,$p' | head -30; sed -n '1,/^## Comments/p' issue.md | sed -n '20,80p'
```

> ## Comments
> 
> ### RezaSoleymanifar on issue #212 (2026-10-08T06:58:17Z)
> 
> /plan
> 
> 
> 
> ### RezaSoleymanifar on issue #212 (2026-10-08T07:21:57Z)
> 
> /plan On the first question: the whole tree. As #205 settled, starting autopilot picks up what is already waiting anywhere under the issue, so already approved PRs of sub-issues merge too. Your other two assumptions are right.
> 
> ### dokima-runtime on issue #212 (2026-10-08T07:22:15Z)
> ### dokima-runtime on issue #212 (2026-10-08T07:35:36Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> **Reviewer (plan)** · getting ready
> 
> The machine is getting ready. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37744394202)</sub>
> 
> 
> **Acceptance criteria:**
> - On an issue on autopilot, when the code review approves and every required check on the pull request has passed, the pull request is merged, the issue it was built for gets exactly one comment reading `Autopilot: merged PR #N` (N the pull request's number), and the card says it merged; `/autopilot start` said on an issue whose pull request is already approved by the reviewer with green checks merges it the same way. ([source](https://github.com/dokima-dev/dokima/issues/205))
> - On an issue not on autopilot, an approved pull request still waits for the owner to merge it, exactly as today, and

**Agent:** No new owner words since last review. Check the test changes and run it.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 9598d50 80463a5 --stat; git diff 9598d50 80463a5 -- tests/ | head -200; python3 -m pytest -q tests/test_automerge.py 2>&1 | tail -30
```

> tests/test_automerge.py | 37 ++++++++++++++++++++++++++++++-------
>  1 file changed, 30 insertions(+), 7 deletions(-)
> diff --git a/tests/test_automerge.py b/tests/test_automerge.py
> index 7de8077..0a31940 100644
> --- a/tests/test_automerge.py
> +++ b/tests/test_automerge.py
> @@ -599,7 +599,8 @@ def test_a_refused_merge_stops_for_the_owner_and_says_why(record_property, tmp_p
>      GitHub refusing for branch protection (its words must be on the pull request). Each must leave #60 unmerged, post
>      no Autopilot line, mention the owner on #60 with the reason, show Needs you on the board and start nothing else.
>      `/autopilot start` on an approved pull request with a red check must likewise merge nothing and say on #60 which
> -    check is red, mentioning the owner."""
> +    check is red, mentioning the owner; and with every check green but GitHub refusing (a conflict, then branch
> +    protection), it must try the merge, leave #60 unmerged and give GitHub's words on #60, mentioning the owner."""
>      record_property("proves", "212.3")
>      cases = (("red check", RED, "", RED_NAME), ("no checks", [], "", "no checks"),
>               ("conflict", GREEN, CONFLICT, CONFLICT), ("branch protection", GREEN, PROTECTED, PROTECTED))
> @@ -612,21 +613,31 @@ def test_a_refused_merge_stops_for_the_owner_and_says_why(record_property, tmp_p
>      m = Command(tmp_path / "command-red", APPROVED, {}, RED)
>      m.listen("/autopilot start")
>      assert_waits(m, "212.3", "/autopilot start, red check", RED_NAME)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_automerge.py 2>&1 | grep -E "^FAILED|^ERROR"; grep -n "moves" tests/test_automerge.py | head -20
```

> FAILED tests/test_automerge.py::test_on_autopilot_an_approved_pull_request_with_green_checks_merges_and_says_so - AssertionError: 212.1 (code review): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> FAILED tests/test_automerge.py::test_autopilot_start_merges_a_pull_request_already_approved - AssertionError: 212.1 (/autopilot start on the issue): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> FAILED tests/test_automerge.py::test_autopilot_start_merges_the_approved_pull_requests_of_the_whole_tree - AssertionError: 212.1 (tree): /autopilot start on #57 should merge exactly #60, #61 and #63 (approved, green, inside the tree); it merged []:
> FAILED tests/test_automerge.py::test_without_autopilot_an_approved_pull_request_waits_for_the_owner - AssertionError: 212.2: test control: on autopilot the same review did not merge:
> FAILED tests/test_automerge.py::test_a_refused_merge_stops_for_the_owner_and_says_why - AssertionError: 212.3 (red check): no comment on pull request #60 mentions @owner-person and says why ('Unit tests (3.12)'): [': [],\n  "resolved": [],\n  "asks": [\n   {\n    "ask": "Fix it.",\n    "source": "https://github.com/o/r/issues/57",\n    "criterion": "57.1"\n   }\n  ]\n },\n "check": {\n  "passed": true,\n  "problems": []\n }\n}\n```\n\n</details>\n\n<sub>Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-pr.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
prev=json.load(open('in/03-reviewer-plan.json'))['handback']
r={"previous_step":{"did":[
 "The planner added `/autopilot start` cases to 212.3's test where every check is green but GitHub refuses the merge, once for a conflict and once for branch protection.",
 "It added `/autopilot start` cases to 212.6's test with no checks and with a new commit pushed while it merges, plus a case where every check is green and the pull request must merge at its head.",
 "It tightened 212.4's test: step 6 of AGENTS.md must name the approval and green checks, and must not say autopilot never merges."],
 "decided":["The criteria are unchanged from the last round."],
 "open":["An older test for 188.3 still fails on main and is not this issue's to fix."]},
 "verdict":"approve",
 "summary":"Every ask has a criterion and every criterion now has a test that fails today because merging on autopilot does not exist yet, including the `/autopilot start` cases that were missing.",
 "blockers":[],
 "notes":[{"text":"In 212.3's test, the new `/autopilot start` refusal cases come after the code-review cases, so today the test stops at the first code-review case. Each `/autopilot start` case still has its own named failure, so once merging exists a gap there shows up by name.","evidence":"pytest -q tests/test_automerge.py: 212.3 fails at '212.3 (red check): no comment on pull request #60 mentions @owner-person'; the new cases are at tests/test_automerge.py lines 616-621."}],
 "outside_plan":[],
 "resolved":["B1","B2"],
 "issues_found":prev["issues_found"],
 "asks":prev["asks"]}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 212 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for #212. Both blockers from the last review are fixed, and both checks on the review file pass.

- **B1 (212.3), fixed:** the test now also runs `/autopilot start` when every check is green but GitHub refuses the merge, once for a conflict and once for branch protection. In each case it checks that a merge was tried, the pull request stays open, no Autopilot line is posted, and GitHub's reason appears on the pull request with the owner mentioned.
- **B2 (212.6), fixed:** `/autopilot start` is now tested with a check still running, with no checks, and with a new commit pushed while it merges. None of these may merge. A new control case checks that it does merge at the head when every check is green.
- **212.4 test tightened:** the AGENTS.md test now needs step 6 to mention the approval and green checks, and fails if it says autopilot never merges. This answers my earlier note.

All 8 tests in `tests/test_automerge.py` fail today for the right reason: merging on autopilot doesn't exist yet. None fails from a crash or a broken setup. The owner hasn't commented since the last review, and every ask still maps to a criterion.

I left one note: in the 212.3 test, the new `/autopilot start` cases come after the code-review cases. So today the test stops at the first code-review case and never reaches them. Each one has its own named failure message, though, so once merging exists a gap there will show up by name.

The older 188.3 test that fails on main is still listed as a separate issue for the owner to file.

The review is in `/tmp/dokima-out/review.json`.
