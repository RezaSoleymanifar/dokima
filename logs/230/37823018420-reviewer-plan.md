# reviewer (plan) for #230

Run: https://github.com/dokima-dev/dokima/actions/runs/37823018420

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json 2>/dev/null
```

> .:
> total 48
> drwxr-xr-x  3 runner runner  4096 Oct  8 18:18 .
> drwxrwxrwt 18 root   root    4096 Oct  8 18:18 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 18:18 in
> -rw-r--r--  1 runner runner 17466 Oct  8 18:18 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 18:18 open_blockers.json
> -rw-r--r--  1 runner runner  9946 Oct  8 18:18 plan.json
> 
> in:
> total 20
> drwxr-xr-x 2 runner runner  4096 Oct  8 18:18 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 18:18 ..
> -rw-r--r-- 1 runner runner 10647 Oct  8 18:18 01-planner.json
> # Issue #230: Cards show everything I need with icons, and nothing I don't
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
> The cards bury what matters in the folded JSON and show noise up front. I want one card that tells me everything at a glance.
> 
> What I want:
> - Icons everywhere, GitHub's official octicons in the same style as the current status icons, hard-wired 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;p=json.load(open('/tmp/pack/plan.json'));r=json.load(open('/tmp/pack/in/01-planner.json'));print(p==r.get('handback'), list(r.keys()))"; grep -n "Reviewer (\|def criterion_row\|def circle\|owner_review\|def links_row\|html_url" dokima/card.py dokima/agent.py | head -40; grep -n "FOLD_START\|FOLD_END" dokima/*.py | head; ls dokima/icons
```

> True ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> dokima/card.py:53:def circle(repo, st, url=None):
> dokima/card.py:150:def links_row(repo, issue, pr, worker, check_runs, page):
> dokima/card.py:154:        links.append(f"[latest run]({worker['html_url']})")
> dokima/card.py:164:def criterion_row(repo, text, check, tests):
> dokima/card.py:172:    return f"<tr><td>{circle(repo, st, check and check['html_url'])}</td><td>{words}</td></tr>"
> dokima/card.py:192:def owner_review(reviews, owners):
> dokima/card.py:203:    approval = owner_review(found["reviews"], found["owners"])
> dokima/card.py:206:            f"{circle(repo, state(all_tests), all_tests and all_tests['html_url'])} All tests · "
> dokima/card.py:208:            f"{circle(repo, approval_st, approval and approval.get('html_url'))} Owner approval")
> dokima/card.py:293:    return {"status": run["status"], "conclusion": run["conclusion"], "html_url": run["html_url"]} if run else None
> dokima/card.py:374:        return {"name": name, "status": status, "conclusion": conclusion, "html_url": f"https://github.com/{repo}/actions/runs/2"}
> dokima/card.py:393:    done = {"status": "completed", "conclusion": "success", "html_url": f"https://github.com/{repo}/actions/runs/1"}
> dokima/agent.py:234:    head = {"planner": "Planner", "reviewer": f"Reviewer ({stage})", "worker": "Worker",
> dokima/body.py:9:FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
> dokima/body.py:

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "acceptance_criteria\|Verified by\|def render\|def details\|def footnote" dokima/agent.py | head -30
```

> 163:    lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
> 327:def details(rec):
> 398:def render(rec, pr=None):
> 431:        criteria = [c.get("text", "") if isinstance(c, dict) else c for c in h.get("acceptance_criteria") or []]
> 518:def footnote(rec):
> 798:    count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
> 1332:    return [[c.get("text") if isinstance(c, dict) else c for c in plan.get(k) or []] for k in ("acceptance_criteria", "non_functional")]

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner split the issue into 4 stories: fixed icons for every field, the issue and PR card, the run comments, and the owner's ask shown open."],
  "decided": ["Stories 2 and 3 build on the icon table from story 1; story 4 stands alone.", "The owner's merge counts as Owner approval, and the issue and PR card are drawn to match."],
  "open": ["Whether the planner's own run comment also lists criteria with Verified by.", "Whether the issue and PR card must match to the character, including the link to the page they sit on."]
 },
 "verdict": "approve",
 "summary": "The split gives every ask in the issue and the later comment to exactly one story, with no ask dropped or added; its two questions are real readings for the owner to settle.",
 "blockers": [],
 "notes": [
  {"text": "Story 3's third criterion depends on the first question: the owner wrote that the reviewer's card mirrors the planner card with why it fails 'in place of Verified by', which suggests the planner's run comment shows Verified by too. Story 3's own plan should follow the owner's answer.", "evidence": "Issue #230 body; dokima/agent.py:431 lists the planner's criteria as plain text with no Verified by."},
  {"text": "Story 4 changes the rule in AGENTS.md, 'The issue body', that keeps the ask folded; its plan should list AGENTS.md in scope, as the concern says.", "evidence": "dokima/body.py:9 FOLD_START; AGENTS.md 'The issue body'"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Icons everywhere, GitHub's official octicons in the same style as the current status icons", "source": "https://github.com/dokima-dev/dokima/issues/230", "criterion": "S1.1"},
  {"ask": "hard-wired in code to each field so agents never pick or skip them", "source": "https://github.com/dokima-dev/dokima/issues/230", "criterion": "S1.3"},
  {"ask": "planner, worker, plan review, code revie
```

> rc=0

**Agent:** I've approved the planner's split of issue #230. Neither of its two questions can go ahead on autopilot without you. Both checks on the hand-back pass. The review is in `/tmp/dokima-out/review.json`.

**What the planner proposed:** four stories.
1. Every field gets its own fixed GitHub icon, set by code.
2. The issue and PR cards list criteria as bullets, count your merge as Owner approval, and always match.
3. Run comments show only fields that have something, say "Plan review" and "Code review", show no codes like B1 or 212.3, and fold the stats.
4. Your original text shows open on the issue you wrote, folded only where it's quoted elsewhere.

**Your asks:** I went through the issue and your later comment and found 15 asks. Each one belongs to exactly one story, nothing is missing, and nothing was added beyond what you wrote. No story has more than five criteria. I checked the facts the planner relied on against the code and they hold: the reviewer heading, the icon link, how Owner approval is read, the "Original issue" fold, and the six existing icons.

**Its questions:** I accepted neither assumption. Neither changes how the system works or what it costs, but neither matches your words:
- **Verified by on the issue and PR card only:** You wrote that the reviewer's card shows why a criterion fails "in place of Verified by". That suggests the planner's run comment shows Verified by too, which is the opposite of what the planner assumed.
- **Leaving out the link to the page each card sits on:** That keeps a difference between the two cards, and you wrote that they "always show the same thing".

**Notes for the stories' own plans:**
- Story 3's mirrored-criteria part depends on your answer to the first question.
- Story 4 must also update the line in AGENTS.md that says your text is kept folded.

**Next:** you answer the two questions with `/plan` and your words, or say `/work` to go ahead with the split as planned.
