# reviewer (plan) for #477

Run: https://github.com/dokima-dev/dokima/actions/runs/38094041750

`1. Bash`
```
cd /tmp/pack; ls -R; cat issue.md; cat open_blockers.json; cat plan.json
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
> # Issue #477: Code shows as code, never escaped
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> Code that agents write shows on cards and run comments exactly as written, never escaped.
> 
> **Review**
> 
> https://github.com/dokima-dev/dokima/pull/488 · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/files-changed.svg" width="16" height="16" align="absmiddle" alt="files changed"> [files changed](https://github.com/dokima-dev/dokima/pull/488/files)
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/related.svg" width="16" height="16" align="absmiddle" alt="related"> **Relates to:** #460, #470
> 
> **User story:** Code, file paths and commands in what agents write show as code, with &lt;, &gt; and &amp; exactly as typed.
> 
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/acceptance-criterion.svg" width="16" height="16" align="absmiddle" alt="acceptance criterion"> **Acceptance criteria**
> 
> - <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> **<a href="https://github.com/dokima-dev/dokima/actions/runs/38093223314/job/114333760655">Acceptance criterion</a>:** Code in backticks or in a code block shows its &lt;, &

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git log --stat -3 | head -40; cat tests/test_code_unescaped.py; python -m pytest -q tests/test_code_unescaped.py 2>&1 | tail -30
```

> commit 58869fbe74060e37b41612ace373d0e6bce9b16d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 23:09:23 2026 +0000
> 
>     planner for #477 (run 38093659340)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  tests/test_code_unescaped.py | 53 ++++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 53 insertions(+)
> 
> commit 92db70bad74fe09e55d6b938d1e3ebe4ee4256e5
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 22:55:40 2026 +0000
> 
>     worker for #477 (run 38093114054)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  dokima/card.py           | 29 ++++++++++++++++++++++++++++-
>  dokima/roles/planner.md  |  5 +++++
>  dokima/roles/reviewer.md |  5 +++++
>  dokima/roles/worker.md   |  5 +++++
>  4 files changed, 43 insertions(+), 1 deletion(-)
> 
> commit 177070079aabfe1d66ef6baca7568ea472653ee2
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Sat Oct 10 22:51:50 2026 +0000
> 
>     planner for #477 (run 38092603948)
>     
>     Co-authored-by: Reza Soleymanifar <34189616+RezaSoleymanifar@users.noreply.github.com>
> 
>  tests/test_code_unescaped.py | 163 +++++++++++++++++++++++++++++++++++++++++++
>  1 file changed, 163 insertions(+)
> """Code an agent writes shows as code: Dokima never escapes text inside markdown code (#477).
> 
> The owner: "Agents write c

`3. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_code_unescaped.py 2>&1 | grep -E "^E .*477|FAILED"; cat /tmp/pack/in/04-reviewer-pr.json | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps(d.get('handback',d).get('raises'),indent=1)[:1500])"; cat /tmp/pack/parent.json | head -c 600
```

> E           AssertionError: 477.2: 'Run `a\n\n<img src=x>` now' should come back 'Run `a\n\n&lt;img src=x&gt;` now', escaped outside GitHub's code and as written in it; got 'Run `a\n\n<img src=x>` now'
> E           AssertionError: 477.2: the card draws an agent's <img> from 'Run `a\n\n<img src=x>` now':
> FAILED tests/test_code_unescaped.py::test_no_span_across_blank_line_or_after_backslash - AssertionError: 477.2: 'Run `a\n\n<img src=x>` now' should come back 'Run `a\n\n&lt;img src=x&gt;` now', escaped outside GitHub's code and as written in it; got 'Run `a\n\n<img src=x>` now'
> FAILED tests/test_code_unescaped.py::test_card_escapes_html_outside_github_code - AssertionError: 477.2: the card draws an agent's <img> from 'Run `a\n\n<img src=x>` now':
> [
>  {
>   "kind": "blocker",
>   "to": "planner",
>   "label": "Weak test",
>   "text": "The tests for 477.2 pass while an agent's `<img>` still draws on the issue card. Dokima treats two things as code that GitHub does not: (1) a pair of backticks with a blank line between them, because GitHub never lets code cross a blank line, so the `<img src=x>` on the line after it is real HTML; (2) a backtick written as \\` (backslash, then backtick), which GitHub shows as a plain backtick and never treats as the start of code. Both were escaped on main. Smallest fix: add tests to `tests/test_code_unescaped.py` that `card.escape` still escapes `<img src=x>` in `Run `a` + blank line + `<img src=x>` now` and in `Run \\`<img src=x>\\` now`, and that the car

`4. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {"did": ["The planner added tests that an agent's `<img>` stays escaped after backticks split by a blank line, or a line of spaces, and between backslash-backticks, both in `card.escape` and on the drawn issue card.", "The planner added a test that real code across one line break, ending in a backslash, or after an escaped backslash still shows as written."], "decided": ["Code follows GitHub's own reading: a code span never crosses a blank line, and a backtick after a backslash opens no code."], "open": ["The worker still has to make `card.escape` follow those rules; the two new tests for 477.2 fail on the branch today."]},
 "verdict": "approve",
 "summary": "The plan now proves that an agent's HTML stays escaped where GitHub does not read code, with matching tests that real code still shows as written, and the two new tests fail today for the missing behavior.",
 "raises": [],
 "answers": [],
 "asks": [
  {"ask": "Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for several lines)", "source": "https://github.com/dokima-dev/dokima/issues/477", "criterion": "477.3"},
  {"ask": "Dokima never escapes text inside code, so `<`, `>` and `&` show as written.", "source": "https://github.com/dokima-dev/dokima/issues/477", "criterion": "477.1"}
 ]}
EOF
cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 477 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack
```

> Exit code 1
> summary holds 37 words, more than 20% over its cap of 25: shorten it to 25 words or fewer

`5. Bash`
```
python3 - <<'EOF'
import json;p='/tmp/dokima-out/review.json';d=json.load(open(p))
d["summary"]="The plan now proves an agent's HTML stays escaped where GitHub reads no code, and the two new tests fail today for the missing behavior."
json.dump(d,open(p,'w'),indent=1)
EOF
python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 477 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the revised plan for [#477](https://github.com/dokima-dev/dokima/issues/477) (code shows as code, never escaped). The hand-back is in `/tmp/dokima-out/review.json` and passes both checks.

- **The earlier blocker is fixed.** The code review on [#488](https://github.com/dokima-dev/dokima/pull/488) (the pull request for this issue) found that an agent's `<img>` could still draw on the card in two cases. One is backticks with a blank line between them. The other is backticks written after a backslash. The planner added two tests for 477.2 that check the `<img>` stays escaped in both cases, both in `card.escape` and on the drawn issue card. They also cover a line holding only spaces.
- **The new tests fail for the right reason.** On the branch, both fail because `escape` returns `<img src=x>` unchanged. The other 10 tests pass.
- **The fix can't overshoot.** A separate test checks that real code still shows as written: code across one line break, code ending in a backslash, and a backtick after an escaped backslash. Escaping everything would fail it.
- **Nothing the owner asked for is missing.** Both of the owner's asks map to criteria (477.3 and 477.1), no blockers were open for me to answer, and I raised nothing new.

The worker is next: `card.escape` still needs to follow those two rules before the new tests pass.
