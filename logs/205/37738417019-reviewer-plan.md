# reviewer (plan) for #205

Run: https://github.com/dokima-dev/dokima/actions/runs/37738417019

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (107.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3a0b927a-645e-4057-8c8c-61420d800beb/tool-results/b5hxter83.txt
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
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: on autopilot the river goes on by itself where it would otherwise wait for the owner: an approved plan starts the wor

`2. Bash`
```
cd /tmp/pack; wc -c issue.md; ls -la in; cat open_blockers.json; wc -c plan.json
```

> 93205 issue.md
> total 92
> drwxr-xr-x 2 runner runner  4096 Oct  8 06:35 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 06:35 ..
> -rw-r--r-- 1 runner runner 14406 Oct  8 06:35 01-planner.json
> -rw-r--r-- 1 runner runner 15669 Oct  8 06:35 02-planner.json
> -rw-r--r-- 1 runner runner  4719 Oct  8 06:35 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 16640 Oct  8 06:35 04-planner.json
> -rw-r--r-- 1 runner runner  2269 Oct  8 06:35 05-reviewer-plan.json
> -rw-r--r-- 1 runner runner 17837 Oct  8 06:35 06-planner.json
> []17098 plan.json
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^#### \|^\*\*.*wrote\|^---" issue.md | head -80
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
> 955:### RezaSoleymanifar on issue #205 (2026-10-08T06:29:47Z)
> 959:### RezaSoleymanifar on issue #205 (2026-10-08T06:32:43Z)
> 963:### dokima-runtime on issue #205 (2026-10-08T06:33:04Z)
> 1193:### RezaSoleymanifar on issue #205 (2026-10-08T06:35:04Z)
> 1197:### dokima-runtime on issue #205 (2026-10-08T06:35:23Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; sed -n 1,45p issue.md; for l in 293 521 955 959 1193; do sed -n "$l,$((l+3))p" issue.md; done; sed -n 1197,1300p issue.md
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
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> {
>  "kind": "feature",
>  "feature": "The owner hands a whole issue tree to Dokima with `/autopilot start` and gets it back done, stopped only where the owner must decide, and sees on the board what is on autopilot. Split by R2 and R3: the ask holds far more than five criteria (two commands, an Autopilot pill on every card including children filed later, Needs you replacing Autopilot where it stops, an autopilot table view, three hand-offs, every stop, and an automatic end), and the work spans unrelated parts of the code: the command listener, the board, the river's next step, merging, and what happens when an issue closes. Every story leaves main working: story 1 only switches autopilot on and off, story 2 only shows it, and each later story adds hand-offs that do nothing until autopilot is on. The owner confirmed every assumption of the first round (comment of 2026-10-08 06:24): the reviewer's approval with green checks merges, `/autopilot start` picks up what is already waiting, and it covers the issue it is said on and everything under it. The owner's correction of 06:25 is followed: no separate Autopilot needs you pill (the existing Needs you pill is used, and Autopilot and Needs you never show on the same card), the autopilot view is a table like the Needs you view, and there is no On autopilot from #N line. The owner's comment of 06:29 is followed too: wherever the owner would have typed a command, autopilot posts one short line starting `Autopilot:` in its place, so the 

**Agent:** Reading the newest split plan for issue #205 and the earlier reviews, then grading it.

`6. Bash`
```
cd /tmp/pack/in; for f in 03-reviewer-plan.json 05-reviewer-plan.json; do python3 -c "
import json,sys;d=json.load(open('$f'));print(json.dumps(d,indent=1)[:5000])"; done; python3 -c "
import json;d=json.load(open('06-planner.json'));print(list(d.keys()));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37737659763",
>  "commit_before": "cbaa6788ad51d2feaba463206619de20a6b8cfb6",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 34050,
>   "turns": 7,
>   "cost_usd": 0.35365440000000004,
>   "tokens_in": 240421,
>   "tokens_out": 3570
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/205/37737659763-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37737659763",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner re-planned after the owner confirmed the three assumptions and asked for an Autopilot pill on every card, an Autopilot needs you pill, a board view and an On autopilot from #N line.",
>     "It proposes a split into five stories: switch on and off, show it on the board and card, an approved plan starts the worker, an approved pull request merges, and children start and the tree ends by itself."
>    ],
>    "decided": [
>     "Autopilot is kept as an `autopilot` label on every issue in the tree; the board pill follows that label."
>    ],
>    "open": [
>     "The plan was written before the owner's correction at 06:25 and still holds the Autopilot needs you pill and the On autopilot from #N line the owner dropped."
>    ]
>   },
>   "verdict": "block",
>   "summary": "The split misses the owner's correction of 06:25: it still promises an Autopilot needs you pill and an On autopilot from #N line the owner dropped, never says Autopilot a

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner folded in the owner's comment of 06:29: wherever the owner would have typed a command, autopilot posts one line starting `Autopilot:` in its place, and each hand-off story owns its own line (plan approved, split approved, merged PR #N, blockers merged)."],
  "decided": ["The split stays at five stories, with the Needs you pill, the table view and no On autopilot from #N line as the owner corrected at 06:25.",
              "The `Autopilot: merged PR #N` line goes on the issue the pull request was built for."],
  "open": ["Whether the merged line belongs on the issue or the pull request is asked as a question; the owner said /review, so the planner's reading stands."]},
 "verdict": "approve",
 "summary": "The split now also gives every hand-off its own Autopilot line where the owner would have typed a command, as asked at 06:29, and still gives every promise of the issue to exactly one story; it is ready for /work.",
 "blockers": [],
 "notes": [
  {"text": "Story 1 adds a promise the owner did not state: `/autopilot start` and `/autopilot stop` post one comment naming every issue switched. It fits the owner's wish that the trail shows who moved it, but the owner may want to confirm it when story 1 is planned.",
   "evidence": "plan.json story 1, criterion 3; owner comment 2026-10-08T06:29:47Z."},
  {"text": "Story 2's view criterion may end up (manual) if GitHub's API cannot create project views; the reason should be stated when that story is planned.",
   "evidence": "plan.json story 2 context."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": []}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 205 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for issue #205 and wrote the review to `/tmp/dokima-out/review.json`. Both hand-back checks pass.

- **What's new since the last approval:** the owner asked at 06:29 for a short line wherever they would have typed a command. The planner now gives each hand-off one `Autopilot:` line, owned by the story that does it:
  - **Story 3:** "plan approved, starting work" and "split approved, filing its stories".
  - **Story 4:** "merged PR #N".
  - **Story 5:** "blockers merged, starting plan".
- **Earlier corrections still hold:** the board uses the existing Needs you pill instead of a separate Autopilot needs you pill, and a card never shows both. The autopilot view is a table like the Needs you view, and there's no On autopilot from #N line.
- **The split:** five stories, each promise in the issue given to exactly one of them. No tests are expected yet, because each story gets its own plan and tests later.
- **One open question:** should the merged line go on the issue or on the pull request? The plan puts it on the issue. The owner answered with `/review`, which means "go on with the planner's assumptions", so that reading stands.
- **No blockers:** none were open from earlier rounds.

I left two notes, neither blocking:
1. Story 1 adds something the owner didn't ask for: `/autopilot start` and `/autopilot stop` post a comment listing every issue they switched. It fits the owner's wish that the trail shows who moved things, but the owner may want to confirm it when story 1 is planned.
2. Story 2's table view may have to be set up by hand if GitHub's API can't create board views. If so, story 2's plan should say why.
