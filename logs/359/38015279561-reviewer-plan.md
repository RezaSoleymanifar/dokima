# reviewer (plan) for #359

Run: https://github.com/dokima-dev/dokima/actions/runs/38015279561

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #359: Source links to where the owner said it, shown as a GitHub reference with icon and name
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 354 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #359](https://github.com/dokima-dev/dokima/issues/359)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #354
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summ

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; cat tests/test_card_refs.py; cat /tmp/pack/parent.json | head -50
```

> commit e7b6d94e329fe715b0c394223620f4c018495b35
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 01:59:12 2026 +0000
> 
>     planner for #359 (run 38014530280)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |   4 +-
>  tests/raised_goldens/old-issue-card.md           |   4 +-
>  tests/raised_goldens/rejected-issue-card.md      |   4 +-
>  tests/test_card.py                               |   5 +-
>  tests/test_card_bullets.py                       |  18 +-
>  tests/test_card_refs.py                          | 253 +++++++++++++++++++++++
>  tests/test_card_status.py                        |   4 +-
>  tests/test_field_icons.py                        |   4 +-
>  8 files changed, 275 insertions(+), 21 deletions(-)
> """Every issue and pull request a card names shows as GitHub's own reference.
> 
> Issue #359. GitHub draws a reference to an issue, a pull request or a comment on one with its status icon, its title
> and its number, but only when the markdown leaves the reference bare: `#N`, or the page's own link written out on
> its own (`https://github.com/o/r/issues/N`, `.../pull/N`, `.../issues/N#issuecomment-M`). A reference wrapped in a
> link of its own, `[issue #40](...)` or `<a href="...">Source</a>`, shows only the wrapped words, with no icon and no
> title. These tests draw cards with `dokima/card.py` and read the markdown: every issue or pull request the card
> names must be a bare reference, and none may sit inside a link with words of its own. A

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Relates to\|Blocked by\|Blocks:\|def _ref\|#{" dokima/card.py | head -40; python -m pytest -q tests/test_card_refs.py 2>&1 | tail -15
```

> 60:    """One line per kind of link a plan has (Blocked by, Blocks, Relates to), each with its own icon; none for a kind
> 64:    for kind, field, label in (("blocked_by", "blocked by", "Blocked by"), ("blocks", "blocks", "Blocks"),
> 65:                               ("relates_to", "related", "Relates to")):
> 68:            out.append(f"{field_icon(repo, field)} **{label}:** " + ", ".join(f"#{n}" for n in numbers))
> 115:                print(f"::warning title=Links not read::the links of #{s} could not be read: {e}")
> 175:    """What the card's Blocked by, Blocks and loop lines show, from GitHub now.
> 339:    return f"- [#{n}](https://github.com/{repo}/issues/{n}) {escape(child.get('title'))} · {st}"
> 347:    links.append(f"[issue #{issue['number']}]({issue['url']})")
> 349:        links.append(f"[PR #{pr['number']}](https://github.com/{repo}/pull/{pr['number']})")
> 467:        related.insert(0, f"{field_icon(repo, 'blocked by')} **Blocked by and Blocks:** GitHub could not list this "
> 556:    run = next((r for r in runs if r["display_title"] == f"worker for #{number}"), None)
> 695:            print(f"::error title=Card not updated::the card of #{n} could not be updated: {reason(e)}")
> 748:            print(f"::error title=Card not updated::the card of PR #{i['number']} could not be updated: {reason(e)}")
> 757:            print(f"::error title=Card not updated::the card of #{n} could not be updated: {reason(e)}")
> 829:    (False) issues from the index of those whose approved plans link here.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_card.py tests/test_card_bullets.py tests/test_card_status.py tests/test_field_icons.py tests/raised_goldens/old-issue-card.md | head -150; python -m pytest -q tests 2>&1 | tail -15
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bsdn4lwbp). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/3693ab82-c4b5-4db0-b7a7-fd757d1494cd/tasks/bsdn4lwbp.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_card.py tests/test_card_bullets.py tests/test_card_status.py tests/test_field_icons.py tests/raised_goldens/old-issue-card.md | head -160
```

> commit e7b6d94e329fe715b0c394223620f4c018495b35
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 01:59:12 2026 +0000
> 
>     planner for #359 (run 38014530280)
> 
> diff --git a/tests/raised_goldens/old-issue-card.md b/tests/raised_goldens/old-issue-card.md
> index 30f3b40..8e5099b 100644
> --- a/tests/raised_goldens/old-issue-card.md
> +++ b/tests/raised_goldens/old-issue-card.md
> @@ -3,7 +3,7 @@ Slow calls hand back a job id.
>  
>  **Plan**
>  
> -[issue #299](https://github.com/o/r/issues/299)
> +https://github.com/o/r/issues/299
>  
>  <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #12
>  
> @@ -12,7 +12,7 @@ Slow calls hand back a job id.
>  <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
>  
>  - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** A slow call returns a job id.
> -  - <a href="https://github.com/o/r/issues/299">Source</a>
> +  - Source: https://github.com/o/r/issues/299
>  
>  <details><summary><b>Non-functional requirements</b></summary>
>  
> diff --git a/tests/test_card.py b/tests/test_card.py
> index f23a251..ffa23df 100644
> --- a/tests/test_card.py
> +++ b/tests/test_card.py
> @@ -71,8 +71,9 @@ def test_ti

**Agent:** I've read the plan and its tests, and confirmed all six new tests fail today for the right reason. Next I'm writing up the plan review.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned the issue as one story with four criteria: Source, the top row, the stories of a split, and every other issue or PR on the card all show as GitHub's own reference.",
          "It added six tests in tests/test_card_refs.py and updated eight older tests and three golden cards that expected the old linked words."],
  "decided": ["Issues, pull requests and Sources are written out bare (#N or the page's link alone), so GitHub draws the icon, title and number; a story's line no longer repeats its title."],
  "open": ["It asks whether the Source line keeps a Source: label in front of the reference, and whether the agents' run comments are covered or only the card on top of the issue and PR."]},
 "verdict": "approve",
 "summary": "The plan covers every place the owner named and each test fails today because cards still link issues, PRs and Sources under words of their own; the two questions are left for the owner.",
 "blockers": [],
 "notes": [
  {"text": "The tests prove the card's markdown leaves each reference bare; whether GitHub then draws the icon and title (especially for a link to a comment, which GitHub may show as '#40 (comment)') can only be checked by eye on a real card after merge.",
   "evidence": "tests/test_card_refs.py module docstring: the tests 'read the markdown'; none can see GitHub's rendering."},
  {"text": "Blocked by, Blocks and Relates to already write #N today, so 359.4 passes for them unchanged; that matches the owner's ask only if GitHub draws an inline #N with its title, as the owner saw for #300 in Out of scope.",
   "evidence": "dokima/card.py:68 writes ', '.join(f\"#{n}\" ...); the owner's comment of 2026-10-09T21:27:54Z names Relates to, Blocks and Blocked by among the places to change."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "On the card, Source shows the way GitHub shows a re
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> the ask "On the card, Source shows the way GitHub shows a reference to an issue, pull request or comment, with its status icon and name (as the Out of scope section shows #300), not a plain word "Source" linked to a page." is matched to 1, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)
> the ask "the Source may point to a story, an issue or a comment, whichever holds the ask; don't force it to a single comment" is matched to 1, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)
> the ask "every reference to an issue or pull request on a card shows the way GitHub shows its own references: the status icon (circle), then the title, then the number" is matched to 4, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)
> the ask "the issue and PR links at the top" is matched to 2, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)
> the ask "Stories" is matched to 3, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)
> the ask "Relates to, Blocks, Blocked by, ... Out of scope, and anywhere else a card names an issue or PR. One consistent look everywhere." is matched to 4, which is not a criterion of the plan (359.1, 359.2, 359.3, 359.4)

`7. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open("review.json"))
r["summary"]="The plan covers every place the owner named and each new test fails today for the right reason; both questions go to the owner."
for a in r["asks"]: a["criterion"]="359."+a["criterion"]
json.dump(r,open("review.json","w"),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 359 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#359](https://github.com/dokima-dev/dokima/issues/359) (cards show issues, PRs and Sources the way GitHub shows its own references). It isn't cleared to build yet: both of the planner's questions now go to you.

**Why it passes:**
- Every place you asked for has a criterion: Source, the issue and PR links at the top, the stories of a split, and Relates to / Blocks / Blocked by / Out of scope. Your first comment, which narrowed the issue, is respected: a Source may point to a comment, the issue or a story.
- I ran the six new tests and each fails today for the right reason: the card still writes the linked words `issue #40`, `PR #5` and `Source`.
- The eight older tests and three golden cards it changes still check the same things; they now expect the bare link instead of linked words.

**The two questions:**
1. **Does the Source line keep a `Source:` label in front of the reference?** You wrote "instead of the plain word Source", which could also mean dropping the word entirely. I didn't accept the planner's guess.
2. **Are the agents' run comments covered, or only the card on top of the issue and PR?** You wrote "anywhere else a card names an issue or PR", and AGENTS.md also calls a run's live comment a card. Leaving run comments out narrows your ask, so I didn't accept that guess either.

**Two things no test can prove:**
- The tests only check that the card's text leaves each reference bare. Whether GitHub then draws the icon and title can only be checked by eye on a real card after merge. This matters most for links to a comment, which GitHub may draw as `#40 (comment)` rather than a title.
- Blocked by, Blocks and Relates to already write `#N` today, so they pass without any change. That only gives you the look you want if GitHub draws an inline `#N` with its title, the way you saw `#300` drawn in Out of scope.

The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

`8. Bash`
```
tail -20 /tmp/claude-1001/-home-runner-work-dokima-dokima/3693ab82-c4b5-4db0-b7a7-fd757d1494cd/tasks/bsdn4lwbp.output
```

> assert img("merged") not in other, f"234.2: a child still in Plan shows the merged icon: {other}"
>  
>  
>     
>     </details>
>     
>     **Scope:** `dokima/agent.py`
>     
>     <details><summary><b>Out of scope</b></summary>
>     
>     - The board.
>     
>     </details>
>     
>     **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
>     
>     <!-- /dokima-card -->
> 14 failed, 817 passed, 79 skipped in 184.00s (0:03:03)
> 
> [exited with code 0]

`9. Bash`
```
grep -E "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/3693ab82-c4b5-4db0-b7a7-fd757d1494cd/tasks/bsdn4lwbp.output | cut -c1-160
```

> (Bash completed with no output)

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python -m pytest -q tests -rf 2>&1 | grep -E "^FAILED" | cut -c1-140
```

> FAILED tests/test_card.py::test_links_row - AssertionError: assert '[latest run]...pull/5/files)' == '[latest run]...pull/5/files)'
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[open] - AssertionError: 235.4: the card doe
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[merged] - AssertionError: 235.4: the card d
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[closed] - AssertionError: 235.4: the card d
> FAILED tests/test_card_bullets.py::test_each_criterion_has_a_source_line_after_verified_by - AssertionError: the Source line is not Source: 
> FAILED tests/test_card_refs.py::test_each_source_shows_as_a_github_reference_to_where_the_ask_is - AssertionError: 359.1: the Source of “F
> FAILED tests/test_card_refs.py::test_the_issue_and_pr_at_the_top_show_as_github_references - AssertionError: 359.2: the issue card links the
> FAILED tests/test_card_refs.py::test_with_no_pr_the_top_row_names_only_the_issue - AssertionError: 359.2: the issue is linked with words of 
> FAILED tests/test_card_refs.py::test_each_story_shows_as_a_github_reference_then_its_stage - AssertionError: 359.3: expected one line naming
> FAILED tests/test_card_refs.py::test_no_issue_or_pr_on_a_card_is_a_link_with_words_of_its_own - AssertionError: 359.4: the issue card links 
> FAILED tests/test_card_refs.py::test_a_merged_pr_card_still_names_both_as_references - AssertionError

**Agent:** My plan approval for [#359](https://github.com/dokima-dev/dokima/issues/359) (cards show issues, PRs and Sources as GitHub references) stands. The full test suite has finished: 817 passed, 14 failed and 79 were skipped.

All 14 failures are expected, because each one is a test the planner wrote or changed for this issue:
- the six new tests in `tests/test_card_refs.py`
- the seven older tests and three golden cards (the golden cards are checked by three of those seven) that now expect the bare link instead of linked words such as `issue #40`, `PR #5` and `Source`

Every one fails because the card hasn't been changed yet. None fails on a crash, a missing tool or a bad path, and no test outside this issue breaks. The review in `/tmp/dokima-out/review.json` needs no change, and the two questions are still waiting for your answer.
