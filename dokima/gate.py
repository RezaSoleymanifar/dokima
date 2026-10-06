"""Workflow changes wait for the owner's approval.

    python3 -m dokima.gate touched BASE        # prints the workflow files changed since BASE, one per line
    python3 -m dokima.gate waiting N RUN_URL   # comment: this build changes workflows, approve on the run
    python3 -m dokima.gate stopped N RUN_URL   # comment: approval rejected or expired, nothing pushed

The bot can never push a workflow file. A build that changes one is pushed by a separate
job that holds the only key able to, and that job runs only after the owner approves it
on GitHub (an environment with the owner as required reviewer).
"""
import os
import subprocess
import sys

WORKFLOWS = ".github/workflows/"


def workflow_files(paths):
    return sorted(p for p in paths if p.startswith(WORKFLOWS))


def waiting(files, run_url):
    listed = "\n".join(f"- `{f}`" for f in files)
    return (f"**Waiting for your approval:** this build changes workflow files, so it is not pushed yet.\n\n{listed}\n\n"
            f"Review the changes and approve on the run: [open the run]({run_url}). Nothing is pushed until you do.")


def stopped(run_url):
    return f"**Workflow change not pushed:** the approval was rejected or expired, so nothing was pushed. [See the run]({run_url})"


def changed_since(base):
    out = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], check=True, capture_output=True, text=True).stdout
    return [p for p in out.splitlines() if p]


def comment(number, body):
    subprocess.run(["gh", "issue", "comment", number, "-R", os.environ["GITHUB_REPOSITORY"], "--body", body], check=True)


def main(argv):
    action = argv[1]
    if action == "touched":
        print("\n".join(workflow_files(changed_since(argv[2]))))
    elif action == "waiting":
        files = [l for l in sys.stdin.read().splitlines() if l]
        comment(argv[2], waiting(files, argv[3]))
    elif action == "stopped":
        comment(argv[2], stopped(argv[3]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
