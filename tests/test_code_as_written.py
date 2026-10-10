"""Agents write code as markdown code, and Dokima never escapes it (#456).

Story 5 of #416.

The agents' prompts (dokima/roles/planner.md, worker.md, reviewer.md) tell them to write code, file paths, commands and
quoted code as markdown code: backticks inline, a code block for several lines. Cards (`card.render` in dokima/card.py)
and run comments (`agent.render` in dokima/agent.py) then draw an agent's text with `<`, `>` and `&` exactly as written
inside backticks or a code block, and escaped everywhere else, so an agent's words never draw HTML.

The texts below mix code with prose that tries to draw HTML (a <kbd> element and an <img> whose alt is "evil"):

    inside code      must show as written, `<`, `>` and `&` included, never as &lt; &gt; &amp;
    outside code     must stay escaped, also after a backtick or a fence that never closes

Two kinds of proof: the raw text the code writes, and GitHub's own rendering of that text, recorded in the repo by
tests/github_html.py (an answer recorded for other text fails the test). "Visible" means a run comment without its
Full record fold, which holds the raw JSON by design.
"""
import copy
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent, card  # noqa: E402
import github_html  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
REPO = "o/r"
SRC = "https://github.com/o/r/issues/456"
INLINE = "a < b && c > d"
BLOCK = "if a < b && c > d:\n    print('<ok> & done')"
PROSE = '<kbd>evil</kbd> & <img src="x.png" alt="evil">'
PROSE_ESCAPED = '&lt;kbd&gt;evil&lt;/kbd&gt; &amp; &lt;img src="x.png" alt="evil"&gt;'
RAW_HTML = ("<kbd>", '<img src="x.png"')

PLAN = {"kind": "user_story", "summary": f"Run `{INLINE}` first, while {PROSE} stays text.",
        "user_story": "Owners read `<T> & U` as written.",
        "acceptance_criteria": [{"text": f"The check runs this:\n```\n{BLOCK}\n```\nwhile {PROSE} stays text.", "source": SRC},
                                {"text": "Paths like `dokima/<name>.py` show as written; an open ` <kbd>tick</kbd> stays text.",
                                 "source": SRC}],
        "non_functional": [{"text": "Nothing else changes.", "why": "safety", "principle": "Fail closed"}],
        "scope": ["dokima/card.py"],
        "out_of_scope": [f"The `--x <y>` flag & {PROSE}.", "An open fence\n```\n<kbd>fence</kbd>"],
        "tests": {"456.1": ["tests/test_a.py::test_one"], "456.2": ["tests/test_a.py::test_two"],
                  "456.3": ["tests/test_a.py::test_three"]},
        "test_changes": {}, "links": {"blocked_by": [], "blocks": [], "relates_to": []}, "raises": [], "answers": []}
TESTS = {"tests/test_a.py::test_one": {"verified_by": "The `<b>` tag & more show as written.",
                                       "url": "https://github.com/o/r/blob/abc/tests/test_a.py#L3"},
         "tests/test_a.py::test_two": {"verified_by": "Paths show as written.",
                                       "url": "https://github.com/o/r/blob/abc/tests/test_a.py#L9"},
         "tests/test_a.py::test_three": {"verified_by": "Nothing else changes.",
                                         "url": "https://github.com/o/r/blob/abc/tests/test_a.py#L15"}}
CARD_CODES = [INLINE, "<T> & U", "dokima/<name>.py", "--x <y>", "<b>"]

BLOCKER = {"kind": "blocker", "to": "worker", "label": "456.2", "text": f"`{INLINE}` fails, while {PROSE} stays text.",
           "evidence": f"Ran `pytest -k '<x>'` & saw {PROSE}.", "raised_by": "reviewer", "id": "R1"}
QUESTION = {"kind": "question", "to": "owner", "label": "Two readings",
            "text": f"Should this run?\n```\n{BLOCK}\n```\nThe plan assumes {PROSE} stays text.",
            "evidence": "The issue names `<a> & <b>` only.", "raised_by": "reviewer", "id": "R2"}
REVIEW = {"verdict": "block", "summary": "Two proofs are weak.", "raises": [BLOCKER, QUESTION], "answers": [], "asks": []}
COMMENT_CODES = [INLINE, "pytest -k '<x>'", "dokima/<name>.py", "<a> & <b>"]
RECORD_FOLD = "<details><summary>Full record</summary>"


def rec(role, stage, handback, n=1):
    """One agent record, as the record step builds it."""
    return {"role": role, "stage": stage, "handback": copy.deepcopy(handback), "check": {"passed": True, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}", "run_id": str(n), "log": "https://g/log.md",
            "models": ["claude-opus-5-5"],
            "report": {"duration_ms": 1000, "turns": 2, "cost_usd": 0.1, "tokens_in": 950, "tokens_out": 12000}}


@pytest.fixture
def env(monkeypatch):
    """The repo and run the workflow sets, which icons and links are drawn from."""
    for k, v in {"GITHUB_REPOSITORY": REPO, "GITHUB_SERVER_URL": "https://github.com", "GITHUB_RUN_ID": "1"}.items():
        monkeypatch.setenv(k, v)


def the_card():
    """A planned issue's card whose texts hold code and prose that tries HTML."""
    found = {"recs": [rec("planner", None, PLAN, 11)], "pr": None, "check_runs": [], "reviews": [], "owners": {"boss"},
             "tests": TESTS, "worker": None, "children": []}
    return card.render(REPO, {"number": 456, "url": SRC, "state": "open", "labels": []}, found)


def the_comment():
    """A blocking code review's run comment whose blocker and question hold code."""
    return agent.render(rec("reviewer", "pr", REVIEW, 14), plan=PLAN)


def visible(comment):
    """The comment without its Full record fold."""
    return comment.split(RECORD_FOLD)[0]


def shows_block(text, criterion, where):
    """Why the code block is not in `text` as written in a fence; None when it is."""
    lines = text.splitlines()
    first, second = BLOCK.splitlines()
    for i, line in enumerate(lines[:-1]):
        indent = line[:len(line) - len(line.lstrip())]
        if line.strip() == first and lines[i + 1] == indent + second:
            before = [x.strip() for x in lines[:i]]
            if before and before[-1].startswith("```"):
                return None
    return f"{criterion}: {where} does not hold the code block's lines exactly as written inside a fence: {BLOCK!r}"


def test_every_agent_prompt_says_to_write_code_as_markdown_code(record_property):
    """The planner's, worker's and reviewer's prompts each say to write code as markdown code.

    Proves 456.1. Each prompt must hold one paragraph that names markdown code and covers code, file paths, commands and quoted
    code, with backticks inline and a code block for several lines."""
    record_property("proves", "456.1")
    for role in ("planner", "worker", "reviewer"):
        text = open(os.path.join(ROOT, "dokima", "roles", f"{role}.md")).read()
        paragraphs = re.split(r"\n\s*\n", text)
        found = [p for p in paragraphs if "markdown code" in p.lower()]
        assert found, f"456.1: dokima/roles/{role}.md never tells the agent to write code as markdown code"
        need = {"backticks inline": r"backtick", "a code block for several lines": r"code block",
                "file paths": r"\bpaths?\b", "commands": r"\bcommands?\b", "quoted code": r"quoted code",
                "several lines": r"several lines|more than one line|multi-?line"}
        best = max(found, key=lambda p: sum(bool(re.search(v, p, re.I)) for v in need.values()))
        missing = [k for k, v in need.items() if not re.search(v, best, re.I)]
        assert not missing, (f"456.1: dokima/roles/{role}.md's paragraph on markdown code does not cover: "
                             f"{', '.join(missing)}")


def test_code_on_the_card_shows_exactly_as_written_and_prose_stays_escaped(record_property, env):
    """On the card, code is written exactly as the agent wrote it.

    Proves 456.2. Draws a planned issue's card whose summary, user story, criteria, Verified by line and Out of scope hold code with
    <, > and &, and checks each code span and the code block are there as written, while the prose around them,
    which tries to draw HTML, is still escaped."""
    record_property("proves", "456.2")
    text = the_card()
    missing = [c for c in CARD_CODES if f"`{c}`" not in text]
    assert not missing, f"456.2: the card does not show this code as written: {missing}"
    problem = shows_block(text, "456.2", "the card")
    assert not problem, problem
    assert PROSE_ESCAPED in text, f"456.2: the prose around the code on the card is no longer escaped"
    raw = [h for h in RAW_HTML if h in text]
    assert not raw, f"456.2: the card writes an agent's HTML unescaped outside code: {raw}"


def test_code_in_a_run_comment_shows_exactly_as_written_and_prose_stays_escaped(record_property, env):
    """In a run comment, code is written exactly as the agent wrote it.

    Proves 456.2. Draws a code review's comment with a failing criterion, its blocker, the blocker's evidence and a question for the
    owner, all holding code with <, > and &, and checks each code span and the code block are there as written, while
    the prose around them is still escaped."""
    record_property("proves", "456.2")
    text = visible(the_comment())
    missing = [c for c in COMMENT_CODES if f"`{c}`" not in text]
    assert not missing, f"456.2: the run comment does not show this code as written: {missing}"
    problem = shows_block(text, "456.2", "the run comment")
    assert not problem, problem
    assert PROSE_ESCAPED in text, f"456.2: the prose around the code in the run comment is no longer escaped"
    raw = [h for h in RAW_HTML if h in text]
    assert not raw, f"456.2: the run comment writes an agent's HTML unescaped outside code: {raw}"


def check_rendering(text, codes, where):
    """Check GitHub shows every code in `text` as written and its prose draws no HTML."""
    seen = github_html.page(github_html.rendered(text, "456.3"))
    missing = [c for c in codes if c not in seen.codes]
    assert not missing, (f"456.3: as GitHub renders {where}, this code does not show as written "
                         f"(it shows {[c for c in seen.codes if '&' in c][:5]}): {missing}")
    assert BLOCK + "\n" in seen.codes or BLOCK in seen.codes, \
        f"456.3: as GitHub renders {where}, the code block does not show as written: {BLOCK!r}"
    drawn = [t for t, a in seen.tags if t == "kbd" or (t == "img" and a.get("alt") == "evil")]
    assert not drawn, f"456.3: as GitHub renders {where}, the agent's prose draws HTML: {drawn}"
    assert "<kbd>evil</kbd>" in "".join(seen.text), \
        f"456.3: as GitHub renders {where}, the agent's prose no longer reads as written"


def test_github_renders_code_on_the_card_as_written(record_property, env):
    """As GitHub renders the card, code shows <, > and & as written.

    Proves 456.3. The prose around it must draw no HTML. Feeds the card the code writes to GitHub's markdown rendering (its answer recorded in the repo for exactly that
    text) and reads the code elements and tags in the HTML GitHub returns."""
    record_property("proves", "456.3")
    check_rendering(the_card(), CARD_CODES, "the card")


def test_github_renders_code_in_a_run_comment_as_written(record_property, env):
    """As GitHub renders a run comment, code shows <, > and & as written.

    Proves 456.3. The prose around it must draw no HTML. Feeds the whole code review comment the code writes, Full record fold included, to GitHub's markdown rendering
    (its answer recorded in the repo for exactly that text) and reads the HTML GitHub returns."""
    record_property("proves", "456.3")
    check_rendering(the_comment(), COMMENT_CODES, "a run comment")


def test_an_agents_words_outside_code_never_draw_html(record_property, env):
    """An agent's words outside code never draw HTML, even next to unclosed code.

    Proves 456.4. The code spans around the prose must show as written; the prose between them, after an unclosed backtick and
    under an unclosed fence must be escaped, on the card and in the run comment."""
    record_property("proves", "456.4")
    text = the_card()
    assert "`dokima/<name>.py`" in text, "456.4: the code next to the prose is not shown as written on the card"
    assert "&lt;kbd&gt;tick&lt;/kbd&gt;" in text and "<kbd>tick" not in text, \
        "456.4: after a backtick that never closes, the card writes an agent's HTML unescaped"
    assert "&lt;kbd&gt;fence&lt;/kbd&gt;" in text and "<kbd>fence" not in text, \
        "456.4: under a fence that never closes, the card writes an agent's HTML unescaped"
    for where, body in (("the card", text), ("the run comment", visible(the_comment()))):
        raw = [h for h in RAW_HTML if h in body]
        assert not raw, f"456.4: {where} writes an agent's HTML unescaped outside code: {raw}"
