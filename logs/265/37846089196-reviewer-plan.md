# reviewer (plan) for #265

Run: https://github.com/dokima-dev/dokima/actions/runs/37846089196

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #265: Issues the reviewer finds are filed automatically, parked and labeled filed by Dokima
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> Today an issue the reviewer finds outside the one it reviews stays a proposal on its card, and a /issue command to file it is only planned. #222 shows the cost: Dokima found the no-PR bug, nobody filed it, and it sat unseen until it broke main.
> 
> What I want:
> - Every issue the reviewer finds is filed by code right away as its own issue, parked and labeled filed-by-dokima.
> - It says where it was found, with a link to the review that found it.
> - Nothing more: its links, size and plan are worked out when it is planned.
> - The same finding is never filed twice.
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #265 (2026-10-08T21:05:36Z)
> 
> /autopilot start
> 
> #

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; python -m pytest -q tests/test_filed_issues.py 2>&1 | tail -30; grep -n "issuecomment\|def check_review\|asks" dokima/agent.py | head -40
```

> commit 2780fa7b7ebd08a18cdb83d30aced508e4ca9760
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:20:22 2026 +0000
> 
>     planner for #265 (run 37844344508)
> 
>  tests/test_filed_issues.py | 398 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 398 insertions(+)
>   <details><summary><b>Details</b></summary>
>   
>   - The split keeps every promise once.
>   
>   </details>
>   
>   <details><summary><b>The owner's asks</b></summary>
>   
>   - Fix it. (57.1, https://github.com/o/r/issues/57)
>   
>   </details>
>   
>   <details><summary><b>What the previous step did</b></summary>
>   
>   - **Did:** Proposed a split into two stories.
>   
>   </details>
>   
>   <details><summary>Full record</summary>
>   
>   
>   
>   </details>
>   
>   <sub>Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md) · [run](https://github.com/o/r/actions/runs/42)</sub>
>   
>   **Next:** @owner-person The plan is approved. Say `/work` to build it, or `/plan` with changes.
>   
> assert ('The board drops closed pull requests' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...ns/runs/42)</sub>\n\n**Next:** @owner-person The plan is approved. Say `/work` to build it, or `/plan` with changes.\n' and 'HTTP 502' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" heig...ns/runs/42)</sub>\n\n**Next:** @o

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E  )" | head -40
```

> E       AssertionError: 265.1: a plan review that found two issues did not file exactly those two, by their titles; filed: []
> E       assert [] == ['The board d... card behind']
> E         
> E         Right contains 2 more items, first extra item: 'The board drops closed pull requests'
> E         
> E         Full diff:
> E         + []
> E         - [
> E         -     'The board drops closed pull requests',
> E         -     'A cancelled run leaves its queued card behind',
> E         - ]
> E           AssertionError: 265.2 (plan review): expected 2 filed issues, got []
> E           assert 0 == 2
> E            +  where 0 = len([])
> E            +    where [] = filed()
> E            +      where filed = <test_filed_issues.Reviews object at 0x7fa73cb96ba0>.filed
> E            +  and   2 = len([{'title': 'The board drops closed pull requests', 'why': 'Cards for merged work go stale on the board.', 'evidence': ...nd', 'why': 'The owner sees a run that never ends.', 'evidence': 'dokima/agent.py:290 queue() never removes the card'}])
> E       AssertionError: 265.3: the review did not file its two findings; filed: []
> E       assert 0 == 2
> E        +  where 0 = len(set())
> E       AssertionError: 265.4: one review listing a finding twice did not file it exactly once beside the other; filed: []
> E       assert [] == ['The board d... card behind']
> E         
> E         Right contains 2 more items, first extra item: 'The board drops closed pull requests'
> E         
> E         Full diff:
> E         + []
> E        

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote five criteria and seven tests for the reviewer's found issues being filed by code, parked and labeled filed-by-dokima, never twice, linked to the review."],
  "decided": ["Only plan and code reviews file issues; the reviewer's prompt in dokima/roles/ stays unchanged and is left to a follow-up issue."],
  "open": ["The owner's later comment asks for the planner and worker to report issues too, for the checker to file them, and for the planner's links to be written the same way; the plan does not cover it yet."]},
 "verdict": "block",
 "summary": "The plan covers the original ask, but misses the owner's later comment: planner and worker must report found issues too, the existing checker must file them, and the planner's links must be written by that same checker.",
 "blockers": [
  {"id": "B1", "criterion": "missing", "test": null,
   "problem": "The owner asked that any agent, planner, worker and reviewer, can report an issue it finds outside its own, with the same field in their hand-back. The plan only files issues a plan review or code review finds (criterion 265.1).",
   "evidence": "Owner's /plan comment on #265 (2026-10-08T21:08:55Z): \"Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.\" plan.json criterion 1 says \"Each issue a plan review or a code review finds\"; no criterion or test covers the planner or worker.",
   "fix": "Add a criterion that the planner's and the worker's hand-backs take the same found-issues field as the reviewer's and that each is filed the same way, with a test per role.",
   "fixer": "planner"},
  {"id": "B2", "criterion": "missing", "test": null,
   "problem": "The owner asked for no new component: the checker that already runs at the end of every agent's turn files the found issues, only after the hand-back passes. The plan does not promise where filing
```

> blocker B1 names missing, which is not a criterion of the plan (265.1, 265.2, 265.3, 265.4, 265.5, 265.6, 265.7)
> blocker B2 names missing, which is not a criterion of the plan (265.1, 265.2, 265.3, 265.4, 265.5, 265.6, 265.7)
> blocker B3 names missing, which is not a criterion of the plan (265.1, 265.2, 265.3, 265.4, 265.5, 265.6, 265.7)
> 1

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
for b,c in zip(r["blockers"],["265.1","265.6","265.3"]): b["criterion"]=c
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 265 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I've blocked the plan for #265 and sent it back to the planner. It covers your original ask but misses all three things you added in your later `/plan` comment. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the plan gets right:** reviews file what they find as their own issues, parked and labeled filed-by-dokima. Each filed issue links back to the review that found it, nothing more is done to it, and the same finding is never filed twice. I ran all seven new tests and each fails today for the right reason: nothing gets filed yet.

**Blockers (the planner fixes all three):**
- **B1:** You asked that the planner and the worker can report issues they find too, using the same field in their hand-back as the reviewer. The plan only files what a plan review or a code review finds.
- **B2:** You asked for no new component: the checker that already runs at the end of every agent's turn should do the filing, and only after the hand-back passes. The plan doesn't promise that, and it only tests that a rejected review files nothing, not a rejected planner or worker hand-back.
- **B3:** You asked that the planner's links (blocked by, blocks, relates to) are written by that same checker. The plan has no criterion for this, and its out-of-scope list even leaves linking for later.

Your added asks don't fit any single existing criterion, so the review's check made me tie each blocker to its closest one: B1 to 265.1, B2 to 265.6 and B3 to 265.3. In the review's list of your asks, all three are marked missing.

I also left two notes:
- With these asks added, the issue may now be big enough to need a split.
- The planner's and worker's prompts in `dokima/roles/` will need the new field, so those files could go in scope rather than being left to a follow-up.

Two more `/plan` runs from your comment are already queued, so a revised plan should follow.
