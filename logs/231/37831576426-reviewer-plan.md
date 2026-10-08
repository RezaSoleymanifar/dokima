# reviewer (plan) for #231

Run: https://github.com/dokima-dev/dokima/actions/runs/37831576426

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null
```

> <persisted-output>
> Output too large (103.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/013ff2fe-64be-42d7-9394-241544879d58/tool-results/bf1rjfqi2.txt
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
> # Issue #231: The planner finds the issues this one blocks, is blocked by, or relates to
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> Today nothing finds links between this issue and the ones already open. Blocking is only tracked between sibling stories of one split, and the reviewer's issues found are new issues, not links to existing ones.
> 
> What I want:
> - The planner's starter pack includes the repo's open issues.
> - The planner's prompt tells it explicitly to find which ex

`2. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; cat open_blockers.json; python3 -c "
import json
p=json.load(open('plan.json'));print(json.dumps(p,indent=1)[:20000])"
```

> 28:### RezaSoleymanifar on issue #231 (2026-10-08T18:05:49Z)
> 32:### dokima-runtime on issue #231 (2026-10-08T18:06:15Z)
> 37:### RezaSoleymanifar on issue #231 (2026-10-08T18:13:23Z)
> 41:### dokima-runtime on issue #231 (2026-10-08T18:13:46Z)
> 209:### dokima-runtime on issue #231 (2026-10-08T18:25:49Z)
> 360:### RezaSoleymanifar on issue #231 (2026-10-08T18:48:10Z)
> 366:### dokima-runtime on issue #231 (2026-10-08T18:48:29Z)
> 515:### dokima-runtime on issue #231 (2026-10-08T18:50:57Z)
> 687:### RezaSoleymanifar on issue #231 (2026-10-08T19:11:29Z)
> 691:### dokima-runtime on issue #231 (2026-10-08T19:11:52Z)
> 866:### dokima-runtime on issue #231 (2026-10-08T19:13:49Z)
> 1060:### RezaSoleymanifar on issue #231 (2026-10-08T19:21:38Z)
> 1064:### dokima-runtime on issue #231 (2026-10-08T19:21:59Z)
> 1262:### dokima-runtime on issue #231 (2026-10-08T19:23:19Z)
> []{
>  "kind": "feature",
>  "summary": "The planner finds which open issues this one is blocked by, blocks or relates to; code checks those links, shows them on the cards of both issues, records blocking as GitHub's own blocked-by links once the plan passes review, keeps both cards current when a link is added or removed by hand, and autopilot holds a blocked issue's worker until its blockers close.",
>  "feature": "Every plan says how its issue connects to the other open issues, the owner sees it on the cards of both issues whether a plan or a person made the link, GitHub itself records who waits on whom, and autopilot never starts work that is st

`3. Bash`
```
cd /tmp/pack; sed -n 355,366p issue.md; sed -n 685,692p issue.md; sed -n 1058,1066p issue.md; sed -n 1262,1500p issue.md | head -120
```

> <sub>Opus 5.5 · 6.6 min · 10 turns · 388,046 tokens in, 6,399 out · $0.51 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/231/37824213007-reviewer-plan.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37824213007)</sub>
> 
> **Next:** @RezaSoleymanifar The reviewer did not accept the plan's assumption for: "By "the card shows them", do you mean only the card at the top of the issue and its pull request, or also the planner's run comment?" Answer with `/plan` and your words, or say `/work` to build it on its assumptions.
> 
> 
> ### RezaSoleymanifar on issue #231 (2026-10-08T18:48:10Z)
> 
> /plan Answer: both. The links show on the issue card and on the planner's run comment, so the planner card mirrors the issue card.
> 
> One more: once the plan passes review, code records each link on both issues using GitHub's own blocked-by relationships, so the other issue shows it too and autopilot waits on real blockers. The model never writes them itself.
> 
> ### dokima-runtime on issue #231 (2026-10-08T18:48:29Z)
> 
> 
> ### RezaSoleymanifar on issue #231 (2026-10-08T19:11:29Z)
> 
> /plan Answers: Relates to is never written as a comment. Code updates the cards of both issues whenever any link (blocked by, blocks, relates to) is added or removed, and handles a contradiction, like two issues blocking each other, as an edge case. On autopilot, a blocked issue still plans, but its worker waits until every blocker closes, then starts by itself.
> 
> ### dokima-runtime on iss

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
r=json.load(open('06-reviewer-plan.json'));print(json.dumps(r,indent=1)[:8000])
p=json.load(open('07-planner.json'));print(json.dumps({k:v for k,v in p.items() if k!='handback'},indent=1)[:3000]); print(p.keys())"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37830376602",
>  "commit_before": "7b130ade45e79f6b9155411e43aa89587cdb6d88",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 37906,
>   "turns": 7,
>   "cost_usd": 0.2395584,
>   "tokens_in": 199427,
>   "tokens_out": 4138
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/231/37830376602-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37830376602",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner re-planned #231 as a split into four stories: links found and checked, links shown on the cards, links recorded on both issues once the plan passes review, and autopilot holding a blocked issue's worker."
>    ],
>    "decided": [
>     "Relates-to links are never posted as comments; code redraws the cards of both issues when an approved plan adds or drops any link.",
>     "Two issues that would block each other record none of the plan's links and stop for the owner.",
>     "On autopilot a blocked issue plans as usual, and its worker starts with `Autopilot: blockers closed, starting work` when the last blocker closes."
>    ],
>    "open": [
>     "It asks whether a blocked-by link a person adds or removes by hand on GitHub also redraws both cards at once; it planned for only links an approved plan changes."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The four-story split gives every one of the owner's asks, including all three answer

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_issue_links.py 2>&1 | tail -10; git diff --stat main..HEAD; grep -rn "dependenc\|issue_dependencies" .github/workflows | head
```

> **Out of scope:**
>   
>   
>   **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
>   
>   <!-- /dokima-card -->
> assert []
> FAILED tests/test_issue_links.py::test_the_planner_never_plans_without_the_open_issues - Failed: DID NOT RAISE Exception
> 7 failed in 0.41s
>  tests/test_fixer.py       |   3 +
>  tests/test_issue_links.py | 290 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 293 insertions(+)

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned #231 as a split into five stories, adding a fifth: a blocked-by link a person adds or removes by hand on GitHub updates the cards of both issues."],
  "decided": ["Story 4 now promises that AGENTS.md's flow section states the autopilot rule for blocked issues.",
              "Story 5 shows a hand-made loop of two issues blocking each other on both cards and, on autopilot, stops for the owner.",
              "The link lines on a card come from GitHub's own blocked-by links read when the card is drawn; if GitHub cannot list them, the card says so."],
  "open": ["Story 5's planner must find which GitHub event, if any, runs when a blocked-by link changes, or pick the nearest reliable trigger."]},
 "verdict": "approve",
 "summary": "The five-story split now gives every ask of the owner, including the 19:21 answer on hand-made links, to exactly one story, and asks nothing more of the owner.",
 "blockers": [],
 "notes": [
  {"text": "Story 2 draws the links \"the newest plan has\", while story 5 says blocking lines come from GitHub's own links read when the card is drawn; story 5's planner should state plainly which source wins for blocked-by and blocks lines so the two stories do not draw different things.",
   "evidence": "plan.json story 2 criterion 1 and story 5 non_functional"},
  {"text": "GitHub Actions may have no workflow event for a blocked-by link changing; if story 5's planner falls back to a schedule, its plan should say how soon a card catches up so the owner sees the delay.",
   "evidence": "plan.json story 5 context; no workflow in .github/workflows listens to dependency changes (grep found none)"},
  {"text": "Round one's tests on this branch still carry criterion numbers 231.1 to 231.5 and fail today for the right reason; stories 1 and 2 must renumber them when reusing them.",
   "evidence": "python3 -m pytest -q tests/test_issue_lin
```

> 0

**Agent:** I approved the plan for #231. Each of the owner's asks now belongs to exactly one story, and the plan has no questions left for the owner. The verdict is saved in `/tmp/dokima-out/review.json`, and both hand-back checks passed.

**What changed this round:** the planner split the work into five stories instead of four. The new fifth story covers the owner's 19:21 answer: a blocked-by link someone adds or removes by hand on GitHub updates the cards of both issues. Story 4 now also requires the flow section of AGENTS.md to describe the autopilot rule for blocked issues; I had flagged that gap last round.

**The stories:**
1. The planner gets the open issues and finds the links, and code checks them.
2. The issue card and the planner's run comment show the links, each kind with its own icon.
3. Once the plan passes review, code records the links on both issues as GitHub's own blocked-by links and redraws both cards. If two issues would block each other, nothing is recorded and the river stops for the owner.
4. On autopilot, a blocked issue still plans, but its worker waits until every blocker closes and then starts by itself.
5. A link added or removed by hand updates both cards.

**Tests:** this is a split, so each story's planner writes its own tests. The 7 tests already on the branch from round one still fail for the right reason: the feature is missing.

**Notes, none of them blocking:**
- **Which source the card uses:** story 2 draws the links the newest plan has. Story 5 instead reads the blocked-by and blocks lines from GitHub's own links at the time the card is drawn. Story 5's planner should say which source wins.
- **What triggers the redraw:** nothing in this repo's workflows runs today when a dependency changes, and GitHub Actions may have no event for it. If story 5's planner falls back to a scheduled run, its plan should say how long a card can lag.
- **Test numbers:** stories 1 and 2 must give round one's tests new criterion numbers when they reuse them.
