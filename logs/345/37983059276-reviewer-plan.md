# reviewer (plan) for #345

Run: https://github.com/dokima-dev/dokima/actions/runs/37983059276

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (31.1KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b166a3e8-b1a0-47a3-a18e-e64c4e6519a3/tool-results/bo4bbfxhn.txt
> 
> Preview (first 2KB):
> .:
> total 56
> drwxr-xr-x  3 runner runner  4096 Oct  9 19:51 .
> drwxrwxrwt 18 root   root    4096 Oct  9 19:51 ..
> drwxr-xr-x  2 runner runner  4096 Oct  9 19:51 in
> -rw-r--r--  1 runner runner 26884 Oct  9 19:51 issue.md
> -rw-r--r--  1 runner runner     2 Oct  9 19:51 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct  9 19:51 parent.json
> -rw-r--r--  1 runner runner  4163 Oct  9 19:51 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  9 19:51 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 19:51 ..
> -rw-r--r-- 1 runner runner 3874 Oct  9 19:51 01-planner.json
> -rw-r--r-- 1 runner runner 3551 Oct  9 19:51 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 1439 Oct  9 19:51 03-worker.json
> -rw-r--r-- 1 runner runner 3404 Oct  9 19:51 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4791 Oct  9 19:51 05-planner.json
> # Issue #345: Merging a PR redraws its card and its issue's card
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 344 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> Merging a pull request redraws its card and its issue's card, so neither keeps a card read just before the merge.
> 
> **Review**
> 
> [issue #345](https://github.com/dokima-dev/dokima/issues/345) · [PR #351](https://github.com/dokima-dev/dokima/pull/351) · <img src="https://

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-original\|Original\|<!-- dokima-ask/,$p' issue.md | head -400
```

> <!-- dokima-ask -->
> 
> Nothing redraws a card when a PR is merged, so the last redraw may come from a run that read the PR just before the merge.
> 
> What I want:
> - Merging a PR redraws that PR's card and its issue's card.
> - #246's and #312's cards show Merged once this ships, without anyone clicking anything.
> 
> Small fix, added on top of today's card code. Do not rewrite card.py and do not delete code beyond what this fix needs. Keep it one user story. #332's planner already wrote tests for this on branch try/issue-332 (tests/test_card_now.py and tests/test_hand_links.py): reuse the ones that fit instead of writing new ones.
> 
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #345 (2026-10-09T19:33:45Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #345 (2026-10-09T19:34:12Z)
> 
> Autopilot: switched on, starting plan
> 
> ### dokima-runtime on issue #345 (2026-10-09T19:34:15Z)
> 
> Autopilot is on for #345. Planning started for #345, which wait on nothing open.
> 
> 
> ### dokima-runtime on issue #345 (2026-10-09T19:34:26Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **User story:** When a pull request merges, by the owner or by Dokima on autopilot, its card and its issue's card both say Merged right

`3. Bash`
```
cd /tmp/pack; cat plan.json parent.json; echo; for f in in/*; do echo "== $f"; cat $f; echo; done
```

> {
>  "kind": "user_story",
>  "summary": "Merging a pull request redraws its card and its issue's card, so neither keeps a card read just before the merge.",
>  "user_story": "When a pull request merges, by the owner or by Dokima on autopilot, its card and its issue's card both say Merged right away, with no one doing anything else.",
>  "acceptance_criteria": [
>   {
>    "text": "Merging a pull request, by the owner or by Dokima on autopilot, redraws its card and its issue's card, both saying Merged. The pull request keeps its closing line, and no other card changes. Only a merge does this: a pull request closed without merging, by the owner or by the bot, redraws no card.",
>    "source": "https://github.com/dokima-dev/dokima/issues/345"
>   },
>   {
>    "text": "PR #246's and PR #312's cards say Merged after their merge, with nothing else done. Each shows All tests, Code review and Owner approval passed, and its issue's card (#239, #283) says Merged too.",
>    "source": "https://github.com/dokima-dev/dokima/issues/345"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "The redraw on a merge runs main's card.yml and card code, never the code of the pull request being merged.",
>    "why": "A pull request's own copy runs with the code under review, and the card run holds the bot's key.",
>    "principle": "Humans are free; bots are compliant: agents can't change the workflows that judge them."
>   }
>  ],
>  "scope": [
>   ".github/workflows/card.yml",
>   "dokima/card.py"
>  ],
>  "out_of_scope": [
>   "Giving each is

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git diff main --stat; git show da3d06f --stat; git diff main -- .github; python3 -m pytest -q tests/test_card_merge.py 2>&1 | tail -20
```

> .github/workflows/card.yml |   12 +-
>  tests/test_card_merge.py   | 1052 ++++++++++++++++++++++++++++++++++++++++++++
>  2 files changed, 1060 insertions(+), 4 deletions(-)
> commit da3d06f0214400b3139325226a6aac4c4159c406
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 19:51:02 2026 +0000
> 
>     planner for #345 (run 37982659623)
> 
>  tests/test_card_merge.py | 26 ++++++++++++++++++++++++++
>  1 file changed, 26 insertions(+)
> diff --git a/.github/workflows/card.yml b/.github/workflows/card.yml
> index 9324eb9..4ebe62c 100644
> --- a/.github/workflows/card.yml
> +++ b/.github/workflows/card.yml
> @@ -3,7 +3,8 @@ name: card
>  # worker finish, or a person changes or comments on an issue; the cards of the
>  # issues it blocks or is blocked by follow when their links changed. GitHub
>  # announces no event for a blocked-by link added or removed by hand, so a run
> -# every 15 minutes catches up the cards whose links changed. These triggers
> +# every 15 minutes catches up the cards whose links changed. A merged pull request redraws its card and its issue's,
> +# whoever merged it. These triggers
>  # always use the default branch's copy of this file and of dokima/card.py, so
>  # the work being judged cannot change how it is reported.
>  on:
> @@ -12,6 +13,8 @@ on:
>      types: [completed]
>    issues:
>    issue_comment:
> +  pull_request_target:
> +    types: [closed]
>    schedule:
>      - cron: '*/15 * * * *'
>  concurrency:
> @@ -27,8 +30,9 @@ jobs:
>    card:
>      environmen

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 975,1052p tests/test_card_merge.py
```

> hub = Hub(tmp_path)
>     for event in (pr_event(239, 246, "edited", "bot"), pr_event(283, 312, "edited", "bot")):
>         r = Run(hub, *event)
>         assert not (r.started and r.card_ran()), \
>             f"345.1: the bot's own edit of PR #{event[1]['number']} ran card.yml's card job, so card writes loop"
>     r = Run(hub, *pr_event(283, 312, "closed", "bot", merged=True))
>     assert r.started and r.card_ran(), "345.1: beside the edits, a merge did not run card.yml's card job"
> 
> 
> def test_closing_a_pr_without_merging_redraws_nothing(tmp_path, record_property):
>     """Only a merge redraws: a pull request closed unmerged leaves every card as it was.
> 
>     PR #312 is closed on GitHub without merging, once by the owner and once by Dokima's bot. Neither close event runs
>     card.yml's card job, directly or through a relay, and issue #283's and PR #312's bodies stay exactly as they were.
>     Beside them, the merge of PR #246 does run the card job, so the check never passes by redrawing nothing at all.
>     Proves 345.1."""
>     record_property("proves", "345.1")
>     for who in ("owner", "bot"):
>         hub = Hub(tmp_path / who)
>         s = hub.load()
>         s["prs"]["312"].update(state="closed", merged=False, closed_at="2026-10-09T09:00:00Z",
>                                updated_at="2026-10-09T09:00:00Z")
>         hub.save()
>         before = (hub.issue_body(283), hub.pr_body(312))
>         r = hub.run(*pr_event(283, 312, "closed", OWNER if who == "owner" else "bot", merged=False), "345

**Agent:** Now verify the suggested fix passes all tests, and the tests fail on main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/rv; git worktree add -q /tmp/rv HEAD 2>&1; cd /tmp/rv; sed -i "s/|| (github.event.sender.type != 'Bot' \&\& !github.event.issue.pull_request/|| (github.event_name != 'pull_request_target' \&\& github.event.sender.type != 'Bot' \&\& !github.event.issue.pull_request/" .github/workflows/card.yml; git diff --stat; python3 -m pytest -q tests/test_card_merge.py 2>&1|tail -2; git checkout -q main -- .github/workflows/card.yml; python3 -m pytest -q tests/test_card_merge.py 2>&1|tail -8; git checkout -q HEAD -- .; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/rv
```

> .github/workflows/card.yml | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> ......                                                                   [100%]
> 6 passed in 4.05s
>  +  where False = <test_card_merge.Run object at 0x7faa575791c0>.started
> FAILED tests/test_card_merge.py::test_prs_246_and_312_show_merged_after_their_merge_with_no_click - AssertionError: 345.2: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> assert False
>  +  where False = <test_card_merge.Run object at 0x7faa57678b90>.started
> FAILED tests/test_card_merge.py::test_the_merge_redraw_runs_mains_code - AssertionError: 345.3: card.yml does not start on pull_request_target closed, so the cards are not redrawn
> assert False
>  +  where False = <test_card_merge.Run object at 0x7faa5757bc50>.started
> 6 failed in 0.14s

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Added a test that a pull request closed without merging, by the owner or by the bot, runs no card redraw and leaves its card and its issue's card as they were, with a merge beside it that does redraw.",
          "Changed 345.1 to say only a merge redraws: a pull request closed without merging redraws no card."],
  "decided": ["The fix stays in card.yml: keep every pull request close that is not a merge out of the card job's last rule, with no card.py change expected."],
  "open": []},
 "verdict": "approve",
 "summary": "The re-plan answers the code review's blocker: a new test proves a pull request closed without merging redraws nothing, it fails today for that reason, and a one-line card.yml change passes all six tests.",
 "blockers": [],
 "notes": [
  {"text": "I checked the new test: on the branch it fails only because an owner's unmerged close runs the card job; with `github.event_name != 'pull_request_target' &&` added to the job's last rule, all six tests pass; on main all six fail because no merge starts card.yml.",
   "evidence": "python3 -m pytest -q tests/test_card_merge.py: branch 1 failed, 5 passed (test_closing_a_pr_without_merging_redraws_nothing: 'PR #312 closed without merging by the owner ran card.yml's card job'); with the one-line change 6 passed; with main's card.yml 6 failed"},
  {"text": "The owner asked that #246's and #312's own cards show Merged once this ships. Both are already merged, so this change never runs for them again; the plan relies on their cards already saying Merged since #350. Whoever approves the result should look at both cards.",
   "evidence": "plan.json concerns[1]; card.yml starts only on pull_request_target closed, which a merged pull request never sends again"},
  {"text": "The fix changes a workflow file, so on autopilot the pull request stops for the owner before it merges.",
   "evidence": "plan.json scope lists .gith
```

> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The re-plan adds a test that an unmerged close redraws nothing; it fails today for that reason, and a one-line card.yml change passes all six."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 345 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the re-plan for #345. The hand-back is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

**What changed since last round:** In code review I had blocked because closing a pull request without merging it also redrew the cards, and the plan says it must not. The planner fixed this in two places:
- Criterion 345.1 now says only a merge redraws, and a pull request closed without merging (by the owner or the bot) redraws no card.
- A new test, `tests/test_card_merge.py::test_closing_a_pr_without_merging_redraws_nothing`, checks that an unmerged close changes no card. Next to it, a merge has to redraw, so the test can't pass by redrawing nothing at all.

**What I ran:**
- **This branch:** the new test fails for the right reason: "PR #312 closed without merging by the owner ran card.yml's card job". The other 5 pass.
- **This branch, with one line added to card.yml:** I added `github.event_name != 'pull_request_target' &&` to the job's last `if:` rule, and all 6 tests pass.
- **main:** all 6 fail, because nothing starts card.yml on a merge there.

Both of your asks map to a criterion: the merge redraw is 345.1, and #246's and #312's cards showing Merged is 345.2. The plan has no questions for you.

**Things to check yourself before approving the result:**
- Look at #246's and #312's cards on GitHub. Both pull requests merged before this fix, so the new trigger will never run for them. The plan relies on their cards already saying Merged since #350, and its tests only use made-up stand-ins for those two pull requests.
- The fix changes `.github/workflows/card.yml`, so on autopilot the pull request will stop for you before it merges.
