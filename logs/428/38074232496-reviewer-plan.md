# reviewer (plan) for #428

Run: https://github.com/dokima-dev/dokima/actions/runs/38074232496

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

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
> **Context:** On 2026-10-09 GraphQL hit zero while REST had about 4,000 of 5,000 left. GraphQL is spent by: dokima/plan.py lines 169 and 186 (an issue's or pull request's links, which REST answers at /repos/{o}/{r}/issues/{n}/sub_issues and /issues/{n}/dependencies/blocked_by and blocking); dokima/board.py graphql() for the project board (Projects v2; check whether GitHub's REST project endpoints cover the reads before moving them, and keep GraphQL where they do not); and every `gh issue view`, `gh pr view` and `gh pr list` in dokima/agent.py, board.py and planner.py and in .github/workflows/, which gh runs as GraphQL. dokima/card.py may change only as far as this story needs, since the issue asks for every read. Writes and reads REST cannot answer stay on GraphQL.
> 
> **Acceptance 

`2. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 150,200p dokima/plan.py; grep -rn "graphql" dokima/*.py | grep -v "^dokima/board.py" | head -30; grep -rn "sub_issues\|blocked_by\|dependencies" dokima/*.py | grep -v "^\s*#" | head -40
```

> def approved_version(body, edits, at):
>     """The issue text as it stood at time `at`. `edits` come from GitHub's edit history, each the full text."""
>     if not at or not edits:
>         return body
>     before = [e for e in edits if e["editedAt"] <= at]
>     return max(before, key=lambda e: e["editedAt"])["diff"] if before else body
> 
> 
> def gh(*args):
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> def fetch_issue(repo, number):
>     """The issue with its plan as approved (or as it is, when not approved) and what changed since."""
>     owner, name = repo.split("/")
>     query = ("query($o:String!,$n:String!,$i:Int!){repository(owner:$o,name:$n){issue(number:$i)"
>              "{number title body url userContentEdits(first:100){nodes{editedAt diff}}}}}")
>     data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}", "-F", f"i={number}"))
>     issue = data["data"]["repository"]["issue"]
>     edits = [e for e in issue.pop("userContentEdits")["nodes"] if e.get("diff") is not None]
>     events = json.loads(gh("api", f"repos/{repo}/issues/{number}/events?per_page=100", "--paginate"))
>     at = approved_at(events, repo_approvers(owner))
>     current = parse(issue["body"])
>     approved = parse(approved_version(issue["body"], edits, at)) if at else current
>     issue.update(approved_at=at, plan=approved, current_body=issue["body"],
>                  changes=changes(approved, current) if at else [])
>     return i

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rnE '"(issue|pr)", "(view|list|status|checks)"|gh (issue|pr) (view|list|status|checks)|graphql' dokima/ .github/workflows/ --include=*.py --include=*.yml | grep -v "^dokima/manifest.py" | awk -F: '{print $1}' | sort | uniq -c; ls dokima/*.py | head -50
```

> 4 .github/workflows/agent.yml
>       1 .github/workflows/planner.yml
>       1 .github/workflows/worker.yml
>      13 dokima/agent.py
>       1 dokima/audit.py
>       3 dokima/board.py
>       2 dokima/plan.py
>       1 dokima/planner.py
> dokima/agent.py
> dokima/audit.py
> dokima/board.py
> dokima/body.py
> dokima/card.py
> dokima/checks.py
> dokima/fence.py
> dokima/manifest.py
> dokima/plan.py
> dokima/planner.py
> dokima/raises.py
> dokima/scan.py
> dokima/trail.py
> dokima/uptodate.py
> dokima/words.py

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rnE 'graphql|query\(|query \{|\{repository|"query' dokima/*.py | grep -v manifest.py | head -40; grep -rnE 'gh (issue|pr) (view|list)|"(issue|pr)", "(view|list)"' dokima/agent.py dokima/planner.py dokima/audit.py .github/workflows/ | cut -c1-160
```

> dokima/audit.py:198:BOARD_QUERY = 'query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name color description}}}} views(first:50){nodes{id name layout filter}}}}}'
> dokima/board.py:30:    args = ["gh", "api", "graphql", "-f", f"query={query}"]
> dokima/board.py:51:        p = q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}', o=owner, n=int(number))["organization"]["projectV2"]
> dokima/board.py:58:        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{id projectItems(first:20){{nodes{{id project{{id}}}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=number)["repository"][field]
> dokima/board.py:77:        node = self.q('query($i:ID!,$f:String!){node(id:$i){... on ProjectV2Item{fieldValueByName(name:$f){... on ProjectV2ItemFieldSingleSelectValue{name}}}}}', i=iid, f=field)["node"]
> dokima/board.py:83:        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{labels(first:100){{nodes{{name}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=int(number))["repository"][field]
> dokima/board.py:119:        nodes = self.q('query($o:String!,$r:String!,$h:String!){repository(owner:$o,name:$r){pullRequests(headRefName:$h,states:[OPEN],first:1){nodes{number}}}}', o=self.repo_o

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 98,108p .github/workflows/agent.yml; grep -n "BOARD_QUERY" dokima/audit.py; python3 -m dokima.agent 2>&1 | head -5; grep -n "level\|parent" dokima/planner.py | head -20
```

> GH_TOKEN: ${{ steps.card-key.outputs.token }}
>           SCRUB_CLAUDE: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
>           SCRUB_GITHUB: ${{ github.token }}
>         run: |
>           # Where the record will go: the PR once there is one, for the worker and the PR reviewer.
>           PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --json number -q '.[0].number' || true)
>           WHERE=$N; if [ -n "$PR" ] && { [ "$ROLE" = worker ] || [ "$STAGE" = pr ]; }; then WHERE=$PR; fi
>           python3 -m dokima.agent card "$ROLE" "$STAGE" queued > /tmp/card.md
>           if ID=$(gh api -X POST "repos/$GITHUB_REPOSITORY/issues/$WHERE/comments" -F body=@/tmp/card.md --jq .id); then
>             echo "CARD_ID=$ID" >> "$GITHUB_ENV"
>           else
> 198:BOARD_QUERY = 'query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name color description}}}} views(first:50){nodes{id name layout filter}}}}}'
> 212:            p = board.gql(BOARD_QUERY, o=self.owner, n=self.number)["organization"]["projectV2"]
> Traceback (most recent call last):
>   File "<frozen runpy>", line 198, in _run_module_as_main
>   File "<frozen runpy>", line 88, in _run_code
>   File "/tmp/runtime/dokima/agent.py", line 2285, in <module>
>     sys.exit(main(sys.argv))
> 9:criterion's source is issue N, its parent issue named in the pack, or a comment on either; every test it names is in
> 30:from dokima.agent import pack_parent, pr

**Agent:** I've checked the split's coverage against the code. Next I'll write the review and run the check.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposed splitting the story into 4 stories: the river's reads, the board's reads, the workflows' and audit's reads, and one list of the GraphQL reads left with a test."],
  "decided": ["The edit-history read (fetch_issue) and the closing-issue read (pr_issue_number) in dokima/plan.py stay on GraphQL, since REST has no endpoint for them; the issue's context had called them links reads.", "Each story's planner moves the test fakes of its own area to REST, since the worker cannot change tests."],
  "open": ["Whether this story, already a sub-issue of #368, may split a second level (question P1 for the owner)."]},
 "verdict": "block",
 "summary": "The split covers every GraphQL read in the code, but story 3 adds a failure rule the owner did not ask for, and whether a sub-issue may split again is the owner's call.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Added to the ask",
   "text": "Story 3's non-functional line adds 'A refused lookup of an open pull request never reads as none.' The owner asked only that a moved read GitHub refuses fails the same way the GraphQL read did. Today agent.yml line 103 deliberately reads a refused lookup as none (`|| true`) and posts the queued card on the issue, so story 3 would change that step's behavior instead of keeping it. Smallest fix: drop that sentence, or keep it only for the reads that fail today, and name line 103 as keeping its fallback.",
   "evidence": ".github/workflows/agent.yml:103 `PR=$(gh pr list ... -q '.[0].number' || true)`; the issue's Non-functional line: 'fails the same way the GraphQL read did, naming GitHub's reason'."},
  {"kind": "issue", "label": "Outside this issue",
   "text": "AGENTS.md says a split has one level ('2 to 5 children, one level') while the autopilot rules speak of 'every sub-issue under it at every level'; the two disagree on whether a tree can be deeper than 
```

> Exit code 1
> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`7. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The split covers every GraphQL read, but story 3 adds a failure rule the owner never asked for."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 428 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I blocked the plan for [#428](https://github.com/dokima-dev/dokima/issues/428) (moving reads from GraphQL to REST), with one blocker sent back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner proposed:** split this story into 4 stories:
1. The river's reads move to REST.
2. The board's reads move to REST.
3. The workflows' and the audit's reads move to REST.
4. One list of the GraphQL reads left, with why REST can't answer each, and a test that checks the list.

**What holds up:**
- **Nothing is missed.** I searched `dokima/` and `.github/workflows/` for every GraphQL use, and each one is covered by story 1, 2 or 3. One project read in `dokima/audit.py` isn't named in any story, but story 4's list would have to include it.
- **The planner was right about `dokima/plan.py`.** The issue called its two GraphQL reads "links" reads, but they actually read an issue's edit history and the issue a pull request closes. REST has no endpoint for either, so they stay on GraphQL.

**The blocker (for the planner):** story 3 adds a rule you didn't ask for: "A refused lookup of an open pull request never reads as none." You asked only that a moved read fails the same way the GraphQL read did. Today `.github/workflows/agent.yml:103` deliberately treats a failed lookup as "no pull request" (`|| true`) and posts the queued run card on the issue instead. Story 3 would change that. The fix is to drop the sentence, or name that line as keeping its fallback.

**Your call:** the planner asked whether a story that is already a sub-issue of [#368](https://github.com/dokima-dev/dokima/issues/368) (tracking the GitHub API budget) may split again. AGENTS.md says a split has "one level". I didn't answer it for you: allowing it changes how the system works, and nothing you've written settles it. The river waits for you on this question.

I also raised a separate issue: AGENTS.md says splits have one level, but its autopilot rules talk about sub-issues "at every level", so the two disagree on how deep a tree can go.
