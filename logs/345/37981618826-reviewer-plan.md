# reviewer (plan) for #345

Run: https://github.com/dokima-dev/dokima/actions/runs/37981618826

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  9 19:38 .
> drwxrwxrwt 18 root   root   4096 Oct  9 19:39 ..
> drwxr-xr-x  2 runner runner 4096 Oct  9 19:38 in
> -rw-r--r--  1 runner runner 7387 Oct  9 19:38 issue.md
> -rw-r--r--  1 runner runner    2 Oct  9 19:38 open_blockers.json
> -rw-r--r--  1 runner runner   15 Oct  9 19:38 parent.json
> -rw-r--r--  1 runner runner 3242 Oct  9 19:38 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  9 19:38 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 19:38 ..
> -rw-r--r-- 1 runner runner 3874 Oct  9 19:38 01-planner.json
> # Issue #345: Merging a PR redraws its card and its issue's card
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 344 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> **Backlog**
> 
> [issue #345](https://github.com/dokima-dev/dokima/issues/345)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #344
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/in/01-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; git show --stat HEAD; cat tests/test_card_merge.py; git branch -a | grep 332; git log --oneline -3 origin/try/issue-332 2>/dev/null
```

> <persisted-output>
> Output too large (48KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/9fb28ecd-7c32-4c2e-9704-b7d96ca6866c/tool-results/b5okd1zia.txt
> 
> Preview (first 2KB):
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37981123156",
>  "commit_before": "75e92d39382169818574145883e92d3166548974",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 218036,
>   "turns": 28,
>   "cost_usd": 1.4162438000000002,
>   "tokens_in": 1813992,
>   "tokens_out": 19450
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/345/37981123156-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37981123156",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> commit 58e7101e5260b57f1ca53a818eb52aaf5c37beca
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 19:38:26 2026 +0000
> 
>     planner for #345 (run 37981123156)
> 
>  tests/test_card_merge.py | 1026 ++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 1026 insertions(+)
> """Merging a pull request redraws its card and its issue's card (#345).
> 
> Nothing redrew a card when a pull request merged: card.yml started only on issue events from a person, on comments,
> on finished checks and on a schedule, so a merge by Dokima's bot on autopilot redrew nothing, and the last card could
> come from a run that read the pull request just before the merge. Now the merge itself redraws bot

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,200p tests/test_card_merge.py; git branch -a | grep -i 332
```

> """Merging a pull request redraws its card and its issue's card (#345).
> 
> Nothing redrew a card when a pull request merged: card.yml started only on issue events from a person, on comments,
> on finished checks and on a schedule, so a merge by Dokima's bot on autopilot redrew nothing, and the last card could
> come from a run that read the pull request just before the merge. Now the merge itself redraws both cards from GitHub
> as it is after the merge.
> 
> These tests reuse the player and fake GitHub #332's planner wrote on branch try/issue-332 (tests/test_card_now.py).
> They play card.yml the way GitHub runs it, for one event at a time, against a fake GitHub:
> - The event starts the workflow when card.yml's `on:` lists it (and its activity type, and for workflow_run the
>   workflow that finished). Then every job runs in the order its `needs` allow: a job's `if:` and every `${{ }}` are
>   evaluated with tests/test_start.py's evaluator (github, vars, secrets, needs, steps, env); `uses:` steps are skipped
>   (checkout is noted with the ref it would check out, and the app token step gives a fake token); `run:` steps run with
>   bash, from a copy of this repo's dokima/ and .github/, with a fake `gh` first on PATH.
> - Pull request events are sent as GitHub sends them: pull_request_target for the pull request itself (main's copy of
>   the workflow), pull_request_review and pull_request_review_comment for reviews and line notes (the pull request's own
>   copy). Such events reach card.yml only through

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def \|^    \"\"\"\|^class " tests/test_card_merge.py | sed -n 1,200p; git show origin/try/issue-332 --stat | head -20; git show origin/try/issue-332:tests/test_card_now.py | grep -n "^def test" ; git show origin/try/issue-332:tests/test_hand_links.py | grep -n "^def test"
```

> 62:def save():
> 66:def flag(*names):
> 73:def fields():
> 86:def positional():
> 101:def fail(msg):
> 106:def refuse(op, n):
> 112:def tick():
> 117:def write(op, n):
> 121:def jq(value, q):
> 135:def only(value):
> 136:    """Keep only the fields `--json` asked for, as gh does."""
> 145:def out(value):
> 158:def number(x):
> 162:def issue(n):
> 169:def pr(p):
> 176:def pr_state(x):
> 180:def issue_rest(n):
> 197:def comments_rest(cs):
> 202:def comments_gh(cs):
> 206:def pr_rest(p):
> 216:def pr_gh(p):
> 228:def issue_gh(n):
> 235:def prs(head=None, state="open"):
> 247:def text_arg():
> 255:def set_issue_body(n, text):
> 265:def set_pr_body(p, text):
> 411:def record(rec, at):
> 412:    """A comment the bot posted holding one agent record."""
> 416:def plan_record(n, story):
> 417:    """A planner record of issue n that passed its check: one criterion and its test."""
> 427:def review_record(stage):
> 428:    """An approving review record at `stage` (plan or pr) that passed its check."""
> 434:def worker_record():
> 435:    """A worker record that passed its check."""
> 440:def card_of(text):
> 441:    """The card block in a body, between its two marks; None when there is none."""
> 446:def stage_of(text):
> 447:    """The stage a card's status line shows (Backlog, Plan, Work, Review or Merged), or None."""
> 455:def done_of(text):
> 456:    """The Definition of Done a card shows: {All tests, Code review, Owner approval: passed/failed/...}."""
> 470:class Hub:
> 471:    """A fake GitHub holding issues #239 and #283 and their PRs #246 and #312."""
> 584:de

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 400,660p tests/test_card_merge.py
```

> if r.startswith("contents/"):
>         fail(f"HTTP 404: Not Found (https://api.github.com/{route})")
>     if r.startswith("actions/"):
>         out({"total_count": 0, "workflow_runs": []})
>         sys.exit(0)
> fail(f"fake gh: no such call {a}")
> '''
> 
> 
> # --- the fake GitHub ---------------------------------------------------------------------------------------------
> 
> def record(rec, at):
>     """A comment the bot posted holding one agent record."""
>     return {"login": BOT, "body": f"{agent.MARK}\n**Record**\n\n```json\n{json.dumps(rec)}\n```\n", "at": at}
> 
> 
> def plan_record(n, story):
>     """A planner record of issue n that passed its check: one criterion and its test."""
>     h = {"kind": "user_story", "summary": f"Issue {n} is planned.", "user_story": story,
>          "acceptance_criteria": [{"text": f"Criterion one of #{n}.", "source": f"https://github.com/o/r/issues/{n}"}],
>          "non_functional": [], "scope": ["dokima/x.py"], "out_of_scope": ["Nothing else."],
>          "tests": {f"{n}.1": ["tests/test_x.py::test_one"]}, "test_changes": {},
>          "links": {"blocked_by": [], "blocks": [], "relates_to": []}}
>     return {"role": "planner", "stage": None, "handback": h, "check": {"passed": True, "problems": []},
>             "run": "https://github.com/o/r/actions/runs/1", "run_id": "1"}
> 
> 
> def review_record(stage):
>     """An approving review record at `stage` (plan or pr) that passed its check."""
>     return {"role": "reviewer", "stage": stage, "handback": {"verdict": "approve", "

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 696,1026p tests/test_card_merge.py
```

> def github_ctx(event_name, event):
>     """The `github` context GitHub gives card.yml for one event."""
>     ref = "refs/heads/main"
>     if event_name in ("pull_request", "pull_request_review", "pull_request_review_comment"):
>         ref = f"refs/pull/{event['pull_request']['number']}/merge"
>     return wrap({"event_name": event_name, "event": event, "repository": "o/r", "repository_owner": "o", "ref": ref,
>                  "sha": "mainsha", "run_id": "42", "run_number": "7", "server_url": "https://github.com",
>                  "actor": (event.get("sender") or {}).get("login", "github"), "workflow": "card",
>                  "token": "fake-workflow-token"})
> 
> 
> def workflow():
>     """card.yml, read."""
>     return load_yaml(open(CARD_YML).read())
> 
> 
> def workflows():
>     """Every workflow of the repo but card.yml, read, as {file name: workflow}."""
>     out = {}
>     for f in sorted(os.listdir(WORKFLOWS)):
>         path = os.path.join(WORKFLOWS, f)
>         if f.endswith((".yml", ".yaml")) and path != CARD_YML:
>             out[f] = load_yaml(open(path).read())
>     return out
> 
> 
> def listened():
>     """The workflows card.yml starts after, by its workflow_run trigger, as {file name: workflow}."""
>     t = triggers(workflow()).get("workflow_run")
>     names = listed(t.get("workflows")) if isinstance(t, dict) else []
>     return {f: wf for f, wf in workflows().items() if wf.get("name") in names}
> 
> 
> def relays(event_name, event):
>     """The workflows card.yml starts after that start on this event, a

**Agent:** Reading the planner's tests; now running them.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_card_merge.py 2>&1 | grep -E "^(FAILED|PASSED|E  .*345)|passed|failed" | head -30; sed -n 1,60p .github/workflows/card.yml
```

> """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 345.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 345.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> E       AssertionError: 345.1: beside the edits, a merge did not run card.yml's card job
>         with All tests, Code review and Owner approval passed, and its issue's card (#239, #283) says Merged too. Proves
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 345.2: card.yml does not start on pull_request_target closed, so the cards are not redrawn
>         """Play the event; fail naming k unless card.yml started, ran dokima/card.py and every job passed."""
> E       AssertionError: 345.3: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> FAILED tests/test_card_merge.py::test_merging_a_pr_redraws_its_card_and_its_issues_card - AssertionError: 345.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> FAILED tests/test_card_merge.py::test_merging_one_pr_leaves_other_cards_alone - AssertionError: 345.1: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> FAILED tests/t

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 20 gh pr view 246 --json body -q .body 2>&1 | head -8; git show origin/try/issue-332:tests/test_card_now.py | sed -n 1135,1190p; git show origin/try/issue-332:tests/test_card_now.py | sed -n 1299,1327p
```

> gh: To use GitHub CLI in a GitHub Actions workflow, set the GH_TOKEN environment variable. Example:
>   env:
>     GH_TOKEN: ${{ github.token }}
> def test_the_merge_rewrites_the_pr_card_as_merged_with_the_true_definition_of_done(tmp_path, record_property):
>     """After the merge the PR card shows Merged with its true Definition of Done.
> 
>     PR #260 has every check passed and an approving code review, and the owner merges it: the merge event leaves
>     #260's card saying Merged with All tests, Code review and Owner approval passed. On a fresh GitHub where All tests
>     failed on the PR's last commit, the code review blocked and the bot merged it, the merge leaves Merged with All
>     tests failed, Code review failed and Owner approval not passed. Proves 332.3."""
>     record_property("proves", "332.3")
>     hub = Hub(tmp_path / "green")
>     hub.merge(246, 260)
>     must_redraw(hub, pr_event(246, 260, "closed", OWNER, merged=True), "332.3")
>     assert stage_of(hub.pr_body(260)) == "Merged", f"332.3: PR #260's card does not say Merged: {hub.pr_body(260)!r}"
>     done = done_of(hub.pr_body(260))
>     assert done == {"All tests": "passed", "Code review": "passed", "Owner approval": "passed"}, \
>         f"332.3: merged PR #260's Definition of Done is not every check passed: {done}"
>     hub = Hub(tmp_path / "red")
>     s = hub.load()
>     s["checks"]["sha260"][1].update(conclusion="failure")
>     blocked = review_record("pr")
>     blocked["handback"].update(verdict="block", summary="Blocked.",
>   

`9. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && python3 - <<'EOF'
p='.github/workflows/card.yml'; s=open(p).read()
s=s.replace("  issue_comment:\n","  issue_comment:\n  pull_request_target:\n    types: [closed]\n",1)
s=s.replace("if: github.event_name == 'workflow_run' ||","if: (github.event_name == 'pull_request_target' && github.event.pull_request.merged) || github.event_name == 'workflow_run' ||",1)
s=s.replace("          PR_NUMBER: ${{ github.event.workflow_run.pull_requests[0].number }}","          PR_NUMBER: ${{ github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number }}",1)
open(p,'w').write(s)
EOF
timeout 600 python3 -m pytest -q tests/test_card_merge.py 2>&1 | tail -8
```

> .....                                                                    [100%]
> 5 passed in 4.66s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned one user story with two criteria: a merge, by the owner or by Dokima on autopilot, redraws the pull request's card and its issue's card as Merged; PR #246 and PR #312 show Merged with every check passed after their merge.",
          "Added a rule that the merge redraw runs main's card.yml and card code, never the pull request's.",
          "Wrote five tests in tests/test_card_merge.py, built on the player and fake GitHub from #332's tests; all five fail today because card.yml does not start on a merge."],
  "decided": ["The fix goes in .github/workflows/card.yml (a merge trigger, letting a merged pull request through the bot filter, passing its number), with no card.py change expected.",
              "PR #246 and PR #312 are proven on look-alike test data, because on GitHub their cards already say Merged since #350 shipped."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan covers both asks, its five tests fail today only because nothing redraws a card on a merge, and a four-line card.yml change makes them all pass.",
 "blockers": [],
 "notes": [
  {"text": "The owner asked that #246's and #312's own cards show Merged once this ships. Those pull requests are already merged, so this fix's new merge trigger will never run for them again; the plan relies on their cards already saying Merged. Whoever approves the result should open both pull requests and check their cards with their own eyes.",
   "evidence": "plan.json concerns[1]; card.yml after the candidate change starts only on pull_request_target closed, which a merged PR never sends again"},
  {"text": "The fix changes a workflow file, which AGENTS.md reserves for issues that ask for it explicitly. The ask can only be met there, the planner said so openly, and on autopilot a pull request that changes a workflow file stops for the owner before it merges, so the owner sees it either way.",
   
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> rc=0

`11. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan covers both asks; its five tests fail today only because no merge redraws a card, and a small card.yml change passes them."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 345 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #345. There are no blockers, and the hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Both asks are covered.** Criterion 345.1 says merging a PR, by you or by the bot on autopilot, redraws that PR's card and its issue's card. Criterion 345.2 says #246's and #312's cards show Merged with nothing clicked.
- **The tests fail for the right reason today.** All 5 tests in `tests/test_card_merge.py` fail on this branch because `card.yml` does not start when a PR is merged.
- **The tests can pass.** In a copy of the repo, I made the 4-line change the planner described in `card.yml`: start on a merge, let a merged PR past the filter that skips the bot, and pass the PR number. All 5 tests then passed.
- **Your request to reuse the tests is honoured.** The new tests reuse the test harness and fake GitHub from #332's tests, cut down to the merge case.

I added three notes for you:

1. **#246 and #312 won't be redrawn by this fix.** Both are already merged, so the new merge trigger will never fire for them. The plan relies on the planner's claim that their cards already say Merged since #350 shipped. I couldn't confirm that because I had no GitHub access, so please open both PRs and check their cards.
2. **The fix changes a workflow file.** AGENTS.md only allows that when the issue explicitly asks for it. Your ask can only be met in `card.yml`, and the planner said so openly. Even on autopilot, a PR that changes a workflow file waits for you before it merges.
3. **What I checked:** 5 failed on the branch as it is, and 5 passed with the change.
