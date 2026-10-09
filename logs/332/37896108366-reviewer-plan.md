# reviewer (plan) for #332

Run: https://github.com/dokima-dev/dokima/actions/runs/37896108366

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
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
> **Context:** Split from #330 (rule R2, R3). card.yml runs on finished checks, the worker, issue events and comments, and a 15-minute schedule that only redraws cards whose blocked-by links changed (dokima/card.py, sweep and refresh); it never runs when a PR is merged or closed, so #246's PR card was never rewritten after its merge, and #312's PR card missed a dropped redraw. Its concurrency group is the single 'card' group, so a pending run for one issue is cancelled by the next issue's. card.status() already returns Merged for a merged PR; draw() writes the PR card for an open, merged or closed PR once it is found, but find_work() and the workflow triggers decide whether it is found. This story makes every event about an issue or its PR, and the 15-minute sweep, redraw that issue's card and PR card from state, one queue per issue. Redrawing every closed card every 15 minutes may cost too many API calls; the sweep may compare what a card shows with the state and

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; wc -l tests/test_card_now.py dokima/card.py; cat .github/workflows/card.yml
```

> commit a3ecbb8d5e198785879221e688c870160f0d08d8
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 06:55:14 2026 +0000
> 
>     planner for #332 (run 37893473407)
> 
>  tests/test_card_now.py   | 1248 ++++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_hand_links.py |   24 +-
>  2 files changed, 1259 insertions(+), 13 deletions(-)
>  1248 tests/test_card_now.py
>   721 dokima/card.py
>  1969 total
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
>     # request draws no issue card on it; an issue deleted or move

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_card_now.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|AssertionError|^E " | head -60; timeout 600 python -m pytest -q tests/test_hand_links.py 2>&1 | tail -5
```

> E       AssertionError: 332.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> E       assert False
> E        +  where False = <test_card_now.Run object at 0x7fc57115ba10>.started
> tests/test_card_now.py:863: AssertionError
> E       AssertionError: 332.1: card.yml does not start on pull_request_target synchronize, so the cards are not redrawn
> E       assert False
> E        +  where False = <test_card_now.Run object at 0x7fc570fdb4a0>.started
> tests/test_card_now.py:863: AssertionError
> E       AssertionError: 332.1: card.yml started on issue_comment created but its card job was skipped
> E       assert False
> E        +  where False = card_ran()
> E        +    where card_ran = <test_card_now.Run object at 0x7fc570fdb440>.card_ran
> tests/test_card_now.py:864: AssertionError
> E       AssertionError: 332.1: card.yml does not start on: ['pull_request_target opened', 'pull_request_target edited', 'pull_request_target reopened', 'pull_request_target synchronize', 'pull_request_target closed', 'pull_request_review submitted', 'pull_request_review edited', 'pull_request_review dismissed', 'pull_request_review_comment created', 'pull_request_review_comment edited', 'pull_request_review_comment deleted']
> E       assert not ['pull_request_target opened', 'pull_request_target edited', 'pull_request_target reopened', 'pull_request_target synchronize', 'pull_request_target closed', 'pull_request_review submitted', ...]
> tests/test_card_now.py:993: AssertionError
> E   

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_card_now.py 2>&1 | tail -15; git diff HEAD~1 -- tests/test_hand_links.py
```

> return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
>              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>     File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/subprocess.py", line 571, in run
>       raise CalledProcessError(retcode, process.args,
>   subprocess.CalledProcessError: Command '['gh', 'api', '-X', 'PATCH', 'repos/o/r/pulls/260', '-F', 'body=@pr.md']' returned non-zero exit status 1.
>   
>   
> assert False
>  +  where False = any(<generator object test_an_event_names_the_card_it_cannot_write_fails_and_writes_the_other.<locals>.<genexpr> at 0x7f8007991080>)
> FAILED tests/test_card_now.py::test_runs_started_by_a_pull_request_run_mains_code - AssertionError: 332.7: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> assert False
>  +  where False = <test_card_now.Run object at 0x7f8007b336e0>.started
> FAILED tests/test_card_now.py::test_a_sweep_with_nothing_to_put_right_makes_few_github_calls - AssertionError: 332.8: the first sweep left closed issues or their merged PRs not saying Merged: [246, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428]
> assert not [246, 400, 401, 402, 403, 404, ...]
> 13 failed in 3.54s
> diff --git a/tests/test_hand_links.py b/tests/test_hand_links.py
> index 0005a53..8deee20 100644
> --- a/tests/test_hand_links.py
> +++ b/tests/test_hand_links.py
> @@ -518,9 +51

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,200p tests/test_card_now.py
```

> """Every issue card and PR card is drawn from GitHub's state right now (#332).
> 
> Story 2 of #330. A card used to trust the one event that started its run: card.yml never ran when a pull request was
> merged, closed or reviewed, so #246's PR card kept its open card after the merge, and #312's PR card missed a dropped
> redraw for good. Now any event about an issue or its pull request, and a sweep every 15 minutes, redraws both cards from
> GitHub as it is, each issue in its own queue.
> 
> These tests play card.yml the way GitHub runs it, for one event at a time, against a fake GitHub:
> - The event starts the workflow when card.yml's `on:` lists it (and its activity type, and for workflow_run the
>   workflow that finished). Then every job runs in the order its `needs` allow: a job's `if:` and every `${{ }}` are
>   evaluated with tests/test_start.py's evaluator (github, vars, secrets, needs, steps, env); `uses:` steps are skipped
>   (checkout is noted with the ref it would check out, and the app token step gives a fake token); `run:` steps run with
>   bash, from a copy of this repo's dokima/ and .github/, with a fake `gh` first on PATH. Values a step writes to
>   GITHUB_OUTPUT or GITHUB_ENV are read as KEY=value lines, and a job's `outputs:` reach later jobs through `needs`.
> - Every concurrency group card.yml declares (the workflow's and each job's that runs) is evaluated for the event.
> - Pull request events reach card.yml as pull_request_target (main's copy of the workflow), pull_request_revie

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 200,520p tests/test_card_now.py
```

> def comments_rest(cs):
>     return [{"id": k + 1, "user": {"login": c["login"], "type": "Bot" if c["login"] == BOT_LOGIN else "User"},
>              "body": c["body"], "created_at": c["at"], "updated_at": c["at"]} for k, c in enumerate(cs)]
> 
> 
> def comments_gh(cs):
>     return [{"author": {"login": c["login"]}, "body": c["body"], "createdAt": c["at"]} for c in cs]
> 
> 
> def pr_rest(p):
>     x = pr(p)
>     return {"number": int(p), "id": 800000 + int(p), "node_id": f"PR_{p}", "title": x["title"], "body": x["body"],
>             "state": pr_state(x), "merged": x["merged"], "merged_at": x.get("merged_at"),
>             "merged_by": {"login": x["merged_by"]} if x.get("merged_by") else None, "closed_at": x.get("closed_at"),
>             "head": {"ref": x["head_ref"], "sha": x["sha"]}, "base": {"ref": "main"}, "draft": False,
>             "user": {"login": BOT_LOGIN, "type": "Bot"}, "updated_at": x["updated_at"],
>             "html_url": f"https://github.com/{REPO}/pull/{p}"}
> 
> 
> def pr_gh(p):
>     x = pr(p)
>     return {"number": int(p), "title": x["title"], "body": x["body"],
>             "state": "MERGED" if x["merged"] else pr_state(x).upper(), "headRefName": x["head_ref"],
>             "headRefOid": x["sha"], "baseRefName": "main", "mergedAt": x.get("merged_at"), "closed": pr_state(x) == "closed",
>             "url": f"https://github.com/{REPO}/pull/{p}", "updatedAt": x["updated_at"],
>             "comments": comments_gh(x.get("comments", [])),
>             "reviews": [{"author": {"login": r["login"]}

**Agent:** I'm reading the planner's new tests for #332. All 13 fail today, and I'm checking whether each one fails for the right reason.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 520,880p tests/test_card_now.py
```

> def load(self):
>         """Read the fake GitHub's state back, as the run left it."""
>         self.state = json.load(open(os.path.join(self.dir, "state.json")))
>         return self.state
> 
>     def merge(self, n, p, by=OWNER):
>         """Merge PR p and close issue n on GitHub, redrawing no card."""
>         s = self.load()
>         s["prs"][str(p)].update(state="closed", merged=True, merged_by=by, merged_at="2026-10-09T09:00:00Z",
>                                 closed_at="2026-10-09T09:00:00Z", updated_at="2026-10-09T09:00:00Z")
>         s["issues"][str(n)].update(state="closed", closed_at="2026-10-09T09:00:00Z", updated_at="2026-10-09T09:00:00Z")
>         self.save()
> 
>     def no_pr_card(self, p, n):
>         """Leave PR p with only its closing line, as after a dropped redraw."""
>         s = self.load()
>         s["prs"][str(p)]["body"] = f"Closes #{n}"
>         self.save()
> 
>     def refuse(self, op, n):
>         """GitHub refuses `op` (read-issue, write-issue or write-pr) on n with HTTP 502."""
>         s = self.load()
>         s["refuse"].append({"op": op, "n": n, "error": f"HTTP 502: Server Error (https://api.github.com/repos/o/r/{n})"})
>         self.save()
> 
>     def issue_body(self, n):
>         """Issue n's body as it stands on GitHub."""
>         return self.load()["issues"][str(n)]["body"]
> 
>     def pr_body(self, p):
>         """PR p's body as it stands on GitHub."""
>         return self.load()["prs"][str(p)]["body"]
> 
>     def writes(self, op=None):
>         """Every body or comment the ru

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 880,1248p tests/test_card_now.py
```

> ("the checks finishing", lambda: checks_finished(246, 260)),
> ]
> 
> 
> def test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now(tmp_path, record_property):
>     """Any event about an issue or its PR redraws both cards as GitHub is now.
> 
>     PR #260 is merged and #246 closed on GitHub while both cards still show the old Review card. For each of nine
>     events (the merge by the bot or the owner, the issue closing, a comment on the issue or the PR, an Approve, the
>     bot's review, a note on a line, the checks finishing), on a fresh GitHub, card.yml runs and afterwards #246's card
>     and #260's card are the same card, saying Merged, and the PR keeps its closing line. Proves 332.1."""
>     record_property("proves", "332.1")
>     for what, make in MERGE_EVENTS:
>         hub = Hub(tmp_path / re.sub(r"\W+", "-", what))
>         hub.merge(246, 260)
>         must_redraw(hub, make(), "332.1")
>         issue_card, pr_card = card_of(hub.issue_body(246)), card_of(hub.pr_body(260))
>         assert stage_of(hub.issue_body(246)) == "Merged", \
>             f"332.1: after {what}, #246's card does not say Merged, as GitHub is now: {issue_card!r}"
>         assert stage_of(hub.pr_body(260)) == "Merged", \
>             f"332.1: after {what}, PR #260's card does not say Merged, as GitHub is now: {pr_card!r}"
>         assert issue_card == pr_card, f"332.1: after {what}, #246 and PR #260 show different cards"
>         assert hub.pr_body(260).rstrip().endswith("Closes #246"), \
>             f"33

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -B2 -A8 "pull_request_review" .github/workflows/*.yml | head -80; grep -rn "merge ref\|refs/pull" tests/test_start.py | head
```

> .github/workflows/board.yml-18-  pull_request_target:
> .github/workflows/board.yml-19-    types: [opened, reopened, synchronize, closed]
> .github/workflows/board.yml:20:  pull_request_review:
> .github/workflows/board.yml-21-    types: [submitted]
> .github/workflows/board.yml-22-  workflow_run:
> .github/workflows/board.yml-23-    workflows: [done-whens]
> .github/workflows/board.yml-24-    types: [completed]
> .github/workflows/board.yml-25-permissions:
> .github/workflows/board.yml-26-  contents: read
> .github/workflows/board.yml-27-concurrency:
> .github/workflows/board.yml-28-  group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
> .github/workflows/commands.yml-15-  issue_comment:
> .github/workflows/commands.yml-16-    types: [created]
> .github/workflows/commands.yml:17:  pull_request_review:
> .github/workflows/commands.yml-18-    types: [submitted]
> .github/workflows/commands.yml-19-permissions:
> .github/workflows/commands.yml-20-  contents: read
> .github/workflows/commands.yml-21-  issues: read
> .github/workflows/commands.yml-22-  pull-requests: read
> .github/workflows/commands.yml-23-  actions: read
> .github/workflows/commands.yml-24-jobs:
> .github/workflows/commands.yml-25-  route:

`10. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,80p .github/workflows/board.yml; sed -n 1,15p .github/workflows/commands.yml; grep -n "checkout" -A3 .github/workflows/commands.yml | head -20
```

> name: board
> # Keeps the project board's Status and "Waiting on" current at every stage moment,
> # its Priority Blocker on open issues that block an open issue (from blocked-by links,
> # read on close, reopen and every 15 minutes, since GitHub sends no event for a link),
> # and otherwise in step with the high and parked labels. A code owner's command in a
> # review clears Needs you at once, and every merge sweeps every pill.
> # Rules live in dokima/board.py. Does nothing unless the repo variable DOKIMA_BOARD
> # names a board ("org/number").
> on:
>   issues:
>     types: [labeled, unlabeled, closed, reopened]
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
>   workflow_run:
>     workflows: [done-whens]
>     types: [completed]
> permissions:
>   contents: read
> concurrency:
>   group: board-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
>   cancel-in-progress: false
> jobs:
>   sync:
>     environment: keys
>     if: vars.DOKIMA_BOARD != ''
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.repository.default_branch }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           pyt

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rln "card.yml\|CARD_YML" tests/ ; grep -rn "group: card\|'card'\|\"card\"" tests/*.py | grep -i group | head; timeout 900 python -m pytest -q -x --deselect tests/test_card_now.py -p no:cacheprovider 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bhttc16ji). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Code review\|Owner approval\|All tests\|def " dokima/card.py | head -80
```

> 46:def icon(repo, name, alt=None):
> 52:def field_icon(repo, field):
> 57:def link_lines(repo, links):
> 74:def merged(*many):
> 86:def linked_from(text):
> 98:def their_links(repo, number, sources, plans=None):
> 125:def reason(e):
> 130:def blocking(repo, number, cache):
> 146:def loop_of(repo, number, cache):
> 151:    def by(i):
> 172:def github_links(repo, number, cache):
> 182:def shown_links(text):
> 195:def state(check):
> 204:def circle(repo, st, url=None):
> 210:def fold(title, lines):
> 215:def escape(text):
> 219:def checks_by_key(check_runs):
> 229:def as_items(steps, owner=None):
> 236:def checks_passed(number, h, check_runs):
> 237:    """True when every criterion's check of plan `h`, and All tests, passed on the PR's latest commit."""
> 245:def todo(issue, found, rec):
> 269:def status(issue, found):
> 289:def status_line(repo, stage, todo):
> 295:def child_row(repo, child):
> 304:def links_row(repo, issue, pr, worker, check_runs):
> 317:def criterion_item(repo, label, c, check, tests):
> 334:def criteria_list(repo, number, start, label, criteria, plan_tests, by_key, tests):
> 343:def code_review(recs):
> 351:def owner_review(reviews, owners):
> 358:def owner_merge(pr, owners):
> 364:def done_row(repo, found, all_tests):
> 365:    """The Definition of Done: All tests, the code review and the owner's approval, each with its verdict and proof.
> 373:            f"{circle(repo, state(all_tests), all_tests and all_tests['html_url'])} All tests · "
> 374:            f"{circle(repo, review_st, review and review.get('run'))} {field

**Agent:** I'm waiting on the full test suite. Meanwhile I'm checking how the existing card code draws the Definition of Done.

`13. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output | tail -5
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output tail -5. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`14. Monitor`
```
until grep -qE "passed|failed|error" /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output; do sleep 5; done; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output
```

> <tool_use_error>InputValidationError: Monitor failed due to the following issue:
> The required parameter `description` is missing
> 
> This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 600000ms are capped to 600000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required"

**Agent:** Meanwhile I'll write the review.

`15. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote 13 new tests in tests/test_card_now.py that run card.yml and dokima/card.py, event by event, against a fake GitHub holding #246/#260 and #312/#314.",
          "Loosened two older tests in tests/test_hand_links.py where the new behavior makes them wrong, and gave a reason for each."],
  "decided": ["Any event about an issue or its pull request, including the merge, a review, a line note and an agent's record, redraws both cards; the cards' own writes start nothing.",
              "Each issue gets its own queue, separate from the sweep's, and a sweep with nothing to fix writes nothing and makes at most 10 GitHub calls plus one per open issue and two per open pull request.",
              "Runs started by a pull request use main's copy of card.yml and dokima/card.py."],
  "open": ["The plan asks the owner no questions."]},
 "verdict": "block",
 "summary": "The plan covers every ask, and all 13 new tests fail today for the right reason, but its safety promise that pull request runs use main's copy of card.yml is untrue for reviews and line notes, and its test cannot see that.",
 "blockers": [{"id": "B1", "criterion": "332.7",
   "test": "tests/test_card_now.py::test_runs_started_by_a_pull_request_run_mains_code",
   "problem": "332.7 promises that runs started by a pull request use main's copy of card.yml. But criterion 1 has card.yml start on reviews and line notes (pull_request_review, pull_request_review_comment), and GitHub runs those from the pull request's merge ref, so it uses the pull request's own copy of card.yml, with the keys. The test always plays the repo's own card.yml and checks only which ref the checkout step names. A pull request that edits card.yml would therefore still pass it, so the test proves only the checkout, not the promise.",
   "evidence": "tests/test_card_now.py:22 (docstring: 'on a review GitHub's own ref is the pull request's merge 
```

> class Context(Ctx):
>     """An expression context read with dots, where a missing name is null."""
> 
>     def __getattr__(self, k):
>     return v
> 
> 
> def github_ctx(event_name, event):
>     """The `github` context GitHub gives card.yml for one event."""
>     ref = "refs/heads/main"
>     if event_name in ("pull_request", "pull_request_review", "pull_request_review_comment"):

`16. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def github_ctx\|^def workflow\|wf = workflow()\|^def test_runs_started\|^def test_the_merge_rewrites\|^def test_card_yml_starts_on_every_kind\|budget = \|on a review GitHub" tests/test_card_now.py
```

> 17:  pull_request_review_comment; on a review GitHub's own ref is the pull request's merge ref.
> 687:def github_ctx(event_name, event):
> 698:def workflow():
> 759:        wf = workflow()
> 976:def test_card_yml_starts_on_every_kind_of_event_about_an_issue_or_its_pr(record_property):
> 983:    wf = workflow()
> 1063:def test_the_merge_rewrites_the_pr_card_as_merged_with_the_true_definition_of_done(tmp_path, record_property):
> 1200:def test_runs_started_by_a_pull_request_run_mains_code(tmp_path, record_property):
> 1243:    budget = 10 + 2 + 2 * 1

`17. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
p='review.json'; s=open(p).read()
for a,b in [("tests/test_card_now.py:22 (docstring","tests/test_card_now.py:17 (docstring"),("github_ctx at :684-689","github_ctx at :687-693"),("workflow() (the repo's card.yml, :657-659)","workflow() (the repo's card.yml, :698 and :759)"),("(:1210-1229)","(:1200)"),("tests/test_card_now.py:1245 budget","tests/test_card_now.py:1243 budget"),("(:1060-1085)","(:1063)"),("(:970-993)","(:976)")]:
    assert a in s, a; s=s.replace(a,b)
json.loads(s); open(p,'w').write(s)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 332 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; tail -5 /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output
```

> previous_step holds at most five lines
> summary holds 42 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1
> tests/test_card_guard.py
> tests/test_hand_links.py
> tests/test_app.py
> tests/test_card.py
> tests/test_card_now.py

`18. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
p='review.json'; r=json.load(open(p))
r["summary"]="Every ask is covered and the new tests fail rightly, but reviews and line notes would run the pull request's own card.yml, which no test catches."
r["previous_step"]["did"]=["Wrote 13 new tests that run card.yml and the card code, event by event, against a fake GitHub; loosened two older tests, with a reason for each."]
r["previous_step"]["decided"]=r["previous_step"]["decided"][:3]
r["previous_step"]["open"]=["No questions for the owner."]
json.dump(r,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 332 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> rc=0

`19. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output | tail -4
```

> tests/test_hand_links.py
> tests/test_app.py
> tests/test_card.py
> tests/test_card_now.py

`20. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "concurrency\|group\|pull_request\|issue_comment\|Bot" tests/test_card_guard.py tests/test_app.py tests/test_card.py | grep -i "card.yml\|CARD\|group" | head -20
```

> tests/test_card_guard.py:11:    line = re.search(r"^\s+if:\s*(.+)$", text, re.M).group(1)
> tests/test_card_guard.py:24:    assert runs("issues", "opened", "Bot"), "87.1: card job is skipped for an issue opened by a bot"
> tests/test_card_guard.py:30:    assert not runs("issues", "edited", "Bot"), "87.2: a bot's own edit would re-trigger the card (loop)"
> tests/test_card_guard.py:32:    assert runs("workflow_run", None, "Bot"), "87.2: workflow_run events must still write the card"
> tests/test_card.py:128:    assert "github.event.sender.type != 'Bot'" in yml

**Agent:** I've blocked the plan for #332, with one blocker for the planner. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks; the only remark is a warning that the summary runs 26 words against a cap of 25, which is allowed.

**What holds up:**
- **Every ask is covered.** Each of the six asks in the issue maps to a criterion (332.1 to 332.6), and none is missing.
- **The new tests fail for the right reason.** All 13 in `tests/test_card_now.py` fail today because the feature is missing, not because of crashes or bad paths. For example, the size check fails on "721 < 721", and the sweep test fails because #246 still shows "Review" instead of "Merged".
- **The two loosened tests are justified.** The changed tests in `tests/test_hand_links.py` still pass (16 passed), and the planner gave a fair reason for each change.
- **Not run:** a full run of the rest of the suite was still going when I handed back, so I have no result from it.

**Blocker B1 (332.7, for the planner):** the plan promises that runs started by a pull request use main's copy of `card.yml`. But criterion 1 makes `card.yml` start on reviews and line notes, and GitHub runs those events from the pull request's own copy of the workflow file, with the keys. The test always plays the repo's own `card.yml` and only checks which branch the checkout step uses, so a pull request that edited `card.yml` would still pass it. The fix is one of two:
- **Make the promise true:** route reviews and line notes to the card run through a small listener that holds no keys, and test that `card.yml` no longer starts on them.
- **Narrow the promise:** reduce it to what the test really proves (every run checks out main's `dokima/card.py`), and ask the owner whether review runs may use the pull request's copy of `card.yml`. `board.yml` already works that way today.

**Notes (not blocking):**
- **Call budget:** the limit of "one call per open issue" is only tested with two open issues. With so few, a sweep spending three calls per open issue still fits inside the fixed 10.
- **Code review line:** after a merge, Code review is only ever shown as passed. A card that always said "passed" there would not be caught.
- **Unchecked pull request events:** for a person editing or reopening a pull request, the tests only check that the event is in `card.yml`'s trigger list. Nothing checks that the job then actually runs.

**Proposed new issue:** `board.yml` has the same flaw as B1 today. It runs on reviews with the keys, so a pull request that edits `board.yml` changes how its own review run behaves.

`21. Bash`
```
tail -4 /tmp/claude-1001/-home-runner-work-dokima-dokima/771f5315-e1e5-49ac-8c94-e84605d8240e/tasks/bhttc16ji.output
```

> ....................................................................     [100%]
> 788 passed, 13 deselected in 392.33s (0:06:32)
> 
> [exited with code 0]

**Agent:** The rest of the test suite has now finished: 788 tests passed. Only the planner's 13 new tests were left out, and those fail as expected. So the plan's test changes break nothing else.

My verdict stays the same. The plan for #332 is blocked on B1, for the planner: reviews and line notes would run the pull request's own copy of `card.yml`, and the safety test can't detect that. The hand-back in `/tmp/dokima-out/review.json` is unchanged.
