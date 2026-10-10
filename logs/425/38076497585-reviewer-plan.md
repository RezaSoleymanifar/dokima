# reviewer (plan) for #425

Run: https://github.com/dokima-dev/dokima/actions/runs/38076497585

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (39.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/23900810-48a4-4cc3-87b4-1fc2ff5e4582/tool-results/bn115774c.txt
> 
> Preview (first 2KB):
> # Issue #425: The card always shows what is true right now: one rule, one place
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [380, 416], "loop": []} -->
> Every change on an issue or its pull request redraws both cards in one place, and a real sandbox play-through proves it step by step.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/425
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Real GitHub test:** The play-through on real GitHub needs Dokima's app key on a sandbox repo, so it cannot be part of All tests, which run in CI with no secrets. The plan assumes it is its own workflow, started by hand with the Run workflow button on dokima-dev/card-gallery, and that All tests keep proving each story with the fake GitHub in tests/card_player.py. Is that right, and is card-gallery the sandbox? · for you
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #380, #416
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"

`2. Bash`
```
cd /tmp/pack; ls in; cat open_blockers.json; echo; sed -n '/dokima-card-end\|Original issue/,$p' issue.md | head -300
```

> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-planner.json
> []
> <details><summary>Original issue</summary>
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
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #425 (2026-10-10T17:52:07Z)
> 
> Also covers #410: once a build has started, the card shows Work and no longer asks me to say /work. And #422: when a plan is approved, its PR's checks re-run by themselves (Dokima's app gets permission to re-run them; tell me exactly which setting if it lacks it).
> 
> ### RezaSoleymanifar on issue #425 (2026-10-10T17:52:22Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #425 (2026-10-10T17:52:47Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #425 (2026-10-10T17:52:49Z)
> 
> Autopilot is on for #425. Plannin

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"; python3 -c "
import json;d=json.load(open('in/05-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:4000])"
```

> {
>  "kind": "feature",
>  "summary": "Every change on an issue or its pull request redraws both cards in one place, and a real sandbox play-through proves it step by step.",
>  "feature": "The owner never sees an old card: every change on an issue or its pull request redraws both cards from GitHub's state now, in one place, and a play-through on dokima-dev/card-gallery proves it on every pull request that changes card, board or workflow code before it merges. Split by R1 (four independent goals: the play-through proof, the one redraw rule, #410's Work status and #422's check re-run) and R2 (about 18 criteria). Every promise of the issue and its comments goes to exactly one story.",
>  "stories": [
>   {
>    "title": "A play-through on a real sandbox repo checks the card after every step from issue to merge",
>    "user_story": "The owner can run one play-through on a real GitHub sandbox repo, with stand-in agents that use no model, and see after each step from a new issue to a merged pull request whether the card showed what had just happened.",
>    "task": "Add a workflow that plays one issue on dokima-dev/card-gallery from opened to merged: /plan, the plan review, /work and the build starting, the build's record, the code review starting, its record, the merge. Stand-in agents hand back fixed, valid hand-backs and call no model. After each step it waits for the card runs that step started to finish, reads the issue card and the PR card from GitHub, and compares them with what that step 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p .github/workflows/card.yml; git log --oneline -3 -- .github/workflows/card.yml; ls .github/workflows; python3 -c "import json;print(json.load(open('/tmp/pack/in/04-reviewer-plan.json'))['handback']['raises'])" | head -c 600
```

> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, the full suite starts, the bot puts up a code review's run card on
> # the pull request, or a person changes or comments on an issue; the cards of the
> # issues it blocks or is blocked by follow when their links changed. GitHub
> # announces no event for a blocked-by link added or removed by hand, so a run
> # every 15 minutes catches up the cards whose links changed. A merged pull request redraws its card and its issue's,
> # whoever merged it. These triggers
> # always use the default branch's copy of this file and of dokima/card.py, so
> # the work being judged cannot change how it is reported.
> # An issue and its pull request share one queue, so the newest redraw waits for the
> # running one and is never cancelled, while other issues' redraws and the sweep go
> # on beside it.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [in_progress, completed]
>   issues:
>   issue_comment:
>   pull_request_target:
>     types: [closed]
>   schedule:
>     - cron: '*/15 * * * *'
> permissions:
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   queue:
>     # The bot's own edits and comments (the card itself) don't trigger another card, and a comment on a pull
>     # request draws no issue card on it; an issue deleted or moved away has no card left to draw. A merge, even the
>     # bot's on autopilot, draws its pull request's card and its is

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added to S2.5 that story 2's pull request names the exact branch protection setting on main, with the check's name, that makes the play-through block the owner's merge button too.",
          "The planner folded the #419 moment into S2.3's every-step pass and left running by hand to S1.2, keeping story 2 at five criteria."],
  "decided": ["The play-through runs on dokima-dev/card-gallery by hand in story 1, and by itself on pull requests that change .github/workflows/, dokima/card.py, dokima/body.py or dokima/board.py in story 2."],
  "open": []},
 "verdict": "approve",
 "summary": "The split now carries every ask, including that a red play-through blocks a merge by hand as well as on autopilot, so it is ready for /work.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "One place redraws cards, and every change on an issue or PR reaches it, edits included.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S2.1"},
  {"ask": "One rule, one place: anything changes on an issue or its PR, the card is redrawn from scratch from what is on GitHub right now.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S2.2"},
  {"ask": "No exceptions, no special timing. A run's start and its result are both changes.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S2.1"},
  {"ask": "One test, on real GitHub in a sandbox repo with stand-in agents (no tokens): an issue is played from start to merge, and after each step the card shows what just happened.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S1.1"},
  {"ask": "stand-in agents (no tokens)", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S1.4"},
  {"ask": "It fails on today's code at the #419 moment.", "source": "https://github.com/dokima-dev/dokima/issues/425", "criterion": "S1.3
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)

**Agent:** Writing the plan review now; the check found the summary is two words over its limit, so I'm shortening it.

`6. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The split now carries every ask, including that a red play-through blocks a merge by hand as well as on autopilot."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 425 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#425](https://github.com/dokima-dev/dokima/issues/425) (one place redraws the card) with no new blockers. The hand-back passes both checks.

- **Last blocker fixed:** your rule that the play-through "must pass before that pull request merges" now applies to merges by hand, not only autopilot's. Story 2's pull request will name the exact branch protection setting on main, with the check's name as GitHub shows it, that makes the play-through block your merge button. The bot can't change that setting itself, so you'll have to switch it on.
- **Every ask is covered:** I matched each of the 14 asks in the issue and your comments to a criterion and found none missing. Your 18:12 answer (card-gallery is the sandbox, it runs on every pull request that changes card, board or workflow code, running by hand stays possible, and All tests keep the fake-GitHub checks) is spread across stories 1 and 2.
- **Nothing to run yet:** this is a split, so no tests exist at this stage. Each story writes and proves its own tests when it is planned.
- **Bug still on main:** the card bug from [#419](https://github.com/dokima-dev/dokima/issues/419) (the card kept saying Code review running) is still there. `card.yml` hasn't changed since before f7340db, the commit story 1 replays.

Next, `/work` on [#425](https://github.com/dokima-dev/dokima/issues/425) files the four stories, or autopilot does it on its own since this issue is on autopilot. Stories 1, 3 and 4 can start straight away; story 2 waits for stories 1 and 3.
