"""Keep the project board's Status, Action ("Needs you" or "Autopilot") and Priority current, from GitHub events.

    python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")

Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing.
"""
import json
import os
import re
import subprocess
import sys

from dokima import manifest

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


def gql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)["data"]


def api(method, path, **fields):
    """One REST call; raises subprocess.CalledProcessError when GitHub refuses it."""
    args = ["gh", "api", "-X", method, path]
    for k, v in fields.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
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
        """The card's current option of that field, or None."""
        node = self.q('query($i:ID!,$f:String!){node(id:$i){... on ProjectV2Item{fieldValueByName(name:$f){... on ProjectV2ItemFieldSingleSelectValue{name}}}}}', i=iid, f=field)["node"]
        return ((node or {}).get("fieldValueByName") or {}).get("name")

    def autopilot(self, kind, number):
        """Whether the issue or PR carries the autopilot label."""
        field = "issue" if kind == "issue" else "pullRequest"
        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{labels(first:100){{nodes{{name}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=int(number))["repository"][field]
        return AUTOPILOT in {label["name"] for label in node["labels"]["nodes"]}

    def open_pr(self, number):
        """The open pull request built for the issue (from its try branch), or None."""
        nodes = self.q('query($o:String!,$r:String!,$h:String!){repository(owner:$o,name:$r){pullRequests(headRefName:$h,states:[OPEN],first:1){nodes{number}}}}', o=self.repo_owner, r=self.repo_name, h=f"try/issue-{number}")["repository"]["pullRequests"]["nodes"]
        return nodes[0]["number"] if nodes else None

    def parent(self, number):
        """The issue's parent issue, or None."""
        up = self.q('query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){parent{number}}}}', o=self.repo_owner, r=self.repo_name, n=int(number))["repository"]["issue"].get("parent")
        return up["number"] if up else None

    def label(self, kind, number, on):
        """Put the autopilot label on or off the issue or PR, leaving its other labels alone."""
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


def action(board, kind, number, needs_you):
    """The Action pill: Needs you when the river stops for the owner, else Autopilot while on autopilot, else none."""
    return "Needs you" if needs_you else "Autopilot" if board.autopilot(kind, number) else None


def switched(event, p):
    """The issue number when its autopilot label was added or removed, else None."""
    if event == "issues" and p["action"] in ("labeled", "unlabeled") and p["label"]["name"] == AUTOPILOT:
        return p["issue"]["number"]
    return None


def opened(event, p):
    """(PR number, linked issues) when a pull request opened or reopened, else None."""
    if event in ("pull_request", "pull_request_target") and p["action"] in ("opened", "reopened"):
        return p["pull_request"]["number"], linked(p["pull_request"].get("body"))
    return None


def switch(board, number):
    """Follow the issue's autopilot label on its card, its open PR's card and the PR's label, never touching Needs you;
    then, at the top of what was switched on, add the Autopilot view if the board has none."""
    on = board.autopilot("issue", number)
    pr = board.open_pr(number)
    for kind, n in [("issue", number)] + ([("pr", pr)] if pr else []):
        iid = board.item(kind, n)
        current = board.value(iid, "Action")
        if current != "Needs you" and current != ("Autopilot" if on else None):
            board.set(iid, "Action", "Autopilot" if on else None)
    if pr and board.autopilot("pr", pr) != on:
        board.label("pr", pr, on)
    if not on:
        return
    # Only the top of a tree switched on adds the view: its sub-issues' board runs may overlap it and read no view yet.
    up = board.parent(number)
    if up and board.autopilot("issue", up):
        return
    try:
        if "Autopilot" not in board.views():
            view = manifest.VIEWS["Autopilot"]
            board.add_view("Autopilot", view["layout"], view["filter"])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not add the Autopilot view to the board: {(e.stderr or str(e)).strip()}") from e


def sync(event, payload, spec, repo, q=gql, rest=api):
    changes, pill = decide(event, payload), priority(event, payload)
    on_off, pr = switched(event, payload), opened(event, payload)
    if not spec or not (changes or pill or on_off):
        return []
    board = Board(spec, repo, q, rest)
    if pr and any(board.autopilot("issue", n) for n in pr[1]) and not board.autopilot("pr", pr[0]):
        # A pull request built for an issue on autopilot carries the label too, so the Autopilot view lists it.
        board.label("pr", pr[0], True)
    for kind, number, status, needs_you in changes:
        iid = board.item(kind, number)
        board.set(iid, "Status", status)
        board.set(iid, "Action", action(board, kind, number, needs_you))
    if pill and "Priority" in board.fields:
        number, option = pill
        board.set(board.item("issue", number), "Priority", option)
    if on_off:
        switch(board, on_off)
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
        print(f"::error::{e}")
        return 1
    for change in changes:
        print("board:", *change)
    return 0


if __name__ == "__main__":
    sys.exit(main())
