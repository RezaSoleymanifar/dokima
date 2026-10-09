# reviewer (plan) for #315

Run: https://github.com/dokima-dev/dokima/actions/runs/37891005510

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (69.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/78323b9a-86c9-41e0-baba-96ee01a4350e/tool-results/bax81mduv.txt
> 
> Preview (first 2KB):
> .:
> total 96
> drwxr-xr-x  3 runner runner  4096 Oct  9 05:57 .
> drwxrwxrwt 18 root   root    4096 Oct  9 05:57 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 05:57 in
> -rw-r--r--  1 runner runner 69853 Oct  9 05:57 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 05:57 open_blockers.json
> -rw-r--r--  1 runner runner  4409 Oct  9 05:57 plan.json
> 
> in:
> total 56
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:57 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:57 ..
> -rw-r--r-- 1 runner runner 4500 Oct  9 05:57 01-planner.json
> -rw-r--r-- 1 runner runner 4836 Oct  9 05:57 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5358 Oct  9 05:57 03-planner.json
> -rw-r--r-- 1 runner runner 3159 Oct  9 05:57 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1943 Oct  9 05:57 05-worker.json
> -rw-r--r-- 1 runner runner 3212 Oct  9 05:57 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner  357 Oct  9 05:57 07-updater.json
> -rw-r--r-- 1 runner runner 5048 Oct  9 05:57 08-planner.json
> # Issue #315: The PR card is redrawn after merge and shows the true Definition of Done
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Cards on an issue and its pull request are redrawn whenever what they show changes, including after merge, and stale merged cards are fixed once.
> 
> **Rev

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; echo; grep -n "^## \|^### \|^---\|dokima-owner\|^\*\*@" issue.md | head -80
```

> {
>  "kind": "user_story",
>  "summary": "Cards on an issue and its pull request are redrawn whenever what they show changes, including after merge, and stale merged cards are fixed once.",
>  "user_story": "The owner can trust the card on any issue or pull request, merged or not, to show where it truly stands.",
>  "acceptance_criteria": [
>   {
>    "text": "The issue and pull request cards are redrawn when a check finishes, an agent posts a record, the owner approves or it merges. The card's own edit of or comment on the issue, and the commands run a command in an issue comment starts, redraw nothing; a person's comment on an issue still redraws its card, as #254 set.",
>    "source": "https://github.com/dokima-dev/dokima/issues/315"
>   },
>   {
>    "text": "After a code owner merges, both cards say Merged with All tests, Code review and Owner approval passed. Code review is found on the pull request, where the review's record is, and links to its run; the owner's merge counts as Owner approval and links to the pull request.",
>    "source": "https://github.com/dokima-dev/dokima/issues/315"
>   },
>   {
>    "text": "On each criterion, only its first sentence links to its check. The explanation after it reads as plain text, and a criterion with no check links nothing.",
>    "source": "https://github.com/dokima-dev/dokima/issues/315"
>   },
>   {
>    "text": "When this change reaches main, each merged pull request whose card is stale is redrawn once, on it and its issue. Cards that already match a fresh d

`3. Bash`
```
cd /tmp/pack; sed -n 1,90p issue.md; sed -n 240,262p issue.md; sed -n 705,790p issue.md; sed -n 875,930p issue.md; sed -n 1080,1200p issue.md
```

> # Issue #315: The PR card is redrawn after merge and shows the true Definition of Done
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Cards on an issue and its pull request are redrawn whenever what they show changes, including after merge, and stale merged cards are fixed once.
> 
> **Review**
> 
> [issue #315](https://github.com/dokima-dev/dokima/issues/315) · [PR #325](https://github.com/dokima-dev/dokima/pull/325) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/325/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #183, #292, #254, #106
> 
> **User story:** The owner can trust the card on any issue or pull request, merged or not, to show where it truly stands.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Acceptance criterion:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37889980610/job/113688525128">The issue and pull request cards

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['04-reviewer-plan.json','06-reviewer-pr.json','08-planner.json']:
  d=json.load(open(f)); print(f); print(json.dumps(d.get('handback'),indent=1)[:5000])
"
```

> 04-reviewer-plan.json
> {
>  "previous_step": {
>   "did": [
>    "Added an owner's edit of issue #40 to the queue test, which now fails when the card's own edit of issue #40 or a command waits in the same queue as that redraw."
>   ],
>   "decided": [
>    "The requirement now says each issue and pull request has its own redraw queue, and a waiting redraw is replaced only by a newer redraw of the same issue or pull request, never by another one's redraw, the card's own edit of the issue or a command."
>   ],
>   "open": []
>  },
>  "verdict": "approve",
>  "summary": "Every ask is planned, and the queue test now fails when the card's own issue edit would cancel a waiting redraw of that issue.",
>  "blockers": [],
>  "notes": [
>   {
>    "text": "The approval case in 315.1 relies on the commands workflow finishing after a pull request review, so the worker should keep card.yml listening to the commands workflow, not to pull_request_review.",
>    "evidence": "tests/test_card_redraw.py 315.1 approval case uses workflow_run('commands', event='pull_request_review'); the plan's out of scope names this route."
>   }
>  ],
>  "outside_plan": [],
>  "resolved": [
>   "B1"
>  ],
>  "issues_found": [],
>  "asks": [
>   {
>    "ask": "A card is redrawn whenever anything it shows changes: a check finishing, a review record, an approval, a merge.",
>    "source": "https://github.com/dokima-dev/dokima/issues/315",
>    "criterion": "315.1"
>   },
>   {
>    "ask": "Its last drawing always matches the truth, including after merge.",
>    "source": "http

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --graph; git branch -a; git merge-base --is-ancestor 65edcee HEAD && echo has-main; git show --stat HEAD | head -20; git show --stat HEAD~1 | head
```

> * c7546fc planner for #315 (run 37890525484)
> * 58c5fee worker for #315 (run 37888164614)
> *   a5058de Merge remote-tracking branch 'origin/main' into try/issue-315
> |\  
> | * 930523a The Blocker pill is computed from blocked-by links, not set by hand (#317)
> * | 15432fc planner for #315 (run 37887845325)
> * | 0f8ea73 planner for #315 (run 37885551794)
> |/  
> * 02a6d8d A drift audit reports what is off on one pinned Setup issue, and stays silent otherwise (#312)
> * e1a21e7 Three kinds of raise and one table of who raises to whom, checked by code (#304)
>   main
> * try/issue-315
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
>   remotes/origin/issue-116-board-sync
>   remotes/origin/issue-121-needs-you
>   remotes/origin/issue-126-keys-from-main
>   remotes/origin/issue-138-prompt
>   remotes/origin/issue-40-app
>   remotes/origin/issue-46-approve
>   remotes/origin/issue-54-plan
>   remotes/origin/issue-60-wrap
>   remotes/origin/issue-63-latest
>   remotes/origin/issue-67-label
>   remotes/origin/issue-74-layout
>   remotes/origin/issue-78-design
>   remotes/origin/issue-80-planner
>   remotes/origin/issue-81-build-on-main
>   remotes/origin/issue-89-planner-prompt
>   remotes/origin/issue-90-assign
>   remotes/origin/issue-93-terms
>   remotes/origin/logs
>   remotes/

**Agent:** I'm reviewing the re-planned tests for #315 against the new main (#307), which conflicted with the PR.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -5 origin/main; git log --oneline -3 main; git cat-file -t 65edcee 2>&1; git show c7546fc -- tests/test_card_redraw.py
```

> 65edcee A link added or removed by hand on GitHub updates the cards of both issues (#307)
> 1b0cda6 The audit runs once a day in the background, and on the Run workflow button (#318)
> 930523a The Blocker pill is computed from blocked-by links, not set by hand (#317)
> 02a6d8d A drift audit reports what is off on one pinned Setup issue, and stays silent otherwise (#312)
> e1a21e7 Three kinds of raise and one table of who raises to whom, checked by code (#304)
> 65edcee A link added or removed by hand on GitHub updates the cards of both issues (#307)
> 1b0cda6 The audit runs once a day in the background, and on the Run workflow button (#318)
> 930523a The Blocker pill is computed from blocked-by links, not set by hand (#317)
> commit
> commit c7546fce68dcbca68e49a55aafb5f813a15433e5
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:56:29 2026 +0000
> 
>     planner for #315 (run 37890525484)
> 
> diff --git a/tests/test_card_redraw.py b/tests/test_card_redraw.py
> index b1dd06a..71be2aa 100644
> --- a/tests/test_card_redraw.py
> +++ b/tests/test_card_redraw.py
> @@ -20,6 +20,7 @@ dokima.body, and answers what the card reads today:
>      gh api repos/o/r/contents/.github/CODEOWNERS    "* @boss"; any other file is missing
>      gh api repos/o/r/actions/workflows/.../runs     no runs
>      gh api repos/o/r/issues/N  [.../events]
> +    gh api repos/o/r/issues/N/dependencies/blocked_by|blocking --paginate   no blocked-by links
>      gh api -X PATCH repos/o/r/pulls/

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff 930523a 65edcee --stat; git show 65edcee:.github/workflows/card.yml
```

> .github/workflows/audit.yml   |  33 +++
>  .github/workflows/card.yml    |  19 +-
>  AGENTS.md                     |   2 +-
>  dokima/card.py                | 174 +++++++++++-
>  tests/test_audit_workflow.py  | 263 ++++++++++++++++++
>  tests/test_autopilot_close.py |   6 +-
>  tests/test_card.py            |   9 +-
>  tests/test_card_guard.py      |  17 +-
>  tests/test_hand_links.py      | 601 ++++++++++++++++++++++++++++++++++++++++++
>  9 files changed, 1099 insertions(+), 25 deletions(-)
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
>     # request draws no issue 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt-main; git worktree add -q /tmp/wt-main origin/main 2>&1 | tail -1; cp tests/test_card_redraw.py /tmp/wt-main/tests/; cd /tmp/wt-main; timeout 600 python3 -m pytest -q tests/test_card_redraw.py 2>&1 | grep -E "^(FAILED|E   +315|[0-9]+ (passed|failed))|AssertionError: 315|passed|failed" | head -40
```

> assert done_row(g.prs[5]["body"])[2][0] == "passed", \
>                         "315.1: the card redrawn after the owner's Approve does not show Owner approval passed"
> E       AssertionError: 315.1: the owner approved the PR: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E         315.1: the PR merged: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E         315.1: the code review's record was posted: agent.yml runs no card redraw after it posts the run's record
> _ test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed _
>     def test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed(record_property, monkeypatch,
>         """After the owner merges, both cards say Merged with every Definition of Done item passed.
>         Merged; All tests must link its check; Code review must be passed and link the review's run; Owner approval
>         must be passed and link the PR. The same merge by someone who is not a code owner must not show Owner approval
>         passed. Proves 315.2."""
> E       AssertionError: 315.2: the owner merged PR #5: the card was not redrawn on issue #40 (writes: [], calls GitHub refused: [])
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the criterion reads
> E       AssertionError: 315.3: the non-functional requirement reads <a href="https://github.com/o/r/actions/runs/9/j

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def groups\|def run_workflow\|def test_\|person\|User\")" tests/test_card_redraw.py | head -40; sed -n 575,680p tests/test_card_redraw.py
```

> 582:def test_the_card_is_redrawn_on_both_pages_whenever_something_it_shows_changes(record_property, monkeypatch, tmp_path):
> 639:def test_after_the_owner_merges_both_cards_show_every_definition_of_done_item_passed(record_property, monkeypatch,
> 700:def test_only_the_criterion_sentence_links_to_its_run(record_property, text, sentence, rest):
> 713:def test_the_sentence_link_holds_for_non_functional_requirements_and_no_check_means_no_link(record_property):
> 762:def test_when_this_lands_every_merged_pr_with_a_stale_card_is_redrawn_once(record_property, monkeypatch, tmp_path):
> 789:def test_only_mains_copy_of_the_card_code_ever_draws_a_card(record_property, tmp_path):
> 812:def groups(events):
> 829:def test_a_redraw_waiting_its_turn_is_never_dropped_for_an_unrelated_run(record_property):
> 849:              "owner's edit of issue #41": ("issues", issue_edit(41, "User")),
> 850:              "owner's edit of issue #40": ("issues", issue_edit(40, "User")),
> 851:              "owner's comment on issue #42": ("issue_comment", issue_comment(42, "User")),
>         run_card(monkeypatch, args, {k: env[k] for k in CARD_ENV if k in env})
>         return None
>     return f"agent.yml's steps {[n for n, _ in found]} never ran the card code"
> 
> 
> # 315.1: the card is redrawn whenever anything it shows changes
> 
> def test_the_card_is_redrawn_on_both_pages_whenever_something_it_shows_changes(record_property, monkeypatch, tmp_path):
>     """Both cards are redrawn after a check, a record, an approval and a merge.
> 
>     R

`10. Bash`
```
cd /tmp/wt-main; grep -rn "issue_comment" tests/*.py | grep -v test_card_redraw | head -20
```

> tests/test_autopilot_board.py:329:    board.sync("issue_comment", comment_event(57, "**Planner question**\n\nWhich?", [LABEL]), SPEC, REPO)
> tests/test_autopilot.py:133:        github = Ctx(event_name="issue_comment", actor=self.actor, event=event, run_id="42", run_attempt="1",
> tests/test_autopilot.py:158:                results[name], outputs[name] = self.run_job(name, job, ctx, "issue_comment",
> tests/test_autopilot_river.py:119:        github = Ctx(event_name="issue_comment", actor=OWNER, event=event, run_id="42", run_attempt="1",
> tests/test_autopilot_river.py:143:                results[name], outputs[name] = self.run_job(name, job, ctx, "issue_comment",
> tests/test_board.py:29:        assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": body}}) == [("issue", 5, "Plan", True)]
> tests/test_board.py:30:    assert board.decide("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": YOU, "body": "Plan written above"}}) == [], "116.1: a person's comment moved the board"
> tests/test_board.py:108:    board.sync("issue_comment", {"action": "created", "issue": {"number": 5}, "comment": {"user": BOT, "body": "**Planner question**"}}, "dokima-dev/1", "o/r", q=gh)
> tests/test_automerge.py:449:        github = Ctx(event_name="issue_comment", actor=OWNER, event=event, run_id="42", run_attempt="1",
> tests/test_automerge.py:470:                results[name], outputs[name] = self.run_job(f"{name}-{len(self.

`11. Bash`
```
cd /tmp/wt-main; sed -n 1,40p tests/test_hand_links.py; grep -n "card.yml\|def test_" tests/test_hand_links.py tests/test_card_guard.py | head -40
```

> """A blocked-by link added or removed by hand shows on both cards (#254).
> 
> Story 5 of #231.
> 
> GitHub Actions has no event for a blocked-by link being added or removed, so, as the owner answered on #254, the cards
> update on every event GitHub does announce on either issue, with a schedule only as a backstop. card.yml runs
> `python3 dokima/card.py` on every issues and issue_comment event a person causes on an issue (ISSUE_NUMBER is that
> issue, GITHUB_EVENT_NAME issues or issue_comment): it redraws that issue's card and the card of every issue it blocks
> or is blocked by, on GitHub now or on its card before, so a link removed by hand leaves the other card too. card.yml
> also runs on a cron (GITHUB_EVENT_NAME=schedule, no ISSUE_NUMBER), and then card.py sweeps every open issue. Both read
> GitHub's own blocked-by links (GET repos/o/r/issues/N/dependencies/blocked_by and .../blocking) and rewrite another
> issue's card only when its blocking links, or loop of issues blocking each other, differ from what its card shows.
> Every redraw draws the Blocked by and Blocks lines from GitHub's links read right then.
> 
> Every test runs the real `python3 dokima/card.py` as a subprocess against the fake GitHub of
> tests/test_plan_links_recorded.py (a `gh` first on PATH keeping its state in one JSON file), extended here with two
> things: GitHub failing to list one issue's blocked-by links (state "unreadable": {issue: GitHub's error}), and a
> project board reached through dokima.board.Board's own GraphQL call

**Agent:** Checking that the new main's existing card tests (from #307) and the plan's tests can both pass together.

`12. Bash`
```
cd /tmp/wt-main; sed -n 430,560p tests/test_hand_links.py
```

> out |= set(range(lo, hi + 1, int(step) if step else 1))
>     return sorted(out)
> 
> 
> def on_block(text):
>     """The lines of card.yml's `on:` block."""
>     m = re.search(r"^on:\n((?:[ \t]+.*\n|\n)+)", text, re.M)
>     return m.group(1) if m else ""
> 
> 
> def trigger(on, name):
>     """The activity types card.yml lists for one trigger.
> 
>     None when the trigger is absent, "all" when it lists no types."""
>     lines = on.splitlines()
>     for i, line in enumerate(lines):
>         m = re.match(r"^(\s+)" + re.escape(name) + r":\s*(\{\}|null)?\s*$", line)
>         if not m:
>             continue
>         indent, block = len(m.group(1)), []
>         for nxt in lines[i + 1:]:
>             if nxt.strip() and len(nxt) - len(nxt.lstrip()) <= indent:
>                 break
>             block.append(nxt)
>         text = "\n".join(block)
>         if "types:" not in text:
>             return "all"
>         inline = re.search(r"types:\s*\[([^\]]*)\]", text)
>         if inline:
>             return {t.strip().strip("'\"") for t in inline.group(1).split(",") if t.strip()}
>         return set(re.findall(r"^\s*-\s*['\"]?(\w+)", text.split("types:", 1)[1], re.M))
>     return None
> 
> 
> def job_if(text):
>     """card.yml's job condition, a one-line GitHub expression, as a function of the `github` context.
> 
>     Reads the first `if:` under `jobs:` and turns GitHub's ==, !=, &&, || and ! on context paths and quoted strings
>     into Python; a missing path is null, as on GitHub. A job with no `if:` runs on every event."""
>     jobs = 

`13. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_card_redraw.py 2>&1 | grep -E "^E  .*315|passed|failed" | head
```

> 9 passed in 0.24s

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 780,830p tests/test_card_redraw.py; grep -n "def concurrency\|def job_runs\|def evaluate\|def expr" tests/test_card_redraw.py; git diff a5058de 58c5fee -- .github/workflows/card.yml
```

> assert block(g.issues[40]["body"]) == block(expected.issues[40]["body"]), "315.4: issue #40's card is not a fresh drawing"
>     assert g.prs[5]["body"].endswith("Closes #40"), "315.4: PR #5 lost its line closing the issue"
>     g.writes.clear()
>     again = backfill_by_push(monkeypatch, g)
>     assert again == [], f"315.4: running the redraw a second time wrote {again}; a card already right is left alone"
> 
> 
> # 315.5: main's copy draws every card, and no waiting redraw is dropped
> 
> def test_only_mains_copy_of_the_card_code_ever_draws_a_card(record_property, tmp_path):
>     """Only main's copy of the card code draws a card, never a pull request's own.
> 
>     card.yml must not listen to events that run a pull request's copy of the workflow (pull_request,
>     pull_request_review, pull_request_review_comment) and must never check out a pull request's code; agent.yml's
>     redraw after a record must run the runtime copied from main, not the branch it has checked out. Proves 315.5."""
>     record_property("proves", "315.5")
>     wf = card_yml()
>     on = wf.get("on")
>     for ev in ("pull_request", "pull_request_review", "pull_request_review_comment"):
>         assert listed(on, ev) is None, f"315.5: card.yml listens to {ev}, which runs the pull request's own copy"
>     for job in (wf.get("jobs") or {}).values():
>         for step in job.get("steps") or []:
>             if "checkout" in str(step.get("uses")):
>                 assert not (step.get("with") or {}).get("ref"), \
>                     f"315

**Agent:** The re-plan holds up: all 9 tests fail on the new main for the right reasons. Writing the review.

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Re-planned against the new main after #307, which added redraws on a person's comment and a 15-minute sweep of blocked-by links.",
   "Added to the tests the bot's own comment on the issue, a comment on a pull request, an owner's comment on an issue and the 15-minute sweep."
  ],
  "decided": [
   "The bot's own comment on the issue redraws nothing; a person's comment on an issue still redraws its card, as #254 set.",
   "No waiting redraw is replaced by the 15-minute sweep, the bot's own comment or a comment on a pull request."
  ],
  "open": []
 },
 "verdict": "approve",
 "summary": "The re-plan keeps every ask from the first plan, and adds the comment and 15-minute sweep redraws that #307 brought to main to the queue rule. All nine tests fail on today's main because the feature is missing.",
 "blockers": [],
 "notes": [
  {
   "text": "A person's comment on an issue still redrawing its card (the last clause of 315.1) is proven by #254's own test, not by a test of this plan. The worker must keep that test green when it merges main.",
   "evidence": "tests/test_hand_links.py::test_card_yml_starts_on_every_change_a_person_makes_and_on_a_schedule asserts a person's comment on an issue passes card.yml's job if:, and tests/test_card_redraw.py has no such case."
  },
  {
   "text": "#254's test reads only the first if: under jobs, as one line. If the worker adds the commands-run and merge conditions to the job's if: instead of the step's, that if: has to stay one line or #254's test cannot read it.",
   "evidence": "tests/test_hand_links.py job_if: re.search(r\"^\\s+if:\\s*(.+?)\\s*$\", jobs); the earlier work put those conditions in the step's multi-line if:."
  }
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "A card is redrawn whenever anything it shows changes: a check finishing, a review record, an approval, a merge.", "sourc
```

> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> rc=1

`16. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The re-plan keeps every ask and adds #307's comment and sweep redraws to the queue rule; all nine tests fail on main for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 315 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`17. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The re-plan keeps every ask and adds #307's comment and sweep redraws to the queue rule; all nine tests fail on main as they should."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 315 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-plan for #315, and the hand-back is in `/tmp/dokima-out/review.json`; it passes both checks.

**What changed in the plan:** pull request #325 clashed with main after #307 landed. #307 makes a person's comment on an issue redraw its card and adds a sweep of blocked-by links every 15 minutes. The planner re-planned with those in mind:
- The bot's own comment on the issue now redraws nothing.
- A person's comment on an issue still redraws its card.
- A waiting redraw is never replaced by the 15-minute sweep, the bot's own comment, or a comment on a pull request.

The tests now cover these cases.

**What I checked:**
- **Asks:** all seven of the owner's asks from the issue and their `/plan` comment are still covered, by criteria 315.1–315.5. None is missing.
- **Tests fail today:** I ran the plan's 9 tests against current main (with #307), and all 9 fail because the feature isn't there yet. None fails from a crash, a missing tool or a bad path.
- **Current branch:** the same 9 pass on `try/issue-315`. That branch still holds the worker's earlier code, built on the main from before #307.
- **No clash with #307's test:** the plan's tests don't conflict with `tests/test_hand_links.py`.

**Two notes for the worker:**
- The last part of 315.1 is that a person's comment still redraws the card. Only #254's existing test, `test_card_yml_starts_on_every_change_a_person_makes_and_on_a_schedule`, checks it, not one of this plan's tests. That test has to stay green when the worker merges main.
- That same test reads the first `if:` under `jobs` in `card.yml` as a single line. If the worker moves the new conditions from the step's `if:` (where the earlier work put them) into the job's `if:`, that line must stay on one line or the test can't read it.

No blockers were open from earlier rounds, and I found no problems outside this issue.
