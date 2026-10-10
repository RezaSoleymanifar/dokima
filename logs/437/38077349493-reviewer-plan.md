# reviewer (plan) for #437

Run: https://github.com/dokima-dev/dokima/actions/runs/38077349493

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> # Issue #437: A play-through on a real sandbox repo checks the card after every step from issue to merge
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [438], "loop": []} -->
> **Backlog**
> 
> https://github.com/dokima-dev/dokima/issues/437
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #438
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #425, story 1</summary>
> 
> **Part of:** #425 The card always shows what is true right now: one rule, one place
> 
> **User story:** The owner can run one play-through on a real GitHub sandbox repo, with stand-in agents that use no model, and see after each step from a new issue to a merged pull request whether the card showed what had just happened.
> 
> **Context:** tests/card_player.py already plays card.yml against a fake GitHub; this story is the real-GitHub counterpart the owner asked for. The owner already tested on dokima-dev/card-gallery (see #416). The #419 moment: the code review's record is an edit of its live run card by the bot, and card.yml's `queue` job condition (.github/workflows/card.yml line 33) ignores every edit the bot makes, so after the review passed the card kept saying Code review runni

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "import json;d=json.load(open('parent.json'));print(json.dumps(d,indent=1)[:6000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD; wc -l tests/test_playthrough.py
```

> []{
>  "number": 425
> }
> commit ca643818a61b627f93ca8c940172a0bcb1da6788
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 18:49:27 2026 +0000
> 
>     planner for #437 (run 38076664550)
> 
>  tests/test_playthrough.py | 363 ++++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 363 insertions(+)
> 363 tests/test_playthrough.py

`3. Read`
```
/home/runner/work/dokima/dokima/tests/test_playthrough.py
```

> 1	"""The sandbox play-through checks both cards after every step, from new issue to merge (#437).
> 2	
> 3	#419: the code review had passed, yet the card said Code review running for 30 minutes. The review's record is the
> 4	bot's edit of its live run card, and card.yml skips every edit the bot makes, so nothing redrew the card. The fake
> 5	GitHub of tests/card_player.py plays card.yml one event at a time, but only a run on real GitHub proves what the owner
> 6	sees. So `python3 -m dokima.playthrough`, started by .github/workflows/playthrough.yml's Run workflow button, plays
> 7	one issue on dokima-dev/card-gallery with stand-in agents that call no model, and judges both cards after each step.
> 8	
> 9	These tests run with no GitHub and no key. They prove the parts that decide the verdict: the steps in order, the
> 10	judge of each step's cards (drawn by dokima/card.py), the #419 moment replayed through today's card.yml, the wait
> 11	that fails a hung step, the guard that keeps the play-through on the sandbox, the stand-in agents' empty usage, and
> 12	the workflow's button, key and permissions.
> 13	"""
> 14	import ast
> 15	import json
> 16	import os
> 17	import re
> 18	import subprocess
> 19	import sys
> 20	import time
> 21	
> 22	sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
> 23	sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
> 24	from card_player import OWNER, Hub, issue_comment, must_redraw, pr_comment, record, review_record  # noqa: E402
> 25	from test_card_runni

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_playthrough.py 2>&1 | grep -E "^(E   |FAILED|ERROR|[0-9]+ )" | head -40
```

> E           ImportError: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           AssertionError: 437.1: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           ImportError: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           AssertionError: 437.1: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           ImportError: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           AssertionError: 437.2: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> E       AssertionError: 437.3: .github/workflows/playthrough.yml does not exist, so there is no play-through to start
> E       assert False
> E        +  where False = <function exists at 0x7f34435ef600>('/home/runner/work/dokima/dokima/.github/workflows/playthrough.yml')
> E        +    where <function exists at 0x7f34435ef600> = <module 'posixpath' (frozen)>.exists
> E        +      where <module 'posixpath' (frozen)> = os.path
> E       AssertionError: 437.4: .github/workflows/playthrough.yml does not exist
> E       assert ''
> E           ImportError: cannot import name 'playthrough' from 'dokima' (unknown location)
> E           AssertionError: 437.5: dokima/playthrough.py does not exist yet, so there is no pla

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -l card_player tests/*.py; for f in test_card_queue test_card_running test_card_sweep test_parent_sweep; do echo $f $(grep -c "^def test_" tests/$f.py); done; grep -n "asks\|criterion" dokima/agent.py | grep -i ask | head -30
```

> tests/test_card_running.py
> tests/test_card_sweep.py
> tests/test_card_queue.py
> tests/test_parent_sweep.py
> tests/test_playthrough.py
> test_card_queue 2
> test_card_running 4
> test_card_sweep 10
> test_parent_sweep 4
> 557:                  ("The owner's asks", bullets(h.get("asks"), lambda a: f"{a.get('ask', '')} ({a.get('criterion', '')}, {a.get('source', '')})"))]
> 579:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")
> 582:        return f"The planner planned this issue and asks you {q} question{'s' if q > 1 else ''}." if q else "The planner planned this issue."
> 914:def problems_asks(r, ids):
> 915:    """Everything wrong with a plan review's asks list: every ask the owner made, in their words, with a link to where
> 916:    they said it and the plan's criterion (one of ids) that keeps it, or "missing"; an approve keeps every ask."""
> 917:    asks = r.get("asks")
> 918:    if not isinstance(asks, list) or not asks:
> 919:        return ["asks must list every ask in the owner's issue and comments, each {\"ask\": \"the owner's words\", "
> 921:    bad = problems_items(r, "asks", ("ask", "source", "criterion"), name="ask")
> 922:    good = [a for a in asks if isinstance(a, dict) and all(filled(a.get(k)) for k in ("ask", "source", "criterion"))]
> 926:            bad.append(f"the ask \"{a['ask']}\" is matched to {c}, which is not a criterion of the plan "
> 928:    gone = [a["ask"] for a in good if a["criterion"].strip() == "missing

**Agent:** Tests all fail for the right reason. Now checking how the review checker matches asks to criteria, then sanity-checking the cards the tests draw.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def plan_criteria" -A15 dokima/agent.py; grep -n "def footnote" -A25 dokima/agent.py | grep -n token
```

> 1023:def plan_criteria(plan, number):
> 1024-    """The plan's criteria ids: N.k for a story (acceptance criteria, then non-functional), S<s>.<k> for each story of a split."""
> 1025-    count = lambda p: sum(len(p.get(k)) for k in ("acceptance_criteria", "non_functional") if isinstance(p.get(k), list))
> 1026-    if plan.get("kind") == "feature":
> 1027-        stories = plan.get("stories") if isinstance(plan.get("stories"), list) else []
> 1028-        return [f"S{s}.{k}" for s, st in enumerate(stories, 1) if isinstance(st, dict) for k in range(1, count(st) + 1)]
> 1029-    return [f"{number}.{k}" for k in range(1, count(plan) + 1)]
> 1030-
> 1031-
> 1032-def problems_plan(kind, h, plan, number):
> 1033-    """Everything in a work.json that does not match the plan: one line per criterion."""
> 1034-    ids = plan_criteria(plan, number)
> 1035-    bad = []
> 1036-    if kind == "work":
> 1037-        crit = h.get("criteria")
> 1038-        if isinstance(crit, dict):
> 2:796-    """One line under every card: model, time, turns, tokens and cost, and the link to the full conversation."""
> 13:807-    if r.get("tokens_in") or r.get("tokens_out"):
> 14:808-        parts.append(f"{r.get('tokens_in', 0):,} tokens in, {r.get('tokens_out') or 0:,} out")

`7. Bash`
```
cd /home/runner/work/dokima/dokima/tests; python3 - <<'EOF' 2>&1 | grep -vE "^\s*$" | grep -iE "^\*\*|Code review|Definition|work" | cut -c1-200
import test_playthrough as t
r=t.right_cards()
for s,(i,p) in r.items():
    print("=====",s)
    print(i[:1500].split("<!-- dokima-ask")[0] if i else None)
    if p: print("--PR--"); print(p[:1500])
EOF
```

> (Bash completed with no output)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF' 2>&1 | grep -E "=====|^\*\*|Definition|PR--|Traceback|Error" | sed -E 's/<img[^>]*alt="([^"]*)">/[\1]/g' | cut -c1-250
import sys; sys.path.insert(0,"tests")
import test_playthrough as t
r=t.right_cards()
for s,(i,p) in r.items():
    print("=====",s)
    print(i)
    if p: print("--PR--"); print(p)
EOF
```

> ===== issue opened
> **Backlog**
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> ===== plan posted
> **Plan**
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> ===== plan approved
> **Plan** · [needs you] Needs you: Say /work to build the plan
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> ===== build started
> **Work**
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> ===== pull request opened
> **Review**
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> --PR--
> **Review**
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [not started] All tests · [not started] [code review] Code review · [not started] [owner approval] Owner approval
> ===== code review started
> **Review**
> **User story:** The owner sees the thing.
> **Scope:** `app/x.py`
> **Definition of Done:** [no

`9. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF' 2>&1 | sed -E 's/<img[^>]*alt="([^"]*)">/[\1]/g' | head -12
import sys; sys.path.insert(0,"tests")
import test_playthrough as t
r=t.right_cards()
print(r["merged"][0][:800])
EOF
```

> <!-- dokima-card -->
> A thing is built.
> 
> [merged] **Merged**
> 
> https://github.com/o/r/issues/1 · https://github.com/o/r/pull/5 · [files changed] [files changed](https://github.com/o/r/pull/5/files)
> 
> **User story:** The owner sees the thing.
> 
> [acceptance criterion] **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle"

**Agent:** Tests' card drawings look sound. Next I'll check the tests can actually pass by dropping a quick throwaway judge into a scratch copy of the repo.

`10. Bash`
```
rm -rf /tmp/scratch && cp -r /home/runner/work/dokima/dokima /tmp/scratch && cd /tmp/scratch && cat > dokima/playthrough.py <<'EOF'
import re, time
STEPS = ("issue opened", "plan posted", "plan approved", "build started", "pull request opened",
         "code review started", "code review record posted", "merged")
def look(b):
    if b is None: return None
    b = re.sub(r'<img[^>]*alt="([^"]*)">', r'[\1]', b)
    st = re.search(r"\*\*(Backlog|Plan|Work|Review|Merged|Done)\*\*", b)
    cr = re.search(r"\[(not started|running|passed|failed|blocked)\]\)?\s*\[code review\]", b.replace("</a>",""))
    return {"stage": st and st.group(1), "cr": cr and cr.group(1), "work": "/work" in b}
WANT = {"issue opened": ("Backlog",None,None), "plan posted": ("Plan",None,False), "plan approved": ("Plan",None,True),
 "build started": ("Work",None,False), "pull request opened": (("Work","Review"),None,None),
 "code review started": ("Review","running",None), "code review record posted": ("Review","passed",None),
 "merged": ("Merged",None,None)}
def judge(step, i, p):
    st, cr, w = WANT[step]
    cards = [("issue", i)] + ([("PR", p)] if STEPS.index(step) >= 4 else [])
    for name, b in cards:
        l = look(b)
        if l is None: return f"FAIL: {step}: the PR card is missing"
        ok = (l["stage"] in st if isinstance(st, tuple) else l["stage"] == st) and (cr is None or l["cr"] == cr) and (w is None or l["work"] == w)
        if not ok: return f"FAIL: {step}: the {name} card showed {l['stage']}, Code review {l['cr']}, /work {l['work']}"
    return f"PASS: {step}"
def wait_for_cards(step, n, wait, poll):
    end = time.monotonic() + wait
    while n():
        if time.monotonic() > end: return f"FAIL: {step}: card runs still running after {wait} s"
        time.sleep(poll)
EOF
python3 -m pytest -q tests/test_playthrough.py -k "each_step or todays or not_finish" 2>&1 | grep -E "^E  |passed|failed" | head
```

> 3 passed, 6 deselected in 2.34s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** A rough judge passes those three tests, so they can pass. Now checking whether a play-through that plays nothing would still pass every test.

`11. Bash`
```
cd /tmp/scratch && cat >> dokima/playthrough.py <<'EOF'
import json, os, subprocess, sys
def standin(role, stage, out):
    json.dump({}, open(os.path.join(out, {"planner": "plan.json", "worker": "work.json"}.get(role, "review.json")), "w"))
if __name__ == "__main__":
    repo = os.environ.get("REPO", "")
    if repo != "dokima-dev/card-gallery": sys.exit(f"refusing {repo}")
    subprocess.run(["gh", "api", f"repos/{repo}"])
    sys.exit(0)
EOF
cat > .github/workflows/playthrough.yml <<'EOF'
name: playthrough
on:
  workflow_dispatch:
    inputs:
      commit:
        required: true
permissions: {}
jobs:
  play:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/create-github-app-token@v1
        id: t
        with:
          app-id: 1
          private-key: ${{ secrets.DOKIMA_APP_KEY }}
          owner: dokima-dev
          repositories: card-gallery
      - uses: actions/checkout@v4
        with:
          ref: ${{ inputs.commit }}
          path: played
      - run: python3 -m dokima.playthrough
EOF
python3 -m pytest -q tests/test_playthrough.py 2>&1 | tail -3
```

> .........                                                                [100%]
> 9 passed in 2.28s
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Confirmed: a play-through that plays no step at all passes all nine tests. That means the plan needs to go back to the planner, so I'm writing the review now.

`12. Bash`
```
mkdir -p /tmp/dokima-out && cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": ["The planner wrote five criteria, three non-functional promises and nine tests in tests/test_playthrough.py for a play-through run from a Run workflow button on dokima-dev/card-gallery."],
  "decided": ["The play-through lives in dokima/playthrough.py and .github/workflows/playthrough.yml, with eight steps from issue opened to merged.",
              "The tests run with no key: they check the step list, the judge of each step's cards, the #419 moment on today's card.yml, the wait, the sandbox guard and the workflow file."],
  "open": ["The planner asks whether the owner presses Run workflow on f7340db before approving, expecting FAIL at build started and at code review record posted, with the play-through playing on after a failure and exiting 1."]
 },
 "verdict": "block",
 "summary": "The plan's tests never prove that a run plays the steps: a play-through that plays no step and logs nothing passes all nine, so the plan goes back to the planner.",
 "raises": [
  {
   "kind": "blocker",
   "to": "planner",
   "label": "437.1: Weak test",
   "text": "Criterion 437.1 promises one run that plays the eight steps in order, checks both cards after each and logs a PASS or FAIL line per step. The tests only read the STEPS list and call judge() on cards they draw themselves; nothing checks that a run ever plays a step, waits for its card runs, judges it or logs its line. The same gap leaves 437.4 (the stand-ins are what the run uses) and the wait promise (the run waits after each step) proved only on helper functions the run may never call. Smallest fix: add a test that drives the play loop with GitHub faked (for example, a play function given a fake step player and card reader, or a fake gh on PATH that answers) and checks that it plays all eight steps in order, calls the stand-ins, waits and judges after each, prints one PASS or FAIL line per step in order, and exits non-ze
```

> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`13. Bash`
```
python3 - <<'EOF'
import json;p="/tmp/dokima-out/review.json";d=json.load(open(p))
d["summary"]="No test proves a run plays the steps: a play-through that plays nothing passes all nine tests, so the plan goes back."
json.dump(d,open(p,"w"),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 437 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for [#437](https://github.com/dokima-dev/dokima/issues/437) (the play-through on the sandbox repo), so it goes back to the planner. The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**Why it's blocked:** criterion 437.1 promises that one run plays all eight steps, checks both cards after each, and writes a PASS or FAIL line for every step. No test proves that.
- The tests only read the list of step names and call the card-judging function on cards they draw themselves.
- In a throwaway copy of the repo, I wrote a play-through that only turns away other repos, makes one call to GitHub and exits. With a minimal workflow file beside it, all 9 tests passed. It played no step and logged nothing.
- The same gap leaves two other promises proven only on helper functions the real run might never call: 437.4 (the stand-in agents) and the fixed wait after each step.
- **Smallest fix:** add a test that drives the whole run against a fake GitHub. It should check the eight steps are played in order, the stand-ins are used, each step waits and is judged, there is one line per step, and the exit code is non-zero when any step fails. The other option is to mark 437.1 as a manual check and say why.

**What holds up:**
- All 9 new tests fail today for the right reason: the play-through and its workflow file don't exist yet.
- The card judge's tests are strict both ways: a judge that always says FAIL is caught, and so is one that misses a card the step didn't redraw. My rough judge passed them, so they can be passed.
- Every ask in the issue, including the three non-functional ones, maps to a criterion. None is missing.

**Still waiting on you:** the planner asked whether you'll press Run workflow on commit f7340db yourself before approving. It assumes the run will fail at "build started" and at "code review record posted", keep going after a failure, and exit 1. I left that question for you: nothing you've written settles it, and it means extra work on your side.

One thing for later: the 437.2 test expects today's card behaviour to fail. Once [#438](https://github.com/dokima-dev/dokima/issues/438) (which this issue blocks) fixes that behaviour, the test will go red, so #438 will need to change it.
