"""The issue body: code's card above one marker, the owner's ask folded below, never rewritten.

Every ask, the owner's own or a split's story quoted by code from the parent's approved plan, sits folded under
Original issue (#373). Bodies saved between #237 and #373 show the ask open: reading still accepts it, and the next
redraw folds it.

Every code path that redraws an issue body (the card and the planner) saves it through `save`, which keeps the
owner's part byte for byte or refuses, leaves the body as it was and says why in a comment on the issue.
"""
import subprocess

MARKER = "<!-- dokima-ask -->"
FOLD_START = "\n<details><summary>Original issue</summary>\n\n"
FOLD_END = "\n\n</details>"
OPEN_START = "\n\n"


class Refused(Exception):
    """A redraw that would change the owner's part; its message says why."""


def ask(body):
    """The owner's part below the first marker, byte for byte; the whole body when there is no marker yet."""
    body = body or ""
    if MARKER not in body:
        return body
    below = body.split(MARKER, 1)[1]
    if below.startswith(FOLD_START) and below.endswith(FOLD_END) and len(below) >= len(FOLD_START) + len(FOLD_END):
        return below[len(FOLD_START):len(below) - len(FOLD_END)]
    if below.startswith(OPEN_START):
        return below[len(OPEN_START):]
    return below


def redraw(body, top):
    """The new body: `top` above the marker, the owner's part folded below; Refused when it would change."""
    body = body or ""
    owner = ask(body)
    below = FOLD_START + owner + FOLD_END
    new = top.rstrip("\n") + "\n\n" + MARKER + below
    if ask(new) != ask(body) or new.split(MARKER, 1)[1] != below:
        raise Refused("the owner's part below the marker would change: the new card holds the marker "
                      f"`{MARKER}` itself, so the owner's original ask would no longer read back as written")
    return new


def gh(*args, **kw):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, **kw).stdout


def save(repo, number, current, top):
    """Save `top` above the owner's part on issue `number` and return True; when refused, leave the body as it was,
    comment why on the issue and return False."""
    try:
        new = redraw(current, top)
    except Refused as e:
        gh("issue", "comment", str(number), "-R", repo, "--body",
           f"**Issue text not updated:** {e}. The issue text was left as it was.")
        print(f"::error title=Issue text not updated::{e}")
        return False
    gh("issue", "edit", str(number), "-R", repo, "--body-file", "-", input=new)
    return True
