"""Read the GitHub API budget left, GraphQL and REST, before or after a run.

Each reading goes to the log and a file kept with the run.

    python3 -m dokima.budget before|after KEY FILE     # KEY: app or github-token; reads GH_TOKEN

The one call is `gh api rate_limit`, which costs nothing from either budget. Each reading is one JSON line added to
FILE, naming the workflow, the run, the time in UTC, whose key it is and the moment. A budget GitHub would not give
is said with GitHub's reason and holds no numbers; the command always exits 0, so reading never stops the run.
"""
import datetime
import json
import os
import subprocess
import sys


def read():
    """(graphql, rest, None) left on GH_TOKEN's budgets, else (None, None, why)."""
    try:
        r = subprocess.run(["gh", "api", "rate_limit"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        return None, None, f"gh could not be run: {e}"
    if r.returncode != 0:
        return None, None, (r.stderr or r.stdout).strip() or f"gh exited {r.returncode}"
    try:
        res = json.loads(r.stdout)["resources"]
        graphql, rest = res["graphql"]["remaining"], res["core"]["remaining"]
    except (ValueError, KeyError, TypeError) as e:
        return None, None, f"GitHub's answer holds no budget ({type(e).__name__}): {r.stdout.strip()[:200]}"
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in (graphql, rest)):
        return None, None, f"GitHub's answer holds no budget: {r.stdout.strip()[:200]}"
    return graphql, rest, None


def reading(moment, key):
    """One reading as it goes into the file."""
    graphql, rest, why = read()
    e = {"workflow": os.environ.get("GITHUB_WORKFLOW", ""), "run": os.environ.get("GITHUB_RUN_ID", ""),
         "time": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "key": key,
         "moment": moment}
    if why:
        e["error"] = why
    else:
        e.update(graphql=graphql, rest=rest)
    return e


def line(e):
    """The reading as the log says it."""
    head = f"Budget {e['moment']} the run, {e['key']} key:"
    if "error" in e:
        return f"{head} could not be read: {' '.join(str(e['error']).split())}"
    return f"{head} GraphQL {e['graphql']:,} left, REST {e['rest']:,} left."


def main(argv):
    if len(argv) != 4 or argv[1] not in ("before", "after"):
        print("usage: python3 -m dokima.budget before|after KEY FILE; the budget could not be read")
        return 0
    moment, key, path = argv[1:4]
    e = reading(moment, key)
    print(line(e))
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(e) + "\n")
    except OSError as err:
        print(f"::warning title=Budget not kept::{path} could not be written: {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
