# reviewer (plan) for #236

Run: https://github.com/dokima-dev/dokima/actions/runs/37862083000

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (67.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a0d101c0-ba98-4adf-89da-e3dd714a733e/tool-results/bjhpg0ahu.txt
> 
> Preview (first 2KB):
> .:
> total 88
> drwxr-xr-x  3 runner runner  4096 Oct  8 23:55 .
> drwxrwxrwt 18 root   root    4096 Oct  8 23:55 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 23:55 in
> -rw-r--r--  1 runner runner 57648 Oct  8 23:55 issue.md
> -rw-r--r--  1 runner runner  1235 Oct  8 23:55 open_blockers.json
> -rw-r--r--  1 runner runner  9376 Oct  8 23:55 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner  4096 Oct  8 23:55 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 23:55 ..
> -rw-r--r-- 1 runner runner  8734 Oct  8 23:55 01-planner.json
> -rw-r--r-- 1 runner runner  7692 Oct  8 23:55 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10041 Oct  8 23:55 03-planner.json
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
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; head -c 20000 issue.md
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
cd /tmp/pack; cat plan.json; cat open_blockers.json
```

> {
>  "kind": "user_story",
>  "summary": "Run comments show each field only when it has something, in one style for every agent, with reviews giving their verdict and failures in plain words.",
>  "user_story": "Every run comment shows only what the owner needs, each field drawn the same way by every agent: a plan's criteria with proof and source, a review's verdict and failures in plain words, the worker's files on one line, and the stats folded away.",
>  "acceptance_criteria": [
>   {
>    "text": "A review run is called Plan review or Code review on its live card and run comment, never Reviewer (plan), Reviewer (pr) or The reviewer.",
>    "source": "https://github.com/dokima-dev/dokima/issues/236"
>   },
>   {
>    "text": "Each field of a run comment shows only when it has something, and a field two agents share looks the same from both. The optional fields are the worker's suspect tests, changes outside scope, replies to blockers and test result line, a review's changes outside the plan, questions and issues found, and the planner's questions. Nothing shows as a blank heading or an empty fold. The worker's changes outside scope and a review's changes outside the plan are drawn as one Outside the plan fold with the same icon, label and lines. A review's questions are drawn exactly like the planner's Questions for you. A review's comment no longer shows What the previous step did, Details or Notes; an escalation still shows its summary, the reason it reaches the owner.",
>    "source": "https

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; 
```

> 29:### RezaSoleymanifar on issue #236 (2026-10-08T18:43:02Z)
> 33:### RezaSoleymanifar on issue #236 (2026-10-08T19:14:16Z)
> 40:### dokima-runtime on issue #236 (2026-10-08T21:43:57Z)
> 44:### dokima-runtime on issue #236 (2026-10-08T21:44:08Z)
> 252:### dokima-runtime on issue #236 (2026-10-08T22:16:49Z)
> 473:### RezaSoleymanifar on issue #236 (2026-10-08T23:45:03Z)
> 479:### dokima-runtime on issue #236 (2026-10-08T23:45:21Z)
> 703:### dokima-runtime on issue #236 (2026-10-08T23:55:25Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 252,300p issue.md; sed -n 470,480p issue.md; sed -n 703,760p issue.md; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d['handback'],indent=1)[:5000])"
```

> ### dokima-runtime on issue #236 (2026-10-08T22:16:49Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer blocked the plan on 1 criterion.
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **B1** (236.1, the planner fixes it): The owner said the reviewer card shows "the verdict", but no criterion promises it and no test checks it. The verdict lives only in the opening sentence (the check icon in front shows whether code accepted the hand-back, not whether the review passed), and 236.1 only checks that this sentence names Plan review or Code review. An opening of "Plan review judged the plan." for every verdict would pass every test, and a passing review would then show nothing saying it passed.
> 
> **The plan's assumptions:**
> - Should the planner's criterion rows end with a Source link too, as the reviewer's rows do? Not accepted: It changes neither how the system works nor its cost, and fits the owner's "It mirrors the planner card exactly", but those words are in a comment whose link is not in the pack, so they cannot be checked; the issue's own text never gives the planner's rows a Source l

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; wc -l tests/test_run_comment_fields.py; grep -rn "268" dokima tests AGENTS.md | head
```

> commit 511028c440a552b4e2854a6cc97db624824f5a12
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:55:15 2026 +0000
> 
>     planner for #236 (run 37861151571)
> 
>  tests/test_run_cards.py          |   7 ++-
>  tests/test_run_comment_fields.py | 126 +++++++++++++++++++++++++++++++++++++--
>  2 files changed, 125 insertions(+), 8 deletions(-)
> 
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
> 
> commit 4ff02784de75ecba18740dfdadcf9f579900e22c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 16:43:32 2026 -0500
> 
>     Every field on a card has its own GitHub icon, fixed by code (#248)
>     
>     * planner for #234 (run 37825194734)
>     
>     * worker for #234 (run 37829546576)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  dokima/agent.py                       |  50 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_run_comment_fields.py 2>&1 | tail -30
```

> "tests/test_jobs.py::test_kept_twice"
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
> assert (['<details><summary><b>Non-functional requirements</b></summary>\n\n- Jobs survive a restart of the server. (work is n...bs.py::test_kept_twice\n- 77.3: tests/test_jobs.py::test_done\n- 77.4: tests/test_jobs.py::test_restart\n\n</details>'] and '<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats">' in '<details><summary><b>Tests</b></summary>\n\n- 77.1: tests/test_jobs.py::test_fast\n- 77.2: tests/test_jobs.py::test_k...obs.py::test_kept_twice\n- 77.3: tests/test_jobs.py::test_done\n- 77.4: tests/test_jobs.py::test_restart\n\n</details>')
>  +  where '<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats">' = img('stats')
> FAILED tests/test_run_comment_fields.py::test_a_blocker_the_plan_cannot_place_still_shows_why - Assertion

**Agent:** Checking the planner's new tests for the verdict and the owner's latest answers, then writing the review.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_run_comment_fields.py 2>&1 | grep -E "^FAILED" | cut -c1-260; git show 511028c -- tests/test_run_comment_fields.py | head -220
```

> FAILED tests/test_run_comment_fields.py::test_review_runs_are_called_plan_review_and_code_review - AssertionError: 236.1: the queued live card of a plan review does not say Plan review:
> FAILED tests/test_run_comment_fields.py::test_a_run_comment_shows_each_optional_part_only_when_it_has_something - AssertionError: 236.2: a worker with nothing for 'Its own test run' still shows it (blank None):
> FAILED tests/test_run_comment_fields.py::test_a_review_comment_drops_the_previous_step_details_and_notes - AssertionError: 236.2: the passing plan review's comment still shows 'What the previous step did':
> FAILED tests/test_run_comment_fields.py::test_a_field_two_agents_show_looks_the_same_from_both - AssertionError: 236.2: a plan review draws Outside the plan unlike the worker:
> FAILED tests/test_run_comment_fields.py::test_the_planners_comment_lists_each_criterion_with_its_circle_verified_by_and_source - AssertionError: 236.3: 77.1 'A slow call returns a job id within 2 s.' does not follow its status circle (not started):
> FAILED tests/test_run_comment_fields.py::test_a_blocking_review_lists_only_the_failing_criteria_with_why_and_source - AssertionError: 236.4: the failing criterion "The job's result is kept for a day." does not show exactly once:
> FAILED tests/test_run_comment_fields.py::test_a_code_review_and_a_pass_list_nothing_that_passed - AssertionError: 236.4: the code review does not show its failing criterion with why and its Source:
> FAILED tests/test_run_comment_fields.py::test

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "issues_found\|outside_scope\|outside_plan\|suspect_tests" dokima/agent.py | head -30
```

> 355:                  ("What it found", bullets(h.get("outside_scope"), lambda o: f"{mark('outside the plan')} Outside the plan: {o.get('file', '')}: {o.get('why', '')}")),
> 356:                  ("What it raised", bullets(h.get("suspect_tests"), lambda t: f"Suspect test {t.get('test', '')}: {t.get('evidence', '')}")
> 364:                  (f"{mark('outside the plan')} Outside the plan", bullets(h.get("outside_plan"), lambda o: f"{o.get('file', '')}: {o.get('change', '')}")),
> 456:        if h.get("issues_found"):
> 458:            lines += [f"{i}. {f.get('title')}: {f.get('why')}" for i, f in enumerate(h["issues_found"], 1)]
> 639:    for i, f in enumerate(r.get("issues_found") or [], 1):
> 732:    for s in w.get("suspect_tests", []):
> 782:        bad += problems_items(h, "outside_plan", ("file", "change"))
> 783:        bad += problems_items(h, "issues_found", ("title", "why", "evidence"))
> 797:    bad += problems_items(h, "outside_scope", ("file", "why"))
> 798:    bad += problems_items(h, "suspect_tests", ("test", "evidence"))

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner rewrote 236.2 and 236.4 after the owner's answers and added two tests: one for fields two agents share, one for a review's verdict and order."],
  "decided": ["A review's comment opens with passed, blocked or escalated, then lists failing criteria, uncovered asks, changes outside the plan, unconfirmed questions and issues found, in that order.",
              "The planner's criterion rows end with a Source link; the plan no longer asks the owner anything.",
              "Linking each issue found to the issue filed for it is left to #268."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now covers every ask, including the verdict and the order of the review card the owner gave, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "The owner asked for issues found \"as links to the issues filed for them\"; the plan keeps them last in a review's comment and leaves the links to #268, which files them. Nothing is filed today, so there is nothing to link yet, but check #268 really promises the link.",
   "evidence": "plan.json concerns[0] and out_of_scope[0]; owner comment of 2026-10-08T23:45:03Z"},
  {"text": "The owner's shared-style rule is tested on the two fields both agents draw (Outside the plan and Questions for you); a review's failing criterion rows are tested against the planner's row parts (circle, sentence, Source), not as a byte-for-byte match.",
   "evidence": "tests/test_run_comment_fields.py::test_a_field_two_agents_show_looks_the_same_from_both; ::test_a_blocking_review_lists_only_the_failing_criteria_with_why_and_source"}
 ],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "The live card and the record say Plan review where they said Reviewer (plan), and Code review where they said Reviewer (pr).", "source": "https://github.com/dokima-dev/dokima/issues/236", "crit
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`11. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['summary']="The plan now covers every ask, including the review's verdict and the owner's order, and every new test fails today because the feature is missing."
for a in d['asks']:
    if a['ask'].startswith('The full JSON record'): a['criterion']='236.7'
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #236. The review is in `/tmp/dokima-out/review.json` and passes both checks.

- **Last round's blocker is fixed.** It was that nothing promised or tested that a review's comment says its verdict. The plan now promises that the comment opens with passed, blocked or escalated, and never one of the others. A new test checks this for plan reviews and code reviews. It also checks that a review the code rejected claims no verdict.
- **Your answers from 23:45 are all in the plan:**
  - The planner's criterion rows end with a Source link.
  - The review card follows your order: failing criteria, then your asks that nothing covers, then changes outside the plan, then questions it couldn't confirm from your words, then issues it found.
  - Fields that both agents show (Outside the plan, Questions for you) are drawn the same way by both, and a test checks this.
- **Every ask you made maps to a criterion, and the plan has no open questions left.**
- **All 12 new tests fail today because the feature isn't built yet,** not because a test crashes or has a bad path.

I left two notes, neither blocking:
1. You asked for issues found to show "as links to the issues filed for them". The plan puts them last on the review card but leaves the links to #268, which does the filing. Nothing gets filed today, so there's nothing to link yet. I couldn't see #268 from here, so please check it really promises those links.
2. The test for one shared style covers the two fields both agents show. The review's failing criterion rows are checked for the same parts as the planner's rows (circle, sentence, Source), but not for an exact match.

This issue is on autopilot, so the approval starts the worker without waiting for you. If #268 doesn't promise those links, nothing else is tracking them.
