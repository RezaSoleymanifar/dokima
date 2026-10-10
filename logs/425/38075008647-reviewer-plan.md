# reviewer (plan) for #425

Run: https://github.com/dokima-dev/dokima/actions/runs/38075008647

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (30.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5c0d5aaf-d7e4-4c8b-9e76-c8096934bf15/tool-results/b2laxq68e.txt
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
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Test cannot pass:** S2.4 promises the play-through passes every step from a new issue to a merged pull request on the code story 2 ships, and the play-through checks

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n '1,400p'
```

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
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Test cannot pass:** S2.4 promises the play-through passes every step from a new issue to a merged pull request on the code story 2 ships, and the play-through checks the card after /work, where it should show what just happened: a build started. That is story 3's fix (#410), yet story 2 depends only on story 1, so on autopilot story 2 can be built before story 3 and its own crit

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []{
>  "kind": "feature",
>  "summary": "Every change on an issue or its pull request redraws both cards in one place, and a real sandbox play-through proves it step by step.",
>  "feature": "The owner never sees an old card: every change on an issue or its pull request redraws both cards from GitHub's state now, in one place, and a play-through on dokima-dev/card-gallery proves it on every pull request that changes card, board or workflow code. Split by R1 (four independent goals: the play-through proof, the one redraw rule, #410's Work status and #422's check re-run) and R2 (about 18 criteria). Every promise of the issue and its comments goes to exactly one story.",
>  "stories": [
>   {
>    "title": "A play-through on a real sandbox repo checks the card after every step from issue to merge",
>    "user_story": "The owner can run one play-through on a real GitHub sandbox repo, with stand-in agents that use no model, and see after each step from a new issue to a merged pull request whether the card showed what had just happened.",
>    "task": "Add a workflow that plays one issue on dokima-dev/card-gallery from opened to merged: /plan, the plan review, /work and the build starting, the build's record, the code review starting, its record, the merge. Stand-in agents hand back fixed, valid hand-backs and call no model. After each step it waits for the card runs that step started to finish, reads the issue card and the PR card from GitHub, and compares them with what that step should show. It

`4. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima .github/workflows; sed -n 25,40p .github/workflows/card.yml; grep -n "actions" dokima/app.json; git log --oneline -1 f7340db; ls /tmp/pack/in
```

> .github/workflows:
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
> 
> dokima:
> agent.py
> app.json
> audit.py
> board.py
> body.py
> card.py
> checks.py
> fence.py
> icons
> manifest.py
> plan.py
> planner.py
> raises.py
> roles
> scan.py
> trail.py
> uptodate.py
> words.py
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   queue:
>     # The bot's own edits and comments (the card itself) don't trigger another card, and a comment on a pull
>     # request draws no issue card on it; an issue deleted or moved away has no card left to draw. A merge, even the
>     # bot's on autopilot, draws its pull request's card and its issue's; a pull request closed unmerged draws none.
>     # A run that starts redraws only for the full suite, so All tests shows running. The bot's comments on a pull
>     # request are read below: only a code review's run card redraws both cards, so Code review shows running.
>     if: (github.event_name == 'workflow_run' && (github.event.action != 'in_progress' || github.event.workflow_run.name == 'full suite')) || (github.event_name == 'issue_comment' && github.event.action == 'created' && github.event.issue.pull_request && github.event.sender.type == 'Bot') || (github.event_name == 'pull_request_target' && github.event.pull_request.merged) || github.event_name == 'schedule' || (github.event_name == 'issues' && github.event.action == 'opened') || (

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner kept the split into four stories and made the redraw story wait for the play-through story and the Work-status story.",
          "The planner added the moment a build has started to the steps the play-through checks."],
  "decided": ["The play-through runs by hand on dokima-dev/card-gallery in story 1, and by itself on pull requests that change .github/workflows/, dokima/card.py, dokima/body.py or dokima/board.py in story 2.",
              "Autopilot does not merge such a pull request until the play-through is green; making it required for a human merge is left to a branch protection setting the plan's context says the pull request names."],
  "open": ["No criterion says the owner is told which setting makes the play-through block a human merge."]},
 "verdict": "block",
 "summary": "The owner asked that the play-through must pass before a card, board or workflow pull request merges, and the plan promises that only for autopilot's merges, not for the owner's own merge button.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "No criterion",
   "text": "The owner said the play-through \"must pass before that pull request merges\". S2.5 promises only that autopilot waits for it; a pull request merged by hand with the play-through red is not covered by any criterion. The plan's own context says the bot cannot make the check required and that the pull request names the branch protection setting for the owner, but no criterion carries that, so a build that never tells the owner passes. Smallest fix: add to S2.5 (or a new S2 criterion) that story 2's pull request names the exact branch protection setting, by the check's name as GitHub shows it, that makes the play-through required on main, so a red play-through blocks the owner's merge button too.",
   "evidence": "Owner's comment of 2026-10-10T18:12:56Z on #425: \"it must pass before that pull requ
```

> Exit code 1
> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** Shortening the review's summary to pass the hand-back check.

`6. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The owner said the play-through must pass before such a pull request merges; the plan promises that only for autopilot's merges."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 425 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I blocked the plan for [#425](https://github.com/dokima-dev/dokima/issues/425) (one place redraws the card) and sent it back to the planner with one blocker. The review is in `/tmp/dokima-out/review.json` and passes both checks.

- **Earlier blocker fixed:** Story 2 (one workflow redraws the card) now waits for stories 1 and 3. Story 1's play-through now also checks the card right after a build starts.
- **The ask now missing:** Your comment of 2026-10-10 says the play-through "must pass before that pull request merges." Criterion S2.5 only stops autopilot from merging a pull request with a red play-through. Nothing in the plan stops your own merge button.
- **The fix I asked for:** The bot can't make the check required, because that is a branch protection setting. The plan mentions this, but only in its notes, not in any criterion. I asked the planner to add a criterion: story 2's pull request must name the exact branch protection setting. Turning that on makes a red play-through block your merges too.

Every other ask, from the issue and your two comments, is covered by a criterion. This plan is a split with no tests yet, so I had no tests to run. I raised no questions for you.
