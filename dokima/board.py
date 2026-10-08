"""Keep the project board's Status and Action ("Needs you") current, from GitHub events.

    python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")

Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing. Every run then
recomputes each card's Needs you from its latest record; run by hand (workflow_dispatch, the board's "Run workflow"
button) it also puts every card back in the column its real state says.
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
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)["data"]


class Board:
    def __init__(self, spec, repo, q=gql):
        self.q = q
        owner, number = spec.split("/")
        self.repo_owner, self.repo_name = repo.split("/")
        p = q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}', o=owner, n=int(number))["organization"]["projectV2"]
        self.id, self.login, self.number = p["id"], owner, int(number)
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

    def cards(self):
        """Every issue and pull request of this repo on the board: {iid, kind, number, closed, head, body, Status, Action}."""
        query = ('query($o:String!,$n:Int!,$after:String){organization(login:$o){projectV2(number:$n){items(first:100,after:$after){'
                 'nodes{id content{__typename ... on Issue{number state repository{nameWithOwner}} '
                 '... on PullRequest{number state headRefName body repository{nameWithOwner}}} '
                 'fieldValues(first:20){nodes{... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2SingleSelectField{name}}}}}} '
                 'pageInfo{hasNextPage endCursor}}}}}')
        repo, out, after = f"{self.repo_owner}/{self.repo_name}", [], None
        while True:
            page = self.q(query, o=self.login, n=self.number, **({"after": after} if after else {}))["organization"]["projectV2"]["items"]
            for it in page["nodes"]:
                c = it.get("content") or {}
                if c.get("__typename") not in ("Issue", "PullRequest") or (c.get("repository") or {}).get("nameWithOwner") != repo:
                    continue
                values = {(v.get("field") or {}).get("name"): v.get("name") for v in it["fieldValues"]["nodes"] if v}
                out.append({"iid": it["id"], "kind": "issue" if c["__typename"] == "Issue" else "pr", "number": c["number"],
                            "closed": c["state"] != "OPEN", "head": c.get("headRefName", ""), "body": c.get("body", ""),
                            "Status": values.get("Status"), "Action": values.get("Action")})
            if not page["pageInfo"]["hasNextPage"]:
                return out
            after = page["pageInfo"]["endCursor"]

    def describe(self, link):
        """Add the link to the board's description, after whatever the owner wrote there, unless it is there already."""
        text = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){shortDescription}}}',
                      o=self.login, n=self.number)["organization"]["projectV2"].get("shortDescription") or ""
        if link in text:
            return False
        text = f"{text.rstrip()} · Refresh the board: {link}" if text.strip() else f"Refresh the board: {link}"
        self.q('mutation($p:ID!,$d:String!){updateProjectV2(input:{projectId:$p,shortDescription:$d}){projectV2{id}}}', p=self.id, d=text)
        return True


def river_place(items):
    """Where the river put an issue after its latest record: (column, needs_you). No record is Backlog.

    Only records the bot posted count; what follows that record is decided as the river decided it, from the
    conversation before it."""
    from dokima import agent
    at = next((i for i in range(len(items) - 1, -1, -1) if agent.is_record(items[i])), None)
    if at is None:
        return "Backlog", False
    rec = agent.records([items[at]])[0]
    if rec.get("role") == "split":
        return "Work", False
    return agent.board_place(rec, agent.next_step(items[:at], rec, owners()))


def owners():
    """The people whose words count: OWNERS when the workflow set it, else the approvers in CODEOWNERS."""
    from dokima import plan
    named = [o for o in os.environ.get("OWNERS", "").split(",") if o]
    return named or sorted(plan.repo_approvers(os.environ.get("GITHUB_REPOSITORY_OWNER", "")))


def refresh(board, repo, columns=True):
    """Recompute every card's Needs you from its latest record, and with columns its Status from its real state too.

    Closed or merged is Done and never needs you; an open issue goes where the river put it after its latest record;
    an open pull request goes with the issue it was built for, or to Review when it was built for none."""
    from dokima import agent
    places, changed = {}, []

    def issue_place(n):
        if n not in places:
            places[n] = river_place(agent.conversation(repo, n)[1])
        return places[n]

    for c in board.cards():
        if c["closed"]:
            column, needs = "Done", False
        elif c["kind"] == "issue":
            column, needs = issue_place(c["number"])
        else:
            n = agent.issue_of_pr(c["head"], c["body"])
            column, needs = issue_place(int(n)) if n else ("Review", False)
        status, action = column if columns else c["Status"], "Needs you" if needs else None
        if columns and status != c["Status"]:
            board.set(c["iid"], "Status", status)
        if action != c["Action"]:
            board.set(c["iid"], "Action", action)
        if (columns and status != c["Status"]) or action != c["Action"]:
            changed.append((c["kind"], c["number"], status, needs))
    return changed


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
    event, repo = os.environ["GITHUB_EVENT_NAME"], os.environ["GITHUB_REPOSITORY"]
    payload = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
    for change in sync(event, payload, spec, repo):
        print("board:", *change)
    b = Board(spec, repo)
    if b.describe(f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/workflows/board.yml"):
        print("board: the description now links to the refresh button")
    # The button (workflow_dispatch) puts every card back in its column; every other run recounts the pills.
    for change in refresh(b, repo, columns=event == "workflow_dispatch"):
        print("board: refresh", *change)
    return 0


if __name__ == "__main__":
    sys.exit(main())
