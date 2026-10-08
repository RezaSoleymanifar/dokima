# reviewer (plan) for #176

Run: https://github.com/dokima-dev/dokima/actions/runs/37707358053

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
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
cd /home/runner/work/dokima/dokima; git diff 9eb599b HEAD --stat; wc -l tests/test_start.py; timeout 600 python -m pytest -q tests/test_start.py 2>&1 | tail -40
```

> tests/test_start.py | 489 +++++++++++++++++++++++++++++++++++-----------------
>  1 file changed, 332 insertions(+), 157 deletions(-)
> 631 tests/test_start.py
>     File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/subprocess.py", line 571, in run
>       raise CalledProcessError(retcode, process.args,
>   subprocess.CalledProcessError: Command '['gh', 'pr', 'view', '60', '-R', 'o/r', '--json', 'headRefName,body']' returned non-zero exit status 1.
>   
> assert 0 == 1
>  +  where 0 = len([])
> FAILED tests/test_start.py::test_a_start_failure_still_fails_the_run - AssertionError: 176.5: the start failure posted 0 comments, expected one:
>   ## run: Starting branch (exit 1)
>   ::error title=Nothing to worker::try/issue-57 does not exist; run the planner first.
>   
>   ## run: Decide what follows, and say it on the card (exit 0)
>   stop
>   Traceback (most recent call last):
>     File "<frozen runpy>", line 198, in _run_module_as_main
>     File "<frozen runpy>", line 88, in _run_code
>     File "/tmp/pytest-of-runner/pytest-0/test_a_start_failure_still_fai0/branch/runtime/dokima/agent.py", line 830, in <module>
>       sys.exit(main(sys.argv))
>                ^^^^^^^^^^^^^^
>     File "/tmp/pytest-of-runner/pytest-0/test_a_start_failure_still_fai0/branch/runtime/dokima/agent.py", line 799, in main
>       step = next_step(items, json.load(open(os.path.join(out, "record.json"))), owners)
>                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>   FileNotFoundError: [Errno 2] No such f

`3. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_start.py 2>&1 | grep -E "^(FAILED|E  )|176\.[0-9]:" | head -30; cat tests/test_start.py
```

> <persisted-output>
> Output too large (37.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6f1b58ae-52b8-48e9-9847-4571ba5a4323/tool-results/byhj1quot.txt
> 
> Preview (first 2KB):
> >       assert r.agent_started(), (f"176.1: the plan reviewer never started on a split with no try/issue-57 branch; "
> E       AssertionError: 176.1: the plan reviewer never started on a split with no try/issue-57 branch; it stopped at 'Starting branch':
> E         ## run: Starting branch (exit 1)
> E         ::error title=Nothing to reviewer::try/issue-57 does not exist; run the planner first.
> E         
> E         ## run: Decide what follows, and say it on the card (exit 0)
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
> E         FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-

`4. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python -m pytest -q tests/test_start.py 2>&1 | grep -E "^FAILED"; sed -n 1,200p tests/test_start.py
```

> FAILED tests/test_start.py::test_the_plan_reviewer_starts_on_a_split_with_no_try_branch - AssertionError: 176.1: the plan reviewer never started on a split with no try/issue-57 branch; it stopped at 'Starting branch':
> FAILED tests/test_start.py::test_a_reviewed_split_stops_for_the_owner_and_files_nothing_before_work - AssertionError: 176.2: the reviewer never reviewed the proposed split; it stopped at 'Starting branch':
> FAILED tests/test_start.py::test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner - AssertionError: 176.3: a failure at 'Only a code owner starts an agent' posted 0 comments, expected one:
> FAILED tests/test_start.py::test_a_failed_command_says_why_and_stops_for_the_owner - AssertionError: 176.4: a failure at 'r' posted 0 comments, expected one:
> FAILED tests/test_start.py::test_a_start_failure_still_fails_the_run - AssertionError: 176.5: the start failure posted 0 comments, expected one:
> """A command either starts its agent or says why on the issue, and a split gets its plan review (#176).
> 
> These tests run the workflows' own steps, read from .github/workflows/agent.yml and commands.yml, the way GitHub runs
> them: each job's and step's `if:` is evaluated, its `${{ }}` expressions filled in, and its script run with bash in a
> clone of a temp git repo whose origin is a local bare repo. Jobs run in the order their `needs` allow, each on its own
> fresh clone and its own /tmp. Nothing leaves the machine: a fake `gh` answers from a fake issue and records eve

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 200,631p tests/test_start.py
```

> l = lines[pos[0]]
>         return seq(indent(l)) if l.lstrip().startswith("- ") else mapping(indent(l))
> 
>     def mapping(at):
>         d = {}
>         while True:
>             skip()
>             if pos[0] >= len(lines):
>                 return d
>             l = lines[pos[0]]
>             if indent(l) != at or l.lstrip().startswith("- "):
>                 return d
>             m = re.match(r"\s*([^\s:][^:]*?):(?:\s+(.*))?$", l)
>             assert m, f"test setup: cannot read workflow line {l!r}"
>             pos[0] += 1
>             d[m.group(1)] = value(m.group(2) or "", at)
> 
>     def seq(at):
>         items = []
>         while True:
>             skip()
>             if pos[0] >= len(lines):
>                 return items
>             l = lines[pos[0]]
>             if indent(l) != at or not l.lstrip().startswith("- "):
>                 return items
>             rest = l[at + 2:]
>             if re.match(r"[^\s:'\"][^:]*:(\s|$)", rest):
>                 lines[pos[0]] = " " * (at + 2) + rest
>                 items.append(mapping(at + 2))
>             else:
>                 pos[0] += 1
>                 items.append(scalar(rest))
> 
>     return node()
> 
> 
> def workflow(name):
>     """One of this repo's workflows, read."""
>     return load_yaml(open(os.path.join(ROOT, ".github", "workflows", name)).read())
> 
> 
> def sh(cwd, *args):
>     """Run git or another command quietly; fail loudly with its output."""
>     p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=git_env(os.environ))
>     assert p.returnco

**Agent:** Still checking the planner's revised tests: all five fail today, and now I'm checking that each one fails for the right reason.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -A25 "176.4: a failure at" /home/runner/.claude/projects/-home-runner-work-dokima-dokima/6f1b58ae-52b8-48e9-9847-4571ba5a4323/tool-results/byhj1quot.txt | head -40; cat -n .github/workflows/commands.yml | sed -n 1,90p
```

> 1	name: commands
>      2	run-name: "${{ github.event.comment.body }}"
>      3	# The listener. A code owner's comment whose first line starts with /plan, /work or /review starts that stage, on the
>      4	# issue or on its pull request, and so does a PR review submitted as a comment or a change request. An Approve never
>      5	# starts anything: it only ever means merge. Everything after the command, and every other comment, review and line
>      6	# note, reaches the agent through its pack. No command, nothing starts; bots never start anything. On an issue
>      7	# /review grades the plan; on a pull request, the work.
>      8	on:
>      9	  issue_comment:
>     10	    types: [created]
>     11	  pull_request_review:
>     12	    types: [submitted]
>     13	permissions:
>     14	  contents: read
>     15	  issues: read
>     16	  pull-requests: read
>     17	  actions: read
>     18	jobs:
>     19	  route:
>     20	    if: >-
>     21	      (github.event.comment.user.type || github.event.review.user.type) == 'User' &&
>     22	      startsWith(github.event.comment.body || github.event.review.body, '/') &&
>     23	      github.event.review.state != 'approved' 
>     24	    runs-on: ubuntu-24.04
>     25	    outputs:
>     26	      role: ${{ steps.r.outputs.role }}
>     27	      stage: ${{ steps.r.outputs.stage }}
>     28	      issue: ${{ steps.r.outputs.issue }}
>     29	    steps:
>     30	      - uses: actions/checkout@v5
>     31	        with:
>     32	          persist-credentials: false
>     33	      - id: r
>     34	       

`7. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/probe && cat > /tmp/probe/p.py <<'EOF'
import sys, pathlib, tempfile
sys.path.insert(0, "tests"); sys.path.insert(0, ".")
import test_start as T
from dokima import agent
d = pathlib.Path(tempfile.mkdtemp())
r = T.Run(d/"good", "reviewer", "plan", T.STORY_PLANNED, try_branch=True)
print("good", r.agent_started(), r.failed, [(x["role"], x["check"]["passed"]) for x in agent.records([{"author":{"login":agent.BOT},"body":p["body"]} for p in r.posted()])])
r = T.Listener(d/"filed", "/work", T.SPLIT_APPROVED)
print("filed", r.failed, r.results, len(r.posted()), r.created_issues()[:1]); print(r.tail()[-800:] if r.failed else "")
r = T.Listener(d/"plan", "/plan", T.STORY_PLANNED)
print("plan", r.failed, r.agent_run_started(), r.posted())
r = T.Listener(d/"str", "/plan", T.STORY_PLANNED, actor="stranger")
print("stranger", r.failed, r.agent_run_started(), r.posted())
r = T.Listener(d/"route", "/review", T.SPLIT_APPROVED, on_pr=True, gh_fail="pr view|GraphQL: gone")
print("route", r.failed, r.failed_step, r.results)
r = T.Listener(d/"split", "/work", T.SPLIT_APPROVED, gh_fail="issue create|HTTP 403")
print("splitfail", r.failed, r.failed_step, r.results)
r = T.Run(d/"inst", "worker", "", T.STORY_APPROVED, try_branch=True, broken={"pip": T.PIP_BROKEN})
print("install", r.failed_step)
r = T.Run(d/"chk", "worker", "", T.SPLIT_APPROVED+[T.owner_comment("/work","2026-10-07T10:30:00Z")], try_branch=True)
print("check", r.failed_step); print(r.tail()[:600])
EOF
python /tmp/probe/p.py 2>&1 | tail -40
```

> good True False [('reviewer', True)]
> filed False {'route': 'success', 'split': 'success', 'run': 'skipped'} 1 [['issue', 'create', '-R', 'o/r', '--title', 'First', '--body', '<!-- dokima-card -->\n<!-- /dokima-card -->\n\n<details open><summary>From the approved plan of #57, story 1</summary>\n\n**Part of:** #57 Stuck issue\n\n**User story:** u1\n\n**Acceptance criteria:**\n- a ([source](https://github.com/o/r/issues/57))\n\n</details>\n']]
> 
> plan False True []
> stranger False False []
> route True r {'route': 'failure', 'split': 'skipped', 'run': 'skipped'}
> splitfail True File the approved split's stories as sub-issues {'route': 'success', 'split': 'failure', 'run': 'skipped'}
> install Install pytest and Claude Code
> check Code checks the pack has everything this role needs
> ## run: Code checks the pack has everything this role needs (exit 1)
> ::error title=Incomplete pack::plan.json is a split: /work files its stories as sub-issues, no worker builds it
> 
> ## run: Decide what follows, and say it on the card (exit 0)
> stop
> Traceback (most recent call last):
>   File "<frozen runpy>", line 198, in _run_module_as_main
>   File "<frozen runpy>", line 88, in _run_code
>   File "/tmp/tmpk7cg5gvv/chk/runtime/dokima/agent.py", line 830, in <module>
>     sys.exit(main(sys.argv))
>              ^^^^^^^^^^^^^^
>   File "/tmp/tmpk7cg5gvv/chk/runtime/dokima/agent.py", line 799, in main
>     s

`8. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Widened the promise about failed starts to every step before the agent, and added an install failure, an incomplete pack and a run that starts normally to its test.",
          "Added a promise that a code owner's command that fails in the listener (it cannot be routed, or a split's stories cannot be filed) says why where it was written and mentions the owner, with commands.yml in scope.",
          "Asked the owner whether 'command' also covers the listener, and planned for yes."],
  "decided": ["A comment from someone who is not a code owner still gets no reply.", "A failed listener command does not move the board card."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now covers every step that can fail before an agent starts and the listener's own failures, as the owner confirmed with 'yes, cover both', and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [
  {"text": "Criterion 176.2 (child issues only after /work) comes from the owner's comment on how a split should go, but its source points at the issue itself; the link would be more exact if it pointed to that comment.",
   "evidence": "plan.json acceptance_criteria[1].source; owner comment of 2026-10-07T23:54:56Z on #176."},
  {"text": "All five tests fail today for the right reason, and their good cases already pass: a plan review with a try branch posts only its own record, a split files fine, the owner's /plan starts the planner, a stranger's /plan gets no reply. The failure cases stop at the intended steps ('Starting branch', 'Install pytest and Claude Code', the pack check with 'plan.json is a split', the route step, the split filing step) and post nothing.",
   "evidence": "pytest -q tests/test_start.py: 5 failed (e.g. '176.4: a failure at 'r' posted 0 comments, expected one'); a probe script running the Run and Listener cases from tests/test_start.py
```

> rc=0

**Agent:** I approved the revised plan for #176. Both blockers from the last round (B1 and B2) are resolved, and the hand-back is in `/tmp/dokima-out/review.json`. Both required checks on it passed.

- **B1 (only three start failures were promised):** criterion 176.3 now covers every step that can fail before the agent starts. Its test adds two new failures: the tools failing to install, and the pack check finding a split. It also adds a run that starts normally and must post only its own record.
- **B2 (a reading of "command" picked without asking):** the planner asked which reading you meant. It planned for the broader one in a new criterion 176.4, which adds `commands.yml` to the scope. Your reply "/review yes, cover both" picks that same reading.
- **Tests:** all five new tests in `tests/test_start.py` fail today, and each fails because the feature is missing, not because the test is broken. Each failure case stops at the step it is meant to and posts nothing. The cases that should keep working (a normal plan review, a split that files fine, your `/plan`, a stranger's `/plan`) already pass today.

I left three notes, none of them blocking:
- Criterion 176.2 says no child issue is filed until your `/work`. It cites the issue as its source, but that rule comes from your comment on how a split should go, so a link to that comment would be more exact.
- The second note records the test results above.
- The fix changes `agent.yml` and `commands.yml`, and the bot can't push workflow files, so you will probably have to push the worker's change yourself.
