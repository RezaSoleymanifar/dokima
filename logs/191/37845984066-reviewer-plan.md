# reviewer (plan) for #191

Run: https://github.com/dokima-dev/dokima/actions/runs/37845984066

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  8 21:19 .
> drwxrwxrwt 18 root   root   4096 Oct  8 21:20 ..
> drwxr-xr-x  2 runner runner 4096 Oct  8 21:19 in
> -rw-r--r--  1 runner runner 8769 Oct  8 21:19 issue.md
> -rw-r--r--  1 runner runner    2 Oct  8 21:19 open_blockers.json
> -rw-r--r--  1 runner runner 2467 Oct  8 21:19 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  8 21:19 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 21:19 ..
> -rw-r--r-- 1 runner runner 3078 Oct  8 21:19 01-planner.json
> # Issue #191: Queued PRs are retested on the latest main before merging
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
> <details open><summary>From the approved plan of #57, story 3</summary>
> 
> **Part of:** #57 Keep PRs up to date with main automatically
> 
> **User story:** With GitHub's merge queue on, every PR is retested against the latest main, with every criterion's check, before it merges.
> 
> **Context:** The required checks come from full-suite.yml ('all tests') and done-whens.yml (one check per criterion plus 'all done-whens passed'). Neither runs on the merge_group event today, so a queue would wait for checks that never come. dokima/checks.py 'matrix' reads the PR number from the pull_request event (GITHUB_EVENT_PATH ['pull_r

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_merge_queue.py; git show --stat HEAD
```

> """Queued pull requests are retested on the latest main, with every criterion's check, before they merge.
> 
> GitHub's merge queue tests each pull request on top of the latest main in a temporary commit and sends the
> `merge_group` event, not `pull_request`. These tests prove the two required workflows (full-suite.yml and
> done-whens.yml) run on that event, that `python3 -m dokima.checks matrix` finds the pull request's issue from the
> queue's branch (refs/heads/gh-readonly-queue/<base>/pr-<N>-<sha>) and lists the same checks as on the pull request, and
> that pull request checks are unchanged.
> 
> `dokima.checks matrix` runs for real, as a subprocess, against a fake `gh` put first on PATH. The fake knows a few pull
> requests and issues (see PRS and PLANS) and answers:
>   - `gh pr view N [--json ...] [-q/--jq .path]`: number, headRefName, body, comments, reviews, closingIssuesReferences;
>   - `gh pr list ...`: [];
>   - `gh issue view N --json ...`: the issue with its bot record comments (an approved plan);
>   - `gh api repos/O/R/pulls/N`: number, head.ref, body; `gh api repos/O/R/pulls/N/comments`: [];
>   - `gh api graphql ...` with the pull request number in any -F/-f field: repository.pullRequest with number,
>     headRefName, body and closingIssuesReferences.nodes.
> Anything else exits 1 saying the fake does not know the call.
> 
> The workflows' commit expressions are checked by evaluating them: each must be `${{ a || b ... }}` where every part is
> `github.sha` or a `github.event...` path; the f

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/full-suite.yml .github/workflows/done-whens.yml
```

> name: full suite
> # Every test in the repo, on every pull request and on main.
> on:
>   pull_request:
>   push:
>     branches: [main]
> permissions:
>   contents: read
> jobs:
>   all-tests:
>     name: all tests
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - run: pytest -q -p no:cacheprovider tests
> name: done-whens
> # One GitHub check per criterion of the PR's approved plan, plus one gate check.
> # Runs main's copy of this workflow and of Dokima's code; only the tests, and the code they judge, come from the PR.
> on:
>   pull_request_target:
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
> jobs:
>   list:
>     name: list done-whens
>     runs-on: ubuntu-24.04
>     outputs:
>       matrix: ${{ steps.m.outputs.matrix }}
>     steps:
>       - uses: actions/checkout@v5
>       - id: m
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
> 
>   check:
>     needs: list
>     if: needs.list.outputs.matrix != '[]'
>     name: ${{ matrix.name }}
>     strategy:
>       fail-fast: false
>       matrix:
>         include: ${{ fromJSON(needs.list.outputs.matrix) }}
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           persist-credentials: false
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.pull_request.head.sha }}
>           path: pr
>  

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat dokima/checks.py
```

> """Turn the criteria of an issue's approved plan into GitHub checks, and annotate the tests they ran.
> 
>     python3 -m dokima.checks matrix          # print the check list for this PR
>     python3 -m dokima.checks annotate r.xml  # print one annotation per test in a JUnit report
> 
> The plan is the newest one the planner handed back, once the reviewer approved it, read from the bot's own record
> comments; each criterion's check runs exactly the tests that plan lists for it.
> 
> A test proves a criterion by calling record_property("proves", "<issue>.<n>"),
> where n counts the issue's criteria from 1, top to bottom.
> """
> import json
> import os
> import re
> import sys
> import xml.etree.ElementTree as ET
> 
> from dokima import agent, plan
> 
> PROVES = re.compile(r"""record_property\(\s*["']proves["']\s*,\s*["']([\d.]+)["']\s*\)""")
> TEST_DEF = re.compile(r"^def (test_\w+)\(")
> 
> 
> def find_tests(paths):
>     """Map each criterion key like '29.1' to the tests that prove it, as 'path::test'."""
>     found = {}
>     for path in sorted(paths):
>         current = None
>         with open(path) as f:
>             for line in f:
>                 name = TEST_DEF.match(line)
>                 if name:
>                     current = name.group(1)
>                 for key in PROVES.findall(line):
>                     if current:
>                         found.setdefault(key, []).append(f"{path}::{current}")
>     return found
> 
> 
> def check_name(key, text, limit=60):
>     """The check's name on GitHub: '29.1 · <criterion, shortened>'."

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_merge_queue.py 2>&1 | tail -40
```

> KeyError: 'pull_request'
>   
> assert 1 == 0
> FAILED tests/test_merge_queue.py::test_queue_branch_on_another_base_still_finds_the_pr - AssertionError: 191.2: in the merge queue on release/2.0, `dokima.checks matrix` failed:
>   Traceback (most recent call last):
>     File "<frozen runpy>", line 198, in _run_module_as_main
>     File "<frozen runpy>", line 88, in _run_code
>     File "/home/runner/work/dokima/dokima/dokima/checks.py", line 95, in <module>
>       main(sys.argv)
>     File "/home/runner/work/dokima/dokima/dokima/checks.py", line 85, in main
>       pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]
>            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
>   KeyError: 'pull_request'
>   
> assert 1 == 0
> FAILED tests/test_merge_queue.py::test_queued_pr_with_no_linked_issue_fails_the_gate_with_the_same_reason - AssertionError: 191.3: in the merge queue (pull request #90), `dokima.checks matrix` failed:
>   Traceback (most recent call last):
>     File "<frozen runpy>", line 198, in _run_module_as_main
>     File "<frozen runpy>", line 88, in _run_code
>     File "/home/runner/work/dokima/dokima/dokima/checks.py", line 95, in <module>
>       main(sys.argv)
>     File "/home/runner/work/dokima/dokima/dokima/checks.py", line 85, in main
>       pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]
>            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
>   KeyError: 'pull_request'
>   
> assert 1 == 0
> FAILED tests/test_merge_queue.py:

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_merge_queue.py 2>&1 | grep -E "^(FAILED|E  )" | head; grep -n "def issue_of_pr\|def pr_issue_number\|def conversation" -A25 dokima/agent.py dokima/plan.py | head -120
```

> E           AssertionError: 191.1: full-suite.yml does not run on the merge queue's merge_group event; its `on:` is ['pull_request', 'push']
> E           assert 'merge_group' in {'pull_request', 'push'}
> E            +  where {'pull_request', 'push'} = triggers(['name: full suite', '# Every test in the repo, on every pull request and on main.', 'on:', '  pull_request:', '  push:', '    branches: [main]', ...])
> E            +    where ['name: full suite', '# Every test in the repo, on every pull request and on main.', 'on:', '  pull_request:', '  push:', '    branches: [main]', ...] = workflow('full-suite.yml')
> E       AssertionError: 191.2: in the merge queue (pull request #12), `dokima.checks matrix` failed:
> E         Traceback (most recent call last):
> E           File "<frozen runpy>", line 198, in _run_module_as_main
> E           File "<frozen runpy>", line 88, in _run_code
> E           File "/home/runner/work/dokima/dokima/dokima/checks.py", line 95, in <module>
> E             main(sys.argv)
> dokima/plan.py:175:def pr_issue_number(repo, pr):
> dokima/plan.py-176-    """The issue a PR closes, or None."""
> dokima/plan.py-177-    owner, name = repo.split("/")
> dokima/plan.py-178-    query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
> dokima/plan.py-179-             "{closingIssuesReferences(first:1){nodes{number}}}}}")
> dokima/plan.py-180-    data = json.loads(gh("api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={nam

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "asks\|\"criterion\"\|missing" dokima/agent.py | head -40; cat /tmp/pack/in/01-planner.json | head -c 600
```

> 204:        handback = {"missing": f"{HANDBACK[role]}: {e}"}
> 356:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 378:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 381:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 384:        n = len({b.get("criterion") for b in h.get("blockers") or [] if isinstance(b, dict)})
> 596:            bad.append(f"question {i} asks nothing: its question needs a '?'")
> 620:        for field in ("id", "criterion", "problem", "evidence", "fix"):
> 633:        bad.append("the reviewer never asks the owner; escalate on round three instead")
> 637:def problems_asks(r, ids):
> 638:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 639:    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
> 640:    asks = r.get("asks")
> 641:    if not isinstance(asks, list) or not asks:
> 642:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 643:                "\"source\": \"a link to where they said it\", \"criterion\": \"N.k\" or \"missing\"}"]
> 644:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="as

**Agent:** I've read the plan and run its tests. All 7 fail today for the right reason: the merge queue isn't supported yet. Now I'm writing the review.

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned three criteria and one non-functional requirement, taken from the issue: both required checks run in the merge queue on the queued commit, the queue finds the pull request's issue from its branch and lists the same checks, and an unlinked queued pull request fails with the same reason.",
          "Wrote tests/test_merge_queue.py: 6 tests (7 runs). They run `dokima.checks matrix` for real against a fake GitHub CLI, for pull request and merge queue events, and read the two workflows' triggers and commit expressions."],
  "decided": ["Limited the work to full-suite.yml, done-whens.yml and dokima/checks.py; turning the queue on stays the owner's setting on GitHub."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the issue, and each test runs the real check list for a queued and an unqueued pull request; all 7 fail today because the queue isn't supported yet.",
 "blockers": [],
 "notes": [
  {"text": "191.2 says the issue is found from the queue's branch, but the test's queue event also says 'Merge pull request #N' in its commit message, so code that reads the message instead of the branch would still pass. The list it produces would be the same, so this does not block.",
   "evidence": "tests/test_merge_queue.py queue_event(): head_commit.message = f\"Merge pull request #{n}\""},
  {"text": "191.1 checks the triggers and the done-whens commit expressions. It would not catch a job-level `if:` that skips the checks on merge_group, or a full-suite checkout pinned to a commit other than the queued one.",
   "evidence": "tests/test_merge_queue.py::test_both_required_workflows_run_in_the_merge_queue_on_the_queued_commit reads only `on:`, `ref:` next to `path: pr`, and HEAD_SHA"}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "With GitHub's merge queue on, every PR is retested against the latest main, 
```

> rc=0

**Agent:** I approved the plan for issue #191. The hand-back is in `/tmp/dokima-out/review.json` and passed both checks.

**What I checked:**
- **Every ask is covered.** The issue asks for five things: the user story, three criteria and one non-functional requirement. Each one has a criterion in the plan (191.1 to 191.4), and none is missing.
- **The tests fail today for the right reason.** I ran `tests/test_merge_queue.py`: all 7 test runs fail. In the queue cases, `dokima.checks matrix` stops with `KeyError: 'pull_request'` because it can't read a merge queue event yet. The trigger checks fail because the queue's `merge_group` event isn't in either workflow yet. The pull request cases of the same tests already work against the fake GitHub CLI, so the failures come from the missing feature, not a broken test setup.
- **The tests run the real thing.** They run the actual check-list builder for both a pull request and a queued one. They cover three ways a pull request can be linked to its issue (by branch name, by "Closes #N" in the body, and by GitHub's own link), plus a base branch with a slash in its name and a pull request with no linked issue. They also require pull request checks to stay exactly as before: same triggers, same check names, same commit tested.

**Two notes (they don't block the plan):**
- 191.2 says the issue is found from the queue's branch. But the test's fake queue event also has "Merge pull request #N" in its commit message, so code that read the message instead would still pass. The check list would come out the same either way.
- 191.1 reads the workflow triggers and which commit the done-whens test. It wouldn't catch a job-level `if:` that skips the checks in the queue, or the full suite being pinned to a commit other than the queued one.

The plan has no questions for the owner, so it now waits for `/work`, or starts by itself if the issue is on autopilot.
