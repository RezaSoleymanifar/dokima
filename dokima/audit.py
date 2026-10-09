"""Compare the repo's live settings with the manifest; report drift on one pinned Setup issue.

    python3 -m dokima.audit OWNER/REPO   # reads DOKIMA_BOARD ("org/number") and .github/CODEOWNERS where it runs

compare() gives one plain line per setting that differs from dokima/manifest.py or could not be read. run() first sets
each declared label, board option and view that differs to the manifest's (never a whole missing field, a branch rule
or an app permission, which it only reports), then puts what is still off on the Setup issue (opened, pinned and marked
Needs you, or updated) followed by what it fixed. When nothing is left off it lists the fixes, if any, and closes the
Setup issue with one line; it writes nothing when nothing was off and none is open. Both take a GitHub object for every
read and write; GitHub below is the real one, through gh.
"""
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote

from dokima import board, manifest

TITLE = "Setup"
MARK = "<!-- dokima-setup -->"
NOTHING_OFF = "Nothing is off: every setting matches what Dokima needs."
RANK = {"read": 1, "write": 2, "admin": 3}
FAILED = (subprocess.CalledProcessError, RuntimeError)


def reason(e):
    """GitHub's reason for refusing a call, on one line."""
    if isinstance(e, subprocess.CalledProcessError):
        said = " ".join(str(e.stderr or "").split())
        return re.sub(r"^gh:\s*", "", said) or f"gh exited with {e.returncode}"
    return " ".join(str(e).split())


def unverified(what, e):
    return f"{what} could not be verified: GitHub said `{reason(e)}`."


def label_lines(name, want, have):
    if have is None:
        return [f"Label `{name}` is missing; Dokima needs it with color `{want['color']}` and description "
                f"`{want['description']}`."]
    lines = []
    if (have.get("color") or "").lower() != want["color"].lower():
        lines.append(f"Label `{name}` has color `{have.get('color')}`; Dokima needs `{want['color']}`.")
    if (have.get("description") or "") != want["description"]:
        lines.append(f"Label `{name}` has description `{have.get('description') or ''}`; Dokima needs "
                     f"`{want['description']}`.")
    return lines


def compare_labels(live):
    return [l for name, want in manifest.LABELS.items() for l in label_lines(name, want, live.get(name))]


def missing_field(field, options):
    return [f"Board field `{field}` is missing; Dokima needs it with the options "
            + ", ".join(f"`{o}` ({v['color']})" for o, v in options.items()) + "."]


def option_lines(field, option, want, have):
    if have is None:
        return [f"Option `{option}` of the board field `{field}` is missing; Dokima needs it with color "
                f"`{want['color']}` and description `{want['description']}`."]
    lines = []
    if (have.get("color") or "").upper() != want["color"].upper():
        lines.append(f"Option `{option}` of the board field `{field}` has color `{have.get('color')}`; "
                     f"Dokima needs `{want['color']}`.")
    if (have.get("description") or "") != want["description"]:
        lines.append(f"Option `{option}` of the board field `{field}` has description "
                     f"`{have.get('description') or ''}`; Dokima needs `{want['description']}`.")
    return lines


def field_lines(field, options, have_options):
    return [l for option, want in options.items() for l in option_lines(field, option, want, have_options.get(option))]


def compare_fields(live):
    lines = []
    for field, options in manifest.FIELDS.items():
        have_options = live.get(field)
        lines += missing_field(field, options) if have_options is None else field_lines(field, options, have_options)
    return lines


def view_lines(view, want, have):
    if have is None:
        return [f"View `{view}` is missing on the board; Dokima needs a `{want['layout']}` view filtered to "
                f"`{want['filter']}`."]
    lines = []
    if (have.get("layout") or "").lower() != want["layout"].lower():
        lines.append(f"View `{view}` has layout `{have.get('layout')}`; Dokima needs `{want['layout']}`.")
    if (have.get("filter") or "") != want["filter"]:
        lines.append(f"View `{view}` has filter `{have.get('filter') or ''}`; Dokima needs `{want['filter']}`.")
    return lines


def compare_views(live):
    return [l for view, want in manifest.VIEWS.items() for l in view_lines(view, want, live.get(view))]


def compare_rule(branch, live, want):
    needed = want["required_checks"]
    if live is None:
        return [f"Branch `{branch}` has no rule; Dokima needs one requiring "
                + " and ".join(f"`{c}`" for c in needed) + "."]
    have = live.get("required_checks") or []
    return ([f"Branch rule of `{branch}` does not require `{c}`; Dokima needs it required." for c in needed
             if c not in have]
            + [f"Branch rule of `{branch}` requires `{c}`, a check Dokima does not declare." for c in have
               if c not in needed])


def compare_permissions(live):
    lines = []
    for perm, want in manifest.PERMISSIONS.items():
        have = live.get(perm)
        if have is None:
            lines.append(f"App permission `{perm}` is missing; Dokima needs `{want}`.")
        elif RANK.get(have, 0) < RANK[want]:
            lines.append(f"App permission `{perm}` is `{have}`; Dokima needs `{want}`.")
        elif RANK.get(have, 0) > RANK[want]:
            lines.append(f"App permission `{perm}` is `{have}`, broader than the `{want}` Dokima needs.")
    for perm, have in live.items():
        if perm not in manifest.PERMISSIONS:
            lines.append(f"App permission `{perm}` is `{have}`, broader than Dokima needs: it needs none.")
    return lines


def reads(github, repo):
    """(what, read, check) for every setting compared, in the order of its lines."""
    out = [("Labels", lambda: github.labels(repo), compare_labels),
           ("Board fields", github.fields, compare_fields),
           ("Board views", github.views, compare_views)]
    out += [(f"Branch rule of `{branch}`", lambda branch=branch: github.branch_rule(repo, branch),
             lambda rule, branch=branch, want=want: compare_rule(branch, rule, want))
            for branch, want in manifest.BRANCH_RULES.items()]
    out += [("App permissions", lambda: github.permissions(repo), compare_permissions)]
    return out


def compare(github, repo):
    """One line per setting that differs from the manifest or could not be read."""
    lines = []
    for what, read, check in reads(github, repo):
        try:
            live = read()
        except FAILED as e:
            lines.append(unverified(what, e))
            continue
        lines += check(live)
    return lines


def fix_labels(github, repo, live, attempt):
    for name, want in manifest.LABELS.items():
        have = live.get(name)
        write = github.create_label if have is None else github.update_label
        attempt(label_lines(name, want, have), lambda: write(repo, name, want["color"], want["description"]))


def fix_fields(github, repo, live, attempt):
    """Set each declared field's options to the manifest's, adding missing ones.

    Every option the field has goes back with its id, so it and its cards stay."""
    off = []
    for field, options in manifest.FIELDS.items():
        have = live.get(field)
        if have is None:
            off += missing_field(field, options)
            continue
        new = [{"id": v.get("id"), "name": o, "color": v.get("color"), "description": v.get("description") or ""}
               for o, v in have.items()]
        for o in new:
            want = options.get(o["name"])
            if want:
                o.update(color=want["color"], description=want["description"])
        new += [{"id": None, "name": o, "color": want["color"], "description": want["description"]}
                for o, want in options.items() if o not in have]
        attempt(field_lines(field, options, have), lambda: github.set_options(field, new))
    return off


def fix_views(github, repo, live, attempt):
    for view, want in manifest.VIEWS.items():
        have = live.get(view)
        write = github.create_view if have is None else github.update_view
        attempt(view_lines(view, want, have), lambda: write(view, want["layout"], want["filter"]))


def fix(github, repo):
    """(still off, fixed): compare()'s lines, after setting declared labels, options and views.

    A fix GitHub refuses stays off with GitHub's reason; branch rules and permissions are only read."""
    off, fixed = [], []

    def attempt(lines, write):
        if not lines:
            return
        try:
            write()
        except FAILED as e:
            off.extend(f"{l} The audit could not set it: GitHub said `{reason(e)}`." for l in lines)
        else:
            fixed.extend(lines)

    fixes = {"Labels": fix_labels, "Board fields": fix_fields, "Board views": fix_views}
    for what, read, check in reads(github, repo):
        try:
            live = read()
        except FAILED as e:
            off.append(unverified(what, e))
            continue
        if what in fixes:
            off += fixes[what](github, repo, live, attempt) or []
        else:
            off += check(live)
    return off, fixed


def code_owners(root):
    """The owners of `*` in root/.github/CODEOWNERS; the last `*` line wins, as on GitHub."""
    owners = []
    try:
        text = open(os.path.join(root, ".github", "CODEOWNERS")).read()
    except FileNotFoundError:
        return owners
    for line in text.splitlines():
        parts = line.split("#")[0].split()
        if parts and parts[0] == "*":
            owners = [p for p in parts[1:] if p.startswith("@")]
    return owners


def setup_body(lines, owners, fixed=()):
    body = MARK + "\n"
    if lines:
        who = " ".join(owners) + ", " if owners else ""
        body += (f"{who}the drift audit found settings on this repo that differ from what Dokima needs, or that it "
                 f"could not verify:\n\n" + "".join(f"- {l}\n" for l in lines) + "\n")
    if fixed:
        body += ("The drift audit fixed these settings itself, setting each to what Dokima needs:\n\n"
                 + "".join(f"- {l}\n" for l in fixed) + "\n")
    return body + "Each audit updates this issue, and closes it once nothing is off.\n"


def run(github, repo, root="."):
    """Fix what it may, report on the Setup issue; returns the issue touched, or None."""
    lines, fixed = fix(github, repo)
    issue = github.setup_issue(repo)
    if not lines:
        if issue is None and not fixed:
            return None
        if issue is None:
            n = github.create_issue(repo, TITLE, setup_body(lines, [], fixed))
        else:
            n = issue["number"]
            if fixed:
                github.edit_issue(repo, n, setup_body(lines, [], fixed))
        github.comment(repo, n, NOTHING_OFF)
        github.close_issue(repo, n)
        return n
    body = setup_body(lines, code_owners(root), fixed)
    if issue is None:
        n = github.create_issue(repo, TITLE, body)
        github.pin_issue(repo, n)
    else:
        n = issue["number"]
        if issue["body"] != body:
            github.edit_issue(repo, n, body)
    github.needs_you(repo, n)
    return n


def gh(*args):
    """gh's output; raises subprocess.CalledProcessError, with GitHub's reason in stderr, when GitHub refuses."""
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def graphql(query, **variables):
    """One GraphQL call with its variables as JSON; raises subprocess.CalledProcessError when GitHub refuses it."""
    body = json.dumps({"query": query, "variables": variables})
    return subprocess.run(["gh", "api", "graphql", "--input", "-"], input=body, check=True, capture_output=True,
                          text=True).stdout


def pages(out):
    """Every item of a paginated REST list (gh prints one JSON array per page)."""
    decoder, items, i, out = json.JSONDecoder(), [], 0, out.strip()
    while i < len(out):
        page, i = decoder.raw_decode(out, i)
        items += page
        while i < len(out) and out[i].isspace():
            i += 1
    return items


BOARD_QUERY = 'query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id fields(first:50){nodes{... on ProjectV2SingleSelectField{id name options{id name color description}}}} views(first:50){nodes{id name layout filter}}}}}'


class GitHub:
    """The live repo and board, read and written through gh."""

    def __init__(self, spec):
        self.spec = spec
        self.owner, number = spec.split("/")
        self.number = int(number)
        self.project = None

    def board(self):
        if self.project is None:
            p = board.gql(BOARD_QUERY, o=self.owner, n=self.number)["organization"]["projectV2"]
            if p is None:
                raise RuntimeError(f"no board {self.spec}")
            self.project = p
        return self.project

    def labels(self, repo):
        return {l["name"]: {"color": l["color"], "description": l.get("description") or ""}
                for l in pages(gh("api", "--paginate", f"repos/{repo}/labels?per_page=100"))}

    def fields(self):
        return {f["name"]: {o["name"]: {"color": o.get("color"), "description": o.get("description") or "", "id": o["id"]}
                            for o in f["options"]}
                for f in self.board()["fields"]["nodes"] if f and "options" in f}

    def views(self):
        return {v["name"]: {"layout": re.sub(r"_LAYOUT$", "", v.get("layout") or "").lower(),
                            "filter": v.get("filter") or ""}
                for v in self.board()["views"]["nodes"]}

    def branch_rule(self, repo, branch):
        try:
            rule = json.loads(gh("api", f"repos/{repo}/branches/{branch}/protection"))
        except subprocess.CalledProcessError as e:
            if "Branch not protected" in f"{e.stderr} {e.stdout}":
                return None
            raise
        checks = rule.get("required_status_checks") or {}
        return {"required_checks": checks.get("contexts") or [c["context"] for c in checks.get("checks") or []]}

    def permissions(self, repo):
        return json.loads(gh("api", f"repos/{repo}/installation"))["permissions"]

    def setup_issue(self, repo):
        listed = json.loads(gh("issue", "list", "--repo", repo, "--state", "open", "--limit", "1000", "--json",
                               "number,title,body"))
        found = sorted((i for i in listed if MARK in (i.get("body") or "")), key=lambda i: i["number"])
        return {"number": found[0]["number"], "body": found[0]["body"]} if found else None

    def create_issue(self, repo, title, body):
        url = gh("issue", "create", "--repo", repo, "--title", title, "--body", body)
        return int(re.search(r"(\d+)\s*$", url).group(1))

    def edit_issue(self, repo, n, body):
        gh("issue", "edit", str(n), "--repo", repo, "--body", body)

    def comment(self, repo, n, text):
        gh("issue", "comment", str(n), "--repo", repo, "--body", text)

    def close_issue(self, repo, n):
        gh("issue", "close", str(n), "--repo", repo)

    def pin_issue(self, repo, n):
        gh("issue", "pin", str(n), "--repo", repo)

    def create_label(self, repo, name, color, description):
        gh("api", "-X", "POST", f"repos/{repo}/labels", "-f", f"name={name}", "-f", f"color={color}",
           "-f", f"description={description}")

    def update_label(self, repo, name, color, description):
        gh("api", "-X", "PATCH", f"repos/{repo}/labels/{quote(name, safe='')}", "-f", f"color={color}",
           "-f", f"description={description}")

    def set_options(self, field, options):
        """Replace the field's options; one passed with its id keeps its cards."""
        fid = {f["name"]: f["id"] for f in self.board()["fields"]["nodes"] if f and "options" in f}[field]
        given = [{**({"id": o["id"]} if o.get("id") else {}), "name": o["name"], "color": o["color"],
                  "description": o["description"]} for o in options]
        graphql('mutation($f:ID!,$o:[ProjectV2SingleSelectFieldOptionInput!]){updateProjectV2Field(input:{fieldId:$f,singleSelectOptions:$o}){projectV2Field{... on ProjectV2SingleSelectField{id}}}}', f=fid, o=given)

    def create_view(self, name, layout, filter):
        gh("api", "-X", "POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", "-f", f"name={name}",
           "-f", f"layout={layout}", "-f", f"filter={filter}")

    def update_view(self, name, layout, filter):
        """Set the view's filter, and its layout only when that differs."""
        view = {v["name"]: v for v in self.board()["views"]["nodes"]}[name]
        if re.sub(r"_LAYOUT$", "", view.get("layout") or "").lower() != layout.lower():
            graphql('mutation($v:ID!,$l:ProjectV2ViewLayout!,$f:String!){updateProjectV2View(input:{viewId:$v,layout:$l,filter:$f}){projectV2View{id}}}', v=view["id"], l=f"{layout.upper()}_LAYOUT", f=filter)
        else:
            graphql('mutation($v:ID!,$f:String!){updateProjectV2View(input:{viewId:$v,filter:$f}){projectV2View{id}}}', v=view["id"], f=filter)

    def needs_you(self, repo, n):
        b = board.Board(self.spec, repo)
        b.set(b.item("issue", n), "Action", "Needs you")


def main(argv):
    if len(argv) != 1 or argv[0].count("/") != 1:
        print("usage: python3 -m dokima.audit OWNER/REPO", file=sys.stderr)
        return 2
    spec = os.environ.get("DOKIMA_BOARD", "").strip()
    if not spec:
        print("::error::No DOKIMA_BOARD set; the audit needs the board to check it and mark the Setup issue.")
        return 1
    try:
        n = run(GitHub(spec), argv[0])
    except FAILED as e:
        print(f"::error::The audit could not report on the Setup issue: {reason(e)}")
        return 1
    print(f"Setup issue: #{n}" if n else "Nothing is off.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
