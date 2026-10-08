# reviewer (plan) for #229

Run: https://github.com/dokima-dev/dokima/actions/runs/37824982682

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (51.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b0a707aa-5b48-4a8d-be6c-75dcf234aa47/tool-results/b99uienwu.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct  8 18:31 .
> drwxrwxrwt 18 root   root    4096 Oct  8 18:32 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 18:31 in
> -rw-r--r--  1 runner runner 42108 Oct  8 18:31 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 18:31 open_blockers.json
> -rw-r--r--  1 runner runner 10326 Oct  8 18:31 plan.json
> 
> in:
> total 40
> drwxr-xr-x 2 runner runner  4096 Oct  8 18:31 .
> drwxr-xr-x 3 runner runner  4096 Oct  8 18:31 ..
> -rw-r--r-- 1 runner runner  9722 Oct  8 18:31 01-planner.json
> -rw-r--r-- 1 runner runner  6594 Oct  8 18:31 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 11032 Oct  8 18:31 03-planner.json
> # Issue #229: Every card reads like plain English, and the checker catches long text before the reviewer does
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" alig

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-3000
```

> # Issue #229: Every card reads like plain English, and the checker catches long text before the reviewer does
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> <details><summary>Original issue</summary>
> 
> Cards are too verbose. Worker and reviewer summaries read like changelogs full of file names and flags, and acceptance criteria run 80+ words (see #212). I want every card to read like what I asked for, in plain English, and still say the same thing.
> 
> What I want:
> - Every agent's role file says how I like to read cards: short, plain words, reads like my ask, no file, function or flag names in card text. Technical detail goes in docstrings. Planner, worker and reviewer each get it in their own role file, not a shared rule.
> - Every card opens with one plain sentence. The worker's summary today is "two sentences, cause and change" with no voice rule; fix that. The reviewer's summary says what was approved in my terms

`3. Bash`
```
cd /tmp/pack; grep -n "^### " issue.md; awk '/^### /{n++} n>=6' issue.md | grep -v '^ *"' | cut -c1-2500 | head -150
```

> 33:### RezaSoleymanifar on issue #229 (2026-10-08T18:05:32Z)
> 37:### dokima-runtime on issue #229 (2026-10-08T18:05:57Z)
> 42:### RezaSoleymanifar on issue #229 (2026-10-08T18:13:40Z)
> 46:### dokima-runtime on issue #229 (2026-10-08T18:14:03Z)
> 243:### dokima-runtime on issue #229 (2026-10-08T18:16:58Z)
> 472:### RezaSoleymanifar on issue #229 (2026-10-08T18:29:37Z)
> 476:### dokima-runtime on issue #229 (2026-10-08T18:29:57Z)
> 690:### dokima-runtime on issue #229 (2026-10-08T18:31:42Z)
> ### RezaSoleymanifar on issue #229 (2026-10-08T18:29:37Z)
> 
> /plan Answers: Caps are 25 words for criteria and summaries, and 15 words for a docstring's first line. Reject a hand-back only if it is still more than 20% over after the agent's own fix. A doubt about the ask goes in as a question, same as today. Your other assumptions are right.
> 
> ### dokima-runtime on issue #229 (2026-10-08T18:29:57Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> The planner proposes a split into 5 stories.
> 
> **Feature:** Cards read like plain English within the owner's caps, each agent is told how in its own role file, and the reviewer blocks on verbose text.
> 
> 1. The planner's criteria and docstrings stay short, and a little over the cap never fails a run
> 2. Every card opens with one short plain sentence, and the worker's docstrings are checked too
> 3. The planner hands back no concerns or replies, keeps

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"; grep -o 'issuecomment-[0-9]*' -r . | sort -u
```

> {
>  "kind": "feature",
>  "summary": "Every card should read like the owner's own ask in plain English, and the checker should catch long text before the reviewer does.",
>  "feature": "Cards read like plain English within the owner's caps, each agent is told how in its own role file, and the reviewer blocks on verbose text.",
>  "stories": [
>   {
>    "title": "The planner's criteria and docstrings stay short, and a little over the cap never fails a run",
>    "user_story": "The owner reads one short sentence per criterion, and a plan a few words over the cap is never rejected for it.",
>    "context": "Split rule R2 (more than five criteria) and R3 (checker code, card code and three role files). The owner set the caps: 25 words for a criterion's first sentence and for summaries, 15 words for a docstring's first line; a hand-back is rejected only when a text is still more than 20% over its cap (over 30 words for a 25-word cap, over 18 for a 15-word cap). Today dokima/planner.py checks shape only: from_kind() and check_stories() accept a criterion of any length, and unsummarized() only checks that a new test's docstring opens with one sentence, never its length. The same check runs inside the agent's run (agent.yml tells the agent to run it and fix what it reports) and again at the gate, which rejects on a non-zero exit, so the check can list every text over its cap but exit non-zero only past 20%. Build the length rule as one small shared helper (cap, 20% tolerance, message) that story 2 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3; git diff main --stat; cat /tmp/pack/open_blockers.json; python3 -c "
import json
for f in ['01-planner','02-reviewer-plan','03-planner']:
  d=json.load(open('/tmp/pack/in/'+f+'.json')); print(f, d.get('check'), list(d.keys()))"
```

> 27453f2 Every run comment is a short card with the long parts in folds (#228)
> c999661 Autopilot: a pull request the reviewer approved merges by itself (#227)
> 00846f5 Autopilot: the owner sees on the board and on every card what is on autopilot (#226)
> []01-planner {'passed': True, 'problems': []} ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> 02-reviewer-plan {'passed': True, 'problems': []} ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> 03-planner {'passed': True, 'problems': []} ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']

**Agent:** I'm reviewing the planner's 5-story split against the owner's asks and answers; next I'm checking a couple of code facts.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "Before you finish\|run this check\|def main\|sys.exit\|def problems_work\|def problems_shape\|def check_split\|five\|> 5\|len(stories)" dokima/agent.py dokima/planner.py .github/workflows/*.yml | head -40
```

> .github/workflows/agent.yml:230:          Hand back into $OUT. Before you finish, run this check on your hand-back and fix everything it reports:
> .github/workflows/agent.yml:415:          python3 -c "import json,sys; r=json.load(open('$OUT/record.json')); m=r.get('models') or []; bad=[x for x in m if x!='$MODEL']; sys.exit(print('models:', m) or (1 if bad or not m else 0))"
> dokima/planner.py:108:    last = len(stories) - 1
> dokima/planner.py:127:    for i in range(len(stories)):
> dokima/planner.py:144:        if not isinstance(stories, list) or not 2 <= len(stories) <= 5:
> dokima/planner.py:324:def main_with_tests(base, into):
> dokima/planner.py:412:def main(argv):
> dokima/planner.py:464:    sys.exit(main(sys.argv))
> dokima/agent.py:610:    elif sum(len(prev.get(k) or []) for k in ("did", "decided", "open")) > 5:
> dokima/agent.py:611:        bad.append("previous_step holds at most five lines")
> dokima/agent.py:710:def problems_work(w):
> dokima/agent.py:752:def problems_shape(kind, h):
> dokima/agent.py:1401:def main(argv):
> dokima/agent.py:1460:        print(queue(argv[2], argv[3], argv[4], argv[5] if len(argv) > 5 else "queued"))
> dokima/agent.py:1619:        sys.exit(main(sys.argv))
> dokima/agent.py:1623:        sys.exit(1)

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 215,245p .github/workflows/agent.yml; sed -n 100,160p dokima/planner.py
```

> worker)       GRADE=result-grade; FILE=work.json;   CHECK="python3 -m dokima.agent check work $OUT/work.json $PACK/plan.json $N" ;;
>           esac
>           CHECK="$CHECK && python3 -m dokima.agent check-round $ROLE $OUT/$FILE $PACK"
>           echo "CHECK=$CHECK" >> "$GITHUB_ENV"
>           claude -p "$(cat /tmp/runtime/dokima/roles/$GRADE.md /tmp/runtime/dokima/roles/$ROLE.md)
> 
>           # Your pack
>           - $PACK/issue.md: issue #$N as it stands, with every comment (the owner's words and answers are here).
>           - $PACK/in/: every earlier record of this issue, oldest first (NN-role.json). Each holds that run's hand-back,
>             the code check's verdict and the run it came from. Answer open blockers by id from the newest review.
>           - $PACK/plan.json: the newest plan that passed its check (absent until the planner has one).
>           - $PACK/open_blockers.json: the open blockers from the newest review at your stage. Answer every one by id.$( [ "$STAGE" = pr ] && echo "
>           - $PACK/diff.patch: the work against main. $PACK/tests.txt and tests.xml: all tests, run by code on this machine.
>           - $PACK/worker-run/: the worker's session log." )
>           You are on branch try/issue-$N. Your stage is: ${STAGE:-$ROLE}.
>           Hand back into $OUT. Before you finish, run this check on your hand-back and fix everything it reports:
>             $CHECK" \
>             --model "$MODEL" --dangerously-skip-permissions --max-turns 60 --output-format json > "$OUT/

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n '\$CHECK\|env.CHECK\|dokima.agent check\|dokima.planner' .github/workflows/agent.yml | head
```

> 181:          python3 -m dokima.agent check-pack "$ROLE" "$STAGE" "$PACK" > /tmp/pack-check.txt \
> 212:            planner)      GRADE=plan-grade;   FILE=plan.json;   CHECK="python3 -m dokima.planner check $N $OUT" ;;
> 213:            reviewerplan) GRADE=plan-grade;   FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json $PACK/plan.json $N" ;;
> 214:            reviewerpr)   GRADE=result-grade; FILE=review.json; CHECK="python3 -m dokima.agent check review $OUT/review.json $PACK/plan.json $N" ;;
> 215:            worker)       GRADE=result-grade; FILE=work.json;   CHECK="python3 -m dokima.agent check work $OUT/work.json $PACK/plan.json $N" ;;
> 217:          CHECK="$CHECK && python3 -m dokima.agent check-round $ROLE $OUT/$FILE $PACK"
> 218:          echo "CHECK=$CHECK" >> "$GITHUB_ENV"
> 231:            $CHECK" \
> 256:          set +e; bash -c "$CHECK" > "$OUT/check.txt" 2>&1; rc=$?; set -e

`9. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner re-split the issue into five stories with the owner's caps: planner length checks, one-sentence summaries for every card, no concerns or replies, reading rules in each role file, and the reviewer blocking on verbose text."],
  "decided": ["Criteria and summaries are capped at 25 words and a docstring's first line at 15; a hand-back is rejected only when a text is more than 20% over.",
              "A doubt about the ask goes in as a question, and the worker keeps its replies to blockers."],
  "open": []},
 "verdict": "approve",
 "summary": "The five stories keep every ask and the owner's answers, with the caps the owner set.",
 "blockers": [],
 "notes": [
  {"text": "The owner asked that the check give each agent its problems, length and everything else it checks; today the planner's check stops at its first problem, so story 1's plan should say whether it lists every problem at once or only every text over its cap.",
   "evidence": "dokima/planner.py from_kind() raises Garbled on the first problem (lines 143-160); plan.json S1.4 lists only texts over their caps"},
  {"text": "A few criteria still join two behaviors, which the owner asks a criterion not to do; each story's own plan should give each its own criterion.",
   "evidence": "plan.json S1.4 (passes and lists), S2.5 (lists and rejects), S4.1 (plain words and detail in docstrings), S4.5 (questions and no concerns or replies)"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Every agent's role file says how I like to read cards: short, plain words, reads like my ask, no file, function or flag names in card text.", "source": "https://github.com/dokima-dev/dokima/issues/229", "criterion": "S4.1"},
  {"ask": "no file, function or flag names in card text", "source": "https://github.com/dokima-dev/dokima/issues/229", "criterion": "S4.2"},
  {"ask": "Technical detail goes in docstrings. Pla
```

> rc=0

**Agent:** I approved the plan for issue #229, and the hand-back passes both checks. It's in `/tmp/dokima-out/review.json`.

- **What the planner did:** it re-split the issue into five stories using your answers:
  1. the planner's own text stays short;
  2. every card opens with one short sentence, and the worker's docstrings are checked too;
  3. the planner hands back no concerns or replies;
  4. each role file states the reading rules;
  5. the reviewer blocks on verbose or jargon text.
- **Your answers are all in the plan:** the 25-word and 15-word caps, rejecting only when a text is more than 20% over, a doubt going in as a question, criteria named by number, and the worker keeping its replies.
- **Asks:** every one of your asks in the issue and your follow-up comment maps to a story criterion; none is missing. The plan has no questions, and no earlier blockers were open.
- **Tests:** a split carries no tests yet; each story writes its own when it is planned.

Two notes for the stories' own plans, neither one blocking:
- **Listing every problem:** you asked the check to give each agent "length and everything else it checks." Today the planner's check stops at the first problem it finds (`dokima/planner.py`, `from_kind()`), and story 1 only promises to list every text over its cap. Story 1's plan should say whether the check lists every problem at once.
- **Criteria that join two behaviors:** a few criteria still do (S1.4, S2.5, S4.1, S4.5), which you asked a criterion not to do. Each story's plan should split them.

I couldn't find a link to your follow-up comment in the pack, so those three asks point to the issue itself; the check accepted that.
