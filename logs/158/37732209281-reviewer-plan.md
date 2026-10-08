# reviewer (plan) for #158

Run: https://github.com/dokima-dev/dokima/actions/runs/37732209281

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #158: The reviewer lists every ask in the owner's words, and real hand-backs become test samples
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #139, story 5</summary>
> 
> **Part of:** #139 Agent hand-backs: one deterministic checker that reads only the JSON files
> 
> **User story:** A plan never drops one of the owner's asks unnoticed: the reviewer reads the issue on its own and lists every ask it finds, each matched to a criterion or marked missing.
> 
> **Context:** The owner's answer 3 on the issue: the planner cannot check itself for dropped asks because it writes the criteria from the owner's words, so the reviewer reads the issue text on its own and lists every ask; review.json gets a field for exactly this, and the checker rejects a plan review without it. The review.json shape lives in dokima/roles/reviewer.md (the owner asks for this change, so editing dokima/roles/ is allowed here) and is checked by dokima/agent.py problems_review. Proposed shape: "asks": [{"ask": "the owner's words", "source": "issue or comment link", "criterion": "N.k" | "S<s>.<k>" | "missing"}]. Answer 1: keep real JSON hand-backs from this run as test samples once the format is settled; the records in .dokima/139/ written before this story (01-planner.json, 02-reviewer-plan.json) predate the asks field, so the samples are hand-backs recorded after stories 1 to 4 land, copied into tests/samples/.
> 
> **Acceptance criteria:**
> - The reviewer's prompt tells

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_review_asks.py
```

> commit c8a58d91b659ccfae721afe9740c886d25d00c07
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:17:46 2026 +0000
> 
>     planner for #158 (run 37730752132)
> 
>  tests/test_failed_run_card.py |   3 +-
>  tests/test_review_asks.py     | 235 ++++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py           |   7 +-
>  3 files changed, 242 insertions(+), 3 deletions(-)
> """A plan review lists every ask of the owner, and real hand-backs are kept as samples that pass their checkers.
> 
> The planner writes the criteria from the owner's words, so it cannot check itself for an ask it dropped. The reviewer
> reads the issue on its own and hands back an asks list in review.json: each ask in the owner's words, a link to where
> they said it, and the plan's criterion it maps to, or "missing". Code rejects a plan review without that list, and a
> plan review that marks an ask missing cannot approve.
> 
> Every check here runs the real commands the workflow runs on a review (`agent check review FILE PLAN N`, then
> `agent check-round reviewer FILE PACK`) on a starting pack built in a temp folder, with STAGE set as the workflow's job
> sets it: a plan review's pack, or a code review's pack, which also holds the PR's diff. A plan for issue 9 with criteria 9.1 to 9.3 stands in for the plan.
> """
> import json
> import os
> import re
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> SAMPLES = os.path.join(ROOT, "te

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_review_asks.py 2>&1 | grep -E "^E .*15[8]|passed|failed" | head -20; python -m pytest -q 2>&1 | tail -8; git show HEAD -- tests/test_start.py tests/test_failed_run_card.py
```

> E       AssertionError: 158.1: the review.json shape in reviewer.md has no asks list of {"ask": ..., "source": ..., "criterion": "N.k" | "missing"}
> E       AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> E       AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> E       AssertionError: 158.4: tests/samples/ holds no samples: keep real hand-backs there, one folder per issue
> 4 failed in 0.67s
>  +    and   re.DOTALL = re.S
> FAILED tests/test_review_asks.py::test_a_plan_review_must_list_every_ask_well_formed - AssertionError: 158.2: a plan review with no asks list was let through (exit 0); it must be rejected
> assert 0 == 1
> FAILED tests/test_review_asks.py::test_a_plan_review_with_a_missing_ask_cannot_approve - AssertionError: 158.3: an approve with the ask 'Oil the hinges' marked missing was let through (exit 0); it must be rejected
> assert 0 == 1
> FAILED tests/test_review_asks.py::test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers - AssertionError: 158.4: tests/samples/ holds no samples: keep real hand-backs there, one folder per issue
> assert []
> 4 failed, 288 passed in 73.10s (0:01:13)
> commit c8a58d91b659ccfae721afe9740c886d25d00c07
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 05:17:46 2026 +0000
> 
>     planner for #158 (run 37730752132)
> 
> diff --git a/tests/test_failed_run_card.py b/tests/

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "STAGE" .github/workflows/agent.yml | head -20; grep -n "check review\|check-round" .github/workflows/agent.yml
```

> 48:      STAGE: ${{ (inputs.role || github.event.client_payload.role) == 'reviewer' && (inputs.stage || github.event.client_payload.stage) || '' }}
> 84:          elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
> 96:          LOG="logs/$N/${{ github.run_id }}-$ROLE${STAGE:+-$STAGE}.md"
> 104:          python3 -m dokima.agent pack "$N" "$ROLE" "$STAGE" "$PACK" 2> /tmp/pack-err.txt || {
> 111:          if [ "$STAGE" = pr ]; then git diff origin/main...HEAD > "$PACK/diff.patch"; fi
> 119:        if: env.STAGE == 'pr'
> 125:          python3 -m dokima.agent check-pack "$ROLE" "$STAGE" "$PACK" > /tmp/pack-check.txt \
> 135:          case "$ROLE$STAGE" in
> 150:          - $PACK/open_blockers.json: the open blockers from the newest review at your stage. Answer every one by id.$( [ "$STAGE" = pr ] && echo "
> 153:          You are on branch try/issue-$N. Your stage is: ${STAGE:-$ROLE}.
> 174:            python3 -m dokima.agent record "$ROLE" "$STAGE" "$OUT" "$OUT/check.txt" "${PASSED:-false}" /home/runner/.claude/projects
> 180:            python3 -m dokima.agent not-started "$ROLE" "$STAGE" "$OUT" /tmp/why.txt
> 241:          { echo "# ${ROLE}${STAGE:+ ($STAGE)} for #$N"; echo; echo "Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"; echo
> 262:          if [ -n "$PR" ] && { [ "$ROLE" = worker ] || [ "$STAGE" = pr ]; }; then
> 137:            reviewerplan) GRADE=plan-grade;   FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json $PACK/pl

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def read_output" -A25 dokima/planner.py | head -40; grep -n "def .*round\|resolved" dokima/agent.py | head -30
```

> 44:def read_output(out, number=None):
> 45-    """('plan', dict) or ('feature', str); Garbled if OUT holds anything else.
> 46-
> 47-    Given the issue number, every criterion's source must be that issue's link or one of its comment links.
> 48-    """
> 49-    if os.path.exists(os.path.join(out, "question.md")):
> 50-        raise Garbled(f"found question.md: {ALWAYS}")
> 51-    if not os.path.exists(os.path.join(out, "plan.json")):
> 52-        raise Garbled(f"found no plan.json: {ALWAYS}")
> 53-    try:
> 54-        p = json.load(open(os.path.join(out, "plan.json")))
> 55-    except ValueError as e:
> 56-        raise Garbled(f"plan.json is not valid JSON: {e}")
> 57-    if not isinstance(p, dict):
> 58-        raise Garbled(f"plan.json must be an object, not a {type(p).__name__}: {ALWAYS}")
> 59-    if "kind" not in p:
> 60-        raise Garbled(f"plan.json has no kind: {ALWAYS}")
> 61-    return from_kind(p, issue_link(number) if number is not None else None)
> 62-
> 63-
> 64-def strings(v):
> 65-    return isinstance(v, list) and all(isinstance(x, str) and x.strip() for x in v)
> 66-
> 67-
> 68-def check_source(where, source, issue):
> 69-    """Garbled unless the source is this issue's link or one of its comment links; no issue given, nothing to check."""
> 127:def problems_round(role, h, pack_dir):
> 133:        resolved, listed = h.get("resolved", []), h.get("blockers", [])
> 134:        if not isinstance(resolved, list) or not all(isinstance(x, str) for x in resolved):
> 135:            bad.append("resolved must be a list

**Agent:** I've read the plan and run its tests; all four new ones fail for the right reason. Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote four criteria: the reviewer's prompt asks for every ask; a plan review's asks list is checked; a missing ask cannot approve; real hand-backs are kept as samples that pass their checkers.",
          "Wrote one test per criterion in tests/test_review_asks.py, and added an asks list to the fake plan reviews in four older tests."],
  "decided": ["Only a plan review must carry an asks list; a code review on the pull request needs none.",
              "The samples are issue #132's plan and PR #192's work and code review, since no plan review with an asks list exists yet; the owner went on with this reading by saying /review."],
  "open": ["A real plan review with an asks list joins the samples in a follow-up once one is recorded."]},
 "verdict": "approve",
 "summary": "Every ask of the issue has a criterion and a test that fails today because the feature is missing; the plan can go to work.",
 "blockers": [],
 "notes": [
  {"text": "158.4 checks that each sample has a link to the comment it was copied from and passes its checker, but not that its content matches that comment, so a hand-written sample with a real-looking link would pass. The code review should compare the samples with the linked records by hand.",
   "evidence": "tests/test_review_asks.py::test_real_hand_backs_are_kept_as_samples_and_pass_their_checkers checks sources.json against a link pattern only."},
  {"text": "158.1 reads the prompt's words rather than running a reviewer; that is the only practical proof for a prompt change.",
   "evidence": "tests/test_review_asks.py::test_the_reviewer_prompt_asks_for_every_ask_in_the_owners_words reads dokima/roles/reviewer.md."}],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 158 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/r
```

> exit 0

**Agent:** I approved the plan for #158. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the planner proposed:**
1. The reviewer's prompt tells it to read the issue and comments on its own. It then lists every ask in your words, with a link to where you said it. Each ask is matched to a criterion or marked missing.
2. A plan review is rejected if its asks list is absent, empty or badly formed, or if an ask names a criterion the plan doesn't have. The rejection says what's wrong. A code review on the pull request doesn't need an asks list.
3. A plan review with any ask marked missing can't approve, and the rejection names each missing ask.
4. Real records are kept as test samples under `tests/samples/`, and each must pass its checker on every test run. These are issue #132's plan and PR #192's work and code review. When you said `/review`, you went with this reading of the planner's question. A plan review with an asks list gets added later, once one exists.

**Checks I ran:**
- **New tests:** all four fail today because the feature is missing. None of them crash or fail on a bad path.
- **Full suite:** 288 pass and only those four fail, so the asks lists the planner added to four older tests' fake reviews break nothing.
- **Workflow:** the review check knows whether it's grading a plan or a pull request without any change to `.github/workflows/`.

**Two notes, neither blocking:**
- **Copies not checked against originals:** the samples test checks each sample's link and that it passes its checker. It doesn't check that the content matches the comment it links to, so a hand-written file with a real-looking link would pass. At code review, someone should compare the samples with the linked records by hand.
- **Prompt test reads words only:** the test for criterion 1 reads the prompt's wording rather than running a reviewer. That's the only practical way to test a prompt change.

**Next:** it's your call to approve the plan with `/work`.
