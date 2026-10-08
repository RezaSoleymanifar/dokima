"""Word caps on the texts agents hand back: a text a little over its cap is listed, one far over is rejected.

The owner sets each cap; a text more than TOLERANCE over it (over 30 words for a 25-word cap, over 18 for 15) fails
the check, and one over its cap but within the tolerance only gets listed, so a few words over never fails a run.
"""
import re

TOLERANCE = 20  # percent over its cap a text may run before it is rejected


def count(text):
    """How many words the text holds."""
    return len(text.split())


def first_sentence(text):
    """The text up to its first sentence end ('.', '?' or '!' followed by a space), or all of it when there is none."""
    return re.split(r"(?<=[.?!])\s", text.strip(), maxsplit=1)[0]


def limit(cap):
    """The most words a text with this cap may hold and still pass."""
    return cap + cap * TOLERANCE // 100


def over_cap(where, text, cap, what="opens with"):
    """(listed, rejected) for one text against its cap: each a message, or None.

    Within the cap: neither. Over it by at most TOLERANCE: listed, the text still passes. Past that: rejected.
    """
    n = count(text)
    if n <= cap:
        return None, None
    if n <= limit(cap):
        return f"{where} {what} {n} words, over its cap of {cap} (up to {limit(cap)} passes)", None
    return None, (f"{where} {what} {n} words, more than {TOLERANCE}% over its cap of {cap}: "
                  f"shorten it to {cap} words or fewer")


def check(texts, cap, what="opens with"):
    """(listed, rejected) messages for every (where, text) pair against the same cap."""
    listed, rejected = [], []
    for where, text in texts:
        warn, bad = over_cap(where, text, cap, what)
        listed += [warn] if warn else []
        rejected += [bad] if bad else []
    return listed, rejected


SUMMARY_CAP = 25  # words in the one-sentence summary every planner, worker and reviewer hands back


def summary_caps(text, cap=SUMMARY_CAP):
    """(listed, rejected) for a hand-back's summary: one sentence, held to its cap.

    A second sentence is rejected however short the summary is; its words follow the TOLERANCE rule.
    """
    text = text.strip() if isinstance(text, str) else ""
    if first_sentence(text) != text:
        return [], ["summary holds more than one sentence: make it one sentence of at most "
                    f"{cap} words saying what the run did"]
    return check([("summary", text)], cap, "holds")
