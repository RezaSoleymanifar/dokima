"""Run a board or card update once more after GitHub's empty API budget resets.

A failure counts as a budget failure only when GitHub's rate-limit endpoint, read right after it, reports 0 left in
the GraphQL or REST budget. Then the update waits until the later reset of the empty budgets and runs once more, from
scratch; a second failure fails as any other. Any other failure, or a budget GitHub cannot report, fails at once.

rate_limit(), sleep() and now() are the seams to GitHub and the clock; callers reach them through this module.
"""
import json
import subprocess
import time

MARGIN = 5  # seconds past the reported reset, so the budget is surely back


def rate_limit():
    """GitHub's `GET /rate_limit` answer, which costs nothing from either budget.

    Raises CalledProcessError when GitHub refuses."""
    return json.loads(subprocess.run(["gh", "api", "rate_limit"], check=True, capture_output=True, text=True).stdout)


def sleep(seconds):
    time.sleep(seconds)


def now():
    return time.time()


def empty_reset():
    """The later reset of the empty budgets, or None.

    None when no budget is empty or GitHub cannot say; the reset is in epoch seconds."""
    try:
        resources = rate_limit()["resources"]
        resets = [resources[n]["reset"] for n in ("core", "graphql") if (resources.get(n) or {}).get("remaining") == 0]
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError, TypeError) as e:
        print(f"GitHub could not report its API budget, so this is not a budget failure: {getattr(e, 'stderr', '') or e}")
        return None
    return max(resets) if resets else None


def wait_for_budget(what):
    """Wait for the empty budget's reset and return True.

    Returns False at once when no budget is empty."""
    reset = empty_reset()
    if reset is None:
        return False
    seconds = max(0, reset - now()) + MARGIN
    print(f"::warning::GitHub's API budget is empty, so {what} waits {int(seconds)} s for its reset and runs once more.")
    sleep(seconds)
    return True


def once_more(what, update, failed=lambda result: False, errors=(subprocess.CalledProcessError, RuntimeError)):
    """update(), run once more after the reset when it failed on an empty budget.

    It failed when it raised one of `errors` or `failed(result)` holds."""
    try:
        result = update()
    except errors:
        if not wait_for_budget(what):
            raise
        return update()
    if failed(result) and wait_for_budget(what):
        return update()
    return result
