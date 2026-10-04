import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokima import trail  # noqa: E402


def test_link_and_title(record_property):
    record_property("proves", "47.1")
    assert trail.link_comment("o/r", 5) == "Work is in PR [#5](https://github.com/o/r/pull/5)"
    assert trail.work_title(47, "Do it") == "Work on #47: Do it"


def test_edit_comment_names_editor_and_diffs(record_property):
    record_property("proves", "47.2")
    c = trail.edit_comment("reza", "a\nb\nc", "a\nB\nc")
    assert "@reza" in c
    assert "-b" in c and "+B" in c
    assert "-a" not in c


def test_check_note_complete(record_property):
    record_property("proves", "47.3")
    assert trail.check_note("Did: x\nWhy: y") == []


def test_check_note_empty(record_property):
    record_property("proves", "47.3")
    assert trail.check_note("") == ["Did:", "Why:"]
    assert trail.check_note("Did:\nWhy:  \n") == ["Did:", "Why:"]


def test_check_note_without_why(record_property):
    record_property("proves", "47.3")
    assert trail.check_note("Did: x") == ["Why:"]


def test_note_comment_token_sizes(record_property):
    record_property("proves", "47.4")
    f = lambda t: trail.note_comment("N", "http://u", 12, 30, t)
    assert f(850) == "N\n\nCost: 12 min · 30 turns · 850 tokens · [run](http://u)"
    assert "· 45k tokens ·" in f(45_000)
    assert "· 1.2M tokens ·" in f(1_200_000)
