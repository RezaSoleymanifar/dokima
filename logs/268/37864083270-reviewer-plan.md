# reviewer (plan) for #268

Run: https://github.com/dokima-dev/dokima/actions/runs/37864083270

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (139.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/ac435204-cab9-42c3-8388-a1e02f2b7b36/tool-results/beo7y862n.txt
> 
> Preview (first 2KB):
> .:
> total 156
> drwxr-xr-x  3 runner runner   4096 Oct  9 00:18 .
> drwxrwxrwt 18 root   root     4096 Oct  9 00:18 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 00:18 in
> -rw-r--r--  1 runner runner 129173 Oct  9 00:18 issue.md
> -rw-r--r--  1 runner runner   1428 Oct  9 00:18 open_blockers.json
> -rw-r--r--  1 runner runner  11148 Oct  9 00:18 plan.json
> 
> in:
> total 104
> drwxr-xr-x 2 runner runner  4096 Oct  9 00:18 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 00:18 ..
> -rw-r--r-- 1 runner runner  5150 Oct  9 00:18 01-planner.json
> -rw-r--r-- 1 runner runner  4552 Oct  9 00:18 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  3910 Oct  9 00:18 03-worker.json
> -rw-r--r-- 1 runner runner  2965 Oct  9 00:18 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner  8223 Oct  9 00:18 05-planner.json
> -rw-r--r-- 1 runner runner  4332 Oct  9 00:18 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner   333 Oct  9 00:18 07-not-started.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:18 08-updater.json
> -rw-r--r-- 1 runner runner  8647 Oct  9 00:18 09-planner.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:18 10-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:18 11-updater.json
> -rw-r--r-- 1 runner runner   325 Oct  9 00:18 12-updater.json
> -rw-r--r-- 1 runner runner  5440 Oct  9 00:18 13-reviewer-pla

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo ----; cat plan.json
```

> [
>  {
>   "id": "B1",
>   "criterion": "268.1",
>   "test": "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled",
>   "problem": "The fake worker's summary in every test is two sentences. Since #277 (d64ed46), code on main rejects a worker summary of more than one sentence. So every worker case is rejected before any filing is checked. That breaks the proofs of 268.1, 268.2, 268.3, 268.5 (both tests), 268.6 and 268.7, and they would fail on main however good the work is.",
>   "evidence": "tests/test_filed_issues.py:223 work_handback(summary=\"Built it. The fix is in x.py.\"). Test file copied onto origin/main (a302cb1), pytest -q tests/test_filed_issues.py: 8 failed, 7 with '268.x (worker...): code rejected the worker's hand-back, so this case proves nothing', problem 'summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did'. Same copy with only that default changed to \"Built the fix in x.py.\": 8 failed, all for the right reason, e.g. '268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []'.",
>   "fix": "In tests/test_filed_issues.py work_handback, make the default summary one sentence (e.g. \"Built the fix in x.py.\"), list the change in test_changes, and check the file again against the newest main (#277, #281, #286 merged after this plan).",
>   "fixer": "planner"
>  }
> ]----
> {
>  "kind": "user_story",
>  "summary": "Issues the planner, the worke

`3. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|^---\|^\*\*.*commented\|^<!-- \|^# " issue.md | head -80; wc -l issue.md
```

> 1:# Issue #268: Issues any agent finds are filed by the end-of-turn check, parked and labeled filed-by-dokima
> 3:<!-- dokima-card -->
> 61:<!-- /dokima-card -->
> 63:<!-- dokima-ask -->
> 66:<!-- dokima-card -->
> 67:<!-- /dokima-card -->
> 93:## Comments
> 95:### dokima-runtime on issue #268 (2026-10-08T21:27:32Z)
> 99:### dokima-runtime on issue #268 (2026-10-08T21:27:46Z)
> 101:<!-- dokima-record -->
> 268:### dokima-runtime on issue #268 (2026-10-08T21:40:31Z)
> 270:<!-- dokima-record -->
> 409:### dokima-runtime on issue #268 (2026-10-08T21:43:11Z)
> 414:### dokima-runtime on issue #268 (2026-10-08T21:43:13Z)
> 416:<!-- dokima-record -->
> 495:### dokima-runtime on PR #274 (2026-10-08T21:54:27Z)
> 497:<!-- dokima-record -->
> 595:### dokima-runtime on issue #268 (2026-10-08T22:03:21Z)
> 597:<!-- dokima-record -->
> 793:### dokima-runtime on PR #274 (2026-10-08T22:07:27Z)
> 797:### dokima-runtime on issue #268 (2026-10-08T22:11:55Z)
> 799:<!-- dokima-record -->
> 930:### dokima-runtime on PR #274 (2026-10-08T22:13:23Z)
> 934:### dokima-runtime on issue #268 (2026-10-08T22:15:43Z)
> 939:### dokima-runtime on PR #274 (2026-10-08T22:15:45Z)
> 941:<!-- dokima-record -->
> 973:### dokima-runtime on PR #274 (2026-10-08T22:19:15Z)
> 977:### dokima-runtime on PR #274 (2026-10-08T22:52:23Z)
> 981:### dokima-runtime on PR #274 (2026-10-08T23:47:03Z)
> 985:### dokima-runtime on issue #268 (2026-10-08T23:47:05Z)
> 987:<!-- dokima-record -->
> 1022:### dokima-runtime on issue #268 (2026-10-08T23:47:20Z)
> 1024:<!-- dokima-record -->
> 1223:### doki

`4. Bash`
```
cd /tmp/pack; sed -n 60,100p issue.md; sed -n 409,415p issue.md; sed -n 790,800p issue.md; sed -n 925,990p issue.md; sed -n 1220,1230p issue.md; sed -n 1260,1270p issue.md;sed -n 1300,1312p issue.md; sed -n 1695,1713p issue.md
```

> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #265, story 1</summary>
> 
> **Part of:** #265 Issues the reviewer finds are filed automatically, parked and labeled filed by Dokima
> 
> **User story:** Every problem the planner, the worker or the reviewer comes across outside its own issue becomes a real, parked GitHub issue the moment its run's hand-back passes the check, linked to the run that found it, so nothing Dokima finds is lost again.
> 
> **Context:** Today only a review's hand-back has issues_found (title, why, evidence): dokima/agent.py problems_shape() checks it at line 773 and render() lists it as proposals at lines 447-449; dokima/roles/reviewer.md lines 68-76 describe it and say the findings stay proposals until the owner files them. The planner's plan.json and the worker's work.json have no such field, so their prompts (dokima/roles/planner.md, dokima/roles/worker.md) and checks (dokima/planner.py, dokima/agent.py) need it; the owner's ask names the prompts' field, so dokima/roles/ is in scope. Where filing fits: in .github/workflows/agent.yml the hand-back is checked keyless ('Code checks the hand-back', PASSED), then the app key is minted after the agent finished and 'Decide what follows' runs `python3 -m dokima.agent next` before the record is posted into the run's card comment (CARD_ID), so the link to the record is known there; filing i

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git fetch -q origin main 2>&1|tail -2; git log --oneline -8 origin/main; git log --oneline -3; grep -rn "raises\b\|\"answers\"\|289" dokima/*.py dokima/roles/*.md AGENTS.md | grep -v "pytest.raises" | head -20; ls /tmp/pack/in; cat /tmp/pack/in/13-reviewer-plan.json | head -60
```

> a302cb1 The Autopilot view shows only open issues and pull requests (#286)
> 1c8e0e0 The issue card and the planner's run comment show the links, each kind with its own icon (#281)
> d64ed46 Every card opens with one short plain sentence, and the worker's docstrings are checked too (#277)
> 209ae2f A clash with main goes to the planner, on the record (#279)
> 826a1b9 The issue and PR card list criteria as bullets, count the owner's merge and always match (#276)
> 7cc3eda On autopilot, a question the reviewer answers from the owner's words shows plainly (#275)
> fdb0c5f The planner finds the issues this one is blocked by, blocks or relates to, and code checks them (#256)
> 61e0b7e Open PRs are brought up to date after every merge to main (#267)
> 73649fe planner for #268 (run 37863125401)
> 6c65b78 planner for #268 (run 37861337507)
> fbc77f5 planner for #268 (run 37850995733)
> dokima/board.py:70:    """One REST call; raises subprocess.CalledProcessError when GitHub refuses it."""
> AGENTS.md:42:- **Planner:** turns a rough issue into a plan: an objective, acceptance criteria, scope, and a test for every criterion written before any code. It judges the ask first and raises a concern only with evidence. It may change or delete an older test when the plan makes it wrong, with a reason the owner sees. It proposes splits; it never writes code.
> 01-planner.json
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> 06-reviewer-plan.json
> 07-not-started.json
> 08-updater.json
> 09-planner.json

**Agent:** Checking that the blocker fix holds on main, and weighing the owner's new comment about #289.

`6. Bash`
```
cd /tmp && rm -rf mainchk && git -C /home/runner/work/dokima/dokima worktree add -q /tmp/mainchk origin/main 2>&1|tail -1; cp /home/runner/work/dokima/dokima/tests/test_filed_issues.py /tmp/mainchk/tests/; cd /tmp/mainchk && timeout 600 python3 -m pytest -q tests/test_filed_issues.py 2>&1 | grep -E "^(FAILED|E  +AssertionError|[0-9]+ (failed|passed))|proves nothing|test setup" | head -30; grep -n "summary=" tests/test_filed_issues.py | head
```

> E       AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> E       AssertionError: 268.2: planner: expected 2 filed issues, got []
> E       AssertionError: 268.3: planner: the run did not file its two findings; filed: []
> E       AssertionError: 268.4: a planner listing a finding twice did not file it exactly once beside the other; filed: []
> E       AssertionError: 268.5: planner: the run did not file its two findings; filed: []
>             assert titles(m) == [], f"test setup: GitHub refused every issue, yet some were filed: {titles(m)}"
> E       AssertionError: 268.5: planner: the card does not say the finding was not filed and GitHub's reason:
>                 wrong.append(f"test setup: the {case}'s bad hand-back passed its check")
> E       AssertionError: 268.6: planner: the same agent with a good hand-back did not file its findings; filed: []
> E       AssertionError: 268.7: planner: the run did not file its two findings; filed: []
> FAILED tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled - AssertionError: 268.1: planner (repo with the labels) found two issues but did not file exactly those two by their titles; filed: []
> FAILED tests/test_filed_issues.py::test_a_filed_issue_says_where_and_by_whom_it_was_found_and_links_the_record - AssertionError: 268.2: planner: expected 2 filed issues, got []
> FAILED tests/test_filed_issues.py::test_a_filed_issue_gets_nothing

`7. Bash`
```
cd /tmp/pack; sed -n 1699,1704p issue.md; grep -o "issuecomment-[0-9]*" issue.md | sort -u | tail -5; grep -n "issues_found\|raise" /home/runner/work/dokima/dokima/tests/test_filed_issues.py | head -20
```

> ### RezaSoleymanifar on issue #268 (2026-10-09T00:13:00Z)
> 
> Heads up: #289 replaces the many raise-type fields with two shared ones, raises and answers. Build this toward that shape and add no new raise-type field.
> 
> 6:issues_found ({title, why, evidence}), and the run that hands them back files each one once its hand-back passes.
> 220:            "issues_found": [dict(f) for f in found], "_tests": tests}
> 228:            "issues_found": [dict(f) for f in found]}
> 234:            "issues_found": [dict(f) for f in found]}
> 239:    return {**tam.review_pr("approve"), "issues_found": [dict(f) for f in found]}
> 370:    no finding files nothing. Each agent's prompt names the same field, issues_found, with a title, why and evidence."""
> 387:        if not re.search(r'"issues_found":\s*\[\{"title":\s*"[^"]*",\s*"why":\s*"[^"]*",\s*"evidence":', prompt):
> 389:                         '"issues_found": [{"title": ..., "why": ..., "evidence": ...}]')
> Shell cwd was reset to /home/runner/work/dokima/dokima

`8. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Made the fake worker's summary in every test one sentence, \"Built the fix in x.py.\", since main now rejects a longer one, and listed the change for each test."],
  "decided": ["Kept the five criteria, the two non-functional requirements and every test's checks unchanged, with the found-issues field named issues_found on all three agents."],
  "open": []},
 "verdict": "block",
 "summary": "The test fix holds on today's main, but the plan still adds an issues_found field to the planner and the worker, which the owner's newest comment asks not to do.",
 "blockers": [
  {"id": "B2", "criterion": "268.1",
   "test": "tests/test_filed_issues.py::test_every_issue_any_agent_finds_is_filed_parked_and_labeled",
   "problem": "After this plan was written, the owner said #289 replaces the many raise-type fields with two shared ones, raises and answers, and asked to build this toward that shape and add no new raise-type field. The plan still adds issues_found to the planner's and the worker's hand-backs, and its tests require that exact field name in every prompt and fake hand-back, so the worker would be forced to add the new field the owner ruled out.",
   "evidence": "Owner comment on #268 at 2026-10-09T00:13:00Z: \"Build this toward that shape and add no new raise-type field.\" plan.json 268.1: \"all take the same found-issues field (issues_found: title, why, evidence)\". tests/test_filed_issues.py:220, 228, 234 put issues_found in the planner and worker hand-backs; lines 387-389 fail unless each prompt names \"issues_found\". Neither raises nor #289 appears anywhere in the plan.",
   "fix": "Re-plan 268.1 and its tests on the owner's comment: carry findings in the shared shape #289 brings (raises) instead of a new issues_found field on the planner and worker, and change the tests that pin issues_found in the prompts and hand-backs. If #289's shape is not settled enough to 
```

> summary holds 30 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The test fix holds on main, but the plan still adds an issues_found field the owner's newest comment rules out."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 268 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I'm sending the plan for #268 back to the planner. The test fix from last round works, but the owner commented after this plan was written, and the plan doesn't follow that comment yet.

- **Last round's blocker (B1) is resolved.** I copied the new tests onto today's main and ran them. All 8 fail, and each fails because the feature is missing (for example, "268.1: planner … did not file exactly those two by their titles; filed: []"). None stop early on the fake worker's summary any more.
- **New blocker (B2), for the planner, on criterion 268.1.** At 00:13 the owner wrote: "#289 replaces the many raise-type fields with two shared ones, raises and answers. Build this toward that shape and add no new raise-type field." The plan still adds a new `issues_found` field to the planner's and the worker's hand-backs. The tests also require that exact name in every prompt and fake hand-back (`tests/test_filed_issues.py:220`, `:228`, `:234`, `:387-389`), so the worker would have to add the field the owner ruled out. Neither #289 nor `raises` appears anywhere in the plan.
- **The fix:** re-plan 268.1 and its tests so findings go in #289's shared `raises` field instead of a new one. If #289's shape isn't settled enough to plan against, the plan should ask the owner which reading to build rather than keep `issues_found` without saying so.
- **The owner's asks:** the five criteria and two non-functional requirements each trace to the issue. The new comment is the only ask with no matching criterion, which is why the plan can't be approved.
- **One note:** this branch is still behind main, so the next build should merge main first.

The review is in `/tmp/dokima-out/review.json` and passes both `check review` and `check-round`.
