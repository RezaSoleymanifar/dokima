# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37870109421

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (62.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8ea0d769-0a23-4e08-8013-b4b9f075ab99/tool-results/b0of9rqfs.txt
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
> Agents raise things through about ten different fields today (questions, concerns, repl

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md
```

> <persisted-output>
> Output too large (48.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8ea0d769-0a23-4e08-8013-b4b9f075ab99/tool-results/bd0oo00wx.txt
> 
> Preview (first 2KB):
> <!-- dokima-ask -->
> 
> Agents raise things through about ten different fields today (questions, concerns, replies, suspect tests, outside scope, blockers, notes, assumptions, issues found, outside plan, resolved). They are the same few ideas in different clothes. I want the smallest set that covers every case.
> 
> What I want:
> - Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).
> - A raise is exactly one of three kinds: question (for me; on autopilot the reviewer answers it for me when my own words settle it, with them as evidence), blocker (names who must fix it), or issue (outside this one; code files it). The list is closed: the checker rejects any other kind, and adding a kind is a code change I approve, never something an agent invents.
> - Who can raise to whom is a fixed table in code: the planner raises questions to me; the worker raises blockers for the planner only through the reviewer, who judges whether they are real; the reviewer raises to the planner, the worker or me; anyone can raise an issue. The checker rejects anything outside the table.
> - Every raise addressed to an agent is answered by that agent in its next turn, done or dis

`3. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items()},indent=1)[:20000])"
```

> 28:### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 32:### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 36:### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 41:### dokima-runtime on issue #289 (2026-10-09T00:13:36Z)
> 256:### dokima-runtime on issue #289 (2026-10-09T00:16:36Z)
> 440:### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 448:### dokima-runtime on issue #289 (2026-10-09T01:27:45Z)
> 660:### dokima-runtime on issue #289 (2026-10-09T01:30:29Z)
> []{
>  "kind": "feature",
>  "summary": "Agents raise and answer through two fields, raises and answers, with three kinds of raise and a fixed table of who raises to whom.",
>  "feature": "Every agent raises and answers through raises and answers only, so the owner reads one Raised list and nothing raised is ever dropped. Split by rule R2 (it needs more than five criteria) and R3 (it spans the checker, the cards, the river and all three prompts). Stories: (1) the closed kinds, the labels and the who-to-whom table in code, with their checks; (2) cards draw one Raised section; depends on (1). (3) every hand-back moves to raises and answers, with the river and the prompts; depends on (1) and (2). (4) issue raises are filed by code; depends on (3). This round follows the owner's answers of 2026-10-09: any stage may raise any kind and only the table limits whom; a change outside the plan or outside scope is a blocker for the owner; a suspect test is a blocker for the planner, through the reviewer; notes are dropped;

`4. Bash`
```
cd /tmp/pack; sed -n 440,450p issue.md; python3 -c "
import json;r=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(r,indent=1)[:9000])"
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
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37863939769",
>  "commit_before": "a302cb153f452b7209be0cecbebe5c55dc9a4e5b",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 52651,
>   "turns": 6,
>   "cost_usd": 0.36965519999999996,
>   "tokens_in": 199883,
>   "tokens_out": 5782
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/289/37863939769-reviewer-plan.md",
>  "run": "https://git

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;r=json.load(open('in/03-planner.json'));print(r.get('check'));h=r['handback'];print(h.get('replies'), h.get('concerns'))"; ls /tmp/dokima-out 2>&1
```

> {'passed': True, 'problems': []}
> [] [{'text': "#241 says the planner hands back no replies; this newer issue says every agent answers each raise sent to it, so the planner answers by id. Story 3 follows this issue; #241's replies part should be dropped.", 'evidence': '#241'}, {'text': '#175 (worker problems routed through the reviewer) and #268/#265/#193 (filing found issues) overlap stories 3 and 4; recommend folding them in rather than building them twice.', 'evidence': '#175, #268'}]
> claude.json
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Grading the re-plan against the owner's answers of 2026-10-09; writing the hand-back now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner re-planned after the owner's answers, keeping the split into 4 stories: the kinds and who-raises-to-whom table in code; one Raised section on cards; every hand-back moved to raises and answers, with the river and the prompts; issue raises filed by code."],
  "decided": [
   "Any agent may raise any kind, limited only by the table; a label such as outside plan, outside scope or suspect test has no behavior.",
   "Outside plan and outside scope become blockers for the owner, suspect tests blockers for the planner through the reviewer; notes are dropped; links stay the planner's own field.",
   "Answers show in one Answered fold on cards; story 3 reuses story 1's checks."
  ],
  "open": ["Asks whether the worker's blocker for the owner goes through the reviewer or straight to the owner."]
 },
 "verdict": "approve",
 "summary": "The re-plan follows every one of your answers and gives each ask to exactly one story; its one question changes how the worker's blockers reach you, so it stops for you.",
 "blockers": [],
 "notes": [
  {"text": "S1.2 lets the worker raise to the owner, while the issue named only blockers for the planner; that follows your later answer that any stage may raise any kind, and the plan's question asks how it reaches you.", "evidence": "plan.json stories[0].acceptance_criteria[1]; owner's /plan comment of 2026-10-09T01:27:26Z"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).", "source": "https://github.com/dokima-dev/dokima/issues/289", "criterion": "S3.1"},
  {"ask": "A raise is exactly one of three kinds: question ..., blocker ..., or issue ... The list is closed: the checker rejects any other kind", "source": "https://github.com/dokima-dev/doki
```

> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`7. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The re-plan follows your answers and covers every ask; its one question changes how the worker's blockers reach you, so it stops for you."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for issue #289, but its one question isn't settled by your own words, so the river will stop for you. Both checks on my hand-back pass, and it's in `/tmp/dokima-out/review.json`.

**The question that needs your answer:** when the worker finds a change outside scope, does that blocker for you go through the reviewer first, or straight to you?
- The planner assumed it goes through the reviewer, the same way the worker's blockers for the planner do.
- Your words cover two things: the worker's blockers for the planner go through the reviewer, and outside scope is a blocker for you. They don't say how the worker's blocker for you travels.
- I didn't accept the assumption because it changes what reaches you: sending it through the reviewer would let the reviewer drop it before you see it.

**What the planner did:** it re-planned after your answers and kept the split into four stories:
1. The three kinds of raise and the table of who raises to whom, checked by code.
2. Cards show one Raised section and one Answered fold.
3. Every agent's hand-back uses only raises and answers, with the river and the three prompts updated. This story reuses story 1's checks instead of building new ones.
4. Code files issue raises as real GitHub issues.

**What I checked:**
- **Your answers:** each one from your comment is now in a story. Any agent may raise any kind, limited only by the table. Labels such as outside plan, outside scope and suspect test have no behavior of their own. Outside plan and outside scope are blockers for you. Suspect tests are blockers for the planner, through the reviewer. Notes are dropped. The links stay the planner's own field.
- **Your asks:** I matched all 13 asks in the issue and your comment to a criterion, and none is missing.
- **Open blockers:** none were left from the last round.

**One note, not blocking:** the table now lets the worker raise to you, while the issue only named blockers for the planner. That follows your later answer that any stage may raise any kind, and the planner's question asks how those raises reach you.

The plan's tests come later: this round splits the issue into stories, so I had no tests to run.
