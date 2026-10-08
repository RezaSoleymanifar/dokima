# reviewer (plan) for #179

Run: https://github.com/dokima-dev/dokima/actions/runs/37737441139

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ====; cat open_blockers.json; echo ===; cat plan.json
```

> <persisted-output>
> Output too large (63.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/25534f5b-b4b1-4f9a-8565-0533b7a0a743/tool-results/b4dtdw7xi.txt
> 
> Preview (first 2KB):
> total 60
> drwxr-xr-x 2 runner runner 4096 Oct  8 06:26 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 06:26 ..
> -rw-r--r-- 1 runner runner 5002 Oct  8 06:26 01-planner.json
> -rw-r--r-- 1 runner runner 3655 Oct  8 06:26 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5829 Oct  8 06:26 03-planner.json
> -rw-r--r-- 1 runner runner 2610 Oct  8 06:26 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3880 Oct  8 06:26 05-worker.json
> -rw-r--r-- 1 runner runner 4095 Oct  8 06:26 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 9431 Oct  8 06:26 07-planner.json
> -rw-r--r-- 1 runner runner 5786 Oct  8 06:26 08-planner.json
> # Issue #179: The owner's ask is kept below a fixed marker and never rewritten
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #200](https://github.com/dokima-dev/dokima/pull/200) · [files changed](https://github.com/dokima-dev/dokima/pull/200/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37737107500/job/113179044729)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 1</summary>
> 
> **Part of:** #143 C

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (58.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/25534f5b-b4b1-4f9a-8565-0533b7a0a743/tool-results/bwowk6ek1.txt
> 
> Preview (first 2KB):
> # Issue #179: The owner's ask is kept below a fixed marker and never rewritten
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #200](https://github.com/dokima-dev/dokima/pull/200) · [files changed](https://github.com/dokima-dev/dokima/pull/200/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37737107500/job/113179044729)
> 
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #143, story 1</summary>
> 
> **Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 
> **User story:** Owners can trust that whatever code redraws on an issue, their original ask below the marker stays exactly as they wrote it.
> 
> **Context:** Split rules R1, R2 and R3: #143 holds several independent goals (body protection, the issue/PR card's content, its status and children, run cards, a backfill), needs well over five criteria, and spans dokima/planner.py, dokima/card.py, dokima/agent.py, dokima/roles/ and AGENTS.md. This story keeps the promise moved in from #48. Today dokima/planner.py render() folds the ow

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/25534f5b-b4b1-4f9a-8565-0533b7a0a743/tool-results/bwowk6ek1.txt
```

> 1	# Issue #179: The owner's ask is kept below a fixed marker and never rewritten
> 2	
> 3	<!-- dokima-card -->
> 4	### Approve the result to merge
> 5	[PR #200](https://github.com/dokima-dev/dokima/pull/200) · [files changed](https://github.com/dokima-dev/dokima/pull/200/files)
> 6	
> 7	This issue has no objective and acceptance criteria yet.
> 8	
> 9	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37737107500/job/113179044729)
> 10	
> 11	<!-- /dokima-card -->
> 12	
> 13	<details open><summary>From the approved plan of #143, story 1</summary>
> 14	
> 15	**Part of:** #143 Card: one deterministic card from the agents' JSON, the same on issue and PR
> 16	
> 17	**User story:** Owners can trust that whatever code redraws on an issue, their original ask below the marker stays exactly as they wrote it.
> 18	
> 19	**Context:** Split rules R1, R2 and R3: #143 holds several independent goals (body protection, the issue/PR card's content, its status and children, run cards, a backfill), needs well over five criteria, and spans dokima/planner.py, dokima/card.py, dokima/agent.py, dokima/roles/ and AGENTS.md. This story keeps the promise moved in from #48. Today dokima/planner.py render() folds the owner's text between <!-- dokima-original --> and <!-- /dokima-original --> and original() reads it back, but dokima/card.py main() rewrites the whole body via issue_body

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/open_blockers.json; git log --oneline -8; git show --stat HEAD; git diff HEAD~1 -- tests/; git merge-base HEAD origin/main
```

> []8feec99 planner for #179 (run 37736820123)
> 7cbeff7 worker for #179 (run 37733545849)
> 46249a2 Merge remote-tracking branch 'origin/main' into try/issue-179
> 825ed45 planner for #179 (run 37730917744)
> 7fd811f Board: a failed run puts its card in Needs you (#192)
> 90adfdc Plan checker: new tests are checked as new, renames as changes (#194)
> 1be32e5 planner for #179 (run 37729957222)
> ad72396 Planner questions are a question and its assumption, nothing else (#178)
> commit 8feec99b9df24efe0c5c43bf80b3178502725d96
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 06:20:50 2026 +0000
> 
>     planner for #179 (run 37736820123)
> 
>  tests/test_body.py | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> diff --git a/tests/test_body.py b/tests/test_body.py
> index f108f54..7fff555 100644
> --- a/tests/test_body.py
> +++ b/tests/test_body.py
> @@ -129,7 +129,7 @@ def run_card(monkeypatch, github, current):
>  REASON = "the owner's part below the marker would change"
>  
>  PLAN_TESTS = ('def test_card(record_property):\n    """The card shows."""\n'
> -              '    record_property("proves", "40.1")\n    assert True\n')
> +              '    record_property("proves", "40.1")\n    assert False\n')
>  PLAN = {"kind": "user_story", "user_story": "Owners see a card on every issue.",
>          "acceptance_criteria": [{"text": "The issue shows a card on top.", "source": f"https://github.com/{REPO}/issues/{NUMBER}"}],
>          "non_functional": [], "scope": ["dokim

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | tail -3; rm -rf /tmp/m && git worktree add -q /tmp/m origin/main 2>&1|tail -1; cp tests/test_body.py tests/test_card.py /tmp/m/tests/; cd /tmp/m && python -m pytest -q tests/test_body.py 2>&1 | grep -E "FAILED|ERROR|passed|failed" | cut -c1-220
```

> ........................................................................ [ 94%]
> ................                                                         [100%]
> 304 passed in 70.85s (0:01:10)
> FAILED tests/test_body.py::test_body_is_the_card_above_one_marker_and_the_ask_folded_below - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_marker_is_the_same_after_every_redraw - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_writes_its_card_above_the_marker - Failed: 179.1: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_owner_part_is_byte_for_byte_the_same_after_many_redraws - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_the_card_never_changes_the_owner_part - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_replanning_never_changes_the_owner_part - Failed: 179.2: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_a_redraw_that_would_change_the_owner_part_is_refused - Failed: 179.3: dokima/body.py, the one helper that owns the issue body, does not exist yet
> FAILED tests/test_body.py::test_a_refused_save_leaves_the_body_and_comments_why - Failed: 179.3: dokima/

**Agent:** Running the tests checks out: all 304 pass on the branch, and all 16 new tests fail on main only because the body helper is missing. Writing the review now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/m; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Changed the sample plan used by the two tests of the planner's save so that its one new test fails today, which lets the planner get as far as saving the issue body.",
          "Kept the four criteria, the scope, the tests and the two questions as they were."],
  "decided": ["The fix goes in the tests, not in the planner's check that rejects new tests that already pass."],
  "open": ["Whether the issue's wording counts as asking to change dokima/card.py; the plan assumes it does and the owner went on with that assumption."]},
 "verdict": "approve",
 "summary": "The plan is unchanged apart from a one-line fix to the tests of the planner's save: every new test now fails on main only because the body helper is missing, and all of them pass on the worker's branch.",
 "blockers": [],
 "notes": [
  {"text": "The comparison that refuses a save is still only exercised by one case, a card that contains the marker; the earlier notes on this stand but do not block.",
   "evidence": "tests/test_body.py: test_a_redraw_that_would_change_the_owner_part_is_refused, test_a_refused_save_leaves_the_body_and_comments_why and test_a_refusal_is_a_comment_on_the_issue all use a top that quotes body.MARKER."}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 179 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #179. Both hand-back checks passed, and the review is in `/tmp/dokima-out/review.json`.

- **What changed:** the planner changed one line in `tests/test_body.py`. The sample plan used by the two tests of the planner's save had a test ending in `assert True`. It now ends in `assert False`. That matters because the planner's own check rejects a plan whose new test already passes, so the sample plan was being rejected before the save was ever reached. That fixes both blockers from the code review (B2 and B3). The criteria, scope, tests and questions are otherwise the same as the plan approved earlier.
- **On the branch:** the full suite passes, 304 tests.
- **On main:** I copied the new tests onto main's code. All 16 tests in `tests/test_body.py` fail, and each one fails only because `dokima/body.py` doesn't exist yet.
- **Open blockers:** none at the plan stage.
- **One note, not blocking:** every test that checks a refusal still causes it the same way, with a card that contains the marker. Earlier reviews raised the same point.

The open question about whether this issue counts as permission to change `dokima/card.py` is unchanged. The plan assumes it does, and the owner went on with that assumption.
