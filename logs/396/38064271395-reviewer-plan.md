# reviewer (plan) for #396

Run: https://github.com/dokima-dev/dokima/actions/runs/38064271395

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #396: board.yml runs the pull request's own copy of itself, with the keys, on a review
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/396
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Filed by Dokima from issues its agents raised during their runs and nobody filed. It goes to the backlog; nothing starts until the owner decides.
> 
> - Raised by the reviewer on #332 (2026-10-09, [record](https://github.com/dokima-dev/dokima/issues/332#issuecomment-6076022496)): **board.yml runs the pull request's own copy of itself, with the keys, on a review**. Under 'Identity and safety', agents can't change the workflows that judge them. A pull_request_review run uses the workflow file from the pull request's merge ref, so a pull request that edits board.yml changes how its own review run behaves while it holds the keys environment.
>   Evidence: .github/workflows/board.yml:15-21 (its comment says pull_request_target uses main's copy, but pull_request_review is also listed) and :31 environment: keys.
> 
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercont

`2. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print({k:v for k,v in d.items() if k!='handback'})" | head -50; git show --stat HEAD; cat tests/test_review_relay.py; cat .github/workflows/board.yml
```

> {'role': 'planner', 'stage': None, 'run_id': '38063544260', 'commit_before': 'e02bcb264bf540a81ee342e4d6eb36435fcaa4fa', 'started_by': 'RezaSoleymanifar', 'models': ['claude-opus-5-5'], 'report': {'duration_ms': 578829, 'turns': 32, 'cost_usd': 1.5257986000000006, 'tokens_in': 2052103, 'tokens_out': 25662}, 'log': 'https://github.com/dokima-dev/dokima/blob/logs/logs/396/38063544260-planner.md', 'run': 'https://github.com/dokima-dev/dokima/actions/runs/38063544260', 'check': {'passed': True, 'problems': []}}
> commit b4f96e45fbdd51004daf5093d27dc1b1900f0437
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 15:35:51 2026 +0000
> 
>     planner for #396 (run 38063544260)
> 
>  tests/test_board_state.py  |  11 ++-
>  tests/test_needs_you.py    |  17 ++--
>  tests/test_plan.py         |   6 ++
>  tests/test_review_relay.py | 210 +++++++++++++++++++++++++++++++++++++++++++++
>  4 files changed, 232 insertions(+), 12 deletions(-)
> """The board hears every review and line note, never through a PR's own keyed copy (#396).
> 
> GitHub runs a workflow triggered by pull_request, pull_request_review, pull_request_review_comment, push to a branch
> or workflow_dispatch from the copy of the workflow file on that branch or pull request, so a pull request that edits
> board.yml would change how its own board run behaves while that run holds the keys environment. Only issues,
> issue_comment, schedule, pull_request_target and workflow_run always run the default branch'

`3. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -rn "workflow_run" .github/workflows dokima/*.py | head -30
```

> agent.yml
> assign.yml
> audit.yml
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
> .github/workflows/card.yml:15:  workflow_run:
> .github/workflows/card.yml:37:    if: (github.event_name == 'workflow_run' && (github.event.action != 'in_progress' || github.event.workflow_run.name == 'full suite')) || (github.event_name == 'issue_comment' && github.event.action == 'created' && github.event.issue.pull_request && github.event.sender.type == 'Bot') || (github.event_name == 'pull_request_target' && github.event.pull_request.merged) || github.event_name == 'schedule' || (github.event_name == 'issues' && github.event.action == 'opened') || (github.event_name != 'pull_request_target' && github.event.sender.type != 'Bot' && !github.event.issue.pull_request && !(github.event_name == 'issues' && (github.event.action == 'deleted' || github.event.action == 'transferred')))
> .github/workflows/card.yml:51:          PR: ${{ github.event.pull_request.number || github.event.workflow_run.pull_requests[0].number }}
> .github/workflows/card.yml:52:          HEAD: ${{ github.event.pull_request.head.ref || github.event.workflow_run.head_branch }}
> .github/workflows/card.yml:53:          TITLE: ${{ github.event.workflow_run.display_title }}
> .github/workflows/card.yml:94:          HEAD_SHA: ${{ github.event.workflow_run.head_sha }}
> .github/workflows/card.yml:95:          PR_NUMBER: ${{ github.event.workflow_run.pull_requests[0].number || 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 150,260p dokima/board.py; grep -n "pull_request_review\|workflow_run\|def queue\|def sync" dokima/board.py
```

> if c.get("__typename") not in ("Issue", "PullRequest"):
>                     continue
>                 out.append({"kind": "issue" if c["__typename"] == "Issue" else "pr", "number": c["number"],
>                             "status": (it.get("status") or {}).get("name"),
>                             "action": (it.get("fieldValueByName") or {}).get("name"), "closed": c["state"] != "OPEN",
>                             "autopilot": AUTOPILOT in {label["name"] for label in c["labels"]["nodes"]}})
>             if not items["pageInfo"]["hasNextPage"]:
>                 return out
>             cursor = items["pageInfo"]["endCursor"]
> 
>     def views(self):
>         return [v["name"] for v in self.view_nodes()]
> 
>     def view_nodes(self):
>         """The board's views, each as {id, name, filter}."""
>         p = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){views(first:50){nodes{id name filter}}}}}', o=self.owner, n=self.number)["organization"]["projectV2"]
>         return p["views"]["nodes"]
> 
>     def set_view_filter(self, view_id, filter):
>         self.q('mutation($v:ID!,$f:String!){updateProjectV2View(input:{viewId:$v,filter:$f}){projectV2View{id}}}', v=view_id, f=filter)
> 
>     def add_view(self, name, layout, filter):
>         self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)
> 
> 
> def about(event, p):
>     """[(kind, number, head, body)] of the issue or pull requests an event is about."""
>     if event in ("iss

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_board_state.py tests/test_needs_you.py tests/test_plan.py; python3 -m pytest -q tests/test_review_relay.py tests/test_needs_you.py tests/test_board_state.py tests/test_plan.py 2>&1 | tail -30
```

> commit b4f96e45fbdd51004daf5093d27dc1b1900f0437
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 15:35:51 2026 +0000
> 
>     planner for #396 (run 38063544260)
> 
> diff --git a/tests/test_board_state.py b/tests/test_board_state.py
> index b22113f..3ba3fda 100644
> --- a/tests/test_board_state.py
> +++ b/tests/test_board_state.py
> @@ -228,15 +228,18 @@ def test_the_board_runs_on_every_event_about_an_issue_or_its_pull_request(record
>      """The board workflow runs on every event about an issue or its PR.
>  
>      Proves 331.1. Reads .github/workflows/board.yml's triggers: issues opened, edited, closed, reopened, labeled and unlabeled; a
> -    comment created; a pull request opened, reopened, synchronized and closed; a review submitted; a line note created;
> -    the done-whens checks completed; and the schedule */15 * * * *."""
> +    comment created; a pull request opened, reopened, synchronized and closed; the done-whens checks completed; the
> +    schedule */15 * * * *; and, through a keyless workflow it runs after (#396), a review submitted and a line note created."""
>      record_property("proves", "331.1")
>      on = triggers(open(WORKFLOW).read())
>      want = {"issues": {"opened", "edited", "closed", "reopened", "labeled", "unlabeled"}, "issue_comment": {"created"},
> -            "pull_request_target": {"opened", "reopened", "synchronize", "closed"}, "pull_request_review": {"submitted"},
> -            "pull_request_review_comment": {"create

`6. Bash`
```
cd /home/runner/work/dokima/dokima; cp -r . /tmp/sim && cd /tmp/sim && python3 - <<'EOF'
p='.github/workflows/board.yml'; t=open(p).read()
t=t.replace("""  pull_request_review:
    types: [submitted]
  pull_request_review_comment:
    types: [created]
""","").replace("workflows: [done-whens]","workflows: [done-whens, reviews]")
open(p,'w').write(t)
open('.github/workflows/reviews.yml','w').write("""name: reviews
on:
  pull_request_review:
    types: [submitted]
  pull_request_review_comment:
    types: [created]
permissions: {}
jobs:
  heard:
    runs-on: ubuntu-24.04
    steps:
      - run: echo heard
""")
EOF
python3 -m pytest -q tests 2>&1 | tail -5
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b5axs6rnc). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/c13fdaa2-aeea-4d93-bd52-5e9763e3f101/tasks/b5axs6rnc.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** I'm checking the plan for #396 against a quick sample fix, to confirm its tests pass when the work is done right. Running just the related tests while the full suite runs.

`7. Bash`
```
cd /tmp/sim && python3 -m pytest -q tests/test_review_relay.py tests/test_needs_you.py tests/test_board_state.py tests/test_plan.py tests/test_keys.py 2>&1 | tail -5
```

> ...............................................                          [100%]
> 47 passed in 1.25s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`8. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner planned a fix: board.yml stops running on reviews and line notes, and a new keyless workflow, reviews.yml, runs on them instead, with board.yml running from main's copy when it finishes.",
          "It wrote five new tests and rewrote three older ones that required board.yml itself to run on reviews."],
  "decided": ["commands.yml has the same hole; the planner raised it as its own issue rather than fixing it here."],
  "open": ["Nothing waits on the owner; the plan has no questions."]},
 "verdict": "approve",
 "summary": "The plan closes the hole the issue names: board.yml would only run from main's copy, and reviews and line notes would still move both cards. Every new test fails today for the right reason and passes once the fix is in.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "board.yml runs the pull request's own copy of itself, with the keys, on a review", "source": "https://github.com/dokima-dev/dokima/issues/396", "criterion": "1.1"},
  {"ask": "A pull_request_review run uses the workflow file from the pull request's merge ref, so a pull request that edits board.yml changes how its own review run behaves while it holds the keys environment.", "source": "https://github.com/dokima-dev/dokima/issues/396", "criterion": "1.1"}
 ]}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 396 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds more than one sentence: make it one sentence of at most 25 words saying what the run did
> the ask "board.yml runs the pull request's own copy of itself, with the keys, on a review" is matched to 1.1, which is not a criterion of the plan (396.1, 396.2, 396.3)
> the ask "A pull_request_review run uses the workflow file from the pull request's merge ref, so a pull request that edits board.yml changes how its own review run behaves while it holds the keys environment." is matched to 1.1, which is not a criterion of the plan (396.1, 396.2, 396.3)

`9. Bash`
```
cd /tmp/dokima-out && sed -i 's/"criterion": "1.1"/"criterion": "396.1"/' review.json && python3 - <<'EOF'
import json;p='review.json';d=json.load(open(p))
d["summary"]="The plan stops board.yml running a pull request's copy with the keys, keeps reviews moving the board, and its tests fail today for the right reason."
json.dump(d,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 396 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)
> OK

`10. Bash`
```
cd /tmp/dokima-out && python3 - <<'EOF'
import json;p='review.json';d=json.load(open(p))
d["summary"]="The plan stops board.yml running a pull request's copy with the keys, keeps reviews moving the board, and its tests fail today as they should."
json.dump(d,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 396 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK; rm -rf /tmp/sim
```

> OK

**Agent:** I approved the plan for [#396](https://github.com/dokima-dev/dokima/issues/396) (board.yml runs a pull request's own copy of itself, with the keys, on a review). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the plan does:**
- board.yml stops running on reviews and line notes. It keeps only triggers that GitHub always runs from main's copy.
- A new workflow, reviews.yml, runs on reviews and line notes instead. It holds no keys. When it finishes, board.yml runs from main's copy.
- Three older tests are rewritten because they required board.yml itself to run on reviews.
- The planner noticed commands.yml has the same hole and raised it as a separate issue instead of fixing it here.

**What I checked:**
- **Tests fail today for the right reason:** all five new tests and the three rewritten ones fail only because no relay workflow exists yet and board.yml still runs on reviews. None fail on a crash or a bad path.
- **Tests pass once the fix is in:** on a throwaway copy of the repo I made a minimal version of the fix and ran it against all the related test files: 47 passed. I also started the full suite on that copy but deleted the copy before it finished, so I have no full-suite result.
- **Tests catch the wrong fix:** the tests fail if board.yml keeps any review trigger or adds another trigger that runs a branch's copy. They also fail if board.yml drops the keys or if the relay touches a secret or a key. The review tests cover both sides: a code owner's `/review` clears Needs you on both cards, and someone else's `/work` leaves it.
- **Every ask is kept:** both asks in the issue text are covered by the plan's first criterion. Your only comment was `/plan`, so there were no other asks.

I raised no blockers. There were no open blockers from earlier rounds to answer.

One gap I didn't block on: nothing requires the relay to drop GitHub's built-in token permissions. A pull request can rewrite its own copy of the relay anyway, so a test there wouldn't add much protection.

`11. Bash`
```
tail -15 /tmp/claude-1001/-home-runner-work-dokima-dokima/c13fdaa2-aeea-4d93-bd52-5e9763e3f101/tasks/b5axs6rnc.output
```

> return wrap_session(config, _main)
>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/_pytest/main.py", line 362, in wrap_session
>     os.chdir(session.startpath)
> FileNotFoundError: [Errno 2] No such file or directory: '/tmp/sim'
> pwd: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
> 
> [exited with code 1]

**Agent:** The full-suite run on the sample fix has no result. It crashed because I deleted its folder while it was still running (`FileNotFoundError: '/tmp/sim'`), so it tells us nothing about the plan or the fix.

The approval doesn't depend on it. The full suite matters more for the worker's pull request, and the code review will run it there. What it rests on:
- All eight new and rewritten tests fail on the branch today, each because the fix is missing.
- The same tests pass once a minimal fix is in, along with the rest of the related test files (47 passed).

The approval and `/tmp/dokima-out/review.json` are unchanged.
