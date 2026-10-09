# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37863939769

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (30.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/cb558a84-0099-4307-b5f3-9f8667228844/tool-results/blwje9vu0.txt
> 
> Preview (first 2KB):
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
> Agents raise things through about ten different fields today (questions, concerns, replies, suspect tests, outside scope, blockers, notes, assumptions, issues found, outside plan, resolved). T

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md; ls in; cat open_blockers.json
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
cd /home/runner/work/dokima/dokima; grep -n "Every blocker names who fixes it" AGENTS.md | head; grep -n "def problems_assumptions" -A40 dokima/agent.py | head -60
```

> 53:5. **Code review.** The reviewer starts by itself when the worker finishes. Every blocker names who fixes it: the worker for code, the planner for a test shown too weak. A block sends it back to the worker by itself, or to the planner when any blocker is the planner's; that test fix goes planner, plan review, worker, code review, and an approved re-plan whose criteria are unchanged goes straight to the worker, while one that changes any criterion, or comes after the owner spoke, waits for `/work`. An approval stops for the owner.
> 744:def problems_assumptions(r, plan, number):
> 745-    """Everything wrong with a plan review's judgements of the plan's questions: every question judged once, each
> 746-    saying whether its assumption is accepted and whether it changes how the system works or what it costs; one
> 747-    accepted never changes them and names the owner's words and where they said them; one not accepted says why."""
> 748-    qs = [q.get("question") for q in plan.get("questions") or [] if isinstance(q, dict)]
> 749-    judged = r.get("assumptions", [])
> 750-    if not isinstance(judged, list):
> 751-        return [f"assumptions must be a list, one per question of the plan, each {ASSUMPTION_SHAPE}"]
> 752-    bad, seen = [], []
> 753-    for i, a in enumerate(judged, 1):
> 754-        if not isinstance(a, dict):
> 755-            bad.append(f"assumptions item {i} must be an object, {ASSUMPTION_SHAPE}")
> 756-            continue
> 757-        q = a.get("question")
> 758-        label = 

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposed splitting the issue into 4 stories: the closed kinds and who-raises-to-whom table in code; one Raised section on cards; every hand-back moved to raises and answers, with the river and the prompts; issue raises filed by code."],
  "decided": ["Split by rule R2 (more than five criteria) and R3 (checker, cards, river and all three prompts).", "Stories run in order: 2 waits on 1, 3 waits on 1 and 2, 4 waits on 3."],
  "open": ["Asks whether the reviewer raises only questions to the owner and blockers only to the planner or worker.", "Asks where today's notes, outside_plan, outside_scope and suspect_tests go, since they are none of the three kinds."]},
 "verdict": "approve",
 "summary": "The split gives every ask in the issue to exactly one story; its two questions both change how the river works, so they stop for you.",
 "blockers": [],
 "notes": [
  {"text": "Stories 1 and 3 both promise that a turn skipping a raise is rejected (S1.4 builds the check, S3.4 wires it into every hand-back); story 3's plan should say it reuses story 1's check rather than build a second one.", "evidence": "plan.json stories[0].acceptance_criteria[3] and stories[2].acceptance_criteria[3]"},
  {"text": "Story 2 must keep showing what old records raised, and the reviewer's 'Answered from your words' section is not named among the sections it retires; its plan should say where those answers show.", "evidence": "plan.json stories[1].acceptance_criteria[1]; dokima/agent.py render()"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Every agent's hand-back has the same two fields for this: raises and answers. Everything else in it stays the agent's actual work (summary, plan, criteria built, verdict, links).", "source": "https://github.com/dokima-dev/dokima/issues/289", "criterion": "S3.1"},
  {"ask": "A raise is exactly one of three kinds: question ..., blocker ..
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> 0

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"The split gives every ask in the issue to exactly one story; its two questions both change how the river works, so they stop for you."/"The split gives every ask to exactly one story; its two questions both change how the river works, so they stop for you."/' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the planner's split of #289, but neither of its two questions can go ahead on autopilot. Both stop for you. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**The split:** four stories that run in order.
1. The three kinds of raise and the table of who raises to whom, checked in code.
2. One Raised section on cards.
3. Every hand-back moves to raises and answers, along with the river and the prompts.
4. Code files issue raises.

Every ask in the issue lands in exactly one story criterion, so nothing is missing and there are no blockers.

**The two questions (both not accepted, both change how the river works):**
- **Can the reviewer only send you questions, never blockers?** The issue says the reviewer raises to "the planner, the worker or me" but not which kinds come to you. There's also a loop: on autopilot the reviewer answers your questions itself, so it would be answering its own.
- **Where do today's notes, outside_plan, outside_scope and suspect_tests go?** The planner's answer drops some notes and reroutes the rest. Your words don't settle that.

**Two notes for the stories' own plans:**
- Stories 1 and 3 both promise to reject a turn that skips a raise. Story 3 should reuse story 1's check rather than build a second one.
- Story 2 lists the old card sections it removes, but not the reviewer's "Answered from your words" section. Its plan should say where those answers show.
