# reviewer (plan) for #111

Run: https://github.com/dokima-dev/dokima/actions/runs/38004532506

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> total 24
> drwxr-xr-x 2 runner runner  4096 Oct  9 23:28 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 23:28 ..
> -rw-r--r-- 1 runner runner 15085 Oct  9 23:28 01-planner.json
> # Issue #111: Merge queue: approve PRs in any order, main stays green
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #111](https://github.com/dokima-dev/dokima/issues/111)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: PRs can be approved and merged in any order without breaking main, by turning on GitHub's merge queue, as part of onbo

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print({k:v for k,v in d.items() if k not in ('handback',)}.keys()); print(json.dumps(d.get('check') or d.get('verdict'),indent=0)[:1500])"; ls dokima | head -50; grep -n "merge_queue\|merge-queue\|PERMISSIONS\|administration" dokima/manifest.py | head; git log --oneline -3 -- dokima/uptodate.py; grep -n "merge_group" .github/workflows/*.yml | head; grep -n "merged PR" dokima/agent.py | head
```

> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'check'])
> {
> "passed": true,
> "problems": []
> }
> agent.py
> app.json
> audit.py
> board.py
> body.py
> card.py
> checks.py
> fence.py
> icons
> manifest.py
> plan.py
> planner.py
> raises.py
> roles
> scan.py
> trail.py
> uptodate.py
> words.py
> 56:PERMISSIONS = {
> 65:    "administration": "read",
> 87:    (r"branches/[^/]+/protection", "administration"),
> 158:        have = PERMISSIONS.get(perm)
> 39825a6 Bug: a pull request that clashes with main is re-planned on every merge but never rebuilt (#374)
> 209ae2f A clash with main goes to the planner, on the record (#279)
> 61e0b7e Open PRs are brought up to date after every merge to main (#267)
> .github/workflows/done-whens.yml:7:  merge_group:
> .github/workflows/done-whens.yml:40:          ref: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
> .github/workflows/done-whens.yml:60:          HEAD_SHA: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
> .github/workflows/full-suite.yml:9:  merge_group:
> 1634:        gh("issue", "comment", str(number), "-R", repo, "--body", f"Autopilot: merged PR #{pr}")
> 2032:                step = ("merged", f"Autopilot merged PR #{pr}; what it unblocks starts when the issue closes.") if merged else \

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner split the issue into 5 stories: the queue declared and checked, uptodate stops updating branches with a queue, the queue's card and board runs do nothing, autopilot and the owner's Approve join the queue and report the merge when it lands, and AGENTS.md describes it."],
  "decided": ["Each story keeps a criterion for repos with no merge queue, where Dokima works as today.", "When the queue removes a pull request, its issue says why and the river stops for the owner."],
  "open": ["Whether Dokima turns the queue on by itself or reports a missing queue on the Setup issue (planned: it reports).", "Whether the owner's Approve adds a Dokima pull request to the queue (planned: yes, where main has a queue)."]},
 "verdict": "approve",
 "summary": "The split gives every ask from the owner's comments of 2026-10-09 to exactly one story, and asks the owner the two points their words leave open.",
 "blockers": [],
 "notes": [
  {"text": "The concern about #369 is already settled: its fix landed on main, so story 2 plans against the new dokima/uptodate.py.", "evidence": "git log -- dokima/uptodate.py shows 39825a6 '(#374)' on main, the fix for #369."},
  {"text": "Story 1 only reports a missing queue; if the owner answers that Dokima should turn it on by itself, story 1 needs its criteria redone and the app needs administration: write.", "evidence": "dokima/manifest.py:65 \"administration\": \"read\"; AGENTS.md 'The bot can't approve, can't push workflow changes, and can't change settings.'"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Dokima sets the queue up by itself when it is set up on a repo (declared in the manifest with everything else it needs from GitHub, #282)", "source": "https://github.com/dokima-dev/dokima/issues/111", "criterion": "S1.1"},
  {"ask": "Dokima turns it on only where GitHub offers it, and keeps working 
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)

`4. Bash`
```
sed -i 's/"summary": "The split gives every ask from the owner.s comments of 2026-10-09 to exactly one story, and asks the owner the two points their words leave open."/"summary": "The split gives every ask in the owner'"'"'s comments of 2026-10-09 to one story and asks the two points their words leave open."/' /tmp/dokima-out/review.json && grep summary /tmp/dokima-out/review.json && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 111 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> "summary": "The split gives every ask in the owner's comments of 2026-10-09 to one story and asks the two points their words leave open.",
> rc=0

**Agent:** I approved the planner's split for [#111](https://github.com/dokima-dev/dokima/issues/111) (merge queue: approve pull requests in any order, main stays green). The hand-back is in `/tmp/dokima-out/review.json`, and both checks on it pass.

No tests ran at this stage. A split has none yet; each story writes its own tests when it is planned.

**The split:** every ask in your comments of 2026-10-09 lands in exactly one of five stories:
1. The merge queue is declared in the manifest, and the setup check looks for it where GitHub offers one.
2. With a queue on main, the job that keeps pull requests current with main stops updating them but still finds clashes. Without a queue it works as today.
3. The card and board runs that the queue's own test runs trigger do nothing and never fail.
4. Autopilot's line says a pull request joined the queue, and the issue reports the merge when it lands, or why the queue removed it. Your Approve adds the pull request to the queue. Without a queue, nothing changes.
5. AGENTS.md describes all of this.

The split follows the rules: five stories, and no story depends on another in a loop.

**The planner's two questions for you.** I didn't accept either assumption, so on autopilot both stop for you:
- **Should Dokima turn the queue on by itself?** You wrote that it "sets the queue up by itself". The planner assumed it only reports a missing queue on the Setup issue. That is narrower than your words. Turning it on would also need a new app permission, since the app can only read settings today.
- **Should your Approve add a Dokima pull request to the queue?** This matches your words, but today an Approve starts nothing, so it changes how Dokima works.

**Notes:**
- The planner's worry about clashing with [#369](https://github.com/dokima-dev/dokima/issues/369) (a clash with main was re-planned on every merge but never rebuilt) is already settled. Its fix landed on main in [#374](https://github.com/dokima-dev/dokima/pull/374), so story 2 builds on the current code.
- If you answer that Dokima should turn the queue on itself, story 1's criteria need redoing.
