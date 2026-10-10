# reviewer (plan) for #428

Run: https://github.com/dokima-dev/dokima/actions/runs/38077189981

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (33.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3dfb1baa-7f73-4b5e-91f8-aee86f825c84/tool-results/b737m42oy.txt
> 
> Preview (first 2KB):
> # Issue #428: Reads that can use REST instead of GraphQL do, so the two budgets share the load
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/428
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
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
> **Context:** On 2026-10-09 GraphQL hit zero while REST had about 4,000 of 5,000 left. GraphQL is spent by: dokima/plan.py lines 169 and 186 (an issue's or pull request's links, which REST answers at /repos/{o}/{r}/issues/{n}/sub_issues and /issues/{n}/dependencies/blocked_by and blocking); dokima/board.py graphql() for the project board (Projects v2; check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not); and every `gh issue view`, `gh pr view` and `gh pr list` in dokima/agent.py, board.py and planner.py 

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | tail -n +20; ls in; cat open_blockers.json
```

> **User story:** Dokima's reads draw on GitHub's REST budget wherever REST can answer them, so the GraphQL budget no longer runs out while REST sits mostly unused.
> 
> **Context:** On 2026-10-09 GraphQL hit zero while REST had about 4,000 of 5,000 left. GraphQL is spent by: dokima/plan.py lines 169 and 186 (an issue's or pull request's links, which REST answers at /repos/{o}/{r}/issues/{n}/sub_issues and /issues/{n}/dependencies/blocked_by and blocking); dokima/board.py graphql() for the project board (Projects v2; check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not); and every `gh issue view`, `gh pr view` and `gh pr list` in dokima/agent.py, board.py and planner.py and in .github/workflows/, which gh runs as GraphQL. dokima/card.py may change only as far as this story needs, since the issue asks for every read. Writes and reads REST cannot answer stay on GraphQL.
> 
> **Acceptance criteria:**
> - Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through GitHub's REST API. The cards and board it feeds show exactly what they show today. ([source](https://github.com/dokima-dev/dokima/issues/368))
> - Every read that still uses GraphQL is listed in one place in the code with why REST cannot answer it. A test checks that list against every GraphQL call left. ([source](https://github.com/dokima-dev/dokima/issues/368))
> 
> **Non-functional:**
> - A read moved to REST that GitHub refuses fails the

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k not in()},indent=1)[:6000])"; python3 -c "
import json;d=json.load(open('in/03-planner.json'));print(list(d.keys()));print(json.dumps(d.get('raises') or d.get('handback',{}).get('raises'),indent=1)[:3000])"
```

> {
>  "kind": "user_story",
>  "summary": "Dokima's reads of issues, pull requests and comments move from GraphQL to REST, and the GraphQL reads left are listed in one place with why.",
>  "user_story": "Dokima reads issues, pull requests and their comments through GitHub's REST budget, so the GraphQL budget no longer runs out while REST sits mostly unused, and the owner can see in one place every read still on GraphQL and why.",
>  "acceptance_criteria": [
>   {
>    "text": "Every read of an issue, pull request, comment list, sub-issues or blocked-by links in dokima/ and .github/workflows/ goes through GitHub's REST API. No `gh issue view`, `gh issue list`, `gh pr view` or `gh pr list` call and no GraphQL query reads them any more. Today's reads are in dokima/agent.py (linked_prs, conversation, file_split, where_card, parent_words, rerun_plan_check, started_before, try_merge, open_pr and main), dokima/board.py (Board.labels, Board.open_pr, Board.parent, issue_of and stopped), dokima/planner.py (main), dokima/audit.py (GitHub.setup_issue), agent.yml (its three pull request lookups and its title read), worker.yml (its pull request lookup) and planner.yml (its issue read). The workflows keep these reads as `gh api` commands on REST paths.",
>    "source": "https://github.com/dokima-dev/dokima/issues/428"
>   },
>   {
>    "text": "What those reads feed shows exactly what it shows today. That covers the cards, records, starting packs, board and workflow steps: the same comments, reviews and line no

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; wc -l tests/test_rest_reads.py; timeout 600 python -m pytest -q tests/test_rest_reads.py 2>&1 | tail -30
```

> commit dc6acd275d83635d4468b27f79c759f7d046e96d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:47:04 2026 +0000
> 
>     planner for #428 (run 38076089391)
> 
>  tests/test_rest_reads.py | 723 +++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 723 insertions(+)
> 723 tests/test_rest_reads.py
>     .github/workflows/planner.yml::The issue as it stands: gh issue view "$N" -R "$GITHUB_REPOSITORY" --json number,title,body -q '"Issue #
>     .github/workflows/worker.yml::Push and open the pull request: if [ -z "$(gh pr list -R "$GITHUB_REPOSITORY" --head "work/issue-$N" --state ope
> assert not {'dokima/agent.py::linked_prs': 'gh pr list', 'dokima/agent.py::conversation': 'gh issue view', 'dokima/agent.py::file_split': 'gh issue view', 'dokima/agent.py::where_card': 'gh pr list', ...}
> FAILED tests/test_rest_reads.py::test_conversation_is_the_same_as_today - AssertionError: agent.conversation failed (CalledProcessError(1, ['gh', 'issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments'])); calls it made that a REST-only GitHub refused: [['issue', 'view', '7', '-R', 'o/r', '--json', 'number,title,body,comments']]
> FAILED tests/test_rest_reads.py::test_pull_request_lookups_are_the_same_as_today - AssertionError: agent.linked_prs failed (CalledProcessError(1, ['gh', 'pr', 'list', '-R', 'o/r', '--head', 'work/issue-7', '--state', 'all', '--json', 'number'])); calls it made that a REST-only GitHub refused: [['pr', 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,260p tests/test_rest_reads.py
```

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 260,723p tests/test_rest_reads.py
```

> """Tests for #428: issue and pull request reads use REST, and GraphQL reads left are listed.
> 
> GitHub gives REST and GraphQL separate budgets, and on 2026-10-09 GraphQL ran out while REST had most of its budget
> left. `gh issue view`, `gh pr view` and `gh pr list` all run as GraphQL, as does every `gh api graphql` query. These
> tests prove three things:
> 
> - Every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through REST. Each read is
>   run against a fake `gh` put first on PATH. The fake answers GitHub's REST paths only and refuses `gh issue`,
>   `gh pr` and `gh api graphql`, logging every call. A static scan names every GraphQL read left in dokima/ and
>   .github/workflows/.
> - What those reads feed comes out exactly as today: the same conversation (same comments, reviews and line notes, in
>   the same order, with the bot named as `dokima-runtime` the way GraphQL names it), the same pull request, labels,
>   parent and issue text.
> - The GraphQL reads left are listed in one place, `GRAPHQL_READS` in dokima/manifest.py, each with why REST cannot
>   answer it, and the scan checks that list against every GraphQL read in the code.
> 
> A read moved to REST that GitHub refuses must still fail as the GraphQL read did, naming GitHub's reason; the fake
> refuses every REST read when the state says so.
> """
> import ast
> import json
> import os
> import re
> import shutil
> import stat
> import subprocess
> import sys
> import textwrap
> 
> import pytest
> 
> ROOT = os.path.abspath(os.path.j

> def change(self, **kw):
>             s = self.state()
>             s.update(kw)
>             path.write_text(json.dumps(s))
> 
>         def graphql_calls(self):
>             return [c["argv"] for c in self.state()["calls"] if c["kind"] != "rest"]
> 
>         def rest_reads(self):
>             return [c for c in self.state()["calls"] if c["kind"] == "rest"]
> 
>     return Fake()
> 
> 
> def run(fake, what, fn):
>     """Run a read, failing in plain words when it still reads through GraphQL."""
>     try:
>         out = fn()
>     except Exception as e:  # noqa: BLE001 - every failure is reported with the calls that caused it
>         raise AssertionError(f"{what} failed ({e!r}); calls it made that a REST-only GitHub refused: "
>                              f"{fake.graphql_calls()}") from e
>     assert not fake.graphql_calls(), f"{what} still reads through GraphQL: {fake.graphql_calls()}"
>     return out
> 
> 
> def new_board():
>     """A Board with its project already read, so only issue reads run."""
>     b = board.Board.__new__(board.Board)
>     b.q, b.rest = board.gql, board.api
>     b.owner, b.number, b.repo_owner, b.repo_name = "o", 1, "o", "r"
>     b.id, b.fields = "PVT_1", {}
>     return b
> 
> 
> def view(c):
>     """What the cards and records read from a conversation item."""
>     return (c["author"]["login"], c["body"], c["createdAt"], c["where"], c.get("url"))
> 
> 
> # 428.1: every read of an issue, pull request, comment list, sub-issues or blocked-by links goes through REST
> 
> def test_river_reads_only_rest(fake, record_p

**Agent:** Status: the 14 new tests all fail today for the right reason. Next I'm checking that the plan's code scan really finds every GraphQL read in the code.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "GRAPHQL_OP" dokima/manifest.py; python3 -c "
import sys;sys.path.insert(0,'tests');sys.path.insert(0,'.')
import test_rest_reads as t
for k,v in sorted(t.graphql_reads('.').items()): print(k,'|',v)
"; grep -rn "graphql" dokima/*.py | grep -v "^dokima/board.py" | head -30
```

> 109:GRAPHQL_OP = re.compile(r"\s*(query|mutation)\s*(\w+\s*)?[({]")
> 141:    level = "write" if GRAPHQL_OP.match(text).group(1) == "mutation" else "read"
> 207:        op = GRAPHQL_OP.match(text).group(1)
> 293:            if GRAPHQL_OP.match(s):
> .github/workflows/agent.yml::Post the record as a comment, on the PR once there is one | PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --jso
> .github/workflows/agent.yml::Push the planner's tests or the worker's code to try/issue-N | if [ "$ROLE" = worker ] && [ -z "$(gh pr list -R "$GITHUB_REPOSITORY" --head "tr
> .github/workflows/agent.yml::Put up the run's card, queued | PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --jso
> .github/workflows/planner.yml::The issue as it stands | gh issue view "$N" -R "$GITHUB_REPOSITORY" --json number,title,body -q '"Issue #
> .github/workflows/worker.yml::Push and open the pull request | if [ -z "$(gh pr list -R "$GITHUB_REPOSITORY" --head "work/issue-$N" --state ope
> dokima/agent.py::conversation | gh issue view
> dokima/agent.py::file_split | gh issue view
> dokima/agent.py::linked_prs | gh pr list
> dokima/agent.py::main | gh pr list
> dokima/agent.py::merge_outcome | gh pr view
> dokima/agent.py::open_pr | gh pr list
> dokima/agent.py::parent_words | gh issue view
> dokima/agent.py::rerun_plan_check | gh pr list
> dokima/agent.py::started_before | gh issue view
> dokima/agent.py::try_merge | gh pr view
> dokima/agent.py::where_card | gh pr list
> dokima/audit.py::BOARD

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rnoE "gh (repo|label|project|search|release|run|workflow|issue|pr) [a-z-]+" dokima/*.py .github/workflows/ | awk -F: '{print $NF}' | sort | uniq -c; grep -rnE '"(repo|label|project|search)", "(view|list)"' dokima/*.py | head; grep -n "def try_merge" -A30 dokima/agent.py | grep -n "pr\", \"view\|gh(" 
```

> 7 gh issue comment
>       1 gh issue edit
>       2 gh issue view
>       3 gh pr comment
>       2 gh pr create
>       4 gh pr list
>       1 gh pr merge
> 6:1676-        files = [f["filename"] for p in pages(gh("api", f"repos/{repo}/pulls/{pr}/files?per_page=100", "--paginate")) for f in p]
> 10:1680-        head = gh("pr", "view", str(pr), "-R", repo, "--json", "headRefOid", "-q", ".headRefOid").strip()
> 17:1687-        gh("pr", "merge", str(pr), "-R", repo, "--squash", "--match-head-commit", head)
> 27:1697-    return gh("pr", "list", "-R", repo, "--head", f"try/issue-{number}", "--state", "open", "--json", "number",

`9. ToolSearch`
```
{"query": "select:WebFetch", "max_results": 1}
```

> 

`10. WebFetch`
```
{"url": "https://docs.github.com/en/rest/projects/items", "prompt": "For \"List items for an organization owned project\": what query parameters exist (e.g. fields), and does the response include field values (like a single select Status) and the item's content (issue state and labels)? Is there an endpoint to get an item by issue? Quote exact text."}
```

> **Query parameters** (plus path parameters `org` and `project_number`):
> 
> - **`q`**: "Search query to filter items, see Filtering projects for more information." The page doesn't document the filter syntax.
> - **`fields`**: "Limit results to specific fields, by their IDs. If not specified, the title field will be returned." Accepts `fields[]=123&fields[]=456` or `fields=123,456,789`.
> - **`before` / `after`**: Pagination cursors, given in the Link header.
> - **`per_page`**: Maximum 100, default 30.
> 
> **Response contents:**
> 
> - **Field values (e.g., Status):** Each item has a `fields` array of objects, but the page doesn't document its structure. Since only the title field is returned by default, you would presumably need to pass the Status field's ID in `fields`. The page doesn't explain how to find that ID or show the output shape.
> - **Item content (issue state, labels):** `content` is documented only as "object or null, additional properties allowed," so this page doesn't confirm that issue state or labels are returned. The detailed Issue schema (with `state` and `labels`) appears only in the Add item responses.
> 
> **Get an item by issue:** No. The only single-item GET is by item ID: `GET /orgs/{org}/projectsV2/{project_number}/items/{item_id}`. The Add item endpoint accepts `owner`, `repo`, and `number`, but it adds an item rather than retrieving one. To find an issue's item ID through this page's endpoints, you would have to list items, possibly using `q`, but the page doesn't do

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -lE '"issue", "view"|"pr", "list"|"pr", "view"|issue view|pr list|pr view' tests/*.py | grep -v test_rest_reads | wc -l; grep -n "def file_issues" -A25 dokima/agent.py | grep -n "issue\", \"create\|sub_issues\|blocked" 
```

> 34
> 22:1320-            url = gh("issue", "create", "-R", repo, "--title", title, "--body", "\n".join(body)).strip()

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned #428 as one story, no split, as the owner asked: every issue, pull request and comment read moves to REST, and the GraphQL reads left are listed in GRAPHQL_READS in dokima/manifest.py with a test.",
          "The planner raised the rewrite of the older tests' fakes as its own issue, as the owner asked, and wrote 14 new tests in tests/test_rest_reads.py."],
  "decided": ["The edit history, a pull request's closing issues, its merge-queue state and the board's project reads stay on GraphQL, each with a reason."],
  "open": ["Whether the fakes story goes under #368 with #428 blocked by it (question P3 for the owner); until it merges, this story's pull request turns about 140 older tests red."]},
 "verdict": "approve",
 "summary": "The plan carries every ask as one story and its 14 tests fail today for the right reason; it waits on you to order it after the fakes story, and to accept that the board's card sweep stays on GraphQL.",
 "raises": [
  {"kind": "question", "to": "owner", "label": "Board sweep stays on GraphQL",
   "text": "The plan keeps the board's whole-board read (Board.cards), its field value read (Board.value) and its item lookup (Board.item) on GraphQL. GitHub's REST project items list does take a fields parameter that returns field values such as Status, but its docs leave the shape of those values and of the issue content undocumented, and there is no lookup of an item by issue. Is keeping those reads on GraphQL right, since the sweep every 15 minutes is a large GraphQL spender? The review assumes it is, because a read built on an undocumented shape could break silently.",
   "evidence": "docs.github.com/en/rest/projects/items, List items for an organization owned project: 'fields: Limit results to specific fields, by their IDs'; content is 'object or null, additional properties allowed'; the only single-item GET is by item ID. Criter
```

> Exit code 1
> summary holds 40 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** The checker found the summary too long. Shortening it, then running the check again.

`13. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan carries every ask in one story and its tests fail today for the right reason; it waits on you for its order and the board sweep."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 428 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)
> 0

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan carries every ask in one story and its tests fail for the right reason; it waits on you for ordering and the board sweep."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 428 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> 0

**Agent:** I approved the plan for [#428](https://github.com/dokima-dev/dokima/issues/428) (moving reads from GraphQL to REST), with one new question for you. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the plan does:** it follows your `/plan` comment. It stays one story with no second level of split. Every read of an issue, pull request or comment in `dokima/` and in agent.yml, worker.yml and planner.yml moves to REST, and the cards and board show exactly what they show today. The reads that stay on GraphQL are listed in `GRAPHQL_READS` in `dokima/manifest.py`, each with a reason. A test checks that list against the code and names any GraphQL read that isn't on it.

**What I checked:**
- **Today's run:** all 14 new tests in `tests/test_rest_reads.py` fail for the right reason. Calls still go to GraphQL, or `GRAPHQL_READS` doesn't exist yet; none fails on a crash.
- **The code scan:** run against today's code, it finds every GraphQL read the plan names. It also catches a new read added in Python or in a workflow.
- **The fake:** it answers REST only, with 105 comments and 160 open issues so reads must go past the first 100 results. It pins the exact conversation order, the bot's name, the right pull request (or none), labels, parent and issue text. It also checks that a refused read fails with GitHub's reason, while the queued-card lookup keeps its deliberate fallback.

**Your decisions:**
- **Ordering (P3, the planner's question):** this story can only merge after the story that rewrites the older tests' fakes. Without it, about 140 older tests go red, and the worker isn't allowed to change them. The fakes story will be filed as a plain issue, not under [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking the GitHub API budget), so placing it under #368 and marking #428 blocked by it is up to you.
- **The board sweep (my new question):** the plan keeps three board reads on GraphQL: the whole-board sweep (`Board.cards`), the field value read (`Board.value`) and the lookup of an issue's board item (`Board.item`). GitHub's REST endpoint that lists project items does take a `fields` option that returns values like Status. But its docs don't describe the shape of those values or of the issue data, and REST has no way to look up an item by issue. I went along with keeping them on GraphQL, since a read built on an undocumented shape could break without warning. The 15-minute sweep is a big GraphQL spender, though, so it's your decision.

**The fakes issue (P2):** I confirmed the issue raise for rewriting the fakes, so it gets filed. 34 older test files fake `gh issue view`, `gh pr view` or `gh pr list` by their exact arguments.

**Ask not tied to a criterion:** I left one of your asks off the review's list: filing the fakes rewrite as its own story. No criterion carries it, because it's handled by the filed issue rather than by code.
