# reviewer (plan) for #456

Run: https://github.com/dokima-dev/dokima/actions/runs/38086439027

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; echo ----; cat plan.json; echo ----; cat open_blockers.json
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
> 02-reviewer-plan.json
> 03-worker.json
> 04-reviewer-pr.json
> 05-planner.json
> # Issue #456: Agents write code as markdown code, and Dokima never escapes text inside it
> 
> <!-- dokima-card -->
> <!-- dokima-linked-from: 454, 455 -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Agents write code as markdown code, and cards and run comments show `&lt;`, `&gt;` and `&amp;` inside it exactly as written.
> 
> **Plan**
> 
> https://github.com/dokima-dev/dokima/issues/456 · https://github.com/dokima-dev/dokima/pull/462 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/462/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #452, #453, #454, #455
> 
> **User story:** File paths, commands and quoted code in plans, records and cards show as code, with `&lt;`, `&gt;` and `&amp;` exactly as written, while an agent's other words still never draw HTML.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/doki

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show 97c990e --stat; git show 97c990e -- tests | head -150; cat tests/test_code_as_written.py
```

> <persisted-output>
> Output too large (45.9KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/40350af8-3d4e-4336-b279-d5d7e3f8e72c/tool-results/bdkmtgtxi.txt
> 
> Preview (first 2KB):
> commit 97c990ed5f6c7bb7708af90ba41521deab6c72f7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 21:07:36 2026 +0000
> 
>     planner for #456 (run 38086312639)
> 
>  tests/github_rendering.json   |  4 ++--
>  tests/test_code_as_written.py | 10 ++++++----
>  2 files changed, 8 insertions(+), 6 deletions(-)
> commit 97c990ed5f6c7bb7708af90ba41521deab6c72f7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 21:07:36 2026 +0000
> 
>     planner for #456 (run 38086312639)
> 
> diff --git a/tests/github_rendering.json b/tests/github_rendering.json
> index 51c5126..dd8d3aa 100644
> --- a/tests/github_rendering.json
> +++ b/tests/github_rendering.json
> @@ -5,8 +5,8 @@
>     "html": "\n<p>Run <code class=\"notranslate\">a &amp;lt; b &amp;amp;&amp;amp; c &amp;gt; d</code> first, while &lt;kbd&gt;evil&lt;/kbd&gt; &amp; &lt;img src=\"x.png\" alt=\"evil\"&gt; stays text.</p>\n<p><strong>Plan</strong></p>\n<p><a href=\"https://github.com/o/r/issues/456\">https://github.com/o/r/issues/456</a></p>\n<p><strong>User story:</strong> Owners read <code class=\"notranslate\">&amp;lt;T&amp;gt; &amp;amp; U</code> as written.</p>\n<p><a target=\"_blank\" rel=\"noopener noreferrer nofollow\" href=\"https://raw.gi

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show 97c990e -- tests/test_code_as_written.py; cat tests/test_code_as_written.py; ls tests/github_html.py; git diff origin/main --stat 2>/dev/null || git diff main --stat
```

> commit 97c990ed5f6c7bb7708af90ba41521deab6c72f7
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 21:07:36 2026 +0000
> 
>     planner for #456 (run 38086312639)
> 
> diff --git a/tests/test_code_as_written.py b/tests/test_code_as_written.py
> index 353a122..01e1aff 100644
> --- a/tests/test_code_as_written.py
> +++ b/tests/test_code_as_written.py
> @@ -56,7 +56,8 @@ TESTS = {"tests/test_a.py::test_one": {"verified_by": "The `<b>` tag & more show
>                                           "url": "https://github.com/o/r/blob/abc/tests/test_a.py#L15"}}
>  CARD_CODES = [INLINE, "<T> & U", "dokima/<name>.py", "--x <y>", "<b>"]
>  
> -BLOCKER = {"kind": "blocker", "to": "worker", "label": "456.2", "text": f"`{INLINE}` fails, while {PROSE} stays text.",
> +BLOCKER = {"kind": "blocker", "to": "worker", "label": "456.2",
> +           "text": f"`{INLINE}` fails under `pytest -k '<x>'`, while {PROSE} stays text.",
>             "evidence": f"Ran `pytest -k '<x>'` & saw {PROSE}.", "raised_by": "reviewer", "id": "R1"}
>  QUESTION = {"kind": "question", "to": "owner", "label": "Two readings",
>              "text": f"Should this run?\n```\n{BLOCK}\n```\nThe plan assumes {PROSE} stays text.",
> @@ -151,9 +152,10 @@ def test_code_on_the_card_shows_exactly_as_written_and_prose_stays_escaped(recor
>  def test_code_in_a_run_comment_shows_exactly_as_written_and_prose_stays_escaped(record_property, env):
>      """In a run comment, code is written exactly as the agent wrote it.
>  

`4. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | tail -8; rm -rf /tmp/mainwt; git worktree add -q /tmp/mainwt main 2>&1|tail -1; cp tests/test_code_as_written.py tests/github_html.py tests/github_rendering.json /tmp/mainwt/tests/; cd /tmp/mainwt; python3 -m pytest -q tests/test_code_as_written.py 2>&1 | grep -E "^E +(Assert|456|assert)|passed|failed" | head -30
```

> "dokima/github_rendering.json (an answer recorded for other text does not count). Record it with "
>                         "DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.")
> E           Failed: 456.3: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.
> 
> tests/github_html.py:68: Failed
> =========================== short test summary info ============================
> FAILED tests/test_code_as_written.py::test_github_renders_code_in_a_run_comment_as_written - Failed: 456.3: GitHub's rendering of the text the code writes now is not recorded in dokima/github_rendering.json (an answer recorded for other text does not count). Record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.
> 1 failed, 5 passed in 0.16s
> E           AssertionError: 456.1: dokima/roles/planner.md never tells the agent to write code as markdown code
> E           assert []
> E       AssertionError: 456.2: the card does not show this code as written: ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       assert not ['a < b && c > d', '<T> & U', 'dokima/<name>.py', '--x <y>', '<b>']
> E       AssertionError: 456.2: the run comment does not show this code as written: ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a> & <b>']
> E       assert not ['a < b && c > d', "pytest -k '<x>'", 'dokima/<name>.py', '<a>

`5. Bash`
```
cd /home/runner/work/dokima/dokima; python3 -m pytest -q -x --deselect tests/test_code_as_written.py::test_github_renders_code_in_a_run_comment_as_written 2>&1 | tail -3; git worktree remove --force /tmp/mainwt
```

> Command did not complete within its 120s timeout and was moved to the background (ID: bqe09d3ca). Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/40350af8-3d4e-4336-b279-d5d7e3f8e72c/tasks/bqe09d3ca.output. You will be notified when it completes. If it is still running after 10m in the background, it will be stopped and you will be notified. To check interim output, use Read on that file path.
> Session cwd remains /home/runner/work/dokima/dokima; directory changes made by the backgrounded command do not apply to subsequent commands.

`6. Bash`
```
cd /tmp/pack; head -c 1500 parent.json; echo; python3 -c "
import json;d=json.load(open('in/05-planner.json'));print(json.dumps(d.get('check'),indent=1)[:800])"
```

> {"number": 416}
> {
>  "passed": true,
>  "problems": []
> }
> Shell cwd was reset to /home/runner/work/dokima/dokima

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner moved the blocker's command `pytest -k '<x>'` from its evidence into its words, so a blocker placed under its criterion shows it.",
          "The planner recorded GitHub's answer for the run comment the main code writes with the new text in tests/github_rendering.json."],
  "decided": ["The older test for 236.4 stays unchanged: a placed blocker still hides its evidence."],
  "open": ["The worker must record GitHub's answer for the run comment its code writes now in dokima/github_rendering.json."]},
 "verdict": "approve",
 "summary": "The re-plan fixes the test that could not pass without touching the older test, and every new test fails on main because the feature is missing.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "The planner's, worker's and reviewer's prompts tell them to write code, paths, commands and quoted code as markdown code. Inline uses backticks; several lines use a code block.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "456.1"},
  {"ask": "Text inside backticks or a code block shows on cards and in run comments exactly as written, `<`, `>` and `&` included. Outside code they are still escaped.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "456.2"},
  {"ask": "As GitHub renders a card and a run comment, `<`, `>` and `&` inside code show as written, never as `&lt;`, `&gt;` or `&amp;`. Outside code they never make GitHub draw HTML. This is checked on GitHub's own rendering of what the code writes, not only on the raw text.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "456.3"},
  {"ask": "Text outside code is escaped as today, so an agent's words can never inject HTML into a card.", "source": "https://github.com/dokima-dev/dokima/issues/416", "criterion": "456.4"}
 ]}
EOF
cd /home/runner/work/dokima/dokima; python3 -m dokima.agent check revi
```

> summary holds 26 words, over its cap of 25 (up to 30 passes)

`8. Bash`
```
cd /home/runner/work/dokima/dokima; sed -i 's/"summary": "The re-plan fixes the test that could not pass without touching the older test, and every new test fails on main because the feature is missing."/"summary": "The re-plan fixes the test that could not pass, leaves the older test alone, and every new test fails on main for the missing feature."/' /tmp/dokima-out/review.json; python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 456 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** Now waiting for the branch's full test run to finish before I confirm the approval.

`9. ToolSearch`
```
{"query": "select:Monitor", "max_results": 1}
```

> 

`10. Bash`
```
f=/tmp/claude-1001/-home-runner-work-dokima-dokima/40350af8-3d4e-4336-b279-d5d7e3f8e72c/tasks/bqe09d3ca.output; until grep -qE "passed|failed|error" $f; do sleep 2; done; tail -3 $f
```

> Command running in background with ID: bt441cdh3. Output is being written to: /tmp/claude-1001/-home-runner-work-dokima-dokima/40350af8-3d4e-4336-b279-d5d7e3f8e72c/tasks/bt441cdh3.output. You will be notified when it completes. To check interim output, use Read on that file path.

**Agent:** I'm waiting for the full test run on the branch to finish. I'll come back when it does.

`11. Bash`
```
cat /tmp/claude-1001/-home-runner-work-dokima-dokima/40350af8-3d4e-4336-b279-d5d7e3f8e72c/tasks/bqe09d3ca.output
```

> .................ss.sss........................................ss....... [ 98%]
> ..........s                                                              [100%]
> 942 passed, 77 skipped, 1 deselected in 255.59s (0:04:15)
> 
> [exited with code 0]

**Agent:** I approved the plan for [#456](https://github.com/dokima-dev/dokima/issues/456) (code shows as written on cards and in run comments). The review is in `/tmp/dokima-out/review.json` and passes both hand-back checks.

**The fix to the earlier blocker works.** An older test hides the evidence of a blocker filed under its criterion (rule 236.4), and the run comment test needed the command `pytest -k '<x>'` to show there, so no code could pass both. The planner moved the command from the blocker's evidence into its words, which do show, and left the older test alone.

**Test runs:**
- **On main, with the new tests copied in:** all 6 new tests fail because the feature is missing, not because of a crash or bad path.
- **On the branch:** 5 of the 6 pass. The one that fails is the check of GitHub's rendering of a run comment, because GitHub's answer for the comment the new code writes isn't recorded yet. That's the worker's next step, and the plan says so.
- **Full suite on the branch,** leaving out that one test: 942 passed, 77 skipped, none failed.

**Owner asks:** the issue holds four asks, all quoted from [#416](https://github.com/dokima-dev/dokima/issues/416) (the parent this is story 5 of). Each one maps to a criterion, 456.1 to 456.4, and none is missing.

There were no open blockers to answer and I raised nothing new. On autopilot the worker starts next.
