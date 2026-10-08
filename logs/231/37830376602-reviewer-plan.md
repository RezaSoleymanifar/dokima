# reviewer (plan) for #231

Run: https://github.com/dokima-dev/dokima/actions/runs/37830376602

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null
```

> <persisted-output>
> Output too large (71.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/db9bda4d-8e63-4c1d-95d4-3c9149c7e0c8/tool-results/b1hfts8u1.txt
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
> - The planner's prompt tells it explicitly to find which existing issues this one is blocked by, b

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json
p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []
> {
>  "kind": "feature",
>  "summary": "The planner finds which open issues this one is blocked by, blocks or relates to; code checks those links, shows them on the cards of both issues, records blocking as GitHub's own blocked-by links once the plan passes review, and autopilot holds a blocked issue's worker until its blockers close.",
>  "feature": "Every plan says how its issue connects to the other open issues, the owner sees it on the cards of both issues, GitHub itself records who waits on whom, and autopilot never starts work that is still blocked.",
>  "stories": [
>   {
>    "title": "The planner finds the issues this one is blocked by, blocks or relates to, and code checks them",
>    "user_story": "Every plan names the open issues its issue is blocked by, blocks and relates to, and code refuses a plan whose links are missing, malformed or wrong.",
>    "context": "Split from #231 under rule R2 (seven criteria once the owner's second comment added the run comment and GitHub's own links) and R3 (the native links live in the river and autopilot code, apart from the pack and checks). Round one of #231 planned this part and its plan review passed it; its tests are on branch try/issue-231 in tests/test_issue_links.py (criteria 231.1, 231.2, 231.3 and 231.5 there map to this story's criteria 1, 2, 3 and its non-functional requirement) and can be reused with new criterion numbers, together with the fake_github helper change in tests/test_fixer.py. Where the work goes: agent.pack() in do

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; python3 -c "
import json
r=json.load(open('in/04-reviewer-plan.json'));print(json.dumps(r,indent=1)[:8000])
r=json.load(open('in/05-planner.json'));print(json.dumps({k:v for k,v in r.items() if k!='plan'},indent=1)[:4000])"
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
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37827443838",
>  "commit_before": "7b130ade45e79f6b9155411e43aa89587cdb6d88",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 57126,
>   "turns": 7,
>   "cost_usd": 0.28835599999999995,
>   "tokens_in": 236198,
>   "tokens_out": 5601
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/231/37827443838-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37827443838",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner re-planned #231 as a split into three stories: links found and checked, links shown on the issue card and the planner's run comment, and links recorded as GitHub's own blocked-by links once the plan passes review."
>    ],
>    "decided": [
>     "Stories 2 and 3 wait o

`4. Bash`
```
cd /tmp/pack; sed -n 355,370p issue.md; sed -n 680,700p issue.md; sed -n 866,1000p issue.md | head -60
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
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> The planner proposes a split into 3 stories and asks you questions.
> 
> </details>
> 
> <sub>Opus 5.5 · 1.0 min · 7 turns · 236,198 tokens in, 5,601 out · $0.29 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/231/37827443838-reviewer-plan.md) · [run](ht

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 --stat | head -20; timeout 300 python3 -m pytest -q tests/test_issue_links.py 2>&1 | tail -15; grep -n "def check_split\|R1\|R2\|R3" dokima/agent.py | head
```

> 7b130ad planner for #231 (run 37822609938)
>  tests/test_fixer.py       |   3 +
>  tests/test_issue_links.py | 290 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 293 insertions(+)
> 27453f2 Every run comment is a short card with the long parts in folds (#228)
>  AGENTS.md               |   3 +-
>  dokima/agent.py         | 175 ++++++++++++++++++++-----
>  dokima/card.py          |  10 +-
>  tests/test_run_cards.py | 340 ++++++++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 492 insertions(+), 36 deletions(-)
> c999661 Autopilot: a pull request the reviewer approved merges by itself (#227)
>  .github/workflows/agent.yml |   6 +-
>  AGENTS.md                   |   4 +-
>  dokima/agent.py             | 124 +++++++-
>  tests/test_automerge.py     | 702 ++++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 831 insertions(+), 5 deletions(-)
>   </table>
>   
>   **Scope:**
>   
>   - dokima/x.py
>   
>   **Out of scope:**
>   
>   
>   **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
>   
>   <!-- /dokima-card -->
> assert []
> FAILED tests/test_issue_links.py::test_the_planner_

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned #231 as a split into four stories: links found and checked, links shown on the cards, links recorded on both issues once the plan passes review, and autopilot holding a blocked issue's worker."],
  "decided": ["Relates-to links are never posted as comments; code redraws the cards of both issues when an approved plan adds or drops any link.",
              "Two issues that would block each other record none of the plan's links and stop for the owner.",
              "On autopilot a blocked issue plans as usual, and its worker starts with `Autopilot: blockers closed, starting work` when the last blocker closes."],
  "open": ["It asks whether a blocked-by link a person adds or removes by hand on GitHub also redraws both cards at once; it planned for only links an approved plan changes."]},
 "verdict": "approve",
 "summary": "The four-story split gives every one of the owner's asks, including all three answers from the 19:11 comment, to exactly one story; its one question goes to the owner because it changes what triggers a card redraw.",
 "blockers": [],
 "notes": [
  {"text": "The owner asked that a contradiction be handled \"as an edge case\" without saying how; story 3 chooses to record nothing and stop for the owner, which follows Fail closed, but story 3's planner should say so in its plan so the owner sees the choice.",
   "evidence": "plan.json story 3 criterion 3; owner comment 2026-10-08T19:11:29Z"},
  {"text": "Story 4's context says AGENTS.md's flow section must state the new autopilot rule, but no criterion of story 4 promises it; its planner should add it to scope.",
   "evidence": "plan.json story 4 context and acceptance_criteria"},
  {"text": "Round one's tests on this branch still carry criterion numbers 231.1 to 231.5 and fail today for the right reason (7 failed, e.g. DID NOT RAISE for the missing open-issues fetch); story 1 and 2
```

> 0

**Agent:** I approved the plan for #231. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

The planner split the issue into four stories:
1. **Finding the links:** the planner gets the repo's open issues, finds which ones this issue is blocked by, blocks or relates to, and code checks those links.
2. **Showing the links:** the issue card and the planner's run comment show each kind of link with its own icon.
3. **Recording the links:** once the plan passes review, code records them on both issues. Blocking links become GitHub's own blocked-by links, and relates-to links are never posted as comments. Code redraws both issues' cards. If two issues would end up blocking each other, the river stops for you.
4. **Autopilot:** a blocked issue still plans, but its worker waits and starts by itself when its last blocker closes.

Every ask in your issue and your two comments (18:48 and 19:11) is in exactly one of these stories.

**The plan's question: your call.** You said cards update "whenever any link is added or removed". The plan assumes that covers only links an approved plan adds or drops. A blocked-by link someone adds or removes by hand on GitHub would only show the next time each card is redrawn. I didn't accept that assumption: it narrows what you wrote, and reacting to links made by hand would need a new trigger. So on autopilot this stops for you to answer.

**Notes for the story planners (they don't block approval):**
- **Contradictions:** you said to handle one "as an edge case" without saying how. Story 3 records none of the plan's links and stops for you. Its plan should say that choice openly so you see it.
- **AGENTS.md:** story 4's context says the file has to describe the new autopilot rule, but none of its criteria promise it.
- **Old tests:** round one's tests in `tests/test_issue_links.py` all fail today because the feature is missing, which is the right reason. They still use the old criterion numbers (231.1 to 231.5), so stories 1 and 2 must renumber them when they reuse them.
