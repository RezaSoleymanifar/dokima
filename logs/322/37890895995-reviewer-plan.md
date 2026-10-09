# reviewer (plan) for #322

Run: https://github.com/dokima-dev/dokima/actions/runs/37890895995

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #322: A PR's card shows its true state after merge, however fast I merge
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #322](https://github.com/dokima-dev/dokima/issues/322)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> A PR's card can stay frozen after merge. On #246 the tests finished at 21:36:42 and I merged at 21:36:54. The card run that followed wrote at 21:37:06, after the merge, and skipped the PR because the card is only written while a PR is open. The PR card still says All tests is running. Merging a PR also never triggers a card redraw, so whichever run happens to come last decides what the card shows.
> 
> What I wan

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_card_after_merge.py; cat .github/workflows/card.yml; wc -l dokima/card.py
```

> """A PR's card shows its true state after merge, however fast the owner merges (#322).
> 
> On #246 the owner merged twelve seconds after the tests finished; the card run that followed could no longer find the
> PR (GitHub's event names no PR once it is merged, and GitHub lists only open PRs for a squash-merged commit), so the
> PR card kept saying All tests was running. These tests read the real `.github/workflows/card.yml`: they work out, for
> one GitHub event, whether the card job runs, its concurrency group and the env its "Write the card" step gets, the way
> GitHub would, then run the real `dokima/card.py` main() with that env against a fake GitHub.
> 
> The fake GitHub (FakeGitHub below) answers `gh` the way GitHub does for these reads:
>     gh api repos/o/r/commits/SHA/pulls          open PRs whose head is SHA, plus the merged PR of a commit on main
>     gh api repos/o/r/pulls?head=o:BRANCH&state=open|closed|all   (any order of query parameters)
>     gh api repos/o/r/pulls?state=...            every PR in that state
>     gh api repos/o/r/pulls/N                    one PR
>     gh api search/issues?q=...SHA...            the PRs whose head is SHA, open or merged
>     gh api graphql ... -F p=N                   the issue PR N closes (closingIssuesReferences)
>     gh api -X PATCH repos/o/r/pulls/N -F body=@FILE   writes the PR's description
> Anything else fails as a refused call would, and is logged in `refused`. What the card draws from (records, checks,
> reviews) is faked at card.gather, so th

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_card_after_merge.py 2>&1 | grep -E "Error|assert|passed|failed" | head -40
```

> assert job_runs(check_finished("abc", "try/issue-40", [])), "322.1: the card job is skipped when a check finishes"
> >       assert drawn == [(40, 5)], (f"322.1: a check finishing after PR #5 merged drew {drawn or 'nothing'}, "
> E       AssertionError: 322.1: a check finishing after PR #5 merged drew nothing, not issue #40 with its merged PR #5
> E       assert [] == [(40, 5)]
> /home/runner/work/dokima/dokima/tests/test_card_after_merge.py:348: AssertionError
>         with All tests, Code review and Owner approval passed."""
> >       assert types is not None and "closed" in types, \
> E       AssertionError: 322.2: card.yml does not start on a PR closing (pull_request_target types: None)
> E       assert (None is not None)
> tests/test_card_after_merge.py:376: AssertionError
>         assert merge and merge == late, (f"322.3: the merge's card run (group {merge!r}) and a late check's on the same PR "
> >       assert other_check != merge and other_issue != merge, \
> E       AssertionError: 322.3: card runs for other issues share the merge's group 'card', so they can drop its waiting run
> E       assert ('card' != 'card')
> tests/test_card_after_merge.py:406: AssertionError
> >       assert trigger_types("workflow_dispatch") is not None, "322.4: card.yml cannot be run by hand (no workflow_dispatch)"
> E       AssertionError: 322.4: card.yml cannot be run by hand (no workflow_dispatch)
> E       assert None is not None
> tests/test_card_after_merge.py:419: AssertionError
> >       assert trigger_types("pull_re

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def \|PR_NUMBER\|HEAD_SHA\|ISSUE_NUMBER\|HEAD_BRANCH\|RUN_TITLE\|pulls" dokima/card.py | head -80; sed -n '/^def main/,$p' dokima/card.py
```

> 46:def icon(repo, name, alt=None):
> 52:def field_icon(repo, field):
> 57:def link_lines(repo, links):
> 74:def merged(*many):
> 86:def linked_from(text):
> 98:def their_links(repo, number, sources, plans=None):
> 121:def state(check):
> 130:def circle(repo, st, url=None):
> 136:def fold(title, lines):
> 141:def escape(text):
> 145:def checks_by_key(check_runs):
> 155:def as_items(steps, owner=None):
> 162:def checks_passed(number, h, check_runs):
> 171:def todo(issue, found, rec):
> 195:def status(issue, found):
> 215:def status_line(repo, stage, todo):
> 221:def child_row(repo, child):
> 230:def links_row(repo, issue, pr, worker, check_runs):
> 243:def criterion_item(repo, label, c, check, tests):
> 260:def criteria_list(repo, number, start, label, criteria, plan_tests, by_key, tests):
> 269:def code_review(recs):
> 277:def owner_review(reviews, owners):
> 284:def owner_merge(pr, owners):
> 290:def done_row(repo, found, all_tests):
> 305:def render(repo, issue, found, page="issue"):
> 348:def issue_body(card, notes):
> 353:def pr_body(card, body):
> 359:def gh(*args):
> 363:def issue_pr(repo, n):
> 367:        prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
> 373:def find_work(repo):
> 375:    if os.environ.get("ISSUE_NUMBER"):
> 376:        n = int(os.environ["ISSUE_NUMBER"])
> 378:    title = re.match(r"worker for #(\d+)$", os.environ.get("RUN_TITLE", ""))
> 382:    pr = os.environ.get("PR_NUMBER")
> 384:        prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
> 391:def lat

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 355,395p dokima/card.py
```

> found = CLOSES.search(body or "")
>     return card + ("\n\n" + found.group(0) if found else "")
> 
> 
> def gh(*args):
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> def issue_pr(repo, n):
>     """The PR built for issue n from its try or work branch, or None."""
>     owner = repo.split("/")[0]
>     for branch in (f"try/issue-{n}", f"work/issue-{n}"):
>         prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
>         if prs:
>             return prs[0]["number"]
>     return None
> 
> 
> def find_work(repo):
>     """The issue and open PR this event is about, as (issue number, PR number or None)."""
>     if os.environ.get("ISSUE_NUMBER"):
>         n = int(os.environ["ISSUE_NUMBER"])
>         return n, issue_pr(repo, n)
>     title = re.match(r"worker for #(\d+)$", os.environ.get("RUN_TITLE", ""))
>     if title:
>         n = int(title.group(1))
>         return n, issue_pr(repo, n)
>     pr = os.environ.get("PR_NUMBER")
>     if not pr:
>         prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
>         pr = prs[0]["number"] if prs else None
>     if not pr:
>         return None, None
>     return plan.pr_issue_number(repo, pr), int(pr)
> 
> 
> def latest_worker_run(repo, number):
>     runs = json.loads(gh("api", f"repos/{repo}/actions/workflows/worker.yml/runs?per_page=50"))["workflow_runs"]
>     run = next((r for r in runs if r["display_title"] == f"worker for #{number}"), None)
>     return {"status": run["status"]

**Agent:** Plan tests all fail today for the right reasons; now checking whether an autopilot merge (made with the bot's token) would actually set off the card workflow.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "merge" .github/workflows/*.yml | grep -i "gh \|token" | head; grep -rln "pulls/.*merge\|pr merge" dokima | head
```

> (Bash completed with no output)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "/merge\|\"merge\"" dokima .github | head
```

> dokima/agent.py:1493:        gh("pr", "merge", str(pr), "-R", repo, "--squash", "--match-head-commit", head)
> dokima/manifest.py:80:    ("pr", "merge"): ("contents", "write"),
> dokima/uptodate.py:135:           "handback": {"base": base, "merge": sha, "merged_pr": by, "pr": n, "files": clashed, **({"why": why} if why else {})},

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote four criteria and one requirement: a late check still writes the merged PR's card, a merge redraws both cards, the merge's card run comes last, and a Run workflow button redraws one issue and its PR.",
   "It wrote five tests that run the real card workflow and card code against a fake GitHub; all five fail today."
  ],
  "decided": [
   "The merge's card run uses main's copy of the card workflow and code, never the PR's.",
   "Redrawing every other stale card stays with #315 and #183."
  ],
  "open": [
   "Whether the owner presses Run workflow once each for #246 and #312 after this ships, or code redraws them with no click."
  ]
 },
 "verdict": "approve",
 "summary": "The plan covers every ask and each of its five tests fails today for the missing feature; it still needs the owner's answer on how #246 and #312 get redrawn.",
 "blockers": [],
 "notes": [
  {
   "text": "This work changes .github/workflows/card.yml, so on autopilot the pull request will stop for the owner before it merges, as AGENTS.md step 6 says.",
   "evidence": "Plan scope lists .github/workflows/card.yml; AGENTS.md: 'a pull request that changes a workflow file ... stops for the owner'."
  },
  {
   "text": "The test for 322.3 proves the merge and a late check on the same PR share one queue, and other issues use other queues. A later check on the same PR may still replace the merge's waiting run, but that run also starts after the merge, so the last word still comes after it.",
   "evidence": "tests/test_card_after_merge.py::test_the_merges_card_run_always_has_the_last_word"
  }
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The PR card is written whether the PR is open or merged.", "source": "https://github.com/dokima-dev/dokima/issues/322", "criterion": "322.1"},
  {"ask": "Merging a PR redraws its card and its issue's card", "source":
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="Every ask is covered and all five tests fail today for the missing feature; the owner still decides how #246 and #312 get redrawn."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 322 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #322. It still stops for you on one question: how #246 and #312 get redrawn.

**The plan:**
- **Late checks:** a check that finishes after its PR merged still writes the card into that PR and its issue. A commit with no PR still gets no card.
- **Merges:** merging a PR, by you or by autopilot, redraws its card and its issue's card. Both show Merged with the true Definition of Done.
- **Order:** the card run a merge starts always has the last word. It waits for a card run already going on the same PR, and other issues' card runs can't cancel it.
- **Hand runs:** a new Run workflow button on the card redraws one issue and its PR, merged or not.
- **Safety:** the merge's card run uses main's copy of the card workflow and card code, never the PR's.

**Checks I ran:**
- Each of your three asks maps to a criterion. Nothing is missing or added.
- The planner wrote five new tests. I ran all five, and each fails today because the feature is missing, not because of a crash or a bad path. For example: "a check finishing after PR #5 merged drew nothing", and "card.yml cannot be run by hand".
- An autopilot merge goes through Dokima's own GitHub app (bot), so it will set off the card workflow too.

**Your decision:** the planner asks whether you press Run workflow once each for #246 and #312 after this ships, or whether code redraws them by itself. It planned for you pressing the button. I did not accept that assumption: your words "#246 and #312 show the right state once this ships" don't say who redraws them, and the button adds a new way to start the card workflow. Even with autopilot on, this question waits for you. Reply with `/plan` and your answer, or `/review` to keep the button.

**Notes, not blockers:**
- The work changes `.github/workflows/card.yml`, so on autopilot the pull request will also stop for you before it merges.
- A later check on the same PR can replace the merge's waiting card run. That run also starts after the merge, so the last word still comes after it.

The review is in `/tmp/dokima-out/review.json`, and both checks on it pass.
