# reviewer (plan) for #254

Run: https://github.com/dokima-dev/dokima/actions/runs/37886890738

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (129KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a8e6ef4e-4287-452b-8d9f-596f3a2d2923/tool-results/b97gdhgjq.txt
> 
> Preview (first 2KB):
> .:
> total 152
> drwxr-xr-x  3 runner runner   4096 Oct  9 05:05 .
> drwxrwxrwt 18 root   root     4096 Oct  9 05:05 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 05:05 in
> -rw-r--r--  1 runner runner 129540 Oct  9 05:05 issue.md
> -rw-r--r--  1 runner runner   1548 Oct  9 05:05 open_blockers.json
> -rw-r--r--  1 runner runner   7421 Oct  9 05:05 plan.json
> 
> in:
> total 80
> drwxr-xr-x 2 runner runner 4096 Oct  9 05:05 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 05:05 ..
> -rw-r--r-- 1 runner runner 5217 Oct  9 05:05 01-planner.json
> -rw-r--r-- 1 runner runner 4014 Oct  9 05:05 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6068 Oct  9 05:05 03-planner.json
> -rw-r--r-- 1 runner runner 5002 Oct  9 05:05 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7432 Oct  9 05:05 05-worker.json
> -rw-r--r-- 1 runner runner 5600 Oct  9 05:05 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 8389 Oct  9 05:05 07-planner.json
> -rw-r--r-- 1 runner runner 6237 Oct  9 05:05 08-reviewer-plan.json
> -rw-r--r-- 1 runner runner 8075 Oct  9 05:05 09-planner.json
> # Issue #254: A link added or removed by hand on GitHub updates the cards of both issues
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 294 -->
> A blocked-by link added or removed by hand shows on both issues' cards once either issue changes, and within 15 min

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat plan.json; echo; wc -c issue.md; grep -n '^## \|^### \|^---' issue.md | head -80
```

> [
>  {
>   "id": "B3",
>   "criterion": "254.4",
>   "test": null,
>   "problem": "plan.json lists changes to tests/test_card.py, tests/test_card_guard.py and tests/test_autopilot_close.py under test_changes, and its replies call B1 and B2 fixed, but none of those files is changed on try/issue-254. The 17 older tests the code review blocked on still fail, and the worker is not allowed to edit tests.",
>   "evidence": "git diff origin/main -- tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py prints nothing; no commit 'planner for #254 (run 37885045582)' exists on try/issue-254 (its newest planner commit is 1cb032a, run 37880667428); grep -rn NOT_RUN_HERE tests finds nothing. PYTHONPATH=$PWD pytest -q tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py tests/test_autopilot_start.py tests/test_blocked_worker.py tests/test_hand_links.py: 17 failed, 32 passed, the same 17 (2 in test_card_guard.py with 'guard uses an unexpected context', 1 in test_card.py, 14 with \"'Nil' object is not subscriptable\"). The planner's log ends with 'The edited test files are in the working tree, not committed.'",
>   "fix": "Make the three test edits the plan describes again (test_card.py reads card.yml's issue triggers with load_yaml and still needs opened and edited; test_card_guard.py's runs() uses test_start's evaluate; test_autopilot_close.py's harness skips card.yml via NOT_RUN_HERE with its reason) so they land on try/issue-254, and check that all 49 tests in t

`3. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 40,96p /tmp/pack/issue.md; sed -n 420,430p /tmp/pack/issue.md; git log --oneline -8; git fetch origin main -q 2>&1|tail -1; git diff --stat origin/main...HEAD; git diff --stat origin/main
```

> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Non-functional requirement:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37885285681/job/113673838762">A run rewrites another issue's card only when its links or loop changed. A change on one issue rewrites no unrelated card, and a scheduled run with nothing changed writes nothing on GitHub.</a>
>   - *<a href="https://github.com/dokima-dev/dokima/blob/e5cd672fe9798dde6b683711159694bee279da78/tests/test_hand_links.py#L570"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: The scheduled run rewrites only the cards whose links changed.*
>   - *<a href="https://github.com/dokima-dev/dokima/blob/e5cd672fe9798dde6b683711159694bee279da78/tests/test_hand_links.py#L586"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/verified-by.svg" width="16" height="16" align="absmiddle" alt="verified by"> Verified by</a>: A change on one issue rewrites another issue's card only when that card's links changed.*
> 
> </details>
> 
> **Scope:**
> 
> - dokima/card.py
> - dokima/agent.py
> - .github/workflows/card.yml
> - AGENTS.md
> - tests/test_hand_links.py
> 
> **Out of scope:**
> 
> - Relates-to links: GitHub has no native relates-to link, so a person cannot make one by hand.
> - Clearing Needs you when a hand-ma

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; git diff origin/main -- tests/test_autopilot_close.py tests/test_card.py tests/test_card_guard.py; PYTHONPATH=$PWD pytest -q tests/test_card.py tests/test_card_guard.py tests/test_autopilot_close.py tests/test_autopilot_start.py tests/test_blocked_worker.py tests/test_hand_links.py 2>&1 | tail -3
```

> commit 7cc2962ac17a03c09e49df251d4a6b0e108de67c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 05:04:52 2026 +0000
> 
>     planner for #254 (run 37886104404)
> 
>  tests/test_autopilot_close.py |  6 +++++-
>  tests/test_card.py            |  9 ++++++++-
>  tests/test_card_guard.py      | 17 ++++++-----------
>  3 files changed, 19 insertions(+), 13 deletions(-)
> diff --git a/tests/test_autopilot_close.py b/tests/test_autopilot_close.py
> index 671d781..3aad1af 100644
> --- a/tests/test_autopilot_close.py
> +++ b/tests/test_autopilot_close.py
> @@ -37,6 +37,10 @@ from test_start import N, OWNER, Ctx, evaluate, condition
>  LABEL = "autopilot"
>  LINE = "Autopilot: blockers merged, starting plan"
>  WORKFLOWS = os.path.join(ts.ROOT, ".github", "workflows")
> +# Workflows a close starts that this harness leaves out, with why. card.yml (#254) redraws cards on every issue event;
> +# it changes nothing autopilot reads, needs a fake GitHub for the card's own calls, and its start on a close is proven
> +# in tests/test_hand_links.py.
> +NOT_RUN_HERE = {"card.yml": "redraws cards only; proven in tests/test_hand_links.py"}
>  
>  TREE_GH = r'''
>  def jload(name, default):
> @@ -331,7 +335,7 @@ class Repo(ts.Machine):
>          open(f"{self.tmp}/event.json", "w").write(json.dumps(github["event"]))
>          ran = []
>          for fname in sorted(os.listdir(WORKFLOWS)):
> -            if not fname.endswith((".yml", ".yaml")):
> +            if not fname.endswith((".yml", ".yaml"))

`5. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['07-planner.json','09-planner.json']:
  d=json.load(open(f)); 
  print(f, list(d.keys()))
" ; python3 - <<'E'
import json
a=json.load(open('07-planner.json')); b=json.load(open('09-planner.json'))
def p(d):
  for k in ('handback','hand_back','plan','output'):
    if k in d: return d[k]
  return d
A,B=p(a),p(b)
for k in set(A)|set(B):
  if A.get(k)!=B.get(k): print('DIFF',k)
E
cat 08-reviewer-plan.json | python3 -m json.tool | head -80
```

> 07-planner.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> 09-planner.json ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> DIFF replies
> {
>     "role": "reviewer",
>     "stage": "plan",
>     "run_id": "37885878317",
>     "commit_before": "e5cd672fe9798dde6b683711159694bee279da78",
>     "started_by": "dokima-runtime[bot]",
>     "models": [
>         "claude-opus-5-5"
>     ],
>     "report": {
>         "duration_ms": 135933,
>         "turns": 19,
>         "cost_usd": 0.8700424000000001,
>         "tokens_in": 1054489,
>         "tokens_out": 8318
>     },
>     "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/254/37885878317-reviewer-plan.md",
>     "run": "https://github.com/dokima-dev/dokima/actions/runs/37885878317",
>     "handback": {
>         "previous_step": {
>             "did": [
>                 "The planner kept the same two criteria, three requirements and 16 tests, and answered the code review's two blockers by listing four older tests under test_changes.",
>                 "The planner dropped the link to #253, which has closed."
>             ],
>             "decided": [
>                 "tests/test_card.py checks that card.yml still starts when an issue is opened or edited, instead of looking for the exact old trigger line; tests/test_card_guard.py reads the job's condition the way GitHub does.",
>                 "The test setup that runs every workflo

**Agent:** I've confirmed the planner's three test edits are now on the branch and all 49 tests in the six affected files pass. Next I'm running the full suite and pulling the earlier list of the owner's asks.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;d=json.load(open('/tmp/pack/in/08-reviewer-plan.json'))['handback'];print(json.dumps({k:d[k] for k in ('asks','assumptions','resolved') if k in d},indent=1))"; PYTHONPATH=$PWD timeout 590 pytest -q -x -n 8 2>&1 | tail -3 || true
```

> {
>  "asks": [
>   {
>    "ask": "When a person adds a blocked-by link by hand on GitHub (#A blocked by #B), with no command, the card of #A shows #B on its Blocked by line and the card of #B shows #A on its Blocks line",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.1"
>   },
>   {
>    "ask": "when the person removes it, neither card shows it any more. No comment is posted on either issue for the link.",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.1"
>   },
>   {
>    "ask": "When a link added by hand makes two issues block each other, directly or through other issues, the cards of both issues say which issues block each other",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.2"
>   },
>   {
>    "ask": "on autopilot the river stops for the owner on them",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.2"
>   },
>   {
>    "ask": "The link lines on a card come from GitHub's own blocked-by links read when the card is drawn, so a card never shows a blocking link GitHub no longer has",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.3"
>   },
>   {
>    "ask": "if GitHub cannot list them, the card says so instead of showing no links",
>    "source": "https://github.com/dokima-dev/dokima/issues/254",
>    "criterion": "254.3"
>   },
>   {
>    "ask": "make it trigger-based wherever GitHub announces something (any change on either issu

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n 'issuecomment\|RezaSoleymanifar on' /tmp/pack/issue.md | head; PYTHONPATH=$PWD timeout 590 pytest -q 2>&1 | tail -3
```

> 426:### RezaSoleymanifar on issue #254 (2026-10-09T03:44:38Z)
> ........................................................................ [ 95%]
> ...............................                                          [100%]
> 751 passed in 398.01s (0:06:38)

`8. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json
asks=json.load(open('/tmp/pack/in/08-reviewer-plan.json'))['handback']['asks']
r={"previous_step":{"did":["The planner committed its three edits to older tests on try/issue-254 (tests/test_card.py, tests/test_card_guard.py, tests/test_autopilot_close.py).","The planner kept the same two criteria, three requirements and 16 tests as the plan before."],
 "decided":["tests/test_card.py checks that card.yml still starts when an issue is opened or edited; tests/test_card_guard.py reads the job's condition the way GitHub does; the close test setup leaves card.yml out, with its reason."],
 "open":[]},
 "verdict":"approve",
 "summary":"The planner's fixes to the 17 older failing tests are now on the branch, and every test passes, so the unchanged plan can go back to the worker.",
 "blockers":[],
 "notes":[{"text":"Leaving card.yml out of the close test setup means the 14 autopilot close tests no longer catch card.yml breaking on a close; tests/test_hand_links.py proves only that it starts there.","evidence":"tests/test_autopilot_close.py: NOT_RUN_HERE = {\"card.yml\": ...} skipped in Repo.close's workflow loop."}],
 "resolved":["B3"],
 "issues_found":[],
 "asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 254 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json
p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The planner's fixes to the 17 failing older tests are now on the branch and every test passes, so the unchanged plan can go ahead."
json.dump(r,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 254 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #254, and I've written the hand-back to `/tmp/dokima-out/review.json`. Both checks on it pass.

- **Blocker B3 is resolved.** Last round, the planner's edits to three older test files never reached the branch. They are now on `try/issue-254` in commit `7cc2962`:
  - `tests/test_card.py` now reads `card.yml`'s triggers and still fails if opening or editing an issue stops starting a card.
  - `tests/test_card_guard.py` now reads the job's condition the way GitHub does.
  - The test setup that runs every workflow a close starts now leaves `card.yml` out, with its reason written next to it.
- **The tests pass.** All 49 tests in the six affected files pass, including the 17 that failed before, and the full suite passes: 751 tests.
- **The plan itself is unchanged.** It has the same two criteria, three requirements and 16 tests as the previous plan. Only its replies are new, and every ask of the owner still maps to a criterion, including their answer asking for updates on any change, with a schedule only as a backstop.
- **One note, not a blocker:** because `card.yml` is left out of the close tests, those 14 autopilot tests no longer catch `card.yml` breaking when an issue closes. `tests/test_hand_links.py` only proves that it starts then.

Since the criteria are unchanged, this re-plan should go straight to the worker.
