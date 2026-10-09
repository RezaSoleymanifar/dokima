# reviewer (plan) for #330

Run: https://github.com/dokima-dev/dokima/actions/runs/37893260985

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #330: Cards and the board always show what is true right now
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #330](https://github.com/dokima-dev/dokima/issues/330)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Cards and the board go stale tonight because each update trusts the one event that started it. When an event is dropped, late or out of order, the card or board stays wrong for good: #312's PR card (a dropped redraw), #246's PR card (written only while the PR is open, and the merge came first), #231 stuck in Work (its "closed" update dropped), and abo

`2. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "S<\|r'S\|\"S\"\|S(\\\\d\|missing" dokima/agent.py | head -30; ls /tmp/pack/in; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(d.keys())"
```

> 147:    """A plan record's links as three lists of issue numbers, empty when missing."""
> 166:        return ["open_issues.json is missing from the pack, so the links cannot be checked"]
> 267:        handback = {"missing": f"{HANDBACK[role]}: {e}"}
> 731:    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
> 735:                "\"source\": \"a link to where they said it\", \"criterion\": \"N.k\" or \"missing\"}"]
> 740:        if c != "missing" and c not in ids:
> 743:    gone = [a["ask"] for a in good if a["criterion"].strip() == "missing"]
> 745:        bad.append("an approve keeps every ask, but these are marked missing: " + "; ".join(f'"{g}"' for g in gone))
> 838:        missing = [k for k in keys if not filled(x.get(k))]
> 839:        if missing:
> 840:            bad.append(f"{label} needs {', '.join(missing)}")
> 845:    """Everything missing, wrongly typed or wrongly shaped in a hand-back against its prompt's shape, each naming the field."""
> 889:    """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
> 925:        return None, f"{name} is missing ({path})"
> 986:    """Everything missing or broken in an agent's starting pack, checked by code before the agent starts."""
> 994:            bad.append(f"{name} is missing")
> 01-planner.json
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 885,910p dokima/agent.py; grep -n "concurrency" -A3 .github/workflows/board.yml .github/workflows/card.yml; grep -n "^on:" -A25 .github/workflows/card.yml | head -40
```

> return bad
> 
> 
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
>     tests = plan.get("tests") if isinstance(plan.get("tests"), dict) else {}
>     for b in h.get("blockers") if isinstance(h.get("blockers"), list) else []:
>         if not isinstance(b, dict) or not filled(b.get("criterion")):
> .gith

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposed splitting #330 into three stories: the board's column and pills from state, the issue and PR cards from state, and a scan that names any card not matching its state."],
  "decided": ["The board and the cards keep their own workflows, each with one queue per issue that keeps the newest run.", "The scan lands after the other two stories, and the owner's check of #246 and #312 on the live board is manual."],
  "open": ["Each story writes its own tests when it is planned."]},
 "verdict": "approve",
 "summary": "The split keeps every ask of #330, each in exactly one story, and follows the split rules; each story's tests come when it is planned.",
 "blockers": [],
 "notes": [
  {"text": "Story 3's scan also names 'every stale card', which the owner's test does not spell out; its plan should say exactly what stale means (a card body that differs from what the state draws) so the test can break on it.", "evidence": "plan.json stories[2].acceptance_criteria[0]; the issue's Test line names closed cards outside Done or with a pill, open cards in the wrong column, and the PR cards of #246 and #312."},
  {"text": "Story 1's shared queue for an issue and its PR needs the PR's issue number in the concurrency group, which GitHub's event for a PR does not carry directly (today it is the PR number); its plan should say how the group is keyed and test it.", "evidence": ".github/workflows/board.yml:28 group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}; .github/workflows/card.yml:18 group: card."},
  {"text": "The owner says #330 replaces #315, #322 and #329; per AGENTS.md those should be closed as duplicates of #330, which is an owner or process step, not a criterion.", "evidence": "Issue #330 last line: 'This replaces #315, #322 and #329.'; AGENTS.md, Changing scope: 'Merging or replacing closes the old issue as a dupli
```

> 0

**Agent:** I approved the planner's split of #330. The review is in `/tmp/dokima-out/review.json`, and both checks on it passed.

**The split:** three stories.
1. The board's column and pills are worked out from each issue's state right now, on every event and every 15 minutes.
2. The issue and PR cards are worked out the same way, and a merged PR's card shows Merged.
3. A scan names every card that doesn't match its state. It lands after the other two, and you check #246 and #312 on the live board by hand.

**Why it passes:** every ask in the issue is kept by exactly one criterion; I listed 12 of them, from S1.1 to S3.2. It follows the split rules: three children, one level, no loops in the dependencies. It's split because the issue has 12 criteria across the board and card code. The plan asks no questions, so there were no assumptions to judge. No story has tests yet; each story writes its own when it is planned.

**Three notes, none blocking:**
- **"Stale" is undefined.** Story 3's scan also names "every stale card", which your test doesn't spell out. Its plan should say exactly what stale means so a test can catch it.
- **The shared queue needs work in the workflow.** Story 1 promises that an issue and its PR share one board queue. Today `board.yml:28` keys the queue on the PR's own number, and GitHub's PR event doesn't carry the issue's number directly. Its plan should say how the queue gets keyed by issue, and test it.
- **The issues this replaces still need closing.** You said #330 replaces #315, #322 and #329, and AGENTS.md says those should be closed as duplicates of #330. No criterion covers that; it's a step for you or the process to take.
