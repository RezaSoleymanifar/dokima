# reviewer (plan) for #282

Run: https://github.com/dokima-dev/dokima/actions/runs/37872991409

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (111.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/d9b476d2-757c-41a9-974a-24cca6cde1f2/tool-results/b3fpg3swx.txt
> 
> Preview (first 2KB):
> .:
> total 136
> drwxr-xr-x  3 runner runner   4096 Oct  9 02:06 .
> drwxrwxrwt 18 root   root     4096 Oct  9 02:06 ..
> drwxr-xr-x  2 runner runner   4096 Oct  9 02:06 in
> -rw-r--r--  1 runner runner 112921 Oct  9 02:06 issue.md
> -rw-r--r--  1 runner runner      2 Oct  9 02:06 open_blockers.json
> -rw-r--r--  1 runner runner   6693 Oct  9 02:06 plan.json
> 
> in:
> total 76
> drwxr-xr-x 2 runner runner 4096 Oct  9 02:06 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 02:06 ..
> -rw-r--r-- 1 runner runner 5771 Oct  9 02:06 01-planner.json
> -rw-r--r-- 1 runner runner 5335 Oct  9 02:06 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7410 Oct  9 02:06 03-planner.json
> -rw-r--r-- 1 runner runner 4838 Oct  9 02:06 04-reviewer-plan.json
> -rw-r--r-- 1 runner runner 7113 Oct  9 02:06 05-planner.json
> -rw-r--r-- 1 runner runner 4512 Oct  9 02:06 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2080 Oct  9 02:06 07-worker.json
> -rw-r--r-- 1 runner runner 2545 Oct  9 02:06 08-reviewer-pr.json
> -rw-r--r-- 1 runner runner  361 Oct  9 02:06 09-updater.json
> -rw-r--r-- 1 runner runner 7346 Oct  9 02:06 10-planner.json
> # Issue #282: Everything Dokima needs from GitHub is declared in one manifest in code
> 
> <!-- dokima-card -->
> Every label, board field and option, view, required check, branch rule and app permissio

`2. Bash`
```
cd /tmp/pack; grep -n "^#\|^## \|^### \|^---\|Comment\|comment by\|^\*\*@" issue.md | head -100; wc -l issue.md
```

> 1:# Issue #282: Everything Dokima needs from GitHub is declared in one manifest in code
> 96:## Comments
> 98:### dokima-runtime on issue #282 (2026-10-08T23:01:40Z)
> 102:### dokima-runtime on issue #282 (2026-10-08T23:01:52Z)
> 281:### dokima-runtime on issue #282 (2026-10-08T23:10:36Z)
> 428:### dokima-runtime on issue #282 (2026-10-08T23:12:01Z)
> 627:### dokima-runtime on issue #282 (2026-10-08T23:19:09Z)
> 781:### RezaSoleymanifar on issue #282 (2026-10-08T23:48:30Z)
> 785:### dokima-runtime on issue #282 (2026-10-08T23:48:50Z)
> 973:### dokima-runtime on issue #282 (2026-10-08T23:57:59Z)
> 1118:### dokima-runtime on issue #282 (2026-10-08T23:59:18Z)
> 1123:### dokima-runtime on issue #282 (2026-10-08T23:59:20Z)
> 1187:### dokima-runtime on PR #288 (2026-10-09T00:12:56Z)
> 1281:### dokima-runtime on PR #288 (2026-10-09T02:02:24Z)
> 1285:### dokima-runtime on issue #282 (2026-10-09T02:02:26Z)
> 1324:### dokima-runtime on issue #282 (2026-10-09T02:02:40Z)
> 1518:### dokima-runtime on issue #282 (2026-10-09T02:06:32Z)
> 1526 issue.md
> Shell cwd was reset to /home/runner/work/dokima/dokima

`3. Bash`
```
cd /tmp/pack; sed -n 1,97p issue.md | grep -v "^<img" ; sed -n 775,800p issue.md; sed -n 1180,1330p issue.md; sed -n 1510,1526p issue.md
```

> # Issue #282: Everything Dokima needs from GitHub is declared in one manifest in code
> 
> <!-- dokima-card -->
> Every label, board field and option, view, required check, branch rule and app permission Dokima relies on is declared in one manifest file, and a test catches code that relies on anything left out.
> 
> **Review** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See why not every check passed
> 
> [issue #282](https://github.com/dokima-dev/dokima/issues/282) · [PR #288](https://github.com/dokima-dev/dokima/pull/288) · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/288/files)
> 
> 
> **User story:** The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a test catches code that relies on anything left out.
> 
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/failed.svg" width="16" height="16" align="absmiddle" alt="failed"> **Acceptance criterion:** <a href="https://github.com/dokima-dev/dokima/actions/runs/37863601453/job/113632610820">One manifest, `dokima/manifest.py`, declares the labels, board fields and options, views, required checks, branch rules and app permissions Dokima ne

`4. Bash`
```
cd /tmp/pack; cat plan.json; python3 -c "
import json;d=json.load(open('in/10-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:2000]); h=d['handback']; print(h.keys()); print(json.dumps({k:h[k] for k in h if k not in ('criteria',)},indent=1)[:3000])"
```

> {
>  "kind": "user_story",
>  "summary": "One manifest file declares every GitHub setting and app permission Dokima relies on, and a test catches code relying on anything left out.",
>  "user_story": "The owner can read in one file every label, board field and option, view, required check, branch rule and app permission Dokima relies on, and a test catches code that relies on anything left out.",
>  "acceptance_criteria": [
>   {
>    "text": "One manifest, `dokima/manifest.py`, declares the labels, board fields and options, views, required checks, branch rules and app permissions Dokima needs. Labels: plan, work, autopilot, blocker, high, parked. Fields: Status (Backlog, Plan, Work, Review, Done), Action (Needs you, Autopilot), Priority (Blocker, High, Parked). View: Autopilot, a table. Required checks: \"all tests\" and \"all done-whens passed\", which main's branch rule requires. Every label and option has a color and description.",
>    "source": "https://github.com/dokima-dev/dokima/issues/282"
>   },
>   {
>    "text": "The manifest declares the Autopilot option as purple, described \"Running on its own\", and the Autopilot view's filter as `label:autopilot is:open`. The board takes that filter from the manifest both when it adds the view and when it moves an Autopilot view still on the old `label:autopilot` filter, so changing the manifest changes both.",
>    "source": "https://github.com/dokima-dev/dokima/issues/282"
>   },
>   {
>    "text": "A test fails when a workflow or Dokima's code relie

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --graph --all | head -30; git show --stat HEAD | head -20; git merge-base --is-ancestor origin/main HEAD && echo main-included; git log --oneline -3 origin/main
```

> * 55e49a5 Conversation of run 37872658551
> * dfc3658 Conversation of run 37871828800
> * aea1628 Conversation of run 37871310094
> * 686c720 Conversation of run 37871687964
> * 2c0062b Conversation of run 37871501057
> * ca55de5 Conversation of run 37871436607
> * 9f3e0ac Conversation of run 37871278316
> * 2e6c4ca Conversation of run 37870801035
> commit c0f0e8edf8bbb66c821e98ea33af6073baa25520
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:06:18 2026 +0000
> 
>     planner for #282 (run 37872658551)
> 
>  tests/test_autopilot_board.py |  2 +-
>  tests/test_manifest.py        | 39 +++++++++++++++++++++++++++++++++++++++
>  2 files changed, 40 insertions(+), 1 deletion(-)
> bf41093 Once the plan passes review, code records its links on both issues and redraws both cards (#290)
> a302cb1 The Autopilot view shows only open issues and pull requests (#286)
> 1c8e0e0 The issue card and the planner's run comment show the links, each kind with its own icon (#281)

**Agent:** Reviewing the re-plan for #282: checking the new test against the branch merged with main.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/ ; git show origin/main:dokima/board.py | grep -n "autopilot is:open\|label:autopilot\|def \(_\)\?.*view" | head -30
```

> commit c0f0e8edf8bbb66c821e98ea33af6073baa25520
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Fri Oct 9 02:06:18 2026 +0000
> 
>     planner for #282 (run 37872658551)
> 
> diff --git a/tests/test_autopilot_board.py b/tests/test_autopilot_board.py
> index efc1c90..6a813de 100644
> --- a/tests/test_autopilot_board.py
> +++ b/tests/test_autopilot_board.py
> @@ -360,7 +360,7 @@ def test_the_board_gets_one_autopilot_table_view(record_property, make):
>      """The first issue switched on autopilot gives the board an Autopilot view, a table showing only what carries the label.
>  
>      On a board with only the Needs you view, switching #57 on autopilot adds exactly one view: named Autopilot, laid
> -    out as a table, filtered to label:autopilot is:open. Switching #101 on afterwards adds no second view, and a stage moment
> +    out as a table, filtered to label:autopilot is:open (#278). Switching #101 on afterwards adds no second view, and a stage moment
>      on a board without the view adds none."""
>      record_property("proves", "210.4")
>      w = make(labels={("issue", 57): {LABEL}, ("issue", 101): {LABEL}, ("issue", 58): set()})
> diff --git a/tests/test_manifest.py b/tests/test_manifest.py
> index 6f53c3a..8335905 100644
> --- a/tests/test_manifest.py
> +++ b/tests/test_manifest.py
> @@ -45,6 +45,7 @@ import textwrap
>  import pytest
>  
>  ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> +sys.path.insert(0, ROOT)  # the code under test is this ch

`7. Bash`
```
cd /home/runner/work/dokima/dokima; git show origin/main:dokima/board.py | sed -n 1,40p | grep -n VIEW; git show origin/main:dokima/board.py | sed -n 190,215p; rm -rf /tmp/wt; git worktree add -q /tmp/wt HEAD 2>&1|tail -1; cd /tmp/wt && git -c user.email=a@b -c user.name=r merge -q --no-edit origin/main 2>&1 | tail -5; git status --short | head
```

> 17:VIEW_FILTER = f"label:{AUTOPILOT} is:open"  # merged and closed items keep their label, so the view shows only open ones
>     try:
>         if "Autopilot" not in board.views():
>             board.add_view("Autopilot", "table", VIEW_FILTER)
>     except subprocess.CalledProcessError as e:
>         raise RuntimeError(f"Could not add the Autopilot view to the board: {(e.stderr or str(e)).strip()}") from e
> 
> 
> def fix_view(board):
>     """Move an Autopilot view still on the old filter, label:autopilot, to VIEW_FILTER; any other filter is the owner's."""
>     try:
>         for v in board.view_nodes():
>             if v["name"] == "Autopilot" and v.get("filter") == f"label:{AUTOPILOT}":
>                 board.set_view_filter(v["id"], VIEW_FILTER)
>     except subprocess.CalledProcessError as e:
>         raise RuntimeError(f"Could not fix the Autopilot view's filter to {VIEW_FILTER}: {(e.stderr or str(e)).strip()}") from e
> 
> 
> def sync(event, payload, spec, repo, q=gql, rest=api):
>     changes, pill = decide(event, payload), priority(event, payload)
>     on_off, pr = switched(event, payload), opened(event, payload)
>     if not spec or not (changes or pill or on_off):
>         return []
>     board = Board(spec, repo, q, rest)
>     if pr and any(board.autopilot("issue", n) for n in pr[1]) and not board.autopilot("pr", pr[0]):
>         # A pull request built for an issue on autopilot carries the label too, so the Autopilot view lists it.
>         board.label("pr", pr[0], True)
> Auto-merging dokima/board.py
> CO

`8. Bash`
```
cd /tmp/wt; git diff dokima/board.py | head -60
```

> diff --cc dokima/board.py
> index 3f6648a,827d704..0000000
> --- a/dokima/board.py
> +++ b/dokima/board.py
> @@@ -183,8 -189,7 +191,12 @@@ def switch(board, number)
>           return
>       try:
>           if "Autopilot" not in board.views():
> ++<<<<<<< HEAD
>  +            view = manifest.VIEWS["Autopilot"]
>  +            board.add_view("Autopilot", view["layout"], view["filter"])
> ++=======
> +             board.add_view("Autopilot", "table", VIEW_FILTER)
> ++>>>>>>> origin/main
>       except subprocess.CalledProcessError as e:
>           raise RuntimeError(f"Could not add the Autopilot view to the board: {(e.stderr or str(e)).strip()}") from e
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Resolve with the branch's side (worker's state) plus main's fix_view, then run the tests.

`9. Bash`
```
cd /tmp/wt; python3 - <<'E'
import re
s=open('dokima/board.py').read()
s=re.sub(r'<<<<<<< HEAD\n(.*?)=======\n.*?>>>>>>> origin/main\n', r'\1', s, flags=re.S)
open('dokima/board.py','w').write(s)
E
git add -A >/dev/null; python3 -m pytest -q tests/test_manifest.py tests/test_autopilot_board.py tests/test_app.py 2>&1 | tail -15; python3 -m pytest -q -x 2>&1 | tail -3
```

> Command did not complete within its 120s timeout and was moved to the background (ID: brv3s8non). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b476d2-757c-41a9-974a-24cca6cde1f2/tasks/brv3s8non.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

**Agent:** Meanwhile, the test on the current branch (no fix_view):

`10. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 100 python3 -m pytest -q tests/test_manifest.py 2>&1 | tail -8; cat /tmp/pack/in/06-reviewer-plan.json | python3 -c "import json,sys;d=json.load(sys.stdin)['handback'];print(json.dumps(d['asks'],indent=0)); print(d.get('assumptions'))"
```

> if not hasattr(board, "fix_view"):
> >           pytest.fail("282.2: the board has no fix_view to move an old Autopilot view to the manifest's filter")
> E           Failed: 282.2: the board has no fix_view to move an old Autopilot view to the manifest's filter
> 
> tests/test_manifest.py:240: Failed
> =========================== short test summary info ============================
> FAILED tests/test_manifest.py::test_the_board_moves_an_old_autopilot_view_to_the_manifests_filter - Failed: 282.2: the board has no fix_view to move an old Autopilot view to the manifest's filter
> 1 failed, 60 passed in 2.33s
> [
> {
> "ask": "One manifest module in `dokima/` declares the labels, board fields and their options, views, required check names, branch rules and app permissions Dokima needs.",
> "source": "https://github.com/dokima-dev/dokima/issues/282",
> "criterion": "282.1"
> },
> {
> "ask": "The manifest declares the Autopilot option as purple, described \"Running on its own\".",
> "source": "https://github.com/dokima-dev/dokima/issues/282",
> "criterion": "282.2"
> },
> {
> "ask": "It declares the Autopilot view's filter as `label:autopilot is:open`. The board code reads that filter from the manifest.",
> "source": "https://github.com/dokima-dev/dokima/issues/282",
> "criterion": "282.2"
> },
> {
> "ask": "A test fails when code or a workflow relies on a setting the manifest leaves out. It names the setting and the file.",
> "source": "https://github.com/dokima-dev/dokima/issues/282",
> "criterion": "282.3"
> },
> {
> "ask": "The manifes

`11. Bash`
```
sleep 90; cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b476d2-757c-41a9-974a-24cca6cde1f2/tasks/brv3s8non.output | tail -20
```

> <tool_use_error>Blocked: sleep 90 followed by: cat /tmp/claude-1001/-home-runner-work-dokima-dokima/d9b476d2-757c-41a9-974a-24cca6cde1f2/tasks/brv3s8non.output tail -20. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>

`12. Read`
```
/tmp/claude-1001/-home-runner-work-dokima-dokima/d9b476d2-757c-41a9-974a-24cca6cde1f2/tasks/brv3s8non.output
```

> 1	  +         'label:autopilot is:open',
> 2	        ),
> 3	    ]
> 4	FAILED tests/test_manifest.py::test_the_guard_passes_settings_the_manifest_declares - AssertionError: 282.3: code or workflows in this repo rely on settings the manifest leaves out: ["dokima/board.py: check 'Autopilot' is not in the manifest's required checks"]
> 5	assert ['dokima/boar...uired checks'] == []
> 6	  
> 7	  Left contains one more item: "dokima/board.py: check 'Autopilot' is not in the manifest's required checks"
> 8	  
> 9	  Full diff:
> 10	  - []
> 11	  + [
> 12	  +     "dokima/board.py: check 'Autopilot' is not in the manifest's required "
> 13	  +     'checks',
> 14	  + ]
> 15	2 failed, 87 passed in 2.32s
> 16

`13. Bash`
```
cd /tmp/wt; timeout 100 python3 -m pytest -q tests/test_manifest.py -k moves 2>&1 | grep -E "^E" | head -5
```

> E       AssertionError: 282.2: with the manifest's filter changed, the board moved the old view with [('V1', 'label:autopilot is:open')]: it does not read the filter from the manifest
> E       assert [('V1', 'labe...lot is:open')] == [('V1', 'labe...no:assignee')]
> E         
> E         At index 0 diff: ('V1', 'label:autopilot is:open') != ('V1', 'label:autopilot is:open no:assignee')
> E
> Shell cwd was reset to /home/runner/work/dokima/dokima

`14. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner re-planned after the pull request clashed with main, where #286 added the board's fix for an old Autopilot view.",
          "Criterion 282.2 now also says the board takes the manifest's filter when it moves an Autopilot view still on the old label:autopilot filter, with one new test for it.",
          "The planner matched a test's description in tests/test_autopilot_board.py to main's, so that file now merges with main cleanly."],
  "decided": ["Which views count as old and when the board fixes them stays as #286 left it; only the filter it moves the view to comes from the manifest."],
  "open": ["dokima/board.py still clashes with main; the worker resolves it."]},
 "verdict": "approve",
 "summary": "The re-plan keeps every ask and adds one test so the board also takes the manifest's filter when it fixes an old Autopilot view; that test fails today for the right reason.",
 "blockers": [],
 "notes": [
  {"text": "Once main is merged in, the guard flags main's own fix_view, which compares a view's name with \"Autopilot\", as a required check left out of the manifest. The worker has to make the guard pass on the merged repo, as 282.3 already says.",
   "evidence": "Branch merged with origin/main in a scratch copy: tests/test_manifest.py::test_the_guard_passes_settings_the_manifest_declares fails with \"dokima/board.py: check 'Autopilot' is not in the manifest's required checks\"."},
  {"text": "The new test fails on the branch because the board has no fix_view yet, and on the branch merged with main because main's fix_view uses its own fixed filter instead of the manifest's: both are the missing feature.",
   "evidence": "Branch: \"282.2: the board has no fix_view ...\". Merged: \"282.2: with the manifest's filter changed, the board moved the old view with [('V1', 'label:autopilot is:open')]: it does not read the filter from the manifest\"."}
 ],
 "outside_pla
```

> summary holds 32 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`15. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The re-plan keeps every ask and adds a test that the board's fix for an old Autopilot view uses the manifest's filter."
json.dump(d,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 282 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?; git worktree list
```

> rc=0
> /home/runner/work/dokima/dokima c0f0e8e [try/issue-282]

**Agent:** I approved the re-plan for #282, and the hand-back in `/tmp/dokima-out/review.json` passes both checks.

**What changed in the plan:** the pull request clashed with main after #286 merged. #286 added code so the board moves an Autopilot view still on the old `label:autopilot` filter to the new one. Criterion 282.2 now also says the board takes that new filter from the manifest when it does this move, and one new test proves it. Every ask in the issue and your comment still maps to a criterion, and nothing is missing.

**The new test fails today for the right reason:**
- **On the branch:** it fails because the board has no code to move an old view yet.
- **On the branch with main merged in (a scratch copy):** it fails because main's board moves the view to its own fixed filter and ignores the manifest.

**Two things the worker still has to fix (notes, not blockers):**
- **`dokima/board.py` still clashes with main.** The planner's change to `tests/test_autopilot_board.py` means that file now merges cleanly.
- **The settings check gives a false alarm once main is merged in.** It reports main's view-fixing code as using a required check called "Autopilot" that the manifest leaves out. Criterion 282.3 already says the check must pass on the repo, so the worker has to fix this.

I had no earlier blockers to clear and the plan has no questions for you.
