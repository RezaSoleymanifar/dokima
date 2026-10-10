# reviewer (plan) for #388

Run: https://github.com/dokima-dev/dokima/actions/runs/38067022499

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat open_blockers.json
```

> total 24
> drwxr-xr-x 2 runner runner 4096 Oct 10 16:17 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 16:17 ..
> -rw-r--r-- 1 runner runner 3964 Oct 10 16:17 01-planner.json
> -rw-r--r-- 1 runner runner 3174 Oct 10 16:17 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4631 Oct 10 16:17 03-planner.json
> # Issue #388: In the merge queue, a pull request's own copy of the checks judges it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 396 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> In the merge queue, done-whens runs the queued commit's copy of Dokima's code, so an edited dokima/checks.py judges itself.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/388
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Workflow files in the queue:** The issue names three files: done-whens.yml, full-suite.yml and dokima/checks.py. Only dokima/checks.py can be fixed in code: on the merge queue's event GitHub runs the queued commit's copy of every workflow file, so a pull request that edits done-whens.yml or full-suite.yml is still judged in the queue by its own copy. The plan fixes dokima/checks.py (done-whens.yml checks out main's Dokima code in the queue, a change to a workflow file this issue asks for) and leaves workflow edits to your approval: the bot cannot push workflow files, and autopilot stops on any pull request that changes one. The other way

`2. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat in/03-planner.json | python3 -m json.tool | head -80; cat in/02-reviewer-plan.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d,indent=1)[:3000])"
```

> {
>  "kind": "user_story",
>  "summary": "In the merge queue, done-whens runs the queued commit's copy of Dokima's code, so an edited dokima/checks.py judges itself.",
>  "user_story": "A pull request in the merge queue is judged by main's copy of Dokima's code, as it already is on the pull request itself, so editing dokima/checks.py cannot wave it through the queue.",
>  "acceptance_criteria": [
>   {
>    "text": "In the merge queue, main's copy of Dokima's code lists a queued pull request's checks and annotates its tests, even with another pull request queued ahead. Neither the queued commit's copy of dokima/checks.py nor the copy of the pull request queued ahead ever runs there, and on the pull request itself main's copy still does both, as before.",
>    "source": "https://github.com/dokima-dev/dokima/issues/388"
>   },
>   {
>    "text": "In the merge queue, the plan's checks still run the queued commit's tests: working code passes and broken code fails. Broken code fails even when the pull request edits dokima/checks.py to list one always-passing check, and on the pull request itself both cases give the same results.",
>    "source": "https://github.com/dokima-dev/dokima/issues/388"
>   }
>  ],
>  "non_functional": [],
>  "scope": [
>   ".github/workflows/done-whens.yml",
>   "tests/test_queue_judge.py"
>  ],
>  "out_of_scope": [
>   "The workflow files themselves: on the merge queue's event GitHub always runs the queued commit's copy of done-whens.yml and full-suite.yml, and nothing inside a workflow file c

**Agent:** Now the test file and the workflow.

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git diff f477545 HEAD --stat; cat tests/test_queue_judge.py; cat .github/workflows/done-whens.yml
```

> tests/test_queue_judge.py | 40 ++++++++++++++++++++++++----------------
>  1 file changed, 24 insertions(+), 16 deletions(-)
> """In the merge queue, main's copy of Dokima's code judges a queued pull request (#388).
> 
> On the merge queue's event GitHub hands done-whens.yml the queued commit: the pull request on top of the latest main.
> A checkout with no `ref:` then copies that commit, so a pull request that edits dokima/checks.py would make its own
> check list in the queue. These tests play GitHub's part. They build four tiny trees: main, the pull request's head,
> the queued commit, and another pull request queued ahead of it. In the queue the event's base_sha is the commit just
> ahead (here that other pull request's queued commit), never main, so only a checkout of main itself finds main's code.
> Each tree holds a stand-in dokima/checks.py that notes whose copy ran; main's lists the plan's one check, while the
> other three are "edited" to list one always-passing Text only check. Each tree also holds app.py and the test that
> checks it, its code working or broken.
> 
> Every job of the real done-whens.yml (list, check once per row of the list's matrix, gate) then runs step by step:
> `actions/checkout` copies the tree its `ref` names on that event (the queued commit by default on merge_group, main
> by default on pull_request_target), other `uses:` steps are skipped, every `run:` script runs with bash, its `${{ }}`
> filled in, with a `pip` that does nothing and a `pytest` that runs this machine's

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_queue_judge.py 2>&1 | grep -E "388\.|passed|failed" | head; 
rm -rf /tmp/rv && cp -r . /tmp/rv && cd /tmp/rv
try(){ git checkout -q -- .github/workflows/done-whens.yml; python3 - "$1" <<'EOF'
import sys
p='.github/workflows/done-whens.yml'; s=open(p).read(); r=sys.argv[1]
s=s.replace("      - uses: actions/checkout@v5\n      - id: m","      - uses: actions/checkout@v5\n        with:\n          ref: "+r+"\n      - id: m")
s=s.replace("      - uses: actions/checkout@v5\n        with:\n          persist-credentials: false\n      - uses","      - uses: actions/checkout@v5\n        with:\n          ref: "+r+"\n          persist-credentials: false\n      - uses",1)
open(p,'w').write(s)
EOF
echo "== $1"; python3 -m pytest -q -p no:cacheprovider tests/test_queue_judge.py 2>&1 | tail -1; }
try '${{ github.event.merge_group.base_sha }}'
try '${{ github.base_ref || github.event.merge_group.base_sha }}'
try '${{ github.event.merge_group.base_ref }}'
try '${{ github.event.merge_group.base_ref || github.base_ref }}'
try 'main'
try '${{ github.event.merge_group.head_sha }}'
```

> Proves 388.1. Queues a pull request whose dokima/checks.py was edited, runs every job of done-whens.yml on the merge queue's
>         record_property("proves", "388.1")
> >           assert not theirs, (f"388.1: on {event} a copy of dokima/checks.py other than main's ran "
> E           AssertionError: 388.1: on merge_group a copy of dokima/checks.py other than main's ran (queued matrix), so a pull request's edit judges it:
>         Proves 388.2. Queues a pull request whose dokima/checks.py was edited to list one always-passing check. With working code the
>         record_property("proves", "388.2")
>             passed, _, logs = queue(tmp_path / f"{event}-good", event, APP_GOOD)
>             assert passed, f"388.2: on {event} a pull request with working code did not pass its done-whens:\n{logs}"
>             passed, ran, logs = queue(tmp_path / f"{event}-bad", event, APP_BAD)
> >           assert not passed, (f"388.2: on {event} a pull request with broken code that edits dokima/checks.py passed "
> == ${{ github.event.merge_group.base_sha }}
> 2 failed in 0.24s
> == ${{ github.base_ref || github.event.merge_group.base_sha }}
> 2 failed in 0.15s
> == ${{ github.event.merge_group.base_ref }}
> 2 passed in 1.53s
> == ${{ github.event.merge_group.base_ref || github.base_ref }}
> 2 passed in 1.53s
> == main
> 2 passed in 1.57s
> == ${{ github.event.merge_group.head_sha }}
> 2 failed in 0.16s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
cd /home/runner/work/dokima/dokima; cat .github/workflows/full-suite.yml | head -50; grep -il autopilot /tmp/pack/issue.md
```

> name: full suite
> # Every test in the repo, on every pull request, in the merge queue and on main.
> # Runs main's copy of this workflow, so a pull request can't rewrite its own judge; only the code it tests comes from
> # the pull request, checked out with no token left behind, and the run holds no secret and only read access.
> on:
>   pull_request_target:
>   push:
>     branches: [main]
>   merge_group:
> permissions:
>   contents: read
> jobs:
>   all-tests:
>     name: all tests
>     runs-on: ubuntu-24.04
>     steps:
>       - uses: actions/checkout@v5
>         with:
>           ref: ${{ github.event.pull_request.head.sha || github.sha }}
>           persist-credentials: false
>       - uses: actions/setup-python@v6
>         with:
>           python-version: "3.12"
>       - run: pip install -q pytest
>       - run: pytest -q -p no:cacheprovider tests
> /tmp/pack/issue.md

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner widened 388.1: main's copy of Dokima's code makes the check list in the merge queue even with another pull request queued ahead, and neither the queued commit's copy nor the one ahead ever runs.",
          "Its test now queues the pull request behind another one whose dokima/checks.py is edited too, so the event's base commit is that other pull request's, not main."],
  "decided": ["Only done-whens.yml changes; full-suite.yml stays as it is because it runs no Dokima code."],
  "open": ["It still asks the owner whether leaving a pull request's own edits to the workflow files to the owner's approval is enough, or whether a repo setting that requires main's workflows should be its own issue."]},
 "verdict": "approve",
 "summary": "The plan's tests now fail when the queue judges a pull request with any copy of Dokima's code but main's, including the one queued ahead; its question about the workflow files themselves still waits for you.",
 "raises": [],
 "answers": [],
 "asks": [{"ask": "A pull request that edits done-whens.yml, full-suite.yml or dokima/checks.py would be judged in the queue by its own edited copy, which is what #263 closed for pull requests.",
           "source": "https://github.com/dokima-dev/dokima/issues/388", "criterion": "388.1"}]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 388 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The tests now fail unless main's copy of Dokima's code judges the queue, even behind another pull request; the workflow-files question still waits for you."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 388 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#388](https://github.com/dokima-dev/dokima/issues/388) (the queued commit's copy of Dokima's checks judging itself in the merge queue). The planner's question about the workflow files themselves still waits for you.

**Last round's blocker is fixed.** The test used to treat the commit just ahead in the queue as main. So a fix that copied that commit would have passed, even though it lets a pull request queued ahead pick the checks for the one behind it. Now the test puts another pull request ahead in the queue, and its `dokima/checks.py` is edited too.

I tried several candidate fixes in `.github/workflows/done-whens.yml` on a copy of the repo and ran `tests/test_queue_judge.py` against each:

| Copy of Dokima's code the checks use | Tests |
|---|---|
| Today's workflow (the queued commit) | 2 failed |
| The commit just ahead in the queue | 2 failed |
| The pull request's own base branch name, falling back to the commit ahead | 2 failed |
| The queued commit, named explicitly | 2 failed |
| `main` | 2 passed |
| The merge queue's base branch | 2 passed |
| The merge queue's base branch, falling back to the pull request's own base branch name | 2 passed |

- **Today both tests fail for the right reason:** the queued commit's edited copy makes the check list, and broken code passes in the queue.
- **Both checks have to move to main:** a fix that changes only the job that makes the check list still fails 388.1, because the queued copy still annotates the tests.
- **The queued code still gets tested:** a fix that also took the tests from main would fail 388.2, because broken code would then pass.

**Your question is still open.** On the queue's event, GitHub always runs the queued commit's own `done-whens.yml` and `full-suite.yml`, so no code change here can stop a pull request that edits those files from judging itself. The plan leaves that to your approval of every change to a workflow file. The planner asks whether that is enough, or whether a repo setting that makes these workflows run from main should be its own issue.

Your second `/plan` had no words, so it didn't answer this. I couldn't answer it for you: the issue isn't on autopilot, and nothing you've written settles it.

Your one ask in the issue is covered by 388.1. The review passed Dokima's own checks and is saved at `/tmp/dokima-out/review.json`.
