# reviewer (plan) for #176

Run: https://github.com/dokima-dev/dokima/actions/runs/37705570467

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #176: Plan review fails silently on a split: it needs a try branch splits never create
> 
> - [ ] Goal: a planner's proposed split gets its plan review like any other plan
>   - [ ] Done when: the plan reviewer starts on an issue whose planner proposed a split, with no try branch needed
>     Verified by: a test that the reviewer's start step accepts a split issue that has no try/issue-N branch
>   - [ ] Done when: a command or step that fails before its agent starts posts a record on the issue saying why and stops for the owner
>     Verified by: a test that a start failure leaves a comment with the reason and the Needs you mention
> 
> Requested by Reza in chat, 2026-10-07.
> 
> <details><summary><b>Context</b></summary>
> 
> When the planner proposes a split, the river starts the plan reviewer, which fails at once with "try/issue-N does not exist; run the planner first", because a split never creates a try branch. The failure posts nothing on the issue and pings no one, so the issue looks like it is still being reviewed. Seen on #143 (twice today) and #57 (run 37695866467). Both are stuck until this lands.
> 
> </details>
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #176 (2026-10-07T23:54:56Z)
> 
> How a split should go. The planner proposes it, the reviewer reviews it, then it stops and pings me. Child issues get filed only after my /work, never before.
> 
> ### RezaSoleymanifar on issue #176 (2026-10-07T23:54:57Z)
> 
> /plan
> 
> ### dokima-runtime on issue #176 (2026-10-08T00:02:07Z)
> 
> <!-- dokima-record -

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_start.py; ls dokima tests
```

> commit 9eb599b207bbeef2c5880ff534a32a0bd4b52fb3
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 00:02:00 2026 +0000
> 
>     planner for #176 (run 37704929062)
> 
>  tests/test_start.py | 456 ++++++++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 456 insertions(+)
> """A run that starts an agent either starts it or says why on the issue, and a split gets its plan review (#176).
> 
> These tests run the agent workflow's own steps, read from .github/workflows/agent.yml, the way GitHub runs them: each
> step's `if:` is evaluated, its `${{ }}` expressions filled in, and its script run with bash in a clone of a temp git
> repo whose origin is a local bare repo. Nothing leaves the machine: a fake `gh` answers from a fake issue and records
> every comment, dispatch and issue it is asked to create; a fake `claude` hands back a review; `pip` and `npm` do
> nothing; pushes to github.com are redirected to the local origin. Steps that only `uses:` an action are skipped (the
> app token step gives a fake token). Paths under /tmp and /home/runner are moved into the test's temp folder. Values a
> step writes to GITHUB_ENV or GITHUB_OUTPUT are read as single KEY=value lines.
> 
> The fake issue is #57 in repo o/r, owned by `owner-person` through CODEOWNERS; Dokima's code is copied from this repo.
> """
> import json
> import os
> import re
> import shutil
> import subprocess
> import sys
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from dokima 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_start.py 2>&1 | tail -80
```

> ## Post the record as a comment, on the PR once there is one (exit 1)
>   Traceback (most recent call last):
>     File "/tmp/pytest-of-runner/pytest-0/test_a_reviewed_split_stops_fo0/split/bin/gh", line 13, in <module>
>       body = open(flag("--body-file")).read() if flag("--body-file") else flag("--body")
>              ^^^^^^^^^^^^^^^^^^^^^^^^^
>   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_a_reviewed_split_stops_fo0/split/dokima-out/comment.md'
>   
>   ## Fail closed on a bad hand-back or the wrong model (exit 1)
>   Traceback (most recent call last):
>     File "<string>", line 1, in <module>
>   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-0/test_a_reviewed_split_stops_fo0/split/dokima-out/record.json'
>   
> assert False
>  +  where False = agent_started()
>  +    where agent_started = <test_start.Run object at 0x7f25646995b0>.agent_started
> FAILED tests/test_start.py::test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner - AssertionError: 176.3: a start failure at 'Only a code owner starts an agent' posted 0 comments, expected one:
>   ## Only a code owner starts an agent (exit 1)
>   ::error title=Not started::stranger is not a code owner.
>   
>   ## Decide what follows, and say it on the card (exit 0)
>   stop
>   Traceback (most recent call last):
>     File "<frozen runpy>", line 198, in _run_module_as_main
>     File "<frozen runpy>", line 88, in _run_code
>     File "/tmp/pytest-of-runner/pytest-0/test

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_start.py 2>&1 | grep -E "^E |FAILED|AssertionError" | head -30
```

> E       AssertionError: 176.1: the plan reviewer never started on a split with no try/issue-57 branch; it stopped at 'Starting branch':
> E         ## Starting branch (exit 1)
> E         ::error title=Nothing to reviewer::try/issue-57 does not exist; run the planner first.
> E         
> E         ## Decide what follows, and say it on the card (exit 0)
> E         stop
> E         Traceback (most recent call last):
> E           File "<frozen runpy>", line 198, in _run_module_as_main
> E           File "<frozen runpy>", line 88, in _run_code
> E           File "/tmp/pytest-of-runner/pytest-1/test_the_plan_reviewer_starts_0/split/runtime/dokima/agent.py", line 830, in <module>
> E             sys.exit(main(sys.argv))
> E                      ^^^^^^^^^^^^^^
> E           File "/tmp/pytest-of-runner/pytest-1/test_the_plan_reviewer_starts_0/split/runtime/dokima/agent.py", line 799, in main
> E             step = next_step(items, json.load(open(os.path.join(out, "record.json"))), owners)
> E                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E         FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-1/test_the_plan_reviewer_starts_0/split/dokima-out/record.json'
> E         
> E         ## Post the record as a comment, on the PR once there is one (exit 1)
> E         Traceback (most recent call last):
> E           File "/tmp/pytest-of-runner/pytest-1/test_the_plan_reviewer_starts_0/split/bin/gh", line 13, in <module>
> E             body = open(f

`5. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/rv && cat > /tmp/rv/probe.py <<'EOF'
import sys, os, tempfile, pathlib
sys.path.insert(0, "tests"); sys.path.insert(0, ".")
import test_start as T
d = pathlib.Path(tempfile.mkdtemp())
story = [T.owner_comment("/plan","2026-10-07T10:00:00Z"), T.record_comment(T.planner_record(T.STORY),"2026-10-07T10:10:00Z")]
r = T.Run(d/"a","reviewer","plan",story,try_branch=True)
print("started",r.agent_started(),"failed",r.failed,r.failed_step, "base==try", r.env.get("BASE")==r.try_sha)
print([p["body"][-300:] for p in r.posted()]); print(r.board(), r.dispatches())
r = T.Run(d/"b","reviewer","plan",T.SPLIT_PROPOSED,try_branch=True)
print("split w/ branch: started",r.agent_started(),"failed",r.failed,r.failed_step)
print([p["body"][-300:] for p in r.posted()]); print(r.board(), r.dispatches(), r.created_issues())
if r.failed: print(r.tail())
EOF
python /tmp/rv/probe.py
```

> started True failed False None base==try True
> ['problems": []\n }\n}\n```\n\n</details>\n\n<sub>Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md) · [run](https://github.com/o/r/actions/runs/42)</sub>\n\n**Next:** @owner-person The plan is approved. Say `/work` to build it, or `/plan` with changes.\n']
> Plan needs []
> split w/ branch: started True failed False None
> ['problems": []\n }\n}\n```\n\n</details>\n\n<sub>Opus 5.5 · 0.0 min · 1 turns · [conversation](https://github.com/o/r/blob/logs/logs/57/42-reviewer-plan.md) · [run](https://github.com/o/r/actions/runs/42)</sub>\n\n**Next:** @owner-person The plan is approved. Say `/work` to build it, or `/plan` with changes.\n']
> Plan needs [] []

`6. Bash`
```
cd /home/runner/work/dokima/dokima; ls .github/workflows; grep -n "name:\|exit 1\|::error\|dispatches\|if:" .github/workflows/commands.yml | head -80
```

> agent.yml
> assign.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> wiki.yml
> worker.yml
> 1:name: commands
> 2:run-name: "${{ github.event.comment.body }}"
> 20:    if: >-
> 51:    if: needs.route.outputs.role == 'split'
> 63:      - name: File the approved split's stories as sub-issues
> 70:    if: needs.route.outputs.role != '' && needs.route.outputs.role != 'split'

`7. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/commands.yml; grep -n "name:\|::error\|exit 1\|  if:\|      if:" .github/workflows/agent.yml
```

> name: commands
> run-name: "${{ github.event.comment.body }}"
> # The listener. A code owner's comment whose first line starts with /plan, /work or /review starts that stage, on the
> # issue or on its pull request, and so does a PR review submitted as a comment or a change request. An Approve never
> # starts anything: it only ever means merge. Everything after the command, and every other comment, review and line
> # note, reaches the agent through its pack. No command, nothing starts; bots never start anything. On an issue
> # /review grades the plan; on a pull request, the work.
> on:
>   issue_comment:
>     types: [created]
>   pull_request_review:
>     types: [submitted]
> permissions:
>   contents: read
>   issues: read
>   pull-requests: read
>   actions: read
> jobs:
>   route:
>     if: >-
>       (github.event.comment.user.type || github.event.review.user.type) == 'User' &&
>       startsWith(github.event.comment.body || github.event.review.body, '/') &&
>       github.event.review.state != 'approved' 
>     runs-on: ubuntu-24.04
>     outputs:
>       role: ${{ steps.r.outputs.role }}
>       stage: ${{ steps.r.outputs.stage }}
>       issue: ${{ steps.r.outputs.issue }}
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           persist-credentials: false
>       - id: r
>         env:
>           BODY: ${{ github.event.comment.body || github.event.review.body }}
>           ON_PR: ${{ github.event.issue.pull_request != null || github.event.pull_request != null }}
>           NUMBER: ${{ github.event.issue.number |

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 55,120p .github/workflows/agent.yml; sed -n 220,262p .github/workflows/agent.yml
```

> - uses: actions/checkout@v5
>         with:
>           fetch-depth: 0
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - name: Copy the runtime from main before touching any branch
>         run: mkdir -p /tmp/runtime && cp -r dokima /tmp/runtime/dokima
>       - name: Only a code owner starts an agent
>         env:
>           SENDER: ${{ github.actor }}
>           EVENT: ${{ github.event_name }}
>         run: |
>           # The river's own signal comes from Dokima's bot; everything else needs a code owner.
>           [ "$EVENT" = repository_dispatch ] && [ "$SENDER" = "dokima-runtime[bot]" ] && exit 0
>           python3 -m dokima.plan approvers | tr ',' '\n' | grep -qx "$SENDER" \
>             || { echo "::error title=Not started::$SENDER is not a code owner."; exit 1; }
>       - name: Starting branch
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run: |
>           if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
>             git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
>             if [ "$ROLE" = worker ]; then
>               git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
>             fi
>           elif [ "$ROLE" = planner ]; then
>             git checkout -q -B "try/issue-$N" origin/main
>           else
>             echo "::error title=Nothing to $ROLE::try/issue-$N does not exist; run the

`9. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned four promises: the plan reviewer starts on a split with no try branch, a reviewed split stops for the owner and files nothing before /work, a run that fails before its agent says why on the issue and mentions the owner, and that run still ends as failed.",
          "Wrote one test per promise in tests/test_start.py, running the agent workflow's own steps against a fake GitHub and a fake Claude."],
  "decided": ["Only three start failures are promised: not a code owner, no try branch, no approved plan.",
              "The /work step in commands.yml that files a split's stories is left out, on the reading that no agent starts there."],
  "open": []},
 "verdict": "block",
 "summary": "The split part of the plan is sound and proven, but the start-failure promise covers only three of the failures the owner's words take in, and leaves out a command failure without asking.",
 "blockers": [
  {"id": "B1", "criterion": "176.3", "test": "tests/test_start.py::test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner",
   "problem": "The owner asked that any step that fails before its agent starts says why and stops for the owner. Criterion 3 lists only three failures, and the test proves only those three. The agent workflow has more steps that fail before the agent: copying the runtime, installing pytest and Claude Code, and the check that the pack has everything the role needs. A fix that posts a reason only for the three named failures passes every test, while an incomplete pack still fails as silently as the split did.",
   "evidence": ".github/workflows/agent.yml:111-114 ('Code checks the pack has everything this role needs' exits 1 with 'Incomplete pack') and :104-105 (install step) both run before 'The agent (Claude Code)' at :115; criterion 3 text '(someone who is not a code owner started it, the issue has no try branch, or there is no approved plan to
```

> (Bash completed with no output)

**Agent:** I'm sending the plan for issue #176 back to the planner with two blockers. The review is saved at `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What holds up:** All four new tests in `tests/test_start.py` fail today for the right reason. The plan reviewer stops at "Starting branch" with "try/issue-57 does not exist", and a run that fails before its agent posts nothing on the issue. I also checked that the test setup works: a plan review on an issue that has a try branch already passes through it. It starts the agent, posts one record whose Next line mentions the owner, and doesn't fail. So once the branch problem is fixed, the split promises (176.1 and 176.2) should be properly proven.

**Blockers (both for the planner):**
- **B1 (176.3):** The owner asked that any step failing before its agent starts says why and stops for the owner. The plan promises and tests only three failures: not a code owner, no try branch, no approved plan. Other steps can also fail before the agent:
  - copying the runtime;
  - installing pytest and Claude Code (`agent.yml:104-105`);
  - the check that the pack has everything the role needs (`agent.yml:111-114`).

  A fix that handles only the three named cases would pass every test while those failures stay silent. The fix is to word the promise as every step before the agent and add a test case for one of the later steps, such as the pack check.
- **B2 (176.3):** The owner wrote "a command or step". The plan puts the `/work` step that files a split's stories (in `commands.yml`) out of scope, on the reading that no agent starts there. That's one of two possible readings, and the planner chose it without asking. A failed filing would leave the issue stuck with no message, which is the problem this issue is about. The planner should either ask the owner, or add a promise and test that a failed filing posts the reason and mentions the owner.

**Note:** The plan changes `.github/workflows/agent.yml`. The issue's wording points there, so that's within reach. But the bot can't push workflow changes yet (the approval step for that is still planned), so the owner will probably have to push the worker's change by hand.
