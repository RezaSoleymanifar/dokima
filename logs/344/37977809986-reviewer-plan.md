# reviewer (plan) for #344

Run: https://github.com/dokima-dev/dokima/actions/runs/37977809986

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 40
> drwxr-xr-x  3 runner runner 4096 Oct  9 19:05 .
> drwxrwxrwt 18 root   root   4096 Oct  9 19:05 ..
> drwxr-xr-x  2 runner runner 4096 Oct  9 19:05 in
> -rw-r--r--  1 runner runner 8837 Oct  9 19:05 issue.md
> -rw-r--r--  1 runner runner    2 Oct  9 19:05 open_blockers.json
> -rw-r--r--  1 runner runner   15 Oct  9 19:05 parent.json
> -rw-r--r--  1 runner runner 4561 Oct  9 19:05 plan.json
> 
> in:
> total 16
> drwxr-xr-x 2 runner runner 4096 Oct  9 19:05 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 19:05 ..
> -rw-r--r-- 1 runner runner 5204 Oct  9 19:05 01-planner.json
> # Issue #344: A merged PR's card is written and says Merged with the true Definition of Done
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [333], "loop": []} -->
> **Backlog**
> 
> [issue #344](https://github.com/dokima-dev/dokima/issues/344)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #333
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git show --stat HEAD; cat tests/test_no_size_cap.py; grep -n "shorter_than_before" -A30 tests/test_board_state.py | head -50; cat /tmp/pack/parent.json
```

> cd84ef3 planner for #344 (run 37977066131)
> b06c44b issue.md points to each record's file instead of repeating its JSON (#342)
> 09881bd The board's column and pills are always computed from the issue's state right now (#339)
> commit cd84ef31bcf008889692a50c3f8744a9a4479b50
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 19:05:09 2026 +0000
> 
>     planner for #344 (run 37977066131)
> 
>  tests/test_no_size_cap.py | 93 +++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 93 insertions(+)
> """No test caps how many lines dokima/agent.py or dokima/board.py may have (#344).
> 
> #331 added tests/test_board_state.py::test_the_board_code_is_shorter_than_before, which failed whenever board.py, or
> board.py and agent.py together, grew past their line counts of that day. The owner asked for it to go: a size limit is
> not a behavior, and it blocked work that had to add lines. These tests hold the repo to that: no test anywhere counts
> the lines of either file, the board's tests pass with both files much longer, and every other board test is kept.
> """
> import ast
> import glob
> import os
> import shutil
> import subprocess
> import sys
> 
> ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> CAPPED = ("dokima/agent.py", "dokima/board.py")
> # Every test tests/test_board_state.py held when #344 was planned, except the size cap the owner asked to remove.
> KEPT = ["test_any_event_puts_both_cards_where_the_issues_state_says",
>         "test_th

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "test_changes\|passing_today\|def fence" -r dokima/*.py | head -40
```

> dokima/fence.py:44:def fence(base, scope, clashed=()):
> dokima/planner.py:11:test_changes. Every new test has a one-sentence summary, names each criterion it proves by number below it, and fails
> dokima/planner.py:200:    tc = p.get("test_changes", {})
> dokima/planner.py:202:        raise Garbled("plan.json test_changes must map each changed older test to a non-empty reason")
> dokima/planner.py:205:                    "non_goals": p.get("out_of_scope", []), "scope": p["scope"], "test_changes": tc,
> dokima/planner.py:244:def test_changes(paths, before, after):
> dokima/planner.py:302:    out += [f"{t} is an older test the planner changed or deleted, with no reason in test_changes"
> dokima/planner.py:303:            for t in older if t not in plan["test_changes"]]
> dokima/planner.py:428:def passing_today(added, base="HEAD"):
> dokima/planner.py:466:        lines += [f"- `{t}`: {plan['test_changes'].get(t, 'no reason given')}" for t in older]
> dokima/planner.py:517:            tc = test_changes(paths, read_at(base), read_now)
> dokima/planner.py:528:            bad += unsummarized(tc["added"]) + unnumbered(tc["added"]) + passing_today(tc["added"], base)
> dokima/agent.py:409:                  ("Test changes", pairs(h.get("test_changes"))),

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 240,310p dokima/planner.py; sed -n 420,460p dokima/planner.py; sed -n 500,540p dokima/planner.py; sed -n 30,90p dokima/fence.py
```

> block.append(line)
>     return out
> 
> 
> def test_changes(paths, before, after):
>     """Tests the planner touched, by path::name: added, changed (with their old keys) and deleted.
> 
>     A test whose source is unchanged apart from its name is a rename: a change, filed under its old name, with its
>     new name under renamed (old -> new), a key that is there only when something was renamed.
>     """
>     added, changed, deleted, renamed = {}, {}, {}, {}
>     for path in paths:
>         old, new = test_functions(before(path)), test_functions(after(path))
>         gone = [name for name in old if name not in new]
>         for name, (src, keys) in new.items():
>             if name not in old:
>                 was = next((o for o in gone if old[o][0].replace(f"def {o}(", f"def {name}(", 1) == src), None)
>                 if was:
>                     gone.remove(was)
>                     changed[f"{path}::{was}"] = (old[was][1], keys)
>                     renamed[f"{path}::{was}"] = f"{path}::{name}"
>                 else:
>                     added[f"{path}::{name}"] = keys
>             elif old[name][0] != src:
>                 changed[f"{path}::{name}"] = (old[name][1], keys)
>         for name in gone:
>             deleted[f"{path}::{name}"] = old[name][1]
>     return dict({"added": added, "changed": changed, "deleted": deleted}, **({"renamed": renamed} if renamed else {}))
> 
> 
> def proving(tc):
>     """Each added or changed test with the keys it proves now."""
>     return dict(tc["added"], **{t: new for t, (_,

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 680,760p dokima/card.py; grep -n "merged\|Merged\|\"open\"\|state" dokima/card.py | head -60
```

> if follow(repo, number, before, now, cache):
>         sys.exit(1)
> 
> 
> def draw(repo, number, pr_number, plans=None, noted=None, cache=None):
>     """Write the card at the top of the issue and its PR.
> 
>     Returns the blocking links and loop its card showed before and shows now.
>     `plans` gives the links of a plan approved just now, by issue (see their_links). `noted` adds (True) or removes
>     (False) issues from the index of those whose approved plans link here. The Blocked by and Blocks lines are
>     GitHub's own blocked-by links, read now; `cache` keeps what this run already read.
>     """
>     cache = {} if cache is None else cache
>     issue = plan.fetch_issue(repo, number)
>     found = gather(repo, number, pr_number)
>     sources = set(linked_from(issue["current_body"]))
>     for s, on in (noted or {}).items():
>         (sources.add if on else sources.discard)(s)
>     found["sources"] = sorted(sources)
>     before, now = shown_links(issue["current_body"]), github_links(repo, int(number), cache)
>     found["blocking"] = now
>     if now.get("unread"):
>         found["unread"] = reason(blocking(repo, int(number), cache))
>     found["linked"] = {"relates_to": their_links(repo, number, found["sources"], plans)["relates_to"],
>                        "blocked_by": now.get("blocked_by") or [], "blocks": now.get("blocks") or []}
>     pr = found["pr"]
>     # Only the part above the marker is code's; the owner's ask below it is saved as it is, or the save is refused.
>     if body.save(repo, number, 

**Agent:** Checking the planner's claim that card.py already writes merged PR cards, then the #332 tests the owner asked to reuse.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 440,530p dokima/card.py; git fetch -q origin try/issue-332 2>&1|tail -2; git show origin/try/issue-332 --stat 2>&1 | head; git ls-tree origin/try/issue-332 tests/ | grep -E "card_now|hand_links"
```

> def pr_body(card, body):
>     """The PR's description: the card, then the line linking the issue, and nothing else."""
>     found = CLOSES.search(body or "")
>     return card + ("\n\n" + found.group(0) if found else "")
> 
> 
> def gh(*args):
>     return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
> 
> 
> def issue_pr(repo, n):
>     """The PR built for issue n from its try or work branch, or None."""
>     owner = repo.split("/")[0]
>     for branch in (f"try/issue-{n}", f"work/issue-{n}"):
>         prs = json.loads(gh("api", f"repos/{repo}/pulls?head={owner}:{branch}&state=all"))
>         if prs:
>             return prs[0]["number"]
>     return None
> 
> 
> def find_work(repo):
>     """The issue and open PR this event is about, as (issue number, PR number or None)."""
>     if os.environ.get("ISSUE_NUMBER"):
>         n = int(os.environ["ISSUE_NUMBER"])
>         return n, issue_pr(repo, n)
>     title = re.match(r"worker for #(\d+)$", os.environ.get("RUN_TITLE", ""))
>     if title:
>         n = int(title.group(1))
>         return n, issue_pr(repo, n)
>     pr = os.environ.get("PR_NUMBER")
>     if not pr:
>         prs = json.loads(gh("api", f"repos/{repo}/commits/{os.environ['HEAD_SHA']}/pulls"))
>         pr = prs[0]["number"] if prs else None
>     if not pr:
>         return None, None
>     return plan.pr_issue_number(repo, pr), int(pr)
> 
> 
> def latest_worker_run(repo, number):
>     runs = json.loads(gh("api", f"repos/{repo}/actions/workflows/worker.yml/runs?per_page=50"))["workflow_runs"]
>   

`7. Bash`
```
cd /home/runner/work/dokima/dokima; for f in test_card_now test_hand_links; do echo "== $f"; git show origin/try/issue-332:tests/$f.py | grep -nE "^def test|record_property\(\"proves" ; done; git show origin/try/issue-332:tests/test_card_now.py | grep -n -i "merged" | head -30
```

> == test_card_now
> 950:def test_any_event_about_the_issue_or_its_pr_redraws_both_cards_from_github_now(tmp_path, record_property):
> 957:    record_property("proves", "332.1")
> 972:def test_an_event_redraws_an_open_issue_and_its_pr_from_the_records_now(tmp_path, record_property):
> 979:    record_property("proves", "332.1")
> 1010:def test_records_redraw_the_cards_and_the_cards_own_writes_redraw_nothing(tmp_path, record_property):
> 1016:    record_property("proves", "332.1")
> 1042:def test_card_yml_starts_on_every_kind_of_event_about_an_issue_or_its_pr(tmp_path, record_property):
> 1050:    record_property("proves", "332.1")
> 1104:def test_the_sweep_puts_right_every_stale_issue_card_and_pr_card_open_or_closed(tmp_path, record_property):
> 1111:    record_property("proves", "332.2")
> 1135:def test_the_merge_rewrites_the_pr_card_as_merged_with_the_true_definition_of_done(tmp_path, record_property):
> 1142:    record_property("proves", "332.3")
> 1167:def test_a_pr_card_is_written_while_the_pr_is_open(tmp_path, record_property):
> 1172:    record_property("proves", "332.3")
> 1186:def test_each_issue_has_its_own_queue_and_one_issue_never_cancels_another(tmp_path, record_property):
> 1193:    record_property("proves", "332.4")
> 1221:def test_the_card_code_is_smaller_than_before(record_property):
> 1226:    record_property("proves", "332.5")
> 1234:def test_the_sweep_names_a_card_it_cannot_redraw_fails_and_puts_the_rest_right(tmp_path, record_property):
> 1239:    record_property("proves", "332.6")
> 1254:def test_a

`8. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/try/issue-332:tests/test_card_now.py | sed -n 1130,1185p; rm -rf /tmp/t332 && mkdir /tmp/t332 && git archive HEAD | tar -x -C /tmp/t332 && git show origin/try/issue-332:tests/test_card_now.py > /tmp/t332/tests/test_card_now.py && cd /tmp/t332 && timeout 300 python -m pytest -q -p no:cacheprovider tests/test_card_now.py -k "merge_rewrites or written_while_the_pr_is_open" 2>&1 | tail -30
```

> "332.2: a redraw after the sweep changed a PR card, so the sweep did not leave it as GitHub's state draws it"
> 
> 
> # 332.3 -----------------------------------------------------------------------------------------------------------
> 
> def test_the_merge_rewrites_the_pr_card_as_merged_with_the_true_definition_of_done(tmp_path, record_property):
>     """After the merge the PR card shows Merged with its true Definition of Done.
> 
>     PR #260 has every check passed and an approving code review, and the owner merges it: the merge event leaves
>     #260's card saying Merged with All tests, Code review and Owner approval passed. On a fresh GitHub where All tests
>     failed on the PR's last commit, the code review blocked and the bot merged it, the merge leaves Merged with All
>     tests failed, Code review failed and Owner approval not passed. Proves 332.3."""
>     record_property("proves", "332.3")
>     hub = Hub(tmp_path / "green")
>     hub.merge(246, 260)
>     must_redraw(hub, pr_event(246, 260, "closed", OWNER, merged=True), "332.3")
>     assert stage_of(hub.pr_body(260)) == "Merged", f"332.3: PR #260's card does not say Merged: {hub.pr_body(260)!r}"
>     done = done_of(hub.pr_body(260))
>     assert done == {"All tests": "passed", "Code review": "passed", "Owner approval": "passed"}, \
>         f"332.3: merged PR #260's Definition of Done is not every check passed: {done}"
>     hub = Hub(tmp_path / "red")
>     s = hub.load()
>     s["checks"]["sha260"][1].update(conclusion="failure")
>     blocked = re

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "^def main" -A45 dokima/card.py | head -70; grep -rn "card" .github/workflows/*.yml | grep -v "^.github/workflows/card.yml" | head; sed -n 1,40p .github/workflows/card.yml
```

> 667:def main():
> 668-    if sys.argv[1:2] == ["gallery"] and len(sys.argv) == 3:
> 669-        gallery(os.environ.get("REPO") or "dokima-dev/dokima", sys.argv[2])
> 670-        return
> 671-    repo = os.environ["REPO"]
> 672-    if not os.environ.get("ISSUE_NUMBER") and os.environ.get("GITHUB_EVENT_NAME") == "schedule":
> 673-        sys.exit(1 if sweep(repo) else 0)
> 674-    number, pr_number = find_work(repo)
> 675-    if not number:
> 676-        print("No issue for this event; nothing to write.")
> 677-        return
> 678-    cache = {}
> 679-    before, now = draw(repo, number, pr_number, cache=cache)
> 680-    if follow(repo, number, before, now, cache):
> 681-        sys.exit(1)
> 682-
> 683-
> 684-def draw(repo, number, pr_number, plans=None, noted=None, cache=None):
> 685-    """Write the card at the top of the issue and its PR.
> 686-
> 687-    Returns the blocking links and loop its card showed before and shows now.
> 688-    `plans` gives the links of a plan approved just now, by issue (see their_links). `noted` adds (True) or removes
> 689-    (False) issues from the index of those whose approved plans link here. The Blocked by and Blocks lines are
> 690-    GitHub's own blocked-by links, read now; `cache` keeps what this run already read.
> 691-    """
> 692-    cache = {} if cache is None else cache
> 693-    issue = plan.fetch_issue(repo, number)
> 694-    found = gather(repo, number, pr_number)
> 695-    sources = set(linked_from(issue["current_body"]))
> 696-    for s, on in (noted or {}).items():
> 697-        (

`10. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; grep -rn "345\|347" /home/runner/work/dokima/dokima/AGENTS.md | head
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "37977066131",
>  "commit_before": "b06c44b7fe97e65db672b32fdc1cfb3f6529507d",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 338834,
>   "turns": 39,
>   "cost_usd": 2.0945596000000006,
>   "tokens_in": 3158892,
>   "tokens_out": 29890
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/344/37977066131-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37977066131",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> Shell cwd was reset to /home/runner/work/dokima/dokima

`11. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 400 python -m pytest -q -p no:cacheprovider tests/test_no_size_cap.py tests/test_card_bullets.py::test_the_issue_and_pr_cards_are_identical_and_link_both_pages tests/test_card_records.py::test_the_issue_and_its_pr_show_the_same_card tests/test_card_status.py::test_merged_once_the_pr_is_merged tests/test_card_bullets.py::test_only_a_code_owners_merge_shows_owner_approval_passed tests/test_card_records.py::test_all_tests_shows_the_state_github_reports tests/test_card_records.py::test_a_missing_stale_or_unproven_review_never_shows_as_passed 2>&1 | grep -E "Error|passed|failed" | head
```

> E       AssertionError: 344.3: these tests still cap the line count of agent.py or board.py: tests/test_board_state.py::test_the_board_code_is_shorter_than_before
> tests/test_no_size_cap.py:68: AssertionError
> E       AssertionError: 344.3: with agent.py and board.py 3000 lines longer, tests/test_board_state.py fails:
> E         E       AssertionError: 331.5: dokima/board.py has 3445 lines, not fewer than the 446 it had before
> E         tests/test_board_state.py:634: AssertionError
> E         FAILED tests/test_board_state.py::test_the_board_code_is_shorter_than_before - AssertionError: 331.5: dokima/board.py has 3445 lines, not fewer than the 446 it had before
> E         1 failed, 18 passed in 1.42s
> E        +  where 1 = CompletedProcess(args=['/opt/hostedtoolcache/Python/3.12.15/x64/bin/python', '-m', 'pytest', '-q', '-p', 'no:cacheprov...py has 3445 lines, not fewer than the 446 it had before\nassert 3445 < 446\n1 failed, 18 passed in 1.42s\n', stderr='').returncode
> tests/test_no_size_cap.py:92: AssertionError
> FAILED tests/test_no_size_cap.py::test_no_test_caps_the_line_count_of_agent_py_or_board_py - AssertionError: 344.3: these tests still cap the line count of agent.py or board.py: tests/test_board_state.py::test_the_board_code_is_shorter_than_before

**Agent:** Both new tests fail today for the right reason: the cap is still there. I also confirmed that `card.py` already writes the PR card whether the PR is open, merged or closed. Writing the hand-back now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Wrote two tests that fail while any test caps the line count of dokima/agent.py or dokima/board.py, and pass once the cap is gone with every other board test kept.",
          "Filed six existing card tests as proof that a PR's card is written open, merged or closed and says Merged with the Definition of Done GitHub records."],
  "decided": ["The first two asks already hold on main (dokima/card.py:711), so no card code changes; the stale #246 card is left to #345 and #347."],
  "open": ["Asks whether the owner deletes the size-cap test by hand on try/issue-344, since neither the planner nor the worker can both delete it and prove it."]},
 "verdict": "approve",
 "summary": "The plan covers all three asks with tests that hold today or fail for the right reason, but only the owner can remove the size-cap test, so it waits for their answer.",
 "blockers": [],
 "notes": [
  {"text": "The owner asked to reuse #332's tests where they fit. Its two merged-PR tests (332.3) fail on main only because card.yml never starts on a pull request event. That trigger belongs to #345, so they don't fit here, but the plan never says this.",
   "evidence": "Ran origin/try/issue-332:tests/test_card_now.py -k 'merge_rewrites or written_while_the_pr_is_open' on main: both fail with 'card.yml does not start on pull_request_target closed/opened'."},
  {"text": "The no-cap scan only finds caps written as len(...splitlines()) or len(...readlines()) in a test that names one of the two files. The padding test only runs tests/test_board_state.py, so a cap written another way in a different file would slip past both tests.",
   "evidence": "tests/test_no_size_cap.py counts_lines() and line 88 run only tests/test_board_state.py."}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "A PR's card is written whether the PR is open or merged.", "source": "https://github.com/d
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> assumptions item 1 judges "Will you delete tests/test_board_state.py::test_the_board_code_is_shorter_than_before by hand on try/issue-344, or should the plan check let the planner's own deletion count?", which is not a question of the plan
> the assumption of "Only the planner may delete a test (the worker's fence undoes any test change), and the plan check refuses a new test that already passes, so no agent can both remove the size cap and prove it. Will you delete tests/test_board_state.py::test_the_board_code_is_shorter_than_before by hand on try/issue-344, or should the plan check let the planner's own deletion count?" must be judged exactly once in assumptions, {"question": "the plan's question", "accepted": true | false, "changes": true | false, "matched": "the owner's words", "source": "where they said them"} (or "why" when not accepted)
> rc=1

`13. Bash`
```
python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p)); plan=json.load(open('/tmp/pack/plan.json'))
r['summary']="The plan proves all three asks, but only the owner can delete the size-cap test, so it waits for their answer."
r['assumptions'][0]['question']=plan['questions'][0]['question']
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 344 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for #344. It still stops for you on its one question: whether you'll delete the size-cap test yourself on `try/issue-344`. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**Your first two asks already work on main.** The planner says no code needs to change for them, and that holds up:
- `dokima/card.py:711` writes the same card into the PR whether it is open, merged or closed.
- It finds the PR even after the merge.
- The merged card says Merged and shows All tests, Code review and Owner approval as GitHub records them.

The plan uses six existing card tests as proof of this.

**Why #246's card is still stale.** Nothing redraws a card after a merge: `card.yml` doesn't start when a pull request merges. The plan leaves that to #345 and #347, so a merged PR's card will stay stale until one of those lands. I couldn't open #345 or #347 to confirm what they cover.

**Removing the size cap needs you.** The planner's two new tests fail today for the right reason: the cap test still fails as soon as `board.py` grows. Neither agent can delete that test and still prove it's gone:
- When the plan is checked, the planner's own test deletion is in place, so its new tests would already pass, and the check refuses new tests that pass.
- The worker's test-file changes are always undone.

I didn't let the river go on with "you delete it by hand", because you never said that. To go on, either delete only `tests/test_board_state.py::test_the_board_code_is_shorter_than_before` on `try/issue-344`, or reply with `/plan` and your words.

Two notes, neither blocking:
- **#332's tests weren't reused.** You asked to reuse them where they fit. Its two merged-PR tests fail on main only because `card.yml` doesn't start on a pull request event, which is #345's job, so they don't fit here. The plan never says this.
- **The new no-cap test is narrow.** It only catches a cap written one particular way. A cap written another way in a different test file would slip past both new tests.
