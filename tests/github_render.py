"""GitHub's own rendering of Dokima's markdown, from answers recorded in the repo.

Tests run in CI with no network and no secrets, so they cannot ask GitHub each time. Instead each answer GitHub's
markdown API (POST https://api.github.com/markdown, mode gfm) gave is kept in a store file, a JSON list of
{"text": what was sent, "html": what GitHub answered}. `rendered(criterion, text, stores)` returns the HTML recorded
for exactly `text`; an answer recorded for any other text never counts, so a change to what the code writes fails the
test until GitHub's answer for the new text is recorded.

Two kinds of store: the planner's, under tests/rendered/ (recorded on the code of the day the tests were written), and
the worker's, under docs/rendered/, where a build records GitHub's answers for what its code writes now:

    DOKIMA_RECORD_RENDERING=docs/rendered/454.json python3 -m pytest tests/test_github_rendering.py

asks GitHub for every text a test renders and keeps the answer in that file. To ask GitHub again for every text a
store holds (when GitHub's rendering may have changed):

    python3 tests/github_render.py docs/rendered/454.json

Both use GITHUB_TOKEN or GH_TOKEN when set; GitHub's markdown API also answers without one, a few times an hour.
`blocks(html)` reads the HTML the way the owner sees the page: the top-level elements, in order.
"""
import json
import os
import sys
import urllib.request
from html.parser import HTMLParser

import pytest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
API = "https://api.github.com/markdown"
CONTEXT = "dokima-dev/dokima"


def ask_github(text):
    """GitHub's markdown API's HTML for `text`, rendered as on an issue of this repo."""
    headers = {"Accept": "application/vnd.github+json", "Content-Type": "application/json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps({"text": text, "mode": "gfm", "context": CONTEXT}).encode()
    with urllib.request.urlopen(urllib.request.Request(API, data=data, headers=headers), timeout=30) as r:
        return r.read().decode()


def load(path):
    """The answers a store file holds; none when it does not exist."""
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return []
    with open(full) as f:
        return json.load(f)


def keep(path, text, html):
    """Keep GitHub's answer for `text` in the store, replacing an older one."""
    answers = [a for a in load(path) if a.get("text") != text] + [{"text": text, "html": html}]
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        json.dump(answers, f, indent=1)
        f.write("\n")


def rendered(criterion, text, stores):
    """The HTML GitHub answered for exactly `text`, from the first store holding it.

    With DOKIMA_RECORD_RENDERING set to a store file, GitHub is asked now and its answer kept there first. Fails
    naming the criterion when no store holds an answer for this very text."""
    target = os.environ.get("DOKIMA_RECORD_RENDERING")
    if target:
        keep(target, text, ask_github(text))
        stores = [target] + [s for s in stores if s != target]
    for path in stores:
        for a in load(path):
            if a.get("text") == text:
                return a["html"]
    pytest.fail(f"{criterion}: no answer of GitHub's markdown API is recorded for the text the code writes now, so "
                f"how GitHub shows it is unknown. Record it with DOKIMA_RECORD_RENDERING={stores[-1]} python3 -m "
                f"pytest on this test, and commit {stores[-1]}. The text:\n{text}")


class Blocks(HTMLParser):
    """Collects the top-level elements of an HTML fragment, with their text and links."""

    VOID = {"img", "br", "hr", "input", "meta", "link", "source", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.depth, self.in_summary = [], 0, False

    def handle_starttag(self, tag, attrs):
        if self.depth == 0:
            self.out.append({"tag": tag, "attrs": dict(attrs), "text": "", "links": [], "summary": None, "inner": []})
        elif self.out:
            self.out[-1]["inner"].append(tag)
            if tag == "a" and dict(attrs).get("href"):
                self.out[-1]["links"].append(dict(attrs)["href"])
        if tag == "summary" and self.out:
            self.out[-1]["summary"], self.in_summary = "", True
        if tag not in self.VOID:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "summary":
            self.in_summary = False
        if tag not in self.VOID:
            self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        if self.depth == 0:
            if data.strip():
                self.out.append({"tag": "#text", "attrs": {}, "text": data, "links": [], "summary": None, "inner": []})
            return
        if self.out:
            b = self.out[-1]
            b["text"] += data
            if self.in_summary:
                b["summary"] += data


def blocks(html):
    """The top-level elements of GitHub's HTML, in order.

    Each is a dict of tag, attrs, text, links, summary and inner tags.

    `summary` is the text of a fold's summary (None for anything but a fold); `text` is all the element's words."""
    p = Blocks()
    p.feed(html)
    p.close()
    for b in p.out:
        b["text"] = " ".join(b["text"].split())
        if b["summary"] is not None:
            b["summary"] = " ".join(b["summary"].split())
    return p.out


if __name__ == "__main__":
    for store in sys.argv[1:]:
        for a in load(store):
            keep(store, a["text"], ask_github(a["text"]))
        print(f"Asked GitHub again for every text in {store}.")
