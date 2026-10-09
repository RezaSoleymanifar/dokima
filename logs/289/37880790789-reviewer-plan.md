# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37880790789

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (230.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/30a3d7a3-6bb4-490c-9353-7f7f20e36226/tool-results/bcwx7vlqq.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-planner.json
> 06-reviewer-plan.json
> 07-planner.json
> 08-reviewer-plan.json
> 09-planner.json
> 10-reviewer-plan.json
> 11-planner.json
> # Issue #289: Every agent raises things and answers them through the same two fields
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 268 -->
> Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #289](https://github.com/dokima-dev/dokima/issues/289)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #268
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #241, #175, #268, #265, #193, #236, #51
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16"

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json in/*; cat open_blockers.json; grep -n "^## \|^### \|dokima-original\|<!-- dokima" issue.md | head -80
```

> 215527 issue.md
>  20122 plan.json
>      2 open_blockers.json
>  11840 in/01-planner.json
>   5872 in/02-reviewer-plan.json
>  13586 in/03-planner.json
>   5772 in/04-reviewer-plan.json
>  15936 in/05-planner.json
>   7968 in/06-reviewer-plan.json
>  19523 in/07-planner.json
>   8587 in/08-reviewer-plan.json
>  20348 in/09-planner.json
>   9190 in/10-reviewer-plan.json
>  20865 in/11-planner.json
> 375138 total
> []3:<!-- dokima-card -->
> 4:<!-- dokima-linked-from: 268 -->
> 27:<!-- dokima-ask -->
> 39:## Comments
> 41:### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 45:### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 49:### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 54:### dokima-runtime on issue #289 (2026-10-09T00:13:36Z)
> 56:<!-- dokima-record -->
> 269:### dokima-runtime on issue #289 (2026-10-09T00:16:36Z)
> 271:<!-- dokima-record -->
> 453:### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 461:### dokima-runtime on issue #289 (2026-10-09T01:27:45Z)
> 463:<!-- dokima-record -->
> 673:### dokima-runtime on issue #289 (2026-10-09T01:30:29Z)
> 675:<!-- dokima-record -->
> 857:### RezaSoleymanifar on issue #289 (2026-10-09T01:39:55Z)
> 869:### dokima-runtime on issue #289 (2026-10-09T01:40:19Z)
> 871:<!-- dokima-record -->
> 1100:### dokima-runtime on issue #289 (2026-10-09T01:43:15Z)
> 1102:<!-- dokima-record -->
> 1347:### RezaSoleymanifar on issue #289 (2026-10-09T01:45:00Z)
> 1354:### dokima-runtime on issue #289 (2026-10-09T01:45:18Z)
> 1356:<!-- dokima-record -->
> 1610:### dokima-runtime on issue #289

`3. Bash`
```
cd /tmp/pack; sed -n 20,55p issue.md; sed -n 453,460p issue.md; sed -n 857,868p issue.md; sed -n 1347,1353p issue.md; sed -n 1883,1886p issue.md; sed -n 2428,2431p issue.md; sed -n 2682,2720p issue.md
```

> **Out of scope:**
> 
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Agents raise things through about ten different fields today (questions, concerns, replies, suspect tests, outside scope, blockers, notes, assumptions, issues found, outside plan, resolved). They are the same few ideas in different clothes. I want the smallest set that covers every case.
> 
> What I want:
> - Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).
> - A raise is exactly one of three kinds: question (for me; on autopilot the reviewer answers it for me when my own w

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json
d=json.load(open('in/10-reviewer-plan.json'));print(json.dumps(d,indent=1)[:9000])"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37871687964",
>  "commit_before": "a302cb153f452b7209be0cecbebe5c55dc9a4e5b",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 49090,
>   "turns": 10,
>   "cost_usd": 0.4419582,
>   "tokens_in": 436202,
>   "tokens_out": 5045
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/289/37871687964-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37871687964",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner added the owner's comment of 2026-10-09T01:47:51Z as story 5's fifth criterion: AGENTS.md and the shared prompt section give an example of every thing code raises itself, and the prompt says agents never raise these.",
>     "Story 2 now has a criterion, not only a non-functional line, that what code detects keeps its own name, icon and place on the card exactly as today."
>    ],
>    "decided": [
>     "Story 5 grows the one shared prompt file story 3 adds, rather than adding a second one."
>    ],
>    "open": [
>     "Asks what the planner's concerns become, since they are not one of the three kinds."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The re-plan keeps every ask, including your newest; its question on the planner's concerns changes the river, so it waits for you.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "Your 'No backfill: old issues keep their old records as they are' is kept only in story 2's context, not as 

**Agent:** Now the newest plan.

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json
d=json.load(open('plan.json'));print(json.dumps(d,indent=1))"; python3 -c "
import json
d=json.load(open('in/11-planner.json'));h=d.get('handback');print({k:v for k,v in d.items() if k!='handback'})"
```

> {
>  "kind": "feature",
>  "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
>  "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. Before each run, code hands the agent the exact list of open raises it must answer. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river, the prompts and AGENTS.md). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the starting pack, the river and one shared prompt section; depends on (1) and (2). (4) the reviewer settles workers' raises and confirms issues before code files them; depends on (3). (5) AGENTS.md records the design, and the shared prompt section gives many examples and asks agents to raise actively; depends on (3) and (4). This round follows your answer of 2026-10-09T03:44:37Z: a doubt about the ask becomes a question for you, with its evidence. Story 3 retires the planner's concerns into such questions, and story 5 adds doubt about the ask as a named instance of the question kind, with examples. What code detects (work outside the plan, failing test

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def said_there\|def pack\|def open_blockers\|def problems_round\|def next_step" dokima/agent.py; python3 -m dokima.agent check plan /tmp/pack/plan.json 289 2>&1 | tail -3
```

> 120:def open_blockers(recs, stage):
> 192:def problems_round(role, h, pack_dir):
> 640:def pack(repo, number, role, stage, dest):
> 1442:def said_there(words, source, items, body, owners, number):
> 1467:def next_step(items, rec, owners, rounds=3, autopilot=lambda: False, body="", number=""):
> the check needs plan.json and the issue number: agent check review|work FILE PLAN N

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/w.py <<'EOF'
import json
I="https://github.com/dokima-dev/dokima/issues/289"
C1=I+"#issuecomment"  # placeholder not used
src=I
asks=json.load(open('/tmp/pack/in/10-reviewer-plan.json'))['handback']['asks']
asks.append({"ask":"No backfill: old issues keep their old records as they are.","source":src,"criterion":"missing"})
asks.append({"ask":"a doubt about the ask becomes a question for me, with its evidence.","source":src,"criterion":"S3.1"})
asks.append({"ask":"Add \"doubt about the ask\" as a named instance of the question kind, with examples.","source":src,"criterion":"S5.3"})
r={"previous_step":{"did":["The planner took the owner's answer of 2026-10-09T03:44:37Z: the planner's concerns field goes, and a doubt about the ask reaches the owner as a question carrying its evidence (story 3, criterion 1).","Story 5 names doubt about the ask as an instance of the question kind in AGENTS.md and gives examples of it in the shared prompt section."],
 "decided":["Doubt about the ask is a label only, with no behavior of its own."],
 "open":["The plan has no questions left for the owner."]},
 "verdict":"block",
 "summary":"The re-plan takes your answer on doubts about the ask, but your 'No backfill: old issues keep their old records as they are' still has no criterion, so nothing stops the new checks from breaking old issues.",
 "blockers":[{"id":"B1","criterion":"S2","test":None,
  "problem":"The owner's ask 'No backfill: old issues keep their old records as they are' is only in story 2's context, not an acceptance criterion of any story. In a split, /work approves each story's criteria as final, so no test will ever hold it. Story 3 makes the checker reject every old field and rebuilds the starting pack from the issue's history, and story 2 redraws cards from raises and answers; code that misreads or rejects an older record would pass every criterion as written.",
  "evidence":"Owner comment 2026-10-09T01:39:55Z ('No backfill: old issu
```

> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> blocker B1 names S2, which is not a criterion of the plan (S1.1, S1.2, S1.3, S1.4, S1.5, S2.1, S2.2, S2.3, S2.4, S2.5, S3.1, S3.2, S3.3, S3.4, S3.5, S4.1, S4.2, S4.3, S5.1, S5.2, S5.3, S5.4, S5.5)
> rc=1

`8. Bash`
```
cd /tmp; sed -i 's/"criterion":"S2","test"/"criterion":"S2.5","test"/; s/"summary":"The re-plan takes.*nothing stops the new checks from breaking old issues."/"summary":"The re-plan takes your answer on doubts about the ask, but your no-backfill ask still has no criterion or test."/' w.py; python3 w.py; cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for issue #289 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json`, and it passes both hand-back checks.

**What the planner did:** it took the owner's answer of 2026-10-09T03:44:37Z.
- The planner's concerns field goes away. A doubt about the ask now reaches the owner as a question that carries its evidence (story 3, criterion 1).
- Story 5 names "doubt about the ask" as a kind of question in AGENTS.md and gives examples of it in the shared prompt section.
- The plan has no questions left for the owner.

**Blocker B1 (for the planner):** the owner wrote "No backfill: old issues keep their old records as they are" in the comment of 2026-10-09T01:39:55Z. That ask is only in story 2's background text; no story has it as an acceptance criterion, so nothing will test it.
- This is a split plan, so `/work` approves each story's criteria as final.
- Story 3 makes the checker reject every old field and rebuilds the starting pack from the issue's history. Story 2 redraws cards from the new fields. Code that breaks on an older record would still pass every criterion as written.
- **Fix:** add one criterion to story 2 or 3. A record posted before this change keeps its comment exactly as it is, the issue card and a new run's starting pack still read it without error, and only new hand-backs must use the new fields.

**Why I blocked when round 5 approved:** the round 5 review raised this same gap only as a note, and the planner did not take it up. Under the grading rules, an owner's ask with no criterion is a blocker. Because the issue is on autopilot, it goes back to the planner without waiting for the owner.

**Notes (not blocking):**
- Story 4 still treats an issue the reviewer raises itself as already confirmed. The plan says this openly.
- Some line numbers cited for `dokima/agent.py` have drifted (for example `problems_round()` is now at line 192). The function names still find them.

The plan has no tests yet because the stories come first, so I had no new tests to run.
