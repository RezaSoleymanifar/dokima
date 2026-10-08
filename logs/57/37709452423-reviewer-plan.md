# reviewer (plan) for #57

Run: https://github.com/dokima-dev/dokima/actions/runs/37709452423

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (35.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fa856f50-fe35-4b59-afd7-1b9ebfba455d/tool-results/brwdnx338.txt
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
> 02-planner.json
> # Issue #57: Keep PRs up to date with main automatically
> 
> - [ ] Goal: PRs that fall behind main are brought up to date automatically, with GitHub's own record of it
>   - [ ] Done when: when main changes, a workflow runs GitHub's "Update branch" on every open PR that is behind
>     Verified by: a test that a workflow runs on pushes to main and calls the update-branch API for PRs that are behind
> 
> **Not checked:** the timeline entry on the real PR page.
> 
> Requested by Reza in chat, 2026-10-03. Parked.
> 
> <details><summary><b>Context</b></summary>
> 
> From the [design chat](https://claude.ai/chat/ec603489-6708-440d-a512-327390dbcd94) between Reza and Claude, 2026-10-03 to 2026-10-04.
> 
> The merge gate is strict: a branch must be up to date with main and is checked against the latest main. That means queued PRs go stale after every merge.
> 
> Updates should not depend on a chat remembering to do them. When automated, they should use GitHub's own "Update branch" action so the timeline records it.
> 
> For now Reza is fine tapping "Update branch" himself, so automation is wanted but not urgent.
> 
> </details>
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #57 (2026-10-07T21:56:38Z)
> 
> Hybrid. After each merge, up

`2. Bash`
```
cd /tmp/pack; sed -n 30,400p issue.md; echo ====; cat open_blockers.json; echo ===; cat plan.json
```

> <persisted-output>
> Output too large (34.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/fa856f50-fe35-4b59-afd7-1b9ebfba455d/tool-results/bzuztkrsg.txt
> 
> Preview (first 2KB):
> ### RezaSoleymanifar on issue #57 (2026-10-07T21:56:39Z)
> 
> /plan
> 
> ### dokima-runtime on issue #57 (2026-10-07T21:59:00Z)
> 
> <!-- dokima-record -->
> **Planner**
> 
> Proposes a split: PRs never sit stale behind main: after each merge Dokima updates every open PR that fell behind, sends clashes to the PR's worker, and GitHub's merge queue retests each PR on the latest main before it merges.
> 
> 1. Open PRs are brought up to date after every merge to main
> 2. Clashes with main go to the PR's worker
> 3. Queued PRs are retested on the latest main before merging
> 
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - For PRs Dokima did not build there is no worker, so story 2 comments on the clash and mentions you instead; is that the reading you meant by 'send clashes to its worker'?
> 
> <details><summary>Full record</summary>
> 
> ```json
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37692901600",
>  "commit_before": "acfbaa71555f8fb187d080aa32eddaa3ef69e204",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 110078,
>   "turns": 10,
>   "cost_usd": 0.6225242,
>   "tokens_in": 400876,
>   "tokens_out": 10330
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/57/37692901600

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/fa856f50-fe35-4b59-afd7-1b9ebfba455d/tool-results/bzuztkrsg.txt
```

> 1	### RezaSoleymanifar on issue #57 (2026-10-07T21:56:39Z)
> 2	
> 3	/plan
> 4	
> 5	### dokima-runtime on issue #57 (2026-10-07T21:59:00Z)
> 6	
> 7	<!-- dokima-record -->
> 8	**Planner**
> 9	
> 10	Proposes a split: PRs never sit stale behind main: after each merge Dokima updates every open PR that fell behind, sends clashes to the PR's worker, and GitHub's merge queue retests each PR on the latest main before it merges.
> 11	
> 12	1. Open PRs are brought up to date after every merge to main
> 13	2. Clashes with main go to the PR's worker
> 14	3. Queued PRs are retested on the latest main before merging
> 15	
> 16	**Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> 17	- For PRs Dokima did not build there is no worker, so story 2 comments on the clash and mentions you instead; is that the reading you meant by 'send clashes to its worker'?
> 18	
> 19	<details><summary>Full record</summary>
> 20	
> 21	```json
> 22	{
> 23	 "role": "planner",
> 24	 "stage": null,
> 25	 "run_id": "37692901600",
> 26	 "commit_before": "acfbaa71555f8fb187d080aa32eddaa3ef69e204",
> 27	 "started_by": "RezaSoleymanifar",
> 28	 "models": [
> 29	  "claude-opus-5-5"
> 30	 ],
> 31	 "report": {
> 32	  "duration_ms": 110078,
> 33	  "turns": 10,
> 34	  "cost_usd": 0.6225242,
> 35	  "tokens_in": 400876,
> 36	  "tokens_out": 10330
> 37	 },
> 38	 "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/57/37692901600-planner.md",
> 39	 "run": "https://github.com/dokima-dev/dokima/actions/runs/37692901600",
> 40	 "handback": {
> 41	

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline main..HEAD; git diff --stat main; python3 -c "import json;d=json.load(open('/tmp/pack/in/02-planner.json'));print(d.keys());print(d.get('check'))"; grep -n "merge_group\|merge queue" -ri .github dokima AGENTS.md | head
```

> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> {'passed': True, 'problems': []}
> AGENTS.md:31:- **Use what GitHub already has.** Comments, reviews, checks, branch protection, CODEOWNERS, project boards, merge queue. Build only the thin glue GitHub lacks.
> AGENTS.md:36:- **Small and lean.** One issue, one PR. Fold related things together. Extras (the board, merge queue) are optional and never required.
> AGENTS.md:116:- Dokima lives in the `dokima-dev` organization so its bot can keep the project board and use the merge queue; on personal repos those extras fall back or are skipped.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "pull_request\|GITHUB_EVENT" dokima/checks.py | head; grep -n "merge -q\|BASE=\|concurrency\|group:" .github/workflows/agent.yml | head; grep -n "^on:" -A6 .github/workflows/full-suite.yml .github/workflows/done-whens.yml; grep -n "def issue_of_pr" -A8 dokima/agent.py
```

> 85:        pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]
> 33:concurrency:
> 34:  group: agent-${{ (inputs.issue || github.event.client_payload.issue) }}
> 82:              git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
> 91:          echo "BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> 93:          echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
> 95:          echo "PLANNER_RUN_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> .github/workflows/full-suite.yml:3:on:
> .github/workflows/full-suite.yml-4-  pull_request:
> .github/workflows/full-suite.yml-5-  push:
> .github/workflows/full-suite.yml-6-    branches: [main]
> .github/workflows/full-suite.yml-7-permissions:
> .github/workflows/full-suite.yml-8-  contents: read
> .github/workflows/full-suite.yml-9-jobs:
> .github/workflows/done-whens.yml:4:on:
> .github/workflows/done-whens.yml-5-  pull_request_target:
> .github/workflows/done-whens.yml-6-permissions:
> .github/workflows/done-whens.yml-7-  contents: read
> .github/workflows/done-whens.yml-8-  issues: read
> .github/workflows/done-whens.yml-9-  pull-requests: read
> .github/workflows/done-whens.yml-10-jobs:
> 626:def issue_of_pr(head, body):
> 627-    """The issue a pull request was built for: from its branch (work/issue-N or try/issue-N), else 'Closes #N'."""
> 628-    m = re.match(r"(?:work|try)/issue-(\d+)$", head or "") or re.search(r"(?i)\b(?:closes|fixes|resolves) #(\d+)", body or "")
> 629-    return m.group(1

**Agent:** Reading done: it's a three-part split plan with no tests yet, and the context it relies on matches the repo. Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned issue #57 as a split into three stories: bring open PRs up to date after each merge, send a clash to the planner on the record, and retest queued PRs on the latest main."],
  "decided": ["A clash on a Dokima PR posts a bot record on the issue naming the merge and the files that clashed, then starts the planner, never the worker.",
              "A clash on a PR Dokima did not build starts no agent and mentions the owner on the PR.",
              "Turning on the merge queue stays an owner setting on GitHub; the story only makes the checks run inside the queue."],
  "open": ["Each story still needs its own plan and tests once the split is approved with /work."]},
 "verdict": "approve",
 "summary": "The split covers every ask, including the owner's three follow-ups on 2026-10-07 (clashes go to the planner, the record names the merge and what clashed, PRs Dokima didn't build only ping the owner), and gives each one to exactly one story.",
 "blockers": [],
 "notes": [
  {"text": "Stories 1 and 2 both promise a comment on the PR when an update is refused. Story 1 criterion 3 says 'one comment' with GitHub's reason, and story 2 criterion 3 adds a comment naming the merge and the files for PRs Dokima didn't build. When the child stories are planned, they should say whether this is one comment or two, so the 'one comment' test can't be passed by either reading.", "evidence": "plan.json stories[0].acceptance_criteria[2] and stories[1].acceptance_criteria[2]"},
  {"text": "Story 2 treats only try/issue-N branches as Dokima PRs, but the code that links a PR to its issue also accepts work/issue-N branches and 'Closes #N'. Story 2's plan should say which of these count as a PR Dokima built.", "evidence": "dokima/agent.py:626-629 issue_of_pr; plan.json stories[1].acceptance_criteria[0]"},
  {"text": "Story 3 depends on the owner turning on the merge queue in G
```

> rc=0

**Agent:** I approved the plan for issue #57, and the review is in `/tmp/dokima-out/review.json`. Both hand-back checks passed.

**What the plan is:** the planner split the issue into three stories:
1. **Keep PRs up to date:** after every merge to main, each open PR that fell behind is updated with GitHub's own "Update branch".
2. **Clashes go to the planner:** when a Dokima PR clashes with main, the issue gets a record naming the merge and the files that clashed, and the planner starts right away. A clash on a PR Dokima didn't build starts nothing and pings the owner.
3. **Merge queue retest:** the checks also run inside GitHub's merge queue, so each PR is retested on the latest main. Turning the queue on stays the owner's job in GitHub's settings.

**Why it passes:** each of the owner's asks, including the three follow-ups of 2026-10-07, belongs to exactly one story. Each source traces to the owner's own words. Story 2 waits for story 1, and there are no cycles. I checked the plan's claims about the current code against the repo and they hold. No test was run: this plan is only the split, so the branch has no tests yet. Each story gets its own plan and tests once the owner approves the split with `/work`.

**Notes for the story plans (none block):**
- **Possible double comment:** stories 1 and 2 could both comment on the same PR when an update is refused. Story 1 promises "one comment", so the story plans should settle whether it's one comment or two.
- **Which PRs count as Dokima's:** story 2 counts only `try/issue-N` branches. But the code that links a PR to its issue also accepts `work/issue-N` branches and "Closes #N" (`dokima/agent.py:626`). Story 2's plan should say which of these count.
- **Owner's setting:** story 3 should list turning on the merge queue as a manual step for the owner.

I found no problems outside this issue worth proposing as new ones.
