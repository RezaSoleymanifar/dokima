# reviewer (plan) for #429

Run: https://github.com/dokima-dev/dokima/actions/runs/38078259903

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (40.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/e50708be-2241-4b77-ba57-ce1d297c0d28/tool-results/bigpjgcpm.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct 10 19:03 .
> drwxrwxrwt 18 root   root    4096 Oct 10 19:03 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 19:03 in
> -rw-r--r--  1 runner runner 35694 Oct 10 19:03 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 19:03 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 19:03 parent.json
> -rw-r--r--  1 runner runner  4708 Oct 10 19:03 plan.json
> 
> in:
> total 36
> drwxr-xr-x 2 runner runner 4096 Oct 10 19:03 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 19:03 ..
> -rw-r--r-- 1 runner runner 5317 Oct 10 19:03 01-planner.json
> -rw-r--r-- 1 runner runner 3599 Oct 10 19:03 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1577 Oct 10 19:03 03-worker.json
> -rw-r--r-- 1 runner runner 3233 Oct 10 19:03 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5352 Oct 10 19:03 05-planner.json
> # Issue #429: A board or card update the budget stopped is retried once the budget is back
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 417, 428 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A board or card update stopped by GitHub's empty API budget waits for the reset and runs once more.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/429 · https://github.com/dokima-dev/dokima/pull/446 · <img src="https://raw.githubuse

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json parent.json; cat plan.json; for f in in/*; do echo "=== $f"; cat $f; echo; done
```

> []{"number": 368}{
>  "kind": "user_story",
>  "summary": "A board or card update stopped by GitHub's empty API budget waits for the reset and runs once more.",
>  "user_story": "When GitHub's API budget runs out, every board card and issue card the outage stopped is put right by itself once the budget resets, with no comment needed.",
>  "acceptance_criteria": [
>   {
>    "text": "A board update that fails because GitHub's GraphQL or REST budget ran out runs again once that budget resets. That covers board.yml's runs on an event, its 15-minute sweeps and the board step at the end of every agent run. Its cards end in the columns and pills their state on GitHub gives then, with no comment needed, and the run passes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/368"
>   },
>   {
>    "text": "An issue or pull request card redraw that fails because a budget ran out is redrawn after the reset, showing the issue's state then. That covers card.yml's redraws and its 15-minute sweeps, and the run passes.",
>    "source": "https://github.com/dokima-dev/dokima/issues/368"
>   },
>   {
>    "text": "A board or card update that fails for any other reason fails as it does today, at once, with no wait and no second run. A failure counts as a budget failure only when GitHub's rate-limit endpoint, read right after it, reports 0 left in the GraphQL or REST budget; when GitHub cannot report the budget, it is not one.",
>    "source": "https://github.com/dokima-dev/dokima/issues/368"
>   }
>  ],
>  "non_function

`3. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> <persisted-output>
> Output too large (34.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/e50708be-2241-4b77-ba57-ce1d297c0d28/tool-results/bwvtpvfdv.txt
> 
> Preview (first 2KB):
> # Issue #429: A board or card update the budget stopped is retried once the budget is back
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 417, 428 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> A board or card update stopped by GitHub's empty API budget waits for the reset and runs once more.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/429 · https://github.com/dokima-dev/dokima/pull/446 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/446/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **End-of-run board step:** Should the board step at the end of an agent run also wait for the reset? It runs just before the step that starts the next stage, so during an outage the next stage could start up to an hour later. The plan assumes it waits, since the ask names every board update. · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue fo

`4. Bash`
```
cd /tmp/pack; grep -n -E "^#|^## |^### |Comment|commented|RezaSoleymanifar|dokima-original|Original issue|<!-- dokima" issue.md | head -80
```

> 1:# Issue #429: A board or card update the budget stopped is retried once the budget is back
> 3:<!-- dokima-card -->
> 4:<!-- dokima-linked-from: 417, 428 -->
> 5:<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> 65:<!-- dokima-ask -->
> 66:<details><summary>Original issue</summary>
> 68:<!-- dokima-card -->
> 92:## Comments
> 94:### dokima-runtime on issue #429 (2026-10-10T17:59:16Z)
> 98:### dokima-runtime on issue #429 (2026-10-10T17:59:39Z)
> 100:<!-- dokima-record -->
> 164:### dokima-runtime on issue #429 (2026-10-10T18:15:07Z)
> 166:<!-- dokima-record -->
> 212:**Next:** @RezaSoleymanifar The links are recorded, but the card of #429 could not be redrawn: GraphQL: API rate limit already exceeded for installation ID 168252268.. The links are recorded, but the card of #380 could not be redrawn: gh: API rate limit already exceeded for installation ID 168252268.. The links are recorded, but the card of #417 could not be redrawn: gh: API rate limit already exceeded for installation ID 168252268.. The links are recorded, but the card of #426 could not be redrawn: gh: API rate limit already exceeded for installation ID 168252268.. The links are recorded, but the card of #427 could not be redrawn: gh: API rate limit already exceeded for installation ID 168252268.. The links are recorded, but the card of #428 could not be redrawn: gh: API rate limit already exceeded for installation ID 168252268.. Nothing starts by itself: fix it, then say `/work`, or `/plan` with changes.
> 215:###

`5. Bash`
```
cd /tmp/pack; sed -n 60,98p issue.md; sed -n 213,220p issue.md
```

> **Definition of Done:** <a href="https://github.com/dokima-dev/dokima/actions/runs/38078243205/job/114289623682"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/running.svg" width="16" height="16" align="absmiddle" alt="running"></a> All tests · <a href="https://github.com/dokima-dev/dokima/actions/runs/38077523418"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #368, story 4</summary>
> 
> **Part of:** #368 Dokima tracks its GitHub API budget per run and warns before it runs out
> 
> **User story:** When GitHub's budget runs out, every board card and issue card the outage left behind is put right by itself once the budget resets, with no comment needed.
> 
> **Context:** After the 2026-

**Agent:** Reviewing the re-plan for #429: checking the new failed-run test now.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head; python3 -m pytest -q tests/test_budget_retry.py 2>&1 | tail -30
```

> commit 968504a0848fa86923182d30db24805abd271c4b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 19:02:58 2026 +0000
> 
>     planner for #429 (run 38077930705)
> 
>  tests/test_budget_retry.py | 28 ++++++++++++++++++++++++++++
>  1 file changed, 28 insertions(+)
> E           }
> 
> tests/test_budget_retry.py:297: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> board: #57 and its open pull request -> Work · Needs you
> ::warning::GitHub could not be read, so the board may not show it: GraphQL: API rate limit already exceeded for installation ID 168252268
> =========================== short test summary info ============================
> FAILED tests/test_budget_retry.py::test_the_board_step_after_a_failed_run_shows_needs_you_after_the_reset - AssertionError: 429.1: after the budget reset the failed run's cards are at {'#57': ('Backlog', None), 'PR #70': ('Review', None)}, not both in Work with Needs you: the board step after a failed run gave up instead of waiting for the reset
> assert {'#57': ('Bac...eview', None)} == {'#57': ('Wor... 'Needs you')}
>   
>   Differing items:
>   {'PR #70': ('Review', None)} != {'PR #70': ('Work', 'Needs you')}
>   {'#57': ('Backlog', None)} != {'#57': ('Work', 'Needs you')}
>   
>   Full diff:
>     {
>         '#57': (
>   -         'Work',
>   -         'Needs you',
>   +         'Backlog',
>   +         None,
>         ),
>         'PR #70': (
>   -         'Work',
>   -         'Needs you'

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_budget_retry.py; grep -n "def run_ends\|def _gh\|def fake\|once_more\|sleep" tests/test_budget_retry.py | head -30; sed -n 2265,2300p dokima/agent.py
```

> commit 968504a0848fa86923182d30db24805abd271c4b
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 19:02:58 2026 +0000
> 
>     planner for #429 (run 38077930705)
> 
> diff --git a/tests/test_budget_retry.py b/tests/test_budget_retry.py
> index 611f560..8f9cfe2 100644
> --- a/tests/test_budget_retry.py
> +++ b/tests/test_budget_retry.py
> @@ -273,6 +273,34 @@ def test_the_board_step_at_the_end_of_a_run_runs_again_after_the_reset(record_pr
>          f"429.1: after the budget reset #57's card is at {place(w, 'issue', 57)}, not Plan with Needs you"
>  
>  
> +def test_the_board_step_after_a_failed_run_shows_needs_you_after_the_reset(record_property, make, budget, monkeypatch, tmp_path):
> +    """After a failed run, a budget-stopped board step shows Needs you once the budget resets.
> +
> +    Proves 429.1. A worker run on #57 fails its check, so the river stops for the owner: the step must put #57 and its
> +    open pull request #70 in Work with Needs you. Their cards sit in Backlog and Review. GitHub refuses the board's
> +    first read while the GraphQL budget is empty until 22:29Z, so a step that gives up at once leaves both cards where
> +    they were. The step must exit 0, open the board twice (before and after the wait), and leave both in Work with
> +    Needs you."""
> +    record_property("proves", "429.1")
> +    b = budget("429.1", empty={"graphql": 19 * 60})
> +    w = make(prs={57: 70}, cards={("issue", 57): {"Status": "Backlog"}, ("pr", 70): {"Status"

`8. Bash`
```
rm -rf /tmp/rv && cp -r /home/runner/work/dokima/dokima /tmp/rv && cd /tmp/rv && python3 - <<'EOF'
p='dokima/agent.py'; s=open(p).read()
old="""            board.stopped(board.Board(spec, repo), repo, argv[2], column)
        except (subprocess.CalledProcessError, KeyError, ValueError) as e:"""
new="""            retry.once_more("the board step", lambda: board.stopped(board.Board(spec, repo), repo, argv[2], column))
        except (subprocess.CalledProcessError, KeyError, ValueError, RuntimeError) as e:"""
assert old in s; open(p,'w').write(s.replace(old,new))
EOF
python3 -m pytest -q -p no:cacheprovider tests/test_budget_retry.py 2>&1 | tail -3; sed -n 1,60p dokima/retry.py | grep -n "def once_more" 
```

> ...........                                                              [100%]
> 11 passed in 0.31s
> 57:def once_more(what, update, failed=lambda result: False, errors=(subprocess.CalledProcessError, RuntimeError)):
> Shell cwd was reset to /home/runner/work/dokima/dokima

`9. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added a test for the board step after a failed agent run: when the empty budget stops it, the issue and its pull request must show Work with Needs you after the reset."],
  "decided": ["The criteria, scope and other tests stay as approved; only criterion 429.1 gains the new test."],
  "open": []},
 "verdict": "approve",
 "summary": "The re-plan adds the missing test for the board step after a failed run; it fails on the branch today because that step gives up at once, and passes once the step waits for the reset.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "When GitHub's budget runs out, every board card and issue card the outage left behind is put right by itself once the budget resets, with no comment needed.", "source": "https://github.com/dokima-dev/dokima/issues/429", "criterion": "429.1"},
  {"ask": "A board update that fails because a budget ran out runs again after the budget resets. Its cards end in the columns and pills their state says, with no comment needed.", "source": "https://github.com/dokima-dev/dokima/issues/429", "criterion": "429.1"},
  {"ask": "An issue or pull request card redraw that fails because the budget ran out is redrawn after the budget resets, showing the issue's state then.", "source": "https://github.com/dokima-dev/dokima/issues/429", "criterion": "429.2"},
  {"ask": "A board or card update that fails for any other reason fails as it does today and is not treated as a budget failure.", "source": "https://github.com/dokima-dev/dokima/issues/429", "criterion": "429.3"},
  {"ask": "A retry waits for GitHub's reported reset time instead of retrying in a loop.", "source": "https://github.com/dokima-dev/dokima/issues/429", "criterion": "429.4"}
 ]}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 429 && python3 -m dokima.agent check-round reviewer /tmp/
```

> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`10. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The new test for the board step after a failed run fails today because that step gives up at once, and passes once it waits."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 429 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; rm -rf /tmp/rv
```

> rc=0

**Agent:** I approved the re-plan for [#429](https://github.com/dokima-dev/dokima/issues/429) (board and card updates retried once GitHub's API budget resets). The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

- **What changed:** the planner answered my earlier blocker about a weak test. It added a test for the board step after a failed agent run. When the empty budget stops that step, the issue and its pull request must end up in Work with Needs you after the reset. Nothing else in the plan changed.
- **Fails today for the right reason:** on this branch the new test fails because the step gives up at once and both cards stay where they were. The other 10 tests pass.
- **Passes once fixed:** in a throwaway copy of the repo I made the failed-run step wait for the reset the same way the other branch does. All 11 tests then pass. The test also checks that the step waited the full time until the reset and read the board twice, so code that skips the wait can't pass it.
- **Raises and answers:** none in this review. Nothing was open for me to answer. The planner's earlier question about the end-of-run step was settled when you said `/work` on the plan that assumed it waits.
- **Asks:** all five asks in the issue still map to a criterion, none missing.

The worker's fix is still to come: [PR #446](https://github.com/dokima-dev/dokima/pull/446) (the retry build for this issue) needs that change before the new test passes.
