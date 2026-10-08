# reviewer (plan) for #245

Run: https://github.com/dokima-dev/dokima/actions/runs/37829291684

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #245: /autopilot start turns autopilot on but never starts the work
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
> When I type `/autopilot start` on a new issue, autopilot turns on and the bot says no stage was started. Nothing happens until I type `/plan` myself. Seen on #229, #230, #231 and #244.
> 
> The user story of #205 was that I hand over an issue and get it back done, stopping only where I must decide. Its criteria only covered the hand-offs after a plan exists, and the start of the work itself was never built. Today it only starts planning issues under the one I switched on, never that issue itself.
> 
> What I want:
> - `/autopilot start` on an issue with no plan starts its planner, with one Autopilot line where I would have typed `/plan`.
> - It still picks up whatever is already waiting anywhere in the tree, as today.
> - A test proves the whole journey: a new 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_autopilot_start.py; cat tests/test_autopilot_start.py
```

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_start.py 2>&1 | tail -40
```

> commit e9a1990ef080ec0d64324fb9d71042e117af729b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 19:05:05 2026 +0000
> 
>     planner for #245 (run 37827923976)
> 
>  tests/test_autopilot_start.py | 217 ++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 217 insertions(+)
> 217 tests/test_autopilot_start.py
> """`/autopilot start` on an issue with no plan starts its planner, and the issue then runs to merged by itself (#245).
> 
> Before this, `/autopilot start` switched the issue on and said "No stage was started": it only started planning for
> issues under the one switched on, never that issue itself, so nothing happened until the owner typed `/plan`.
> 
> These tests run the command listener (.github/workflows/commands.yml) the way GitHub runs it, on the machine from
> test_start.py, against the fake GitHub of test_autopilot_close.py (issue tree, labels, states, blocked-by links,
> comments, signals) and, for the journey, test_automerge.py's (pull requests, checks, merging). Where only the river's
> decision between two stages matters, the journey runs `python3 -m dokima.agent next 57` on the finished stage's record,
> against the same fake GitHub, as agent.yml does after every run.
> """
> import json
> import os
> import subprocess
> import sys
> 
> import test_automerge as tam
> import test_autopilot_close as tac
> import test_start as ts
> from dokima import agent
> from test_start import N, OWNER, PR
> 
> LABEL = "autopilot"
> LINE = "Autopilot: switched on, star

> assert ({} == {57: 1}
>   
>   Right contains 1 more item:
>   {57: 1}
>   
>   Full diff:
>   + {}
>   - {
>   -     57: 1,
>   - })
> FAILED tests/test_autopilot_start.py::test_saying_autopilot_start_twice_starts_the_planner_once - AssertionError: 245.5: saying /autopilot start twice started #57's planner 0 times, not once
> assert {} == {57: 1}
>   
>   Right contains 1 more item:
>   {57: 1}
>   
>   Full diff:
>   + {}
>   - {
>   -     57: 1,
>   - }
> FAILED tests/test_autopilot_start.py::test_a_new_issue_on_autopilot_ends_merged_with_no_command_from_the_owner - AssertionError: 245.4: the journey stopped at the start: /autopilot start did not start #57's planner: []
>   ## route-0: r (exit 0)
>   autopilot=start
>   issue=57
>   
>   ## autopilot-1: Switch the issue tree on or off autopilot, and say which issues, where it was written (exit 0)
>   https://github.com/o/r/issues/57#issuecomment-5001
>   
> assert {} == {57: 1}
>   
>   Right contains 1 more item:
>   {57: 1}
>   
>   Full diff:
>   + {}
>   - {
>   -     57: 1,
>   - }
> 5 failed in 4.65s

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_autopilot_start.py 2>&1 | grep -E "^FAILED|^E .*24[0-9]\.[0-9]" | head; grep -n "planners_started\|def close\|def listen\|running_runs\|def planned\|def running" tests/test_autopilot_close.py tests/test_automerge.py | head -30
```

> E       AssertionError: 245.1: /autopilot start on #57, a new issue with no plan, did not start its planner exactly once; planners started: {}
> E       AssertionError: 245.2 (new issue): /autopilot start on #57 with no plan and nothing open to wait for did not start its planner once with one 'Autopilot: switched on, starting plan'; planners started: {}, its comments: ['Autopilot is on for #57. No stage was started.\n']
> E       AssertionError: 245.3 (new issue): /autopilot start on #57 with no plan and nothing open to wait for did not start its planner once with one 'Autopilot: switched on, starting plan'; planners started: {}, its comments: ['Autopilot is on for #57. No stage was started.\n']
> E       AssertionError: 245.5: saying /autopilot start twice started #57's planner 0 times, not once
> E       AssertionError: 245.4: the journey stopped at the start: /autopilot start did not start #57's planner: []
> FAILED tests/test_autopilot_start.py::test_autopilot_start_on_an_issue_with_no_plan_starts_its_planner - AssertionError: 245.1: /autopilot start on #57, a new issue with no plan, did not start its planner exactly once; planners started: {}
> FAILED tests/test_autopilot_start.py::test_autopilot_start_never_starts_the_issue_itself_where_it_must_not - AssertionError: 245.2 (new issue): /autopilot start on #57 with no plan and nothing open to wait for did not start its planner once with one 'Autopilot: switched on, starting plan'; planners started: {}, its comments: ['Autopilot is on

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 425,480p tests/test_automerge.py; sed -n 370,395p tests/test_autopilot_close.py; grep -n "def comments\|author" tests/test_start.py | head -20
```

> """An issue tree whose issues have pull requests, on which a code owner says a command (commands.yml).
> 
>     `prs` maps each pull request's number to its state (pr_state); `reviews` maps each issue with a pull request to
>     its newest code review's verdict ("approve" or "block"). The tree is #50 > #57, #58 and #57 > #101, #102, #105,
>     #101 > #103, #104 unless another is given."""
> 
>     def __init__(self, tmp, prs, reviews, labels=None, tree=None):
>         tree = tree or {50: [57, 58], 57: [101, 102, 105], 101: [103, 104]}
>         by_issue = {p["issue"]: n for n, p in prs.items()}
>         seed = []
>         for issue, verdict in sorted(reviews.items()):
>             seed += history(issue, by_issue[issue], verdict, base=10000 + 100 * issue)
>         super().__init__(tmp, tree, labels=labels or {}, seed=seed, history=[])
>         t = self.tmp
>         open(f"{t}/bin/gh", "w").write(fake_gh())
>         json.dump({str(k): v for k, v in prs.items()}, open(f"{t}/gh/prs.json", "w"))
> 
>     def listen(self, body, on_pr=None):
>         """A code owner's comment `body` on issue #57, or on pull request `on_pr`, runs commands.yml."""
>         t = self.tmp
>         number = int(on_pr or N)
>         issue = {"number": number, **({"pull_request": {"url": f"https://api.github.com/repos/o/r/pulls/{number}"}} if on_pr else {})}
>         event = {"comment": {"body": body, "user": {"login": OWNER, "type": "User"}}, "issue": issue}
>         open(f"{t}/event.json", "w").write(json.dumps(event))
>         github 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/rv && python3 - <<'E'
s=open('tests/test_autopilot_start.py').read()
s=s.replace('    assert_a_new_issue_starts(tmp_path / "unblocked"','    pass #').replace('    assert_a_new_issue_starts(tmp_path / "new", "245.3")','    pass')
open('/tmp/rv/test_rv_start.py','w').write(s)
E
cd tests && timeout 600 python -m pytest -q -p no:cacheprovider --rootdir=/tmp/rv /tmp/rv/test_rv_start.py -k "where_it_must_not or picks_up" 2>&1 | grep -E "^E  .*24|passed|failed" | head
```

> (Bash completed with no output)

**Agent:** Checking that the plan's "must not start" cases run correctly against today's code.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; PYTHONPATH=tests:. timeout 600 python -m pytest -q -p no:cacheprovider /tmp/rv/test_rv_start.py -k "where_it_must_not or picks_up" 2>&1 | tail -15
```

> ..                                                                       [100%]
> 2 passed, 3 deselected in 6.92s

`8. Bash`
```
rm -rf /tmp/rv; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner wrote a plan with four acceptance criteria, one non-functional requirement and five tests in tests/test_autopilot_start.py."],
  "decided": ["`/autopilot start` on an issue with no plan, no sub-issues and nothing open blocking it starts its planner once, with one line `Autopilot: switched on, starting plan`.",
              "The issue itself is not started when it is already planned or planning, split, or blocked by an open issue; a blocked issue starts once its last blocker closes.",
              "Saying `/autopilot start` twice starts the planner once."],
  "open": ["One question: an issue blocked by an open issue waits for its blocker to close before planning."]},
 "verdict": "approve",
 "summary": "The plan keeps all three asks, and every test fails today only because `/autopilot start` never starts the issue's own planner.",
 "blockers": [],
 "notes": [
  {"text": "The tests check the switch comment for the words `Planning started for #57`, an exact wording the criterion only describes; the worker must use those words.", "evidence": "tests/test_autopilot_start.py::test_autopilot_start_on_an_issue_with_no_plan_starts_its_planner: assert f\"Planning started for #{N}\" in said"},
  {"text": "The journey test's check that the owner wrote nothing along the way cannot fail, because the fake GitHub never stores a comment as the owner; the real proof is that each stage follows the one before.", "evidence": "tests/test_automerge.py Command.listen sends the event without writing a comment; test_a_new_issue_on_autopilot_ends_merged_with_no_command_from_the_owner: by_owner == []"},
  {"text": "With the good-case checks removed, the 'must not start' cases of 245.2 and 245.3 pass on today's code, including a blocked issue starting when its blocker closes. So once the feature exists, these tests fail only if it starts too much.", "evidence": "A copy of
```

> rc=0

**Agent:** I approved the plan for #245, with no blockers, and wrote the review to `/tmp/dokima-out/review.json`. Both of Dokima's checks on the review pass.

- **The owner's asks:** the issue asks for three things and each one has a criterion:
  - Start the planner, with one Autopilot line where you'd have typed `/plan` (245.1).
  - Still pick up whatever is already waiting in the tree (245.3).
  - A test of the whole journey from a new issue to merged, with no command from you (245.4).
- **The new tests:** all five fail on the branch today, and only because `/autopilot start` never starts the issue's own planner. Each one stops at that point with "No stage was started" or "planners started: {}".
- **The "must not start" cases:** I ran a temporary copy of the tests without the start checks. The 245.2 and 245.3 cases where nothing should start pass on today's code. That includes a blocked issue starting once its blocker closes. So once the feature is built, these tests go red only if it starts too much.
- **The planner's one question:** a blocked issue waits for its blocker to close before planning. I accepted that assumption. It matches AGENTS.md word for word ("every issue on autopilot whose blocked-by issues have now all closed starts its planner"), and it changes neither how the system works nor what it costs.

Three notes, none of them blocking:
1. The tests require the switch comment to contain the exact words `Planning started for #57`, so the worker has to use that wording. The criterion only describes it.
2. The journey test checks that you wrote nothing along the way, but that check can never fail: the fake GitHub doesn't record your comments. The test still proves the journey by checking that each stage starts the next one.
3. The good case runs first in 245.2 and 245.3, so on today's code their "must not start" cases never run. That's why I checked them separately.
