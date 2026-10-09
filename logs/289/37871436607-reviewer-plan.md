# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37871436607

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (143.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f0d172f6-ffa0-47e5-94ff-9fed3283aae1/tool-results/bfpvne9bm.txt
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
> # Issue #289: Every agent raises things and answers them through the same two fields
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #289](https://github.com/dokima-dev/dokima/issues/289)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Agents rai

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n '20,400p'
```

> - A raise is exactly one of three kinds: question (for me; on autopilot the reviewer answers it for me when my own words settle it, with them as evidence), blocker (names who must fix it), or issue (outside this one; code files it). The list is closed: the checker rejects any other kind, and adding a kind is a code change I approve, never something an agent invents.
> - Who can raise to whom is a fixed table in code: the planner raises questions to me; the worker raises blockers for the planner only through the reviewer, who judges whether they are real; the reviewer raises to the planner, the worker or me; anyone can raise an issue. The checker rejects anything outside the table.
> - Every raise addressed to an agent is answered by that agent in its next turn, done or disagree with why. The checker rejects a turn that skips one, so nothing is ever dropped. Three blocks in a row still stop and come to me.
> - Cards show one Raised section, each line with its kind's icon and who it is for.
> - One shared section on raising and answering in the prompts, the same for all three agents, with examples for each kind.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 
> Autopilot is on for #289. Planning started for #289, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #289 (2026-10-09T00:13:36

`3. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md; cat open_blockers.json; ls -la in
```

> 28:### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 32:### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 36:### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 41:### dokima-runtime on issue #289 (2026-10-09T00:13:36Z)
> 256:### dokima-runtime on issue #289 (2026-10-09T00:16:36Z)
> 440:### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 448:### dokima-runtime on issue #289 (2026-10-09T01:27:45Z)
> 660:### dokima-runtime on issue #289 (2026-10-09T01:30:29Z)
> 844:### RezaSoleymanifar on issue #289 (2026-10-09T01:39:55Z)
> 856:### dokima-runtime on issue #289 (2026-10-09T01:40:19Z)
> 1087:### dokima-runtime on issue #289 (2026-10-09T01:43:15Z)
> 1334:### RezaSoleymanifar on issue #289 (2026-10-09T01:45:00Z)
> 1341:### dokima-runtime on issue #289 (2026-10-09T01:45:18Z)
> 1597:### dokima-runtime on issue #289 (2026-10-09T01:46:59Z)
> []total 96
> drwxr-xr-x 2 runner runner  4096 Oct  9 01:47 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 01:47 ..
> -rw-r--r-- 1 runner runner 11840 Oct  9 01:47 01-planner.json
> -rw-r--r-- 1 runner runner  5872 Oct  9 01:47 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13586 Oct  9 01:47 03-planner.json
> -rw-r--r-- 1 runner runner  5772 Oct  9 01:47 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 15936 Oct  9 01:47 05-planner.json
> -rw-r--r-- 1 runner runner  7968 Oct  9 01:47 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 19523 Oct  9 01:47 07-planner.json
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n '440,447p;844,855p;1334,1340p' issue.md; python3 -c "
import json
for f in ['in/04-reviewer-plan.json','in/06-reviewer-plan.json']:
  d=json.load(open(f)); h=d.get('handback',d); print(f, json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','notes','assumptions']},indent=1))
"
```

> ### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 
> /plan Answers:
> - Any stage can raise any kind; the only limit is the who-can-address-whom table. The reviewer can raise a question or a blocker to me (a change beyond the plan is a blocker for me, since only I can accept it).
> - Think of it in three levels. Archetype: raise. Kind: question, blocker, issue, a closed list in code, because each kind does something different (stop for me, route to whoever fixes it, file an issue); a new kind only with my approval. Instance: a short label such as outside plan, outside scope or suspect test, used for display and prompt examples, with no behavior of its own, so adding one is cheap and safe.
> - So today's fields map like this: outside plan and outside scope are blockers for me; suspect tests are blockers for the planner, through the reviewer; notes are dropped.
> - Blocked by, blocks and relates to are not raises; they stay the planner's own links field.
> 
> ### RezaSoleymanifar on issue #289 (2026-10-09T01:39:55Z)
> 
> /plan Narrowing this issue. It now covers only the agents' judgments; everything code already detects stays exactly as it is.
> 
> Stays deterministic, raised by code only, each keeping its own name and icon: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs me, three blocks in a row.
> 
> Raise and answer, for model judgment only: question, blocker (for example a weak test, a wrong plan, a missing

`5. Bash`
```
cd /tmp/pack; sed -n '1597,1610p' issue.md; python3 -c "
import json
d=json.load(open('plan.json')); print(json.dumps(d,indent=1))
"
```

> ### dokima-runtime on issue #289 (2026-10-09T01:46:59Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> **Reviewer (plan)** · setting up
> 
> The machine is setting up: the branch, the starting pack and the tools. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37871436607)</sub>
> 
> {
>  "kind": "feature",
>  "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
>  "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. Before each run, code hands the agent the exact list of open raises it must answer. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river, the prompts and AGENTS.md). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the starting p

**Agent:** I'm reviewing the newest plan (round 4) against every owner comment; next I'll check how the checker validates the asks list.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;d=json.load(open('/tmp/pack/in/07-planner.json'));print(d.get('check'))"; grep -n "asks\|missing" dokima/agent.py | head -40
```

> {'passed': True, 'problems': []}
> 147:        return ["open_issues.json is missing from the pack, so the links cannot be checked"]
> 248:        handback = {"missing": f"{HANDBACK[role]}: {e}"}
> 396:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 418:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 421:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 669:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 706:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 710:def problems_asks(r, ids):
> 711:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 712:    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
> 713:    asks = r.get("asks")
> 714:    if not isinstance(asks, list) or not asks:
> 715:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 716:                "\"source\": \"a link to where they said it\", \"criterion\": \"N.k\" or \"missing\"}"]
> 717:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 718:    good = [a for a in asks if isins

`7. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/06-reviewer-plan.json'));h=d.get('handback',d)
for a in h['asks']: print(a['criterion'],'|',a['ask'][:150],'|',a['source'])"
```

> S3.1 | Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, crit | https://github.com/dokima-dev/dokima/issues/289
> S1.1 | A raise is exactly one of three kinds: question ..., blocker ..., or issue ... The list is closed: the checker rejects any other kind | https://github.com/dokima-dev/dokima/issues/289
> S1.2 | blocker (names who must fix it) | https://github.com/dokima-dev/dokima/issues/289
> S4.2 | issue (outside this one; code files it) | https://github.com/dokima-dev/dokima/issues/289
> S1.2 | Who can raise to whom is a fixed table in code ... The checker rejects anything outside the table. | https://github.com/dokima-dev/dokima/issues/289
> S3.2 | Every raise addressed to an agent is answered by that agent in its next turn, done or disagree with why. The checker rejects a turn that skips one | https://github.com/dokima-dev/dokima/issues/289
> S3.3 | Three blocks in a row still stop and come to me. | https://github.com/dokima-dev/dokima/issues/289
> S2.1 | Cards show one Raised section, each line with its kind's icon and who it is for. | https://github.com/dokima-dev/dokima/issues/289
> S3.5 | One shared section on raising and answering in the prompts, the same for all three agents, with examples for each kind. | https://github.com/dokima-dev/dokima/issues/289
> S1.2 | Any stage can raise any kind; the only limit is the who-can-address-whom table. | https://github.com/dokima-dev/dokima/issues/2

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/gen.py <<'EOF'
import json
I="https://github.com/dokima-dev/dokima/issues/289"
def a(ask,c): return {"ask":ask,"source":I,"criterion":c}
r={"previous_step":{
 "did":["The planner re-planned the split into 5 stories, adding a fifth story for the AGENTS.md design section and the shared prompt examples from the owner's comment of 2026-10-09T01:45:00Z.",
        "Story 3 now has each agent's starting pack list every open raise addressed to it, or passing through it for the reviewer, and rejects a hand-back that leaves one unanswered."],
 "decided":["What code detects (work outside the plan, failing tests, red main, merge conflicts, rejected hand-backs, workflow changes, three blocks in a row) keeps its own sections, unchanged.",
            "An issue the reviewer raises itself counts as confirmed and its card says so."],
 "open":["Asks what the planner's concerns become, since they are not one of the three kinds."]},
 "verdict":"approve",
 "summary":"The re-plan adds your three new asks and keeps every earlier one; its one question, what the planner's concerns become, changes the river, so it waits for you.",
 "blockers":[],
 "notes":[
  {"text":"Your words 'everything code already detects stays exactly as it is', each keeping its own name and icon, are kept only as story 2's non-functional line, not as a criterion; story 2's own plan should test that those sections still draw as today.",
   "evidence":"plan.json stories[1].non_functional[0]; owner comment 2026-10-09T01:39:55Z"},
  {"text":"Story 3's prompt section (S3.5, one example per kind) and story 5's (S5.3, S5.4, many examples) change the same new file; story 5's plan should grow that file, not add a second one.",
   "evidence":"plan.json stories[2].context and stories[4].context"}],
 "resolved":[],
 "issues_found":[],
 "asks":[
  a("Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan,
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> 0

`9. Bash`
```
sed -i 's/"summary":"The re-plan adds your three new asks and keeps every earlier one; its one question, what the planner.s concerns become, changes the river, so it waits for you."/"summary":"The re-plan keeps every ask, including your three new ones; its question on the planner'"'"'s concerns changes the river, so it waits for you."/' /tmp/gen.py && python3 /tmp/gen.py && cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?; grep -o '"summary": "[^"]*"' /tmp/dokima-out/review.json
```

> 0
> "summary": "The re-plan keeps every ask, including your three new ones; its question on the planner's concerns changes the river, so it waits for you."

**Agent:** I approved the round-4 plan for issue #289. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass with no problems.

**The plan:** five stories.
1. The three kinds of raise and the table of who can raise to whom, checked in code.
2. The cards show what was raised and how each earlier raise was answered.
3. Every agent's hand-back moves to the two fields `raises` and `answers`, and each agent's starting pack lists the raises it must answer.
4. The reviewer settles raises between agents and confirms issues before code files them.
5. The design section in AGENTS.md, and the shared prompt section with many examples.

**Your asks:** I listed 27 from the issue and your three comments. Each maps to a criterion in the plan, and none is missing. There were no open blockers from earlier rounds.

**Its one question needs you:** what the planner's "concerns" become. The plan assumes a concern about this issue becomes a question for you, and a concern about another issue becomes an issue raise. I did not accept this assumption because it changes the river: a concern stops nothing today, but as a question it would stop the river, and as an issue raise it would file a new GitHub issue each time. Your words don't settle where concerns go, so on autopilot this waits for your answer.

**Notes:**
- You said "everything code already detects stays exactly as it is", each keeping its own name and icon. The plan keeps this only as a non-functional line in story 2, not as a tested criterion. Story 2's own plan should test that those sections still show as they do today.
- Stories 3 and 5 both write the shared prompt section. Story 5 should add to the file story 3 creates, not start a second one.

The plan has no tests of its own to run yet, because a split's stories each get their own plan and tests.
