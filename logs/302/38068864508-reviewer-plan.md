# reviewer (plan) for #302

Run: https://github.com/dokima-dev/dokima/actions/runs/38068864508

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (43.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/0e3c5c2a-2faf-423e-8d58-91874bb4cd79/tool-results/bz0f361kc.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct 10 16:44 .
> drwxrwxrwt 18 root   root    4096 Oct 10 16:44 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 16:44 in
> -rw-r--r--  1 runner runner 44048 Oct 10 16:44 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 16:44 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 16:44 parent.json
> -rw-r--r--  1 runner runner  5893 Oct 10 16:44 plan.json
> 
> in:
> total 44
> drwxr-xr-x 2 runner runner 4096 Oct 10 16:44 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 16:44 ..
> -rw-r--r-- 1 runner runner 5475 Oct 10 16:44 01-planner.json
> -rw-r--r-- 1 runner runner 3622 Oct 10 16:44 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1876 Oct 10 16:44 03-worker.json
> -rw-r--r-- 1 runner runner 1573 Oct 10 16:44 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 2566 Oct 10 16:44 05-worker.json
> -rw-r--r-- 1 runner runner 2564 Oct 10 16:44 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 6531 Oct 10 16:44 07-planner.json
> # Issue #302: AGENTS.md records the raise design, and the shared prompt section teaches it with many examples
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299, 300, 301, 355 -->
> <!-- dokima-blocking: {"blocked_by": [298, 300, 301], "blocks": [], "loop": []} -->
> AGENTS.md gets one section on raising, and the prompt section all th

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md
```

> <persisted-output>
> Output too large (41.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/0e3c5c2a-2faf-423e-8d58-91874bb4cd79/tool-results/b9c9smigz.txt
> 
> Preview (first 2KB):
> # Issue #302: AGENTS.md records the raise design, and the shared prompt section teaches it with many examples
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299, 300, 301, 355 -->
> <!-- dokima-blocking: {"blocked_by": [298, 300, 301], "blocks": [], "loop": []} -->
> AGENTS.md gets one section on raising, and the prompt section all three agents share teaches it with examples.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/302 · https://github.com/dokima-dev/dokima/pull/419 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/419/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Import:** The owner asked for tests/test_raise_design.py to import dokima the way the other test files do. Tests are the planner's and code restores them as the planner committed them, so the planner should add sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")) before `from dokima import raises`, as this round's diff does. · for the planner
> 
> <img src="https://raw.githubuserconte

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/0e3c5c2a-2faf-423e-8d58-91874bb4cd79/tool-results/b9c9smigz.txt
```

> 1	# Issue #302: AGENTS.md records the raise design, and the shared prompt section teaches it with many examples
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-linked-from: 298, 299, 300, 301, 355 -->
> 5	<!-- dokima-blocking: {"blocked_by": [298, 300, 301], "blocks": [], "loop": []} -->
> 6	AGENTS.md gets one section on raising, and the prompt section all three agents share teaches it with examples.
> 7	
> 8	**Review**
> 9	
> 10	https://github.com/dokima-dev/dokima/issues/302 · https://github.com/dokima-dev/dokima/pull/419 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/419/files)
> 11	
> 12	**Raised:**
> 13	
> 14	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Import:** The owner asked for tests/test_raise_design.py to import dokima the way the other test files do. Tests are the planner's and code restores them as the planner committed them, so the planner should add sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")) before `from dokima import raises`, as this round's diff does. · for the planner
> 15	
> 16	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298, #300, #301
> 17	<img src="https://raw.g

`4. Bash`
```
cd /tmp/pack; sed -n 401,600p /home/runner/.claude/projects/-home-runner-work-dokima-dokima/0e3c5c2a-2faf-423e-8d58-91874bb4cd79/tool-results/b9c9smigz.txt; cat open_blockers.json parent.json; python3 -c "
import json;d=json.load(open('in/07-planner.json'));print(json.dumps(d,indent=1)[:5000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests | head -60
```

> []{"number": 289}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38068575208",
>  "commit_before": "d12626cfcece8bd3a25fe6da4ec913b3b9170dbf",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 2621,
>   "turns": 2,
>   "cost_usd": 0.512112,
>   "tokens_in": 112975,
>   "tokens_out": 171
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/302/38068575208-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38068575208",
>  "handback": {
>   "kind": "user_story",
>   "summary": "AGENTS.md gets one section on raising, and the prompt section all three agents share teaches it with examples.",
>   "user_story": "The owner and every agent read one section in AGENTS.md on what code raises by itself and what agents raise by judgment, and the prompt section the planner, worker and reviewer share shows a worked example of every kind and common case, asks agents to speak up, and ends with a short checklist.",
>   "acceptance_criteria": [
>    {
>     "text": "AGENTS.md has one section on raising, Raising and answering, which takes in today's Questions section. It lists what code detects and raises itself: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs the owner, and three blocks in a row. It lists the three kinds agents raise by judgment: question, blocker and issue. It names doubt about the ask as a question for the owner that carries its 

`5. Bash`
```
cd /tmp && env -u PYTHONPATH python3 -m pytest -q /home/runner/work/dokima/dokima/tests/test_raise_design.py 2>&1 | tail -3; cd /home/runner/work/dokima/dokima; git log --oneline main -1; rm -rf /tmp/mainchk && git worktree add -q /tmp/mainchk main && cp tests/test_raise_design.py /tmp/mainchk/tests/ && cd /tmp && env -u PYTHONPATH python3 -m pytest -q /tmp/mainchk/tests/test_raise_design.py 2>&1 | grep -E "FAILED|passed|failed|Error" | head -20
```

> .......                                                                  [100%]
> 7 passed in 0.04s
> f7340db board.yml runs the pull request's own copy of itself, with the keys, on a review (#418)
> E       AssertionError: 302.1: AGENTS.md does not have exactly one '## Raising and answering' section
> mainchk/tests/test_raise_design.py:168: AssertionError
> E       AssertionError: 302.2: AGENTS.md does not have exactly one '## Raising and answering' section
> mainchk/tests/test_raise_design.py:190: AssertionError
> E       AssertionError: 302.2: AGENTS.md does not have exactly one '## Raising and answering' section
> mainchk/tests/test_raise_design.py:212: AssertionError
> E           AssertionError: 302.3: the shared section has no example of a question to the owner labelled 'Two readings'
> mainchk/tests/test_raise_design.py:242: AssertionError
> E       AssertionError: 302.4: the shared section does not ask agents not to stay quiet
> mainchk/tests/test_raise_design.py:260: AssertionError
> E       AssertionError: 302.5: AGENTS.md does not have exactly one '## Raising and answering' section
> mainchk/tests/test_raise_design.py:283: AssertionError
> E       AssertionError: 302.6: the shared section has 3 example raises, fewer than 9
> E        +  where 3 = len([{'kind': 'question', 'to': 'owner', 'label': 'Failed runs', 'text': 'Should a failed run move its card to Needs you? ..., 'text': 'The board ignores closed pull requests, so their cards go stale.', 'evidence': 'dokima/board.py, column()'}])
> mainchk

**Agent:** I'm checking the planner's fix: the test file now loads Dokima when run from outside the repo root, and its tests still fail on main because the feature is missing. Next I'll write the review.

`6. Bash`
```
git worktree remove --force /tmp/mainchk; git diff d12626c HEAD --stat; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner made tests/test_raise_design.py add the repo root to the import path before importing dokima, the way tests/test_agent.py does, as the owner asked on 2026-10-10.",
          "It kept the same five criteria, one non-functional requirement and seven tests."],
  "decided": ["No criterion, scope or test changes beyond the import line."],
  "open": []},
 "verdict": "approve",
 "summary": "The planner's tests now load Dokima when each criterion's check runs on its own, as the owner asked, and the plan is otherwise unchanged and still proves every ask.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "AGENTS.md has one design section on raising. It lists what code detects and raises itself: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs you, and three blocks in a row. It lists the three kinds agents raise by judgment: question, blocker and issue.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "302.1"},
  {"ask": "It names doubt about the ask as an instance of the question kind: a question for you that carries its evidence.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "302.1"},
  {"ask": "The same section gives the who-can-address-whom table, row for row the same as the table in code.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "302.2"},
  {"ask": "It gives the two tiers of autonomy: always on, the reviewer settles anything addressed to an agent and confirms issues before they are filed; on autopilot only, the reviewer answers a question for you only with your own words as evidence.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "302.2"},
  {"ask": "The shared prompt section gives an exa
```

> tests/test_raise_design.py | 4 +++-
>  1 file changed, 3 insertions(+), 1 deletion(-)
> summary holds 29 words, over its cap of 25 (up to 30 passes)

`7. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The planner's tests now load Dokima when each check runs on its own, as the owner asked; the plan is otherwise unchanged."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 302 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#302](https://github.com/dokima-dev/dokima/issues/302) (AGENTS.md and the shared prompt section explain how agents raise things). The hand-back is in `/tmp/dokima-out/review.json`, and both the review check and the round check accept it.

- **What changed:** you used `/plan` to ask the planner to fix the test file's import of Dokima. That is the planner's only change since the plan was first approved: `tests/test_raise_design.py` now adds the repo root to the import path before importing Dokima, the way `tests/test_agent.py` does. The five criteria, the requirement that every example raise is one code accepts, the scope and the seven tests are the same.
- **The import works:** run from `/tmp` with no import path set, the way each criterion's check runs on GitHub, the file now passes 7 of 7 on this branch. Before, it failed with "No module named dokima".
- **The tests still prove the feature:** I ran the same test file against main's `AGENTS.md` and prompts. All seven fail because the feature is missing, each naming its criterion (for example "302.1: AGENTS.md does not have exactly one '## Raising and answering' section"), and none of them fail on the import.
- **Your asks:** I listed nine, and each maps to a criterion. Your `/plan` import ask has no criterion of its own because it is a fix to the tests, so I put it under 302.6. Its source link points to the issue, not to your comment.

I raised nothing, and no open raises were waiting for my answer.
