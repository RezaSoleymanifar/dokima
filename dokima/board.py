"""Keep the project board's Status and Action ("Needs you") current, from GitHub events.

    python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")

Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing.
"""
import json
import os
import re
import subprocess
import sys

CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.I)
YOUR_TURN = ("Plan written above", "**Planner question**", "**Plan rejected:**")


def linked(body):
    return [int(n) for n in CLOSES.findall(body or "")]


def decide(event, p):
    """[(kind, number, status, needs_you)]: kind is "issue" or "pr"; needs_you True marks it for the owner."""
    out = []
    if event == "issues":
        n, action = p["issue"]["number"], p["action"]
        if action == "labeled" and p["label"]["name"] == "plan":
            out.append(("issue", n, "Plan", False))
        elif action == "labeled" and p["label"]["name"] == "work":
            out.append(("issue", n, "Work", False))
        elif action == "closed":
            out.append(("issue", n, "Done", False))
    elif event == "issue_comment" and p["action"] == "created":
        if p["comment"]["user"]["type"] == "Bot" and p["comment"]["body"].startswith(YOUR_TURN):
            out.append(("issue", p["issue"]["number"], "Plan", True))
    elif event in ("pull_request", "pull_request_target"):
        pr, action = p["pull_request"], p["action"]
        both = [("pr", pr["number"])] + [("issue", n) for n in linked(pr.get("body"))]
        if action in ("opened", "reopened", "synchronize"):
            out += [(k, n, "Review", False) for k, n in both]
        elif action == "closed":
            out += [(k, n, "Done", False) for k, n in both if k == "pr" or pr.get("merged")]
    elif event == "pull_request_review" and p["action"] == "submitted":
        pr = p["pull_request"]
        if p["review"]["state"].lower() == "changes_requested":
            out += [("pr", pr["number"], "Work", False)] + [("issue", n, "Work", False) for n in linked(pr.get("body"))]
    elif event == "workflow_run" and p["action"] == "completed":
        for pr in p["workflow_run"].get("pull_requests") or []:
            out.append(("pr", pr["number"], "Review", True))
    return out


def gql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if v is None:
            continue
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)["data"]


class Board:
    def __init__(self, spec, repo, q=gql):
        self.q = q
        owner, number = spec.split("/")
        self.repo_owner, self.repo_name = repo.split("/")
        p = q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}', o=owner, n=int(number))["organization"]["projectV2"]
        self.id = p["id"]
        self.fields = {f["name"]: (f["id"], {o["name"]: o["id"] for o in f["options"]}) for f in p["fields"]["nodes"] if f}

    def item(self, kind, number):
        """The board item for an issue or PR, added at the top if it is not on the board yet."""
        field = "issue" if kind == "issue" else "pullRequest"
        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{id projectItems(first:20){{nodes{{id project{{id}}}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=number)["repository"][field]
        for it in node["projectItems"]["nodes"]:
            if it["project"]["id"] == self.id:
                return it["id"]
        iid = self.q('mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}', p=self.id, c=node["id"])["addProjectV2ItemById"]["item"]["id"]
        self.q('mutation($p:ID!,$i:ID!){updateProjectV2ItemPosition(input:{projectId:$p,itemId:$i}){clientMutationId}}', p=self.id, i=iid)
        return iid

    def set(self, iid, field, option):
        if field not in self.fields:
            return
        fid, options = self.fields[field]
        if option is None:
            self.q('mutation($p:ID!,$i:ID!,$f:ID!){clearProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f}){projectV2Item{id}}}', p=self.id, i=iid, f=fid)
        elif option in options:
            self.q('mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}}', p=self.id, i=iid, f=fid, o=options[option])


ITEMS = """query($p:ID!,$after:String){node(id:$p){... on ProjectV2{items(first:100,after:$after){
  pageInfo{hasNextPage endCursor}
  nodes{id content{__typename
    ... on Issue{number state labels(first:20){nodes{name}} closedByPullRequestsReferences(first:5){nodes{state}}}
    ... on PullRequest{number state}}}}}}}"""


def place(content):
    """(status, clear_flag): the column an issue or PR belongs in, from its real state.

    Closed or merged is Done and drops the Needs you flag; an open PR, or an issue
    with an open PR, is Review; then the work label is Work, the plan label is Plan,
    and anything else is Backlog.
    """
    if content["state"] in ("CLOSED", "MERGED"):
        return "Done", True
    if content["__typename"] == "PullRequest":
        return "Review", False
    if any(pr["state"] == "OPEN" for pr in content["closedByPullRequestsReferences"]["nodes"]):
        return "Review", False
    labels = {label["name"] for label in content["labels"]["nodes"]}
    if "work" in labels:
        return "Work", False
    if "plan" in labels:
        return "Plan", False
    return "Backlog", False


def refresh(board):
    """Put every issue and PR on the board back in the column its real state says."""
    moved, after = [], None
    while True:
        page = board.q(ITEMS, p=board.id, after=after)["node"]["items"]
        for it in page["nodes"]:
            content = it["content"]
            if not content or content["__typename"] not in ("Issue", "PullRequest"):
                continue
            status, clear = place(content)
            board.set(it["id"], "Status", status)
            if clear:
                board.set(it["id"], "Action", None)
            moved.append((content["number"], status))
        if not page["pageInfo"]["hasNextPage"]:
            return moved
        after = page["pageInfo"]["endCursor"]


def sync(event, payload, spec, repo, q=gql):
    changes = decide(event, payload)
    if not spec or not changes:
        return []
    board = Board(spec, repo, q)
    for kind, number, status, needs_you in changes:
        iid = board.item(kind, number)
        board.set(iid, "Status", status)
        board.set(iid, "Action", "Needs you" if needs_you else None)
    return changes


def main():
    spec = os.environ.get("DOKIMA_BOARD", "").strip()
    if not spec:
        print("No DOKIMA_BOARD set; nothing to sync.")
        return 0
    if os.environ["GITHUB_EVENT_NAME"] == "workflow_dispatch":
        for number, status in refresh(Board(spec, os.environ["GITHUB_REPOSITORY"])):
            print("board: refreshed", number, status)
        return 0
    payload = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
    for change in sync(os.environ["GITHUB_EVENT_NAME"], payload, spec, os.environ["GITHUB_REPOSITORY"]):
        print("board:", *change)
    return 0


if __name__ == "__main__":
    sys.exit(main())
