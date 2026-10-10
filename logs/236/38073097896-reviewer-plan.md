# reviewer (plan) for #236

Run: https://github.com/dokima-dev/dokima/actions/runs/38073097896

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (152KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tool-results/bsaynpu2r.txt
> 
> Preview (first 2KB):
> total 224
> drwxr-xr-x 2 runner runner  4096 Oct 10 17:46 .
> drwxr-xr-x 3 runner runner  4096 Oct 10 17:46 ..
> -rw-r--r-- 1 runner runner  8734 Oct 10 17:46 01-planner.json
> -rw-r--r-- 1 runner runner  7692 Oct 10 17:46 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10041 Oct 10 17:46 03-planner.json
> -rw-r--r-- 1 runner runner  6349 Oct 10 17:46 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  4281 Oct 10 17:46 05-worker.json
> -rw-r--r-- 1 runner runner  3309 Oct 10 17:46 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 12547 Oct 10 17:46 07-planner.json
> -rw-r--r-- 1 runner runner  7179 Oct 10 17:46 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13586 Oct 10 17:46 09-planner.json
> -rw-r--r-- 1 runner runner  6591 Oct 10 17:46 10-reviewer-plan.json
> -rw-r--r-- 1 runner runner  2421 Oct 10 17:46 11-worker.json
> -rw-r--r-- 1 runner runner  1752 Oct 10 17:46 12-reviewer-pr.json
> -rw-r--r-- 1 runner runner   319 Oct 10 17:46 13-updater.json
> -rw-r--r-- 1 runner runner 12998 Oct 10 17:46 14-planner.json
> -rw-r--r-- 1 runner runner   319 Oct 10 17:46 15-updater.json
> -rw-r--r-- 1 runner runner  6538 Oct 10 17:46 16-reviewer-plan.json
> -rw-r--r-- 1 runner runner   319 Oct 10 17:46 17-updater.json
> -rw-r--r-- 1 runner runner   319 Oct 10 17:46 18-updater.json
> -rw-r--r-- 1 runner runner

`2. Bash`
```
cd /tmp/pack; ls in | tail -20; wc -c issue.md plan.json open_blockers.json; cat open_blockers.json
```

> 14-planner.json
> 15-updater.json
> 16-reviewer-plan.json
> 17-updater.json
> 18-updater.json
> 19-updater.json
> 20-updater.json
> 21-updater.json
> 22-updater.json
> 23-updater.json
> 24-updater.json
> 25-updater.json
> 26-updater.json
> 27-updater.json
> 28-updater.json
> 29-updater.json
> 30-updater.json
> 31-updater.json
> 32-updater.json
> 33-planner.json
> 144224 issue.md
>   9214 plan.json
>      2 open_blockers.json
> 153440 total
> []
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat in/33-planner.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> {
>  "kind": "user_story",
>  "summary": "Run comments show only what each run changed, decided or raised, named Plan review and Code review, with stats folded and tokens short.",
>  "user_story": "Every run comment shows only what that run changed, decided or raised and what the owner must do now, each field drawn the same way by every agent, never repeating the card above it.",
>  "acceptance_criteria": [
>   {
>    "text": "A review run is called Plan review or Code review on its live card and run comment, never Reviewer (plan), Reviewer (pr) or The reviewer. That holds for a review that passed, was rejected, was cancelled or never started, and a code review's queued live card still makes the card show Code review running.",
>    "source": "https://github.com/dokima-dev/dokima/issues/236"
>   },
>   {
>    "text": "The planner's run comment no longer repeats the card above it. It shows no user story, criteria, non-functional requirements, scope, out of scope, tests, or Blocked by, Blocks and Relates to lines. It shows its one sentence, what it raised, its answers and its changes to older tests with their reasons, each only when it has one, and a split still lists its stories.",
>    "source": "https://github.com/dokima-dev/dokima/issues/236#issuecomment-6091234167"
>   },
>   {
>    "text": "A review's comment opens with its verdict, passed, blocked or escalated, then lists only what fails. First each failing criterion: its sentence from the plan behind the failed circle, each of its blockers' words 

`4. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|issuecomment-\|^\*\*" issue.md | head -150
```

> 8:**Plan**
> 16:**User story:** Every run comment shows only what the owner needs, each field drawn the same way by every agent: a plan's criteria with proof and source, a review's verdict and failures in plain words, the worker's files on one line, and the stats folded away.
> 54:**Scope:** `dokima/agent.py`, `AGENTS.md`
> 68:**Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37891343203/job/113692733587"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <a href="https://github.com/dokima-dev/dokima/actions/runs/37866844632"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 80:**Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 82:**User story:** Every run comment shows only the fields that have something, names the reviews

`5. Bash`
```
cd /tmp/pack; sed -n 78,115p issue.md; echo =====; sed -n 263,268p issue.md; sed -n 497,500p issue.md; sed -n 1273,1276p issue.md; sed -n 1369,1400p issue.md; sed -n 1479,1600p issue.md
```

> <details open><summary>From the approved plan of #230, story 3</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** Every run comment shows only the fields that have something, names the reviews Plan review and Code review, lists a failing criterion with why it fails, and folds the stats.
> 
> **Context:** Run comments are drawn by render(), details() and footnote() in dokima/agent.py; the live card's heading is set in live_card() ('Reviewer ({stage})'). The reviewer's blockers today show as '**B1** (212.3, ...)'. The worker hand-back holds suspect_tests, outside_scope, replies and evidence (its test result line); the reviewer's holds outside_plan, notes and previous_step.open (still open); the planner's holds questions. The planner's comment lists its criteria; the reviewer's should mirror it with only the failing ones, each with the blocker's problem in place of Verified by. Files changed means the worker's changed files, shown on one inline line. The owner answered (comment of 2026-10-08T18:29:55Z) that the planner's own run comment shows each criterion with its status and Verified by, so the reviewer's comment mirrors that list. dokima/agent.py render() today lists the planner's criteria as plain numbered text.
> 
> **Acceptance criteria:**
> - The live card and the record say Plan review where they said Reviewer (plan), and Code review where they said Reviewer (pr). ([source](https://github.com/dokima-dev/dokima/issues/230))
> - 

**Agent:** I'm reviewing the plan for #236: I've read the owner's comments and am now matching each ask to a criterion and running the new tests.

`6. Bash`
```
cd /tmp/pack; grep -o "issuecomment-[0-9]*" issue.md | sort | uniq -c; grep -n "issuecomment" issue.md | head; python3 -c "
import json;d=json.load(open('in/16-reviewer-plan.json'));print(json.dumps(d['handback'],indent=1)[:5000])"
```

> {
>  "previous_step": {
>   "did": [
>    "The planner re-planned after the pull request clashed with main, keeping every criterion, test and scope of the approved plan.",
>    "It rewrote the test for the no-new-raise-type-field requirement: it now watches every field code reads off a hand-back while drawing each agent's comment, and fails on any field the agents' prompts do not define."
>   ],
>   "decided": [
>    "The worker's files changed and each test's Verified by line live in the run's record, not in a hand-back."
>   ],
>   "open": []
>  },
>  "verdict": "approve",
>  "summary": "The plan is unchanged except for a stronger no-new-field test; every new test fails on main for the missing feature.",
>  "blockers": [],
>  "notes": [
>   {
>    "text": "The rewritten raise-type test turns red when code reads a field no agent's prompt defines: reading raises off a review hand-back fails it.",
>    "evidence": "injecting h.get(\"raises\") into render() in dokima/agent.py: '236.9: code reads hand-back fields no agent's prompt defines, so a hand-back gained a field: ['raises']'; tests/test_run_comment_fields.py on main: 13 failed, each naming its criterion; pytest -q on try/issue-236: 765 passed"
>   },
>   {
>    "text": "The branch still has to take in main's newer AGENTS.md (#307, #319) before it can merge; the plan's AGENTS.md change touches only the Agent records and cards paragraph.",
>    "evidence": "git merge-base --is-ancestor 65edcee HEAD fails; git diff origin/main...HEAD -- AGENTS.md changes one paragra

`7. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/14-planner.json'))['handback']
for c in d['acceptance_criteria']: print('-',c['text'][:400], c['source'])
print(d.get('out_of_scope'))
print(d.get('non_functional'))
"; cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff f2ffd16 85681f4 --stat
```

> - A review run is called Plan review or Code review on its live card and run comment, never Reviewer (plan), Reviewer (pr) or The reviewer. https://github.com/dokima-dev/dokima/issues/236
> - Each field of a run comment shows only when it has something, and a field two agents share looks the same from both. The optional fields are the worker's suspect tests, changes outside scope, replies to blockers and test result line, a review's changes outside the plan, questions and issues found, and the planner's questions. Nothing shows as a blank heading or an empty fold. The worker's changes  https://github.com/dokima-dev/dokima/issues/236
> - The planner's run comment lists each criterion behind its status circle, then Verified by with its tests' docstring first lines, then a Source link. The circle is the not started one the issue card shows before any check runs, the docstrings are read from the planner's test files, and non-functional requirements show the same rows in their fold, without Source since they have none. https://github.com/dokima-dev/dokima/issues/236
> - A review's comment opens with its verdict, then shows only these, in this order. First, each failing criterion: its sentence from the plan behind the failed circle, each of its blockers' problems behind the blocker icon, then its Source link, in place of Verified by. Then each ask of the owner's with no criterion: the ask, Nothing covers this and its Source link. Then its changes outside the plan, https://github.com/doki

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git log --format='%h %p %s' -3; git diff f2ffd16 85681f4 -- tests/test_answered_questions.py tests/test_autopilot_river.py tests/test_fixer.py | head -80; git diff origin/main HEAD --stat 2>/dev/null | tail -3; git log origin/main --oneline -1
```

> 85681f4 f2ffd16 planner for #236 (run 38071347062)
> f2ffd16 5232246 planner for #236 (run 37890549750)
> 5232246 0c133d2 1b0cda6 Merge branch 'main' into try/issue-236
> diff --git a/tests/test_answered_questions.py b/tests/test_answered_questions.py
> new file mode 100644
> index 0000000..8ceb538
> --- /dev/null
> +++ b/tests/test_answered_questions.py
> @@ -0,0 +1,193 @@
> +"""A question the reviewer answers from the owner's words shows plainly (#238, story 5 of #230).
> +
> +When the plan reviewer accepts a planner question's assumption on the owner's own words, the run comment shows the
> +question, the answer below it (the plan's assumption for that question) and the evidence (the owner's matched words,
> +linked to where they said them). Today render() packs all of that into one line under "The plan's assumptions:" and
> +never shows the answer at all.
> +
> +These tests run the workflow's own record step, `python3 -m dokima.agent record reviewer plan OUT check.txt true LOGS`,
> +with the reviewed plan in `$PACK/plan.json` (the job-wide PACK of agent.yml, where the plan reviewer's plan lives), and
> +read the comment it writes to OUT/comment.md. The answer of a question is the "assumption" the plan gave it.
> +
> +What the comment must hold, pinned here:
> +    the section     a heading line holding the words "Answered from your words", then the list under it: every line
> +                    after the heading up to the first non-empty line that is neither a list item ("- " or "1. ") nor
> +                    in

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -1; git log origin/main --oneline -1; for f in tests/test_answered_questions.py tests/test_autopilot_river.py tests/test_fixer.py; do echo "$f: main $(git cat-file -e origin/main:$f 2>/dev/null && echo yes || echo no), f2ffd16 $(git cat-file -e f2ffd16:$f 2>/dev/null && echo yes||echo no)"; done; git diff f2ffd16 85681f4 -- tests/test_autopilot_river.py tests/test_fixer.py
```

> f7340db board.yml runs the pull request's own copy of itself, with the keys, on a review (#418)
> tests/test_answered_questions.py: main yes, f2ffd16 no
> tests/test_autopilot_river.py: main yes, f2ffd16 yes
> tests/test_fixer.py: main yes, f2ffd16 yes
> diff --git a/tests/test_autopilot_river.py b/tests/test_autopilot_river.py
> index 0d7a657..92d7904 100644
> --- a/tests/test_autopilot_river.py
> +++ b/tests/test_autopilot_river.py
> @@ -514,6 +514,20 @@ def test_an_assumption_is_accepted_only_on_words_the_owner_really_said(record_pr
>              f"211.5 ({case}): the Next line should name only the question whose words were not found ({named!r}): {nxt!r}"
>  
>  
> +def test_the_review_card_shows_the_owners_words_each_assumption_matched(record_property):
> +    """The plan review's card shows, for each accepted assumption, the owner's words it matched and where they said them.
> +
> +    Draws the card of a plan review that accepts two assumptions, one matched to AGENTS.md and one to a comment on the
> +    issue. The readable part of the card, above the folded record, must show each question, the words it matched and
> +    their source."""
> +    record_property("proves", "211.5")
> +    body = agent.render(ts.review_record({**APPROVE, "assumptions": [ACCEPT_1, ACCEPT_2]}))
> +    shown = body.split("<details><summary>Full record")[0]
> +    for a in (ACCEPT_1, ACCEPT_2):
> +        for k in ("question", "matched", "source"):
> +            assert a[k] in shown, f"211.5: the review's card does not show the {k} of a

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git grep -c "test_the_review_card_shows_the_owners_words_each_assumption_matched\|test_the_review_comment_shows_who_fixes_each_blocker" origin/main -- tests; git diff origin/main HEAD -- tests/test_answered_questions.py tests/test_autopilot_river.py tests/test_fixer.py | head -20; git merge-base HEAD origin/main; git log --oneline -1 $(git merge-base HEAD origin/main)
```

> origin/main:tests/test_autopilot_river.py:1
> origin/main:tests/test_fixer.py:1
> diff --git a/tests/test_answered_questions.py b/tests/test_answered_questions.py
> index 82d6474..8ceb538 100644
> --- a/tests/test_answered_questions.py
> +++ b/tests/test_answered_questions.py
> @@ -14,9 +14,8 @@ What the comment must hold, pinned here:
>                      after the heading up to the first non-empty line that is neither a list item ("- " or "1. ") nor
>                      indented under one
>      each answer     inside the section, the question on one line, the answer on a later line and the evidence on a
> -                    later line still; the evidence holds the matched words in quotes and then the issue or comment
> -                    link as given, written out bare so GitHub draws it as its own reference (#359); for "AGENTS.md"
> -                    it is a markdown link whose text holds the matched words and whose target is the file on the
> +                    later line still; the evidence is a markdown link whose text holds the matched words and whose
> +                    target is the source: the issue or comment link as given, or for "AGENTS.md" the file on the
>                      repo's main branch, https://github.com/o/r/blob/main/AGENTS.md
>      no blank heading  a line that is only a bold heading ending in a colon (an icon may lead it) is always followed,
>                      past blank lines, by a list item
> @@ -123,15 +122,8 @@ def line_of(body, needle):
>  
>  
>  def link(match

`11. Bash`
```
cd /home/runner/work/dokima/dokima; for f in tests/test_answered_questions.py; do git cat-file -e 1b0cda6:$f && echo base-has; done; git diff 1b0cda6 HEAD -- tests/test_answered_questions.py tests/test_autopilot_river.py tests/test_fixer.py | wc -l; git diff 1b0cda6 f2ffd16 --stat -- tests/test_answered_questions.py tests/test_autopilot_river.py tests/test_fixer.py
```

> base-has
> 0
>  tests/test_answered_questions.py | 193 ---------------------------------------
>  tests/test_autopilot_river.py    |  14 ---
>  tests/test_fixer.py              |  15 ---
>  3 files changed, 222 deletions(-)

**Agent:** Checking the planner's tests now: confirmed its edits to three unrelated test files only restore them to main's state; running the new tests next.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_run_comment_fields.py 2>&1 | grep -E "^(FAILED|ERROR|PASSED)|passed|failed|Error" | cut -c1-400
```

> ("rejected", run("reviewer", stage, BLOCK, passed=False, problems="a problem\n")[0]),
>                       ("never started", agent.render(agent.not_started("reviewer", stage, "the pack failed", META)))]
> E       AttributeError: module 'dokima.card' has no attribute 'review_running'
> /home/runner/work/dokima/dokima/tests/test_run_comment_fields.py:271: AttributeError
> E           AssertionError: 236.2: the planner's comment repeats the card's user story: 'Callers get a job id for a slow call zq.'
> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> tests/test_run_comment_fields.py:302: AssertionError
> E       AssertionError: 236.2: a plan with nothing to fold shows folds other than Stats and Full record: ['<b>Non-functional requirements</b>', '<b>Scope</b>', '<b>Out of scope</b>', '<b>Tests</b>', '<b><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Stats</b>', 'Full record']
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="plann

`13. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_run_comment_fields.py -rA 2>&1 | grep ^PASSED; grep -n "review_running" -r dokima tests | head; sed -n 240,280p tests/test_run_comment_fields.py
```

> PASSED tests/test_run_comment_fields.py::test_a_passing_review_lists_nothing_that_passed
> PASSED tests/test_run_comment_fields.py::test_a_review_comment_drops_details_the_previous_step_notes_and_asks
> PASSED tests/test_run_comment_fields.py::test_a_worker_that_changed_nothing_and_ran_no_test_shows_neither_line
> PASSED tests/test_run_comment_fields.py::test_a_split_says_no_model_ran_and_a_run_no_agent_started_keeps_its_line
> PASSED tests/test_run_comment_fields.py::test_token_counts_read_short[950-950]
> PASSED tests/test_run_comment_fields.py::test_the_full_record_stays_the_last_fold_and_reads_back
> tests/test_run_comment_fields.py:271:    assert card.review_running([bot]), "236.1: the card no longer sees a code review running from its queued live card"
> tests/test_run_comment_fields.py:275:    assert not card.review_running([{"author": {"login": agent.BOT}, "body": agent.live_card("reviewer", "plan", "queued")}]), \
> 
>     Draws the live card of a plan review and a code review in every state, and the run comment of each review that
>     passes, blocks, escalates, is rejected, is cancelled after or before its agent started, and never starts; each
>     names its own review and never the other, Reviewer (...) or The reviewer, where the owner reads it. A planner's
>     and a worker's live cards keep their names. A code review's queued live card still makes the card show Code
>     review running, as dokima/card.py and .github/workflows/card.yml read it, and a plan review's never does.
> 
>     Pro

`14. Bash`
```
cd /home/runner/work/dokima/dokima; git grep -n "def review_running\|Reviewer (pr)\|Reviewer (" origin/main -- dokima/card.py .github/workflows/card.yml | head; echo ---; git grep -n "Reviewer (\|review_running" HEAD -- dokima/card.py .github/workflows/card.yml | head
```

> origin/main:.github/workflows/card.yml:59:            if [[ "$COMMENT" != '<!-- dokima-live -->'* || "$COMMENT" != *'**Reviewer (pr)**'* ]]; then
> origin/main:dokima/card.py:394:def review_running(items):
> ---

`15. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/main:dokima/card.py | sed -n 385,410p; git show origin/main:.github/workflows/card.yml | sed -n 50,65p
```

> def code_review(recs):
>     """The newest code review whose record passed its check, since the worker last built; None when there is none."""
>     builds = [i for i, r in enumerate(recs) if r.get("role") == "worker"]
>     after = recs[builds[-1] + 1:] if builds else recs
>     reviews = [r for r in after if r.get("role") == "reviewer" and r.get("stage") == "pr" and r.get("check", {}).get("passed")]
>     return reviews[-1] if reviews else None
> 
> 
> def review_running(items):
>     """True while the bot's code review run card since the newest build awaits its record."""
>     from dokima import agent
>     running = False
>     for c in items or []:
>         rs = agent.records([c])
>         if rs:
>             if rs[0].get("role") == "worker" or (rs[0].get("role") == "reviewer" and rs[0].get("stage") == "pr"):
>                 running = False
>             continue
>         if (c.get("author") or {}).get("login") in (agent.BOT, f"{agent.BOT}[bot]") and \
>                 re.match(re.escape(agent.LIVE) + r"[^*]*\*\*Reviewer \(pr\)\*\*", (c.get("body") or "").strip()):
>             running = True
>     return running
> 
> 
> def owner_review(reviews, owners):
>           COMMENT: ${{ github.event.comment.body }}
>           PR: ${{ github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number }}
>           HEAD: ${{ github.event.pull_request.head.ref || github.event.workflow_run.head_branch }}
>           TITLE: ${{ github.event.workflow_run.display_title }}
>           RUN: ${{ github.run_id }}
>   

`16. Bash`
```
cd /home/runner/work/dokima/dokima; git diff origin/main HEAD --stat -- dokima/ AGENTS.md | tail -5; git log --oneline 1b0cda6..HEAD | head -20; grep -n "Plan review\|Code review" dokima/agent.py | head
```

> dokima/roles/reviewer.md     |   82 ++-
>  dokima/roles/worker.md       |   43 +-
>  dokima/scan.py               |  109 ----
>  dokima/uptodate.py           |   50 +-
>  15 files changed, 728 insertions(+), 1616 deletions(-)
> 85681f4 planner for #236 (run 38071347062)
> f2ffd16 planner for #236 (run 37890549750)
> 5232246 Merge branch 'main' into try/issue-236
> 0c133d2 Merge branch 'main' into try/issue-236
> ce098ca Merge branch 'main' into try/issue-236
> 7e326db Merge branch 'main' into try/issue-236
> 79aceca Merge branch 'main' into try/issue-236
> 37f1665 Merge branch 'main' into try/issue-236
> 88979d9 Merge branch 'main' into try/issue-236
> 203a6e4 Merge branch 'main' into try/issue-236
> 1ae3a66 Merge branch 'main' into try/issue-236
> 936f0d8 planner for #236 (run 37865186115)
> a8a2dcf planner for #236 (run 37863965870)
> ee7acaa worker for #236 (run 37862227884)
> 2849298 Merge remote-tracking branch 'origin/main' into try/issue-236
> 511028c planner for #236 (run 37861151571)
> 8189470 planner for #236 (run 37848814808)
> 377:    """A review run's name: Plan review for the plan, Code review for the work."""
> 378:    return "Plan review" if stage == "plan" else "Code review"

`17. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt-main; git worktree add -q /tmp/wt-main origin/main 2>&1|tail -1; cp tests/test_run_comment_fields.py /tmp/wt-main/tests/; cd /tmp/wt-main; timeout 600 python3 -m pytest -q tests/test_run_comment_fields.py -rA 2>&1 | grep -E "^(PASSED|FAILED|ERROR)|passed|failed" | cut -c1-300
```

> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planne
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned th
> E           "passed": true,
>         item opening with the failed circle and its sentence from the plan, with each of its blockers' words behind the
> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> The review
> E             - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Retries:** Should a failed job retry by itself? · for you
> E            +    where <built-in method count of str object at 0x55fc1fb47010> = '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...00 out · $3.20 at API prices · [c

**Agent:** All 24 new tests fail on main because the feature is missing, not from crashes. Now checking whether "drawn the same by every agent" is covered.

`18. Bash`
```
cd /home/runner/work/dokima/dokima; git grep -n "drawn the same\|same from both\|looks the same" origin/main -- tests AGENTS.md | head; sed -n '/def test_every_agents_answers_show_in_the_same_raised_earlier_section/,/^def /p' tests/test_run_comment_fields.py | head -60
```

> origin/main:tests/test_open_until_planned.py:169:    byte in the closed Original issue fold with only the Definition of Done after it, redrawn the same; beside it,
> def test_every_agents_answers_show_in_the_same_raised_earlier_section(record_property, env):
>     """The planner's, the worker's and a review's answers look the same.
> 
>     Draws a review, a planner and a worker that each answer the same earlier raises the same way (one done, one
>     disagree), and checks each comment shows one Raised earlier section whose items are exactly the same lines; and
>     that a planner and a worker that answer nothing show no Raised earlier section.
> 
>     Proves 236.6."""
>     record_property("proves", "236.6")
>     w1 = raised("blocker", "The kept test reads a file that never exists zq.", "planner", "Kept test", "W1", "worker")
>     r9 = raised("blocker", "submit() still blocks for a minute zq.", "worker", "Speed", "R9")
>     earlier = [rec("worker", "", dict(WORK, raises=[w1])), rec("reviewer", "pr", dict(APPROVE, raises=[r9]))]
>     answers = [{"raise": "W1", "answer": "done", "why": "The test now makes the file itself zq."},
>                {"raise": "R9", "answer": "disagree", "why": "It returns in 0.1 s, see the test result zq."}]
>     drawn = {role: section(visible(agent.render(rec(role, stage, dict(hb, answers=answers)), earlier=earlier)),
>                            "Raised earlier:")
>              for role, stage, hb in (("reviewer", "pr", APPROVE), ("planner", "", PLAN), ("worker", "", WOR

`19. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/main:tests/test_raised_cards.py | grep -n "def test_\|same" | head -30
```

> 35:issue card of failing tests); they must stay byte for byte the same.
> 235:def test_a_run_comment_shows_every_raise_in_one_raised_section(record_property, env, record, raises, who):
> 256:def test_a_run_that_raised_nothing_shows_no_raised_section(record_property, env):
> 260:    heading; then checks the same planner with one raise does show it, so the check is not passing on nothing.
> 279:def test_the_issue_card_shows_every_raise_still_waiting_for_an_answer(record_property, env):
> 319:def test_no_card_shows_a_raise_or_answer_id(record_property, env):
> 341:def test_a_review_card_shows_earlier_raises_with_its_answers_apart_from_its_own(record_property, env):
> 369:def test_an_answer_given_for_you_on_autopilot_quotes_your_words_and_links_them(record_property, env):
> 390:def test_a_review_that_answered_nothing_shows_no_section_for_earlier_raises(record_property, env):
> 393:    Draws the same review with no answers and checks no Raised earlier heading shows, while its own Raised section
> 405:def test_the_record_step_draws_earlier_raises_from_the_pack(record_property, tmp_path):
> 429:def test_a_record_posted_before_this_change_keeps_its_comment_exactly(record_property, env, name, record):
> 434:    tests/raised_goldens/, with no Raised section; then checks a record of the same role posted after this change does
> 451:def test_the_issue_card_draws_old_records_as_before_and_raised_only_for_newer(record_property, env):
> 506:def test_what_code_detects_draws_exactly_as_today(record_property, env, name, 

`20. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n '/def test_the_worker_shows_the_files_it_changed_as_links_on_one_line/,/^def test_every/p' tests/test_run_comment_fields.py | head -90
```

> def test_the_worker_shows_the_files_it_changed_as_links_on_one_line(record_property, run):
>     """The worker's comment links the files it changed, on one line, not its sentences.
> 
>     Runs the record step for a worker that committed a change to app/jobs.py, left app/keep.py changed and added
>     app/new.py, and checks one line with the files changed icon links all three to the file on try/issue-77, and
>     app/page.py, which it did not touch, never shows. Its per-criterion sentence never shows, its test result line
>     does, and the record keeps the hand-back exactly with the files beside it.
> 
>     Proves 236.5."""
>     record_property("proves", "236.5")
>     repo = run.repo
>     (repo / "app" / "jobs.py").write_text("# jobs, now queued\n")
>     git(repo, "commit", "-q", "-am", "queue the jobs")
>     (repo / "app" / "keep.py").write_text("# keep, changed\n")
>     (repo / "app" / "new.py").write_text("# new\n")
>     body, record = run("worker", "", WORK)
>     text = visible(body)
>     links = {p: f"https://github.com/o/r/blob/try/issue-77/{p}" for p in ("app/jobs.py", "app/keep.py", "app/new.py")}
>     lines = [l for l in text.splitlines() if any(u in l for u in links.values())]
>     assert len(lines) == 1, f"236.5: the files the worker changed must be links on one line, found {len(lines)}:\n{text}"
>     for p, url in links.items():
>         assert f"]({url})" in lines[0] or f'href="{url}"' in lines[0], f"236.5: {p} is not linked to {url}:\n{lines[0]}"
>     assert img("files changed") in lin

`21. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q -x -p no:randomly 2>&1 | tail -3; timeout 900 python3 -m pytest -q 2>&1 | grep FAILED | grep -v test_run_comment_fields | cut -c1-200
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b11lizsuw). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tasks/b11lizsuw.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Full test suite is running in the background; meanwhile I'll draft the hand-back.

`22. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned against the owner's latest words: the planner's comment no longer repeats the card, the review drops Details and What the previous step did, the worker's work shows as links to its files, and token counts read short.",
          "It wrote new tests for each of the eight criteria and the record requirement, and updated or deleted seven older tests the new comments make wrong, each with its reason."],
  "decided": ["The worker's work shows as links to the files it changed on the issue's branch, not its commits; token counts round to the nearest, halves up.",
              "Linking each issue a review finds to its filed issue stays with #268."],
  "open": ["Main's tests that pin today's comments are updated once the worker's merge of main reaches the branch."]},
 "verdict": "approve",
 "summary": "The plan keeps every ask of yours, including Monday's re-plan (drop Details and What the previous step did, the worker's files as links, short token counts), and every new test fails on main for the missing feature.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The live card and the record say Plan review where they said Reviewer (plan), and Code review where they said Reviewer (pr).", "source": "https://github.com/dokima-dev/dokima/issues/236", "criterion": "236.1"},
  {"ask": "The reviewer's card shows only what I care about: did I get what I asked for. That is the verdict, each criterion delivered or not, each failure with its reason, and any ask of mine with no criterion as a blocker.", "source": "https://github.com/dokima-dev/dokima/issues/236#issuecomment-6071262672", "criterion": "236.3"},
  {"ask": "Remove the What the previous step did fold, the Details fold and the Notes section.", "source": "https://github.com/dokima-dev/dokima/issues/236#issuecomment-6071262672", "criterion": "236.4"},
  {"ask": "A failing criterion: its sentence, then
```

> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`23. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['summary']="The plan keeps every ask of yours, including the latest re-plan, and every new test fails on main because the feature is missing."
for a in d['asks']:
    if 'issuecomment-6071262672' in a['source']: a['source']="https://github.com/dokima-dev/dokima/issues/236"
    if a['ask'].startswith("the planner's run comment does not show Relates"): a['source']="https://github.com/dokima-dev/dokima/issues/236#issuecomment-6089549985"
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** Hand-back passes both checks. Waiting for the full suite to finish to confirm no other test breaks.

`24. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tasks/b11lizsuw.output | tail -15 | cut -c1-250
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tasks/b11lizsuw.output tail -15 cut -c1-250. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`25. Bash`
```
tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tasks/b11lizsuw.output | cut -c1-250
```

> assert None is not None
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 30 passed in 2.51s

**Agent:** The second, full run is still going; I'll wait for it to finish.

`26. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 590 python3 -m pytest -q -n auto 2>&1 | tail -3 || true
```

> inifile: None
>   rootdir: /home/runner/work/dokima/dokima

`27. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 590 python3 -m pytest -q 2>&1 | grep -E "FAILED|passed|failed" | grep -v "test_run_comment_fields" | cut -c1-220 | tail -20
```

> FAILED tests/test_run_cards.py::test_the_long_parts_of_every_run_comment_are_folded - AssertionError: 182.1 (review): 'A note on naming-zq.' is in no fold of the comment:
>   <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/doki
>     "passed": true,
>  +  where '<summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/outside-the-plan.svg" wid...idth="16" height="16" align="absmiddle" alt="stats"> Stats</b></summary>\n\nmodel unknown
> FAILED tests/test_run_cards.py::test_the_reviewer_card_shows_pass_or_only_the_criteria_it_blocks_on - AssertionError: 182.4: the reviewer card does not show its proposed issue on top:
>   <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/doki
> assert '1. Board ignores closed PRs: cards go stale' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w...ma/icons/plan-review.svg" width="16" height
>   <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width=
>   <img src="https://

`28. Bash`
```
cd /home/runner/work/dokima/dokima; grep "^FAILED" /tmp/claude-1001/-home-runner-work-dokima-dokima/61182d6d-4cba-4096-9264-01e996c9e1eb/tasks/b11lizsuw.output | grep -v test_run_comment_fields | cut -d' ' -f2 | sort -u
```

> tests/test_answered_questions.py::test_an_accepted_question_shows_the_question_then_its_answer_then_the_owners_words_linked
> tests/test_answered_questions.py::test_no_answered_question_means_no_section_and_no_blank_heading
> tests/test_answered_questions.py::test_only_an_assumption_accepted_with_the_owners_words_and_source_shows_as_answered
> tests/test_autopilot_river.py::test_the_review_card_shows_the_owners_words_each_assumption_matched
> tests/test_blocked_worker.py::test_on_autopilot_a_blocked_plan_waits_with_one_line_and_mentions_no_one
> tests/test_field_icons.py::test_the_review_comment_shows_blocker_note_outside_and_issue_icons
> tests/test_fixer.py::test_the_review_comment_shows_who_fixes_each_blocker
> tests/test_plan_links_recorded.py::test_both_cards_show_every_new_link_from_their_own_side
> tests/test_plan_links_recorded.py::test_the_other_card_keeps_the_link_after_its_own_redraw
> tests/test_run_cards.py::test_the_long_parts_of_every_run_comment_are_folded
> tests/test_run_cards.py::test_the_reviewer_card_shows_pass_or_only_the_criteria_it_blocks_on

`29. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 300 python3 -m pytest -q tests/test_plan_links_recorded.py tests/test_blocked_worker.py::test_on_autopilot_a_blocked_plan_waits_with_one_line_and_mentions_no_one tests/test_fixer.py::test_the_review_comment_shows_who_fixes_each_blocker 2>&1 | grep -E "^E " | head -12 | cut -c1-300; grep -n "def review\b\|def review(" -A6 tests/test_fixer.py | head -12
```

> E           AssertionError: 252.2: the owner's ask on #301 changed
> E           assert 'Issue 301: t...wner approval' == "Issue 301: t...'s own words."
> E             
> E             - Issue 301: the owner's own words.
> E             + Issue 301: the owner's own words.
> E             ?                                  +
> E             + 
> E             + <!-- dokima-done -->
> E             + **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmi
> E           AssertionError: 252.2: the owner's ask on #302 changed on redraw
> E           assert 'Issue 302: t...wner approval' == "Issue 302: t...'s own words."
> E             
> 34:def review(*blockers, verdict="block"):
> 35-    """A well-formed review.json holding these blockers, listing the owner's one ask matched to 9.1.
> 36-
> 37-    A plan review must list every ask and a code review may, so the sample passes code's check on any stage (#244)."""
> 38-    return {"previous_step": {"did": ["Built it."], "decided": [], "open": []}, "verdict": verdict,
> 39-            "summary": "s", "blockers": list(blockers), "notes": [], "outside_plan": [], "resolved": [],
> 40-            "asks": [{"ask": "Paint the door blue", "source": "https://github.com/o/r/issues/9", "criterion": "9.1"}]}

`30. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt-main; git status --short | head; cat /tmp/dokima-out/review.json | head -15; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> {
>  "previous_step": {
>   "did": [
>    "The planner re-planned against the owner's latest words: the planner's comment no longer repeats the card, the review drops Details and What the previous step did, the worker's work shows as links to its files, and token counts read short.",
>    "It wrote new tests for each of the eight criteria and the record requirement, and updated or deleted seven older tests the new comments make wrong, each with its reason."
>   ],
>   "decided": [
>    "The worker's work shows as links to the files it changed on the issue's branch, not its commits; token counts round to the nearest, halves up.",
>    "Linking each issue a review finds to its filed issue stays with #268."
>   ],
>   "open": [
>    "Main's tests that pin today's comments are updated once the worker's merge of main reaches the branch."
>   ]
>  },
>  "verdict": "approve",
> rc=0

**Agent:** I approved the plan for #236. The hand-back is at `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Why it passes**
- **Your asks:** I read your issue text and all your comments and found 18 asks. Each one is kept by one of the plan's criteria; none is missing. The latest re-plan is covered:
  - the review drops Details and What the previous step did;
  - the worker's comment shows links to the files it changed, on one line;
  - token counts read short (12K, 3M);
  - the planner's comment no longer repeats the card or its links.
- **Newest words win:** where your later words override earlier ones (for example, the planner's comment no longer lists criteria with a Source link), the plan follows the later words.
- **Tests:** all 24 new tests fail on `main` because the feature is missing, each naming its criterion. None of them fails by crashing.
- **Planner's edits to older tests:** the planner edited three test files the plan doesn't list (`tests/test_answered_questions.py`, `tests/test_autopilot_river.py`, `tests/test_fixer.py`). Those edits only put them back as they are at the point the branch split from `main`, so on net nothing changed there.

**What the worker will run into**
- **The branch is behind `main` and doesn't fully pass yet.** It still holds the partial build from PR #287, and its full test suite has 29 failures: 18 new tests that aren't built yet, plus 11 older tests. The older ones fail because that partial build broke comments in the old record format, and some come from the branch being out of date with `main`. None of them conflicts with the plan, so this is for the worker to fix, not the planner.
- **Some of `main`'s tests will clash after the merge.** A few tests on `main` that pin today's comments will fail once the worker merges `main` in. The plan says the planner updates them after that merge, so the worker will need to hand them back to the planner then.

**Choices the plan made for you**
- Rounding: token counts round to the nearest, halves up, so 1,500 reads 2K.
- Files, not commits: the worker's comment links its files rather than its commits. Your words allowed either.
- Links to issues a review finds are left to #268. Reviews still list those issues last.

I didn't flag any of these three.
