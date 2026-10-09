# reviewer (plan) for #308

Run: https://github.com/dokima-dev/dokima/actions/runs/37884549218

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
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

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git diff HEAD~1 -- tests/test_wiki.py; ls docs/wiki
```

> commit 54faa2bb4c73282c310d706e4f453cbc20a7e7ec
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 04:34:42 2026 +0000
> 
>     planner for #308 (run 37884160496)
> 
>  tests/test_wiki.py | 286 +++++++++++++++++++++++++++++++++++++++++++++++++----
>  1 file changed, 269 insertions(+), 17 deletions(-)
> diff --git a/tests/test_wiki.py b/tests/test_wiki.py
> index 7bfb8c9..3672b42 100644
> --- a/tests/test_wiki.py
> +++ b/tests/test_wiki.py
> @@ -1,29 +1,281 @@
> +"""Tests for the wiki pages under docs/wiki/, which wiki.yml mirrors to the GitHub wiki.
> +
> +The reference pages of #308 (Commands and labels, The card, Configuration) are checked against the code itself:
> +the commands come from dokima/agent.py COMMANDS, the labels, board fields, views, branch rule and app permissions from
> +dokima/manifest.py, the card's stages and circle states from dokima/card.py, and the secrets and variables from what
> +the workflows read. When the code gains or renames one of these, the page must follow or these tests go red.
> +
> +On the Commands and labels page each command and label has its own entry: one table row or bullet whose first
> +backticked word is its name, for example "| `/plan` | ..." or "- `parked`: ...".
> +"""
> +import re
>  from pathlib import Path
>  
> -WIKI = Path(__file__).parent.parent / "docs" / "wiki"
> +from dokima import agent, card, manifest
> +
> +ROOT = Path(__file__).parent.parent
> +WIKI = ROOT / "docs" / "wiki"
> +COMMANDS_PAGE = "Commands-and-labels.md"
> +CA

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
from dokima import agent, card, manifest
print(agent.COMMANDS); print(card.STAGES); print(card.ICON_FILE); print(getattr(card,'FIELD_ICONS',None)); print(manifest.LABELS); print(manifest.PERMISSIONS); print(manifest.FIELDS); print(manifest.VIEWS); print(manifest.BRANCH_RULES)"; grep -n "TODO\|Definition of Done\|Needs you\|Verified by" dokima/card.py | head -30; cat docs/wiki/The-card.md | head -60
```

> {'/plan': 'planner', '/work': 'worker', '/review': 'reviewer'}
> {'Merged', 'Plan', 'Review', 'Work', 'Backlog'}
> {'passed': 'passed', 'failed': 'failed', 'running': 'running', 'not started': 'none'}
> {'planner': 'planner', 'worker': 'worker', 'plan review': 'plan-review', 'code review': 'code-review', 'autopilot': 'autopilot', 'passed': 'passed', 'failed': 'failed', 'needs you': 'needs-you', 'owner approval': 'owner-approval', 'merged': 'merged', 'still open': 'still-open', 'acceptance criterion': 'acceptance-criterion', 'verified by': 'verified-by', 'files changed': 'files-changed', 'question': 'question', 'blocker': 'blocker', 'note': 'note', 'outside the plan': 'outside-the-plan', 'issue found': 'issue-found', 'related': 'related', 'blocked by': 'blocked-by', 'blocks': 'blocks', 'stats': 'stats'}
> {'plan': {'color': '1d76db', 'description': 'Starts the planner'}, 'work': {'color': '0e8a16', 'description': 'Starts the worker on the approved plan'}, 'autopilot': {'color': '8250df', 'description': 'Running on its own'}, 'blocker': {'color': 'b60205', 'description': 'Priority: blocks other work'}, 'high': {'color': 'd93f0b', 'description': 'Priority: high'}, 'parked': {'color': 'c5c5c5', 'description': 'Priority: parked for later'}}
> {'contents': 'write', 'pull_requests': 'write', 'issues': 'write', 'checks': 'read', 'actions': 'write', 'statuses': 'read', 'metadata': 'read', 'workflows': 'write', 'administration': 'read', 'organization_projects': 'write'}
> {'Status': {'Backlog': {'

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_wiki.py 2>&1 | grep -E "Error|passed|failed" | head -30; grep -ho "secrets\.[A-Z_0-9]*\|vars\.[A-Z_0-9]*" .github/workflows/*.yml | sort -u; grep -n "label" .github/workflows/planner.yml .github/workflows/worker.yml | head; grep -rn "autopilot start\|autopilot stop" dokima/*.py | head -5
```

> E       AssertionError: 308.1: docs/wiki/Commands-and-labels.md does not exist yet
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.2: the card page does not name the stages ['Backlog', 'Merged', 'Review', 'Work']
> tests/test_wiki.py:130: AssertionError
> E       AssertionError: 308.3: docs/wiki/Configuration.md does not exist yet
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.4: docs/wiki/Commands-and-labels.md does not exist yet
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.5: docs/wiki/Commands-and-labels.md does not exist yet
> tests/test_wiki.py:28: AssertionError
> E       AssertionError: 308.6: docs/wiki/Commands-and-labels.md does not exist yet
> tests/test_wiki.py:28: AssertionError
> FAILED tests/test_wiki.py::test_commands_and_labels - AssertionError: 308.1: docs/wiki/Commands-and-labels.md does not exist yet
> FAILED tests/test_wiki.py::test_the_card - AssertionError: 308.2: the card page does not name the stages ['Backlog', 'Merged', 'Review', 'Work']
> FAILED tests/test_wiki.py::test_configuration - AssertionError: 308.3: docs/wiki/Configuration.md does not exist yet
> FAILED tests/test_wiki.py::test_wiki_tests_catch_a_missing_command_or_label - AssertionError: 308.4: docs/wiki/Commands-and-labels.md does not exist yet
> FAILED tests/test_wiki.py::test_reference_pages_follow_the_style - AssertionError: 308.5: docs/wiki/Commands-and-labels.md does not exist yet
> FAILED tests/test_wiki.py::test_reference_pages_mark_what_is_plann

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,12p .github/workflows/worker.yml; grep -n "code owner" .github/workflows/worker.yml | head -3; grep -rln "autopilot" .github/workflows/ ; grep -n "labeled\|code owner" .github/workflows/autopilot.yml .github/workflows/board.yml | head
```

> name: worker
> run-name: "worker for #${{ github.event.issue.number }}${{ github.event.label.name != 'work' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> # Adding the `work` label to an issue approves its plan and starts the worker: a
> # fresh GitHub machine builds what the plan asks and opens (or updates) the PR.
> # Only a code owner's label counts. Removing the label stops a running build;
> # adding it again builds again from the plan as it stands then.
> on:
>   issues:
>     types: [labeled, unlabeled]
> # Labeling or unlabeling `work` cancels the build already running for that issue.
> # Other labels use their own group, so they never interrupt a build.
> concurrency:
> 5:# Only a code owner's label counts. Removing the label stops a running build;
> 31:      - name: Only a code owner's label counts
> 39:            echo "::notice title=Not started::$SENDER added work, but only a code owner's label starts the worker."
> .github/workflows/commands.yml
> .github/workflows/autopilot.yml
> .github/workflows/agent.yml
> .github/workflows/board.yml:8:    types: [labeled, unlabeled, closed]

**Agent:** Reviewing the plan for #308. I've found two gaps where the tests are weaker than what the owner asked for, and I'm writing up the review now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def check_review\|asks\|criterion" dokima/agent.py | grep -i "ask" | head -20
```

> 415:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 437:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 440:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 688:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 725:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 729:def problems_asks(r, ids):
> 730:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 731:    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
> 732:    asks = r.get("asks")
> 733:    if not isinstance(asks, list) or not asks:
> 734:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 736:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 737:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 741:            bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
> 743:    gone = [a["ask"] for a in good if a["criterion"].strip() == "missing"]
> 818:        bad.append("the 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def plan_criteria" -A12 dokima/agent.py
```

> 888:def plan_criteria(plan, number):
> 889-    """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
> 890-    count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
> 891-    if plan.get("kind") == "feature":
> 892-        stories = plan.get("stories") if isinstance(plan.get("stories"), list) else []
> 893-        return [f"S{s}.{k}" for s, st in enumerate(stories, 1) if isinstance(st, dict) for k in range(1, count(st) + 1)]
> 894-    return [f"{number}.{k}" for k in range(1, count(plan) + 1)]
> 895-
> 896-
> 897-def problems_plan(kind, h, plan, number):
> 898-    """Everything in a hand-back that does not match the approved plan: a work line per criterion, exactly, and every
> 899-    blocker on one of the plan's criteria, naming either no test or one of the plan's tests for that criterion."""
> 900-    ids = plan_criteria(plan, number)

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote four criteria for three wiki pages (Commands and labels, The card, Configuration) and the wiki tests that check them, plus two style and planned-marking rules with their own tests.",
   "The planner rewrote the card page's test, deleted the Home page's test and dropped the work-label line from the Writing issues test."
  ],
  "decided": [
   "The tests read commands, labels, stages, circle states, board fields, permissions and required checks from the code, so the pages must follow the code."
  ],
  "open": [
   "The card criterion lists a fixed set of fields and leaves out most of the card's named fields; the label entries are not checked for who may use them."
  ]
 },
 "verdict": "block",
 "summary": "The plan narrows two of the owner's asks: the card page only has to explain a short list of fields, not every field, and the tests never check who may use each label.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "308.2",
   "test": "tests/test_wiki.py::test_the_card",
   "problem": "The owner asked the card page to describe every field the card and run records show today, and pointed to dokima/card.py FIELD_ICONS as where the fields live. The plan's criterion 2 replaces \"every field ... includes\" with a closed list (\"That is the stage, ... cost\"), and the test checks only that list. Most of the card's named fields are never checked: questions, blockers, notes, outside the plan, issues found, files changed, related, blocked by, blocks, still open, merged, plan review, code review, acceptance criterion. A page that leaves all of them out passes.",
   "evidence": "python3 -c 'from dokima import card; print(list(card.FIELD_ICONS))' lists 23 fields; test_the_card (tests/test_wiki.py, around lines 120-140) only checks card.STAGES, card.ICON_FILE and ten fixed words. The issue's Context says \"The card fields live in dokima/card.py (FIELD_ICO
```

> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "work\` label" docs/wiki/*.md; python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="The plan narrows two asks: the card page need not explain every card field, and no test checks who may use each label."
r['issues_found'][0]['evidence']="docs/wiki/Home.md and docs/wiki/Writing-issues.md still mention the `work` label as the way to approve; this plan deletes test_home and the Writing issues assertion that pinned it."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 308 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> docs/wiki/Writing-issues.md:54:When the planner has posted its plan, read it. Adding the `work` label approves the plan and starts the worker.
> docs/wiki/The-card.md:36:The Approve button means "approve the result to merge". It is for the finished work, not the plan; you approve the plan by adding the `work` label to the issue.
> docs/wiki/Home.md:40:2. **The planner** turns it into a plan and the tests that will prove it, then waits for your go. You approve the plan by adding the `work` label to the issue. *Planned.*
> rc=0

**Agent:** I've blocked the plan for #308 and sent it back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

The plan covers all seven of the owner's asks, and each new test fails today for the right reason: the pages don't exist yet or still have the old wording. It still narrows two asks, so I blocked it:

- **B1, the card page (308.2):** The owner asked the card page to describe every field the card and run records show, and pointed to `FIELD_ICONS` in `dokima/card.py`. The plan replaces "every field" with a fixed short list. Most of the card's 23 named fields are never checked, such as questions, blockers, notes, issues found, files changed, related, blocked by and blocks. A page that leaves them all out would pass. The fix is for `test_the_card` to check every field in `FIELD_ICONS`.
- **B2, who may use each label (308.1):** The owner asked that each command and label say who may use it. The test only looks for "triage" or "write access" anywhere on the page. In the code, only a code owner's `plan` or `work` label starts anything (`planner.yml:30`, `worker.yml:31`). So a page saying anyone with triage access can start the planner would pass while being wrong. The fix is for the `plan` and `work` entries to say only a code owner's label counts, and for the test to check each label's entry.

I added two notes that don't block:
- `test_the_card` fails on any mention of the work label, even a correct one.
- The test for marking unbuilt behaviour as planned only looks for three things, so whoever reviews the pull request should still read the pages against the code.

I also proposed one new issue. Once this plan removes the old tests, nothing checks `Home.md` and `Writing-issues.md`, and both still say adding the `work` label approves the plan. They stay wrong until stories 2 and 3 land.
