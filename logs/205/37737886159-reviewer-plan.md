# reviewer (plan) for #205

Run: https://github.com/dokima-dev/dokima/actions/runs/37737886159

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (83.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/dc696b1b-1479-41c9-babd-c1a95ab77875/tool-results/bmatnzx5f.txt
> 
> Preview (first 2KB):
> # Issue #205: Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: the owner can hand a whole issue tree to Dokima and get it back done, stopped only where the owner must decide**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: `/autopilot start` on a parent issue puts its whole tree on autopilot, and `/autopilot stop` ends it; both work on issues and PRs
> *Verified by: tests that each command sets and clears autopilot for the parent and its children*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: an issue on autopilot shows an Autopilot pill on the board while it runs
> *Verified by: a test that start sets the pill and stop clears it*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: on autopilot the river goes on by itself where it would otherwise wait for the owner: an approved plan starts the work

`2. Bash`
```
cd /tmp/pack; wc -c issue.md plan.json open_blockers.json; ls in; cat open_blockers.json
```

> 67096 issue.md
> 15888 plan.json
>  2553 open_blockers.json
> 85537 total
> 01-planner.json
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> [
>  {
>   "id": "B1",
>   "criterion": "S2.2",
>   "test": null,
>   "problem": "Story 2 promises a separate 'Autopilot needs you' pill. The owner dropped it: the existing Needs you pill is used, and Autopilot and Needs you never show on the same card. No criterion says the Autopilot pill is hidden while Needs you shows.",
>   "evidence": "Owner comment 2026-10-08T06:25:19Z: 'No separate Autopilot needs you pill, use the Needs you pill we have. Autopilot and Needs you never show on the same card, when autopilot stops for me the card shows Needs you instead.' plan.json story 2, criterion 2 and user_story; feature text lists 'the Autopilot needs you pill'.",
>   "fix": "Replace story 2 criterion 2 with: when the river stops for the owner on an issue on autopilot, the card shows Needs you and no Autopilot pill, and shows Autopilot again (and no Needs you) once the river goes on; a card never shows both. Remove Autopilot needs you from the feature text, user story and context.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "S2.4",
>   "test": null,
>   "problem": "Story 2 still promises an 'On autopilot from #N' line on the issue card, and story 1 records where autopilot started to feed it, and card.py is put in scope for it. The owner dropped that line.",
>   "evidence": "Owner comment 2026-10-08T06:25:19Z: 'Drop the On autopilot from #N line on the 

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^\*\*.*wrote\|^---" issue.md | head -80
```

> 4:### Plan: add `work` to start
> 40:## Comments
> 42:### RezaSoleymanifar on issue #205 (2026-10-08T06:17:49Z)
> 46:### dokima-runtime on issue #205 (2026-10-08T06:18:10Z)
> 293:### RezaSoleymanifar on issue #205 (2026-10-08T06:24:34Z)
> 297:### dokima-runtime on issue #205 (2026-10-08T06:24:52Z)
> 521:### RezaSoleymanifar on issue #205 (2026-10-08T06:25:19Z)
> 525:### dokima-runtime on issue #205 (2026-10-08T06:26:57Z)
> 633:### dokima-runtime on issue #205 (2026-10-08T06:28:14Z)
> 870:### dokima-runtime on issue #205 (2026-10-08T06:29:28Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 1,45p issue.md; sed -n 290,297p issue.md; sed -n 518,525p issue.md
```

> # Issue #205: Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: the owner can hand a whole issue tree to Dokima and get it back done, stopped only where the owner must decide**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: `/autopilot start` on a parent issue puts its whole tree on autopilot, and `/autopilot stop` ends it; both work on issues and PRs
> *Verified by: tests that each command sets and clears autopilot for the parent and its children*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: an issue on autopilot shows an Autopilot pill on the board while it runs
> *Verified by: a test that start sets the pill and stop clears it*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: on autopilot the river goes on by itself where it would otherwise wait for the owner: an approved plan starts the worker, an approved PR merges, and a child starts planning once its blockers merge
> *Verified by: tests for each of the three hand-offs on an autopilot issue, and that none happens without autopilot*
> 
> <img src="https://ra

`5. Bash`
```
cd /tmp/pack; sed -n 525,640p issue.md
```

> ### dokima-runtime on issue #205 (2026-10-08T06:26:57Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (plan)**
> 
> **block**: The split misses the owner's correction of 06:25: it still promises an Autopilot needs you pill and an On autopilot from #N line the owner dropped, never says Autopilot and Needs you never show together, and does not make the autopilot view a table list like the Needs you view.
> - **B1** (S2.2, the planner fixes it): Story 2 promises a separate 'Autopilot needs you' pill. The owner dropped it: the existing Needs you pill is used, and Autopilot and Needs you never show on the same card. No criterion says the Autopilot pill is hidden while Needs you shows.
> - **B2** (S2.4, the planner fixes it): Story 2 still promises an 'On autopilot from #N' line on the issue card, and story 1 records where autopilot started to feed it, and card.py is put in scope for it. The owner dropped that line.
> - **B3** (S2.3, the planner fixes it): The board view criterion only says 'a view that lists every issue and pull request on autopilot'. The owner said the autopilot view is a table list like the Needs you view, so a board-layout view or any other shape would pass this criterion.
> 
> <details><summary>What the previous step did</summary>
> 
> - **Did:** The planner re-planned after the owner confirmed the three assumptions and asked for an Autopilot p

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> {
>  "kind": "feature",
>  "feature": "The owner hands a whole issue tree to Dokima with `/autopilot start` and gets it back done, stopped only where the owner must decide, and sees on the board what is on autopilot. Split by R2 and R3: the ask holds far more than five criteria (two commands, an Autopilot pill on every card including children filed later, Needs you replacing Autopilot where it stops, an autopilot table view, three hand-offs, every stop, and an automatic end), and the work spans unrelated parts of the code: the command listener, the board, the river's next step, merging, and what happens when an issue closes. Every story leaves main working: story 1 only switches autopilot on and off, story 2 only shows it, and each later story adds hand-offs that do nothing until autopilot is on. The owner confirmed every assumption of the first round (comment of 2026-10-08 06:24): the reviewer's approval with green checks merges, `/autopilot start` picks up what is already waiting, and it covers the issue it is said on and everything under it. The owner's correction of 06:25 is followed: no separate Autopilot needs you pill (the existing Needs you pill is used, and Autopilot and Needs you never show on the same card), the autopilot view is a table like the Needs you view, and there is no On autopilot from #N line. Promises and their owners: start and stop on issues and pull requests go to story 1; the Autopilot pill on every card in the tree (children filed later too), Needs you

**Agent:** Checking the newest plan against the three open blockers: all three look fixed in the plan text. Now I'm confirming the code checker's verdict before I write the review.

`7. Bash`
```
cd /tmp/pack; python3 -c "
import json;r=json.load(open('in/04-planner.json'));print(r.get('check'));print(list(r))"; cd /home/runner/work/dokima/dokima; git status --short; git log --oneline -1
```

> {'passed': True, 'problems': []}
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> cbaa678 A re-plan after the worker built is rejected: new tests are judged against the branch, not main (#204)

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner reworked story 2 to follow the owner's correction of 06:25: the existing Needs you pill replaces Autopilot where autopilot stops, and a card never shows both.",
   "It made the autopilot view a table like the Needs you view, and removed the On autopilot from #N line, the start-point record and card.py from the plan."
  ],
  "decided": [
   "The split stays at five stories: switch on and off, show it on the board, an approved plan or split goes on, an approved pull request merges, children start and the tree switches itself off."
  ],
  "open": [
   "Every story needs a workflow change, so each child must say so in its own words; #86 should close as a duplicate of story 5."
  ]
 },
 "verdict": "approve",
 "summary": "The split now follows the owner's correction of 06:25 in full and gives every promise of the issue to exactly one story; it is ready for /work.",
 "blockers": [],
 "notes": [
  {
   "text": "Story 2's view criterion may end up (manual) if GitHub's API cannot create project views; when that story is planned, the reason should be stated and the table layout and filter checked by hand.",
   "evidence": "plan.json story 2 context: 'if it cannot, the view is a one-time setup step next to the Needs you view and its criterion is (manual)'."
  },
  {
   "text": "Story 5 keeps two halves (children starting, and the tree switching off) together because both react to an issue closing; that reason is stated, so it is fine as one story.",
   "evidence": "plan.json story 5 context, first sentence."
  }
 ],
 "outside_plan": [],
 "resolved": ["B1", "B2", "B3"],
 "issues_found": []
}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 205 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for issue #205; the planner fixed all three of my earlier blockers, so the issue is ready for your `/work`. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks passed.

The planner's update now follows your correction of 06:25:
- **B1 (fixed):** There's no separate Autopilot needs you pill. When autopilot stops for you, the card shows the existing Needs you pill instead of Autopilot, and a card never shows both.
- **B2 (fixed):** The On autopilot from #N line is gone. So are the record of where autopilot started and the plan to change `card.py`.
- **B3 (fixed):** The autopilot view is now a table like the Needs you view, listing everything on autopilot and nothing else.

The plan splits the issue into five stories, and each promise in your ask belongs to exactly one of them:
1. `/autopilot start` and `/autopilot stop` switch an issue tree on and off.
2. The board and every card show what's on autopilot.
3. An approved plan or split goes on by itself, and autopilot still stops wherever you must decide.
4. A pull request the reviewer approved merges once every check is green.
5. Children start once their blockers merge, and autopilot switches itself off when the whole tree is done.

A split has no tests of its own; each story gets planned and tested on its own after you say `/work`.

Two notes, neither blocking:
- **Board view:** If GitHub can't create a board view through its API, story 2's view becomes a one-time setup step that is checked by hand, with the reason stated.
- **Story 5:** It covers two things, starting children and switching off, because both happen when an issue closes. The plan says so, which is enough.

Still open from the planner:
- **Workflow files:** Every story needs a change under `.github/workflows/`. Each child issue has to say so explicitly, because AGENTS.md only allows workflow changes when the issue asks for them.
- **#86:** It overlaps story 5 and should be closed as a duplicate of it.
