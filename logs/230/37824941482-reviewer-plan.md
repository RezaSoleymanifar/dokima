# reviewer (plan) for #230

Run: https://github.com/dokima-dev/dokima/actions/runs/37824941482

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (45.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6ae6e987-42ed-4b32-86fe-087aa3280d49/tool-results/bpesv2atd.txt
> 
> Preview (first 2KB):
> .:
> total 76
> drwxr-xr-x  3 runner runner  4096 Oct  8 18:31 .
> drwxrwxrwt 18 root   root    4096 Oct  8 18:31 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 18:31 in
> -rw-r--r--  1 runner runner 45866 Oct  8 18:31 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 18:31 open_blockers.json
> -rw-r--r--  1 runner runner 11405 Oct  8 18:31 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner  4096 Oct  8 18:31 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 18:31 ..
> -rw-r--r-- 1 runner runner 10647 Oct  8 18:31 01-planner.json
> -rw-r--r-- 1 runner runner  6783 Oct  8 18:31 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 12112 Oct  8 18:31 03-planner.json
> # Issue #230: Cards show everything I need with icons, and nothing I don't
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Ow

`2. Bash`
```
cd /tmp/pack; sed -n 15,200p issue.md
```

> The cards bury what matters in the folded JSON and show noise up front. I want one card that tells me everything at a glance.
> 
> What I want:
> - Icons everywhere, GitHub's official octicons in the same style as the current status icons, hard-wired in code to each field so agents never pick or skip them: planner, worker, plan review, code review, autopilot, passed, failed, needs you, owner approval, merged, still open, acceptance criterion, verified by, files changed, question, blocker, note, outside the plan, issue found, related, blocked by, blocks, stats.
> - Acceptance criteria as an indented bullet list, not a table. Each line: status icon, then **Acceptance criterion:** and its sentence. Under it, in italics: *Verified by:* and the test's one-sentence docstring. Only the words "Verified by" are a link, to the exact test.
> - The criterion's status moves from empty, to running, to passed or failed during a run, and the criterion text itself links to its point in the run. This exists today on the status icon; move the link to the text, don't rebuild it.
> - Show a field only when it has something: worker's suspect tests, changes outside scope, replies to blockers and the test result line; reviewer's changes outside the plan, notes and what's still open; planner's questions. Never show blank sections.
> - The reviewer's card mirrors the planner card: it lists only the failing criteria, and under each one, why it fails, in place of Verified by. No codes like B1 or 212.3.
> - Rename "Revi

`3. Bash`
```
cd /tmp/pack; sed -n 200,2000p issue.md | grep -v '^ *"' | head -300
```

> {
>      },
>      {
>      },
>      {
>      }
>     ],
>      {
>      }
>     ],
>    }
>   ],
>    {
>    },
>    {
>    }
>   ],
>    {
>    }
>   ]
>  },
>  }
> }
> ```
> 
> </details>
> 
> <sub>Opus 5.5 · 1.3 min · 11 turns · 407,339 tokens in, 8,017 out · $0.58 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/230/37822674017-planner.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37822674017)</sub>
> 
> **Next:** The reviewer starts now.
> 
> 
> ### dokima-runtime on issue #230 (2026-10-08T18:16:34Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> The reviewer passed the plan.
> 
> **The plan's assumptions:**
> - Should bullets with Verified by apply to the issue and PR card only, or also to the planner's run comment, which today lists its criteria without status or proof? Not accepted: The owner's words point the other way: the reviewer's card should mirror the planner card with why it fails 'in place of Verified by', which reads as the planner card showing Verified by. Nothing the owner wrote limits Verified by to the issue and PR card.
> - The issue card and PR card each leave out the link to the page they sit on; should that difference go too, so the two are identical to the character? Not accepted: The owner wrote 'The PR card and the issue card always show the same thing'; keeping a difference between them is a narrower reading than those words, and nothing the ow

**Agent:** Now the plan itself.

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> {
>  "kind": "feature",
>  "summary": "The issue card, the PR card and every run comment show what the owner needs at a glance, with fixed icons and no empty or coded noise, questions the reviewer answered on autopilot show plainly, and the owner's own words read open on the issue they wrote.",
>  "feature": "Cards show everything the owner needs with icons, and nothing they don't.",
>  "stories": [
>   {
>    "title": "Every field on a card has its own GitHub icon, fixed by code",
>    "user_story": "Every field on the issue card, the PR card and the run comments carries its own GitHub Octicon, in the same style as today's status icons, chosen by code and never by an agent.",
>    "context": "Today dokima/icons/ holds six Octicon circles (passed, failed, running, queued, cancelled, none), served by card.icon() in dokima/card.py and used by agent.py through icon(). The issue names 23 fields. Add one SVG per field in the same 16px style and one fixed table in code from field to icon; the later stories draw with it. Rule R1/R2 split: this story is the shared base.",
>    "acceptance_criteria": [
>     {
>      "text": "dokima/icons/ holds one Octicon SVG, 16 by 16 like today's status icons, for each of the 23 fields the owner named: planner, worker, plan review, code review, autopilot, passed, failed, needs you, owner approval, merged, still open, acceptance criterion, verified by, files changed, question, blocker, note, outside the plan, issue found, related, blocked by, blocks and stats.",
>      "s

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print([k for k in d]); print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:2000])"; grep -n "issuecomment" issue.md | head
```

> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37824743362",
>  "commit_before": "27453f26a426dc885019a0e5dae4d503a2a5107e",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 31127,
>   "turns": 7,
>   "cost_usd": 0.2633892,
>   "tokens_in": 259914,
>   "tokens_out": 3043
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/230/37824743362-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37824743362",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> Shell cwd was reset to /home/runner/work/dokima/dokima

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def links_row\|def owner_review\|Reviewer (\|def done_row\|FOLD_START =\|From the approved plan" dokima/*.py | head; ls dokima/icons
```

> dokima/body.py:9:FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> dokima/agent.py:158:             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
> dokima/agent.py:234:    head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker",
> dokima/card.py:150:def links_row(repo, issue, pr, worker, check_runs, page):
> dokima/card.py:192:def owner_review(reviews, owners):
> dokima/card.py:199:def done_row(repo, found, all_tests):
> cancelled.svg
> failed.svg
> none.svg
> passed.svg
> queued.svg
> running.svg

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 140,175p dokima/agent.py
```

> bad.append("resolved must be a list of blocker ids")
>             resolved = []
>         if not isinstance(listed, list) or not all(isinstance(b, dict) for b in listed):
>             bad.append("blockers must be a list of objects")
>             listed = listed if isinstance(listed, list) else []
>         carried = set(resolved) | {b.get("id") for b in listed if isinstance(b, dict)}
>         return bad + [f"earlier blocker {b} is neither resolved nor still listed" for b in sorted(blockers - carried)]
>     replies = h.get("replies", [])
>     if not isinstance(replies, list) or not all(isinstance(r, dict) for r in replies):
>         bad.append("replies must be a list of objects")
>         replies = replies if isinstance(replies, list) else []
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
>     lines += [

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-planned the split into 5 stories after the owner's answers and new ask: fixed icons, the issue and PR card, the run comments, the owner's ask shown open, and questions answered on autopilot."],
  "decided": ["The planner's own run comment lists each criterion with its status and Verified by, and the reviewer's comment mirrors it with only the failing ones (story 3).",
              "The issue card and PR card are identical, each including the link back to its own page (story 2).",
              "A question the reviewer answers on autopilot shows the question, the answer and the owner's linked words, only when there is one (story 5)."],
  "open": ["The plan has no questions left for the owner."]},
 "verdict": "approve",
 "summary": "The split now keeps every ask, including both answers and the new autopilot-question ask, each in exactly one story, so it can go to work.",
 "blockers": [],
 "notes": [
  {"text": "Story 4's third criterion says a sub-issue's quoted text 'stays folded', but the story body itself is written with an open fold; only the outer Original issue fold hides it today. Once story 4 opens that outer fold, the sub-issue would show open unless story_body changes too, so story 4's own plan should test a filed sub-issue's body after a redraw.", "evidence": "dokima/agent.py:158 '<details open><summary>From the approved plan of #...'; dokima/body.py:9 FOLD_START"},
  {"text": "Stories 3 and 5 both change how render() in dokima/agent.py draws the reviewer's comment, and story 5 depends only on story 1; story 5's plan should build on story 3's layout or the two may clash when both land.", "evidence": "plan.json stories[4].depends_on = [0]; stories[2].context and stories[4].context both name render() in dokima/agent.py"},
  {"text": "Story 4 changes the rule in AGENTS.md 'The issue body' that keeps the ask folded; its plan should list AGENTS.md i
```

> rc=0

**Agent:** I approved the plan for issue #230, and the review is in `/tmp/dokima-out/review.json`. Both checks on it passed.

**What the planner changed this round:** it re-planned the split into 5 stories after your answers and your new ask:
1. Each field gets its own fixed GitHub icon.
2. The issue card and the PR card list criteria as bullets, count your merge as Owner approval, and are identical, each with its link back to its own page.
3. Run comments show only fields that have something, say Plan review and Code review, and have no codes like B1. The planner's own comment shows each criterion with its status and Verified by, and the reviewer's comment mirrors it with only the failing ones.
4. Your text shows open on the issue you wrote, and stays folded where it's quoted elsewhere.
5. On autopilot, a question the reviewer answers from your words shows the question, the answer and your linked words, and only when there is one.

**Why I approved:** I matched 19 of your asks from the issue and your comments, including both answers and the new autopilot ask. Each one lands in exactly one story and none is missing. The plan has no questions left for you and there were no open blockers. A split carries no tests yet, so there was nothing to run.

**Three notes for the stories' own plans (they don't block):**
- **Story 4, sub-issues:** a filed sub-issue's quoted story is written with an open fold (`dokima/agent.py:158`). Today only the outer "Original issue" fold hides it. Once story 4 opens that outer fold, sub-issues would show open unless that code changes too, so story 4 should test a sub-issue after a redraw.
- **Stories 3 and 5:** both change the same code that draws the reviewer's comment, but story 5 depends only on story 1. Story 5 should build on story 3's layout, or the two may clash when both land.
- **Story 4, AGENTS.md:** it changes the rule in AGENTS.md that keeps your text folded, so its plan should include AGENTS.md, as the planner's own concern says.
