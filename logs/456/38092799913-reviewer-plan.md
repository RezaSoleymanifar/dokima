# reviewer (plan) for #456

Run: https://github.com/dokima-dev/dokima/actions/runs/38092799913

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (64.2KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7336152c-09db-4374-b678-d14457110208/tool-results/bdxilxzlt.txt
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
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> 06-reviewer-plan.json
> 07-worker.json
> 08-reviewer-pr.json
> 09-updater.json
> 10-planner.json
> 11-reviewer-plan.json
> 12-worker.json
> 13-reviewer-pr.json
> 14-planner.json
> 15-reviewer-plan.json
> 16-worker.json
> 17-reviewer-pr.json
> 18-planner.json
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/pull/462 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #453, #454, #455
> 
> **User story:** File paths, commands and quoted code in plans, records and car

`2. Bash`
```
cd /tmp/pack; cat issue.md | sed -n '1,400p'
```

> <persisted-output>
> Output too large (36.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/7336152c-09db-4374-b678-d14457110208/tool-results/byrgm5d2v.txt
> 
> Preview (first 2KB):
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/pull/462 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #453, #454, #455
> 
> **User story:** File paths, commands and quoted code in plans, records and cards show as code, with `&lt;`, `&gt;` and `&amp;` exactly as written, while an agent's other words still never draw HTML.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/m

`3. Bash`
```
cd /tmp/pack; sed -E 's/<img [^>]*>//g' issue.md | head -c 20000
```

> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/pull/462 ·  [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 
>  **Relates to:** #453, #454, #455
> 
> **User story:** File paths, commands and quoted code in plans, records and cards show as code, with `&lt;`, `&gt;` and `&amp;` exactly as written, while an agent's other words still never draw HTML.
> 
>  **Acceptance criteria**
> 
> -  **<a href="https://github.com/dokima-dev/dokima/actions/runs/38091394199/job/114328416375">Acceptance criterion</a>:** The planner's, worker's and reviewer's prompts tell them to write code, file paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.
>   - *<a href="https://github.com/dokima-dev/dokima/blob/00eaa56cb79ed62b32b083d4918a3f470f8cf0fc/tests/test_code_as_written.py#L132"> Verified by</a>: The planner's, worker's and reviewer's prompts each say to write code as markdown code.*
>   - Source: https://github.com/dokima-dev/dokima/issues/416
> -  **<a href="https://github.com/dokima-dev/dokima/actions/runs/38091394199/job/114328416415">Acceptance criterion</a>:** Text inside backticks or a code block

`4. Bash`
```
cd /tmp/pack; sed -E 's/<img [^>]*>//g' issue.md | tail -c +20000 | grep -v '^$' 
```

> summary><b> Stats</b></summary>
> Opus 5.5 · 0.5 min · 8 turns · 340K tokens in, 3K out · $0.40 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/456/38086788638-worker.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/38086788638)
> </details>
> <details><summary>Full record</summary>
> (full record: in/07-worker.json)
> </details>
> **Next:** The reviewer starts now.
> ### dokima-runtime on PR #462 (2026-10-10T21:14:38Z)
> <!-- dokima-record -->
>   Code review blocked the work with 2 blockers.
> -  Text outside code is escaped as today, so an agent's words can never inject HTML. That holds between two pieces of code and after a backtick or fence that never closes.
>   -  The test for the non-functional requirement only puts an unclosed fence in the middle of a line, where GitHub never opens a code block. An unclosed fence at the start of a line, such as a plan summary that is just ```` ``` open ````, passes the test while GitHub draws an agent's `&lt;kbd&gt;` as HTML. Smallest fix: add a case to `tests/test_code_as_written.py::test_an_agents_words_outside_code_never_draw_html` where an agent text starts with an unclosed fence (backticks and tildes) and a later text on the same card or run comment holds a code block with `&lt;kbd&gt;evil&lt;/kbd&gt;`, and check GitHub's recorded rendering draws no `kbd`.
>   -  `card.escape` writes a fence that never closes as plain words, unescaped, at the start of a line: as the first words of a text placed at a line 

`5. Bash`
```
cd /tmp/pack; cat open_blockers.json; python3 -c "
import json;p=json.load(open('plan.json'));print(json.dumps({k:v for k,v in p.items() if k not in()},indent=1)[:6000])"; cat parent.json | head -c 1500; git -C /home/runner/work/dokima/dokima log --oneline -3
```

> []{
>  "kind": "user_story",
>  "summary": "Agents write code as markdown code, and cards and run comments show `<`, `>` and `&` inside it exactly as written.",
>  "user_story": "File paths, commands and quoted code in plans, records and cards show as code, with `<`, `>` and `&` exactly as written, while an agent's other words still never draw HTML.",
>  "acceptance_criteria": [
>   {
>    "text": "The planner's, worker's and reviewer's prompts tell them to write code, file paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.",
>    "source": "https://github.com/dokima-dev/dokima/issues/416"
>   },
>   {
>    "text": "Text inside backticks or a code block shows on cards and in run comments exactly as written, `<`, `>` and `&` included. A code block keeps its lines, and outside code they are still escaped.",
>    "source": "https://github.com/dokima-dev/dokima/issues/416"
>   },
>   {
>    "text": "As GitHub renders a card and a run comment, `<`, `>` and `&` inside code show as written, never as `&lt;`, `&gt;` or `&amp;`. Outside code they never make GitHub draw HTML. This is checked on GitHub's own rendering of what the code writes, recorded in `dokima/github_rendering.json`; an answer recorded for other text fails the test.",
>    "source": "https://github.com/dokima-dev/dokima/issues/416"
>   }
>  ],
>  "non_functional": [
>   {
>    "text": "Text outside code is escaped as today, so an agent's words can never inject HTML. That holds between two pieces of code a

`6. Bash`
```
cd /tmp/pack; grep -o 'issuecomment-[0-9]*' -r . | sort -u | head; grep -n 'Scope cut' -r . | head -3
```

> issue.md:618:/plan Scope cut, overrides earlier words: keep only 456.1 (prompts say write code as markdown code) and 456.2 (text inside code shows as written; outside code escaping stays exactly as main does it). Drop 456.3, the non-functional requirement, all GitHub-rendering tests and recorded answers. No new edge cases. Smallest change.
> Shell cwd was reset to /home/runner/work/dokima/dokima

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added a test that a raise's label over several lines or holding a code block draws no HTML in a run comment's Raised and Raised earlier sections, and widened the non-functional requirement to name that case."],
  "decided": ["The planner dropped the card's lone-backtick label case, since raises left the card in #465."],
  "open": ["The plan still carries 456.3, the non-functional requirement and every GitHub-rendering test, which the owner's newest /plan drops."]},
 "verdict": "block",
 "summary": "The owner's newest /plan cuts the scope to 456.1 and 456.2 only, and this plan still carries 456.3, the non-functional requirement and every GitHub-rendering test and recorded answer.",
 "raises": [
  {"kind": "blocker", "to": "planner", "label": "Owner's scope cut not done",
   "text": "The owner's newest /plan says to keep only 456.1 (prompts say to write code as markdown code) and 456.2 (text inside code shows as written; outside code, escaping stays exactly as main does it), and to drop 456.3, the non-functional requirement, all GitHub-rendering tests and recorded answers, with no new edge cases and the smallest change. The plan still has criterion 456.3, the non-functional requirement 456.4 with four tests, `dokima/github_rendering.json` in scope and recorded GitHub answers. Smallest fix: keep only 456.1 and 456.2 and their tests; make 456.2's 'outside code' part say escaping stays exactly as main does it; drop 456.3, 456.4, their tests, `tests/github_code_rendering.json`, `dokima/github_rendering.json` from scope and the out-of-scope line about GitHub's markdown API.",
   "evidence": "The owner's comment on #456 of 2026-10-10T22:43:51Z: '/plan Scope cut, overrides earlier words: keep only 456.1 ... and 456.2 ... Drop 456.3, the non-functional requirement, all GitHub-rendering tests and recorded answers. No new edge cases. Smallest change.' /tmp/pack/plan.js
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d['summary']="The plan still carries 456.3, the non-functional requirement and the GitHub-rendering tests, which the owner's newest /plan drops."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 456 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack; echo $?
```

> 0

**Agent:** I blocked the plan for [#456](https://github.com/dokima-dev/dokima/issues/456) (code shown as written on cards and in comments). It doesn't follow your newest `/plan`, the scope cut you sent at 22:43.

**Why it's blocked:** your cut keeps only two criteria. 456.1 is that the prompts say to write code as markdown code. 456.2 is that text inside code shows as written, and outside code escaping stays exactly as main does it. You asked to drop everything else. But the plan was written a minute before your cut, so it still carries:
- 456.3;
- the non-functional requirement, with its four tests;
- every check against how GitHub displays the text, plus the GitHub answers saved in the repo for them.

The blocker goes to the planner. The fix is to keep only 456.1 and 456.2 and their tests, and remove the rest from the plan and its scope.

**Question for you:** you also wrote that a fresh issue replaces this one, and you closed [#462](https://github.com/dokima-dev/dokima/pull/462) (the pull request for this issue). So should #456 be planned again at all, or closed as a duplicate of the fresh issue? I graded the plan against your cut in case it goes on.

I didn't rerun the tests, since the problem is the plan's scope, not whether the tests work. The review is in `/tmp/dokima-out/review.json` and passes both Dokima checks.
