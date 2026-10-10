# reviewer (plan) for #452

Run: https://github.com/dokima-dev/dokima/actions/runs/38085074101

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat plan.json; cat open_blockers.json
```

> # Issue #452: The issue card drops its link to itself, and a PR closes its issue by the issue's full address
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [453], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/452
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #453
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #416, story 1</summary>
> 
> **Part of:** #416 Card links show as GitHub's own references: no self-link on the issue, full address after Closes
> 
> **User story:** On the issue's own page the card no longer links to that same issue, and at the bottom of a PR the closing line shows the issue's title and state.
> 
> **Context:** The first plan of #416 (run 38063764349) worked this out and was rejected only because that run wrote outside tests/. Its findings stand: the top row is drawn by `links_row` in `dokima/card.py`, the same for both pages; `pr_body` copies the first `CLOSES` match (`Closes #N`) to the end of the PR's description; `dokima/agent.py` reads which issue a PR was built for from that line when its branch does not say; `dokima/scan.py` compares each card with the one Dokima draws now, so it must expect the issue's card without its own link and the PR's with it. The owner tes

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -60; cat tests/test_card_self_link.py; ls tests | grep -i render; cat tests/record_rendering.py 2>/dev/null | head -80
```

> commit 49f168a73b822d0e3b953eb85fcc3f8931348e57
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 20:46:30 2026 +0000
> 
>     planner for #452 (run 38083227252)
> 
>  tests/card_player.py                             |   8 +
>  tests/github_rendering.json                      |  17 ++
>  tests/raised_goldens/failing-tests-issue-card.md |   2 +-
>  tests/raised_goldens/old-issue-card.md           |   2 -
>  tests/raised_goldens/rejected-issue-card.md      |   2 -
>  tests/record_rendering.py                        |  43 +++
>  tests/test_card.py                               |  13 +-
>  tests/test_card_bullets.py                       |  17 +-
>  tests/test_card_folds.py                         |  45 +--
>  tests/test_card_merge.py                         |  17 +-
>  tests/test_card_records.py                       |   6 +-
>  tests/test_card_refs.py                          |  25 +-
>  tests/test_card_self_link.py                     | 367 +++++++++++++++++++++++
>  tests/test_card_sweep.py                         |  15 +-
>  tests/test_scan.py                               |  14 +-
>  15 files changed, 530 insertions(+), 63 deletions(-)
> """The issue card drops its self-link; a PR closes its issue by full address.
> 
> Issue #452, story 1 of #416. On the issue's own page GitHub shortens a link to that same page to a bare #N, and it
> adds nothing there, so the issue's card leaves it out of its top row; the PR's card keeps it. At the bottom of a PR,
> `Closes #N` shows

`3. Bash`
```
cd /home/runner/work/dokima/dokima; head -c 3000 tests/github_rendering.json; echo; python3 -c "
import json;d=json.load(open('tests/github_rendering.json'));print(type(d), len(d)); print(list(d)[:5] if isinstance(d,dict) else d[0].keys())"; timeout 600 pytest -q tests/test_card_self_link.py 2>&1 | tail -40
```

> [
>  {
>   "name": "issue top row",
>   "text": "[latest run](https://github.com/dokima-dev/dokima/actions/runs/38083227252) · https://github.com/dokima-dev/dokima/pull/448 · <img src=\"https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg\" width=\"16\" height=\"16\" align=\"absmiddle\" alt=\"files changed\"> [files changed](https://github.com/dokima-dev/dokima/pull/448/files)",
>   "html": "<p dir=\"auto\"><a href=\"https://github.com/dokima-dev/dokima/actions/runs/38083227252\">latest run</a> · <a class=\"issue-link js-issue-link\" data-error-text=\"Failed to load title\" data-id=\"5794308892\" data-permission-text=\"Title is private\" data-url=\"https://github.com/dokima-dev/dokima/issues/448\" data-hovercard-type=\"pull_request\" data-hovercard-url=\"/dokima-dev/dokima/pull/448/hovercard\" href=\"https://github.com/dokima-dev/dokima/pull/448\">#448</a> · <a target=\"_blank\" rel=\"noopener noreferrer nofollow\" href=\"https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg\"><img src=\"https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg\" width=\"16\" height=\"16\" align=\"absmiddle\" alt=\"files changed\" style=\"max-width: 100%; height: auto; max-height: 16px;; aspect-ratio: 16 / 16; background-color: var(--bgColor-muted); border-radius: 6px\" class=\"js-gh-image-fallback\"></a> <a href=\"https://github.com/dokima-dev/dokima/pull/448/files\">files changed</a></p>"
>  },
>  {
>   "na

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 pytest -q tests/test_card_self_link.py 2>&1 | grep -E "^(FAILED|E )" | head -30; grep -n "def render\|def pr_body\|def links_row\|CLOSES" dokima/card.py | head; grep -n "def issue_of_pr" -A15 dokima/agent.py; grep -n "def issue_of" -A15 dokima/board.py
```

> E       AssertionError: 452.1: the issue card's top row still links issue #40 itself: [latest run](https://github.com/o/r/actions/runs/1) · https://github.com/o/r/issues/40 · https://github.com/o/r/pull/5 · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/o/r/pull/5/files)
> E       assert ('https://git.../r/issues/40' not in '[latest run...ull/5/files)'
> E         
> E         'https://github.com/o/r/issues/40' is contained here:
> E           runs/1) · https://github.com/o/r/issues/40 · https://github.com/o/r/pull/5 · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/o/r/pull/5/files)
> E         ?           ++++++++++++++++++++++++++++++++)
> E           AssertionError: 452.1: the saved issue card's top row links issue #40 itself: [latest run](https://github.com/o/r/actions/runs/1) · https://github.com/o/r/issues/40 · https://github.com/o/r/pull/5 · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/o/r/pull/5/files)
> E           assert (not True)
> E            +  where True = bare('[latest run](https://github.com/o/r/actions/runs/1) · https://github.com/o/r/issues/40 · https://github.com/o/r/pull

`5. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 pytest -q -x -n auto 2>/dev/null | tail -3 || true; timeout 900 pytest -q 2>&1 | grep -E "^FAILED|passed|failed" | sed 's/ - .*//' | head -60
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bvimu5vxs). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bvimu5vxs.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, check the planner's diff to old tests and the stub-pass question for 452.2.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 -- tests/test_card_refs.py tests/test_card_folds.py tests/card_player.py tests/raised_goldens | head -200
```

> diff --git a/tests/card_player.py b/tests/card_player.py
> index 7b24463..44d5583 100644
> --- a/tests/card_player.py
> +++ b/tests/card_player.py
> @@ -438,6 +438,14 @@ def card_of(text):
>      return m.group(0) if m else None
>  
>  
> +def without_issue_link(text, n):
> +    """The PR's card with its link back to issue n taken out of its top row.
> +
> +    That is the card the issue itself shows since #452."""
> +    url = re.escape(f"https://github.com/o/r/issues/{n}")
> +    return re.sub(rf"^{url} · | · {url}(?= · |$)", "", text or "", count=1, flags=re.M)
> +
> +
>  def stage_of(text):
>      """The stage a card's status line shows (Backlog, Plan, Work, Review or Merged), or None."""
>      for line in (card_of(text) or "").splitlines():
> diff --git a/tests/raised_goldens/failing-tests-issue-card.md b/tests/raised_goldens/failing-tests-issue-card.md
> index 25f86b6..8b88c55 100644
> --- a/tests/raised_goldens/failing-tests-issue-card.md
> +++ b/tests/raised_goldens/failing-tests-issue-card.md
> @@ -3,7 +3,7 @@ Slow calls hand back a job id.
>  
>  **Review** · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See why not every check passed
>  
> -https://github.com/o/r/issues/299 · https://github.com/o/r/pull/5 · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/o/r/pull/5/files)
> +https://gi

`7. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bvimu5vxs.output | tail -60
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bvimu5vxs.output tail -60. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** I'll wait for the background suite to finish. Meanwhile, drafting the hand-back.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Wrote six criteria: the issue card drops its own link, the PR card keeps it, the PR closes by the issue's full address, a check on GitHub's recorded rendering, reading a PR's issue from either closing line, and the board scan.",
   "Wrote tests/test_card_self_link.py, recorded GitHub's rendering of three texts in tests/github_rendering.json with tests/record_rendering.py to refresh it, and updated 26 older tests that compared the two cards as identical."
  ],
  "decided": [
   "The check on GitHub's rendering uses answers recorded in the repo, not a call to GitHub in CI.",
   "Only the card's top row drops the issue's own link; a Source pointing at the issue is left to #453."
  ],
  "open": [
   "Three questions for the owner: whether GitHub drawing its own reference stands for the title and state icon, recorded answers versus calling GitHub, and whether Sources count as a link to itself."
  ]
 },
 "verdict": "approve",
 "summary": "The plan covers every ask of the story with tests that fail today for the right reason; its three questions wait for the owner.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "On the issue's own page, the card's top row no longer links to that issue; the latest run, the PR and its files changed stay.", "source": "https://github.com/dokima-dev/dokima/issues/452", "criterion": "452.1"},
  {"ask": "On the PR, the card's top row still shows the issue's link, and the rest of the card is the same as on the issue.", "source": "https://github.com/dokima-dev/dokima/issues/452", "criterion": "452.2"},
  {"ask": "The PR's description ends with \"Closes\" and the issue's full address, and every redraw keeps it. It is the description's only closing reference, so GitHub lists that issue as the one the PR closes.", "source": "https://github.com/dokima-dev/dokima/issues/452", "criterion": "452.3"},
  {"ask": "As GitHub renders them, the PR's c
```

> (Bash completed with no output)

`9. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`10. Bash`
```
F=/tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bvimu5vxs.output; until grep -qE "passed|failed|error" $F; do sleep 3; done; tail -60 $F
```

> Command running in background with ID: bfrydlrtc. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bfrydlrtc.output. You will be notified when it completes. To check interim output, use Read on that file path.

**Agent:** I've drafted my plan review approving the plan for [#452](https://github.com/dokima-dev/dokima/issues/452) (the issue card drops its link to itself, and a PR closes its issue by the issue's full address). It passes both hand-back checks. I'm still waiting on the full test suite before I treat it as final.

**What I checked:**
- **The new tests:** I ran `tests/test_card_self_link.py`. All 9 of its tests fail today because the feature is missing, not because of a crash or a bad path:
  - The issue card still links to itself.
  - The issue and PR cards are still identical.
  - The PR still ends with `Closes #40`.
  - Dokima can't yet read an issue from a full-address closing line.
  - The scan still expects the issue's card to link to itself.
- **Every ask is covered:** each of the story's four criteria and two non-functional asks maps to one criterion (452.1 to 452.6).
- **The tests would catch wrong work:**
  - The PR test checks that the two cards differ in exactly one line, the top row.
  - The closing-line test checks the description holds exactly one closing reference.
  - The rendering test fails on any text that wasn't recorded word for word.
- **The older tests the plan changed** (the ones that treated the two cards as identical) were changed for the reasons the planner gave.

**The planner's three questions wait for you.** The issue is on autopilot, so I could answer them for you, but only with your own words as proof. The story's text is quoted from the approved plan of [#416](https://github.com/dokima-dev/dokima/issues/416) (card links show as GitHub's own references), not written by you, so I left all three:
1. GitHub's rendering doesn't include the title or state icon. GitHub's page adds them later in the browser. So the check can only prove that GitHub draws the closing line as its own link to the issue. Is that enough?
2. Should the rendering check use GitHub's answers saved in the repo, as the plan assumes, or call GitHub during CI?
3. Should "no link to itself" also cover a criterion's Source that points at the issue? The plan leaves that to [#453](https://github.com/dokima-dev/dokima/issues/453) (writing out the card's other references).

I raised no blockers and no outside issues.

The review is in `/tmp/dokima-out/review.json`. If the full suite turns up a failing test the plan didn't mention, I'll revise the review before it goes out.

`11. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/25af3a66-442f-4ca0-bce4-4ceeb8f3065f/tasks/bvimu5vxs.output
```

> Runs the card for an issue whose code review passed, with its PR open, merged and closed, and checks the card
>         own card leaves out the link to itself, #452), both link to PR #5, and both show the code review passed.
> E        
> E        
> E         **Definition of Done:** <a href="https://github.com/o/r/actions/runs/2/job/4"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <a href="https://github.com/o/r/actions/runs/14"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> E        
> E        
> E         **Definition of Done:** <a href="https://github.com/o/r/actions/runs/2/job/4"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <a href="https://github.com/o/r/actions/runs/14"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passe

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 590 pytest -q -p no:cacheprovider -rf 2>&1 | grep -E "^FAILED|^ERROR|[0-9]+ (passed|failed)" | sed 's/ - .*//'
```

> FAILED tests/test_card.py::test_links_row
> FAILED tests/test_card.py::test_same_card_on_issue_and_pr_and_only_icons_change
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[open]
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[merged]
> FAILED tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages[closed]
> FAILED tests/test_card_folds.py::test_scope_shows_every_file_as_code_on_one_line
> FAILED tests/test_card_folds.py::test_out_of_scope_sits_in_a_closed_fold
> FAILED tests/test_card_folds.py::test_non_functional_requirements_sit_in_a_closed_fold_beside_out_of_scope
> FAILED tests/test_card_folds.py::test_the_pr_card_carries_the_same_original_issue_fold
> FAILED tests/test_card_folds.py::test_an_old_pr_card_gains_the_fold_on_its_next_redraw
> FAILED tests/test_card_folds.py::test_the_owners_closing_words_on_the_pr_close_nothing
> FAILED tests/test_card_merge.py::test_merging_a_pr_redraws_its_card_and_its_issues_card
> FAILED tests/test_card_records.py::test_the_issue_and_its_pr_show_the_same_card
> FAILED tests/test_card_refs.py::test_the_issue_and_pr_at_the_top_show_as_github_references
> FAILED tests/test_card_refs.py::test_with_no_pr_the_top_row_names_only_the_issue
> FAILED tests/test_card_self_link.py::test_the_issue_cards_top_row_leaves_out_its_own_link
> FAILED tests/test_card_self_link.py::test_drawing_the_card_saves_the_issue_card_without_its_own_link
> FAILED tests

**Agent:** I've approved the plan for [#452](https://github.com/dokima-dev/dokima/issues/452) (the issue card drops its link to itself, and a PR closes its issue by the issue's full address). The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Test results on the plan's branch:** 893 tests pass and 36 fail. Every failure is either one of the 9 new tests or an older test the planner said it had changed. Each one fails because the feature doesn't exist yet, not because of a crash or a bad path. No other test broke.

**What I checked:**
- **Every ask has a criterion.** The story's four acceptance criteria and its two non-functional asks each map to one criterion, 452.1 to 452.6.
- **The tests would catch wrong work:**
  - The issue card and the PR card must differ in exactly one line: the top row, where the PR's card adds the issue's link.
  - The PR's description must hold exactly one closing reference, its last line.
  - The rendering check fails for any text whose GitHub rendering wasn't saved word for word.
  - The board scan must name a card drawn the old way.

**The planner's three questions are left for you to answer.** The issue is on autopilot, but I may answer for you only with your own words as proof. The story is quoted from the approved plan of [#416](https://github.com/dokima-dev/dokima/issues/416) (card links show as GitHub's own references), not your own writing, so I answered none of them:
1. GitHub's rendering doesn't include the title or state icon; GitHub's page adds them in the browser. So the check can only prove that GitHub draws the closing line as its own link to the issue. Is that enough to stand for "shows the title and state icon"?
2. Should the rendering check use GitHub's answers saved in the repo, as the plan assumes, or call GitHub during CI?
3. Should "the issue card shows no link to itself" also cover a criterion's Source that points at the issue? The plan leaves that to [#453](https://github.com/dokima-dev/dokima/issues/453) (the card's other references).

I raised no blockers and no issues outside this one.
