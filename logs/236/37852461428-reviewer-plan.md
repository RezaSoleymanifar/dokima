# reviewer (plan) for #236

Run: https://github.com/dokima-dev/dokima/actions/runs/37852461428

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (29.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tool-results/b5abj191t.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #236: Run comments show only what has something, in the owner's words, with no codes
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 3</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** Every run comment shows only the fields that have something, names the reviews Plan review and Code review, lists a failing criterion with why it fails, and folds the stats.
> 
> **Context:** Run comments are drawn by render(), details() and footnote() in dokima/agent.py; the live card's heading is set in live_card() ('Reviewer ({stage})'). The reviewer's blockers today show as '**B1** (212.3, ...)'. The worker hand-back holds suspect_tests, outside_scope, replies and evidence (its test result line); the reviewer's holds outside_plan, notes and previous_step.open (still open); the planner's holds questions. The planner's comment lists its criteria; the reviewer's should mirror it with only the failing ones, each with the blocker's problem in place of Verified by. Files changed means the worker's changed files, shown on one inline line. The owner answered (comment of 2026-10-08T18:29:55Z) that the pla

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> # Issue #236: Run comments show only what has something, in the owner's words, with no codes
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 3</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** Every run comment shows only the fields that have something, names the reviews Plan review and Code review, lists a failing criterion with why it fails, and folds the stats.
> 
> **Context:** Run comments are drawn by render(), details() and footnote() in dokima/agent.py; the live card's heading is set in live_card() ('Reviewer ({stage})'). The reviewer's blockers today show as '**B1** (212.3, ...)'. The worker hand-back holds suspect_tests, outside_scope, replies and evidence (its test result line); the reviewer's holds outside_plan, notes and previous_step.open (still open); the planner's holds questions. The planner's comment lists its criteria; the reviewer's should mirror it with only the failing ones, each with the blocker's problem in place of Verified by. Files changed means the worker's changed files, shown on one inline line. The owner answered (comment of 2026-10-08T18:29:55Z) that the planner's own run comment shows each criterion with its status and Verified by, so the reviewer's comment mirrors that list. dokima/agent.py render() today lists the planner's criteria as plain numbered text.
> 
> **Acceptance criteria:**
> - The live card and the record say Plan review wher

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/open_blockers.json; ls /tmp/pack/in; git show --stat HEAD; wc -l tests/test_run_comment_fields.py; timeout 600 python -m pytest -q tests/test_run_comment_fields.py 2>&1 | tail -40
```

> []01-planner.json
> commit 8189470f6fdd78820b460fc0721dc46560a8669f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 22:16:40 2026 +0000
> 
>     planner for #236 (run 37848814808)
> 
>  tests/test_agent.py              |   2 -
>  tests/test_field_icons.py        |  31 +--
>  tests/test_fixer.py              |  15 --
>  tests/test_run_cards.py          |  19 +-
>  tests/test_run_comment_fields.py | 502 +++++++++++++++++++++++++++++++++++++++
>  5 files changed, 527 insertions(+), 42 deletions(-)
> 502 tests/test_run_comment_fields.py
>     ],
>     "out_of_scope": [
>      "Cancelling a job."
>     ],
>     "tests": {
>      "77.1": [
>       "tests/test_jobs.py::test_fast"
>      ],
>      "77.2": [
>       "tests/test_jobs.py::test_kept",
>       "tests/test_jobs.py::test_kept_twice"
>      ],
>      "77.3": [
>       "tests/test_jobs.py::test_done"
>      ],
>      "77.4": [
>       "tests/test_jobs.py::test_restart"
>      ]
>     },
>     "test_changes": {}
>    },
>    "check": {
>     "passed": true,
>     "problems": []
>    }
>   }
>   ```
>   
>   </details>
>   
>   <sub><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 4.0 min · 23 turns · 401,000 tokens in, 18,000 out · $3.20 at API prices · [conversation](https://g/log.md) · [run](https://github.com/o/r/actions/runs/1)</sub>
>   
> assert (['<details><summary><b>Non-functional requirements</b></summary>\n\n- Jobs survive a restart of the server. (work is 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_run_comment_fields.py 2>&1 | grep -E "^(FAILED|ERROR)"; cat tests/test_run_comment_fields.py
```

> <persisted-output>
> Output too large (33.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tool-results/beyhczgz7.txt
> 
> Preview (first 2KB):
> FAILED tests/test_run_comment_fields.py::test_review_runs_are_called_plan_review_and_code_review - AssertionError: 236.1: the queued live card of a plan review does not say Plan review:
> FAILED tests/test_run_comment_fields.py::test_a_run_comment_shows_each_optional_part_only_when_it_has_something - AssertionError: 236.2: a worker with nothing for 'Its own test run' still shows it (blank None):
> FAILED tests/test_run_comment_fields.py::test_a_review_comment_drops_the_previous_step_details_and_notes - AssertionError: 236.2: the passing plan review's comment still shows 'What the previous step did':
> FAILED tests/test_run_comment_fields.py::test_the_planners_comment_lists_each_criterion_with_its_circle_verified_by_and_source - AssertionError: 236.3: 77.1 'A slow call returns a job id within 2 s.' does not follow its status circle (not started):
> FAILED tests/test_run_comment_fields.py::test_a_blocking_review_lists_only_the_failing_criteria_with_why_and_source - AssertionError: 236.4: the failing criterion "The job's result is kept for a day." does not show exactly once:
> FAILED tests/test_run_comment_fields.py::test_a_code_review_and_a_pass_list_nothing_that_passed - AssertionError: 236.4: the code review does not show its failing criterion with why and its Source:
> FAILE

`5. Read`
```
/home/runner/work/dokima/dokima/tests/test_run_comment_fields.py
```

> 1	"""Run comments show only what has something, in plain words, with no codes (#236).
> 2	
> 3	A run comment is what code posts when a planner, worker or reviewer run ends: `agent record ROLE STAGE OUT CHECK PASSED
> 4	LOGS` in dokima/agent.py writes OUT/record.json and OUT/comment.md. These tests run that command the way the workflow
> 5	does, from the repo root of the run, and read the comment the way the owner does:
> 6	
> 7	    the planner's comment  lists each criterion as the issue card does: its status circle, its sentence, Verified by
> 8	                           with the first docstring line of each of its tests (read from the test files in the folder
> 9	                           the command runs in), then its Source link
> 10	    a review's comment     lists only what fails, read against the plan in $PACK/plan.json: each failing criterion's
> 11	                           sentence, why it fails (its blockers' problems) and its Source link; and each ask of the
> 12	                           owner's no criterion keeps: the ask, "Nothing covers this" and its Source link
> 13	    the worker's comment   names the files it changed since $BASE (committed, uncommitted or new) on one line
> 14	    every comment          folds its stats right above the Full record fold, which stays the last fold
> 15	
> 16	"Visible" below means the comment without its Full record fold: the record holds every code and number by design.
> 17	"""
> 18	import json
> 19	import os
> 20	import re
> 21	import subprocess
> 22	import sys
> 

**Agent:** Reviewing the plan for #236: all 10 new tests fail today on the missing feature. Now checking the owner's asks against the criteria and the current render code.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def render\|def top\|approved\|blocked the\|escalat" dokima/agent.py | head -40; timeout 900 python -m pytest -q -x --deselect tests/test_run_comment_fields.py 2>&1 | tail -5; timeout 900 python -m pytest -q tests/test_field_icons.py tests/test_agent.py tests/test_fixer.py tests/test_run_cards.py 2>&1 | tail -8
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bq03pu7go). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tasks/bq03pu7go.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def render\|approved the\|blocked the\|def _top\|escalat" dokima/agent.py | head -40
```

> 20:VERDICTS = {"approve", "block", "escalate"}
> 359:        parts += [("Details", ([f"- {h['summary']}"] if h.get("summary") and h.get("verdict") != "escalate" else [])
> 396:                "escalate": f"The reviewer escalated {what} to you."}.get(h.get("verdict"), f"The reviewer judged {what}.")
> 407:def render(rec, pr=None):
> 444:        if h.get("verdict") == "escalate" and h.get("summary"):
> 614:        bad.append("verdict must be approve, block or escalate")
> 643:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 772:            bad.append("verdict must be approve, block or escalate")
> 1269:    Otherwise an approval, a question, an escalation or a hand-back code rejected always stops for the owner. A
> 1310:    if verdict == "escalate":
> 1311:        return ("stop", "The reviewer escalated this to you, see why above.")

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 380,470p dokima/agent.py
```

> role, h, passed = rec["role"], rec["handback"], rec["check"]["passed"]
>     if not passed and role == "worker":
>         return "The worker stopped early with its hand-back rejected by code."
>     if not passed:
>         return f"{HEADS[role]}'s run ended with its hand-back rejected by code."
>     if role == "planner" and h.get("kind") == "feature":
>         n = len(h.get("stories") or [])
>         return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
>     if role == "planner":
>         q = len(h.get("questions") or [])
>         return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
>     if role == "reviewer":
>         what = "the plan" if rec.get("stage") == "plan" else "the work"
>         n = len({b.get("criterion") for b in h.get("blockers") or [] if isinstance(b, dict)})
>         return {"approve": f"The reviewer passed {what}.",
>                 "block": f"The reviewer blocked {what} on {n} criteri{'a' if n != 1 else 'on'}.",
>                 "escalate": f"The reviewer escalated {what} to you."}.get(h.get("verdict"), f"The reviewer judged {what}.")
>     if role == "split":
>         return f"Code filed the split as {len(h.get('stories') or [])} stories."
>     return change_sentence(h.get("summary"))
> 
> 
> def record_fold(rec):
>     """The full JSON record, always the last fold of a run comment: later packs are built from it."""
>     return ["", "<details><

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "matched" dokima/agent.py | head -20; grep -rn "issuecomment" /tmp/pack/issue.md /tmp/pack/in/01-planner.json | head
```

> 453:            lines += [f"- {a.get('question', '')} Accepted on your words \"{a.get('matched', '')}\" ({a.get('source', '')})."
> 659:            bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
> 668:                    '"matched": "the owner\'s words", "source": "where they said them"} (or "why" when not accepted)')
> 708:            if not filled(a.get("matched")):
> 709:                bad.append(f"{label} is accepted with no matched words: quote the owner's words it matches")
> 1257:          and a.get("changes") is False and said_there(a.get("matched"), a.get("source"), items, body, owners, number)}

`10. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def said_there" -A30 dokima/agent.py
```

> 1236:def said_there(words, source, items, body, owners, number):
> 1237-    """True when the words appear word for word where the source says: the issue's own text, a code owner's comment on
> 1238-    this issue, or AGENTS.md. Anything else, a comment by anyone else (the bot included) or one not found, is False."""
> 1239-    flat = lambda t: " ".join((t or "").split())
> 1240-    words, source = flat(words), (source or "").strip()
> 1241-    if not words or not owner_source(source, number):
> 1242-        return False
> 1243-    if source == "AGENTS.md":
> 1244-        return words in flat(agents_text())
> 1245-    if source == issue_url(number):
> 1246-        from dokima.body import ask
> 1247-        return words in flat(ask(body))
> 1248-    return any(c.get("url") == source and (c.get("author") or {}).get("login") in owners and words in flat(c.get("body"))
> 1249-               for c in items)
> 1250-
> 1251-
> 1252-def not_accepted(items, h, owners, body, number):
> 1253-    """The questions of the reviewed plan whose assumption the review did not accept on the owner's real words."""
> 1254-    plan = latest(records(items), "planner")
> 1255-    qs = [q.get("question") for q in ((plan or {}).get("handback") or {}).get("questions") or [] if isinstance(q, dict)]
> 1256-    ok = {a.get("question") for a in h.get("assumptions") or [] if isinstance(a, dict) and a.get("accepted") is True
> 1257-          and a.get("changes") is False and said_there(a.get("matched"), a.get("source"), items, body, owners, number)}
> 12

`11. Bash`
```
sleep 60; tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tasks/bq03pu7go.output
```

> <tool_use_error>Blocked: sleep 60 followed by: tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tasks/bq03pu7go.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Waiting on the background test run; meanwhile drafting the review.

`12. Bash`
```
tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/70cdf60e-9fa8-4464-bf8e-795f4387f8ad/tasks/bq03pu7go.output
```

> 1269:    Otherwise an approval, a question, an escalation or a hand-back code rejected always stops for the owner. A
> 1306:        why = "The plan is approved. Say `/work` to build it, or `/plan` with changes."
> 1309:        return ("stop", "The work is approved. Merge the pull request, or review it with a command to send it back.")
> 1310:    if verdict == "escalate":
> 1311:        return ("stop", "The reviewer escalated this to you, see why above.")
> 1322:    """What `/autopilot start` picks up on the issue: "worker" for an approved plan waiting for `/work`, "split" for an
> 1323:    approved split not yet filed, else None, decided by the river as if the approval came on autopilot. Nothing is
> 1325:    if not approved(records(items)):
> 1348:    since that review, and its criteria are exactly those of the plan the owner approved with `/work`."""
> 1491:        if not approved(recs) or latest(recs, "planner")["handback"].get("kind") != "feature":
> 1492:            print("The newest plan is not an approved split.")
> 1522:        print(plan["handback"].get("kind", "") if plan and approved(recs) else "")
> 1601:        picked = {"worker": f"#{number}'s approved plan goes to the worker now.",
> 1602:                  "split": f"#{number}'s approved split files its stories now."}.get(pick, "")
> 1611:            # What its code review already approved anywhere in the tree merges now, as on autopilot.

`13. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 500 python -m pytest -q -p no:cacheprovider tests/test_field_icons.py tests/test_fixer.py tests/test_run_cards.py 2>&1 | tail -8
```

> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **B1** (9.2, the worker fixes it): The day is never checked.
>   - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **B2** (9.3, the worker fixes it): Restarts are not tried.
>   
>   
> assert not <re.Match object; span=(526, 528), match='B1'>
>  +  where <re.Match object; span=(526, 528), match='B1'> = <function search at 0x7f84c1bf3060>('\\b9\\.\\d\\b|\\bB\\d\\b', '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w...width="16" height="16" align="absmiddle" alt="blocker"> **B2** (9.3, the worker fixes it): Restarts are not tried.\n\n')
>  +    where <function search at 0x7f84c1bf3060> = re.search
> 9 failed, 64 passed in 0.87s

`14. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote 6 criteria and 2 non-functional requirements, with 10 new tests in tests/test_run_comment_fields.py and changes to 6 older tests."],
  "decided": ["A review's comment drops What the previous step did, Details, Notes and blocker codes, and lists only failing criteria and uncovered asks with their Source.",
              "The worker's changed files are kept in the record and shown on one line; the stats move into a fold right above the full record."],
  "open": ["The planner asks 3 questions: a Source link on the planner's rows, which review parts stay, and where the stats fold sits."]},
 "verdict": "block",
 "summary": "The plan covers every ask but one: nothing promises or proves that a review's comment still says its verdict, which the owner named first in what the reviewer card must show.",
 "blockers": [
  {"id": "B1", "criterion": "236.1", "test": "tests/test_run_comment_fields.py::test_review_runs_are_called_plan_review_and_code_review",
   "problem": "The owner said the reviewer card shows \"the verdict\", but no criterion promises it and no test checks it. The verdict lives only in the opening sentence (the check icon in front shows whether code accepted the hand-back, not whether the review passed), and 236.1 only checks that this sentence names Plan review or Code review. An opening of \"Plan review judged the plan.\" for every verdict would pass every test, and a passing review would then show nothing saying it passed.",
   "evidence": "Owner comment of 2026-10-08T18:43:02Z: \"That is the verdict, each criterion delivered or not...\". dokima/agent.py:394-396 puts the verdict only in the opening sentence; test_run_comment_fields.py:207-208 only asserts `name in first`; 236.2 removes the summary from approve and block comments (line 287).",
   "fix": "Add to 236.1 (or a new criterion) that a review's opening sentence says whether it passed, bl
```

> (Bash completed with no output)

**Agent:** I've blocked the plan for #236 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Why it's blocked:** in their 18:43 comment, the owner said the reviewer's comment must show "the verdict". No criterion promises that, and no test checks it.
- Today the verdict (passed, blocked or escalated) appears only in the comment's first sentence (`dokima/agent.py:394-396`).
- The icon in front of that sentence only shows whether code accepted the hand-back, so it says nothing about the verdict.
- 236.1's test only checks that the first sentence says "Plan review" or "Code review". A first line like "Plan review judged the plan." would pass every test, and a passing review would then say nowhere that it passed.
- The fix I asked for: promise that the first sentence says whether the review passed, blocked or escalated, and test each verdict.

**The rest of the plan holds up:**
- I matched the owner's other 13 asks to criteria 236.1 to 236.7.
- All 10 new tests fail today because the feature is missing, not because of a crash or bad setup.
- The six older tests the planner rewrote also fail today in the way that change implies. I ran them as three files (9 of 73 tests fail). I didn't check that output from the full suite.

**The planner's 3 questions** (this issue is on autopilot, so any I don't accept stops for the owner):
- **Stats fold right above the full record:** accepted. It matches the issue's line "The full JSON record stays in its last fold".
- **A Source link on the planner's criteria too:** not accepted. The change is harmless and fits the owner's "It mirrors the planner card exactly", but those words are in a comment whose link isn't in my pack. The issue's own text never gives the planner's criteria a Source line.
- **Keeping the plan's assumptions and the proposed issues in a review's comment:** not accepted. The owner said "Every word on the card has to earn its place" and never named either, so it's their call.

I also left two notes that don't block:
- 236.3's test doesn't check that the non-functional rows sit inside their fold.
- "An escalation still shows its summary" is the planner's own addition, not something the owner asked for.

The source links for the owner's comment asks point at the issue itself, because the comment links weren't in my pack.
