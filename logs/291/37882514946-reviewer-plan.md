# reviewer (plan) for #291

Run: https://github.com/dokima-dev/dokima/actions/runs/37882514946

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (80.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2339a078-1ab5-40db-8d54-f25c01c6edda/tool-results/be9wqtw5z.txt
> 
> Preview (first 2KB):
> .:
> total 112
> drwxr-xr-x  3 runner runner  4096 Oct  9 04:09 .
> drwxrwxrwt 18 root   root    4096 Oct  9 04:09 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 04:09 in
> -rw-r--r--  1 runner runner 82001 Oct  9 04:09 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 04:09 open_blockers.json
> -rw-r--r--  1 runner runner 11636 Oct  9 04:09 plan.json
> 
> in:
> total 52
> drwxr-xr-x 2 runner runner  4096 Oct  9 04:09 .
> drwxr-xr-x 3 runner runner  4096 Oct  9 04:09 ..
> -rw-r--r-- 1 runner runner 10086 Oct  9 04:09 01-planner.json
> -rw-r--r-- 1 runner runner  3892 Oct  9 04:09 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner  1844 Oct  9 04:09 03-worker.json
> -rw-r--r-- 1 runner runner  2573 Oct  9 04:09 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 12310 Oct  9 04:09 05-planner.json
> -rw-r--r-- 1 runner runner   342 Oct  9 04:09 06-updater.json
> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 282, 295 -->
> The pull request checks take the Definition of Done's names, All tests and Acceptance criteria, and the word done-when disappears.
> 
> **Plan**
> 
> [issue #291](https://github.com/dokima-dev/dokima/issues/291) · [PR #293](https://github.com/dokima-dev/dokima/pull/293) · <img src="https://raw.githubuser

`2. Bash`
```
cd /tmp/pack; grep -n "^## \|^### \|<!-- dokima-original\|Original" issue.md | head -60; wc -l issue.md
```

> 67:<details><summary>Original issue</summary>
> 94:## Comments
> 96:### dokima-runtime on issue #291 (2026-10-09T01:30:31Z)
> 100:### dokima-runtime on issue #291 (2026-10-09T01:30:45Z)
> 318:### dokima-runtime on issue #291 (2026-10-09T01:39:02Z)
> 449:### dokima-runtime on issue #291 (2026-10-09T01:45:21Z)
> 454:### dokima-runtime on issue #291 (2026-10-09T01:45:23Z)
> 518:### dokima-runtime on PR #293 (2026-10-09T01:52:04Z)
> 611:### RezaSoleymanifar on issue #291 (2026-10-09T03:57:11Z)
> 615:### dokima-runtime on issue #291 (2026-10-09T03:57:32Z)
> 866:### dokima-runtime on PR #293 (2026-10-09T04:04:33Z)
> 870:### dokima-runtime on issue #291 (2026-10-09T04:04:35Z)
> 907:### dokima-runtime on issue #291 (2026-10-09T04:08:50Z)
> 915 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 1,100p issue.md; sed -n 440,620p issue.md; sed -n 860,915p issue.md
```

> <persisted-output>
> Output too large (29.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/2339a078-1ab5-40db-8d54-f25c01c6edda/tool-results/b1pgak5sj.txt
> 
> Preview (first 2KB):
> # Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 282, 295 -->
> The pull request checks take the Definition of Done's names, All tests and Acceptance criteria, and the word done-when disappears.
> 
> **Plan**
> 
> [issue #291](https://github.com/dokima-dev/dokima/issues/291) · [PR #293](https://github.com/dokima-dev/dokima/pull/293) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/293/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #292
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #262, #233, #191, #282, #295
> 
> **User story:** The owner sees a pull request's checks named All tests and Acceptance criteria, the same words as its Definition of Done, finds no done-when anywhere they read, and is told plainly how to switch the branch rule when the rename merges.
> 
> <img src="https://raw.g

`4. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/2339a078-1ab5-40db-8d54-f25c01c6edda/tool-results/b1pgak5sj.txt
```

> 1	# Issue #291: The checks are named All tests and Acceptance criteria, with no done-whens left
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-linked-from: 282, 295 -->
> 5	The pull request checks take the Definition of Done's names, All tests and Acceptance criteria, and the word done-when disappears.
> 6	
> 7	**Plan**
> 8	
> 9	[issue #291](https://github.com/dokima-dev/dokima/issues/291) · [PR #293](https://github.com/dokima-dev/dokima/pull/293) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/293/files)
> 10	
> 11	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #292
> 12	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #262, #233, #191, #282, #295
> 13	
> 14	**User story:** The owner sees a pull request's checks named All tests and Acceptance criteria, the same words as its Definition of Done, finds no done-when anywhere they read, and is told plainly how to switch the branch rule when the rename merges.
> 15	
> 16	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 1

`5. Bash`
```
cd /tmp/pack; cat plan.json; echo; python3 -c "
import json;d=json.load(open('in/05-planner.json'));print(json.dumps(d.get('check'),indent=1));print(d.get('handback',{}).keys())"; cat in/06-updater.json
```

> {
>  "kind": "user_story",
>  "summary": "The checks take the names All tests and Acceptance criteria where the owner chose, and done-when disappears except in the gate check's own name.",
>  "user_story": "The owner sees the check running every test named All tests and the criteria checks under a workflow named Acceptance criteria, finds no done-when anywhere they read except the gate check's own name, and is told plainly how to switch the branch rule when the rename merges.",
>  "acceptance_criteria": [
>   {
>    "text": "The check that runs every test in the repo, and its workflow, are named All tests, in plain words with no number. Dokima's manifest requires the check by that name for main's branch rule, in place of all tests. The card still shows that check's verdict in its Definition of Done row and redraws when it finishes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/291"
>   },
>   {
>    "text": "The workflow of the criteria checks is named Acceptance criteria, in the file acceptance-criteria.yml, with no number. Its gate check keeps its name, all done-whens passed, which the manifest still requires; the owner leaves renaming it to #262. The gate still passes only when every criterion's check passed. Each criterion keeps its own check, named by its number and words. The card and the board still update when these checks finish.",
>    "source": "https://github.com/dokima-dev/dokima/issues/291"
>   },
>   {
>    "text": "No text a person reads says done-when or done-whens, exce

**Agent:** Reviewing the re-plan for issue #291 now: I've read the issue, the owner's re-plan comment, and the new plan. Next I'm checking the branch and running the planner's tests.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --stat | head -60; git diff origin/main --stat 2>/dev/null | tail -20; ls .github/workflows
```

> 46e839b Merge branch 'main' into try/issue-291
> 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
>  AGENTS.md                         |   2 +-
>  dokima/agent.py                   |  81 ++++++++++-
>  tests/test_blocked_worker.py      | 290 ++++++++++++++++++++++++++++++++++++++
>  tests/test_plan_links_recorded.py |  10 +-
>  4 files changed, 378 insertions(+), 5 deletions(-)
> 6ac9bf9 Merge branch 'main' into try/issue-291
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)
>  dokima/app.json        |   4 +-
>  dokima/board.py        |  13 +-
>  dokima/manifest.py     | 416 +++++++++++++++++++++++++++++++
>  tests/test_app.py      |   3 +-
>  tests/test_manifest.py | 650 +++++++++++++++++++++++++++++++++++++++++++++++++
>  5 files changed, 1079 insertions(+), 7 deletions(-)
> 016d6af Merge branch 'main' into try/issue-291
> bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
>  dokima/agent.py                   | 130 +++++++
>  dokima/card.py                    |  94 ++++-
>  tests/test_plan_links_recorded.py | 707 ++++++++++++++++++++++++++++++++++++++
>  3 files changed, 918 insertions(+), 13 deletions(-)
> c610eb4 worker for #291 (run 37871310094)
>  .../workflows/{done-whens.yml => acceptance-criteria.yml}    | 12 ++++++------
>  .github/workflows/board.yml                                  |  2 +-
>  .github/workflows/card.yml                                   |  2 +-
>  .github/w

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def test_" tests/test_check_names.py; git status; git branch -a | head; git log origin/main --oneline -3
```

> 66:def test_the_check_running_every_test_and_its_workflow_are_named_all_tests(record_property):
> 83:def test_the_card_shows_the_all_tests_verdict_in_its_definition_of_done_row(record_property):
> 104:def test_the_card_redraws_when_the_all_tests_workflow_finishes(record_property):
> 118:def test_the_criteria_workflow_and_its_gate_check_are_named_acceptance_criteria(record_property):
> 145:def test_the_card_and_the_board_update_when_the_acceptance_criteria_checks_finish(record_property):
> 206:def test_no_text_a_person_reads_says_done_when(record_property):
> 247:def test_agents_md_lists_the_checks_in_definition_of_done_order(record_property):
> 265:def test_agents_md_names_the_required_checks_and_the_branch_rule_switch(record_property):
> 296:def test_autopilot_merges_only_when_all_tests_and_acceptance_criteria_both_passed(record_property, tmp_path):
> On branch try/issue-291
> nothing to commit, working tree clean
>   main
> * try/issue-291
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 5261412 On autopilot, a blocked issue plans but its worker waits until every blocker closes (#296)
> fd83ff5 Everything Dokima needs from GitHub is declared in one manifest in code (#288)

`8. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/05-planner.json'));h=d.pop('handback');print(json.dumps(d,indent=1))"; for r in 'git log --all --oneline -15'; do cd /home/runner/work/dokima/dokima; $r; done; git log --all --oneline | grep -i "291" 
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37881618763",
>  "commit_before": "6ac9bf9afcbbadadf3afdec60e6a6361965b1a38",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 628398,
>   "turns": 24,
>   "cost_usd": 1.688289,
>   "tokens_in": 1937689,
>   "tokens_out": 25445
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/291/37881618763-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37881618763",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> b52b4d0 Conversation of run 37881618763
> 1fdf004 Conversation of run 37882266981
> 769d6a4 Conversation of run 37880701207
> ef4930a planner for #297 (run 37880701207)
> 36b8ebc Conversation of run 37882123559
> 37f1665 Merge branch 'main' into try/issue-236
> ea2c5b4 Merge branch 'main' into try/issue-295
> d99847b Queued PRs are retested on the latest main before merging (#270)
> 07ba98b Conversation of run 37881627558
> da2f934 Conversation of run 37881136131
> 49dfbce planner for #283 (run 37881136131)
> d6f6e4f Conversation of run 37881700063
> bd8d951 Conversation of run 37881386661
> 8a2e8ed planner for #298 (run 37881386661)
> 1caf263 Conversation of run 37881492739
> 46e839b Merge branch 'main' into try/issue-291
> 6ac9bf9 Merge branch 'main' into try/issue-291
> 70b2910 planner for #268 (run 37875588130)
> 016d6af Merge branch 'main' into try/issue-291
> c610eb4 worker for #291 (run 37871310094)
> 885417e planner for #291 (run 37870112685)
> ddf07fd Conversation of run 3782929

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "
import json;p=json.load(open('/tmp/pack/plan.json'))
for k,v in p['tests'].items():
  for t in v: print(t)" > /tmp/ids.txt; timeout 600 python3 -m pytest -q $(cat /tmp/ids.txt) 2>&1 | tail -15; git show 6ac9bf9:tests/test_check_names.py | grep -n "^def test_"; git log --all --oneline -- tests/test_check_names.py
```

> ERROR: not found: /home/runner/work/dokima/dokima/tests/test_check_names.py::test_the_manifest_requires_all_tests_by_its_new_name
> (no match in any of [<Module test_check_names.py>])
> 
> ERROR: not found: /home/runner/work/dokima/dokima/tests/test_check_names.py::test_the_criteria_workflow_is_named_acceptance_criteria_and_its_gate_keeps_its_name
> (no match in any of [<Module test_check_names.py>])
> 
> ERROR: not found: /home/runner/work/dokima/dokima/tests/test_check_names.py::test_autopilot_merges_only_when_all_tests_and_the_gate_check_both_passed
> (no match in any of [<Module test_check_names.py>])
> 
> 
> no tests ran in 0.17s
> 66:def test_the_check_running_every_test_and_its_workflow_are_named_all_tests(record_property):
> 83:def test_the_card_shows_the_all_tests_verdict_in_its_definition_of_done_row(record_property):
> 104:def test_the_card_redraws_when_the_all_tests_workflow_finishes(record_property):
> 118:def test_the_criteria_workflow_and_its_gate_check_are_named_acceptance_criteria(record_property):
> 145:def test_the_card_and_the_board_update_when_the_acceptance_criteria_checks_finish(record_property):
> 206:def test_no_text_a_person_reads_says_done_when(record_property):
> 247:def test_agents_md_lists_the_checks_in_definition_of_done_order(record_property):
> 265:def test_agents_md_names_the_required_checks_and_the_branch_rule_switch(record_property):
> 296:def test_autopilot_merges_only_when_all_tests_and_acceptance_criteria_both_passed(record_property, tmp_path):
> 885417e planner for #291 (run 

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_check_names.py 2>&1 | tail -30; sed -n 200,300p tests/test_check_names.py
```

> for m in OLD_WORD.finditer(line):
>                     if allowed(path, line, m):
>                         agents_mentions += path == "AGENTS.md"
>                     else:
>                         left.append(f"{path} line {i}: {line.strip()[:120]}")
> >       assert not left, "291.3: the old word done-when is still where a person reads it:\n" + "\n".join(left)
> E       AssertionError: 291.3: the old word done-when is still where a person reads it:
> E         dokima/manifest.py line 51: CHECKS = ["all tests", "all done-whens passed"]
> E         dokima/manifest.py line 54: "main": {"required_checks": ["all tests", "all done-whens passed"]},
> E         tests/test_manifest.py line 121: Proves 282.1. The required checks are the two Dokima's merge waits on, "all tests" and "all done-whens passed", each the
> E         tests/test_manifest.py line 127: assert set(m.CHECKS) == {"all tests", "all done-whens passed"}, f"282.1: the required checks are {m.CHECKS}"
> E         tests/test_manifest.py line 363: "all tests" and "all done-whens passed" by name and through a constant, and reading main's branch rule both ways,
> E         tests/test_manifest.py line 385: DONE_WHENS = "all done-whens passed"
> E         tests/test_manifest.py line 385: DONE_WHENS = "all done-whens passed"
> E         tests/test_manifest.py line 394: whens = next(r for r in runs if r["name"] == DONE_WHENS)
> E       assert not ['dokima/manifest.py line 51: CHECKS = ["all tests", "all done-whens passed"]', 'dokima/manifest.py line 54:

`11. Bash`
```
cd /home/runner/work/dokima/dokima; git show d99847b --stat | head -20; git show d99847b -- .github/workflows/full-suite.yml; git diff 46e839b d99847b -- .github/workflows/ dokima/manifest.py | head -80
```

> commit d99847b719bee7d724090c48566b2b342fdcfca0
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:04:16 2026 -0500
> 
>     Queued PRs are retested on the latest main before merging (#270)
>     
>     * planner for #191 (run 37844031933)
>     
>     * worker for #191 (run 37846162765)
>     
>     * planner for #191 (run 37847537372)
>     
>     * planner for #191 (run 37861344296)
>     
>     * worker for #191 (run 37861677012)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
> commit d99847b719bee7d724090c48566b2b342fdcfca0
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 23:04:16 2026 -0500
> 
>     Queued PRs are retested on the latest main before merging (#270)
>     
>     * planner for #191 (run 37844031933)
>     
>     * worker for #191 (run 37846162765)
>     
>     * planner for #191 (run 37847537372)
>     
>     * planner for #191 (run 37861344296)
>     
>     * worker for #191 (run 37861677012)
>     
>     ---------
>     
>     Co-authored-by: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
>     Co-authored-by: dokima <dokima@users.noreply.github.com>
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
> diff --git a/.github/workflows/full-suite.yml b/.github/workflows/full-suite.yml
> index e498b21..49d756d 10

**Agent:** Still reviewing: the plan's new tests are missing from the branch, so I'm now checking whether the merge-queue change (#270) that landed after the plan adds more places this plan has to cover.

`12. Bash`
```
cd /home/runner/work/dokima/dokima; git grep -niE "done.?whens?|\"all tests\"|'all tests'" d99847b -- dokima .github README.md AGENTS.md | grep -v "dokima/plan.py" | head -40; git diff 46e839b d99847b --stat | tail -15
```

> d99847b:.github/workflows/board.yml:16:    workflows: [done-whens]
> d99847b:.github/workflows/card.yml:8:    workflows: [done-whens, full suite, worker]
> d99847b:.github/workflows/done-whens.yml:1:name: done-whens
> d99847b:.github/workflows/done-whens.yml:14:    name: list done-whens
> d99847b:.github/workflows/done-whens.yml:47:      - name: Run this done-when's tests
> d99847b:.github/workflows/done-whens.yml:53:          if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi
> d99847b:.github/workflows/done-whens.yml:63:    name: all done-whens passed
> d99847b:.github/workflows/done-whens.yml:73:            echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
> d99847b:dokima/card.py:24:ALL_TESTS = "all tests"
> d99847b:dokima/checks.py:70:def annotations(junit_xml, repo, sha, done_when):
> d99847b:dokima/checks.py:78:        lines.append(f"::{kind} file={path},line={line},title={done_when} {verdict}::"
> d99847b:dokima/manifest.py:51:CHECKS = ["all tests", "all done-whens passed"]
> d99847b:dokima/manifest.py:54:    "main": {"required_checks": ["all tests", "all done-whens passed"]},
> d99847b:dokima/roles/planner.md:63:Words: "All tests", never "Full suite". "Out of scope", never "Non-goals".
>  dokima/card.py                                     |   2 +-
>  dokima/checks.py                                   |  21 +-
>  tests/test_all_tests_judge.py                      |  12 +-
>  tests/test_autome

`13. Bash`
```
cd /home/runner/work/dokima/dokima; git show d99847b:tests/test_merge_queue.py | grep -niE "done.?when|all tests|full suite|full-suite" | head -30; git diff 46e839b d99847b -- dokima/checks.py | head -50
```

> 4:`merge_group` event, not `pull_request`. These tests prove the two required workflows (full-suite.yml and
> 5:done-whens.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> 177:    """The pull_request_target payload done-whens.yml gets for pull request n."""
> 240:    lines = workflow("done-whens.yml")
> 253:    """The `ref:` of every checkout in full-suite.yml, the commit the all tests check runs."""
> 254:    return [line.split(":", 1)[1].strip() for line in workflow("full-suite.yml") if re.match(r"^\s+ref:\s", line)]
> 260:    Proves 191.1. Reads the `on:` of full-suite.yml and done-whens.yml and checks each lists merge_group; then evaluates the commit
> 261:    the done-whens check checks out and the commit its annotations link to for a merge_group event, and checks both are
> 263:    the commit the all tests check checks out."""
> 265:    for name in ("full-suite.yml", "done-whens.yml"):
> 271:            f"191.1: in the merge queue the all tests checkout `{expr}` gives {got!r}, not the queued commit {QUEUE_SHA}"
> 273:    assert refs and heads, "191.1: done-whens.yml has no `ref:` on the checkout with `path: pr` or no HEAD_SHA"
> 277:            assert got is not None, f"191.1: done-whens.yml {what} `{expr}` is not `${{{{ a || b }}}}` of github.sha / github.event paths"
> 279:                f"191.1: in the merge queue the done-whens {what} `{expr}` gives {got!r}, not the queued commit {QUEUE_SHA}"
> 285:    """In the queue, the done-whens fin

`14. Bash`
```
cd /home/runner/work/dokima/dokima; git show d99847b:tests/test_merge_queue.py | grep -n "^def test_"
```

> 257:def test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit(record_property):
> 284:def test_queued_pr_gets_the_same_checks_as_on_the_pr(record_property, run_matrix, pr, issue):
> 301:def test_queue_branch_on_another_base_still_finds_the_pr(record_property, run_matrix):
> 312:def test_queued_pr_with_no_linked_issue_fails_the_gate_with_the_same_reason(record_property, run_matrix):
> 334:def test_pull_request_checks_behave_exactly_as_before(record_property, run_matrix):

`15. Bash`
```
cd /tmp/pack; grep -o "https://github.com/dokima-dev/dokima/issues/291#issuecomment-[0-9]*" issue.md | sort -u; grep -n "RezaSoleymanifar on" -A3 issue.md
```

> 611:### RezaSoleymanifar on issue #291 (2026-10-09T03:57:11Z)
> 612-
> 613-/plan Re-plan on today's main: since #288 merged, test 291.3 fails, because the new manifest names the required check "all done-whens passed". That name only changes with #262, so leave the check name itself to #262 and cover every other place a person reads.
> 614-
> Shell cwd was reset to /home/runner/work/dokima/dokima

`16. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner rewrote the plan so the gate check keeps its name, all done-whens passed, and every other place a person reads loses done-when.",
   "The planner kept renaming the check that runs every test to All tests, in the manifest too, and listed 22 older tests to change."
  ],
  "decided": [
   "AGENTS.md names All tests and all done-whens passed as the checks main's branch rule requires, and never says the rule switches to Acceptance criteria."
  ],
  "open": [
   "The planner asks whether the check that runs every test is still renamed to All tests, though the manifest and the branch rule name it too.",
   "No open story renames the gate check all done-whens passed."
  ]
 },
 "verdict": "block",
 "summary": "The new plan follows your note, but its new tests never reached the branch and it misses the merge-queue tests that landed after it, so neither the tests nor the worker could ever pass.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "291.1",
   "test": "tests/test_check_names.py::test_the_manifest_requires_all_tests_by_its_new_name",
   "problem": "The plan's tests are not on the branch. Three of the tests it names do not exist. The tests that do exist are still the first plan's, and they check the opposite of the new criteria: 291.4's test requires AGENTS.md to switch the rule to Acceptance criteria, and 291.3's test allows all done-whens passed only once, in AGENTS.md. None of the 22 test_changes, such as test_manifest.py's DONE_WHENS constant, were made either.",
   "evidence": "pytest -q on the plan's test ids: 'ERROR: not found: tests/test_check_names.py::test_the_manifest_requires_all_tests_by_its_new_name', the same for test_the_criteria_workflow_is_named_acceptance_criteria_and_its_gate_keeps_its_name and test_autopilot_merges_only_when_all_tests_and_the_gate_check_both_passed. git log --all has no 'planner for #291 (run 37881618763)' commit
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> blocker B2 names tests/test_merge_queue.py::test_pull_request_checks_behave_exactly_as_before, which is not one of the plan's tests for 291.1

`17. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
r=json.load(open('review.json'))
r['summary']="The plan follows your note, but its new tests never reached the branch and it misses the merge-queue tests that now name the old checks."
r['blockers'][1]['test']="tests/test_check_names.py::test_the_check_running_every_test_and_its_workflow_are_named_all_tests"
json.dump(r,open('review.json','w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 291 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the re-plan for #291 and sent it back to the planner. Your note is reflected in the plan, but its tests can't run as they stand. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the new plan does:** the gate check keeps its name, all done-whens passed, which is left to #262 as you asked. Everything else is renamed: the check that runs every test becomes All tests, and the criteria workflow becomes Acceptance criteria. Every other place a person reads loses done-when.

**Blockers (both for the planner):**
- **B1: the new tests were never committed.** The planner's run left no commit on `try/issue-291`. Three of the tests the plan names don't exist; pytest reports them "not found". The tests on the branch are still from the first plan and check the opposite of the new criteria: they require AGENTS.md to switch the branch rule to Acceptance criteria, which the new plan forbids. None of the 22 listed changes to older tests were made either.
- **B2: the plan misses the merge-queue tests from #270.** #270 merged after this plan was written. Its tests in `tests/test_merge_queue.py` check that the check is still named "all tests", open `done-whens.yml` by name, and say done-whens in many places. The plan doesn't list that file among the tests to change. The worker can't change test files either, so this work would always fail.

**The planner's one question:** it asks whether the check that runs every test should still be renamed to All tests, since the manifest and main's branch rule also name it. I didn't let autopilot go on with the planner's guess, so this stops for you. Renaming it changes a check the branch rule requires, and your note can be read as leaving that name to #262 too.

**Also noted:**
- No open issue renames the gate check yet, so that leftover name will need its own issue under #262.
- As an issue outside #291, I proposed that a planner run should not pass its check when its tests never reached the branch.

All 10 of your asks in the issue and your comment are covered by a criterion.
