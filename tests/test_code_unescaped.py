"""Code an agent writes shows as code: Dokima never escapes text inside markdown code (#477).

The owner: "Agents write code, file paths, commands and quoted code as markdown code (backticks, or a code block for
several lines), and Dokima never escapes text inside code, so `<`, `>` and `&` show as written."

Why: inside backticks GitHub shows text literally, so an escaped `&lt;` inside a code span reaches the owner as the
five characters `&lt;` instead of `<`. Outside code, the same characters must still be escaped, so an agent's
`<kbd>` or `<img>` in plain words never draws HTML.

What these tests pin, so the worker knows the shape:
- `dokima.card.escape(text)` is the one escape for agent text. Inside a code span (a run of N backticks closed by a
  run of exactly N backticks, as GitHub reads it) and inside a fenced code block (a line opening with ``` closed by a
  line opening with ```), it changes nothing. Everywhere else it escapes `&`, `<` and `>` as today.
- A backtick with no closing run opens no code span, so the text after it is still escaped.
- As on GitHub, a code span never crosses a blank line (a line holding only spaces counts), though it may cross one
  line break; and a backtick written after a backslash (\\`) is a plain backtick that opens no code span. Inside a
  code span a backslash is plain text, so `C:\\` is a whole code span, and a backslash that is itself escaped
  (\\\\`) leaves the backtick after it free to open one.
- The issue card (`card.render`) and a run comment (`agent.render`) draw agent text through it: a criterion's text,
  an out-of-scope line, a raise's words and its evidence.
- The planner, worker and reviewer prompts (`dokima/roles/*.md`) each hold one section headed "# Code in text" that
  tells the agent to write code, file paths, commands and quoted code as markdown code: backticks, or a code block
  for several lines.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import agent, card  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = "o/r"
ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40"}
ASK = "https://github.com/o/r/issues/40"
CODE = "`if a < b && c > d: run('<kbd>')`"


def plan_with(criterion, out_of_scope):
    """A small approved-looking plan whose first criterion and only out-of-scope line are the given words."""
    return {"kind": "user_story", "summary": "Owners see one card.", "user_story": "Owners see one card on every issue.",
            "acceptance_criteria": [{"text": criterion, "source": ASK}],
            "non_functional": [], "scope": ["dokima/card.py"], "out_of_scope": [out_of_scope],
            "tests": {"40.1": ["tests/test_a.py::test_one"]}, "test_changes": {}}


def rec(role, stage=None, n=1, **handback):
    """One agent record, as dokima.agent.records reads it from a bot comment."""
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}"}


def draw(criterion, out_of_scope):
    """The issue card for a plan with the given criterion and out-of-scope words."""
    found = {"recs": [rec("planner", n=11, **plan_with(criterion, out_of_scope))], "pr": None, "check_runs": [],
             "reviews": [], "owners": {"boss"}, "tests": {}, "worker": None, "children": []}
    return card.render(REPO, ISSUE, found)


def line_with(text, words):
    """The one line of `text` holding `words`; fails naming them when none does."""
    found = [ln for ln in text.splitlines() if words in ln]
    assert found, f"no line holds {words!r} in:\n{text}"
    return found[0]


def test_code_span_kept_as_written(record_property):
    """Code in backticks keeps its <, > and & as written.

    Escapes a sentence holding a one-backtick span, a two-backtick span with a backtick inside, and a span right at
    the start and end of the text, and checks each span comes back character for character. Proves 477.1."""
    record_property("proves", "477.1")
    cases = [f"Run {CODE} first.",
             "Use ``a < `b` & c`` here.",
             "`<b>` & `x>y`"]
    for text in cases:
        got = card.escape(text)
        for span in re.findall(r"(`+)(.+?)\1", text):
            whole = span[0] + span[1] + span[0]
            assert whole in got, f"477.1: the code {whole!r} was escaped to {got!r}"


def test_code_block_kept_as_written(record_property):
    """A code block of several lines keeps its <, > and & as written.

    Escapes text holding a fenced code block and checks every line inside the fence comes back unchanged, while the
    plain line above it is still escaped. Proves 477.1."""
    record_property("proves", "477.1")
    block = ["```python", "if a < b and c > d:", "    print('&amp; <kbd>x</kbd>')", "```"]
    text = "\n".join(["Call it like <this>:", *block, "Done."])
    got = card.escape(text).splitlines()
    for ln in block:
        assert ln in got, f"477.1: the code block line {ln!r} was changed; got:\n" + "\n".join(got)
    assert got[0] == "Call it like &lt;this&gt;:", f"477.1: the plain line above the block was not escaped: {got[0]!r}"


def test_card_shows_code_as_written(record_property):
    """On the issue card, a criterion and an out-of-scope line show their code as written.

    Draws the card for a plan whose criterion and out-of-scope line each hold code in backticks with <, > and &,
    and checks the card's line for each holds that code character for character, with no &lt;, &gt; or &amp;. Proves 477.1."""
    record_property("proves", "477.1")
    text = draw(f"The check runs {CODE} on every push", f"Changing {CODE} itself")
    for words in ("The check runs", "Changing"):
        ln = line_with(text, words)
        assert CODE in ln, f"477.1: the card shows the code escaped: {ln!r}"


def test_run_comment_shows_code_as_written(record_property, monkeypatch):
    """In a run comment, a raise's words and evidence show their code as written.

    Draws a plan review that raises a blocker whose words and evidence hold code in backticks with <, > and &, and
    checks the comment's raise line and evidence line each hold that code character for character. Proves 477.1."""
    record_property("proves", "477.1")
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
    raise_ = {"kind": "question", "to": "owner", "label": "Two readings",
              "text": f"Should the check run {CODE} too?", "evidence": f"dokima/x.py calls {CODE} today."}
    r = rec("reviewer", "plan", n=12, verdict="approve", summary="Looks right.", raises=[raise_], answers=[])
    out = agent.render(r)
    record = out.split("<details", 1)[0] if "<details" in out else out
    for words in ("Should the check run", "Evidence:"):
        ln = line_with(record, words)
        assert CODE in ln, f"477.1: the run comment shows the code escaped: {ln!r}"


def test_plain_words_still_escaped(record_property):
    """Outside code, <, > and & are still escaped, so an agent's HTML never draws.

    Escapes plain words holding a kbd tag and an ampersand, words beside a code span, and words after a lone
    backtick that opens no code span, and checks each is escaped exactly as before. Proves 477.2."""
    record_property("proves", "477.2")
    assert card.escape("Press <kbd>Enter</kbd> & go") == "Press &lt;kbd&gt;Enter&lt;/kbd&gt; &amp; go", \
        "477.2: plain words were not escaped"
    assert card.escape("<img src=x> then `a<b`") == "&lt;img src=x&gt; then `a<b`", \
        "477.2: the words beside a code span were not escaped, or the span was"
    assert card.escape("A lone ` then <b>bold</b>") == "A lone ` then &lt;b&gt;bold&lt;/b&gt;", \
        "477.2: a lone backtick turned escaping off for the rest of the text"
    assert card.escape("``a<b` then <i>") == "``a&lt;b` then &lt;i&gt;", \
        "477.2: a backtick run closed only by a shorter one opened a code span"


def test_card_still_escapes_plain_words(record_property):
    """On the issue card, plain words keep HTML as text beside code shown as written.

    Draws the card for a criterion with a kbd tag outside any code and code in backticks after it, and checks the
    card's line holds the tag escaped and the code character for character. Proves 477.2."""
    record_property("proves", "477.2")
    ln = line_with(draw(f"Press <kbd>Enter</kbd> to run {CODE}", "Nothing else"), "Press")
    assert f"Press &lt;kbd&gt;Enter&lt;/kbd&gt; to run {CODE}" in ln, \
        f"477.2: the card drew an agent's HTML, or escaped its code: {ln!r}"


def test_span_rules_follow_github(record_property):
    """Code across a line break, or ending in a backslash, keeps its <, >, &.

    GitHub lets a code span cross one line break, reads a backslash inside a span as plain text, and lets a backtick
    after an escaped backslash open a span. Escapes one text of each kind and checks it comes back as GitHub shows it.
    Proves 477.1."""
    record_property("proves", "477.1")
    cases = {"Run `a\n<b>` now": "Run `a\n<b>` now",
             "Path `C:\\` & `<b>`": "Path `C:\\` &amp; `<b>`",
             "Odd \\\\`<b>` & c": "Odd \\\\`<b>` &amp; c"}
    for text, want in cases.items():
        got = card.escape(text)
        assert got == want, f"477.1: {text!r} should show as GitHub reads it, {want!r}, but came back {got!r}"


def test_no_span_across_blank_line_or_after_backslash(record_property):
    """Backticks GitHub does not read as code never stop an agent's HTML being escaped.

    Escapes a pair of backticks with a blank line between them (and one with a line of spaces between them), and a
    pair written as backslash-backtick, and checks the <img> in each is still escaped exactly as on main. Beside each,
    the nearest real code (a span across one line break, a span ending in a backslash) keeps its <b> as written, so
    escaping everything does not pass. Proves 477.2."""
    record_property("proves", "477.2")
    cases = {"Run `a\n<b>` now": "Run `a\n<b>` now",
             "Path `C:\\` & `<b>`": "Path `C:\\` &amp; `<b>`",
             "Run `a\n\n<img src=x>` now": "Run `a\n\n&lt;img src=x&gt;` now",
             "Run `a\n  \n<img src=x>` now": "Run `a\n  \n&lt;img src=x&gt;` now",
             "Run \\`<img src=x>\\` now": "Run \\`&lt;img src=x&gt;\\` now"}
    for text, want in cases.items():
        got = card.escape(text)
        assert got == want, f"477.2: {text!r} should come back {want!r}, escaped outside GitHub's code and as written in it; got {got!r}"


def test_card_escapes_html_outside_github_code(record_property):
    """On the issue card, an <img> outside GitHub's code shows as text.

    Draws the card for a criterion whose <img> sits after backticks split by a blank line, and one whose <img> sits
    between backslash-backticks, and checks the card never holds the raw tag and shows it escaped. Beside them, a
    criterion with real code across one line break shows its <b> as written, so escaping everything does not pass.
    Proves 477.2."""
    record_property("proves", "477.2")
    text = draw("Run `a\n<b>` now", "Nothing else")
    assert "<b>` now" in text, f"477.2: the card escaped real code that crosses one line break:\n{text}"
    for criterion in ("Run `a\n\n<img src=x>` now", "Run \\`<img src=x>\\` now"):
        text = draw(criterion, "Nothing else")
        assert "<img src=x>" not in text, f"477.2: the card draws an agent's <img> from {criterion!r}:\n{text}"
        assert "&lt;img src=x&gt;" in text, f"477.2: the card lost the agent's <img> from {criterion!r}:\n{text}"


@pytest.mark.parametrize("role", ["planner", "worker", "reviewer"])
def test_prompts_ask_for_code_as_code(record_property, role):
    """Every agent is told to write code, paths, commands and quotes as markdown code.

    Reads the planner's, worker's and reviewer's prompts and checks each holds a "# Code in text" section naming code,
    file paths, commands and quoted code, backticks, and a code block for several lines. Proves 477.3."""
    record_property("proves", "477.3")
    text = open(os.path.join(ROOT, "dokima", "roles", f"{role}.md")).read()
    m = re.search(r"^# Code in text\n(.*?)(?=^# |\Z)", text, re.S | re.M)
    assert m, f"477.3: the {role} prompt has no '# Code in text' section"
    section = " ".join(m.group(1).split()).lower()
    for words in ("code", "file paths", "commands", "quoted code", "backticks", "code block", "several lines"):
        assert words in section, f"477.3: the {role} prompt's '# Code in text' section never says {words!r}"
