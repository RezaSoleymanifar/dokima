# reviewer (plan) for #262

Run: https://github.com/dokima-dev/dokima/actions/runs/37869988626

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (85.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/80a64690-5051-4fa2-851d-5be70efa092c/tool-results/bm2mpw3g0.txt
> 
> Preview (first 2KB):
> .:
> total 100
> drwxr-xr-x  3 runner runner  4096 Oct  9 01:29 .
> drwxrwxrwt 18 root   root    4096 Oct  9 01:29 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 01:29 in
> -rw-r--r--  1 runner runner 73507 Oct  9 01:29 issue.md
> -rw-r--r--  1 runner runner  1045 Oct  9 01:29 open_blockers.json
> -rw-r--r--  1 runner runner 12001 Oct  9 01:29 plan.json
> 
> in:
> total 64
> drwxr-xr-x 2 runner runner  4096 Oct  9 01:29 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 01:29 ..
> -rw-r--r-- 1 runner runner 10430 Oct  9 01:29 01-planner.json
> -rw-r--r-- 1 runner runner  6788 Oct  9 01:29 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 12283 Oct  9 01:29 03-planner.json
> -rw-r--r-- 1 runner runner  5780 Oct  9 01:29 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 12645 Oct  9 01:29 05-planner.json
> # Issue #262: The checks on a pull request read exactly like its Definition of Done
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="ht

`2. Bash`
```
cd /tmp/pack; grep -v "^$" issue.md | head -c 30000
```

> <persisted-output>
> Output too large (29.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/80a64690-5051-4fa2-851d-5be70efa092c/tool-results/toolu_01NsqkNX1juf1uWKpSWujiEs.txt
> 
> Preview (first 2KB):
> # Issue #262: The checks on a pull request read exactly like its Definition of Done
> <!-- dokima-card -->
> **Backlog**
> This issue has no plan yet.
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> <!-- /dokima-card -->
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> The checks on a pull request should repeat its Definition of Done, in the same words and order, so I read one thing in both places. "All done-whens passed" is a leftover name and reads badly.
> What I want:
> - The checks are named like the Definition of Done rows: All tests (every test in the repo), Acceptance criteria (each criterion's own tests), then Acceptance test, or End-to-end test on a feature, once #233 adds them.
> - Code review and Owner approval show alongside them, as on the card.
> - No leftover names like

`3. Bash`
```
cd /tmp/pack; grep -v "^$" issue.md | tail -c +30000 | head -c 45000
```

> <persisted-output>
> Output too large (42.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/80a64690-5051-4fa2-851d-5be70efa092c/tool-results/bx0wmhdl8.txt
> 
> Preview (first 2KB):
> /dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner proposes a split into 2 stories and asks you questions.
> **Feature:** The owner reads one Definition of Done everywhere: a pull request's checks say All tests, Acceptance criteria, Code review and Owner approval, just like its card.
> 1. The checks are named All tests and Acceptance criteria, with no done-whens left
> 2. Code review and Owner approval show as checks beside All tests and Acceptance criteria, as on the card
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - GitHub orders a pull request's checks list itself, and a workflow can't set that order. Should the check names carry a number (like 1 · All tests, 2 · Acceptance criteria, on the card too) to force the Definition of Done order on GitHub, or stay plain words? Assumed: They stay plain words, exactly as on the card. The order holds where Dokima writes it: the card's Definition of Done row and AGENTS.md. GitHub's own list may show them in its own order.
> <details><summary><b>Concerns</b></summary>
> - Posti

`4. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md
```

> 27:### RezaSoleymanifar on issue #262 (2026-10-08T20:21:52Z)
> 31:### dokima-runtime on issue #262 (2026-10-08T20:22:16Z)
> 36:### dokima-runtime on issue #262 (2026-10-08T21:24:43Z)
> 40:### dokima-runtime on issue #262 (2026-10-08T21:24:57Z)
> 199:### dokima-runtime on issue #262 (2026-10-08T21:28:10Z)
> 397:### RezaSoleymanifar on issue #262 (2026-10-08T23:48:29Z)
> 401:### dokima-runtime on issue #262 (2026-10-08T23:48:47Z)
> 562:### dokima-runtime on issue #262 (2026-10-08T23:52:17Z)
> 745:### RezaSoleymanifar on issue #262 (2026-10-09T01:27:27Z)
> 749:### dokima-runtime on issue #262 (2026-10-09T01:27:47Z)
> 903:### dokima-runtime on issue #262 (2026-10-09T01:29:02Z)
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 395,400p issue.md; sed -n 743,748p issue.md; sed -n 903,1100p issue.md | cut -c1-600
```

> ### RezaSoleymanifar on issue #262 (2026-10-08T23:48:29Z)
> 
> /plan Answer: yes, Code review and Owner approval appear as their own checks in the pull request's checks list, so the list reads exactly like the Definition of Done.
> 
> 
> 
> ### RezaSoleymanifar on issue #262 (2026-10-09T01:27:27Z)
> 
> /plan Answer: plain words, no numbers. The card already shows the order.
> 
> ### dokima-runtime on issue #262 (2026-10-09T01:29:02Z)
> 
> <!-- dokima-live -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/queued.svg" width="16" height="16" align="absmiddle" alt="queued"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/plan-review.svg" width="16" height="16" align="absmiddle" alt="plan review"> **Reviewer (plan)** · setting up
> 
> The machine is setting up: the branch, the starting pack and the tools. This card says working when the agent starts, then becomes the run's record.
> 
> <sub>[run](https://github.com/dokima-dev/dokima/actions/runs/37869988626)</sub>
> Shell cwd was reset to /home/runner/work/dokima/dokima

`6. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; python3 -c "
import json;d=json.load(open('in/04-reviewer-plan.json'));print(json.dumps(d,indent=1)[:6000])"
```

> [
>  {
>   "id": "B2",
>   "criterion": "S1.3",
>   "test": null,
>   "problem": "S1.4 requires AGENTS.md to say the branch rule must switch \"from all tests and all done-whens passed\" to the new names, while S1.3 says no text in AGENTS.md says done-whens and lists only dokima/plan.py, the tests feeding it and tests/samples as exceptions. No work can pass both, so the worker would have to drop one of the owner's asks.",
>   "evidence": "plan.json stories[0].acceptance_criteria[2] (S1.3): \"It also covers ... AGENTS.md and the README. The only exceptions are the owner's older \\\"Done when:\\\" plan lines ... and copies of past records in tests/samples.\"; stories[0].acceptance_criteria[3] (S1.4): \"the rule must switch from all tests and all done-whens passed to All tests and Acceptance criteria.\"",
>   "fix": "Add to S1.3's exceptions the one AGENTS.md sentence that names the old check \"all done-whens passed\" so the owner knows which branch rule entry to switch, and have S1.3's test allow exactly that sentence.",
>   "fixer": "planner"
>  }
> ]
> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37861799429",
>  "commit_before": "d64ed46622029151cc12af13f13b96bfc4be92be",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 71524,
>   "turns": 7,
>   "cost_usd": 0.48494060000000005,
>   "tokens_in": 292939,
>   "tokens_out": 5176
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/262/37861799429-reviewer-plan.md",
>  "run": "https://git

**Agent:** Reading the new plan now to see whether the earlier B2 clash is fixed.

`7. Bash`
```
cd /tmp/pack; cat plan.json | python3 -m json.tool; python3 -c "
import json;d=json.load(open('in/05-planner.json'));h=d['handback'];print({k:v for k,v in h.items() if k not in ('plan',)}.keys()); print(json.dumps(d.get('handback',{}).get('replies') or d.get('handback',{}).get('summary'),indent=1))"
```

> {
>     "kind": "feature",
>     "summary": "A pull request's checks get the Definition of Done's plain names, Code review and Owner approval become checks, and done-whens leave everything a person reads.",
>     "feature": "The owner reads one Definition of Done everywhere: a pull request's checks say All tests, Acceptance criteria, Code review and Owner approval, just like its card.",
>     "stories": [
>         {
>             "title": "The checks are named All tests and Acceptance criteria, with no done-whens left",
>             "user_story": "The owner sees a pull request's checks named All tests and Acceptance criteria, the same words as its Definition of Done, finds no done-when anywhere they read, and is told plainly how to switch the branch rule when the rename merges.",
>             "context": "Today the PR shows two workflows. `.github/workflows/full-suite.yml` is named `full suite` and its job (the check) is `all tests`; `dokima/card.py` finds it by the exact name `ALL_TESTS = \"all tests\"` (card.py line 24, used in `checks_passed` and `render`). `.github/workflows/done-whens.yml` is named `done-whens`: a job `list done-whens`, one job per criterion named `N.k \u00b7 <criterion>` (built by `dokima/checks.py` `check_name`, parsed back by card.py `checks_by_key`, so keep that shape), and a gate job `all done-whens passed`. Every place the old word survives today (grep -rni 'done.when'): done-whens.yml lines 1, 12, 45 (step `Run this done-when's tests`), 51 (`No test verifies th

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added to story 1's third criterion one exception: the single AGENTS.md sentence that names the old check all done-whens passed, so the owner knows which branch rule entry to switch.",
          "It put the owner's answer (plain words, no numbers) into the check names of story 1 and the card's Definition of Done row in story 2."],
  "decided": ["The checks keep plain names; the order is shown on the card and in AGENTS.md, and GitHub's own checks list may show them in its own order."],
  "open": ["The plan has no questions left for the owner."]},
 "verdict": "approve",
 "summary": "The split now asks nothing impossible: AGENTS.md may keep exactly one sentence naming the old check so the owner knows what to switch, and the owner's plain-names answer is in both stories.",
 "blockers": [],
 "notes": [
  {"text": "Story 1's own plan should test that AGENTS.md holds the old name in exactly one sentence, the one about switching the branch rule, and nowhere else, so the exception cannot grow.",
   "evidence": "plan.json stories[0].acceptance_criteria[2] and [3]; stories[0].context last sentence."},
  {"text": "Story 2's own plan should test against dokima/agent.py that an Owner approval check still waiting does not stop an autopilot merge; today any pending check stops it.",
   "evidence": "plan.json stories[1].non_functional[1]; stories[1].context names agent.py unproven."}
 ],
 "outside_plan": [],
 "resolved": ["B2"],
 "issues_found": [],
 "asks": [
  {"ask": "The checks on a pull request should repeat its Definition of Done, in the same words and order, so I read one thing in both places.", "source": "https://github.com/dokima-dev/dokima/issues/262", "criterion": "S2.3"},
  {"ask": "\"All done-whens passed\" is a leftover name and reads badly.", "source": "https://github.com/dokima-dev/dokima/issues/262", "criterion": "S1.2"},
  {"ask": "The checks are named like
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`9. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The split is ready: AGENTS.md may keep one sentence naming the old check, and both stories use plain names as the owner answered."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 262 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for issue #262, a split into two stories. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Last round's blocker (B2) is fixed.** Two rules used to contradict each other: AGENTS.md had to name the old check "all done-whens passed", but another rule banned the word "done-whens" there. Story 1 now allows exactly one AGENTS.md sentence with the old name, the one telling the owner which branch rule entry to switch.
- **The owner's latest answer is in the plan.** Their reply "plain words, no numbers" is now part of the check names in story 1 and the card's Definition of Done row in story 2. The plan has no questions left for the owner.
- **No owner request is missing.** All 11 things the owner asked for each match one criterion of the plan.

A split plan contains no tests yet, so there were none to run this round. I left two notes for when each story writes its own tests:
- **Story 1:** test that AGENTS.md uses the old name in exactly that one sentence and nowhere else, so the exception can't grow.
- **Story 2:** test that an Owner approval check still waiting for the owner doesn't stop an autopilot merge. Today, `dokima/agent.py` stops on any pending check.
