# reviewer (plan) for #425

Run: https://github.com/dokima-dev/dokima/actions/runs/38073763010

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
> # Issue #425: The card always shows what is true right now: one rule, one place
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [380, 416], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/425
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #380, #416
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The card must always show what is true right now. Today several places decide when to redraw it, at different moments, so it shows old information (#419: the review had passed, the card said running for 30 minutes).
> 
> One rule, one place: anything changes on an issue or its PR, the card is redrawn from scratch from what is on GitHub right now. No exceptions, no special timing. A run's start and its result are both changes.
> 
> Done when
> - One place redraws cards, and every change on an issue or PR reaches it, edits included.
> - One test, on real GitHub in a sandbox repo with stand-in agents (no tokens): an issue is played from start to merge, and after each step the card shows what just happened. It fails on today's code at the #419 moment.
> 
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print([k for k in d]);print(json.dumps({k:v for k,v in d.items() if k not in('handback','plan')},indent=1)[:3000])"; cat parent.json | head -50; cd /home/runner/work/dokima/dokima; git show --stat da897bc | tail -8; sed -n 25,45p .github/workflows/card.yml; grep -n "Say /work" dokima/card.py
```

> []['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38073532593",
>  "commit_before": "f7340dbe974171be90d445f0412eae96bd53f258",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 144563,
>   "turns": 19,
>   "cost_usd": 0.996743,
>   "tokens_in": 1069339,
>   "tokens_out": 14299
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/425/38073532593-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38073532593",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> {"number": null}    Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> 
>  AGENTS.md                  |  33 ++++-
>  dokima/roles/planner.md    |  35 ++++-
>  dokima/roles/reviewer.md   |  35 ++++-
>  dokima/roles/worker.md     |  35 ++++-
>  tests/test_raise_design.py | 310 +++++++++++++++++++++++++++++++++++++++++++++
>  5 files changed, 434 insertions(+), 14 deletions(-)
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   queue:
>     # The bot's own edits and comments (the card itself) don't trigger another card, and a comment on a pull
>     # request draws no issue card on it; an issue deleted or moved away has no card left to draw. A merge, even the
>     # bot's on autopilot, draws its pull request's card and its issue's; a pull request closed unmerged draws

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposed splitting #425 into four stories: a real-GitHub play-through, one redraw rule in card.yml, Work status once a build starts (#410), and checks re-running on plan approval (#422)."],
  "decided": ["The redraw story waits on the play-through story and must pass it on every step from new issue to merge.", "The play-through is pinned to commit f7340db as today's code for the #419 moment."],
  "open": ["The planner asks whether the play-through is its own hand-started workflow on dokima-dev/card-gallery, outside All tests."]},
 "verdict": "block",
 "summary": "Every ask has a story, but the redraw story promises the play-through passes every step while not waiting for the story that makes the card say Work once a build starts, so it can be built first and then cannot pass.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Test cannot pass",
   "text": "S2.4 promises the play-through passes every step from a new issue to a merged pull request on the code story 2 ships, and the play-through checks the card after /work, where it should show what just happened: a build started. That is story 3's fix (#410), yet story 2 depends only on story 1, so on autopilot story 2 can be built before story 3 and its own criterion fails at the /work step. Smallest fix: make story 2 depend on stories 1 and 3 (depends_on [0, 2]), and have S1.1 name the moment a build has started as one of the steps it checks, so the play-through also proves #410.",
   "evidence": "plan.json stories[1].depends_on is [0]; stories[2] context: dokima/card.py todo() returns 'Say /work to build the plan' (dokima/card.py line 26) until the worker's record, even while the worker runs."}
 ],
 "answers": [],
 "asks": [
  {"ask": "One place redraws cards, and every change on an issue or PR reaches it, edits included.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterio
```

> Exit code 1
> summary holds 41 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`4. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Every ask has a story, but the redraw story must pass the play-through without waiting for the story that makes the card say Work."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 425 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#425](https://github.com/dokima-dev/dokima/issues/425) (the card always shows what is true right now). The hand-back is in `/tmp/dokima-out/review.json`, and both checks on it pass.

**The plan:** the planner wants to split the issue into four stories:
1. A test on a real sandbox repo plays one issue from start to merge and checks the card after every step.
2. One workflow, `card.yml`, redraws the card on every change to an issue or its pull request.
3. Once a build has started, the card says Work and stops asking for `/work` (from [#410](https://github.com/dokima-dev/dokima/issues/410), the card kept asking for /work).
4. When a plan is approved, its pull request's checks run again by themselves (from [#422](https://github.com/dokima-dev/dokima/issues/422), re-running a PR's checks).

**Your asks:** I found nine in the issue and your comment. Every one is kept by a story, and none is missing.

**The blocker (for the planner):** story 2 cannot be sure of passing its own test.
- Story 2 promises the sandbox test passes every step from a new issue to a merged pull request.
- One of those steps is right after `/work`, when the card should say Work. That is story 3's fix; today `dokima/card.py` still says "Say /work to build the plan" while the build runs.
- But story 2 waits only for story 1. On autopilot it can be built before story 3, and then it fails at that step.
- The fix I proposed: story 2 also waits for story 3, and the sandbox test checks the moment a build starts, so it proves story 3's change too.

**The planner's question, left for you:** it assumes the sandbox test runs as its own workflow you start by hand on dokima-dev/card-gallery, outside the regular tests. That is because it needs Dokima's app key, and the regular test run holds no secrets. I didn't answer it for you, because your words don't settle it and it changes how the system works.

**Not raised:** story 1 calls commit f7340db "today's main", but main is now da897bc. That newer commit changes only the docs, the agent prompts and one test file, not the card code, so the old commit still shows the [#419](https://github.com/dokima-dev/dokima/issues/419) moment (the review had passed but the card still said running).
