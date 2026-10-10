# reviewer (plan) for #301

Run: https://github.com/dokima-dev/dokima/actions/runs/38062642890

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (33KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7a610ca1-e50e-4a4e-9280-6e2af7a7453b/tool-results/biq98910v.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct 10 15:12 .
> drwxrwxrwt 18 root   root    4096 Oct 10 15:12 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 15:12 in
> -rw-r--r--  1 runner runner 32951 Oct 10 15:12 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 15:12 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 15:12 parent.json
> -rw-r--r--  1 runner runner  4932 Oct 10 15:12 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct 10 15:12 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 15:12 ..
> -rw-r--r-- 1 runner runner 4700 Oct 10 15:12 01-planner.json
> -rw-r--r-- 1 runner runner 2607 Oct 10 15:12 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2619 Oct 10 15:12 03-worker.json
> -rw-r--r-- 1 runner runner 2835 Oct 10 15:12 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5561 Oct 10 15:12 05-planner.json
> # Issue #301: The reviewer settles raises between agents and confirms issues before code files them
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 298, 299, 300 -->
> <!-- dokima-blocking: {"blocked_by": [298, 300], "blocks": [302], "loop": []} -->
> The reviewer settles a worker's raise for the planner itself, and an agent's issue is filed only once the reviewer confirms it.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/301 · https://github.com/dokima-

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json parent.json; sed -n '/dokima-ask\|Original issue/,$p' issue.md | head -400
```

> []{"number": 289}<!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #289, story 4</summary>
> 
> **Part of:** #289 Every agent raises things and answers them through the same two fields
> 
> **User story:** A worker's judgment that a test or the plan is wrong reaches the right agent without waiting for the owner, and an issue an agent finds becomes a real GitHub issue only once the reviewer confirms it.
> 
> **Context:** Owner's words: the issue body ('the worker raises blockers for the planner only through the reviewer, who judges whether they are real'; 'issue ... code files it') and the comment of 2026-10-09T01:39:55Z (always on: the reviewer settles anything addressed to an agent, routing a worker's 'this test is broken' to the planner or back to the worker without waiting; an issue is filed only after the reviewer confirms it). Today the worker's suspect_tests reach the code reviewer, which may block for the planner (next_step() fixer == planner, dokima/agent.py next_step() 1467), and nothing files issues_found. Open issues #268, #265 and #193 plan filing found issues (parked, labeled filed-by-dokima); fold them into this story or re-point them at raises of kind issue rather than build filing twice. Reading taken: an issue the reviewer raises itself counts as confirmed; one from the planner or worker is filed only when the reviewer answers it done.
> 
> **Acceptance criteria:**
> - A 

`3. Bash`
```
cd /tmp/pack; cat plan.json; python3 -c "import json;d=json.load(open('in/05-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:3000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests | head -200
```

> {
>  "kind": "user_story",
>  "summary": "The reviewer settles a worker's raise for the planner itself, and an agent's issue is filed only once the reviewer confirms it.",
>  "user_story": "A worker's judgment that a test or the plan is wrong reaches the right agent without waiting for the owner, and an issue an agent finds becomes a real GitHub issue only once the reviewer confirms it.",
>  "acceptance_criteria": [
>   {
>    "text": "A worker's raise for the planner goes to the reviewer first. When the reviewer answers it done, the planner starts with it as the reviewer's blocker and must answer it, even when the same review also sends the planner blockers of its own; when the reviewer answers disagree, the worker starts again with the reviewer's why. This holds whether the review approves the code or blocks it, and neither waits for the owner nor, on autopilot, merges the pull request.",
>    "source": "https://github.com/dokima-dev/dokima/issues/301"
>   },
>   {
>    "text": "Code files an issue raise as its own GitHub issue only once the reviewer confirms it. The filed issue is titled with the raise's first sentence, and its body holds the raise's words, its evidence and the issue it was found on. The reviewer's own issue raises count as confirmed and are filed in its run, and its card names each by its new number and says the reviewer confirmed it. The planner's or worker's issue raises are never filed in their own run: the reviewer's next run must answer each, and code files it when the 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_reviewer_settles.py tests/test_raise_handbacks.py 2>&1 | tail -15; grep -n 'for_planner(h)' dokima/agent.py
```

> assert 0 == 1
>  +  where 0 = len({})
> FAILED tests/test_reviewer_settles.py::test_an_issue_raise_the_reviewer_answers_done_is_filed_and_disagree_is_not - AssertionError: 301.2: the worker's issue the reviewer confirmed should file exactly one issue, filed {}
> assert 0 == 1
>  +  where 0 = len({})
> FAILED tests/test_reviewer_settles.py::test_a_plan_reviewer_confirming_the_planners_issue_files_it - AssertionError: 301.2: the planner's issue the reviewer confirmed should file exactly one issue, filed {}
> assert 0 == 1
>  +  where 0 = len({})
> FAILED tests/test_reviewer_settles.py::test_an_issue_github_refuses_to_file_says_why_and_the_record_stands - AssertionError: 301.3: neither the record nor a comment on #301 names the finding with GitHub's reason 'HTTP 502: Server Error (https://api.github.com/repos/o/r/issues)'
> assert []
> FAILED tests/test_raise_handbacks.py::test_each_starting_pack_lists_exactly_the_open_raises_for_that_agent - AssertionError: 300.2: after the code review answered W1 done, the planner's pack should list it once as the reviewer's blocker, lists:
>   [{"kind": "blocker", "to": "planner", "text": "The second test proves a neighbour of the promise.", "raised_by": "reviewer", "id": "R3"}]
> assert 0 == 1
>  +  where 0 = len([])
> 7 failed, 17 passed in 6.79s
> 185:                if on and on["id"] not in answered and not (a.get("answer") == "done" and for_planner(h)):
> 239:def for_planner(h):
> 1883:    return ("start", "planner" if stage == "plan" or for_planner(h) or "done" in word

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat f91e05e | head; git log --oneline -6 --all | head; git branch -a; python3 -m pytest -q tests/test_reviewer_settles.py 2>&1 | grep -E 'FAILED|passed'
```

> commit f91e05e8bb6d61ae0360e8746a697b6731fce0ad
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 14:52:01 2026 +0000
> 
>     worker for #301 (run 38060688591)
> 
>  dokima/agent.py  | 100 +++++++++++++++++++++++++++++++++++++++++++++++++------
>  dokima/raises.py |  36 ++++++++++++++++++--
>  2 files changed, 124 insertions(+), 12 deletions(-)
> 730ee0e Conversation of run 38062105068
> 94926ee planner for #410 (run 38062105068)
> e34753f Conversation of run 38062103512
> 6892855 planner for #408 (run 38062103512)
> fe26ca7 Conversation of run 38061710918
> a9f6893 planner for #301 (run 38061710918)
>   main
> * try/issue-301
>   remotes/origin/agent-components
>   remotes/origin/agents-scope-rule
>   remotes/origin/archive/try-issue-154-before-main-moved
>   remotes/origin/commands
>   remotes/origin/fix-planner-issue-step
>   remotes/origin/issue-100-planner-check
>   remotes/origin/issue-107-pitch
>   remotes/origin/issue-113-workflow-gate
>   remotes/origin/issue-116-board-sync
>   remotes/origin/issue-121-needs-you
>   remotes/origin/issue-126-keys-from-main
>   remotes/origin/issue-138-prompt
>   remotes/origin/issue-40-app
>   remotes/origin/issue-46-approve
>   remotes/origin/issue-54-plan
>   remotes/origin/issue-60-wrap
>   remotes/origin/issue-63-latest
>   remotes/origin/issue-67-label
>   remotes/origin/issue-74-layout
>   remotes/origin/issue-78-design
>   remotes/origin/issue-80-planner
>   remotes/origin/issue-81-build-on-main
>   remotes/origin/issue-89-planner-prompt
>   remote

**Agent:** I'm checking why some of the plan's tests fail on the branch that already holds the worker's code.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; env | grep -i python; env -u PYTHONSAFEPATH -u PYTHONPATH python3 -m pytest -q tests/test_reviewer_settles.py tests/test_raise_handbacks.py 2>&1 | grep -E 'FAILED|passed'
```

> PKG_CONFIG_PATH=/opt/hostedtoolcache/Python/3.12.15/x64/lib/pkgconfig
> Python_ROOT_DIR=/opt/hostedtoolcache/Python/3.12.15/x64
> pythonLocation=/opt/hostedtoolcache/Python/3.12.15/x64
> PYTHONSAFEPATH=1
> PYTHONPATH=/tmp/runtime
> Python3_ROOT_DIR=/opt/hostedtoolcache/Python/3.12.15/x64
> LD_LIBRARY_PATH=/opt/hostedtoolcache/Python/3.12.15/x64/lib
> Python2_ROOT_DIR=/opt/hostedtoolcache/Python/3.12.15/x64
> PATH=/opt/hostedtoolcache/Python/3.12.15/x64/bin:/opt/hostedtoolcache/Python/3.12.15/x64:/snap/bin:/home/runner/.local/bin:/opt/pipx_bin:/home/runner/.cargo/bin:/home/runner/.config/composer/vendor/bin:/usr/local/.ghcup/bin:/home/runner/.dotnet/tools:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
>             passed_on = [r for r in mine if r.get("id") != "R1"]
> >           assert len(passed_on) == 1, \
>         planner's also the worker's raise the review answered done, passed on as the reviewer's blocker (#301: a review's
>         rejected = rec("worker", "", {**WORK, "raises": [WX]}, passed=False)
>                     passed_on = [g for g in got if isinstance(g, dict) and confirmed_w1(g)]
> >                   assert len(passed_on) == 1, (f"300.2: after the code review answered W1 done, the planner's pack should "
> FAILED tests/test_reviewer_settles.py::test_a_confirmed_raise_reaches_the_planner_beside_the_reviews_own_blocker_for_it - AssertionError: 301.1: the planner should get the confirmed worker raise beside the review's own blocker (bl

**Agent:** Only the new and changed tests fail with the repo's own code. Now checking that the fix the plan names turns them green.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/chk && git worktree add -q /tmp/chk HEAD && cd /tmp/chk && sed -i 's/ and not (a.get("answer") == "done" and for_planner(h)):/:/' dokima/agent.py && git diff --stat && env -u PYTHONSAFEPATH -u PYTHONPATH python3 -m pytest -q tests/test_reviewer_settles.py tests/test_raise_handbacks.py tests/test_raises.py 2>&1 | tail -3; sed -n 175,195p dokima/agent.py
```

> dokima/agent.py | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> ....................................                                     [100%]
> 36 passed in 6.82s
>                 continue
>             confirm = raises.for_review(x)
>             if confirm is None:
>                 out.append(x)
>             elif not reviewed:
>                 out.append(confirm)
>         if r["role"] == "reviewer":
>             for a in card.answers_of(h):
>                 x = by_id.get(a["raise"]) if isinstance(a["raise"], str) else None
>                 on = raises.passes_on(x, a) if x else None
>                 if on and on["id"] not in answered:
>                     out.append(on)
>         by_id.update({x["id"]: x for x in card.raises_of(h) if isinstance(x.get("id"), str)})
>         stage = r.get("stage") or ""
>         old = h.get("blockers") if isinstance(h.get("blockers"), list) else []
>         if r["role"] == "reviewer" and newest.get(stage) == i and h.get("verdict") != "approve":
>             out += [old_blocker(b, stage) for b in old if isinstance(b, dict) and filled(b.get("id"))
>                     and b["id"] not in answered]
>     return out
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** The fix makes them pass. Running the full suite on that fixed copy to be sure the changed older test breaks nothing else.

`8. Bash`
```
cd /tmp/chk && env -u PYTHONSAFEPATH -u PYTHONPATH timeout 500 python3 -m pytest -q -x 2>&1 | tail -3; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/chk
```

> ........................................................................ [ 93%]
> .ss.sss.................................ss.................s             [100%]
> 846 passed, 78 skipped in 237.12s (0:03:57)

**Agent:** All green. Writing the hand-back.

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner widened 301.1: a raise the reviewer confirms reaches the planner even when the same review also sends the planner blockers of its own.",
          "It added one test for that case, once with a blocking and once with an approving review, and changed the older 300.2 test to expect the confirmed raise beside the review's own blocker, with its reason."],
  "decided": ["The older test checks the passed-on raise by its kind, who it is for, who raised it and the worker's words, not by an exact ID."],
  "open": []},
 "verdict": "approve",
 "summary": "The re-plan closes the gap the code review found: a confirmed raise now must reach the planner beside the review's own blocker, and the new and changed tests fail on the current code for exactly that reason and pass once it is fixed.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "the worker raises blockers for the planner only through the reviewer, who judges whether they are real", "source": "https://github.com/dokima-dev/dokima/issues/289", "criterion": "301.1"},
  {"ask": "When the reviewer answers done, the planner starts with it as the reviewer's blocker; when the reviewer answers disagree, the worker starts again with the why. Neither waits for you.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.1"},
  {"ask": "Code files an issue raise as its own GitHub issue only once the reviewer confirms it.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.2"},
  {"ask": "The reviewer's own issue raises count as confirmed, and its card says so; the planner's or worker's are filed when it answers done, never when it answers disagree.", "source": "https://github.com/dokima-dev/dokima/issues/301", "criterion": "301.2"},
  {"ask": "An issue that fails to file says why on this issue, and the run's record still stands.", "source": "https://github.com/dokima-
```

> Exit code 1
> summary holds 43 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`10. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="A confirmed raise now must reach the planner beside the review's own blocker, and the new tests fail today for exactly that reason."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 301 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the re-plan for [#301](https://github.com/dokima-dev/dokima/issues/301) (the reviewer settles raises between agents and confirms issues before code files them). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner changed:** The earlier code review found a gap in the worker's code. A worker's raise that the reviewer confirmed never reached the planner if the same review also sent the planner a blocker of its own. The planner fixed this in three ways:
- **Criterion 301.1:** it now says the confirmed raise reaches the planner even when the review sends the planner blockers of its own.
- **New test:** it covers that case once with a blocking review and once with an approving one.
- **Changed older test:** the 300.2 test now expects the confirmed raise beside the review's own blocker, with a reason the owner can see.

**What I checked:**
- **The tests fail today for the right reason.** On this branch, which already has the worker's code, only the new test and the changed older test fail. In both, the planner's list lacks the confirmed raise.
- **The fix turns them green.** In a scratch copy I removed the one condition in `open_raises()` (`dokima/agent.py:185`) that drops the confirmed raise. The full suite then passed: 846 passed, 78 skipped. I then deleted that copy; I changed no file in the repo.
- **No ask is dropped.** All five of the owner's asks map to 301.1, 301.2 or 301.3. There were no open blockers to answer.

The tests only run correctly with the sandbox's `PYTHONSAFEPATH` and `PYTHONPATH` unset. Under the default settings, the copy of Dokima in `/tmp/runtime` is used instead of the branch's code, and four extra tests fail.

Because the re-plan changes a criterion, it should wait for your `/work` rather than go straight to the worker.
