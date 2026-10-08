# reviewer (plan) for #212

Run: https://github.com/dokima-dev/dokima/actions/runs/37743844404

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct  8 07:30 .
> drwxrwxrwt 18 root   root    4096 Oct  8 07:30 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 07:30 in
> -rw-r--r--  1 runner runner 19590 Oct  8 07:30 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 07:30 open_blockers.json
> -rw-r--r--  1 runner runner  5534 Oct  8 07:30 plan.json
> 
> in:
> total 24
> drwxr-xr-x 2 runner runner 4096 Oct  8 07:30 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 07:30 ..
> -rw-r--r-- 1 runner runner 6817 Oct  8 07:30 01-planner.json
> -rw-r--r-- 1 runner runner 6163 Oct  8 07:30 02-planner.json
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
> **Context:** The owner confirmed that on autopilot the reviewer's approval with green checks stands in for theirs. Today the code review's approve stops w

`2. Bash`
```
cd /home/runner/work/dokima/dokima; wc -l tests/test_automerge.py; cat tests/test_automerge.py
```

> <persisted-output>
> Output too large (38KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/93c13abd-e363-4079-bb32-8a4b619d4973/tool-results/bss2uib2i.txt
> 
> Preview (first 2KB):
> 671 tests/test_automerge.py
> """On autopilot, a pull request the reviewer approved merges by itself once every check is green (#212).
> 
> These tests run the real workflows the way GitHub runs them, on the machine from test_start.py: the agent workflow
> (.github/workflows/agent.yml) for the code review of pull request #60, built for issue #57, and the command listener
> (.github/workflows/commands.yml) for `/autopilot start`. Every step's `if:` is evaluated and its script run with bash
> against a fake `gh`, which here also knows issue #57's labels (the issue tree and label calls of test_autopilot.py) and
> pull request #60 as GitHub would show it:
> 
> - its head commit, the tip of try/issue-57, and the checks GitHub reports on each commit;
> - the files it changes;
> - whether it is merged, and every merge call.
> 
> A test can add more open pull requests, each built for another issue of the tree on its own real try/issue-N branch,
> with that issue's history (`gh issue view N`, or GET on repos/o/r/issues/N/comments); comments posted on such a pull
> request are kept on it. Without a selector, a `gh pr` call means #60.
> 
> GitHub answers about a pull request through any of: `gh pr view` (a number, URL or branch, `--json` with every field: number,
> headRefName, headRefOid, body, state, mergeable

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,330p tests/test_automerge.py
```

> """On autopilot, a pull request the reviewer approved merges by itself once every check is green (#212).
> 
> These tests run the real workflows the way GitHub runs them, on the machine from test_start.py: the agent workflow
> (.github/workflows/agent.yml) for the code review of pull request #60, built for issue #57, and the command listener
> (.github/workflows/commands.yml) for `/autopilot start`. Every step's `if:` is evaluated and its script run with bash
> against a fake `gh`, which here also knows issue #57's labels (the issue tree and label calls of test_autopilot.py) and
> pull request #60 as GitHub would show it:
> 
> - its head commit, the tip of try/issue-57, and the checks GitHub reports on each commit;
> - the files it changes;
> - whether it is merged, and every merge call.
> 
> A test can add more open pull requests, each built for another issue of the tree on its own real try/issue-N branch,
> with that issue's history (`gh issue view N`, or GET on repos/o/r/issues/N/comments); comments posted on such a pull
> request are kept on it. Without a selector, a `gh pr` call means #60.
> 
> GitHub answers about a pull request through any of: `gh pr view` (a number, URL or branch, `--json` with every field: number,
> headRefName, headRefOid, body, state, mergeable, mergeStateStatus, files, statusCheckRollup, comments, reviews),
> `gh pr list` (open, merged or all, with --head or --search head:...), `gh pr checks` (with or without --required; with --json, or as text exiting 1 on a
> failed check and 8 on a

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 330,671p tests/test_automerge.py
```

> "models": ["claude-opus-5-5"], "handback": review, "check": {"passed": True, "problems": []}}
> 
> 
> BUILT = ts.STORY_APPROVED + [ts.record_comment(worker_record(), "2026-10-07T11:00:00Z")]
> APPROVED = BUILT + [ts.record_comment(pr_review_record(PR_APPROVE), "2026-10-07T11:30:00Z")]
> BLOCKED = BUILT + [ts.record_comment(pr_review_record(PR_BLOCK), "2026-10-07T11:30:00Z")]
> 
> 
> def set_pr(m, checks, workflow_file=False, refuse="", moves=False):
>     """Give the machine's pull request #60 its head (the try branch's tip), checks and files, and what GitHub refuses.
> 
>     With workflow_file, the try branch first gets a commit that changes .github/workflows/extra.yml, so the branch and
>     GitHub's file list agree. With moves, a new commit with its checks still running becomes the head the moment code
>     first reads the head or its checks."""
>     src = f"{m.tmp}/src"
>     if workflow_file:
>         os.makedirs(f"{src}/.github/workflows", exist_ok=True)
>         open(f"{src}/.github/workflows/extra.yml", "w").write("name: extra\non: push\njobs: {}\n")
>         sh(src, "git", "add", "-A")
>         sh(src, "git", "commit", "-qm", "workflow")
>         sh(src, "git", "push", "-q", "origin", f"try/issue-{N}")
>         m.try_sha = sh(src, "git", "rev-parse", "HEAD")
>     files = sh(src, "git", "diff", "--name-only", f"main...try/issue-{N}").split()
>     later = "b" * 40
>     state = {"issue": int(N), "branch": f"try/issue-{N}", "head": m.try_sha,
>              "checks": {m.try_sha: checks, later: [{"name": "Al

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_automerge.py 2>&1 | grep -E "^(FAILED|PASSED|E  )|passed|failed" | head -60
```

> assert m.agent_started(), f"212.1: test setup: the code review never ran; it stopped at '{m.failed_step}':\n{m.tail()}"
> E       AssertionError: 212.1 (code review): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> E         ## run: Decide what follows, and say it on the card (exit 0)
> E         stop
> E         
> E         ## run: Post the record as a comment, on the PR once there is one (exit 0)
> E         iewer\",\n \"stage\": \"pr\",\n \"run_id\": \"42\",\n \"commit_before\": \"540223053ffdfc08fddfcde85dc1a7e7250f9180\",\n \"started_by\": \"owner-person\",\n \"models\": [\n  \"claude-opus-5-5\"\n ],\n \"report\": {\n  \"duration_ms\": 1000,\n  \"turns\": 1,\n  \"cost_usd\": null,\n  \"tokens_in\": 0,\n  \"tokens_out\": null\n },\n \"log\": \"https://github.com/o/r/blob/logs/logs/57/42-reviewer-pr.md\",\n \"run\": \"https://github.com/o/r/actions/runs/42\",\n \"handback\": {\n  \"previous_step\": {\n   \"did\": [\n    \"Built x.py.\"\n   ],\n   \"decided\": [],\n   \"open\": []\n  },\n  \"stage\": \"pr\",\n  \"round\": 1,\n  \"verdict\": \"approve\",\n  \"summary\": \"Every criterion has its proof.\",\n  \"blockers\": [],\n  \"notes\": [],\n  \"outside_plan\": [],\n  \"resolved\": [],\n  \"asks\": [\n   {\n    \"ask\": \"Fix it.\",\n    \"source\": \"https://github.com/o/r/issues/57\",\n    \"criterion\": \"57.1\"\n   }\n  ]\n },\n \"check\": {\n  \"passed\": true,\n  \"problems\": []\n }\n}\n```\n\n</details>\n\n<sub>Opus 5

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_automerge.py 2>&1 | grep -E "^E +AssertionError|passed|failed" | cut -c1-300
```

> assert m.agent_started(), f"212.1: test setup: the code review never ran; it stopped at '{m.failed_step}':\n{m.tail()}"
> E       AssertionError: 212.1 (code review): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
> E         iewer\",\n \"stage\": \"pr\",\n \"run_id\": \"42\",\n \"commit_before\": \"3b57d2afefee7e7073432b96e1f8c4e0b80d154e\",\n \"started_by\": \"owner-person\",\n \"models\": [\n  \"claude-opus-5-5\"\n ],\n \"report\": {\n  \"duration_ms\": 1000,\n  \"turns\": 1,\n  \"cost_usd\": null,\n  \"toke
>             assert not m.failed, f"212.1 ({case}): the listener failed on /autopilot start:\n{m.tail()}"
> E       AssertionError: 212.1 (/autopilot start on the issue): the approved pull request with green checks was not merged at its head (merged: None, merge calls: []):
>         assert not m.failed, f"212.1 (tree): the listener failed on /autopilot start:\n{m.tail()}"
> E       AssertionError: 212.1 (tree): /autopilot start on #57 should merge exactly #60, #61 and #63 (approved, green, inside the tree); it merged []:
>         assert m.agent_started(), f"212.2: test setup: the code review never ran; it stopped at '{m.failed_step}':\n{m.tail()}"
> E       AssertionError: 212.2: test control: on autopilot the same review did not merge:
> E         iewer\",\n \"stage\": \"pr\",\n \"run_id\": \"42\",\n \"commit_before\": \"fe396541e660cdd81f728174913aec4622bd9714\",\n \"started_by\": \"owner-person\",\n \"models\": [\n  \"claude

**Agent:** Running the plan's tests is done: all 8 fail today because the feature is missing. Next I'm checking a pre-existing failure the planner mentioned, then writing the review.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_cancelled_run.py 2>&1 | tail -3; sed -n '/^## The flow/,/^## Commands/p' AGENTS.md | grep -n "6\."
```

> assert (0 == 1)
>  +  where 0 = len([])
> 1 failed, 3 passed in 5.79s
> 8:6. **Merge.** The owner approves and merges.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner re-planned after the owner's answer: `/autopilot start` now merges every already-approved pull request with green checks anywhere in the issue's tree, each issue getting its own Autopilot line.",
   "It added a test with a three-level tree, a blocked pull request, a red one and one outside the tree."
  ],
  "decided": [
   "Every check on the pull request's head must pass, not only those branch protection requires; the earlier review's card is not edited (both confirmed by the owner)."
  ],
  "open": [
   "An older test for 188.3 already fails on main and is not this issue's to fix."
  ]
 },
 "verdict": "block",
 "summary": "The plan covers every ask, but two of its promises about `/autopilot start` have no test: a merge GitHub refuses after `/autopilot start`, and a new commit pushed while `/autopilot start` is merging.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "212.3",
   "test": "tests/test_automerge.py::test_a_refused_merge_stops_for_the_owner_and_says_why",
   "problem": "The criterion promises that a merge GitHub refuses after `/autopilot start` says why on the pull request and mentions the owner. The test covers `/autopilot start` only with a red check, which Dokima catches before it asks GitHub to merge. It never has GitHub refuse the merge on that path. Code that ignores GitHub's refusal after `/autopilot start`, posting nothing, would pass.",
   "evidence": "tests/test_automerge.py lines 593-595: the only `/autopilot start` case is `Command(..., APPROVED, {}, RED)`. The conflict and branch-protection cases (refuse=CONFLICT/PROTECTED, lines 584-585) run only through `Review`.",
   "fix": "Add a `/autopilot start` case with green checks where GitHub refuses (for example `Command(tmp_path / \"command-conflict\", APPROVED, {}, GREEN, refuse=CONFLICT)`), and assert `assert_waits(m, \"212.3\", \"/autopilot start, conflict\", CONFLICT)`."
```

> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "command-red\|refuse=refuse\|command-running\|(\"one red\"" tests/test_automerge.py
```

> 607:        m = Review(tmp_path / case.replace(" ", "-"), PR_APPROVE, {57: [LABEL]}, checks, refuse=refuse)
> 612:    m = Command(tmp_path / "command-red", APPROVED, {}, RED)
> 659:    cases = (("one red", RED, False), ("one running", PENDING, False), ("none", [], False), ("head moved", GREEN, True))
> 667:    m = Command(tmp_path / "command-running", APPROVED, {}, PENDING)

`10. Bash`
```
cd /tmp/dokima-out; sed -i 's/lines 593-595: the only/line 612: the only/; s/(refuse=CONFLICT\/PROTECTED, lines 584-585) run only/(refuse=CONFLICT\/PROTECTED, line 607) run only/; s/lines 657-659: the only/line 667: the only/; s/(line 646) run only/(line 659) run only/' review.json; grep -o "line[s]* [0-9-]*" review.json; cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 212 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> line 612
> line 607
> line 667
> line 659
> line 
> line 
> rc=0

**Agent:** I reviewed the plan for #212 and blocked it. It goes back to the planner to fix two tests.

All 8 of the plan's new tests fail today, and for the right reason: autopilot doesn't merge yet and AGENTS.md doesn't mention it. Every ask in the issue and in your comment from 07:21 maps to a criterion, including merging approved pull requests across the whole tree.

**Blockers (both for the planner):**
- **B1 (212.3):** The plan promises that when GitHub refuses a merge after `/autopilot start`, the pull request says why and mentions you. The only `/autopilot start` case in the test is a red check (`tests/test_automerge.py:612`), and Dokima catches that before it ever asks GitHub to merge. The conflict and branch-protection cases only run through the code review path (line 607). Code that stays silent when GitHub refuses a `/autopilot start` merge would pass. Fix: add a `/autopilot start` case with green checks where GitHub refuses the merge.
- **B2 (212.6):** The rule "nothing merges unless every check on the exact commit that merges has passed" also applies to `/autopilot start`. On that path the test only tries a check that is still running (line 667). The other two cases, a new commit pushed after the checks were read and no checks at all, only run through the code review (line 659). So a `/autopilot start` merge that isn't pinned to the commit it checked would pass every test. Fix: add both cases to the `/autopilot start` part of the test.

**Notes (not blocking):**
- The AGENTS.md test only checks that step 6 contains the words "merge" and "autopilot". A step saying autopilot never merges would pass it.
- In the workflow-file test (212.5), the code-review case already passes today, because the usual approval card mentions you. It doesn't show that the pull request says *why* it's waiting.

**Proposed new issue:** `tests/test_cancelled_run.py::test_nothing_starts_by_itself_after_a_cancel_or_a_failure` (188.3) fails on this branch too, not only on main. I reran it and got 1 failed, 3 passed. The planner also flagged it as unrelated to this issue.

The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.
