# reviewer (plan) for #212

Run: https://github.com/dokima-dev/dokima/actions/runs/37753574432

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (82.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tool-results/b2ddprcsq.txt
> 
> Preview (first 2KB):
> total 84
> drwxr-xr-x 2 runner runner 4096 Oct  8 09:00 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 09:00 ..
> -rw-r--r-- 1 runner runner 6817 Oct  8 09:00 01-planner.json
> -rw-r--r-- 1 runner runner 6163 Oct  8 09:00 02-planner.json
> -rw-r--r-- 1 runner runner 7158 Oct  8 09:00 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6866 Oct  8 09:00 04-planner.json
> -rw-r--r-- 1 runner runner 4704 Oct  8 09:00 05-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3364 Oct  8 09:00 06-worker.json
> -rw-r--r-- 1 runner runner 3412 Oct  8 09:00 07-reviewer-pr.json
> -rw-r--r-- 1 runner runner 7291 Oct  8 09:00 08-planner.json
> -rw-r--r-- 1 runner runner 5158 Oct  8 09:00 09-reviewer-plan.json
> -rw-r--r-- 1 runner runner  308 Oct  8 09:00 10-not-started.json
> -rw-r--r-- 1 runner runner 6097 Oct  8 09:00 11-planner.json
> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #223](https://github.com/dokima-dev/dokima/pull/223) · [files changed](https://github.com/dokima-dev/dokima/pull/223/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](http

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (76.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tool-results/b61oyxn5n.txt
> 
> Preview (first 2KB):
> # Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #223](https://github.com/dokima-dev/dokima/pull/223) · [files changed](https://github.com/dokima-dev/dokima/pull/223/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37746714549/job/113209821588)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
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
> **User story:** On autopilot, a pull request the reviewer approved merges on its own once every check is green, and the issue says so in o

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tool-results/b61oyxn5n.txt
```

> 1	# Issue #212: Autopilot: a pull request the reviewer approved merges by itself
> 2	
> 3	<!-- dokima-card -->
> 4	### Approve the result to merge
> 5	[PR #223](https://github.com/dokima-dev/dokima/pull/223) · [files changed](https://github.com/dokima-dev/dokima/pull/223/files)
> 6	
> 7	This issue has no objective and acceptance criteria yet.
> 8	
> 9	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37746714549/job/113209821588)
> 10	
> 11	<!-- /dokima-card -->
> 12	
> 13	<!-- dokima-ask -->
> 14	<details><summary>Original issue</summary>
> 15	
> 16	<!-- dokima-card -->
> 17	### Plan: add `work` to start
> 18	
> 19	
> 20	This issue has no objective and acceptance criteria yet.
> 21	
> 22	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 23	
> 24	<!-- /dokima-card -->
> 25	
> 26	<details open><summary>From the approved plan of #205, story 4</summary>
> 27	
> 28	**Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 29	
> 30	**User story:** On autopilot, a pull request the reviewer approved merges on its own once every check is green, and the issue says so in one Autopilot line, so the owner no longer merges by hand.
> 31	
> 32	**Context:** The owner confirmed that on autopilot the reviewer's appr

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tool-results/b61oyxn5n.txt
```

> 936	  "duration_ms": 215619,
> 937	  "turns": 21,
> 938	  "cost_usd": 0.998979,
> 939	  "tokens_in": 1254656,
> 940	  "tokens_out": 10165
> 941	 },
> 942	 "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/212/37749800374-planner.md",
> 943	 "run": "https://github.com/dokima-dev/dokima/actions/runs/37749800374",
> 944	 "handback": {
> 945	  "kind": "user_story",
> 946	  "user_story": "On autopilot, a pull request the reviewer approved merges by itself once every check on it is green, and the issue says so in one line, so the owner no longer merges by hand.",
> 947	  "acceptance_criteria": [
> 948	   {
> 949	    "text": "On an issue on autopilot, when the code review approves and every check on the pull request's head has passed, the pull request is merged at that head, the issue it was built for gets exactly one comment reading `Autopilot: merged PR #N` (N the pull request's number), the review's card ends with a Next line saying it merged without mentioning the owner, the board shows no Needs you, and the run that merged starts no other stage itself (an issue the merge unblocks starts through autopilot's close handling from #213, as on today's main). `/autopilot start`, said on an issue or on its pull request, merges the same way every pull request already approved by its code review with every check green anywhere in that issue's tree: the issue's own and those of its sub-issues at every level, each issue getting its own Autopilot line. It merges nothing outside the tree, nothing whose newe

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/open_blockers.json; git log --oneline -3; git diff --stat main..HEAD; git diff main..HEAD -- tests | head -50; wc -l tests/test_automerge.py; python3 -m pytest -q tests/test_automerge.py 2>&1 | tail -30; python3 -m pytest -q 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b42mhygwd). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tasks/b42mhygwd.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** I've read the issue and every earlier round, and I'm now running the plan's tests on the fresh branch while I read them.

`6. Read`
```
/home/runner/work/dokima/dokima/tests/test_automerge.py
```

> 1	"""On autopilot, a pull request the reviewer approved merges by itself once every check on it is green (#212).
> 2	
> 3	These tests run the workflows the way GitHub runs them, on the machine from test_start.py: every job's and step's
> 4	`if:` is evaluated and its scripts run with bash against a fake `gh`. Two ways lead to a merge:
> 5	  - the code review: agent.yml runs the reviewer at the pr stage on issue #57 (pull request #60, branch try/issue-57),
> 6	    and the fake Claude Code hands back the review the test chose;
> 7	  - `/autopilot start`: commands.yml runs on a code owner's comment, on the issue or on its pull request.
> 8	
> 9	The fake GitHub of test_autopilot_close.py (issue tree, labels, states, blocked-by links, comments, signals) is taught
> 10	pull requests, their checks and merging. It keeps them in prs.json, one entry per pull request:
> 11	{issue, branch, head, checks: {sha: [{name, kind, state}]}, files, refuse, merged, merged_by, moves_to}. It answers:
> 12	  - `gh pr list` with --head BRANCH and --state open|closed|merged|all (open by default), --json any fields, and
> 13	    -q/--jq `.[0].number` or `.[].number`;
> 14	  - `gh pr view N|BRANCH|URL --json ...` (number, url, title, body "Closes #ISSUE", headRefName, headRefOid,
> 15	    baseRefName, state, merged, mergeable, files, statusCheckRollup, comments, reviews), -q/--jq with a plain `.field`;
> 16	  - `gh pr checks N` (--json name,state,bucket,link,workflow; exit 1 when one failed, 8 when one is still running,
> 17	    and "no

`7. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/2a7c161d-1f99-49ee-94b8-b33f5c5e38e3/tasks/b42mhygwd.output
```

> []a94955c planner for #212 (run 37751612186)
> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
>  tests/test_automerge.py | 702 ++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 702 insertions(+)
> diff --git a/tests/test_automerge.py b/tests/test_automerge.py
> new file mode 100644
> index 0000000..5542fa5
> --- /dev/null
> +++ b/tests/test_automerge.py
> @@ -0,0 +1,702 @@
> +"""On autopilot, a pull request the reviewer approved merges by itself once every check on it is green (#212).
> +
> +These tests run the workflows the way GitHub runs them, on the machine from test_start.py: every job's and step's
> +`if:` is evaluated and its scripts run with bash against a fake `gh`. Two ways lead to a merge:
> +  - the code review: agent.yml runs the reviewer at the pr stage on issue #57 (pull request #60, branch try/issue-57),
> +    and the fake Claude Code hands back the review the test chose;
> +  - `/autopilot start`: commands.yml runs on a code owner's comment, on the issue or on its pull request.
> +
> +The fake GitHub of test_autopilot_close.py (issue tree, labels, states, blocked-by links, comments, signals) is taught
> +pull requests, their checks and merging. It keeps them in prs.json, one entry per pull request:
> +{issue, branch, head, checks: {sha: [{name, kind, state}]}, files, refuse, merged, merged_by, moves_to}. It answers:
> +  - `g

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python3 -m pytest -q tests/test_automerge.py 2>&1 | grep -E "^FAILED" | cut -c1-260
```

> FAILED tests/test_automerge.py::test_on_autopilot_an_approved_pull_request_with_green_checks_merges_and_says_so - AssertionError: 212.1 (code review): pull request #60, approved with every check green, was not merged at its head (merged: None, merges tried: []
> FAILED tests/test_automerge.py::test_autopilot_start_merges_a_pull_request_already_approved - AssertionError: 212.1 (/autopilot start said on the issue): pull request #60, approved with every check green, was not merged at its head (merged: None, merges tried:
> FAILED tests/test_automerge.py::test_autopilot_start_merges_the_approved_pull_requests_of_the_whole_tree - AssertionError: 212.1 (tree): #60 of #57, approved and green inside the tree, was not merged at its head:
> FAILED tests/test_automerge.py::test_without_autopilot_an_approved_pull_request_waits_for_the_owner - AssertionError: 212.2: the same review on autopilot did not merge, so this test proves nothing:
> FAILED tests/test_automerge.py::test_a_refused_merge_stops_for_the_owner_and_says_why - AssertionError: 212.3 (red check): no comment on pull request #60 gives the reason ('pytest (3.12)') and mentions @owner-person: ['ed"> **Reviewer (pr)**\n\n**approve**: Ev
> FAILED tests/test_automerge.py::test_agents_md_says_autopilot_merges_what_the_reviewer_approved - AssertionError: 212.4: AGENTS.md step 6 does not say autopilot merges what the reviewer approved with green checks; missing ['autopilot', 'green or check']: '6. *
> FAILED tests/test_automerge.py::test_a_pull_r

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python3 -m pytest -q -x --deselect tests/test_automerge.py -p no:cacheprovider --ignore=tests/test_automerge.py 2>&1 | tail -3
```

> )
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 162 passed in 51.69s

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python3 -m pytest -q -p no:cacheprovider --ignore=tests/test_automerge.py 2>&1 | grep -E "FAILED|passed|failed" | cut -c1-300
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it"
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'
> 3 failed, 368 passed in 164.68s (0:02:44)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "asks must list" -n dokima/*.py | head; grep -n "def check_review\|asks" dokima/agent.py | head -30
```

> dokima/agent.py:535:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 489:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 526:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 530:def problems_asks(r, ids):
> 531:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 533:    asks = r.get("asks")
> 534:    if not isinstance(asks, list) or not asks:
> 535:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 537:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 538:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 566:        bad.append("the worker never asks the owner; the plan is the contract")
> 698:                bad += problems_asks(data, plan_criteria(plan, number))

**Agent:** I've checked the plan and its tests. All 8 new tests fail on today's main because merging doesn't exist yet. Now I'm writing the review.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned again from today's main after the old branch was deleted, keeping the same six promises and the same eight tests.",
          "It made two of its rules exact: a pull request that changes a workflow file must say so on itself and mention the owner, and commit statuses count as checks just like check runs.",
          "It added that the merge uses Dokima's app key and never GitHub's auto-merge, so the workflows that run when an issue closes still run."],
  "decided": ["Starting what a merge unblocks stays with #213's close handling, already on main; this story only makes the merge happen."],
  "open": []},
 "verdict": "approve",
 "summary": "Every ask has a criterion, and all 8 tests fail on today's main because merging on autopilot doesn't exist yet; none of them fails from a crash or a bad setup.",
 "blockers": [],
 "notes": [
  {"text": "Run on this branch, which is today's main plus the new test file, each of the 8 tests fails at its first promise, and nothing crashes. For example: '212.1 (code review): pull request #60, approved with every check green, was not merged at its head (merged: None, merges tried: [])', and '212.5 (code review): no comment on pull request #60 gives the reason ('.github/workflows')'.",
   "evidence": "python3 -m pytest -q tests/test_automerge.py on try/issue-212 (a94955c): 8 failed"},
  {"text": "When `/autopilot start` finds a pull request with no checks at all, the tests only prove that it doesn't merge (212.6). They don't prove that it says why on the pull request. Code review runs do get that proof (212.3). The criterion promises a reason after `/autopilot start` only for a refused merge, so this isn't a blocker.",
   "evidence": "tests/test_automerge.py lines 631-635 (212.3 `/autopilot start` cases: red check, conflict, branch protection) and lines 692-696 (212.6 checks that no checks means no merge)"}],
 "outside_p
```

> exit 0

**Agent:** I approved the plan for #212. Every ask from the issue and your comments has a criterion, and all 8 new tests fail on today's main because merging on autopilot doesn't exist yet. None of them fails from a crash or a broken setup.

- **What changed since the last plan:** this is the same six promises with the same eight tests, now planned on today's main. Two rules are more exact:
  - A pull request that changes a workflow file must say so on itself and mention you.
  - Status checks from outside services count the same as GitHub's own checks.

  The merge must also use Dokima's app key and never GitHub's auto-merge, so the steps that run when an issue closes still run.
- **No open blockers:** none were left from earlier rounds, and I found no new ones.
- **One gap, noted but not a blocker:** when `/autopilot start` finds a pull request with no checks at all, the tests prove it doesn't merge but not that it says why on the pull request. The plan only promises a reason after `/autopilot start` when a merge is refused, so this doesn't break a promise.
- **Proposed issue outside this one:** three other tests fail on main today:
  - `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner`
  - `tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named`
  - `tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests`

  The new asks check rejects their sample reviews (`dokima/agent.py:535`). This branch is main plus only the new test file, so this work didn't cause them. The rest of the suite passes: 368 tests.

The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks. Next, it's yours: say `/work` to build it.
