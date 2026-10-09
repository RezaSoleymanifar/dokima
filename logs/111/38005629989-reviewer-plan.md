# reviewer (plan) for #111

Run: https://github.com/dokima-dev/dokima/actions/runs/38005629989

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (37.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/92af2890-9516-4462-9563-23e87cd74992/tool-results/bmq1woooz.txt
> 
> Preview (first 2KB):
> # Issue #111: Merge queue: approve PRs in any order, main stays green
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Dokima works with GitHub's merge queue where a repo has one and keeps working where it has none.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #111](https://github.com/dokima-dev/dokima/issues/111)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #369, #363, #284, #272, #114
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
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not s

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-ask/,$p' issue.md | head -c 30000
```

> <!-- dokima-ask -->
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> **Objective: PRs can be approved and merged in any order without breaking main, by turning on GitHub's merge queue, as part of onboarding any repo**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: Dokima's required checks also run in the merge queue, so a queued PR is tested together with main and every PR ahead of it
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Acceptance criteria: onboarding a repo turns on the merge queue for its main branch; a PR that fails in the queue is removed with a comment saying why, and the rest of the queue carries on
> 
> </dd></dl>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
>   - [ ] Acceptance criteria: the PR's card shows the merge queue as its own line (in queue, passed, or removed with the reason), linked to that run
>   - [ ] Acceptance criteria: on repos where GitHub's merge queue is unavailable (personal accounts, private repos without Enterprise), Dokima does the same job itself before merging: update the PR to the latest main, re-run the checks, merge only if they pass
>   - [ ] Acceptance criteria: ever

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; ls in; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> {
>  "kind": "feature",
>  "summary": "Dokima works with GitHub's merge queue where a repo has one and keeps working where it has none.",
>  "feature": "With the merge queue on, approved pull requests merge in any order without breaking main, Dokima stops spending test runs on bringing branches up to date, and every card and Autopilot line tells the truth about what the queue did. Split by R2 (more than five criteria) and R3 (the manifest and audit, uptodate, the card and board workflows, autopilot's merge and AGENTS.md are unrelated parts of the code). Stories: (1) the queue is declared, and a missing one is reported on the Setup issue for the owner to switch on; (2) uptodate stops updating branches when a queue is on, depends on (1); (3) the card and board runs of the queue do nothing; (4) autopilot and the owner's Approve join the queue and report when the merge lands, depends on (1); (5) AGENTS.md describes it, depends on (1) to (4). This round takes the owner's answers of 2026-10-09: Dokima never switches the queue on itself (story 1), and the owner's Approve adds a Dokima pull request to the queue (story 4). Every promise of the owner's /plan comments of 2026-10-09 goes to exactly one story: 'sets the queue up where GitHub offers it and works without it' to (1), with 'works without it' also kept story by story as each one's no-queue criterion; 'uptodate.yml stops updating branches when a queue is on but keeps finding cla

`4. Bash`
```
cd /tmp/pack; grep -o 'issuecomment-[0-9]*' issue.md | sort -u; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d,indent=1)[:3000])"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "38004532506",
>  "commit_before": "39825a662f7f1107a85d897006f18f49fd757b6c",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 53003,
>   "turns": 5,
>   "cost_usd": 0.39987219999999996,
>   "tokens_in": 191562,
>   "tokens_out": 5935
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/111/38004532506-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38004532506",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner split the issue into 5 stories: the queue declared and checked, uptodate stops updating branches with a queue, the queue's card and board runs do nothing, autopilot and the owner's Approve join the queue and report the merge when it lands, and AGENTS.md describes it."
>    ],
>    "decided": [
>     "Each story keeps a criterion for repos with no merge queue, where Dokima works as today.",
>     "When the queue removes a pull request, its issue says why and the river stops for the owner."
>    ],
>    "open": [
>     "Whether Dokima turns the queue on by itself or reports a missing queue on the Setup issue (planned: it reports).",
>     "Whether the owner's Approve adds a Dokima pull request to the queue (planned: yes, where main has a queue)."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The split gives every ask in the owner's comments of 2026-10-09 to one story and asks the two points their words leave open.",
>   "blockers": 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def needs_you\|def compare\|BRANCH_RULES\|rules/branches" dokima/audit.py dokima/manifest.py | head; grep -n "update-branch\|def trial_merge\|def clash" dokima/uptodate.py | head; grep -n "merged PR" dokima/agent.py | head; grep -n "merge_group\|workflow_run" .github/workflows/card.yml .github/workflows/board.yml | head
```

> dokima/manifest.py:52:BRANCH_RULES = {
> dokima/manifest.py:88:    (r"rules/branches/", "metadata"),
> dokima/manifest.py:113:BRANCH_RULE = re.compile(r"(?:rules/branches/([\w.\-]+)|branches/([\w.\-]+)/protection)")
> dokima/manifest.py:221:            if branch not in BRANCH_RULES:
> dokima/audit.py:37:def compare_labels(live):
> dokima/audit.py:53:def compare_fields(live):
> dokima/audit.py:76:def compare_views(live):
> dokima/audit.py:91:def compare_rule(branch, live, want):
> dokima/audit.py:103:def compare_permissions(live):
> dokima/audit.py:119:def compare(github, repo):
> 51:            rest("PUT", f"repos/{repo}/pulls/{n}/update-branch", expected_head_sha=head)
> 64:def trial_merge(base, sha, pr):
> 117:def clash(repo, base, sha, pr, rest=api, files=None, owners=None):
> 1634:        gh("issue", "comment", str(number), "-R", repo, "--body", f"Autopilot: merged PR #{pr}")
> 2032:                step = ("merged", f"Autopilot merged PR #{pr}; what it unblocks starts when the issue closes.") if merged else \
> .github/workflows/board.yml:27:  workflow_run:
> .github/workflows/card.yml:14:  workflow_run:
> .github/workflows/card.yml:34:    if: github.event_name == 'workflow_run' || (github.event_name == 'pull_request_target' && github.event.pull_request.merged) || github.event_name == 'schedule' || (github.event_name == 'issues' && github.event.action == 'opened') || (github.event_name != 'pull_request_target' && github.event.sender.type != 'Bot' && !github.event.issue.pull_request && !(github.event_name 

**Agent:** The plan's references to the code check out. Now I'm writing the review: approve.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-split the issue into the same 5 stories and took in the owner's two answers of 2026-10-09."],
  "decided": ["Dokima never switches the merge queue on; where GitHub offers one and main has none, the Setup issue says only the owner can switch it on, marked Needs you.",
              "A code owner's Approve on a pull request Dokima built adds it to the merge queue where main has one; without a queue an Approve still starts nothing.",
              "When the queue removes a pull request, its issue says why and the river stops for the owner."],
  "open": []},
 "verdict": "approve",
 "summary": "The split now follows both of the owner's answers and gives every ask of the 2026-10-09 comments to exactly one story, with no questions left.",
 "blockers": [],
 "notes": [
  {"text": "Story 4's 'the river stops for the owner' when the queue removes a pull request goes a little past the owner's words ('or why the queue removed it'); it follows the rule that a failure always says why and blocks, but story 4's planner should keep it to one stop with the Needs you pill, not a new kind of stop.",
   "evidence": "plan.json story 4 criterion 3; AGENTS.md Principles, 'Fail closed'."},
  {"text": "Story 4 will need commands.yml to react to an approved review, and story 3 changes card.yml and board.yml; the issue names those workflows, but each story's planner must list the workflow files in its scope, since AGENTS.md forbids changing .github/workflows/ unless the issue asks.",
   "evidence": ".github/workflows/card.yml:14 and board.yml:27 run on workflow_run; AGENTS.md 'Never change .github/workflows/ ... unless the issue explicitly asks.'"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Dokima sets the queue up by itself when it is set up on a repo (declared in the manifest with everything else it needs from GitHub, #282)", "source": "ht
```

> (Bash completed with no output)

**Agent:** I approved the plan for issue [#111](https://github.com/dokima-dev/dokima/issues/111) (merge queue: approve PRs in any order, main stays green). The review is in `/tmp/dokima-out/review.json` and passed both hand-back checks.

The plan splits the work into five stories:
1. **Setup:** the manifest declares the merge queue. Where GitHub offers a queue and main has none, the Setup issue [#324](https://github.com/dokima-dev/dokima/issues/324) says only the owner can switch it on, marked Needs you. Dokima never turns the queue on itself, and the app keeps read-only admin access.
2. **Branch updates:** with a queue on, `uptodate.yml` stops updating branches but still finds clashes. Without a queue it keeps updating them as it does now.
3. **Card and board runs:** `card.yml` and `board.yml` do nothing on the queue's own runs and never fail.
4. **Merging:** autopilot's line says a pull request joined the queue, the merge is reported when it lands, and the issue says why if the queue removes it. A code owner's Approve on a pull request Dokima built adds it to the queue.
5. **AGENTS.md** describes all of the above.

- **Owner's answers:** the plan now follows both of the owner's answers from 2026-10-09: report a missing queue rather than turn it on, and let an Approve add a pull request to the queue. It has no questions left.
- **Coverage:** every ask from the owner's comments of 2026-10-09 is covered by exactly one story criterion.
- **Code references:** the files and functions the plan points to exist where it says.
- **No blockers, no earlier blockers to close:** there were none open from the last round.

I left two notes for the stories' planners, neither blocking:
- **Stopping for the owner:** story 4 says the river stops for the owner when the queue removes a pull request. The owner only asked to be told why, so this goes slightly further. It fits the rule that a failure always blocks and says why, but it should stay one stop with the Needs you pill.
- **Workflow files:** stories 3 and 4 will need to change `card.yml`, `board.yml` and probably `commands.yml`. The issue explicitly asks for those changes, but each story's planner must list the files in its scope.
