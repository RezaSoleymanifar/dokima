"""Print the matrix of done-when checks for this pull request (demo).

One entry per done-when in the PR's linked issue: its check name, and the tests
that declare they prove it via record_property("proves", "<issue>.<n>").
"""
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, ".")
from dokima.card import parse_issue  # noqa: E402

repo = os.environ["GITHUB_REPOSITORY"]
pr = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["pull_request"]["number"]
owner, name = repo.split("/")
query = ("query($o:String!,$n:String!,$p:Int!){repository(owner:$o,name:$n){pullRequest(number:$p)"
         "{closingIssuesReferences(first:1){nodes{number body}}}}}")
out = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}", "-f", f"o={owner}", "-f", f"n={name}",
                      "-F", f"p={pr}"], check=True, capture_output=True, text=True).stdout
nodes = json.loads(out)["data"]["repository"]["pullRequest"]["closingIssuesReferences"]["nodes"]

tests = {}
for path in glob.glob("tests/test_*.py"):
    current = None
    for line in open(path):
        fn = re.match(r"def (test_\w+)\(", line)
        if fn:
            current = fn.group(1)
        mark = re.search(r'record_property\("proves",\s*"([\d.]+)"\)', line)
        if mark and current:
            tests.setdefault(mark.group(1), []).append(f"{path}::{current}")

matrix = []
if nodes:
    issue = nodes[0]
    for goal in parse_issue(issue["body"]):
        for dw in goal["done_whens"]:
            key = f"{issue['number']}.{dw['n']}"
            text = dw["text"] if len(dw["text"]) <= 60 else dw["text"][:57] + "..."
            matrix.append({"id": key, "name": f"{key} · {text}", "tests": " ".join(tests.get(key, []))})
print("matrix=" + json.dumps(matrix))
