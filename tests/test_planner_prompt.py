import os

PROMPT = os.path.join(os.path.dirname(__file__), "..", "dokima", "roles", "planner.md")
SECTIONS = ["Where you are", "Judge the ask", "The plan", "Where your tests run", "Before you finish", "Split"]


def test_planner_prompt_has_every_section(record_property):
    record_property("proves", "89.1")
    headings = [line[2:] for line in open(PROMPT) if line.startswith("# ")]
    missing = [s for s in SECTIONS if not any(h.startswith(s) for h in headings)]
    assert not missing, f"89.1: planner.md is missing sections: {missing}"
