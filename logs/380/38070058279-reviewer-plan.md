# reviewer (plan) for #380

Run: https://github.com/dokima-dev/dokima/actions/runs/38070058279

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
> 02-planner.json
> # Issue #380: The board and cards update only when something they show can change, and bursts become one update
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 372 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Board runs skip events that cannot move a card, a burst on one issue becomes one run, and an unchanged card is not saved.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> https://github.com/dokima-dev/dokima/issues/380
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #368, #377, #372
> 
> **User story:** The board and cards look exactly as they do today, but board runs drop to the events that can change a card, one per burst, so GitHub's hourly budget no longer runs out.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** An event that cannot ch

`2. Bash`
```
cd /tmp/pack; cat parent.json | head -50; python3 -c "
import json;d=json.load(open('in/02-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000]);print(d.keys())"
```

> {"number": null}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38068987145",
>  "commit_before": "e067a2e19c4df5861e258914c3ddd95f2b36e8e8",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 875924,
>   "turns": 39,
>   "cost_usd": 2.1793274,
>   "tokens_in": 3366615,
>   "tokens_out": 31176
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/380/38068987145-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38068987145",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git diff --stat main...HEAD; git diff e067a2e HEAD --stat; wc -l tests/test_quiet_board.py
```

> tests/test_body.py        |   6 +-
>  tests/test_quiet_board.py | 698 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 702 insertions(+), 2 deletions(-)
>  tests/test_open_ask.py    |   8 +-
>  tests/test_quiet_board.py | 186 ++++++++++++++++++++++++++++++++--------------
>  2 files changed, 136 insertions(+), 58 deletions(-)
> 698 tests/test_quiet_board.py

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_quiet_board.py; git diff main...HEAD -- tests/test_body.py
```

> <persisted-output>
> Output too large (42.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/100a4b03-f2e9-46db-8fad-356c17305eb0/tool-results/beyhnmurs.txt
> 
> Preview (first 2KB):
> """The board updates only when a card can change, once per burst (#380).
> 
> GitHub's GraphQL budget (5,000 calls an hour, shared by every Dokima workflow) ran out on 2026-10-09, and board.yml
> alone used about 56% of it: it recomputed an issue's cards on every comment, line note, new commit and finished
> check, though none of those can move a card. These tests hold the fix to the owner's words:
> 
> - `python3 -m dokima.board queue`, the step that already names each event's board queue from its payload alone,
>   also writes `run=true` or `run=false` to GITHUB_OUTPUT: false exactly for an event that cannot change a card's
>   column or pill, true for every other one (and for any event it cannot read). board.yml's sync job runs only on
>   true, so a skipped event spends no GraphQL call at all.
> - A review or line note reaches board.yml only as reviews.yml's run completing (#418), which carries no summary, so
>   the step reads it from the run's event and name: reviews.yml names its run from the review, and a run named any
>   other way (a pull request whose own reviews.yml is older) still runs the update.
> - Events about one issue that arrive within a minute become one update: board.yml waits one minute in a queue of
>   the issue's own that a newer event cancels, and only then syncs.
> 

`5. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/100a4b03-f2e9-46db-8fad-356c17305eb0/tool-results/beyhnmurs.txt
```

> 1	"""The board updates only when a card can change, once per burst (#380).
> 2	
> 3	GitHub's GraphQL budget (5,000 calls an hour, shared by every Dokima workflow) ran out on 2026-10-09, and board.yml
> 4	alone used about 56% of it: it recomputed an issue's cards on every comment, line note, new commit and finished
> 5	check, though none of those can move a card. These tests hold the fix to the owner's words:
> 6	
> 7	- `python3 -m dokima.board queue`, the step that already names each event's board queue from its payload alone,
> 8	  also writes `run=true` or `run=false` to GITHUB_OUTPUT: false exactly for an event that cannot change a card's
> 9	  column or pill, true for every other one (and for any event it cannot read). board.yml's sync job runs only on
> 10	  true, so a skipped event spends no GraphQL call at all.
> 11	- A review or line note reaches board.yml only as reviews.yml's run completing (#418), which carries no summary, so
> 12	  the step reads it from the run's event and name: reviews.yml names its run from the review, and a run named any
> 13	  other way (a pull request whose own reviews.yml is older) still runs the update.
> 14	- Events about one issue that arrive within a minute become one update: board.yml waits one minute in a queue of
> 15	  the issue's own that a newer event cancels, and only then syncs.
> 16	- The 15-minute sweep stays, so a card a skipped event could have put right is put right there.
> 17	- A card run saves the card on the issue, and writes it on the pull request, o

**Agent:** I've read the plan and its tests, and now I'm running them to check each one fails today for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_quiet_board.py -x -q 2>&1 | tail -5; timeout 900 python3 -m pytest -q tests/test_quiet_board.py 2>&1 | grep -E "^(FAILED|PASSED|ERROR)|passed|failed" | cut -c1-400
```

> FAILED tests/test_quiet_board.py::test_events_that_cannot_move_a_card_do_not_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> assert None in ('true', 'false')
>  +  where None = <built-in method get of dict object at 0x7f95c1a2b4c0>('run')
>  +    where <built-in method get of dict object at 0x7f95c1a2b4c0> = {'group': 'board-57'}.get
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> FAILED tests/test_quiet_board.py::test_events_that_cannot_move_a_card_do_not_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_events_that_can_move_a_card_still_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issues event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_an_event_the_queue_step_cannot_read_still_runs_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_board_yml_syncs_the_board_only_when_the_queue_step_says_so - AssertionError: 380.1: board.yml's 'sync' job still syncs the board on: ["a stranger's comment on the issue", "the code owner's comment that is no command", "the 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,80p .github/workflows/board.yml; grep -n "run-name\|^on:\|^  [a-z_]*:" .github/workflows/reviews.yml | head -20
```

> name: board
> # Puts every card in the column and pill its issue's state on GitHub gives now, on
> # every event about an issue or its pull request and every 15 minutes (only what
> # changed since the last sweep that succeeded); keeps its Priority Blocker on open
> # issues that block an open issue (from blocked-by links, read on close, reopen and
> # every 15 minutes, since GitHub sends no event for a link), and otherwise in step
> # with the high and parked labels. Every merge sweeps every card.
> # An issue and its pull requests share one queue, so the newest recompute waits for the
> # running one and is never cancelled, while other issues' runs go on beside it.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [opened, edited, labeled, unlabeled, closed, reopened]
>   schedule:
>     - cron: "*/15 * * * *"
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   pull_request_review:
>     types: [submitted]
>   pull_request_review_comment:
>     types: [created]
>   workflow_run:
>     workflows: [done-whens]
>     types: [completed]
> permissions:
>   contents: read
> jobs:
>   queue:
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     outputs:
>       group: ${{ steps.queue.outputs.group }}
>     steps:
>       - use

`8. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; git log --oneline -5 main; git log --all --oneline | grep -i 418 | head; grep -rn "418" dokima AGENTS.md tests --include=*.py --include=*.md | head
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
> uptodate.yml
> wiki.yml
> worker.yml
> f7340db board.yml runs the pull request's own copy of itself, with the keys, on a review (#418)
> bcb36e4 The reviewer settles raises between agents and confirms issues before code files them (#414)
> e02bcb2 Every agent's hand-back raises and answers through the same two fields, and nothing raised is skipped (#383)
> 6259897 A new issue shows the owner's text open until a plan exists; it folds only once planned (#411)
> 2e33bbe Source links to where the owner said it, shown as a GitHub reference with icon and name (#409)
> f7340db board.yml runs the pull request's own copy of itself, with the keys, on a review (#418)
> 14783f8 Conversation of run 37890224187
> 9ab21d2 Conversation of run 37883641801
> 29367af Conversation of run 37883334181
> 55e2026 Conversation of run 37864554184
> bf3cfcd Conversation of run 37822643418
> 0cc893e Conversation of run 37744187317
> 8041888 Merge branch 'main' into agents-scope-rule
> tests/test_quiet_board.py:11:- A review or line note reaches board.yml only as reviews.yml's run completing (#418), which carries no summary, so
> tests/test_quiet_board.py:101:    A review or line note reaches board.yml only as reviews.yml's run completing (#418), which carries no summary.
> tests/test_quiet_board.py:103:    request's title when reviews.yml names no run (or, on a branch from before #418, does not exist)."""
> tests/test_field

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git show main:.github/workflows/reviews.yml | head -40; git show main:.github/workflows/board.yml | sed -n 10,40p; git diff HEAD main --stat | tail -3
```

> name: reviews
> # Runs on every submitted review and new line note, only so board.yml, which runs
> # after it as main's copy, puts the cards where their state says. GitHub runs this
> # file from the pull request's own copy, so it holds no key and starts nothing.
> on:
>   pull_request_review:
>     types: [submitted]
>   pull_request_review_comment:
>     types: [created]
> permissions: {}
> jobs:
>   heard:
>     runs-on: ubuntu-24.04
>     steps:
>       - run: echo "Review or line note on pull request ${{ github.event.pull_request.number }}"
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [opened, edited, labeled, unlabeled, closed, reopened]
>   schedule:
>     - cron: "*/15 * * * *"
>   issue_comment:
>     types: [created]
>   # pull_request_target runs main's copy of this file, so the keys environment opens;
>   # this job only checks out main's code, never the PR's.
>   pull_request_target:
>     types: [opened, reopened, synchronize, closed]
>   # A review or line note would run the pull request's own copy of this file, so
>   # they reach it through reviews.yml, which holds no key; this runs after it.
>   workflow_run:
>     workflows: [done-whens, reviews]
>     types: [completed]
> permissions:
>   contents: read
> jobs:
>   queue:
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     outputs:
>       group: ${{ steps.queue.outputs.group }}
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.e

`10. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt main 2>&1|tail -1; cd /tmp/wt; git checkout -q HEAD; git show try/issue-380:tests/test_quiet_board.py > tests/test_quiet_board.py; git merge-tree --write-tree main try/issue-380 >/dev/null && echo mergeclean; timeout 900 python3 -m pytest -q tests/test_quiet_board.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-300
```

> mergeclean
> FAILED tests/test_quiet_board.py::test_events_that_cannot_move_a_card_do_not_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_events_that_can_move_a_card_still_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issues event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_an_event_the_queue_step_cannot_read_still_runs_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_board_yml_syncs_the_board_only_when_the_queue_step_says_so - AssertionError: 380.1: board.yml's 'sync' job still syncs the board on: ["a stranger's comment on the issue", "the code owner's comment that is no command", "the code owner's comment naming a command 
> FAILED tests/test_quiet_board.py::test_events_about_one_issue_wait_a_minute_in_a_queue_of_their_own_that_a_newer_one_cancels - AssertionError: 380.2: board.yml has no job the sync waits on that sleeps in a queue a newer event cancels
> FAILED tests/test_quiet_board.py::test_an_update_a_newer_event_cancelled_never_syncs - AssertionError: 380.2: board.yml has no job the sync waits on that sleeps in a queue a newer event cancels
> FAILED tests/test_quiet_board.py::test_a_skipped_

`11. Bash`
```
cd /tmp/wt; git diff e067a2e 386c1ce -- tests/test_open_ask.py; grep -n "run_card\|saved" tests/test_open_ask.py | head -30; grep -rln "card.main\|run_card" tests | head -20
```

> diff --git a/tests/test_open_ask.py b/tests/test_open_ask.py
> index acd4af8..950cfaa 100644
> --- a/tests/test_open_ask.py
> +++ b/tests/test_open_ask.py
> @@ -96,15 +96,15 @@ def test_the_open_ask_stays_byte_for_byte_after_many_redraws(record_property):
>  def test_the_card_shows_the_owners_ask_open(record_property, monkeypatch, github):
>      """When the card is drawn on an issue the owner wrote, their text shows open below it.
>  
> -    Runs the card's main on a fresh owner-written issue, then again on what it saved, and checks both bodies have the
> -    card on top and the owner's text open below the marker, byte for byte. The second run may save nothing when the
> -    card has not changed; the body it leaves is then the first one."""
> +    Runs the card's main on a fresh owner-written issue, then again on what it saved, and checks both saved bodies
> +    have the card on top and the owner's text open below the marker, byte for byte."""
>      record_property("proves", "237.1")
>      saved = run_card(monkeypatch, github, TRICKY)
>      assert saved is not None, "237.1: the card saved nothing on the issue"
>      assert saved.startswith(plan.CARD_START), "237.1: the card is not at the top of the issue"
>      assert_open("237.1", saved, TRICKY)
> -    again = run_card(monkeypatch, github, saved) or saved
> +    again = run_card(monkeypatch, github, saved)
> +    assert again is not None, "237.1: the second card run saved nothing"
>      assert_open("237.1", again, TRICKY)
>      assert below(again) == below(

**Agent:** I'm checking whether an existing test would break once the plan's "don't save an unchanged card" rule is built.

`12. Bash`
```
cd /tmp/wt; git diff main 386c1ce -- tests/test_open_ask.py | head; cat > /tmp/probe_test.py <<'EOF'
import sys,os
sys.path.insert(0,"/tmp/wt/tests"); sys.path.insert(0,"/tmp/wt")
from test_body import TRICKY, github, run_card  # noqa
def test_probe(monkeypatch, github):
    s = run_card(monkeypatch, github, TRICKY)
    a = run_card(monkeypatch, github, s)
    print("SAME" if a == s else "DIFF")
    s2 = run_card(monkeypatch, github, TRICKY.replace("x","x"))
EOF
cp /tmp/probe_test.py tests/test_zz_probe.py; python3 -m pytest -q -s tests/test_zz_probe.py 2>&1 | grep -E "SAME|DIFF|passed|failed|Error"; rm tests/test_zz_probe.py
```

> diff --git a/tests/test_open_ask.py b/tests/test_open_ask.py
> index 1bf8b9a..950cfaa 100644
> --- a/tests/test_open_ask.py
> +++ b/tests/test_open_ask.py
> @@ -1,10 +1,11 @@
> -"""The owner's folded text is never changed by a redraw, nor read as the plan.
> +"""The owner's ask reads open on the issue they wrote, folded only where it is quoted from somewhere else.
>  
> -Issue #237, story 4 of #230, opened the owner's ask below the card; issue #373 folds every ask again under a closed
> -`<details><summary>Original issue</summary>` (tests/test_card_folds.py proves that). What #237 kept still holds: an
> SAME
> 1 passed in 0.03s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`13. Bash`
```
cd /tmp/wt; git checkout -q tests/test_open_ask.py 2>/dev/null; grep -n "again\|run_card(monkeypatch, github, saved\|is not None" tests/test_open_ask.py tests/test_card_folds.py tests/test_card_records.py tests/test_card_bullets.py tests/test_summary_caps.py | head -30
```

> tests/test_open_ask.py:3:Issue #237, story 4 of #230, opened the owner's ask below the card; issue #373 folds every ask again under a closed
> tests/test_open_ask.py:57:    Draws a story body the way code files a split's sub-issue, redraws it fresh and again, and checks the quoted
> tests/test_open_ask.py:64:    again = body.redraw(new, "another card")
> tests/test_open_ask.py:65:    assert_folded("237.3", again, quoted)
> tests/test_open_ask.py:66:    assert below(again) == below(new), "237.3: a redraw changed the part below the marker of a split's story"
> tests/test_open_ask.py:71:    """A split's sub-issue already folded today stays folded when the card is drawn again.
> tests/test_open_ask.py:78:    assert saved is not None, "237.3: the card saved nothing on a split's story"
> tests/test_open_ask.py:82:    assert owners is not None, "237.3: the card saved nothing on an owner's ask"
> tests/test_open_ask.py:94:    assert saved is not None, "237.3: the card saved nothing on a fresh split story"
> tests/test_open_ask.py:97:    assert owners is not None, "237.3: the card saved nothing on an owner's ask"
> tests/test_card_folds.py:165:    one with the owner's own fold) fresh and again, and checks each sits byte for byte inside one closed Original
> tests/test_card_folds.py:172:        again = body.redraw(new, "another card")
> tests/test_card_folds.py:173:        assert_folded("373.3", again, ask)
> tests/test_card_folds.py:199:        assert saved is not None, "373.3: the card saved nothing on the is

`14. Bash`
```
cd /tmp/wt; sed -n 225,262p tests/test_card_folds.py; sed -n 340,368p tests/test_card_folds.py; grep -n "changed_only\|def main\|CARD_SWEEP\|unchanged" dokima/card.py | head -30
```

> # 373.3: the PR card carries the same Original issue fold, so the issue and PR cards stay identical
> 
> PR = 5
> 
> 
> def draw_both(monkeypatch, github, current, pr_text, changed_only=False):
>     """Run the card's draw on issue 40 and its open PR 5, returning both saved bodies.
> 
>     Returns (the issue body saved, the PR description written), each None when not written. GitHub is faked: the issue's text is `current`, the PR's description `pr_text`, and the card is drawn from one
>     plan record, as tests/test_body.py run_card does."""
>     issue = {"number": 40, "title": "t", "url": SRC, "approved_at": None, "changes": [], "plan": None,
>              "current_body": current, "body": current}
>     pr = {"number": PR, "merged": False, "state": "open", "body": pr_text, "head": {"sha": "abc", "ref": "try/issue-40"}}
>     found = {"recs": [rec("planner", **plan_of())], "pr": pr, "check_runs": [], "reviews": [], "owners": {"boss"},
>              "tests": {}, "worker": None}
>     monkeypatch.setattr(card.plan, "fetch_issue", lambda repo, n: issue)
>     monkeypatch.setattr(card, "gather", lambda repo, n, p: dict(found))
>     monkeypatch.setattr(card, "github_links", lambda repo, n, cache: {"blocked_by": [], "blocks": [], "loop": []})
>     monkeypatch.setattr(card, "their_links", lambda *a, **k: {"relates_to": []})
>     saves, calls = len(github.saves), len(github.calls)
>     card.draw(REPO, 40, PR, changed_only=changed_only)
>     written = [text_of(c, {}) for c in github.calls[calls:] if "PATCH" in c and

`15. Bash`
```
cd /tmp/wt; cat > tests/test_zz_probe.py <<'EOF'
from test_card_folds import *  # noqa
from test_body import github  # noqa
def test_probe(monkeypatch, github):
    ask = "This fixes #99.\nCloses: #12 and resolved o/r#7, see #5.\n"
    saved, pr_text = draw_both(monkeypatch, github, ask, "Closes #40")
    _, again = draw_both(monkeypatch, github, saved, pr_text)
    print("PRSAME" if again == pr_text else "PRDIFF")
    s2, _ = draw_both(monkeypatch, github, saved, pr_text)
    print("ISSUE-SAVED-AGAIN" if s2 is not None else "issue none")
EOF
python3 -m pytest -q -s tests/test_zz_probe.py 2>&1 | grep -E "SAME|DIFF|ISSUE|none|passed|failed|Error"; rm tests/test_zz_probe.py
```

> PRSAME
> ISSUE-SAVED-AGAIN
> 12 passed in 0.07s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The plan's card rule would break an existing test that the plan doesn't list. I'm trying a rough version of the rule to find every such test.

`16. Bash`
```
cd /tmp/wt; git show try/issue-380:tests/test_body.py > tests/test_body.py; sed -n 829,835p dokima/card.py; sed -i '829s/changed_only=False/changed_only=True/' dokima/card.py; sed -n 829p dokima/card.py; timeout 1200 python3 -m pytest -q -x -p no:cacheprovider tests --deselect tests/test_quiet_board.py 2>&1 | tail -3; timeout 1800 python3 -m pytest -q tests 2>&1 | grep -E "^FAILED|passed|failed" | grep -v test_quiet_board | cut -c1-250
```

> def draw(repo, number, pr_number, plans=None, noted=None, cache=None, changed_only=False):
>     """Write the card at the top of the issue and its PR.
> 
>     Returns the blocking links and loop its card showed before and shows now. With `changed_only`, a card that
>     already shows what it would be drawn as is not rewritten.
>     `plans` gives the links of a plan approved just now, by issue (see their_links). `noted` adds (True) or removes
>     (False) issues from the index of those whose approved plans link here. The Blocked by and Blocks lines are
> def draw(repo, number, pr_number, plans=None, noted=None, cache=None, changed_only=True):
> ........................................................................ [ 93%]
> ......ss.sss.................................ss.................s        [100%]
> 851 passed, 78 skipped, 12 deselected in 187.84s (0:03:07)
> 10 failed, 853 passed, 78 skipped in 196.10s (0:03:16)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`17. Bash`
```
cd /tmp/wt; git checkout -q dokima/card.py; sed -i '854s/not (changed_only and shows(current, top))/not shows(current, top)/; 860s/not (changed_only and pr_body/not (pr_body/' dokima/card.py; sed -n '854p;860p' dokima/card.py; timeout 1800 python3 -m pytest -q tests 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-250
```

> if not shows(current, top) and body.save(repo, number, current, top):
>     if pr and not (pr_body(top, pr.get("body"), ask) == (pr.get("body") or "")):
> FAILED tests/test_card_folds.py::test_the_owners_closing_words_on_the_pr_close_nothing - AssertionError: 373.5: a second redraw lost the PR's own Closes #40 or picked up the owner's:
> FAILED tests/test_new_issue_card.py::test_a_new_issues_card_is_not_rewritten_when_nothing_changed - AssertionError: 371.2: redrawing a new issue's card changed its body
> FAILED tests/test_open_until_planned.py::test_an_open_new_issue_is_not_rewritten_when_nothing_changed - AssertionError: 407.1: redrawing a new issue's card changed its body
> FAILED tests/test_open_until_planned.py::test_a_split_story_stays_folded_before_its_own_plan - AssertionError: 407.3: redrawing a split story's card changed its body
> FAILED tests/test_open_until_planned.py::test_the_owners_text_is_kept_or_the_save_refused - AssertionError: 407.4: a save of 'My ask.\n\n<!-- dokima-done -->\nmy own line' was neither made nor refused with a comment on the issue
> FAILED tests/test_quiet_board.py::test_events_that_cannot_move_a_card_do_not_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issue_comment event, with no run=true or run=false
> FAILED tests/test_quiet_board.py::test_events_that_can_move_a_card_still_run_the_board_update - AssertionError: 380.1: the queue step wrote {'group': 'board-57'} to GITHUB_OUTPUT on a issues

`18. Bash`
```
cd /tmp/wt; python3 -m pytest -q tests/test_new_issue_card.py::test_a_new_issues_card_is_not_rewritten_when_nothing_changed tests/test_open_until_planned.py::test_the_owners_text_is_kept_or_the_save_refused 2>&1 | grep -E "Error|assert" | head -12; grep -n "def shows" -A12 dokima/card.py
```

> assert_new_issue_layout("371.2", saved, ask, [])
>             assert draw(monkeypatch, github, saved, [], changed_only=True) is None, \
> >           assert draw(monkeypatch, github, saved, []) == saved, "371.2: redrawing a new issue's card changed its body"
> E           AssertionError: 371.2: redrawing a new issue's card changed its body
> E           assert None == '<!-- dokima-card -->\n<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->\n**Backlog**\n\nhttps://.../r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval'
> /tmp/wt/tests/test_new_issue_card.py:175: AssertionError
> >                   assert len(github.comments) > comments, \
> E                   AssertionError: 407.4: a save of 'My ask.\n\n<!-- dokima-done -->\nmy own line' was neither made nor refused with a comment on the issue
> E                   assert 0 > 0
> /tmp/wt/tests/test_open_until_planned.py:208: AssertionError
> FAILED tests/test_new_issue_card.py::test_a_new_issues_card_is_not_rewritten_when_nothing_changed - AssertionError: 371.2: redrawing a new issue's card changed its body
> assert None == '<!-- dokima-card -->\n<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->\n**Backlog**\n\nhttps://.../r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval'
> 516:def shows(current, top):
> 517-    """True when the issue body already shows `top` above its marke

`19. Bash`
```
cd /tmp/wt; git checkout -q dokima/card.py; sed -n 812,828p dokima/card.py; grep -n "draw(" dokima/card.py | head
```

> def main():
>     if sys.argv[1:2] == ["gallery"] and len(sys.argv) == 3:
>         gallery(os.environ.get("REPO") or "dokima-dev/dokima", sys.argv[2])
>         return
>     repo = os.environ["REPO"]
>     if not os.environ.get("ISSUE_NUMBER") and os.environ.get("GITHUB_EVENT_NAME") == "schedule":
>         sys.exit(1 if sweep(repo) else 0)
>     number, pr_number = find_work(repo)
>     if not number:
>         print("No issue for this event; nothing to write.")
>         return
>     cache = {}
>     before, now = draw(repo, number, pr_number, cache=cache)
>     if follow(repo, number, before, now, cache):
>         sys.exit(1)
> 
> 
> 519:        return body.redraw(current, top) == current
> 699:                draw(repo, n, issue_pr(repo, n), cache=cache)
> 761:            draw(repo, n, pr_number or issue_pr(repo, n), cache=cache, changed_only=True)
> 824:    before, now = draw(repo, number, pr_number, cache=cache)
> 829:def draw(repo, number, pr_number, plans=None, noted=None, cache=None, changed_only=False):
> Shell cwd was reset to /home/runner/work/dokima/dokima

`20. Bash`
```
cd /tmp/wt; sed -i '824s/cache=cache)/cache=cache, changed_only=True)/' dokima/card.py; sed -n 824p dokima/card.py; timeout 1800 python3 -m pytest -q tests 2>&1 | grep -E "^FAILED|passed|failed" | grep -v quiet_board | cut -c1-250; python3 -m pytest -q tests/test_quiet_board.py 2>&1 | grep -E "380.4|passed|failed"|cut -c1-200
```

> before, now = draw(repo, number, pr_number, cache=cache, changed_only=True)
> 10 failed, 853 passed, 78 skipped in 189.92s (0:03:09)
> 10 failed, 2 passed in 6.32s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`21. Bash`
```
cd /tmp/wt; sed -n 680,700p dokima/card.py; git checkout -q dokima/card.py tests/test_body.py
```

> items = as_items(steps, owner)
>         found = {"recs": agent.records(items), "items": items, "pr": pr_, "check_runs": check_runs, "reviews": [],
>                  "owners": {owner}, "tests": {}, "worker": worker, "children": children}
>         with open(os.path.join(out, f"{name}.md"), "w") as f:
>             f.write(render(repo, issue, found) + "\n")
>         print(f"Drew {name}.md")
> 
> 
> def refresh(repo, numbers, cache, bodies=None):
>     """Redraw each card whose blocking links or loop on GitHub differ from what it shows.
> 
>     One that cannot be updated is named in the run and the others still go on; returns how many failed."""
>     failed = 0
>     for n in numbers:
>         try:
>             text = (bodies or {}).get(n)
>             if text is None:
>                 text = json.loads(gh("api", f"repos/{repo}/issues/{n}")).get("body") or ""
>             if github_links(repo, n, cache) != shown_links(text):
>                 draw(repo, n, issue_pr(repo, n), cache=cache)
>         except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** All 12 new tests fail today for the right reason, on this branch and on current main. I'm writing the hand-back now.

`22. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Replanned the issue after the owner's /plan, with five criteria and twelve new tests in tests/test_quiet_board.py.",
   "Extended the card rule to the pull request: a card run writes the issue's card and the pull request's card only where what it draws differs."
  ],
  "decided": [
   "card.yml keeps its triggers, because a blocked-by link added by hand has no event of its own; such a run now writes nothing when the cards are current.",
   "A review or line note is judged from the name of the reviews run that carries it to board.yml; a run named any other way still updates the board."
  ],
  "open": [
   "No questions for the owner."
  ]
 },
 "verdict": "approve",
 "summary": "The plan keeps every ask of the owner, and each of its twelve new tests fails today because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The board is updated only when an event can change an item's column or pills", "source": "https://github.com/dokima-dev/dokima/issues/380", "criterion": "380.1"},
  {"ask": "Yes, update the board only when the column can change", "source": "https://github.com/dokima-dev/dokima/issues/380", "criterion": "380.1"},
  {"ask": "An event that cannot change the column or a pill (for example an ordinary comment, a review comment, or a check run that is not a required check) does not run the board update.", "source": "https://github.com/dokima-dev/dokima/issues/380", "criterion": "380.1"},
  {"ask": "a burst of events on one issue within a minute becomes one update", "source": "https://github.com/dokima-dev/dokima/issues/380", "criterion": "380.2"},
  {"ask": "Events about one issue that arrive close together cause one board update for that issue, not one each.", "source": "https://github.com/dokima-dev/dokima/issues/380", "criterion": "380.2"},
  {"ask": "The 15-minute sweep stays as the safety net, so a skipped event never leaves
```

> exit 0

**Agent:** I approved the plan for [#380](https://github.com/dokima-dev/dokima/issues/380) (board updates only when a card can change, and a burst becomes one update), with no blockers. The hand-back is at `/tmp/dokima-out/review.json` and passes both checks.

- **The owner's asks:** I found eight in the issue, and each one maps to a criterion. "Run it on autopilot" is an instruction for how to run this issue, not something to build, so I left it off the list.
- **New tests:** all 12 fail today because the feature is missing, not because of a setup error. That holds both on this branch and on current main. This branch is behind main, but merging the two has no conflicts.
- **The rule against saving an unchanged card:** I worried that this rule would break older card tests that the plan doesn't list. So I made the simplest change that does it (the card run skips saving a card that hasn't changed) and ran the whole suite. Both of the plan's tests for this rule passed, and no older test broke. A broader version of the change does break several older tests, starting with `tests/test_card_folds.py`. The worker would see those failures, and the simple version avoids them.
- **Gap, not a blocker:** the only command tested on the pull request is `/review`. A filter that missed `/work` or `/plan` said there would not be caught. The plan grade counts thin coverage like this as never a blocker.

The plan does touch `dokima/card.py`, `board.yml` and `reviews.yml`, which AGENTS.md forbids unless the issue asks. I accepted this because the issue explicitly asks to change when board and card updates run, and that can't be done without them.
