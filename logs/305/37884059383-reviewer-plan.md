# reviewer (plan) for #305

Run: https://github.com/dokima-dev/dokima/actions/runs/37884059383

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (76.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/f2f1b49d-e666-4414-80d9-54a61aadedf6/tool-results/b903as01y.txt
> 
> Preview (first 2KB):
> .:
> in
> issue.md
> open_blockers.json
> plan.json
> 
> ./in:
> 01-planner.json
> 02-reviewer-plan.json
> 03-planner.json
> # Issue #305: Rewrite the README and wiki to match the current code
> 
> <!-- dokima-card -->
> The README and the wiki are rewritten to describe Dokima as it works today, in one plain style.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Answer the questions with /plan, or say /review
> 
> [issue #305](https://github.com/dokima-dev/dokima/issues/305)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocks.svg" width="16" height="16" align="absmiddle" alt="blocks"> **Blocks:** #306
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #137, #114, #291
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> 
> **Scope:**
> 
> 
> **Out of scope:**
> 
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16"

`2. Bash`
```
cd /tmp/pack; sed -n '/dokima-card/,$p' issue.md | grep -v 'raw.githubusercontent' | head -300
```

> <!-- dokima-card -->
> The README and the wiki are rewritten to describe Dokima as it works today, in one plain style.
> 
> 
> [issue #305](https://github.com/dokima-dev/dokima/issues/305)
> 
> 
> 
> 
> **Scope:**
> 
> 
> **Out of scope:**
> 
> 
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Rewrite the README and the wiki so they describe Dokima as it works today and read like the docs of an established, polished tool.
> 
> ## Context
> 
> The README pitches four times before it says what Dokima is, has no quickstart, and its roadmap shows every box unticked even though the planner, reviewer, cards, autopilot and merge gate all exist. Parts of the docs are now wrong: they say adding the `work` label approves a plan (it is `/work`), the sidebar links to the old `RezaSoleymanifar/dokima` repo, the README says merges happen on their own and labels say whose turn it is. `tests/test_wiki.py` pins the stale "`work` label" wording. The last docs change was around #108.
> 
> `docs/wiki/` stays the only place docs are written; `wiki.yml` already mirrors it to the GitHub wiki.
> 
> ## What I want
> 
> README:
> - First sentence says plainly what Dokima is. Tagline: "Agents write the code. Dokima proves it's done."
> - One diagram of the flow: issue, planner, owner approves, worker, reviewer, gate, main.
> - A short quickstart, and an honest shipped vs planned table.
> - Badges for CI and license. Drop the stacked pitch sections and the hype.
> 
> Wiki, in this order, with nothing repeated between pages:
> - Get started (a blank repo to a first mer

`3. Bash`
```
cd /tmp/pack; sed -n '/dokima-card/,$p' issue.md | grep -v 'raw.githubusercontent' | sed -n '300,$p' | grep -n '^### ' ; cat open_blockers.json; python3 -c "
import json
for f in ['in/02-reviewer-plan.json','in/03-planner.json']:
  d=json.load(open(f)); print(f, json.dumps(d,indent=1)[:6000])
"
```

> 19:### dokima-runtime on issue #305 (2026-10-09T04:15:39Z)
> 256:### RezaSoleymanifar on issue #305 (2026-10-09T04:26:32Z)
> 260:### dokima-runtime on issue #305 (2026-10-09T04:27:04Z)
> 506:### dokima-runtime on issue #305 (2026-10-09T04:28:41Z)
> []in/02-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "37883035387",
>  "commit_before": "d99847b719bee7d724090c48566b2b342fdcfca0",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 62087,
>   "turns": 8,
>   "cost_usd": 0.45554160000000005,
>   "tokens_in": 300171,
>   "tokens_out": 6650
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/305/37883035387-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/37883035387",
>  "handback": {
>   "previous_step": {
>    "did": [
>     "The planner split the issue into 4 stories: the reference pages; Get started and the how-tos; Home, How Dokima works, FAQ and the sidebar; the README."
>    ],
>    "decided": [
>     "The plan and work labels are described as they still work, while /plan and /work are shown as the way to approve.",
>     "The README uses this issue's tagline, not the one #137 asked for."
>    ],
>    "open": [
>     "Which license Dokima carries: the planner assumed MIT, since the repo has no LICENSE file for the badge to read."
>    ]
>   },
>   "verdict": "approve",
>   "summary": "The split covers every ask across four stories; the MIT license assumption is the owner's call, so that question waits 

**Agent:** Let me see the owner's comment at 04:26.

`4. Bash`
```
cd /tmp/pack; sed -n '/dokima-card/,$p' issue.md | grep -v 'raw.githubusercontent' | sed -n '550,570p'; python3 -c "
import json
d=json.load(open('plan.json')); 
print(json.dumps(d.get('questions'),indent=1)); print(d['feature']); s=d['stories'][3]; print(json.dumps(s,indent=1)[-3500:])
print([ (i,len(s['acceptance_criteria'])) for i,s in enumerate(d['stories'])])
"; diff <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/plan.json')),indent=1,sort_keys=True))") <(python3 -c "import json;print(json.dumps(json.load(open('/tmp/pack/in/03-planner.json'))['handback'],indent=1,sort_keys=True))") | head -30
```

> **Next:** @RezaSoleymanifar The reviewer did not accept the plan's assumption for: "The repo has no LICENSE file, so a license badge has nothing to show. Which license should Dokima carry?" Answer with `/plan` and your words, or say `/work` to build it on its assumptions.
> 
> 
> ### RezaSoleymanifar on issue #305 (2026-10-09T04:26:32Z)
> 
> /plan Answer: Apache 2.0. Add the LICENSE file with it.
> 
> ### dokima-runtime on issue #305 (2026-10-09T04:27:04Z)
> 
> <!-- dokima-record -->
> 
> **Feature:** The docs describe Dokima as it works today. Rule R2: the issue holds more than five criteria (four README promises, nine wiki pages, the style rules and the test change). Stories: (1) the reference pages; (2) Get started and the how-tos, depending on (1); (3) Home, explanation, FAQ and sidebar, depending on (1) and (2); (4) the README and its Apache 2.0 LICENSE file, depending on (2).
> 
> 1. The wiki's reference pages describe every command, label, card field and setting as the code has them today
> 2. Get started and the how-to pages take an owner from a blank repo to a merged pull request
> 3. The wiki's Home, explanation, FAQ and sidebar link the pages in order with nothing repeated
> 4. The README says what Dokima is, shows the flow and a quickstart, is honest about what has shipped, and the repo carries an Apache 2.0 license
> 
> 
> null
> The docs describe Dokima as it works today. Rule R2: the issue holds more than five criteria (four README promises, nine wiki pages, the style rules and the test change). Stor

`5. Bash`
```
mkdir -p /tmp/dokima-out; cd /tmp; python3 - <<'EOF'
import json
prev=json.load(open('/tmp/pack/in/02-reviewer-plan.json'))['handback']
asks=prev['asks']
for a in asks:
    if a['criterion']=='S4.5':
        a['ask']="Badges for CI and license. Drop the stacked pitch sections and the hype."
asks.append({"ask":"Answer: Apache 2.0. Add the LICENSE file with it.","source":"https://github.com/dokima-dev/dokima/issues/305","criterion":"S4.5"})
r={"previous_step":{"did":["The planner re-planned after the owner chose Apache 2.0: story 4 now adds a LICENSE file at the repo root with the full Apache License 2.0 text and an Apache 2.0 license badge in the README.","The other three stories and the split are unchanged."],
 "decided":["The plan carries no open questions."],"open":[]},
 "verdict":"approve",
 "summary":"The re-plan takes the owner's Apache 2.0 answer into story 4 and still covers every ask across four stories, so the split is ready for /work.",
 "blockers":[],
 "notes":[{"text":"Story 3 rewrites Home but has no criterion that tests/test_wiki.py stops pinning the stale wording on Home; its planner should add one when it plans the story.","evidence":"tests/test_wiki.py test_home asserts \"`work` label\" in Home.md; S1.4 and S2.5 cover only their own pages; S3 names it only in its context."}],
 "resolved":[],"issues_found":[],"asks":asks}
json.dump(r,open('/tmp/dokima-out/review.json','w'),indent=1)
EOF
grep -n 'work. label' /home/runner/work/dokima/dokima/tests/test_wiki.py; cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 305 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> 15:    assert "`work` label" in text
> 29:    assert "`work` label" in read("Home.md")
> summary holds 26 words, over its cap of 25 (up to 30 passes)

`6. Bash`
```
python3 - <<'EOF'
import json
p='/tmp/dokima-out/review.json'; r=json.load(open(p))
r['summary']="The re-plan takes the owner's Apache 2.0 answer into story 4 and still covers every ask, so the split is ready for /work."
json.dump(r,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 305 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the re-plan for issue #305. My review is saved to `/tmp/dokima-out/review.json` and passes both checks.

- **Your licence answer is in the plan.** Story 4 now adds a LICENSE file at the repo root with the full Apache License 2.0 text, and the README gets an Apache 2.0 licence badge beside the CI badge.
- **Nothing else changed.** The split is still four stories:
  1. The three reference pages.
  2. Get started and the three how-to pages.
  3. Home, How Dokima works, the FAQ and the sidebar.
  4. The README and the LICENSE file.
- **Every ask is covered.** I matched each ask in the issue to a criterion, and added your "Apache 2.0" comment as an ask covered by story 4.
- **No open questions or blockers.** The plan has no questions left. There were no earlier blockers to carry over.
- **One note, not a blocker.** `tests/test_wiki.py:29` still checks for the old "`work` label" wording in `Home.md`. Story 3 rewrites Home but only mentions this test in its background text, with no criterion requiring the change. Whoever plans story 3 should add one.

It's waiting for you to say `/work`, because you've commented since the last plan.
