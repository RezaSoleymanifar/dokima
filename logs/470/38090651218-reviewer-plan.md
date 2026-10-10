# reviewer (plan) for #470

Run: https://github.com/dokima-dev/dokima/actions/runs/38090651218

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/plan.json; cat /tmp/pack/open_blockers.json
```

> # Issue #470: Everything Dokima writes for me is simple, terse, plain English; technical detail lives in docstrings
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Everything Dokima writes for the owner is short and plain, checked by code, with each question shown as one line.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: See the newest record below
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Phone screen:** A small plan fitting one phone screen came with the sizing you dropped. The plan drops it too and lets the word caps keep plans short. Right? · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Jargon by code:** Should code also send back file paths and code names, or only the reviewer judge jargon? The plan assumes code catches those (story 2). · for you
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Doubt: overlaps #241 and #242:** #242 puts reading rules in each role file, and #241 caps a story at five criteria. Should both close as replaced by this issue? T

`2. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('02-reviewer-plan.json'));print(json.dumps(d,indent=1)[:6000])"
```

> {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "38090098313",
>  "commit_before": "bf1443b25e29a12d5eeb00b2a4b60822404cc84b",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 85943,
>   "turns": 8,
>   "cost_usd": 0.5500458,
>   "tokens_in": 356099,
>   "tokens_out": 8793
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/470/38090098313-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38090098313",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner split the issue into four stories: whole-text word caps, sending back file paths and code names, one shared style file heading every prompt, and one line per question with the reviewer's take."
>    ],
>    "decided": [
>     "It dropped plan sizing and the caps on how many criteria, tests and questions a plan has, after the owner's comment.",
>     "It set a criterion at 12 words with no slack and left the other limits to the first story."
>    ],
>    "open": [
>     "Its three questions (phone screen, jargon by code, closing #241 and #242) were answered yes by the owner."
>    ]
>   },
>   "verdict": "block",
>   "summary": "Every ask is covered, but story 2 would reject file paths in a raise's evidence without asking the owner.",
>   "raises": [
>    {
>     "kind": "blocker",
>     "to": "planner",
>     "label": "Two readings: evidence",
>     "text": "Story 2 sends back any file path in every field of story 1's list, and that list includes a raise's evid

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "roles/" .github/workflows/agent.yml | head; grep -n "CAP\|TOLERANCE\|def " dokima/words.py | head -20; grep -n "def next_step\|def quoted\|def answered_lines" dokima/*.py; ls dokima/roles
```

> 227:          claude -p "$(cat /tmp/runtime/dokima/roles/$GRADE.md /tmp/runtime/dokima/roles/$ROLE.md)
> 3:The owner sets each cap; a text more than TOLERANCE over it (over 30 words for a 25-word cap, over 18 for 15) fails
> 8:TOLERANCE = 20  # percent over its cap a text may run before it is rejected
> 11:def count(text):
> 16:def first_sentence(text):
> 21:def limit(cap):
> 23:    return cap + cap * TOLERANCE // 100
> 26:def over_cap(where, text, cap, what="opens with"):
> 29:    Within the cap: neither. Over it by at most TOLERANCE: listed, the text still passes. Past that: rejected.
> 36:    return None, (f"{where} {what} {n} words, more than {TOLERANCE}% over its cap of {cap}: "
> 40:def check(texts, cap, what="opens with"):
> 50:SUMMARY_CAP = 25  # words in the one-sentence summary every planner, worker and reviewer hands back
> 53:def summary_caps(text, cap=SUMMARY_CAP):
> 56:    A second sentence is rejected however short the summary is; its words follow the TOLERANCE rule.
> dokima/agent.py:653:def answered_lines(repo, rec, earlier):
> dokima/agent.py:2100:def quoted(raised):
> dokima/agent.py:2125:def next_step(items, rec, owners, rounds=3, autopilot=lambda: False, body="", number="", parent=lambda: None):
> plan-grade.md
> planner.md
> result-grade.md
> reviewer.md
> worker.md

`4. Bash`
```
cd /tmp/pack/in; python3 -c "
import json;d=json.load(open('02-reviewer-plan.json'));print(json.dumps(d['handback']['asks'][19:],indent=1))"
```

> [
>  {
>   "ask": "instead of clumping all of that together in the freaking next section where it mentions my name",
>   "source": "https://github.com/dokima-dev/dokima/issues/470",
>   "criterion": "S4.5"
>  },
>  {
>   "ask": "code catches file paths and code names, the reviewer judges the rest",
>   "source": "https://github.com/dokima-dev/dokima/issues/470",
>   "criterion": "S2.2"
>  }
> ]
> Shell cwd was reset to /home/runner/work/dokima/dokima

`5. Bash`
```
mkdir -p /tmp/dokima-out; cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/02-reviewer-plan.json'))['handback']['asks']
for a in prev:
    if a['ask'].startswith('code catches file paths'): a['criterion']='S2.1'
    if a['ask'].startswith('Every check on length'): a['criterion']='S1.3'
asks=prev+[{"ask":"Yes, evidence keeps file paths.","source":"https://github.com/dokima-dev/dokima/issues/470","criterion":"S2.4"}]
r={"previous_step":{"did":["The planner added a story 2 criterion that lets a raise's evidence keep file paths and code names."],
 "decided":["It kept the four stories and their other criteria unchanged."],
 "open":["Its question on evidence was answered yes by the owner with /review."]},
 "verdict":"approve",
 "summary":"Every ask has a criterion, and the evidence reading now matches the owner's answer.",
 "raises":[{"kind":"issue","label":"Absorbed issues","text":"The issue absorbs #229, #243 and #463, but the plan links none of them, so they may stay open after this lands.","evidence":"The issue says 'Absorbs #229, #243 and #463.'; the plan's links name only #455, #242 and #241."}],
 "answers":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 470 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> (Bash completed with no output)

**Agent:** I approved the plan for [#470](https://github.com/dokima-dev/dokima/issues/470) (short, plain-English writing checked by code). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Last round's blocker is fixed.** Story 2 now has a criterion that lets a raise's evidence keep file paths and code names. You confirmed that with "/review Yes, evidence keeps file paths."
- **Every ask has a criterion.** I listed 22 of your asks, from the issue text and your comments. Each one matches a criterion in the four stories, and none is missing. The sizing caps and the phone-screen rule are left out because you dropped them.
- **The plan's claims about the code are accurate.** I checked them: today's word caps, the prompt being built in `agent.yml`, and where Next quotes every raise in full. This is a split, so there are no tests to run yet; each story gets its own plan and tests later.
- **One note that doesn't block:** your issue says it absorbs [#229](https://github.com/dokima-dev/dokima/issues/229), [#243](https://github.com/dokima-dev/dokima/issues/243) and [#463](https://github.com/dokima-dev/dokima/issues/463), but the plan links none of them. They could stay open after this lands, so I raised it as a separate issue for you to file or not.

I didn't answer the plan's open question on evidence for you, because your own `/review` comment already answers it.
