# reviewer (plan) for #437

Run: https://github.com/dokima-dev/dokima/actions/runs/38080855412

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (42.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/dbb69f08-279a-4330-88ca-48d0bc1021b2/tool-results/bbr4ym0ap.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> parent.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> # Issue #437: A play-through on a real sandbox repo checks the card after every step from issue to merge
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [438], "loop": []} -->
> One play-through on the sandbox repo checks both cards after every step from a new issue to a merge.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/437
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Proving the real run:** All tests run with no key, so they prove the play-through's steps, its judge of each card, the #419 moment replayed through today's card.yml, the wait and the sandbox guard, but not a real run on card-gallery. The plan assumes you press Run workflow on this pull request's branch with commit f7340db before approving, and expect FAIL at build started (#439, not fixed yet) and at code review record posted saying Code review running, with every other step PASS. So the play-through plays every step to the end even after one fails, and exits 1 when any failed. Is that right? · for you
> 
> <img src="https://raw.gith

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (35.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/dbb69f08-279a-4330-88ca-48d0bc1021b2/tool-results/b77q1vo3y.txt
> 
> Preview (first 2KB):
> # Issue #437: A play-through on a real sandbox repo checks the card after every step from issue to merge
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [438], "loop": []} -->
> One play-through on the sandbox repo checks both cards after every step from a new issue to a merge.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/437
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Proving the real run:** All tests run with no key, so they prove the play-through's steps, its judge of each card, the #419 moment replayed through today's card.yml, the wait and the sandbox guard, but not a real run on card-gallery. The plan assumes you press Run workflow on this pull request's branch with commit f7340db before approving, and expect FAIL at build started (#439, not fixed yet) and at code review record posted saying Code review running, with every other step PASS. So the play-through plays every step to the end even after one fails, and exits 1 when any failed. Is that right? · for you
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="block

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/dbb69f08-279a-4330-88ca-48d0bc1021b2/tool-results/b77q1vo3y.txt
```

> 1	# Issue #437: A play-through on a real sandbox repo checks the card after every step from issue to merge
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-blocking: {"blocked_by": [], "blocks": [438], "loop": []} -->
> 5	One play-through on the sandbox repo checks both cards after every step from a new issue to a merge.
> 6	
> 7	**Plan**
> 8	
> 9	https://github.com/dokima-dev/dokima/issues/437
> 10	
> 11	**Raised:**
> 12	
> 13	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Proving the real run:** All tests run with no key, so they prove the play-through's steps, its judge of each card, the #419 moment replayed through today's card.yml, the wait and the sandbox guard, but not a real run on card-gallery. The plan assumes you press Run workflow on this pull request's branch with commit f7340db before approving, and expect FAIL at build started (#439, not fixed yet) and at code review record posted saying Code review running, with every other step PASS. So the play-through plays every step to the end even after one fails, and exits 1 when any failed. Is that right? · for you
> 14	
> 15	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #438
> 16	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relat

`4. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items()},indent=1)[:12000])"; cat in/03-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps(d.get('handback',d),indent=1)[:200])"
```

> []{
>  "kind": "user_story",
>  "summary": "One play-through on the sandbox repo checks both cards after every step from a new issue to a merge.",
>  "user_story": "The owner presses Run workflow with a Dokima commit and gets one play-through on dokima-dev/card-gallery, with stand-in agents that use no model, whose log says after each step from a new issue to a merged pull request whether both cards showed what had just happened.",
>  "acceptance_criteria": [
>   {
>    "text": "One run of `python3 -m dokima.playthrough` plays an issue on dokima-dev/card-gallery through eight steps. After each it waits for the card runs to finish, then checks both cards. The steps, in order: issue opened, plan posted, plan approved, build started (after /work), pull request opened, code review started, code review record posted, merged. Its log says `PASS: <step>` when both cards show that step, or `FAIL: <step>: ...` naming the wrong card and quoting what it showed (its stage, and Code review's state at the review steps). Each step should show: issue opened, Backlog; plan posted, Plan; plan approved, Plan asking for /work; build started, Work with no ask for /work; pull request opened, both cards in Work or Review; code review started, both in Review with Code review running; code review record posted, both in Review with Code review passed; merged, both Merged. From the pull request on, a missing PR card fails the step. It plays every step to the end even after one fails, and exits 1 when any step fail

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git show --stat HEAD; wc -l tests/test_playthrough.py; cat tests/test_playthrough.py
```

> 057a0e9 planner for #437 (run 38078512598)
> ca64381 planner for #437 (run 38076664550)
> 03d4200 Autopilot says it merged a PR that only queued or is waiting for my approval (#430)
> commit 057a0e9015541d6824173564ef25ab2797c793a6
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 19:10:03 2026 +0000
> 
>     planner for #437 (run 38078512598)
> 
>  tests/test_playthrough.py | 134 +++++++++++++++++++++++++++++++++++++++++++++-
>  1 file changed, 133 insertions(+), 1 deletion(-)
> 495 tests/test_playthrough.py
> """The sandbox play-through checks both cards after every step, from new issue to merge (#437).
> 
> #419: the code review had passed, yet the card said Code review running for 30 minutes. The review's record is the
> bot's edit of its live run card, and card.yml skips every edit the bot makes, so nothing redrew the card. The fake
> GitHub of tests/card_player.py plays card.yml one event at a time, but only a run on real GitHub proves what the owner
> sees. So `python3 -m dokima.playthrough`, started by .github/workflows/playthrough.yml's Run workflow button, plays
> one issue on dokima-dev/card-gallery with stand-in agents that call no model, and judges both cards after each step.
> 
> These tests run with no GitHub and no key. They prove the parts that decide the verdict: the steps in order, the
> judge of each step's cards (drawn by dokima/card.py), the #419 moment replayed through today's card.yml, the wait
> that fails a hung step, the guard that kee

**Agent:** Now running the plan's tests to confirm each one fails today because the play-through doesn't exist yet.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_playthrough.py 2>&1 | grep -E "^(FAILED|ERROR|[0-9]+ )|AssertionError" | head -30
```

> >           raise AssertionError(f"{k}: dokima/playthrough.py does not exist yet, so there is no play-through: {e}")
> E           AssertionError: 437.1: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> tests/test_playthrough.py:41: AssertionError
> >           raise AssertionError(f"{k}: dokima/playthrough.py does not exist yet, so there is no play-through: {e}")
> E           AssertionError: 437.1: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> tests/test_playthrough.py:41: AssertionError
> >           raise AssertionError(f"{k}: dokima/playthrough.py does not exist yet, so there is no play-through: {e}")
> E           AssertionError: 437.2: dokima/playthrough.py does not exist yet, so there is no play-through: cannot import name 'playthrough' from 'dokima' (unknown location)
> tests/test_playthrough.py:41: AssertionError
> E       AssertionError: 437.3: .github/workflows/playthrough.yml does not exist, so there is no play-through to start
> tests/test_playthrough.py:170: AssertionError
> E       AssertionError: 437.4: .github/workflows/playthrough.yml does not exist
> tests/test_playthrough.py:209: AssertionError
> >           raise AssertionError(f"{k}: dokima/playthrough.py does not exist yet, so there is no play-through: {e}")
> E           AssertionError: 437.5: dokima/playthrough.py does not exist yet, so there is no

`7. Bash`
```
cd /home/runner/work/dokima/dokima/tests; mkdir -p /tmp/scr && cat > /tmp/scr/s.py <<'EOF'
import sys,os,tempfile,pathlib
sys.path.insert(0,os.getcwd())
import test_playthrough as t
r=t.right_cards()
for k,(i,p) in r.items():
    import re
    print(k, '|', [l for l in i.splitlines() if re.search(r'Plan\*\*|Work\*\*|Review\*\*|Backlog|Merged|Code review', l)][:3] and '', 'pr' if p else '-')
from card_player import *
from test_card_running import review_queued
d=pathlib.Path(tempfile.mkdtemp())
hub=Hub(d); text=review_queued(hub)
must_redraw(hub, pr_comment(246,260,who="bot",text=text),"x")
s=hub.load(); lc=next(c for c in s["prs"]["260"]["comments"] if c["body"]==text)
lc["body"]=record(review_record("pr"),lc["at"])["body"]; hub.save()
hub.run(*pr_comment(246,260,who="bot",action="edited",text=lc["body"]),"x")
print("running" , "Code review running" in hub.issue_body(246), "running" in hub.pr_body(260).lower())
must_redraw(hub, issue_comment(246, who=OWNER, text="ok"),"x")
print("after", "Code review running" in hub.issue_body(246))
EOF
python3 /tmp/scr/s.py 2>&1 | tail -15
```

> issue opened |  -
> plan posted |  -
> plan approved |  -
> build started |  -
> pull request opened |  pr
> code review started |  pr
> code review record posted |  pr
> merged |  pr
> running False True
> after False

`8. Bash`
```
cd /home/runner/work/dokima/dokima/tests; cat >> /tmp/scr/s.py <<'EOF'
EOF
python3 - <<'EOF'
import sys,os,tempfile,pathlib,re
sys.path.insert(0,os.getcwd())
from card_player import *
from test_card_running import review_queued
d=pathlib.Path(tempfile.mkdtemp())
hub=Hub(d); text=review_queued(hub)
must_redraw(hub, pr_comment(246,260,who="bot",text=text),"x")
s=hub.load(); lc=next(c for c in s["prs"]["260"]["comments"] if c["body"]==text)
lc["body"]=record(review_record("pr"),lc["at"])["body"]; hub.save()
hub.run(*pr_comment(246,260,who="bot",action="edited",text=lc["body"]),"x")
for l in hub.issue_body(246).splitlines():
  if 'Definition' in l or re.match(r'\*\*\w+\*\*$',l): print(l[:600])
must_redraw(hub, issue_comment(246, who=OWNER, text="ok"),"x")
for l in hub.issue_body(246).splitlines():
  if 'Definition' in l: print(l[:600])
EOF
```

> **Review**
> **Definition of Done:** <a href="https://github.com/o/r/runs/2602"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/running.svg" width="16" height="16" align="absmiddle" alt="running"> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" heigh
> **Definition of Done:** <a href="https://github.com/o/r/runs/2602"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> All tests · <a href="https://github.com/o/r/actions/runs/2"><img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a> <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.co

`9. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "card-gallery" --include=*.py --include=*.yml --include=*.md . | grep -v tests/test_playthrough | head; ls .github/workflows; grep -n "uses:.*dokima\|DOKIMA_REF\|dokima-dev/dokima" .github/workflows/card.yml | head; python3 -c "
from dokima import agent;print(repr(agent.footnote({'role':'planner','report':agent.run_report('/nonexist/claude.json'),'run':'x'})))"
```

> agent.yml
> assign.yml
> audit.yml
> autopilot.yml
> board.yml
> card.yml
> commands.yml
> done-whens.yml
> full-suite.yml
> planner.yml
> reviews.yml
> uptodate.yml
> wiki.yml
> worker.yml
> '<sub><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/stats.svg" width="16" height="16" align="absmiddle" alt="stats"> model unknown · [run](x)</sub>'

`10. Bash`
```
cd /tmp/pack; grep -o "PLAYED[^\"]\{0,200\}" in/*.json | head; grep -o "[^\"]\{0,200\}f7340db[^\"]\{0,100\}" in/03-planner.json | head -3; cat parent.json | head -c 3000
```

> ugrep: error: error at position 627
> ]|\xf4[\x80-\x8f][\x80-\xbf][\x80-\xbf]){0,100}
>                   exceeds complexity limits___/
> 
> 
> {"number": 425}
> Shell cwd was reset to /home/runner/work/dokima/dokima

`11. Bash`
```
cd /tmp/pack; grep -c PLAYED in/*.json; python3 - <<'EOF'
import json,re
for f in ['in/01-planner.json','in/02-reviewer-plan.json','in/03-planner.json']:
    s=open(f).read()
    for m in re.finditer(r'.{0,200}(PLAYED|card-gallery.{0,40}workflow|commit to play).{0,200}',s): print(f, m.group(0)[:400]); 
EOF
```

> in/01-planner.json:0
> in/03-planner.json:0
> in/02-reviewer-plan.json:0
> in/01-planner.json     "text": "Running it by hand stays possible: the Run workflow button starts .github/workflows/playthrough.yml, with a required `commit` input naming the Dokima commit to play. It checks that commit out into a folder of its own and runs `python3 -m dokima.playthrough`.",
> in/01-planner.json     "text": "Every app token playthrough.yml mints names owner dokima-dev and repositories card-gallery only, and the workflow's own GitHub token may write nothing.",
> in/01-planner.json ": "All tests run with no key, so they prove the play-through's steps, its judge of each card, the #419 moment replayed through today's card.yml, the wait and the sandbox guard, but not a real run on card-gallery. The plan assumes you press Run workflow on this pull request's branch with commit f7340db before approving, and expect FAIL at build started (#439, not fixed yet) and at code review reco
> in/02-reviewer-plan.json     "ask": "Running it by hand stays possible: the Run workflow button starts it, with the Dokima commit to play as an input.",
> in/03-planner.json     "text": "Running it by hand stays possible: the Run workflow button starts .github/workflows/playthrough.yml, with a required `commit` input naming the Dokima commit to play. It checks that commit out into a folder of its own and runs `python3 -m dokima.playthrough`.",
> in/03-planner.json     "text": "Every app token playthrough.yml mints names owner doki

**Agent:** The tests all fail today for the right reason. One gap: nothing proves the `commit` input changes which Dokima code draws the cards on card-gallery. Writing the review now.

`12. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added three tests that drive the play-through's run on a fake sandbox: all eight steps in order, a wait and both cards checked after each, one PASS or FAIL line per step, and play on after a failure or a hung step.",
          "The planner added to criterion 437.1 that the run plays every step to the end and exits 1 when any step failed, as the owner answered."],
  "decided": ["The four agent steps are played with stand-in hand-backs that leave no model report; the other steps get none.",
              "Fixing the build started card (#439) is no longer named in the plan."],
  "open": ["Nothing proves the Dokima commit given to Run workflow is the code that draws the cards on card-gallery."]},
 "verdict": "block",
 "summary": "The plan now proves the run plays, waits and judges every step, but nothing proves the commit you give Run workflow is the Dokima code whose cards get checked, so a play-through that ignores it would pass.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "437.3: Weak test",
   "text": "The owner asked for Run workflow to take the Dokima commit to play, and criterion 437.2 expects a run on f7340db to fail at the code review record step. That only holds if the cards on card-gallery are drawn by that commit's card.yml and dokima/card.py. Criterion 437.3 promises only that playthrough.yml checks the commit out into a folder and runs the module. No criterion says how that commit reaches the card runs on card-gallery, and no test checks it. A play-through that never uses the checked-out commit passes every test, and its PASS or FAIL lines would then describe whatever Dokima card-gallery happens to run, not the commit the owner named. Smallest fix: one sentence in 437.3 saying how the played commit becomes the code that draws card-gallery's cards (for example, card-gallery's workflows run Dokima at a ref the play-through sets, o
```

> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`13. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Nothing proves the commit given to Run workflow is the Dokima code whose cards get checked, so a play-through ignoring it would pass."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 437 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for [#437](https://github.com/dokima-dev/dokima/issues/437) (a play-through on card-gallery that checks both cards after every step), with one blocker for the planner. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner fixed.** The earlier blocker said nothing showed that a run actually plays the steps, and that is now covered. Three new tests drive the run on a fake sandbox. They check that it plays all eight steps in order and waits for the card runs before reading both cards. They check it logs one PASS or FAIL line per step, keeps going after a failed or hung step, and exits 1 when any step failed. Your `/plan` answer (play to the end, exit 1 on any failure) is now in criterion 437.1.

**The tests fail today for the right reason.** All 12 fail because `dokima/playthrough.py` and `playthrough.yml` don't exist yet, not because of a crash or a bad path. I also replayed the [#419](https://github.com/dokima-dev/dokima/issues/419) moment (the card stuck on Code review running) through today's `card.yml` on the fake GitHub. The card keeps saying Code review running after the bot edits its run card into the review's record, and shows passed once an owner comment redraws it. So the 437.2 test can pass once the play-through is built.

**The blocker (437.3, weak test).** You asked for Run workflow to take "the Dokima commit to play", and 437.2 expects a run on f7340db to fail at the review record step. That only works if card-gallery's cards are drawn by that commit's code. The plan only says the workflow checks the commit out into a folder and runs the module. Nothing says how that commit reaches the card runs on card-gallery. The test sets a `PLAYED` folder, but no criterion or test says what it does, and nothing in this repo mentions card-gallery. A play-through that ignored the commit would pass every test, and its PASS/FAIL lines would describe whatever Dokima card-gallery already runs.

The smallest fix is one sentence in 437.3 on how the commit becomes card-gallery's code, plus a test that fails if the commit is ignored. If the planner can't know how card-gallery runs Dokima, it should ask you. You may be able to settle this fastest yourself, with a `/plan` comment saying how card-gallery runs Dokima.

**Your asks.** All 11 of your asks from the issue and your comment are carried by a criterion; none are missing.
