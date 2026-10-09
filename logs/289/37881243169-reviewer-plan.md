# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37881243169

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (329.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/35e99257-21ed-4916-80ce-405eb580f501/tool-results/b4619bkaq.txt
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
> 12-reviewer-plan.json
> 13-planner.json
> 14-reviewer-plan.json
> 15-planner.json
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
> <img src="https://raw.githubusercontent.

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json in/*; grep -n "dokima-card\|^## \|^### \|Comment\|^---" issue.md | head -80
```

> 313511 issue.md
>  21892 plan.json
>   1610 open_blockers.json
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
>  10252 in/12-reviewer-plan.json
>  22927 in/13-planner.json
>  10885 in/14-reviewer-plan.json
>  22644 in/15-planner.json
> 543208 total
> 3:<!-- dokima-card -->
> 25:<!-- /dokima-card -->
> 39:## Comments
> 41:### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 45:### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 49:### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 54:### dokima-runtime on issue #289 (2026-10-09T00:13:36Z)
> 269:### dokima-runtime on issue #289 (2026-10-09T00:16:36Z)
> 453:### RezaSoleymanifar on issue #289 (2026-10-09T01:27:26Z)
> 461:### dokima-runtime on issue #289 (2026-10-09T01:27:45Z)
> 673:### dokima-runtime on issue #289 (2026-10-09T01:30:29Z)
> 857:### RezaSoleymanifar on issue #289 (2026-10-09T01:39:55Z)
> 869:### dokima-runtime on issue #289 (2026-10-09T01:40:19Z)
> 1100:### dokima-runtime on issue #289 (2026-10-09T01:43:15Z)
> 1347:### RezaSoleymanifar on issue #289 (2026-10-09T01:45:00Z)
> 1354:### dokima-runtime on issue #289 (2026-10-09T01:45:18Z)
> 1610:### dokima-runtime on issue #289 (2026-10-09T01:46:59Z)
> 1883:### RezaSoleymanifar on issue #289 (2026-10-09T01:47:51Z)
> 1887:### dokima-runtim

`3. Bash`
```
cd /tmp/pack; sed -n 1,53p issue.md; for l in 453 857 1347 1883 2428 2985; do sed -n "${l},$((l+12))p" issue.md; echo ----; done; sed -n 3245,3256p issue.md; sed -n 3820,3830p issue.md; tail -c 6000 issue.md
```

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
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> 
> **Scope:**
> 
> 
> **Out of scope:**
> 
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://ra

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/14-reviewer-plan.json'));print(json.dumps(d,indent=1)[:9000])"
```

> [
>  {
>   "id": "B2",
>   "criterion": "S2.5",
>   "test": null,
>   "problem": "The owner's ask that what code detects stays as it is, each keeping its own name and icon, no longer has a criterion. Round 6 held it in story 2 criterion 5; this round overwrote that criterion with a near word-for-word copy of criterion 4 (no backfill). Story 2 redraws every card section from raises and answers, so code that folds a failing check or work outside the plan into the Raised section, or drops its icon, would pass every criterion as written.",
>   "evidence": "Owner comment 2026-10-09T01:39:55Z: 'Stays deterministic, raised by code only, each keeping its own name and icon: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs me, three blocks in a row.' in/11-planner.json stories[1].acceptance_criteria[4]: 'What code detects keeps its own name, icon and place on the card, exactly as today...'. plan.json stories[1].acceptance_criteria[3] and [4] both read 'A record posted before this change keeps its comment exactly as it is ... the issue card still draws it ... without error'. Story 5 criterion 5 covers only prompt and AGENTS.md examples, not the cards.",
>   "fix": "Put back story 2 criterion 5 as in the previous round ('What code detects keeps its own name, icon and place on the card, exactly as today: work outside the plan, failing tests, red main, merge conflicts, a rejected hand-back, a workflow file change and thre

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/14-reviewer-plan.json'));h=d['handback'];print(json.dumps(h['asks'][26:],indent=1));print(json.dumps(h.get('assumptions'),indent=1))
p=json.load(open('plan.json'));print(p.keys())
for i,s in enumerate(p.get('stories',[])):
  print('=== S',i+1,s['title']);print(s.get('context'));print('deps',s.get('depends_on'))
  for j,c in enumerate(s['acceptance_criteria']): print(' ',j+1,c['text'])
print(p.get('questions'),p.get('concerns'),p.get('replies'))
print({k:v for k,v in p.items() if k!='stories'})
"
```

> [
>  {
>   "ask": "encourages agents to raise things actively rather than stay quiet",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "S5.4"
>  },
>  {
>   "ask": "Stays deterministic, raised by code only, each keeping its own name and icon: work outside the plan, failing tests, red main, merge conflicts, a hand-back the checker rejects, a workflow file change that needs me, three blocks in a row.",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "missing"
>  },
>  {
>   "ask": "the prompts and AGENTS.md also give an example for each thing code raises itself (work outside the plan, a failing test, red main, a merge conflict, a rejected hand-back, a workflow file change, three blocks in a row), so agents know what each looks like and never raise these themselves.",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "S5.5"
>  },
>  {
>   "ask": "No backfill: old issues keep their old records as they are.",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "S2.4"
>  },
>  {
>   "ask": "a doubt about the ask becomes a question for me, with its evidence.",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "S3.1"
>  },
>  {
>   "ask": "Add \"doubt about the ask\" as a named instance of the question kind, with examples.",
>   "source": "https://github.com/dokima-dev/dokima/issues/289",
>   "criterion": "S5.3"
>  },
>  {
>   "ask": "the shared prompt section ends with a short checklist

**Agent:** I'm writing the review now: blocker B2 from last round is fixed, and nothing the owner wrote since then is unaddressed.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
h=json.load(open('in/14-reviewer-plan.json'))['handback']
asks=h['asks']
for a in asks:
    if a['criterion']=='missing': a['criterion']='S2.5'
asks.append({"ask":"question (for me; on autopilot the reviewer answers it for me when my own words settle it, with them as evidence)","source":"https://github.com/dokima-dev/dokima/issues/289","criterion":"S3.4"})
r={"previous_step":{"did":["The planner put back story 2 criterion 5: what code detects keeps its own name, icon and place on the card, exactly as today, and never shows in the Raised section, listing all seven items.","The planner kept one copy of the no-backfill criterion, as story 2 criterion 4."],
 "decided":["The split stays at five stories with the same order of dependencies."],
 "open":["The plan has no questions for the owner; it recommends folding #175, #268, #265 and #193 into stories 3 and 4."]},
 "verdict":"approve",
 "summary":"Your ask that what code detects keeps its own name and icon is back in story 2, so every ask you made now has a criterion.",
 "blockers":[],
 "notes":[{"text":"Story 4 still treats an issue the reviewer raises itself as confirmed; the plan says so openly in story 4's context and criterion 2.","evidence":"plan.json stories[3].context and acceptance_criteria[1]"}],
 "resolved":["B2"],"issues_found":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="Your ask that what code detects keeps its own name and icon is back in story 2; every ask you made now has a criterion."
r['summary']="What code detects keeping its own name and icon is back in story 2, so every ask you made now has a criterion."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for issue #289. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass with nothing reported.

- **Last round's blocker (B2) is fixed.** Story 2 criterion 5 is back: what code detects keeps its own name, icon and place on the card, exactly as today, and never shows up in the Raised section. It lists all seven items from your comment of 2026-10-09T01:39:55Z. Only one copy of the no-backfill criterion is left, as story 2 criterion 4.
- **Every ask you made has a criterion.** I matched 34 asks from the issue and your comments to criteria. The one I had marked missing last round now maps to story 2 criterion 5.
- **Nothing new from you since the last review.** Your latest comment, the checklist at 03:47:28Z, was already covered by story 5 criterion 4 in the previous round.
- **No tests to run this round.** The plan is a split into five stories, so each story will plan and test its own work later.

I left one note, which doesn't block: story 4 counts an issue the reviewer raises itself as already confirmed. The plan says this openly, but it's the planner's reading, not your words.

The plan also recommends folding #175, #268, #265 and #193 into stories 3 and 4 so issue filing isn't built twice. That's yours to decide. Next, your card says to type `/work` to build it.
