# reviewer (plan) for #428

Run: https://github.com/dokima-dev/dokima/actions/runs/38080853655

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (58.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4fdacd01-948c-4e5d-94d6-3e88adae40f0/tool-results/bemv055vt.txt
> 
> Preview (first 2KB):
> .:
> total 80
> drwxr-xr-x  3 runner runner  4096 Oct 10 19:44 .
> drwxrwxrwt 18 root   root    4096 Oct 10 19:44 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 19:44 in
> -rw-r--r--  1 runner runner 53117 Oct 10 19:44 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 19:44 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 19:44 parent.json
> -rw-r--r--  1 runner runner  6195 Oct 10 19:44 plan.json
> 
> in:
> total 56
> drwxr-xr-x 2 runner runner  4096 Oct 10 19:44 .
> drwxr-xr-x 3 runner runner  4096 Oct 10 19:44 ..
> -rw-r--r-- 1 runner runner 10027 Oct 10 19:44 01-planner.json
> -rw-r--r-- 1 runner runner  3928 Oct 10 19:44 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 10186 Oct 10 19:44 03-planner.json
> -rw-r--r-- 1 runner runner  4567 Oct 10 19:44 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner  6842 Oct 10 19:44 05-planner.json
> -rw-r--r-- 1 runner runner  2607 Oct 10 19:44 06-reviewer-plan.json
> # Issue #428: Reads that can use REST instead of GraphQL do, so the two budgets share the load
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 426 -->
> <!-- dokima-blocking: {"blocked_by": [445], "blocks": [], "loop": []} -->
> Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.
> 
> **Plan**
> 
> https://

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json parent.json; echo; cat plan.json; echo; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> <persisted-output>
> Output too large (43.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/4fdacd01-948c-4e5d-94d6-3e88adae40f0/tool-results/b7w1fgwmr.txt
> 
> Preview (first 2KB):
> []{"number": 368}
> {
>  "kind": "user_story",
>  "summary": "Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.",
>  "user_story": "Dokima reads issues, pull requests and their comments through GitHub's REST budget, so the GraphQL budget no longer runs out while REST sits mostly unused, and the owner can see in one place every read still on GraphQL and why.",
>  "acceptance_criteria": [
>   {
>    "text": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links in dokima/ and .github/workflows/ goes through GitHub's REST API. No `gh issue view`, `gh issue list`, `gh pr view` or `gh pr list` call and no GraphQL query reads them any more. Today's reads are in dokima/agent.py (linked_prs, conversation, file_split, where_card, parent_words, rerun_plan_check, started_before, try_merge, open_pr and main), dokima/board.py (Board.labels, Board.open_pr, Board.parent, issue_of and stopped), dokima/planner.py (main), dokima/audit.py (GitHub.setup_issue), agent.yml (its three pull request lookups and its title read), worker.yml (its pull request lookup) and planner.yml (its issue read). The workflows keep these reads as `gh api` commands on REST paths.",
>    "source": "https

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/4fdacd01-948c-4e5d-94d6-3e88adae40f0/tool-results/b7w1fgwmr.txt
```

> 1	[]{"number": 368}
> 2	{
> 3	 "kind": "user_story",
> 4	 "summary": "Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.",
> 5	 "user_story": "Dokima reads issues, pull requests and their comments through GitHub's REST budget, so the GraphQL budget no longer runs out while REST sits mostly unused, and the owner can see in one place every read still on GraphQL and why.",
> 6	 "acceptance_criteria": [
> 7	  {
> 8	   "text": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links in dokima/ and .github/workflows/ goes through GitHub's REST API. No `gh issue view`, `gh issue list`, `gh pr view` or `gh pr list` call and no GraphQL query reads them any more. Today's reads are in dokima/agent.py (linked_prs, conversation, file_split, where_card, parent_words, rerun_plan_check, started_before, try_merge, open_pr and main), dokima/board.py (Board.labels, Board.open_pr, Board.parent, issue_of and stopped), dokima/planner.py (main), dokima/audit.py (GitHub.setup_issue), agent.yml (its three pull request lookups and its title read), worker.yml (its pull request lookup) and planner.yml (its issue read). The workflows keep these reads as `gh api` commands on REST paths.",
> 9	   "source": "https://github.com/dokima-dev/dokima/issues/428"
> 10	  },
> 11	  {
> 12	   "text": "What those reads feed shows exactly what it shows today. That covers the cards, records, starting packs, board and workflow 

`4. Bash`
```
cd /tmp/pack; grep -n "^##\|^###\|^\*\*.*wrote\|^---" issue.md | head -80; wc -l issue.md
```

> 96:## Comments
> 98:### dokima-runtime on issue #428 (2026-10-10T17:59:13Z)
> 102:### dokima-runtime on issue #428 (2026-10-10T17:59:36Z)
> 141:### dokima-runtime on issue #428 (2026-10-10T18:03:18Z)
> 194:### RezaSoleymanifar on issue #428 (2026-10-10T18:30:57Z)
> 198:### dokima-runtime on issue #428 (2026-10-10T18:31:29Z)
> 271:### dokima-runtime on issue #428 (2026-10-10T18:47:16Z)
> 328:### RezaSoleymanifar on issue #428 (2026-10-10T19:07:00Z)
> 332:### dokima-runtime on issue #428 (2026-10-10T19:08:32Z)
> 397:### RezaSoleymanifar on issue #428 (2026-10-10T19:42:11Z)
> 401:### RezaSoleymanifar on issue #428 (2026-10-10T19:42:14Z)
> 405:### dokima-runtime on issue #428 (2026-10-10T19:42:29Z)
> 447:### dokima-runtime on issue #428 (2026-10-10T19:42:33Z)
> 455 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /tmp/pack; sed -n 1,97p issue.md; sed -n 190,200p issue.md; sed -n 325,335p issue.md; sed -n 395,455p issue.md
```

> # Issue #428: Reads that can use REST instead of GraphQL do, so the two budgets share the load
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 426 -->
> <!-- dokima-blocking: {"blocked_by": [445], "blocks": [], "loop": []} -->
> Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/428
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Split a second level:** This story is itself story 3 of #368, and AGENTS.md says a split has one level. Splitting it again adds a second level under #368. Can it split again? The plan assumes it can, because one pull request would mean rewriting the fakes in about 30 test files across the river, the board, the workflows and the audit, all at once. · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue found"> **Outside this issue:** AGENTS.md says a split has one level ('2 to 5 children, one level') while the autopilot rules speak of 'every sub-issue under it at every level'; the two disagree on whether a tree can be deeper than one level. · filed as an issue
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmidd

**Agent:** I'm re-grading the plan for #428 after the owner's second `/review`; the plan hasn't changed since the last approval, so I'm running the new tests to confirm.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff main --stat; timeout 300 python3 -m pytest -q tests/test_rest_reads.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|AssertionError|Error" | head -40
```

> dc6acd2 planner for #428 (run 38076089391)
> 03d4200 Autopilot says it merged a PR that only queued or is waiting for my approval (#430)
> 20badec A PR that cannot be updated with main gets one comment, updated in place (#431)
>  .github/workflows/done-whens.yml |   4 -
>  dokima/agent.py                  | 102 ++----
>  dokima/card.py                   |   7 +-
>  tests/conftest.py                |   1 +
>  tests/test_build_started_card.py | 117 -------
>  tests/test_checks_rerun.py       | 420 -----------------------
>  tests/test_plan_check_rerun.py   |  29 +-
>  tests/test_queue_judge.py        | 219 ------------
>  tests/test_rest_reads.py         | 723 +++++++++++++++++++++++++++++++++++++++
>  9 files changed, 782 insertions(+), 840 deletions(-)
>         CalledProcessError. The CalledProcessError object will have the return code
>                 raise ValueError('stdin and input arguments may not both be used.')
>                 raise ValueError('stdout and stderr arguments may not be used '
> >               raise CalledProcessError(retcode, process.args,
> E               subprocess.CalledProcessError: Command '['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']' returned non-zero exit status 1.
> /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/subprocess.py:571: CalledProcessError
> >           raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
> E           AssertionError: agent.conversation failed (CalledProcessError(1, 

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main...HEAD --stat; timeout 300 python3 -m pytest -q tests/test_rest_reads.py 2>&1 | tail -16
```

> tests/test_rest_reads.py | 723 +++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 723 insertions(+)
> assert False
>  +  where False = isinstance(None, dict)
> FAILED tests/test_rest_reads.py::test_graphql_list_matches_every_graphql_read_in_the_code - AssertionError: 428.4: dokima/manifest.py has no GRAPHQL_READS dict listing the GraphQL reads left
> assert False
>  +  where False = isinstance(None, dict)
> FAILED tests/test_rest_reads.py::test_the_list_check_catches_a_new_graphql_read - AssertionError: 428.4: dokima/manifest.py has no GRAPHQL_READS dict listing the GraphQL reads left
> assert False
>  +  where False = isinstance(None, dict)
> FAILED tests/test_rest_reads.py::test_refused_river_and_board_reads_fail_naming_githubs_reason - AssertionError: 428.5: conversation failed without GitHub's reason: 'gh: this fake GitHub answers REST reads only, and gh issue/pr run as GraphQL (HTTP 400)\n'
> assert 'Resource not accessible by integration (HTTP 403)' in (('gh: this fake GitHub answers REST reads only, and gh issue/pr run as GraphQL (HTTP 400)\n'))
>  +  where 'gh: this fake GitHub answers REST reads only, and gh issue/pr run as GraphQL (HTTP 400)\n' = CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']).stderr
>  +    where CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']) = <ExceptionInfo CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner kept #428 as one story blocked by #445, the fakes story, with the same criteria, scope and 14 tests as the plan the last review passed."
  ],
  "decided": [
   "The edit history, a pull request's closing issues, its merge-queue state and the board's project reads stay on GraphQL, each listed with a reason in GRAPHQL_READS."
  ],
  "open": [
   "Nothing is built until #445 merges; the earlier question about keeping the board sweep on GraphQL has no answer from the owner yet."
  ]
 },
 "verdict": "approve",
 "summary": "Nothing changed since the last approval: every ask has a criterion, and all 14 new tests still fail because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through GitHub's REST API.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.1"},
  {"ask": "The cards and board it feeds show exactly what they show today.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.2"},
  {"ask": "Every read that still uses GraphQL is listed in one place in the code with why REST cannot answer it.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.3"},
  {"ask": "A test checks that list against every GraphQL call left.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.4"},
  {"ask": "check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.3"},
  {"ask": "A read moved to REST that GitHub refuses fails the same way the GraphQL read did, naming GitHub's reason.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.5"},
  {"ask": "Keep this story to what one p
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#428](https://github.com/dokima-dev/dokima/issues/428) (moving reads from GraphQL to REST). Nothing changed since the last approval, and the hand-back is in `/tmp/dokima-out/review.json`, which passes both checks.

- **Plan unchanged:** it's the same one the last review approved. It's still one story and still waits on [#445](https://github.com/dokima-dev/dokima/issues/445) (rewriting the older tests' fakes) before anything is built. The only file the branch adds is `tests/test_rest_reads.py`.
- **New tests:** all 14 fail today because the feature is missing, not because of a crash or a bad path. Some still read through GraphQL, `GRAPHQL_READS` doesn't exist yet in `dokima/manifest.py`, and the failures don't name GitHub's reason. Each failure names its criterion.
- **Your asks:** I found 7 in the issue and your comments, and each has a criterion. None is missing.
- **Your comments since the last review:** only the two `/review` commands, so there was nothing new to check.
- **Raises:** I raised none, and no raises were waiting for my answer.

One question from an earlier review is still open, and I didn't raise it again: whether the board's whole-board read, its field value read and its item lookup should stay on GraphQL. The plan assumes they should, because GitHub's REST docs don't describe the shape of the data REST would return. If you'd rather move them, answer with `/plan`.

The sources for "Keep this story to what one pull request can do" and "check whether GitHub's REST project endpoints cover the reads" point to the issue itself. The first is from your `/plan` comment and the second from the parent story's context, and I didn't have comment links to use instead.
