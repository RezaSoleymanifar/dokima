"""Records GitHub's own rendering of the texts tests/test_card_self_link.py and tests/test_card_raises_status.py check.

The answers go into tests/github_rendering.json.

    python3 tests/record_rendering.py

Tests run in CI with no network and no secrets, so they never call GitHub. This script is how GitHub's answer reaches
them: it draws each text with the code as it is now (texts() of each of those test files), sends it to GitHub's markdown API
(POST https://api.github.com/markdown, gfm mode, in the context of dokima-dev/dokima, the way GitHub renders an issue
or a PR there) and saves the text and the HTML GitHub returned, side by side. A test looks its text up byte for byte,
so an answer recorded for any other text fails the test instead of passing it. Run it again whenever the code changes
what it writes; GITHUB_TOKEN, when set, is sent so the call is not limited to GitHub's anonymous budget.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from test_card_self_link import GITHUB, RECORDED, texts  # noqa: E402
import test_card_raises_status  # noqa: E402


def render(text):
    """GitHub's HTML for `text`, from its markdown API."""
    data = json.dumps({"text": text, "mode": "gfm", "context": GITHUB}).encode()
    req = urllib.request.Request("https://api.github.com/markdown", data=data, method="POST",
                                 headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def main():
    """Record GitHub's answer for every text the tests check, and save them all."""
    answers = [{"name": name, "text": text, "html": render(text)} for name, text in {**texts(), **test_card_raises_status.texts()}.items()]
    with open(RECORDED, "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"Recorded GitHub's rendering of {len(answers)} texts in {RECORDED}")


if __name__ == "__main__":
    main()
