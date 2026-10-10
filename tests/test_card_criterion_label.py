"""On every card, a criterion's label links to its check; its text stays plain.

Issue #354. The owner: "the word acceptance criterion should get the hyperlink, not the description in front of it."

The card is drawn by `dokima/card.py` (render, from `found`). Each criterion is one bullet:

    - <status icon> **<a href="check">Acceptance criterion</a>:** the criterion's text

The status icon is never inside a link, the only link on the bullet sits on the label's words (with or without its
colon), and the criterion's text after it is plain. With no check there is no link at all. Non-functional
requirements, in their fold, read the same with the label Non-functional requirement. Markdown links `[text](url)` and
HTML links `<a href="url">text</a>` are read alike.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import card, plan  # noqa: E402

REPO = "o/r"
ISSUE = {"number": 40, "url": "https://github.com/o/r/issues/40"}
ASK = "https://github.com/o/r/issues/40"
PLAN = {"kind": "user_story", "summary": "Owners see one card.", "user_story": "Owners see one card on every issue.",
        "acceptance_criteria": [{"text": "First thing works", "source": ASK},
                                {"text": "Second thing works", "source": ASK}],
        "non_functional": [{"text": "Nothing leaks", "why": "Secrets stay secret.", "principle": "Fail closed."}],
        "scope": ["dokima/card.py"], "out_of_scope": ["The board stays as it is."],
        "tests": {"40.1": ["tests/test_a.py::test_one"], "40.2": ["tests/test_a.py::test_two"],
                  "40.3": ["tests/test_a.py::test_three"]},
        "test_changes": {}}
TESTS = {f"tests/test_a.py::test_{w}": {"verified_by": f"The {w} thing runs.",
                                       "url": f"https://github.com/o/r/blob/abc/tests/test_a.py#L{i}"}
         for i, w in enumerate(("one", "two", "three"), 1)}


def rec(role, stage=None, n=1, **handback):
    """One agent record, as dokima.agent.records reads it from a bot comment."""
    return {"role": role, "stage": stage, "handback": handback, "check": {"passed": True, "problems": []},
            "run": f"https://github.com/o/r/actions/runs/{n}"}


RECS = [rec("planner", n=11, **PLAN), rec("reviewer", "plan", n=12, verdict="approve"), rec("worker", n=13),
        rec("reviewer", "pr", n=14, verdict="approve")]
PR = {"number": 5, "merged": False, "state": "open", "body": "Closes #40", "html_url": "https://github.com/o/r/pull/5",
      "merged_by": None}


def job(n):
    return f"https://github.com/o/r/actions/runs/2/job/{n}"


def run(name, status="completed", conclusion="success", n=7):
    """One GitHub check run on the PR's latest commit."""
    return {"name": name, "status": status, "conclusion": conclusion, "html_url": job(n)}


GREEN = [run("40.1 · First thing works", n=1), run("40.2 · Second thing works", n=2), run("40.3 · Nothing leaks", n=3),
         run("all tests", n=4)]
FOUND = {"recs": RECS, "pr": PR, "check_runs": GREEN, "reviews": [], "owners": {"boss"}, "tests": TESTS,
         "worker": {"status": "completed", "conclusion": "success", "html_url": "https://github.com/o/r/actions/runs/1"},
         "children": []}


def draw(**kw):
    return card.render(REPO, ISSUE, dict(FOUND, **kw))


def plain(html):
    """The words a reader sees: no images, tags, italic or bold markers."""
    text = re.sub(r"<img [^>]*>", "", html)
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)
    return re.sub(r"\s+", " ", text.replace("**", "").replace("*", "").replace("_", "")).strip()


def bullet(text, words, k):
    """The one bullet line holding the criterion's text `words`, links written as HTML.

    Fails naming criterion k unless exactly one such bullet is on the card."""
    assert plan.CARD_START in text and plan.CARD_END in text, f"{k}: the text holds no card between its markers"
    block = text[text.index(plan.CARD_START):text.index(plan.CARD_END)]
    block = re.sub(r"\[((?:<img [^>]*>|[^\]])*)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', block)
    found = [l for l in block.splitlines() if l.startswith("- ") and words in l]
    assert len(found) == 1, f"{k}: expected one bullet holding “{words}”, found {len(found)}:\n{block}"
    return found[0]


def label_link(text, label, words, k):
    """The link on the label of criterion `words`, or None when it has none.

    Fails naming criterion k unless the bullet is the status icon, outside any link, then the label and the text as a
    reader sees them ("label: words"), with at most one link, on the label's words only, and the text unlinked."""
    line = bullet(text, words, k)
    m = re.fullmatch(r'- <img [^>]*alt="[^"]*"[^>]*>\s*(.*)', line)
    assert m, f"{k}: the bullet of “{words}” does not open with its status icon outside any link: {line}"
    rest = m.group(1)
    assert plain(rest) == f"{label}: {words}", f"{k}: the bullet of “{words}” does not read “{label}: {words}”: {line}"
    links = re.findall(r'<a href="([^"]+)">(.*?)</a>', rest)
    if not links:
        return None
    assert len(links) == 1, f"{k}: the bullet of “{words}” holds {len(links)} links, not one on its label: {line}"
    url, inside = links[0]
    assert plain(inside).rstrip(":").strip() == label, \
        f"{k}: the link on the bullet of “{words}” is on “{plain(inside)}”, not on the words {label}: {line}"
    after = rest[rest.index("</a>") + len("</a>"):]
    assert words in plain(after), f"{k}: the text “{words}” is not plain text after the linked label: {line}"
    return url


@pytest.mark.parametrize("check", [
    run("40.1 · First thing works", "queued", None, n=1),
    run("40.1 · First thing works", "in_progress", None, n=1),
    run("40.1 · First thing works", n=1),
    run("40.1 · First thing works", conclusion="failure", n=1),
], ids=["queued", "running", "passed", "failed"])
def test_the_words_acceptance_criterion_link_to_the_check_and_the_text_is_plain(record_property, check):
    """The words Acceptance criterion link to the check; the criterion's text after them is plain.

    Draws the card with criterion 1's check queued, running, passed and failed, and checks each time that the only
    link on its bullet is on the words Acceptance criterion, pointing to that check, while the status icon and the
    criterion's text after the label are outside any link. Proves 354.1."""
    record_property("proves", "354.1")
    url = label_link(draw(check_runs=[check]), "Acceptance criterion", "First thing works", "354.1")
    assert url == job(1), f"354.1: the words Acceptance criterion link to {url}, not to the criterion's check {job(1)}"


def test_each_acceptance_criterion_label_links_its_own_check_and_none_without_one(record_property):
    """Each label links to its own check; with no check, nothing is linked.

    Draws the card with both criteria's checks and checks the label of criterion 1 links to check 1 and the label of
    criterion 2 to check 2, with both texts plain; then draws it with only criterion 1's check and checks criterion 2
    reads Acceptance criterion: and its text with neither linked. Proves 354.1."""
    record_property("proves", "354.1")
    text = draw()
    for words, n in (("First thing works", 1), ("Second thing works", 2)):
        url = label_link(text, "Acceptance criterion", words, "354.1")
        assert url == job(n), f"354.1: the label of “{words}” links to {url}, not to its own check {job(n)}"
    text = draw(check_runs=[run("40.1 · First thing works", n=1)])
    url = label_link(text, "Acceptance criterion", "First thing works", "354.1")
    assert url == job(1), f"354.1: the label of “First thing works” links to {url}, not to its check {job(1)}"
    url = label_link(text, "Acceptance criterion", "Second thing works", "354.1")
    assert url is None, f"354.1: a criterion with no check links to {url}"


def test_the_words_non_functional_requirement_link_to_the_check_and_the_text_is_plain(record_property):
    """The words Non-functional requirement link to the check; the requirement's text after them is plain.

    Draws the card with the non-functional requirement's check passed and failed, and checks the only link on its
    bullet is on the words Non-functional requirement, pointing to that check, with its text plain; then draws it
    with no check and checks the bullet has no link. Proves 354.2."""
    record_property("proves", "354.2")
    for check in (run("40.3 · Nothing leaks", n=3), run("40.3 · Nothing leaks", conclusion="failure", n=3)):
        url = label_link(draw(check_runs=[check]), "Non-functional requirement", "Nothing leaks", "354.2")
        assert url == job(3), f"354.2: the words Non-functional requirement link to {url}, not to its check {job(3)}"
    url = label_link(draw(check_runs=[]), "Non-functional requirement", "Nothing leaks", "354.2")
    assert url is None, f"354.2: a non-functional requirement with no check links to {url}"
