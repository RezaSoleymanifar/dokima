# reviewer (plan) for #166

Run: https://github.com/dokima-dev/dokima/actions/runs/37673922849

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
> 02-reviewer-plan.json
> 03-planner.json
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
> - After a code review sends a weak test back, should the approved re-plan go straight to the worker, or wait for your `/work` a

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 6f17ea1 fbc1c4e --stat; git diff 6f17ea1 fbc1c4e -- tests/; grep -n "def test_an_approved_test_fix" -A120 tests/test_fixer.py
```

> tests/test_fixer.py | 42 ++++++++++++++++++++++++++++++------------
>  1 file changed, 30 insertions(+), 12 deletions(-)
> diff --git a/tests/test_fixer.py b/tests/test_fixer.py
> index fd30eb4..6ce3861 100644
> --- a/tests/test_fixer.py
> +++ b/tests/test_fixer.py
> @@ -150,24 +150,42 @@ def test_the_planner_answers_the_test_blockers_and_the_worker_the_code_ones(reco
>      assert got == ["B2"], f"166.3: the worker was handed blockers {got}, not exactly the code blocker B2"
>  
>  
> +def with_criteria(criteria, non_functional=()):
> +    """STORY with these criterion texts and stronger tests, as a re-plan that a code review asked for would hand back."""
> +    return {**STORY, "acceptance_criteria": [{"text": t, "source": "https://x/9"} for t in criteria],
> +            "non_functional": [{"text": t, "why": "w", "principle": "p"} for t in non_functional],
> +            "tests": {f"9.{k}": [f"tests/test_x.py::test_stronger_{k}"] for k in range(1, len(criteria) + len(non_functional) + 1)}}
> +
> +
>  def test_an_approved_test_fix_goes_straight_back_to_the_worker(record_property):
> -    """When the plan review approves a re-plan a code review asked for, the worker starts at once; other plan approvals still wait for /work.
> +    """An approved re-plan that only strengthens tests goes straight to the worker; one that changes any criterion waits for /work.
>  
> -    The river after a plan approval: with a code review's test blocker since the owner last spoke, it starts the
> -    worker. With no code review behind it,

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,80p tests/test_fixer.py; pytest -q 2>&1 | tail -15
```

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
>          "non_functional": [], "scope": ["dokima/x.py"], "out_of_scope": [],
>          "tests": {"9.1": ["tests/test_x.py::test_a"], "9.2": ["tests/test_x.py::test_b"], "9.3": ["tests/test_x.py::test_c"]}}
> 
> 
> def blocker(id_, fixer, criterion="9.1"):
>     """One well-formed blocker; fixer None leaves the field out."""
>     b = {"id": id_, "criterion": criterion, "test": None, "problem": f"problem {id_}", "evidence": "e", "fix"

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Changed criterion 166.4 so a re-plan asked for by a code review goes straight to the worker only when its criteria are the same as the plan the owner approved with /work.",
          "Added test cases where the re-plan rewrites, adds or drops a criterion, or adds a non-functional one; each must stop and ask the owner for /work."],
  "decided": ["A re-plan counts as unchanged when every criterion's text is the same, in the same order; a changed source link or changed tests alone do not need a new /work."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now follows your answer: a re-plan that only strengthens tests goes straight to the worker, and one that changes any criterion waits for your /work, with a test for each case.",
 "blockers": [],
 "notes": [
  {"text": "All six new tests fail today because the feature is missing, and the rest of the suite passes.",
   "evidence": "`pytest -q`: 6 failed, 179 passed; e.g. 166.4 fails with ('stop', 'The plan is approved. Say `/work` to build it...') where it expects ('start', 'worker', '')."},
  {"text": "The plan says criteria count as unchanged only in the same order, but no test reorders them; code that ignores order would still pass. Worth a one-line case.",
   "evidence": "plan.json out_of_scope, last line; tests/test_fixer.py:177-180 covers rewritten, added, dropped and non-functional added, not reordered."}
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 166 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the plan for issue #166. The planner followed your answer, so the one blocker from the last round (B1) is resolved.

**What changed:** Criterion 166.4 now matches your words. If a code review sends a weak test back, the re-plan goes straight to the worker only when its criteria are the same as the plan you approved with `/work`. A re-plan that rewrites, adds or drops a criterion, or adds a non-functional one, stops and asks you for `/work`. The test covers each of those four changes next to the unchanged case. It also checks that these still wait for `/work`:
- a first plan,
- a code review whose blockers were all for the worker,
- a re-plan after you spoke since the code review.

**Test run:** `pytest -q` gave 6 failed and 179 passed. Each of the 6 is a new test failing because the feature isn't built yet, not because of a crash or a bad path. The rest of the suite passes.

**One small gap (a note, not a blocker):** The plan says criteria count as unchanged only if they're in the same order, but no test reorders them. Code that ignores order would still pass. One more test case would close that.

The review is in `/tmp/dokima-out/review.json` and passes both checks.
