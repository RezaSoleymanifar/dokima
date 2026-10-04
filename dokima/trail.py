"""The paper trail: comments the workflows post, and the check on an agent's note."""
import difflib
import re


def link_comment(repo, pr):
    return f"Work is in PR [#{pr}](https://github.com/{repo}/pull/{pr})"


def work_title(issue, title):
    return f"Work on #{issue}: {title}"


def edit_comment(editor, before, after):
    diff = difflib.unified_diff(before.splitlines(), after.splitlines(), lineterm="", n=0)
    lines = [l for l in diff if not l.startswith(("---", "+++", "@@"))]
    return f"@{editor} edited the issue:\n\n```diff\n" + "\n".join(lines) + "\n```"


def check_note(text):
    """Return the labels ("Did:", "Why:") that are missing or empty in the note."""
    missing = []
    for label in ("Did", "Why"):
        if not re.search(rf"^\s*{label}:[ \t]*\S", text, re.MULTILINE):
            missing.append(f"{label}:")
    return missing


def _tokens(n):
    if n < 1000:
        return str(n)
    if n < 1_000_000:
        return f"{round(n / 1000)}k"
    return f"{n / 1_000_000:.1f}M"


def note_comment(note, run_url, minutes, turns, tokens):
    return (f"{note.rstrip()}\n\nCost: {minutes} min · {turns} turns · "
            f"{_tokens(tokens)} tokens · [run]({run_url})")
