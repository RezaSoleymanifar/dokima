# reviewer (plan) for #262

Run: https://github.com/dokima-dev/dokima/actions/runs/37861799429

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (57.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d65c5848-3a5b-4633-ae63-17dc67e215ce/tool-results/bdexgdrog.txt
> 
> Preview (first 2KB):
> .:
> total 76
> drwxr-xr-x  3 runner runner  4096 Oct  8 23:52 .
> drwxrwxrwt 18 root   root    4096 Oct  8 23:52 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 23:52 in
> -rw-r--r--  1 runner runner 45820 Oct  8 23:52 issue.md
> -rw-r--r--  1 runner runner  1088 Oct  8 23:52 open_blockers.json
> -rw-r--r--  1 runner runner 11630 Oct  8 23:52 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner  4096 Oct  8 23:52 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 23:52 ..
> -rw-r--r-- 1 runner runner 10430 Oct  8 23:52 01-planner.json
> -rw-r--r-- 1 runner runner  6788 Oct  8 23:52 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 12283 Oct  8 23:52 03-planner.json
> # Issue #262: The checks on a pull request read exactly like its Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not sta

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> # Issue #262: The checks on a pull request read exactly like its Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> The checks on a pull request should repeat its Definition of Done, in the same words and order, so I read one thing in both places. "All done-whens passed" is a leftover name and reads badly.
> 
> What I want:
> - The checks are named like the Definition of Done rows: All tests (every test in the repo), Acceptance criteria (each criterion's own tests), then Acceptance test, or End-to-end test on a feature, once #233 adds them.
> - Code review and Owner approval show alongside them, as on the card.
> - No leftover names like "done-whens" anywhere a person reads.
> - Renaming a required check must not leave pull requests stuck waiting on the old name: the change says plainly that my branch rule needs the new names at merge, and nothing merges in between

`3. Bash`
```
cd /tmp/pack; sed -n 400,2000p issue.md | cut -c1-3000 | head -300; echo ====; cat open_blockers.json; echo ===; cat plan.json
```

> ### dokima-runtime on issue #262 (2026-10-08T23:48:47Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner proposes a split into 2 stories and asks you questions.
> 
> **Feature:** The owner reads one Definition of Done everywhere: a pull request's checks say All tests, Acceptance criteria, Code review and Owner approval, just like its card.
> 
> 1. The checks are named All tests and Acceptance criteria, with no done-whens left
> 2. Code review and Owner approval show as checks beside All tests and Acceptance criteria, as on the card
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - GitHub orders a pull request's checks list itself, and a workflow can't set that order. Should the check names carry a number (like 1 · All tests, 2 · Acceptance criteria, on the card too) to force the Definition of Done order on GitHub, or stay plain words? Assumed: They stay plain words, exactly as on the card. The order holds where Dokima writes it: the card's Definition of Done row and AGENTS.md. GitHub's own list may

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff main --stat; grep -rni 'done.when' --include=*.yml --include=*.py --include=*.md -l . | head -30; grep -n "unproven" -A25 dokima/agent.py | head -50
```

> d64ed46 Every card opens with one short plain sentence, and the worker's docstrings are checked too (#277)
> 209ae2f A clash with main goes to the planner, on the record (#279)
> 826a1b9 The issue and PR card list criteria as bullets, count the owner's merge and always match (#276)
> dokima/plan.py
> dokima/checks.py
> .github/workflows/card.yml
> tests/test_wiki.py
> .github/workflows/board.yml
> .github/workflows/done-whens.yml
> tests/test_autopilot_board.py
> tests/test_open_ask.py
> tests/test_card.py
> tests/test_plan.py
> tests/test_body.py
> tests/test_checks.py
> tests/test_terms.py
> tests/test_merge_check.py
> 1226:def unproven(repo, sha):
> 1227-    """Why the commit is not proven by every check on it, check runs and commit statuses alike, or None when every
> 1228-    check on it has passed."""
> 1229-    runs = [r for p in pages(gh("api", f"repos/{repo}/commits/{sha}/check-runs?per_page=100", "--paginate"))
> 1230-            for r in p.get("check_runs", [])]
> 1231-    statuses = [s for p in pages(gh("api", f"repos/{repo}/commits/{sha}/status?per_page=100", "--paginate"))
> 1232-                for s in p.get("statuses") or []]
> 1233-    if not runs and not statuses:
> 1234-        return f"there are no checks on its head commit {sha[:7]}"
> 1235-    red = [f"{r['name']} ({r.get('conclusion')})" for r in runs if r.get("status") == "completed" and r.get("conclusion") not in PASSING]
> 1236-    red += [f"{s.get('context')} ({s.get('state')})" for s in statuses if s.get("state") not in ("success", "pending")]
> 1237- 

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner kept the split into two stories and made Code review and Owner approval their own checks on the pull request, as the owner answered.",
   "It widened story 1's third criterion to every text a person reads, with exceptions only for the older \"Done when:\" lines Dokima still reads and copies of past records."
  ],
  "decided": [
   "The card's Definition of Done row gains an Acceptance criteria circle, so the card and the checks read the same four names.",
   "On autopilot, an Owner approval check waiting for the owner never stops a merge the code review approved."
  ],
  "open": [
   "It still asks whether the check names carry a number to force the Definition of Done order in GitHub's checks list."
  ]
 },
 "verdict": "block",
 "summary": "The plan now covers every ask, but two of its own promises contradict each other: AGENTS.md must name the old check \"all done-whens passed\" for the branch rule switch, while another promise forbids done-whens in AGENTS.md with no exception for that line.",
 "blockers": [
  {
   "id": "B2",
   "criterion": "S1.3",
   "test": null,
   "problem": "S1.4 requires AGENTS.md to say the branch rule must switch \"from all tests and all done-whens passed\" to the new names, while S1.3 says no text in AGENTS.md says done-whens and lists only dokima/plan.py, the tests feeding it and tests/samples as exceptions. No work can pass both, so the worker would have to drop one of the owner's asks.",
   "evidence": "plan.json stories[0].acceptance_criteria[2] (S1.3): \"It also covers ... AGENTS.md and the README. The only exceptions are the owner's older \\\"Done when:\\\" plan lines ... and copies of past records in tests/samples.\"; stories[0].acceptance_criteria[3] (S1.4): \"the rule must switch from all tests and all done-whens passed to All tests and Acceptance criteria.\"",
   "fix": "Add to S1.3's exceptions the one AGENTS.md
```

> Exit code 1
> summary holds 42 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** The summary is too long for the check. I'm shortening it and running the check again.

`6. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Two promises clash: AGENTS.md must name the old check \"all done-whens passed\", yet another promise bans done-whens in AGENTS.md."
json.dump(d,open(p,'w'),indent=1,ensure_ascii=False)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 262 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for #262 on one new problem: two of its promises can't both pass.

**The clash (new blocker B2, for the planner):** S1.4 requires AGENTS.md to tell you the branch rule must switch "from all tests and all done-whens passed" to the new names. S1.3 says no text in AGENTS.md may say done-whens, and it doesn't allow an exception for that sentence. Whatever the worker builds would break one of your asks. The smallest fix is to let S1.3 allow exactly that one AGENTS.md sentence and have its test accept only that line.

**What's fixed and covered:**
- **Last round's blocker:** B1 is resolved. S1.3 now covers everything a person reads, as you asked.
- **Your answer:** Code review and Owner approval are now their own checks on the pull request (S2.1 and S2.2).
- **Your asks:** each one now has a criterion behind it.
- **Card row:** the planner made the Acceptance criteria circle a plan promise instead of a question (S2.3). I didn't block on it, because your "so I read one thing in both places" means the card has to match the checks.

**Still your call:** I didn't accept the planner's assumption that check names stay plain words. GitHub orders the checks list itself, so plain names can lose the order there. You asked for "the same words and order", so on autopilot this question will stop for you.

**One note:** the planner added a rule that an Owner approval check still waiting for you never blocks an autopilot merge. It isn't in your words, but it keeps step 6 of the flow working. Today the merge code (`dokima/agent.py:1237`) stops on any check that is still waiting, so story 2's plan needs a test proving this.

There are no tests to run at this stage: the plan is still a split, and each story writes its own tests later. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.
