# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37871687964

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (186.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5f18974d-9f0e-4013-ac81-f2ca9c27bb40/tool-results/bqap02fnu.txt
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
> <!-- /dokima-car

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md | head -300; wc -c issue.md
```

> <!-- dokima-ask -->
> 
> Agents raise things through about ten different fields today (questions, concerns, replies, suspect tests, outside scope, blockers, notes, assumptions, issues found, outside plan, resolved). They are the same few ideas in different clothes. I want the smallest set that covers every case.
> 
> What I want:
> - Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).
> - A raise is exactly one of three kinds: question (for me; on autopilot the reviewer answers it for me when my own words settle it, with them as evidence), blocker (names who must fix it), or issue (outside this one; code files it). The list is closed: the checker rejects any other kind, and adding a kind is a code change I approve, never something an agent invents.
> - Who can raise to whom is a fixed table in code: the planner raises questions to me; the worker raises blockers for the planner only through the reviewer, who judges whether they are real; the reviewer raises to the planner, the worker or me; anyone can raise an issue. The checker rejects anything outside the table.
> - Every raise addressed to an agent is answered by that agent in its next turn, done or disagree with why. The checker rejects a turn that skips one, so nothing is ever dropped. Three blocks in a row still stop and come to me.
> - Cards show one Raised section, each line with its kind's icon and who it is fo

`3. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md; cat open_blockers.json; for f in in/*; do echo "== $f"; python3 -c "
import json,sys;d=json.load(open('$f'));h=d.get('handback',d);print(json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','resolved','questions','replies']},indent=0)[:4000]);print('check',d.get('check'))"; done
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
> 1870:### RezaSoleymanifar on issue #289 (2026-10-09T01:47:51Z)
> 1874:### dokima-runtime on issue #289 (2026-10-09T01:48:11Z)
> 2132:### dokima-runtime on issue #289 (2026-10-09T01:50:15Z)
> []== in/01-planner.json
> {
> "verdict": null,
> "summary": "Agents raise and answer through two fields, raises and answers, with three kinds and a fixed table of who raises to whom.",
> "blockers": null,
> "resolved": null,
> "questions": [
> {
> "question": "When the reviewer raises something to you, is it always a question, with a blocker only ever for the planner or the worker?",
> "assumption": "Yes: the reviewer raises questions to you (such as a change outside the plan or a

**Agent:** Now the owner's comments.

`4. Bash`
```
cd /tmp/pack; for n in 440 844 1334 1870; do sed -n "${n},$((n+11))p" issue.md; echo ----; done
```

> ### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 
> /plan Answers:
> - Any stage can raise any kind; the only limit is the who-can-address-whom table. The reviewer can raise a question or a blocker to me (a change beyond the plan is a blocker for me, since only I can accept it).
> - Think of it in three levels. Archetype: raise. Kind: question, blocker, issue, a closed list in code, because each kind does something different (stop for me, route to whoever fixes it, file an issue); a new kind only with my approval. Instance: a short label such as outside plan, outside scope or suspect test, used for display and prompt examples, with no behavior of its own, so adding one is cheap and safe.
> - So today's fields map like this: outside plan and outside scope are blockers for me; suspect tests are blockers for the planner, through the reviewer; notes are dropped.
> - Blocked by, blocks and relates to are not raises; they stay the planner's own links field.
> 
> ### dokima-runtime on issue #289 (2026-10-09T01:27:45Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner proposes a split into 4 stories and asks you questions.
> ----
> ### RezaSoleymanifar on issue #289 (2026-10-09T01:39:55Z)
> 
> /plan Narrowing this issue

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('plan.json'));print(json.dumps(d,indent=1))"
```

> {
>  "kind": "feature",
>  "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
>  "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. Before each run, code hands the agent the exact list of open raises it must answer. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river, the prompts and AGENTS.md). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the starting pack, the river and one shared prompt section; depends on (1) and (2). (4) the reviewer settles workers' raises and confirms issues before code files them; depends on (3). (5) AGENTS.md records the design, and the shared prompt section gives many examples and asks agents to raise actively; depends on (3) and (4). This round adds your comment of 2026-10-09T01:47:51Z to story 5: AGENTS.md and the prompts give an example of each thing code raises itself, so agents never raise those. Story 2 now tests that what code detects still draws as today. What code detects (work outside the plan, failing tests, red main, merge conflicts, a rejected hand-

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json
a=json.load(open('in/07-planner.json'));b=json.load(open('in/09-planner.json'));p=json.load(open('plan.json'))
print(a.get('run_id'),b.get('run_id'), a.keys())
print(a['handback']==b['handback'], b['handback']==p)
import difflib
x=json.dumps(a['handback'],indent=1).splitlines();y=json.dumps(b['handback'],indent=1).splitlines()
print('\n'.join(difflib.unified_diff(x,y,lineterm='')))
r=json.load(open('in/08-reviewer-plan.json'));print(json.dumps(r['handback'],indent=1))
"; sed -n 2132,2140p issue.md; tail -5 issue.md
```

> 37871278316 37871501057 dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> False True
> --- 
> +++ 
> @@ -1,7 +1,7 @@
>  {
>   "kind": "feature",
>   "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
> - "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. Before each run, code hands the agent the exact list of open raises it must answer. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river, the prompts and AGENTS.md). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the starting pack, the river and one shared prompt section; depends on (1) and (2). (4) the reviewer settles workers' raises and confirms issues before code files them; depends on (3). (5) AGENTS.md records the design, and the shared prompt section gives many examples and asks agents to raise actively; depends on (3) and (4). This round adds your comment of 2026-10-09T01:45:00Z: the pack lists every open raise to answer, the AGENTS.md design section, and abundant pro

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline main..HEAD; git diff --stat main; ls /tmp/dokima-out 2>/dev/null
```

> claude.json

`8. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/dokima-out; python3 - <<'EOF'
import json
I="https://github.com/dokima-dev/dokima/issues/289"
r=json.load(open('/tmp/pack/in/08-reviewer-plan.json'))['handback']
asks=r['asks']
asks+= [
 {"ask":"Stays deterministic, raised by code only, each keeping its own name and icon: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs me, three blocks in a row.","source":I,"criterion":"S2.5"},
 {"ask":"the prompts and AGENTS.md also give an example for each thing code raises itself (work outside the plan, a failing test, red main, a merge conflict, a rejected hand-back, a workflow file change, three blocks in a row), so agents know what each looks like and never raise these themselves.","source":I,"criterion":"S5.5"},
]
for a in asks:
    if a["ask"].startswith("blocker (names who must fix it)"): a["criterion"]="S1.2"
out={
"previous_step":{
 "did":["The planner added the owner's comment of 2026-10-09T01:47:51Z as story 5's fifth criterion: AGENTS.md and the shared prompt section give an example of every thing code raises itself, and the prompt says agents never raise these.",
        "Story 2 now has a criterion, not only a non-functional line, that what code detects keeps its own name, icon and place on the card exactly as today."],
 "decided":["Story 5 grows the one shared prompt file story 3 adds, rather than adding a second one."],
 "open":["Asks what the planner's concerns become, since they are not one of the three kinds."]},
"verdict":"approve",
"summary":"The re-plan now keeps your newest ask (examples of what code raises itself) and every earlier one; its question on the planner's concerns changes the river, so it still waits for you.",
"blockers":[],
"notes":[
 {"text":"Your 'No backfill: old issues keep their old records as they are' is kept only in story 2's context, not as a criterion; story 2's own plan should test that a record posted before the chan
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`9. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
d=json.load(open('review.json'))
d['summary']="The re-plan keeps every ask, including your newest; its question on the planner's concerns changes the river, so it waits for you."
json.dump(d,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for issue #289. It still waits for you on one question: what the planner's concerns become. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

**What changed since my last review:** the planner added your comment of 2026-10-09T01:47:51Z as story 5's fifth criterion. AGENTS.md and the shared prompt section will each give an example of everything code raises itself, and the prompt will tell agents never to raise those. Story 2 also turns "what code detects keeps its own name, icon and place, exactly as today" into a full criterion; before, it was only a non-functional line.

**Asks:** every ask in the issue and your four comments maps to a criterion in the 5-story split. None is missing.

**Your open question:**
- **The question:** the planner's concerns (a doubt about the ask, with evidence) aren't one of the three kinds, so where do they go?
- **The planner's guess:** a concern about this issue becomes a question for you, and one about another issue becomes an issue raise.
- **Why I didn't accept it:** today a concern doesn't stop the river or file anything, and under this guess it would do both. None of your comments says where concerns go.

So on autopilot the river stops here until you answer with `/plan` and your words. You can also say `/review` to go on with the planner's guess.

**Two notes, not blockers:**
- "No backfill" sits only in story 2's background text, not in a criterion. Story 2's own plan should test that records posted before the change look the same as today.
- Story 4 treats an issue the reviewer raises itself as already confirmed. If you want those checked again before they're filed too, say so when you answer the concerns question.

There were no earlier blockers to carry over, and this split adds no tests yet, so there was nothing to run.
