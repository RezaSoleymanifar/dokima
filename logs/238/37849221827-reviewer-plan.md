# reviewer (plan) for #238

Run: https://github.com/dokima-dev/dokima/actions/runs/37849221827

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  8 21:47 .
> drwxrwxrwt 18 root   root   4096 Oct  8 21:47 ..
> drwxr-xr-x  2 runner runner 4096 Oct  8 21:47 in
> -rw-r--r--  1 runner runner 8646 Oct  8 21:47 issue.md
> -rw-r--r--  1 runner runner    2 Oct  8 21:47 open_blockers.json
> -rw-r--r--  1 runner runner 2419 Oct  8 21:47 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  8 21:47 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 21:47 ..
> -rw-r--r-- 1 runner runner 3019 Oct  8 21:47 01-planner.json
> # Issue #238: On autopilot, a question the reviewer answers from the owner's words shows plainly
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 5</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** When the plan reviewer on autopilot answers a planner's question for the owner from the owner's own words, the run comment shows the question, the answer below it, and the evidence: the owner's words linked to where they said them.
> 
> **Context:** dokima/agent.py render() today shows each judged assumption on one line under 'The plan's assumptions:' ('Accepted on your words "..." (source).' or 'Not accepted: why'). The reviewer's hand-back already holds assumptions with question, accepted, matched and source (problems_assumptions, ASSUMPTION_SHAPE); the answer is the plan's assumption for that question. The question icon comes from story 1's table.
> 
> **Acceptance criteria:**
> - W

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_answered_questions.py; git show --stat HEAD
```

> """A question the reviewer answers from the owner's words shows plainly (#238, story 5 of #230).
> 
> When the plan reviewer accepts a planner question's assumption on the owner's own words, the run comment shows the
> question, the answer below it (the plan's assumption for that question) and the evidence (the owner's matched words,
> linked to where they said them). Today render() packs all of that into one line under "The plan's assumptions:" and
> never shows the answer at all.
> 
> These tests run the workflow's own record step, `python3 -m dokima.agent record reviewer plan OUT check.txt true LOGS`,
> with the reviewed plan in `$PACK/plan.json` (the job-wide PACK of agent.yml, where the plan reviewer's plan lives), and
> read the comment it writes to OUT/comment.md. The answer of a question is the "assumption" the plan gave it.
> 
> What the comment must hold, pinned here:
>     the section     a heading line holding the words "Answered from your words", then the list under it: every line
>                     after the heading up to the first non-empty line that is neither a list item ("- " or "1. ") nor
>                     indented under one
>     each answer     inside the section, the question on one line, the answer on a later line and the evidence on a
>                     later line still; the evidence is a markdown link whose text holds the matched words and whose
>                     target is the source: the issue or comment link as given, or for "AGENTS.md" the file on the
>                 

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "assumption\|def render\|PACK\|plan.json\|def main\|AGENTS.md" dokima/agent.py | head -80
```

> 33:HANDBACK = {"planner": "plan.json", "reviewer": "review.json", "worker": "work.json"}
> 407:def render(rec, pr=None):
> 450:        judged = [a for a in h.get("assumptions") or [] if isinstance(a, dict)]
> 452:            lines += ["", "**The plan's assumptions:**"]
> 466:        lines += [f"- {q.get('question', '')} Assumed: {q.get('assumption', '')}" if isinstance(q, dict) else f"- {q}"
> 577:        json.dump(plan["handback"], open(os.path.join(dest, "plan.json"), "w"), indent=1)
> 585:QUESTION_SHAPE = '{"question": "...?", "assumption": "..."}'
> 596:            bad.append(f"question {i} must be a question and its assumption, {QUESTION_SHAPE}")
> 598:        extra = sorted(str(k) for k in q if k not in ("question", "assumption"))
> 600:            bad.append(f"question {i} has {', '.join(extra)}: a question is only the question and its assumption, "
> 602:        for field in ("question", "assumption"):
> 677:    """True when a source names the owner's words Dokima can check: the issue's own text, one of its comments, or AGENTS.md."""
> 678:    return source == "AGENTS.md" or bool(re.fullmatch(re.escape(issue_url(number)) + r"(#issuecomment-\d+)?", source))
> 681:def problems_assumptions(r, plan, number):
> 683:    saying whether its assumption is accepted and whether it changes how the system works or what it costs; one
> 686:    judged = r.get("assumptions", [])
> 688:        return [f"assumptions must be a list, one per question of the plan, each {ASSUMPTION_SHAPE}"]
> 692:            bad.append(f"a

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 400,480p dokima/agent.py; grep -n "def record\|\"record\"\|'record'" dokima/agent.py; grep -n "PACK" .github/workflows/agent.yml | head -20
```

> def record_fold(rec):
>     """The full JSON record, always the last fold of a run comment: later packs are built from it."""
>     return ["", "<details><summary>Full record</summary>", "", "```json", json.dumps(rec, indent=1), "```", "", "</details>"]
> 
> 
> def render(rec, pr=None):
>     """The comment that carries a record: one plain sentence saying what the run did, the short version the owner
>     needs at a glance, the long parts in folds, then the full record as JSON in the last fold. `pr` is the link of the
>     worker's pull request, once it exists."""
>     role, h = rec["role"], rec["handback"]
>     repo = os.environ.get("GITHUB_REPOSITORY", "")
>     if role == "not-started":
>         a = rec.get("attempt")
>         who = {"planner": "The planner", "reviewer": "The reviewer", "worker": "The worker",
>                "split": "Filing the split"}.get(a, "The command")
>         lines = [MARK, f"{icon(repo, 'failed')} {role_icon(repo, a, rec.get('stage'))}{who} stopped before any agent started.", ""] + [f"- {p}" for p in rec["check"]["problems"]]
>         lines += record_fold(rec) + ["", f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
>         return "\n".join(lines) + "\n"
>     if role == "cancelled":
>         a = rec.get("attempt")
>         who = {"planner": "The planner", "reviewer": "The reviewer", "worker": "The worker"}.get(a, "The command")
>         what = (f"{who} run was cancelled after its agent started, and nothing it handed back is used." if rec.get("agent_started")
>       

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 45,60p .github/workflows/agent.yml; grep -n "agent record" .github/workflows/agent.yml; sed -n 1435,1480p dokima/agent.py; python3 -m pytest -q tests/test_answered_questions.py 2>&1 | grep -E "^E   .*23[8]|passed|failed" | head -20
```

> jobs:
>   run:
>     environment: keys
>     runs-on: ubuntu-24.04
>     env:
>       N: ${{ (inputs.issue || github.event.client_payload.issue) }}
>       ROLE: ${{ (inputs.role || github.event.client_payload.role) }}
>       STAGE: ${{ (inputs.role || github.event.client_payload.role) == 'reviewer' && (inputs.stage || github.event.client_payload.stage) || '' }}
>       PACK: /tmp/pack
>       # Dokima's own code and prompts always come from main, never from the branch being judged.
>       PYTHONPATH: /tmp/runtime
>       PYTHONSAFEPATH: "1"
>       OUT: /tmp/dokima-out
>       MODEL: claude-opus-5-5
>       # A card already up for this run: queued by the listener, or by the hand-off that started it.
>       CARD_ID: ${{ (inputs.card || github.event.client_payload.card) }}
> 5:# conversation (comments, reviews, line notes) and every earlier agent record. The agent runs its own check before it
> 275:            python3 -m dokima.agent record "$ROLE" "$STAGE" "$OUT" "$OUT/check.txt" "${PASSED:-false}" /home/runner/.claude/projects
>     if argv[1] == "record":
>         role, stage, out, check_file, passed, log_dir = argv[2:8]
>         meta = {"run_id": os.environ.get("GITHUB_RUN_ID"), "commit_before": os.environ.get("BASE"),
>                 "started_by": os.environ.get("GITHUB_ACTOR"), "models": models_used(log_dir),
>                 "report": run_report(os.path.join(out, "claude.json")), "log": os.environ.get("LOG_URL"),
>                 "run": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.envi

`6. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote a plan with two criteria and one non-functional requirement, and three tests that run the record step and read the comment it writes."],
  "decided": ["The section is headed \"Answered from your words\"; the answer is the plan's assumption, read from the reviewed plan in the starting pack.",
              "Words from AGENTS.md link to the file on main.",
              "The question icon may lead the heading, but no test requires it; the workflow files stay as they are."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps every ask of the issue, and its three tests fail today because the comment has no answered-question section, not because of a crash.",
 "blockers": [],
 "notes": [
  {"text": "The tests list each question's judgement in the same order as the plan's questions, so code that pairs a question with its answer by position instead of by the question would still pass; the worker should pair them by the question.",
   "evidence": "tests/test_answered_questions.py: plan((Q1, A1), (Q2, A2), ...) and the assumptions list are always in the same order in all three tests."},
  {"text": "The issue's Context says the question icon comes from story 1's table; the plan leaves it optional and untested. It is not in the issue's acceptance criteria, so this is not a blocker.",
   "evidence": "plan.json out_of_scope: \"The question icon from story 1's table may lead the section's heading; no test requires it.\""}
 ],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "When the plan reviewer accepts a question's assumption on the owner's words, its run comment shows the question, then below it the answer, then the evidence: the owner's matched words, linked to where they said them.",
   "source": "https://github.com/dokima-dev/dokima/issues/238", "criterion": "238.1"},
  {"ask": "When the review answered no questi
```

> rc=0

**Agent:** I approved the plan for #238. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks (`check review` and `check-round`) passed.

- **Asks:** each of the issue's three asks is kept by a criterion: the question, then the answer, then your linked words (238.1); no section and no empty heading when nothing was answered (238.2); and only accepted questions with your words and a source shown (238.3). None is missing.
- **Tests fail today for the right reason:** I ran the three new tests and all fail because the comment has no "Answered from your words" section. Today the comment still puts each assumption on one line and never shows the answer. They fail on the missing feature, not on a crash or a bad path.
- **Answers are found:** the tests run the same record command the workflow uses, with the reviewed plan where the workflow keeps it, so the answer to each question is read from that plan.
- **Blockers:** none. The plan has no questions for you, so there are no assumptions to judge.

Two notes:
1. The tests always list the reviewer's judgements in the same order as the plan's questions. Code that pairs a question with its answer by position instead of by the question's text would still pass, so the worker should pair them by the question.
2. The issue's Context says the question icon comes from story 1's table, but the plan makes it optional and no test checks it. It isn't in the issue's acceptance criteria, so I didn't block on it.
