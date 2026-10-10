"""Outside prose, every issue Dokima names shows as GitHub's own reference: its full address.

Issue #480, part of #416. Inside prose (a sentence, a record's text) an issue stays short, as #N, so the text reads
well. In the card's fields and lists an issue is written out as its full address,
`https://github.com/OWNER/REPO/issues/N`, on its own, so GitHub draws it with its icon, its title and its number. An
acceptance criterion's Source on the card is always that full address, never #N.

These tests draw the card with `dokima/card.py` and read the markdown it writes.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card, plan  # noqa: E402

REPO = "o/r"
N = 480
ISSUE = {"number": N, "url": f"https://github.com/o/r/issues/{N}"}
SRC = f"https://github.com/o/r/issues/{N}"
PR = {"number": 5, "merged": False, "state": "open", "body": f"Closes #{N}", "html_url": "https://github.com/o/r/pull/5",
      "merged_by": None}
PLAN = {"kind": "user_story", "summary": "Builds on #300 for the card.", "user_story": "Like #301, owners see one card.",
        "acceptance_criteria": [{"text": "The card works as #302 said.", "source": SRC}],
        "non_functional": [{"text": "Nothing breaks, as #303 asked.", "why": "it must", "principle": "Fail closed"}],
        "scope": ["dokima/card.py"],
        "out_of_scope": ["Filing raises; story 3 (#310) does that.", "The board, see #311 and #312.",
                         "Leave `#313` in code as written."],
        "tests": {f"{N}.1": ["tests/test_a.py::test_one"], f"{N}.2": ["tests/test_a.py::test_two"]},
        "links": {"blocked_by": [50, 51], "blocks": [52], "relates_to": [53]}}


def url(n):
    """The full address of issue n in the test repo."""
    return f"https://github.com/o/r/issues/{n}"


def rec(role, stage=None, n=1, **handback):
    """One agent record that passed its check, as dokima.agent.records reads it from a bot comment."""
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}"}


def draw(handback=None, page="issue", children=()):
    """The card between its markers, for an approved plan with an open PR."""
    recs = [rec("planner", n=11, **(handback or PLAN)), rec("reviewer", "plan", n=12, verdict="approve")]
    found = {"recs": recs, "pr": PR, "check_runs": [], "reviews": [], "owners": {"boss"}, "tests": {}, "worker": None,
             "children": list(children)}
    text = card.render(REPO, ISSUE, found, page=page)
    assert plan.CARD_START in text and plan.CARD_END in text, "the card has no markers"
    return text[text.index(plan.CARD_START) + len(plan.CARD_START):text.index(plan.CARD_END)]


def short(n, text):
    """True when `text` names issue n short, as #N."""
    return re.search(rf"(?<![\w/&]){re.escape('#')}{n}\b", text) is not None


def bare(address, text):
    """True when `address` stands on its own in `text`, never inside a link."""
    at = [m.start() for m in re.finditer(re.escape(address) + r"(?![\w/#-])", text)]
    return bool(at) and all(not text[:i].endswith(("](", 'href="', "(<")) for i in at)


def line_of(text, label):
    """The one card line carrying the bold label, e.g. **Blocked by:**."""
    rows = [l for l in text.splitlines() if f"**{label}:**" in l]
    assert len(rows) == 1, f"the card has {len(rows)} lines with {label}:\n{text}"
    return rows[0]


# 480.1: Blocked by, Blocks and Relates to name each issue by its full address

def test_blocked_by_blocks_and_relates_to_show_full_addresses(record_property):
    """Blocked by, Blocks and Relates to name each issue by its full address.

    Proves 480.1. Draws the card of a plan blocked by #50 and #51, blocking #52 and relating to #53, on the issue and on its PR, and
    checks each line names exactly its own issues, each as its full address on its own, and none as #N. The top row
    still names the PR (and on the PR the issue) by full address."""
    record_property("proves", f"{N}.1")
    for page in ("issue", "pr"):
        text = draw(page=page)
        for label, numbers in (("Blocked by", [50, 51]), ("Blocks", [52]), ("Relates to", [53])):
            line = line_of(text, label)
            for n in numbers:
                assert bare(url(n), line), \
                    f"480.1: on the {page} card the {label} line does not name #{n} by its full address {url(n)}: {line}"
                assert not short(n, line), f"480.1: on the {page} card the {label} line still names #{n} as #{n}: {line}"
            shown = sorted(int(x) for x in re.findall(r"https://github\.com/o/r/issues/(\d+)", line))
            assert shown == numbers, f"480.1: on the {page} card the {label} line names {shown}, not {numbers}: {line}"
        assert bare("https://github.com/o/r/pull/5", text), f"480.1: the {page} card's top row lost the PR's full address"
        if page == "pr":
            assert bare(SRC, text), f"480.1: the PR card's top row lost the issue's full address"


def test_stories_keep_their_full_addresses_beside_the_links(record_property):
    """A split's Stories and its links both show full addresses on the card.

    Proves 480.1. Draws the card of a split with two stories that also relates to #53, and checks each story row names its story by
    full address, and the Relates to line names #53 by full address, not as #53."""
    record_property("proves", f"{N}.1")
    feature = {"kind": "feature", "summary": "Two stories.", "feature": "f", "links": {"relates_to": [53]},
               "stories": [{"title": t, "user_story": "u", "acceptance_criteria": [], "non_functional": [],
                            "depends_on": []} for t in ("A", "B")]}
    text = draw(feature, children=[{"number": 61, "title": "A", "stage": "Plan"},
                                    {"number": 62, "title": "B", "stage": "Merged"}])
    for n in (61, 62):
        assert bare(url(n), text), f"480.1: the Stories list does not name story #{n} by its full address:\n{text}"
    line = line_of(text, "Relates to")
    assert bare(url(53), line) and not short(53, line), \
        f"480.1: a split's Relates to line does not name #53 by its full address: {line}"


# 480.2: Out of scope names issues by full address; prose keeps #N

def test_out_of_scope_names_issues_by_full_address_while_prose_stays_short(record_property):
    """Out of scope names issues by full address; the plan's sentences keep #N.

    Proves 480.2. Draws the card of a plan whose Out of scope names #310, #311 and #312, and checks each is its full address and no
    longer #N there; `#313` inside code stays as written. On the same card the summary, user story, criterion and
    non-functional texts keep #300 to #303 short, with no full address for them."""
    record_property("proves", f"{N}.2")
    for page in ("issue", "pr"):
        text = draw(page=page)
        assert "<summary><b>Out of scope</b></summary>" in text, f"480.2: the {page} card has no Out of scope fold"
        fold = text.split("<summary><b>Out of scope</b></summary>", 1)[1].split("</details>", 1)[0]
        for n in (310, 311, 312):
            assert bare(url(n), fold), f"480.2: on the {page} card Out of scope does not name #{n} by its full address:\n{fold}"
            assert not short(n, fold), f"480.2: on the {page} card Out of scope still names #{n} as #{n}:\n{fold}"
        assert "`#313`" in fold and url(313) not in text, \
            f"480.2: on the {page} card Out of scope changed `#313`, which is code, not a reference:\n{fold}"
        assert "Filing raises; story 3 (" in fold and "The board, see " in fold, \
            f"480.2: on the {page} card Out of scope lost its words around the references:\n{fold}"
        for n in (300, 301, 302, 303):
            assert short(n, text), f"480.2: on the {page} card the prose naming #{n} no longer says #{n}:\n{text}"
            assert url(n) not in text, f"480.2: on the {page} card the prose naming #{n} became its full address:\n{text}"


# 480.3: a criterion's Source is always the full address

def test_a_source_given_as_a_short_reference_shows_its_full_address(record_property):
    """A Source written as #N still shows its full address on the card.

    Proves 480.3. Draws the card of a plan whose first criterion's source is "#480" and second is a comment's full link, and checks
    the first Source line reads the issue's full address and no #480, and the comment's link is kept exactly."""
    record_property("proves", f"{N}.3")
    comment = f"{SRC}#issuecomment-77"
    handback = dict(PLAN, acceptance_criteria=[{"text": "First thing works", "source": f"#{N}"},
                                               {"text": "Second thing works", "source": comment}],
                    tests={f"{N}.1": ["tests/test_a.py::test_one"], f"{N}.2": ["tests/test_a.py::test_two"],
                           f"{N}.3": ["tests/test_a.py::test_three"]})
    for page in ("issue", "pr"):
        sources = [l.strip() for l in draw(handback, page).splitlines() if l.strip().startswith("- Source:")]
        assert len(sources) >= 2, f"480.3: the {page} card shows {len(sources)} Source lines, not one per criterion"
        assert sources[0] == f"- Source: {SRC}", \
            f"480.3: on the {page} card a source written #{N} shows as “{sources[0]}”, not its full address {SRC}"
        assert sources[1] == f"- Source: {comment}", \
            f"480.3: on the {page} card a comment's source changed to “{sources[1]}”, not {comment}"
