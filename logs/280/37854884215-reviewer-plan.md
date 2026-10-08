# reviewer (plan) for #280

Run: https://github.com/dokima-dev/dokima/actions/runs/37854884215

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

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
> Today the board's Autopilot option was missing for hours and a branch rule silently blocked autopilot merges. Nobody noticed until something broke.
> 
> What I want:
> - Everything Dokima needs from GitHub is declared in one manifest in code: labels, board fields and their options, required check names, branch rules, app permissions. A test fails if code relies on a setting the manifest does not declare.
> - A drift audit compares the manifest with the rep

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git status --short; git log --oneline -2; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.keys());print(d.get('check'))"; ls dokima; cat dokima/app.json 2>/dev/null | head -40; grep -n "options" AGENTS.md
```

> 7cc3eda On autopilot, a question the reviewer answers from the owner's words shows plainly (#275)
> fdb0c5f The planner finds the issues this one is blocked by, blocks or relates to, and code checks them (#256)
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> {'passed': True, 'problems': []}
> agent.py
> app.json
> board.py
> body.py
> card.py
> checks.py
> fence.py
> icons
> plan.py
> planner.py
> roles
> trail.py
> uptodate.py
> words.py
> {
>   "name": "Dokima Runtime",
>   "description": "Dokima's bot. Opens PRs, posts the card, never approves. Nothing merges until it's proven.",
>   "url": "https://github.com/RezaSoleymanifar/dokima",
>   "hook_attributes": {
>     "url": "https://github.com/RezaSoleymanifar/dokima",
>     "active": false
>   },
>   "public": false,
>   "default_permissions": {
>     "contents": "write",
>     "pull_requests": "write",
>     "issues": "write",
>     "checks": "read",
>     "actions": "read",
>     "statuses": "read",
>     "metadata": "read",
>     "workflows": "write"
>   },
>   "default_events": []
> }
> 79:- One Autopilot view, a table filtered to `label:autopilot`, lists everything on autopilot. Code adds it the first time a tree goes on autopilot, from the board run of the tree's top issue only, and a refused view fails that run naming it. The Autopilot option of the Action field is a one-time step on the board, like Needs you; code never edits the field's options.

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner split the issue into four stories: the manifest, the audit report on a pinned Setup issue, the audit's own fixes, and when the audit runs."],
  "decided": ["Story 2 reads 'the owner of the repo' as the repo's code owners from CODEOWNERS.", "Settings GitHub will not show, such as branch rules before Administration read, are listed as not verified, never as fine."],
  "open": ["Whether board and permission changes are caught only by the daily run.", "Whether 'whenever I ask' means the Run workflow button or a new /audit command."]},
 "verdict": "approve",
 "summary": "The split keeps every ask of the issue in exactly one story, but both of its questions need the owner's answer before work starts.",
 "blockers": [],
 "notes": [
  {"text": "The planner's concern says the AGENTS.md line 'code never edits the field's options' must change with story 3, but no criterion of story 3 says so; story 3's own plan should make that edit a criterion so the rule and the code do not disagree.", "evidence": "AGENTS.md:79; plan.json stories[2].acceptance_criteria has no AGENTS.md criterion"},
  {"text": "Story 1's test that catches unlisted settings covers labels, board options, views and check names; branch rules are declared but nothing checks that code relies only on declared ones. Story 1's own plan should say how, or why it cannot.", "evidence": "plan.json stories[0].acceptance_criteria[1]; issue: 'A test fails if code relies on a setting the manifest does not declare.'"},
  {"text": "Adding a board option rewrites the field's whole option list, so story 3's plan needs a test that every existing option keeps its id and value after a fix.", "evidence": "plan.json concerns[0]; dokima/board.py reads options by id"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Everything Dokima needs from GitHub is declared in one manifest in code: labe
```

> (Bash completed with no output)

**Agent:** I approved the plan, but issue #280 still stops for you because I didn't accept either of the planner's two questions. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks ran without reporting any problems.

**The split.** The planner split the issue into four stories:
1. One manifest in code that declares every setting Dokima needs from GitHub.
2. An audit that reports what is off on a pinned Setup issue.
3. The audit fixes harmless gaps itself.
4. The audit runs daily, after a settings change, and on request.

I found 12 asks in your issue, and each one is kept by exactly one story criterion, so none is missing. A split has no tests of its own yet, so there were no new tests for me to run. The planner read "the owner of the repo" as the repo's code owners in CODEOWNERS. That fits AGENTS.md, so I accepted it.

**Questions that need your answer:**
- **Board and permission changes:** GitHub doesn't tell Actions when board options, views or app permissions change, so the planner wants those caught only by the daily run. Your words were "after a settings change", with no exception. A delay of up to a day is your call.
- **"Whenever I ask":** it could mean the Run workflow button on the Actions tab or a new `/audit` command. The two work differently, and neither the issue nor AGENTS.md picks one.

**Notes for the stories' own plans:**
- **AGENTS.md rule:** AGENTS.md says "code never edits the field's options", and story 3 would break that rule. No criterion in story 3 updates that line.
- **Branch rules in story 1:** story 1's test catches undeclared labels, board options, views and check names. Nothing checks the same for branch rules.
- **Existing board options:** adding a board option rewrites the whole option list. Story 3 needs a test that every existing option keeps its id and value.
