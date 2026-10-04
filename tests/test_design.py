import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_design_doc_has_every_section(record_property):
    record_property("proves", "78.1")
    text = open(os.path.join(ROOT, "DESIGN.md")).read()
    for heading in ("## The picture", "## Principles", "## Roles", "## The flow", "## Decisions log"):
        assert heading in text
    assert "senior engineer" in text and "remote engineers" in text


def test_agents_are_pointed_to_the_design_doc(record_property):
    record_property("proves", "78.2")
    assert "DESIGN.md" in open(os.path.join(ROOT, "CLAUDE.md")).read()
