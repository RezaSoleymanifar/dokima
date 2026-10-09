# reviewer (plan) for #236

Run: https://github.com/dokima-dev/dokima/actions/runs/37891360747

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (212.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6c98fe72-0db2-4456-8e1d-662ef6cb20c9/tool-results/byq5x8za8.txt
> 
> Preview (first 2KB):
> .:
> total 244
> drwxr-xr-x  3 runner runner   4096 Oct  9 06:01 .
> drwxrwxrwt 18 root   root     4096 Oct  9 06:01 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 06:01 in
> -rw-r--r--  1 runner runner 216131 Oct  9 06:01 issue.md
> -rw-r--r--  1 runner runner      2 Oct  9 06:01 open_blockers.json
> -rw-r--r--  1 runner runner  12307 Oct  9 06:01 plan.json
> 
> in:
> total 140
> drwxr-xr-x 2 runner runner  4096 Oct  9 06:01 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 06:01 ..
> -rw-r--r-- 1 runner runner  8734 Oct  9 06:01 01-planner.json
> -rw-r--r-- 1 runner runner  7692 Oct  9 06:01 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10041 Oct  9 06:01 03-planner.json
> -rw-r--r-- 1 runner runner  6349 Oct  9 06:01 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  4281 Oct  9 06:01 05-worker.json
> -rw-r--r-- 1 runner runner  3309 Oct  9 06:01 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 12547 Oct  9 06:01 07-planner.json
> -rw-r--r-- 1 runner runner  7179 Oct  9 06:01 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13586 Oct  9 06:01 09-planner.json
> -rw-r--r-- 1 runner runner  6591 Oct  9 06:01 10-reviewer-plan.json
> -rw-r--r-- 1 runner runner  2421 Oct  9 06:01 11-worker.json
> -rw-r--r-- 1 runner runner  1752 Oct  9 06:01 12-reviewer-pr.json
> -rw-r--r-- 1 runner runner   319 Oct  9 06:01 13-u

**Agent:** The issue is huge. Let me look at the owner's original ask (below the marker) and recent comments.

`2. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|dokima-owner\|^---" issue.md | head -100; wc -l issue.md
```

> 99:## Comments
> 101:### RezaSoleymanifar on issue #236 (2026-10-08T18:43:02Z)
> 105:### RezaSoleymanifar on issue #236 (2026-10-08T19:14:16Z)
> 112:### dokima-runtime on issue #236 (2026-10-08T21:43:57Z)
> 116:### dokima-runtime on issue #236 (2026-10-08T21:44:08Z)
> 324:### dokima-runtime on issue #236 (2026-10-08T22:16:49Z)
> 545:### RezaSoleymanifar on issue #236 (2026-10-08T23:45:03Z)
> 551:### dokima-runtime on issue #236 (2026-10-08T23:45:21Z)
> 775:### dokima-runtime on issue #236 (2026-10-08T23:55:25Z)
> 983:### dokima-runtime on issue #236 (2026-10-08T23:57:02Z)
> 988:### dokima-runtime on issue #236 (2026-10-08T23:57:04Z)
> 1084:### dokima-runtime on PR #287 (2026-10-09T00:10:35Z)
> 1186:### RezaSoleymanifar on issue #236 (2026-10-09T00:13:01Z)
> 1190:### dokima-runtime on issue #236 (2026-10-09T00:16:54Z)
> 1425:### dokima-runtime on issue #236 (2026-10-09T00:23:46Z)
> 1656:### dokima-runtime on issue #236 (2026-10-09T00:31:03Z)
> 1903:### dokima-runtime on issue #236 (2026-10-09T00:40:07Z)
> 2121:### dokima-runtime on issue #236 (2026-10-09T00:46:19Z)
> 2126:### dokima-runtime on PR #287 (2026-10-09T00:46:21Z)
> 2197:### dokima-runtime on PR #287 (2026-10-09T00:50:59Z)
> 2288:### dokima-runtime on PR #287 (2026-10-09T05:51:03Z)
> 2292:### dokima-runtime on issue #236 (2026-10-09T05:51:05Z)
> 2329:### dokima-runtime on issue #236 (2026-10-09T05:51:20Z)
> 2570:### dokima-runtime on PR #287 (2026-10-09T06:00:37Z)
> 2574:### dokima-runtime on issue #236 (2026-10-09T06:00:40Z)
> 2611:### dokima-runtime on issue #236 

`3. Bash`
```
cd /tmp/pack; sed -n 1,112p issue.md; sed -n 545,551p issue.md; sed -n 1186,1190p issue.md; sed -n 2288,2330p issue.md; sed -n 2570,2619p issue.md
```

> # Issue #236: Run comments show only what has something, in the owner's words, with no codes
> 
> <!-- dokima-card -->
> Run comments show each field only when it has something, in one style for every agent, with reviews giving verdict and failures plainly.
> 
> **Review** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See why not every check passed
> 
> [issue #236](https://github.com/dokima-dev/dokima/issues/236) · [PR #287](https://github.com/dokima-dev/dokima/pull/287) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/287/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #183
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #268, #243, #230, #289
> 
> **User story:** Every run comment shows only what the owner needs, each field drawn the same way by every agent: a plan's criteria with proof and source, a review's verdict and failures in plain words, the worker's files on one line, and the stats folded away.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/do

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; python3 -c "
import json
for f in ['10-reviewer-plan.json','12-reviewer-pr.json','14-planner.json']:
  d=json.load(open('in/'+f)); print(f, json.dumps(d,indent=1)[:5000]); print('-----')
"
```

> {
>  "kind": "user_story",
>  "summary": "Run comments show each field only when it has something, in one style for every agent, with reviews giving verdict and failures plainly.",
>  "user_story": "Every run comment shows only what the owner needs, each field drawn the same way by every agent: a plan's criteria with proof and source, a review's verdict and failures in plain words, the worker's files on one line, and the stats folded away.",
>  "acceptance_criteria": [
>   {
>    "text": "A review run is called Plan review or Code review on its live card and run comment, never Reviewer (plan), Reviewer (pr) or The reviewer.",
>    "source": "https://github.com/dokima-dev/dokima/issues/236"
>   },
>   {
>    "text": "Each field of a run comment shows only when it has something, and a field two agents share looks the same from both. The optional fields are the worker's suspect tests, changes outside scope, replies to blockers and test result line, a review's changes outside the plan, questions and issues found, and the planner's questions. Nothing shows as a blank heading or an empty fold. The worker's changes outside scope and a review's changes outside the plan are drawn as one Outside the plan fold with the same icon, label and lines. A review's questions are drawn exactly like the planner's Questions for you. A review's comment no longer shows What the previous step did, Details or Notes; an escalation still shows its summary, the reason it reaches the owner.",
>    "source": "https://github.com

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/09-planner.json'))['handback']; b=json.load(open('plan.json'))
for k in set(a)|set(b):
  if a.get(k)!=b.get(k): print('DIFF',k); print(' OLD',json.dumps(a.get(k))[:3000]); print(' NEW',json.dumps(b.get(k))[:3000])
"; python3 -c "
import json;d=json.load(open('in/14-planner.json'));print(d.get('check'));print(d['handback'].get('replies'))"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- AGENTS.md | head -80
```

> DIFF replies
>  OLD [{"blocker": "B2", "answer": "fixed", "why": "Added non-functional requirement 236.9, traced to the owner's comment of 2026-10-09T00:13: no hand-back gains a new raise-type field. tests/test_run_comment_fields.py::test_no_hand_back_gains_a_new_raise_type_field reads every field name dokima/agent.py reads and fails on any beyond main's, other than the two record fields this story adds (files_changed, verified_by); it also hands back raises and answers from each agent and fails if either shows in a comment, while today's question, blocker and issue found still show. It fails on main because the record does not yet keep those two fields."}]
>  NEW []
> DIFF non_functional
>  OLD [{"text": "The full JSON record stays in the last fold of every run comment, right under the stats, and reads back exactly.", "why": "later packs are rebuilt from the records, and tests/test_run_cards.py already pins the record as the last fold", "principle": "Everything lives on GitHub"}, {"text": "A blocker the plan cannot place, or a review with no plan to read, still shows why it fails, without a blocker code.", "why": "a failure the comment leaves out would read as a pass", "principle": "Fail closed"}, {"text": "No hand-back gains a new raise-type field. The only new fields code reads are the two this story keeps in the run's record: files_changed (the worker's files changed) and verified_by (each test's Verified by line). A hand-back that also carries raises or answers shows neither in 

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_run_comment_fields.py; git log --oneline -8 --graph; git cat-file -t e934cfe 2>&1; git branch -a; git merge-base --is-ancestor 65edcee HEAD && echo has307
```

> Exit code 1
> commit f2ffd162ce95ffc45c7463ad3f9f625823a8a47e
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 06:00:49 2026 +0000
> 
>     planner for #236 (run 37890549750)
> 
> diff --git a/tests/test_run_comment_fields.py b/tests/test_run_comment_fields.py
> index 1257a42..1e65377 100644
> --- a/tests/test_run_comment_fields.py
> +++ b/tests/test_run_comment_fields.py
> @@ -618,61 +618,86 @@ def test_a_blocker_the_plan_cannot_place_still_shows_why(record_property, run):
>  
>  # 236.9: no new raise-type field
>  
> -FIELDS_READ_ON_MAIN = {
> -    "BASE", "BODY", "CARD_ID", "DOKIMA_BOARD", "DOKIMA_BOT", "GITHUB_ACTOR", "GITHUB_REPOSITORY", "GITHUB_RUN_ID",
> -    "GITHUB_SERVER_URL", "HEAD", "LOG_URL", "NUMBER", "ON_PR", "OWNERS", "PACK", "PLANNER_BASE", "ROLE", "STAGE",
> -    "acceptance_criteria", "accepted", "agent_started", "answer", "ask", "asks", "assumption", "assumptions", "attempt",
> -    "author", "base", "blocked_by", "blocker", "blockers", "body", "cache_creation_input_tokens",
> -    "cache_read_input_tokens", "change", "changes", "check", "check_runs", "command", "comments", "concerns",
> -    "conclusion", "content", "context", "cost_usd", "createdAt", "created_at", "criteria", "criterion", "depends_on",
> -    "dropped_by_fence", "duration_ms", "evidence", "feature", "file", "file_path", "filename", "files", "fix", "fixer",
> -    "handback", "headRefName", "id", "input", "input_tokens", "issue", "issues_found", "kind", "labels", "line",
> -    

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -5 origin/main; git log --oneline -3 main; git diff --stat origin/main...HEAD; git diff --stat HEAD origin/main | tail -3
```

> e934cfe The board shows Needs you only when something truly waits on me, and Autopilot otherwise (#319)
> 65edcee A link added or removed by hand on GitHub updates the cards of both issues (#307)
> 1b0cda6 The audit runs once a day in the background, and on the Run workflow button (#318)
> 930523a The Blocker pill is computed from blocked-by links, not set by hand (#317)
> 02a6d8d A drift audit reports what is off on one pinned Setup issue, and stays silent otherwise (#312)
> e934cfe The board shows Needs you only when something truly waits on me, and Autopilot otherwise (#319)
> 65edcee A link added or removed by hand on GitHub updates the cards of both issues (#307)
> 1b0cda6 The audit runs once a day in the background, and on the Run workflow button (#318)
>  AGENTS.md                        |   2 +-
>  dokima/agent.py                  | 266 +++++++++++----
>  tests/test_agent.py              |   2 -
>  tests/test_answered_questions.py | 193 -----------
>  tests/test_autopilot_river.py    |  14 -
>  tests/test_field_icons.py        |  31 +-
>  tests/test_fixer.py              |  15 -
>  tests/test_run_cards.py          |  26 +-
>  tests/test_run_comment_fields.py | 703 +++++++++++++++++++++++++++++++++++++++
>  9 files changed, 928 insertions(+), 324 deletions(-)
>  tests/test_run_cards.py          |  26 +-
>  tests/test_run_comment_fields.py | 703 ---------------------------------------
>  20 files changed, 1954 insertions(+), 969 deletions(-)

**Agent:** I'm reviewing the re-plan for #236. The planner only rewrote the "no new raise-type field" test, so next I'm running the tests on main and on the branch.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git diff origin/main...HEAD -- AGENTS.md; rm -rf /tmp/wt; git worktree add -q /tmp/wt origin/main 2>&1|tail -1; for f in tests/test_run_comment_fields.py tests/test_field_icons.py tests/test_agent.py tests/test_run_cards.py tests/test_autopilot_river.py tests/test_fixer.py; do cp $f /tmp/wt/$f; done; rm -f /tmp/wt/tests/test_answered_questions.py; cd /tmp/wt && python3 -m pytest -q tests/test_run_comment_fields.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-300
```

> diff --git a/AGENTS.md b/AGENTS.md
> index 5d2a750..39ede24 100644
> --- a/AGENTS.md
> +++ b/AGENTS.md
> @@ -85,7 +85,7 @@ The body has two parts split by a fixed marker. Above it, the current-state card
>  
>  ## Agent records and cards
>  
> -Every agent run posts one comment, written by code: one plain sentence on top saying what the run did, the short version the owner needs (the plan, its questions or the split; the worker's own words on what it changed, linking its pull request, or why it stopped; the criteria a review blocks on and its proposed issues), the long parts in folds drawn by the same code as the issue card, the full JSON record in the last fold, and a footnote with the model, time, turns, tokens, API-equivalent cost and a one-click link to the run's whole conversation. Those comments are the permanent records; only comments the bot posted count as records. The card on top of the issue is drawn from them (planned). Each run also gets one live card from queued to done (planned, #164).
> +Every agent run posts one comment, written by code: one plain sentence on top saying what the run did, the short version the owner needs (the plan's criteria, each with its circle, Verified by and Source, its questions or the split; the worker's own words on what it changed, linking its pull request, or why it stopped; a review's verdict, then only what fails: each failing criterion with why and its Source, each ask nothing covers, its changes outside the plan, the questions it could not confir

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 655,705p tests/test_run_comment_fields.py; python3 -m pytest -q 2>&1 | tail -3; python3 -c "
import sys;sys.path.insert(0,'tests')
import test_run_comment_fields as t; p=t.prompt_fields(); print(len(p), sorted(x for x in ['raises','answers','files_changed','verified_by','raise','notes','previous_step','outside_scope'] if x in p))"
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bhbtjx802). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/6c98fe72-0db2-4456-8e1d-662ef6cb20c9/tasks/bhbtjx802.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 655,705p tests/test_run_comment_fields.py; python3 -c "
import sys;sys.path.insert(0,'tests')
import test_run_comment_fields as t; p=t.prompt_fields(); print(len(p), sorted(x for x in ['raises','answers','files_changed','verified_by','raise','notes','previous_step','outside_scope'] if x in p))"; timeout 100 python3 -m pytest -q tests/test_run_comment_fields.py 2>&1|tail -2
```

> if isinstance(x, dict):
>         return Watched({k: watched(v) for k, v in x.items()})
>     if isinstance(x, list):
>         return [watched(v) for v in x]
>     return x
> 
> 
> def test_no_hand_back_gains_a_new_raise_type_field(record_property, run, monkeypatch):
>     """Run comments are drawn from the fields agents hand back today, never a new one.
> 
>     Draws a planner's, a worker's and both reviews' comments from hand-backs that also carry raises and answers, while
>     watching every field code reads off a hand-back (the agent's own file and the plan a review reads). Every field read
>     must be one the agents' prompts in dokima/roles define, so no raise-type field is added ahead of #289's raises and
>     answers; the two fields this story adds (the worker's files changed and each test's Verified by line) must sit in
>     the run's record, not in a hand-back. Then checks raises and answers never show while today's question, blocker and
>     issue found still do. Proves 236.9."""
>     record_property("proves", "236.9")
>     real = json.load
>     handbacks = set(agent.HANDBACK.values())
> 
>     def load(f, *args, **kwargs):
>         data = real(f, *args, **kwargs)
>         return watched(data) if os.path.basename(getattr(f, "name", "")) in handbacks else data
>     monkeypatch.setattr(agent.json, "load", load)
>     Watched.read = set()
>     extra = {"raises": [{"kind": "question", "text": "A raise nobody may read zr."}],
>              "answers": [{"raise": "R1", "answer": "done", "why": "An answer nob

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def render\|HANDBACK\b\|HANDBACK =" dokima/agent.py | head; sed -n "$(grep -n 'def render' dokima/agent.py | head -1 | cut -d: -f1),+6p" dokima/agent.py
```

> 34:HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 263:    hb = os.path.join(out, HANDBACK[role])
> 267:        handback = {"missing": f"{HANDBACK[role]}: {e}"}
> 587:def render(rec, pr=None, plan=None):
> 1559:    newest = next((r for r in reversed(recs) if r.get("role") in HANDBACK), None)
> def render(rec, pr=None, plan=None):
>     """The comment that carries a record: one plain sentence saying what the run did, the short version the owner
>     needs at a glance, the long parts in folds, then the full record as JSON in the last fold. `pr` is the link of the
>     worker's pull request, once it exists; `plan` is the plan a plan review judged, whose assumptions answer its
>     questions."""
>     role, h = rec["role"], rec["handback"]
>     repo = os.environ.get("GITHUB_REPOSITORY", "")

`12. Bash`
```
cd /home/runner/work/dokima/dokima; cp dokima/agent.py /tmp/agent.bak; python3 - <<'E'
p='dokima/agent.py';s=open(p).read()
s=s.replace('    role, h = rec["role"], rec["handback"]\n','    role, h = rec["role"], rec["handback"]\n    _x = h.get("raises") if isinstance(h, dict) else None\n',1)
open(p,'w').write(s)
E
timeout 100 python3 -m pytest -q tests/test_run_comment_fields.py -k raise 2>&1|grep -E "236.9|passed|failed"|head -3; cp /tmp/agent.bak dokima/agent.py
python3 - <<'E'
p='dokima/agent.py';s=open(p).read()
s=s.replace('    role, h = rec["role"], rec["handback"]\n','    role, h = rec["role"], rec["handback"]\n    _x = h.get("files_changed") if isinstance(h, dict) else None\n',1)
open(p,'w').write(s)
E
timeout 100 python3 -m pytest -q tests/test_run_comment_fields.py -k raise 2>&1|grep -E "236.9|passed|failed"|head -3; cp /tmp/agent.bak dokima/agent.py; git status --short
```

> issue found still do. Proves 236.9."""
>         record_property("proves", "236.9")
>             assert kept in text, f"236.9: the {role} {stage} comment lost {kept!r}, drawn from a field it has today:\n{text}"
>         issue found still do. Proves 236.9."""
>         record_property("proves", "236.9")
>             assert kept in text, f"236.9: the {role} {stage} comment lost {kept!r}, drawn from a field it has today:\n{text}"

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
p='dokima/agent.py';s=open(p).read()
s=s.replace('    role, h = rec["role"], rec["handback"]\n','    role, h = rec["role"], rec["handback"]\n    _x = h.get("raises") if isinstance(h, dict) else None\n',1)
open(p,'w').write(s)
E
timeout 100 python3 -m pytest -q tests/test_run_comment_fields.py -k raise 2>&1|grep -E "^E +(Assert|236)|passed|failed"|head -3; cp /tmp/agent.bak dokima/agent.py; git status --short; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/6c98fe72-0db2-4456-8e1d-662ef6cb20c9/tasks/bhbtjx802.output | tail -3
```

> E       AssertionError: 236.9: code reads hand-back fields no agent's prompt defines, so a hand-back gained a field: ['raises']
> 1 failed, 12 deselected in 0.18s
>         "236.9: the worker's record does not keep its files changed (files_changed)"
>     assert "verified_by" in records["planner"], \
>         "236.9: the planner's record does not keep each test's Verified by line (verified_by)"

**Agent:** The rewritten test catches a new field being read. Now I'm running the full suite on the branch.

`14. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 500 python3 -m pytest -q -x -p no:cacheprovider 2>&1 | tail -3
```

> ........................................................................ [ 94%]
> .............................................                            [100%]
> 765 passed in 400.69s (0:06:40)

**Agent:** The full suite passes on the branch: 765 tests. Next I'm writing the hand-back, reusing the list of the owner's asks from the last approved plan review.

`15. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'E'
import json
asks=json.load(open('in/10-reviewer-plan.json'))['handback']['asks']
for a in asks: print(a['criterion'], '|', a['ask'][:100], '|', a['source'])
r={"previous_step":{"did":["The planner re-planned after the pull request clashed with main, keeping every criterion, test and scope of the approved plan.",
 "It rewrote the test for the no-new-raise-type-field requirement: it now watches every field code reads off a hand-back while drawing each agent's comment, and fails on any field the agents' prompts do not define."],
 "decided":["The worker's files changed and each test's Verified by line live in the run's record, not in a hand-back."],"open":[]},
 "verdict":"approve",
 "summary":"The plan is unchanged apart from a stronger test for adding no new raise-type field; every new test fails on main for the missing feature and passes on the branch.",
 "blockers":[],
 "notes":[{"text":"The rewritten raise-type test turns red when code reads a field no agent's prompt defines: reading raises off a review hand-back fails it.","evidence":"injecting h.get(\"raises\") into render() in dokima/agent.py: '236.9: code reads hand-back fields no agent's prompt defines, so a hand-back gained a field: ['raises']'; tests/test_run_comment_fields.py on main: 13 failed, each naming its criterion; pytest -q on try/issue-236: 765 passed"},
  {"text":"The branch still has to take in main's newer AGENTS.md (#307, #319) before it can merge; the plan's AGENTS.md change touches only the Agent records and cards paragraph.","evidence":"git merge-base --is-ancestor 65edcee HEAD fails; git diff origin/main...HEAD -- AGENTS.md changes one paragraph"}],
 "resolved":[],"issues_found":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
E
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/doki
```

> 236.1 | The live card and the record say Plan review where they said Reviewer (plan), and Code review where  | https://github.com/dokima-dev/dokima/issues/236
> 236.2 | A run comment shows each of these only when it has something, and never a blank heading or empty sec | https://github.com/dokima-dev/dokima/issues/236
> 236.3 | The planner's run comment lists each criterion with its status icon and, under it, Verified by and i | https://github.com/dokima-dev/dokima/issues/236
> 236.4 | a blocking review's comment mirrors that list with only the failing criteria, each by its sentence,  | https://github.com/dokima-dev/dokima/issues/236
> 236.5 | The files the worker changed show on one inline line, not one per line. | https://github.com/dokima-dev/dokima/issues/236
> 236.6 | The stats (model, time, turns, tokens and cost) sit in a fold at the bottom of every run comment, no | https://github.com/dokima-dev/dokima/issues/236
> 236.7 | The full JSON record stays in its last fold, unchanged, so later packs still read every run. | https://github.com/dokima-dev/dokima/issues/236
> 236.4 | The reviewer's card shows only what I care about: did I get what I asked for. That is the verdict | https://github.com/dokima-dev/dokima/issues/236
> 236.4 | any ask of mine with no criterion as a blocker | https://github.com/dokima-dev/dokima/issues/236
> 236.2 | Remove the What the previous step did fold, the Details fold and the Notes section. | https://github.com/dokima-dev/dokima/issues/236
> 236.4 | A failing cri

`16. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan is unchanged except for a stronger no-new-field test; every new test fails on main for the missing feature."
json.dump(r,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 236 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; git worktree remove --force /tmp/wt; git status --short
```

> rc=0

**Agent:** I approved the re-plan for #236, and both hand-back checks pass on it.

**What changed:** the pull request clashed with main over `AGENTS.md`, so the planner re-planned. The criteria, scope and test list are the same as the plan approved last time. The only change is that the planner rewrote the test for "add no new raise-type field" (`tests/test_run_comment_fields.py`). It used to compare against a fixed list of field names; now it watches every field the code reads from an agent's output while it draws each comment. It fails on any field the agents' prompts don't already define.

**Tests I ran:**
- **On main**, with the planner's tests copied in: all 13 tests in `tests/test_run_comment_fields.py` fail, each naming its criterion and failing because the feature is missing.
- **Breaking it on purpose:** I made the comment code read `raises` from a review's output. The rewritten test turned red, naming `raises`.
- **On the branch** (`try/issue-236`): `pytest -q` gives 765 passed.

**Notes in the review:**
- The owner's ask that the issues a review finds show "as links to the issues filed for them" is left to #268, as in the last approved plan. This plan only puts those issues last in a review's comment.
- The branch still needs main's newer `AGENTS.md` (from #307 and #319) merged in before it can merge.

There were no open blockers from earlier rounds. The review is in `/tmp/dokima-out/review.json`.
