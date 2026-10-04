from pathlib import Path

WIKI = Path(__file__).parent.parent / "docs" / "wiki"


def read(name):
    return (WIKI / name).read_text()


def test_writing_issues(record_property):
    record_property("proves", "72.1")
    text = read("Writing-issues.md")
    assert "criteria" in text
    assert "Verified by" in text
    assert "`work` label" in text
    assert "done when" not in text.lower()


def test_the_card(record_property):
    record_property("proves", "72.2")
    text = read("The-card.md")
    assert "issue" in text and "PR" in text
    assert "circle" in text
    assert "approve the result to merge" in text


def test_home(record_property):
    record_property("proves", "72.3")
    assert "`work` label" in read("Home.md")
