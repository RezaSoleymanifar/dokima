# reviewer (plan) for #332

Run: https://github.com/dokima-dev/dokima/actions/runs/37897435464

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (46.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/11914798-d1f1-46b8-b60d-2d32a55b6695/tool-results/bb46d0tqc.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  9 07:09 .
> drwxrwxrwt 18 root   root    4096 Oct  9 07:09 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 07:09 in
> -rw-r--r--  1 runner runner 45465 Oct  9 07:09 issue.md
> -rw-r--r--  1 runner runner  1673 Oct  9 07:09 open_blockers.json
> -rw-r--r--  1 runner runner  7556 Oct  9 07:09 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct  9 07:09 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 07:09 ..
> -rw-r--r-- 1 runner runner 6537 Oct  9 07:09 01-planner.json
> -rw-r--r-- 1 runner runner 6487 Oct  9 07:09 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8224 Oct  9 07:09 03-planner.json
> # Issue #332: The issue and PR cards are always computed from the issue's state right now, and a merged PR's card shows Merged
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #330, story 2</summary>
> 
> **Part of:** #330 Cards and the board always show what is true right now
> 
> **User story:** The owner reads the true state on every issue card and PR card, including a PR merged before its card was last written.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; head -c 20000 issue.md
```

> # Issue #332: The issue and PR cards are always computed from the issue's state right now, and a merged PR's card shows Merged
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #330, story 2</summary>
> 
> **Part of:** #330 Cards and the board always show what is true right now
> 
> **User story:** The owner reads the true state on every issue card and PR card, including a PR merged before its card was last written.
> 
> **Context:** Split from #330 (rule R2, R3). card.yml runs on finished checks, the worker, issue events and comments, and a 15-minute schedule that only redraws cards whose blocked-by links changed (dokima/card.py, sweep and refresh); it never runs when a PR is merged or closed, so #246's PR card was never rewritten after its merge, and #312's PR card missed a dropped redraw. Its concurrency group is the single 'card' group, so a pending run for one issue is cancelled by the next issue's. card.status() already returns Merged for a merged PR; draw() writes the PR card for an open, merged or closed PR once it is found, but find_work() and the workflow triggers decide whether it is found. This story makes every event about an issue or its PR, and the 15-minute sweep, redraw that issue's card and PR card from state, one queue per issue. Redrawing every closed card every 15 minutes may cost too many API calls; the sweep may compare what a card shows with the state and redraw only the ones that differ. The owner's ask covers dokima/ca

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; cat plan.json; cat in/02-reviewer-plan.json
```

> [
>  {
>   "id": "B1",
>   "criterion": "332.7",
>   "test": "tests/test_card_now.py::test_runs_started_by_a_pull_request_run_mains_code",
>   "problem": "332.7 promises that runs started by a pull request use main's copy of card.yml. But criterion 1 has card.yml start on reviews and line notes (pull_request_review, pull_request_review_comment), and GitHub runs those from the pull request's merge ref, so it uses the pull request's own copy of card.yml, with the keys. The test always plays the repo's own card.yml and checks only which ref the checkout step names. A pull request that edits card.yml would therefore still pass it, so the test proves only the checkout, not the promise.",
>   "evidence": "tests/test_card_now.py:17 (docstring: 'on a review GitHub's own ref is the pull request's merge ref') and github_ctx at :687-693 set ref refs/pull/N/merge for reviews, yet Run.__init__ reads workflow() (the repo's card.yml, :698 and :759) for every event. test_runs_started_by_a_pull_request_run_mains_code (:1200) asserts only r.checkouts and that 'pull_request' is not a trigger. Today board.yml:15-21 starts on pull_request_review the same way.",
>   "fix": "Either make the promise true: have reviews and line notes reach card.yml through a relay without keys (for example a workflow_run of a small listener), and test that card.yml's on: lists neither pull_request_review nor pull_request_review_comment. Or narrow 332.7 to what is true and tested ('every run checks out main's dokima/card.py, never 

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; tail -c 6000 issue.md | head -80
```

> 29:### dokima-runtime on issue #332 (2026-10-09T06:25:44Z)
> 33:### dokima-runtime on issue #332 (2026-10-09T06:25:55Z)
> 234:### dokima-runtime on issue #332 (2026-10-09T06:55:23Z)
> 398:### dokima-runtime on issue #332 (2026-10-09T07:04:31Z)
> 610:### dokima-runtime on issue #332 (2026-10-09T07:09:33Z)
>     "why": "Redrawing all of the repo's 330-odd cards every 15 minutes would cost about 13,000 calls an hour, far past GitHub's 5,000-an-hour limit, and every card run would then fail.",
>     "principle": "Small and lean."
>    }
>   ],
>   "scope": [
>    "dokima/card.py",
>    ".github/workflows/card.yml",
>    ".github/workflows/card-relay.yml",
>    "AGENTS.md"
>   ],
>   "out_of_scope": [
>    "The board's columns and pills; that is #331.",
>    "The scan that proves every card and board item is true; that is #333.",
>    "How a card looks: the same card is drawn, only when and from what changes.",
>    "A closed issue's card is checked against its state, comment count and pull request, not the text of each comment, so the sweep stays inside GitHub's limits.",
>    "Comments the bot posts that hold no record (live run cards, Autopilot lines) start no redraw.",
>    "board.yml also starts on reviews from the pull request's own copy; the reviewer proposed that as its own issue, and this story leaves board.yml alone."
>   ],
>   "tests": {
>    "332.1": [
>     "tests/test_card_now.py::test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now",
>     "tests/test_card_now.py::test_an_event_redraws_an_open

`5. Bash`
```
cd /tmp/pack; sed -n 398,420p issue.md; sed -n 610,640p issue.md
```

> ### dokima-runtime on issue #332 (2026-10-09T07:04:31Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** The owner reads the true state on every issue card and PR card, including a PR merged before its card was last written, whichever events were dropped or late.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria:**
> 
> 1. Any event about an issue or its pull request redraws both cards from GitHub as it is now. That covers the issue changing, a comment on either, the merge or close, a review, a line note, new commits, the checks finishing and an agent's record; the cards' own writes start no further redraw.
> 2. Every 15 minutes a sweep puts right every issue card and PR card that does not show its issue's state now, open or closed. #246's merged PR and #312's PR with no card are such cards.
> 3. A pull request's card is written whether it is open or merged. After the merge it says Merged, with the true Definition of Done: All tests, Code review and Owner approval as GitHub records them.
> 4. Each issue's card runs, for the is

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat a3ecbb8 3384ccb; git diff --stat e934cfe 3384ccb; ls .github/workflows; wc -l dokima/card.py tests/test_card_now.py
```

> tests/test_card_now.py | 165 +++++++++++++++++++++++++++++++++++++++++--------
>  1 file changed, 138 insertions(+), 27 deletions(-)
>  tests/test_card_now.py   | 1359 ++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_hand_links.py |   24 +-
>  2 files changed, 1370 insertions(+), 13 deletions(-)
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
> uptodate.yml
> wiki.yml
> worker.yml
>    721 dokima/card.py
>   1359 tests/test_card_now.py
>   2080 total

**Agent:** I'm in round two of reviewing the plan for #332. Next I'll look at what the planner changed in the tests to fix last round's blocker B1.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff a3ecbb8 3384ccb
```

> diff --git a/tests/test_card_now.py b/tests/test_card_now.py
> index a84f6f2..9492cc6 100644
> --- a/tests/test_card_now.py
> +++ b/tests/test_card_now.py
> @@ -13,8 +13,11 @@ These tests play card.yml the way GitHub runs it, for one event at a time, again
>    bash, from a copy of this repo's dokima/ and .github/, with a fake `gh` first on PATH. Values a step writes to
>    GITHUB_OUTPUT or GITHUB_ENV are read as KEY=value lines, and a job's `outputs:` reach later jobs through `needs`.
>  - Every concurrency group card.yml declares (the workflow's and each job's that runs) is evaluated for the event.
> -- Pull request events reach card.yml as pull_request_target (main's copy of the workflow), pull_request_review and
> -  pull_request_review_comment; on a review GitHub's own ref is the pull request's merge ref.
> +- Pull request events are sent as GitHub sends them: pull_request_target for the pull request itself (main's copy of
> +  the workflow), pull_request_review and pull_request_review_comment for reviews and line notes (the pull request's own
> +  copy, from its merge ref). Such a review or line note reaches card.yml through a relay: any workflow of this repo
> +  that card.yml's workflow_run lists by name and that starts on the event is played first, and when it passes,
> +  card.yml is played for the workflow_run GitHub then sends, carrying the pull request.
>  
>  The fake GitHub (repo o/r, code owner `boss` through CODEOWNERS, Dokima's bot `dokima-runtime`) keeps its state in one
>  JSON file and a

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,60p .github/workflows/card.yml; for f in .github/workflows/*.yml; do echo "== $f"; grep -nE "^name:|^on:|^  [a-z_]+:|permissions|environment|secrets\.|app-token" $f | head -30; done
```

> name: card
> # Writes the card at the top of the issue and its PR whenever the checks or the
> # worker finish, or a person changes or comments on an issue; the cards of the
> # issues it blocks or is blocked by follow when their links changed. GitHub
> # announces no event for a blocked-by link added or removed by hand, so a run
> # every 15 minutes catches up the cards whose links changed. These triggers
> # always use the default branch's copy of this file and of dokima/card.py, so
> # the work being judged cannot change how it is reported.
> on:
>   workflow_run:
>     workflows: [done-whens, full suite, worker]
>     types: [completed]
>   issues:
>   issue_comment:
>   schedule:
>     - cron: '*/15 * * * *'
> concurrency:
>   group: card
>   cancel-in-progress: false
> permissions:
>   contents: read
>   actions: read
>   checks: read
>   issues: read
>   pull-requests: read
> jobs:
>   card:
>     environment: keys
>     # The bot's own edits and comments (the card itself) don't trigger another card, and a comment on a pull
>     # request draws no issue card on it; an issue deleted or moved away has no card left to draw.
>     if: github.event_name == 'workflow_run' || github.event_name == 'schedule' || (github.event_name == 'issues' && github.event.action == 'opened') || (github.event.sender.type != 'Bot' && !github.event.issue.pull_request && !(github.event_name == 'issues' && (github.event.action == 'deleted' || github.event.action == 'transferred')))
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>   

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import sys; sys.path.insert(0,'tests')
import test_card_now as t
for f,wf in t.listened().items(): print(f, sorted(t.triggers(wf)), t.keys_held(wf))
"; timeout 900 python3 -m pytest -q tests/test_card_now.py tests/test_hand_links.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed|AssertionError|^E " | head -60
```

> done-whens.yml ['merge_group', 'pull_request_target'] []
> full-suite.yml ['merge_group', 'pull_request_target', 'push'] []
> worker.yml ['issues'] ['job work opens environment keys', "job work makes the app's token", 'it reads a secret']
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 332.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> E       assert False
> E        +  where False = <test_card_now.Run object at 0x7f6cb5d863c0>.started
> tests/test_card_now.py:929: AssertionError
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 332.1: card.yml does not start on pull_request_target synchronize, so the cards are not redrawn
> E       assert False
> E        +  where False = <test_card_now.Run object at 0x7f6cb5d92090>.started
> tests/test_card_now.py:929: AssertionError
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 332.1: card.yml started on issue_comment created but its card job was skipped
> E       assert False
> E        +  where False = card_ran()
> E        +    where card_ran = <test_card_now.Run object at 0x7f6cb5e22480>.card_ran
> tests/test_card_now.py:930: AssertionError
> E       AssertionError: 332.1: card.yml does not start on: ['pull_request_target opened', 'pull_request_target edited', 'pull_

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_card_now.py tests/test_hand_links.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | tail -30; timeout 900 python3 -m pytest -q tests/test_card_now.py -k "mains_code or few_github" 2>&1 | grep -E "^E " | head
```

> PR #260 has every check passed and an approving code review, and the owner merges it: the merge event leaves
>         #260's card saying Merged with All tests, Code review and Owner approval passed. On a fresh GitHub where All tests
>         failed on the PR's last commit, the code review blocked and the bot merged it, the merge leaves Merged with All
>         tests failed, Code review failed and Owner approval not passed. Proves 332.3."""
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
>         the checks passed so far, and the closing line kept. Proves 332.3."""
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> >       assert r.failed(), f"332.6: the scheduled run passed although #312's card could not be redrawn:\n{r.log[-2000:]}"
> E       AssertionError: 332.6: the scheduled run passed although #312's card could not be redrawn:
> E        +  where False = failed()
> E        +    where failed = <test_card_now.Run object at 0x7ff16a6a92b0>.failed
>             assert r.failed(), f"332.6: the run passed although #{named}'s card could not be written"
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> FAILED tests/test_card_now.py::test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github

`11. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && cat > .github/workflows/card-relay.yml <<'EOF'
name: card relay
on:
  pull_request_review:
    types: [submitted, edited, dismissed]
  pull_request_review_comment:
    types: [created, edited, deleted]
permissions:
  contents: read
jobs:
  relay:
    runs-on: ubuntu-24.04
    steps:
      - run: echo relayed
EOF
python3 - <<'EOF'
p='.github/workflows/card.yml'; s=open(p).read()
s=s.replace("workflows: [done-whens, full suite, worker]","workflows: [done-whens, full suite, worker, card relay]")
s=s.replace("  issue_comment:\n","  issue_comment:\n  pull_request_target:\n    types: [opened, edited, reopened, synchronize, closed]\n")
s=s.replace("ref: main","").replace("      - uses: actions/checkout@v5","      - uses: actions/checkout@v5\n        with:\n          ref: main")
s=s.replace("group: card\n","group: card-${{ github.event.issue.number || github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number || github.run_id }}\n")
open(p,'w').write(s)
EOF
python3 -m pytest -q tests/test_card_now.py -k "mains_code" 2>&1 | grep -E "^E |passed|failed" | head
```

> """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> >       assert not r.failed(), f"{k}: card.yml's run on {what} failed:\n{r.log[-3000:]}"
> E       AssertionError: 332.7: card.yml's run on pull_request_target closed failed:
> E         ## card: Write the card (exit 1)
> E         Traceback (most recent call last):
> E           File "/tmp/pytest-of-runner/pytest-3/test_runs_started_by_a_pull_re0/ws/dokima/card.py", line 721, in <module>
> E             main()
> E           File "/tmp/pytest-of-runner/pytest-3/test_runs_started_by_a_pull_re0/ws/dokima/card.py", line 674, in main
> E             number, pr_number = find_work(repo)
> E                                 ^^^^^^^^^^^^^^^
> Shell cwd was reset to /home/runner/work/dokima/dokima

`12. Bash`
```
cd /tmp/rv && python3 -c "
import sys; sys.path.insert(0,'tests')
import test_card_now as t
for e in (t.review_event(246,260), t.line_note(246,260)):
    print(e[0], t.reaches(*e), [n for n,_ in t.relays(*e)])
for f,wf in t.listened().items(): print(f, t.keys_held(wf) if set(t.triggers(wf))&t.OWN_COPY else '-')
"
```

> pull_request_review True ['card relay']
> pull_request_review_comment True ['card relay']
> card-relay.yml []
> done-whens.yml []
> full-suite.yml []
> worker.yml -
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The planner's fix for B1 holds up when I try it in a copy of the repo. Writing the hand-back now.

`13. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Changed the 332.7 test so that a review or a line note on a pull request reaches card.yml only through a relay workflow, and so that any relay that runs the pull request's own copy must hold no keys.",
   "Folded in the three notes from last round: 21 open issues in the call-count test, a merged pull request with a blocked code review, and owner edits, reopens, dismissed reviews and deleted line notes each run through card.yml."
  ],
  "decided": [
   "card.yml starts only on events GitHub runs from main's copy; reviews and line notes reach it through a new keyless relay, .github/workflows/card-relay.yml, which is added to the scope.",
   "A sweep with nothing to fix makes at most 10 GitHub calls plus two for each open issue or pull request; board.yml is left alone."
  ],
  "open": [
   "No questions for the owner."
  ]
 },
 "verdict": "approve",
 "summary": "The plan covers every ask. Reviews and line notes now reach the card through a relay that holds no keys, and the test catches a card.yml or relay that would run the pull request's own copy with the keys.",
 "blockers": [],
 "notes": [
  {
   "text": "The relay runs from the pull request's own copy, so a pull request could edit card-relay.yml in its own branch. The test reads only the repo's copy of the relay. The keys stay safe only because the keys environment opens for main's workflows alone, and that is a GitHub setting no test here can prove.",
   "evidence": "tests/test_card_now.py keys_held() and listened() read .github/workflows/ from the checkout; worker.yml:95 says the keys environment is one 'which only main's reviewed workflows can open'."
  }
 ],
 "outside_plan": [],
 "resolved": ["B1"],
 "issues_found": [],
 "asks": [
  {"ask": "Any event about an issue or its PR, including a merge, close or review, redraws the issue card and PR card from GitHub's state now.", "source": "https://github.com/dok
```

> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> rc=1

`14. Bash`
```
python3 - <<'EOF'
import json; p='/tmp/dokima-out/review.json'; d=json.load(open(p))
d["summary"]="The plan covers every ask, and reviews and line notes now reach the card through a keyless relay that the test checks."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 332 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #332, and last round's only blocker (B1) is now resolved. The hand-back is in `/tmp/dokima-out/review.json`, and both checks on it pass.

**B1 (332.7):** last round, reviews and line notes on a pull request would have run the pull request's own copy of `card.yml`, which holds the keys. The planner fixed this rather than narrowing the promise:
- `card.yml` may now start only on events GitHub runs from main's copy.
- Reviews and line notes reach it through a new relay, `.github/workflows/card-relay.yml`, which must hold no keys. It is now in scope.
- The test now runs the relay first, then `card.yml`. It fails if `card.yml` starts directly on a review or line note, or if the relay opens the keys environment.

I tried a minimal keyless relay in a scratch copy of the repo. Reviews and line notes reach `card.yml` through it, and the keys check on `done-whens`, `full suite` and the relay comes back clean. The test then gets past the workflow and fails only inside the card code, which hasn't been built yet.

**Today's tests:** all 13 new tests in `tests/test_card_now.py` fail, each because the feature is missing (no crashes or bad paths). The 16 that pass in that run include the two older tests the planner relaxed in `tests/test_hand_links.py`.

**Last round's three notes** were all folded in:
- The call-count test now has 21 open issues, so a sweep that spends three calls per open issue would go over the limit.
- A merged pull request whose code review blocked must show Code review as failed.
- Owner edits and reopens, and edited and dismissed reviews and line notes, are now each run through `card.yml`.

All six asks in the issue map to criteria 332.1–332.6, and the plan has no questions for the owner.

I left one note: a pull request could edit its own copy of the relay. What keeps the keys safe is GitHub's rule that only main's workflows can open the keys environment. That is a repo setting, and no test can prove it.
