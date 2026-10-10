"""The card as the owner reads it, wherever its Definition of Done sits.

Since #454 a planned issue's body reads: the card, the Original issue fold, then the Definition of Done as its last
line, below the fold; the pull request keeps its Definition of Done inside the card, above its Original issue fold.
Tests that compare a card with another, or read a card's Definition of Done, use `owner_card` so both pages read
alike: the card from its start marker to its end marker, with a planned issue's Definition of Done put back where the
card itself would hold it, right above the end marker.
"""
import re

from dokima import body, plan

FOLD_HEAD = "<details><summary>Original issue</summary>"
DONE_BELOW = re.compile(r"</details>\s*(?:<!--[^\n]*?-->\s*)*(\*\*Definition of Done:\*\*[^\n]*)\s*$")


def owner_card(text):
    """The card in `text`, from marker to marker, holding its Definition of Done.

    When the Definition of Done is the body's last line below the Original issue fold (a planned issue since #454),
    it is put back right above the end marker, as the pull request's card holds it."""
    assert plan.CARD_START in text and plan.CARD_END in text, "the text holds no card between its markers"
    shown = text[text.index(plan.CARD_START):text.index(plan.CARD_END)]
    below = text.split(body.MARKER, 1)[1] if body.MARKER in text else ""
    m = DONE_BELOW.search(below)
    if m and below.lstrip("\n").startswith(FOLD_HEAD) and "**Definition of Done:**" not in shown:
        shown = shown.rstrip("\n") + "\n\n" + m.group(1) + "\n\n"
    return shown + plan.CARD_END
