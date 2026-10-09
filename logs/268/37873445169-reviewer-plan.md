# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37873445169

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (223.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/703cee57-84c9-4a2f-be25-7be0a0037f14/tool-results/bq1o7bvgv.txt
> 
> Preview (first 2KB):
> total 156
> drwxr-xr-x 2 runner runner  4096 Oct  9 02:12 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 02:12 ..
> -rw-r--r-- 1 runner runner  5150 Oct  9 02:12 01-planner.json
> -rw-r--r-- 1 runner runner  4552 Oct  9 02:12 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  3910 Oct  9 02:12 03-worker.json
> -rw-r--r-- 1 runner runner  2965 Oct  9 02:12 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner  8223 Oct  9 02:12 05-planner.json
> -rw-r--r-- 1 runner runner  4332 Oct  9 02:12 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner   333 Oct  9 02:12 07-not-started.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:12 08-updater.json
> -rw-r--r-- 1 runner runner  8647 Oct  9 02:12 09-planner.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:12 10-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:12 11-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:12 12-updater.json
> -rw-r--r-- 1 runner runner  5440 Oct  9 02:12 13-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11812 Oct  9 02:12 14-planner.json
> -rw-r--r-- 1 runner runner  5673 Oct  9 02:12 15-reviewer-plan.json
> -rw-r--r-- 1 runner runner 15025 Oct  9 02:12 16-planner.json
> -rw-r--r-- 1 runner runner  5435 Oct  9 02:12 17-reviewer-plan.json
> -rw-r--r-- 1 runner runner   325 Oct  9 02:12 18-updater.json
> -rw-r--r-- 1 runner run

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json; cat open_blockers.json; echo; python3 -c "
import json;d=json.load(open('in/19-planner.json'));print(json.dumps(d,indent=1)[:6000])"
```

> 213070 issue.md
>  14131 plan.json
>      2 open_blockers.json
> 227203 total
> []
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37872667045",
>  "commit_before": "8adf188a6ef635b878e04089b2c86a9aeeb76c3f",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 448375,
>   "turns": 14,
>   "cost_usd": 0.6941208,
>   "tokens_in": 712049,
>   "tokens_out": 6030
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/268/37872667045-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37872667045",
>  "handback": {
>   "kind": "user_story",
>   "summary": "Issues any agent finds outside its own issue are filed by code at the end of the run, parked and labeled filed-by-dokima.",
>   "user_story": "Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.",
>   "acceptance_criteria": [
>    {
>     "text": "Every agent hands back the issues it finds as raises of kind issue (title, why, evidence), in the shared field #289 brings. The planner's, the worker's and the reviewer's prompts each describe it. No hand-back gains a new issues_found or other raise-type field, and a finding handed back any other way is not filed. Every issue raised that way is filed during that agent's own run, with no command, as its own GitHub issue. The issue takes the find

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('plan.json'));print(json.dumps({k:v for k,v in d.items()},indent=1))" | sed -n '1,400p' | tail -n +60 | head -120; for f in in/1[3-9]*.json in/0[6-9]*.json; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f'));h=d.get('handback') or {};print(d.get('role'),d.get('check',d.get('verdict')));print(json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','resolved','questions']},indent=1)[:2500])"; done
```

> "tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record"
>   ],
>   "268.3": [
>    "tests/test_filed_issues.py::test_a_filed_issue_gets_nothing_more_than_filing"
>   ],
>   "268.4": [
>    "tests/test_filed_issues.py::test_the_same_finding_is_never_filed_twice"
>   ],
>   "268.5": [
>    "tests/test_filed_issues.py::test_the_card_names_each_filed_issue",
>    "tests/test_filed_issues.py::test_a_finding_github_refuses_to_file_says_why_on_the_card"
>   ],
>   "268.6": [
>    "tests/test_filed_issues.py::test_a_rejected_handback_files_nothing"
>   ],
>   "268.7": [
>    "tests/test_filed_issues.py::test_the_key_that_files_is_made_only_after_the_agent_and_the_check"
>   ]
>  },
>  "test_changes": {
>   "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled": "Re-planned on the new main after #279 merged. The fake planner's plan shared by every test in this file (plan_handback) now carries empty links, which the planner check from #256 requires; without them every fake planner run was rejected and the tests failed before checking any filing. Its checks are unchanged. Re-planned again on main a302cb1 after #277, #281 and #286 merged: the fake worker's summary shared by every test in this file (work_handback) is now one sentence, \"Built the fix in x.py.\", because since #277 code rejects a worker summary of more than one sentence and every worker case was rejected before any filing was checked. Re-planned on the owner's comment of 2026-1

`4. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^---\|^\*\*@\|^> \*\*\|commented\|issuecomment" issue.md | head -80
```

> 94:## Comments
> 96:### dokima-runtime on issue #268 (2026-10-08T21:27:32Z)
> 100:### dokima-runtime on issue #268 (2026-10-08T21:27:46Z)
> 269:### dokima-runtime on issue #268 (2026-10-08T21:40:31Z)
> 410:### dokima-runtime on issue #268 (2026-10-08T21:43:11Z)
> 415:### dokima-runtime on issue #268 (2026-10-08T21:43:13Z)
> 496:### dokima-runtime on PR #274 (2026-10-08T21:54:27Z)
> 596:### dokima-runtime on issue #268 (2026-10-08T22:03:21Z)
> 794:### dokima-runtime on PR #274 (2026-10-08T22:07:27Z)
> 798:### dokima-runtime on issue #268 (2026-10-08T22:11:55Z)
> 931:### dokima-runtime on PR #274 (2026-10-08T22:13:23Z)
> 935:### dokima-runtime on issue #268 (2026-10-08T22:15:43Z)
> 940:### dokima-runtime on PR #274 (2026-10-08T22:15:45Z)
> 974:### dokima-runtime on PR #274 (2026-10-08T22:19:15Z)
> 978:### dokima-runtime on PR #274 (2026-10-08T22:52:23Z)
> 982:### dokima-runtime on PR #274 (2026-10-08T23:47:03Z)
> 986:### dokima-runtime on issue #268 (2026-10-08T23:47:05Z)
> 1023:### dokima-runtime on issue #268 (2026-10-08T23:47:20Z)
> 1224:### dokima-runtime on PR #274 (2026-10-08T23:51:08Z)
> 1228:### dokima-runtime on issue #268 (2026-10-08T23:51:10Z)
> 1265:### dokima-runtime on PR #274 (2026-10-08T23:56:57Z)
> 1269:### dokima-runtime on issue #268 (2026-10-08T23:57:00Z)
> 1306:### dokima-runtime on PR #274 (2026-10-09T00:02:40Z)
> 1310:### dokima-runtime on issue #268 (2026-10-09T00:02:42Z)
> 1347:### dokima-runtime on issue #268 (2026-10-09T00:03:25Z)
> 1493:### dokima-runtime on issue #268 (2026-10-09T00:07:21Z)
> 1702:##

`5. Bash`
```
cd /tmp/pack; sed -n 1,95p issue.md; sed -n 1700,1706p issue.md; sed -n 2238,2290p issue.md; sed -n 2506,2530p issue.md
```

> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> Issues any agent finds outside its own issue are filed by code at the end of the run, parked and labeled filed-by-dokima.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #268](https://github.com/dokima-dev/dokima/issues/268) · [PR #274](https://github.com/dokima-dev/dokima/pull/274) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/274/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #265, #193, #269, #289
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercon

**Agent:** I'm checking whether #289 (the raises field) is on main yet, then running the plan's tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 origin/main 2>/dev/null; git log --oneline origin/main | grep -i "289\|raise" | head; grep -rn "raises" dokima/*.py dokima/roles/*.md | head -10; git diff --stat origin/main...HEAD 2>/dev/null | tail -3
```

> bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
> a302cb1 The Autopilot view shows only open issues and pull requests (#286)
> 1c8e0e0 The issue card and the planner's run comment show the links, each kind with its own icon (#281)
> dokima/board.py:70:    """One REST call; raises subprocess.CalledProcessError when GitHub refuses it."""
>  dokima/roles/worker.md     |   7 +-
>  tests/test_filed_issues.py | 642 +++++++++++++++++++++++++++++++++++++++++++++
>  7 files changed, 766 insertions(+), 15 deletions(-)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat origin/main...HEAD; git diff --stat origin/main HEAD; timeout 600 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E   .*26[8]\.|[0-9]+ (passed|failed))" | head -30
```

> AGENTS.md                  |   6 +-
>  dokima/agent.py            | 113 +++++++-
>  dokima/planner.py          |   5 +-
>  dokima/roles/planner.md    |   3 +
>  dokima/roles/reviewer.md   |   5 +-
>  dokima/roles/worker.md     |   7 +-
>  tests/test_filed_issues.py | 642 +++++++++++++++++++++++++++++++++++++++++++++
>  7 files changed, 766 insertions(+), 15 deletions(-)
>  .github/workflows/agent.yml           |  18 +-
>  .github/workflows/uptodate.yml        |  34 --
>  AGENTS.md                             |   8 +-
>  dokima/agent.py                       | 430 +++++++--------------
>  dokima/board.py                       |  27 +-
>  dokima/card.py                        | 212 +++-------
>  dokima/fence.py                       |  29 +-
>  dokima/icons/acceptance-criterion.svg |   1 -
>  dokima/icons/autopilot.svg            |   1 -
>  dokima/icons/blocked-by.svg           |   1 -
>  dokima/icons/blocker.svg              |   1 -
>  dokima/icons/blocks.svg               |   1 -
>  dokima/icons/code-review.svg          |   1 -
>  dokima/icons/files-changed.svg        |   1 -
>  dokima/icons/issue-found.svg          |   1 -
>  dokima/icons/merged.svg               |   1 -
>  dokima/icons/needs-you.svg            |   1 -
>  dokima/icons/note.svg                 |   1 -
>  dokima/icons/outside-the-plan.svg     |   1 -
>  dokima/icons/owner-approval.svg       |   1 -
>  dokima/icons/plan-review.svg          |   1 -
>  dokima/icons/planner.svg              |   1 -
>  dokima/icons/question.svg             |   1 -
>  dokima/icons/related.svg 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt origin/main 2>&1|tail -1; cp tests/test_filed_issues.py /tmp/mainwt/tests/; cd /tmp/mainwt; timeout 900 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E   +(AssertionError: )?26[8]\.[0-9]+: [^ ]+ ?[^ ]*|[0-9]+ (passed|failed))" | cut -c1-200 | awk '!seen[substr($0,1,60)]++' | head -40
```

> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: worker (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: code review (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: planner (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: plan review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: worker (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: code review (repo without the labels) found two issues but did not file exactly those two by their titles; filed: []
> E         268.1: dokima/roles/planner.md does not give the planner's found issues as "raises": [{"kind": "issue", "title": ..., "why": ..., "evidence": ...}]
> E         268.1: dokima/roles/worker.md does not give the worker's found issues as "raises": [{"kind": "issue", "title": ..., "why": ..., "evidence": ...}]
> E         268.1: dokima/roles/reviewer.md does not give the reviewer's found issues as "raises": [{"kind": "issue", "title": ..., 

`9. Bash`
```
cd /tmp/pack; grep -o "https://github.com/dokima-dev/dokima/issues/268#issuecomment-[0-9]*" issue.md | sort -u | head; grep -o 'issuecomment[^")]*' in/*.json | sort -u | head; python3 -c "import json;print(json.load(open('plan.json')).get('questions'))"; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/mainwt
```

> None
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /tmp/pack; python3 -c "
import json;h=json.load(open('in/17-reviewer-plan.json'))['handback'];print(json.dumps({k:h.get(k) for k in ['asks','notes','previous_step']},indent=1))"
```

> {
>  "asks": [
>   {
>    "ask": "The planner's, the worker's and the reviewer's hand-backs each take the same found-issues field, and every issue listed there is filed in that agent's own run, with no command, as its own GitHub issue titled with the finding's title and labeled exactly parked and filed-by-dokima, also on a repo that has neither label yet; a hand-back that lists none files none.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268",
>    "criterion": "268.1"
>   },
>   {
>    "ask": "Each filed issue says where it was found (the issue the run worked on, and its pull request when there is one) and by which agent, carries the finding's why and evidence, and links the comment that holds the record of the run that found it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268",
>    "criterion": "268.2"
>   },
>   {
>    "ask": "A filed issue gets nothing more: it is not made a sub-issue, gets no blocked-by link, does not go on autopilot even when the issue it was found on is, and no stage starts on it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268",
>    "criterion": "268.3"
>   },
>   {
>    "ask": "The same finding is never filed twice: a title already filed by Dokima, open or closed, ignoring letter case and spacing, is not filed again, whether it repeats in one hand-back or comes back in a later run of any agent; new findings beside it are still filed.",
>    "source": "https://github.com/dokima-dev/dokima/issues/268",
>    "criterion": "268.4"
>   },
>   {

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned on the newest main (bf41093, #290) and on the owner's answer to wait for #289.",
          "Added checks that the reviewer, in plan review and code review, handing findings back in an issues_found field files nothing, like the planner and the worker."],
  "decided": ["Found issues are raises of kind issue for all three agents, with no question left for the owner.",
              "Marked the issue blocked by #289 and said the worker should start only after #289 merges, merging main first."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan builds found issues on #289's raises shape as the owner answered, waits on #289, and all eight tests fail on main only because nothing is filed yet.",
 "blockers": [],
 "notes": [
  {"text": "The tests pin the raise shape {\"kind\": \"issue\", \"title\", \"why\", \"evidence\"} before #289 has merged; if #289 lands with other names, the tests need a re-plan before the worker starts.",
   "evidence": "git log origin/main has no #289 commit (head bf41093); plan.json links.blocked_by is [289]; tests/test_filed_issues.py checks each prompt for \"raises\": [{\"kind\": \"issue\", ...}]."},
  {"text": "This branch is still behind main and holds round one's code, which on this branch already files a finding handed back in issues_found; the build must start from main, where the tests fail for the right reason.",
   "evidence": "pytest on try/issue-268: '268.1: planner with issues_found filed ['Found in a field of its own']'. Same test file on origin/main: 8 failed, each with 'filed: []' or a prompt not yet naming raises."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The planner's, the worker's and the reviewer's hand-backs each take the same found-issues field, and every issue listed there is filed in that agent's own run, with no command, as its own GitHub issue titled with the fin
```

> summary holds 29 words, over its cap of 25 (up to 30 passes)
> rc=0

**Agent:** The summary is a few words over its cap, so I'm shortening it.

`12. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan builds found issues on #289's raises shape and waits for #289; all eight tests fail on main only because nothing is filed."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #268, and the review is in `/tmp/dokima-out/review.json`. Both hand-back checks pass on it.

- **Your two comments are covered.** Found issues are filed as raises of kind `issue`, the shape #289 brings, and no hand-back gets a new `issues_found` field. The planner, the worker and the reviewer all file this way only, and there are no questions left for you.
- **It waits for #289.** The plan marks #268 as blocked by #289 and says the worker should start only after #289 merges, merging main first. #289 is not on main yet; main is at bf41093.
- **The tests fail for the right reason.** I copied the test file onto current main and ran it: all 8 tests fail only because nothing is filed yet and the prompts don't describe raises yet.
- **No earlier blockers were open.** My one note from last round is fixed: there is now a check that the reviewer handing findings back in `issues_found` files nothing.

Two non-blocking notes in the review:
1. The tests fix the exact field names of a raise (`kind`, `title`, `why`, `evidence`) before #289 has merged. If #289 lands with different names, the tests need a re-plan before the worker starts.
2. The `try/issue-268` branch is behind main and still holds round one's code, which already files findings from `issues_found` there. The build has to start from main, where the tests fail as they should.

The review lists your nine asks, each matched to a criterion and none missing. I found no problems outside this issue.
