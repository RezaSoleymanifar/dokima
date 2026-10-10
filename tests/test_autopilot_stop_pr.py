"""`/autopilot stop` on a pull request takes the autopilot label off it (#369).

On 2026-10-09 `/autopilot stop` on PR #323 answered "No issue in #284's tree was on autopilot" and did nothing: only
the pull request carried the `autopilot` label, not its issue, so the clash loop kept running until the label was
removed by hand. This runs the command listener (.github/workflows/commands.yml) on the machine from test_autopilot.py,
where pull request #60 is built for issue #57 (branch try/issue-57) and every label lives on GitHub's issues API.
"""
from test_autopilot import LABEL, Tree, mentioned
import test_start as ts

PR = int(ts.PR)


def test_autopilot_stop_on_a_pull_request_takes_the_label_off_it(record_property, tmp_path):
    """`/autopilot stop` on a pull request takes its label off, even when its issue had none.

    Proves 369.4.
    Only pull request #60 and the parent #50 carry the autopilot label. After the code owner's `/autopilot stop` on
    #60, the listener must not fail, #60 must no longer carry the label, #50 (outside #57's tree) must keep it, and
    the one comment left on #60 must name #60."""
    record_property("proves", "369.4")
    m = Tree(tmp_path / "stop", {50: [LABEL], PR: [LABEL]})
    m.listen("/autopilot stop", on_pr=True)
    assert not m.failed, f"369.4: the listener failed on /autopilot stop:\n{m.tail()}"
    labels = m.labels()
    assert LABEL not in labels.get(PR, []), f"369.4: /autopilot stop on #{PR} left the autopilot label on it: {labels}"
    assert LABEL in labels.get(50, []), f"369.4: /autopilot stop on #{PR} also took #50, outside its tree, off autopilot"
    posts = [p for p in m.posted() if int(p["where"][2]) == PR]
    assert len(posts) == 1, f"369.4: /autopilot stop left {len(posts)} comments on #{PR}, expected one"
    assert PR in mentioned(posts[0]["body"]), f"369.4: the comment does not name #{PR}, the pull request it switched off:\n{posts[0]['body']}"
