# reviewer (plan) for #240

Run: https://github.com/dokima-dev/dokima/actions/runs/37850167076

`1. Bash`
```
cd /tmp/pack; cat issue.md; ls in; cat open_blockers.json; cat plan.json
```

> # Issue #240: Every card opens with one short plain sentence, and the worker's docstrings are checked too
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #229, story 2</summary>
> 
> **Part of:** #229 Every card reads like plain English, and the checker catches long text before the reviewer does
> 
> **User story:** The owner opens every planner, worker and reviewer card on one short plain sentence instead of a changelog.
> 
> **Context:** Today dokima/roles/worker.md asks for a summary of 'Two plain sentences: the cause and the change', and dokima/agent.py opening() shows only the second via change_sentence(); details() puts the cause sentence in the 'What it built' fold. problems_work() and problems_shape() check the worker's and reviewer's summaries only for being non-empty, and the planner's summary is not length-checked. The worker's check can find the Python docstrings the worker added or changed from git diff against main. Reuse story 1's helper: 25 words for a summary, 15 for a docstring's first line, rejected only when more than 20% over, every text over its cap listed either way.
> 
> **Acceptance criteria:**
> - The planner's summary is one sentence of at most 25 words. ([source](https://github.com/dokima-dev/dokima/issues/229))
> - The worker's card opens with its summary, one sentence of at most 25 words, with no second sentence. ([source](https://github.com/dokima-dev/dokima/issues/229))
> - The reviewer's summary is one sentence of at mo

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_summary_caps.py; cat dokima/words.py
```

> commit 7b67354d3c21a4e569b29d43387f25b11d8d0907
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:55:47 2026 +0000
> 
>     planner for #240 (run 37848078692)
> 
>  tests/samples/132/review-pr.json |   2 +-
>  tests/samples/132/work.json      |   2 +-
>  tests/test_handback_check.py     |   5 +-
>  tests/test_review_asks.py        |   5 +-
>  tests/test_run_cards.py          |  10 +-
>  tests/test_summary_caps.py       | 215 +++++++++++++++++++++++++++++++++++++++
>  6 files changed, 230 insertions(+), 9 deletions(-)
> """Every card opens on one short sentence, and worker docstrings are capped too.
> 
> Issue #240 (story 2 of #229). The planner's, worker's and reviewer's summaries are each one sentence of at most 25
> words; every docstring the worker adds or changes opens with a line of at most 15 words. As in story 1 (#239,
> dokima/words.py), a text up to 20% over its cap (30 words for 25, 18 for 15) passes and is listed; one past that is
> rejected, naming it and its word count. A summary with a second sentence is rejected however short it is.
> 
> The planner's tests run `python3 -m dokima.planner check 9 OUT` through the `check` fixture of tests/test_plan_check.py.
> The worker's and reviewer's tests run the real command the workflow runs, `python3 -m dokima.agent check work|review
> FILE PLAN N`, from a temp git repo whose base commit is PLANNER_BASE, as the workflow sets it for every run; the
> worker's code there lives in app/, so nothing in the temp re

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_summary_caps.py 2>&1 | grep -E "^E .*240|passed|failed" | head -30; python3 -m pytest -q 2>&1 | tail -8
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b00wxwo1y). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** While that runs, let me look at the changed tests and the current checks.

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_run_cards.py tests/test_handback_check.py tests/test_review_asks.py tests/samples | head -150; grep -n "summary\|def problems_work\|def problems_shape\|def change_sentence\|PLANNER_BASE" dokima/agent.py | head -50
```

> commit 7b67354d3c21a4e569b29d43387f25b11d8d0907
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 21:55:47 2026 +0000
> 
>     planner for #240 (run 37848078692)
> 
> diff --git a/tests/samples/132/review-pr.json b/tests/samples/132/review-pr.json
> index 003728d..9249c22 100644
> --- a/tests/samples/132/review-pr.json
> +++ b/tests/samples/132/review-pr.json
> @@ -10,7 +10,7 @@
>    "open": []
>   },
>   "verdict": "approve",
> - "summary": "A failed run now always leaves its card, and its open pull request's, in its stage's column with Needs you, even when the run's own last steps fail; all three tests fail on main and pass here, with the full suite green.",
> + "summary": "A failed run now always leaves its card, and its open pull request's, in its stage's column with Needs you.",
>   "blockers": [],
>   "notes": [
>    {
> diff --git a/tests/samples/132/work.json b/tests/samples/132/work.json
> index a47d68e..e87e384 100644
> --- a/tests/samples/132/work.json
> +++ b/tests/samples/132/work.json
> @@ -1,5 +1,5 @@
>  {
> - "summary": "`agent board` read board.txt with no fallback, so when the run's \"Decide what follows\" step failed (or nothing was written) it crashed and the card was never moved or marked. Now, without a readable board.txt, it places the card as a stop for the owner: the column of the run's own stage from record.json, or from the run's ROLE and STAGE when there is no record, with Needs you.",
> + "summary": "Without a readable board.txt, agent board 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "PLANNER_BASE" .github dokima | head -20; sed -n 700,790p dokima/agent.py; sed -n 35,50p dokima/roles/worker.md
```

> .github/workflows/planner.yml:59:          echo "PLANNER_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
> dokima/planner.py:494:            base = os.environ.get("PLANNER_BASE", "HEAD")
> .github/workflows/agent.yml:149:          echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
>             if not filled(a.get("source")) or not owner_source(a["source"].strip(), number):
>                 bad.append(f"{label} needs a source: {issue_url(number)}, one of its comments' links, or AGENTS.md")
>         elif a.get("accepted") is False and not filled(a.get("why")):
>             bad.append(f"{label} is not accepted and needs why")
>     for q in qs:
>         if seen.count(q) != 1:
>             bad.append(f"the assumption of \"{q}\" must be judged exactly once in assumptions, {ASSUMPTION_SHAPE}")
>     return bad
> 
> 
> def problems_work(w):
>     """Everything wrong with a work.json, as plain sentences; empty when it is well formed."""
>     bad = []
>     if not str(w.get("summary", "")).strip():
>         bad.append("summary is empty")
>     if not isinstance(w.get("criteria"), dict) or not w["criteria"]:
>         bad.append("criteria must give one line per criterion")
>     if not str(w.get("evidence", "")).strip():
>         bad.append("evidence is empty: name the last test command and its result line")
>     for r in w.get("replies", []):
>         if r.get("answer") not in ANSWERS or not str(r.get("why", "")).strip() or not r.get("blocker"):
>             bad.append(f"reply to {r.get('blocker', '?')

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 135,160p .github/workflows/agent.yml; grep -n "check work\|check review\|check \"\$\|agent check" .github/workflows/agent.yml | head
```

> if git ls-remote --exit-code --heads origin "try/issue-$N" >/dev/null; then
>             git fetch -q origin "try/issue-$N" && git checkout -q -B "try/issue-$N" FETCH_HEAD
>             if [ "$ROLE" = worker ]; then
>               git -c user.name=dokima -c user.email=dokima@users.noreply.github.com merge -q --no-edit origin/main
>             fi
>           elif [ "$ROLE" = planner ] || [ "$STAGE" = plan ]; then
>             # A plan review needs no branch: a split never makes one, so it reviews from main.
>             git checkout -q -B "try/issue-$N" origin/main
>           else
>             echo "try/issue-$N does not exist; run the planner first." > /tmp/why.txt
>             echo "::error title=Nothing to $ROLE::$(cat /tmp/why.txt)"; exit 1
>           fi
>           echo "BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
>           # A plan's tests are everything the issue's branch added since it split off main, over every planning round.
>           echo "PLANNER_BASE=$(git merge-base HEAD origin/main)" >> "$GITHUB_ENV"
>           # What this run starts from: the planner may change only tests from here on.
>           echo "PLANNER_RUN_BASE=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
>           LOG="logs/$N/${{ github.run_id }}-$ROLE${STAGE:+-$STAGE}.md"
>           echo "LOG=$LOG" >> "$GITHUB_ENV"
>           echo "LOG_URL=${{ github.server_url }}/${{ github.repository }}/blob/logs/$LOG" >> "$GITHUB_ENV"
>       - name: Build the starting pack
>         env:
>           GH_TOKEN: ${{ github.token }}
>         run

`7. Bash`
```
sleep 100; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output
```

> <tool_use_error>Blocked: sleep 100 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`8. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 110 python3 -m pytest -q tests/test_summary_caps.py 2>&1 | grep -E "^E +(AssertionError: )?240|passed|failed" | head -20
```

> E       AssertionError: 240.1: the 28-word summary is not listed as over its cap: 'plan\n'
>         summary of two short sentences, each naming the summary. A passed worker card shows the summary, word for word,
> E       AssertionError: 240.2: a 31-word worker summary was not rejected naming it:
> E       AssertionError: 240.3: a 31-word review summary was not rejected naming it:
> E           AssertionError: 240.4: a 19-word docstring first line (committed, app/x.py::fresh) was not rejected naming it and its 19 words:
> E           AssertionError: 240.5: the worker's check does not list summary with its 28 words:
> 5 failed in 1.52s

`9. Bash`
```
until grep -qE "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output; do sleep 5; done; tail -12 /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output
```

> E       AssertionError: 240.1: the 28-word summary is not listed as over its cap: 'plan\n'
>         summary of two short sentences, each naming the summary. A passed worker card shows the summary, word for word,
> E       AssertionError: 240.2: a 31-word worker summary was not rejected naming it:
> E       AssertionError: 240.3: a 31-word review summary was not rejected naming it:
> E           AssertionError: 240.4: a 19-word docstring first line (committed, app/x.py::fresh) was not rejected naming it and its 19 words:
> E           AssertionError: 240.5: the worker's check does not list summary with its 28 words:
> 5 failed in 1.59s

**Agent:** The five new tests all fail today for the right reason. Next I'm running the full suite to check the existing tests the plan changed.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 550 python3 -m pytest -q -x --deselect tests/test_summary_caps.py -p no:cacheprovider tests/test_run_cards.py tests/test_handback_check.py tests/test_review_asks.py 2>&1 | tail -5
```

> ...............................                                          [100%]
> 31 passed in 7.21s

`11. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five criteria, one per line of the issue, with one test each in tests/test_summary_caps.py.",
          "The planner shortened two kept sample summaries and dropped the cause-sentence checks from two card tests."],
  "decided": ["A summary with a second sentence is rejected for the planner, worker and reviewer, however short.",
              "The worker's docstrings are found by comparing the branch with PLANNER_BASE, and the worker's prompt line asks for one sentence."],
  "open": ["One question: whether a second sentence rejects the planner's and reviewer's summaries too."]},
 "verdict": "approve",
 "summary": "The plan keeps all five asks of the issue, and each of its five tests fails today because the caps are missing.",
 "blockers": [],
 "notes": [
  {"text": "The docstring test never has the worker edit only the body of the older function; a check that flags every docstring in a touched function would still pass.",
   "evidence": "tests/test_summary_caps.py::test_each_docstring_the_worker_adds_or_changes_opens_with_at_most_15_words only appends to app/x.py or rewrites kept's docstring; old() is never edited."},
  {"text": "On a real run, PLANNER_BASE is the merge base with main, so the worker's check also reads the docstrings the planner's tests added on the branch; they are held to the same 15-word cap by story 1, so this should pass.",
   "evidence": ".github/workflows/agent.yml:149 sets PLANNER_BASE=$(git merge-base HEAD origin/main)."}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "The planner's summary is one sentence of at most 25 words.", "source": "https://github.com/dokima-dev/dokima/issues/240", "criterion": "240.1"},
  {"ask": "The worker's card opens with its summary, one sentence of at most 25 words, with no second sentence.", "source": "https://github.com/dokima-dev/dokima/issues/240", "criterion": "240.2"},
  {"as
```

> (Bash completed with no output)

**Agent:** I approved the plan for #240. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Asks:** each of the issue's five asks maps to its own criterion (240.1 to 240.5), and none is missing.
- **Tests:** all five new tests in `tests/test_summary_caps.py` fail today because the feature isn't built yet, not because of a crash or a bad setup. For example, a 31-word worker summary is not rejected, and a 19-word docstring first line is not named.
- **Changed tests:** the three changed test files (31 tests) still pass.
- **The plan's one question** asks whether a summary with a second sentence should be rejected for the planner and reviewer too, not just the worker. I accepted the planner's "yes". The issue's own words cover it: "The owner opens every planner, worker and reviewer card on one short plain sentence instead of a changelog." Rejecting a second sentence doesn't change how the steps flow or what a run costs.

I left two notes, neither of which blocks:
1. The docstring test never has the worker edit only the body of an older function. So a check that wrongly flags every docstring in a touched function would still pass.
2. On a real run, the worker's check compares the branch against where it split from main (`.github/workflows/agent.yml:149`). That means it also reads the docstrings the planner's tests added. Those are already held to the same 15-word cap by story 1 (#239), so they should pass.

I started a run of the whole test suite in the background but never read its results, so I don't know whether the full suite passes.

`12. Bash`
```
tail -10 /tmp/claude-1001/-home-runner-work-dokima-dokima/2cdd4cc3-9be2-453e-a091-05338c233ca1/tasks/b00wxwo1y.output
```

> FAILED tests/test_summary_caps.py::test_each_docstring_the_worker_adds_or_changes_opens_with_at_most_15_words - AssertionError: 240.4: a 19-word docstring first line (committed, app/x.py::fresh) was not rejected naming it and its 19 words:
>   
> assert (0 == 1)
> FAILED tests/test_summary_caps.py::test_the_worker_and_reviewer_checks_list_every_text_over_its_cap_and_reject_only_past_20_percent - AssertionError: 240.5: the worker's check does not list summary with its 28 words:
>   
> assert None
>  +  where None = line_naming('', 'summary', 28)
> 5 failed, 500 passed in 330.89s (0:05:30)
> 
> [exited with code 0]

**Agent:** The full test suite has now finished: 500 passed and 5 failed. The 5 failures are exactly the new tests for #240, each failing because the caps aren't built yet. No existing test broke.

So the approval stands, and `/tmp/dokima-out/review.json` needs no change.
