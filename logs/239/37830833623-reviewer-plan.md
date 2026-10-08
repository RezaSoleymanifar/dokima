# reviewer (plan) for #239

Run: https://github.com/dokima-dev/dokima/actions/runs/37830833623

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json
```

> <persisted-output>
> Output too large (41.5KB). Full output saved to: /home/runner/.claude/projects/-home-runner-work-dokima-dokima/26c518b9-fe50-4483-b18b-88f427bb5a08/tool-results/bz9f6c90a.txt
> 
> Preview (first 2KB):
> .:
> total 64
> drwxr-xr-x  3 runner runner  4096 Oct  8 19:17 .
> drwxrwxrwt 18 root   root    4096 Oct  8 19:17 ..
> drwxr-xr-x  2 runner runner  4096 Oct  8 19:17 in
> -rw-r--r--  1 runner runner 41722 Oct  8 19:17 issue.md
> -rw-r--r--  1 runner runner     2 Oct  8 19:17 open_blockers.json
> -rw-r--r--  1 runner runner  3754 Oct  8 19:17 plan.json
> 
> in:
> total 32
> drwxr-xr-x 2 runner runner 4096 Oct  8 19:17 .
> drwxr-xr-x 3 runner runner 4096 Oct  8 19:17 ..
> -rw-r--r-- 1 runner runner 3960 Oct  8 19:17 01-planner.json
> -rw-r--r-- 1 runner runner 3478 Oct  8 19:17 02-reviewer-plan.json
> -rw-r--r-- 1 runner runner 2086 Oct  8 19:17 03-worker.json
> -rw-r--r-- 1 runner runner 3223 Oct  8 19:17 04-reviewer-pr.json
> -rw-r--r-- 1 runner runner 4383 Oct  8 19:17 05-planner.json
> # Issue #239: The planner's criteria and docstrings stay short, and a little over the cap never fails a run
> 
> <!-- dokima-card -->
> The planner check holds criteria and test docstrings to the owner's word caps, and fails a plan only past 20% over.
> 
> **Review**
> 
> [PR #246](https://github.com/dokima-dev/dokima/pull/246) · [files changed](https://github.com/dokima-dev/dokima/pull/246/files)
> 
> **User story:** The owner reads one short sentence per criterion, and a plan a few words over the cap is never rejected for it.
> 
> **Ac

`2. Bash`
```
cd /tmp/pack; sed -n 1,400p issue.md | cut -c1-1500
```

> # Issue #239: The planner's criteria and docstrings stay short, and a little over the cap never fails a run
> 
> <!-- dokima-card -->
> The planner check holds criteria and test docstrings to the owner's word caps, and fails a plan only past 20% over.
> 
> **Review**
> 
> [PR #246](https://github.com/dokima-dev/dokima/pull/246) · [files changed](https://github.com/dokima-dev/dokima/pull/246/files)
> 
> **User story:** The owner reads one short sentence per criterion, and a plan a few words over the cap is never rejected for it.
> 
> **Acceptance criteria**
> 
> <table>
> <tr><td><a href="https://github.com/dokima-dev/dokima/actions/runs/37829590650/job/113491239095"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a></td><td>Each criterion of a plan or of a split's story opens with one sentence of at most 25 words, and a paragraph may follow it.<br>Verified by: <a href="https://github.com/dokima-dev/dokima/blob/9f8187768ec152dfdbe2fa1f5c68d6ebc99d91c4/tests/test_word_caps.py#L79">A criterion's first sentence is held to 25 words; a paragraph may follow it.</a></td></tr>
> <tr><td><a href="https://github.com/dokima-dev/dokima/actions/runs/37829590650/job/113491239240"><img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"></a></td><td>Each docstring the planner adds or rewrites in its tests opens with a line of at most 1

`3. Bash`
```
cd /tmp/pack; sed -n 400,900p issue.md | cut -c1-2500; cat open_blockers.json; cat plan.json
```

> ```
> 
> </details>
> 
> <sub>Opus 5.5 · 8.7 min · 23 turns · 1,363,934 tokens in, 11,814 out · $1.01 at API prices · [conversation](https://github.com/dokima-dev/dokima/blob/logs/logs/239/37828382883-worker.md) · [run](https://github.com/dokima-dev/dokima/actions/runs/37828382883)</sub>
> 
> **Next:** The reviewer starts now.
> 
> 
> ### dokima-runtime on PR #246 (2026-10-08T19:07:47Z)
> 
> <!-- dokima-record -->
> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/passed.svg" width="16" height="16" align="absmiddle" alt="passed"> The reviewer blocked the work on 1 criterion.
> 
> - **B1** (239.2, the planner fixes it): Criterion 239.2 says every docstring the planner adds, including helpers and the file's own docstring, opens with a line of at most 15 words. The check measures the docstring's literal first line, so a docstring written as three quotes, a line break, then a 30-word line counts as 0 words and is neither listed nor rejected. New tests are still caught, but only because the older one-sentence summary check rejects an empty first line; helpers and the file docstring are not. The test only writes docstrings whose text starts on the same line as the quotes, so it passes while this is still wrong.
> 
> <details><summary><b>Details</b></summary>
> 
> - All ten new tests pass, but a helper or file docstring that begins on its second line escapes the 15-word cap, and no test catches it.
> - B1 on 239.2: Criterion 239.2 says every docstring the planner adds, including helpers an

`4. Bash`
```
cd /home/runner/work/dokima/dokima; git show f719bf5 --stat; git show f719bf5 -- tests | head -150; sed -n 340,370p dokima/planner.py
```

> commit f719bf5105b712be5e541e06893337c94ec78d1c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 19:17:12 2026 +0000
> 
>     planner for #239 (run 37830572304)
> 
>  tests/test_word_caps.py | 17 +++++++++++------
>  1 file changed, 11 insertions(+), 6 deletions(-)
> commit f719bf5105b712be5e541e06893337c94ec78d1c
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 19:17:12 2026 +0000
> 
>     planner for #239 (run 37830572304)
> 
> diff --git a/tests/test_word_caps.py b/tests/test_word_caps.py
> index e98b326..9680881 100644
> --- a/tests/test_word_caps.py
> +++ b/tests/test_word_caps.py
> @@ -104,16 +104,21 @@ def test_a_docstring_the_planner_adds_is_held_to_15_words_in_its_first_line(reco
>      """Every docstring the planner adds, helpers included, opens with at most 15 words.
>  
>      Proves 239.2. Docstrings of 15 words pass unlisted. A 19-word first line is rejected by name in a new test, a
> -    helper and the module docstring; the words of the paragraph below never count.
> +    helper and the module docstring; the words of the paragraph below never count. A docstring that opens with a line
> +    break is measured by its first line of text, so a helper or module docstring written that way is held to 15 too.
>      """
>      record_property("proves", "239.2")
> -    good = jobs(id_doc=words(15), id_rest=words(40) + " Proves 9.1.", helper_doc=words(15), module_doc=words(15))
> -    rc, why, printed = run(che

`5. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 1,100p tests/test_word_caps.py; sed -n 120,140p tests/test_word_caps.py; timeout 600 python3 -m pytest -q tests/test_word_caps.py 2>&1 | tail -20
```

> """The planner check caps criteria and docstrings; a little over never fails a run.
> 
> Issue #239 (story 1 of #229). The owner set the caps: 25 words for a criterion's first sentence, 15 words for the
> first line of every docstring the planner adds in its tests. A text up to 20% over its cap (30 words for 25, 18 for 15)
> passes, and the check lists it; a text past that is rejected, naming it and its word count. Every new test's docstring
> names the criteria it proves by number, below its first line.
> 
> Every test here runs `python3 -m dokima.planner check 9 OUT` through planner.main, in the temp git repo of the `check`
> fixture of tests/test_plan_check.py (issue #9, one older test at the start, the planner's tests on top). Each test
> rewrites the planner's tests/test_jobs.py and plan.json there, runs the check, and reads back the exit code, the reason
> saved for the issue, and what the check printed.
> """
> import copy
> import os
> import subprocess
> import sys
> 
> import pytest
> 
> sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
> from tests.test_plan_check import FEATURE, STORY, check  # noqa: E402,F401
> 
> 
> def words(n, end="."):
>     """A sentence of exactly n words, ending in the given mark."""
>     return " ".join(f"w{i}" for i in range(1, n + 1)) + end
> 
> 
> ID_DOC = "A slow call returns a job id."
> UNIQUE_DOC = "Job ids never repeat."
> 
> 
> def jobs(id_doc=ID_DOC, unique_doc=UNIQUE_DOC, id_rest="Proves 9.1.", unique_rest="Proves 9.2 and 9.3.",
>          helper_doc=None, module_doc=None):
>  

**Agent:** Checking the plan's revised 239.2 test: it fails on the branch for the right reason; now confirming the worker's fix would make it pass.

`6. Bash`
```
cd /home/runner/work/dokima/dokima; rm -rf /tmp/wt; git worktree add -q /tmp/wt HEAD && cd /tmp/wt && python3 - <<'E'
p='dokima/planner.py';s=open(p).read()
s=s.replace('out[name] = doc.split("\\n")[0].strip()','out[name] = next((l.strip() for l in doc.split("\\n") if l.strip()), "")')
open(p,'w').write(s)
E
git diff --stat; timeout 900 python3 -m pytest -q tests/test_word_caps.py tests/test_new_test_check.py 2>&1 | tail -3; cd /home/runner/work/dokima/dokima; git worktree remove --force /tmp/wt
```

> dokima/planner.py | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> .........................                                                [100%]
> 25 passed in 27.30s

`7. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'E'
{"previous_step": {
  "did": ["The planner added cases to the 239.2 test where a helper and the file's own docstring start with a line break, then a 19-word line, and expects each rejected by name with '19 words'.",
          "It added a matching good case: the same shape with a 15-word line and a 40-word paragraph must pass unlisted."],
  "decided": ["A docstring that opens with a line break is measured by its first line of text."],
  "open": ["The plan has no questions for the owner."]},
 "verdict": "approve",
 "summary": "The revised plan now tests helper and file docstrings that start on their second line; that test fails on the branch today for exactly that reason, and passes once the first line of text is measured.",
 "blockers": [],
 "notes": [{"text": "The code review's B1 is answered by the plan: the 239.2 test fails on the current branch because make_job's 19-word second-line docstring is accepted, and all 25 tests in test_word_caps.py and test_new_test_check.py pass once planner.docstrings measures the first non-blank line.",
            "evidence": "python3 -m pytest -q tests/test_word_caps.py: 1 failed (239.2: tests/test_jobs.py::make_job with a 19-word docstring first line was accepted), 9 passed; with dokima/planner.py:356 changed to the first non-blank line in a throwaway copy: 25 passed."}],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Each criterion opens with one sentence of at most 25 words, and a paragraph may follow it.", "source": "https://github.com/dokima-dev/dokima/issues/239", "criterion": "239.1"},
  {"ask": "Each docstring the planner adds opens with a line of at most 15 words.", "source": "https://github.com/dokima-dev/dokima/issues/239", "criterion": "239.2"},
  {"ask": "Each new test's docstring names the criterion it proves by its number.", "source": "https://github.com/dokima-dev/dokima/issues/239", "criterion": "239.3"},
  {"ask": "A plan whose texts a
```

> rc=0

**Agent:** I approved the revised plan for #239. My review is in `/tmp/dokima-out/review.json`, and both hand-back checks pass.

- **What the planner changed:** The test for 239.2 now covers the gap the code review blocked on (B1). A helper or file docstring that starts with a line break and then has a 19-word line must be rejected by name, with "19 words". The same layout with a 15-word line and a 40-word paragraph below it must pass without being listed.
- **Fails today for the right reason:** On this branch, the 239.2 test fails because `make_job`'s 19-word docstring is accepted. The other 9 tests in `tests/test_word_caps.py` pass.
- **The fix it expects works:** In a throwaway copy, I changed `dokima/planner.py:356` to measure the docstring's first line that isn't blank. With that change, all 25 tests in `tests/test_word_caps.py` and `tests/test_new_test_check.py` pass. The copy is deleted, and I changed no files in the repo.
- **Nothing dropped:** All five of the owner's asks are still covered, one each by criteria 239.1 to 239.5. There are no open blockers at the plan stage and no questions for the owner.

Next, the worker needs to make that one-line change so the review on PR #246 can clear.
