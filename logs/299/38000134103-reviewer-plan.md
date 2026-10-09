# reviewer (plan) for #299

Run: https://github.com/dokima-dev/dokima/actions/runs/38000134103

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (77.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/72fdb955-1b10-46c0-8239-3a736a0dddf6/tool-results/b647ffwyx.txt
> 
> Preview (first 2KB):
> .:
> total 100
> drwxr-xr-x  3 runner runner  4096 Oct  9 22:36 .
> drwxrwxrwt 18 root   root    4096 Oct  9 22:36 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 22:36 in
> -rw-r--r--  1 runner runner 73040 Oct  9 22:36 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 22:36 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 22:36 parent.json
> -rw-r--r--  1 runner runner  5369 Oct  9 22:36 plan.json
> 
> in:
> total 80
> drwxr-xr-x 2 runner runner 4096 Oct  9 22:36 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 22:36 ..
> -rw-r--r-- 1 runner runner 5244 Oct  9 22:36 01-planner.json
> -rw-r--r-- 1 runner runner 7570 Oct  9 22:36 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6727 Oct  9 22:36 03-planner.json
> -rw-r--r-- 1 runner runner 6870 Oct  9 22:36 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6514 Oct  9 22:36 05-planner.json
> -rw-r--r-- 1 runner runner 5319 Oct  9 22:36 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1712 Oct  9 22:36 07-worker.json
> -rw-r--r-- 1 runner runner 2148 Oct  9 22:36 08-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5478 Oct  9 22:36 09-planner.json
> -rw-r--r-- 1 runner runner 6004 Oct  9 22:36 10-planner.json
> # Issue #299: Cards show what was raised and how each earlier raise was answered
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298 -->
> <!-- dok

`2. Bash`
```
cd /tmp/pack; cat parent.json open_blockers.json; echo; cat plan.json; echo; wc -l issue.md
```

> {"number": 289}[]
> {
>  "kind": "user_story",
>  "summary": "Run comments and the issue card show what an agent raised in one Raised section, and a review shows how it answered earlier raises.",
>  "user_story": "The owner reads every question, blocker and issue a run raised in one Raised section that says who each one is for, and on a review sees how each earlier raise was answered, without ever seeing an ID.",
>  "acceptance_criteria": [
>   {
>    "text": "A run comment shows one Raised section with every raise of the run. The issue card shows one Raised section with every raise on the issue still waiting for an answer, from every run, and a raise leaves it only once it is answered, done or disagree. Each line opens with its kind's icon (question, blocker or issue), shows its label when it has one, and says who it is for: you, the planner, the worker, or filed as an issue. A run that raised nothing shows no Raised section on its comment, and the issue card shows none only when every raise has an answer.",
>    "source": "https://github.com/dokima-dev/dokima/issues/299"
>   },
>   {
>    "text": "No card shows a raise's or an answer's ID.",
>    "source": "https://github.com/dokima-dev/dokima/issues/299"
>   },
>   {
>    "text": "A review card shows what earlier steps raised in its own Raised earlier section, apart from what this review raises. Each earlier raise shows the reviewer's answer: done or disagree, and why. An answer given for you on autopilot quotes your words and links where you said them

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -5; git log --oneline -5 origin/main 2>&1; git branch -a; git show --stat HEAD | head -20; git cat-file -t b6d00ea 2>&1
```

> 4b9471d planner for #299 (run 37999623766)
> c539f55 Text-only changes (AGENTS.md, README, wiki) skip the plan and tests (#362)
> 7a2349e On autopilot, a blocked issue plans only after its blockers merge (reverses #253) (#360)
> 3ae65a6 A scan of the whole board and every card names anything that does not match its state (#361)
> 8b12495 AGENTS.md: every issue reference is a link plus a few plain words (#357)
> b6d00ea Cards show what was raised and how each earlier raise was answered (#327)
> c539f55 Text-only changes (AGENTS.md, README, wiki) skip the plan and tests (#362)
> 7a2349e On autopilot, a blocked issue plans only after its blockers merge (reverses #253) (#360)
> 3ae65a6 A scan of the whole board and every card names anything that does not match its state (#361)
> 8b12495 AGENTS.md: every issue reference is a link plus a few plain words (#357)
>   main
> * try/issue-299
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
>   remotes/o

`4. Bash`
```
cd /tmp/pack; sed -n 1,120p issue.md
```

> # Issue #299: Cards show what was raised and how each earlier raise was answered
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298 -->
> <!-- dokima-blocking: {"blocked_by": [298], "blocks": [300], "loop": []} -->
> Run comments and the issue card show what an agent raised in one Raised section, and a review shows how it answered earlier raises.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/merged.svg" width="16" height="16" align="absmiddle" alt="merged"> **Merged**
> 
> [issue #299](https://github.com/dokima-dev/dokima/issues/299) · [PR #327](https://github.com/dokima-dev/dokima/pull/327) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/327/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #298
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #300
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #300, #301, #302
> 
> **User story:** The owner reads every question, blocker and issue a run raised in one Raised section that says who eac

`5. Bash`
```
cd /tmp/pack; grep -n '^## \|^### \|^\*\*.*commented\|^---' issue.md | head -80
```

> 89:## Comments
> 91:### dokima-runtime on issue #299 (2026-10-09T04:35:51Z)
> 95:### dokima-runtime on issue #299 (2026-10-09T04:36:06Z)
> 155:### dokima-runtime on issue #299 (2026-10-09T05:01:22Z)
> 220:### RezaSoleymanifar on issue #299 (2026-10-09T05:25:47Z)
> 224:### dokima-runtime on issue #299 (2026-10-09T05:26:08Z)
> 284:### dokima-runtime on issue #299 (2026-10-09T05:34:24Z)
> 348:### RezaSoleymanifar on issue #299 (2026-10-09T05:39:53Z)
> 352:### dokima-runtime on issue #299 (2026-10-09T05:40:13Z)
> 411:### dokima-runtime on issue #299 (2026-10-09T05:42:30Z)
> 470:### dokima-runtime on issue #299 (2026-10-09T05:44:26Z)
> 475:### dokima-runtime on issue #299 (2026-10-09T05:44:28Z)
> 502:### dokima-runtime on PR #327 (2026-10-09T05:54:56Z)
> 539:### RezaSoleymanifar on issue #299 (2026-10-09T22:08:10Z)
> 543:### dokima-runtime on issue #299 (2026-10-09T22:08:28Z)
> 600:### RezaSoleymanifar on issue #299 (2026-10-09T22:30:47Z)
> 604:### dokima-runtime on issue #299 (2026-10-09T22:31:06Z)
> 666:### RezaSoleymanifar on PR #327 review (approved) (2026-10-09T22:31:08Z)
> 670:### dokima-runtime on issue #299 (2026-10-09T22:36:30Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`6. Bash`
```
cd /tmp/pack; sed -n 220,224p issue.md; sed -n 348,352p issue.md; sed -n 470,678p issue.md
```

> ### RezaSoleymanifar on issue #299 (2026-10-09T05:25:47Z)
> 
> /plan Show every raise on the issue that is still waiting for an answer, not just the newest run's. Every raise must be answered, so none should drop out of view.
> 
> ### dokima-runtime on issue #299 (2026-10-09T05:26:08Z)
> ### RezaSoleymanifar on issue #299 (2026-10-09T05:39:53Z)
> 
> /plan As answered above: the issue card's Raised section shows every raise on the issue still waiting for an answer, from every run, and a raise leaves it only once it is answered. Drop the question and write this into a criterion and its test, as the reviewer's B2 says.
> 
> ### dokima-runtime on issue #299 (2026-10-09T05:40:13Z)
> ### dokima-runtime on issue #299 (2026-10-09T05:44:26Z)
> 
> Autopilot: plan approved, starting work
> 
> 
> ### dokima-runtime on issue #299 (2026-10-09T05:44:28Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/worker.svg" width="16" height="16" align="absmiddle" alt="worker"> Run comments and the issue card draw raises in one Raised section without IDs; a review card shows its answers to earlier raises. ([pull request #327](https://github.com/dokima-dev/dokima/pull/327))
> 
> <details><summary><b>What it built</b></summary>
> 
> - 299.1: card.raise_line draws icon, label, text and who it is for; agent.raised_lines adds a run's Raised sec

`7. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
for f in ['06-reviewer-plan.json','04-reviewer-plan.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:5000])
"
```

> 06-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37889866273",
>  "commit_before": "f6753f8ed70eaff1db66d2f31164dd166fe3b31c",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 39009,
>   "turns": 9,
>   "cost_usd": 0.4644704,
>   "tokens_in": 341038,
>   "tokens_out": 4035
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/299/37889866273-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37889866273",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner wrote the owner's answer into criterion 1: the issue card shows every raise still waiting for an answer, from every run, and a raise leaves only once it is answered, done or disagree.",
>     "The planner rewrote the issue card test to follow raises across a planner, a quiet run, a worker, a review that answers two, a rejected review and a review that answers the rest."
>    ],
>    "decided": [
>     "A rejected hand-back's raises are not drawn, and its answers take no raise off the issue card."
>    ],
>    "open": [
>     "One question for the owner: whether a rejected run still shows what it raised, planned as no."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The plan now keeps every unanswered raise on the issue card, as the owner asked, and every test fails today because the feature is missing.",
>   "blockers": [],
>   "notes": [
>    {
>     "text": "All 23 tests fail today. The 299.4 and 299.5 goldens match today

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raised_cards.py 2>&1 | tail -30; git diff --stat c539f55 main -- tests/ | tail -3; git diff c539f55..main --stat | tail -5; git diff HEAD main -- tests/test_raised_cards.py tests/raised_goldens | head -20
```

> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
>   
>   - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **Acceptance criterion:** <a href="https://x/check/1">A slow call returns a job id.</a>
>     - <a href="https://github.com/o/r/issues/299">Source</a>
>   
>   <details><summary><b>Non-functional requirements</b></summary>
>   
>   - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **Non-functional requirement:** <a href="https://x/check/2">Nothing leaks.</a>
>   
>   </details>
>   
>   **Scope:**
>   
>   - dokima/agent.py
>   
>   **Out of scope:**
>   
>   - The board.
>   
>   **Definition of Done:** <a href="https://x/check/3"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> All tests · <a href="https://github.com/o/r/actions/runs/7"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_raised_cards.py 2>&1 | grep -E '^FAILED' | sed 's/ - .*\(299\.[0-9]\)/ ... \1/' | cut -c1-200; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1; cd /tmp/mainwt && python3 -m pytest -q tests/test_raised_cards.py 2>&1 | tail -2
```

> FAILED tests/test_raised_cards.py::test_a_run_comment_shows_every_raise_in_one_raised_section[record0-raises0-the planner's comment] - Failed: render() takes no earlier records yet, so a review cannot
> FAILED tests/test_raised_cards.py::test_a_run_comment_shows_every_raise_in_one_raised_section[record1-raises1-the worker's comment] - Failed: render() takes no earlier records yet, so a review cannot 
> FAILED tests/test_raised_cards.py::test_a_run_comment_shows_every_raise_in_one_raised_section[record2-raises2-the review's comment] - Failed: render() takes no earlier records yet, so a review cannot 
> FAILED tests/test_raised_cards.py::test_a_run_that_raised_nothing_shows_no_raised_section ... 299.1: a planner run with raises shows no Raised section
> FAILED tests/test_raised_cards.py::test_the_issue_card_shows_every_raise_still_waiting_for_an_answer ... 299.1: after the planner's run, the issue card must have exactly one Raised section:
> FAILED tests/test_raised_cards.py::test_no_card_shows_a_raise_or_answer_id - Failed: render() takes no earlier records yet, so a review cannot show what it answered
> FAILED tests/test_raised_cards.py::test_a_review_card_shows_earlier_raises_with_its_answers_apart_from_its_own - Failed: render() takes no earlier records yet, so a review cannot show what it answered
> FAILED tests/test_raised_cards.py::test_an_answer_given_for_you_on_autopilot_quotes_your_words_and_links_them - Failed: render() takes no earlier records yet, so a review cannot show what it

`10. Bash`
```
cd /tmp/pack/in; python3 -c "
import json
a=json.load(open('09-planner.json'))['handback'];b=json.load(open('10-planner.json'))['handback']
for i,(x,y) in enumerate(zip(a['acceptance_criteria'],b['acceptance_criteria'])):
  if x!=y: print(i+1,'\n OLD',x['text'],'\n NEW',y['text'])
print(a.get('questions'), b.get('questions')); print(a['tests']==b['tests'])
"; cd /home/runner/work/dokima/dokima; git worktree remove /tmp/mainwt
```

> 2 
>  OLD No card shows a raise's or an answer's ID; only the full record keeps them. 
>  NEW No card shows a raise's or an answer's ID.
> 5 
>  OLD What code detects keeps its own name, icon and place on the card, exactly as today, and never appears in the Raised section. That is work outside the plan, failing tests, red main, merge conflicts, a rejected hand-back, a workflow file change that needs you and three blocks in a row, and also a run stopped before its agent and a cancelled run. 
>  NEW What code detects keeps its own name, icon and place on the card, exactly as today, and never appears in the Raised section. That is work outside the plan, failing tests, red main, merge conflicts, a rejected hand-back, a workflow file change that needs you and three blocks in a row.
> [{'question': 'Should a run whose hand-back code rejected still show what it raised?', 'assumption': 'No: a rejected hand-back is not used, so its comment stays exactly as today, showing why it was rejected, its raises are not drawn, and its answers take no raise off the issue card.'}] None
> True

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner replanned against main as it stood before PR #327 merged, keeping the same five criteria and the same 23 tests.",
   "The planner cut criteria 2 and 5 back to the owner's own words and dropped its question about rejected hand-backs."
  ],
  "decided": [
   "A rejected hand-back still draws exactly as today, as criterion 5 says."
  ],
  "open": [
   "The planner says this work already merged as PR #327 and recommends closing the issue instead of building it again."
  ]
 },
 "verdict": "approve",
 "summary": "The plan keeps every ask of the owner with a test that fails today because the feature is missing, and the same tests pass on main, where PR #327 already built this.",
 "blockers": [],
 "notes": [
  {
   "text": "This work is already on main: PR #327 merged while the planner ran, and its tests are the same files as this plan's. Building it again would change nothing, so closing the issue is the owner's call.",
   "evidence": "git diff HEAD main -- tests/test_raised_cards.py tests/raised_goldens is empty; on main, pytest -q tests/test_raised_cards.py gives 23 passed; git log main shows b6d00ea 'Cards show what was raised and how each earlier raise was answered (#327)'."
  },
  {
   "text": "All 23 tests fail on this branch because the feature is missing, each naming its criterion: no Raised section, no Raised earlier section, or render() taking no earlier records.",
   "evidence": "pytest -q tests/test_raised_cards.py on try/issue-299 (c539f55 plus tests): 23 failed in 0.54s, e.g. '299.1: after the planner's run, the issue card must have exactly one Raised section'."
  },
  {
   "text": "The tests still check that a run stopped before its agent and a cancelled run draw as today, though criterion 5 no longer names them. This keeps those cards unchanged and asks nothing new of the work.",
   "evidence": "tests/test_raised_cards.py::test_what_code_dete
```

> Exit code 1
> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** The check says the summary is too long, so I'm shortening it and running the check again.

`12. Bash`
```
python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; d=json.load(open(p))
d['summary']="Every ask has a test that fails today because the feature is missing; the same tests already pass on main, where PR #327 built this."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 299 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#299](https://github.com/dokima-dev/dokima/issues/299) (cards show what was raised and how each earlier raise was answered). But this work is already on main: [#327](https://github.com/dokima-dev/dokima/pull/327) (the pull request that built this issue) merged while the planner was running.

- **The plan:** it keeps the same five criteria and 23 tests as before. Criteria 2 and 5 now use the owner's own words, and the question about rejected hand-backs is gone. All 11 asks of the owner I found in the issue and its comments map to a criterion, including "Show every raise on the issue that is still waiting for an answer". None is missing, and no earlier blockers were left open.
- **Tests on this branch:** all 23 fail because the feature is missing, and each failure names its criterion. None fails from a crash or a bad path.
- **Tests on main:** the same 23 pass. The test files are identical on both, and the merge is commit `b6d00ea`.

The review notes that building it again would change nothing. The planner recommends closing the issue, and that's your call. Since the issue has been on autopilot, an approval could start a worker on it unless the issue is closed first.

The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.
