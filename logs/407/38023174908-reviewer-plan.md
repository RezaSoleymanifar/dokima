# reviewer (plan) for #407

Run: https://github.com/dokima-dev/dokima/actions/runs/38023174908

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #407: A new issue shows the owner's text open until a plan exists; it folds only once planned
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #407](https://github.com/dokima-dev/dokima/issues/407)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> Until an issue has a plan, the owner's original text shows open on its card, not folded: it is the only content, so it reads first, with the Definition of Done below it. Once a plan exists, the original text moves into its "Original issue" fold, as today.
> 
> Owner's words (2026-10-09): "which story handles unfolding original story and showing it as full when issue is first created? currently it is folded even for the first ever story."
> 
> Why: #237 promised "The owner's ask reads open on the issue they wrote". #373 then folded the original text on every card, and #371 put the Definition of Done below that fold, so a brand-new issue (for example #405) shows only "Original issue" closed.
> 
> 
> </details>
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_open_until_planned.py; wc -l dokima/body.py
```

> commit d61836af3f62766760d3acc67c01f88a288b0ce4
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 04:10:57 2026 +0000
> 
>     planner for #407 (run 38022598356)
> 
>  tests/test_new_issue_card.py     |  32 +++---
>  tests/test_open_until_planned.py | 242 +++++++++++++++++++++++++++++++++++++++
>  2 files changed, 258 insertions(+), 16 deletions(-)
> """A new issue shows the owner's text open until planned, then folded under Original issue.
> 
> Issue #407. #237 promised the owner's ask reads open on the issue they wrote; #373 then folded the owner's text on
> every card and #371 put the Definition of Done below that fold, so a brand-new issue showed only a closed "Original
> issue" fold and the Definition of Done. The owner asked (2026-10-09) that until an issue has a plan, its original text
> shows open, read first, with the Definition of Done below it; once a plan exists the text moves into its Original
> issue fold, as today.
> 
> A split's sub-issue is not the owner's own text: code quotes it from the parent's approved plan, and #237 (237.3)
> decided it stays folded. It keeps its fold here too.
> 
> The card is drawn by dokima/card.py render and saved by card.draw through dokima/body.py. These tests run card.draw
> with GitHub faked by the recorder in tests/test_body.py (via the helpers of tests/test_new_issue_card.py) and read the
> body it saves the way the owner reads the issue.
> """
> import os
> import re
> import sys
> 
> sys.path.insert(0, os.path.join(os.path

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_new_issue_card.py; cat dokima/body.py; timeout 600 python -m pytest -q tests/test_open_until_planned.py tests/test_new_issue_card.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ (passed|failed))|Error|assert" | head -60
```

> commit d61836af3f62766760d3acc67c01f88a288b0ce4
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 04:10:57 2026 +0000
> 
>     planner for #407 (run 38022598356)
> 
> diff --git a/tests/test_new_issue_card.py b/tests/test_new_issue_card.py
> index 63ee355..2d25d60 100644
> --- a/tests/test_new_issue_card.py
> +++ b/tests/test_new_issue_card.py
> @@ -2,10 +2,10 @@
>  
>  Issue #371. The owner asked (2026-10-09) that when an issue is first posted and has no plan yet, the Definition of
>  Done line no longer comes before the owner's original issue text: it moves below that text, and the line "This issue
> -has no plan yet." goes away. Since #373 the owner's text sits in a closed fold titled Original issue below the card's
> -marker, so on an issue with no plan the body reads: the card's status and link lines, the Original issue fold, then the
> -Definition of Done. Once the issue has a plan, the card is drawn as before, with the Definition of Done at its bottom,
> -above the fold.
> +has no plan yet." goes away. Since #407 the owner's text shows open below the card's marker until the issue has a plan,
> +so on an issue with no plan the body reads: the card's status and link lines, the owner's text, then the Definition of
> +Done. Once the issue has a plan, the card is drawn as before, with the Definition of Done at its bottom, above the
> +owner's text in its closed Original issue fold.
>  
>  The card is drawn by dokima/card.py render and saved by card.draw through 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "237.3\|237\.1\b" tests/*.py | head; grep -n "def story_body" -A25 dokima/agent.py; python -m pytest -q tests/test_open_until_planned.py 2>&1 | tail -10; timeout 900 python -m pytest -q -x -p no:cacheprovider 2>&1 | tail -5
```

> tests/test_open_ask.py:52:# 237.3: where the owner's text is quoted from somewhere else, like a split's sub-issues, it stays folded
> tests/test_open_ask.py:60:    record_property("proves", "237.3")
> tests/test_open_ask.py:63:    assert_folded("237.3", new, quoted)
> tests/test_open_ask.py:65:    assert_folded("237.3", again, quoted)
> tests/test_open_ask.py:66:    assert below(again) == below(new), "237.3: a redraw changed the part below the marker of a split's story"
> tests/test_open_ask.py:67:    assert_folded("237.3", body.redraw("An owner's own ask.", "the card"), "An owner's own ask.")
> tests/test_open_ask.py:75:    record_property("proves", "237.3")
> tests/test_open_ask.py:78:    assert saved is not None, "237.3: the card saved nothing on a split's story"
> tests/test_open_ask.py:79:    assert_folded("237.3", saved, quoted)
> tests/test_open_ask.py:80:    assert not github.comments, "237.3: redrawing a split's story posted a refusal"
> 228:def story_body(parent, i, story, parent_title):
> 229-    """A story's issue body, drawn by code from the approved plan, so the child planner starts from exactly what was agreed."""
> 230-    lines = ["<!-- dokima-card -->", "<!-- /dokima-card -->", "",
> 231-             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
> 232-             f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
> 233-    if story.get("context"):
> 234-        lines += [f"**Context:** {story['conte

`5. Bash`
```
cd /home/runner/work/dokima/dokima; ls tests | grep -i -E "fold|ask|body|card"; grep -ln "Original issue" tests/*.py
```

> card_player.py
> test_body.py
> test_card.py
> test_card_bullets.py
> test_card_criterion_label.py
> test_card_folds.py
> test_card_guard.py
> test_card_merge.py
> test_card_queue.py
> test_card_records.py
> test_card_running.py
> test_card_status.py
> test_card_sweep.py
> test_failed_run_card.py
> test_live_card.py
> test_new_issue_card.py
> test_open_ask.py
> test_progress_card.py
> test_raised_cards.py
> test_review_asks.py
> test_run_cards.py
> tests/test_card.py
> tests/test_card_folds.py
> tests/test_open_ask.py
> tests/test_open_until_planned.py
> tests/test_scan.py
> tests/test_new_issue_card.py

**Agent:** I'm checking whether the plan's tests are complete by trying a quick prototype of the change in a scratch copy of the repo.

`6. Bash`
```
rm -rf /tmp/proto && cp -r /home/runner/work/dokima/dokima /tmp/proto && cd /tmp/proto && python3 - <<'EOF'
p='dokima/body.py'; s=open(p).read()
s=s.replace('''    if i < 0 or "\\n" in below[i + len(TRAILER):] or not below[:i].endswith(FOLD_END) or \\
            not below.startswith(FOLD_START) or i < len(FOLD_START) + len(FOLD_END):
        return below, ""''','''    if i < 0 or "\\n" in below[i + len(TRAILER):]:
        return below, ""
    if below.startswith(FOLD_START) and below[:i].endswith(FOLD_END) and i >= len(FOLD_START) + len(FOLD_END):
        return below[:i], below[i:]
    if below.startswith(OPEN_START) and not below.startswith(FOLD_START):
        return below[:i], below[i:]
    return below, ""''')
s=s.replace('''    below = FOLD_START + owner + FOLD_END + ("" if done is None else TRAILER + done.strip("\\n"))''','''    story = owner.startswith("<!-- dokima-card -->\\n<!-- /dokima-card -->\\n\\n<details open><summary>From the approved plan of #")
    wrap = FOLD_START + owner + FOLD_END if done is None or story else OPEN_START + owner
    below = wrap + ("" if done is None else TRAILER + done.strip("\\n"))''')
open(p,'w').write(s)
EOF
timeout 900 python -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | head -30
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bxuhatsx6). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/c0f9cd6d-d5a8-448c-97e3-405fee72828a/tasks/bxuhatsx6.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/c0f9cd6d-d5a8-448c-97e3-405fee72828a/tasks/bxuhatsx6.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/c0f9cd6d-d5a8-448c-97e3-405fee72828a/tasks/bxuhatsx6.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Meanwhile I'll look at the AGENTS.md wording and the scan test.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Original issue" tests/test_scan.py tests/test_card_folds.py tests/test_card.py | head -20
```

> tests/test_scan.py:316:            # The PR carries its issue's Original issue fold below the card (#373), read from the issue's body.
> tests/test_card.py:118:    # Since #373 the PR also carries the owner's text in a closed Original issue fold between the card and Closes #40.
> tests/test_card.py:121:    assert "\n<details><summary>Original issue</summary>\n\nMy ask.\n\n</details>" in pr
> tests/test_card_folds.py:10:and card.pr_body(card, pr_body, ask) puts the same Original issue fold on the PR, between the card and its Closes line.
> tests/test_card_folds.py:137:# 373.3: the owner's original issue text sits in a fold titled Original issue, closed by default
> tests/test_card_folds.py:141:FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> tests/test_card_folds.py:152:        f"{k}: the owner's text is not alone inside a closed Original issue fold below the card:\n{below!r}"
> tests/test_card_folds.py:162:    """The owner's text sits below the card in a closed fold titled Original issue.
> tests/test_card_folds.py:177:    """An ask that shows open today folds under Original issue on its next redraw.
> tests/test_card_folds.py:180:    each and checks it is saved, not refused, with the text byte for byte in the closed Original issue fold."""
> tests/test_card_folds.py:191:    """The card and the planner both save the owner's text folded under Original issue.
> tests/test_card_folds.py:194:    ask, and checks every saved body keeps the owner's text byte for byte in the closed Origin

`9. Bash`
```
until grep -qE "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/c0f9cd6d-d5a8-448c-97e3-405fee72828a/tasks/bxuhatsx6.output; do sleep 5; done; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/c0f9cd6d-d5a8-448c-97e3-405fee72828a/tasks/bxuhatsx6.output
```

> FAILED tests/test_open_until_planned.py::test_agents_md_says_the_text_shows_open_until_planned - AssertionError: 407.5: AGENTS.md's The issue body does not say an issue with no plan shows the owner's text open, with its Definition of Done
> 1 failed, 839 passed, 79 skipped in 188.63s (0:03:08)
> 
> [exited with code 0]

**Agent:** The prototype passes every test except the AGENTS.md one, which only a docs change can fix. So the tests are consistent and can be met within the plan's scope.

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote three criteria: an issue with no plan shows the owner's text open with the Definition of Done below it; once planned the text folds under Original issue; a split's sub-issue keeps its quoted story folded.",
          "The planner added eight tests in tests/test_open_until_planned.py and updated the shared layout check in tests/test_new_issue_card.py to expect open text on an issue with no plan."],
  "decided": ["Only dokima/body.py and AGENTS.md change; dokima/card.py and the pull request's Original issue fold stay as they are.",
              "A split's sub-issue, whose text code quotes from the parent's plan, stays folded before its own plan, as #237 decided."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers every ask: an issue with no plan shows the owner's text open with the Definition of Done below, and once planned the text folds; every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "All eight new tests fail today for the right reason. A quick trial change to dokima/body.py alone (open the text when the card has no plan, unless the body is a split's quoted story) passes every test in the suite except the AGENTS.md one, so the tests can be met within the plan's scope and don't conflict with the earlier tests for #237, #371 or #373.",
   "evidence": "pytest -q tests/test_open_until_planned.py: 8 failed (e.g. '407.1 (no record): an issue with no plan still folds the owner's text under Original issue'); with the trial change in a scratch copy, the full suite gives 1 failed (407.5 AGENTS.md), 839 passed."},
  {"text": "The owner's comment says 'even for the first ever story'. The plan reads 'story' as the issue the owner wrote and keeps split stories folded, following #237 and AGENTS.md ('a split's sub-issue ... is folded the same way'). That earlier decision covers it, so no questio
```

> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`11. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers every ask: the owner's text shows open until planned, then folds; every new test fails today because the feature is missing."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 407 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; rm -rf /tmp/proto
```

> rc=0

**Agent:** I approved the plan for [#407](https://github.com/dokima-dev/dokima/issues/407) (a new issue shows the owner's text open until it has a plan). The review is in `/tmp/dokima-out/review.json` and passes both checks.

- **Every ask is covered.** Each of the four things the owner asked for, in the issue and in their comment, maps to a criterion: the text shows open first with the Definition of Done below it, and once a plan exists it folds under Original issue. Nothing is marked missing.
- **The new tests fail today for the right reason.** All eight tests in `tests/test_open_until_planned.py` fail because the feature is missing, not because a test is broken. For example: "407.1 (no record): an issue with no plan still folds the owner's text under Original issue".
- **The tests can be met within the plan's scope.** In a scratch copy, which I deleted afterwards, I changed only `dokima/body.py`. With that change the whole suite passes except the AGENTS.md test (839 passed, 1 failed), and that one needs the AGENTS.md wording the plan already includes. So the new tests don't clash with the earlier ones for #237, #371 or #373.
- **Split sub-issues stay folded.** The owner's comment says "even for the first ever story". The plan reads "story" as the owner's own issue and keeps a split's sub-issues folded before their own plan. #237 and AGENTS.md already decided that, so no question to the owner was needed. I recorded this as a note, not a blocker.

The plan asked the owner no questions, and I raised no blockers.
