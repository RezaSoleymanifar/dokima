# reviewer (plan) for #470

Run: https://github.com/dokima-dev/dokima/actions/runs/38090098313

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat plan.json; cat open_blockers.json
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
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/question.svg" width="16" height="16" align="absmiddle" alt="question"> **Doubt: overlaps #241 and #242:** #242 puts reading rules in each role file, and #24

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat /tmp/pack/parent.json | head -50; python3 -c "import json;d=json.load(open('/tmp/pack/in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:1500])"; git log --oneline | grep -E '#(229|243|463|241|242)\b' ; grep -rn "463\|#243\|#229" AGENTS.md dokima/roles | head; grep -n "cat dokima/roles" .github/workflows/*.yml; grep -n "evidence" dokima/agent.py | head -30
```

> {"number": null}{
>  "role": "planner",
>  "stage": null,
>  "run_id": "38089381509",
>  "commit_before": "bf1443b25e29a12d5eeb00b2a4b60822404cc84b",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 120252,
>   "turns": 13,
>   "cost_usd": 0.8776498000000001,
>   "tokens_in": 745513,
>   "tokens_out": 12056
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/470/38089381509-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38089381509",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> .github/workflows/planner.yml:70:          claude -p "$(cat dokima/roles/plan-grade.md dokima/roles/planner.md)
> .github/workflows/worker.yml:69:          claude -p "$(cat dokima/roles/result-grade.md dokima/roles/worker.md)
> 146:    out = {"kind": "blocker", "to": to, "label": b.get("criterion"), "text": text, "evidence": b.get("evidence"),
> 686:        if filled(r.get("evidence")):
> 687:            lines.append(f"  - Evidence: {card.escape(escape_line(r['evidence']))}")
> 735:                 if files else []) + ([f"- Its own test run: {escape_line(h['evidence'])}"] if filled(h.get("evidence")) else [])
> 772:                  ("Concerns", bullets(h.get("concerns"), lambda c: f"{c.get('text', '')} ({c.get('evidence', '')})")),
> 776:                   + ([f"- Its own test run: {h['evidence']}"] if h.get("evidence") else [])),
> 778:                  ("What it raised", bullets(h.get("suspect_tests"), lambda t: f"Suspect test {t.get(

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "roles" .github/workflows/agent.yml | head; sed -n 1180,1195p dokima/agent.py; sed -n 1250,1258p dokima/agent.py; grep -n "evidence" dokima/roles/*.md | head -20
```

> 227:          claude -p "$(cat /tmp/runtime/dokima/roles/$GRADE.md /tmp/runtime/dokima/roles/$ROLE.md)
>     return source == "AGENTS.md" or any(re.fullmatch(re.escape(issue_url(n)) + r"(#issuecomment-\d+)?", source)
>                                         for n in ([number, parent] if parent else [number]))
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
>     return bad
> 
> 
>     crit = h.get("criteria")
>     if not isinstance(crit, dict) or not crit:
>         bad.append("criteria must be an object giving one line per criterion")
>     else:
>         bad += [f"criteria: the line for {k} must be non-empty text" for k, v in crit.items() if not filled(v)]
>     if not filled(h.get("evidence")):
>         bad.append("evidence must name the last test command and its result line")
>     return bad
> 
> dokima/roles/worker.md:26:   whole pull request. If you have concrete evidence a test is wrong, raise it as a blocker for the planner instead of working around it.
> dokima/roles/worker.md:29:   evidence the reviewer can check.
> dokima/roles/worker.md:45:  "label", "text" and "e

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "\"context\"\|\['context'\]\|get(\"context\")" dokima/*.py | head
```

> dokima/agent.py:365:    if story.get("context"):
> dokima/agent.py:366:        lines += [f"**Context:** {story['context']}", ""]
> dokima/agent.py:1946:    running += [s.get("context") for s in statuses if s.get("state") == "pending"]
> dokima/audit.py:240:        return {"required_checks": checks.get("contexts") or [c["context"] for c in checks.get("checks") or []]}

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 345,375p dokima/agent.py
```

> if role == "reviewer":
>         questions = [r for r in open_raises(pack_records(pack_dir))
>                      if r.get("kind") == "question" and r.get("to") == "owner" and r.get("raised_by") == "planner"]
>     bad = raises.check_answers(role, answers, listed + questions)
>     if questions and isinstance(answers, list):
>         asked = {r["id"] for r in questions}
>         number, parent = pack_issue(pack_dir), pack_parent(pack_dir)
>         for a in answers:
>             if isinstance(a, dict) and a.get("raise") in asked:
>                 bad += problems_for_owner(a, number, parent)
>     if role == "planner":
>         bad += problems_links(h, pack_dir)
>     return bad
> 
> 
> def story_body(parent, i, story, parent_title):
>     """A story's issue body, drawn by code from the approved plan, so the child planner starts from exactly what was agreed."""
>     lines = ["<!-- dokima-card -->", "<!-- /dokima-card -->", "",
>              f"<details open><summary>From the approved plan of #{parent}, story {i}</summary>", "",
>              f"**Part of:** #{parent} {parent_title}", "", f"**User story:** {story.get('user_story', '')}", ""]
>     if story.get("context"):
>         lines += [f"**Context:** {story['context']}", ""]
>     lines += ["**Acceptance criteria:**"]
>     lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
>     if story.get("non_functional"):
>         lines += ["", "**Non-functional:**"] + [f"- {n.get('text', '')} ({n.get('why', 

**Agent:** I'm checking the split plan for #470 against the owner's words and comments; next I'll write the review file.

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner split the issue into four stories: whole-text word caps, sending back file paths and code names, one shared style file heading every prompt, and one line per question with the reviewer's take."],
  "decided": ["It dropped plan sizing and the caps on how many criteria, tests and questions a plan has, after the owner's comment.", "It set a criterion at 12 words with no slack and left the other limits to the first story."],
  "open": ["Its three questions (phone screen, jargon by code, closing #241 and #242) were answered yes by the owner."]},
 "verdict": "block",
 "summary": "The split covers every ask, but story 2 would also send back file paths in a raise's evidence, which every agent is told to give, without asking the owner.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Two readings: evidence",
   "text": "Story 2 sends back any file path in every field of story 1's list, and that list includes a raise's evidence. Every agent is told to back a raise with a file and line, so this changes how raising works. The owner never said whether evidence counts. Ask the owner whether evidence may keep file paths, or add a story 2 criterion that names evidence as exempt, and say which reading the plan takes.",
   "evidence": "Story 1's context lists 'each raise's label and text and evidence'; story 2's context says 'Use the same field list'. dokima/roles/worker.md:54 and planner.md:25 say evidence is 'a file and line'. The owner's reply of 2026-10-10 says only 'code catches file paths and code names'."}
 ],
 "answers": [],
 "asks": [
  {"ask": "Simple, terse, plain English, no jargon, high signal, focused on what matters.", "source": "https://github.com/dokima-dev/dokima/issues/470", "criterion": "S3.1"},
  {"ask": "Technical detail (function names, mechanisms, file paths, edge cases) belongs in code docstrings, not in anything I read on GitHub.", "s
```

> summary holds 29 words, over its cap of 25 (up to 30 passes)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="Every ask is covered, but story 2 would reject file paths in a raise's evidence without asking the owner."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 470 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#470](https://github.com/dokima-dev/dokima/issues/470) (short, plain writing for the owner) and sent it back to the planner over one problem. The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the plan covers:** it splits the issue into four stories:
1. Code caps the whole text of every field you read, with a criterion capped at 12 words and no slack.
2. Code sends back any text you read that names a file path or a code name.
3. One shared style file heads every agent's prompt, with the word limits, the #451 before/after example and a checklist.
4. Each question for you is one line with the reviewer's take, and Next only says what to do.

Every ask in your issue and your comment maps to a criterion; none are missing. Plan sizing and the caps on how many criteria, tests and questions a plan has are dropped, as you asked. Your `/review` reply already answered the planner's three questions, so the review gives no answers to them.

**The blocker:** story 2 would send back a file path in any field from story 1's list, and that list includes the evidence behind a raise. Every agent's instructions say that evidence should be "a file and line", so this would change how raising works. Your words cover file paths in what you read, but don't say whether evidence counts. The fix I asked for is either of these:
- the planner asks you whether evidence may keep file paths, or
- it adds a criterion to story 2 that keeps evidence out of the check, and says which reading it chose.

The block goes back to the planner automatically, so there's nothing for you to do yet. If the planner asks, the river will stop for your answer.
