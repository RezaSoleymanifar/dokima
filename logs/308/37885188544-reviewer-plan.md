# reviewer (plan) for #308

Run: https://github.com/dokima-dev/dokima/actions/runs/37885188544

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (53KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/94f069d8-4743-429c-9959-6018fd2faa4b/tool-results/bxak4vywn.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:43 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:43 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:43 in
> -rw-r--r--  1 runner runner 44998 Oct  9 04:43 issue.md
> -rw-r--r--  1 runner runner  2537 Oct  9 04:43 open_blockers.json
> -rw-r--r--  1 runner runner  6053 Oct  9 04:43 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  9 04:43 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 04:43 ..
> -rw-r--r-- 1 runner runner 5256 Oct  9 04:43 01-planner.json
> -rw-r--r-- 1 runner runner 7886 Oct  9 04:43 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6699 Oct  9 04:43 03-planner.json
> # Issue #308: The wiki's reference pages describe every command, label, card field and setting as the code has them today
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #305, story 1</summary>
> 
> **Part of:** #305 Rewrite the README and wiki to match the current code
> 
> **User story:** Owners look up any command, label, card field or setting in three reference pages and find it described exactly as Dokima does it today.
> 
> ...
> </persisted-output>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`2. Bash`
```
cd /tmp/pack; head -c 20000 issue.md
```

> # Issue #308: The wiki's reference pages describe every command, label, card field and setting as the code has them today
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #305, story 1</summary>
> 
> **Part of:** #305 Rewrite the README and wiki to match the current code
> 
> **User story:** Owners look up any command, label, card field or setting in three reference pages and find it described exactly as Dokima does it today.
> 
> **Context:** Docs are written only in docs/wiki/ (wiki.yml mirrors it to the GitHub wiki on every push to main) and README.md. Facts found in the code at planning time: commands are /plan, /work, /review, /autopilot start and /autopilot stop, read by .github/workflows/commands.yml from a code owner's comment or PR review summary (CODEOWNERS); /issue is planned. Labels are declared in dokima/manifest.py LABELS: plan, work, autopilot, blocker, high, parked. The plan and work labels still start the older .github/workflows/planner.yml and worker.yml, so they exist and must be described as they work, while the docs present /plan and /work as the way to approve. Merges are not automatic except on autopilot (AGENTS.md step 6). Required checks on main are "all tests" and "all done-whens passed" (manifest.py CHECKS; #291 may rename them later). Workflows read secrets CLAUDE_CODE_OAUTH_TOKEN and DOKIMA_APP_KEY and variables DOKIMA_APP_ID and DOKIMA_BOARD (board.yml does nothing without it). There is no one-command onboarding y

`3. Bash`
```
cd /tmp/pack; tail -c +20000 issue.md | grep -v "^\s*$" | head -400 | cut -c1-600
```

> (/issue, co-author credit, one-command setup) and merges outside autopilot. Other unbuilt behaviour would get through, so the reviewer of the pull request should read the pages against the code too. (tests/test_wiki.py PLANNED = (r"`/issue`", r"co-author", r"one[- ]command"))
> </details>
> <details><summary><b>The owner's asks</b></summary>
> - A Commands and labels page describes every command and label the code has today. Commands are /plan, /work, /review, /autopilot start and /autopilot stop, with /issue marked planned; labels are plan, work, autopilot, blocker, high and parked; each says what it does today and who may use it. (308.1, https://github.com/dokima-dev/dokima/issues/308)
> - The card page describes every field the card and the run records show today. That includes the stage, the Next line, the Needs you and Autopilot pills, each criterion's circle and Verified by line, and the Definition of Done line, and no longer says the work label approves a plan. (308.2, https://github.com/dokima-dev/dokima/issues/308)
> - A Configuration page lists every setting Dokima needs, as the code has it. That is every secret and variable the workflows read, the CODEOWNERS file, the branch rule on main with its required checks, the app's permissions and the optional project board, each as the code and dokima/manifest.py have it. (308.3, https://github.com/dokima-dev/dokima/issues/308)
> - tests/test_wiki.py checks the current wording of these three pages. It fails when a command or label the

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json'))['acceptance_criteria'],indent=1))"; git show --stat HEAD HEAD~1 | head -40; git diff HEAD~1 HEAD | head -200
```

> [
>  {
>   "text": "A Commands and labels page gives every command and label its own entry saying what it does today. The commands are /plan, /work, /review, /autopilot start and /autopilot stop, with /issue marked planned. The labels are plan, work, autopilot, blocker, high and parked. The page says only a code owner's commands count. Each label's entry says who may add it: the plan and work entries say only a code owner's label counts, and the autopilot, blocker, high and parked entries say anyone with triage or write access adds them. The work label's entry no longer says it approves a plan, and nothing the code lacks is listed.",
>   "source": "https://github.com/dokima-dev/dokima/issues/308"
>  },
>  {
>   "text": "The card page explains every field the card and its run records show today. That includes every named field in dokima/card.py FIELD_ICONS (planner, worker, plan review, code review, autopilot, passed, failed, needs you, owner approval, merged, still open, acceptance criterion, verified by, files changed, question, blocker, note, outside the plan, issue found, related, blocked by, blocks), the stage (Backlog, Plan, Work, Review, Merged), the Next line, the Needs you and Autopilot pills, each criterion's circle (passed, failed, running, not started) and Verified by line, the Definition of Done row (All tests, Code review, Owner approval) and each record's footnote with its model, turns, tokens and cost; the stats icon only marks that footnote. It says /work approves a plan;

`5. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -n "code owner\|labeled\|sender\|autopilot" .github/workflows/*.yml | head -60; python3 -c "from dokima import card; print(list(card.FIELD_ICONS)); print(card.STAGES); print(card.ICON_FILE)"
```

> agent.yml
> assign.yml
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
> .github/workflows/assign.yml:2:# Assigns every new issue to the repo's code owners, so it shows up in their
> .github/workflows/assign.yml:15:      - name: Assign the code owners
> .github/workflows/board.yml:8:    types: [labeled, unlabeled, closed]
> .github/workflows/agent.yml:3:# Runs one agent on a fresh GitHub machine. Started by hand here, or by commands.yml when a code owner's comment
> .github/workflows/agent.yml:10:# agent's, the bot sends a dokima-next signal that starts it here. On autopilot an approved plan starts the worker and
> .github/workflows/agent.yml:72:      - name: Only a code owner starts an agent
> .github/workflows/agent.yml:77:          # The river's own signal comes from Dokima's bot; everything else needs a code owner.
> .github/workflows/agent.yml:80:            || { echo "$SENDER is not a code owner, so they cannot start an agent." > /tmp/why.txt
> .github/workflows/agent.yml:363:      # On autopilot, a code review's approval with every check green merges the pull request here, so this step
> .github/workflows/agent.yml:365:      - name: Decide what follows, merge on autopilot, and say it on the card
> .github/workflows/agent.yml:411:          # On autopilot, one line on the issue where the owner would have typed `/work`.
> .github/workflows/agent.yml:412:          if [ -s "$OUT/autopilot.md" ]; then gh issue comment "$N" -R "$

**Agent:** Both earlier blockers look fixed in the planner's newest commit. Next I'm running the new tests to confirm each one fails today for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_wiki.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed|AssertionError|^E " | head -40
```

> E       AssertionError: 308.1: docs/wiki/Commands-and-labels.md does not exist yet
> E       assert False
> E        +  where False = exists()
> E        +    where exists = PosixPath('/home/runner/work/dokima/dokima/docs/wiki/Commands-and-labels.md').exists
> tests/test_wiki.py:28: AssertionError
> E           AssertionError: 308.2: the card page does not explain planner
> E           assert None
> E            +  where None = <function search at 0x7f97955ef060>('\\bplanners?\\b', "# The card\n\nDokima's job is to move your attention from the work to the verification. The card is how it does that:...eans the listed checks passed, nothing more. Making the gaps visible is what lets you decide where to look yourself.\n", re.IGNORECASE)
> E            +    where <function search at 0x7f97955ef060> = re.search
> E            +    and   re.IGNORECASE = re.I
> tests/test_wiki.py:142: AssertionError
> E       AssertionError: 308.3: docs/wiki/Configuration.md does not exist yet
> E       assert False
> E        +  where False = exists()
> E        +    where exists = PosixPath('/home/runner/work/dokima/dokima/docs/wiki/Configuration.md').exists
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.4: docs/wiki/Commands-and-labels.md does not exist yet
> E       assert False
> E        +  where False = exists()
> E        +    where exists = PosixPath('/home/runner/work/dokima/dokima/docs/wiki/Commands-and-labels.md').exists
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.5: docs/wiki/Com

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,110p tests/test_wiki.py; sed -n 150,330p tests/test_wiki.py
```

> """Tests for the wiki pages under docs/wiki/, which wiki.yml mirrors to the GitHub wiki.
> 
> The reference pages of #308 (Commands and labels, The card, Configuration) are checked against the code itself:
> the commands come from dokima/agent.py COMMANDS, the labels, board fields, views, branch rule and app permissions from
> dokima/manifest.py, the card's stages and circle states from dokima/card.py, and the secrets and variables from what
> the workflows read. When the code gains or renames one of these, the page must follow or these tests go red.
> 
> On the Commands and labels page each command and label has its own entry: one table row or bullet whose first
> backticked word is its name, for example "| `/plan` | ..." or "- `parked`: ...".
> """
> import re
> from pathlib import Path
> 
> from dokima import agent, card, manifest
> 
> ROOT = Path(__file__).parent.parent
> WIKI = ROOT / "docs" / "wiki"
> COMMANDS_PAGE = "Commands-and-labels.md"
> CARD_PAGE = "The-card.md"
> CONFIG_PAGE = "Configuration.md"
> REFERENCE = (COMMANDS_PAGE, CARD_PAGE, CONFIG_PAGE)
> STALE_PIN = "`work`" + " label"
> 
> 
> def read(name, criterion="308"):
>     """The text of one wiki page; a missing page fails naming its criterion."""
>     path = WIKI / name
>     assert path.exists(), f"{criterion}: docs/wiki/{name} does not exist yet"
>     return path.read_text()
> 
> 
> def commands():
>     """Every command the code reads today, with /issue (planned) last."""
>     return list(agent.COMMANDS) + ["/autopilot start", "/autopilot stop", "/issue"]
> 
> 
> def ent

`8. Bash`
```
cd /tmp/pack; python3 -c "import json;p=json.load(open('plan.json'));print(p.keys());print(p.get('questions'))"; cat open_blockers.json | head -5
```

> dict_keys(['kind', 'summary', 'user_story', 'acceptance_criteria', 'non_functional', 'scope', 'out_of_scope', 'tests', 'test_changes', 'links', 'replies'])
> None
> [
>  {
>   "id": "B1",
>   "criterion": "308.2",
>   "test": "tests/test_wiki.py::test_the_card",
> Shell cwd was reset to /home/runner/work/dokima/dokima

`9. Bash`
```
mkdir -p /tmp/dokima-out; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/02-reviewer-plan.json'))
asks=(prev.get('handback') or prev)['asks']
r={"previous_step":{"did":["The planner made the card page's test check every named card field from dokima/card.py, failing with the field it misses.",
 "The planner made each label's entry say who may add it: a code owner for plan and work, triage or write access for autopilot, blocker, high and parked."],
 "decided":["The stats icon is the only card field left out of the check, because it only marks the record's footnote, which is checked as model, turns, tokens and cost."],
 "open":[]},
 "verdict":"approve",
 "summary":"The plan now covers every card field and says who may add each label, and every new test fails today because the pages are missing or out of date.",
 "blockers":[],
 "notes":[
  {"text":"The test for unbuilt behaviour only catches /issue, co-author credit, one-command setup and merges outside autopilot. The pull request's reviewer should still read the pages against the code for anything else unbuilt.",
   "evidence":"tests/test_wiki.py PLANNED = (r\"`/issue`\", r\"co-author\", r\"one[- ]command\")"},
  {"text":"The card page's test fails on any mention of the work label, even a correct one. That is stricter than the criterion, but fine as long as the card page never needs to mention labels.",
   "evidence":"tests/test_wiki.py test_the_card: assert not re.search(r\"`?work`? label\", text)"}],
 "outside_plan":[],
 "resolved":["B1","B2"],
 "issues_found":[{"title":"Home and Writing issues pages still say the work label approves a plan",
   "why":"This story drops the tests that pinned that wording, so nothing checks those pages, and they still tell owners to approve with the work label until stories 2 and 3 land.",
   "evidence":"docs/wiki/Home.md and docs/wiki/Writing-issues.md mention the `work` label as the way to approve; the plan deletes test_home and the Writing issues line that pinned i
```

> summary holds 29 words, over its cap of 25 (up to 30 passes)
> rc=0

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="The plan now covers every card field and who may add each label; every new test fails today because the pages are missing or stale."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 308 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #308. Both blockers from the last round are fixed, and the hand-back is in `/tmp/dokima-out/review.json`. Both checks on it pass.

- **B1 (card fields): fixed.** The card page's test now checks every named field in `dokima/card.py` `FIELD_ICONS` (`tests/test_wiki.py:138-142`). It fails naming the field the page misses. Only `stats` is skipped, because that icon just marks the record's footnote, and the test checks the footnote's model, turns, tokens and cost instead.
- **B2 (who may add a label): fixed.** The plan and work label entries must now say only a code owner's label counts. That matches the "Only a code owner's label counts" steps in `.github/workflows/planner.yml` and `.github/workflows/worker.yml`. The autopilot, blocker, high and parked entries must each say triage or write access.
- **Tests today:** 6 of the 7 tests in `tests/test_wiki.py` fail, each for the right reason. Five fail because a page doesn't exist yet. The card test fails because the old card page doesn't mention the planner. The one passing test is `test_writing_issues`, which isn't part of this plan.
- **Owner's asks:** all seven are matched to a criterion; none are missing. The plan has no questions for the owner.

I left two notes, and one problem outside this issue:
- **Note:** the test for unbuilt behaviour only catches `/issue`, co-author credit, one-command setup and merges outside autopilot. Whoever reviews the pull request should still read the pages against the code for anything else unbuilt.
- **Note:** the card page's test fails on any mention of the work label, even a correct one. That's stricter than the criterion asks.
- **Outside this issue:** the Home and Writing issues pages still say the work label approves a plan. This plan removes the tests that pinned that wording, so nothing checks those pages until stories 2 and 3 land. I proposed it as its own issue.
