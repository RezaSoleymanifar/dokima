# reviewer (plan) for #166

Run: https://github.com/dokima-dev/dokima/actions/runs/37684435161

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (38.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b3ea93f4-b454-46dd-af7c-47c18808aa46/tool-results/bawjlgswm.txt
> 
> Preview (first 2KB):
> total 48
> drwxr-xr-x 2 runner runner 4096 Oct  7 20:45 .
> drwxr-xr-x 3 runner runner 4096 Oct  7 20:45 ..
> -rw-r--r-- 1 runner runner 4372 Oct  7 20:45 01-planner.json
> -rw-r--r-- 1 runner runner 3285 Oct  7 20:45 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4794 Oct  7 20:45 03-planner.json
> -rw-r--r-- 1 runner runner 2113 Oct  7 20:45 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2359 Oct  7 20:45 05-worker.json
> -rw-r--r-- 1 runner runner 2856 Oct  7 20:45 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4947 Oct  7 20:45 07-planner.json
> # Issue #166: River: a code review block about a weak test goes to the planner, not the worker
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #169](https://github.com/dokima-dev/dokima/pull/169) · [files changed](https://github.com/dokima-dev/dokima/pull/169/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37679569811/job/112991776310)
> 
> <!-- /dokima-card -->
> 
> Found on 154 and PR 165. When the code reviewer finds that a planner's test is too weak, the river sends the block to the worker, who may 

`2. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b3ea93f4-b454-46dd-af7c-47c18808aa46/tool-results/bawjlgswm.txt | sed -n 30,400p
```

> ### dokima-runtime on issue #166 (2026-10-07T18:15:10Z)
> 
> <!-- dokima-record -->
> **Planner**
> 
> When a code review finds a planner's test too weak, the planner strengthens the test and the work goes on, instead of the worker going round in circles until it reaches the owner.
> 
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - After a code review sends a weak test back, should the approved re-plan go straight to the worker, or wait for your `/work` as a first plan does? I planned for straight to the worker, from your words "a test fix then goes planner, plan review, worker, code review"; the other reading keeps your `/work` as the only gate that freezes a plan (AGENTS.md, The flow, step 3).
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37654844239",
>  "commit_before": "860b40de3ad96832391c461da1576fc7167dbc4d",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 184028,
>   "turns": 16,
>   "cost_usd": 1.0104456,
>   "tokens_in": 757455,
>   "tokens_out": 16899
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/166/37654844239-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37654844239",
>  "handback": {
>   "kind": "user_story",
>   "user_story": "When a code review finds a planner's test too weak, the planner strengthens the test and the work goes on, instead of the worker going round in circl

`3. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b3ea93f4-b454-46dd-af7c-47c18808aa46/tool-results/bawjlgswm.txt | sed -n 400,900p | grep -v '^ *"\(run_id\|commit_before\|models\|duration_ms\|turns\|cost_usd\|tokens_in\|tokens_out\|log\|run\)"'
```

> "notes": [
>    {
>     "text": "All six new tests fail today because the feature is missing, and the rest of the suite passes.",
>     "evidence": "`pytest -q`: 6 failed, 179 passed; e.g. 166.4 fails with ('stop', 'The plan is approved. Say `/work` to build it...') where it expects ('start', 'worker', '')."
>    },
>    {
>     "text": "The plan says criteria count as unchanged only in the same order, but no test reorders them; code that ignores order would still pass. Worth a one-line case.",
>     "evidence": "plan.json out_of_scope, last line; tests/test_fixer.py:177-180 covers rewritten, added, dropped and non-functional added, not reordered."
>    }
>   ],
>   "outside_plan": [],
>   "resolved": [
>    "B1"
>   ],
>   "issues_found": []
>  },
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> ```
> 
> </details>
> 
> <sub>Opus 5.5 · 0.5 min · 5 turns · 164,304 tokens in, 2,018 out · $0.28 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/166/37673922849-reviewer-plan.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37673922849)</sub>
> 
> **Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 
> 
> ### RezaSoleymanifar on issue #166 (2026-10-07T20:04:33Z)
> 
> /work
> 
> ### dokima-runtime on PR #169 (2026-10-07T20:06:57Z)
> 
> <!-- dokima-record -->
> **Worker**
> 
> A code review's blockers did not say who fixes them, so the river always sent a block back to the worker, who may not touch tests. Now every review blocker names its fixer, a co

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -6; git show --stat HEAD; git show HEAD -- tests/ | head -200
```

> 9bd8b71 planner for #166 (run 37684224308)
> ffd1b56 worker for #166 (run 37679285802)
> 83e8b44 Merge remote-tracking branch 'origin/main' into try/issue-166
> fbc1c4e planner for #166 (run 37673723142)
> acfbaa7 AGENTS.md: the conventions we settled (#163)
> 6672bda A re-plan is judged only on what the planner changed in its own run (#167)
> commit 9bd8b71520fbd631e85da0c77276531ab0257726
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 20:45:08 2026 +0000
> 
>     planner for #166 (run 37684224308)
> 
>  tests/test_fixer.py | 31 +++++++++++++++++++++++++++++++
>  1 file changed, 31 insertions(+)
> commit 9bd8b71520fbd631e85da0c77276531ab0257726
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 20:45:08 2026 +0000
> 
>     planner for #166 (run 37684224308)
> 
> diff --git a/tests/test_fixer.py b/tests/test_fixer.py
> index 6ce3861..83cddb2 100644
> --- a/tests/test_fixer.py
> +++ b/tests/test_fixer.py
> @@ -203,3 +203,34 @@ def test_the_reviewer_is_told_to_name_who_fixes_each_blocker(record_property):
>      weak = [p for p in grade.split("\n7.")[1:]]
>      assert weak and '"fixer": "planner"' in weak[0].split("\nNotes")[0], \
>          "166.5: the result grade's weak-test rule does not tell the reviewer to set the fixer to the planner"
> +
> +
> +def test_three_blocks_on_the_test_fix_route_still_stop_for_the_owner(record_property):
> +    """On the new route, the third blocking code review in a row stops the river and

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q 2>&1 | tail -3; python -m pytest -q tests/test_fixer.py -k three 2>&1 | tail -3; grep -n "blocking reviews\|def next_step\|def test_fix\|three\|3 \|in a row" dokima/agent.py | head -30
```

> ........................................................................ [ 77%]
> ...........................................                              [100%]
> 187 passed in 3.63s
> .                                                                        [100%]
> 1 passed, 6 deselected in 0.01s
> 389:        bad.append("at most three notes")
> 394:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 631:def next_step(items, rec, owners, rounds=3):
> 635:    review sends the work back, until three blocks in a row at that stage since the owner last spoke; then it is the
> 660:        return ("stop", f"{blocks} blocking reviews in a row without agreement. Your call: `/plan`, `/work` or `/review` with your words.")
> 670:def test_fix(items, owners):

**Agent:** The new test passes on the branch, which is expected since the owner asked for a test of behaviour that's already built. Next I'm checking whether the test would catch the rule breaking.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 600,720p dokima/agent.py; sed -n 1,80p tests/test_fixer.py
```

> COMMANDS = {"/plan": "planner", "/work": "worker", "/review": "reviewer"}
> 
> 
> def command_of(body):
>     """The stage a comment starts: its first line's first word, when that word is a command; otherwise None."""
>     first = (body or "").strip().splitlines()[0].split() if (body or "").strip() else []
>     return COMMANDS.get(first[0].lower()) if first else None
> 
> 
> def issue_of_pr(head, body):
>     """The issue a pull request was built for: from its branch (work/issue-N or try/issue-N), else 'Closes #N'."""
>     m = re.match(r"(?:work|try)/issue-(\d+)$", head or "") or re.search(r"(?i)\b(?:closes|fixes|resolves) #(\d+)", body or "")
>     return m.group(1) if m else None
> 
> 
> def route(body, on_pr, number, head="", pr_body=""):
>     """What a code owner's comment starts: {role, stage, issue}, or None when it starts nothing.
> 
>     /review on an issue grades the plan; on a pull request it grades the work. A pull request routes to its issue."""
>     role = command_of(body)
>     if not role:
>         return None
>     issue = issue_of_pr(head, pr_body) if on_pr else str(number)
>     if not issue:
>         return None
>     stage = ("pr" if on_pr else "plan") if role == "reviewer" else ""
>     return {"role": role, "stage": stage, "issue": issue}
> 
> 
> def next_step(items, rec, owners, rounds=3):
>     """The river: what follows the run that just finished. ("start", role, stage) or ("stop", why), decided by code.
> 
>     A planner hands to the reviewer unless it has questions for the owner. A worker hands to the r

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cp dokima/agent.py /tmp/agent.bak
t(){ python -m pytest -q tests/test_fixer.py -k three 2>&1 | grep -E "166.6|passed|failed" | head -2; cp /tmp/agent.bak dokima/agent.py; }
echo "M1 no stop when planner blocker"; sed -i 's/    if blocks >= rounds:/    if blocks >= rounds and not any(b.get("fixer")=="planner" for b in h.get("blockers",[])):/' dokima/agent.py; t
echo "M2 owner speech does not reset"; sed -i 's/    later = \[r for r in records(items\[last_owner + 1:\])/    later = [r for r in records(items)/' dokima/agent.py; t
echo "M3 count resets at worker run"; python - <<'E'
p='dokima/agent.py';s=open(p).read()
s=s.replace('    later = [r for r in records(items[last_owner + 1:]) if','    _rs = records(items[last_owner + 1:]); _w = max([i for i,r in enumerate(_rs) if r.get("role")=="worker"], default=-1)\n    later = [r for r in _rs[_w+1:] if')
open(p,'w').write(s)
E
t
echo "M4 rounds=4"; sed -i 's/def next_step(items, rec, owners, rounds=3)/def next_step(items, rec, owners, rounds=4)/' dokima/agent.py; t
echo "M5 stop at 2"; sed -i 's/def next_step(items, rec, owners, rounds=3)/def next_step(items, rec, owners, rounds=2)/' dokima/agent.py; t
git status --short
```

> M1 no stop when planner blocker
>         record_property("proves", "166.6")
>             assert step == ("start", "planner", ""), f"166.6: code review block {n} with a test blocker gave {step}, not the planner"
> M2 owner speech does not reset
>         record_property("proves", "166.6")
>             assert step == ("start", "planner", ""), f"166.6: code review block {n} with a test blocker gave {step}, not the planner"
> M3 count resets at worker run
>         record_property("proves", "166.6")
>             assert step == ("start", "planner", ""), f"166.6: code review block {n} with a test blocker gave {step}, not the planner"
> M4 rounds=4
>         record_property("proves", "166.6")
>             assert step == ("start", "planner", ""), f"166.6: code review block {n} with a test blocker gave {step}, not the planner"
> M5 stop at 2
>         record_property("proves", "166.6")
> >           assert step == ("start", "planner", ""), f"166.6: code review block {n} with a test blocker gave {step}, not the planner"

`8. Bash`
```
cd /home/runner/work/dokima/dokima
t(){ python -m pytest -q tests/test_fixer.py -k three 2>&1 | grep -E "^E +(Assertion|.*166)|passed|failed" | head -2; cp /tmp/agent.bak dokima/agent.py; }
echo M1; sed -i 's/    if blocks >= rounds:/    if blocks >= rounds and not any(b.get("fixer")=="planner" for b in h.get("blockers",[])):/' dokima/agent.py; t
echo M2; sed -i 's/    later = \[r for r in records(items\[last_owner + 1:\])/    later = [r for r in records(items)/' dokima/agent.py; t
echo M3; python - <<'E'
p='dokima/agent.py';s=open(p).read()
s=s.replace('    later = [r for r in records(items[last_owner + 1:]) if','    _rs = records(items[last_owner + 1:]); _w = max([i for i,r in enumerate(_rs) if r.get("role")=="worker"], default=-1)\n    later = [r for r in _rs[_w+1:] if')
open(p,'w').write(s)
E
t
echo M4; sed -i 's/rounds=3)/rounds=4)/' dokima/agent.py; t
echo M5; sed -i 's/rounds=3)/rounds=2)/' dokima/agent.py; t
git status --short; git stash list | head -1
```

> M1
> E           AssertionError: 166.6: the third blocking code review in a row, with a test blocker, gave ('start', 'planner', ''), not a stop for the owner
> 1 failed, 6 deselected in 0.04s
> M2
> E       AssertionError: 166.6: after the owner spoke, a code review block gave ('stop', '3 blocking reviews in a row without agreement. Your call: `/plan`, `/work` or `/review` with your words.'); the count must start again and go to the planner
> 1 failed, 6 deselected in 0.04s
> M3
> E           AssertionError: 166.6: the third blocking code review in a row, with a test blocker, gave ('start', 'planner', ''), not a stop for the owner
> 1 failed, 6 deselected in 0.04s
> M4
> E           AssertionError: 166.6: the third blocking code review in a row, with a test blocker, gave ('start', 'planner', ''), not a stop for the owner
> 1 failed, 6 deselected in 0.04s
> M5
> E           AssertionError: 166.6: code review block 2 with a test blocker gave ('stop', '2 blocking reviews in a row without agreement. Your call: `/plan`, `/work` or `/review` with your words.'), not the planner
> 1 failed, 6 deselected in 0.04s

**Agent:** All five ways I tried breaking the rule were caught by the new test, and the code is restored. Writing the hand-back now.

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["Added criterion 166.6: on the new route, the third blocking code review in a row since the owner last spoke stops and asks the owner, whether its blockers are for the planner or the worker.",
          "Added one test that walks the route twice (code review block, planner, approved re-plan, worker) and checks the third block stops, and that the count starts again once the owner speaks."],
  "decided": ["Left criteria 166.1 to 166.5, the scope and the other tests as they were."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan adds only what you asked: a test that three blocking code reviews in a row still stop for you on the new planner route, and that test breaks if the rule does.",
 "blockers": [],
 "notes": [
  {"text": "The new test passes today, as it should: you asked for proof that behavior already built on this branch still holds. It turns red when the rule is broken in each way tried: no stop when a block is for the planner, no fresh count after the owner speaks, a count that restarts at each worker run, a stop after four blocks, and a stop after two.",
   "evidence": "pytest -q: 187 passed. With each of those five changes to next_step in dokima/agent.py, tests/test_fixer.py::test_three_blocks_on_the_test_fix_route_still_stop_for_the_owner failed with its 166.6 message, e.g. '166.6: the third blocking code review in a row, with a test blocker, gave ('start', 'planner', ''), not a stop for the owner'. The file was restored afterwards."},
  {"text": "Only the new test was added in this round; criteria 166.1 to 166.5 are word for word the same. Since a criterion was added, this plan waits for your /work, as you set out.",
   "evidence": "git show 9bd8b71 --stat: tests/test_fixer.py, 31 insertions; plan.json 166.1 to 166.5 match 03-planner.json."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
E
cd /home/runner/work/dokima/dokima; python3
```

> rc=0

**Agent:** I approved the re-plan for #166. The hand-back is in `/tmp/dokima-out/review.json` and both checks on it pass.

**What the planner did:** It added only what the owner asked for. Criterion 166.6 says that on the new route, the third blocking code review in a row since the owner last spoke stops the river for the owner. That holds whether the blockers are for the planner or the worker, and the count starts again once the owner speaks. It added one test for it, `tests/test_fixer.py::test_three_blocks_on_the_test_fix_route_still_stop_for_the_owner`. Criteria 166.1 to 166.5, the scope and the other tests are unchanged.

**Evidence:**
- The full suite passes (187 tests). The new test passes on this branch, and it should: the owner asked for proof that behaviour already built still holds.
- I checked that the test breaks if the rule does. I made five temporary changes to the routing code in `dokima/agent.py`, one at a time:
  - no stop when a block is for the planner
  - the count doesn't start again after the owner speaks
  - the count restarts at each worker run
  - the stop comes after four blocks
  - the stop comes after two blocks

  The test failed every time with a 166.6 message. I restored the file afterwards and the working tree is clean.

**Next:** this plan waits for the owner's `/work`. A criterion was added, and the owner's earlier answer was that any change to the criteria needs a new `/work`.

There were no earlier blockers left open.
