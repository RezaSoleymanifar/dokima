# reviewer (plan) for #265

Run: https://github.com/dokima-dev/dokima/actions/runs/37846694007

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (47.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9e7814de-737f-4f3c-9dfc-2b9359788843/tool-results/bi4tcdqd7.txt
> 
> Preview (first 2KB):
> # Issue #265: Issues the reviewer finds are filed automatically, parked and labeled filed by Dokima
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
> Today an issue the reviewer finds outside the one it reviews stays a proposal on its card, and a /issue command to file it is only planned. #222 shows the cost: Dokima found the no-PR bug, nobody filed it, and it sat unseen until it broke main.
> 
> What I want:
> - Every issue the reviewer finds is filed by code right away as its own issue, parked and labeled filed-by-dokima.
> - It says where it was found, with a link to the review that found it.
> - Nothing more: its links, size and plan are worked out when it is plann

`2. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> [
>  {
>   "id": "B1",
>   "criterion": "265.1",
>   "test": null,
>   "problem": "The owner asked that any agent, planner, worker and reviewer, can report an issue it finds outside its own, with the same field in their hand-back. The plan only files issues a plan review or code review finds (criterion 265.1).",
>   "evidence": "Owner's /plan comment on #265 (2026-10-08T21:08:55Z): \"Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.\" plan.json criterion 1 says \"Each issue a plan review or a code review finds\"; no criterion or test covers the planner or worker.",
>   "fix": "Add a criterion that the planner's and the worker's hand-backs take the same found-issues field as the reviewer's and that each is filed the same way, with a test per role.",
>   "fixer": "planner"
>  },
>  {
>   "id": "B2",
>   "criterion": "265.6",
>   "test": null,
>   "problem": "The owner asked for no new component: the checker that already runs at the end of every agent's turn files the found issues, only after the hand-back passes. The plan does not promise where filing happens beyond the review's run, and its rejected-hand-back test covers only reviews.",
>   "evidence": "Owner's comment: \"No new component. The checker that already runs at the end of every agent's turn does it: it checks the hand-back, and only if it passes, it files the found issues. A rejected hand-back files nothing.\" plan.js

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; awk '/^### RezaSoleymanifar/{p=1} /^### dokima-runtime/{p=0} p' issue.md
```

> 27:### RezaSoleymanifar on issue #265 (2026-10-08T21:05:36Z)
> 31:### dokima-runtime on issue #265 (2026-10-08T21:05:58Z)
> 35:### dokima-runtime on issue #265 (2026-10-08T21:06:00Z)
> 40:### dokima-runtime on issue #265 (2026-10-08T21:06:13Z)
> 212:### RezaSoleymanifar on issue #265 (2026-10-08T21:08:31Z)
> 218:### dokima-runtime on issue #265 (2026-10-08T21:08:52Z)
> 228:### RezaSoleymanifar on issue #265 (2026-10-08T21:08:55Z)
> 234:### dokima-runtime on issue #265 (2026-10-08T21:09:14Z)
> 244:### dokima-runtime on issue #265 (2026-10-08T21:20:32Z)
> 417:### dokima-runtime on issue #265 (2026-10-08T21:22:26Z)
> 558:### dokima-runtime on issue #265 (2026-10-08T21:25:36Z)
> ### RezaSoleymanifar on issue #265 (2026-10-08T21:05:36Z)
> 
> /autopilot start
> 
> ### RezaSoleymanifar on issue #265 (2026-10-08T21:08:31Z)
> 
> /plan Two more:
> - Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.
> - No new component. The checker that already runs at the end of every agent's turn does it: it checks the hand-back, and only if it passes, it files the found issues. A rejected hand-back files nothing. The planner's links (blocked by, blocks, relates to) are written the same way, by that same checker.
> 
> ### RezaSoleymanifar on issue #265 (2026-10-08T21:08:55Z)
> 
> /plan Two more:
> - Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.
> - No new component. The checker that already runs 

`4. Bash`
```
cd /tmp/pack; sed -n 212,260p issue.md; sed -n 417,440p issue.md; sed -n 558,640p issue.md
```

> ### RezaSoleymanifar on issue #265 (2026-10-08T21:08:31Z)
> 
> /plan Two more:
> - Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.
> - No new component. The checker that already runs at the end of every agent's turn does it: it checks the hand-back, and only if it passes, it files the found issues. A rejected hand-back files nothing. The planner's links (blocked by, blocks, relates to) are written the same way, by that same checker.
> 
> ### dokima-runtime on issue #265 (2026-10-08T21:08:52Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> **Planner** · waiting for [this run](https://github.com/dokima-dev/dokima/actions/runs/37844344508)
> 
> Queued, and waiting for [this run](https://github.com/dokima-dev/dokima/actions/runs/37844344508) on the same issue to end; this run starts after it. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37844655193)</sub>
> 
> 
> ### RezaSoleymanifar on issue #265 (2026-10-08T21:08:55Z)
> 
> /plan Two more:
> - Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.
> - No new component. The checker that already runs at the end of every agent's turn does it: it checks the hand-back, and only if it passes, it files the 

`5. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(list(d.keys()));[print(k,json.dumps(d[k],indent=1)[:1500]) for k in d if k not in('handback',)]"; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d.get('handback',d),indent=1)[:5000])" | grep -A40 '"asks"'
```

> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> role "planner"
> stage null
> run_id "37846313917"
> commit_before "2780fa7b7ebd08a18cdb83d30aced508e4ca9760"
> started_by "dokima-runtime[bot]"
> models [
>  "claude-opus-5-5"
> ]
> report {
>  "duration_ms": 137758,
>  "turns": 14,
>  "cost_usd": 0.9878161999999999,
>  "tokens_in": 797754,
>  "tokens_out": 12452
> }
> log "https://github.com/dokima-dev/dokima/blob/logs/logs/265/37846313917-planner.md"
> run "https://github.com/dokima-dev/dokima/actions/runs/37846313917"
> check {
>  "passed": true,
>  "problems": []
> }
>  "asks": [
>   {
>    "ask": "Every issue the reviewer finds is filed by code right away as its own issue, parked and labeled filed-by-dokima.",
>    "source": "https://github.com/dokima-dev/dokima/issues/265",
>    "criterion": "265.1"
>   },
>   {
>    "ask": "It says where it was found, with a link to the review that found it.",
>    "source": "https://github.com/dokima-dev/dokima/issues/265",
>    "criterion": "265.2"
>   },
>   {
>    "ask": "Nothing more: its links, size and plan are worked out when it is planned.",
>    "source": "https://github.com/dokima-dev/dokima/issues/265",
>    "criterion": "265.3"
>   },
>   {
>    "ask": "The
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Checking the previous review's ask links and how the checker expects a split's asks, then I'll write the review.

`6. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/02-reviewer-plan.json'));print(json.dumps(d['handback']['asks'],indent=1))"; cd /home/runner/work/dokima/dokima; grep -n "S<\|asks\|split" dokima/agent.py | head -60
```

> [
>  {
>   "ask": "Every issue the reviewer finds is filed by code right away as its own issue, parked and labeled filed-by-dokima.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "265.1"
>  },
>  {
>   "ask": "It says where it was found, with a link to the review that found it.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "265.2"
>  },
>  {
>   "ask": "Nothing more: its links, size and plan are worked out when it is planned.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "265.3"
>  },
>  {
>   "ask": "The same finding is never filed twice.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "265.4"
>  },
>  {
>   "ask": "Any agent can report an issue it finds outside its own: planner, worker and reviewer, with the same field in their hand-back.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "missing"
>  },
>  {
>   "ask": "No new component. The checker that already runs at the end of every agent's turn does it: it checks the hand-back, and only if it passes, it files the found issues. A rejected hand-back files nothing.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "missing"
>  },
>  {
>   "ask": "The planner's links (blocked by, blocks, relates to) are written the same way, by that same checker.",
>   "source": "https://github.com/dokima-dev/dokima/issues/265",
>   "criterion": "missing"
>  }
> ]
> 169:def file_split(repo, parent, 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 795,815p dokima/agent.py; grep -n "split\|R1\|R2\|rule" dokima/planner.py | head -30
```

> def plan_criteria(plan, number):
>     """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
>     count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
>     if plan.get("kind") == "feature":
>         stories = plan.get("stories") if isinstance(plan.get("stories"), list) else []
>         return [f"S{s}.{k}" for s, st in enumerate(stories, 1) if isinstance(st, dict) for k in range(1, count(st) + 1)]
>     return [f"{number}.{k}" for k in range(1, count(plan) + 1)]
> 
> 
> def problems_plan(kind, h, plan, number):
>     """Everything in a hand-back that does not match the approved plan: a work line per criterion, exactly, and every
>     blocker on one of the plan's criteria, naming either no test or one of the plan's tests for that criterion."""
>     ids = plan_criteria(plan, number)
>     bad = []
>     if kind == "work":
>         crit = h.get("criteria")
>         if isinstance(crit, dict):
>             bad += [f"criteria has no line for {c}, a criterion of the plan" for c in ids if c not in crit]
>             bad += [f"criteria gives a line for {c}, which the plan does not have" for c in crit if c not in ids]
>         return bad
> 4:    python3 -m dokima.planner post N OUT    # write the plan into issue N, or post the proposed split
> 77:    """Garbled unless every story of a split is complete, its criteria cite this issue, and its dependencies point at
> 78:    the split's 

`8. Bash`
```
cd /tmp/pack; grep -o "issuecomment-[0-9]*" issue.md | sort -u | head; cd /home/runner/work/dokima/dokima; ls tests/test_filed_issues.py && git diff --stat main..HEAD; grep -n "/issue\b\|/issue\`" AGENTS.md dokima/roles/*.md | head
```

> tests/test_filed_issues.py
>  .github/workflows/full-suite.yml |   7 +-
>  tests/test_all_tests_judge.py    | 339 ---------------------------------
>  tests/test_checks.py             |   2 +-
>  tests/test_filed_issues.py       | 398 +++++++++++++++++++++++++++++++++++++++
>  tests/test_fixer.py              |  32 +---
>  tests/test_handback_check.py     |  79 ++------
>  6 files changed, 428 insertions(+), 429 deletions(-)
> AGENTS.md:66:- `/issue`: file the reviewer's proposed issues (planned).

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat $(git merge-base main HEAD)..HEAD; git log --oneline -3 main
```

> tests/test_filed_issues.py | 398 +++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 398 insertions(+)
> ab2dcaa The all tests check runs main's copy of its workflow, so a pull request can't rewrite its own judge (#263)
> 79e34d6 planner for #244 (run 37827165425) (#266)
> 772791d A finished worker always opens the pull request, even with nothing new to push (#259)

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner turned the plan into a split of two stories after the owner's added asks.",
   "Story 1: the planner, the worker and the reviewer each list found issues in the same hand-back field, and the code that already checks the hand-back files them, parked and labeled filed-by-dokima, only once the check passes.",
   "Story 2: the planner's blocked-by, blocks and relates-to links are written by that same end-of-turn code, only once the check passes; it waits on story 1."
  ],
  "decided": [
   "A finding counts as already filed when a Dokima-filed issue, open or closed, has the same title ignoring case and spacing; relates-to is written as a cross-reference seen on both issues."
  ],
  "open": [
   "Whether a later plan that drops a link removes the link written earlier is left to story 2's planner."
  ]
 },
 "verdict": "approve",
 "summary": "The split covers every ask, including the owner's later comment: any agent's found issues and the planner's links are written by the existing end-of-turn check, only after it passes.",
 "blockers": [],
 "notes": [
  {
   "text": "Story 1 holds seven criteria (five acceptance, two non-functional), above the five-criteria guide; its planner should keep each role's field and the filing in one tight plan, since the split rules allow only one level.",
   "evidence": "plan.json stories[0]: 5 acceptance_criteria and 2 non_functional, ids S1.1 to S1.7."
  },
  {
   "text": "Story 1 should also update AGENTS.md, whose Commands section still says `/issue` files the reviewer's proposed issues (planned), and reviewer.md, which says findings stay proposals until the owner files them.",
   "evidence": "AGENTS.md line 66; dokima/roles/reviewer.md lines 68-76 as cited in story 1's context."
  }
 ],
 "outside_plan": [],
 "resolved": ["B1", "B2", "B3"],
 "issues_found": [],
 "asks": [
  {"ask": "Every issue the reviewer finds is filed by 
```

> rc=0

**Agent:** I approved the plan for #265, and both hand-back checks passed. The review is in `/tmp/dokima-out/review.json`.

The planner answered the owner's later comment by splitting the issue into two stories:

- **Story 1:** the planner, the worker and the reviewer each list issues they find outside their own in the same field of their hand-back. The code that already checks the hand-back at the end of each turn files them, marked parked and filed-by-dokima, but only after the check passes, so a rejected hand-back files nothing. The same finding is never filed twice.
- **Story 2:** the planner's "blocked by", "blocks" and "relates to" links are written by that same end-of-turn check. This story waits on story 1.

**Earlier blockers:** all three from my last review are fixed.
- **B1:** the planner and worker now report found issues too (story 1, criterion 1).
- **B2:** no new component is added, and a rejected hand-back files nothing (story 1, criterion 6).
- **B3:** the planner's links are written by the same check (story 2).

**Owner's asks:** I matched each of the seven to a criterion, and none is missing. The plan asks the owner no questions.

**Choices the planner made itself:**
- A finding counts as already filed when an issue Dokima filed, open or closed, has the same title, ignoring letter case and spacing.
- "Relates to" is written as a cross-reference the owner sees on both issues, because GitHub has no built-in link of that kind.
- Whether a later plan that drops a link also removes it is left to story 2's planner.

**Notes for the story planners (not blockers):**
- Story 1 has seven criteria, above the guide of five, and it can't be split again, so its planner needs to keep it tight.
- Story 1 should also update `AGENTS.md`, which still lists `/issue` as a planned command for filing found issues. It should also update `dokima/roles/reviewer.md`, which says findings stay proposals until the owner files them.

The split has no tests of its own; each story writes its tests when it is planned. Story 1 plans to reuse the tests left on this branch in `tests/test_filed_issues.py`, which I haven't run this round.
