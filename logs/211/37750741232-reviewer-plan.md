# reviewer (plan) for #211

Run: https://github.com/dokima-dev/dokima/actions/runs/37750741232

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; echo ====; cat open_blockers.json; echo ====; cat plan.json
```

> <persisted-output>
> Output too large (99.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/053377fd-c2d4-4176-8f2c-5de5e1fc28be/tool-results/bmtlku36o.txt
> 
> Preview (first 2KB):
> .:
> total 120
> drwxr-xr-x  3 runner runner  4096 Oct  8 08:34 .
> drwxrwxrwt 18 root   root    4096 Oct  8 08:34 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 08:34 in
> -rw-r--r--  1 runner runner 90799 Oct  8 08:34 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 08:34 open_blockers.json
> -rw-r--r--  1 runner runner  9533 Oct  8 08:34 plan.json
> 
> in:
> total 104
> drwxr-xr-x 2 runner runner  4096 Oct  8 08:34 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 08:34 ..
> -rw-r--r-- 1 runner runner  7629 Oct  8 08:34 01-planner.json
> -rw-r--r-- 1 runner runner  8235 Oct  8 08:34 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10096 Oct  8 08:34 03-planner.json
> -rw-r--r-- 1 runner runner  4992 Oct  8 08:34 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  5272 Oct  8 08:34 05-worker.json
> -rw-r--r-- 1 runner runner  4116 Oct  8 08:34 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner  9467 Oct  8 08:34 07-planner.json
> -rw-r--r-- 1 runner runner  4515 Oct  8 08:34 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner  3374 Oct  8 08:34 09-worker.json
> -rw-r--r-- 1 runner runner  2106 Oct  8 08:34 10-reviewer-pr.json
> -rw-r--r-- 1 runner runner 10196 Oct  8 08:34 11-planner.json
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
> 
> <!-- doki

`2. Bash`
```
cd /tmp/pack; python3 -c "
s=open('issue.md').read()
print(len(s))
print(s[:30000])
"
```

> <persisted-output>
> Output too large (29.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/053377fd-c2d4-4176-8f2c-5de5e1fc28be/tool-results/bf612h9ms.txt
> 
> Preview (first 2KB):
> 90731
> # Issue #211: Autopilot: an approved plan starts the worker, and autopilot still stops where the owner must decide
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #220](https://github.com/dokima-dev/dokima/pull/220) · [files changed](https://github.com/dokima-dev/dokima/pull/220/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37746497322/job/113209109429)
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #205, story 3</summary>
> 
> **Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 
> **User story:** On autopilot, an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`, and the river still stops and mentions the owner wherever the owner must decide.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Let me read in chunks with Read.

`3. Read`
```
/tmp/pack/issue.md
```

> 20	
> 21	**Part of:** #205 Autopilot: /autopilot start runs an issue tree end to end, stopping only where the owner must decide
> 22	
> 23	**User story:** On autopilot, an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`, and the river still stops and mentions the owner wherever the owner must decide.
> 24	
> 25	**Context:** The river is next_step in dokima/agent.py: today a plan review's approve stops with 'Say `/work` to build it' unless test_fix() holds. On autopilot it should start the worker instead; an approved split (kind feature) should file its stories as `/work` does (agent.py `split`, commands.yml). Every other stop already exists in next_step: questions, escalate, three blocks in a row (rounds=3), a rejected hand-back and a run that failed or never started; board_place puts Needs you on every stop. 'Silent failures' in the issue reads as a run that failed or never started. The owner confirmed `/autopilot start` picks up what is already waiting, so an approved plan already waiting for `/work` starts too. The owner asked (comment of 2026-10-08 06:29) that wherever they would have typed a command, autopilot posts one short line in its place, like 'Autopilot: plan approved, starting work'; the line is posted by code on the issue, exactly once per hand-off, and is the bot's comment, so it starts nothing by itself (only a code owner's commands count).
> 26	
> 27	**Acceptance criteria:**

`4. Bash`
```
cd /tmp/pack; grep -n '^### ' issue.md
```

> 4:### Approve the result to merge
> 43:### RezaSoleymanifar on issue #211 (2026-10-08T06:56:48Z)
> 47:### RezaSoleymanifar on issue #211 (2026-10-08T06:58:15Z)
> 51:### dokima-runtime on issue #211 (2026-10-08T06:58:34Z)
> 182:### dokima-runtime on issue #211 (2026-10-08T07:13:24Z)
> 328:### dokima-runtime on issue #211 (2026-10-08T07:15:50Z)
> 476:### dokima-runtime on issue #211 (2026-10-08T07:21:58Z)
> 604:### RezaSoleymanifar on issue #211 (2026-10-08T07:27:05Z)
> 608:### dokima-runtime on issue #211 (2026-10-08T07:27:24Z)
> 670:### dokima-runtime on PR #220 (2026-10-08T07:44:08Z)
> 770:### dokima-runtime on issue #211 (2026-10-08T07:50:02Z)
> 915:### dokima-runtime on issue #211 (2026-10-08T07:55:52Z)
> 1035:### dokima-runtime on PR #220 (2026-10-08T08:03:01Z)
> 1090:### dokima-runtime on PR #220 (2026-10-08T08:07:01Z)
> 1170:### RezaSoleymanifar on issue #211 (2026-10-08T08:25:57Z)
> 1174:### dokima-runtime on issue #211 (2026-10-08T08:26:17Z)
> 1316:### dokima-runtime on issue #211 (2026-10-08T08:34:29Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 600,612p issue.md; echo ...; sed -n 1165,1180p issue.md; echo; sed -n 1316,1500p issue.md
```

> **Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 
> 
> ### RezaSoleymanifar on issue #211 (2026-10-08T07:27:05Z)
> 
> /work
> 
> ### dokima-runtime on issue #211 (2026-10-08T07:27:24Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Worker**
> 
> ...
> <sub>Opus 5.5 · 3.5 min · 11 turns · 444,933 tokens in, 3,446 out · $0.53 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/211/37747715025-reviewer-pr.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37747715025)</sub>
> 
> **Next:** @RezaSoleymanifar The work is approved. Merge the pull request, or review it with a command to send it back.
> 
> 
> ### RezaSoleymanifar on issue #211 (2026-10-08T08:25:57Z)
> 
> /plan The PR clashes with main after #213 merged. Re-plan on top of today's main.
> 
> ### dokima-runtime on issue #211 (2026-10-08T08:26:17Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Planner**
> 
> On autopilot an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`; a planner's question stops only when the plan reviewer cannot match its assumption to the owner's own words; and the river still stops and mentions the ow

`6. Bash`
```
cd /tmp/pack; cat plan.json; echo; python3 -c "
import json
d=json.load(open('in/11-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])
h=d.get('handback',{});print(h.get('notes'), h.get('test_changes'), [k for k in h])
"
```

> {
>  "kind": "user_story",
>  "user_story": "On autopilot an approved plan goes straight to the worker and an approved split files itself, each with one Autopilot line where the owner would have typed `/work`; a planner's question stops only when the plan reviewer cannot match its assumption to the owner's own words; and the river still stops and mentions the owner wherever the owner must decide.",
>  "acceptance_criteria": [
>   {
>    "text": "On an issue on autopilot, a plan review that approves starts the worker by itself, and so does `/autopilot start` said on an issue whose plan is already approved and waiting for `/work`. The issue gets exactly one comment reading `Autopilot: plan approved, starting work`, the review's card ends \"Next: The worker starts now.\" with no Needs you, and no comment says no stage was started. A plan already handed to the worker, by autopilot or by the owner's `/work`, is not started again, and a code review's approval still stops for the owner.",
>    "source": "https://github.com/dokima-dev/dokima/issues/211"
>   },
>   {
>    "text": "On an issue on autopilot, an approved split files its stories as sub-issues by itself, as `/work` would, and so does `/autopilot start` said on an issue whose split is approved and not yet filed. The issue gets one Split filed record and exactly one comment reading `Autopilot: split approved, filing its stories`, and no worker starts. As `/work` on autopilot does today, every story is filed on autopilot and each story with no

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -2; git log --oneline -3 origin/main; git merge-base --is-ancestor origin/main HEAD && echo CONTAINS_MAIN || echo NOT; git merge-tree --write-tree HEAD origin/main | head -20; git diff --stat origin/main...HEAD; git show --stat HEAD | head -20
```

> f1b30ab Autopilot: children start once their blockers merge, and the tree switches itself off when done (#218)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
> 4cccffe Live card: minutes and the current step while the agent works (#216)
> NOT
> 46223462c41e5dc4ef10f6c24b8623175ee06b1b
> 100644 f57cf798bac7a5819f34de4e97af0e4c4dc34cf3 1	AGENTS.md
> 100644 1ab67380d78936d4814c06180aa5a3a1e0201f9a 2	AGENTS.md
> 100644 364de292b88931489655e220ede6e70de9d8733a 3	AGENTS.md
> 100644 42def94497917e7892a342c821ecf25924ae2fc6 1	dokima/agent.py
> 100644 451957257ee1c9383adfc0e5158658eea962dd93 2	dokima/agent.py
> 100644 b5467eeb4a116571edc47a2aa88410f81d5afa67 3	dokima/agent.py
> 
> Auto-merging .github/workflows/agent.yml
> Auto-merging AGENTS.md
> CONFLICT (content): Merge conflict in AGENTS.md
> Auto-merging dokima/agent.py
> CONFLICT (content): Merge conflict in dokima/agent.py
>  .github/workflows/agent.yml    |  21 +-
>  .github/workflows/commands.yml |  20 +-
>  AGENTS.md                      |   6 +-
>  dokima/agent.py                | 212 ++++++++++++++--
>  dokima/roles/reviewer.md       |  15 +-
>  tests/test_autopilot_river.py  | 545 +++++++++++++++++++++++++++++++++++++++++
>  tests/test_start.py            |   2 +
>  7 files changed, 797 insertions(+), 24 deletions(-)
> commit 1b009ff8fa3b16d4b430a16a7c5b1399a1fcae44
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 08:34:16 2026 +0000
> 
>     planner for #211 (run 37749798

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n -B3 -A25 "Starting branch" .github/workflows/agent.yml | head -60
```

> 106-            echo "::warning title=No live card::the card could not be put up; the record is posted at the end"
> 107-          fi
> 108-          gh api -X DELETE installation/token --silent || echo "::warning title=Key not revoked::the card's key could not be revoked"
> 109:      - name: Starting branch
> 110-        env:
> 111-          GH_TOKEN: ${{ github.token }}
> 112-        run: |
> 113-          if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
> 114-            git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
> 115-            if [ "$ROLE" = worker ]; then
> 116-              git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
> 117-            fi
> 118-          elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
> 119-            # A plan review needs no branch: a split never makes one, so it reviews from main.
> 120-            git checkout -q -B "try/issue-$N" origin/main
> 121-          else
> 122-            echo "try/issue-$N does not exist; run the planner first." > /tmp/why.txt
> 123-            echo "::error title=Nothing to $ROLE::$(cat /tmp/why.txt)"; exit 1
> 124-          fi
> 125-          echo "BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> 126-          # A plan's tests are everything the issue's branch added since it split off main, over every planning round.
> 127-          echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
> 128-          # What this run

**Agent:** Reviewing the re-planned #211: the branch still clashes with main, so I'm checking the new tests against today's main next.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wm; git worktree add -q /tmp/wm origin/main 2>&1|tail -1; cp tests/test_autopilot_river.py /tmp/wm/tests/; cp tests/test_start.py /tmp/wm/tests/; cd /tmp/wm; python -m pytest -q tests/test_autopilot_river.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-300; python -m pytest -q tests/test_start.py 2>&1 | tail -2
```

> assert r.agent_started() and not r.failed, f"211.1: setup: the plan review did not run:\n{r.tail()}"
>         assert not m.failed, f"211.1: the listener failed on /autopilot start:\n{m.tail()}"
>         """On autopilot the river still stops on an escalation, three blocks in a row, a rejected hand-back and a run that failed or never started.
>         Decides what follows a passed plan that has two questions for the owner. On autopilot the plan reviewer must start
> >           assert code != 0, f"211.5 ({case}): the check passed a plan review that does not judge every question properly"
> E           AssertionError: 211.5 (none judged): the check passed a plan review that does not judge every question properly
>         assert r.agent_started() and not r.failed, f"211.5: setup: the plan review did not pass its check:\n{r.tail()}"
> E               AssertionError: 211.5: the review's card does not show the question of an accepted assumption ('Should a failed run move its card to Needs you?'):
> E                 <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Reviewer (plan)**
> E               assert 'Should a failed run move its card to Needs you?' in '<!-- dokima-record -->\n<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" w...eviation.\n\n<details><summary>What the previous step did</summary>\n\n- **Did:** Planned one story.\n\
> FAILED tests/test_a

`10. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/ | head -40; python -m pytest -q tests/test_autopilot_river.py 2>&1 | tail -3
```

> commit 1b009ff8fa3b16d4b430a16a7c5b1399a1fcae44
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 08:34:16 2026 +0000
> 
>     planner for #211 (run 37749798848)
> 
> diff --git a/tests/test_autopilot_river.py b/tests/test_autopilot_river.py
> index 1b7d864..92d7904 100644
> --- a/tests/test_autopilot_river.py
> +++ b/tests/test_autopilot_river.py
> @@ -272,11 +272,24 @@ def test_autopilot_start_starts_the_worker_on_a_plan_already_waiting_for_work(re
>          assert autopilot_lines(m) == [], f"211.1 ({case}): /autopilot start posted another Autopilot line: {autopilot_lines(m)}"
>  
>  
> +def assert_stories_as_work_files_them(m, case):
> +    """The split's stories were filed as `/work` files them on autopilot: each on autopilot, and only the unblocked one planning."""
> +    for c in m.created_issues():
> +        given = [c[j + 1] for j, x in enumerate(c[:-1]) if x in ("--label", "-l")]
> +        assert "autopilot" in [l.strip() for v in given for l in v.split(",")], \
> +            f"211.2 ({case}): a story was filed off autopilot, unlike `/work` on autopilot: {c[:6]} labels {given}"
> +    planners = sorted(s for s in starts(m) if s[0] == "planner")
> +    assert planners == [("planner", "900")], (f"211.2 ({case}): the stories did not start as `/work` on autopilot starts "
> +                                              f"them (only #900, which waits on nothing, plans): {planners}")
> +
> +
>  def test_on_autopilot_an_approved_split_files_its_stories_with_one_

`11. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['08-reviewer-plan.json','10-reviewer-pr.json']:
  d=json.load(open('in/'+f));h=d['handback'];print(f,h['verdict'],h['summary']);print(json.dumps(h.get('asks'),indent=0));print(json.dumps(h.get('notes'),indent=0)); print(h.get('issues_found'))
"
```

> 08-reviewer-plan.json approve The planner fixed the code review's blocker by giving the test machine the real AGENTS.md; the criteria are unchanged, all 11 tests of this issue fail on main because the feature is missing and pass on the branch.
> [
> {
> "ask": "On an issue on autopilot, a plan review that approves starts the worker by itself, and so does `/autopilot start` said on an issue whose plan is already approved and waiting for `/work`; the issue gets exactly one comment reading `Autopilot: plan approved, starting work`, the card's Next line says the worker starts now, and no Needs you is set.",
> "source": "https://github.com/dokima-dev/dokima/issues/211",
> "criterion": "211.1"
> },
> {
> "ask": "On an issue on autopilot, an approved split files its stories as sub-issues by itself, as `/work` would, and so does `/autopilot start` said on an issue whose split is already approved; the issue gets exactly one comment reading `Autopilot: split approved, filing its stories`.",
> "source": "https://github.com/dokima-dev/dokima/issues/211",
> "criterion": "211.2"
> },
> {
> "ask": "On an issue not on autopilot, an approved plan or split still stops for the owner, exactly as today, and no Autopilot line is posted.",
> "source": "https://github.com/dokima-dev/dokima/issues/211",
> "criterion": "211.3"
> },
> {
> "ask": "On autopilot, the river still stops on ... an escalation, three blocking reviews in a row, a hand-back code rejected and a run that failed or never started; each stop says why on the issue, ment

`12. Bash`
```
cd /tmp/wm; grep -n "autopilot" AGENTS.md | head; grep -n "def start_waiting\|def split" dokima/agent.py
```

> 55:On autopilot, the river runs a whole issue tree end to end and stops for the owner only where the owner must decide (planned, story 2 of #205); `/autopilot start` and `/autopilot stop` switch it on and off. When an issue closes, every issue on autopilot whose blocked-by issues have now all closed starts its planner, with one line `Autopilot: blockers merged, starting plan` where the owner would have said `/plan`; a parent whose last sub-issue closes closes too, saying its whole tree is done, which counts as a close one level up; and when the top issue closes, its whole tree goes off autopilot. Closes are handled one at a time, in one queue for the repo (autopilot.yml), and an issue already planned, running or started is never started again.
> 64:- `/autopilot start` / `/autopilot stop`: put the issue, or the issue a PR was built for, and every sub-issue under it at every level on or off autopilot (the `autopilot` label). It starts no stage on that issue itself, and leaves one comment where it was said naming every issue it switched. `/autopilot start` picks up what is waiting: every issue under it, at every level, with no sub-issues, no plan and nothing open to wait for starts its planner. A split filed by `/work` on autopilot puts its stories on autopilot and starts the ones with nothing to wait for.
> 876:def start_waiting(repo, numbers, need_blocker=False):
> Shell cwd was reset to /home/runner/work/dokima/dokima

`13. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Re-planned on today's main: 211.2 now also promises that, as `/work` on autopilot does since #213, every filed story is on autopilot and only a story with nothing to wait for starts its planner.",
   "Added that check to the split test and dropped the out-of-scope line that kept filed stories off autopilot."
  ],
  "decided": [
   "Kept the other five criteria, the scope and the tests as approved; starting the next sibling and closing a finished tree stay with #213."
  ],
  "open": [
   "The branch still clashes with main in dokima/agent.py and AGENTS.md; a planner may only change tests, so someone must resolve the clash on the branch or delete the branch before `/work`, or the worker fails before it starts."
  ]
 },
 "verdict": "approve",
 "summary": "The plan now matches today's main and all 11 tests fail on main because the feature is missing, but the branch still clashes with main, so `/work` will fail at its first step until the clash is resolved on the branch or the branch is deleted.",
 "blockers": [],
 "notes": [
  {
   "text": "Your ask to re-plan on today's main is done in the plan, but not on the branch: the branch still clashes with main, and the worker's run merges main first, so it stops there and never builds. The planner says so in its first concern; resolve the clash on try/issue-211 (keeping both #213's and this story's changes) or delete the branch so the worker rebuilds on main, then say `/work`.",
   "evidence": "git merge-tree HEAD origin/main (1b009ff vs f1b30ab): CONFLICT in AGENTS.md and dokima/agent.py; .github/workflows/agent.yml 'Starting branch' line 116 merges origin/main for the worker."
  },
  {
   "text": "Every new test fails on main for the right reason, and on the branch only the changed split test fails, because the branch's code predates #213 and files stories off autopilot.",
   "evidence": "Branch tests copied onto a worktr
```

> rc=0

`14. Bash`
```
cd /tmp/pack; python3 -c "
import json;print(json.load(open('in/07-planner.json'))['handback']['acceptance_criteria'][1]['text'])"
```

> On an issue on autopilot, an approved split files its stories as sub-issues by itself, as `/work` would, and so does `/autopilot start` said on an issue whose split is approved and not yet filed. The issue gets one Split filed record and exactly one comment reading `Autopilot: split approved, filing its stories`, and no worker starts; a split already filed is not filed again.
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** I approved the re-planned #211, but `/work` will fail until someone fixes the branch: `try/issue-211` still clashes with today's main in `dokima/agent.py` and `AGENTS.md`. The worker's run merges main first (`.github/workflows/agent.yml:116`) and will stop there before building anything. The planner can only change tests, so it couldn't fix this, and it says so in its first concern. Before `/work`, you need to do one of these:
- resolve the clash on the branch, keeping both #213's changes and this story's, or
- delete the branch so the worker rebuilds this story on today's main.

**What the planner changed:** acceptance criterion 211.2 now matches how `/work` files a split on autopilot since #213. Every filed story goes on autopilot, and only a story that isn't waiting on another one starts its planner. It also removed the out-of-scope line that kept filed stories off autopilot, since that now contradicts main. The other five criteria are unchanged.

**Test results:**
- **On today's main:** all 11 new tests fail because the feature is missing, not because anything crashes.
- **On the branch:** 10 pass. The one that fails is the changed split test, because the branch's code predates #213.

**Why it waits for you:** 211.2 changed in this round, so the worker won't start on its own even after the clash is fixed.

**Your asks:** all of them map to a criterion, including "Re-plan on top of today's main", which maps to 211.2.

I also proposed one new issue: when another merge clashes with an issue's branch, its worker run fails with no way for an agent to recover, so the issue stalls until a person fixes it by hand.

The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.
