# reviewer (plan) for #251

Run: https://github.com/dokima-dev/dokima/actions/runs/37853555482

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  8 22:27 .
> drwxrwxrwt 18 root   root   4096 Oct  8 22:27 ..
> drwxr-xr-x  2 runner runner 4096 Oct  8 22:27 in
> -rw-r--r--  1 runner runner 9151 Oct  8 22:27 issue.md
> -rw-r--r--  1 runner runner    2 Oct  8 22:27 open_blockers.json
> -rw-r--r--  1 runner runner 2531 Oct  8 22:27 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  8 22:27 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 22:27 ..
> -rw-r--r-- 1 runner runner 3151 Oct  8 22:27 01-planner.json
> # Issue #251: The issue card and the planner's run comment show the links, each kind with its own icon
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #231, story 2</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** The owner sees which issues this one is blocked by, blocks and relates to, on the card at the top of the issue and its pull request and on the planner's run comment, each kind with its own icon.
> 
> **Context:** The owner answered round one's question on #231: both cards show the links, so the planner's run comment mirrors the issue card. The issue card is drawn by card.render() in dokima/card.py; the run comment by render() in dokima/agent.py, whose long parts are folds drawn by the same code as the issue card (#228). Round one's tests on branch try/issue-231 (tests/test_issue_links.py, criterion 231.4: test_the_card_shows_each_kind_of_link_with_its_own_icon

`2. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima/icons; grep -n "FIELD_ICONS\|ICONS\b\|blocked-by\|related\|def render\|def _icon\|links" dokima/card.py | head -60; git show --stat HEAD | head; cat tests/test_link_lines.py
```

> acceptance-criterion.svg
> autopilot.svg
> blocked-by.svg
> blocker.svg
> blocks.svg
> cancelled.svg
> code-review.svg
> failed.svg
> files-changed.svg
> issue-found.svg
> merged.svg
> needs-you.svg
> none.svg
> note.svg
> outside-the-plan.svg
> owner-approval.svg
> passed.svg
> plan-review.svg
> planner.svg
> question.svg
> queued.svg
> related.svg
> running.svg
> stats.svg
> still-open.svg
> verified-by.svg
> worker.svg
> 36:FIELD_ICONS = {"planner": "planner", "worker": "worker", "plan review": "plan-review", "code review": "code-review",
> 41:               "outside the plan": "outside-the-plan", "issue found": "issue-found", "related": "related",
> 42:               "blocked by": "blocked-by", "blocks": "blocks", "stats": "stats"}
> 54:    return icon(repo, FIELD_ICONS[field], alt=field)
> 166:def links_row(repo, issue, pr, worker, check_runs, page):
> 167:    """The links that matter, minus a link to the page the card is on ("issue" or "pr")."""
> 168:    links = []
> 170:        links.append(f"[latest run]({worker['html_url']})")
> 172:        links.append(f"[issue #{issue['number']}]({issue['url']})")
> 174:        links.append(f"[PR #{pr['number']}](https://github.com/{repo}/pull/{pr['number']})")
> 176:        links.append(f"{field_icon(repo, 'files changed')} [files changed](https://github.com/{repo}/pull/{pr['number']}/files)")
> 177:    return " · ".join(links)
> 228:def render(repo, issue, found, page="issue"):
> 241:    links = links_row(repo, issue, pr, worker, check_runs, page)
> 242:    if links:
> 243:        lines += [links, ""]
> commit 26

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_link_lines.py 2>&1 | grep -E "Error|assert|passed|failed" | head -30; sed -n 30,60p dokima/card.py; git log --oneline -3 -- dokima/icons/blocks.svg; git show 4ff0278 --stat | head -30
```

> assert len(files) == 3, f"251.1: the three kinds of link share icons: {files}"
> >       assert len(lines) == len(shown), \
> E       AssertionError: 251.1: the issue card of a user_story shows 0 link lines, not one each for ['blocked_by', 'blocks', 'relates_to']:
> E       assert 0 == 3
> tests/test_link_lines.py:103: AssertionError
> >       assert len(lines) == len(shown), \
> E       AssertionError: 251.1: the issue card of a plan with only blocks shows 0 link lines, not one each for ['blocks']:
> E       assert 0 == 1
> tests/test_link_lines.py:103: AssertionError
> >       assert len(lines) == len(shown), \
> E       AssertionError: 251.1: the issue card after a re-plan shows 0 link lines, not one each for ['relates_to']:
> E       assert 0 == 1
> tests/test_link_lines.py:103: AssertionError
> text = '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...· 1.0 min · 3 turns · 10 tokens in, 5 out · $0.10 at API prices · [run](https://github.com/o/r/actions/runs/1)</sub>\n'
> >       assert len(lines) == len(shown), \
> E       AssertionError: 251.2: the planner's run comment for a user_story shows 0 link lines, not one each for ['blocked_by', 'blocks', 'relates_to']:
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="plann

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned two criteria: the issue and pull request card show one line per kind of link with its own icon (251.1), and the planner's run comment shows the same lines outside its folds (251.2).",
          "Wrote five tests in tests/test_link_lines.py; all five fail today because no card or run comment draws link lines."],
  "decided": ["Reuses blocked-by.svg, blocks.svg and related.svg, added by #234, instead of adding three new icons.",
              "Leaves links off a rejected planner run's comment."],
  "open": []},
 "verdict": "block",
 "summary": "The plan and its tests are sound, but the owner's \"none of them a verdict or run icon\" is not in any criterion or test, so a link line drawn with the passed or running icon would still pass.",
 "blockers": [{"id": "B1", "criterion": "251.1",
   "test": "tests/test_link_lines.py::test_the_issue_card_shows_each_kind_of_link_on_its_own_line_with_its_own_icon",
   "problem": "The issue asks for link icons that are \"none of them a verdict or run icon\". Criterion 251.1 only says \"a different icon from the fixed icon table\", and that table also holds passed, failed, running and the other verdict and run icons. The test only checks that the three kinds use three different files from card.FIELD_ICONS. Since dokima/card.py is in scope, a worker could map \"related\" to \"passed\" in FIELD_ICONS and every test would still pass.",
   "evidence": "Issue #251 criterion 1: \"three new SVG icons in dokima/icons, none of them a verdict or run icon\". tests/test_link_lines.py:121-122 asserts only len({card.FIELD_ICONS[f] ...}) == 3; img() at line 46 reads the icon file from FIELD_ICONS, so changing the map changes what the test expects.",
   "fix": "Add \"none of them a verdict or run icon\" to 251.1. In the test, assert that the three kinds draw exactly blocked-by.svg, blocks.svg and related.svg, and that none of them is a verdict or
```

> rc=0

**Agent:** I blocked the plan for #251 on one point. The review is saved to `/tmp/dokima-out/review.json`, and it passes both the review check and the round check.

**What the planner did:** It planned two criteria:
- **251.1:** the card on the issue and on its pull request shows one line per kind of link (Blocked by, Blocks, Relates to), each with its own icon.
- **251.2:** the planner's run comment shows those same lines, outside its folds.

It wrote five tests in `tests/test_link_lines.py`. I ran them and all five fail today for the right reason: nothing draws link lines yet. It also chose to reuse the three link icons #234 already added (`blocked-by.svg`, `blocks.svg`, `related.svg`) instead of adding three new files. That fits what the owner asked for, so I didn't block on it.

**Blocker B1 (for the planner):** the owner said the icons must be "none of them a verdict or run icon", and no criterion or test keeps that. Criterion 251.1 only asks for "a different icon from the fixed icon table", and that table also holds icons like passed and failed. The test only checks that the three kinds use three different icon files. Because `dokima/card.py` is in the work's scope, the worker could point "related" at the passed icon and every test would still pass. The fix is to add those words to 251.1 and have the test check that the three kinds draw exactly those three files, and that none of them is a verdict or run icon.

**Notes (not blocking):**
- The rule that an older plan with no links field "draws as it does today" is only tested by comparing it with a plan whose links are all empty. If both picked up the same new extra line, such as a bare "Links:" heading, the test would still pass.
- I listed five asks from the owner's words: four map to a criterion and the icon one is marked missing. The plan has no questions to judge.
