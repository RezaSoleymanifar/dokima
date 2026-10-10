# reviewer (plan) for #456

Run: https://github.com/dokima-dev/dokima/actions/runs/38087941644

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> <persisted-output>
> Output too large (40.7KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8a33e85a-1c0b-4728-bef7-2e0f6691045c/tool-results/bixxr46yn.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct 10 21:42 .
> drwxrwxrwt 18 root   root    4096 Oct 10 21:42 ..
> drwxr-xr-x  2 runner runner  4096 Oct 10 21:42 in
> -rw-r--r--  1 runner runner 36235 Oct 10 21:42 issue.md
> -rw-r--r--  1 runner runner     2 Oct 10 21:42 open_blockers.json
> -rw-r--r--  1 runner runner    15 Oct 10 21:42 parent.json
> -rw-r--r--  1 runner runner  4300 Oct 10 21:42 plan.json
> 
> in:
> total 64
> drwxr-xr-x 2 runner runner 4096 Oct 10 21:42 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 21:42 ..
> -rw-r--r-- 1 runner runner 4373 Oct 10 21:42 01-planner.json
> -rw-r--r-- 1 runner runner 3150 Oct 10 21:42 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3661 Oct 10 21:42 03-worker.json
> -rw-r--r-- 1 runner runner 3099 Oct 10 21:42 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4965 Oct 10 21:42 05-planner.json
> -rw-r--r-- 1 runner runner 2527 Oct 10 21:42 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2530 Oct 10 21:42 07-worker.json
> -rw-r--r-- 1 runner runner 4456 Oct 10 21:42 08-reviewer-pr.json
> -rw-r--r-- 1 runner runner  358 Oct 10 21:42 09-updater.json
> -rw-r--r-- 1 runner runner 4931 Oct 10 21:42 10-planner.json
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 --

`2. Bash`
```
cd /tmp/pack; cat issue.md
```

> <persisted-output>
> Output too large (35.4KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/8a33e85a-1c0b-4728-bef7-2e0f6691045c/tool-results/bfd7rx0qg.txt
> 
> Preview (first 2KB):
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/issues/456 · https://github.com/dokima-dev/dokima/pull/462 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 
> **Raised:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue found"> **Outside this issue:** The test re-plan also answered a raise R1 twice as RW1, which the planner card shows as 'A raise not found in this issue's earlier records'; the earlier worker raise was W1, so an answer by a wrong ID passed the check. · filed as an issue
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates t

`3. Read`
```
/home/runner/.claude/projects/-home-runner-work-dokima-dokima/8a33e85a-1c0b-4728-bef7-2e0f6691045c/tool-results/bfd7rx0qg.txt
```

> 1	# Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 2	
> 3	<!-- dokima-card -->
> 4	<!-- dokima-linked-from: 454, 455 -->
> 5	<!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> 6	Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 7	
> 8	**Review**
> 9	
> 10	https://github.com/dokima-dev/dokima/issues/456 · https://github.com/dokima-dev/dokima/pull/462 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 11	
> 12	**Raised:**
> 13	
> 14	- <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/issue-found.svg" width="16" height="16" align="absmiddle" alt="issue found"> **Outside this issue:** The test re-plan also answered a raise R1 twice as RW1, which the planner card shows as 'A raise not found in this issue's earlier records'; the earlier worker raise was W1, so an answer by a wrong ID passed the check. · filed as an issue
> 15	
> 16	<img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #452, #453, #454, #455
> 17	
> 18	**User story:** File paths, commands and quoted code in plans, records and cards show as code, with `&lt;`, `&gt;` and `&amp;` exactly as writ

`4. Bash`
```
cd /tmp/pack; cat plan.json; echo; cat open_blockers.json parent.json; echo; cat in/10-planner.json; echo; cat in/08-reviewer-pr.json
```

> {
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
>    "text": "Text outside code is escaped as today, so an agent's words can never inject HTML. That holds between two pieces of code and

`5. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -8 --stat | head -60; git diff origin/main --stat 2>/dev/null || git diff main --stat; ls tests/github* dokima/github* 2>&1
```

> 5ef7233 planner for #456 (run 38087336174)
>  tests/github_code_rendering.json | 20 ++++++++++++++++
>  tests/github_html.py             |  4 ++--
>  tests/github_rendering.json      | 12 ----------
>  tests/test_code_as_written.py    | 49 ++++++++++++++++++++++++++++++++++++----
>  4 files changed, 67 insertions(+), 18 deletions(-)
> bbea275 worker for #456 (run 38086788638)
>  dokima/github_rendering.json | 4 ++++
>  1 file changed, 4 insertions(+)
> 97c990e planner for #456 (run 38086312639)
>  tests/github_rendering.json   |  4 ++--
>  tests/test_code_as_written.py | 10 ++++++----
>  2 files changed, 8 insertions(+), 6 deletions(-)
> 6cd1790 worker for #456 (run 38085449663)
>  dokima/agent.py              |  6 ++--
>  dokima/card.py               | 84 ++++++++++++++++++++++++++++++++++++++++----
>  dokima/github_rendering.json |  8 +++++
>  dokima/roles/planner.md      |  5 +++
>  dokima/roles/reviewer.md     |  5 +++
>  dokima/roles/worker.md       |  5 +++
>  6 files changed, 103 insertions(+), 10 deletions(-)
> c472207 Merge remote-tracking branch 'origin/main' into try/issue-456
> d270c52 A play-through on a real sandbox repo checks the card after every step from issue to merge (#451)
>  .github/workflows/playthrough.yml |  49 +++
>  dokima/playthrough.py             | 324 ++++++++++++++++++++
>  tests/test_playthrough.py         | 619 ++++++++++++++++++++++++++++++++++++++
>  3 files changed, 992 insertions(+)
> dc59136 planner for #456 (run 38083234466)
>  tests/github_html.py          | 112 ++++++++++++++++++++++
>  test

**Agent:** Reading the plan's tests and checking which file they read GitHub's answers from.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; git log --oneline -3 origin/main; git merge-base HEAD origin/main; cat tests/test_code_as_written.py; cat tests/github_html.py | head -60; cat tests/github_code_rendering.json | head -c 1500; echo; python3 -c "import json;print(len(json.load(open('dokima/github_rendering.json'))))"
```

> bf1443b The issue card drops its link to itself, and a PR closes its issue by the issue's full address (#464)
> d270c52 A play-through on a real sandbox repo checks the card after every step from issue to merge (#451)
> 3d9fa7b The checks are named All tests and Acceptance criteria, with no done-whens left (#450)
> d270c5236950043e73f59cbe072d94f98bd03e32
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
> tests/github_html.py (an answer recorded for other text fails the test). "Visible" means a run comment without its
> Full record fold, which holds the raw JSON by design.
> """
> impor

`7. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | tail -15; python3 -m pytest -q -x 2>&1 | tail -3
```

> found = next((a for a in answers + load(PLANNED) if a.get("text") == text), None)
>         if found is None and os.environ.get("DOKIMA_RECORD_RENDER") == "1":
>             found = {"text": text, "html": ask_github(text)}
>             save(answers + [found])
>         if found is None:
> >           pytest.fail(f"{criterion}: GitHub's rendering of the text the code writes now is not recorded in "
>                         "dokima/github_rendering.json (an answer recorded for other text does not count). Record it with "
>                         "DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.")
> E           Failed: 456.4: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.
> 
> tests/github_html.py:68: Failed
> =========================== short test summary info ============================
> FAILED tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html[the card] - Failed: 456.4: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.
> FAILED tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html[the run comment] - Failed: 456.4: GitHub's rendering of the text the code writes now is not rec

`8. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wm; git worktree add -q /tmp/wm origin/main 2>&1|tail -1; cp tests/test_code_as_written.py tests/github_html.py tests/github_code_rendering.json /tmp/wm/tests/; cd /tmp/wm; ls dokima/github_rendering.json 2>&1; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^(FAILED|E  |[0-9]+ (passed|failed))" | cut -c1-300
```

> ls: cannot access 'dokima/github_rendering.json': No such file or directory
> E           AssertionError: 456.1: dokima/roles/planner.md never tells the agent to write code as markdown code
> E           assert []
> E       AssertionError: 456.2: the card does not show this code as written: ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       assert not ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       AssertionError: 456.2: the run comment does not show this code as written: ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       assert not ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       AssertionError: 456.3: as GitHub renders the card, this code does not show as written (it shows ['a &lt; b &amp;&amp; c &gt; d', '&lt;T&gt; &amp; U', "if a &lt; b &amp;&amp; c &gt; d:\n    print('&lt;ok&gt; &amp; done')\n", '&lt;b&gt;', 'dokima/&lt;name&gt;.py']): ['a < b && c > d', '<T> & U
> E       assert not ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       AssertionError: 456.3: as GitHub renders a run comment, this code does not show as written (it shows ['dokima/&lt;name&gt;.py', 'a &lt; b &amp;&amp; c &gt; d', "pytest -k '&lt;x&gt;'", "if a &lt; b &amp;&amp; c &gt; d: print('&lt;ok&gt; &amp; done')", '&lt;a&gt; &amp; &lt;b&gt;']): ['a < b &
> E       assert not ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       AssertionError: 456.4: the c

`9. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wm; rm -rf /tmp/wb; git worktree add -q --detach /tmp/wb HEAD; cd /tmp/wb; git -c user.name=r -c user.email=r@r merge -q --no-edit origin/main 2>&1 | tail -3; git status --short | head; 
```

> Auto-merging dokima/agent.py
> Auto-merging dokima/card.py
> Shell cwd was reset to /home/runner/work/dokima/dokima

`10. Bash`
```
cd /tmp/wb; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^(FAILED|[0-9]+ (passed|failed))" | cut -c1-300; cp dokima/github_rendering.json /tmp/gr.bak; DOKIMA_RECORD_RENDER=1 timeout 120 python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^(FAILED|E  |[0-9]+ (passed|failed))" | cut -c1-300
```

> FAILED tests/test_code_as_written.py::test_github_renders_code_on_the_card_as_written - Failed: 456.3: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_RECORD_RENDER=1 python3 
> FAILED tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html[the card] - Failed: 456.4: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_R
> FAILED tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html[the run comment] - Failed: 456.4: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with D
> 3 failed, 5 passed in 0.18s
> E       AssertionError: 456.4: as GitHub renders the card, a fence that never closes at a line start opens a code block, and an agent's <kbd>evil</kbd> after it is drawn as HTML
> E       assert not ['kbd']
> E       AssertionError: 456.4: as GitHub renders the run comment, a fence that never closes at a line start opens a code block, and an agent's <kbd>evil</kbd> after it is drawn as HTML
> E       assert not ['kbd']
> FAILED tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html[the card] - AssertionError: 456.4: as GitHub renders 

**Agent:** The new test catches the hole on GitHub's live rendering. Now checking that a fix can pass it.

`11. Bash`
```
cd /tmp/wb; grep -n "def escape\b\|def escape(\|def escape_words" -A30 dokima/card.py | head -90
```

> 244:def escape_words(line):
> 245-    """One line of an agent's words: code in backticks as written, everything else HTML-escaped.
> 246-
> 247-    Backticks pair as GitHub pairs them: a run opens a code span closed by the next run of the same length, a
> 248-    backslash before a backtick makes it plain, and a run that never closes is plain text."""
> 249-    out, i = [], 0
> 250-    while i < len(line):
> 251-        if line[i] == "\\":
> 252-            out.append(html.escape(line[i:i + 2], quote=False))
> 253-            i += 2
> 254-            continue
> 255-        if line[i] == "`":
> 256-            run = re.match(r"`+", line[i:]).group(0)
> 257-            close = re.compile(rf"(?<!`){run}(?!`)").search(line, i + len(run))
> 258-            if close:
> 259-                out.append(line[i:close.end()])
> 260-                i = close.end()
> 261-            else:
> 262-                out.append(run)
> 263-                i += len(run)
> 264-            continue
> 265-        j = i
> 266-        while j < len(line) and line[j] not in "\\`":
> 267-            j += 1
> 268-        out.append(html.escape(line[i:j], quote=False))
> 269-        i = j
> 270-    return "".join(out)
> 271-
> 272-
> 273:def escape(text, indent=""):
> 274-    """An agent's text, safe to draw: code as written, every other word HTML-escaped.
> 275-
> 276-    So its words never draw HTML. Code is a span in backticks or a fenced code block. The words go on one line; each code block keeps its lines,
> 277-    on lines of its own under `indent`, the indent of t

`12. Bash`
```
cd /tmp/wb; python3 - <<'EOF'
p='dokima/card.py'; s=open(p).read()
s=s.replace('''            out += [(indent if out else "") + escape_words(" ".join(part.split()))]''','''            w = escape_words(" ".join(part.split()))
            w = re.sub(r"^([`~])(?=\\1\\1)", lambda m: "&#96;" if m.group(1) == "`" else "&#126;", w)
            out += [(indent if out else "") + w]''')
open(p,'w').write(s)
EOF
DOKIMA_RECORD_RENDER=1 timeout 120 python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^(FAILED|E  |[0-9]+ (passed|failed))" | cut -c1-300; python3 -m pytest -q tests/test_code_as_written.py tests/test_run_comment_fields.py tests/test_card*.py 2>&1 | tail -2
```

> 8 passed in 0.54s
> ............................                                             [100%]
> 172 passed in 41.97s
> Shell cwd was reset to /home/runner/work/dokima/dokima

`13. Bash`
```
cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wb; git status --short; mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner added a test for 456.4 where a fence that never closes starts a line (the plan's summary, and the words right after a code block, with backticks and tildes), on the card and in the run comment, judged on GitHub's recorded rendering.",
          "The planner moved its recorded answers for what main writes to `tests/github_code_rendering.json`, since main now uses `tests/github_rendering.json` for its own tests."],
  "decided": ["The non-functional requirement now names the line-start case: the first words of a text drawn at a line start, or the words right after a code block."],
  "open": ["The worker still has to make `card.escape` write a line-start fence so GitHub cannot read it as one, and record GitHub's answers in `dokima/github_rendering.json`."]},
 "verdict": "approve",
 "summary": "The plan now has a test that catches an unclosed fence at a line start drawing HTML, and every test fails today on main for the missing feature.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The planner's, worker's and reviewer's prompts tell them to write code, paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.1"},
  {"ask": "Text inside backticks or a code block shows on cards and in run comments exactly as written, `<`, `>` and `&` included. Outside code they are still escaped.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.2"},
  {"ask": "As GitHub renders a card and a run comment, `<`, `>` and `&` inside code show as written, never as `&lt;`, `&gt;` or `&amp;`. Outside code they never make GitHub draw HTML. This is checked on GitHub's own rendering of what the code writes, not only on the raw text.",
```

> summary holds 28 words, over its cap of 25 (up to 30 passes)

`14. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now tests an unclosed fence at a line start, and every test fails on main for the missing feature."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 456 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for [#456](https://github.com/dokima-dev/dokima/issues/456) (code in cards and run comments shows exactly as written). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

**What the planner changed this round:** It fixed the weak test from the last code review. It added `test_a_fence_that_never_closes_at_a_line_start_draws_no_html`, which covers the card and the run comment. Each case has an unclosed ``` or ~~~ fence at the start of a line, followed by a closed code block of `<kbd>evil</kbd>`. The test then checks GitHub's rendering. It also moved its saved GitHub answers to `tests/github_code_rendering.json`, because main now uses `tests/github_rendering.json` for its own tests.

**What I checked:**
- **On main:** all 8 tests in `tests/test_code_as_written.py` fail because the feature is missing, not because of a crash or a bad path.
- **The new test catches the hole:** I merged the branch with the new main and asked GitHub to render what the worker's current code writes. The new test failed in both cases with "a fence that never closes at a line start opens a code block, and an agent's `<kbd>evil</kbd>` after it is drawn as HTML".
- **A fix can pass it:** I wrote a small fix in a throwaway copy of the repo. It makes `card.escape` write a fence at the start of a line so GitHub doesn't read it as a fence. With that fix and GitHub's answers saved, all 8 tests pass, and so do the card and run-comment suites (172 tests). The copy is deleted and nothing in the repo changed.
- **The owner's asks:** each of the four asks in the issue maps to a criterion (456.1 to 456.4). No blockers were open for me to answer.

**Still open, for the worker:**
- Change `card.escape` to make an unclosed fence at the start of a line harmless. This was blocker R3 in the last code review.
- Bring in the latest main.
- Save GitHub's answers in `dokima/github_rendering.json`.

On the branch as it stands, the two new tests fail only because those answers aren't saved yet.

The planner also reworded the non-functional requirement to name the line-start case. The owner has already spoken with `/review`, so the river may wait for `/work` before the worker starts.
