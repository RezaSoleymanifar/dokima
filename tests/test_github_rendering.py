"""On GitHub, the fold sits above the Definition of Done, and stats come last.

Issue #454, story 3 of #416: "Anything about how GitHub displays text is checked against GitHub's real rendering (its
markdown API), not only against the raw text the code writes." Each test draws the text exactly as Dokima's code
writes it (the issue body as the card's main saves it, the run comment as `agent next` leaves it to be posted), then
reads the HTML GitHub's markdown API answered for that very text (tests/github_render.py): recorded by the planner in
tests/rendered/454.json for today's code, and by the build in docs/rendered/454.json for its own. An answer recorded
for any other text never counts, so the test fails until GitHub's answer for what the code writes now is recorded.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from dokima import agent  # noqa: E402
from github_render import blocks, rendered  # noqa: E402
from test_body import github, run_card  # noqa: E402,F401
from test_run_comment_fields import WORK, rec  # noqa: E402
from test_stats_last import LINKS, STATS, post  # noqa: E402,F401

STORES = ["tests/rendered/454.json", "docs/rendered/454.json"]


def test_github_shows_a_planned_issues_fold_right_above_its_definition_of_done(record_property, monkeypatch, github):
    """On GitHub, a planned issue shows its fold, then its Definition of Done last.

    Proves 454.4.

    Saves a planned issue's body with the card's main, reads GitHub's own rendering of exactly that body, and checks
    its last element is the Definition of Done, the one right above it is the Original issue fold holding the
    owner's words, and the Definition of Done shows nowhere else on the page."""
    record_property("proves", "454.4")
    saved = run_card(monkeypatch, github, "My ask, as I wrote it.")
    assert saved is not None, "454.4: setup: the card saved nothing"
    page = blocks(rendered("454.4", saved, STORES))
    assert page, "454.4: GitHub's rendering of the issue is empty"
    last = page[-1]
    assert last["tag"] == "p" and last["text"].startswith("Definition of Done:"), \
        f"454.4: on GitHub the issue's last element is not its Definition of Done: <{last['tag']}> {last['text'][:200]!r}"
    fold = page[-2] if len(page) > 1 else {}
    assert fold.get("tag") == "details" and fold.get("summary") == "Original issue", \
        f"454.4: on GitHub the element right above the Definition of Done is not the Original issue fold: {fold}"
    assert "My ask, as I wrote it." in fold["text"], "454.4: on GitHub the Original issue fold does not hold the owner's words"
    shown = [b for b in page if "Definition of Done" in b["text"]]
    assert len(shown) == 1, f"454.4: on GitHub the Definition of Done shows {len(shown)} times on the issue"


def test_github_shows_a_run_comment_ending_with_its_stats_line(record_property, post):
    """On GitHub, a run comment ends with its stats line, right below its Next line.

    Proves 454.4.

    Posts a worker's comment as the workflow does, reads GitHub's own rendering of exactly that comment, and checks
    its last element shows the model, time, turns, tokens, cost and links to the conversation and the run, the one
    right above it is the Next line, and no Stats fold is left."""
    record_property("proves", "454.4")
    page = blocks(rendered("454.4", post(rec("worker", "", WORK)), STORES))
    assert page, "454.4: GitHub's rendering of the run comment is empty"
    last = page[-1]
    for said in STATS:
        assert said in last["text"], f"454.4: on GitHub the comment's last element does not show {said!r}: {last['text'][:300]!r}"
    for link in LINKS:
        assert link in last["links"], f"454.4: on GitHub the comment's last element does not link {link}: {last['links']}"
    above = page[-2] if len(page) > 1 else {}
    assert above.get("tag") == "p" and above.get("text", "").startswith("Next:"), \
        f"454.4: on GitHub the element right above the stats is not the Next line: {above}"
    folds = [b["summary"] for b in page if b["tag"] == "details"]
    assert not any("Stats" in (s or "") for s in folds), f"454.4: on GitHub the comment still shows a Stats fold: {folds}"
