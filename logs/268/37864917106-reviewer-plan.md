# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37864917106

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (183.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d77e972d-cd2c-43c6-8f78-8d484621643e/tool-results/b8vjgn87k.txt
> 
> Preview (first 2KB):
> total 128
> drwxr-xr-x 2 runner runner  4096 Oct  9 00:28 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 00:28 ..
> -rw-r--r-- 1 runner runner  5150 Oct  9 00:28 01-planner.json
> -rw-r--r-- 1 runner runner  4552 Oct  9 00:28 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  3910 Oct  9 00:28 03-worker.json
> -rw-r--r-- 1 runner runner  2965 Oct  9 00:28 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner  8223 Oct  9 00:28 05-planner.json
> -rw-r--r-- 1 runner runner  4332 Oct  9 00:28 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner   333 Oct  9 00:28 07-not-started.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:28 08-updater.json
> -rw-r--r-- 1 runner runner  8647 Oct  9 00:28 09-planner.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:28 10-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:28 11-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:28 12-updater.json
> -rw-r--r-- 1 runner runner  5440 Oct  9 00:28 13-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11812 Oct  9 00:28 14-planner.json
> -rw-r--r-- 1 runner runner  5673 Oct  9 00:28 15-reviewer-plan.json
> -rw-r--r-- 1 runner runner 15025 Oct  9 00:28 16-planner.json
> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> Issues the planner, the

`2. Bash`
```
cd /tmp/pack; wc -c issue.md; cat open_blockers.json; echo ----; cat plan.json
```

> 170549 issue.md
> [
>  {
>   "id": "B2",
>   "criterion": "268.1",
>   "test": "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled",
>   "problem": "After this plan was written, the owner said #289 replaces the many raise-type fields with two shared ones, raises and answers, and asked to build this toward that shape and add no new raise-type field. The plan still adds issues_found to the planner's and the worker's hand-backs, and its tests require that exact field name in every prompt and fake hand-back, so the worker would be forced to add the new field the owner ruled out.",
>   "evidence": "Owner comment on #268 at 2026-10-09T00:13:00Z: \"Build this toward that shape and add no new raise-type field.\" plan.json 268.1: \"all take the same found-issues field (issues_found: title, why, evidence)\". tests/test_filed_issues.py:220, 228, 234 put issues_found in the planner and worker hand-backs; lines 387-389 fail unless each prompt names \"issues_found\". Neither raises nor #289 appears anywhere in the plan.",
>   "fix": "Re-plan 268.1 and its tests on the owner's comment: carry findings in the shared shape #289 brings (raises) instead of a new issues_found field on the planner and worker, and change the tests that pin issues_found in the prompts and hand-backs. If #289's shape is not settled enough to plan against, ask the owner in the plan's questions which reading to build, rather than keeping issues_found silently.",
>   "fixer": "planner"
>  }
> ]----
> {
>  "k

`3. Bash`
```
cd /tmp/pack; grep -n '^## \|^### \|^---\|^\*\*@\|^> \*\*\|Comment by\|^#### ' issue.md | head -80
```

> 93:## Comments
> 95:### dokima-runtime on issue #268 (2026-10-08T21:27:32Z)
> 99:### dokima-runtime on issue #268 (2026-10-08T21:27:46Z)
> 268:### dokima-runtime on issue #268 (2026-10-08T21:40:31Z)
> 409:### dokima-runtime on issue #268 (2026-10-08T21:43:11Z)
> 414:### dokima-runtime on issue #268 (2026-10-08T21:43:13Z)
> 495:### dokima-runtime on PR #274 (2026-10-08T21:54:27Z)
> 595:### dokima-runtime on issue #268 (2026-10-08T22:03:21Z)
> 793:### dokima-runtime on PR #274 (2026-10-08T22:07:27Z)
> 797:### dokima-runtime on issue #268 (2026-10-08T22:11:55Z)
> 930:### dokima-runtime on PR #274 (2026-10-08T22:13:23Z)
> 934:### dokima-runtime on issue #268 (2026-10-08T22:15:43Z)
> 939:### dokima-runtime on PR #274 (2026-10-08T22:15:45Z)
> 973:### dokima-runtime on PR #274 (2026-10-08T22:19:15Z)
> 977:### dokima-runtime on PR #274 (2026-10-08T22:52:23Z)
> 981:### dokima-runtime on PR #274 (2026-10-08T23:47:03Z)
> 985:### dokima-runtime on issue #268 (2026-10-08T23:47:05Z)
> 1022:### dokima-runtime on issue #268 (2026-10-08T23:47:20Z)
> 1223:### dokima-runtime on PR #274 (2026-10-08T23:51:08Z)
> 1227:### dokima-runtime on issue #268 (2026-10-08T23:51:10Z)
> 1264:### dokima-runtime on PR #274 (2026-10-08T23:56:57Z)
> 1268:### dokima-runtime on issue #268 (2026-10-08T23:57:00Z)
> 1305:### dokima-runtime on PR #274 (2026-10-09T00:02:40Z)
> 1309:### dokima-runtime on issue #268 (2026-10-09T00:02:42Z)
> 1346:### dokima-runtime on issue #268 (2026-10-09T00:03:25Z)
> 1492:### dokima-runtime on issue #268 (2026-10-09T00:07:21Z)
> 1701:###

`4. Bash`
```
cd /tmp/pack; sed -n 1,95p issue.md | cut -c1-1500; echo; sed -n 1700,1706p issue.md
```

> # Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 
> <!-- dokima-card -->
> Issues the planner, the worker or the reviewer find outside their own issue are filed on GitHub by code at the end of the run, parked and labeled filed-by-dokima.
> 
> **Plan**
> 
> [issue #268](https://github.com/dokima-dev/dokima/issues/268) · [PR #274](https://github.com/dokima-dev/dokima/pull/274) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/274/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #265, #193, #269
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue as soon as its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** The planner's, the

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['in/13-reviewer-plan.json','in/15-reviewer-plan.json']:
  d=json.load(open(f)); print(f); print(json.dumps(d,indent=1)[:6000])
"
```

> in/13-reviewer-plan.json
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37862779490",
>  "commit_before": "6c65b788e7c75f2b2ebd8e91b80d5535685e2911",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 188740,
>   "turns": 15,
>   "cost_usd": 0.6171674000000001,
>   "tokens_in": 690345,
>   "tokens_out": 6166
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/268/37862779490-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37862779490",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "Re-planned on main after #279: the fake planner's plan in every test now carries empty links, which the planner check from #256 requires.",
>     "Added uptodate.yml, from #267, to the list of workflows the rejected hand-back test expects."
>    ],
>    "decided": [
>     "Kept the five criteria, the two non-functional requirements and every test's checks unchanged."
>    ],
>    "open": []
>   },
>   "verdict": "block",
>   "summary": "On today's main, seven of eight tests stop at the fake worker's two-sentence summary, so they fail for the wrong reason.",
>   "blockers": [
>    {
>     "id": "B1",
>     "criterion": "268.1",
>     "test": "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled",
>     "problem": "The fake worker's summary in every test is two sentences. Since #277 (d64ed46), code on main rejects a worker summary of more than one sentence. So every worker case is rejected before 

**Agent:** Reading the plan and the owner's newest comment; next I run the planner's tests against main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -2; git log --oneline -3 origin/main; git merge-base --is-ancestor origin/main HEAD && echo uptodate; git diff --stat origin/main...HEAD | tail -5; grep -rn "289\|raises" dokima AGENTS.md | head -20
```

> a302cb1 The Autopilot view shows only open issues and pull requests (#286)
> 1c8e0e0 The issue card and the planner's run comment show the links, each kind with its own icon (#281)
> d64ed46 Every card opens with one short plain sentence, and the worker's docstrings are checked too (#277)
>  dokima/roles/planner.md    |   3 +
>  dokima/roles/reviewer.md   |   5 +-
>  dokima/roles/worker.md     |   7 +-
>  tests/test_filed_issues.py | 639 +++++++++++++++++++++++++++++++++++++++++++++
>  7 files changed, 763 insertions(+), 15 deletions(-)
> AGENTS.md:42:- **Planner:** turns a rough issue into a plan: an objective, acceptance criteria, scope, and a test for every criterion written before any code. It judges the ask first and raises a concern only with evidence. It may change or delete an older test when the plan makes it wrong, with a reason the owner sees. It proposes splits; it never writes code.
> dokima/board.py:70:    """One REST call; raises subprocess.CalledProcessError when GitHub refuses it."""

`7. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/m; git worktree add -q /tmp/m origin/main 2>&1|tail -1; cp tests/test_filed_issues.py /tmp/m/tests/; cd /tmp/m && timeout 900 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^E .*268|passed|failed" | head -40
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

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "issues_found\|kind\|def \|raised" tests/test_filed_issues.py | head -80
```

> 6:field, raises, the shared field #289 brings: each found issue is a raise of kind issue ({kind: "issue", title, why,
> 8:that shape and add no new raise-type field, so no hand-back gains an issues_found field.
> 61:PLANNER_TEST = '''def test_a(record_property):
> 73:def save_filed():
> 76:def filed_labels(i):
> 78:def filed_obj(i):
> 83:def new_filed(title, body, labels):
> 92:def filed_list(want, st):
> 94:def split_labels(vals):
> 96:def file_body(v):
> 187:def fake_gh():
> 201:def keyed(job):
> 216:def raised(found):
> 217:    """These findings as raises of kind issue, the shape #289 gives every hand-back."""
> 218:    return [{"kind": "issue", **f} for f in found]
> 221:def plan_handback(*found, tests=True):
> 227:            "raises": raised(found), "_tests": tests}
> 230:def work_handback(*found, summary="Built the fix in x.py."):
> 235:            "raises": raised(found)}
> 238:def plan_review(*found, verdict="approve"):
> 241:            "raises": raised(found)}
> 244:def code_review(*found):
> 246:    return {**tam.review_pr("approve"), "raises": raised(found)}
> 257:    def __init__(self, tmp, stage, labels=None, repo_labels=None, options=None):
> 277:    def base_env(self, event_name):
> 283:    def run(self, role, handback):
> 310:    def filed(self):
> 319:    def close_filed(self, number):
> 327:    def record(self):
> 328:        """The comment carrying the newest run's record, as it stands now: {id, kind, number, body, passed}, or None."""
> 333:                return {"id": c["id"], "kind": c["kind"], "number": c["nu

`9. Bash`
```
cd /tmp/pack; grep -o 'issues/268#issuecomment-[0-9]*' issue.md | sort -u | head; grep -n "issuecomment" in/16-planner.json | head -3; sed -n 1705,1720p issue.md | cut -c1-400
```

> ### dokima-runtime on issue #268 (2026-10-09T00:18:15Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> The reviewer blocked the plan on 1 criterion.
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **B2** (268.1, the planner fixes it): After this plan was written, the owner said #289 replaces the many raise-type fields with two shared ones, raises and answers, and asked to build this toward that shape and add no new raise-type field. The plan 
> 
> <details><summary><b>Details</b></summary>
> 
> - The test fix holds on main, but the plan still adds an issues_found field the owner's newest comment rules out.
> - B2 on 268.1: After this plan was written, the owner said #289 replaces the many raise-type fields with two shared ones, raises and answers, and asked to build this toward that shape and add no new raise-type field. The plan still adds issues_found to the planner's and the worker's hand-backs, and its tests require that exact field name in every prompt and fake hand-back, so the worker would be f
> - B1
> 
> </details>
> 
> <details><summary><b><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/do

`10. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/15-reviewer-plan.json'))['handback']
asks=prev['asks']
for a in asks:
    if a['criterion']=='missing': a['criterion']='268.1'
L="https://github.com/dokima-dev/dokima/issues/268"
r={"previous_step":{
 "did":["Moved found issues in 268.1 and every test from an issues_found field to raises of kind issue, the shared field #289 brings.",
        "Added checks that a planner or worker handing findings back in issues_found, or as a raise of another kind, files nothing, and that no prompt still names issues_found."],
 "decided":["Kept the five criteria' other promises, the two non-functional requirements and the scope unchanged, and left the other raise kinds and answers to #289."],
 "open":["Asks whether the reviewer's found issues also move from issues_found into raises now; planned for yes."]},
 "verdict":"approve",
 "summary":"The plan now carries found issues in #289's shared raises field as the owner asked, and all eight tests fail on main only because filing is missing.",
 "blockers":[],
 "notes":[
  {"text":"Nothing checks that a reviewer still handing findings back in its old issues_found field files nothing, though 268.1 says a finding handed back any other way is not filed; if the owner answers yes to the question, the worker could keep filing the reviewer's issues_found and still pass.",
   "evidence":"tests/test_filed_issues.py:397-400 try issues_found and a blocker raise only for the planner and the worker."},
  {"text":"This branch is still behind main and already holds round one's prompt changes; the next build should merge main first, since the tests only fail for the right reason on main's newest code.",
   "evidence":"git merge-base --is-ancestor origin/main HEAD fails; git diff origin/main...HEAD changes dokima/roles/*.md."}],
 "resolved":["B2"],
 "issues_found":[],
 "asks":asks,
 "assumptions":[{"question":"Should the reviewer's
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="The plan now carries found issues in #289's shared raises field, and all eight tests fail on main only because filing is missing."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; git worktree remove --force /tmp/m
```

> rc=0

**Agent:** I approved the plan for issue #268. The review is in `/tmp/dokima-out/review.json` and passes both checks.

- **Last open blocker (B2) is fixed.** You said to build toward #289's shared raises field and add no new raise-type field. The plan now does that: the planner, the worker and the reviewer hand back found issues as raises of kind issue, not in an issues_found field. A planner or worker that uses issues_found, or raises a finding as another kind, files nothing. The tests also fail if any agent's instructions still name issues_found.
- **The tests fail for the right reason.** I put the planner's test file onto the newest main and ran it. All 8 tests fail only because filing doesn't exist yet: nothing gets filed, the cards don't name filed issues, and the instructions don't describe raises.
- **Every ask is covered.** Every ask in the issue maps to a criterion, including your comment about #289.

**One question waits for you.** The planner asks whether the reviewer's found issues should move from its existing issues_found field into raises now, and it planned for yes. I didn't accept that on your behalf. It changes the reviewer's output on every run before #289 lands, and your comment doesn't say whether this issue should do that. So the plan stops for your answer. The tests are already written for "yes": they fail if the reviewer's instructions still mention issues_found.

**Two notes, neither blocking:**
- No test checks that a reviewer using the old issues_found field files nothing. Only the planner and the worker are tested that way. If you answer yes, the worker could keep filing the reviewer's issues_found and still pass.
- The branch `try/issue-268` is behind main and still has the instruction changes from the first round of work. The next build should merge main first, because the tests only fail for the right reason on main's newest code.
