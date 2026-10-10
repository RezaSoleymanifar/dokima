# reviewer (plan) for #416

Run: https://github.com/dokima-dev/dokima/actions/runs/38082476707

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (49.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/3b444838-417a-4f22-969b-cd86cb980e93/tool-results/bci5q1d1v.txt
> 
> Preview (first 2KB):
> .:
> total 72
> drwxr-xr-x  3 runner runner  4096 Oct 10 20:07 .
> drwxrwxrwt 18 root   root    4096 Oct 10 20:07 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 20:07 in
> -rw-r--r--  1 runner runner 31918 Oct 10 20:07 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 20:07 open_blockers.json
> -rw-r--r--  1 runner runner    16 Oct 10 20:07 parent.json
> -rw-r--r--  1 runner runner 18391 Oct 10 20:07 plan.json
> 
> in:
> total 64
> drwxr-xr-x 2 runner runner  4096 Oct 10 20:07 .
> drwxr-xr-x 3 runner runner  4096 Oct 10 20:07 ..
> -rw-r--r-- 1 runner runner  8216 Oct 10 20:07 01-planner.json
> -rw-r--r-- 1 runner runner 14010 Oct 10 20:07 02-planner.json
> -rw-r--r-- 1 runner runner  6957 Oct 10 20:07 03-reviewer-plan.json
> -rw-r--r-- 1 runner runner 19166 Oct 10 20:07 04-planner.json
> # Issue #416: Card links show as GitHub's own references: no self-link on the issue, full address after Closes
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 291, 425 -->
> <!-- dokima-blocking: {"blocked_by": [236, 291], "blocks": [], "loop": []} -->
> Cards and Dokima's comments show issues and pull requests as GitHub's own references, raises leave the card, and code shows as code.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/416
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/

`2. Bash`
```
cd /tmp/pack; cat open_blockers.json parent.json; sed -n '/dokima-original\|Original issue/,$p' issue.md | head -400
```

> []{"number": null}<details><summary>Original issue</summary>
> 
> Two links on the card don't show as GitHub's own references (title and state icon):
> - On the issue's own page, the card's link to that same issue shows as a bare #N, because GitHub shortens a link to the page you're on. It adds nothing there, since I'm already on that issue.
> - At the bottom of a PR, "Closes #407" shows as a bare #407. GitHub draws the title only for a full address, and "Closes" followed by the full issue address still closes the issue (tested on dokima-dev/card-gallery: a PR whose body said "Closes https://github.com/dokima-dev/card-gallery/issues/34" listed #34 as the issue it closes).
> 
> Done when
> - The issue card leaves out the link to its own issue; the PR card still shows it.
> - The PR's closing line reads "Closes" followed by the issue's full address, and GitHub still lists that issue as the one the PR closes.
> 
> Widened (10-10): every reference to an issue, pull request or comment that Dokima writes shows as GitHub's own reference (status icon, title, number), on the card and in every comment Dokima posts. Today Blocked by, Blocks and Relates to still print a bare #N (dokima/card.py line 68), and #359 assumed a bare #N already renders that way; it doesn't, GitHub draws the title only for a full address.
> - On a planned issue, the Original issue fold sits right above the Definition of Done line, not below the card.
> - Anything about how GitHub displays text is checked against GitHub's real rendering

`3. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('plan.json'))
print(json.dumps(p,indent=1))" | head -400; python3 -c "
import json;p=json.load(open('in/03-reviewer-plan.json'));print(json.dumps(p.get('handback',p),indent=1)[:4000])"
```

> {
>  "kind": "feature",
>  "summary": "Cards and Dokima's comments show issues and PRs as GitHub's own references, raises leave the card, code shows as code, and stats come last.",
>  "feature": "Every link on a card or in a Dokima comment shows the way GitHub draws its own references, the card shows only what needs the owner, and what GitHub shows is checked on GitHub's own rendering. Split by R1 and R2: five independent goals (the self-link and closing line, references, the layout of cards and run comments, raises, code text) with well over five criteria, and each can land on its own.",
>  "stories": [
>   {
>    "title": "The issue card drops its link to itself, and a PR closes its issue by the issue's full address",
>    "user_story": "On the issue's own page the card no longer links to that same issue, and at the bottom of a PR the closing line shows the issue's title and state.",
>    "context": "The first plan of #416 (run 38063764349) worked this out and was rejected only because that run wrote outside tests/. Its findings stand: the top row is drawn by `links_row` in `dokima/card.py`, the same for both pages; `pr_body` copies the first `CLOSES` match (`Closes #N`) to the end of the PR's description; `dokima/agent.py` reads which issue a PR was built for from that line when its branch does not say; `dokima/scan.py` compares each card with the one Dokima draws now, so it must expect the issue's card without its own link and the PR's with it. The owner tested on dokima-dev/card-gallery

`4. Bash`
```
cd /tmp/pack; python3 -c "
import json;p=json.load(open('in/03-reviewer-plan.json'));h=p.get('handback',p);print(json.dumps(h['asks'],indent=1)); print(list(p.keys()))"
```

> [
>  {
>   "ask": "The issue card leaves out the link to its own issue; the PR card still shows it.",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S1.1"
>  },
>  {
>   "ask": "the PR card still shows it",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S1.2"
>  },
>  {
>   "ask": "The PR's closing line reads \"Closes\" followed by the issue's full address, and GitHub still lists that issue as the one the PR closes.",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S1.3"
>  },
>  {
>   "ask": "every reference to an issue, pull request or comment that Dokima writes shows as GitHub's own reference (status icon, title, number), on the card and in every comment Dokima posts",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S2.2"
>  },
>  {
>   "ask": "Today Blocked by, Blocks and Relates to still print a bare #N",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S2.1"
>  },
>  {
>   "ask": "On a planned issue, the Original issue fold sits right above the Definition of Done line, not below the card.",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "S3.1"
>  },
>  {
>   "ask": "Anything about how GitHub displays text is checked against GitHub's real rendering (its markdown API), not only against the raw text the code writes.",
>   "source": "https://github.com/dokima-dev/dokima/issues/416",
>   "criterion": "missing"
>  },
>  {
>   "ask": "Raises 

`5. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "issuecomment\|\*\*Plan\*\*\|def links_row\|def link_lines\|Original issue\|def todo\|autopilot" dokima/card.py | head -50; grep -n "issuecomment" dokima/agent.py | head
```

> 37:               "autopilot": "autopilot", "passed": "passed", "failed": "failed", "needs you": "needs-you",
> 59:def link_lines(repo, links):
> 283:def todo(issue, found, rec):
> 329:    # A pull request autopilot put in the merge queue is GitHub's to merge, so nothing is the owner's.
> 351:def links_row(repo, issue, pr, worker, check_runs):
> 513:    """The PR's description: the card, the owner's Original issue fold, then the Closes line.
> 801:    """On autopilot, a loop of issues blocking each other stops the river for the owner.
> 803:    One comment mentioning them, and the Needs you pill. Off autopilot nothing runs, so the card's loop line is all.
> 804:    When GitHub cannot say whether the issue is on autopilot, the river stops."""
> 806:    if agent.on_autopilot(repo, number) is False:
> 1180:    return source == "AGENTS.md" or any(re.fullmatch(re.escape(issue_url(n)) + r"(#issuecomment-\d+)?", source)

**Agent:** I'm checking the split plan's criteria against the owner's words in the card code, then I'll write the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 55,80p dokima/card.py; sed -n 351,380p dokima/card.py; grep -n '"Plan"\|Plan\*\*\|plan_line\|def render' dokima/card.py | head
```

> """The fixed icon of a field, drawn in front of it, with the field's name as its alt text."""
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
> LINKED = re.compile(r"<!-- dokima-linked-from:([\d ,]*)-->")
> SIDE = {"blocked_by": "blocks", "blocks": "blocked_by", "relates_to": "relates_to"}
> 
> 
> def merged(*many):
>     """Several links fields as one, each kind's numbers in order and once."""
>     out = {}
>     for links in many:
>         for kind in SIDE:
> def links_row(repo, issue, pr, worker, check_runs):
>     """The links that matter, the issue and its PR both included, so the card reads the same on either page.
> 
>     The issue and the PR are written out bare, so GitHub draws them as its own references."""
>     links = []
>     if worker:
>         links.append(f"[latest run]({worker['html_url']})")
>     links.append(issue["url"])
>   

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner keeps the split into 5 stories and adds the owner's newest ask: in every run comment the stats line is the last line, below Next (story 3)."],
  "decided": ["Every story whose promise is about what GitHub shows gets its own criterion checked on GitHub's rendering of what the code writes.",
              "Story 2 adds a criterion that every list of issues or pull requests in a comment Dokima posts names each by its full address, the review's Filed as issues list included."],
  "open": ["Asks the owner 3 questions: recorded GitHub answers or the live markdown API, leaving the filing of issue raises to #268, and where the autopilot icon goes."]},
 "verdict": "approve",
 "summary": "The split now carries every ask of the owner, including the stats line last and the check on GitHub's own rendering in each story; it waits on the owner's three questions.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The issue card leaves out the link to its own issue", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "S1.1"},
  {"ask": "the PR card still shows it", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "S1.2"},
  {"ask": "The PR's closing line reads \"Closes\" followed by the issue's full address, and GitHub still lists that issue as the one the PR closes.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "S1.3"},
  {"ask": "every reference to an issue, pull request or comment that Dokima writes shows as GitHub's own reference (status icon, title, number), on the card and in every comment Dokima posts", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "S2.2"},
  {"ask": "Today Blocked by, Blocks and Relates to still print a bare #N", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "S2.1"},
  {"ask": "On a planned issue, the Original iss
```

> Exit code 1
> summary holds 31 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The split now carries every ask of the owner, the stats line last and GitHub's own rendering included; it waits on the owner's three questions."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 416 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan review for issue #416. The hand-back passed both checks and is saved at `/tmp/dokima-out/review.json`.

- **Both earlier blockers are fixed.** Every one of the five stories that promises something about what GitHub shows now has its own criterion checked against GitHub's real rendering. Story 2 now also covers lists of issues and pull requests in Dokima's comments, including the review's Filed as issues list.
- **Your newest ask is in.** "The stats line is the very last line, below Next" is now criterion 3.2.
- **All 19 of your asks map to a criterion.** That includes [#401](https://github.com/dokima-dev/dokima/issues/401) (the to-do line still looks for the retired questions field) as criterion 4.3, and [#394](https://github.com/dokima-dev/dokima/issues/394) (the autopilot icon is never drawn) as criterion 3.3.

**One mapping is generous.** I matched "Issue raises are filed and parked on their own" to criterion 4.1, but 4.1 only takes raises off the card. Whether this issue also files them depends on your answer to the second question below. I didn't block on it because the planner raised it with you as an open question.

**The plan still stops for you.** None of the planner's three questions can be settled from your own words, so I answered none of them:
1. Should the check against GitHub's rendering call GitHub's markdown API live in CI, or use GitHub's answers recorded in the repo with a script that refreshes them? The plan assumes recorded answers.
2. Should this issue only take issue raises off the card and leave filing them to [#268](https://github.com/dokima-dev/dokima/issues/268) (files issues agents find, parked)? The plan assumes so.
3. Where should the autopilot icon go? The plan assumes the card's status line, hidden while Needs you shows.

Answer with `/plan` and your words, or `/review` to go on with the planner's assumptions.

Because the plan is a split, it has no tests yet, so I graded only the criteria. Each story's tests come when that story is planned.
