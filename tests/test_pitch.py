from pathlib import Path

PITCH = (
    "**Agents out-code us on narrow tasks. The bottleneck is knowing their work is done. "
    "Dokima moves your effort from writing code to verifying it.**"
)


def test_pitch_opens_readme_and_wiki_home(record_property):
    record_property("proves", "107.1")
    for path in ("README.md", "docs/wiki/Home.md"):
        lines = Path(path).read_text().splitlines()
        assert lines[0] == "# Dokima"
        assert lines[2] == PITCH
