# reviewer (plan) for #456

Run: https://github.com/dokima-dev/dokima/actions/runs/38090358092

`1. Bash`
```
cd /tmp/pack; ls -la in; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
```

> <persisted-output>
> Output too large (52.3KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b7b101f7-7dd7-484a-9bec-fee00d90c489/tool-results/ba56w6hn3.txt
> 
> Preview (first 2KB):
> total 84
> drwxr-xr-x 2 runner runner 4096 Oct 10 22:09 .
> drwxr-xr-x 3 runner runner 4096 Oct 10 22:09 ..
> -rw-r--r-- 1 runner runner 4373 Oct 10 22:09 01-planner.json
> -rw-r--r-- 1 runner runner 3150 Oct 10 22:09 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 3661 Oct 10 22:09 03-worker.json
> -rw-r--r-- 1 runner runner 3099 Oct 10 22:09 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4965 Oct 10 22:09 05-planner.json
> -rw-r--r-- 1 runner runner 2527 Oct 10 22:09 06-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2530 Oct 10 22:09 07-worker.json
> -rw-r--r-- 1 runner runner 4456 Oct 10 22:09 08-reviewer-pr.json
> -rw-r--r-- 1 runner runner  358 Oct 10 22:09 09-updater.json
> -rw-r--r-- 1 runner runner 4931 Oct 10 22:09 10-planner.json
> -rw-r--r-- 1 runner runner 2752 Oct 10 22:09 11-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2588 Oct 10 22:09 12-worker.json
> -rw-r--r-- 1 runner runner 3674 Oct 10 22:09 13-reviewer-pr.json
> -rw-r--r-- 1 runner runner 5111 Oct 10 22:09 14-planner.json
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&

`2. Bash`
```
cd /tmp/pack; sed -n '/Original issue/,$p' issue.md | head -300
```

> <details><summary>Original issue</summary>
> 
> <!-- dokima-card -->
> <!-- /dokima-card -->
> 
> <details open><summary>From the approved plan of #416, story 5</summary>
> 
> **Part of:** #416 Card links show as GitHub's own references: no self-link on the issue, full address after Closes
> 
> **User story:** File paths, commands and quoted code in plans, records and cards show as code, with `<`, `>` and `&` exactly as written.
> 
> **Context:** `escape` in `dokima/card.py` HTML-escapes every agent text, code spans included, so `a < b` written as code shows as `a &lt; b`. The role prompts in `dokima/roles/` (planner.md, worker.md, reviewer.md) say nothing about writing code as markdown code; the owner's ask names agents, so it explicitly asks for a prompt change there (AGENTS.md: dokima/roles/ changes only when the issue asks). Run comments draw the same texts through `dokima/agent.py`. The check against GitHub's real rendering feeds what the code writes to GitHub's markdown rendering (its markdown API, or its answers recorded in the repo with a script that refreshes them; see the open question) and reads the HTML GitHub returns; an answer recorded for different text fails the test rather than passing it.
> 
> **Acceptance criteria:**
> - The planner's, worker's and reviewer's prompts tell them to write code, paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block. ([source](https://github.com/dokima-dev/dokima/issues/416))
> - Text inside backticks or a co

`3. Bash`
```
cd /tmp/pack; sed -n '/2026-10-10T21:21:43Z/,$p' issue.md | sed -n '20,400p'; echo ----; cat open_blockers.json
```

> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/planner.svg" width="16" height="16" align="absmiddle" alt="planner"> The planner planned this issue.
> 
> **Raised earlier:**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/blocker.svg" width="16" height="16" align="absmiddle" alt="blocker"> **Weak test for 456.4:** The test for the non-functional requirement only puts an unclosed fence in the middle of a line, where GitHub never opens a code block. An unclosed fence at the start of a line, such as a plan summary that is just ```` ``` open ````, passes the test while GitHub draws an agent's `&lt;kbd&gt;` as HTML. Smallest fix: add a case to `tests/test_code_as_written.py::test_an_agents_words_outside_code_never_draw_html` where an agent text starts with an unclosed fence (backticks and tildes) and a later text on the same card or run comment holds a code block with `&lt;kbd&gt;evil&lt;/kbd&gt;`, and check GitHub's recorded rendering draws no `kbd`. · for the planner
>   - Done: Added `tests/test_code_as_written.py::test_a_fence_that_never_closes_at_a_line_start_draws_no_html`, on the card and in the run comment: the plan's summary is just ``` open, and words right after a code block are ``` open and ~~~ open (backticks and tildes), with later closed c

`4. Bash`
```
cd /tmp/pack; cat plan.json; cat in/14-planner.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps({k:v for k,v in d.items() if k!='plan'},indent=1)[:4000])"; cd /home/runner/work/dokima/dokima; git show --stat HEAD
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
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_code_as_written.py; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | tail -30
```

> commit cae0a706fc9e379744a82b6a0af7e518a7bebe9f
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 22:09:13 2026 +0000
> 
>     planner for #456 (run 38090215622)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
> diff --git a/tests/test_code_as_written.py b/tests/test_code_as_written.py
> index 95e9123..dfe2bb6 100644
> --- a/tests/test_code_as_written.py
> +++ b/tests/test_code_as_written.py
> @@ -255,3 +255,41 @@ def test_a_fence_that_never_closes_at_a_line_start_draws_no_html(record_property
>      for fence in (OPEN_TICKS, OPEN_TILDES):
>          assert fence in words, (f"456.4: as GitHub renders {where}, the unclosed fence {fence!r} does not read as "
>                                  "plain words")
> +
> +
> +# A backtick an agent writes where GitHub never pairs it with the next one: inside a link's address, which GitHub reads
> +# first, and in a raise's label, drawn on the same line as its words. Code must not take either for the start of code
> +# and leave the HTML after it unescaped.
> +LINK_TEXT = f"See [the log](run`x) {EVIL} `"
> +TICK_LABEL, TICK_WORDS = "`", f"` {EVIL} `"
> +TICK_RAISE = {"kind": "question", "to": "owner", "label": TICK_LABEL, "text": TICK_WORDS,
> +              "evidence": "Seen.", "raised_by": "planner", "id": "P1"}
> +BARE_PLAN = {**PLAN, "user_story": "Owners read words.", "out_of_scope": ["Nothing."],
> +             "acceptance_criteria": [{"text": "Words show.", "source": SR

**Agent:** I'm checking the plan for #456 (code shown as written): the 4 new tests fail today for the right reason. Next I'm checking where GitHub's recorded answers are read from.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; grep -n "json\|def rendered\|def page" tests/github_html.py | head -40; ls dokima/github_rendering.json tests/github_*.json; python3 -c "import json;d=json.load(open('tests/github_code_rendering.json'));print(type(d), len(d))"
```

> 6:recorded once in dokima/github_rendering.json, as {"answers": [{"text": ..., "html": ...}, ...]}, and read back here.
> 7:tests/github_code_rendering.json holds answers the planner recorded for what the code wrote before the work, in the same
> 22:import json
> 30:ANSWERS = os.path.join(ROOT, "dokima", "github_rendering.json")
> 31:PLANNED = os.path.join(ROOT, "tests", "github_code_rendering.json")
> 36:    req = urllib.request.Request("https://api.github.com/markdown", data=json.dumps({"text": text, "mode": "gfm"}).encode(),
> 37:                                 headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"})
> 48:    return json.load(open(path)).get("answers") or []
> 54:        json.dump({"answers": sorted(answers, key=lambda a: a["text"])}, f, indent=1, ensure_ascii=False)
> 58:def rendered(text, criterion):
> 69:                    "dokima/github_rendering.json (an answer recorded for other text does not count). Record it with "
> 99:def page(html_text):
> dokima/github_rendering.json
> tests/github_code_rendering.json
> tests/github_rendering.json
> <class 'dict'> 1

`7. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,100p tests/github_html.py; git diff HEAD~1 HEAD -- tests/github_code_rendering.json | head -40
```

> <persisted-output>
> Output too large (67KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/b7b101f7-7dd7-484a-9bec-fee00d90c489/tool-results/blfo3vvfy.txt
> 
> Preview (first 2KB):
> """GitHub's own rendering of markdown, recorded in the repo for the tests.
> 
> Tests use it to check how GitHub shows what code writes.
> 
> Tests run in CI with no network and no secrets, so GitHub's answers from its markdown API (POST /markdown, gfm) are
> recorded once in dokima/github_rendering.json, as {"answers": [{"text": ..., "html": ...}, ...]}, and read back here.
> tests/github_code_rendering.json holds answers the planner recorded for what the code wrote before the work, in the same
> shape, so a test can show it fails today for the right reason on GitHub's real rendering.
> An answer counts only for the exact text it was recorded for: when the code writes anything else, the test fails and
> says how to record GitHub's answer for the new text, so a stale answer never passes.
> 
>     DOKIMA_RECORD_RENDER=1 python3 -m pytest tests/test_code_as_written.py   records GitHub's answer for every text
>                                                                               a test asks about and has no answer for
>     python3 tests/github_html.py                                              asks GitHub again for every recorded
>                                                                               text and rewrites its answer
>     DOKIMA_LIVE_RENDER=1 python3 -m pytest ...  

`8. Bash`
```
cd /home/runner/work/dokima/dokima; DOKIMA_LIVE_RENDER=1 timeout 60 python3 -m pytest -q tests/test_code_as_written.py -k backtick_in_a_link 2>&1 | grep -E "Error|passed|failed" | head
```

> E       AssertionError: 456.4: as GitHub renders the card, a backtick inside a link's address lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left the words after it unescaped
> tests/test_code_as_written.py:292: AssertionError
> E       AssertionError: 456.4: as GitHub renders the card, a raise's label that opens a backtick lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left the words after it unescaped
> tests/test_code_as_written.py:292: AssertionError
> E       AssertionError: 456.4: as GitHub renders the run comment, a backtick inside a link's address lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left the words after it unescaped
> tests/test_code_as_written.py:292: AssertionError
> E       AssertionError: 456.4: as GitHub renders the run comment, a raise's label that opens a backtick lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left the words after it unescaped
> tests/test_code_as_written.py:292: AssertionError
> FAILED tests/test_code_as_written.py::test_a_backtick_in_a_link_address_or_a_raise_label_draws_no_html[the card-a backtick inside a link's address] - AssertionError: 456.4: as GitHub renders the card, a backtick inside a link's address lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left th

`9. Bash`
```
cd /home/runner/work/dokima/dokima; timeout 600 python3 -m pytest -q -x -p no:cacheprovider 2>&1 | tail -8
```

> E       assert not ['kbd']
> 
> tests/test_code_as_written.py:292: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_code_as_written.py::test_a_backtick_in_a_link_address_or_a_raise_label_draws_no_html[the card-a backtick inside a link's address] - AssertionError: 456.4: as GitHub renders the card, a backtick inside a link's address lets an agent's <kbd>evil</kbd> draw HTML, because the code took that backtick for the start of code and left the words after it unescaped
> assert not ['kbd']
> !!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
> 1 failed, 365 passed, 33 skipped in 94.48s (0:01:34)

**Agent:** The new tests fail for the right reason, both on the recorded answers and against GitHub's live rendering. Writing the hand-back now.

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["Adds a test with four cases, on the card and in a run comment: a backtick inside a link's address, and a raise whose label is one backtick drawn on the same line as its words. It requires that GitHub draws no `<kbd>` and that `<kbd>evil</kbd>` reads as written.",
          "Records GitHub's answers for what the code writes today in `tests/github_code_rendering.json`. All four cases fail today with GitHub drawing `<kbd>`."],
  "decided": ["The non-functional requirement 456.4 now names both cases. The earlier criteria and tests are unchanged."],
  "open": ["The worker still has to fix `card.escape` for both cases, as the last code review asked."]},
 "verdict": "approve",
 "summary": "The plan now tests both ways the last code review found an agent's words could still draw HTML, and each new case fails today because the fix is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The planner's, worker's and reviewer's prompts tell them to write code, paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.1"},
  {"ask": "Text inside backticks or a code block shows on cards and in run comments exactly as written, `<`, `>` and `&` included. Outside code they are still escaped.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.2"},
  {"ask": "As GitHub renders a card and a run comment, `<`, `>` and `&` inside code show as written, never as `&lt;`, `&gt;` or `&amp;`. Outside code they never make GitHub draw HTML. This is checked on GitHub's own rendering of what the code writes, not only on the raw text.", "source": "https://github.com/dokima-dev/dokima/issues/456", "criterion": "456.3"},
  {"ask": "Text outside code is escaped as today, so an agent's words can never inject HTML into a card.", "source": "ht
```

> summary holds 29 words, over its cap of 25 (up to 30 passes)

`11. Bash`
```
cd /home/runner/work/dokima/dokima; python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now tests both ways an agent's words could still draw HTML, and each new case fails today because the fix is missing."
json.dump(d,open(p,'w'),indent=1,ensure_ascii=False)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 456 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the re-plan for [#456](https://github.com/dokima-dev/dokima/issues/456) (code shown exactly as written on cards and run comments). The hand-back is in `/tmp/dokima-out/review.json` and passed both checks.

**What the planner changed:** The last code review found two ways an agent's words still make GitHub draw HTML. One is a backtick inside a link's address. The other is a lone backtick in a raise's label, which sits on the same line as the raise's words. The planner added a test, `test_a_backtick_in_a_link_address_or_a_raise_label_draws_no_html`, that checks both cases on the card and in the run comment. It also widened the no-HTML requirement (456.4) to name these cases. The other criteria and tests are unchanged.

**What I checked:**
- **New test fails for the right reason:** all 4 cases fail today because GitHub draws `<kbd>`, not because of a crash or a bad path. The 8 earlier tests in that file still pass.
- **Recorded answers match GitHub:** I also ran the new test against GitHub's live rendering, and the planner's recorded answers matched.
- **Can't pass with a sloppy fix:** the test requires the agent's `<kbd>evil</kbd>` to read as plain words. If a fix broke real code instead, the existing tests for 456.2 and 456.3 would fail.
- **Owner's asks:** each of the four asks in the issue maps to a criterion, 456.1 to 456.4. Your only comments on the issue were `/review`, so there were no new asks to check.
- **Full test suite:** with stop-at-first-failure on, 365 tests passed and 33 were skipped before it stopped at the first new case. The rest of the suite did not run after that.

There were no open blockers to answer and I raised nothing. The worker still has to fix the code for both cases, as the last code review asked.
