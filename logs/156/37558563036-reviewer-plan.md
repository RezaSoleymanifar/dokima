# reviewer (plan) for #156

Run: https://github.com/dokima-dev/dokima/actions/runs/37558563036

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
> 04-planner.json
> 05-planner.json
> # Issue #156: Plan checker: features are checked
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 3</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** A proposed split reaches the owner only when it is complete: every story is well formed and its dependencies point at the split's own stories with no loops.
> 
> **Context:** dokima/planner.py from_kind checks only that a feature has 2 to 5 stories. A feature whose story depends on itself, with an empty title, is accepted today. The owner dropped the question checks from this story (comment of 2026-10-06T20:49): the question kind goes away (story 1). In a feature, criteria have no N.k numbers yet; code names story s's criterion k as 'S<s>.<k>' (for example S2.3), which story 4 and story 5 use when a review names a criterion of a split.
> 
> **Acceptance criteria:**
> - A feature story missing its title, user_story, acceptance_criteria or a depends_on list is rejected, and the reason names the story and the field. ([source](https://github.com/dokima-dev/dokima/issues/139))
> - A story that depends on itself, on a story the feature does not have, or on others in a loop is rejected, and the reason names the story; a valid chain of dependencies passes. ([source](https://github.com/dok

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 78fe9eb --stat; cat tests/test_feature_check.py; git diff 78fe9eb -- tests/test_plan_shape.py
```

> tests/test_feature_check.py | 244 ++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py    |   2 +-
>  2 files changed, 245 insertions(+), 1 deletion(-)
> """The planner's check on a proposed split: every story is well formed and its dependencies form no loop.
> 
> Covers #156. A feature (a split into stories) reaches the owner only when every story has its title, user story,
> acceptance criteria and a depends_on list, every criterion of a story has its text and source link, and every dependency points at another story of the same split with
> no loop. Stories are named by their number counting from 1 ("story 2"), the way the split's card numbers them;
> depends_on holds story indices counting from 0, the way /work files them as sub-issues.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import planner  # noqa: E402
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> SRC = "https://github.com/o/r/issues/9"
> 
> 
> def story(title, deps):
>     """One well-formed story with the given title and dependencies."""
>     return {"title": title, "user_story": f"Owners get {title}.",
>             "acceptance_criteria": [{"text": f"{title} works.", "source": SRC}], "non_functional": [], "depends_on": deps}
> 
> 
> def feature(*stories):
>     """A feature holding the given stories."""
>     return {"kind": "feature", "feature": "A split.", "stories": list(stories)}
> 
> 
> def hand_back(tmp_path,

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^SRC" tests/test_plan_shape.py; python -m pytest -q 2>&1 | tail -50
```

> 17:SRC = "https://github.com/o/r/issues/9"
>             assert names(str(e), 2) and not names(str(e), 1), f"156.3: the reason does not name story 2 alone: {e}"
>             return
>         except Exception as e:  # noqa: BLE001
>             pytest.fail(f"156.3: a criterion that is not an object crashed the check with {type(e).__name__}: {e}")
> >       pytest.fail(f"156.3: a story criterion that is not an object ({item!r}) was accepted")
> E       Failed: 156.3: a story criterion that is not an object (['text', 'source']) was accepted
> 
> tests/test_feature_check.py:244: Failed
> =========================== short test summary info ============================
> FAILED tests/test_feature_check.py::test_a_story_missing_a_field_is_rejected_naming_story_and_field[title-<lambda>0] - Failed: 156.1: a broken feature was accepted: [{"title": "First", "user_story": "Owners get First.", "acceptance_criteria": [{"text": "First works.", "source": "https://github.com/o/r/issues/9"}], "non_functional": [], "depends_on": []}, {"user_story": "Owners get Second.", "acceptance_criteria": [{"text": "Second works.", "source": "https://gi
> FAILED tests/test_feature_check.py::test_a_story_missing_a_field_is_rejected_naming_story_and_field[title-<lambda>1] - Failed: 156.1: a broken feature was accepted: [{"title": "First", "user_story": "Owners get First.", "acceptance_criteria": [{"text": "First works.", "source": "https://github.com/o/r/issues/9"}], "non_functional": [], "depends_on": []}, {"title": "  ", "user_

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "source" dokima/planner.py | head -30
```

> 98:        if not str(c.get("source", "")).strip():
> 99:            raise Garbled(f"acceptance criterion '{c['text'][:60]}' has no source link")
> 130:    """Each test function in a file: name -> (its source, the criterion keys it proves)."""

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": [
    "Added the owner's answer to criterion 156.1: a split is refused when any criterion of a story lacks its text or its source link, naming the story and \"text\" or \"source\".",
    "Added tests for that, for a story criterion that is not an object, and for the check command refusing a loop and then passing the fixed chain (9 tests in all)."
  ],
  "decided": [
    "Checks on a story's non_functional list stay out, since the owner named only the story's fields and its criteria's text and source.",
    "Raised that the planner check counts only tests changed in the current round, which refused round 3 of this issue for criteria whose tests already existed."
  ],
  "open": []
 },
 "verdict": "approve",
 "summary": "The plan now does what the owner asked on 2026-10-07 (story criteria need their text and source), and every new test fails today because the split check accepts the broken split, with the good cases passing beside them.",
 "blockers": [],
 "notes": [
  {"text": "Ran the tests on try/issue-156: all 34 new failing cases fail because the broken split is accepted (or the check command exits 0), not from a crash or path; the good cases and the rest of the suite pass.",
   "evidence": "python -m pytest -q: 34 failed, 133 passed; every failure is in tests/test_feature_check.py with a \"156.N: ... was accepted\" or \"exit 0\" message."},
  {"text": "A story criterion's source is checked the same way a user story's is today (present and not blank), so the worker can reuse that rule rather than demand a URL.",
   "evidence": "dokima/planner.py:98 rejects a criterion whose source is blank; tests/test_feature_check.py::test_a_story_criterion_missing_its_text_or_source_is_rejected breaks only by removing or blanking it."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [
  {"title": "Planner check should count a plan's tests across the whole branch, not only 
```

> (Bash completed with no output)

**Agent:** I approved the plan for #156. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks passed with nothing reported.

- **Your ask is in the plan:** On 2026-10-07 you said a story's acceptance criteria need sources too. Criterion 156.1 now rejects a split when any criterion of a story has no text or no source link. The rejection names the story ("story 2") and says whether the text or the source is missing. One test covers each way it can break (missing or blank text, missing or blank source).
- **The new tests fail for the right reason:** I ran the full test suite on `try/issue-156`: 34 failed and 133 passed. Every failure is in `tests/test_feature_check.py`, and each one fails because today's code accepts a broken split or the check command exits 0. None of them crash or fail on a bad path. The well-formed splits and valid dependency chains are already accepted today, and the rest of the suite passes.
- **No earlier blockers:** There were none to answer.

Two notes for the worker:
- A story criterion's source should be checked the same way a user story's is today: present and not blank (`dokima/planner.py:98`). It does not have to be a URL.
- The plan leaves out checks on a story's `non_functional` list, because you named only the story's own fields and its criteria's text and source.

I also proposed one separate issue, which the planner raised. The planner check counts only the tests added or changed in the current round. That is why round 3 of this issue was rejected with "criterion 156.2 has no test" even though those tests already existed on the branch. The check should count the plan's tests on the whole branch instead.
