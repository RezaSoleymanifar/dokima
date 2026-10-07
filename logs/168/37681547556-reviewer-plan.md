# reviewer (plan) for #168

Run: https://github.com/dokima-dev/dokima/actions/runs/37681547556

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #168: Merge check reads the criteria from the approved plan, not the issue text
> 
> <!-- dokima-card -->
> ### Plan: add `work` to start
> 
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="none"> Full suite · no check yet
> 
> <!-- /dokima-card -->
> 
> The merge check "all done-whens passed" fails on every pull request from the new flow, so every merge needs my admin override. It looks for the acceptance criteria in the issue's text, but plans now live in the agents' record comments. It found nothing on #160, #161, #162, #163 and #165.
> 
> What I want. The check reads the criteria and their tests from the newest plan the reviewer approved, and passes only when every criterion's tests pass. A pull request with no approved plan, like a hand built one, still fails, and my override stays the explicit way through. The reason for a failure says which criterion failed or that no approved plan was found.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #168 (2026-10-07T19:16:59Z)
> 
> /plan
> 
> 
> ### dokima-runtime on issue #168 (2026-10-07T19:20:55Z)
> 
> <!-- dokima-record -->
> **Planner**
> 
> Pull requests from the new flow pass the merge check on their own proof, so the owner no longer needs an admin override to merge them.
> 
> **Questions for you** (it planned on the reading it names; reply with `/plan` and your words, or leave them):
> - When the reviewer approved a pl

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_merge_check.py; cat dokima/checks.py; cat .github/workflows/done-whens.yml; git show --stat HEAD HEAD~1 | head -30
```

> """The merge check reads its criteria and their tests from the newest plan the reviewer approved (issue #168).
> 
> Every test here runs the real command the "done-whens" workflow runs, `python3 -m dokima.checks matrix`, from the repo
> root, with GitHub faked: a stub `gh` on PATH answers from a JSON file in a temp folder, and the pull request event is a
> temp file. The issue's records are real record comments, drawn by dokima.agent.render, so the check reads exactly what
> the bot posts. Nothing here touches the network.
> """
> import json
> import os
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima import agent  # noqa: E402
> 
> ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
> BOT = "dokima-runtime"
> REPO = "o/r"
> 
> STUB_GH = '''#!/usr/bin/env python3
> """A stand-in for the GitHub CLI: answers from $STUB_DATA."""
> import json, os, sys
> data = json.load(open(os.environ["STUB_DATA"]))
> a = sys.argv[1:]
> if a[:2] == ["issue", "view"]:
>     print(json.dumps(data["issues"][a[2]]))
> elif a[:2] == ["api", "graphql"]:
>     print(json.dumps({"data": {"repository": {"pullRequest": {"closingIssuesReferences": {"nodes": []}}}}}))
> elif a[:2] == ["pr", "view"]:
>     print(json.dumps({"comments": [], "reviews": [], "headRefName": "", "body": ""}))
> else:
>     print("[]")
> '''
> 
> PLAN = {"kind": "user_story", "user_story": "Owners merge without an override.",
>         "acceptance_criteria": [{"text": "First thing works", "source": "#168"},
>      

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_merge_check.py 2>&1 | tail -30; git diff HEAD~2 --stat; grep -n "done_when\|test_pull_request_without" tests/test_checks.py | head
```

> assert set() == {'168.1', '168.2', '168.3'}
>   
>   Extra items in the right set:
>   '168.1'
>   '168.3'
>   '168.2'
>   
>   Full diff:
>   + set()
>   - {
>   -     '168.1',
>   -     '168.2',
>   -     '168.3',
>   - }
> FAILED tests/test_merge_check.py::test_a_pull_request_with_no_approved_plan_gets_one_failing_check_saying_so - AssertionError: 168.3 (no records): expected one failing check 'No approved plan found for issue #168', got []
>   matrix=[]
>   
> assert False
>  +  where False = no_plan_row([], 'No approved plan found for issue #168')
> FAILED tests/test_merge_check.py::test_a_hand_built_pull_request_with_no_issue_fails_saying_so - AssertionError: 168.3: a pull request with no issue did not fail with 'No approved plan found: no issue linked': []
>   matrix=[]
>   
> assert False
>  +  where False = no_plan_row([], 'No approved plan found: no issue linked')
> FAILED tests/test_merge_check.py::test_records_pasted_by_anyone_but_the_bot_do_not_count - AssertionError: 168.4: records pasted by a person counted as an approved plan: []
>   matrix=[]
>   
> assert False
>  +  where False = no_plan_row([], 'No approved plan found for issue #168')
> 6 failed in 0.28s
>  tests/test_checks.py      |  42 +--------
>  tests/test_merge_check.py | 212 ++++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 213 insertions(+), 41 deletions(-)
> 8:def test_long_done_whens_get_short_check_names(record_property):

`4. Bash`
```
cd /home/runner/work/dokima/dokima; ls dokima; grep -n "DOKIMA_BOT\|def pr_issue_number\|def fetch_issue\|def render\|def records\|author\|stage" dokima/*.py | head -80
```

> __pycache__
> agent.py
> app.json
> board.py
> card.py
> checks.py
> fence.py
> icons
> plan.py
> planner.py
> roles
> trail.py
> dokima/plan.py:158:def fetch_issue(repo, number):
> dokima/plan.py:175:def pr_issue_number(repo, pr):
> dokima/agent.py:26:BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
> dokima/agent.py:45:        items += [{"author": r["author"], "body": r["body"], "createdAt": r["submittedAt"], "where": f"PR #{pr} review ({r['state'].lower()})"}
> dokima/agent.py:48:            items.append({"author": {"login": n["user"]["login"]}, "body": n["body"], "createdAt": n["created_at"],
> dokima/agent.py:55:    """The issue as it stands: title, body and every comment with its author and where it was written, oldest first."""
> dokima/agent.py:58:        parts += ["", f"### {c['author']['login']} on {c['where']} ({c['createdAt']})", "", c["body"]]
> dokima/agent.py:62:def records(items):
> dokima/agent.py:67:        if (c.get("author") or {}).get("login") != BOT or MARK not in body:
> dokima/agent.py:90:    reviews = [r for r in recs[plans[-1] + 1:] if r.get("role") == "reviewer" and r.get("stage") == "plan"
> dokima/agent.py:95:def is_record(c, role=None, stage=None):
> dokima/agent.py:96:    """True when a comment is a record the bot posted, of the given role and stage when given."""
> dokima/agent.py:97:    if (c.get("author") or {}).get("login") != BOT or MARK not in (c.get("body") or ""):
> dokima/agent.py:100:    return bool(r) and (role is None or (r[0].get("role") == role and (r[0].get("stage") or "") ==

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 20,110p dokima/agent.py; sed -n 150,200p dokima/plan.py; grep -n "post\|issue comment\|pr comment" dokima/agent.py | sed -n 1,40p
```

> def gh(*args):
>     """Run the GitHub CLI and return its output."""
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> MARK = "<!-- dokima-record -->"
> BOT = os.environ.get("DOKIMA_BOT", "dokima-runtime")
> HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 
> 
> def linked_prs(repo, number):
>     """Pull requests built for the issue: from its work or try branch."""
>     found = []
>     for head in (f"work/issue-{number}", f"try/issue-{number}"):
>         found += json.loads(gh("pr", "list", "-R", repo, "--head", head, "--state", "all", "--json", "number"))
>     return sorted({p["number"] for p in found})
> 
> 
> def conversation(repo, number):
>     """The issue and its pull requests as one list of comments, oldest first, each saying where it was written."""
>     d = json.loads(gh("issue", "view", str(number), "-R", repo, "--json", "number,title,body,comments"))
>     items = [{**c, "where": f"issue #{number}"} for c in d["comments"]]
>     for pr in linked_prs(repo, number):
>         p = json.loads(gh("pr", "view", str(pr), "-R", repo, "--json", "comments,reviews"))
>         items += [{**c, "where": f"PR #{pr}"} for c in p["comments"]]
>         items += [{"author": r["author"], "body": r["body"], "createdAt": r["submittedAt"], "where": f"PR #{pr} review ({r['state'].lower()})"}
>                   for r in p["reviews"] if r.get("body")]
>         for n in json.loads(gh("api", f"repos/{repo}/pulls/{pr}/comments", "--paginate")):
>  

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def post\|\"comment\"\|\"review\"\|--body\|def main" dokima/agent.py | head -30; grep -rn "agent.py post\|dokima.agent post" .github/workflows | head
```

> 159:        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title)).strip()
> 426:    if kind == "review":
> 517:    bad = problems_shape(kind, data) or (problems_review if kind == "review" else problems_work)(data)
> 678:def main(argv):
> 729:            gh("issue", "comment", parent, "-R", repo, "--body", render(rec))

**Agent:** Reviewing the plan for #168: all six new tests fail today for the right reason. I'm now checking where worker and code-review records land on a real issue.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 678,740p dokima/agent.py; grep -n "record" .github/workflows/*.yml | head -20
```

> def main(argv):
>     """agent pack N ROLE STAGE DIR | agent check-pack ROLE STAGE DIR | agent check review|work FILE PLAN N |
>     agent record ROLE STAGE OUT CHECK_FILE PASSED LOG_DIR  (writes OUT/record.json and OUT/comment.md)"""
>     if argv[1] == "pack":
>         has_plan = pack(os.environ["GITHUB_REPOSITORY"], argv[2], argv[3], argv[4], argv[5])
>         return 0 if has_plan or argv[3] == "planner" else 3
>     if argv[1] == "check":
>         if len(argv) < 6:
>             print("the check needs plan.json and the issue number: agent check review|work FILE PLAN N")
>             return 1
>         return check(argv[2], argv[3], argv[4], argv[5])
>     if argv[1] == "check-pack":
>         bad = problems_pack(argv[2], argv[3], argv[4])
>         for b in bad:
>             print(b)
>         return 1 if bad else 0
>     if argv[1] == "record":
>         role, stage, out, check_file, passed, log_dir = argv[2:8]
>         meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "commit_before": os.environ.get("BASE"),
>                 "started_by": os.environ.get("GITHUB_ACTOR"), "models": models_used(log_dir),
>                 "report": run_report(os.path.join(out, "claude.json")), "log": os.environ.get("LOG_URL"),
>                 "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"}
>         text = open(check_file).read() if os.path.exists(check_file) else ""
>         rec = build_record(role, stage, ou

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 225,258p .github/workflows/agent.yml
```

> env:
>           GH_TOKEN: ${{ github.token }}
>         run: |
>           export OWNERS=$(python3 -m dokima.plan approvers)
>           NEXT=$(python3 -m dokima.agent next "$N" "$OUT") || NEXT=stop
>           echo "next=$NEXT" >> "$GITHUB_OUTPUT"; echo "$NEXT"
>       - name: Post the record as a comment, on the PR once there is one
>         if: always()
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>         run: |
>           PR=$(gh pr list -R "$GITHUB_REPOSITORY" --head "try/issue-$N" --state open --json number -q '.[0].number')
>           if [ -n "$PR" ] && { [ "$ROLE" = worker ] || [ "$STAGE" = pr ]; }; then
>             gh pr comment "$PR" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"
>           else
>             gh issue comment "$N" -R "$GITHUB_REPOSITORY" --body-file "$OUT/comment.md"
>           fi
>       - name: Move the card on the board
>         if: always() && vars.DOKIMA_BOARD != ''
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           DOKIMA_BOARD: ${{ vars.DOKIMA_BOARD }}
>         run: python3 -m dokima.agent board "$N" "$OUT" || echo "::warning title=Board not moved::the card could not be moved"
>       - name: Start the next stage
>         if: always() && startsWith(steps.next.outputs.next, 'start ')
>         env:
>           GH_TOKEN: ${{ steps.app.outputs.token }}
>           NEXT: ${{ steps.next.outputs.next }}
>         run: |
>           set -- $NEXT
>           gh api -X POST "repos/$GITHUB_REPOSITORY/dispatches" -f event_type=dokima-next \
> 

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Re-planned after the owner's answer B: when a newer plan is handed back, the merge check fails until that plan is approved.",
          "Added that case to 168.1 and 168.3 and to their tests (a newer plan not yet reviewed, and a newer plan blocked)."],
  "decided": ["Only dokima/checks.py changes; the done-whens workflow stays as it is.",
              "Three old tests that read criteria from the issue's text are deleted, each replaced by a 168 test."],
  "open": ["The planner flags that a pull request changing dokima/checks.py also changes the check that judges it, and suggests a separate issue."]},
 "verdict": "block",
 "summary": "The plan follows the owner's answer, but no test has the records an issue really holds at merge time (the worker's and the code review's after the plan approval), so a check that still fails every real pull request would pass these tests.",
 "blockers": [{"id": "B1", "criterion": "168.1", "test": "tests/test_merge_check.py::test_one_check_per_criterion_of_the_approved_plan_running_exactly_its_tests",
   "problem": "Every passing case ends with the plan review approval as the very last record. On a real issue the worker's record, and code-stage reviewer records, come after the approval (agent.yml posts the worker's record on the issue when no PR is open yet). A check that takes 'the newest record must be a plan approval', or treats a code-stage block as overturning the plan, passes every test here and still fails every pull request from the flow: the exact bug the owner reported.",
   "evidence": "tests/test_merge_check.py: the passing cases use [planned(PLAN), reviewed(APPROVE)] or end with reviewed(APPROVE); no worker record and no record with stage 'pr' appears anywhere. .github/workflows/agent.yml:236-240 posts worker and pr-stage records on the issue whenever no open PR exists.",
   "fix": "In the 168.1 test, add a case [planned(PLAN),
```

> rc=0

**Agent:** I've blocked the plan for #168 on one point: its tests never include the records a real issue holds at merge time, so they can't catch the bug you reported. The review is written to `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the planner did:** It re-planned on your answer B. Once a newer plan is handed back, the merge check fails until that plan is approved. Both cases are now in criteria 168.1 and 168.3 and in their tests: a newer plan not yet reviewed, and a newer plan that was blocked. Only `dokima/checks.py` changes. Three old tests that read criteria from the issue's text are deleted, and a #168 test replaces each one.

**Tests run today:** All 6 new tests in `tests/test_merge_check.py` fail for the right reason. The check still reads the issue's text and returns an empty check list.

**Blocker B1 (168.1):** In every passing test case, the plan approval is the last record on the issue. On a real issue, the worker's record and the code-review records can come after it: `agent.yml` posts them on the issue whenever no pull request is open. So a check that requires "the newest record is a plan approval" would pass every test and still fail every real pull request. The fix is to add a case to the 168.1 test with a worker record and code-stage block and approve records after the approval, and assert the plan's three checks still come out.

**Notes (not blocking):**
- Check names are cut to 60 characters, but 168.1 promises the criterion's words. The tests only use short criteria, so the cut is neither promised nor tested.

**Proposed separate issue:** Run the merge check from main's code. Right now a pull request runs its own `dokima/checks.py`, so it can change the check that judges it. The planner raised this too.
