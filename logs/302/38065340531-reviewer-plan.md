# reviewer (plan) for #302

Run: https://github.com/dokima-dev/dokima/actions/runs/38065340531

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 44
> drwxr-xr-x  3 runner runner  4096 Oct 10 15:52 .
> drwxrwxrwt 18 root   root    4096 Oct 10 15:52 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 15:52 in
> -rw-r--r--  1 runner runner 12592 Oct 10 15:52 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 15:52 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 15:52 parent.json
> -rw-r--r--  1 runner runner  4835 Oct 10 15:52 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct 10 15:52 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 15:52 ..
> -rw-r--r-- 1 runner runner 5475 Oct 10 15:52 01-planner.json
> # Issue #302: AGENTS.md records the raise design, and the shared prompt section teaches it with many examples
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299, 300, 301, 355 -->
> <!-- dokima-blocking: {"blocked_by": [298, 300, 301], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/302
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298, #300, #301
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #299, #355
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 5</summary>
> 
> **Part of:** #289 Every agent 

`2. Bash`
```
cd /tmp/pack; cat parent.json; python3 -c "import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]); h=d.get('handback',{}); print(json.dumps(h.get('raises'),indent=1)); print(list(d.keys()))"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_raise_design.py
```

> {"number": 289}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38064902150",
>  "commit_before": "bcb36e455d4c614ffa81dc06e7c58f42d24fa783",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 348400,
>   "turns": 19,
>   "cost_usd": 1.1510406000000002,
>   "tokens_in": 1039583,
>   "tokens_out": 22001
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/302/38064902150-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38064902150",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> null
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> commit a5e18fb2794aaf50df4c72e8bf83209c10b8e7cd
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 15:51:48 2026 +0000
> 
>     planner for #302 (run 38064902150)
> 
>  tests/test_raise_design.py | 308 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 308 insertions(+)
> """AGENTS.md records the raise design; the shared prompt section teaches it by example (#302).
> 
> The owner wants one place in AGENTS.md that says what code raises by itself and what agents raise by judgment, with
> code's who-can-address-whom table copied row for row and the two tiers of autonomy, and wants the one section the
> planner, worker and reviewer prompts share ("# Raising and answering", word for word the same in all three, from
> #300) to teach raising with an example of ever

`3. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima/roles/; grep -n "^# " dokima/roles/*.md; cat dokima/raises.py | head -80; grep -rn "roles/" .github/workflows/*.yml dokima/*.py | grep -v "^Binary" | head -30
```

> plan-grade.md
> planner.md
> result-grade.md
> reviewer.md
> worker.md
> dokima/roles/plan-grade.md:1:# Plan grade (shared by the planner and the reviewer of a plan)
> dokima/roles/worker.md:1:# Where you are
> dokima/roles/worker.md:8:# How you work
> dokima/roles/worker.md:34:# Every round
> dokima/roles/worker.md:42:# Raising and answering
> dokima/roles/worker.md:66:# What you hand back
> dokima/roles/result-grade.md:1:# Result grade (shared by the worker and the reviewer of a pull request)
> dokima/roles/reviewer.md:1:# Where you are
> dokima/roles/reviewer.md:8:# What you grade against
> dokima/roles/reviewer.md:14:# What you have
> dokima/roles/reviewer.md:19:# Every round
> dokima/roles/reviewer.md:28:# How you judge
> dokima/roles/reviewer.md:38:# Every ask of the owner
> dokima/roles/reviewer.md:45:# The plan's questions
> dokima/roles/reviewer.md:53:# Summing up the step you review
> dokima/roles/reviewer.md:59:# Raising and answering
> dokima/roles/reviewer.md:83:# What you hand back
> dokima/roles/planner.md:1:# Where you are
> dokima/roles/planner.md:9:# Every round
> dokima/roles/planner.md:17:# Judge the ask before you plan it
> dokima/roles/planner.md:28:# Links to other issues
> dokima/roles/planner.md:34:# Before you finish: the plan grade
> dokima/roles/planner.md:38:# The plan
> dokima/roles/planner.md:95:# Where your tests run
> dokima/roles/planner.md:104:# Split
> dokima/roles/planner.md:111:# Raising and answering
> dokima/roles/planner.md:135:# What you hand back
> """Raises: questions, blockers and issues an age

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raise_design.py 2>&1 | grep -E "^(FAILED|E  |[0-9]+ )" | head -30; grep -rn "## Questions\|Questions section\|# Raising and answering" tests/ dokima/*.py | grep -v test_raise_design | head
```

> E       AssertionError: 302.1: AGENTS.md does not have exactly one '## Raising and answering' section
> E       assert None
> E       AssertionError: 302.2: AGENTS.md does not have exactly one '## Raising and answering' section
> E       assert None
> E       AssertionError: 302.2: AGENTS.md does not have exactly one '## Raising and answering' section
> E       assert None
> E           AssertionError: 302.3: the shared section has no example of a question to the owner labelled 'Two readings'
> E           assert []
> E       AssertionError: 302.4: the shared section does not ask agents not to stay quiet
> E       assert None
> E        +  where None = <function search at 0x7f0e3c7f3060>('stay(ing)? quiet', '# Raising and answering\nThe planner, the worker and the reviewer raise and answer through two fields of their hand-b..., "text": "The board ignores closed pull requests, so their cards go stale.", "evidence": "dokima/board.py, column()"}', re.IGNORECASE)
> E        +    where <function search at 0x7f0e3c7f3060> = re.search
> E        +    and   re.IGNORECASE = re.I
> E       AssertionError: 302.5: AGENTS.md does not have exactly one '## Raising and answering' section
> E       assert None
> E       AssertionError: 302.6: the shared section has 3 example raises, fewer than 9
> E       assert 3 >= 9
> E        +  where 3 = len([{'kind': 'question', 'to': 'owner', 'label': 'Failed runs', 'text': 'Should a failed run move its card to Needs you? ..., 'text': 'The board ignores closed pull requests, so their c

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 585,700p tests/test_raise_handbacks.py; sed -n 125,160p tests/test_plan_check.py
```

> on = agent.next_step(items[:2], Q_PLAN, [OWNER], autopilot=lambda: True)
>     off = agent.next_step(items[:2], Q_PLAN, [OWNER], autopilot=lambda: False)
>     assert on == ("start", "reviewer", "plan"), f"300.4: on autopilot a plan with questions did not go to the plan reviewer: {on}"
>     assert off[0] == "stop", f"300.4: off autopilot a plan with questions did not stop for the owner: {off}"
> 
> 
> # 300.5: one shared section on raising and answering, with an example of each kind.
> 
> ROLE_FILES = ("planner", "worker", "reviewer")
> HEADING = "# Raising and answering"
> 
> 
> def section(role):
>     """The shared section of a role prompt, or None without one.
> 
>     It runs from its heading to the next top-level heading."""
>     lines = open(os.path.join(ROOT, "dokima", "roles", f"{role}.md")).read().splitlines()
>     at = [i for i, l in enumerate(lines) if l.strip() == HEADING]
>     if len(at) != 1:
>         return None
>     end = next((j for j in range(at[0] + 1, len(lines)) if lines[j].startswith("# ")), len(lines))
>     return "\n".join(lines[at[0]:end]).strip()
> 
> 
> def examples(text):
>     """Every JSON object in the text that opens with a "kind" key, parsed.
> 
>     One that does not parse fails the test."""
>     found, dec = [], json.JSONDecoder()
>     for m in re.finditer(r'\{\s*"kind"\s*:', text):
>         try:
>             found.append(dec.raw_decode(text[m.start():])[0])
>         except json.JSONDecodeError as e:
>             pytest.fail(f"300.5: an example raise in the shared section is not valid JSON (

**Agent:** I've checked the plan against the issue and run the planner's tests: all 7 fail today for the right reason, and none conflict with the tests from #300. Now writing the review.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned five criteria: one raising section in AGENTS.md, the who-can-raise-to-whom table matching code, labelled example raises in the shared prompt section, a closing five-item checklist, and an example of everything code raises itself.",
          "It wrote seven tests in tests/test_raise_design.py, one more proving that every example raise is one code accepts."],
  "decided": ["Today's Questions section in AGENTS.md folds into the new Raising and answering section, so raising lives in one place.",
              "The shared prompt section stays the one #300 put word for word in the planner, worker and reviewer prompts; no new prompt file."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of story 5, and each of its seven new tests fails today because the section and examples do not exist yet.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "AGENTS.md has one design section on raising. It lists what code detects and raises itself: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs you, and three blocks in a row. It lists the three kinds agents raise by judgment: question, blocker and issue.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "1.1"},
  {"ask": "It names doubt about the ask as an instance of the question kind: a question for you that carries its evidence.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "1.1"},
  {"ask": "The same section gives the who-can-address-whom table, row for row the same as the table in code.", "source": "https://github.com/dokima-dev/dokima/issues/302", "criterion": "1.2"},
  {"ask": "It gives the two tiers of autonomy: always on, the reviewer settles anything addressed to an agent and confirms issues before they are filed; on autopilot only, the revi
```

> Exit code 1
> summary holds 26 words, over its cap of 25 (up to 30 passes)
> the ask "AGENTS.md has one design section on raising. It lists what code detects and raises itself: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs you, and three blocks in a row. It lists the three kinds agents raise by judgment: question, blocker and issue." is matched to 1.1, which is not a criterion of the plan (302.1, 302.2, 302.3, 302.4, 302.5, 302.6)
> the ask "It names doubt about the ask as an instance of the question kind: a question for you that carries its evidence." is matched to 1.1, which is not a criterion of the plan (302.1, 302.2, 302.3, 302.4, 302.5, 302.6)
> the ask "The same section gives the who-can-address-whom table, row for row the same as the table in code." is matched to 1.2, which is not a criterion of the plan (302.1, 302.2, 302.3, 302.4, 302.5, 302.6)
> the ask "It gives the two tiers of autonomy: always on, the reviewer settles anything addressed to an agent and confirms issues before they are filed; on autopilot only, the reviewer answers a question for you only with your own words as evidence." is matched to 1.2, which is not a criterion of the plan (302.1, 302.2, 302.3, 302.4, 302.5, 302.6)
> the ask "The shared prompt section gives an example of each kind and each common instance you named." is matched to 1.3, which is not a criterion of the plan (302.1, 302.2, 302.3, 302.4, 302.5, 302.6)
> the as

`7. Bash`
```
cd /tmp/dokima-out; sed -i 's/"criterion": "1\./"criterion": "302./; s/"summary": "The plan keeps every ask of story 5, and each/"summary": "The plan keeps every ask of story 5; each/; s/fails today because the section and examples do not exist yet/fails today because the section and examples are missing/' review.json; cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 302 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#302](https://github.com/dokima-dev/dokima/issues/302) (AGENTS.md records how agents raise things, and the shared prompt section teaches it with examples). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Asks:** each of the eight asks in story 5's text matches one of the plan's criteria, 302.1 to 302.5, and none is missing. The plan answers the owner's later comments too:
  - code's table and AGENTS.md's table are compared row for row;
  - there is an example of every one of the seven things code raises by itself;
  - doubt about the ask is named as a kind of question;
  - the five-item checklist comes at the very end, after the last example.
- **Tests:** I ran the 7 new tests in `tests/test_raise_design.py`. All 7 fail today for the right reason: the AGENTS.md section is missing, the labelled examples are missing, or there are only 3 example raises where 9 are needed. None crashes or fails on a bad path.
  - The table test also proves it would catch a drift: it drops one row and widens another, and checks the comparison notices both.
  - The example tests check each example with code's own raise check.
- **Fit with existing work:** the plan grows the one shared section that [#300](https://github.com/dokima-dev/dokima/issues/300) (the shared raising section in the three role prompts) put in the planner, worker and reviewer prompts. The tests #300 left in `tests/test_raise_handbacks.py` still fit with this change.
- **Decision the owner should know:** the plan folds today's "Questions" section of AGENTS.md into the new "Raising and answering" section. I read that as what "one design section" asks for, so I did not block on it.

The plan has no questions and nothing earlier was waiting for an answer, so I raised nothing and answered nothing.
