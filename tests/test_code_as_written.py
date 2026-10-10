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

BLOCKER = {"kind": "blocker", "to": "worker", "label": "456.2",
           "text": f"`{INLINE}` fails under `pytest -k '<x>'`, while {PROSE} stays text.",
           "evidence": f"Ran `pytest -k '<x>'` & saw {PROSE}.", "raised_by": "reviewer", "id": "R1"}
QUESTION = {"kind": "question", "to": "owner", "label": "Two readings",
            "text": f"Should this run?\n```\n{BLOCK}\n```\nThe plan assumes {PROSE} stays text.",
            "evidence": "The issue names `<a> & <b>` only.", "raised_by": "reviewer", "id": "R2"}
REVIEW = {"verdict": "block", "summary": "Two proofs are weak.", "raises": [BLOCKER, QUESTION], "answers": [], "asks": []}
COMMENT_CODES = [INLINE, "pytest -k '<x>'", "dokima/<name>.py", "<a> & <b>"]
RECORD_FOLD = "<details><summary>Full record</summary>"

# Fences that never close, each where GitHub reads a line start: a whole text drawn at the start of a line (the plan's
# summary is the card's first line) and the words right after a closed code block. A later text holds a closed code
# block of HTML; if GitHub took an unclosed fence as an opening, its pairing would shift and that HTML would be drawn.
EVIL = "<kbd>evil</kbd>"
OPEN_TICKS, OPEN_TILDES = "``` open", "~~~ open"
FENCE_PLAN = {**PLAN, "summary": OPEN_TICKS,
              "acceptance_criteria": [{"text": f"First:\n```\nok\n```\n{OPEN_TILDES}", "source": SRC},
                                      {"text": f"Then:\n```\n{EVIL}\n```", "source": SRC}],
              "out_of_scope": [f"Later:\n~~~\n{EVIL}\n~~~"]}
FENCE_REVIEW = {"verdict": "block", "summary": "One proof is weak.", "answers": [], "asks": [], "raises": [
    {"kind": "blocker", "to": "worker", "label": "456.2", "text": f"Fails:\n```\nok\n```\n{OPEN_TICKS}",
     "evidence": "Ran it.", "raised_by": "reviewer", "id": "R1"},
    {"kind": "question", "to": "owner", "label": "Two readings", "text": f"Should it?\n```\nok\n```\n{OPEN_TILDES}",
     "evidence": f"See:\n~~~\n{EVIL}\n~~~", "raised_by": "reviewer", "id": "R2"},
    {"kind": "issue", "label": "Outside this issue", "text": f"Elsewhere:\n```\n{EVIL}\n```",
     "evidence": "Seen.", "raised_by": "reviewer", "id": "R3"}]}


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


def the_card(plan=PLAN):
    """A planned issue's card whose texts hold code and prose that tries HTML."""
    found = {"recs": [rec("planner", None, plan, 11)], "pr": None, "check_runs": [], "reviews": [], "owners": {"boss"},
             "tests": TESTS, "worker": None, "children": []}
    return card.render(REPO, {"number": 456, "url": SRC, "state": "open", "labels": []}, found)


def the_comment(review=REVIEW):
    """A blocking code review's run comment whose blocker and question hold code."""
    return agent.render(rec("reviewer", "pr", review, 14), plan=PLAN)


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

    Proves 456.2. Draws a code review's comment with a failing criterion, the blocker placed under it and a question for the
    owner with its evidence, all holding code with <, > and &, and checks each code span and the code block are there
    as written, while the prose around them is still escaped. A blocker placed under its criterion shows only its
    words (236.4), so the code it must show is in its words, not its evidence."""
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


@pytest.mark.parametrize("where", ["the card", "the run comment"])
def test_a_fence_that_never_closes_at_a_line_start_draws_no_html(record_property, env, where):
    """A fence an agent never closes, at a line start, never lets later text draw HTML.

    Proves 456.4. On the card, the plan's summary is just ``` open and a criterion's words after its code block are
    ~~~ open; in the run comment, a blocker's and a question's words after their code blocks are ``` open and ~~~ open.
    Later texts hold closed code blocks of <kbd>evil</kbd>. As GitHub renders what the code writes (its answer recorded
    for exactly that text), no <kbd> is drawn, each of those code blocks shows <kbd>evil</kbd> as written, and the
    unclosed fences read as plain words."""
    record_property("proves", "456.4")
    text = the_card(FENCE_PLAN) if where == "the card" else the_comment(FENCE_REVIEW)
    seen = github_html.page(github_html.rendered(text, "456.4"))
    drawn = [t for t, a in seen.tags if t == "kbd"]
    assert not drawn, (f"456.4: as GitHub renders {where}, a fence that never closes at a line start opens a code "
                       f"block, and an agent's {EVIL} after it is drawn as HTML")
    shown = [c for c in seen.codes if c.strip() == EVIL]
    assert len(shown) == 2, (f"456.4: as GitHub renders {where}, the two code blocks of {EVIL} should each show it as "
                             f"written, but {len(shown)} do; the code GitHub shows begins {[c[:60] for c in seen.codes]}")
    words = "".join(t for t in seen.text if t not in seen.codes)
    for fence in (OPEN_TICKS, OPEN_TILDES):
        assert fence in words, (f"456.4: as GitHub renders {where}, the unclosed fence {fence!r} does not read as "
                                "plain words")


# A backtick an agent writes where GitHub never pairs it with the next one: inside a link's address, which GitHub reads
# first, and in a raise's label, drawn on the same line as its words. Code must not take either for the start of code
# and leave the HTML after it unescaped.
LINK_TEXT = f"See [the log](run`x) {EVIL} `"
TICK_LABEL, TICK_WORDS = "`", f"` {EVIL} `"
TICK_RAISE = {"kind": "question", "to": "owner", "label": TICK_LABEL, "text": TICK_WORDS,
              "evidence": "Seen.", "raised_by": "planner", "id": "P1"}
BARE_PLAN = {**PLAN, "user_story": "Owners read words.", "out_of_scope": ["Nothing."],
             "acceptance_criteria": [{"text": "Words show.", "source": SRC}] * 2}
TICK_TEXTS = {
    ("the card", "a backtick inside a link's address"): lambda: the_card({**BARE_PLAN, "summary": LINK_TEXT}),
    ("the card", "a raise's label that opens a backtick"): lambda: the_card({**BARE_PLAN, "raises": [TICK_RAISE]}),
    ("the run comment", "a backtick inside a link's address"): lambda: the_comment(
        {**FENCE_REVIEW, "raises": [{**TICK_RAISE, "label": "Two readings", "text": LINK_TEXT, "raised_by": "reviewer"}]}),
    ("the run comment", "a raise's label that opens a backtick"): lambda: the_comment(
        {**FENCE_REVIEW, "raises": [{**TICK_RAISE, "raised_by": "reviewer"}]}),
}


@pytest.mark.parametrize("where,case", list(TICK_TEXTS))
def test_a_backtick_in_a_link_address_or_a_raise_label_draws_no_html(record_property, env, where, case):
    """A backtick in a link address or raise label never lets words draw HTML.

    Proves 456.4. On the card and in the run comment, writes words `See [the log](run`x) <kbd>evil</kbd> `` (GitHub reads
    the backtick as part of the link's address, so it opens no code), and a raise whose label is a lone backtick and
    whose words are `` ` <kbd>evil</kbd> ` `` (label and words share one line, so GitHub may pair the label's backtick
    with the words'). As GitHub renders what the code writes (its answer recorded for exactly that text), no <kbd> is
    drawn and <kbd>evil</kbd> reads as plain words."""
    record_property("proves", "456.4")
    text = TICK_TEXTS[(where, case)]()
    seen = github_html.page(github_html.rendered(text, "456.4"))
    drawn = [t for t, a in seen.tags if t == "kbd"]
    assert not drawn, (f"456.4: as GitHub renders {where}, {case} lets an agent's {EVIL} draw HTML, because the code "
                       "took that backtick for the start of code and left the words after it unescaped")
    words = "".join(seen.text)
    assert EVIL in words, f"456.4: as GitHub renders {where} with {case}, the agent's {EVIL} no longer reads as written"
