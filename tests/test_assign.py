import os

WORKFLOW = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "assign.yml")


def test_new_issues_are_assigned_to_the_code_owners(record_property):
    record_property("proves", "90.1")
    text = open(WORKFLOW).read()
    assert "issues:" in text and "types: [opened]" in text, "90.1: assign.yml does not run on issue opened"
    assert "sender.type" not in text, "90.1: assign.yml filters out bots, so bot-opened issues stay unassigned"
    assert '--add-assignee "$(python3 -m dokima.plan approvers)"' in text, "90.1: assign.yml does not assign the CODEOWNERS approvers"
