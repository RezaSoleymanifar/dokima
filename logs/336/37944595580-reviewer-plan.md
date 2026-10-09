# reviewer (plan) for #336

Run: https://github.com/dokima-dev/dokima/actions/runs/37944595580

`1. Bash`
```
cd /tmp/pack; ls -la . in; cat issue.md; cat open_blockers.json; cat plan.json
```

> .:
> total 32
> drwxr-xr-x  3 runner runner 4096 Oct  9 14:30 .
> drwxrwxrwt 18 root   root   4096 Oct  9 14:30 ..
> drwxr-xr-x  2 runner runner 4096 Oct  9 14:30 in
> -rw-r--r--  1 runner runner 9278 Oct  9 14:30 issue.md
> -rw-r--r--  1 runner runner    2 Oct  9 14:30 open_blockers.json
> -rw-r--r--  1 runner runner 2802 Oct  9 14:30 plan.json
> 
> in:
> total 12
> drwxr-xr-x 2 runner runner 4096 Oct  9 14:30 .
> drwxr-xr-x 3 runner runner 4096 Oct  9 14:30 ..
> -rw-r--r-- 1 runner runner 3425 Oct  9 14:30 01-planner.json
> # Issue #336: AGENTS.md says every spec I give lands on GitHub as a comment, and an issue's text stays frozen
> 
> <!-- dokima-card -->
> <!-- dokima-blocking: {"blocked_by": [], "blocks": [], "loop": []} -->
> **Backlog**
> 
> [issue #336](https://github.com/dokima-dev/dokima/issues/336)
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubuse

`2. Bash`
```
cd /home/runner/work/dokima/dokima; cat tests/test_where_specs_go.py; python -m pytest -q tests/test_where_specs_go.py 2>&1 | tail -15; git show --stat HEAD | head
```

> """AGENTS.md tells every session, human or agent, where the owner's specs go.
> 
> Issue #336 asks for a short rule with an example in AGENTS.md: every spec, answer or scope change lands on GitHub,
> on an existing issue as a comment, an issue's original text stays frozen, and a new idea becomes a new issue. These
> tests read the `## Where specs go` section of AGENTS.md and check each promise is written there, in plain words.
> Matching ignores case, line breaks and repeated spaces, so the worker may wrap lines freely.
> """
> import os
> import re
> 
> ROOT = os.path.join(os.path.dirname(__file__), "..")
> HEADING = "## Where specs go"
> 
> 
> def section():
>     """Returns the lines of the specs section of AGENTS.md, or None when missing."""
>     lines = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read().splitlines()
>     if HEADING not in [line.strip() for line in lines]:
>         return None
>     start = [line.strip() for line in lines].index(HEADING) + 1
>     end = start
>     while end < len(lines) and not lines[end].startswith("## "):
>         end += 1
>     return lines[start:end]
> 
> 
> def flat(lines):
>     """Joins the section into one lower-case line with single spaces, so wrapping never matters."""
>     return re.sub(r"\s+", " ", " ".join(lines)).lower()
> 
> 
> def require(criterion, phrases):
>     """Fails naming the criterion and every phrase the section lacks."""
>     lines = section()
>     assert lines is not None, f"{criterion}: AGENTS.md has no section headed '{HEADING}'"
>     text = flat(lines)
>   

`3. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{"previous_step": {
  "did": ["The planner wrote five criteria for a short \"Where specs go\" section in AGENTS.md, with an example line, and one test per criterion in tests/test_where_specs_go.py."],
  "decided": ["The section has at most 12 non-empty lines and uses the owner's own words for each of the four rules.",
              "No code enforces the rule, and the role prompts and CLAUDE.md stay as they are."],
  "open": []},
 "verdict": "approve",
 "summary": "The plan turns each of the owner's four rules and the ask for a short rule with an example into its own criterion and test, and all five tests fail today because the section is missing.",
 "blockers": [],
 "notes": [
  {"text": "The example test only checks that some line starts with \"Example:\"; it cannot tell whether the example actually shows a spec landing as a comment. Code review should read the example line itself.",
   "evidence": "tests/test_where_specs_go.py::test_section_is_a_short_rule_with_an_example checks only the line prefix"},
  {"text": "\"Nobody edits it\" sits next to \"The issue body\" section, where code redraws the card above the marker. The worker should word the rule so it covers the owner's ask below the marker, as the plan's out-of-scope line says, so the two sections do not seem to contradict each other.",
   "evidence": "AGENTS.md, section \"The issue body\": code only writes above the marker"}
 ],
 "resolved": [],
 "issues_found": [],
 "asks": [
  {"ask": "Any session working on this repo, human or Claude, should know where my specs go.", "source": "https://github.com/dokima-dev/dokima/issues/336", "criterion": "1.1"},
  {"ask": "What I want in AGENTS.md, a short rule with an example", "source": "https://github.com/dokima-dev/dokima/issues/336", "criterion": "1.1"},
  {"ask": "Every spec, answer or scope change I give lands on GitHub, never only in chat.", "source": "https://github.com/dokima-dev/dokima/issue
```

> Exit code 1
> summary holds 36 words, more than 20% over its cap of 25: shorten it to 25 words or fewer
> the ask "Any session working on this repo, human or Claude, should know where my specs go." is matched to 1.1, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)
> the ask "What I want in AGENTS.md, a short rule with an example" is matched to 1.1, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)
> the ask "Every spec, answer or scope change I give lands on GitHub, never only in chat." is matched to 1.2, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)
> the ask "On an existing issue it goes in as a comment: a `/plan` comment when the planner should pick it up, a plain comment on a parked issue." is matched to 1.3, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)
> the ask "An issue's original text is frozen. Nobody edits it; changes are comments." is matched to 1.4, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)
> the ask "A new idea becomes a new issue with the spec in its body." is matched to 1.5, which is not a criterion of the plan (336.1, 336.2, 336.3, 336.4, 336.5)

`4. Bash`
```
cd /tmp/dokima-out && sed -i 's/"criterion": "1\./"criterion": "336./; s/"summary": "The plan turns.*/"summary": "Each of the owner'"'"'s asks has its own criterion and test, and all five tests fail today because the section is missing.",/' review.json && cd /home/runner/work/dokima/dokima && python3 -m dokima.agent check review /tmp/dokima-out/review.json /tmp/pack/plan.json 336 && python3 -m dokima.agent check-round reviewer /tmp/dokima-out/review.json /tmp/pack && echo OK
```

> OK

**Agent:** I approved the plan for #336. The hand-back is `/tmp/dokima-out/review.json`, and it passes both checks.

**What I checked:**
- **Your asks:** I found six in the issue and none is missing. "Any session should know where my specs go" and "a short rule with an example" both map to criterion 336.1. Your four bullets map one each to 336.2 through 336.5.
- **The tests:** I ran `tests/test_where_specs_go.py` on the branch. All five tests fail, and for the right reason: AGENTS.md has no "## Where specs go" section yet. They match on your own words, ignoring case and line wrapping, and they check the section has at most 12 non-empty lines and a line starting with "Example:".
- **Questions:** the plan asks you none, so there were no assumptions to judge.

**Two notes for later, not blockers:**
- The test only checks that some line starts with "Example:". It can't tell whether the example really shows a spec landing as a comment, so code review should read that line itself.
- The worker should word "nobody edits it" so it plainly covers your own text below the marker. AGENTS.md's "The issue body" section already lets code redraw the card above it, and the two sections shouldn't seem to contradict each other.
