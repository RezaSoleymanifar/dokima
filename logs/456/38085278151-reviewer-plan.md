# reviewer (plan) for #456

Run: https://github.com/dokima-dev/dokima/actions/runs/38085278151

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/456
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue found"> **Outside this issue:** Some run comment fields are written with no HTML escaping at all, so an agent's `&lt;kbd&gt;` or `&lt;img&gt;` in them draws HTML: an answer's why, the owner's quoted words, an escalation's summary and the planner's test change reasons. · filed as an issue
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #452, #453, #454, #455
> 
> **User story:** File paths, commands and quoted code in plans, records and cards show as code, with `&lt;`, `&gt;` and `&amp;` exactly as written, while an agent's other words still never draw HTML.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.sv

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; cat tests/test_code_as_written.py; ls tests/github_html.py dokima/github_rendering.json 2>&1
```

> Exit code 2
> commit dc59136dc5ce0d0c52e60e5686f04944b4e257fc
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 20:23:55 2026 +0000
> 
>     planner for #456 (run 38083234466)
> 
>  tests/github_html.py          | 112 ++++++++++++++++++++++
>  tests/github_rendering.json   |  12 +++
>  tests/test_code_as_written.py | 214 ++++++++++++++++++++++++++++++++++++++++++
>  3 files changed, 338 insertions(+)
> """Agents write code as markdown code, and Dokima never escapes it (#456).
> 
> Story 5 of #416.
> 
> The agents' prompts (dokima/roles/planner.md, worker.md, reviewer.md) tell them to write code, file paths, commands and
> quoted code as markdown code: backticks inline, a code block for several lines. Cards (`card.render` in dokima/card.py)
> and run comments (`agent.render` in dokima/agent.py) then draw an agent's text with `<`, `>` and `&` exactly as written
> inside backticks or a code block, and escaped everywhere else, so an agent's words never draw HTML.
> 
> The texts below mix code with prose that tries to draw HTML (a <kbd> element and an <img> whose alt is "evil"):
> 
>     inside code      must show as written, `<`, `>` and `&` included, never as &lt; &gt; &amp;
>     outside code     must stay escaped, also after a backtick or a fence that never closes
> 
> Two kinds of proof: the raw text the code writes, and GitHub's own rendering of that text, recorded in the repo by
> tests/github_html.py (an answer recorded for other text fails the test). "Visible" means

`3. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/github_html.py; cat tests/github_rendering.json; sed -n 60,140p tests/test_code_as_written.py
```

> <persisted-output>
> Output too large (30.8KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b065795a-0b2e-412b-8233-d09f939fa1af/tool-results/bsw8qpupp.txt
> 
> Preview (first 2KB):
> """GitHub's own rendering of markdown, recorded in the repo for the tests.
> 
> Tests use it to check how GitHub shows what code writes.
> 
> Tests run in CI with no network and no secrets, so GitHub's answers from its markdown API (POST /markdown, gfm) are
> recorded once in dokima/github_rendering.json, as {"answers": [{"text": ..., "html": ...}, ...]}, and read back here.
> tests/github_rendering.json holds answers the planner recorded for what the code wrote before the work, in the same
> shape, so a test can show it fails today for the right reason on GitHub's real rendering.
> An answer counts only for the exact text it was recorded for: when the code writes anything else, the test fails and
> says how to record GitHub's answer for the new text, so a stale answer never passes.
> 
>     DOKIMA_RECORD_RENDER=1 python3 -m pytest tests/test_code_as_written.py   records GitHub's answer for every text
>                                                                               a test asks about and has no answer for
>     python3 tests/github_html.py                                              asks GitHub again for every recorded
>                                                                               text and rewrites its answer
>     DOKIMA_LIVE_RENDER=1 python3 -m pytest ...     

`4. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 30,112p tests/github_html.py; python3 -c "
import json;d=json.load(open('tests/github_rendering.json'));print([len(a['text']) for a in d['answers']])"; sed -n 60,135p tests/test_code_as_written.py
```

> ANSWERS = os.path.join(ROOT, "dokima", "github_rendering.json")
> PLANNED = os.path.join(ROOT, "tests", "github_rendering.json")
> 
> 
> def ask_github(text):
>     """GitHub's HTML for `text`, as its markdown API renders a comment."""
>     req = urllib.request.Request("https://api.github.com/markdown", data=json.dumps({"text": text, "mode": "gfm"}).encode(),
>                                  headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"})
>     if os.environ.get("GITHUB_TOKEN"):
>         req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
>     with urllib.request.urlopen(req, timeout=30) as r:
>         return r.read().decode()
> 
> 
> def load(path=ANSWERS):
>     """The answers recorded in `path`; none when the file is missing."""
>     if not os.path.exists(path):
>         return []
>     return json.load(open(path)).get("answers") or []
> 
> 
> def save(answers):
>     """Write the answers back, one per text, in a stable order."""
>     with open(ANSWERS, "w") as f:
>         json.dump({"answers": sorted(answers, key=lambda a: a["text"])}, f, indent=1, ensure_ascii=False)
>         f.write("\n")
> 
> 
> def rendered(text, criterion):
>     """GitHub's recorded HTML for exactly `text`; the test fails when there is none.
> 
>     The failure names `criterion` and says how to record the answer."""
>     answers = load()
>     found = next((a for a in answers + load(PLANNED) if a.get("text") == text), None)
>     if found is None and os.environ.get("DOKIMA_RECORD_RENDER") == "1"

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^(FAILED|E  .*45[0-9]\.|[0-9]+ (passed|failed))" | head -30
```

> E           AssertionError: 456.1: dokima/roles/planner.md never tells the agent to write code as markdown code
> E       AssertionError: 456.2: the card does not show this code as written: ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       AssertionError: 456.2: the run comment does not show this code as written: ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       AssertionError: 456.3: as GitHub renders the card, this code does not show as written (it shows ['a &lt; b &amp;&amp; c &gt; d', '&lt;T&gt; &amp; U', "if a &lt; b &amp;&amp; c &gt; d:\n    print('&lt;ok&gt; &amp; done')\n", '&lt;b&gt;', 'dokima/&lt;name&gt;.py']): ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       AssertionError: 456.3: as GitHub renders a run comment, this code does not show as written (it shows ['dokima/&lt;name&gt;.py', 'a &lt; b &amp;&amp; c &gt; d', "if a &lt; b &amp;&amp; c &gt; d: print('&lt;ok&gt; &amp; done')", '&lt;a&gt; &amp; &lt;b&gt;']): ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       AssertionError: 456.4: the code next to the prose is not shown as written on the card
> FAILED tests/test_code_as_written.py::test_every_agent_prompt_says_to_write_code_as_markdown_code - AssertionError: 456.1: dokima/roles/planner.md never tells the agent to write code as markdown code
> FAILED tests/test_code_as_written.py::test_code_on_the_card_shows_exactly_as_written_and_prose_stays_escaped - Asserti

**Agent:** Plan's six new tests all fail today for the right reason. Now checking the planner's outside-issue raise before writing the review.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "def escape_line" -A6 dokima/agent.py; grep -n "escape_line(a.get('why')\|escape_line(words\|escape_line(h\['summary'\]\|escape_line(h\[.summary.\])" dokima/agent.py
```

> 936:def escape_line(text):
> 937-    """One sentence kept on one line, so the comment opens with it whole."""
> 938-    return re.sub(r"\s+", " ", text or "").strip()
> 939-
> 940-
> 941-def jsonl_files(root):
> 942-    """Every session log under root, hidden folders included (Claude keeps its logs under .claude)."""
> 611:        lines += ["", escape_line(h["summary"])]
> 669:        lines.append(f"  - {word}: {escape_line(a.get('why'))}")
> 932:        return f"[\"{escape_line(words).replace(']', '\\]')}\"]({words_link(source)})"
> 933:    return f"\"{escape_line(words)}\" {source}"

**Agent:** Confirmed. Writing the hand-back.

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Planned four criteria: the three role prompts say to write code as markdown code; cards and run comments show code exactly as written; GitHub's own rendering shows it so; words outside code still never draw HTML.",
          "Wrote six tests in `tests/test_code_as_written.py`, with GitHub's rendering of today's card and run comment recorded in `tests/github_rendering.json`, and a script, `tests/github_html.py`, that asks GitHub again."],
  "decided": ["GitHub's answers are recorded in `dokima/github_rendering.json` instead of calling GitHub in CI; an answer recorded for other text fails the test."],
  "open": ["Raised as its own issue: some run comment fields (an answer's why, the owner's quoted words, an escalation's summary, test change reasons) are written with no HTML escaping."]},
 "verdict": "approve",
 "summary": "The plan carries every ask of story 5 of #416, and each of its six tests fails today because code is still escaped, not because of a crash.",
 "raises": [],
 "answers": [{"raise": "P1", "answer": "done", "why": "Confirmed: `escape_line` in `dokima/agent.py` (line 936) only joins whitespace, and it alone writes the review summary (line 611), an answer's why (line 669) and the owner's quoted words (lines 932-933), so an agent's `<kbd>` there draws HTML. It lies outside this issue's ask and is worth its own issue."}],
 "asks": [
  {"ask": "The planner's, worker's and reviewer's prompts tell them to write code, paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.1"},
  {"ask": "Text inside backticks or a code block shows on cards and in run comments exactly as written, `<`, `>` and `&` included. Outside code they are still escaped.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.2"},
  {"ask"
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan carries every ask of story 5 of #416, and its six tests fail today because code is still escaped."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 456 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#456](https://github.com/dokima-dev/dokima/issues/456) (agents write code as markdown code, and it shows exactly as written). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **Asks covered:** each of the four asks from story 5 of [#416](https://github.com/dokima-dev/dokima/issues/416) (card links show as GitHub's own references) has its own criterion:
  - 456.1: the planner, worker and reviewer prompts say to write code as markdown code.
  - 456.2: code shows exactly as written on cards and in run comments.
  - 456.3: GitHub's own rendering shows that code as written.
  - 456.4: an agent's words outside code still never draw HTML.
- **Tests:** I ran the six new tests and all six fail today for the right reason. The prompts don't say it yet, code is still turned into `&lt;`, `&gt;` and `&amp;`, and GitHub's saved rendering shows it that way. None fails from a crash or a bad path. The tests also check the other direction: words outside code stay escaped, including after a backtick or code fence that never closes. So a change that just stops escaping everything would also fail.
- **Planner's outside-issue raise:** I confirmed it. In `dokima/agent.py`, `escape_line` only joins whitespace, and it is what writes the review summary, an answer's reason and the owner's quoted words into run comments. So HTML an agent puts in those draws on GitHub.

One thing to keep in mind for the code review: the worker writes the saved copy of GitHub's rendering (`dokima/github_rendering.json`) themselves. The tests reject a copy saved for different text, but not one that was made up. The code reviewer should check it against GitHub by running the tests with `DOKIMA_LIVE_RENDER=1` or running `python3 tests/github_html.py`. Both call GitHub, which I didn't do here.
