# reviewer (plan) for #368

Run: https://github.com/dokima-dev/dokima/actions/runs/38073784611

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (29.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4ef4dfad-dfef-404c-bf08-c8da411f4858/tool-results/b28ibyxho.txt
> 
> Preview (first 2KB):
> .:
> total 52
> drwxr-xr-x  3 runner runner  4096 Oct 10 17:57 .
> drwxrwxrwt 18 root   root    4096 Oct 10 17:57 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 17:57 in
> -rw-r--r--  1 runner runner 18547 Oct 10 17:57 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 17:57 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 17:57 parent.json
> -rw-r--r--  1 runner runner 11058 Oct 10 17:57 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner  4096 Oct 10 17:57 .
> drwxr-xr-x 3 runner runner  4096 Oct 10 17:57 ..
> -rw-r--r-- 1 runner runner 11233 Oct 10 17:57 01-planner.json
> -rw-r--r-- 1 runner runner  3758 Oct 10 17:57 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11744 Oct 10 17:57 03-planner.json
> # Issue #368: Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 380 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Dokima tracks each run's GitHub API budget, warns once before it runs out, uses REST where it can, and retries updates an outage stopped.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/368
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Whe

`2. Bash`
```
cd /tmp/pack; cat issue.md; cat parent.json
```

> # Issue #368: Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 380 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Dokima tracks each run's GitHub API budget, warns once before it runs out, uses REST where it can, and retries updates an outage stopped.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/368
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Where runs record:** Card, board, autopilot, command and uptodate runs post no record comment today. Where should they keep their budget numbers? The plan assumes each run writes them to its own log and to a small file kept with the run (a run artifact), which story 2 reads back to name the heaviest workflows; agent runs also show them in their record. · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Floor and place:** What is the safe floor, and where does the one warning go? The plan assumes 1,000 of 5,000 points (20%) for each budget, and one open issue titled 'GitHub API budget low' that gets one comment per hour the floor is crossed, mentioning the owner. · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="a

`3. Bash`
```
cd /tmp/pack; python3 -m json.tool plan.json; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:4000])"; cat in/02-reviewer-plan.json | head -c 2500
```

> {
>     "kind": "feature",
>     "summary": "Dokima tracks each run's GitHub API budget, warns once before it runs out, uses REST where it can, and retries updates an outage stopped.",
>     "feature": "Running out of GitHub's hourly API budget never comes as a surprise again: every run shows what it cost, the repo gets one warning before the budget runs out, the load is split between the GraphQL and REST budgets, and cards an outage left behind are put right once the budget is back. Split by R1 (four independent goals) and R3 (they touch every workflow, the board code, the agent code and the reads in plan.py). Stories: (1) every run records its budget; (2) a low budget is announced once, naming the heaviest workflows, depends on (1); (3) reads move from GraphQL to REST where they can; (4) board and card updates the budget stopped are retried once it is back.",
>     "stories": [
>         {
>             "title": "Every Dokima run records the GitHub API budget left before and after it",
>             "user_story": "The owner can see what each Dokima run cost in GitHub's hourly API budget, GraphQL and REST, so the heaviest workflows are known.",
>             "context": "Each run reaches GitHub through gh in several places: dokima/agent.py (about 60 calls), dokima/card.py, dokima/board.py (its own graphql() and rest() helpers at lines 30 to 41), dokima/plan.py (two GraphQL queries at lines 169 and 186), dokima/planner.py, dokima/body.py and dokima/audit.py, plus about 90 gh calls straight fr

`4. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows/; for f in .github/workflows/*.yml; do echo "== $f: $(grep -cE '\bgh |dokima\.' $f) token: $(grep -oE 'GITHUB_TOKEN|create-github-app-token|app-id|APP_ID' $f | sort -u | tr '\n' ' ')"; done; python3 -c "import json;print(json.load(open('/tmp/pack/plan.json')).get('raises'))"
```

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
> == .github/workflows/agent.yml: 47 token: APP_ID app-id create-github-app-token 
> == .github/workflows/assign.yml: 1 token: 
> == .github/workflows/audit.yml: 1 token: APP_ID app-id create-github-app-token 
> == .github/workflows/autopilot.yml: 2 token: APP_ID app-id create-github-app-token 
> == .github/workflows/board.yml: 2 token: APP_ID app-id create-github-app-token 
> == .github/workflows/card.yml: 1 token: APP_ID app-id create-github-app-token 
> == .github/workflows/commands.yml: 19 token: APP_ID app-id create-github-app-token 
> == .github/workflows/done-whens.yml: 2 token: 
> == .github/workflows/full-suite.yml: 0 token: 
> == .github/workflows/planner.yml: 6 token: APP_ID app-id create-github-app-token 
> == .github/workflows/reviews.yml: 0 token: 
> == .github/workflows/uptodate.yml: 1 token: APP_ID app-id create-github-app-token 
> == .github/workflows/wiki.yml: 0 token: 
> == .github/workflows/worker.yml: 6 token: APP_ID app-id create-github-app-token 
> None

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -nE 'uses:|curl|api' .github/workflows/full-suite.yml .github/workflows/reviews.yml .github/workflows/wiki.yml; grep -n 'token' .github/workflows/assign.yml .github/workflows/done-whens.yml
```

> .github/workflows/full-suite.yml:17:      - uses: actions/checkout@v5
> .github/workflows/full-suite.yml:21:      - uses: actions/setup-python@v6
> .github/workflows/wiki.yml:13:      - uses: actions/checkout@v4
> .github/workflows/done-whens.yml:22:          GH_TOKEN: ${{ github.token }}
> .github/workflows/assign.yml:17:          GH_TOKEN: ${{ github.token }}

**Agent:** I checked the plan against the workflow files, and they match. Next I'm writing the review that approves the plan.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Kept the four-story split and wrote the owner's answers of 2026-10-10 into stories 1 and 2: numbers go to each run's log and a run file, agent runs also show them in their record; the floor is 1,000 of 5,000 for each budget, warned on one open issue \"GitHub API budget low\" at most once an hour, mentioning the owner.",
          "Widened story 1's second criterion to name every Dokima workflow that calls GitHub's API, including assign.yml, audit.yml and done-whens.yml."],
  "decided": ["assign.yml and done-whens.yml record the repo token's own budget, labelled as such; full-suite.yml, reviews.yml and wiki.yml spend no API budget and record nothing."],
  "open": ["The plan has no open questions."]},
 "verdict": "approve",
 "summary": "The split now carries every ask, including the owner's answers on where numbers go and on the floor, and story 1 names every workflow that spends the budget.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Every Dokima run records the GraphQL and REST budget left before and after it, in its record, so the cost of each workflow (card redraws, board, autopilot, agents) is known.", "source": "https://github.com/dokima-dev/dokima/issues/368", "criterion": "S1.2"},
  {"ask": "we want to track numbers for sure", "source": "https://github.com/dokima-dev/dokima/issues/368", "criterion": "S1.1"},
  {"ask": "each run writes its budget numbers to its own log and a small file kept with the run, agent runs also show them in their record", "source": "https://github.com/dokima-dev/dokima/issues/368", "criterion": "S1.2"},
  {"ask": "When the budget left drops below a safe floor, Dokima says so once on the repo (not on every issue), naming which workflows used the most this hour.", "source": "https://github.com/dokima-dev/dokima/issues/368", "criterion": "S2.1"},
  {"ask": "the floor is 1,000 of 5,000 (20%) for each budget, with one open issue \"G
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> rc=0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The split now carries every ask, including the owner's answers on where numbers go and the floor, and covers every workflow that spends the budget."
d['summary']="The split carries every ask, the owner's answers on the numbers' place and the floor, and every workflow that spends the budget."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 368 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the revised plan for [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking Dokima's GitHub API budget), and nothing is raised. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **Last round's blocker is fixed.** Story 1's second criterion now names every workflow that uses GitHub's API, including `assign.yml`, `audit.yml` and `done-whens.yml`, which the plan had missed before. I checked the plan's list against `.github/workflows/` and it matches. Nine workflows use the Dokima app's key. `assign.yml` and `done-whens.yml` use the repo's own token, so they record that token's budget. `full-suite.yml`, `reviews.yml` and `wiki.yml` don't call the API, so they record nothing.
- **Your answers of 2026-10-10 are in the plan.** Each run writes its numbers to its log and to a small file kept with the run, and agent runs also show them in their record. The floor is 1,000 of 5,000 for each budget. The warning goes on one open issue, "GitHub API budget low", at most once an hour, mentioning you.
- **Every ask maps to a criterion.** Each ask in the issue and your two comments is matched to one criterion, and none is missing. The two questions from the earlier plan are settled, and the new plan raises no new ones.

The plan's split proposes no new test files yet, so there was nothing to run.

One small inaccuracy: the asks taken from your comments link to the issue itself rather than to the comment, because I didn't have the comments' own links.
