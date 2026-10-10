# reviewer (plan) for #477

Run: https://github.com/dokima-dev/dokima/actions/runs/38092997507

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
> # Issue #477: Code shows as code, never escaped
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> Part of #416. My words:
> 
> Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for several lines), and Dokima never escapes text inside code, so `<`, `>` and `&` show as written.
> 
> <!-- dokima-done -->
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #477 (2026-10-10T22:44:59Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #477 (2026-10-10T22:4

`2. Bash`
```
cd /tmp/pack; python3 -c "
import json;d=json.load(open('in/01-planner.json'));print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:4000])"; head -c 3000 parent.json; echo; cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_code_unescaped.py
```

> {
>  "role": "planner",
>  "stage": null,
>  "run_id": "38092603948",
>  "commit_before": "b755a9a80820f05cdc2df53adfb3078d51e07bc2",
>  "started_by": "dokima-runtime[bot]",
>  "models": [
>   "claude-opus-5-5"
>  ],
>  "report": {
>   "duration_ms": 354972,
>   "turns": 22,
>   "cost_usd": 1.0292155999999997,
>   "tokens_in": 1275835,
>   "tokens_out": 14470
>  },
>  "log": "https://github.com/dokima-dev/dokima/blob/logs/logs/477/38092603948-planner.md",
>  "run": "https://github.com/dokima-dev/dokima/actions/runs/38092603948",
>  "handback": {
>   "kind": "user_story",
>   "summary": "Code that agents write shows on cards and run comments exactly as written, never escaped.",
>   "user_story": "Code, file paths and commands in what agents write show as code, with <, > and & exactly as typed.",
>   "acceptance_criteria": [
>    {
>     "text": "Code in backticks or in a code block shows its <, > and & as written on the issue card and in run comments.",
>     "source": "https://github.com/dokima-dev/dokima/issues/477"
>    },
>    {
>     "text": "Plain words outside code still show HTML as text, so an agent's <kbd> or <img> never draws.",
>     "source": "https://github.com/dokima-dev/dokima/issues/477"
>    },
>    {
>     "text": "The planner, worker and reviewer are each told to write code, file paths, commands and quoted code as markdown code.",
>     "source": "https://github.com/dokima-dev/dokima/issues/477"
>    }
>   ],
>   "non_functional": [],
>   "scope": [
>    "dokima/card.py",
>    "dokima/roles/planner.md",
>    "dokima/roles/worker.md",
>  

`3. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def _esc\|escape\|html" dokima/card.py | head -60; ls dokima/roles
```

> 14:import html
> 219:def escape(text):
> 220:    return html.escape(text or "", quote=False)
> 242:    words = lambda s: escape(" ".join(str(s).split()))
> 374:        links.append(f"[latest run]({worker['html_url']})")
> 391:        label = f'<a href="{check["html_url"]}">{label}</a>'
> 392:    out = [f"- {circle(repo, state(check))} **{label}:** {escape(c.get('text'))}"]
> 396:                       f'{escape(t["verified_by"])}*')
> 430:                re.match(re.escape(agent.LIVE) + r"[^*]*\*\*Reviewer \(pr\)\*\*", (c.get("body") or "").strip()):
> 455:    approval = {"state": "APPROVED", "html_url": merge.get("html_url")} if merge else owner_review(found["reviews"], found["owners"])
> 458:            f"{circle(repo, state(all_tests), all_tests and all_tests['html_url'])} All tests · "
> 460:            f"{circle(repo, approval_st, approval and approval.get('html_url'))} {field_icon(repo, 'owner approval')} "
> 481:        lines += [escape(h["summary"].strip()), ""]
> 496:                          f"issue's blocked-by links: {escape(found['unread'])}")
> 509:            lines += [f"**User story:** {escape(h['user_story'])}", ""]
> 518:            lines += fold("Out of scope", [f"- {escape(s)}" for s in h["out_of_scope"]]) + [""]
> 589:    return {"status": run["status"], "conclusion": run["conclusion"], "html_url": run["html_url"]} if run else None
> 670:        return {"name": name, "status": status, "conclusion": conclusion, "html_url": f"https://github.com/{repo}/actions/runs/2"}
> 689:    done = {"statu

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_code_unescaped.py 2>&1 | grep -E "Error|assert|passed|failed|477" | head -40; grep -n "escape" dokima/agent.py | head -30
```

> the start and end of the text, and checks each span comes back character for character. Proves 477.1."""
>         record_property("proves", "477.1")
> >               assert whole in got, f"477.1: the code {whole!r} was escaped to {got!r}"
> E               AssertionError: 477.1: the code "`if a < b && c > d: run('<kbd>')`" was escaped to "Run `if a &lt; b &amp;&amp; c &gt; d: run('&lt;kbd&gt;')` first."
> E               assert "`if a < b && c > d: run('<kbd>')`" in "Run `if a &lt; b &amp;&amp; c &gt; d: run('&lt;kbd&gt;')` first."
> tests/test_code_unescaped.py:78: AssertionError
>         plain line above it is still escaped. Proves 477.1."""
>         record_property("proves", "477.1")
> >           assert ln in got, f"477.1: the code block line {ln!r} was changed; got:\n" + "\n".join(got)
> E           AssertionError: 477.1: the code block line 'if a < b and c > d:' was changed; got:
> E           assert 'if a < b and c > d:' in ['Call it like &lt;this&gt;:', '```python', 'if a &lt; b and c &gt; d:', "    print('&amp;amp; &lt;kbd&gt;x&lt;/kbd&gt;')", '```', 'Done.']
> tests/test_code_unescaped.py:91: AssertionError
>         and checks the card's line for each holds that code character for character, with no &lt;, &gt; or &amp;. Proves 477.1."""
>         record_property("proves", "477.1")
> >           assert CODE in ln, f"477.1: the card shows the code escaped: {ln!r}"
> E           AssertionError: 477.1: the card shows the code escaped: '- <img src="https://raw.githubusercontent.com/o/r/main/doki

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_code_unescaped.py 2>&1 | tail -12; sed -n 930,945p dokima/agent.py; grep -rn "def escape\|card.escape\|escape(" dokima/*.py | grep -v "re.escape\|html.escape" | awk -F: '{print $1}' | sort | uniq -c; gh issue view 460 --json title 2>/dev/null | head -3
```

> ?                          ^
>   + &lt;img src=x&gt; then `a&lt;b`
>   ?                          ^^^^
> FAILED tests/test_code_unescaped.py::test_card_still_escapes_plain_words - AssertionError: 477.2: the card drew an agent's HTML, or escaped its code: '- <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> **Acceptance criterion:** Press &lt;kbd&gt;Enter&lt;/kbd&gt; to run `if a &lt; b &amp;&amp; c &gt; d: run(\'&lt;kbd&gt;\')`'
> assert "Press &lt;kbd&gt;Enter&lt;/kbd&gt; to run `if a < b && c > d: run('<kbd>')`" in '- <img src="https://raw.githubusercontent.com/o/r/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle...eptance criterion:** Press &lt;kbd&gt;Enter&lt;/kbd&gt; to run `if a &lt; b &amp;&amp; c &gt; d: run(\'&lt;kbd&gt;\')`'
> FAILED tests/test_code_unescaped.py::test_prompts_ask_for_code_as_code[planner] - AssertionError: 477.3: the planner prompt has no '# Code in text' section
> assert None
> FAILED tests/test_code_unescaped.py::test_prompts_ask_for_code_as_code[worker] - AssertionError: 477.3: the worker prompt has no '# Code in text' section
> assert None
> FAILED tests/test_code_unescaped.py::test_prompts_ask_for_code_as_code[reviewer] - AssertionError: 477.3: the reviewer prompt has no '# Code in text' section
> assert None
> 9 failed in 0.09s
>     AGENTS.md, which is no issue or pull request, stay linked to it."""
>     if source == "AGENTS.md":
>         return f"[\"{escape_line(w

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -rn "&#35;" dokima/*.py | head
```

> dokima/card.py:532:    keeps the PR's own Closes #N. In the PR's copy a `#` after a closing keyword is written `&#35;`, and the `h` of a
> dokima/card.py:537:    shown = KEYWORD_URL.sub(r"\1&#104;", KEYWORD_HASH.sub(r"\1&#35;", ask or ""))

**Agent:** I've run the plan's 9 new tests (all fail today because the feature is missing) and checked where escaping happens in the code. Now I'm writing the review.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned three criteria: code in backticks or a code block shows its <, > and & as written on the card and in run comments; plain words outside code still show HTML as text; the planner, worker and reviewer prompts each ask for code as markdown code.",
          "Wrote nine tests in tests/test_code_unescaped.py, all failing today because the feature is missing."],
  "decided": ["The one escape in dokima/card.py skips code spans and fenced code blocks; everything else is escaped as today.",
              "Fields that are never escaped today are left to #460, and fields drawn on one line still join a block's lines."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan carries the owner's whole ask, and its tests fail today only because code is still escaped and the prompts have no Code in text section.",
 "raises": [
  {"kind": "issue", "label": "Outside this issue",
   "text": "In the pull request's Original issue fold, a `#` after a closing keyword is written `&#35;` even inside code in the owner's words, so `Closes #5` in backticks shows as `Closes &#35;5`.",
   "evidence": "dokima/card.py:537 applies KEYWORD_HASH.sub(r\"\\1&#35;\", ask) to the whole ask, code spans included."}
 ],
 "answers": [],
 "asks": [
  {"ask": "Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for several lines)", "source": "https://github.com/dokima-dev/dokima/issues/477", "criterion": "477.3"},
  {"ask": "Dokima never escapes text inside code, so `<`, `>` and `&` show as written.", "source": "https://github.com/dokima-dev/dokima/issues/477", "criterion": "477.1"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 477 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> summary holds 27 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan carries the owner's whole ask, and every new test fails today only because code is still escaped and the prompts lack the section."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 477 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#477](https://github.com/dokima-dev/dokima/issues/477) (code shows as code, never escaped). The review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **Every ask is covered.** The issue has two asks:
  - Agents write code, paths and commands as markdown code. Criterion 477.3 carries this: the planner, worker and reviewer prompts each get a "Code in text" section.
  - Dokima never escapes text inside code. Criterion 477.1 carries this.

  Criterion 477.2 keeps HTML in plain words shown as text, so an agent's `<kbd>` or `<img>` still never draws.
- **The new tests fail for the right reason.** I ran all 9 tests in `tests/test_code_unescaped.py`. Each fails only because the feature is missing: code is still escaped, and the prompts have no "Code in text" section. None fails from a crash or a bad path.
- **The tests catch both kinds of mistake.** They catch code still escaped and plain words left unescaped. The plain-words cases include a lone backtick and backtick runs of different lengths, so a fix that switches escaping off too widely turns them red.
- **One change covers every place.** All escaping goes through a single function in `dokima/card.py`, and both the issue card and the run comments use it. The tests check the result on both.

I raised one problem outside this issue as a proposal for a new issue. In the pull request's Original issue fold, Dokima changes a `#` after a closing keyword to `&#35;` even inside code in the owner's words (`dokima/card.py:537`). So `Closes #5` written in backticks would show as `Closes &#35;5`.
