# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37862779490

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (93KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d5bddf03-77ec-4e1e-bd83-2fb0f4e66308/tool-results/b4vdgau0x.txt
> 
> Preview (first 2KB):
> .:
> total 116
> drwxr-xr-x  3 runner runner  4096 Oct  9 00:03 .
> drwxrwxrwt 18 root   root    4096 Oct  9 00:03 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 00:03 in
> -rw-r--r--  1 runner runner 94076 Oct  9 00:03 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 00:03 open_blockers.json
> -rw-r--r--  1 runner runner  7984 Oct  9 00:03 plan.json
> 
> in:
> total 84
> drwxr-xr-x 2 runner runner 4096 Oct  9 00:03 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 00:03 ..
> -rw-r--r-- 1 runner runner 5150 Oct  9 00:03 01-planner.json
> -rw-r--r-- 1 runner runner 4552 Oct  9 00:03 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3910 Oct  9 00:03 03-worker.json
> -rw-r--r-- 1 runner runner 2965 Oct  9 00:03 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 8223 Oct  9 00:03 05-planner.json
> -rw-r--r-- 1 runner runner 4332 Oct  9 00:03 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner  333 Oct  9 00:03 07-not-started.json
> -rw-r--r-- 1 runner runner  325 Oct  9 00:03 08-updater.json
> -rw-r--r-- 1 runner runner 8647 Oct  9 00:03 09-planner.json
> -rw-r--r-- 1 runner runner  325 Oct  9 00:03 10-updater.json
> -rw-r--r-- 1 runner runner  325 Oct  9 00:03 11-updater.json
> -rw-r--r-- 1 runner runner  325 Oct  9 00:03 12-updater.json
> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and l

`2. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^---" issue.md | head -80; wc -l issue.md
```

> 82:## Comments
> 84:### dokima-runtime on issue #268 (2026-10-08T21:27:32Z)
> 88:### dokima-runtime on issue #268 (2026-10-08T21:27:46Z)
> 257:### dokima-runtime on issue #268 (2026-10-08T21:40:31Z)
> 398:### dokima-runtime on issue #268 (2026-10-08T21:43:11Z)
> 403:### dokima-runtime on issue #268 (2026-10-08T21:43:13Z)
> 484:### dokima-runtime on PR #274 (2026-10-08T21:54:27Z)
> 584:### dokima-runtime on issue #268 (2026-10-08T22:03:21Z)
> 782:### dokima-runtime on PR #274 (2026-10-08T22:07:27Z)
> 786:### dokima-runtime on issue #268 (2026-10-08T22:11:55Z)
> 919:### dokima-runtime on PR #274 (2026-10-08T22:13:23Z)
> 923:### dokima-runtime on issue #268 (2026-10-08T22:15:43Z)
> 928:### dokima-runtime on PR #274 (2026-10-08T22:15:45Z)
> 962:### dokima-runtime on PR #274 (2026-10-08T22:19:15Z)
> 966:### dokima-runtime on PR #274 (2026-10-08T22:52:23Z)
> 970:### dokima-runtime on PR #274 (2026-10-08T23:47:03Z)
> 974:### dokima-runtime on issue #268 (2026-10-08T23:47:05Z)
> 1011:### dokima-runtime on issue #268 (2026-10-08T23:47:20Z)
> 1212:### dokima-runtime on PR #274 (2026-10-08T23:51:08Z)
> 1216:### dokima-runtime on issue #268 (2026-10-08T23:51:10Z)
> 1253:### dokima-runtime on PR #274 (2026-10-08T23:56:57Z)
> 1257:### dokima-runtime on issue #268 (2026-10-08T23:57:00Z)
> 1294:### dokima-runtime on PR #274 (2026-10-09T00:02:40Z)
> 1298:### dokima-runtime on issue #268 (2026-10-09T00:02:42Z)
> 1335:### dokima-runtime on issue #268 (2026-10-09T00:03:25Z)
> 1343 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 1,90p issue.md; for r in 398 403 782 919 923 928 962 966 970 1212 1253 1294 1335; do sed -n "${r},$((r+6))p" issue.md; echo ----; done
```

> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> Issues the planner, the worker or the reviewer find outside their own issue are filed on GitHub by code at the end of the run, parked and labeled filed-by-dokima.
> 
> **Work** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Fix why nothing ran
> 
> [PR #274](https://github.com/dokima-dev/dokima/pull/274) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/274/files)
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> <table>
> <tr><td><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"></td><td>The planner's, the worker's and the reviewer's hand-backs all take the same found-i

`4. Bash`
```
cd /tmp/pack; for f in in/*.json; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f'));print(json.dumps(d,indent=1)[:3500])"; done
```

> == in/01-planner.json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37846922154",
>  "commit_before": "ab2dcaaae3c66f963818503ad820e5db0dbdbe33",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 657389,
>   "turns": 28,
>   "cost_usd": 1.9991976000000002,
>   "tokens_in": 2210118,
>   "tokens_out": 32844
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/268/37846922154-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37846922154",
>  "handback": {
>   "kind": "user_story",
>   "summary": "Issues the planner, the worker or the reviewer find outside their own issue are filed on GitHub by code at the end of the run, parked and labeled filed-by-dokima.",
>   "user_story": "Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.",
>   "acceptance_criteria": [
>    {
>     "text": "The planner's, the worker's and the reviewer's hand-backs all take the same found-issues field (issues_found: title, why, evidence), and each agent's prompt describes it. Every issue listed there is filed during that agent's own run, with no command, as its own GitHub issue. The issue takes the finding's title and has exactly two labels, parked and filed-by-dokima, even on a repo that doesn't have those labels yet. A hand-back that lists no issu

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/09-planner.json'));h=d['handback']
for k in h:
  if k not in ('acceptance_criteria','non_functional','user_story','summary'): print(k, json.dumps(h[k],indent=1))
print(d.get('check'))
"; diff <(python3 -c "import json;print(json.dumps(json.load(open('in/09-planner.json'))['handback'],indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1,sort_keys=True))") | head
```

> kind "user_story"
> scope [
>  "dokima/agent.py",
>  "dokima/planner.py",
>  "dokima/roles/planner.md",
>  "dokima/roles/worker.md",
>  "dokima/roles/reviewer.md",
>  ".github/workflows/agent.yml",
>  "AGENTS.md"
> ]
> out_of_scope [
>  "Triaging, prioritizing or planning a filed issue: it stays parked until the owner picks it up.",
>  "A /issue command: filing needs no command now.",
>  "Filing findings from a split's stories or from any run other than the planner, the worker and the reviewer.",
>  "Re-filing or editing an issue Dokima filed earlier when a later run finds it again with a new why."
> ]
> tests {
>  "268.1": [
>   "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled"
>  ],
>  "268.2": [
>   "tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record"
>  ],
>  "268.3": [
>   "tests/test_filed_issues.py::test_a_filed_issue_gets_nothing_more_than_filing"
>  ],
>  "268.4": [
>   "tests/test_filed_issues.py::test_the_same_finding_is_never_filed_twice"
>  ],
>  "268.5": [
>   "tests/test_filed_issues.py::test_the_card_names_each_filed_issue",
>   "tests/test_filed_issues.py::test_a_finding_github_refuses_to_file_says_why_on_the_card"
>  ],
>  "268.6": [
>   "tests/test_filed_issues.py::test_a_rejected_handback_files_nothing"
>  ],
>  "268.7": [
>   "tests/test_filed_issues.py::test_the_key_that_files_is_made_only_after_the_agent_and_the_check"
>  ]
> }
> test_changes {
>  "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled": "Re

**Agent:** I'm checking what the planner changed in its latest run, then running the tests on this branch and on main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8; git diff fbc77f5 6c65b78 --stat; git diff fbc77f5 6c65b78 -- tests/ | head -80
```

> 6c65b78 planner for #268 (run 37861337507)
> fbc77f5 planner for #268 (run 37850995733)
> 50b543c worker for #268 (run 37848732101)
> e1baefe Merge remote-tracking branch 'origin/main' into try/issue-268
> 8f2c6ea planner for #268 (run 37846922154)
> 7961d88 The planner's criteria and docstrings stay short, and a little over the cap never fails a run (#246)
> 50765e4 The owner's ask reads open on the issue they wrote (#249)
> ab2dcaa The all tests check runs main's copy of its workflow, so a pull request can't rewrite its own judge (#263)
>  tests/test_filed_issues.py | 9 +++++----
>  1 file changed, 5 insertions(+), 4 deletions(-)
> diff --git a/tests/test_filed_issues.py b/tests/test_filed_issues.py
> index 87286bb..586bf02 100644
> --- a/tests/test_filed_issues.py
> +++ b/tests/test_filed_issues.py
> @@ -45,7 +45,7 @@ EXISTING = ["autopilot", "blocker", "high"]
>  REFUSED = "HTTP 502: Server Error (https://api.github.com/repos/o/r/issues)"
>  ROLES = ("planner", "worker", "reviewer")
>  WORKFLOWS = ["agent.yml", "assign.yml", "autopilot.yml", "board.yml", "card.yml", "commands.yml", "done-whens.yml",
> -             "full-suite.yml", "planner.yml", "wiki.yml", "worker.yml"]
> +             "full-suite.yml", "planner.yml", "uptodate.yml", "wiki.yml", "worker.yml"]
>  
>  FIND_A = {"title": "The board drops closed pull requests", "why": "Cards for merged work go stale on the board.",
>            "evidence": "dokima/board.py:121 asks only for OPEN pull requests"}
> @@ -214,9 +214,10 @@ def keyed(job):
>  def plan_handback

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git branch -a; git log --oneline -3 origin/main 2>&1; git merge-base --is-ancestor origin/main HEAD && echo main-in; git log --oneline origin/main -12 2>/dev/null | head -12; ls .github/workflows
```

> main
> * try/issue-268
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
>   remotes/origin/issue-116-board-sync
>   remotes/origin/issue-121-needs-you
>   remotes/origin/issue-126-keys-from-main
>   remotes/origin/issue-138-prompt
>   remotes/origin/issue-40-app
>   remotes/origin/issue-46-approve
>   remotes/origin/issue-54-plan
>   remotes/origin/issue-60-wrap
>   remotes/origin/issue-63-latest
>   remotes/origin/issue-67-label
>   remotes/origin/issue-74-layout
>   remotes/origin/issue-78-design
>   remotes/origin/issue-80-planner
>   remotes/origin/issue-81-build-on-main
>   remotes/origin/issue-89-planner-prompt
>   remotes/origin/issue-90-assign
>   remotes/origin/issue-93-terms
>   remotes/origin/logs
>   remotes/origin/main
>   remotes/origin/opus-everywhere
>   remotes/origin/owner-questions
>   remotes/origin/replan-base
>   remotes/origin/replan-own-changes
>   remotes/origin/reviewer-role
>   remotes/origin/river
>   remotes/origin/runtime-from-main
>   remotes/origin/split-filing
>   remotes/origin/try/issue-135
>   remotes/origin/try/issue-139
>   remotes/origin/try/issue-154
>   remotes/origin/try/issue-156
>   remotes/origin/try/issue-157
>   remotes/origin/try/issue-166
>   remotes/origin/try/issue-168
>   remotes/origin/try/issue-170
>   remotes/origin/try/issue-176
>   remotes/o

`8. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wm; git worktree add -q /tmp/wm origin/main 2>&1 | tail -1; cp tests/test_filed_issues.py /tmp/wm/tests/; (cd /tmp/wm && timeout 600 python3 -m pytest -q tests/test_filed_issues.py -x -q 2>&1 | tail -5; timeout 900 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E  .*26[8]\.|[0-9]+ (passed|failed))" | head -30) 
```

> **Next:** @owner-person The hand-back was rejected by code, see the problems above. Fix the cause, then start the stage again.
>   
> assert False
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> E       AssertionError: 268.1 (worker, repo with the labels): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.2 (worker): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.3 (worker on autopilot): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.4: a planner listing a finding twice did not file it exactly once beside the other; filed: []
> E       AssertionError: 268.5 (worker): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.5 (worker, GitHub refuses): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.6 (good worker): code rejected the worker's hand-back, so this case proves nothing:
> E       AssertionError: 268.7 (worker): code rejected the worker's hand-back, so this case proves nothing:
> FAILED tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled - AssertionError: 268.1 (worker, repo with the labels): code rejected the worker's hand-back, so this case proves nothing:
> FAILED tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record - AssertionError: 2

`9. Bash`
```
cd /tmp/wm; timeout 600 python3 -m pytest -q tests/test_filed_issues.py -k "rejected_handback" 2>&1 | grep -iE "error|reject|problem" | head -20
```

> ____________________ test_a_rejected_handback_files_nothing ____________________
> tmp_path = PosixPath('/tmp/pytest-of-runner/pytest-2/test_a_rejected_handback_files0')
>     def test_a_rejected_handback_files_nothing(record_property, tmp_path):
>         """A hand-back that code rejects files none of the issues it lists.
>         verdict code does not accept, each listing two issues, and checks each was rejected and filed nothing; beside each,
>                 wrong.append(f"{case}: the rejected run posted no record:\n{no.tail()}")
>                 wrong.append(f"{case}: a hand-back code rejected filed issues: {titles(no)}")
> >       assert rec["passed"], f"{crit} ({case}): code rejected the {m.role}'s hand-back, so this case proves nothing:\n{rec['body']}"
> E       AssertionError: 268.6 (good worker): code rejected the worker's hand-back, so this case proves nothing:
> E         <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/worker.svg" width="16" height="16" align="absmiddle" alt="worker"> The worker stopped early with its hand-back rejected by code. ([pull request #60](https://github.com/o/r/pull/60))
> E           "problems": [
> E         **Next:** @owner-person The hand-back was rejected by code, see the problems above. Fix the cause, then start the stage again.
> tests/test_filed_issues.py:335: AssertionError
> FAILED tests/test_filed_iss

`10. Bash`
```
cd /tmp/wm; timeout 600 python3 -m pytest -q tests/test_filed_issues.py -k "rejected_handback" 2>&1 | grep -A6 '"problems": \[' | head -20
```

> E           "problems": [
> E            "summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did"
> E           ]
> E          },
> E          "dropped_by_fence": []
> E         }
> E         ```
> --
>     "problems": [
>      "summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did"
>     ]
>    },
>    "dropped_by_fence": []
>   }
>   ```
> Shell cwd was reset to /home/runner/work/dokima/dokima

`11. Bash`
```
cd /tmp/wm; grep -n '"Built it. The fix is in x.py."\|Built it\.' tests/test_filed_issues.py; sed -i 's/summary="Built it. The fix is in x.py."/summary="Built the fix in x.py."/' tests/test_filed_issues.py; timeout 900 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^E  +AssertionError|[0-9]+ (passed|failed)" | head -20
```

> 223:def work_handback(*found, summary="Built it. The fix is in x.py."):
> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E       AssertionError: 268.2: planner: expected 2 filed issues, got []
> E       AssertionError: 268.3: planner: the run did not file its two findings; filed: []
> E       AssertionError: 268.4: a planner listing a finding twice did not file it exactly once beside the other; filed: []
> E       AssertionError: 268.5: planner: the run did not file its two findings; filed: []
> E       AssertionError: 268.5: planner: the card does not say the finding was not filed and GitHub's reason:
> E         - Its own test run: pytest: 1 passed
> E       AssertionError: 268.6: planner: the same agent with a good hand-back did not file its findings; filed: []
> E       AssertionError: 268.7: planner: the run did not file its two findings; filed: []
>   - Its own test run: pytest: 1 passed
> 8 failed in 63.85s (0:01:03)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n 'summary=' tests/test_filed_issues.py; grep -n '"summary"' tests/test_filed_issues.py | head; git worktree remove --force /tmp/wm
```

> 223:def work_handback(*found, summary="Built it. The fix is in x.py."):
> 558:            ("worker", "worker", "pr", work_handback(FIND_A, FIND_B, summary=""), work_handback(FIND_A, FIND_B)),
> 219:    return {**ts.STORY, "summary": "Stuck issues get unstuck.", "links": {"blocked_by": [], "blocks": [], "relates_to": []},
> 227:    return {"summary": summary, "criteria": {"57.1": "x.py"}, "evidence": "pytest: 1 passed",

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned on main after #279: the fake planner's plan in every test now carries empty links, which the planner check from #256 requires.",
          "Added uptodate.yml, from #267, to the list of workflows the rejected hand-back test expects."],
  "decided": ["Kept the five criteria, the two non-functional requirements and every test's checks unchanged."],
  "open": []},
 "verdict": "block",
 "summary": "The plan keeps every ask, but on today's main seven of the eight tests stop at the fake worker's two-sentence summary, which main now rejects, so they fail for the wrong reason and would stay red even with the feature built.",
 "blockers": [{"id": "B1", "criterion": "268.1", "test": "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled",
   "problem": "The fake worker's summary in every test is two sentences. Since #277 (d64ed46), code on main rejects a worker summary of more than one sentence. So every worker case is rejected before any filing is checked. That breaks the proofs of 268.1, 268.2, 268.3, 268.5 (both tests), 268.6 and 268.7, and they would fail on main however good the work is.",
   "evidence": "tests/test_filed_issues.py:223 work_handback(summary=\"Built it. The fix is in x.py.\"). Test file copied onto origin/main (a302cb1), pytest -q tests/test_filed_issues.py: 8 failed, 7 with '268.x (worker...): code rejected the worker's hand-back, so this case proves nothing', problem 'summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did'. Same copy with only that default changed to \"Built the fix in x.py.\": 8 failed, all for the right reason, e.g. '268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []'.",
   "fix": "In tests/test_filed_issues.py work_handback, make the default summary one sentence (e.g. \"Built the
```

> summary holds 41 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="On today's main, seven of eight tests stop at the fake worker's two-sentence summary, so they fail for the wrong reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for #268, and the planner is the one to fix it. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the planner changed this round:** the fake planner's plan in every test now has an empty links field, which main has required since #256. The rejected-hand-back test now expects `uptodate.yml`, which #267 added to main. None of the tests' checks changed. The five criteria and two non-functional requirements still cover every ask, and none is missing.

**Blocker B1:** on today's main, 7 of the 8 tests fail for the wrong reason.
- **Cause:** the fake worker's default summary at `tests/test_filed_issues.py:223` is two sentences ("Built it. The fix is in x.py."). Since #277 merged, main rejects a worker summary longer than one sentence.
- **Effect:** every case that uses the fake worker is rejected before any filing is checked. That breaks the proofs of 268.1, 268.2, 268.3, 268.5 (both tests), 268.6 and 268.7, and those tests would stay red even with the feature fully built.
- **Evidence:** with the test file copied onto the newest main (a302cb1), the result is 8 failed, 7 of them with "code rejected the worker's hand-back, so this case proves nothing". When I changed only that summary to one sentence, all 8 still failed, and every failure was the expected one: nothing is filed yet.
- **Fix:** make the default summary one sentence, list the change in `test_changes`, and check the file again against the newest main. #277, #281 and #286 all merged after this plan was written.

**Note:** this branch hasn't taken in main's latest changes (it has no `uptodate.yml`), so the tests behave differently here than on main. The worker should merge main first next round.
