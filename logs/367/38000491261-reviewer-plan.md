# reviewer (plan) for #367

Run: https://github.com/dokima-dev/dokima/actions/runs/38000491261

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #367: Bug: a parent closes and moves to Done when its last sub-issue closes, on autopilot or not
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #367](https://github.com/dokima-dev/dokima/issues/367)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> When the last open sub-issue of a parent closes, the parent closes as completed and moves to Done, whether or not anything is on autopilot. Today only a parent on autopilot closes itself, so #330 sat in Work with all seven sub-issues closed until it was closed by hand.
> 
> Owner's words (2026-10-09): "then this is a bu

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -2 | head -30; pytest -q tests/test_parent_close.py tests/test_parent_sweep.py tests/test_autopilot_close.py 2>&1 | grep -E "FAILED|passed|failed|Error" | head -30
```

> commit 2fa4ef68e28155b4ff3c1259819baa862d3fedbd
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 22:40:24 2026 +0000
> 
>     planner for #367 (run 38000057386)
> 
>  tests/test_parent_close.py |  12 +--
>  tests/test_parent_sweep.py | 230 +++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 236 insertions(+), 6 deletions(-)
> 
> commit 59456afd59c839a555f5bd8fa3735c890e9f891b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 22:34:15 2026 +0000
> 
>     planner for #367 (run 37999660078)
> 
>  tests/test_autopilot_close.py |  14 ++--
>  tests/test_parent_close.py    | 168 ++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 174 insertions(+), 8 deletions(-)
>         assert not m.failed, f"367.1 (last one): a workflow failed when #101 closed: {m.failures}\n{m.tail()}"
> E       AssertionError: 367.1 (last one): #57 is ('open', None) after its last open sub-issue closed off autopilot, expected closed as completed
> tests/test_parent_close.py:53: AssertionError
>         assert not m.failed, f"367.2 (sibling not planned): a workflow failed: {m.failures}\n{m.tail()}"
> E       AssertionError: 367.2 (sibling not planned): #57 is ('open', None) though #102 was closed as not planned and #101 as completed, expected closed as completed
> tests/test_parent_close.py:75: AssertionError
>         assert not m.failed, f"367.3 (in turn): a workflow failed when #202 closed: {m.failures}\n{m.tail()}"
> E  

`3. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_parent_close.py tests/test_parent_sweep.py tests/test_autopilot_close.py 2>&1 | tail -3; cat tests/test_parent_sweep.py
```

> +     None,
>     )
> 9 failed, 1 passed, 11 skipped in 3.01s
> """The 15-minute card sweep closes every open parent whose sub-issues are all closed (#367).
> 
> A parent closes when its last sub-issue closes, but a close event GitHub drops or a run that never went would leave a
> finished parent sitting in Work, as #330 did. The owner asked that the 15-minute card sweep from #347 doubles as the
> safety net: on each sweep, any open parent whose sub-issues are all closed is closed the same way.
> 
> These tests play card.yml's 15-minute schedule with the player of tests/card_player.py, running the real
> `python3 dokima/card.py` against the fake GitHub of tests/test_card_sweep.py, extended here with issue trees:
> - `gh api repos/o/r/issues/N/sub_issues` lists N's sub-issues (each with its state and state_reason), and
>   `gh api repos/o/r/issues/N/parent` gives N's parent (404 when it has none).
> - Every issue GitHub gives carries `state_reason`, `parent_issue_url` and `sub_issues_summary` (total, and completed:
>   the sub-issues closed as completed; one closed as not planned is not counted there, so code that trusts that count
>   alone misses it).
> - `gh issue close N` (--reason/-r, --comment/-c) closes N, and `gh api repos/o/r/issues/N` with -X PATCH and
>   state=closed (state_reason=...) does too.
> Every tree's closes happened at 01:00, before the last sweep that succeeded (05:00), and nothing was updated since: the
> missed close is old, as #330's was, so the sweep must look at every open parent, not o

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def tree_done_comment" -A8 dokima/agent.py; sed -n 1,60p tests/test_parent_close.py; sed -n 140,175p tests/test_parent_close.py; git diff 59456af~1 -- tests/test_autopilot_close.py
```

> 1444:def tree_done_comment(number):
> 1445-    """The comment a parent closes with when its last sub-issue closed on autopilot."""
> 1446-    return f"Every issue under #{number} is closed, so its whole tree is done and it closes.\n"
> 1447-
> 1448-
> 1449-def autopilot_closed(repo):
> 1450-    """What autopilot does when an issue closes, worked out from GitHub's state of every issue on autopilot, so a close
> 1451-    whose own run never went is still handled by the next one. Returns what it did, as lines.
> 1452-
> """A parent closes when its last sub-issue closes, on autopilot or not (#367).
> 
> Today only a parent on autopilot closes itself, so #330 sat in Work with every sub-issue closed until it was closed by
> hand. These tests run the workflows GitHub starts when an issue closes, on the fake GitHub of test_autopilot_close.py,
> with no issue on autopilot unless a test says so. `settle` also closes in turn every issue the workflows closed, the
> way GitHub tells of a close made by Dokima's app, so a grandparent can close one level up in turn.
> """
> import json
> 
> from test_autopilot_close import LABEL, Repo
> 
> 
> class NotPlannedRepo(Repo):
>     """A repo where the issue closed in the test closes as not planned."""
> 
>     def close_quietly(self, n):
>         """Issue n closes as not planned; its close workflows have not run yet."""
>         states = self._json("states.json")
>         states[str(n)] = {"state": "closed", "reason": "not_planned"}
>         json.dump(states, open(f"{self.tmp}/gh/states.json", "w")

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["The planner added criterion 367.5: every 15-minute card sweep closes each open parent whose sub-issues are all closed, with the same one line, and leaves a parent with any open sub-issue alone.", "The planner added four sweep tests in tests/test_parent_sweep.py and moved the rule against closing twice to 367.6, now covering a second sweep too.", "The planner added dokima/card.py to scope and dropped the out-of-scope line that said no sweep closes parents."],
 "decided": ["Parents already left open, like #330, close on the first sweep after this lands; there is no other backfill.", "The board code and the workflow files do not change."],
 "open": []},
 "verdict": "approve",
 "summary": "The plan now covers every ask, including the owner's 15-minute sweep as a safety net, and all nine new or changed tests fail today because parents stay open.",
 "blockers": [],
 "notes": [
  {"text": "Every new test fails today for the right reason: the parent, or the grandparent, stays open after its last sub-issue closes, by a close or by the sweep.", "evidence": "pytest -q tests/test_parent_close.py tests/test_parent_sweep.py tests/test_autopilot_close.py: 9 failed, 1 passed, 11 skipped; e.g. \"367.5 (all closed): the sweep left #57 ('open', None) though all its sub-issues are closed, expected it closed as completed\"."},
  {"text": "Criterion 367.5 names the issue as its source; its words come from the owner's comment of 2026-10-09T22:32:25Z, which allows changing dokima/card.py for the sweep.", "evidence": "plan.json acceptance_criteria[4].source; issue #367 comment by RezaSoleymanifar at 2026-10-09T22:32:25Z."}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "When the last open sub-issue of a parent closes, the parent closes as completed and moves to Done, whether or not anything is on autopilot.", "source": "https://github.com/dokima-dev/dokima
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

**Agent:** The review is written; the checker says its one-line summary is too long, so I'm shortening it and running the check again.

`6. Bash`
```
python3 - <<'EOF'
import json
p="/tmp/dokima-out/review.json"; r=json.load(open(p))
r["summary"]="The plan now covers every ask, including the owner's 15-minute sweep, and every new test fails today because parents stay open."
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 367 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#367](https://github.com/dokima-dev/dokima/issues/367) (a parent closes when its last sub-issue closes), and the hand-back passes both checks.

- **Earlier blocker B1 is fixed.** In a later comment you asked that the 15-minute card sweep act as a safety net. The plan now covers that as criterion 367.5: every sweep closes each open parent whose sub-issues are all closed, with the same one line. A sub-issue closed as not planned counts as done, a grandparent can close in the same sweep, and a parent with any sub-issue still open is left alone. The plan dropped the out-of-scope line that said no sweep closes parents, and it adds `dokima/card.py` to its scope.
- **Every ask you made has a criterion.** I matched all six to criteria 367.1 to 367.5. The rule that a parent is never closed or commented on twice is now 367.6, and it also covers a second sweep.
- **The tests fail today for the right reason.** I ran the tests in `tests/test_parent_close.py`, `tests/test_parent_sweep.py` and `tests/test_autopilot_close.py`: 9 failed, 1 passed, 11 skipped. The failures are all the missing feature (the parent or grandparent stays open), not a crash or a broken setup.
- **One test changed meaning.** `test_a_close_off_autopilot_does_nothing` used to require a parent off autopilot to stay open, which is the bug itself. It now expects the parent to close, and still expects no "Autopilot:" line when the parent is off autopilot.
- **Note on the source:** criterion 367.5 names the issue as its source, but the words come from your comment of 2026-10-09 at 22:32. That comment is also what allows changing `dokima/card.py`, which the repo rules otherwise protect.

The plan decides that parents already left open, like [#330](https://github.com/dokima-dev/dokima/issues/330) (sat in Work with every sub-issue closed), will close on the first sweep after this lands, with no other backfill. Neither the board code nor the workflow files change.
