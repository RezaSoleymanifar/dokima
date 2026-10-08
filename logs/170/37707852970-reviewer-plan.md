# reviewer (plan) for #170

Run: https://github.com/dokima-dev/dokima/actions/runs/37707852970

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #170: Planner questions are a question and its assumption, nothing else
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
> The planner still gives me options and a recommendation in its questions. #168 asked me A or B with its pick. I want a question and its assumption. That's it.
> 
> - Each question in plan.json is two fields, the question and the reading the plan assumed. Code rejects anything else.
> - The card shows the question and the assumption. No options, no recommendation.
> - planner.md drops every line and example that asks for options or a recommendation. #154 removes the old one question section but the example with A and B stays.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #170 (2026-10-08T00:24:27Z)
> 
> /plan
> 
> ### dokima-runtime on issue #170 (2026-10-08T00:27:15Z)
> 
> <!-- dokima-record -->
> **Planner**
> 
> When the planner has a question, the owner sees only the question and the reading the plan assumed, never a menu of options with a pick.
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37707605741",
>  "commit_before": "ad1f75956facdf82b481befc8c00f7cd8e0c7c8a",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 1358

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_questions.py; git show HEAD -- tests/test_agent.py tests/test_plan_check.py
```

> commit daf6f9c4f5b2194bdd275583b3030ace44ee3b06
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 00:27:10 2026 +0000
> 
>     planner for #170 (run 37707605741)
> 
>  tests/test_agent.py      |  13 ++---
>  tests/test_plan_check.py |   2 +-
>  tests/test_questions.py  | 134 +++++++++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 142 insertions(+), 7 deletions(-)
> """Planner questions are a question and its assumption, nothing else (#170).
> 
> The owner asked that every question the planner puts in plan.json be exactly two fields, the question and the reading
> the plan assumed; that code reject anything else; that the card show only the question and the assumption; and that
> the planner's prompt stop asking for options or a recommendation. The check is run the way the workflow runs it,
> through planner.main inside a temp git repo (the `check` fixture of tests/test_plan_check.py); the card is drawn with
> agent.render, the code that writes every record comment.
> """
> import copy
> import os
> import re
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent  # noqa: E402
> from tests.test_plan_check import FEATURE, STORY, check  # noqa: E402,F401
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> GOOD = {"question": "Should job ids be numbers?", "assumption": "The plan assumes they are strings."}
> SECOND = {"question": "Should a failed run move to Needs you?", "assumption": "The p

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -i "question\|option\|recommend\|(A)\|(B)" dokima/roles/planner.md; grep -n "question" dokima/agent.py dokima/planner.py dokima/card.py dokima/*.py | head -60
```

> 6:End with exactly one of two: a plan (with its tests) or a split into 2 to 5 child issues. Your questions for the owner
> 7:go inside it, in its questions list. Too big for one PR is not a question: split it.
> 83:- Question: Should a failed run move its card to Needs you, or only mark it red? (A) Needs you, recommended: the owner
> 84:  sees it without looking. (B) Red mark only.
> 85:- Concern: This overlaps the board refresh issue. Evidence: `dokima/board.py`, `decide()`. Recommend folding it in.
> 122:A plan may also carry "questions": ["...?", ...], plain questions for the owner, as many as you need. Ask only where the owner's
> 124:reading, and say in the question which reading you planned for: the owner may answer or not, and the plan stands either
> 126:question here, never a concern and never dropped. The planner is the only agent that asks the owner anything.
> dokima/agent.py:217:        lines += ["", h.get("user_story") or h.get("question") or ""]
> dokima/agent.py:232:    if role == "planner" and h.get("questions"):
> dokima/agent.py:234:        lines += [f"- {q}" for q in h["questions"]]
> dokima/agent.py:353:def problems_questions(qs):
> dokima/agent.py:354:    """Everything wrong with the planner's questions for the owner: a list of plain questions, each asking something ('?')."""
> dokima/agent.py:356:        return ["questions must be a list of plain questions"]
> dokima/agent.py:357:    return [f"question {i} must be a plain question with a '?'" for i, q in enumerate(qs, 1)
> dokima/ag

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 205,240p dokima/agent.py; sed -n 350,360p dokima/agent.py; sed -n 335,350p dokima/planner.py; sed -n 115,130p dokima/roles/planner.md; python -m pytest -q tests/test_questions.py 2>&1 | tail -40; python -m pytest -q 2>&1 | tail -5
```

> def render(rec):
>     """The comment that carries a record: a short readable summary, then the full record as JSON in a fold."""
>     role, h = rec["role"], rec["handback"]
>     head = {"planner": "Planner", "reviewer": f"Reviewer ({rec.get('stage')})", "worker": "Worker", "split": "Split filed"}[role]
>     lines = [MARK, f"**{head}**" + ("" if rec["check"]["passed"] else " · hand-back rejected by code")]
>     if not rec["check"]["passed"]:
>         lines += [""] + [f"- {p}" for p in rec["check"]["problems"]]
>     elif role == "planner" and h.get("kind") == "feature":
>         lines += ["", f"Proposes a split: {h.get('feature', '')}", ""]
>         lines += [f"{i}. {st.get('title', '')}" for i, st in enumerate(h.get("stories", []), 1)]
>     elif role == "planner":
>         lines += ["", h.get("user_story") or h.get("question") or ""]
>     elif role == "reviewer":
>         lines += ["", f"**{h.get('verdict')}**: {h.get('summary', '')}"]
>         fixes = lambda b: f", the {b['fixer']} fixes it" if b.get("fixer") in FIXERS else ""
>         lines += [f"- **{b.get('id')}** ({b.get('criterion')}{fixes(b)}): {b.get('problem')}" for b in h.get("blockers", [])]
>         if h.get("issues_found"):
>             lines += ["", "**Issues found outside this one** (proposals until you file them):"]
>             lines += [f"{i}. {f.get('title')}: {f.get('why')}" for i, f in enumerate(h["issues_found"], 1)]
>     elif role == "split":
>         num = {f["story"]: f["issue"] for f in h.get("stories", [])}
>         line

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q -rA tests/test_questions.py 2>&1 | grep -E "^(PASSED|FAILED)" | cut -c1-260; python -m pytest -q 2>&1 | grep FAILED | grep -v test_questions | cut -c1-300; git stash -q 2>/dev/null; git checkout -q HEAD~1 && python -m pytest -q 2>&1 | tail -2; git checkout -q try/issue-170
```

> PASSED tests/test_questions.py::test_a_question_with_its_assumption_passes_the_check[feature]
> PASSED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[no question-story]
> PASSED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[an empty question-story]
> PASSED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[a question that asks nothing-story]
> PASSED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[a number-story]
> FAILED tests/test_questions.py::test_a_question_with_its_assumption_passes_the_check[story] - AssertionError: 170.1: a user_story with questions [{'question': 'Should job ids be numbers?', 'assumption': 'The plan assumes they are strings.'}] was rejected: "que
> FAILED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[a plain string-story] - AssertionError: 170.1: a user_story whose question 1 has a plain string was accepted
> FAILED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[a plain string-feature] - AssertionError: 170.1: a feature whose question 1 has a plain string was accepted
> FAILED tests/test_questions.py::test_a_question_that_is_anything_else_is_rejected_saying_which_and_why[no assumption-story] - AssertionError: 170.1: the reason for no assumption does not name 'assumption': "questio

**Agent:** I've read the issue, the plan and its tests, and run the suite. Every new test fails today for the right reason, so I'm writing an approval.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan with three criteria: the check accepts only a question and its assumption, the card shows just those two, and the planner's prompt drops options and recommendations.",
          "Added tests/test_questions.py and updated three older tests that used plain-string questions."],
  "decided": ["A question must still contain a '?', and the check covers splits as well as single stories.",
              "The concern example in the planner's prompt keeps its recommendation, because concerns are not questions."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers all three of your asks, and each one has a test that fails today because the change is missing.",
 "blockers": [],
 "notes": [
  {"text": "The 170.3 test checks the example and the hand-back shape, but not the sentence that calls questions \"plain questions\" and says to name the reading inside the question. The worker should rewrite that sentence too so the prompt stays consistent.",
   "evidence": "dokima/roles/planner.md:122-124"},
  {"text": "A few rejection cases already pass today, such as a question with no '?' in a story and a number in place of a question. They guard behaviour that should keep working. Each test function as a whole still fails today.",
   "evidence": "pytest -rA tests/test_questions.py: 22 failed, 5 passed; all 3 changed older tests fail today on the plain-string rule (full suite 29 failed, 236 passed; main 238 passed)"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 170 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/all 3 changed older tests fail today on the plain-string rule/two of the three changed older tests fail today on the plain-string rule, and the record round-trip test passes/' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 170 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #170. Every new test fails today because the change isn't there yet, not because of a crash or a wrong path. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass on it.

**What the plan promises:**
1. **The check:** each question in plan.json must be exactly a `question` (with a '?') and an `assumption`. This applies to single stories and to splits. Plain strings, missing, empty or non-text fields, and any extra field such as options or a recommendation are rejected. The rejection names the question by number and the field at fault. Plans with no questions, or with correctly shaped ones, still pass.
2. **The card:** each question appears on one line with its own assumption. It never shows raw data, options or a recommendation, even when a record carries them.
3. **The prompt:** the A/B example in `dokima/roles/planner.md` is rewritten, every mention of options and recommendations goes, and the hand-back shape is `{"question": "...?", "assumption": "..."}`. The issue names this file, so the rule against changing `dokima/roles/` doesn't block it.

**Test results:**
- **New tests:** 22 fail and 5 pass on this branch. The 5 that pass are a good-split case and four rejections that already work today, kept to guard existing behaviour. Every new test function fails as a whole.
- **Older tests:** the planner rewrote three. Two now fail on today's plain-string rule; the third already passes. Main passes all 238 tests.

**Notes I left for the worker (not blockers):**
- Lines 122–124 of `planner.md` still call questions "plain questions" and say to name the reading inside the question. No test covers that sentence, so the worker should rewrite it along with the example.
- The plan keeps the old rule that a question must contain a '?', which matches your "code rejects anything else".
