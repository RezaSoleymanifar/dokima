# reviewer (plan) for #359

Run: https://github.com/dokima-dev/dokima/actions/runs/38023076393

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (37.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/1ab4094d-c307-4e27-998f-40cd157783d0/tool-results/b7v0coseu.txt
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
> # Issue #359: Source links to where the owner said it, shown as a GitHub reference with icon and name
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 354 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Cards show every issue, pull request and Source the way GitHub shows its own references: status icon, title and number.
> 
> **Plan** · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/needs-you.svg" width="16" height="16" align="absmiddle" alt="needs you"> Needs you: Say /work to build the plan
> 
> [issue #359](https://github.com/dokima-dev/dokima/issues/359)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #371, #335, #354
> 
> **User story:** Wherever a card names an issue, a pull request or the place the owner asked for something, the owner sees GitHub's own reference, with its status icon, title and number, and can click straight through to it.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmidd

`2. Bash`
```
cd /tmp/pack; sed -n '/Original issue/,$p' issue.md | head -200
```

> <details><summary>Original issue</summary>
> 
> Each acceptance criterion's Source points to the owner's own words: the comment where the owner asked for it, the most recent time, or the issue the owner wrote. It never points to a story the planner wrote when it split a parent. On the card, Source shows the way GitHub shows a reference to an issue, pull request or comment, with its status icon and name (as the Out of scope section shows #300), not a plain word "Source" linked to a page.
> 
> Owner's words (2026-10-09), on PR #327: "the source under the verified by line when I click on it it goes back to the issue itself it doesn't go to a specific comment ... what I wanted was actually a reference to the source something that I said or an original issue ... Take a look at Out of scope section on the same PR you can see that the references to other places is shown with green circle with the green dot in it and followed by whatever name it's trying to reference ... I wanted the source to show things that way"
> 
> Today on PR #327 every Source links to https://github.com/dokima-dev/dokima/issues/299, the split story itself, so the owner cannot check where they asked for it.
> 
> 
> </details>
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #359 (2026-10-09T21:16:30Z)
> 
> Correction, this narrows the issue: the Source may point to a story, an issue or a comment, whichever holds the ask; don't force it to a single comment, since sometimes there is no comment to point to. This issue is only about how Sour

`3. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps(p,indent=1))"
```

> []{
>  "kind": "user_story",
>  "summary": "Cards and the agents' run comments show every issue, pull request and Source the way GitHub shows its own references: status icon, title and number.",
>  "user_story": "Wherever a card or an agent's run comment names an issue, a pull request or the place the owner asked for something, the owner sees GitHub's own reference, with its status icon, title and number, and can click straight through to it.",
>  "acceptance_criteria": [
>   {
>    "text": "Each criterion's Source reads Source: and then GitHub's reference to wherever the ask is, never the word Source linked to a page. It may point to a comment, the issue or a parent story; a criterion with no source shows no Source line.",
>    "source": "https://github.com/dokima-dev/dokima/issues/359"
>   },
>   {
>    "text": "The top row of the card names the issue and its pull request as GitHub references, not the linked words issue #N and PR #N. The latest run and files changed stay links, on the issue and the PR alike.",
>    "source": "https://github.com/dokima-dev/dokima/issues/359#issuecomment-6089549628"
>   },
>   {
>    "text": "A split's card lists each story as a GitHub reference followed by its stage, in the split's order, without repeating the title GitHub already shows.",
>    "source": "https://github.com/dokima-dev/dokima/issues/359#issuecomment-6089549628"
>   },
>   {
>    "text": "Nowhere on the issue or PR card, open or merged, is an issue, pull request or comment linked under words of its own. Blocked 

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD | head -30; python3 -c "
import json;d=json.load(open('/tmp/pack/in/03-planner.json'));print(list(d.keys()));print(json.dumps({k:v for k,v in d.items() if k!='handback'},indent=1)[:3000])"; grep -o 'issuecomment-[0-9]*' /tmp/pack/issue.md | sort -u
```

> commit 72763fe0917adb8e212a2db2bfd3387d71995087
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 04:09:22 2026 +0000
> 
>     planner for #359 (run 38022557752)
> 
>  tests/test_answered_questions.py |  20 ++++--
>  tests/test_card_refs.py          | 135 +++++++++++++++++++++++++++++++++++++--
>  tests/test_raised_cards.py       |   6 +-
>  tests/test_run_cards.py          |  12 +++-
>  tests/test_summary_caps.py       |   4 +-
>  5 files changed, 158 insertions(+), 19 deletions(-)
> ['role', 'stage', 'run_id', 'commit_before', 'started_by', 'models', 'report', 'log', 'run', 'handback', 'check']
> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38022557752",
>  "commit_before": "e7b6d94e329fe715b0c394223620f4c018495b35",
>  "started_by": "RezaSoleymanifar",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 477424,
>   "turns": 32,
>   "cost_usd": 1.7034782,
>   "tokens_in": 2452133,
>   "tokens_out": 21493
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/359/38022557752-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38022557752",
>  "check": {
>   "passed": true,
>   "problems": []
>  }
> }
> issuecomment-6089549628

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git diff HEAD~1 -- tests/ | head -400
```

> diff --git a/tests/test_answered_questions.py b/tests/test_answered_questions.py
> index 8ceb538..82d6474 100644
> --- a/tests/test_answered_questions.py
> +++ b/tests/test_answered_questions.py
> @@ -14,8 +14,9 @@ What the comment must hold, pinned here:
>                      after the heading up to the first non-empty line that is neither a list item ("- " or "1. ") nor
>                      indented under one
>      each answer     inside the section, the question on one line, the answer on a later line and the evidence on a
> -                    later line still; the evidence is a markdown link whose text holds the matched words and whose
> -                    target is the source: the issue or comment link as given, or for "AGENTS.md" the file on the
> +                    later line still; the evidence holds the matched words in quotes and then the issue or comment
> +                    link as given, written out bare so GitHub draws it as its own reference (#359); for "AGENTS.md"
> +                    it is a markdown link whose text holds the matched words and whose target is the file on the
>                      repo's main branch, https://github.com/o/r/blob/main/AGENTS.md
>      no blank heading  a line that is only a bold heading ending in a colon (an icon may lead it) is always followed,
>                      past blank lines, by a list item
> @@ -122,8 +123,15 @@ def line_of(body, needle):
>  
>  
>  def link(matched, source):
> -    """A markdown link whose text holds the matched words and wh

`6. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_refs.py tests/test_answered_questions.py tests/test_raised_cards.py tests/test_run_cards.py tests/test_summary_caps.py tests/test_card.py tests/test_card_bullets.py tests/test_card_status.py tests/test_field_icons.py 2>&1 | grep -E "FAILED|ERROR|passed|failed|^E .*359|^E .*18|^E .*240|^E .*299" | head -60
```

> E               AssertionError: 359.1: the Source of “First thing works” is a link with words of its own, not a GitHub reference: - <a href="https://github.com/o/r/issues/40#issuecomment-111">Source</a>
> E           AssertionError: 359.2: the issue card links the issue or PR with words of its own: [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5')]
> E       AssertionError: 359.2: the issue is linked with words of its own: [('https://github.com/o/r/issues/40', 'issue #40')]
> E           AssertionError: 359.3: expected one line naming story #41 as a GitHub reference, found 0
> E               AssertionError: 359.4: the issue card links issues or PRs under words of their own: [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o/r/issues/40#issuecomment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> E           AssertionError: 359.4: the merged issue card links issues or PRs under words of their own: [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o/r/issues/40#issuecomment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> E       AssertionError: 359.5: the worker's comment links its pull request under words of its own: <img src="https://raw.githubusercontent.com/o/r/main/dokima/ico

**Agent:** Reviewing the plan for #359: every new test fails today for the right reason so far. Now I'm checking the rest of the run comments the plan covers.

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_card_refs.py 2>&1 | tail -15; python3 - <<'E'
import os,sys
os.environ["GITHUB_REPOSITORY"]="o/r";os.environ["GITHUB_SERVER_URL"]="https://github.com"
sys.path.insert(0,'.')
from tests import test_card_refs as t
for n,b in t.comments():
    print("=====",n); print(b.split("Full record")[0][:1800])
E
grep -n "def render\|pull request #\|Your words" dokima/agent.py | head -20
```

> assert 0 == 1
>  +  where 0 = len([])
> FAILED tests/test_card_refs.py::test_no_issue_or_pr_on_a_card_is_a_link_with_words_of_its_own - AssertionError: 359.4: the issue card links issues or PRs under words of their own: [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o/r/issues/40#issuecomment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> assert not [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o...omment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> FAILED tests/test_card_refs.py::test_a_merged_pr_card_still_names_both_as_references - AssertionError: 359.4: the merged issue card links issues or PRs under words of their own: [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o/r/issues/40#issuecomment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> assert not [('https://github.com/o/r/issues/40', 'issue #40'), ('https://github.com/o/r/pull/5', 'PR #5'), ('https://github.com/o...omment-111', 'Source'), ('https://github.com/o/r/issues/40', 'Source'), ('https://github.com/o/r/issues/30', 'Source')]
> FAILED tests/test_card_refs.py::test_the_workers_comment_names_its_pull_request_as_a_git

`8. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n '\](\|href=' dokima/agent.py | grep -v 'icons/' | head -40
```

> 236:    lines += [f"- {c.get('text', '')} ([source]({c.get('source', '')}))" for c in story.get("acceptance_criteria", [])]
> 314:            line = f"{icon(repo, 'queued')} {head} · waiting for [this run]({ahead})"
> 315:            what = (f"Queued, and waiting for [this run]({ahead}) on the same issue to end; this run starts after it. "
> 320:        return "\n".join([LIVE, line, "", what] + ([] if state == "handoff" else ["", f"<sub>[run]({run})</sub>"])) + "\n"
> 323:        what = (f"The agent is working; [watch it live]({run}) on GitHub. This card says checking when the agent ends, "
> 333:    return "\n".join([LIVE, line, "", what, "", f"<sub>[run]({run})</sub>"]) + "\n"
> 486:                lines.append(f"  - Your words: [\"{escape_line(a['words']).replace(']', '\\]')}\"]({words_link(a['source'])})")
> 506:        lines += record_fold(rec) + ["", f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
> 514:        lines += record_fold(rec) + ["", footnote(rec) if rec.get("agent_started") else f"<sub>No agent ran · [run]({rec.get('run', '')})</sub>"]
> 524:        lines += record_fold(rec) + ["", f"<sub>Found by code, no model" + (f" · [run]({rec['run']})" if rec.get("run") else "") + "</sub>"]
> 529:        first += f" ([pull request #{pr.rstrip('/').rsplit('/', 1)[-1]}]({pr}))"
> 557:                          f"  - Your words: [\"{escape_line(a['matched']).replace(']', '\\]')}\"]({words_link(a['source'])})"]
> 652:        return f"<sub>{stats} Filed by code, no model · [run]({rec.get('

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n '/def test_each_source/,/^def test_the_issue/p' tests/test_card_refs.py
```

> def test_each_source_shows_as_a_github_reference_to_where_the_ask_is(record_property):
>     """Each Source shows its comment, issue or parent story as a GitHub reference.
> 
>     Draws the card of a plan whose criteria point to a comment, to the issue and to the parent story, and checks
>     each criterion's last line reads Source: followed by its own link written out bare, so GitHub draws it with its
>     icon and title, that no Source is the word Source linked to a page, and that a criterion with no source shows no
>     Source line. Proves 359.1."""
>     record_property("proves", "359.1")
>     for page in ("issue", "pr"):
>         text = draw(page=page)
>         for words, url in (("First thing works", COMMENT), ("Second thing works", ISSUE["url"]),
>                            ("Third thing works", PARENT)):
>             lines = under(text, words)
>             assert lines, f"359.1: “{words}” has no lines under it on the {page} card"
>             last = lines[-1]
>             assert not wrapped(last) and "<a " not in last and "](" not in last, \
>                 f"359.1: the Source of “{words}” is a link with words of its own, not a GitHub reference: {last.strip()}"
>             assert bare_urls(last) == [url], \
>                 f"359.1: the Source of “{words}” should be {url} written out bare, the line is: {last.strip()}"
>             said = re.sub(r"^\s*-\s*", "", plain(last))
>             assert said == f"Source: {url}", \
>                 f"359.1: the Source line of “{words}” should read “S

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {"did": ["The planner added a fifth criterion: the agents' run comments name issues, pull requests and comments as GitHub references, with the worker's pull request and the owner's quoted words followed by a bare reference.", "It added three tests for it in tests/test_card_refs.py and updated six older tests that expected the old linked words.", "It added dokima/agent.py to the scope."], "decided": ["The Source line keeps a Source: label in front of the reference, as the owner answered; words quoted from AGENTS.md still link to AGENTS.md."], "open": []},
 "verdict": "approve",
 "summary": "The plan now takes both of the owner's answers: Source keeps its label and the agents' run comments show GitHub references too, and every new test fails today because the feature is missing.",
 "blockers": [],
 "notes": [{"text": "Criterion 5 gives the issue as its source, though the ask comes from the owner's /plan answer of 2026-10-10 on the issue; a link to that comment would let the owner click straight to it.", "evidence": "plan.json acceptance_criteria[4].source is https://github.com/dokima-dev/dokima/issues/359; the answer is the owner's comment of 2026-10-10T04:00:39Z."},
           {"text": "The tests prove the markdown leaves each reference bare; whether GitHub then draws the icon and title, especially for a link to a comment, can only be checked by eye on a real card after merge.", "evidence": "tests/test_card_refs.py module docstring: the tests read the markdown."}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "On the card, Source shows the way GitHub shows a reference to an issue, pull request or comment, with its status icon and name (as the Out of scope section shows #300), not a plain word \"Source\" linked to a page.", "source": "https://github.com/dokima-dev/dokima/issues/359", "criterion": "359.1"},
  {"ask": "the Source may point to a story, an issue or a comment,
```

> summary holds 33 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> rc=1

`11. Bash`
```
python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan takes both of the owner's answers, Source keeps its label and run comments show GitHub references, and every new test fails today as it should."
json.dump(d,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 359 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)
> rc=0

`12. Bash`
```
python3 - <<'E'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan takes both owner answers: Source keeps its label, run comments show GitHub references, and every new test fails today as it should."
json.dump(d,open(p,'w'),indent=1)
E
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 359 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo rc=$?
```

> rc=0

**Agent:** I approved the plan for [#359](https://github.com/dokima-dev/dokima/issues/359) (cards and run comments show GitHub-style references). The review is in `/tmp/dokima-out/review.json` and passes both checks.

- **Your two answers are in the plan.**
  - The Source line keeps a short `Source:` label in front of the reference (criterion 1), and its test checks the line reads exactly `Source: <link>`.
  - A new criterion 5 covers the agents' run comments. The worker's pull request is shown as a GitHub reference. Your quoted words stay as plain text in quotes, followed by a reference to where you said them. Words quoted from AGENTS.md still link to AGENTS.md. `dokima/agent.py` is now in scope.
- **Tests:** I ran all nine new tests in `tests/test_card_refs.py` and all nine fail today because the feature is missing, not because of a crash or bad setup. The six older tests the planner changed also fail on the old output for the same reason.
- **Your asks:** every one, from the issue, the widening comment and your `/plan` answers, maps to one of the five criteria. None is missing.
- **No other old links to issues:** the only other spot in `dokima/agent.py` that links an issue under its own words is the text a split's story copies from its parent's plan, which the plan explicitly leaves out.

Two notes, not blockers:
1. Criterion 5's source points to the issue itself, not to your `/plan` answer comment, so clicking it won't take you straight to where you asked for it.
2. The tests only check that each reference is left bare in the text. Whether GitHub then draws the icon and title, especially for a link to a comment, can only be checked by eye on a real card after merge.
