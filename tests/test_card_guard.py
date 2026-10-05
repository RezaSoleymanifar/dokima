import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")


def guard():
    text = open(os.path.join(ROOT, ".github/workflows/card.yml")).read()
    line = re.search(r"^\s+if:\s*(.+)$", text, re.M).group(1)
    return re.sub(r"\$\{\{(.*)\}\}", r"\1", line).strip()


class Ctx(dict):
    __getattr__ = dict.__getitem__


def runs(event_name, action=None, sender="User"):
    """Evaluate the job's `if:` for one event (only ==, !=, &&, || are supported)."""
    expr = guard().replace("&&", " and ").replace("||", " or ")
    expr = expr.replace("github.event_name", repr(event_name))
    expr = expr.replace("github.event.action", repr(action))
    expr = expr.replace("github.event.sender.type", repr(sender))
    assert "github." not in expr, f"guard uses an unexpected context: {expr}"
    return eval(expr)


def test_bot_opened_issue_gets_a_card(record_property):
    record_property("proves", "87.1")
    assert runs("issues", "opened", "Bot"), "87.1: card job is skipped for an issue opened by a bot"
    assert runs("issues", "opened", "User"), "87.1: card job is skipped for an issue opened by a person"


def test_bot_edits_do_not_retrigger_card(record_property):
    record_property("proves", "87.2")
    assert not runs("issues", "edited", "Bot"), "87.2: a bot's own edit would re-trigger the card (loop)"
    assert runs("issues", "edited", "User"), "87.2: a person's edit no longer triggers the card"
    assert runs("workflow_run", None, "Bot"), "87.2: workflow_run events must still write the card"
