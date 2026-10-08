"""Bring every open PR that fell behind main up to date with GitHub's own Update branch, after each merge to main.

    python3 -m dokima.uptodate     # reads GITHUB_REPOSITORY, GITHUB_REF_NAME and GITHUB_SHA

Rules live in run(); the GitHub calls go through rest(method, path, **fields), shaped like dokima.board.api.
"""
import json
import os
import subprocess
import sys

from dokima.board import api

PER_PAGE = 100


def open_prs(repo, base, rest):
    """Every open PR into base, drafts included."""
    out, page = [], 1
    while True:
        batch = rest("GET", f"repos/{repo}/pulls?state=open&base={base}&per_page={PER_PAGE}&page={page}")
        out += [p for p in batch if p.get("base", {}).get("ref") == base]
        if len(batch) < PER_PAGE:
            return out
        page += 1


def reason(e):
    """GitHub's own reason for refusing a call: its JSON message, else gh's one-line error."""
    try:
        message = json.loads(e.output or "").get("message")
    except (ValueError, AttributeError):
        message = None
    return message or (e.stderr or "").strip() or str(e)


def run(repo, base, sha, rest=api, on_clash=None):
    """Update every open PR into base whose branch is behind it; a refused PR gets one comment saying why.

    on_clash(pr, sha) is called for each PR GitHub refuses with a merge conflict. Returns (updated, refused) numbers."""
    updated, refused = [], []
    for pr in open_prs(repo, base, rest):
        n, head = pr["number"], pr["head"]["sha"]
        if not rest("GET", f"repos/{repo}/compare/{base}...{head}").get("behind_by"):
            continue
        try:
            rest("PUT", f"repos/{repo}/pulls/{n}/update-branch", expected_head_sha=head)
        except subprocess.CalledProcessError as e:
            why = reason(e)
            refused.append(n)
            rest("POST", f"repos/{repo}/issues/{n}/comments",
                 body=f"This pull request could not be updated with `{base}` ({sha[:7]}). GitHub said: {why}")
            if on_clash and "merge conflict" in why.lower():
                on_clash(pr, sha)
            continue
        updated.append(n)
    return updated, refused


def main():
    repo, base, sha = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_REF_NAME"], os.environ["GITHUB_SHA"]
    updated, refused = run(repo, base, sha)
    for n in updated:
        print(f"uptodate: updated #{n}")
    for n in refused:
        print(f"::warning::uptodate: #{n} could not be updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
