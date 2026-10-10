# reviewer (plan) for #388

Run: https://github.com/dokima-dev/dokima/actions/runs/38068620890

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> .:
> total 52
> drwxr-xr-x  3 runner runner  4096 Oct 10 16:40 .
> drwxrwxrwt 18 root   root    4096 Oct 10 16:40 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 16:40 in
> -rw-r--r--  1 runner runner 28302 Oct 10 16:40 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 16:40 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 16:40 parent.json
> -rw-r--r--  1 runner runner  2232 Oct 10 16:40 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct 10 16:40 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 16:40 ..
> -rw-r--r-- 1 runner runner 3964 Oct 10 16:40 01-planner.json
> -rw-r--r-- 1 runner runner 3174 Oct 10 16:40 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 4631 Oct 10 16:40 03-planner.json
> -rw-r--r-- 1 runner runner 1875 Oct 10 16:40 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2837 Oct 10 16:40 05-planner.json
> # Issue #388: In the merge queue, a pull request's own copy of the checks judges it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 396 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> In the merge queue, done-whens runs the queued commit's copy of Dokima's code, so an edited dokima/checks.py judges itself.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> https://github.com/dokima-dev/dokima/issues/388
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokim

`2. Bash`
```
cd /tmp/pack; cat plan.json parent.json; cat in/05-planner.json; cat in/04-reviewer-plan.json | head -50; cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; git diff f477545 ef2673e --stat
```

> {
>  "kind": "user_story",
>  "summary": "In the merge queue, done-whens runs the queued commit's copy of Dokima's code, so an edited dokima/checks.py judges itself.",
>  "user_story": "A pull request in the merge queue is judged by main's copy of Dokima's code, as it already is on the pull request itself, so editing dokima/checks.py cannot wave it through the queue.",
>  "acceptance_criteria": [
>   {
>    "text": "In the merge queue, main's copy of Dokima's code lists a queued pull request's checks and annotates its tests, even behind another queued pull request. Neither the queued commit's copy of dokima/checks.py nor the copy of the pull request queued ahead ever runs there, and on the pull request itself main's copy still does both, as before.",
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
>   "The workflow files themselves: on the merge queue's event GitHub always runs the queued commit's copy of done-whens.yml and full-suite.yml, and nothing inside a workflow file can c

`3. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_queue_judge.py 2>&1 | tail -8
```

> $ if [ -z "$MATRIX" ] || [ "$MATRIX" = "[]" ]; then
>     echo "::error title=No done-whens::Link an issue with done-whens (Closes #N) to this pull request."
>     exit 1
>   fi
>   test "$RESULT" = "success"
>   
> assert not True
> 2 failed in 0.27s

`4. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_queue_judge.py 2>&1 | grep -E "^E|388\.|Error" | head -20
```

> Proves 388.1. Queues a pull request whose dokima/checks.py was edited, runs every job of done-whens.yml on the merge queue's
>         record_property("proves", "388.1")
> >           assert not theirs, (f"388.1: on {event} a copy of dokima/checks.py other than main's ran "
> E           AssertionError: 388.1: on merge_group a copy of dokima/checks.py other than main's ran (queued matrix), so a pull request's edit judges it:
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

`5. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner took the owner's answer on the workflow-files question and dropped the question from the plan.",
          "It moved the workflow files themselves out of scope, covered by the owner's approval of every workflow change, and linked the repo setting that requires main's workflows as #420."],
  "decided": ["The criteria and tests are the same as the plan approved last round; only done-whens.yml changes."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan now follows your answer: workflow edits are left to your approval, the repo setting is its own issue (#420), and both tests still fail today for the right reason.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "A pull request that edits done-whens.yml, full-suite.yml or dokima/checks.py would be judged in the queue by its own edited copy, which is what #263 closed for pull requests.",
   "source": "https://github.com/dokima-dev/dokima/issues/388", "criterion": "388.1"},
  {"ask": "my approval of every workflow change is enough here. The repo setting that requires main's workflows goes in its own issue.",
   "source": "https://github.com/dokima-dev/dokima/issues/388", "criterion": "388.1"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 388 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

**Agent:** Approving the plan. The check says my summary is too long, so I'm shortening it.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan follows your answer: workflow edits wait for your approval, the repo setting is #420, and both tests fail today as they should."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 388 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#388](https://github.com/dokima-dev/dokima/issues/388) (main's copy of Dokima's code judges the merge queue). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **What changed this round:** the planner took your answer. It dropped the workflow-files question and moved the workflow files out of scope, since your approval of every workflow change covers them. It linked the repo setting that requires main's workflows as [#420](https://github.com/dokima-dev/dokima/issues/420) (that repo setting, as its own issue). The criteria and tests are the same as last round's approved plan, and the test file hasn't changed since then.
- **Tests:** I ran `pytest -q tests/test_queue_judge.py` and both tests fail today for the right reason. For 388.1, the queued commit's copy of `dokima/checks.py` is the one that makes the check list (`checkout (no ref) -> queued`). For 388.2, the gate passes when it should fail.
- **Your asks:** I matched both to 388.1: the original ask, and your answer that your approval is enough and the setting gets its own issue. None are missing.

No blockers and nothing new to file. The plan now waits for your `/work`.
