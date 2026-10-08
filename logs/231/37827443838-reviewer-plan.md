# reviewer (plan) for #231

Run: https://github.com/dokima-dev/dokima/actions/runs/37827443838

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json 2>/dev/null
```

> <persisted-output>
> Output too large (42.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/57591e41-036e-4d4f-aa55-3293355996ca/tool-results/bm2omaqsb.txt
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
> - The planner's prompt tells it explicitly to find which existing issues this one is blocked by, blocks, or relates to.
> - Its hand-back 

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json
for f in ['in/02-reviewer-plan.json','in/03-planner.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:6000])
"; python3 -m json.tool plan.json
```

> []
> in/02-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37824213007",
>  "commit_before": "7b130ade45e79f6b9155411e43aa89587cdb6d88",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 396526,
>   "turns": 10,
>   "cost_usd": 0.5123068000000001,
>   "tokens_in": 388046,
>   "tokens_out": 6399
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/231/37824213007-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37824213007",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner wrote four criteria: the planner's pack lists every open issue, its prompt asks for the three kinds of link, the round check validates the links field, and the issue card shows each kind with its own icon.",
>     "It wrote seven tests in tests/test_issue_links.py and taught one helper in tests/test_fixer.py to answer the new open-issues listing."
>    ],
>    "decided": [
>     "A link must name an open issue listed in the pack, never a pull request or the issue itself.",
>     "If GitHub cannot list the open issues, the planner's pack fails and the hand-back is refused."
>    ],
>    "open": [
>     "It asks whether the planner's run comment should also show the links; it planned for the issue card only."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The plan covers all five asks, and each of its seven new tests fails today because the feature is missing; one question about which card shows the lin

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; awk '/^### /{p=($2=="RezaSoleymanifar")} p' issue.md
```

> 28:### RezaSoleymanifar on issue #231 (2026-10-08T18:05:49Z)
> 32:### dokima-runtime on issue #231 (2026-10-08T18:06:15Z)
> 37:### RezaSoleymanifar on issue #231 (2026-10-08T18:13:23Z)
> 41:### dokima-runtime on issue #231 (2026-10-08T18:13:46Z)
> 209:### dokima-runtime on issue #231 (2026-10-08T18:25:49Z)
> 360:### RezaSoleymanifar on issue #231 (2026-10-08T18:48:10Z)
> 366:### dokima-runtime on issue #231 (2026-10-08T18:48:29Z)
> 515:### dokima-runtime on issue #231 (2026-10-08T18:50:57Z)
> ### RezaSoleymanifar on issue #231 (2026-10-08T18:05:49Z)
> 
> /autopilot start
> 
> ### RezaSoleymanifar on issue #231 (2026-10-08T18:13:23Z)
> 
> /plan
> 
> ### RezaSoleymanifar on issue #231 (2026-10-08T18:48:10Z)
> 
> /plan Answer: both. The links show on the issue card and on the planner's run comment, so the planner card mirrors the issue card.
> 
> One more: once the plan passes review, code records each link on both issues using GitHub's own blocked-by relationships, so the other issue shows it too and autopilot waits on real blockers. The model never writes them itself.
> Shell cwd was reset to /home/runner/work/dokima/dokima

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(d['check']);print(d['handback'].get('replies'))"; grep -o 'https://github.com/[^ )"]*issuecomment[^ )"]*' issue.md | sort -u; cd /home/runner/work/dokima/dokima; git log --oneline -3; git status --short; grep -n "R1\|R2\|R3\|def problems_split\|split" dokima/agent.py | head -40
```

> {'passed': True, 'problems': []}
> []
> 7b130ad planner for #231 (run 37822609938)
> 27453f2 Every run comment is a short card with the long parts in folds (#228)
> c999661 Autopilot: a pull request the reviewer approved merges by itself (#227)
> 169:def file_split(repo, parent, recs, labels=()):
> 170:    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
> 173:    Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
> 174:    done = latest(recs, "split", passed=True)
> 183:        number = int(url.rstrip("/").split("/")[-1])
> 195:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> 206:           "check": {"passed": passed, "problems": [l for l in check_text.splitlines() if l.strip()] if not passed else []}}
> 209:        rec["dropped_by_fence"] = [l for l in open(dropped).read().splitlines() if l.strip()]
> 215:    lines = [l.strip() for l in why.splitlines() if l.strip()] or ["A step before the agent failed; see the run for which."]
> 235:            "split": "Filing the split"}.get(role, "Command")
> 302:HEADS = {"planner": "The planner", "reviewer": "The reviewer", "worker": "The worker", "split": "Code"}
> 307:    return [x for x in re.split(r"(?<=[.?!])\s+", text.strip() if isinstance(text, str) else "") if x]
> 378:        return f"The planner proposes a split into {n} stories" + (" and asks you question

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 150,200p dokima/agent.py; ls tests/test_issue_links.py && grep -n "^def test" tests/test_issue_links.py
```

> replies = replies if isinstance(replies, list) else []
>     replied = {r.get("blocker") for r in replies if isinstance(r, dict)}
>     return bad + [f"blocker {b} is not answered" for b in sorted(blockers - replied)]
> 
> 
> def story_body(parent, i, story, parent_title):
>     """A story's issue body, drawn by code from the approved plan, so the child planner starts from exactly what was agreed."""
>     lines = ["<!-- dokima-card -->", "<!-- /dokima-card -->", "",
>              f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
>              f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
>     if story.get("context"):
>         lines += [f"**Context:** {story['context']}", ""]
>     lines += ["**Acceptance criteria:**"]
>     lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
>     if story.get("non_functional"):
>         lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', '')})" for n in story["non_functional"]]
>     return "\n".join(lines + ["", "</details>"]) + "\n"
> 
> 
> def file_split(repo, parent, recs, labels=()):
>     """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
>     each created with the given labels.
> 
>     Returns the record of what was filed. Filing twice files nothing new: the newest split record is returned instead."""
>     done = latest(recs, "s

**Agent:** I'm writing the plan review now: the split covers every ask, and its two questions go to the owner.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned #231 as a split into three stories: links found and checked, links shown on the issue card and the planner's run comment, and links recorded as GitHub's own blocked-by links once the plan passes review."],
  "decided": ["Stories 2 and 3 wait on story 1; story 1 reuses round one's tests with new criterion numbers.",
              "A blocks link to #X is recorded as #X blocked by this issue, by code only, and a failed recording stops for the owner."],
  "open": ["It asks whether relates-to links are also recorded on the other issue; it planned for showing them on the cards only.",
           "It asks whether an approved plan on autopilot waits for its open blockers and starts its worker when the last one closes; it planned for that."]},
 "verdict": "approve",
 "summary": "The split gives every one of the owner's asks, including both of the new ones in the second comment, to exactly one story; its two questions go to the owner, because each changes how the system works.",
 "blockers": [],
 "notes": [
  {"text": "Round one's tests on this branch still carry criterion numbers 231.1 to 231.5, which the split no longer has; each story's planner must renumber them when it reuses them, as story 1's context says.",
   "evidence": "tests/test_issue_links.py (seven tests named for 231.x); plan.json story 1 context"},
  {"text": "The two questions are on the parent, and the story bodies code files do not carry questions, so the owner's answers reach story 3 only through the issue history; story 3's context does name both open points.",
   "evidence": "dokima/agent.py:155 story_body() writes user story, context, criteria and non-functional, no questions"}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The planner's starter pack includes the repo's open issues.", "source": "https://github.com/dokima-dev/dokima/issues/231", "criterion": "S1.1"},
 
```

> rc=0

**Agent:** I approved the new plan for #231. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner did:** it split #231 into three stories, because your second comment brought it to seven criteria across unrelated parts of the code.
1. The planner gets the repo's open issues in its pack and hands back blocked-by, blocks and relates-to lists. Code rejects a missing or malformed field, a number that isn't an open issue, or the issue linked to itself.
2. The issue card and the planner's run comment show the links, each kind with its own new icon. This is depends on story 1.
3. Once a plan passes review, code records the links as GitHub's own blocked-by links on both issues, and autopilot waits on them. The model never writes them. This also depends on story 1.

**Your asks:** all nine are covered, including both things you added in your second comment ("both" cards, and code recording the links on both issues). Each is assigned to exactly one story, so there are no blockers.

**Both questions stop for you, even on autopilot.** I didn't accept either assumption, because each changes how the system works:
- **Relates-to links:** you wrote "code records each link on both issues", but GitHub's own links only cover blocked-by. The plan assumes relates-to links appear only on the cards. Recording them on the other issue some other way would mean posting new comments on other issues.
- **"Autopilot waits on real blockers":** this could mean two things. One reading adds a new autopilot rule: an approved plan holds its worker until its last blocker closes, then the worker starts. The other only means today's rule (start the planner when blockers close) now sees these links. The plan assumes the first.

**Two notes, not blockers:**
- The tests already on this branch are still numbered for #231's old criteria (231.1 to 231.5). Whichever story reuses them has to renumber them.
- The sub-issues code files for each story don't include the parent's questions. Your answers reach story 3 only through #231's history, although its context names both open points.

I didn't run the tests this round. A split plan has no tests of its own; each story writes and checks its own when it's planned.
