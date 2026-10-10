# reviewer (plan) for #368

Run: https://github.com/dokima-dev/dokima/actions/runs/38069136790

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #368: Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/368
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Dokima tracks how much of GitHub's hourly API budget it uses, so running out never comes as a surprise.
> 
> Owner's words (2026-10-09): "we want to track numbers for sure"
> 
> What happened: at about 22:10Z on 2026-10-09 the Dokima app's GraphQL budget (5,000 points an hour, shared by every Dokima workflow and the operator's own scripts) hit zero. Until it reset at 22:29Z, commands, cards and the board could not run: an owner's /plan on #299 never started and a board run failed. The REST budget was still about 4,000 of 5,000 at the time.
> 
> - Every Dokima run records the GraphQL and REST budget left before and after it, in its record, so the cost of each workflow (card redraws, board, autopilot, agents) is known.
> - When the budget left drops below a safe floor, Dokima says so once on the repo (not on every issue), naming which workflows used the most this hour.
> - Reads that can use REST instead of GraphQL do, so the two budgets share the load.
> 
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="no

`2. Bash`
```
cd /tmp/pack; cat parent.json | head -50; python3 -c "import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:2000])"; cd /home/runner/work/dokima/dokima; grep -n "def footnote" -A5 dokima/agent.py | head; ls .github/workflows
```

> {"number": null}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38068955202",
>  "commit_before": "f7340dbe974171be90d445f0412eae96bd53f258",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 125545,
>   "turns": 14,
>   "cost_usd": 0.7515285999999999,
>   "tokens_in": 658991,
>   "tokens_out": 10046
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/368/38068955202-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38068955202",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> 795:def footnote(rec):
> 796-    """One line under every card: model, time, turns, tokens and cost, and the link to the full conversation."""
> 797-    r = rec.get("report") or {}
> 798-    stats = field_icon(os.environ.get("GITHUB_REPOSITORY", ""), "stats")
> 799-    if rec.get("role") == "split":
> 800-        return f"<sub>{stats} Filed by code, no model · [run]({rec.get('run', '')})</sub>"
> agent.yml
> assign.yml
> audit.yml
> autopilot.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> reviews.yml
> uptodate.yml
> wiki.yml
> worker.yml

`3. Bash`
```
cd /home/runner/work/dokima/dokima/.github/workflows; for f in *.yml; do echo "$f $(grep -c 'gh \|github.rest\|graphql\|dokima\.' $f) $(grep -m1 '^name' $f)"; done
```

> agent.yml 49 name: agent
> assign.yml 1 name: assign
> audit.yml 1 name: audit
> autopilot.yml 2 name: autopilot
> board.yml 4 name: board
> card.yml 1 name: card
> commands.yml 20 name: commands
> done-whens.yml 2 name: done-whens
> full-suite.yml 0 name: full suite
> planner.yml 6 name: planner
> reviews.yml 0 name: reviews
> uptodate.yml 1 name: uptodate
> wiki.yml 0 name: wiki
> worker.yml 6 name: worker

`4. Bash`
```
cd /home/runner/work/dokima/dokima/.github/workflows; grep -n 'gh \|dokima\.' assign.yml audit.yml done-whens.yml full-suite.yml reviews.yml wiki.yml | head -30
```

> assign.yml:20:        run: gh issue edit "$ISSUE_NUMBER" -R "$REPO" --add-assignee "$(python3 -m dokima.plan approvers)"
> audit.yml:33:        run: python3 -m dokima.audit "$GITHUB_REPOSITORY"
> done-whens.yml:23:        run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
> done-whens.yml:61:        run: python3 -m dokima.checks annotate pr/r.xml

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Split the issue into four stories: every run records its budget; a low budget warns once on the repo; reads move to REST where they can; updates the budget stopped are retried once it is back."],
  "decided": ["Story 2 depends on story 1; stories 1, 3 and 4 wait on nothing.", "Reads REST cannot answer, such as some board reads, stay on GraphQL and are listed with why."],
  "open": ["Asks the owner where runs without a record comment keep their numbers (assumes the run log and a run artifact).", "Asks the owner for the floor and the place of the warning (assumes 1,000 of 5,000 for each budget, one open issue with one comment per hour)."]},
 "verdict": "block",
 "summary": "The split covers every ask, but story 1 promises budget numbers only for some of Dokima's workflows, while the owner asked for every run.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "S1.2",
   "text": "The owner asked that every Dokima run record its budget. Story 1 covers agent runs (S1.1) and card, board, autopilot, command and uptodate runs (S1.2), but leaves out other Dokima workflows that spend the budget: assign.yml (gh issue edit, a GraphQL call), audit.yml (python3 -m dokima.audit) and done-whens.yml (python3 -m dokima.checks). A build that skips them passes S1.2 while their cost stays unknown. Smallest fix: S1.2 says every Dokima workflow run not covered by S1.1, and the story's context names the full list of workflows in .github/workflows/.",
   "evidence": "Issue #368: 'Every Dokima run records the GraphQL and REST budget left before and after it'. .github/workflows/assign.yml line 20 runs gh issue edit; audit.yml line 33 runs python3 -m dokima.audit; done-whens.yml lines 23 and 61 run python3 -m dokima.checks. None are named in S1.1 or S1.2."}
 ],
 "answers": [],
 "asks": [
  {"ask": "Every Dokima run records the GraphQL and REST budget left before and after it, in its r
```

> (Bash completed with no output)

**Agent:** I've blocked the plan for [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking GitHub's hourly API budget) and sent it back to the planner. The review file is in `/tmp/dokima-out/review.json` and passes both checks.

**The plan:** the planner split the issue into four stories:
1. Every run records how much of both budgets (GraphQL and REST) was left before and after it.
2. When the budget runs low, one warning goes on the repo naming the workflows that used the most this hour. This story depends on story 1.
3. Reads move from GraphQL to REST wherever REST can answer them.
4. Board and card updates that failed because the budget ran out are retried once it resets.

Every ask in the issue and in your follow-up comment is kept by one of these stories.

**Why I blocked:** you asked that *every* Dokima run record its budget. Story 1 only covers agent runs and card, board, autopilot, command and uptodate runs. It leaves out other workflows that also call GitHub: `assign.yml` (line 20), `audit.yml` (line 33) and `done-whens.yml` (lines 23 and 61). Code that skipped them would still pass the plan, and their cost would stay unknown. The fix is to make that criterion cover every Dokima workflow run that the agent-run criterion doesn't already cover.

**Your two questions:** I left both for you to answer, even though the issue is on autopilot. Each one changes how the system works, and nothing you've written settles it:
- **Where runs without a record comment keep their numbers.** The plan assumes each run's log plus a small file saved with the run.
- **The safe floor and where the warning goes.** The plan assumes 1,000 of 5,000 for each budget, and one open issue that gets one comment per hour while the budget is below the floor.

So the river will stop for you on these whatever happens with the blocker.
