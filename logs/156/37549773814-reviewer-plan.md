# reviewer (plan) for #156

Run: https://github.com/dokima-dev/dokima/actions/runs/37549773814

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> - A story that depends on itself, on a story the feature does not have, or on others in a loop is rejected, and the reason names the story; a valid chain of dependencies passes. ([source](https://github.com/dokima-dev/dokima/issues/139))
> 
> </details>
> 
> 
> ## Comments
> 
> ### RezaSoleyma

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_feature_check.py; git diff HEAD~1 -- tests/test_plan_shape.py; grep -n "feature\|def from_kind\|stories\|depends" dokima/planner.py | head -60
```

> commit 073bd2ca3b1706cb39f529586b5dfe37f67e67a6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Tue Oct 6 23:23:56 2026 +0000
> 
>     planner for #156 (run 37546126460)
> 
>  tests/test_feature_check.py | 180 ++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_shape.py    |   2 +-
>  2 files changed, 181 insertions(+), 1 deletion(-)
> """The planner's check on a proposed split: every story is well formed and its dependencies form no loop.
> 
> Covers #156. A feature (a split into stories) reaches the owner only when every story has its title, user story,
> acceptance criteria and a depends_on list, and every dependency points at another story of the same split with
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
> def feature(*storie

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "depends_on\|stories" dokima/agent.py | head -30; grep -rn "depends_on" dokima/roles/ | head; python -m pytest -q tests/test_feature_check.py tests/test_plan_shape.py 2>&1 | tail -40
```

> 137:    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links.
> 146:    for i, st in enumerate(plan["stories"], 1):
> 152:                      "blocked_by": [d + 1 for d in st.get("depends_on", [])]})
> 160:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> 187:        lines += [f"{i}. {st.get('title', '')}" for i, st in enumerate(h.get("stories", []), 1)]
> 197:        num = {f["story"]: f["issue"] for f in h.get("stories", [])}
> 199:                         for f in h.get("stories", [])]
> 434:                bad.append("plan.json is a split: /work files its stories as sub-issues, no worker builds it")
> dokima/roles/planner.md:125:  "acceptance_criteria": [...], "non_functional": [...], "depends_on": [story index, ...]}, ...]} with 2 to 5 stories.
>             hand_back(tmp_path, f)
>         except planner.Garbled as e:
>             assert names(str(e), 2), f"156.3: the reason does not name story 2: {e}"
>             return
>         except Exception as e:  # noqa: BLE001
>             pytest.fail(f"156.3: a story that is not an object crashed the check with {type(e).__name__}: {e}")
> >       pytest.fail(f"156.3: a story that is not an object ({item!r}) was accepted")
> E       Failed: 156.3: a story that is not an object (['title']) was accepted
> 
> tests/test_feature_check.py:180: Failed
> =========================== short test summary info ============================
> 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "rejected.txt\|def read_output\|def main\|Garbled" dokima/planner.py | head -20; python -m pytest -q 2>&1 | tail -3
```

> 28:class Garbled(Exception):
> 32:def read_output(out):
> 33:    """('plan', dict) or ('question', str); Garbled if OUT holds anything else."""
> 37:        raise Garbled("the planner must hand back exactly one of plan.json or question.md, found "
> 42:            raise Garbled("question.md must hold one question ending in '?'")
> 47:        raise Garbled(f"plan.json is not valid JSON: {e}")
> 51:        raise Garbled("plan.json needs a non-empty objective")
> 55:            raise Garbled(f"plan.json needs {key} as a {'non-empty ' if required else ''}list of non-empty strings")
> 59:        raise Garbled("plan.json test_changes must map each changed older test to a non-empty reason")
> 77:            raise Garbled("a question needs one question ending in '?'")
> 86:            raise Garbled("a feature needs 2 to 5 stories")
> 89:        raise Garbled(f"plan.json kind must be user_story, feature or question, not {kind!r}")
> 91:        raise Garbled("a story needs a non-empty user_story")
> 94:        raise Garbled("a story needs a non-empty list of acceptance_criteria")
> 97:            raise Garbled("every acceptance criterion needs its text")
> 99:            raise Garbled(f"acceptance criterion '{c['text'][:60]}' has no source link")
> 101:        raise Garbled("every non-functional requirement needs its text and why")
> 103:        raise Garbled("a story needs scope as a non-empty list of files")
> 105:        raise Garbled("out_of_scope must be a list of sentences")
> 108:        raise Garbled("a story needs

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote a plan in which a proposed split is refused when a story lacks its title, user story, criteria or depends_on list, or when a dependency points at itself, at a story the split lacks, or round a loop; each refusal names the story (\"story 2\") and, for a missing field, the field.",
          "Wrote 6 tests (40 cases) in tests/test_feature_check.py and gave the sample story in tests/test_plan_shape.py one criterion so it stays well formed."],
  "decided": ["Stories are named counting from 1 as the card shows them, while depends_on keeps counting from 0 as /work already files them; a story that is not an object at all is refused with a reason, never a crash."],
  "open": ["Asks whether each criterion inside a story must also carry its text and source link; the plan leaves that out."]},
 "verdict": "approve",
 "summary": "The plan covers both of the owner's criteria with tests that run the real check, each turning red on today's code for the right reason and passing the good cases beside them.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 156.1 says a field is missing when it is \"absent, empty, or not a list\"; for depends_on an empty list is valid (a story with no dependencies). The tests already accept depends_on [] and reject only absent, 0 or null, so the worker should follow the tests; the wording could say \"empty\" applies to the text fields and the criteria list only.",
   "evidence": "tests/test_feature_check.py: test_a_well_formed_feature_passes hands back stories with depends_on []; the parametrized missing-field cases for depends_on are pop, 0 and None."},
  {"text": "Ran the tests on try/issue-156: all 25 new failing cases fail because the feature check accepts the broken split (\"a broken feature was accepted\", exit 0 from the check command), not from a crash or path; the 15 good-case tests pass today, and the rest of the suite (133) passes.",
 
```

> (Bash completed with no output)

**Agent:** I approved the plan for #156; it has no blockers. The review is in `/tmp/dokima-out/review.json`, and both checks ran on it without reporting anything.

**What the plan promises:**
- **Missing fields:** a proposed split is refused when any story lacks its title, user story, acceptance criteria or `depends_on` list. The reason names the story as "story 2" (counting from 1, like the card) and the missing field. A complete split is shown to the owner as handed back.
- **Bad dependencies:** a split is refused when a story depends on itself, on a story the split doesn't have, or on others in a loop. The reason names a story at fault and no innocent one. Chains, diamonds and dependencies on later stories pass.
- **Extra safeguard:** the planner added that a story which isn't an object at all is refused with a reason rather than crashing the check.

**Test run:** on this branch the full suite gives 25 failed and 133 passed, and every failure is in the new `tests/test_feature_check.py`. Each of them fails because today's code accepts the broken split, not because of a crash or a bad path. The good-case tests beside them already pass.

**Notes in the review (not blockers):**
- Criterion 156.1 says a field counts as missing when it is "absent, empty, or not a list". For `depends_on`, an empty list is valid: it means the story depends on nothing. The tests already accept `depends_on: []`, so the worker should follow the tests, but the wording could be tightened.
- The second note records the test-run results above.

**Still open for you:** the planner asked whether each criterion inside a story should also need its text and source link. It planned without that check.
