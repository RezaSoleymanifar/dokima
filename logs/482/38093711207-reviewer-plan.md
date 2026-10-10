# reviewer (plan) for #482

Run: https://github.com/dokima-dev/dokima/actions/runs/38093711207

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #482: Code caps the whole text of every field the owner reads
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [483, 484, 486], "loop": []} -->
> **Backlog**
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #483, #484, #486
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #470, story 1</summary>
> 
> **Part of:** #470 Everything Dokima writes for me is simple, terse, plain English; technical detail lives in docstrings
> 
> **User story:** A hand-back with any text over its word limit goes back to the agent that wrote it.
> 
> **Context:** Today dokima/words.py caps only a criterion's first sentence (CRITERION_CAP 25 in dokima/planner.py, criterion_caps uses words.first_sentence), the summary (SUMMARY_CAP 25) and a docstring's first line, each with 20% slack (TOLERANCE); nothing else is capped, which is why #452's criteria ran 33 to 70 words. The checks already run inside the agent's machine: .github/workflows/agent.yml runs `python3 -m dokima.planner check` or `python3 -m dokima.agent check work|review` and tells the agent to fix what it reports, so a rejection there is shortened in the same run with no new run. Fields the owner reads: summary, user story, each criterion, each non-functional text and why, each out-of-sc

`2. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); h=d.get('handback',{}); print(h.get('raises'), h.get('answers'))"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat dokima/words.py
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38092757729",
>  "commit_before": "b755a9a80820f05cdc2df53adfb3078d51e07bc2",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 881016,
>   "turns": 41,
>   "cost_usd": 2.6983194000000004,
>   "tokens_in": 3857779,
>   "tokens_out": 44951
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/482/38092757729-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38092757729",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> None None
> commit ce6e0753f071739e8675f128076288a6e4860459
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 23:03:36 2026 +0000
> 
>     planner for #482 (run 38092757729)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  tests/samples/132/review-pr.json |   6 +-
>  tests/samples/132/work.json      |   4 +-
>  tests/test_whole_text_caps.py    | 382 +++++++++++++++++++++++++++++++++++++++
>  tests/test_word_caps.py          |  50 ++---
>  4 files changed, 400 insertions(+), 42 deletions(-)
> """Word caps on the texts agents hand back: a text a little over its cap is listed, one far over is rejected.
> 
> The owner sets each cap; a text more than TOLERANCE over it (over 30 words for a 25-word cap, over 18 for 15) fails
> the check, and one over its cap but within the tolerance only gets listed, so a few words over never fails a run.
> """
> import re
> 
> TOLERAN

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_whole_text_caps.py; git show HEAD -- tests/test_word_caps.py tests/samples | head -200
```

> """Every text the owner reads is capped whole; a criterion at 12 words.
> 
> Issue #482 (story 1 of #470). Before it, only a criterion's first sentence, the summary and a docstring's first line
> were capped, each with 20% slack, so criteria ran 33 to 70 words. Now every field the owner reads is held to a cap on
> its whole text, and a text one word over its cap is rejected, with no slack. The summary and docstring caps keep their
> rules from #239 and #240.
> 
> The caps live as named numbers in dokima/words.py, so the shared style file (#484) can quote them:
> 
>     CRITERION_CAP 12      each acceptance criterion and each non-functional requirement's text
>     USER_STORY_CAP 20     the user story, a split's feature and each story's user story
>     TITLE_CAP 10          each story's title
>     WHY_CAP 15            each non-functional requirement's why
>     OUT_OF_SCOPE_CAP 15   each out of scope line
>     TEST_CHANGE_CAP 20    each reason in test_changes
>     LABEL_CAP 5           each raise's label
>     RAISE_TEXT_CAP 30     each raise's text
>     EVIDENCE_CAP 30       each raise's evidence
>     ANSWER_CAP 25         each answer's why
>     PREVIOUS_STEP_CAP 15  each did, decided and open line of a review's previous_step
>     BUILT_CAP 15          each line of a work hand-back's criteria
>     TEST_RUN_CAP 20       a work hand-back's evidence (its own test run)
> 
> A rejection names the field the way FIELDS below writes it, then "N words" and "cap of C". The fields of a split's
> story carry the prefix "stor

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_whole_text_caps.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-300; python3 -m pytest -q -x --deselect tests/test_whole_text_caps.py 2>&1 | tail -3; python3 -m pytest -q tests/test_word_caps.py tests/test_review_asks.py 2>&1|tail -2
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bufq8cogf). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, look at how the current checks handle fields and the review asks schema.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "asks\|source" dokima/agent.py | grep -i ask | head -30; grep -n "summary_caps\|criterion_caps\|words\." dokima/planner.py dokima/agent.py | head
```

> 620:    for a in h.get("asks") or []:
> 622:            failing += failed_rows(repo, a.get("ask"), ["  - Nothing covers this"], a.get("source"))
> 787:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 809:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 812:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 1151:def problems_asks(r, ids):
> 1152:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 1154:    asks = r.get("asks")
> 1155:    if not isinstance(asks, list) or not asks:
> 1156:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 1158:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 1159:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 1318:                bad += problems_asks(data, plan_criteria(plan, number))
> 2177:            # A plan posted before #300 asks through its questions field, judged by the review's assumptions.
> dokima/planner.py:12:on today's code. Criteria and the docstrings the planner adds are held to word caps (dokima/words.py): a little over
> dokima/planner.py:353:def criter

`6. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output | cut -c1-250
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output cut -c1-250. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`7. Read`
```
/tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output
```

> 1	>       assert rc == 1, "482.5: a story whose user story is one word over its cap of 20 passed, so the check caps nothing"
> 2	E       AssertionError: 482.5: a story whose user story is one word over its cap of 20 passed, so the check caps nothing
> 3	>           assert rc == 1, f"482.5: a {kind} answer one word over its cap of 25 passed, so the check caps nothing:\n{out}"
> 4	E           AssertionError: 482.5: a work answer one word over its cap of 25 passed, so the check caps nothing:
> 5	FAILED tests/test_whole_text_caps.py::test_a_criterion_over_12_words_is_rejected_with_no_slack - AssertionError: 482.1: dokima/words.py names no criterion cap of 12 (CRITERION_CAP is None)
> 6	FAILED tests/test_whole_text_caps.py::test_every_field_of_a_plan_is_capped_on_its_whole_text - AssertionError: 482.2: dokima/words.py has CRITERION_CAP = None, not 12
> 7	FAILED tests/test_whole_text_caps.py::test_every_field_of_a_work_or_review_is_capped_on_its_whole_text - AssertionError: 482.2: a work hand-back with every owner-read field over its cap was accepted:
> 8	FAILED tests/test_whole_text_caps.py::test_the_planners_check_rejects_one_long_text - AssertionError: 482.3: the planner's check did not reject a 31-word raise naming it: rc 0, ''
> 9	FAILED tests/test_whole_text_caps.py::test_the_worker_and_reviewer_checks_reject_one_long_text - AssertionError: 482.3: the work check did not reject a 31-word raise naming it (exit 0):
> 10	FAILED tests/test_whole_text_caps.py::test_a_plan_rejection_names_the_field_i

`8. Bash`
```
until grep -qE "passed|failed" <(tail -2 /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output | grep -v "^FAILED tests/test_whole"); do sleep 5; done; tail -6 /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output | cut -c1-250
```

> FAILED tests/test_whole_text_caps.py::test_a_plan_with_every_text_at_its_cap_still_passes - AssertionError: 482.5: a story whose user story is one word over its cap of 20 passed, so the check caps nothing
> FAILED tests/test_whole_text_caps.py::test_a_work_or_review_with_every_text_at_its_cap_still_passes - AssertionError: 482.5: a work answer one word over its cap of 25 passed, so the check caps nothing:
> FAILED tests/test_whole_text_caps.py::test_the_planners_check_never_rewrites_the_plan - AssertionError: 482.6: the planner's check exited 0 on a plan over its caps: ''
> FAILED tests/test_whole_text_caps.py::test_the_worker_and_reviewer_checks_never_rewrite_the_handback - AssertionError: 482.6: the work check exited 0 on a hand-back over its caps:
> FAILED tests/test_whole_text_caps.py::test_word_cap_failures_are_reported_apart_from_every_other_failure - AssertionError: 482.7: dokima/words.py has no handback_caps returning a hand-back's word-cap failures on their own
> 12 failed in 3.86s

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned five criteria from #470 and two rules: never rewrite, report caps apart.",
          "Wrote 12 tests that fail today because the caps are missing.",
          "Removed the old 25-word criterion test and shortened one sample hand-back."],
  "decided": ["Caps 13 fields, five of them beyond the owner's list of fields."],
  "open": ["The owner's later comment, keep to my words, is not yet planned for."]},
 "verdict": "block",
 "summary": "The plan caps fields the owner did not list, after the owner said keep to my words.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Beyond the owner's list",
   "text": "The plan caps test changes, review did/decided/open lines, work criteria lines, work evidence and feature, which the owner's field list omits. Cap only listed fields, or ask.",
   "evidence": "Owner's /plan comment: keep to my words; smallest change. tests/test_whole_text_caps.py CAPS; tests/samples/132 shortened."}
 ],
 "answers": [],
 "asks": [
  {"ask": "A criterion over 12 words is rejected, with no slack.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "482.1"},
  {"ask": "Every field the owner reads is capped on its whole text.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "482.2"},
  {"ask": "The planner's, worker's and reviewer's checks all reject text over its cap.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "482.3"},
  {"ask": "A rejection names the field, its word count and its cap.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "482.4"},
  {"ask": "A hand-back with every text within its cap still passes.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "482.5"},
  {"ask": "Code never rewrites an agent's text; it only checks it.", "source": "https://github.com/dokima-dev/dokima/issues/482", "cr
```

> (Bash completed with no output)

`10. Bash`
```
tail -4 /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output | cut -c1-200
```

> FAILED tests/test_whole_text_caps.py::test_the_planners_check_never_rewrites_the_plan - AssertionError: 482.6: the planner's check exited 0 on a plan over its caps: ''
> FAILED tests/test_whole_text_caps.py::test_the_worker_and_reviewer_checks_never_rewrite_the_handback - AssertionError: 482.6: the work check exited 0 on a hand-back over its caps:
> FAILED tests/test_whole_text_caps.py::test_word_cap_failures_are_reported_apart_from_every_other_failure - AssertionError: 482.7: dokima/words.py has no handback_caps returning a hand-back's word-cap 
> 12 failed in 3.86s

**Agent:** I'm blocking the plan for [#482](https://github.com/dokima-dev/dokima/issues/482) (word caps on every text the owner reads). The hand-back is written to `/tmp/dokima-out/review.json` and passes both checks.

**The one blocker (for the planner):** the plan caps 13 fields. Five of them are not in the owner's list of fields:
- reasons for test changes
- the did, decided and open lines of a review
- the criteria lines of a work hand-back
- the test-run evidence of a work hand-back
- a split's feature line

The caps also forced one sample hand-back to be shortened. After this plan was written, the owner commented "/plan Keep to my words; smallest change." This plan doesn't follow that yet. The fix is to cap only the fields the owner listed, or ask the owner about the rest.

**What holds up:**
- **Criteria:** the five match [#470](https://github.com/dokima-dev/dokima/issues/470) (the parent issue) word for word. The two extra rules also come from the owner's text: code never rewrites a text, and word-cap failures are reported separately.
- **New tests:** all 12 in `tests/test_whole_text_caps.py` fail today because the caps don't exist yet, which is the right reason. Each rejection test also has a passing case beside it.
- **Asks:** I listed every ask. All are covered except "Keep to my words; smallest change", which is marked missing.

I haven't seen the result of the full test suite on this branch. It ran in the background and its output only showed the expected failures in the new test file. The review doesn't depend on it.

`11. Bash`
```
tail -8 /tmp/claude-1001/-home-runner-work-dokima-dokima/b9397695-523e-422d-a14f-92218c088199/tasks/bufq8cogf.output | cut -c1-250
```

> 12 failed in 3.86s
> ........................................ss.sss.......................... [ 96%]
> ..............s.................s                                        [100%]
> 965 passed, 76 skipped, 12 deselected in 269.03s (0:04:29)
> s............                                                            [100%]
> 12 passed, 1 skipped in 8.57s
> 
> [exited with code 0]

**Agent:** The full test suite has now finished, and it doesn't change my review.

- **The rest of the suite:** 965 passed and 76 were skipped. The only tests left out were the 12 new ones in `tests/test_whole_text_caps.py`, which I had already run.
- **The two old test files the planner changed:** `tests/test_word_caps.py` and `tests/test_review_asks.py` pass today (12 passed, 1 skipped).

My verdict on the plan for [#482](https://github.com/dokima-dev/dokima/issues/482) (word caps on every text the owner reads) is still to block. The plan caps five fields the owner didn't list, and the owner has since said "Keep to my words; smallest change."
