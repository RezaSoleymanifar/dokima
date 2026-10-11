# reviewer (plan) for #438

Run: https://github.com/dokima-dev/dokima/actions/runs/38106852452

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
```

> <persisted-output>
> Output too large (38.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/993557ac-18d9-4bed-9747-67d26cb0cc5a/tool-results/b09bbkvgy.txt
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
> 01-cancelled.json
> 02-planner.json
> 03-reviewer-plan.json
> 04-planner.json
> # Issue #438: One workflow redraws the card on every change to an issue or its pull request
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 437, 439 -->
> <!-- dokima-blocking: {"blocked_by": [437, 439], "blocks": [], "loop": []} -->
> Every change on an issue or its pull request redraws both cards from card.yml alone, and card pull requests are played on the sandbox first.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: [answer 1 question](https://github.com/dokima-dev/dokima/issues/438#issuecomment-6103178423) with `/plan`, `/work` or `/review`
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:**
> 
> - https://github.com/dokima-dev/dokima/issues/437
> - https://github.com/dokima-dev/dokima/issues/439
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:**
> 
> - https://github.com/dokima-dev/d

`2. Bash`
```
cd /tmp/pack; sed -n '/Original issue/,$p' issue.md | head -300
```

> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #425, story 2</summary>
> 
> **Part of:** #425 The card always shows what is true right now: one rule, one place
> 
> **User story:** Whatever changes on an issue or its pull request, including the bot's own edits, its card and its pull request's card are redrawn from GitHub's state now, by card.yml alone.
> 
> **Context:** Today card.yml (.github/workflows/card.yml line 33) picks moments: it skips the bot's edits and comments except a code review's live card on a pull request, and redraws on run start only for the full suite. That is the #419 bug: the code review's record is an edit of its live card by the bot, so no redraw followed. Other writers: dokima/planner.py line 545 saves its own plan_text above the marker, and dokima/agent.py line 1388 calls card.draw for linked issues when a plan is approved. card.draw already has changed_only (dokima/card.py line 854), which keeps the bot's own card save from redrawing forever. The issue explicitly asks for workflow and card changes, so .github/workflows/card.yml, reviews.yml and dokima/card.py are in reach. The owner asked (comment of 2026-10-10T18:12:56Z) that the play-through run by itself on every such pull request and pass before it merges; that lands here, the first story whose code passes it. Step 6 of AGENTS.md already merges on autopilot only with every check green on the head. Making the check req

`3. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json; cat parent.json | head -50
```

> {
>  "kind": "feature",
>  "summary": "Every change on an issue or its pull request redraws both cards from card.yml alone, and card pull requests are played on the sandbox first.",
>  "feature": "Whatever changes on an issue or its pull request, including the bot's own edits, its card and its pull request's card are redrawn from GitHub's state now, by card.yml alone. Stories: (1) card.yml redraws both cards on every change. (2) Only card.yml writes the card; depends on (1). (3) Card pull requests play the play-through as a required check; depends on (1) and (2).",
>  "stories": [
>   {
>    "title": "card.yml redraws both cards on every change to an issue or its pull request",
>    "user_story": "Whatever changes on an issue or its pull request, the bot's own edits and comments included, card.yml redraws its card and its pull request's card from GitHub's state now.",
>    "context": "Today .github/workflows/card.yml picks moments: it skips the bot's edits and comments except a code review's run card on a pull request, and redraws on a run's start only for the full suite. That is the #419 bug: the code review's record is the bot's edit of its run card, so no redraw followed. card.draw already has changed_only (dokima/card.py), which lets the bot's own card save end the chain. Older tests pin the skips and change with this story: test_card.py::test_same_card_on_issue_and_pr_and_only_icons_change, test_card_guard.py::test_bot_edits_do_not_retrigger_card, test_hand_links.py::test_card_yml_start

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json
for f in ['in/03-reviewer-plan.json','in/04-planner.json']:
  d=json.load(open(f)); print(f, json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:2500])
"; cd /home/runner/work/dokima/dokima; grep -rn "one level\|level" dokima/split*.py dokima/plan*.py 2>/dev/null | head -30; ls dokima
```

> in/03-reviewer-plan.json {
>  "role": "reviewer",
>  "stage": "plan",
>  "run_id": "38094071797",
>  "commit_before": "e496c72783684d4bc136d8d4a69734974937b542",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 258296,
>   "turns": 11,
>   "cost_usd": 0.6605175999999999,
>   "tokens_in": 539677,
>   "tokens_out": 5657
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/438/38094071797-reviewer-plan.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38094071797",
>  "check": {
>   "passed": true,
>   "problems": []
>  },
>  "url": "https://github.com/dokima-dev/dokima/issues/438#issuecomment-6103178423"
> }
> in/04-planner.json {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38106217889",
>  "commit_before": "e496c72783684d4bc136d8d4a69734974937b542",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 644385,
>   "turns": 34,
>   "cost_usd": 1.4216251999999998,
>   "tokens_in": 2429374,
>   "tokens_out": 15130
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/438/38106217889-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38106217889",
>  "check": {
>   "passed": true,
>   "problems": []
>  },
>  "url": "https://github.com/dokima-dev/dokima/issues/438#issuecomment-6104738795"
> }
> agent.py
> app.json
> audit.py
> board.py
> body.py
> card.py
> checks.py
> fence.py
> icons
> manifest.py
> plan.py
> planner.py
> playthrough.py
> raises.py
> retry.py
> roles
> scan.py
> trail.py
> uptodate.py
> wor

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "split\|stories\|sub-issue\|parent" dokima/plan.py | head -60; grep -n "parent" dokima/agent.py | head -30
```

> 53:    for line in (body or "").splitlines():
> 129:    for line in (codeowners or "").splitlines():
> 130:        parts = line.split("#")[0].split()
> 166:    owner, name = repo.split("/")
> 183:    owner, name = repo.split("/")
> 314:def problems_for_owner(a, number, parent):
> 324:    where = f"{issue_url(number)}, its parent {issue_url(parent)}, one of their comments' links" if parent \
> 326:    if not filled(a.get("source")) or not owner_source(a["source"].strip(), number, parent):
> 351:        number, parent = pack_issue(pack_dir), pack_parent(pack_dir)
> 354:                bad += problems_for_owner(a, number, parent)
> 360:def story_body(parent, i, story, parent_title):
> 363:             f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
> 364:             f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
> 374:def file_split(repo, parent, recs, labels=()):
> 375:    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
> 383:    title = json.loads(gh("issue", "view", str(parent), "-R", repo, "--json", "title"))["title"]
> 387:        url = gh("issue", "create", "-R", repo, "--title", st["title"], "--body", story_body(parent, i, st, title), *extra).strip()
> 390:        gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues", "-F", f"sub_issue_id={node}")
> 1066:def parent_of(repo, number):
> 1067:    """The issue's parent number on GitHub; Non

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "/ 3\|// 3\|ceil\|too big\|stories" dokima/agent.py dokima/plan.py | head -40; cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/02-planner.json'));h=d.get('handback') or d.get('plan') or d; print(list(d.keys()))"
```

> dokima/agent.py:375:    """File the stories of the newest approved split as sub-issues of the parent, in order, with their blocked-by links,
> dokima/agent.py:385:    for i, st in enumerate(plan["stories"], 1):
> dokima/agent.py:400:    return {"role": "split", "stage": None, "handback": {"stories": filed}, "check": {"passed": True, "problems": []}}
> dokima/agent.py:590:    The planner's changes to older tests, with their reasons, and a split's stories in detail; nothing it repeats from
> dokima/agent.py:597:                         ("Stories in detail", bullets(h.get("stories"), lambda st: f"{st.get('title', '')}: {st.get('user_story', '')}"))):
> dokima/agent.py:634:        return f"The planner proposes a split into {len(h.get('stories') or [])} stories."
> dokima/agent.py:644:        return f"Code filed the split as {len(h.get('stories') or [])} stories."
> dokima/agent.py:730:        lines += [f"{i}. {st.get('title', '')}" for i, st in enumerate(h.get("stories", []), 1)]
> dokima/agent.py:744:        num = {f["story"]: f["issue"] for f in h.get("stories", [])}
> dokima/agent.py:746:                         for f in h.get("stories", [])]
> dokima/agent.py:773:                  ("Stories in detail", bullets(h.get("stories"), lambda st: f"{st.get('title', '')}: {st.get('user_story', '')}"))]
> dokima/agent.py:808:        n = len(h.get("stories") or [])
> dokima/agent.py:809:        return f"The planner proposes a split into {n} stories" + (" and asks you questions." if h.get("questions") else ".")

**Agent:** I'm reviewing the planner's proposed split of #438. Next I'm checking the size rule and the planner's prompt.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn -i "split\|one level\|story\b" dokima/roles/*.md | head -40; python3 -c "
import json;d=json.load(open('/tmp/pack/in/02-planner.json'))['handback'];print(len(d.get('acceptance_criteria',[])), [c['text'][:80] for c in d.get('acceptance_criteria',[])]); print(len(d.get('non_functional',[])))"
```

> dokima/roles/reviewer.md:20:You may be on round one or round ten. The issue and its pull request hold the whole history, oldest first. Since your
> dokima/roles/reviewer.md:42:split) or marked "missing". An ask marked missing is a blocker: a plan review with one cannot approve. A code review of
> dokima/roles/planner.md:6:End with exactly one of two: a plan (with its tests) or a split into 2 to 5 child issues. Your questions for the owner
> dokima/roles/planner.md:7:go inside it, as raises. Too big for one PR is not a question: split it.
> dokima/roles/planner.md:10:You may be on round one or round ten. The issue and its pull request hold the whole history, oldest first: the owner's
> dokima/roles/planner.md:39:Write the plan the way a product manager writes a story, in these terms:
> dokima/roles/planner.md:40:- **User story:** one sentence, what changes for the owner when this is done. It replaces "Objective".
> dokima/roles/planner.md:41:- **Feature:** a parent issue that splits into 2 to 5 user stories. Each story says which other stories it depends on.
> dokima/roles/planner.md:48:- **Non-functional requirements:** story-specific engineering (security, reliability, failure paths), one plain line
> dokima/roles/planner.md:54:- **Out of scope:** plain sentences about what this story deliberately won't do.
> dokima/roles/planner.md:79:- User story: Owners see one card at the top of every issue and PR, drawn by code from GitHub's records.
> dokima/roles/planner.md:104:# Split
> dokima/roles/planner

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "+ 2) // 3\|/ 3\|ceil\|size" dokima/agent.py | head -20; sed -n 100,115p dokima/roles/planner.md; sed -n 30,40p dokima/roles/plan-grade.md
```

> Current runner (the only one Dokima supports today): python3 -m pytest, tests in tests/, and each test names its criterion with
>     record_property("proves", "N.k")
> 
> # Split
> Split when R1 the issue holds more than one independent goal, R2 it needs more than five criteria, or R3 the work spans
> unrelated parts of the code. Name the rule. Do not split when the parts cannot land separately: main must work after each.
> List every promise of the issue, then give each to exactly one child. Each child: a title, its task in plain words,
> context (what you found, so its planner does not redo your research), its criteria, the promises it keeps, and which
> siblings must merge first. Code files the children as sub-issues with blocked-by links.
> 
> # Raising and answering
> The planner, the worker and the reviewer raise and answer through two fields of their hand-back, and nowhere else.
> - "raises": everything you hand up for someone else to decide, fix or file, each an object with "kind", "to",
>   "label", "text" and "evidence"; label and evidence are optional. The kind is one of three. A question is something only the one it is for can decide; say the reading you went on. A
>   blocker is something that must be fixed before the work goes on, sent to whoever fixes it. An issue is a real problem
>    that run the thing over tests that read code.
> 5. Today, every new test fails for the right reason: the feature is missing, not a crash, a missing tool or a bad path.
> Never blockers:
> 6. Every failure the cri

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner turned #438 into a split of three stories: card.yml redraws on every change, only card.yml writes the card, and card pull requests play the play-through as a required check."],
  "decided": ["The merge-queue rule from the last plan (438.9) is dropped, following the owner's \"Keep to my words; smallest change.\"",
              "Story 2 waits for story 1, and story 3 waits for stories 1 and 2."],
  "open": ["No tests yet: each story would plan its own, and the last plan's tests on try/issue-438 are offered for the stories to take over."]},
 "verdict": "block",
 "summary": "The plan splits #438 into three stories, which fits neither the size rule (five criteria make two stories) nor AGENTS.md (a split is one level, and #438 is already story 2 of #425), and you asked for the smallest change.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Wrong plan",
   "text": "The split has three stories for five criteria. The size rule makes that two stories (5 / 3, rounded up), and AGENTS.md allows only one level of split, while #438 is already story 2 of #425's split. The owner also asked for the smallest change. The split names none of the split rules either: R2 needs more than five criteria and #438 has five. Smallest fix: hand back #438 as one plan with its five criteria, three non-functional lines and the tests already on `try/issue-438`, without 438.9, unless the owner answers the question below otherwise.",
   "evidence": "plan.json: `kind` is `feature` with 3 `stories` holding 1, 1 and 3 criteria; `parent.json` names #425; AGENTS.md, Splitting and the graph: \"2 to 5 children, one level\"; dokima/roles/planner.md line 105: \"R2 it needs more than five criteria\"; owner's comment of 2026-10-11T02:46:10Z: \"Keep to my words; smallest change.\""},
  {"kind": "question", "to": "owner", "label": "Two rules disagree",
   "text": "#438 has five criteria. 
```

> Exit code 1
> summary holds 40 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> behaviors has no judgment of criterion S1.2: say one_behavior true or false, and why in one line
> behaviors has no judgment of criterion S1.3: say one_behavior true or false, and why in one line
> behaviors has no judgment of criterion S2.2: say one_behavior true or false, and why in one line

`10. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
p='review.json'; r=json.load(open(p))
r["summary"]="The three-story split fits neither the size rule (five criteria make two stories) nor AGENTS.md's one-level split; #438 is already a story."
r["behaviors"][1:1]=[{"criterion":"S1.2","one_behavior":True,"why":"One behavior: a redraw that finds both cards current writes nothing."},
 {"criterion":"S1.3","one_behavior":True,"why":"One behavior: every redraw runs main's copy of card.yml and dokima/card.py."}]
r["behaviors"].insert(4,{"criterion":"S2.2","one_behavior":False,"why":"Two results: the run fails naming the issue, and the next change or sweep redraws it."})
json.dump(r,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

`11. Bash`
```
cd /tmp/dokima-out; python3 - <<'EOF'
import json
p='review.json'; r=json.load(open(p))
r["size"]="Five criteria make two stories by the size rule, not three; S2.2, S3.2 and S3.3 each bundle two behaviors; and #438 is already a story of #425, so AGENTS.md's one-level rule forbids splitting it."
json.dump(r,open(p,'w'),indent=1)
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 438 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I blocked the plan for [#438](https://github.com/dokima-dev/dokima/issues/438) (card.yml redraws every card), and the hand-back is in `/tmp/dokima-out/review.json`. Both of Dokima's checks on it pass.

**What the planner did:** It split #438 into three stories:
1. card.yml redraws both cards on every change.
2. Only card.yml writes the card.
3. Card, board and workflow pull requests run the play-through as a required check.

It dropped last round's extra merge-queue rule (438.9), as you asked with "Keep to my words; smallest change."

**Why I blocked it:**
- **Wrong number of stories (sent back to the planner):** Three stories for five criteria fits no rule. The size rule (criteria ÷ 3, rounded up) gives two stories. AGENTS.md allows only one level of split, and #438 is already story 2 of [#425](https://github.com/dokima-dev/dokima/issues/425) (the card always shows what is true now). The split also doesn't name which split rule it uses. The rule for "more than five criteria" doesn't apply, because #438 has exactly five. The smallest fix is to hand back #438 as one plan, using the tests already on `try/issue-438` and leaving out 438.9.
- **A question for you:** The size rule and AGENTS.md disagree here. One says five criteria make two stories; the other says a story can't be split again. My review assumes #438 stays one plan, because of the one-level rule and your ask for the smallest change. Since this question is addressed to you, the river stops until you answer.
- **Criteria bundling two things:** Three criteria each hold two behaviors:
  - The check runs on card pull requests, and passes without playing on all others.
  - Autopilot waits for a green check, and the pull request names the branch protection setting that makes the check required.
  - A card that can't be redrawn fails its run naming the issue, and the next change or 15-minute sweep redraws it.

**Not checked:** I ran no tests, because a split has none at this stage. Each story would plan its own.

**Found along the way:**
- The copies of `dokima/roles/plan-grade.md` and `planner.md` on this branch describe an older size rule (split only above five criteria) than the one my review instructions use (criteria ÷ 3). This may be what led the planner to split, so it's worth bringing them in line.
- The planner also added a detail you didn't write: the setting goes in the header of `playthrough.yml`, where you said "this story's pull request names" it. I didn't block on this.

There were no open raises from earlier rounds to answer.
