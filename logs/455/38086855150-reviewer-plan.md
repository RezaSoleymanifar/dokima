# reviewer (plan) for #455

Run: https://github.com/dokima-dev/dokima/actions/runs/38086855150

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; cat open_blockers.json; cat plan.json
```

> total 36
> drwxr-xr-x 2 runner runner 4096 Oct 10 21:14 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 21:14 ..
> -rw-r--r-- 1 runner runner 5871 Oct 10 21:14 01-planner.json
> -rw-r--r-- 1 runner runner 2934 Oct 10 21:14 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1980 Oct 10 21:14 03-worker.json
> -rw-r--r-- 1 runner runner 2784 Oct 10 21:14 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5681 Oct 10 21:14 05-planner.json
> # Issue #455: Raises come off the card; the status line says what needs the owner and links to where it was raised
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 456 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> The card stops listing raises; its status line counts the questions or blockers waiting on the owner and links to where they were raised.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/455 · https://github.com/dokima-dev/dokima/pull/465 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/465/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Two readings:** Should the check against GitHub's real rendering call GitHub's markdown API in CI, or use its answers recorded in the repo with a way to refresh them? The plan assumes reco

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; git show HEAD -- tests/ | head -150; sed -n 25,70p dokima/fence.py; ls docs/rendered 2>&1; cat /tmp/pack/in/02-reviewer-plan.json | head -60
```

> commit 2293d7b8df4a69e91f9554721b6a41504cad4b22
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 21:14:14 2026 +0000
> 
>     planner for #455 (run 38086746002)
> 
>  tests/github_render.py           | 10 ++++++----
>  tests/test_card_raises_status.py |  2 +-
>  2 files changed, 7 insertions(+), 5 deletions(-)
> commit 2293d7b8df4a69e91f9554721b6a41504cad4b22
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 21:14:14 2026 +0000
> 
>     planner for #455 (run 38086746002)
> 
> diff --git a/tests/github_render.py b/tests/github_render.py
> index 73de115..966dbb9 100644
> --- a/tests/github_render.py
> +++ b/tests/github_render.py
> @@ -2,8 +2,10 @@
>  
>  The owner asked that anything about how GitHub displays text is checked against GitHub's real rendering, not only
>  against the raw text the code writes. Tests run in CI with no network and no secrets, so each answer of GitHub's
> -markdown API (POST https://api.github.com/markdown, mode gfm) is recorded once in tests/github_render/<name>.json,
> -keyed by the exact markdown and the repo it was rendered for. A test asks `rendered(markdown, name)`:
> +markdown API (POST https://api.github.com/markdown, mode gfm) is recorded once in docs/rendered/<name>.json,
> +keyed by the exact markdown and the repo it was rendered for. The recordings live outside tests/ because they record
> +what the built code writes: the worker records them after building, and code drops ever

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 -- tests/github_render.py; ls tests/github_render 2>&1; grep -rn "github_render\|rendered(" tests/*.py | grep -v "^tests/github_render.py" | head; git ls-files | grep -i render; git diff main --stat
```

> 2293d7b planner for #455 (run 38086746002)
> b430559 planner for #455 (run 38083231866)
> ls: cannot access 'tests/github_render': No such file or directory
> tests/test_card_raises_status.py:22:tests/github_render.py: the answers of GitHub's markdown API recorded in docs/rendered/455.json for the exact
> tests/test_card_raises_status.py:37:import github_render  # noqa: E402
> tests/test_card_raises_status.py:376:def test_as_github_renders_the_card_no_raise_shows_and_the_words_link_to_their_comment(record_property, case, steps,
> tests/test_card_raises_status.py:392:    page = read(github_render.rendered(text, "455"))
> tests/test_card_raises_status.py:406:            github_render.rendered(text + " ", "455")
> tests/github_render.py
>  dokima/card.py                   |  37 ++--
>  tests/github_render.py           |  69 +++++++
>  tests/test_card_raises_status.py | 406 +++++++++++++++++++++++++++++++++++++++
>  tests/test_raised_cards.py       |  64 +-----
>  4 files changed, 508 insertions(+), 68 deletions(-)

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_raises_status.py tests/test_raised_cards.py 2>&1 | tail -15
```

> </details>
> 
> **Scope:** `dokima/agent.py`
> 
> <details><summary><b>Out of scope</b></summary>
> 
> - The board.
> 
> </details>
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <a href="https://github.com/o/r/actions/runs/7"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"></a> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 2 failed, 40 passed in 0.22s

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_raises_status.py 2>&1 | grep -E "FAILED|not recorded|Failed:" | head; rm -rf /tmp/rv && git worktree add -q /tmp/rv HEAD && cd /tmp/rv && DOKIMA_RECORD_RENDER=1 timeout 120 python3 -m pytest -q tests/test_card_raises_status.py 2>&1 | tail -2; ls docs/rendered; python3 -m pytest -q tests/test_card_raises_status.py 2>&1 | tail -2; python3 -c "from dokima.fence import is_test; print(is_test('docs/rendered/455.json'))"
```

> >       pytest.fail(f"GitHub's rendering of this exact text is not recorded in docs/rendered/{name}.json, so it "
> E       Failed: GitHub's rendering of this exact text is not recorded in docs/rendered/455.json, so it cannot be checked; record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test. The text:
> >       pytest.fail(f"GitHub's rendering of this exact text is not recorded in docs/rendered/{name}.json, so it "
> E       Failed: GitHub's rendering of this exact text is not recorded in docs/rendered/455.json, so it cannot be checked; record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test. The text:
> FAILED tests/test_card_raises_status.py::test_as_github_renders_the_card_no_raise_shows_and_the_words_link_to_their_comment[plan] - Failed: GitHub's rendering of this exact text is not recorded in docs/rendered/455.json, so it cannot be checked; record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test. The text:
> FAILED tests/test_card_raises_status.py::test_as_github_renders_the_card_no_raise_shows_and_the_words_link_to_their_comment[code-review] - Failed: GitHub's rendering of this exact text is not recorded in docs/rendered/455.json, so it cannot be checked; record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test. The text:
> ....................                                                     [100%]
> 20 passed in 0.44s
> 455.json
> ....................                                                     [100%]
> 20 passed in 0.05s
> Fa

**Agent:** Checking the planner's fix works: the recording now lands outside tests/, so the worker's fence keeps it. Next I'll check that the test still fails against the old card code.

`6. Bash`
```
cd /tmp/rv && git checkout -q main -- dokima/card.py && rm -rf docs/rendered && DOKIMA_RECORD_RENDER=1 timeout 120 python3 -m pytest -q tests/test_card_raises_status.py 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-200; git checkout -q HEAD -- dokima/card.py
```

> E             - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Retry:** Should a failed job be retried once?
> E             **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <a href="http
>         shows its own to-do, or none. Beside each, the same run with one question for the owner, passed and newest, does
>         shows its own to-do, or none. Beside each, the same run with one question for the owner, passed and newest, does
>         shows its own to-do, or none. Beside each, the same run with one question for the owner, passed and newest, does
>         shows its own to-do, or none. Beside each, the same run with one question for the owner, passed and newest, does
> E         - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Retry:** Should a failed job be retried once? · 
> E         **Definition of Done:** <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <a href="https://
> FAILED tests/test_card_raises_status.py::test_the_card_lists_no_raise_and_each_stays_in_its_comment[after a planner raised a question and an issue] - AssertionError: 455.1: after a planner raised a qu
> FAILED tests/t

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/rv; mkdir -p /tmp/dokima-out; python3 - <<'EOF'
import json
I="https://github.com/dokima-dev/dokima/issues/455"
asks=[
 ("The card lists no raises: questions, blockers and issues found stay only in the comment that raised them.","455.1"),
 ("When the river stops for raises sent to the owner, the status line says so with the count, such as \"Needs you: answer 2 questions\". It links to the comment that raised them.","455.2"),
 ("A plan whose questions for the owner are raises shows that to-do, not \"See the newest record below\" (#401).","455.3"),
 ("The same raise is counted once, however many records carry it (#388's card showed one question twice).","455.4"),
 ("As GitHub renders the card, no raise's text shows on it, and the status line's words link to the comment that raised them. This is checked on GitHub's own rendering of what the code writes, not only on the raw text.","455.5"),
 ("Your assumption is fine: use GitHub's answers recorded in the repo, refreshed by a script, as #452 does.","455.5"),
]
r={"previous_step":{
 "did":["The planner moved GitHub's recorded rendering for 455.5 from tests/github_render/455.json to docs/rendered/455.json, outside tests/, so the worker's recording reaches the pull request.",
        "The planner pointed tests/github_render.py and the plan's scope at the new path; the five criteria are otherwise unchanged."],
 "decided":["The worker records docs/rendered/455.json after building, with DOKIMA_RECORD_RENDER=1, as the owner approved."],
 "open":[]},
 "verdict":"approve",
 "summary":"The re-plan fixes the code review's blocker: the recording now lives outside tests/, so the worker's copy is kept, and with it recorded every test passes on the build and fails on main's card.",
 "raises":[],"answers":[],
 "asks":[{"ask":a,"source":I,"criterion":c} for a,c in asks]}
json.dump(r,open("/tmp/dokima-out/review.json","w"),indent=1)
EOF
python3 -m dokima.agent check revi
```

> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
p="/tmp/dokima-out/review.json"; r=json.load(open(p))
r["summary"]="The re-plan fixes the blocker: the recording now lives outside tests/, and once recorded every test passes on the build and fails on main."
json.dump(r,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 455 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK; git status --short
```

> OK

**Agent:** I approved the re-plan for #455 (taking raises off the card). The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**What the re-plan fixed:** The last code review on [#465](https://github.com/dokima-dev/dokima/pull/465) (the build for this issue) blocked on one problem. Criterion 455.5 needs GitHub's recorded rendering of the card, which the worker records after building. But code throws away every change a worker makes under `tests/`, so the recording never reached the pull request. The planner moved the recording to `docs/rendered/455.json`, pointed `tests/github_render.py` and the plan's scope at it, and left the five criteria otherwise unchanged.

**What I checked:**
- Code no longer treats `docs/rendered/455.json` as a test file, so the worker's recording will be kept.
- On the branch as it stands, 455.1 to 455.4 pass. 455.5 fails only because the recording isn't there yet, and the message names the command that records it.
- In a separate copy of the repo I recorded GitHub's rendering, which needs network but no key. All 20 tests then passed without network.
- With main's `dokima/card.py` and a fresh recording, all 20 tests failed, each because the feature is missing. So the tests catch the old behaviour.
- Your `/work` comment ("use GitHub's answers recorded in the repo, refreshed by a script, as #452 does") is carried by 455.5. I linked it to the issue rather than the comment itself, because I didn't have the comment's link.

I raised nothing and had no open blockers to answer. I added no files to the repo; the copy I used for recording has been removed.
