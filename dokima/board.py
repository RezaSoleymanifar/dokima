"""Keep the project board's Status, Action ("Needs you" or "Autopilot") and Priority current, from GitHub events.

Priority is Blocker on an open issue that blocks another open issue, read from GitHub's blocked-by links when an issue
closes or reopens and every 15 minutes on schedule; otherwise it follows the high or parked label.

    python3 -m dokima.board     # reads GITHUB_EVENT_NAME, GITHUB_EVENT_PATH and DOKIMA_BOARD ("org/number")

Without DOKIMA_BOARD the sync does nothing. Rules live in decide(); everything else is plumbing.
"""
import json
import os
import re
import subprocess
import sys

from dokima import agent, manifest, plan

CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.I)
YOUR_TURN = ("Plan written above", "**Planner question**", "**Plan rejected:**")
PRIORITY = {"high": "High", "parked": "Parked"}  # highest first; Blocker comes from blocked-by links, not a label
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
        # A closed issue never waits on the owner, whatever a late comment says.
        if p["comment"]["user"]["type"] == "Bot" and p["comment"]["body"].startswith(YOUR_TURN) and p["issue"].get("state") != "closed":
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
            out.append(("pr", pr["number"], "Review", False))
    return out


def keeps(event, p):
    """True when the event leaves a Needs you as it is.

    A new commit, finished checks or a review answer nothing; a review's command clears it through answered()."""
    return (event in ("pull_request", "pull_request_target") and p["action"] == "synchronize") \
        or event in ("workflow_run", "pull_request_review")


def answered(event, p, owners):
    """[(kind, number)] whose Needs you a code owner's command answers.

    The issue or pull request it was said on and the one it pairs with (an issue's open pull request is found later,
    on the board). An Approve, a bot, anyone else or no command answers nothing."""
    if event == "issue_comment" and p["action"] == "created":
        who, body, issue = p["comment"]["user"], p["comment"]["body"], p["issue"]
        if issue.get("pull_request"):
            out = [("pr", issue["number"])] + [("issue", n) for n in linked(issue.get("body"))]
        else:
            out = [("issue", issue["number"])]
    elif event == "pull_request_review" and p["action"] == "submitted" and p["review"]["state"].lower() != "approved":
        who, body, pr = p["review"].get("user") or {}, p["review"].get("body"), p["pull_request"]
        n = agent.issue_of_pr((pr.get("head") or {}).get("ref"), pr.get("body"))
        out = [("pr", pr["number"])] + ([("issue", int(n))] if n else [])
    else:
        return []
    if who.get("type") == "Bot" or who.get("login") not in owners or not agent.command_of(body):
        return []
    return out


def priority(event, p):
    """(number, option) when a priority label was added or removed: the highest priority label left, or None to clear."""
    if event != "issues" or p["action"] not in ("labeled", "unlabeled") or p["label"]["name"] not in PRIORITY:
        return None
    names = {label["name"] for label in p["issue"].get("labels") or []}
    return p["issue"]["number"], label_priority(names)


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

    def labels(self, kind, number):
        """The names of the labels the issue or PR carries."""
        field = "issue" if kind == "issue" else "pullRequest"
        node = self.q(f'query($o:String!,$r:String!,$n:Int!){{repository(owner:$o,name:$r){{{field}(number:$n){{labels(first:100){{nodes{{name}}}}}}}}}}', o=self.repo_owner, r=self.repo_name, n=int(number))["repository"][field]
        return {label["name"] for label in node["labels"]["nodes"]}

    def autopilot(self, kind, number):
        """Whether the issue or PR carries the autopilot label."""
        return AUTOPILOT in self.labels(kind, number)

    def dependencies(self, number, side):
        """[{number, state}] of the issues this one blocks ("blocking") or is blocked by ("blocked_by"); raises
        subprocess.CalledProcessError when GitHub refuses, never answering none."""
        out, page = [], 1
        while True:
            got = self.rest("GET", f"repos/{self.repo_owner}/{self.repo_name}/issues/{number}/dependencies/{side}?per_page=100&page={page}")
            out += [{"number": i["number"], "state": i["state"]} for i in got]
            if len(got) < 100:
                return out
            page += 1

    def blocking(self, number):
        return self.dependencies(number, "blocking")

    def blocked_by(self, number):
        return self.dependencies(number, "blocked_by")

    def open_issues(self):
        """The numbers of every open issue in the repo, pull requests left out."""
        out, page = [], 1
        while True:
            got = self.rest("GET", f"repos/{self.repo_owner}/{self.repo_name}/issues?state=open&per_page=100&page={page}")
            out += [i["number"] for i in got if "pull_request" not in i]
            if len(got) < 100:
                return out
            page += 1

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

    def state(self, kind, number):
        """"open" or "closed" (a merged pull request is closed); raises subprocess.CalledProcessError when GitHub cannot say."""
        # The issues API answers for pull requests too.
        return "closed" if self.rest("GET", f"repos/{self.repo_owner}/{self.repo_name}/issues/{int(number)}").get("state") == "closed" else "open"

    def cards(self):
        """Every issue and pull request card on the board; drafts are skipped.

        Each is {kind, number, action, closed, autopilot}; a merged pull request counts as closed."""
        out, cursor = [], None
        while True:
            more = {"c": cursor} if cursor else {}
            items = self.q('query($o:String!,$n:Int!,$c:String){organization(login:$o){projectV2(number:$n){items(first:100,after:$c){pageInfo{hasNextPage endCursor} nodes{fieldValueByName(name:"Action"){... on ProjectV2ItemFieldSingleSelectValue{name}} content{__typename ... on Issue{number state labels(first:100){nodes{name}}} ... on PullRequest{number state labels(first:100){nodes{name}}}}}}}}}', o=self.owner, n=self.number, **more)["organization"]["projectV2"]["items"]
            for it in items["nodes"]:
                c = it.get("content") or {}
                if c.get("__typename") not in ("Issue", "PullRequest"):
                    continue
                out.append({"kind": "issue" if c["__typename"] == "Issue" else "pr", "number": c["number"],
                            "action": (it.get("fieldValueByName") or {}).get("name"), "closed": c["state"] != "OPEN",
                            "autopilot": AUTOPILOT in {label["name"] for label in c["labels"]["nodes"]}})
            if not items["pageInfo"]["hasNextPage"]:
                return out
            cursor = items["pageInfo"]["endCursor"]

    def views(self):
        return [v["name"] for v in self.view_nodes()]

    def view_nodes(self):
        """The board's views, each as {id, name, filter}."""
        p = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){views(first:50){nodes{id name filter}}}}}', o=self.owner, n=self.number)["organization"]["projectV2"]
        return p["views"]["nodes"]

    def set_view_filter(self, view_id, filter):
        self.q('mutation($v:ID!,$f:String!){updateProjectV2View(input:{viewId:$v,filter:$f}){projectV2View{id}}}', v=view_id, f=filter)

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


def fix_view(board):
    """Move an Autopilot view still on label:autopilot to the manifest's filter; others are the owner's."""
    new = manifest.VIEWS["Autopilot"]["filter"]
    try:
        for v in board.view_nodes():
            if v["name"] == "Autopilot" and v.get("filter") == f"label:{AUTOPILOT}":
                board.set_view_filter(v["id"], new)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Could not fix the Autopilot view's filter to {new}: {(e.stderr or str(e)).strip()}") from e


<<<<<<< HEAD
def sweep(board, repo, owners):
    """Set every card's pill on the board by the rules.

    Needs you where its issue waits on the owner (the river's last word stopped for the owner and no code owner has
    answered with a command since; a pull request follows its issue), else Autopilot on autopilot, else none. A card
    whose history cannot be read keeps its pill, and the run fails naming it."""
    cards = board.cards()
    labels = {c["number"]: c["autopilot"] for c in cards if c["kind"] == "issue"}
    waits, unread = {}, []

    def waiting(n):
        if n not in waits:
            d, items = agent.conversation(repo, n)
            on = (lambda: labels[n]) if n in labels else (lambda: board.autopilot("issue", n))
            waits[n] = agent.waits_on_owner(items, owners, on, d.get("body") or "", str(n))
        return waits[n]

    for c in cards:
        kind, n = c["kind"], c["number"]
        try:
            if c["closed"]:
                needs = False
            elif kind == "issue":
                needs = waiting(n)
            else:
                p = json.loads(agent.gh("pr", "view", str(n), "-R", repo, "--json", "headRefName,body"))
                issue = agent.issue_of_pr(p.get("headRefName"), p.get("body"))
                needs = bool(issue) and waiting(int(issue))
        except (subprocess.CalledProcessError, ValueError) as e:
            unread.append(f"{'PR ' if kind == 'pr' else ''}#{n} ({(getattr(e, 'stderr', None) or str(e)).strip()})")
            continue
        pill = "Needs you" if needs else "Autopilot" if c["autopilot"] else None
        if pill != c["action"]:
            board.set(board.item(kind, n), "Action", pill)
    if unread:
        raise RuntimeError(f"Could not read the history of {', '.join(unread)}, so the board left its pill as it was.")
=======
def label_priority(labels):
    """The pill the highest priority label gives, or None."""
    return next((option for label, option in PRIORITY.items() if label in labels), None)


def blockers(event, p):
    """What may have moved a Blocker pill, or None.

    "all" on schedule, or (number, state) of the issue that closed or reopened."""
    if event == "schedule":
        return "all"
    if event == "issues" and p["action"] in ("closed", "reopened"):
        return p["issue"]["number"], "closed" if p["action"] == "closed" else "open"
    return None


def recompute(board, touched):
    """Set Blocker on open issues blocking an open issue, else the label's pill.

    Writes only pills that change: every open issue for "all", else the issue that closed or reopened and the issues
    blocking it. An issue whose links GitHub will not list keeps its pill; the rest are still set, then the run fails naming it."""
    failed = []

    def refused(n, e):
        failed.append(f"#{n}: {(e.stderr or str(e)).strip()}")

    if touched == "all":
        todo = {n: "open" for n in board.open_issues()}
    else:
        n, state = touched
        todo = {n: state}
        try:
            todo.update((m["number"], m["state"]) for m in board.blocked_by(n))
        except subprocess.CalledProcessError as e:
            refused(n, e)
    for n, state in todo.items():
        try:
            blocks = state == "open" and any(m["state"] == "open" for m in board.blocking(n))
        except subprocess.CalledProcessError as e:
            refused(n, e)
            continue
        want = "Blocker" if blocks else label_priority(board.labels("issue", n))
        iid = board.item("issue", n)
        if board.value(iid, "Priority") != want:
            board.set(iid, "Priority", want)
    if failed:
        raise RuntimeError("Could not list the blocked-by links of " + "; ".join(failed) + "; their pills were left as they are")
>>>>>>> origin/main


def sync(event, payload, spec, repo, q=gql, rest=api):
    changes, pill = decide(event, payload), priority(event, payload)
    on_off, pr = switched(event, payload), opened(event, payload)
<<<<<<< HEAD
    owners = plan.repo_approvers(repo.split("/")[0]) if spec and event in ("issue_comment", "pull_request_review") else set()
    answers = answered(event, payload, owners)
    merged = event in ("pull_request", "pull_request_target") and payload["action"] == "closed" and payload["pull_request"].get("merged")
    if not spec or not (changes or pill or on_off or answers):
=======
    touched = blockers(event, payload)
    if not spec or not (changes or pill or on_off or touched is not None):
>>>>>>> origin/main
        return []
    board = Board(spec, repo, q, rest)
    if pr and any(board.autopilot("issue", n) for n in pr[1]) and not board.autopilot("pr", pr[0]):
        # A pull request built for an issue on autopilot carries the label too, so the Autopilot view lists it.
        board.label("pr", pr[0], True)
    keep = keeps(event, payload)
    for kind, number, status, needs_you in changes:
        iid = board.item(kind, number)
        board.set(iid, "Status", status)
        shown = action(board, kind, number, needs_you)
        if keep and shown != "Needs you" and board.value(iid, "Action") == "Needs you":
            # A Needs you the river set stays until the owner answers or the item closes.
            continue
        board.set(iid, "Action", shown)
    for kind, number in answers + [("pr", board.open_pr(n)) for k, n in answers if k == "issue"]:
        if number:
            # The owner answered: the pill clears on both cards at once, and the card stays in its column.
            board.set(board.item(kind, number), "Action", action(board, kind, number, False))
    if pill and "Priority" in board.fields:
        # A label never takes Blocker away: only the links do, on the next close, reopen or scheduled run.
        number, option = pill
        iid = board.item("issue", number)
        if board.value(iid, "Priority") != "Blocker":
            board.set(iid, "Priority", option)
    if on_off:
        switch(board, on_off)
    if merged:
        # An old Autopilot view is fixed on the next merge, after the merged cards have moved; then every pill is swept.
        fix_view(board)
<<<<<<< HEAD
        sweep(board, repo, plan.repo_approvers(repo.split("/")[0]))
=======
    if touched is not None and "Priority" in board.fields:
        recompute(board, touched)
>>>>>>> origin/main
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
