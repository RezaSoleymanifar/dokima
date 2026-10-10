# reviewer (plan) for #416

Run: https://github.com/dokima-dev/dokima/actions/runs/38082041223

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> <persisted-output>
> Output too large (29.6KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5a717441-7e68-4bad-8604-339b3251a3db/tool-results/bklhozf2h.txt
> 
> Preview (first 2KB):
> # Issue #416: Card links show as GitHub's own references: no self-link on the issue, full address after Closes
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 291, 425 -->
> <!-- dokima-blocking: {"blocked_by": [236], "blocks": [], "loop": []} -->
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Fix the rejected hand-back
> 
> https://github.com/dokima-dev/dokima/issues/416
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocked-by.svg" width="16" height="16" align="absmiddle" alt="blocked by"> **Blocked by:** #236
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Two links on the card don't show as GitHub's own references (title and state icon):
> - On the issue's own page, the card's link to that same issue shows as a bare #N, because GitHub shortens a link to the page you're on. It adds nothing there, since I'm already on that issue.
> - At the bottom of a PR, "Closes #407" shows as a bare #407. GitHub draws the title only for a full address, and "Closes" followed by the full issue address still closes the issue (tested on dokima-dev/card-gallery: a PR whose body said "Closes https://github.com/dokima-dev/card-gallery/is

`2. Bash`
```
cat /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5a717441-7e68-4bad-8604-339b3251a3db/tool-results/bklhozf2h.txt | tail -c +2000
```

> ue fold sits right above the Definition of Done line, not below the card.
> - Anything about how GitHub displays text is checked against GitHub's real rendering (its markdown API), not only against the raw text the code writes.
> 
> - Raises come off the card. They stay in the comment where they were raised; the card's status line only says what needs me (for example "Needs you: answer 2 questions") and links to that comment. Issue raises are filed and parked on their own.
> - Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for several lines), and Dokima never escapes text inside code, so `<`, `>` and `&` show as written.
> 
> - The rule: inside prose (a sentence, a question, a record's text) issues and PRs are written short, as #N, so the text stays readable. Everywhere outside prose (the card's fields and lists: the top row, Blocked by, Blocks, Relates to, Stories, Out of scope, the PR's closing line) they show as GitHub's own reference. An acceptance criterion's Source always shows as GitHub's own reference, never #N. Seen on #412's question for me.
> - The same raise is listed twice on a card (#388's card shows its workflow-files question twice).
> 
> - Run comments' rows (Details, What the previous step did, What it built, token counts) are #236's, not this issue's.
> 
> More to come; wait for my go before planning.
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/

`3. Bash`
```
head -c 5000 /home/runner/.claude/projects/-home-runner-work-dokima-dokima/5a717441-7e68-4bad-8604-339b3251a3db/tool-results/bklhozf2h.txt | tail -c 3200; echo; python3 -c "import json;d=json.load(open('/tmp/pack/in/02-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"
```

> still print a bare #N (dokima/card.py line 68), and #359 assumed a bare #N already renders that way; it doesn't, GitHub draws the title only for a full address.
> - On a planned issue, the Original issue fold sits right above the Definition of Done line, not below the card.
> - Anything about how GitHub displays text is checked against GitHub's real rendering (its markdown API), not only against the raw text the code writes.
> 
> - Raises come off the card. They stay in the comment where they were raised; the card's status line only says what needs me (for example "Needs you: answer 2 questions") and links to that comment. Issue raises are filed and parked on their own.
> - Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for several lines), and Dokima never escapes text inside code, so `<`, `>` and `&` show as written.
> 
> - The rule: inside prose (a sentence, a question, a record's text) issues and PRs are written short, as #N, so the text stays readable. Everywhere outside prose (the card's fields and lists: the top row, Blocked by, Blocks, Relates to, Stories, Out of scope, the PR's closing line) they show as GitHub's own reference. An acceptance criterion's Source always shows as GitHub's own reference, never #N. Seen on #412's question for me.
> - The same raise is listed twice on a card (#388's card shows its workflow-files question twice).
> 
> - Run comments' rows (Details, What the previous step did, What it built, token counts) are 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "autopilot" dokima/card.py | head -30; grep -n "questions\")" dokima/card.py; sed -n 55,80p dokima/card.py; grep -rn "394\|401" tests/*.py | head
```

> 37:               "autopilot": "autopilot", "passed": "passed", "failed": "failed", "needs you": "needs-you",
> 329:    # A pull request autopilot put in the merge queue is GitHub's to merge, so nothing is the owner's.
> 801:    """On autopilot, a loop of issues blocking each other stops the river for the owner.
> 803:    One comment mentioning them, and the Needs you pill. Off autopilot nothing runs, so the card's loop line is all.
> 804:    When GitHub cannot say whether the issue is on autopilot, the river stops."""
> 806:    if agent.on_autopilot(repo, number) is False:
> 291:    if role == "planner" and h.get("questions"):
>     """The fixed icon of a field, drawn in front of it, with the field's name as its alt text."""
>     return icon(repo, FIELD_ICONS[field], alt=field)
> 
> 
> def link_lines(repo, links):
>     """One line per kind of link a plan has (Blocked by, Blocks, Relates to), each with its own icon; none for a kind
>     with no links or a plan with no links field."""
>     links = links if isinstance(links, dict) else {}
>     out = []
>     for kind, field, label in (("blocked_by", "blocked by", "Blocked by"), ("blocks", "blocks", "Blocks"),
>                                ("relates_to", "related", "Relates to")):
>         numbers = links.get(kind) if isinstance(links.get(kind), list) else []
>         if numbers:
>             out.append(f"{field_icon(repo, field)} **{label}:** " + ", ".join(f"#{n}" for n in numbers))
>     return out
> 
> 
> LINKED = re.compile(r"<!-- dokima-linked-from:([\d ,]*)--

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn '"#{\|f"#{\|#{n}\|#{num' dokima/*.py | grep -v "^dokima/card.py" | head -30
```

> dokima/board.py:238:        raise RuntimeError(f"Could not read the state of #{n} ({reason(e)}), so its cards were left as they were.") from e
> dokima/board.py:354:        failed.append(f"#{n}: {(e.stderr or str(e)).strip()}")
> dokima/audit.py:285:    print(f"Setup issue: #{n}" if n else "Nothing is off.")
> dokima/checks.py:63:        return no_plan(f"No approved plan found for issue #{number}")
> dokima/checks.py:71:    return rows or no_plan(f"No approved plan found for issue #{number}")
> dokima/checks.py:87:        print(f"Could not list the changed files of PR #{number}, so no text-only shortcut: "
> dokima/plan.py:193:    out = [f"Issue #{number}: {title}", ""]
> dokima/scan.py:22:    return f"issue #{n}" if kind == "issue" else f"PR #{n}"
> dokima/uptodate.py:211:        print(f"uptodate: updated #{n}")
> dokima/uptodate.py:213:        print(f"::warning::uptodate: #{n} could not be updated")
> dokima/uptodate.py:215:        print(f"::error::uptodate: the update comment on #{n} could not be listed or changed: {why}")
> dokima/agent.py:50:    items = [{**c, "where": f"issue #{number}"} for c in d["comments"]]
> dokima/agent.py:284:                bad.append(f"links.{k} links #{n}, the issue itself")
> dokima/agent.py:286:                bad.append(f"links.{k} links #{n}, which is not an open issue")
> dokima/agent.py:290:    bad += [f"#{n} sits in more than one list of links: {', '.join(ks)}" for n, ks in seen.items() if len(ks) > 1]
> dokima/agent.py:1072:        print(f"No parent issue of #{numb

**Agent:** Plan review for #416 is in progress: I'm checking the split's criteria against each of the owner's asks. Next I'll look at how lists of issues in Dokima's comments are written.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1512,1566p dokima/agent.py
```

> continue
>             seen.add(path[-1])
>             stack += [path + [c] for c in sorted(blockers(path[-1]))]
>     return []
> 
> 
> def named(numbers):
>     """Issue numbers as words: #1, #2 and #3."""
>     ns = [f"#{n}" for n in numbers]
>     return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]
> 
> 
> def gh_reason(e):
>     """GitHub's own words for a call that failed, on one line."""
>     return " ".join((e.stderr or str(e)).split())
> 
> 
> def first_sentence(text):
>     """A raise's first sentence, on one line, as a filed issue's title."""
>     text = escape_line(text)
>     m = re.match(r"(.+?[.!?])(\s|$)", text)
>     return (m.group(1) if m else text)[:250]
> 
> 
> def file_issues(repo, number, rec, recs):
>     """File every issue raise a passed review confirms as its own GitHub issue.
> 
>     It confirms its own, and each the planner or the worker raised that it answers done; `recs` are the records
>     before it. Returns the record's lines naming each filed issue, or the finding and GitHub's reason when GitHub
>     refuses it; a refusal never stops the run."""
>     h = rec.get("handback") or {}
>     if rec.get("role") != "reviewer" or not (rec.get("check") or {}).get("passed"):
>         return []
>     found = [x for x in card.raises_of(h) if x.get("kind") == "issue"]
>     theirs = {x["id"]: x for x in open_raises(recs) if x.get("kind") == "issue" and raises.sent_to(x) == raises.CONFIRMS}
>     found += [theirs[a["raise"]] for a in card.answers_of(h)
>               if a.get("answer") == "done" an

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner proposes splitting the issue into 5 stories: the self-link and the closing line, references outside prose, the fold's place and the autopilot icon, raises off the card, and code shown as code."],
  "decided": ["Leaves filing issue raises to #268 and draws the autopilot icon on the card's status line, hidden while Needs you shows.", "Checks GitHub's rendering against its answers recorded once in the repo, only for a card's references."],
  "open": ["Asks the owner 3 questions: recorded answers or live markdown API, leaving filing to #268, and where the autopilot icon goes."]},
 "verdict": "block",
 "summary": "The split covers most of the owner's asks, but it narrows two of them: GitHub's real rendering is checked only for a card's references, and in Dokima's comments only Sources become GitHub's own references.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Ask narrowed",
   "text": "The owner asked that anything about how GitHub displays text is checked against GitHub's real rendering. The plan keeps this only as a non-functional note on story 2, limited to a card's references, and no criterion carries it. Stories 1 (the closing line shows the issue's title), 3 (the fold sits right above the Definition of Done) and 5 (`<`, `>` and `&` inside code show as written) are also about what GitHub displays, so they could pass on the raw text alone, the way #359 did. Smallest fix: make it an acceptance criterion in each story whose promise is about what GitHub shows, checked against GitHub's rendering of what the code writes.",
   "evidence": "Issue #416 text: \"Anything about how GitHub displays text is checked against GitHub's real rendering (its markdown API), not only against the raw text the code writes.\" plan.json: the only place this appears is stories[1].non_functional[0], \"How GitHub displays a card's references is checked...\"; stories 
```

> Exit code 1
> summary holds 34 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The split narrows two asks: GitHub's real rendering is checked only for card references, and comments get full addresses only in Sources."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 416 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I blocked the plan for [#416](https://github.com/dokima-dev/dokima/issues/416) (card links show as GitHub's own references) and sent it back to the planner. `review.json` passes both checks.

The planner splits the issue into 5 stories: the self-link and the closing line, references outside prose, where the fold sits and the autopilot icon, raises off the card, and code shown as code. Every ask in your issue text and comments has a criterion except one, the check against GitHub's real rendering.

**Two blockers for the planner, both asks the plan made narrower:**
1. **Checking against GitHub's real rendering.** You asked that anything about how GitHub displays text be checked against GitHub's real rendering. The plan keeps this only as a side note on story 2, and only for a card's references. Three stories that are also about what GitHub shows have no such check, so they could pass on the raw text alone, the way [#359](https://github.com/dokima-dev/dokima/issues/359) (assumed a bare #N shows the title) did:
   - story 1: the closing line shows the issue's title;
   - story 3: the fold sits right above the Definition of Done;
   - story 5: `<`, `>` and `&` inside code show as written.
2. **"In every comment Dokima posts."** In comments, story 2 only turns criterion Sources into full addresses. Lists in comments still print a bare #N, for example the "Filed as issues" list at `dokima/agent.py:1562`, and no criterion would catch it.

**Still waiting for you.** I left the planner's 3 questions unanswered: your words in the issue don't clearly settle any of them.
- **The rendering check:** your words name GitHub's markdown API itself. The plan uses GitHub's answers recorded once in the repo, because tests run with no network.
- **Filing issue raises:** the plan only takes them off the card and leaves filing to [#268](https://github.com/dokima-dev/dokima/issues/268) (files issues agents find, parked).
- **The autopilot icon ([#394](https://github.com/dokima-dev/dokima/issues/394), the icon is never drawn):** the plan draws it on the card's status line, hidden while Needs you shows.
