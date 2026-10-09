# reviewer (plan) for #289

Run: https://github.com/dokima-dev/dokima/actions/runs/37881039262

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (282.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3339a6d6-7659-4b75-a57c-4ef5bad8ea02/tool-results/bweoi5z5y.txt
> 
> Preview (first 2KB):
> .:
> total 300
> drwxr-xr-x  3 runner runner   4096 Oct  9 03:49 .
> drwxrwxrwt 18 root   root     4096 Oct  9 03:49 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 03:49 in
> -rw-r--r--  1 runner runner 264670 Oct  9 03:49 issue.md
> -rw-r--r--  1 runner runner   1210 Oct  9 03:49 open_blockers.json
> -rw-r--r--  1 runner runner  22174 Oct  9 03:49 plan.json
> 
> in:
> total 200
> drwxr-xr-x 2 runner runner  4096 Oct  9 03:49 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 03:49 ..
> -rw-r--r-- 1 runner runner 11840 Oct  9 03:49 01-planner.json
> -rw-r--r-- 1 runner runner  5872 Oct  9 03:49 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 13586 Oct  9 03:49 03-planner.json
> -rw-r--r-- 1 runner runner  5772 Oct  9 03:49 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 15936 Oct  9 03:49 05-planner.json
> -rw-r--r-- 1 runner runner  7968 Oct  9 03:49 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 19523 Oct  9 03:49 07-planner.json
> -rw-r--r-- 1 runner runner  8587 Oct  9 03:49 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 20348 Oct  9 03:49 09-planner.json
> -rw-r--r-- 1 runner runner  9190 Oct  9 03:49 10-reviewer-plan.json
> -rw-r--r-- 1 runner runner 20865 Oct  9 03:49 11-planner.json
> -rw-r--r-- 1 runner runner 10252 Oct  9 03:49 12-reviewer-plan.json
> -rw-r--r-- 1 runner runner 22927 Oct  9 03:4

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; grep -n '^## \|^### \|^---\|^\*\*@\|^#### ' issue.md | head -100; wc -l issue.md
```

> [
>  {
>   "id": "B1",
>   "criterion": "S2.5",
>   "test": null,
>   "problem": "The owner's ask 'No backfill: old issues keep their old records as they are' is only in story 2's context, not an acceptance criterion of any story. In a split, /work approves each story's criteria as final, so no test will ever hold it. Story 3 makes the checker reject every old field and rebuilds the starting pack from the issue's history, and story 2 redraws cards from raises and answers; code that misreads or rejects an older record would pass every criterion as written.",
>   "evidence": "Owner comment 2026-10-09T01:39:55Z ('No backfill: old issues keep their old records as they are.'); plan.json stories[1].context ('records posted before this change are not redrawn (no backfill)'); no criterion in stories[0..4].acceptance_criteria mentions older records. Raised as a note in the review of round 5 (in/10-reviewer-plan.json notes[0]) and not taken up.",
>   "fix": "Add one criterion, in story 2 or 3: a record posted before this change keeps its comment exactly as it is, the issue card and a new run's starting pack still read it without error, and only new hand-backs must use raises and answers.",
>   "fixer": "planner"
>  }
> ]
> 39:## Comments
> 41:### RezaSoleymanifar on issue #289 (2026-10-09T00:12:59Z)
> 45:### dokima-runtime on issue #289 (2026-10-09T00:13:22Z)
> 49:### dokima-runtime on issue #289 (2026-10-09T00:13:24Z)
> 54:### dokima-runtime on issue #289 (2026-10-09T00:13:36Z)
> 269:### dokima-runtime on issue #289

`3. Bash`
```
cd /tmp/pack; sed -n 1,53p issue.md; for l in 453 857 1347 1883 2428 2985; do sed -n "${l},$((l+12))p" issue.md; echo ====; done; sed -n 3245,3263p issue.md
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
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'))
print(json.dumps({k:v for k,v in p.items() if k!='stories'},indent=1))
for s in p.get('stories',[]):
  print('=====');print(json.dumps(s,indent=1))
"
```

> {
>  "kind": "feature",
>  "summary": "Agents raise their judgments as questions, blockers or issues and answer them through two fields; what code detects stays as it is.",
>  "feature": "Agents raise every judgment through raises and answers only: three kinds, a fixed table of who raises to whom, and an ID and raiser set by code. Before each run, code hands the agent the exact list of open raises it must answer. The reviewer settles what is addressed to an agent, and on autopilot it answers your questions only with your own words. Split by rule R2 (more than five criteria) and R3 (the checker, the cards, the river, the prompts and AGENTS.md). Stories: (1) the kinds, the table, code's raiser and ID, and the answer check, in code; (2) cards draw raises and answers; depends on (1). (3) every hand-back moves to raises and answers, with the starting pack, the river and one shared prompt section; depends on (1) and (2). (4) the reviewer settles workers' raises and confirms issues before code files them; depends on (3). (5) AGENTS.md records the design, and the shared prompt section gives many examples and asks agents to raise actively; depends on (3) and (4). This round answers the plan review's blocker B1 and adds your comment of 2026-10-09T03:47:28Z: story 2 now promises that records posted before this change keep their comments and still draw on the issue card, story 3 that the checker never rejects them and the next run's pack still reads them, and story 5 that the shared prompt sec

`5. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['11-planner.json','13-planner.json']:
  d=json.load(open(f)); print(f, list(d.keys()))
  h=d.get('handback') or d.get('hand_back') or d
  def find(o):
    if isinstance(o,dict):
      if 'stories' in o: return o
      for v in o.values():
        r=find(v)
        if r: return r
  p=find(d)
  for i,s in enumerate(p['stories']):
    print(i+1, s['title'])
    for j,c in enumerate(s['acceptance_criteria']): print('   ',j+1,c['text'][:250])
"
```

> 11-planner.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> 1 Three kinds of raise and one table of who raises to whom, checked by code
>     1 The checker rejects a raise of any kind but question, blocker or issue, naming the kind and the three allowed; each of the three passes. A raise may carry a short label such as weak test or missing ask; any label passes, and two raises that differ on
>     2 The checker rejects a question or blocker sent outside the table, and a blocker that names no one to fix it. It names who raised it, its kind and whom it was for. The table: the planner raises to the owner; the worker raises to the planner, through t
>     3 Code stamps each raise with who raised it and an ID unique on the issue. The raiser comes from the agent that ran; a raiser or ID written by the model is rejected.
>     4 An answer names a raise by its ID, says done or disagree, and says why; anything else is rejected, naming the answer. A turn that leaves a raise sent to its agent unanswered is rejected, naming that raise; a turn that answers every one passes.
> 2 Cards show what was raised and how each earlier raise was answered
>     1 A run comment and the issue card show one Raised section with every raise of the run. Each line opens with its kind's icon (question, blocker or issue), shows its label when it has one, and says who it is for: you, the planner, the worker, or filed a
>     2 No card shows a raise's or a

`6. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
d=json.load(open('12-reviewer-plan.json'));print(json.dumps(d['handback'],indent=1)); print(json.dumps(d['check'],indent=1)[:1500])
d=json.load(open('13-planner.json'));print(json.dumps(d['check'],indent=1)[:1500])
"
```

> {
>  "previous_step": {
>   "did": [
>    "The planner took the owner's answer of 2026-10-09T03:44:37Z: the planner's concerns field goes, and a doubt about the ask reaches the owner as a question carrying its evidence (story 3, criterion 1).",
>    "Story 5 names doubt about the ask as an instance of the question kind in AGENTS.md and gives examples of it in the shared prompt section."
>   ],
>   "decided": [
>    "Doubt about the ask is a label only, with no behavior of its own."
>   ],
>   "open": [
>    "The plan has no questions left for the owner."
>   ]
>  },
>  "verdict": "block",
>  "summary": "The re-plan takes your answer on doubts about the ask, but your no-backfill ask still has no criterion or test.",
>  "blockers": [
>   {
>    "id": "B1",
>    "criterion": "S2.5",
>    "test": null,
>    "problem": "The owner's ask 'No backfill: old issues keep their old records as they are' is only in story 2's context, not an acceptance criterion of any story. In a split, /work approves each story's criteria as final, so no test will ever hold it. Story 3 makes the checker reject every old field and rebuilds the starting pack from the issue's history, and story 2 redraws cards from raises and answers; code that misreads or rejects an older record would pass every criterion as written.",
>    "evidence": "Owner comment 2026-10-09T01:39:55Z ('No backfill: old issues keep their old records as they are.'); plan.json stories[1].context ('records posted before this change are not redrawn (no backfill)'); no criterion in s

`7. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp/pack; python3 - <<'EOF'
import json
prev=json.load(open('in/12-reviewer-plan.json'))['handback']
asks=prev['asks']
for a in asks:
    if a['ask'].startswith('No backfill'): a['criterion']='S2.4'
    if a['ask'].startswith('Stays deterministic'): a['criterion']='missing'
asks.append({"ask":"the shared prompt section ends with a short checklist each agent goes through before it hands back: a weak test? a test that cannot pass as written? an ask with no criterion? a doubt about what I meant? a problem outside this issue?","source":"https://github.com/dokima-dev/dokima/issues/289","criterion":"S5.4"})
r={
 "previous_step":{
  "did":["The planner made no backfill a criterion: old records keep their comments and still draw on the issue card (story 2, criterion 4), and the checker never rejects them while the next run's pack still reads them (story 3, criterion 2).",
         "Story 5 now ends the shared prompt section with the owner's five-item checklist (criterion 4).",
         "Story 2's old criterion 5, that what code detects keeps its own name, icon and place on the card, was replaced by a second copy of the no-backfill criterion."],
  "decided":["The empty Raised section and empty earlier-raises section moved into story 2's criteria 1 and 3."],
  "open":["The plan has no questions left for the owner."]},
 "verdict":"block",
 "summary":"The re-plan adds your no-backfill rule and your checklist, but in doing so it dropped your ask that what code detects keeps its own name and icon, and story 2 now repeats one criterion twice.",
 "blockers":[{
  "id":"B2","criterion":"S2.5","test":None,
  "problem":"The owner's ask that what code detects stays as it is, each keeping its own name and icon, no longer has a criterion. Round 6 held it in story 2 criterion 5; this round overwrote that criterion with a near word-for-word copy of criterion 4 (no backfill). Story 2 redraws every card section from raises and answers, so code that folds a failin
```

> summary holds 35 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`8. Bash`
```
python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="No backfill and your checklist are in, but your ask that what code detects keeps its own name and icon was dropped."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 289 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for issue #289 and sent it back to the planner. Both hand-back checks pass on the review.

**Fixed since last round:**
- **B1 (resolved):** your "No backfill" rule is now a real criterion. Story 2.4 says old records keep their comments as posted and still show on the issue card. Story 3.2 says the checker never rejects old records and the next run's starting pack still reads them.
- **Your 03:47:28Z comment is in:** story 5.4 now ends the shared prompt section with your five-item checklist.

**New blocker, B2 (story 2.5, for the planner):** to make room for no backfill, the planner overwrote story 2's old criterion 5, "What code detects keeps its own name, icon and place on the card, exactly as today." It replaced it with a near word-for-word copy of 2.4, so story 2 now says the same thing twice. Your 01:39:55Z ask ("Stays deterministic, raised by code only, each keeping its own name and icon…") now has no criterion in any story. Story 5.5 only covers examples in the prompts and AGENTS.md, not the cards. Code could fold a failing check or work outside the plan into the Raised section, or drop its icon, and still pass every criterion. The fix: restore the old 2.5 word for word and keep one copy of the no-backfill criterion as 2.4.

**One note:** story 4 still counts an issue the reviewer raises itself as already confirmed. The plan says this openly, and you haven't said otherwise.

The plan has no questions left for you. Its split stories carry no tests yet, so there were no tests to run this round. I listed 33 asks; your ask about what code detects is the only one marked missing. The review is in `/tmp/dokima-out/review.json`.
