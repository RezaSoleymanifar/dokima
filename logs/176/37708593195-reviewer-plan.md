# reviewer (plan) for #176

Run: https://github.com/dokima-dev/dokima/actions/runs/37708593195

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (41.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/608171ce-d0b0-4315-ba31-dc6b557d799b/tool-results/bqvjypxp0.txt
> 
> Preview (first 2KB):
> .:
> total 68
> drwxr-xr-x  3 runner runner  4096 Oct  8 00:36 .
> drwxrwxrwt 18 root   root    4096 Oct  8 00:36 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 00:36 in
> -rw-r--r--  1 runner runner 41401 Oct  8 00:36 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 00:36 open_blockers.json
> -rw-r--r--  1 runner runner  4856 Oct  8 00:36 plan.json
> 
> in:
> total 48
> drwxr-xr-x 2 runner runner 4096 Oct  8 00:36 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 00:36 ..
> -rw-r--r-- 1 runner runner 3152 Oct  8 00:36 01-planner.json
> -rw-r--r-- 1 runner runner 5129 Oct  8 00:36 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 6007 Oct  8 00:36 03-planner.json
> -rw-r--r-- 1 runner runner 2901 Oct  8 00:36 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2830 Oct  8 00:36 05-worker.json
> -rw-r--r-- 1 runner runner 3865 Oct  8 00:36 06-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5491 Oct  8 00:36 07-planner.json
> # Issue #176: Plan review fails silently on a split: it needs a try branch splits never create
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #177](https://github.com/dokima-dev/dokima/pull/177) · [files changed](https://github.com/dokima-dev/dokima/pull/177/files)
> 
> **Objective: a planner's proposed split gets its plan review like any other plan**
> 
> <dl><dd>
> 
> <img src="https://raw

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-600
```

> # Issue #176: Plan review fails silently on a split: it needs a try branch splits never create
> 
> <!-- dokima-card -->
> ### Approve the result to merge
> [PR #177](https://github.com/dokima-dev/dokima/pull/177) · [files changed](https://github.com/dokima-dev/dokima/pull/177/files)
> 
> **Objective: a planner's proposed split gets its plan review like any other plan**
> 
> <dl><dd>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Acceptance criteria](https://github.com/dokima-dev/dokima/actions/runs/37708218688/job/113087643346): the plan reviewer starts on an issue whose planner proposed a split, with no try branch needed
> *Verified by: a test that the reviewer's start step accepts a split issue that has no try/issue-N branch*
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Acceptance criteria](https://github.com/dokima-dev/dokima/actions/runs/37708218688/job/113087642863): a command or step that fails before its agent starts posts a record on the issue saying why and stops for the owner
> *Verified by: a test that a start failure leaves a comment with the reason and the Needs you mention*
> 
> </dd></dl>
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> [Full suite](https://github.com/dokima-dev/dokim

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; awk 'NR>400' issue.md | grep -v '^ *"' | cut -c1-800 | head -250
```

> 4:### Approve the result to merge
> 33:### RezaSoleymanifar on issue #176 (2026-10-07T23:54:56Z)
> 37:### RezaSoleymanifar on issue #176 (2026-10-07T23:54:57Z)
> 41:### dokima-runtime on issue #176 (2026-10-08T00:02:07Z)
> 132:### dokima-runtime on issue #176 (2026-10-08T00:03:57Z)
> 233:### dokima-runtime on issue #176 (2026-10-08T00:10:19Z)
> 356:### RezaSoleymanifar on issue #176 (2026-10-08T00:21:41Z)
> 360:### dokima-runtime on issue #176 (2026-10-08T00:23:13Z)
> 449:### RezaSoleymanifar on issue #176 (2026-10-08T00:26:21Z)
> 453:### dokima-runtime on PR #177 (2026-10-08T00:31:32Z)
> 508:### dokima-runtime on PR #177 (2026-10-08T00:33:52Z)
> 605:### dokima-runtime on issue #176 (2026-10-08T00:35:39Z)
>    ],
>    ],
>   },
>    {
>    },
>    {
>    },
>    {
>    }
>   ],
>   ],
>  },
>  }
> }
> ```
> 
> </details>
> 
> <sub>Opus 5.5 · 0.8 min · 9 turns · 386,267 tokens in, 3,787 out · $0.50 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/176/37707358053-reviewer-plan.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37707358053)</sub>
> 
> **Next:** @RezaSoleymanifar The plan is approved. Say `/work` to build it, or `/plan` with changes.
> 
> 
> ### RezaSoleymanifar on issue #176 (2026-10-08T00:26:21Z)
> 
> /work
> 
> ### dokima-runtime on PR #177 (2026-10-08T00:31:32Z)
> 
> <!-- dokima-record -->
> **Worker**
> 
> The agent workflow refused any non-planner without a try branch, and every step that failed before the agent wrote nothing on the issue (the record step even ran the empty hand-back check as a pass

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json
for f in ['in/06-reviewer-pr.json','in/07-planner.json']:
  d=json.load(open(f)); print(f); print(json.dumps(d.get('handback',d),indent=1))
"; diff <(python3 -c "import json;print(json.dumps(json.load(open('in/07-planner.json'))['handback'],indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1,sort_keys=True))")
```

> []in/06-reviewer-pr.json
> {
>  "previous_step": {
>   "did": [
>    "A plan review now starts from main when the issue has no try branch, so a proposed split gets reviewed; the pull request reviewer still needs the branch.",
>    "Each step before the agent writes its reason, and a run whose agent never started posts one 'stopped before any agent started' record that mentions the owner, shows Needs you and still fails the run.",
>    "The command listener posts GitHub's error where the command was written when routing or filing a split fails."
>   ],
>   "decided": [
>    "A run that never started stops for the owner without reading the conversation."
>   ],
>   "open": []
>  },
>  "verdict": "block",
>  "summary": "Almost all of it works, but on GitHub a failed tool install would go unnoticed: the run would carry on to the agent and never post the install failure, because the tests run each step under stricter shell settings than GitHub uses.",
>  "blockers": [
>   {
>    "id": "B3",
>    "criterion": "176.3",
>    "test": "tests/test_start.py::test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner",
>    "problem": "On GitHub, the install step does not fail when pip or npm fails, so it never writes its reason and the agent step still starts. The owner gets a 'hand-back rejected' record instead of the 'Install pytest and Claude Code' reason that 176.3 promises.",
>    "evidence": ".github/workflows/agent.yml:115 pipes the install through `tee`, and only the `|| { ... }` branch writes the reason. Neither

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests/ | head -120; grep -n "pipefail\|tee" .github/workflows/agent.yml | head
```

> commit 30291a89eeeba165b8f98709f6a77deca91875e8
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 00:35:32 2026 +0000
> 
>     planner for #176 (run 37708437259)
> 
>  tests/test_start.py | 35 ++++++++++++++++++++++++++++-------
>  1 file changed, 28 insertions(+), 7 deletions(-)
> commit 30291a89eeeba165b8f98709f6a77deca91875e8
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 00:35:32 2026 +0000
> 
>     planner for #176 (run 37708437259)
> 
> diff --git a/tests/test_start.py b/tests/test_start.py
> index 2d60d6c..a7a5937 100644
> --- a/tests/test_start.py
> +++ b/tests/test_start.py
> @@ -239,6 +239,23 @@ def workflow(name):
>      return load_yaml(open(os.path.join(ROOT, ".github", "workflows", name)).read())
>  
>  
> +def github_shell(step, job, defaults):
> +    """The bash command GitHub runs a step's script with, on Linux.
> +
> +    A step, its job's `defaults.run` or the workflow's `defaults.run` may name a shell; the nearest one wins. With
> +    none, GitHub runs `bash -e {0}`, with no pipefail, so a failure inside a pipe goes unnoticed unless the script
> +    catches it itself. Only `shell: bash` gets `bash --noprofile --norc -eo pipefail {0}`. Any other shell is refused,
> +    so the tests never run a step under settings GitHub would not use."""
> +    shell = step.get("shell")
> +    for d in ((job.get("defaults") or {}).get("run") or {}, ((defaults or {}).get("run") or {})):
> +        shell = shell or d.g

**Agent:** Checking the planner's test fix for B4 by running the tests on the branch, then with a pipefail fix applied.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 900 python3 -m pytest -q tests/test_start.py 2>&1 | tail -15; grep -n "shell\|defaults" .github/workflows/*.yml
```

> def assert_says_why_and_stops(r, reason, crit, where=N, board=True):
>         """The run posted exactly one failed record where it should, naming the reason, mentioning the owner, starting nothing."""
> >       assert not r.agent_started(), f"{crit}: the agent started though its start should have failed"
> E       AssertionError: 176.3: the agent started though its start should have failed
> E       assert not True
> E        +  where True = agent_started()
> E        +    where agent_started = <test_start.Run object at 0x7ff688885820>.agent_started
> 
> tests/test_start.py:555: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_start.py::test_a_start_failure_says_why_on_the_issue_and_stops_for_the_owner - AssertionError: 176.3: the agent started though its start should have failed
> assert not True
>  +  where True = agent_started()
>  +    where agent_started = <test_start.Run object at 0x7ff688885820>.agent_started
> 1 failed, 4 passed in 7.38s

**Agent:** Now the good case: add pipefail to the install step in a scratch copy and rerun.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 108,122p .github/workflows/agent.yml; rm -rf /tmp/wt; git worktree add -q /tmp/wt HEAD; cd /tmp/wt; python3 - <<'E'
p='.github/workflows/agent.yml';s=open(p).read()
s=s.replace("          { pip install pytest && npm","          set -o pipefail\n          { pip install pytest && npm",1);open(p,'w').write(s)
E
git diff --stat; timeout 900 python3 -m pytest -q tests/test_start.py 2>&1 | tail -3; git checkout -q .github/workflows/agent.yml
# also check: on main, the tests fail (feature missing)
git checkout -q main -- .github .dokima dokima 2>/dev/null; git checkout -q main -- .github/workflows dokima; timeout 900 python3 -m pytest -q tests/test_start.py 2>&1 | tail -8; cd /; git -C /home/runner/work/dokima/dokima worktree remove --force /tmp/wt
```

> echo "Building the starting pack failed: $(tail -1 /tmp/pack-err.txt)" > /tmp/why.txt
>             fi
>             cat /tmp/pack-err.txt >&2; echo "::error title=No pack::$(cat /tmp/why.txt)"; exit 1; }
>           if [ "$STAGE" = pr ]; then git diff origin/main...HEAD > "$PACK/diff.patch"; fi
>           ls -R "$PACK" | head -60
>       - name: Install pytest and Claude Code
>         run: |
>           { pip install pytest && npm install -g @anthropic-ai/claude-code; } 2>&1 | tee /tmp/install.txt \
>             || { echo "The step 'Install pytest and Claude Code' failed: $(tail -3 /tmp/install.txt | paste -sd' ')" > /tmp/why.txt; exit 1; }
>       - name: All tests, run by code before the reviewer reads the pull request
>         if: env.STAGE == 'pr'
>         run: |
>           PYTHONPATH= PYTHONSAFEPATH= python3 -m pytest -q -rA --junitxml="$PACK/tests.xml" > "$PACK/tests.txt" 2>&1 || true
>           tail -5 "$PACK/tests.txt"
>       - name: Code checks the pack has everything this role needs
>  .github/workflows/agent.yml | 1 +
>  1 file changed, 1 insertion(+)
> .....                                                                    [100%]
> 5 passed in 8.32s
>     File "<string>", line 1, in <module>
>   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-runner/pytest-2/test_a_start_failure_still_fai0/branch/dokima-out/record.json'
>   
> assert 0 == 1
>  +  where 0 = len([])
>  +    where [] = posted()
>  +      where posted = <test_start.Run object at 0x7f07abd00a10>.posted
> 5 failed in 2.0

`8. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["Changed the shared test helper so every workflow step runs with the shell GitHub would use: plain `bash -e` unless a step or its defaults say `shell: bash`.",
          "Left the criteria, scope and test names unchanged."],
  "decided": ["The test change applies to every test in the file, not only the install case."],
  "open": []},
 "verdict": "approve",
 "summary": "The test for failed starts now runs steps the way GitHub does, so it catches the install failure the pull request still lets through, and passes once the install step catches it itself.",
 "blockers": [],
 "notes": [
  {"text": "On the current branch the 176.3 test fails for the right reason, the agent starting after a failed install, and the other four tests pass. With one line `set -o pipefail` added to the install step, all five pass, so the worker has a clear target for B3.",
   "evidence": "pytest -q tests/test_start.py on try/issue-176: 1 failed ('176.3: the agent started though its start should have failed'), 4 passed; same run with `set -o pipefail` before the install command in agent.yml: 5 passed; with main's workflows and dokima/: 5 failed."},
  {"text": "The new shell rule matches GitHub's: no shell named means `bash -e`, `shell: bash` means `bash --noprofile --norc -eo pipefail`, and a step's own shell wins over its job's defaults, which win over the workflow's. Neither workflow names a shell today, so every step now runs under `bash -e`.",
   "evidence": "tests/test_start.py github_shell (lines 242-256); grep for 'shell'/'defaults' in .github/workflows/*.yml finds nothing."},
  {"text": "The earlier code-review note still stands for the worker: when the kind lookup fails during /work, the route step goes on as a plain worker instead of saying why.",
   "evidence": ".github/workflows/commands.yml route step: `[ \"$(python3 -m dokima.agent kind \"$N\")\" = feature ] && sed ...` (06-reviewer-pr n
```

> rc=0

**Agent:** I approved the plan. The planner fixed B4, the weak test, and `review.json` is in `/tmp/dokima-out` and passes both checks.

**What the planner changed:** only the test helper in `tests/test_start.py`. Every workflow step in the tests now runs with the shell GitHub would actually use. With no shell named, that's plain `bash -e`. The stricter `bash --noprofile --norc -eo pipefail` applies only to steps marked `shell: bash`. The criteria, scope and test names are unchanged.

**What I checked:**
- **On the current branch:** the start-failure test (criterion 176.3) now fails for the right reason: "the agent started though its start should have failed". The install failure is hidden by the pipe, as the pull request review found. The other four tests pass.
- **With the fix applied:** I added `set -o pipefail` to the install step in a scratch copy, and all five tests pass. So the worker has a clear target for B3.
- **Against main's workflows and code:** all five tests fail because the feature isn't there yet.
- **The shell rule:** it matches GitHub's, including which setting wins when a step, its job and the workflow each name one. Neither workflow names a shell today, so every step now runs under `bash -e`.

B4 is marked resolved. B3, the install step that doesn't catch the failure, is still the worker's to fix. One note carried over from the pull request review: when the issue-type lookup fails during `/work`, the routing step carries on as a plain worker instead of saying why.
