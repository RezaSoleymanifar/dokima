"""Every criterion of a plan quotes words the owner wrote at its source; code refuses one that does not."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import planner  # noqa: E402

ISSUE = "https://github.com/o/r/issues/7"
SAID = {ISSUE: "Code shows as code,\nnever escaped.", ISSUE + "#issuecomment-1": "Stats go last."}


def story(*criteria, nfr=()):
    return {"kind": "user_story", "summary": "s", "user_story": "u", "acceptance_criteria": list(criteria),
            "non_functional": list(nfr), "scope": ["dokima/card.py"], "tests": {"7.1": ["tests/t.py::t"]}}


def test_a_criterion_quoting_the_owner_passes():
    """Words found at the source, spacing aside, pass."""
    planner.from_kind(story({"text": "t", "words": "shows as code, never escaped", "source": ISSUE},
                            {"text": "t", "words": "Stats go last", "source": ISSUE + "#issuecomment-1"}), ISSUE, SAID)


@pytest.mark.parametrize("c", [{"text": "t", "source": ISSUE},
                               {"text": "t", "words": "checked on GitHub's rendering", "source": ISSUE},
                               {"text": "t", "words": "Stats go last", "source": ISSUE}])
def test_a_criterion_without_the_owners_words_at_its_source_is_refused(c):
    """No words, invented words, or words from another place are refused."""
    with pytest.raises(planner.Garbled):
        planner.from_kind(story(c), ISSUE, SAID)


def test_a_non_functional_requirement_needs_the_owners_words_too():
    """A requirement the owner never wrote is refused."""
    ok = {"text": "t", "words": "never escaped", "source": ISSUE}
    with pytest.raises(planner.Garbled):
        planner.from_kind(story(ok, nfr=[{"text": "never inject HTML", "why": "safety"}]), ISSUE, SAID)
