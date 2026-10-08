# reviewer (plan) for #234

Run: https://github.com/dokima-dev/dokima/actions/runs/37827334474

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json 2>/dev/null; cat plan.json
```

> <persisted-output>
> Output too large (34.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/663d3935-d68e-4196-a9de-f5351e85b568/tool-results/bt0v1k6s9.txt
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
> # Issue #234: Every field on a card has its own GitHub icon, fixed by code
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
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #230, story 1</summary>
> 
> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** Every field on the issue card, the PR card and the run comments carries its own GitHub Octicon, in the same style as today's status icons, chosen by code and never by an agent.
> 
> **Context:** Today dokima/icons/ holds six Octicon circles (passed, failed, running

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n '20,400p'
```

> **Part of:** #230 Cards show everything I need with icons, and nothing I don't
> 
> **User story:** Every field on the issue card, the PR card and the run comments carries its own GitHub Octicon, in the same style as today's status icons, chosen by code and never by an agent.
> 
> **Context:** Today dokima/icons/ holds six Octicon circles (passed, failed, running, queued, cancelled, none), served by card.icon() in dokima/card.py and used by agent.py through icon(). The issue names 23 fields. Add one SVG per field in the same 16px style and one fixed table in code from field to icon; the later stories draw with it. Rule R1/R2 split: this story is the shared base.
> 
> **Acceptance criteria:**
> - dokima/icons/ holds one Octicon SVG, 16 by 16 like today's status icons, for each of the 23 fields the owner named: planner, worker, plan review, code review, autopilot, passed, failed, needs you, owner approval, merged, still open, acceptance criterion, verified by, files changed, question, blocker, note, outside the plan, issue found, related, blocked by, blocks and stats. ([source](https://github.com/dokima-dev/dokima/issues/230))
> - One fixed table in code maps each of those 23 fields to its icon, and every card and run comment that shows one of those fields shows its icon in front of it. ([source](https://github.com/dokima-dev/dokima/issues/230))
> - An agent's hand-back cannot choose, change or drop an icon: the same field shows the same icon whatever the hand-back holds, including a hand-back t

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "import json;d=json.load(open('plan.json'));print(d.keys())"; cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; git log --oneline -15 --stat -- dokima/card.py | head -40; wc -l tests/test_field_icons.py; ls dokima/icons
```

> []dict_keys(['kind', 'summary', 'user_story', 'acceptance_criteria', 'non_functional', 'scope', 'out_of_scope', 'tests', 'test_changes'])
> commit 29c89fe7d6a095a2de91ff18663e43a234c20271
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 18:49:58 2026 +0000
> 
>     planner for #234 (run 37825194734)
> 
>  tests/test_agent.py        |   4 +-
>  tests/test_card.py         |   3 +-
>  tests/test_card_records.py |  11 +-
>  tests/test_field_icons.py  | 491 +++++++++++++++++++++++++++++++++++++++++++++
>  tests/test_fixer.py        |   5 +-
>  tests/test_questions.py    |   3 +-
>  6 files changed, 511 insertions(+), 6 deletions(-)
> 27453f2 Every run comment is a short card with the long parts in folds (#228)
>  dokima/card.py | 10 +++++++---
>  1 file changed, 7 insertions(+), 3 deletions(-)
> bc3a3e6 The card says what the issue is, where it stands, its children, and what the owner must do (#225)
>  dokima/card.py | 189 ++++++++++++++++++++++++++++++++++++++++++++++++++-------
>  1 file changed, 167 insertions(+), 22 deletions(-)
> a6c75c7 The issue and PR card shows the plan and its proof, drawn only from the records (#217)
>  dokima/card.py | 218 ++++++++++++++++++++++++++++++++++++++++-----------------
>  1 file changed, 152 insertions(+), 66 deletions(-)
> c7de9c0 The owner's ask is kept below a fixed marker and never rewritten (#200)
>  dokima/card.py | 13 +++++++------
>  1 file changed, 7 insertions(+), 6 deletions(-)
> d58749e Objective and Acceptance criteria on 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_field_icons.py
```

> <persisted-output>
> Output too large (31.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/663d3935-d68e-4196-a9de-f5351e85b568/tool-results/bb03fcz7d.txt
> 
> Preview (first 2KB):
> """Every field on a card has its own GitHub icon, fixed by code (issue #234, story 1 of #230).
> 
> The owner named 23 fields. Each gets one Octicon (GitHub's own icon set, MIT) in dokima/icons/, drawn in the same
> 16-by-16 style as today's status circles, and one fixed table in dokima/card.py maps each field to its icon:
> 
>     card.FIELD_ICONS    {field: file name in dokima/icons/ without ".svg"}; the file name is the field's words joined
>                         by "-" (so "plan review" -> "plan-review"), and passed and failed keep today's passed.svg and
>                         failed.svg
> 
> Each field is pinned below to the Octicon it uses (its 16px version, primer/octicons), by the SHA-256 of the icon's
> path data, so an icon that is not that Octicon fails. A field's icon is drawn exactly as today's icons are,
> `card.icon(repo, FIELD_ICONS[field], alt=field)`: an <img> served from the repo's own main branch, with the field's
> name as its alt text. "In front of" means the icon comes right before the field's words, with only a space, `**` or
> `<b>` between them.
> 
> Where each field is shown today and gets its icon:
>     issue and PR card (dokima/card.py render): Needs you and Merged on the status line, Merged on a child's row,
>         files changed in the links row, the Accepta

`5. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/663d3935-d68e-4196-a9de-f5351e85b568/tool-results/bb03fcz7d.txt
```

> 1	"""Every field on a card has its own GitHub icon, fixed by code (issue #234, story 1 of #230).
> 2	
> 3	The owner named 23 fields. Each gets one Octicon (GitHub's own icon set, MIT) in dokima/icons/, drawn in the same
> 4	16-by-16 style as today's status circles, and one fixed table in dokima/card.py maps each field to its icon:
> 5	
> 6	    card.FIELD_ICONS    {field: file name in dokima/icons/ without ".svg"}; the file name is the field's words joined
> 7	                        by "-" (so "plan review" -> "plan-review"), and passed and failed keep today's passed.svg and
> 8	                        failed.svg
> 9	
> 10	Each field is pinned below to the Octicon it uses (its 16px version, primer/octicons), by the SHA-256 of the icon's
> 11	path data, so an icon that is not that Octicon fails. A field's icon is drawn exactly as today's icons are,
> 12	`card.icon(repo, FIELD_ICONS[field], alt=field)`: an <img> served from the repo's own main branch, with the field's
> 13	name as its alt text. "In front of" means the icon comes right before the field's words, with only a space, `**` or
> 14	`<b>` between them.
> 15	
> 16	Where each field is shown today and gets its icon:
> 17	    issue and PR card (dokima/card.py render): Needs you and Merged on the status line, Merged on a child's row,
> 18	        files changed in the links row, the Acceptance criteria heading, Verified by under a criterion, and Code
> 19	        review and Owner approval in the Definition of Done (after their verdict circle)
> 20	    live run c

**Agent:** Reading the planner's tests now; next I'll run them and check the pinned icon hashes against today's files.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; head -c 600 dokima/icons/*.svg; echo; python3 - <<'E'
import hashlib,xml.etree.ElementTree as ET
S="{http://www.w3.org/2000/svg}"
for f in ["passed","failed"]:
    r=ET.parse(f"dokima/icons/{f}.svg").getroot()
    print(f,r.attrib,hashlib.sha256("\n".join(p.get("d") for p in r.iter() if p.tag==S+"path").encode()).hexdigest())
E
pytest -q tests/test_field_icons.py 2>&1 | tail -50
```

> ==> dokima/icons/cancelled.svg <==
> <svg fill="#8c959f" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0Zm3.28 5.78a.75.75 0 0 0-1.06-1.06l-5.5 5.5a.75.75 0 1 0 1.06 1.06Z"/></svg>
> ==> dokima/icons/failed.svg <==
> <svg fill="#cf222e" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M2.343 13.657A8 8 0 1 1 13.658 2.343 8 8 0 0 1 2.343 13.657ZM6.03 4.97a.751.751 0 0 0-1.042.018.751.751 0 0 0-.018 1.042L6.94 8 4.97 9.97a.749.749 0 0 0 .326 1.275.749.749 0 0 0 .734-.215L8 9.06l1.97 1.97a.749.749 0 0 0 1.275-.326.749.749 0 0 0-.215-.734L9.06 8l1.97-1.97a.749.749 0 0 0-.326-1.275.749.749 0 0 0-.734.215L8 6.94Z"/></svg>
> ==> dokima/icons/none.svg <==
> <svg fill="#8c959f" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13Z"/></svg>
> ==> dokima/icons/passed.svg <==
> <svg fill="#2da44e" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 1 8 0a8 8 0 0 1 0 16Zm3.78-9.72a.751.751 0 0 0-.018-1.042.751.751 0 0 0-1.042-.018L6.75 9.19 5.28 7.72a.751.751 0 0 0-1.042.018.751.751 0 0 0-.018 1.042l2 2a.75.75 0 0 0 1.06 0Z"/></svg>
> ==> dokima/icons/queued.svg <==
> <svg fill="#8c959f" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.

`7. Bash`
```
cd /tmp; timeout 20 curl -sL https://raw.githubusercontent.com/primer/octicons/main/icons/light-bulb-16.svg | head -c 400; echo; find / -path /proc -prune -o -name "light-bulb-16.svg" -print 2>/dev/null | head
```

> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-
> Shell cwd was reset to /home/runner/work/dokima/dokima

**Agent:** Network works; verifying every pinned hash against the real Octicons.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; mkdir -p /tmp/octi; python3 -I - <<'E'
import hashlib,re,subprocess,sys,ast,xml.etree.ElementTree as ET
src=open("tests/test_field_icons.py").read()
m=re.search(r"OCTICONS = (\{.*?\n\})",src,re.S); O=ast.literal_eval(m.group(1))
S="{http://www.w3.org/2000/svg}"
for f,(n,h) in O.items():
    p=f"/tmp/octi/{n}.svg"
    subprocess.run(["curl","-sfL","-o",p,f"https://raw.githubusercontent.com/primer/octicons/main/icons/{n}-16.svg"])
    try:
        r=ET.parse(p).getroot()
        got=hashlib.sha256("\n".join(x.get("d") for x in r.iter() if x.tag==S+"path").encode()).hexdigest()
        print(f, n, "OK" if got==h else "MISMATCH", [dict(x.attrib).keys() for x in r.iter() if x.tag==S+"path"] if got!=h else "")
    except Exception as e: print(f,n,"ERR",e)
E
```

> planner light-bulb OK 
> worker tools OK 
> plan review checklist OK 
> code review code-review OK 
> autopilot rocket OK 
> passed check-circle-fill OK 
> failed x-circle-fill OK 
> needs you bell OK 
> owner approval person OK 
> merged git-merge OK 
> still open issue-opened OK 
> acceptance criterion tasklist OK 
> verified by verified OK 
> files changed file-diff OK 
> question question OK 
> blocker blocked OK 
> note note OK 
> outside the plan alert OK 
> issue found bug OK 
> related link OK 
> blocked by issue-tracked-by OK 
> blocks issue-tracks OK 
> stats graph OK

`9. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_field_icons.py 2>&1 | grep -E "^FAILED" | sed 's/ - /\n   /' | grep -oE "(FAILED \S+|   .{0,140})" | paste - - | cut -c1-260; pytest -q --deselect tests/test_field_icons.py 2>&1 | tail -3; pytest -q 2>&1 | tail -2; git diff HEAD~1 -- tests/test_agent.py tests/test_card.py tests/test_fixer.py tests/test_questions.py tests/test_card_records.py
```

> Command did not complete within its 120s timeout and was moved to the background (ID: b3164bhp8). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/663d3935-d68e-4196-a9de-f5351e85b568/tasks/b3164bhp8.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`10. Bash`
```
cd /home/runner/work/dokima/dokima; pytest -q tests/test_field_icons.py 2>&1 | grep -E "^FAILED" | cut -c1-230; git diff HEAD~1 -- tests/test_agent.py tests/test_card.py tests/test_fixer.py tests/test_questions.py tests/test_card_records.py
```

> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[planner] - AssertionError: 234.1: dokima/icons/planner.svg, the planner icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[worker] - AssertionError: 234.1: dokima/icons/worker.svg, the worker icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[plan review] - AssertionError: 234.1: dokima/icons/plan-review.svg, the plan review icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[code review] - AssertionError: 234.1: dokima/icons/code-review.svg, the code review icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[autopilot] - AssertionError: 234.1: dokima/icons/autopilot.svg, the autopilot icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[needs you] - AssertionError: 234.1: dokima/icons/needs-you.svg, the needs you icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[owner approval] - AssertionError: 234.1: dokima/icons/owner-approval.svg, the owner approval icon, does not exist
> FAILED tests/test_field_icons.py::test_every_field_has_its_own_octicon_in_the_status_icon_style[merged] - AssertionError: 2

`11. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "import re\|def readable\|readable(" tests/test_questions.py | head; grep -niE "question|autopilot|blocked|blocks|related|still open|blocker|note|stats|merged|needs you|verified|planner|worker|review" dokima/card.py | grep -v "^\s*#" | cut -c1-170 | head -80
```

> 11:import re
> 77:def readable(rec):
> 101:    text = readable(rec([GOOD, SECOND]))
> 108:    text = readable(rec([dict(GOOD, options=["Numbers-zq", "Strings-zq"], recommendation="Pick-strings-zq")]))
> 10:from the agents' records and GitHub's checks and reviews, never from the issue's
> 25:TODO = {"questions": "Answer the questions with /plan, or say /review",
> 27:        "three blocks": "Three blocks in a row: your call",
> 33:STAGES = {"Backlog", "Plan", "Work", "Review", "Merged"}
> 102:    if role == "planner" and h.get("questions"):
> 103:        return TODO["questions"]
> 104:    verdict = h.get("verdict") if role == "reviewer" else None
> 108:        return TODO["three blocks"]
> 112:        planned = agent.latest(found["recs"], "planner")
> 119:    """(stage, to-do): the board's column and, exactly when the board shows Needs you, what the owner must do; None
> 123:    if pr and pr.get("merged"):
> 124:        return "Merged", None
> 139:    """The small status line under the summary: the stage, then Needs you and the owner's to-do when there is one."""
> 140:    return f"**{stage}**" + (f" · Needs you: {todo}" if todo else "")
> 150:def links_row(repo, issue, pr, worker, check_runs, page):
> 153:    if worker:
> 154:        links.append(f"[latest run]({worker['html_url']})")
> 166:    then its words and, when any of its tests has a docstring, Verified by with each one linking to its test."""
> 169:    proofs = [f'<a href="{t["url"]}">{escape(t["verified_by"])}</a>' for t in tests if t and t.get("verified_by")

`12. Bash`
```
cd /home/runner/work/dokima/dokima; grep -nE "Needs you|Merged|merged|Questions|Still open|Notes|Outside the plan|Issues found|blocked by|Blocked|Acceptance criteria|Verified|Code review|Owner approval|files changed|Stats|<sub>" dokima/agent.py | cut -c1-180 | head -50
```

> 162:    lines += ["**Acceptance criteria:**"]
> 246:        return "\n".join([LIVE, line, "", what] + ([] if state == "handoff" else ["", f"<sub>[run]({run})</sub>"])) + "\n"
> 259:    return "\n".join([LIVE, line, "", what, "", f"<sub>[run]({run})</sub>"]) + "\n"
> 346:                  ("What it found", bullets(h.get("outside_scope"), lambda o: f"Outside the plan: {o.get('file', '')}: {o.get('why', '')}")),
> 354:                  ("Notes", bullets(h.get("notes"), lambda n: f"{n.get('text', '')} ({n.get('evidence', '')})")),
> 355:                  ("Outside the plan", bullets(h.get("outside_plan"), lambda o: f"{o.get('file', '')}: {o.get('change', '')}")),
> 360:                                                     (("did", "Did"), ("decided", "Decided"), ("open", "Still open"))
> 409:        lines += record_fold(rec) + ["", f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
> 417:        lines += record_fold(rec) + ["", footnote(rec) if rec.get("agent_started") else f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
> 433:            lines += ["", "**Acceptance criteria:**", ""] + [f"{i}. {c}" for i, c in enumerate(criteria, 1)]
> 448:            lines += ["", "**Issues found outside this one** (proposals until you file them):"]
> 452:        lines += [""] + [f"{f['story']}. #{f['issue']} {f['title']}" + (f" (blocked by {', '.join('#' + str(num[d]) for d in f['blocked_by'])})" if f["blocked_by"] else "")
> 456:        lines += ["", "**Questions for you** (it planned on the reading i

`13. Bash`
```
cd /tmp/octi; grep -l "fill-rule\|clip-rule\|<g" *.svg; grep -c "<path" *.svg | grep -v ":1$"
```

> (Bash completed with no output)

**Agent:** Checks are done: all 23 pinned hashes match the real Octicons, and every new test fails for the right reason. Writing the review now.

`14. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner planned the issue as one story with three criteria and one non-functional requirement, and wrote tests/test_field_icons.py with a test for each.",
          "It pinned each of the 23 fields to one GitHub Octicon by its drawing, and listed every place a card or run comment shows a field today."],
  "decided": ["Passed and failed keep today's circles; the other 21 fields get new icons in today's colors, no two alike.",
              "The autopilot, related and blocks icons are added to the table but drawn by later stories of #230, since nothing shows them today; the one-line Autopilot comments stay plain words."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan keeps all four of the owner's asks, every test names its criterion, and every new test fails today because the icons and the table do not exist yet.",
 "blockers": [],
 "notes": [
  {"text": "The pinned icons are the real GitHub Octicons: each of the 23 drawings in the test matches the 16px icon published by primer/octicons, and passed and failed match today's circles.",
   "evidence": "Fetched icons/<name>-16.svg from primer/octicons for all 23 names and hashed their path data as the test does: 23 of 23 match; dokima/icons/passed.svg and failed.svg hash to the pinned values."},
  {"text": "The blocker icon is checked only on a code review's comment; a plan review draws its blockers with the same code, so a worker could still pass by drawing it only on one stage.",
   "evidence": "tests/test_field_icons.py::test_the_review_comment_shows_blocker_note_outside_and_issue_icons uses built(\"reviewer\", \"pr\", REVIEW) only."}],
 "outside_plan": [],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "dokima/icons/ holds one Octicon SVG, 16 by 16 like today's status icons, for each of the 23 fields the owner named", "source": "https://github.com/dokima-dev/dokima/issues/234", "criterion": "2
```

> rc=0

**Agent:** I approved the plan for #234. The review is in `/tmp/dokima-out/review.json`, and both hand-back checks ran with no problems reported.

**Why it's approved**
- **Every ask is covered.** The issue asks for four things, and each has its own criterion:
  - one Octicon per field → 234.1
  - one fixed table, with each field's icon in front of it everywhere → 234.2
  - an agent can't choose, change or drop an icon → 234.3
  - icons are served from main → 234.4
- **The icons are the real Octicons.** The tests fix each field to one GitHub Octicon by the data that draws it. I downloaded all 23 from GitHub's official icon set (primer/octicons) and all 23 match. The passed and failed entries also match today's two circle files.
- **Every new test fails today for the right reason.** I ran the new test file: all 47 fail because the icon files, the table or the drawn icons don't exist yet. None fail on a crash or a bad path. Each failure names its criterion.
- **The planner's edits to older tests keep what they check.** They change 12 tests in 5 files, and each edit only ignores the new field icons when reading words or status circles.

**Two notes, not blockers**
- The test only checks the blocker icon on a code review's comment, not on a plan review's comment. A worker could draw it on one stage only and still pass.
- The plan touches `dokima/card.py`, which AGENTS.md says to change only when the issue asks. The issue names `card.icon()` there, and card features have always changed that file, so I didn't block on it.

**Planner's choices you may want to look at**
- Passed and failed keep today's circles; the other 21 fields get new icons, no two alike.
- The autopilot, related and blocks icons go into the table, but nothing draws them yet; later stories of #230 do that.
- The one-line Autopilot comments stay plain words, because code reads them back word for word.

There were no earlier blockers to answer and no questions for you in the plan.

I also started a run of the full test suite, but it was cut off after 2 minutes and moved to the background. I didn't use its result; the approval rests on the runs above.

`15. Bash`
```
grep -E "passed|failed" /tmp/claude-1001/-home-runner-work-dokima-dokima/663d3935-d68e-4196-a9de-f5351e85b568/tasks/b3164bhp8.output | grep -v "^FAILED tests/test_field" | tail -5
```

> 3 failed, 467 passed, 47 deselected in 280.36s (0:04:40)
> 50 failed, 467 passed in 280.14s (0:04:40)
> @@ -69,7 +69,8 @@ def test_title_asks_for_approval_when_all_checks_passed(record_property):

**Agent:** The full test suite finished: 3 tests fail outside the new test file. I'm finding which ones before I stand by the approval.

`16. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 580 pytest -q -rf --deselect tests/test_field_icons.py -p no:cacheprovider 2>&1 | grep -E "^FAILED|passed|failed" | cut -c1-300
```

> FAILED tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner - AssertionError: 166.1: a review whose blockers name their fixer was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said it"
> FAILED tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named - AssertionError: 157.1: a well-formed review.json was rejected: asks must list every ask in the owner's issue and comments, each {"ask": "the owner's words", "source": "a link to where they said
> FAILED tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests - AssertionError: 157.3: a blocker on the plan's own criterion and test was rejected: {'id': 'B1', 'criterion': '9.1', 'test': None, 'problem': 'p', 'evidence': 'e', 'fix': 'f', 'fixer': 'worker'
> 3 failed, 467 passed, 47 deselected in 279.46s (0:04:39)

**Agent:** These three aren't tests the planner edited. Checking whether they also fail on main without the planner's commit.

`17. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/base; git worktree add -q /tmp/base HEAD~1 && cd /tmp/base && timeout 300 python3 -m pytest -q -p no:cacheprovider tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests 2>&1 | tail -2; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/base
```

> )
> 3 failed in 5.11s

**Agent:** The same three tests fail on main without the planner's commit, so the planner didn't cause them. That's a real problem outside this issue, so I'm adding it to the review as a proposed issue.

`18. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'E'
import json
p="/tmp/dokima-out/review.json"; d=json.load(open(p))
d["issues_found"]=[{"title":"Three hand-back check tests fail on main because their sample reviews list no asks",
 "why":"The review check now demands a list of the owner's asks, but the sample reviews in these tests have none, so the full test suite is red on main for every pull request whatever its work.",
 "evidence":"On main (27453f2), pytest fails tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner, tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named and tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests with 'asks must list every ask in the owner's issue and comments'."}]
json.dump(d,open(p,"w"),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 234 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** The approval still stands, but the full test suite isn't green: 3 tests fail on main, before the planner's commit.

The full suite ran in 4 min 40 s: 467 passed, 3 failed, and the 47 new icon tests also fail, as expected. The three failures:
- `tests/test_fixer.py::test_every_review_blocker_names_the_worker_or_the_planner`
- `tests/test_handback_check.py::test_well_formed_hand_backs_pass_and_every_malformed_field_is_named`
- `tests/test_handback_check.py::test_every_blocker_is_about_one_of_the_plans_criteria_and_its_tests`

I checked out the commit before the planner's (main, `27453f2`) in a separate folder and ran these three there: they fail the same way. The review check now requires a list of the owner's asks, and the sample reviews in these tests don't have one. The planner didn't edit these tests and they don't touch this plan, so this doesn't change the approval.

It does mean the "all tests" check stays red for any pull request, this issue's included, until they're fixed. That would hold up #234's merge on autopilot. I added it to `review.json` under `issues_found` as a proposed issue for you to file, and both hand-back checks still pass.
