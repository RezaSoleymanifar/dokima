"""Outside prose, every issue Dokima names shows as GitHub's own reference: its full address.

Issue #480, part of #416. Inside prose (a sentence, a record's text) an issue stays short, as #N, so the text reads
well. Everywhere else, in the card's fields and lists and the lists code writes for a split, an issue is written out
as its full address, `https://github.com/OWNER/REPO/issues/N`, on its own, so GitHub draws it with its icon, its title
and its number. An acceptance criterion's Source is always that full address, never #N and never a word linked to it.

These tests draw the card with `dokima/card.py`, a filed split's comment with `dokima/agent.py`, and file a split
through `agent.file_split` with GitHub faked, then read the markdown they write.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest

from dokima import agent, card, plan  # noqa: E402

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


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.setenv("GITHUB_RUN_ID", "1")


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


def file_split(monkeypatch, sources):
    """Files a two-story split of #139 with GitHub faked; its record and story bodies."""
    calls = []

    def fake_gh(*args):
        calls.append(args)
        if args[:2] == ("issue", "view"):
            return json.dumps({"title": "Parent"})
        if args[:2] == ("issue", "create"):
            return f"https://github.com/o/r/issues/{200 + sum(1 for c in calls if c[:2] == ('issue', 'create'))}\n"
        if args[0] == "api" and args[1].startswith("repos/o/r/issues/2"):
            return json.dumps({"id": 9000 + int(args[1].split("/")[-1])})
        return "{}"
    monkeypatch.setattr(agent, "gh", fake_gh)
    split = {"kind": "feature", "summary": "s", "feature": "f", "stories": [
        {"title": "First", "user_story": "u1", "acceptance_criteria": [{"text": "a", "source": sources[0]}],
         "non_functional": [], "depends_on": []},
        {"title": "Second", "user_story": "u2", "acceptance_criteria": [{"text": "b", "source": sources[1]}],
         "non_functional": [], "depends_on": [0]}]}
    recs = [rec("planner", n=1, **split), rec("reviewer", "plan", n=2, verdict="approve")]
    r = agent.file_split(REPO, 139, recs)
    bodies = [c[c.index("--body") + 1] for c in calls if c[:2] == ("issue", "create")]
    assert len(bodies) == 2, f"filing the split created {len(bodies)} issues, not 2"
    return r, bodies


def test_a_filed_storys_criteria_give_their_source_as_a_full_address(record_property, monkeypatch, env):
    """A filed story's criteria show their Source as the full address, never a linked word.

    Proves 480.3. Files a split whose stories' criteria come from #139 itself and from a comment on it, and checks each story's body
    shows its source's full address on its own, with no [source](...) link and no link with words around it."""
    record_property("proves", f"{N}.3")
    sources = ["https://github.com/o/r/issues/139", "https://github.com/o/r/issues/139#issuecomment-5"]
    _, bodies = file_split(monkeypatch, sources)
    for i, (body, src) in enumerate(zip(bodies, sources), 1):
        assert "[source](" not in body, f"480.3: story {i}'s body links the word source to its Source:\n{body}"
        assert bare(src, body), f"480.3: story {i}'s body does not show its Source {src} on its own:\n{body}"
        line = next((l for l in body.splitlines() if l.startswith("- ") and src in l), "")
        assert re.search(r"Source:?\**\s*" + re.escape(src), line), \
            f"480.3: story {i}'s criterion does not say Source before {src}: {line}"


# 480.4: a split's lists name each issue by its full address

def test_the_split_comment_and_filed_stories_name_issues_by_full_address(record_property, monkeypatch, env):
    """A filed split's comment and each story's Part of name issues by full address.

    Proves 480.4. Files a split of #139 into #201 and #202, #202 blocked by #201, and checks the split's comment lists each story by
    its full address with #202's blocked by naming #201 by full address, none of them as #N; and each story's body
    names its parent in Part of by #139's full address, not as #139."""
    record_property("proves", f"{N}.4")
    r, bodies = file_split(monkeypatch, [SRC, SRC])
    words = re.sub(r"<img [^>]*>\s*", "", agent.render(r)).split("<details>", 1)[0]
    first = next((l for l in words.splitlines() if l.startswith("1. ")), "")
    second = next((l for l in words.splitlines() if l.startswith("2. ")), "")
    assert bare(url(201), first) and not short(201, first), \
        f"480.4: the split's comment does not list story 1 by its full address {url(201)}: {first!r}"
    assert second.startswith(f"2. {url(202)}") and not short(202, second), \
        f"480.4: the split's comment does not list story 2 by its full address {url(202)}: {second!r}"
    assert re.search(r"blocked by " + re.escape(url(201)), second) and not short(201, second), \
        f"480.4: story 2's blocked by does not name #201 by its full address: {second!r}"
    assert "blocked by" not in first, f"480.4: story 1, blocked by nothing, says blocked by: {first!r}"
    for i, body in enumerate(bodies, 1):
        part = next((l for l in body.splitlines() if "Part of" in l), "")
        assert bare(url(139), part) and not short(139, part), \
            f"480.4: story {i}'s Part of does not name its parent #139 by its full address: {part!r}"
