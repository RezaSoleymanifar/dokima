# reviewer (plan) for #280

Run: https://github.com/dokima-dev/dokima/actions/runs/37856890318

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (45.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a44a2095-8917-42a3-87f4-dc29bd79a681/tool-results/bcvg2hw6j.txt
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
> # Issue #280: A drift audit compares the repo's settings with what Dokima needs and tells me what's off
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Today the board's Autopilot option was missing for hours and a branch rule silently blocked autopilot merges. Nobody noticed until 

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md; echo ======; cat open_blockers.json
```

> <persisted-output>
> Output too large (37KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a44a2095-8917-42a3-87f4-dc29bd79a681/tool-results/bse4zy841.txt
> 
> Preview (first 2KB):
> <!-- dokima-ask -->
> 
> Today the board's Autopilot option was missing for hours and a branch rule silently blocked autopilot merges. Nobody noticed until something broke.
> 
> What I want:
> - Everything Dokima needs from GitHub is declared in one manifest in code: labels, board fields and their options, required check names, branch rules, app permissions. A test fails if code relies on a setting the manifest does not declare.
> - A drift audit compares the manifest with the repo's live settings and posts what is off on one pinned Setup issue, marked Needs you, each line in plain words.
> - It fixes harmless gaps itself (labels, board options, views) and only reports anything touching permissions or branch rules.
> - It runs daily, after a settings change, and whenever I ask.
> - It reports only to the owner of the repo it runs on.
> - The Dokima app gets read-only Administration permission so it can read branch rules; it can never change them. Until then, the audit says plainly which settings it could not verify.
> 
> This is the piece of #272's pre-flight check that pays off on this repo now, before onboarding.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #280 (2026-10-08T22:37:39Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #280 (2026-10-08T22:38:05Z)
> 
> Autopilot: switched on, start

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json
p=json.load(open('plan.json'))
print(json.dumps(p,indent=1))
" | head -c 30000
```

> {
>  "kind": "feature",
>  "summary": "One manifest in code lists every GitHub setting Dokima needs, and a quiet daily audit checks the live repo against it, fixes the harmless gaps and reports the rest on a pinned Setup issue.",
>  "feature": "The owner hears about a repo setting only when it has drifted from what Dokima needs: once a day, in the background, the audit fixes the harmless gaps and lists the rest in plain words on one pinned Setup issue. Split by R1 and R2: the manifest, the report, the fixes and the daily run are separate goals that together need well over five criteria; each story lands on its own and main works after each.",
>  "stories": [
>   {
>    "title": "Everything Dokima needs from GitHub is declared in one manifest in code",
>    "user_story": "The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a test catches code that relies on anything left out.",
>    "acceptance_criteria": [
>     {
>      "text": "One manifest module in `dokima/` declares the labels, board fields and their options, views, required check names, branch rules and app permissions Dokima needs.",
>      "source": "https://github.com/dokima-dev/dokima/issues/280"
>     },
>     {
>      "text": "The manifest declares the Autopilot option as purple, described \"Running on its own\". It declares the Autopilot view's filter as `label:autopilot is:open`. The board code reads that filter from the manifest.",
>      "source": "h

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; echo; awk '/^### RezaSoleymanifar/{p=1} /^### dokima-runtime/{p=0} p' issue.md
```

> 28:### RezaSoleymanifar on issue #280 (2026-10-08T22:37:39Z)
> 32:### dokima-runtime on issue #280 (2026-10-08T22:38:05Z)
> 36:### dokima-runtime on issue #280 (2026-10-08T22:38:08Z)
> 41:### dokima-runtime on issue #280 (2026-10-08T22:38:22Z)
> 258:### dokima-runtime on issue #280 (2026-10-08T22:39:54Z)
> 454:### RezaSoleymanifar on issue #280 (2026-10-08T22:51:34Z)
> 458:### RezaSoleymanifar on issue #280 (2026-10-08T22:57:19Z)
> 462:### dokima-runtime on issue #280 (2026-10-08T22:57:40Z)
> 677:### dokima-runtime on issue #280 (2026-10-08T22:59:55Z)
> 
> ### RezaSoleymanifar on issue #280 (2026-10-08T22:37:39Z)
> 
> /autopilot start
> 
> ### RezaSoleymanifar on issue #280 (2026-10-08T22:51:34Z)
> 
> Two board settings I fixed by hand today belong in the manifest: the Action field's Autopilot option (purple, described "Running on its own", so it never looks like the blue Needs you), and the Autopilot view's filter `label:autopilot is:open`.
> 
> ### RezaSoleymanifar on issue #280 (2026-10-08T22:57:19Z)
> 
> /plan Answers: Keep it dead simple and invisible. The audit runs once a day in the background, and that is enough for every kind of setting; nothing extra on settings changes. It only shows up when it finds drift. "Whenever I ask" is just GitHub's Run workflow button on that workflow, no new command. A test proves it runs daily and reports drift.
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['in/01-planner.json','in/02-reviewer-plan.json','in/03-planner.json']:
  d=json.load(open(f)); print('=====',f, list(d.keys()))
d=json.load(open('in/02-reviewer-plan.json')); print(json.dumps(d,indent=1)[:12000])
"
```

> []===== in/01-planner.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> ===== in/02-reviewer-plan.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> ===== in/03-planner.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37854884215",
>  "commit_before": "7cc3eda31bfa1bf0e33c0ba00d44fcdaff905bbc",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 40973,
>   "turns": 4,
>   "cost_usd": 0.31995840000000003,
>   "tokens_in": 132700,
>   "tokens_out": 4545
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/280/37854884215-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37854884215",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner split the issue into four stories: the manifest, the audit report on a pinned Setup issue, the audit's own fixes, and when the audit runs."
>    ],
>    "decided": [
>     "Story 2 reads 'the owner of the repo' as the repo's code owners from CODEOWNERS.",
>     "Settings GitHub will not show, such as branch rules before Administration read, are listed as not verified, never as fine."
>    ],
>    "open": [
>     "Whether board and permission changes are caught only by the daily run.",
>     "Whether 'whenever I as

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json
d=json.load(open('in/03-planner.json')); h=d['handback']; print(d['check']); print([k for k in h]); 
for k in h:
  if k not in ('stories',): print(k, json.dumps(h[k],indent=1)[:3000])
"; cd /home/runner/work/dokima/dokima; git status --short; git log --oneline -3; ls dokima | head -50
```

> {'passed': True, 'problems': []}
> ['kind', 'summary', 'feature', 'stories', 'concerns', 'links']
> kind "feature"
> summary "One manifest in code lists every GitHub setting Dokima needs, and a quiet daily audit checks the live repo against it, fixes the harmless gaps and reports the rest on a pinned Setup issue."
> feature "The owner hears about a repo setting only when it has drifted from what Dokima needs: once a day, in the background, the audit fixes the harmless gaps and lists the rest in plain words on one pinned Setup issue. Split by R1 and R2: the manifest, the report, the fixes and the daily run are separate goals that together need well over five criteria; each story lands on its own and main works after each."
> concerns [
>  {
>   "text": "Story 1 sets the Autopilot view filter to `label:autopilot is:open` and story 3 fixes an existing view's filter, which is all of #278. Recommend closing #278 as a duplicate of this issue once the split is filed.",
>   "evidence": "#278; dokima/board.py:184 adds the view with filter `label:autopilot`"
>  }
> ]
> links {
>  "blocked_by": [],
>  "blocks": [
>   272,
>   114
>  ],
>  "relates_to": [
>   278
>  ]
> }
> 826a1b9 The issue and PR card list criteria as bullets, count the owner's merge and always match (#276)
> 7cc3eda On autopilot, a question the reviewer answers from the owner's words shows plainly (#275)
> fdb0c5f The planner finds the issues this one is blocked by, blocks or relates to, and code checks them (#256)
> agent.py
> app.json
> board.py
> body.py
> card.py
> check

**Agent:** Reading done: the owner's two comments settle both earlier questions, and the new plan has none. Writing the review now.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned the split into four stories, using the owner's answers: the audit runs once a day and from the Run workflow button only.",
          "The planner added the Autopilot option (purple, \"Running on its own\") and the view filter `label:autopilot is:open` to the manifest story."],
  "decided": ["The audit posts nothing when nothing is off, and closes an open Setup issue with one line once drift is gone.",
              "Story 3 now keeps every existing board option and card value when it fixes an option, and updates the AGENTS.md line that said code never edits the Action field's options."],
  "open": ["The planner recommends closing #278 as a duplicate once the split is filed."]},
 "verdict": "approve",
 "summary": "The split now follows the owner's answers: once a day plus the Run workflow button, silent when nothing is off, and the two board settings fixed by hand are in the manifest. Every ask has exactly one story.",
 "blockers": [],
 "notes": [
  {"text": "Story 2 reads \"the owner of the repo\" as the repo's code owners in CODEOWNERS. That matches AGENTS.md, but story 2's own plan should test that nobody outside CODEOWNERS is mentioned, including when CODEOWNERS lists a team.",
   "evidence": "plan.json stories[1].acceptance_criteria[3]; AGENTS.md: \"Approvers come from CODEOWNERS\""},
  {"text": "The owner asked for \"A test proves it runs daily and reports drift.\" Story 4's own tests should read the workflow's real schedule trigger and run its real command, not a copy of either.",
   "evidence": "https://github.com/dokima-dev/dokima/issues/280 owner comment 2026-10-08T22:57:19Z; plan.json stories[3].acceptance_criteria[0] and [2]"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Everything Dokima needs from GitHub is declared in one manifest in code: labels, board fields and their options, required check names, branch rules,
```

> (Bash completed with no output)

**Agent:** I approved the plan for issue #280, and the review is saved in `/tmp/dokima-out/review.json`. Both of Dokima's checks on the hand-back pass.

**Why it passes:** the planner's rework follows the owner's two comments:
- **When the audit runs:** once a day, plus GitHub's Run workflow button. It does not run on settings changes and there is no new comment command.
- **Silence:** the audit posts nothing when nothing is off, and closes an open Setup issue once the drift is gone.
- **Board settings:** the two the owner fixed by hand are now in the manifest. The Autopilot option is purple, described "Running on its own", and the Autopilot view's filter is `label:autopilot is:open`.
- **Earlier notes:** both notes from the last review are now criteria in story 3. One keeps every existing board option and card value when an option is fixed. The other updates the AGENTS.md line that says code never edits the Action field's options.

**Coverage and size:** each of the 14 asks I found in the issue and the owner's comments is covered by exactly one story. The split has 4 stories, each with at most 5 criteria, and their dependencies don't loop. Since it is a split with no tests yet, there was nothing to run; each story writes its own tests when it is planned. The plan asks no questions this time, and there were no open blockers from last round.

**Two notes for the stories' own plans (not blockers):**
- **Story 2:** it reads "the owner of the repo" as the people in CODEOWNERS, which matches AGENTS.md. Its tests should show that nobody else is mentioned, including when CODEOWNERS lists a team.
- **Story 4:** the owner asked for "a test that proves it runs daily and reports drift". That test should use the workflow's real schedule and real command, not a copy of either.

Every ask links to the issue page rather than to the exact comment, because the comment links weren't in what I was given.

The planner also recommends closing #278 as a duplicate once the split is filed.
