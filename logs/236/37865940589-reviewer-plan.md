# reviewer (plan) for #236

Run: https://github.com/dokima-dev/dokima/actions/runs/37865940589

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (162.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tool-results/bw8un5ile.txt
> 
> Preview (first 2KB):
> .:
> total 196
> drwxr-xr-x  3 runner runner   4096 Oct  9 00:40 .
> drwxrwxrwt 18 root   root     4096 Oct  9 00:40 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 00:40 in
> -rw-r--r--  1 runner runner 164421 Oct  9 00:40 issue.md
> -rw-r--r--  1 runner runner    910 Oct  9 00:40 open_blockers.json
> -rw-r--r--  1 runner runner  12897 Oct  9 00:40 plan.json
> 
> in:
> total 100
> drwxr-xr-x 2 runner runner  4096 Oct  9 00:40 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 00:40 ..
> -rw-r--r-- 1 runner runner  8734 Oct  9 00:40 01-planner.json
> -rw-r--r-- 1 runner runner  7692 Oct  9 00:40 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10041 Oct  9 00:40 03-planner.json
> -rw-r--r-- 1 runner runner  6349 Oct  9 00:40 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  4281 Oct  9 00:40 05-worker.json
> -rw-r--r-- 1 runner runner  3309 Oct  9 00:40 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 12547 Oct  9 00:40 07-planner.json
> -rw-r--r-- 1 runner runner  7179 Oct  9 00:40 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13586 Oct  9 00:40 09-planner.json
> # Issue #236: Run comments show only what has something, in the owner's words, with no codes
> 
> <!-- dokima-card -->
> Run comments show each field only when it has something, in one style for every agent, with reviews giving verdict and failures pl

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json
```

> [
>  {
>   "id": "B2",
>   "criterion": "236.2",
>   "test": null,
>   "problem": "The owner asked, after the last plan review, that this story add no new raise-type field and build toward the shared raises and answers of #289. No criterion keeps that promise (236.2, on fields, comes closest but covers only how they are drawn), and no test would turn red if the work added such a field.",
>   "evidence": "Owner's comment on #236 of 2026-10-09T00:13:01Z: \"Build this toward that shape and add no new raise-type field.\" plan.json: no criterion or non-functional requirement mentions raise-type fields; #289 appears only in links.relates_to.",
>   "fix": "Add a non-functional requirement traced to that comment, for example: no hand-back gains a new raise-type field (the fields the hand-back check reads stay those on main), with a test that fails if the check or the comment reads a new one.",
>   "fixer": "planner"
>  }
> ]
> {
>  "kind": "user_story",
>  "summary": "Run comments show each field only when it has something, in one style for every agent, with reviews giving verdict and failures plainly.",
>  "user_story": "Every run comment shows only what the owner needs, each field drawn the same way by every agent: a plan's criteria with proof and source, a review's verdict and failures in plain words, the worker's files on one line, and the stats folded away.",
>  "acceptance_criteria": [
>   {
>    "text": "A review run is called Plan review or Code review on its live card and run comment, never Reviewer (plan), 

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^---\|Comment by\|^\*\*@" issue.md | head -100
```

> 96:## Comments
> 98:### RezaSoleymanifar on issue #236 (2026-10-08T18:43:02Z)
> 102:### RezaSoleymanifar on issue #236 (2026-10-08T19:14:16Z)
> 109:### dokima-runtime on issue #236 (2026-10-08T21:43:57Z)
> 113:### dokima-runtime on issue #236 (2026-10-08T21:44:08Z)
> 321:### dokima-runtime on issue #236 (2026-10-08T22:16:49Z)
> 542:### RezaSoleymanifar on issue #236 (2026-10-08T23:45:03Z)
> 548:### dokima-runtime on issue #236 (2026-10-08T23:45:21Z)
> 772:### dokima-runtime on issue #236 (2026-10-08T23:55:25Z)
> 980:### dokima-runtime on issue #236 (2026-10-08T23:57:02Z)
> 985:### dokima-runtime on issue #236 (2026-10-08T23:57:04Z)
> 1081:### dokima-runtime on PR #287 (2026-10-09T00:10:35Z)
> 1183:### RezaSoleymanifar on issue #236 (2026-10-09T00:13:01Z)
> 1187:### dokima-runtime on issue #236 (2026-10-09T00:16:54Z)
> 1422:### dokima-runtime on issue #236 (2026-10-09T00:23:46Z)
> 1653:### dokima-runtime on issue #236 (2026-10-09T00:31:03Z)
> 1900:### dokima-runtime on issue #236 (2026-10-09T00:40:07Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 60,112p issue.md; sed -n 540,548p issue.md; sed -n 1180,1190p issue.md; sed -n 1650,1665p issue.md; sed -n 1895,1920p issue.md
```

> - The worker's replies keep naming the blocker they answer, since they answer the review by id.
> - Comments of runs that never started, or were cancelled before their agent started, keep their No agent ran line: they have no stats.
> 
> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37864538531/job/113608012760"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <a href="https://github.com/dokima-dev/dokima/actions/runs/37863415920"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 3</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and n

`5. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('08-reviewer-plan.json'));print(json.dumps(d,indent=1)[:9000])"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37864554184",
>  "commit_before": "a8a2dcf4b57ae7d634b737fe1602cc6a558a3224",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 393864,
>   "turns": 18,
>   "cost_usd": 0.6762634,
>   "tokens_in": 800471,
>   "tokens_out": 7862
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/236/37864554184-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37864554184",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner deleted the three tests of the Answered from your words section and the autopilot test that showed the owner's matched words on a review's card, each with its reason.",
>     "The planner listed #289 as a related issue."
>    ],
>    "decided": [
>     "A review's comment shows only the questions it could not confirm, so the tests of accepted questions go."
>    ],
>    "open": [
>     "The owner's ask on #289, to add no new raise-type field, has no criterion or test in the plan."
>    ]
>   },
>   "verdict": "block",
>   "summary": "The plan fixes the old tests that blocked the work, but has no criterion for the owner's newest ask: add no new raise-type field.",
>   "blockers": [
>    {
>     "id": "B2",
>     "criterion": "236.2",
>     "test": null,
>     "problem": "The owner asked, after the last plan review, that this story add no new raise-type field and build toward the shared raises and answers of #289. No criterion keeps that promise (236.2, on f

**Agent:** I'm reviewing the planner's fix for blocker B2 (the "no new raise-type field" ask). Next I'll run the new test on main and on the branch.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff HEAD~1 --stat; grep -n "def test_no_hand_back_gains" -A80 tests/test_run_comment_fields.py
```

> 936f0d8 planner for #236 (run 37865186115)
> a8a2dcf planner for #236 (run 37863965870)
> ee7acaa worker for #236 (run 37862227884)
>  tests/test_run_comment_fields.py | 62 ++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 62 insertions(+)
> 653:def test_no_hand_back_gains_a_new_raise_type_field(record_property, run):
> 654-    """Run comments are drawn from the fields agents hand back today, never a new one.
> 655-
> 656-    Reads every field name dokima/agent.py reads and checks the only new ones since main are the two this story keeps
> 657-    in the record (the worker's files changed and each test's Verified by line), so no raise-type field is added
> 658-    ahead of #289's raises and answers. Then hands back a planner, a worker and a review that also carry raises and
> 659-    answers, and checks those never show while today's question, blocker and issue found still do. Proves 236.9."""
> 660-    record_property("proves", "236.9")
> 661-    path = os.path.join(os.path.dirname(__file__), "..", "dokima", "agent.py")
> 662-    new = fields_read(path) - FIELDS_READ_ON_MAIN
> 663-    assert not new - RECORD_FIELDS_THIS_STORY_ADDS, \
> 664-        f"236.9: dokima/agent.py reads fields main never had, so a hand-back gained a field: {sorted(new - RECORD_FIELDS_THIS_STORY_ADDS)}"
> 665-    assert RECORD_FIELDS_THIS_STORY_ADDS <= new, \
> 666-        f"236.9: the record does not yet keep the worker's files changed and each test's Verified by line " \
> 667-        f"(files_changed, verified_by); dokima/age

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "FIELDS_READ_ON_MAIN\|RECORD_FIELDS_THIS_STORY_ADDS\|def fields_read" -A14 tests/test_run_comment_fields.py | head -60
```

> 621:FIELDS_READ_ON_MAIN = {
> 622-    "BASE", "BODY", "CARD_ID", "DOKIMA_BOARD", "DOKIMA_BOT", "GITHUB_ACTOR", "GITHUB_REPOSITORY", "GITHUB_RUN_ID",
> 623-    "GITHUB_SERVER_URL", "HEAD", "LOG_URL", "NUMBER", "ON_PR", "OWNERS", "PACK", "PLANNER_BASE", "ROLE", "STAGE",
> 624-    "acceptance_criteria", "accepted", "agent_started", "answer", "ask", "asks", "assumption", "assumptions", "attempt",
> 625-    "author", "base", "blocked_by", "blocker", "blockers", "body", "cache_creation_input_tokens",
> 626-    "cache_read_input_tokens", "change", "changes", "check", "check_runs", "command", "comments", "concerns",
> 627-    "conclusion", "content", "context", "cost_usd", "createdAt", "created_at", "criteria", "criterion", "depends_on",
> 628-    "dropped_by_fence", "duration_ms", "evidence", "feature", "file", "file_path", "filename", "files", "fix", "fixer",
> 629-    "handback", "headRefName", "id", "input", "input_tokens", "issue", "issues_found", "kind", "labels", "line",
> 630-    "links", "log", "login", "matched", "merge", "merged_pr", "message", "model", "models", "name", "non_functional",
> 631-    "notes", "num_turns", "number", "original_line", "out_of_scope", "output_tokens", "outside_plan", "outside_scope",
> 632-    "passed", "path", "pattern", "pr", "previous_step", "principle", "problem", "problems", "question", "questions",
> 633-    "replies", "report", "resolved", "reviews", "role", "run", "run_id", "scope", "source", "stage", "state", "status",
> 634-    "statuses", "stories", "story", "

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import sys,subprocess; sys.path.insert(0,'tests')
import importlib.util
spec=importlib.util.spec_from_file_location('t','tests/test_run_comment_fields.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
src=subprocess.check_output(['git','show','origin/main:dokima/agent.py']).decode()
open('/tmp/main_agent.py','w').write(src)
mf=m.fields_read('/tmp/main_agent.py')
print('missing from const',sorted(mf-m.FIELDS_READ_ON_MAIN)); print('extra in const',sorted(m.FIELDS_READ_ON_MAIN-mf))
print('branch new',sorted(m.fields_read('dokima/agent.py')-mf))
EOF
pytest -q 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bbei6yj40). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`9. Bash`
```
head -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output
```

> missing from const []
> extra in const []
> branch new ['files_changed', 'verified_by']

**Agent:** Main's field list matches the test exactly. Now I'll run the new tests against main's code.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt origin/main 2>&1|tail -1; cp -r tests/. /tmp/mainwt/tests/; cd /tmp/mainwt; timeout 300 python3 -m pytest -q tests/test_run_comment_fields.py 2>&1 | grep -E "236\.|passed|failed" | grep -E "^FAILED|^E .*236\.9|passed|failed" | head -30
```

> body = run("worker", "", dict(hb, evidence=evidence), passed=False, problems="evidence is empty\n")[0]
> E                     The reviewer passed the plan. Details - Every ask is kept and proven zq. Notes - A note on naming zq. (jobs.py:3) The owner's asks - Give back a job id at once (77.1, https://github.com/o/r/issues/77) - Keep each result for a day (77.2, https://github.com/o/r/issues/77#issuecomment-501) What the previous step did - Did: Built the jobs queue zq. - Decided: Kept the old endpoint zq. - Still open: The retry rule zq. Opus 5.5 · 4.0 min · 23 turns · 401,000 tokens in, 18,000 out · $3.20 at API prices · conversation · run
> E             <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> E            +  where None = <function search at 0x7f93c9df3060>((('<img\\ src="https://raw\\.githubusercontent\\.com/o/r/main/dokima/icons/none\\.svg"\\ width="16"\\ height="16"\\ align="absmiddle"\\ alt="not\\ started">' + '(?:\\s|<[^>]+>|-)*') + 'A\\ slow\\ call\\ returns\\ a\\ job\\ id\\ within\\ 2\\ s\\.'), '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...00 out · $3.20 at API prices · [conversation](https://g/log.md) · [run](https://github.com/o/r/actions/r

**Agent:** 236.9 fails on main for the right reason: the record doesn't keep the two new fields yet. Now waiting on the full suite run on the branch.

`11. Bash`
```
cd /tmp/mainwt; timeout 300 python3 -m pytest -q tests/test_run_comment_fields.py 2>&1 | tail -1; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/mainwt; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output
```

> 13 failed in 0.62s
> missing from const []
> extra in const []
> branch new ['files_changed', 'verified_by']

`12. Bash`
```
sleep 100; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output
```

> <tool_use_error>Blocked: sleep 100 followed by: tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

**Agent:** Meanwhile I'll write the hand-back.

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added a requirement that no hand-back gains a new raise-type field, with a test that fails if the comment code reads any field main does not, beyond the worker's files changed and each test's Verified by line.",
          "The test also hands back raises and answers from each agent and checks neither shows in a run comment."],
  "decided": ["The only new fields the record keeps are the worker's files changed and each test's Verified by line; replacing the raise-type fields with raises and answers stays with #289."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now keeps the owner's newest ask, to add no new raise-type field, with a test that turns red if one is added, and every ask has a proven criterion.",
 "blockers": [],
 "notes": [
  {"text": "The new raise-type test lists exactly the fields main reads today, and on the branch the work reads only the two new record fields the plan names; it fails on main only because those two are not kept yet.",
   "evidence": "fields_read(main dokima/agent.py) equals FIELDS_READ_ON_MAIN; branch adds ['files_changed', 'verified_by']; tests/test_run_comment_fields.py on main: 13 failed, 236.9 with 'the record does not yet keep the worker's files changed and each test's Verified by line'"},
  {"text": "Linking each issue found to the issue filed for it is left to #268; AGENTS.md asks for a short comment on each side when scope moves between issues.",
   "evidence": "plan.json concerns[0]; AGENTS.md, Changing scope"}],
 "resolved": ["B2"],
 "issues_found": [],
 "asks": [
  {"ask": "The live card and the record say Plan review where they said Reviewer (plan), and Code review where they said Reviewer (pr).", "source": "https://github.com/dokima-dev/dokima/issues/236", "criterion": "236.1"},
  {"ask": "A run comment shows each of these only when it has something, and never a blank heading or empty section", "s
```

> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now keeps the owner's newest ask, add no new raise-type field, with a test that turns red if one is added."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output
```

> rc=0
> missing from const []
> extra in const []
> branch new ['files_changed', 'verified_by']

`15. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`16. Bash`
```
until grep -qE "passed|failed|error" /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output; do sleep 2; done; tail -3 /tmp/claude-1001/-home-runner-work-dokima-dokima/7a7be855-f665-44f5-b5cd-9fc6241110bd/tasks/bbei6yj40.output
```

> 606 passed in 307.58s (0:05:07)
> 
> [exited with code 0]

`17. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["notes"][0]["evidence"]+="; pytest -q on try/issue-236: 606 passed"
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #236. The only open blocker from last round, B2, is fixed. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**B2 fixed:** your comment of 2026-10-09T00:13 asked this story to "add no new raise-type field". The plan now keeps that promise as a new requirement, 236.9, with its own test in `tests/test_run_comment_fields.py:653`. I checked that the test does the job:
- **It covers every field:** its list of fields that main reads today matches what main's `dokima/agent.py` reads, with nothing missing or extra.
- **It goes red on a new field:** it fails if the code reads any field main doesn't, except the two this story needs: the worker's files changed and each test's Verified by line.
- **Raises and answers stay hidden:** it hands back `raises` and `answers` from each agent and checks neither appears in a run comment, while today's question, blocker and issue found still do.
- **On the branch:** the worker's code adds only those two fields.

**Test runs:**
- **On main:** all 13 new tests fail because the feature is missing. The 236.9 test fails because the record doesn't keep the two new fields yet.
- **On the branch:** the full suite passes (606 tests).

Every ask in the issue and its comments now matches a criterion, so none are marked missing. I left two notes and no blockers:
1. The finding above about how the 236.9 test works.
2. Linking each issue found to the issue filed for it is left to #268. AGENTS.md wants a short comment on each issue when scope moves between them.
