# reviewer (plan) for #299

Run: https://github.com/dokima-dev/dokima/actions/runs/37889218505

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (46.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/92e8c837-0693-4986-bf07-738f72192181/tool-results/b7v3yto7a.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  9 05:34 .
> drwxrwxrwt 18 root   root    4096 Oct  9 05:34 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 05:34 in
> -rw-r--r--  1 runner runner 45084 Oct  9 05:34 issue.md
> -rw-r--r--  1 runner runner  2256 Oct  9 05:34 open_blockers.json
> -rw-r--r--  1 runner runner  6086 Oct  9 05:34 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:34 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:34 ..
> -rw-r--r-- 1 runner runner 5244 Oct  9 05:34 01-planner.json
> -rw-r--r-- 1 runner runner 7570 Oct  9 05:34 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6727 Oct  9 05:34 03-planner.json
> # Issue #299: Cards show what was raised and how each earlier raise was answered
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298 -->
> **Backlog**
> 
> [issue #299](https://github.com/dokima-dev/dokima/issues/299)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.co

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md | head -c 20000
```

> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 2</summary>
> 
> **Part of:** #289 Every agent raises things and answers them through the same two fields
> 
> **User story:** The owner reads every judgment an agent raised in one Raised section, sees at a glance what each line is and who must act on it, and on a review card sees what earlier steps raised apart from what this review raises.
> 
> **Context:** Owner's words: the issue body ('Cards show one Raised section, each line with its kind's icon and who it is for') and the comment of 2026-10-09T01:39:55Z (IDs never on a card; the review card shows what earlier steps raised separately from what this review raises; what code detects keeps its own name and icon; no backfill). Today dokima/agent.py details() (387) draws Concerns, What it found, What it raised, Notes and Outside the plan folds, and render() (457) draws blockers, The plan's assumptions, Issues found outside this one and Questions for you, each with an icon from dokima/card.py field_icon(); dokima/icons/ already has question.svg, blocker.svg and issue-found.svg. dokima/card.py reads the planner's questions for the issue card's Next line; the issue asks for the cards to change, so dokima/card.py is in scope. Draw from the raises and answers fields of story 1; records posted before this change are not redrawn (no backfill, criterion 4): their comments stay a

`3. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md | tail -c +20000 | grep -v '^$' | head -400 | cut -c1-1500; echo; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (31.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/92e8c837-0693-4986-bf07-738f72192181/tool-results/brm0745pj.txt
> 
> Preview (first 2KB):
> s an issue. (299.1, https://github.com/dokima-dev/dokima/issues/299)
> - A run that raised nothing shows no Raised section. (299.1, https://github.com/dokima-dev/dokima/issues/299)
> - No card shows a raise's or an answer's ID. (299.2, https://github.com/dokima-dev/dokima/issues/299)
> - A review card shows what earlier steps raised in its own section, apart from what this review raises. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> - Each earlier raise shows the reviewer's answer: done or disagree, and why. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> - An answer given for you on autopilot quotes your words and links where you said them. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> - A review that answered nothing shows no section for earlier raises. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> - A record posted before this change keeps its comment exactly as it is. The issue card still draws it, old fields included, without error, and only newer records draw a Raised section. (299.4, https://github.com/dokima-dev/dokima/issues/299)
> - What code detects keeps its own name, icon and place on the card, exactly as today, and never appears in the Raised section. (299.5, https://github.com/dokima-dev/dokima/issues/299)
> - That is

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/92e8c837-0693-4986-bf07-738f72192181/tool-results/brm0745pj.txt
```

> 1	s an issue. (299.1, https://github.com/dokima-dev/dokima/issues/299)
> 2	- A run that raised nothing shows no Raised section. (299.1, https://github.com/dokima-dev/dokima/issues/299)
> 3	- No card shows a raise's or an answer's ID. (299.2, https://github.com/dokima-dev/dokima/issues/299)
> 4	- A review card shows what earlier steps raised in its own section, apart from what this review raises. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> 5	- Each earlier raise shows the reviewer's answer: done or disagree, and why. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> 6	- An answer given for you on autopilot quotes your words and links where you said them. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> 7	- A review that answered nothing shows no section for earlier raises. (299.3, https://github.com/dokima-dev/dokima/issues/299)
> 8	- A record posted before this change keeps its comment exactly as it is. The issue card still draws it, old fields included, without error, and only newer records draw a Raised section. (299.4, https://github.com/dokima-dev/dokima/issues/299)
> 9	- What code detects keeps its own name, icon and place on the card, exactly as today, and never appears in the Raised section. (299.5, https://github.com/dokima-dev/dokima/issues/299)
> 10	- That is work outside the plan, failing tests, red main, merge conflicts, a rejected hand-back, a workflow file change that needs you and three blocks in a row. (missing, https://github.com/dokima-dev/do

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -50; wc -l tests/test_raised_cards.py; grep -n "def test_\|newest\|waiting" tests/test_raised_cards.py
```

> commit 32d5f3392d5e0de669349a6c89bb94490bb29a8e
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:34:11 2026 +0000
> 
>     planner for #299 (run 37888531909)
> 
>  tests/raised_goldens/failing-tests-issue-card.md |  33 +++++++
>  tests/raised_goldens/merge-failed.md             |  38 ++++++++
>  tests/test_raised_cards.py                       | 114 ++++++++++++++++++++---
>  3 files changed, 170 insertions(+), 15 deletions(-)
> 
> commit 51cf1d924b6922ab3678ce35d2e4d9734968daea
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:01:10 2026 +0000
> 
>     planner for #299 (run 37884628736)
> 
>  tests/raised_goldens/cancelled.md           |  35 ++
>  tests/raised_goldens/clash.md               |  31 ++
>  tests/raised_goldens/not-started.md         |  38 +++
>  tests/raised_goldens/old-issue-card.md      |  33 ++
>  tests/raised_goldens/old-planner.md         | 122 +++++++
>  tests/raised_goldens/old-review.md          | 123 +++++++
>  tests/raised_goldens/old-worker.md          |  78 +++++
>  tests/raised_goldens/rejected-issue-card.md |  33 ++
>  tests/raised_goldens/rejected.md            | 110 ++++++
>  tests/test_raised_cards.py                  | 501 ++++++++++++++++++++++++++++
>  10 files changed, 1104 insertions(+)
> 
> commit e1a21e7925afcc148c291b29387671276d399726
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:34:17 2026 -0500
> 
>     Three kinds of

**Agent:** I'm checking whether the new plan fixes the earlier blocker and follows the owner's /plan answer. Next I'll run the tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 260,300p tests/test_raised_cards.py; sed -n 470,585p tests/test_raised_cards.py; python -m pytest -q tests/test_raised_cards.py 2>&1 | tail -25
```

> Proves 299.1."""
>     record_property("proves", "299.1")
>     for r in (NEW_PLANNER, NEW_WORKER, NEW_REVIEW):
>         quiet = copy.deepcopy(r)
>         quiet["handback"]["raises"] = []
>         quiet["handback"]["answers"] = []
>         body = agent.render(quiet)
>         assert not headings(body, "Raised:"), f"299.1: a {r['role']} run that raised nothing shows a Raised section:\n{body}"
>     assert headings(agent.render(NEW_PLANNER), "Raised:"), "299.1: a planner run with raises shows no Raised section"
> 
> 
> def test_the_issue_card_shows_the_newest_runs_raises_in_one_raised_section(record_property, env):
>     """The issue card lists the newest run's raises in one Raised section.
> 
>     Draws the issue card after a planner run with raises, then after a review with raises, and checks the card has one
>     Raised section with exactly the newest run's raises, each line opening with its kind's icon and saying who it is
>     for; then checks a newest run that raised nothing leaves the card with no Raised section.
> 
>     Proves 299.1."""
>     record_property("proves", "299.1")
>     for recs, raises in (([NEW_PLANNER], [P_QUESTION, P_ISSUE]),
>                          ([NEW_PLANNER, NEW_WORKER, NEW_REVIEW], [R_TO_WORKER, R_TO_PLANNER, R_QUESTION, R_ISSUE])):
>         drawn = card.render(REPO, ISSUE, found_for(recs))
>         assert len(headings(drawn, "Raised:")) == 1, f"299.1: the issue card must have exactly one Raised section:\n{drawn}"
>         items = section(drawn, "Raised:")
>         assert len(item

**Agent:** B1 is fixed. But the new plan ignores the owner's /plan answer, so I'm blocking on that. Writing the hand-back now.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner put the owner's list of what code detects back in criterion 5 word for word, and added a run stopped before its agent and a cancelled run.",
          "The planner added tests that keep the Outside the plan fold, failing tests, the workflow file refusal and three blocks in a row as today and out of Raised."],
  "decided": ["The issue card still shows the raises of the newest run only."],
  "open": ["The owner's answer, to show every raise still waiting for an answer, is not in the plan or its tests."]
 },
 "verdict": "block",
 "summary": "The owner asked the issue card to show every raise still waiting for an answer, but the plan and its test still show only the newest run's raises.",
 "blockers": [
  {"id": "B2", "criterion": "299.1",
   "test": "tests/test_raised_cards.py::test_the_issue_card_shows_the_newest_runs_raises_in_one_raised_section",
   "problem": "The owner answered the plan's first question: 'Show every raise on the issue that is still waiting for an answer, not just the newest run's. Every raise must be answered, so none should drop out of view.' The new plan still asks the same question and still assumes 'The newest run only'. Criterion 1 does not say which raises the issue card shows. The test checks the opposite of what the owner asked: when the newest review raises nothing, it expects no Raised section on the issue card, so the planner's unanswered raises drop out of view.",
   "evidence": "Owner's comment of 2026-10-09T05:25:47Z on https://github.com/dokima-dev/dokima/issues/299. plan.json questions[0].assumption is still 'The newest run only'. tests/test_raised_cards.py:272-293 asserts the card shows 'exactly the newest run's raises' and, at :290-293, that found_for([NEW_PLANNER, quiet review]) shows no Raised section. The module docstring at tests/test_raised_cards.py:15 says 'the issue card shows the raises of the newest record'.",
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> rc=0

`8. Bash`
```
sed -i 's|"summary": "The owner asked the issue card to show every raise still waiting for an answer, but the plan and its test still show only the newest run.s raises."|"summary": "The owner asked the issue card to show every unanswered raise, but the plan and its test still show only the newest run'"'"'s."|' /tmp/dokima-out/review.json && grep '"summary"' /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 299 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> "summary": "The owner asked the issue card to show every unanswered raise, but the plan and its test still show only the newest run's.",
> rc=0

**Agent:** I blocked the plan, because it doesn't do what the owner asked in their `/plan` comment. The review is at `/tmp/dokima-out/review.json`, and both checks pass.

**The earlier blocker (B1) is fixed.** Criterion 5 now has the owner's list of what code detects, word for word. New tests check that "Outside the plan", failing tests, the refusal to merge a workflow file change and the three-blocks to-do all draw as they do today and stay out of Raised.

**New blocker (B2), on criterion 299.1, for the planner to fix.** The owner wrote at 05:25: "Show every raise on the issue that is still waiting for an answer, not just the newest run's." The re-plan ignores that:
- It still asks the same question and still assumes "the newest run only".
- `tests/test_raised_cards.py:272-293` tests the opposite. It expects the issue card to show no Raised section when the newest review raised nothing, so the planner's unanswered raises drop out of view.

The fix is to write the owner's answer into a criterion and rewrite that test:
- Raises nobody has answered stay on the card after a later run that raises nothing.
- A raise leaves the card once it is answered.
- The card shows no Raised section only when every raise has an answer.

**The plan's two questions:**
- **Newest run only:** not accepted. The owner already answered it the other way.
- **A rejected run's raises:** accepted, as in the last review, because it matches the owner's own words.

**Tests:** all 23 tests in the file fail today, each because the Raised section doesn't exist yet. That is the right reason.
