# reviewer (plan) for #305

Run: https://github.com/dokima-dev/dokima/actions/runs/37883035387

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (42.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/a85f5978-2a4a-4146-b612-c56d261d310c/tool-results/bqp8ha3q8.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:15 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:16 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:15 in
> -rw-r--r--  1 runner runner 26198 Oct  9 04:15 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 04:15 open_blockers.json
> -rw-r--r--  1 runner runner 17249 Oct  9 04:15 plan.json
> 
> in:
> total 28
> drwxr-xr-x 2 runner runner  4096 Oct  9 04:15 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 04:15 ..
> -rw-r--r-- 1 runner runner 17994 Oct  9 04:15 01-planner.json
> # Issue #305: Rewrite the README and wiki to match the current code
> 
> <!-- dokima-card -->
> **Backlog**
> 
> [issue #305](https://github.com/dokima-dev/dokima/issues/305)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/do

`2. Bash`
```
cd /tmp/pack; sed -n 20,400p issue.md
```

> The README pitches four times before it says what Dokima is, has no quickstart, and its roadmap shows every box unticked even though the planner, reviewer, cards, autopilot and merge gate all exist. Parts of the docs are now wrong: they say adding the `work` label approves a plan (it is `/work`), the sidebar links to the old `RezaSoleymanifar/dokima` repo, the README says merges happen on their own and labels say whose turn it is. `tests/test_wiki.py` pins the stale "`work` label" wording. The last docs change was around #108.
> 
> `docs/wiki/` stays the only place docs are written; `wiki.yml` already mirrors it to the GitHub wiki.
> 
> ## What I want
> 
> README:
> - First sentence says plainly what Dokima is. Tagline: "Agents write the code. Dokima proves it's done."
> - One diagram of the flow: issue, planner, owner approves, worker, reviewer, gate, main.
> - A short quickstart, and an honest shipped vs planned table.
> - Badges for CI and license. Drop the stacked pitch sections and the hype.
> 
> Wiki, in this order, with nothing repeated between pages:
> - Get started (a blank repo to a first merged PR)
> - How-to: Write an issue, Approve / push back / re-plan, Run on autopilot
> - Reference: Commands and labels, The card, Configuration
> - Explanation: How Dokima works
> - FAQ, trimmed to what the other pages don't answer
> - Home becomes a short landing page that links into these, not a copy of the README.
> 
> Writing style: plain, terse, second person, present tense. No hype words ("powerful", "seamless",

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git status; diff <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json')),indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/in/01-planner.json'))['handback'],indent=1,sort_keys=True))") | head; grep -n "non_functional\|S<s>\|assumption\|asks" dokima/agent.py | head -60
```

> d99847b Queued PRs are retested on the latest main before merging (#270)
> 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
> On branch try/issue-305
> Your branch is up to date with 'origin/main'.
> 
> nothing to commit, working tree clean
> 227:    if story.get("non_functional"):
> 228:        lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', '')})" for n in story["non_functional"]]
> 395:        parts += [("Non-functional requirements", bullets(h.get("non_functional"), lambda n: f"{n.get('text', '')} "
> 415:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 437:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 440:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 460:    worker's pull request, once it exists; `plan` is the plan a plan review judged, whose assumptions answer its
> 509:        judged = [a for a in h.get("assumptions") or [] if isinstance(a, dict)]
> 510:        answers = {q.get("question"): q.get("assumption") for q in (plan or {}).get("questions") or []
> 511:                   if isinstance(q, dict) and q.get("assumption")}
> 521:            lines += ["", "**

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 885,905p dokima/agent.py; ls docs/wiki; cat LICENSE* 2>/dev/null | head -3; ls; grep -n "work. label\|def test" tests/test_wiki.py | head -30; grep -rn "license" -i README.md pyproject.toml 2>/dev/null | head
```

> return bad
> 
> 
> def plan_criteria(plan, number):
>     """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
>     count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
>     if plan.get("kind") == "feature":
>         stories = plan.get("stories") if isinstance(plan.get("stories"), list) else []
>         return [f"S{s}.{k}" for s, st in enumerate(stories, 1) if isinstance(st, dict) for k in range(1, count(st) + 1)]
>     return [f"{number}.{k}" for k in range(1, count(plan) + 1)]
> 
> 
> def problems_plan(kind, h, plan, number):
>     """Everything in a hand-back that does not match the approved plan: a work line per criterion, exactly, and every
>     blocker on one of the plan's criteria, naming either no test or one of the plan's tests for that criterion."""
>     ids = plan_criteria(plan, number)
>     bad = []
>     if kind == "work":
>         crit = h.get("criteria")
>         if isinstance(crit, dict):
>             bad += [f"criteria has no line for {c}, a criterion of the plan" for c in ids if c not in crit]
> FAQ.md
> Home.md
> The-card.md
> Writing-issues.md
> _Sidebar.md
> AGENTS.md
> CLAUDE.md
> README.md
> docs
> dokima
> tests
> 10:def test_writing_issues(record_property):
> 15:    assert "`work` label" in text
> 19:def test_the_card(record_property):
> 27:def test_home(record_property):
> 29:    assert "`work` label" in read("Home.md")

`5. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; sed -n 1,30p .github/workflows/worker.yml | grep -n "label\|on:" ; grep -n "LABELS\|CHECKS" -A8 dokima/manifest.py | head -40; sed -n 1,35p tests/test_wiki.py
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
> 2:run-name: "worker for #${{ github.event.issue.number }}${{ github.event.label.name != 'work' && format(' (label {0}, ignored)', github.event.label.name) || '' }}"
> 3:# Adding the `work` label to an issue approves its plan and starts the worker: a
> 5:# Only a code owner's label counts. Removing the label stops a running build;
> 7:on:
> 9:    types: [labeled, unlabeled]
> 10:# Labeling or unlabeling `work` cancels the build already running for that issue.
> 11:# Other labels use their own group, so they never interrupt a build.
> 13:  group: work-${{ github.event.issue.number }}-${{ github.event.label.name }}
> 21:    if: github.event.action == 'labeled' && github.event.label.name == 'work'
> 22:    runs-on: ubuntu-24.04
> 30:          python-version: "3.12"
> 18:LABELS = {
> 19-    "plan": {"color": "1d76db", "description": "Starts the planner"},
> 20-    "work": {"color": "0e8a16", "description": "Starts the worker on the approved plan"},
> 21-    "autopilot": {"color": "8250df", "description": "Running on its own"},
> 22-    "blocker": {"color": "b60205", "description": "Priority: blocks other work"},
> 23-    "high": {"color": "d93f0b", "description": "Priority: high"},
> 24-    "parked": {"color": "c5c5c5", "description": "Priority: parked for later"},
> 25-}
> 26-
> --
> 51:CHECKS = ["all tests", "all done-whens passed"]
> 52-
> 53-BRANCH_RULES = {
> 54-    "main": {"require

**Agent:** Writing the review now: the split is sound and every ask maps to a story, but the MIT license assumption can't be accepted without the owner.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner split the issue into 4 stories: the reference pages; Get started and the how-tos; Home, How Dokima works, FAQ and the sidebar; the README."],
  "decided": ["The plan and work labels are described as they still work, while /plan and /work are shown as the way to approve.", "The README uses this issue's tagline, not the one #137 asked for."],
  "open": ["Which license Dokima carries: the planner assumed MIT, since the repo has no LICENSE file for the badge to read."]},
 "verdict": "approve",
 "summary": "The split covers every ask of the issue across four stories, but its MIT license assumption is the owner's call, so the license question waits for you.",
 "blockers": [],
 "notes": [
  {"text": "Story 3 rewrites Home but has no criterion for tests/test_wiki.py to stop pinning the stale wording on Home; its planner should add one when it plans the story.", "evidence": "tests/test_wiki.py:27-29 test_home asserts \"`work` label\" in Home.md; S1.4 and S2.5 cover only their own pages."},
  {"text": "The work label still approves a plan in code, so the docs must say it does without making it the main way; the stories' plans should keep that line exact.", "evidence": ".github/workflows/worker.yml:3 and :21; dokima/manifest.py LABELS"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "First sentence says plainly what Dokima is. Tagline: \"Agents write the code. Dokima proves it's done.\"", "source": "https://github.com/dokima-dev/dokima/issues/305", "criterion": "S4.1"},
  {"ask": "One diagram of the flow: issue, planner, owner approves, worker, reviewer, gate, main.", "source": "https://github.com/dokima-dev/dokima/issues/305", "criterion": "S4.2"},
  {"ask": "A short quickstart", "source": "https://github.com/dokima-dev/dokima/issues/305", "criterion": "S4.3"},
  {"ask": "an honest shipped vs planned table", "source": "https://github.com/dokima-dev/do
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> 0

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r["summary"]="The split covers every ask across four stories; the MIT license assumption is the owner's call, so that question waits for you."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 305 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I approved the planner's split of #305, but its license question stays open: the planner assumed MIT, and I didn't accept that, so on autopilot the issue stops there and waits for you.

**The split.** The planner split the issue into four stories:
1. The reference pages: Commands and labels, The card, and Configuration.
2. Get started and the three how-to pages. This waits on story 1.
3. Home, How Dokima works, the FAQ and the sidebar. This waits on stories 1 and 2.
4. The README. This waits on story 2.

Every ask in the issue is covered by one of the stories. That includes the tagline, the diagram, the quickstart, the shipped vs planned table and the badges. It also includes the page order, no repeats between pages, the style rules, marking unbuilt behaviour as planned, and changing `tests/test_wiki.py` to check the current wording. The split follows the rules: four stories, one level deep, no circular waits. The plan has no tests yet; each story's own plan will add them.

**License question (needs your answer).** The repo has no LICENSE file, so a license badge has nothing to show. I didn't accept the MIT assumption because a license sets the legal terms for everyone who uses Dokima. You asked only for a badge and never named a license. Reply with `/plan` and the license you want.

**Notes for the stories' plans:**
- Story 3 rewrites Home, but nothing in it requires `test_home` to stop checking for the old "`work` label" wording (`tests/test_wiki.py:27-29`). Its planner should add that when the story is planned.
- Adding the `work` label still approves a plan in code (`.github/workflows/worker.yml:21`). The docs should say so accurately while presenting `/work` as the way to approve.

The review is saved at `/tmp/dokima-out/review.json` and passes both checks.
