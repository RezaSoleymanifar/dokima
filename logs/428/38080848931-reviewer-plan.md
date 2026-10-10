# reviewer (plan) for #428

Run: https://github.com/dokima-dev/dokima/actions/runs/38080848931

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (56KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/66cefac1-7ec9-48b4-b2c5-89abbc6d9ddd/tool-results/bb5tif7v9.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> 04-reviewer-plan.json
> 05-planner.json
> # Issue #428: Reads that can use REST instead of GraphQL do, so the two budgets share the load
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/428
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Split a second level:** This story is itself story 3 of #368, and AGENTS.md says a split has one level. Splitting it again adds a second level under #368. Can it split again? The plan assumes it can, because one pull request would mean rewriting the fakes in about 30 test files across the river, the board, the workflows and the audit, all at once. · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue found"> **Outside this issue:** AGENTS.md says a split has one 

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-body-marker\|Original issue/,$p' issue.md | head -150; echo ----; wc -l issue.md
```

> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #368, story 3</summary>
> 
> **Part of:** #368 Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> **User story:** Dokima's reads draw on GitHub's REST budget wherever REST can answer them, so the GraphQL budget no longer runs out while REST sits mostly unused.
> 
> **Context:** On 2026-10-09 GraphQL hit zero while REST had about 4,000 of 5,000 left. GraphQL is spent by: dokima/plan.py lines 169 and 186 (an issue's or pull request's links, which REST answers at /repos/{o}/{r}/issues/{n}/sub_issues and /issues/{n}/dependencies/blocked_by and blocking); dokima/board.py graphql() for the project board (Projects v2; check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not); and every `gh issue view`, `gh pr view` and `gh pr list` in dokima/agent.py, board.py and planner.py and in .github/workflows/, which gh runs as GraphQL. dokima/card.py may change only as far as this story needs, since the issue asks for every read. Writes and reads REST cannot answer stay on GraphQL.
> 
> **Acceptance criteria:**
> - Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through GitHub's REST API. The cards and board it feeds show exactly what they show today. ([source](https://github.com/dokima-dev/dokima/issues/368))
> - Every read that still uses GraphQL is 

`3. Bash`
```
cd /tmp/pack; sed -n '250,422p' issue.md
```

> - 428.1: tests/test_rest_reads.py::test_river_reads_only_rest, tests/test_rest_reads.py::test_board_and_audit_read_issues_only_through_rest, tests/test_rest_reads.py::test_no_graphql_read_of_issues_or_pull_requests_is_left
> - 428.2: tests/test_rest_reads.py::test_conversation_is_the_same_as_today, tests/test_rest_reads.py::test_pull_request_lookups_are_the_same_as_today, tests/test_rest_reads.py::test_started_and_parent_words_are_the_same_as_today, tests/test_rest_reads.py::test_board_reads_are_the_same_as_today, tests/test_rest_reads.py::test_audit_finds_the_same_setup_issue_past_100, tests/test_rest_reads.py::test_workflow_lookups_find_the_same_as_today
> - 428.3: tests/test_rest_reads.py::test_graphql_list_names_exactly_the_reads_rest_cannot_answer
> - 428.4: tests/test_rest_reads.py::test_graphql_list_matches_every_graphql_read_in_the_code, tests/test_rest_reads.py::test_the_list_check_catches_a_new_graphql_read
> - 428.5: tests/test_rest_reads.py::test_refused_river_and_board_reads_fail_naming_githubs_reason, tests/test_rest_reads.py::test_refused_workflow_lookups_fail_as_today
> 
> </details>
> 
> <details><summary>Full record</summary>
> 
> (full record: in/03-planner.json)
> 
> </details>
> 
> <sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> Opus 5.5 · 15.2 min · 51 turns · 4,960,287 tokens in, 63,994 out · $3.44 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; echo; cat parent.json | head -50; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k not in ('criteria',)},indent=1)[:6000])"
```

> []
> {"number": 368}{
>  "kind": "user_story",
>  "summary": "Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.",
>  "user_story": "Dokima reads issues, pull requests and their comments through GitHub's REST budget, so the GraphQL budget no longer runs out while REST sits mostly unused, and the owner can see in one place every read still on GraphQL and why.",
>  "acceptance_criteria": [
>   {
>    "text": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links in dokima/ and .github/workflows/ goes through GitHub's REST API. No `gh issue view`, `gh issue list`, `gh pr view` or `gh pr list` call and no GraphQL query reads them any more. Today's reads are in dokima/agent.py (linked_prs, conversation, file_split, where_card, parent_words, rerun_plan_check, started_before, try_merge, open_pr and main), dokima/board.py (Board.labels, Board.open_pr, Board.parent, issue_of and stopped), dokima/planner.py (main), dokima/audit.py (GitHub.setup_issue), agent.yml (its three pull request lookups and its title read), worker.yml (its pull request lookup) and planner.yml (its issue read). The workflows keep these reads as `gh api` commands on REST paths.",
>    "source": "https://github.com/dokima-dev/dokima/issues/428"
>   },
>   {
>    "text": "What those reads feed shows exactly what it shows today. That covers the cards, records, starting packs, board and workflow steps: the same comments, r

`5. Bash`
```
cd /tmp/pack/in; python3 - <<'E'
import json
a=json.load(open('03-planner.json')); b=json.load(open('05-planner.json'))
print(a.keys())
def plan(r):
    for k in ('handback','plan'):
        if k in r: return r[k]
    return r
pa,pb=plan(a),plan(b)
import difflib
for l in difflib.unified_diff(json.dumps(pa,indent=1).splitlines(),json.dumps(pb,indent=1).splitlines(),lineterm='',n=0): print(l[:400])
E
python3 -c "
import json;r=json.load(open('/tmp/pack/in/04-reviewer-plan.json'));print(json.dumps(r,indent=1)[:5000])"
```

> dict_keys(['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check'])
> --- 
> +++ 
> @@ -42 +42 @@
> -  "Rewriting the older tests' fakes of `gh issue view`, `gh pr view`, `gh pr list` and the board's issue queries to answer REST: the owner asked for that as its own story under #368, and it must merge before this one.",
> +  "Rewriting the older tests' fakes of `gh issue view`, `gh pr view`, `gh pr list` and the board's issue queries to answer REST: that is #445, its own story under #368, and this story is blocked by it, as the owner said.",
> @@ -75 +75,3 @@
> -  "blocked_by": [],
> +  "blocked_by": [
> +   445
> +  ],
> @@ -84,27 +86 @@
> - },
> - "answers": [
> -  {
> -   "raise": "R1",
> -   "answer": "done",
> -   "why": "The split is gone, as the owner asked. The one non-functional line (428.5) no longer says a refused lookup never reads as none. It keeps agent.yml's queued-card lookup reading a refusal as no pull request, as today, and tests/test_rest_reads.py::test_refused_workflow_lookups_fail_as_today proves that the step goes on while the record step's lookup still fails with GitHub's reason."
> -  }
> - ],
> - "raises": [
> -  {
> -   "kind": "issue",
> -   "label": "The fakes story the owner asked for",
> -   "text": "The older tests' fakes of GitHub answer the REST reads that #428 moves to, so #428 can land without breaking them. Today 36 test files fake `gh issue view`, `gh pr view`, `gh pr list` and the board's issue GraphQL queries by their exact argu

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q tests/test_rest_reads.py 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed" | cut -c1-300
```

> >           raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
> E           AssertionError: agent.conversation failed (CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments'])); calls it made that a REST-only GitHub refused: [['issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']]
> >           raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
> E           AssertionError: Board.labels failed (CalledProcessError(1, ['gh', 'api', 'graphql', '-f', 'query=query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){labels(first:100){nodes{name}}}}}', '-f', 'o=o', '-f', 'r=r', '-F', 'n=7'])); calls it made that a REST-only
> >           raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
> E           AssertionError: agent.conversation failed (CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments'])); calls it made that a REST-only GitHub refused: [['issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']]
> >           raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
> E           AssertionError: agent.linked_prs failed (CalledProcessError(1, ['gh', 'pr', 'list', '-R', 'o/r', '--head', 'work/issue-7', '--state', 'all', '--json', 'number'])); calls it made that a 

**Agent:** All 14 new tests still fail for the right reason (the reads still use GraphQL, and there is no `GRAPHQL_READS` yet). Writing the hand-back.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner linked #428 as blocked by #445, the fakes story, as the owner asked, and named #445 in the plan's out of scope."],
  "decided": ["The criteria, scope and 14 tests stay the same as the plan of the last round."],
  "open": ["Whether #445 sits under #368 is set on GitHub, not in this plan; #428's card shows Blocked by: #445."]},
 "verdict": "approve",
 "summary": "The plan is unchanged apart from being blocked by #445, as you asked; every ask has a criterion and all 14 new tests fail today because the reads still go through GraphQL.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through GitHub's REST API.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.1"},
  {"ask": "The cards and board it feeds show exactly what they show today.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.2"},
  {"ask": "Every read that still uses GraphQL is listed in one place in the code with why REST cannot answer it.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.3"},
  {"ask": "A test checks that list against every GraphQL call left.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.4"},
  {"ask": "check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.3"},
  {"ask": "A read moved to REST that GitHub refuses fails the same way the GraphQL read did, naming GitHub's reason.", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.5"},
  {"ask": "Keep this story to what one pull request can do", "source": "https://github.com/dokima-dev/dokima/issues/428", "criterion": "428.1"}
 ]}
E
cd /home/runner/wo
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan only adds the blocked-by link to #445 you asked for; every ask has a criterion and all 14 new tests fail for the right reason."
json.dump(r,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 428 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';r=json.load(open(p))
r['summary']="The plan only adds the blocked-by link to #445 you asked for; every ask has a criterion and all 14 new tests fail correctly."
json.dump(r,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 428 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#428](https://github.com/dokima-dev/dokima/issues/428) (moving issue and pull request reads from GraphQL to REST). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **What changed:** since the last review the plan only adds that [#428](https://github.com/dokima-dev/dokima/issues/428) is blocked by [#445](https://github.com/dokima-dev/dokima/issues/445) (rewriting the older tests' stand-ins for GitHub so they answer REST), which is what you asked for. The criteria, scope and 14 tests are the same as in the plan I approved last round.
- **Tests:** I ran `tests/test_rest_reads.py`. All 14 tests fail today for the right reason: the reads still go through GraphQL, and there is no `GRAPHQL_READS` list in `dokima/manifest.py` yet. None fail from a crash or a bad path.
- **Your asks:** each one in the issue and your comments has a criterion that covers it, so I raised no blockers. There were no open raises to answer.

Two things the plan doesn't settle:
- **#445 under #368:** I couldn't confirm that [#445](https://github.com/dokima-dev/dokima/issues/445) sits under [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking the GitHub API budget), because that is set on GitHub and I have no GitHub access. The card does show "Blocked by: #445".
- **Board reads on GraphQL:** you went on with `/review` without answering my earlier question on whether the board's 15-minute sweep should stay on GraphQL. I took that as going on with the plan's reading, which keeps those reads on GraphQL, and didn't ask again.
