"""GitHub's own rendering of markdown, as answers of its markdown API recorded in the repo.

The owner asked that anything about how GitHub displays text is checked against GitHub's real rendering, not only
against the raw text the code writes. Tests run in CI with no network and no secrets, so each answer of GitHub's
markdown API (POST https://api.github.com/markdown, mode gfm) is recorded once in tests/github_render/<name>.json,
keyed by the exact markdown and the repo it was rendered for. A test asks `rendered(markdown, name)`:

- the recorded HTML comes back only for exactly the same markdown and repo; markdown that differs by one character,
  or that was never recorded, fails the test with the command that records it, so a stale answer never passes;
- with DOKIMA_RECORD_RENDER=1 in the environment (and GITHUB_TOKEN when there is one), it asks GitHub instead and
  writes GitHub's answer into the file, replacing any older answer for that markdown. That is the script that
  refreshes the recordings: `DOKIMA_RECORD_RENDER=1 python3 -m pytest tests/<the test file>`.
"""
import json
import os
import urllib.request

import pytest

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "github_render")


def path_of(name):
    """The file the answers of one set of tests are recorded in."""
    return os.path.join(HERE, f"{name}.json")


def recorded(name):
    """Every answer recorded under `name`, each with its repo, markdown and HTML."""
    try:
        with open(path_of(name)) as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    return [a for a in data if isinstance(a, dict)] if isinstance(data, list) else []


def ask_github(markdown, repo):
    """GitHub's own HTML for `markdown` as a comment in `repo`, from its markdown API."""
    req = urllib.request.Request("https://api.github.com/markdown", method="POST",
                                 data=json.dumps({"text": markdown, "mode": "gfm", "context": repo}).encode(),
                                 headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def rendered(markdown, name, repo="o/r"):
    """The HTML GitHub draws for exactly `markdown` in `repo`, from the answers recorded under `name`.

    Fails the calling test, naming the command that records it, when no answer was recorded for this exact text."""
    answers = recorded(name)
    if os.environ.get("DOKIMA_RECORD_RENDER") == "1":
        html = ask_github(markdown, repo)
        kept = [a for a in answers if not (a.get("markdown") == markdown and a.get("repo") == repo)]
        os.makedirs(HERE, exist_ok=True)
        with open(path_of(name), "w") as f:
            json.dump(kept + [{"repo": repo, "markdown": markdown, "html": html}], f, indent=1)
            f.write("\n")
        return html
    for a in answers:
        if a.get("markdown") == markdown and a.get("repo") == repo:
            return a["html"]
    pytest.fail(f"GitHub's rendering of this exact text is not recorded in tests/github_render/{name}.json, so it "
                f"cannot be checked; record it with DOKIMA_RECORD_RENDER=1 python3 -m pytest on this test. The text:\n"
                f"{markdown}")
