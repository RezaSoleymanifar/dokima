# reviewer (plan) for #367

Run: https://github.com/dokima-dev/dokima/actions/runs/37999948347

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  9 22:34 .
> drwxrwxrwt 18 root   root   4096 Oct  9 22:34 ..
> drwxr-xr-x  2 runner runner 4096 Oct  9 22:34 in
> -rw-r--r--  1 runner runner 7151 Oct  9 22:34 issue.md
> -rw-r--r--  1 runner runner    2 Oct  9 22:34 open_blockers.json
> -rw-r--r--  1 runner runner   16 Oct  9 22:34 parent.json
> -rw-r--r--  1 runner runner 3310 Oct  9 22:34 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  9 22:34 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 22:34 ..
> -rw-r--r-- 1 runner runner 3935 Oct  9 22:34 01-planner.json
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
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddl

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/parent.json; git show --stat HEAD; timeout 300 python -m pytest -q tests/test_parent_close.py tests/test_autopilot_close.py 2>&1 | tail -30
```

> {"number": null}commit 59456afd59c839a555f5bd8fa3735c890e9f891b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 22:34:15 2026 +0000
> 
>     planner for #367 (run 37999660078)
> 
>  tests/test_autopilot_close.py |  14 ++--
>  tests/test_parent_close.py    | 168 ++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 174 insertions(+), 8 deletions(-)
>   Full diff:
>     (
>   -     'closed',
>   ?      -- ^ ^
>   +     'open',
>   ?       ^ ^
>   -     'completed',
>   +     None,
>     )
> FAILED tests/test_parent_close.py::test_the_parent_says_why_it_closed_in_one_line_as_on_autopilot - AssertionError: 367.4 (off autopilot): #57 got 0 new comments, expected exactly one saying why it closed: []
> assert 0 == 1
>  +  where 0 = len([])
> FAILED tests/test_parent_close.py::test_a_parent_already_closed_is_left_alone - AssertionError: 367.5 (open parent): #57 is ('open', None) after its last sub-issue closed, expected closed as completed
>   ## close1-autopilot.yml-closed: Close done parents, switch done trees off, start what the close unblocked (exit 0)
>   #101 closed: nothing on autopilot to do.
>   
> assert ('open', None) == ('closed', 'completed')
>   
>   At index 0 diff: 'open' != 'closed'
>   
>   Full diff:
>     (
>   -     'closed',
>   ?      -- ^ ^
>   +     'open',
>   ?       ^ ^
>   -     'completed',
>   +     None,
>     )
> 5 failed, 1 passed, 11 skipped in 2.17s

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rln "schedule\|cron" .github/workflows/ | head; grep -n "cron" .github/workflows/card.yml; grep -n "^def \|sweep" dokima/*.py | grep -i sweep | head -20
```

> .github/workflows/card.yml
> .github/workflows/audit.yml
> .github/workflows/board.yml
> 22:    - cron: '*/15 * * * *'
> dokima/board.py:3:Each event about an issue or its pull request, and a sweep every 15 minutes, put its cards where the issue's state
> dokima/board.py:190:        return "board-sweep"
> dokima/board.py:297:    """[(kind, number)] updated since the last sweep that succeeded, or None to recheck every card."""
> dokima/board.py:303:        print(f"GitHub could not say what changed since the last sweep ({reason(e)}), so every card is rechecked.")
> dokima/board.py:307:def sweep(board, repo, owners, todo=None):
> dokima/board.py:397:        attempt(lambda: sweep(board, repo, owners, changed(repo)))
> dokima/board.py:417:        attempt(lambda: sweep(board, repo, owners))
> dokima/card.py:680:def last_sweep(repo):
> dokima/card.py:681:    """When the last 15-minute sweep that succeeded started: (time, None), or (None, why).
> dokima/card.py:684:    start, not the end, keeps a change made while that sweep ran."""
> dokima/card.py:689:        return None, f"GitHub cannot list the earlier sweeps: {reason(e)}"
> dokima/card.py:691:    return (max(started), None) if started else (None, "no sweep has succeeded yet")
> dokima/card.py:697:    Open or closed, it looks only at the issues and PRs updated since the last sweep that succeeded, and every card
> dokima/card.py:701:    since, why = last_sweep(repo)
> dokima/card.py:733:def sweep(repo):
> dokima/card.py:737:    the issues and PRs updated since the las

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote four criteria and a rule against closing a parent twice, with five tests in tests/test_parent_close.py and one changed test in tests/test_autopilot_close.py; all fail today because the parent stays open."],
  "decided": ["A parent closes only when a sub-issue closes; no periodic sweep closes parents.", "The board code does not change: closing the parent is what moves it to Done."],
  "open": []},
 "verdict": "block",
 "summary": "The plan leaves out the owner's later ask that the 15-minute card sweep also closes any open parent whose sub-issues are all closed, and even lists that sweep as out of scope.",
 "blockers": [{"id": "B1", "criterion": "missing", "test": null,
   "problem": "The owner asked, after the plan was written, that the 15-minute card sweep from #347 doubles as a safety net: on each sweep any open parent whose sub-issues are all closed is closed the same way. No criterion or test covers it, and the plan's out of scope says the opposite: \"No periodic sweep closes parents\".",
   "evidence": "Owner's comment on #367 (2026-10-09T22:32:25Z): \"the 15-minute card sweep from #347 doubles as the safety net. On each sweep, any open parent whose sub-issues are all closed is closed the same way\". plan.json out_of_scope[1]. The sweep lives in dokima/card.py (sweep, line 733; cron in .github/workflows/card.yml line 22), which is not in the plan's scope.",
   "fix": "Add a criterion: on each 15-minute card sweep, every open parent whose sub-issues are all closed (not planned counts as done) closes as completed with the same one line, and a parent with any open sub-issue is left alone; add a test that runs the sweep on both cases; drop the out-of-scope line and add dokima/card.py to scope (the owner's ask allows it).",
   "fixer": "planner"}],
 "notes": [{"text": "All five new tests and the changed one fail today for the right reason: the parent o
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> blocker B1 names missing, which is not a criterion of the plan (367.1, 367.2, 367.3, 367.4, 367.5)

`5. Bash`
```
cd /tmp/dokima-out && python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['summary']="The plan drops the owner's later ask that the 15-minute card sweep also closes any open parent whose sub-issues are all closed."
r['blockers'][0]['criterion']="367.1"
r['blockers'][0]['problem']="Criterion 367.1 closes a parent only on a sub-issue's close. "+r['blockers'][0]['problem']
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 367 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I've blocked the plan for [#367](https://github.com/dokima-dev/dokima/issues/367) (a parent closes when its last sub-issue closes) and sent it back to the planner.

**Why it's blocked:** after the plan was written, you added a comment (2026-10-09 22:32) saying the 15-minute card sweep from #347 should also act as a safety net: on each sweep, any open parent whose sub-issues are all closed gets closed the same way. The plan has no criterion or test for that. Its out-of-scope list even says "No periodic sweep closes parents." I asked the planner to:
- add a criterion and a test that runs the sweep on two cases: a parent whose sub-issues are all closed, and one with a sub-issue still open;
- remove that out-of-scope line;
- add `dokima/card.py` to the scope, since the sweep lives there and your comment asks for it.

**What holds up:** your other five asks each map to a criterion in the plan. All five new tests and the one changed test fail today for the right reason: a parent that isn't on autopilot stays open after its last sub-issue closes.

The hand-back is saved in `/tmp/dokima-out/review.json` and passes both required checks.
