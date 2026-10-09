# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37871138731

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (98.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9d7a0886-9590-49c2-93c8-7d41ac49f0b5/tool-results/b2z3tyzj1.txt
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
> Agents raise things through about ten different f

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md | head -200
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
cd /tmp/pack; grep -n '^### ' issue.md; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))" | head -400
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
> []{
>  "kind": "feature",
>  "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
>  "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river and all three prompts). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the river and one shared prompt section; depends on (1) and (2). (4) the reviewer set

`4. Bash`
```
cd /tmp/pack; sed -n '440,447p;844,855p' issue.md; ls in; for f in in/0[24]*; do python3 -c "
import json,sys;d=json.load(open('$f'));h=d.get('handback',d);print('$f',json.dumps({k:h.get(k) for k in ['verdict','summary','blockers','assumptions','resolved','notes']},indent=1))"; done
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
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/05-planner.json'));print({k:v for k,v in d.items() if k!='handback'})"; cd /home/runner/work/dokima/dokima; git status --short; git log --oneline -2; grep -n "outside_plan\|concerns\|fence\|dropped" dokima/agent.py | head -40
```

> {'role': 'planner', 'stage': None, 'run_id': '37870869697', 'commit_before': 'a302cb153f452b7209be0cecbebe5c55dc9a4e5b', 'started_by': 'RezaSoleymanifar', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 140464, 'turns': 13, 'cost_usd': 0.8231107999999999, 'tokens_in': 697791, 'tokens_out': 15425}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/289/37870869697-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/37870869697', 'check': {'passed': True, 'problems': []}}
> a302cb1 The Autopilot view shows only open issues and pull requests (#286)
> 1c8e0e0 The issue card and the planner's run comment show the links, each kind with its own icon (#281)
> 251:    dropped = os.path.join(out, "dropped.txt")
> 252:    if os.path.exists(dropped):
> 253:        rec["dropped_by_fence"] = [l for l in open(dropped).read().splitlines() if l.strip()]
> 381:                  ("Concerns", bullets(h.get("concerns"), lambda c: f"{c.get('text', '')} ({c.get('evidence', '')})")),
> 395:                  (f"{mark('outside the plan')} Outside the plan", bullets(h.get("outside_plan"), lambda o: f"{o.get('file', '')}: {o.get('change', '')}")),
> 845:        bad += problems_items(h, "outside_plan", ("file", "change"))

**Agent:** I'm checking the split plan for #289 against your comments and writing the plan review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["Re-planned the split into four stories after the owner's comment of 2026-10-09T01:39:55Z: the kinds and table in code, the cards, every hand-back with the river and prompts, and the reviewer settling raises and confirming issues."],
  "decided": ["The issue covers only agents' judgments; what code detects (work outside the plan, failing tests, red main, merge conflicts, rejected hand-backs, workflow changes, three blocks) keeps its own name and icon.", "Code stamps each raise with its raiser and an ID that never shows on a card; old records are not backfilled."],
  "open": ["Two questions for the owner: whether outside_plan and outside_scope simply go, and what the planner's concerns become."]
 },
 "verdict": "approve",
 "summary": "The re-plan follows your narrowing and gives every ask to one story; of its two questions, dropping the outside-the-plan fields matches your words, but turning concerns into questions and filed issues changes what stops and what gets filed, so that one waits for you.",
 "blockers": [],
 "notes": [
  {"text": "You said the reviewer can raise a blocker to you; S1.2 allows it, but S3.3 only routes a blocker 'to the agent it names' and a question for you. The story 3 plan should say a blocker for you stops for you.", "evidence": "plan.json stories[2].acceptance_criteria[2]; owner comment 2026-10-09T01:27:26Z"},
  {"text": "The issue says a blocker 'names who must fix it'; the earlier plan had its own criterion for that and this one leaves it to the table check of S1.2. The story 1 plan should test that a blocker with no one named is rejected.", "evidence": "plan.json stories[0].acceptance_criteria[1]; in/01-planner.json story 1 criterion 3"},
  {"text": "Story 4 assumes the reviewer's own issue raises count as confirmed; that reading is stated in the context, not asked, and the story 4 plan should keep it visible to you.", "evidence": "plan.j
```

> summary holds 44 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`7. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The re-plan covers every ask; dropping the outside-the-plan fields matches your words, but what concerns become changes the river, so that waits for you."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-planned split for #289, with no blockers. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**What the plan is now:** four stories that follow your narrowing comment of 01:39:
1. The three kinds, the who-raises-to-whom table, and code stamping who raised each item with an ID.
2. The cards: one Raised section, earlier raises shown apart on the review card, and no IDs on any card.
3. Every hand-back moves to raises and answers, with the river and one shared prompt section.
4. The reviewer settles what agents raise to each other and confirms issues before code files them.

Each of the 20 things you asked for, across the issue and your two comments, is kept by exactly one criterion. Since this round is a split, the plan has no tests yet; each story's own plan will write them.

**The planner's two questions:**
- **Accepted:** dropping the `outside_plan` and `outside_scope` fields. Your words "Stays deterministic, raised by code only, each keeping its own name and icon: work outside the plan" settle it. Today `outside_plan` is only drawn on the card (`dokima/agent.py:395`) and nothing routes by it, while code's own outside-the-plan check (`dokima/agent.py:251`) stays as it is.
- **Not accepted, so it waits for you:** what the planner's concerns become. The plan would turn a concern about this issue into a question that stops for you, and an overlap with another issue into a new issue that code files. Today a concern stops nothing and files nothing, and your words don't say where concerns go.

**Three notes for the story plans:**
- You said the reviewer can raise a blocker to you, but story 3 only routes a blocker "to the agent it names". Its plan should say a blocker for you stops for you.
- The earlier plan checked that a blocker names who must fix it; this one relies on the who-to-whom table to catch that. Story 1 should test it directly.
- Story 4 treats the reviewer's own issue raises as already confirmed. The planner stated that reading in the story's background rather than asking you, so it should stay visible to you.

I didn't map "No backfill" to a criterion: it asks for nothing to be built, and story 2 says old records are not redrawn.
