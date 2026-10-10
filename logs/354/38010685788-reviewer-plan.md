# reviewer (plan) for #354

Run: https://github.com/dokima-dev/dokima/actions/runs/38010685788

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #354: The words Acceptance criterion carry the link, not the criterion's text
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> On every card, the words Acceptance criterion link to the criterion's check, and the criterion's own text after them is plain.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #354](https://github.com/dokima-dev/dokima/issues/354)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #359, #373
> 
> **User story:** On every issue and PR card, the owner clicks the words Acceptance criterion to open the check that proves it, and reads the criterion's text as plain words with no link on it.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** The words Acceptance criterion link to the criterion's own check, and the criterion's text after them is plain. The status icon is never linked; with no check yet, nothing is.
>   

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git show --stat HEAD | head -20; cat tests/test_card_criterion_label.py; pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py 2>&1 | tail -25
```

> 4ae60ba planner for #354 (run 38006702494)
> 39825a6 Bug: a pull request that clashes with main is re-planned on every merge but never rebuilt (#374)
> 264b394 Bug: a parent closes and moves to Done when its last sub-issue closes, on autopilot or not (#370)
> commit 4ae60baa844c9102085961331fccc37685837fbb
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 00:02:56 2026 +0000
> 
>     planner for #354 (run 38006702494)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |   4 +-
>  tests/test_card_bullets.py                       |  43 +++---
>  tests/test_card_criterion_label.py               | 158 +++++++++++++++++++++++
>  tests/test_card_records.py                       |  21 ++-
>  4 files changed, 197 insertions(+), 29 deletions(-)
> """On every card, a criterion's label links to its check; its text stays plain.
> 
> Issue #354. The owner: "the word acceptance criterion should get the hyperlink, not the description in front of it."
> 
> The card is drawn by `dokima/card.py` (render, from `found`). Each criterion is one bullet:
> 
>     - <status icon> **<a href="check">Acceptance criterion</a>:** the criterion's text
> 
> The status icon is never inside a link, the only link on the bullet sits on the label's words (with or without its
> colon), and the criterion's text after it is plain. With no check there is no link at all. Non-functional
> requirements, in their fold, read the same with the label Non-functional requirement. Markdown links `[text](url)` an

`3. Bash`
```
cd /tmp/pack; grep -o 'issuecomment-[0-9]*' -r . | sort -u; python3 -c "import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d.get('handback',d),indent=1)[:1500])"
```

> {
>  "previous_step": {
>   "did": [
>    "Planned two criteria: the words Acceptance criterion link to the criterion's check with its text plain, and the same for Non-functional requirement.",
>    "Wrote three new tests in tests/test_card_criterion_label.py and updated the link helpers of tests/test_card_bullets.py, tests/test_card_records.py and one golden card to read the link on the label."
>   ],
>   "decided": [
>    "The status icon is never linked, and a criterion with no check has no link at all.",
>    "The Verified by and Source lines stay as they are; cards on GitHub change on their next redraw, with no backfill."
>   ],
>   "open": [
>    "Asks whether Non-functional requirement bullets move the link to their label too; it planned that they do (354.2)."
>   ]
>  },
>  "verdict": "approve",
>  "summary": "The plan moves each criterion's link onto the words Acceptance criterion, its tests fail today for that reason, and its one question goes to the owner.",
>  "blockers": [],
>  "notes": [
>   {
>    "text": "Every new and updated test fails today for the right reason: the link is still on the criterion's text, not on its label.",
>    "evidence": "pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py: 17 failed, 45 passed; each failure reads e.g. '354.1: the link on the bullet of \u201cFirst thing works\u201d is on \u201cFirst thing works\u201d, not on the words Acceptance criterion'."
>   },
>   {
>    "text": "Both issue and pull reque

**Agent:** No comment link is available, so I'll cite the issue link for the owner's answer.

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned after the owner's answer, keeping both criteria: the words Acceptance criterion link to the criterion's check with its text plain, and the same for Non-functional requirement.",
          "Dropped the question about Non-functional requirement bullets, which the owner answered yes."],
  "decided": ["The status icon is never linked, and a criterion with no check has no link at all.",
              "The Verified by and Source lines stay as they are; cards on GitHub change on their next redraw, with no backfill."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now matches the owner's answer: both the Acceptance criterion and Non-functional requirement labels carry the link, and every new test fails today because the link is still on the text.",
 "blockers": [],
 "notes": [
  {"text": "Every new and updated test fails today for the right reason: the link is still on the criterion's text, not on its label.",
   "evidence": "pytest -q tests/test_card_criterion_label.py tests/test_card_bullets.py tests/test_card_records.py tests/test_raised_cards.py: 17 failed, 45 passed; the golden diff shows '**Acceptance criterion:** <a href=...>A slow call returns a job id.</a>' where '**<a href=...>Acceptance criterion</a>:** ...' is expected."},
  {"text": "The owner's answer on the Non-functional requirement bullets is kept by criterion 354.2 and its test, which checks the passed, failed and no-check cases.",
   "evidence": "tests/test_card_criterion_label.py::test_the_words_non_functional_requirement_link_to_the_check_and_the_text_is_plain"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "On every card, the label \"Acceptance criterion\" is the link to the check that proves it; the criterion's own text after it is plain, unlinked text.", "source": "https://github.com/dokima-dev/dokima/issues/354", "criterion": "354.1"},
  {"
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`5. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan follows the owner's answer: both labels carry the link, and every new test fails today because the link is still on the text."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 354 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#354](https://github.com/dokima-dev/dokima/issues/354) (which part of a criterion bullet carries the link). It now matches your answer: on every card, the words Acceptance criterion and Non-functional requirement carry the link to the check, and the criterion's own text is plain.

- **Your answer is in the plan:** you said yes to moving the link onto the Non-functional requirement label too. Criterion 354.2 now covers that, with a test for a passed check, a failed check and no check. The planner removed the question, so the plan has none left.
- **The new tests fail today for the right reason:** 17 failed and 45 passed across the four card test files. Each failure is the link still sitting on the criterion's text instead of its label, not a crash or a bad path.
- **Every ask of yours maps to a criterion:** your two asks about Acceptance criterion go to 354.1, and your answer on Non-functional requirement goes to 354.2. None is missing.
- **Nothing was open from before:** the earlier review had no blockers to carry over.

One small gap: I couldn't find a link to your answer comment itself, so the review cites the issue link for it. The hand-back checks still passed. The review is saved to `/tmp/dokima-out/review.json`.
