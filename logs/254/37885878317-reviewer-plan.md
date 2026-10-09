# reviewer (plan) for #254

Run: https://github.com/dokima-dev/dokima/actions/runs/37885878317

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat open_blockers.json; wc -c issue.md plan.json in/*
```

> .:
> total 124
> drwxr-xr-x  3 runner runner   4096 Oct  9 04:52 .
> drwxrwxrwt 18 root   root     4096 Oct  9 04:52 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 04:52 in
> -rw-r--r--  1 runner runner 100952 Oct  9 04:52 issue.md
> -rw-r--r--  1 runner runner      2 Oct  9 04:52 open_blockers.json
> -rw-r--r--  1 runner runner   7729 Oct  9 04:52 plan.json
> 
> in:
> total 64
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:52 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:52 ..
> -rw-r--r-- 1 runner runner 5217 Oct  9 04:52 01-planner.json
> -rw-r--r-- 1 runner runner 4014 Oct  9 04:52 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6068 Oct  9 04:52 03-planner.json
> -rw-r--r-- 1 runner runner 5002 Oct  9 04:52 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7432 Oct  9 04:52 05-worker.json
> -rw-r--r-- 1 runner runner 5600 Oct  9 04:52 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 8389 Oct  9 04:52 07-planner.json
> []100952 issue.md
>   7729 plan.json
>   5217 in/01-planner.json
>   4014 in/02-reviewer-plan.json
>   6068 in/03-planner.json
>   5002 in/04-reviewer-plan.json
>   7432 in/05-worker.json
>   5600 in/06-reviewer-pr.json
>   8389 in/07-planner.json
> 150403 total
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> <persisted-output>
> Output too large (48.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/83444f31-45b3-4f30-a5a3-4f31f40ee73d/tool-results/bciybjz6x.txt
> 
> Preview (first 2KB):
> {
>  "kind": "user_story",
>  "summary": "A blocked-by link added or removed by hand shows on both issues' cards once either issue changes, and within 15 minutes otherwise.",
>  "user_story": "When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.",
>  "acceptance_criteria": [
>   {
>    "text": "A blocked-by link added by hand (#A blocked by #B) shows as Blocked by #B on #A's card and Blocks #A on #B's. It shows as soon as a person changes either issue (opens, edits, closes, reopens, labels, assigns or comments on it), and within 15 minutes when nobody does. Once it is removed by hand, it leaves both cards the same way. No comment is posted on either issue for the link.",
>    "source": "https://github.com/dokima-dev/dokima/issues/254"
>   },
>   {
>    "text": "When hand-made links make issues block each other, directly or through others, every card in the loop names them all until the loop is gone. On autopilot, each of those issues gets one comment mentioning the owner, and the Needs you pill.",
>    "source": "https://github.com/dokima-dev/dokima/issues/254"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Every time a card is drawn, its Blocked by and Blocks lines come from G

`3. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/83444f31-45b3-4f30-a5a3-4f31f40ee73d/tool-results/bciybjz6x.txt | head -c 26000
```

> {
>  "kind": "user_story",
>  "summary": "A blocked-by link added or removed by hand shows on both issues' cards once either issue changes, and within 15 minutes otherwise.",
>  "user_story": "When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.",
>  "acceptance_criteria": [
>   {
>    "text": "A blocked-by link added by hand (#A blocked by #B) shows as Blocked by #B on #A's card and Blocks #A on #B's. It shows as soon as a person changes either issue (opens, edits, closes, reopens, labels, assigns or comments on it), and within 15 minutes when nobody does. Once it is removed by hand, it leaves both cards the same way. No comment is posted on either issue for the link.",
>    "source": "https://github.com/dokima-dev/dokima/issues/254"
>   },
>   {
>    "text": "When hand-made links make issues block each other, directly or through others, every card in the loop names them all until the loop is gone. On autopilot, each of those issues gets one comment mentioning the owner, and the Needs you pill.",
>    "source": "https://github.com/dokima-dev/dokima/issues/254"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Every time a card is drawn, its Blocked by and Blocks lines come from GitHub's own blocked-by links, read right then. When GitHub cannot list them, the card shows GitHub's reason, and the other cards still update.",
>    "why": "An empty line that was really never read would hide a blocke

`4. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/83444f31-45b3-4f30-a5a3-4f31f40ee73d/tool-results/bciybjz6x.txt | tail -c +26000 | head -c 24000
```

> d_work KeyError 'HEAD_SHA'."
>    }
>   ],
>   "resolved": [],
>   "issues_found": [],
>   "asks": [
>    {
>     "ask": "When a person adds a blocked-by link by hand on GitHub (#A blocked by #B), with no command, the card of #A shows #B on its Blocked by line and the card of #B shows #A on its Blocks line",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.1"
>    },
>    {
>     "ask": "when the person removes it, neither card shows it any more. No comment is posted on either issue for the link.",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.1"
>    },
>    {
>     "ask": "When a link added by hand makes two issues block each other, directly or through other issues, the cards of both issues say which issues block each other",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.2"
>    },
>    {
>     "ask": "on autopilot the river stops for the owner on them",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.2"
>    },
>    {
>     "ask": "The link lines on a card come from GitHub's own blocked-by links read when the card is drawn, so a card never shows a blocking link GitHub no longer has",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.3"
>    },
>    {
>     "ask": "if GitHub cannot list them, the card says so instead of showing no links",
>     "source": "https://github.com/dokima-dev/dokima/issues/254",
>     "criterion": "254.

`5. Bash`
```
cd /tmp/pack; head -c 6000 issue.md; echo; echo ----; grep -n "^#\|^\*\*\|^---\|commented\|RezaSoleymanifar" issue.md | head -80
```

> # Issue #254: A link added or removed by hand on GitHub updates the cards of both issues
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> A blocked-by link added or removed by hand shows on both issues' cards once either issue changes, and within 15 minutes otherwise.
> 
> **Plan**
> 
> [issue #254](https://github.com/dokima-dev/dokima/issues/254) · [PR #307](https://github.com/dokima-dev/dokima/pull/307) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/307/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #231, #253, #294
> 
> **User story:** When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Acceptance criterion:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37885285681/job/113673838738">A blocked-by link added by hand

**Agent:** Reading the pack is done; now I'm checking the planner's changes to the older tests and running them.

`6. Bash`
```
cd /tmp/pack; sed -n 75,95p issue.md; sed -n 426,430p issue.md; cd /home/runner/work/dokima/dokima; git log --oneline -8; git diff e6bee0a HEAD --stat; git diff origin/main --stat 2>/dev/null | tail -15
```

> <details open><summary>From the approved plan of #231, story 5</summary>
> 
> **Part of:** #231 The planner finds the issues this one blocks, is blocked by, or relates to
> 
> **User story:** When the owner adds or removes a blocked-by link by hand on GitHub, the cards of both issues show the change by themselves, the same as links from an approved plan.
> 
> **Context:** The owner's answer on #231 (19:21): "a link I add or remove by hand on GitHub also updates the cards of both issues, the same as links from an approved plan." GitHub's only native link is blocked-by (read by blocked_by() in dokima/agent.py, REST repos/{repo}/issues/{n}/dependencies/blocked_by and .../blocking); relates-to has no native form, so a hand-made link here is always blocked-by. No workflow today runs when a dependency changes: card.yml runs on issues opened/edited and workflow_run, board.yml on labeled/unlabeled/closed and comments. This story's planner must find which GitHub event (if any) Actions receives when a blocked-by link is added or removed, and otherwise choose the nearest reliable trigger; a new or changed workflow file is part of this story, as the owner asked for the behavior. Story 2 draws the link lines and story 3 draws the other issue's side; this story only adds the trigger and reads hand-made links from GitHub when a card is drawn. The owner's 19:11 comment asks that a contradiction, like two issues blocking each other, be handled as an edge case for any link; story 3 handles it for plan lin

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin 2>&1|tail -2; git log --oneline -3 origin/main; git log --format='%h %an %s' -- tests/test_hand_links.py tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py | head; git status --short; git diff origin/main --stat
```

> 02a6d8d A drift audit reports what is off on one pinned Setup issue, and stays silent otherwise (#312)
> e1a21e7 Three kinds of raise and one table of who raises to whom, checked by code (#304)
> 436b3e8 The plan check re-runs when a plan is approved, so it never shows a stale failure (#303)
> 1cb032a dokima-runtime[bot] planner for #254 (run 37880667428)
> 70679e1 dokima-runtime[bot] planner for #254 (run 37872687021)
> 826a1b9 dokima-runtime[bot] The issue and PR card list criteria as bullets, count the owner's merge and always match (#276)
> 4ff0278 dokima-runtime[bot] Every field on a card has its own GitHub icon, fixed by code (#248)
> bc3a3e6 dokima-runtime[bot] The card says what the issue is, where it stands, its children, and what the owner must do (#225)
> f1b30ab dokima-runtime[bot] Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 dokima-runtime[bot] The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> c7de9c0 dokima-runtime[bot] The owner's ask is kept below a fixed marker and never rewritten (#200)
> 76c153c dokima-runtime[bot] Bug: no card on issues the bot opens (#102)
> d58749e dokima-runtime[bot] Objective and Acceptance criteria on issues and cards; folds are never plan (#93) (#94)
>  .github/workflows/card.yml |  19 +-
>  AGENTS.md                  |   2 +-
>  dokima/card.py             | 174 ++++++++++++-
>  tests/test_hand_links.py   | 601 +++++++++++++++++++++++++++++++++++++++++++++
>  4 

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git branch -a | head -20; git ls-remote origin 2>/dev/null | grep -i 254; ls /tmp/dokima-out 2>&1; grep -rn "NOT_RUN_HERE" tests | head
```

> main
> * try/issue-254
>   remotes/origin/HEAD -> origin/main
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
> e5cd672fe9798dde6b683711159694bee279da78	refs/heads/try/issue-254
> bfecb2d9c2544a939bc19b47e0eee9c3f39f175f	refs/pull/216/head
> claude.json

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin logs 2>&1|tail -1; git show FETCH_HEAD:logs/254/37885045582-planner.md 2>/dev/null | grep -n "NOT_RUN_HERE\|test_card_guard\|fence\|dropped\|commit" | head -30
```

> 51:>   "evidence": "PYTHONPATH=$PWD pytest -q on try/issue-254: tests/test_card.py::test_same_card_on_issue_and_pr_and_only_icons_change fails on `assert 'types: [opened, edited]' in card.yml`; tests/test_card_guard.py::test_bot_opened_issue_gets_a_card and ::test_bot_edits_do_not_retrigger_card fail with `guard uses an unexpected context: ... !github.event.issue.pull_request ...`. All three pass on origin/main (same command in a main worktree: 33 passed). 254.4's own test needs the guard to tell a comment on an issue from one on a pull request, which only github.event.issue.pull_request can do, so the guard must use it.",
> 52:>   "fix": "In the plan's test_changes, update test_card.py to check the new issues trigger instead of the literal 'types: [opened, edited]', and teach test_card_guard.py's runs() to evaluate github.event.issue.pull_request and '!' (or reuse test_hand_links.py's job_if), each with a reason.",
> 165:cd /home/runner/work/dokima/dokima; cat tests/test_card_guard.py; grep -n "opened, edited" -B5 -A5 tests/test_card.py
> 391:> 471:        prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
> 396:> 531:        check_runs = json.loads(gh("api", f"repos/{repo}/commits/{pr['head']['sha']}/check-runs?per_page=100"))["check_runs"]
> 528:NOT_RUN_HERE = {"card.yml"}
> 534:new='''            if not fname.endswith((".yml", ".yaml")) or fname in NOT_RUN_HERE:
> 580:p='tests/test_card_guard.py'; s=open(p).read()
> 596:cat tests/test_card_guard.py | head

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git log --all --format='%h %s' | grep -i "254" | head; git show FETCH_HEAD:logs/254/37885045582-planner.md | sed -n 660,735p
```

> e5cd672 Merge branch 'main' into try/issue-254
> 790765f Merge branch 'main' into try/issue-254
> 0e37779 Merge branch 'main' into try/issue-254
> e6bee0a worker for #254 (run 37881697081)
> e8edf1b Merge remote-tracking branch 'origin/main' into try/issue-254
> 1cb032a planner for #254 (run 37880667428)
> 70679e1 planner for #254 (run 37872687021)
> 73649fe planner for #268 (run 37863125401)
> > FAILED tests/test_autopilot_start.py::test_autopilot_start_never_starts_the_issu
> 
> **Agent:** All 17 failures are the ones B1 and B2 name, and the fixes cover every one. Applying them to the repo and writing the hand-back.
> 
> `23. Bash`
> ```
> cd /home/runner/work/dokima/dokima; grep -rn "test_card_guard\|NOT_RUN_HERE" tests | grep -v "^tests/test_card_guard.py" ; cp /tmp/exp/tests/test_card.py /tmp/exp/tests/test_card_guard.py /tmp/exp/tests/test_autopilot_close.py tests/; git diff --stat; mkdir -p /tmp/dokima-out
> ```
> 
> > tests/test_autopilot_close.py |  5 ++++-
> >  tests/test_card.py            |  8 +++++++-
> >  tests/test_card_guard.py      | 19 ++++++++-----------
> >  3 files changed, 19 insertions(+), 13 deletions(-)
> 
> `24. Bash`
> ```
> cd /home/runner/work/dokima/dokima; python3 - <<'E'
> import json
> p=json.load(open('/tmp/pack/plan.json'))
> p["test_changes"]={
>  "tests/test_card.py::test_same_card_on_issue_and_pr_and_only_icons_change": "254.4 makes card.yml start on every issue event, not only opened and edited, so the test no longer looks for the literal 'types: [opened, edited]'; it reads card.yml's trigger

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "test_changes" dokima/*.py .github/workflows/*.yml | head -30; grep -n "planner for" -r dokima .github | head
```

> dokima/agent.py:399:                  ("Test changes", pairs(h.get("test_changes"))),
> dokima/planner.py:10:plan's criteria. Every older test it changes, renames or deletes needs a reason in test_changes. Every new test has a
> dokima/planner.py:186:    tc = p.get("test_changes", {})
> dokima/planner.py:188:        raise Garbled("plan.json test_changes must map each changed older test to a non-empty reason")
> dokima/planner.py:191:                    "non_goals": p.get("out_of_scope", []), "scope": p["scope"], "test_changes": tc,
> dokima/planner.py:230:def test_changes(paths, before, after):
> dokima/planner.py:288:    out += [f"{t} is an older test the planner changed or deleted, with no reason in test_changes"
> dokima/planner.py:289:            for t in older if t not in plan["test_changes"]]
> dokima/planner.py:452:        lines += [f"- `{t}`: {plan['test_changes'].get(t, 'no reason given')}" for t in older]
> dokima/planner.py:503:            tc = test_changes(paths, read_at(base), read_now)
> dokima/roles/result-grade.md:33:   That is a blocker for the plan: set its `"fixer": "planner"`, and it goes back to the planner for a stronger test
> dokima/roles/planner.md:2:You are Dokima's planner for one GitHub issue. In Dokima nothing merges until it is proven. You plan; a worker writes the
> .github/workflows/planner.yml:2:run-name: "planner for #${{ github.event.issue.number }}${{ github.event.label.name != 'plan' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> dokima/age

`12. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 470,560p dokima/planner.py; grep -n "commit\|push\|git add" .github/workflows/planner.yml | head -30
```

> return subprocess.run(["git", *args], capture_output=True, text=True)
> 
> 
> def read_at(base):
>     return lambda path: (lambda r: r.stdout if r.returncode == 0 else "")(git("show", f"{base}:{path}"))
> 
> 
> def read_now(path):
>     return open(path).read() if os.path.exists(path) else ""
> 
> 
> def main(argv):
>     action, number, out = argv[1], argv[2], argv[3]
>     repo = os.environ.get("GITHUB_REPOSITORY", "")
>     if action == "rejected":
>         path = os.path.join(out, "rejected.txt")
>         why = open(path).read().strip() if os.path.exists(path) else "the planner run failed before handing anything back"
>         run = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
>         gh("issue", "comment", number, "-R", repo, "--body", f"**Plan rejected:** {why}\n\n[See the run]({run})")
>         return 0
>     try:
>         kind, result = read_output(out, number)
>         raw = result["raw"] if kind == "plan" else json.loads(result)
>         listed, bad = criterion_caps(raw)
>         more, too_long = words.summary_caps(raw["summary"])
>         listed, bad = more + listed, too_long + bad
>         if kind == "plan":
>             base = os.environ.get("PLANNER_BASE", "HEAD")
>             files = changed_files(base)
>             paths = [p for p in files if p.startswith("tests/") and p.endswith(".py")]
>             broken = unreadable(paths)
>             if broken:
>                 raise Garbled("; ".join(broken))
>             tc = test_changes

`13. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "git add\|git commit\|git push\|planner for\|try/issue" .github/workflows/agent.yml dokima/agent.py | head -30
```

> .github/workflows/agent.yml:103:          PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --json number -q '.[0].number' || true)
> .github/workflows/agent.yml:135:          if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
> .github/workflows/agent.yml:136:            git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
> .github/workflows/agent.yml:142:                echo "Merging main into try/issue-$N failed with no clashed file to resolve." > /tmp/why.txt
> .github/workflows/agent.yml:145:              git add -A && git -c user.name=dokima -c user.email=dokima@users.noreply.github.com commit -q --no-edit
> .github/workflows/agent.yml:150:            git checkout -q -B "try/issue-$N" origin/main
> .github/workflows/agent.yml:152:            echo "try/issue-$N does not exist; run the planner first." > /tmp/why.txt
> .github/workflows/agent.yml:237:          You are on branch try/issue-$N. Your stage is: ${STAGE:-$ROLE}.
> .github/workflows/agent.yml:325:      - name: Push the planner's tests or the worker's code to try/issue-N
> .github/workflows/agent.yml:334:          if [ "$ROLE" = planner ]; then git add tests; else git add -A; fi
> .github/workflows/agent.yml:337:            git commit -qm "$ROLE for #$N (run ${{ github.run_id }})"
> .github/workflows/agent.yml:338:            git push "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" "HEAD:try/issue-$N"
> .github/workflows/agent.yml:34

`14. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 300,345p .github/workflows/agent.yml
```

> SCRUB_GITHUB: ${{ github.token }}
>         run: |
>           python3 -c "
>           import os, dokima.agent as a
>           secrets = [v for k, v in os.environ.items() if k.startswith('SCRUB_')]
>           for f in a.jsonl_files('/home/runner/.claude/projects'):
>               t = open(f).read(); open(f, 'w').write(a.scrub(t, secrets))
>           "
>       - name: Save the hand-back and the full session log
>         if: always()
>         uses: actions/upload-artifact@v4
>         with:
>           name: ${{ env.ROLE }}-${{ env.N }}
>           path: |
>             /tmp/dokima-out/
>             /home/runner/.claude/projects/
>           if-no-files-found: warn
>           retention-days: 90
>       # The app's token for the result is minted only now, after the agent has finished.
>       - id: app
>         if: always()
>         uses: actions/create-github-app-token@v2
>         with:
>           app-id: ${{ vars.DOKIMA_APP_ID }}
>           private-key: ${{ secrets.DOKIMA_APP_KEY }}
>       - name: Push the planner's tests or the worker's code to try/issue-N
>         if: env.PASSED == 'true' && env.ROLE != 'reviewer'
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           SLUG: ${{ steps.app.outputs.app-slug }}
>         run: |
>           BOT_ID=$(gh api "users/${SLUG}[bot]" --jq .id)
>           git config user.name "${SLUG}[bot]"
>           git config user.email "${BOT_ID}+${SLUG}[bot]@users.noreply.github.com"
>           if [ "$ROLE" = planner ]; then git add tests; else git add -A; fi
>           if 

`15. Bash`
```
cd /home/runner/work/dokima/dokima; git diff origin/main -- tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py | wc -l; PYTHONPATH=$PWD timeout 900 python3 -m pytest -q -p no:cacheprovider tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py tests/test_autopilot_start.py tests/test_blocked_worker.py tests/test_hand_links.py 2>&1 | tail -25
```

> 0
>   
>   'github.' is contained here:
>     t'  and  !github.event.issue.pull_request  and  !('issues' == 'issues'  and  ('opened' == 'deleted'  or  'opened' == 'transferred')))
>   ?           +++++++
> FAILED tests/test_card_guard.py::test_bot_edits_do_not_retrigger_card - AssertionError: guard uses an unexpected context: 'issues' == 'workflow_run'  or  'issues' == 'schedule'  or  ('issues' == 'issues'  and  'edited' == 'opened')  or  ('Bot' != 'Bot'  and  !github.event.issue.pull_request  and  !('issues' == 'issues'  and  ('edited' == 'deleted'  or  'edited' == 'transferred')))
> assert 'github.' not in "'issues' ==...nsferred')))"
>   
>   'github.' is contained here:
>     t'  and  !github.event.issue.pull_request  and  !('issues' == 'issues'  and  ('edited' == 'deleted'  or  'edited' == 'transferred')))
>   ?           +++++++
> FAILED tests/test_autopilot_close.py::test_a_close_starts_every_sibling_whose_blockers_have_all_merged - TypeError: 'Nil' object is not subscriptable
> FAILED tests/test_autopilot_close.py::test_the_parent_closes_when_its_last_sub_issue_closes - TypeError: 'Nil' object is not subscriptable
> FAILED tests/test_autopilot_close.py::test_autopilot_goes_off_for_the_whole_tree_when_it_is_done - TypeError: 'Nil' object is not subscriptable
> FAILED tests/test_autopilot_close.py::test_a_close_off_autopilot_does_nothing - TypeError: 'Nil' object is not subscriptable
> FAILED tests/test_autopilot_close.py::test_a_child_planned_running_or_done_is_never_started_again - TypeError: 'Nil

**Agent:** The planner's three edited test files never reached the branch, so the 17 older tests still fail. Next I'm reading the planner's log to judge the edits they meant to make.

`16. Bash`
```
cd /home/runner/work/dokima/dokima; git show FETCH_HEAD:logs/254/37885045582-planner.md | sed -n 500,600p
```

> >     assert "Criterion 40.1: first thing works" in text and "Done when" not in text
> > 
> > 
> > def test_same_card_on_issue_and_pr_and_only_icons_change(record_property):
> >     record_property("proves", "67.6")
> >     assert render(checks=[], pr=None) != render()
> >     assert card.pr_body(render(), "Closes #40.\n\nSome prose.") == render() + "\n\nCloses #40"
> >     src = open(os.path.join(os.path.dirname(__file__), "..", "dokima", "card.py")).read()
> >     assert 'f"repos/{repo}/pulls/{pr_number}", "-F", "body=@pr.md"' in src
> >     yml = open(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "card.yml")).read()
> >     assert "types: [opened, edited]" in yml and "github.event.sender.type != 'Bot'" in yml
> > 
> > import os
> > import re
> > import sys
> > 
> > sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> > from dokima import card, plan  # noqa: E402
> 
> `19. Bash`
> ```
> cd /tmp/exp && git checkout -q tests/test_start.py && python3 - <<'E'
> p='tests/test_autopilot_close.py'; s=open(p).read()
> old='''WORKFLOWS = os.path.join(ts.ROOT, ".github", "workflows")
> '''
> new='''WORKFLOWS = os.path.join(ts.ROOT, ".github", "workflows")
> # card.yml also starts on a close, to redraw the cards (#254); it changes nothing autopilot reads, and its run on any
> # issue event is proven in tests/test_hand_links.py, so these tests leave it out rather than fake every card call.
> NOT_RUN_HERE = {"card.yml"}
> '''
> assert old in s; s=s.replace(old,new,1)
> old='''            if not fname.endswith

`17. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner kept the same two criteria, three requirements and 16 tests, and answered the code review's two blockers by listing four older tests under test_changes.",
   "The planner dropped the link to #253, which has closed."
  ],
  "decided": [
   "tests/test_card.py checks that card.yml still starts when an issue is opened or edited, instead of looking for the exact old trigger line; tests/test_card_guard.py reads the job's condition the way GitHub does.",
   "The test setup that runs every workflow started by a close leaves card.yml out, so the 14 autopilot tests no longer run it."
  ],
  "open": [
   "The three edited test files are not on try/issue-254, so the 17 older tests still fail."
  ]
 },
 "verdict": "block",
 "summary": "The plan says it fixed the 17 older tests that fail, but its edits to those test files never reached the branch, so the same 17 tests still fail and the worker could not make them pass.",
 "blockers": [
  {
   "id": "B3",
   "criterion": "254.4",
   "test": "tests/test_card_guard.py::test_bot_opened_issue_gets_a_card",
   "problem": "plan.json lists changes to tests/test_card.py, tests/test_card_guard.py and tests/test_autopilot_close.py under test_changes, and its replies call B1 and B2 fixed, but none of those files is changed on try/issue-254. The 17 older tests the code review blocked on still fail, and the worker is not allowed to edit tests.",
   "evidence": "git diff origin/main -- tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py prints nothing; no commit 'planner for #254 (run 37885045582)' exists on try/issue-254 (its newest planner commit is 1cb032a, run 37880667428); grep -rn NOT_RUN_HERE tests finds nothing. PYTHONPATH=$PWD pytest -q tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py tests/test_autopilot_start.py tests/test_blocked_worker.py tests/test_hand_links.py: 17 fa
```

> Exit code 1
> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> blocker B3 names tests/test_card_guard.py::test_bot_opened_issue_gets_a_card, which is not one of the plan's tests for 254.4

`18. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json
f='/tmp/dokima-out/review.json'; r=json.load(open(f))
r["summary"]="The plan's fixes to the 17 failing older tests never reached the branch, so those tests still fail and the worker cannot fix them."
r["blockers"][0]["test"]=None
r["issues_found"][0]["evidence"]="Planner run 37885045582 passed its check with three edited test files in its working tree (its log: ' M tests/test_autopilot_close.py', ' M tests/test_card.py', ' M tests/test_card_guard.py'), yet try/issue-254 has no commit from that run; the only later commit is e5cd672, a merge from main."
json.dump(r,open(f,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 254 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I've blocked the plan for #254 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

**Why it's blocked (B3, for the planner):** the plan lists edits to three older test files (`tests/test_card.py`, `tests/test_card_guard.py`, `tests/test_autopilot_close.py`) and says the code review's B1 and B2 are fixed. But none of those edits is on `try/issue-254`:
- `git diff origin/main` on those three files prints nothing.
- There is no commit from planner run 37885045582 on the branch.
- The planner's own log ends with "The edited test files are in the working tree, not committed."

I ran the six affected test files on the branch: 17 failed and 32 passed. These are the same 17 older tests the code review blocked on, and the worker isn't allowed to edit tests. The fix is for the planner to make the same three edits again so they land on the branch, then check that all 49 tests in those files pass.

**What else I found:**
- **The intended edits look right.** From the log, they keep the existing checks and only change how `card.yml`'s triggers and condition are read. One trade-off: once `card.yml` is left out of the close tests, those 14 autopilot tests no longer catch `card.yml` breaking when an issue closes.
- **The plan itself is fine.** The criteria and the 16 tests are unchanged. Every ask from the issue and from your 03:44 comment still maps to a criterion, and you haven't commented since.
- **Proposed new issue:** a planner run can pass its check and still lose its test edits without saying so. I don't know why the push didn't happen here. The only later commit on the branch is a merge from main.
