"""Keep the project board's Status, Action ("Needs you" or "Autopilot") and Priority current, from GitHub events.

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
PRIORITY = {"blocker": "Blocker", "high": "High", "parked": "Parked"}  # highest first
AUTOPILOT = "autopilot"


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


def priority(event, p):
    """(number, option) when a priority label was added or removed: the highest priority label left, or None to clear."""
    if event != "issues" or p["action"] not in ("labeled", "unlabeled") or p["label"]["name"] not in PRIORITY:
        return None
    names = {label["name"] for label in p["issue"].get("labels") or []}
    return p["issue"]["number"], next((option for label, option in PRIORITY.items() if label in names), None)


def switched(event, p):
    """The issue number when its `autopilot` label was added or removed, else None."""
    if event == "issues" and p["action"] in ("labeled", "unlabeled") and p["label"]["name"] == AUTOPILOT:
        return p["issue"]["number"]
    return None


def gql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)["data"]


def api(method, path, **fields):
    """One REST call, as `gh api -X METHOD path -f k=v`; its parsed JSON."""
    args = ["gh", "api", "-X", method, path]
    for k, v in fields.items():
        args += ["-f", f"{k}={v}"]
    out = subprocess.run(args, check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else {}


class Board:
    def __init__(self, spec, repo, q=gql, rest=api):
        self.q, self.rest = q, rest
        owner, number = spec.split("/")
        self.owner, self.number = owner, int(number)
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

    def value(self, iid, field):
        """The card's current option of a single-select field, or None."""
        if field not in self.fields:
            return None
        node = self.q('query($i:ID!,$f:String!){node(id:$i){... on ProjectV2Item{fieldValueByName(name:$f){... on ProjectV2ItemFieldSingleSelectValue{name}}}}}', i=iid, f=field)["node"]
        return ((node or {}).get("fieldValueByName") or {}).get("name")

    def autopilot(self, kind, number):
        """Whether the issue or PR carries the `autopilot` label."""
        field = "issue" if kind == "issue" else "pullRequest"
        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{labels(first:100){{nodes{{name}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=int(number))["repository"][field]
        return any(label["name"] == AUTOPILOT for label in node["labels"]["nodes"])

    def open_pr(self, number):
        """The open pull request built for the issue, or None."""
        nodes = self.q('query($o:String!,$r:String!,$h:String!){repository(owner:$o,name:$r){pullRequests(headRefName:$h,states:OPEN,first:1){nodes{number}}}}', o=self.repo_owner, r=self.repo_name, h=f"try/issue-{number}")["repository"]["pullRequests"]["nodes"]
        return nodes[0]["number"] if nodes else None

    def label(self, kind, number, on):
        """Put the `autopilot` label on or off the issue or PR, leaving its other labels alone."""
        path = f"repos/{self.repo_owner}/{self.repo_name}/issues/{number}/labels"
        if on:
            self.rest("POST", path, **{"labels[]": AUTOPILOT})
        else:
            self.rest("DELETE", f"{path}/{AUTOPILOT}")

    def views(self):
        p = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){views(first:50){nodes{name}}}}}', o=self.owner, n=self.number)["organization"]["projectV2"]
        return [v["name"] for v in p["views"]["nodes"]]

    def add_view(self, name, layout, filter):
        self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)


def pill(needs_you, autopilot):
    """The Action pill: Needs you when the river stops for the owner, else Autopilot while on autopilot, else none."""
    return "Needs you" if needs_you else "Autopilot" if autopilot else None


def switch(board, number):
    """The issue's autopilot label changed: the issue and its open PR show Autopilot or lose it, the PR's label follows
    the issue's, and Needs you is never replaced or cleared. Returns whether the issue is now on autopilot."""
    on = board.autopilot("issue", number)
    targets = [("issue", number)]
    pr = board.open_pr(number)
    if pr:
        targets.append(("pr", pr))
        if board.autopilot("pr", pr) != on:
            board.label("pr", pr, on)
    for kind, n in targets:
        iid = board.item(kind, n)
        if board.value(iid, "Action") != "Needs you":
            board.set(iid, "Action", pill(False, on))
    return on


def add_autopilot_view(board):
    """Add the Autopilot table view once; say so plainly when GitHub refuses it."""
    if "Autopilot" in board.views():
        return
    try:
        board.add_view("Autopilot", "table", f"label:{AUTOPILOT}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not add the Autopilot view to the board: {(e.stderr or e.output or str(e)).strip()}") from e


def sync(event, payload, spec, repo, q=gql, rest=api):
    changes, rank, flipped = decide(event, payload), priority(event, payload), switched(event, payload)
    if not spec or not (changes or rank or flipped):
        return []
    board = Board(spec, repo, q, rest)
    if event in ("pull_request", "pull_request_target") and payload["action"] in ("opened", "reopened", "synchronize"):
        # A PR built for an issue on autopilot carries the label too, so the Autopilot view lists it.
        pr = payload["pull_request"]
        if any(board.autopilot("issue", n) for n in linked(pr.get("body"))) and not board.autopilot("pr", pr["number"]):
            board.label("pr", pr["number"], True)
    for kind, number, status, needs_you in changes:
        iid = board.item(kind, number)
        board.set(iid, "Status", status)
        board.set(iid, "Action", pill(needs_you, not needs_you and board.autopilot(kind, number)))
    if rank and "Priority" in board.fields:
        number, option = rank
        board.set(board.item("issue", number), "Priority", option)
    if flipped and switch(board, flipped):
        add_autopilot_view(board)
    return changes


def main():
    spec = os.environ.get("DOKIMA_BOARD", "").strip()
    if not spec:
        print("No DOKIMA_BOARD set; nothing to sync.")
        return 0
    payload = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
    try:
        changes = sync(os.environ["GITHUB_EVENT_NAME"], payload, spec, os.environ["GITHUB_REPOSITORY"])
    except RuntimeError as e:
        print(f"::error title=Board::{e}")
        return 1
    for change in changes:
        print("board:", *change)
    return 0


if __name__ == "__main__":
    sys.exit(main())
