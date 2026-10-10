"""GitHub's own rendering of markdown, recorded in the repo for the tests.

Tests use it to check how GitHub shows what code writes.

Tests run in CI with no network and no secrets, so GitHub's answers from its markdown API (POST /markdown, gfm) are
recorded once in dokima/github_rendering.json, as {"answers": [{"text": ..., "html": ...}, ...]}, and read back here.
tests/github_code_rendering.json holds answers the planner recorded for what the code wrote before the work, in the same
shape, so a test can show it fails today for the right reason on GitHub's real rendering.
An answer counts only for the exact text it was recorded for: when the code writes anything else, the test fails and
says how to record GitHub's answer for the new text, so a stale answer never passes.

    DOKIMA_RECORD_RENDER=1 python3 -m pytest tests/test_code_as_written.py   records GitHub's answer for every text
                                                                              a test asks about and has no answer for
    python3 tests/github_html.py                                              asks GitHub again for every recorded
                                                                              text and rewrites its answer
    DOKIMA_LIVE_RENDER=1 python3 -m pytest ...                                also asks GitHub live and fails when a
                                                                              recorded answer is not what GitHub says

Both calls use $GITHUB_TOKEN when it is set; without it GitHub allows a few dozen calls an hour.
"""
import html.parser
import json
import os
import sys
import urllib.request

import pytest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ANSWERS = os.path.join(ROOT, "dokima", "github_rendering.json")
PLANNED = os.path.join(ROOT, "tests", "github_code_rendering.json")


def ask_github(text):
    """GitHub's HTML for `text`, as its markdown API renders a comment."""
    req = urllib.request.Request("https://api.github.com/markdown", data=json.dumps({"text": text, "mode": "gfm"}).encode(),
                                 headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def load(path=ANSWERS):
    """The answers recorded in `path`; none when the file is missing."""
    if not os.path.exists(path):
        return []
    return json.load(open(path)).get("answers") or []


def save(answers):
    """Write the answers back, one per text, in a stable order."""
    with open(ANSWERS, "w") as f:
        json.dump({"answers": sorted(answers, key=lambda a: a["text"])}, f, indent=1, ensure_ascii=False)
        f.write("\n")


def rendered(text, criterion):
    """GitHub's recorded HTML for exactly `text`; the test fails when there is none.

    The failure names `criterion` and says how to record the answer."""
    answers = load()
    found = next((a for a in answers + load(PLANNED) if a.get("text") == text), None)
    if found is None and os.environ.get("DOKIMA_RECORD_RENDER") == "1":
        found = {"text": text, "html": ask_github(text)}
        save(answers + [found])
    if found is None:
        pytest.fail(f"{criterion}: GitHub's rendering of the text the code writes now is not recorded in "
                    "dokima/github_rendering.json (an answer recorded for other text does not count). Record it with "
                    "DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test.")
    if os.environ.get("DOKIMA_LIVE_RENDER") == "1":
        live = ask_github(text)
        assert live == found["html"], f"{criterion}: the recorded answer is not what GitHub renders for this text now"
    return found["html"]


class Page(html.parser.HTMLParser):
    """What a reader sees in GitHub's HTML: code, tags drawn and visible text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.codes, self.tags, self.text, self._code = [], [], [], []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == "code":
            self._code.append([])

    def handle_endtag(self, tag):
        if tag == "code" and self._code:
            self.codes.append("".join(self._code.pop()))

    def handle_data(self, data):
        self.text.append(data)
        for c in self._code:
            c.append(data)


def page(html_text):
    """Parse GitHub's HTML into what a reader sees."""
    p = Page()
    p.feed(html_text)
    p.close()
    return p


if __name__ == "__main__":
    answers = load()
    for a in answers:
        a["html"] = ask_github(a["text"])
    save(answers)
    print(f"Asked GitHub again for {len(answers)} recorded texts.", file=sys.stderr)
