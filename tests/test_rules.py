import os


def test_rules_say_close_replaced_issues_as_duplicates(record_property):
    record_property("proves", "70.1")
    rules = open(os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")).read()
    assert "close it as a duplicate of the issue that replaces it" in rules
