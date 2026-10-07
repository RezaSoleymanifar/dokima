# reviewer (plan) for #166

Run: https://github.com/dokima-dev/dokima/actions/runs/37673559948

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
> # Issue #166: River: a code review block about a weak test goes to the planner, not the worker
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
> Found on 154 and PR 165. When the code reviewer finds that a planner's test is too weak, the river sends the block to the worker, who may not touch tests. They went three rounds and it escalated to me. Each blocker in a code review should say who fixes it, the worker for code or the planner for tests, and the river should send it there. A test fix then goes planner, plan review, worker, code review.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #166 (2026-10-07T16:47:46Z)
> 
> /plan
> 
> 
> ### dokima-runtime on issue #166 (2026-10-07T18:15:10Z)
> 
> <!-- dokima-record -->
> **Planner**
> 
> When a code review finds a planner's test too weak, the planner strengthens the test and the work goes on, instead of the worker going round in circles until it reaches the owner.
> 
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - After a code review sends a weak test back, should the approved re-plan go straight to the worker, or wait for your `/work` as a first plan does? I planned for str

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -1 | head -30; cat tests/test_fixer.py
```

> commit 6f17ea1d32c053367f4c8006b056abdb960d34d8
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 18:15:03 2026 +0000
> 
>     planner for #166 (run 37654844239)
> 
>  tests/test_agent.py          |   2 +-
>  tests/test_fixer.py          | 187 +++++++++++++++++++++++++++++++++++++++++++
>  tests/test_handback_check.py |   5 +-
>  3 files changed, 191 insertions(+), 3 deletions(-)
> """A code review's blocker says who fixes it, and the river sends it there: tests to the planner, code to the worker.
> 
> Found on issue 154 and PR 165: a code reviewer found a planner's test too weak, the river sent the block to the worker,
> who may not touch tests, and three rounds later it reached the owner. Each test here drives Dokima's own code the way
> the workflow does (the hand-back check from outside, the river's next_step, the starting pack with GitHub faked) and
> names its criterion on every failure. A plan for issue 9 with criteria 9.1 to 9.3 stands in for the approved plan.
> """
> import json
> import os
> import subprocess
> import sys
> import tempfile
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent  # noqa: E402
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> STORY = {"kind": "user_story", "user_story": "u",
>          "acceptance_criteria": [{"text": "a", "source": "https://x/9"}, {"text": "b", "source": "https://x/9"},
>                                  {"text": "c", "source": "https://x/9"}],
>     

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_fixer.py 2>&1 | grep -E "^E .*166|passed|failed|Error" | head -30; python3 -m pytest -q 2>&1 | tail -3
```

> >           assert code == 1, f"166.1: a blocker with fixer {bad!r} passed the check; it must name the worker or the planner"
> E           AssertionError: 166.1: a blocker with fixer None passed the check; it must name the worker or the planner
> tests/test_fixer.py:83: AssertionError
> E       AssertionError: 166.1: B1's line does not say the planner fixes it: - **B1** (9.1): problem B1
> tests/test_fixer.py:98: AssertionError
> E           AssertionError: 166.2: a code review with a test blocker started ('start', 'worker', ''), not the planner
> tests/test_fixer.py:112: AssertionError
> E       AssertionError: 166.3: the planner was handed blockers [], not exactly the test blocker B1
> tests/test_fixer.py:144: AssertionError
> E       AssertionError: 166.4: an approved test fix asked for by a code review gave ('stop', 'The plan is approved. Say `/work` to build it, or `/plan` with changes.'), not the worker
> tests/test_fixer.py:166: AssertionError
> E       AssertionError: 166.5: the reviewer's hand-back shape gives blockers no fixer of worker or planner
> tests/test_fixer.py:183: AssertionError
> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a blocker with fixer None passed the check; it must name the worker or the planner
> FAILED tests/test_fixer.py::test_the_review_comment_shows_who_fixes_each_blocker - AssertionError: 166.1: B1's line does not say the planner fixes it: - **B1** (9.1): problem B1
> FAILED tests/test_fixer.py::test_a_

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan of five criteria and six tests: each code review blocker names who fixes it, and a weak-test blocker goes to the planner, then plan review, then the worker."],
  "decided": ["An approved re-plan that a code review asked for goes straight to the worker, unless the owner spoke since that review."],
  "open": ["Asked the owner whether the approved re-plan goes straight to the worker or waits for /work; the owner has since answered."]},
 "verdict": "block",
 "summary": "The plan and its tests are sound, but they miss the owner's answer that a re-plan which changes any criterion must still wait for their /work.",
 "blockers": [{"id": "B1", "criterion": "166.4",
   "test": "tests/test_fixer.py::test_an_approved_test_fix_goes_straight_back_to_the_worker",
   "problem": "The owner answered the plan's question: straight to the worker, but \"If the re-plan changes any criterion, it waits for my /work.\" Criterion 166.4 starts the worker after any approved re-plan a code review asked for, and its test only uses a re-plan with the same criteria, so code that starts the worker even when the re-plan rewrote, added or dropped a criterion would pass.",
   "evidence": "Owner's comment on issue #166 (2026-10-07T19:19:02Z): \"/review yes, straight to the worker. A stronger test does not change what I approved. If the re-plan changes any criterion, it waits for my /work.\" plan.json 166.4 has no such case; in the test, `replan = rec(\"planner\", handback=STORY)` is the same STORY as the approved PLAN.",
   "fix": "Add to 166.4: a re-plan asked for by a code review whose criteria differ from the approved plan (a criterion's text changed, one added, one removed) stops and asks the owner for /work. Add those cases to the test beside the unchanged-criteria case that starts the worker, and drop the answered question."}],
 "notes": [{"text": "All six new tests fail today for the ri
```

> 0

**Agent:** I blocked the plan for issue #166 on one point. The plan doesn't include your answer to its question: you said a fix that only makes a test stronger goes straight to the worker, but **if the re-plan changes any criterion, it waits for your `/work`**.

**The blocker (B1, criterion 166.4):** As written, the plan starts the worker after any re-plan that a code review asked for, once the plan review approves it. Its test only tries a re-plan whose criteria are the same as the approved plan. So code that also skipped your `/work` after a criterion was reworded, added or removed would still pass. The fix:
- Add your rule to 166.4: a re-plan whose criteria differ from the approved plan stops and asks you for `/work`.
- Test the reworded, added and removed cases next to the existing case where the criteria stay the same and the worker starts.
- Drop the question, since you've answered it.

**What the planner's plan covers:** five criteria with six tests.
- Every blocker in a review says who fixes it: the worker for code, the planner for tests.
- A code review with any test blocker starts the planner instead of the worker.
- The planner answers the test blockers and the worker answers the code blockers.
- An approved test fix goes straight back to the worker.
- The reviewer's instructions tell it to name who fixes each blocker.

Apart from B1, the plan and its tests hold up. All six new tests fail today for the right reason, because the feature isn't built yet. The rest of the suite passes: 6 failed, 179 passed.

The plan changes the reviewer's instruction files in `dokima/roles/`, which this repo keeps off-limits unless the issue asks. Your issue asks for each code-review blocker to say who fixes it, which needs those instructions to change, so I left it as a note rather than a blocker.

The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.
