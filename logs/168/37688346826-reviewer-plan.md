# reviewer (plan) for #168

Run: https://github.com/dokima-dev/dokima/actions/runs/37688346826

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; echo ----; cat open_blockers.json; echo ----; cat plan.json
```

> <persisted-output>
> Output too large (66.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/79f16f87-41e5-485e-a026-ad76527cc33c/tool-results/bk6w7kckx.txt
> 
> Preview (first 2KB):
> .:
> total 84
> drwxr-xr-x  3 runner runner  4096 Oct  7 21:17 .
> drwxrwxrwt 18 root   root    4096 Oct  7 21:17 ..
> drwxr-xr-x  2 runner runner  4096 Oct  7 21:17 in
> -rw-r--r--  1 runner runner 59474 Oct  7 21:17 issue.md
> -rw-r--r--  1 runner runner  1329 Oct  7 21:17 open_blockers.json
> -rw-r--r--  1 runner runner  6501 Oct  7 21:17 plan.json
> 
> in:
> total 72
> drwxr-xr-x 2 runner runner 4096 Oct  7 21:17 .
> drwxr-xr-x 3 runner runner 4096 Oct  7 21:17 ..
> -rw-r--r-- 1 runner runner 5423 Oct  7 21:17 01-planner.json
> -rw-r--r-- 1 runner runner 5165 Oct  7 21:17 02-planner.json
> -rw-r--r-- 1 runner runner 3834 Oct  7 21:17 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 5953 Oct  7 21:17 04-planner.json
> -rw-r--r-- 1 runner runner 2239 Oct  7 21:17 05-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2412 Oct  7 21:17 06-worker.json
> -rw-r--r-- 1 runner runner 2781 Oct  7 21:17 07-reviewer-pr.json
> -rw-r--r-- 1 runner runner 6512 Oct  7 21:17 08-planner.json
> -rw-r--r-- 1 runner runner 4121 Oct  7 21:17 09-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7134 Oct  7 21:17 10-planner.json
> # Issue #168: Merge check reads the criteria from the approved plan, not the issue text
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #171](https://github.com/dokima-dev/dokima/pull/171) · [files changed](

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> # Issue #168: Merge check reads the criteria from the approved plan, not the issue text
> 
> <!-- dokima-card -->
> ### Checks failing
> [PR #171](https://github.com/dokima-dev/dokima/pull/171) · [files changed](https://github.com/dokima-dev/dokima/pull/171/files)
> 
> This issue has no objective and acceptance criteria yet.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> [Full suite](https://github.com/dokima-dev/dokima/actions/runs/37687934901/job/113020461663)
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
> Pull requests from the new flow pass the merge check on their own proof, so the owner no lon

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; cat open_blockers.json; for f in in/07* in/09* in/10*; do echo "== $f"; python3 -c "import json,sys;d=json.load(open('$f'));print(json.dumps(d.get('handback',d),indent=1)[:6000])"; done
```

> 4:### Checks failing
> 19:### RezaSoleymanifar on issue #168 (2026-10-07T19:16:59Z)
> 24:### dokima-runtime on issue #168 (2026-10-07T19:20:55Z)
> 133:### RezaSoleymanifar on issue #168 (2026-10-07T20:21:24Z)
> 137:### dokima-runtime on issue #168 (2026-10-07T20:22:43Z)
> 241:### dokima-runtime on issue #168 (2026-10-07T20:24:09Z)
> 343:### dokima-runtime on issue #168 (2026-10-07T20:25:59Z)
> 453:### dokima-runtime on issue #168 (2026-10-07T20:27:02Z)
> 541:### RezaSoleymanifar on issue #168 (2026-10-07T20:46:20Z)
> 545:### dokima-runtime on PR #171 (2026-10-07T20:48:16Z)
> 599:### dokima-runtime on PR #171 (2026-10-07T20:50:38Z)
> 688:### RezaSoleymanifar on issue #168 (2026-10-07T21:10:36Z)
> 692:### dokima-runtime on issue #168 (2026-10-07T21:14:10Z)
> 807:### dokima-runtime on issue #168 (2026-10-07T21:15:54Z)
> 902:### dokima-runtime on issue #168 (2026-10-07T21:17:26Z)
> [
>  {
>   "id": "B2",
>   "criterion": "168.5",
>   "test": "tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code",
>   "problem": "168.5 promises the merge check asks for no write permission. The test only looks for a line that says 'write'; a workflow with no permissions list at all passes. On pull_request_target the token then gets the repository's default permissions, which can be read and write, while the job runs the pull request's own tests and setup files (and actions/checkout leaves the token in the checkout). That is the exact hole moving to pull_request_target opens, and the test would

`4. Bash`
```
cd /tmp/pack; sed -n 541,545p issue.md; sed -n 688,692p issue.md; python3 -c "import json;d=json.load(open('in/10-planner.json'));print(json.dumps(d['handback']['replies'],indent=1))"; diff <(python3 -c "import json;print(json.dumps(json.load(open('in/10-planner.json'))['handback'],indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('plan.json')),indent=1,sort_keys=True))"); cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40
```

> ### RezaSoleymanifar on issue #168 (2026-10-07T20:46:20Z)
> 
> /work
> 
> ### dokima-runtime on PR #171 (2026-10-07T20:48:16Z)
> ### RezaSoleymanifar on issue #168 (2026-10-07T21:10:36Z)
> 
> /plan fold in the hole the reviewer found on #171. The merge check has to run main's code, not the pull request's, so a pull request can never change the check that judges it.
> 
> ### dokima-runtime on issue #168 (2026-10-07T21:14:10Z)
> [
>  {
>   "blocker": "B2",
>   "answer": "fixed",
>   "why": "The 168.5 test now also requires a top-level permissions list of only read or none (read-all or {} also count) and fails any job whose own permissions ask for more, with \"168.5: the merge check does not limit its token to read, so the pull request's tests could get write access\". Checked on a copy: a correct pull_request_target workflow passes; the same with no permissions list, with write-all, or with a job asking contents: write each fails."
>  }
> ]
> commit fe613539223b2b8638aab6a2e0cd2b0931236f41
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:17:18 2026 +0000
> 
>     planner for #168 (run 37688166302)
> 
>  tests/test_merge_check.py | 19 ++++++++++++++++++-
>  1 file changed, 18 insertions(+), 1 deletion(-)
> 
> commit 34e9ff3ecad2160c19c26dcb5ffbe01c732e46d6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:14:00 2026 +0000
> 
>     planner for #168 (run 37687521078)
> 
>  tests/test_merge_check.py | 71 +++++++++++++++++++++

**Agent:** Plan matches the newest planner record. Now the test itself.

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show fe61353 -- tests/test_merge_check.py; grep -n "def test_the_merge_check_runs_mains" -A95 tests/test_merge_check.py; cat .github/workflows/done-whens.yml
```

> commit fe613539223b2b8638aab6a2e0cd2b0931236f41
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Wed Oct 7 21:17:18 2026 +0000
> 
>     planner for #168 (run 37688166302)
> 
> diff --git a/tests/test_merge_check.py b/tests/test_merge_check.py
> index 9e47d0d..54cf5ae 100644
> --- a/tests/test_merge_check.py
> +++ b/tests/test_merge_check.py
> @@ -251,6 +251,14 @@ def folder(path):
>      return (path or ".").strip().rstrip("/").removeprefix("./") or "."
>  
>  
> +def permissions_read_only(inline, block):
> +    """Whether a `permissions:` setting grants only read or none: `read-all`, `{}`, or a list of read/none entries."""
> +    if inline:
> +        return inline in ("read-all", "{}")
> +    entries = [line.split(":", 1) for line in block.splitlines() if line.strip() and not line.strip().startswith("#")]
> +    return bool(entries) and all(len(e) == 2 and e[1].split("#")[0].strip() in ("read", "none") for e in entries)
> +
> +
>  def test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code(record_property):
>      """The merge check runs main's own copy of its workflow and of Dokima's code; only the tests come from the pull request.
>  
> @@ -259,7 +267,9 @@ def test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code(recor
>      folder as the pull request's; every other checkout is main's. Every `python3 -m dokima` step must run in one of
>      main's folders, with no PYTHONPATH of its own, and the step that runs pytest must run in the pull reques

`6. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_merge_check.py 2>&1 | tail -5; pytest -q 2>&1 | tail -3
rm -rf /tmp/mut && cp -r . /tmp/mut && cd /tmp/mut && cat > /tmp/good.yml <<'EOF'
name: done-whens
on:
  pull_request_target:
permissions:
  contents: read
  issues: read
  pull-requests: read
jobs:
  list:
    name: list done-whens
    runs-on: ubuntu-24.04
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
    steps:
      - uses: actions/checkout@v5
      - id: m
        env:
          GH_TOKEN: ${{ github.token }}
        run: python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"

  check:
    needs: list
    name: ${{ matrix.name }}
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v5
        with:
          path: main
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          path: pr
      - name: Run
        working-directory: pr
        run: |
          pytest -rA --junitxml=r.xml $TESTS
      - name: Annotate
        working-directory: main
        run: python3 -m dokima.checks annotate ../pr/r.xml
EOF
t(){ cp "$1" .github/workflows/done-whens.yml; echo "== $2: $(pytest -q tests/test_merge_check.py -k mains_code 2>&1 | grep -E 'passed|failed|AssertionError: 168' | head -2 | tr '\n' ' ')"; }
t /tmp/good.yml good
sed '/^permissions:/,/pull-requests: read/d' /tmp/good.yml > /tmp/m1.yml; t /tmp/m1.yml no-perms
sed 's/^permissions:/permissions: write-all\nxpermissions:/' /tmp/good.yml | sed '/^xpermissions:/,/pull-requests: read/d' > /tmp/m2.yml; t /tmp/m2.yml write-all
sed 's/^  check:/  check:\n    permissions:\n      contents: write/' /tmp/good.yml > /tmp/m3.yml; t /tmp/m3.yml job-write
sed 's/^  check:/  check:\n    permissions: write-all/' /tmp/good.yml > /tmp/m4.yml; t /tmp/m4.yml job-write-all
sed 's/^permissions:/permissions:\n  actions: read/; s/  contents: read/  contents: none/' /tmp/good.yml > /tmp/m5.yml; t /tmp/m5.yml read-none-mix
sed '/^permissions:/,/pull-r
```

> FAILED tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code - AssertionError: 168.5: the merge check is not triggered by pull_request_target, so GitHub runs the pull request's copy of it
> assert None
>  +  where None = <function search at 0x7fb25a9e0860>('(?m)^  pull_request_target:', '  pull_request:\n')
>  +    where <function search at 0x7fb25a9e0860> = re.search
> 1 failed, 6 passed in 1.99s
>  +  where None = <function search at 0x7f5b70fe4860>('(?m)^  pull_request_target:', '  pull_request:\n')
>  +    where <function search at 0x7f5b70fe4860> = re.search
> 1 failed, 183 passed in 5.52s
> == good: 1 passed, 6 deselected in 0.05s 
> == no-perms: E       AssertionError: 168.5: the merge check does not limit its token to read, so the pull request's tests could get write access FAILED tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code - AssertionError: 168.5: the merge check does not limit its token to read, so the pull request's tests could get write access 
> == write-all: E       AssertionError: 168.5: the merge check does not limit its token to read, so the pull request's tests could get write access FAILED tests/test_merge_check.py::test_the_merge_check_runs_mains_code_and_judges_the_pull_requests_code - AssertionError: 168.5: the merge check does not limit its token to read, so the pull request's tests could get write access 
> == job-write: E       AssertionError: 168.5: the merge check runs the p

`7. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "Made the 168.5 test also require the merge check to limit its token to read or none, both for the whole workflow and for each job, so a workflow with no permissions list or one asking to write now fails."
  ],
  "decided": [
   "Kept the rest of the plan as it was: five criteria, with only dokima/checks.py and the done-whens workflow in scope."
  ],
  "open": [
   "Pull request #171 is judged by main's old merge check once the workflow moves to main's copy, so the owner must override it one last time."
  ]
 },
 "verdict": "approve",
 "summary": "The plan now proves every part of the owner's ask, including that the merge check runs main's code with a read-only token; each test fails for the right reason when the behavior is missing, and the earlier blocker is fixed.",
 "blockers": [],
 "notes": [
  {
   "text": "B2 checked on a copy of the repo: a correct pull_request_target workflow with a read-only permissions list passes the 168.5 test; the same workflow with no permissions list, with write-all, or with a job asking for contents: write or write-all each fails with a 168.5 message.",
   "evidence": "/tmp/mut with done-whens.yml swapped in: `pytest -q tests/test_merge_check.py -k mains_code` gives 1 passed for good, read-all, read/none mix and a job set to read; failed for no-perms, write-all, job-write, job-write-all."
  },
  {
   "text": "On this branch the 168.5 test fails for the right reason (the workflow still runs on pull_request); the six 168.1 to 168.4 tests already pass with the worker's earlier code.",
   "evidence": "pytest -q tests/test_merge_check.py: 1 failed (168.5: not triggered by pull_request_target), 6 passed; full suite 183 passed, 1 failed."
  },
  {
   "text": "The bot cannot push workflow changes and the pause for workflow changes is still planned, so the owner may need to push or approve the done-whens.yml change by hand.",
   "evidence
```

> rc=0

**Agent:** I approved the plan for #168. Both hand-back checks passed, and the review is in `/tmp/dokima-out/review.json`.

- **Earlier blocker B2 is fixed.** The test for 168.5 now requires the merge check to limit its access token to read or none, for the whole workflow and for each job. I checked this on a copy of the repo by swapping in different versions of the workflow file `done-whens.yml`:
  - A correct version passes, and so do versions using `read-all`, a mix of read and none, or a job set to read.
  - The test fails, with a 168.5 message, when the permissions list is missing, when it says `write-all`, or when a job asks for `contents: write` or `write-all`.
- **The new test fails today for the right reason.** On this branch the 168.5 test fails because the workflow still runs on `pull_request`. The six tests for 168.1 to 168.4 already pass with the worker's earlier code. The full suite gives 183 passed and 1 failed (that 168.5 test).
- **No owner request is left undone.** The owner asked on 21:10 for the merge check to run main's code, not the pull request's. The plan's criterion 168.5 and its test cover that.

Two things for the owner, both noted in the review:
- **Workflow push:** the bot can't push workflow changes, and the pause for those is still planned. The owner may need to push or approve the `done-whens.yml` change by hand.
- **One last override:** PR #171 will be judged by main's old merge check, which still reads the issue text, so it needs the owner's override one more time. The planner raised this itself.
