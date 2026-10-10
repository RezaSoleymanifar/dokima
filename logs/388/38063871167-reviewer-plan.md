# reviewer (plan) for #388

Run: https://github.com/dokima-dev/dokima/actions/runs/38063871167

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #388: In the merge queue, a pull request's own copy of the checks judges it
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/388
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Filed by Dokima from issues its agents raised during their runs and nobody filed. It goes to the backlog; nothing starts until the owner decides.
> 
> - Raised by the reviewer on #270 (2026-10-08, [record](https://github.com/dokima-dev/dokima/pull/270#issuecomment-6069383274)): **In the merge queue, a pull request's own copy of the checks judges it**. On the merge queue's event GitHub runs the workflow files from the queued commit, and done-whens' first checkout (Dokima's code) is the queued commit too. A pull request that edits done-whens.yml, full-suite.yml or dokima/checks.py would be judged in the queue by its own edited copy, which is what #263 closed for pull requests.
>   Evidence: .github/workflows/done-whens.yml: the `list` job's `actions/checkout@v5` has no `ref:`, so on merge_group it checks out github.sha, the queued commit; the workflow header says 'Runs main's copy of this workflow and of Dokima's code'.
> 
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/no

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/done-whens.yml; cat tests/test_queue_judge.py; git show --stat HEAD
```

> name: done-whens
> # One GitHub check per criterion of the PR's approved plan, plus one gate check.
> # Runs main's copy of this workflow and of Dokima's code; only the tests, and the code they judge, come from the PR.
> # In the merge queue they come from the queued commit: the PR on top of the latest main.
> on:
>   pull_request_target:
>   merge_group:
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
>           ref: ${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha }}
>           path: pr
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - name: Run this done-when's tests
>         working-directory: pr
>         env:
>           TESTS: ${{ matrix.tests }}
>           ID: ${{ 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_queue_judge.py 2>&1 | grep -E "^E   |388\.|passed|failed" | head -20
```

> Proves 388.1. Queues a pull request whose dokima/checks.py was edited, runs every job of done-whens.yml on the merge queue's
>         record_property("proves", "388.1")
> >           assert not theirs, (f"388.1: on {event} the pull request's own copy of dokima/checks.py ran "
> E           AssertionError: 388.1: on merge_group the pull request's own copy of dokima/checks.py ran (queued matrix), so it judges itself:
> E             --- list : success
> E             checkout (no ref) -> queued into .
> E             $ python3 -m dokima.checks matrix >> "$GITHUB_OUTPUT"
> E             
> E             --- check text-only: success
> E             checkout (no ref) -> queued into .
> E             checkout 2222222222222222222222222222222222222222 -> queued into pr
> E             $ pip install -q pytest
> E             
> E             $ if [ "$ID" = "text-only" ] && [ -z "$TESTS" ]; then echo "::notice title=Text only::Only text files changed: no plan or tests needed."; exit 0; fi
> E             if [ -z "$TESTS" ]; then echo "::error title=$ID has no test::No test verifies this done-when yet."; exit 1; fi
> E             pytest -rA -p no:cacheprovider -o junit_family=xunit1 --junitxml=r.xml $TESTS
> E             ::notice title=Text only::Only text files changed: no plan or tests needed.
> E             
> E             --- gate : success
> E             $ if [ -z "$MATRIX" ] || [ "$MATRIX" = "[]" ]; then

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_queue_judge.py 2>&1 | grep -E "^E   .*388|passed|failed" | head -20
```

> E           AssertionError: 388.1: on merge_group the pull request's own copy of dokima/checks.py ran (queued matrix), so it judges itself:
>             passed, _, logs = queue(tmp_path / f"{event}-good", event, APP_GOOD)
>             assert passed, f"388.2: on {event} a pull request with working code did not pass its done-whens:\n{logs}"
>             passed, ran, logs = queue(tmp_path / f"{event}-bad", event, APP_BAD)
> >           assert not passed, (f"388.2: on {event} a pull request with broken code that edits dokima/checks.py passed "
> E           AssertionError: 388.2: on merge_group a pull request with broken code that edits dokima/checks.py passed its done-whens (copies that ran: queued matrix):
> FAILED tests/test_queue_judge.py::test_the_queue_still_tests_the_queued_commits_code - AssertionError: 388.2: on merge_group a pull request with broken code that edits dokima/checks.py passed its done-whens (copies that ran: queued matrix):
> 2 failed in 0.17s

`5. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && python3 - <<'E'
p='.github/workflows/done-whens.yml'
s=open(p).read()
s=s.replace("""      - uses: actions/checkout@v5
      - id: m""","""      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.merge_group.base_sha }}
      - id: m""")
s=s.replace("""      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses""","""      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.merge_group.base_sha }}
          persist-credentials: false
      - uses""")
open(p,'w').write(s)
E
python -m pytest -q tests/test_queue_judge.py 2>&1 | tail -2
sed -i 's/merge_group.base_sha }}/merge_group.base_ref }}/' .github/workflows/done-whens.yml; python -m pytest -q tests/test_queue_judge.py 2>&1 | tail -2
```

> ..                                                                       [100%]
> 2 passed in 1.68s
> ..                                                                       [100%]
> 2 passed in 1.58s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The plan's two new tests fail today for the right reason, but a wrong fix can pass the first one. Writing the review now.

`6. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner wrote two criteria: in the merge queue main's copy of dokima/checks.py lists and annotates the checks, and the queued commit's tests still decide pass or fail.",
          "It added tests/test_queue_judge.py, which runs every job of done-whens.yml on the merge queue's event and on the pull request's event."],
  "decided": ["Only done-whens.yml changes; full-suite.yml stays as it is because it runs no Dokima code."],
  "open": ["It asks the owner whether leaving a pull request's own edits to the workflow files to the owner's approval is enough, or whether a repo setting that requires main's workflows should be its own issue."]},
 "verdict": "block",
 "summary": "The plan is right, but its test for 388.1 also passes when the queue checks out the commit queued ahead of this pull request instead of main, so another pull request's edited dokima/checks.py could still judge this one.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "388.1",
   "text": "388.1 promises that main's copy of Dokima's code makes the check list in the merge queue. In the test, the merge queue event's base_sha is main's own commit, and tree_for() maps it to main's tree. On GitHub, base_sha is the parent of the queued commit: when another pull request is ahead in the queue, that parent is the other pull request's queued commit, not main. So a fix that checks out `github.event.merge_group.base_sha` passes both tests, yet in a queue of two it would let the first pull request's edited dokima/checks.py list the second one's checks. Smallest fix: in the merge_group case give the event a base_sha for a fourth tree, a pull request queued ahead whose dokima/checks.py is also edited (and a head_ref built on it), so only a checkout of main (`main`, `refs/heads/main` or base_ref) resolves to main's tree, and assert that copy never ran.",
   "evidence": "tests/test_queue_judge.py context
```

> Exit code 1
> summary holds 38 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`7. Bash`
```
python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The test for 388.1 also passes when the queue uses the commit queued ahead instead of main, so another pull request could judge this one."
json.dump(d,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 388 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#388](https://github.com/dokima-dev/dokima/issues/388) (the merge queue lets a pull request be judged by its own copy of the checks). It goes back to the planner for one test fix.

**What holds up:** both criteria come from the issue. Both new tests fail today, and for the right reason: in the queue, the queued commit's own `dokima/checks.py` makes the check list. A pull request with broken code that also edits that file to list one always-passing check gets through.

**The blocker (388.1):** the test lets a wrong fix pass. In the test's fake queue, the commit the queued pull request sits on is always main itself. On GitHub, when another pull request is ahead in the queue, that commit is the other pull request's queued commit, not main. I made the wrong fix in a scratch copy of the repo: pointing the workflow at that commit. Both tests reported "2 passed". With that fix, the first pull request's edited `dokima/checks.py` could list the second one's checks. The smallest fix I proposed is to give the test a pull request queued ahead, with its own edited `dokima/checks.py`. Then only a checkout of main passes, and the test also checks that the other pull request's copy never ran.

**Still waiting for you:** the planner's question about the workflow files. This issue isn't on autopilot, so I left it for you to answer. A pull request that edits `done-whens.yml` or `full-suite.yml` is still judged in the queue by its own copy, and code alone can't change that. You can either rely on your approval of every workflow change, or open a separate issue for a repo setting that makes these workflows run from main.

The hand-back is in `/tmp/dokima-out/review.json` and passes both of Dokima's checks.
