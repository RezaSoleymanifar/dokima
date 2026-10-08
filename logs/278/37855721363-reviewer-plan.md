# reviewer (plan) for #278

Run: https://github.com/dokima-dev/dokima/actions/runs/37855721363

`1. Bash`
```
cat /tmp/pack/issue.md; ls /tmp/pack/in; cat /tmp/pack/open_blockers.json; cat /tmp/pack/plan.json
```

> # Issue #278: The Autopilot view shows only open issues and pull requests
> 
> <!-- dokima-card -->
> **Backlog**
> 
> This issue has no plan yet.
> 
> **Definition of Done:** <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> All tests · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/code-review.svg" width="16" height="16" align="absmiddle" alt="code review"> Code review · <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/none.svg" width="16" height="16" align="absmiddle" alt="not started"> <img src="https://raw.githubusercontent.com/dokima-dev/dokima/main/dokima/icons/owner-approval.svg" width="16" height="16" align="absmiddle" alt="owner approval"> Owner approval
> 
> <!-- /dokima-card -->
> 
> <!-- dokima-ask -->
> 
> The Autopilot tab on the board still lists pull requests that merged and issues that closed. Its filter is only the autopilot label, and merged or closed items keep that label.
> 
> What I want:
> - The Autopilot view lists only open issues and pull requests on autopilot. Anything merged or closed leaves it.
> - The existing view is fixed too, not only new ones.
> 
> ## Comments
> 
> ### RezaSoleymanifar on issue #278 (2026-10-08T22:27:43Z)
> 
> /autopilot start
> 
> ### dokima-runtime on issue #278 (

`2. Bash`
```
cd /home/runner/work/dokima/dokima; git show --stat HEAD; grep -n -i "view" dokima/board.py | head -80
```

> commit accfe369f8171e1cb25e9a382ff34ab7621a508d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 22:47:54 2026 +0000
> 
>     planner for #278 (run 37853656270)
> 
>  tests/test_autopilot_board.py | 146 ++++++++++++++++++++++++++++++++++++++----
>  1 file changed, 135 insertions(+), 11 deletions(-)
> 41:            out += [(k, n, "Review", False) for k, n in both]
> 44:    elif event == "pull_request_review" and p["action"] == "submitted":
> 46:        if p["review"]["state"].lower() == "changes_requested":
> 50:            out.append(("pr", pr["number"], "Review", True))
> 137:    def views(self):
> 138:        p = self.q('query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){views(first:50){nodes{name}}}}}', o=self.owner, n=self.number)["organization"]["projectV2"]
> 139:        return [v["name"] for v in p["views"]["nodes"]]
> 141:    def add_view(self, name, layout, filter):
> 142:        self.rest("POST", f"orgs/{self.owner}/projectsV2/{self.number}/views", name=name, layout=layout, filter=filter)
> 166:    then, at the top of what was switched on, add the Autopilot view if the board has none."""
> 178:    # Only the top of a tree switched on adds the view: its sub-issues' board runs may overlap it and read no view yet.
> 183:        if "Autopilot" not in board.views():
> 184:            board.add_view("Autopilot", "table", f"label:{AUTOPILOT}")
> 186:        raise RuntimeError(f"Could not add the Autopilot view to the board: {(e.stderr or

`3. Bash`
```
cd /home/runner/work/dokima/dokima; git show HEAD -- tests/test_autopilot_board.py; sed -n 100,200p dokima/board.py
```

> commit accfe369f8171e1cb25e9a382ff34ab7621a508d
> Author: dokima-runtime[bot] <337511017+dokima-runtime[bot]@users.noreply.github.com>
> Date:   Thu Oct 8 22:47:54 2026 +0000
> 
>     planner for #278 (run 37853656270)
> 
> diff --git a/tests/test_autopilot_board.py b/tests/test_autopilot_board.py
> index db8486a..adafe4f 100644
> --- a/tests/test_autopilot_board.py
> +++ b/tests/test_autopilot_board.py
> @@ -22,6 +22,8 @@ What the fake Board offers, and the code is expected to use:
>      .label(kind, n, on)                put the `autopilot` label on (True) or off (False) that issue or pull request
>      .views() -> [name, ...]            the board's views
>      .add_view(name, layout, filter)    add a view to the board
> +    .view(name) -> {"id", "filter"}    the view of that name with its id and filter, or None (#278)
> +    .set_view_filter(view_id, filter)  change that view's filter on GitHub (#278)
>  
>  The fake `gh` answers `pr list` (the issue's open pull request), `issue view` and `api repos/o/r/issues/N` (with
>  labels), `issue create`, sub-issue and blocked-by links, and labels added through `issue create --label`,
> @@ -113,6 +115,13 @@ def fake_board(world):
>          def add_view(self, name, layout, filter):
>              world.view_list.append({"name": name, "layout": layout, "filter": filter})
>  
> +        def view(self, name):
> +            found = next((v for v in world.view_list if v["name"] == name), None)
> +            return {"id": name, "filter": found["filter"]} if found else None
> +
> +    

`4. ToolSearch`
```
{"query": "select:WebSearch,WebFetch", "max_results": 2}
```

> 

`5. WebFetch`
```
{"url": "https://docs.github.com/en/graphql/reference/mutations", "prompt": "List every mutation whose name contains \"ProjectV2\". Is there any mutation to update or delete a ProjectV2 view (e.g. updateProjectV2View)?"}
```

> The page doesn't list any GraphQL mutations, so I can't name any that contain "ProjectV2." It is only an index of reference pages, with a description that says it lets you "learn about the data types available in the GitHub GraphQL API schema."
> 
> It also doesn't mention a `updateProjectV2View` mutation or any other way to update or delete a ProjectV2 view. Its links include a "Projects" page, which may cover ProjectV2 operations, but the content provided doesn't confirm what that page contains.
> 
> To answer both questions, check the mutation reference in the GitHub GraphQL API documentation or run an introspection query against the schema.

**Agent:** I'm checking whether GitHub really offers a way to change a board view's filter, which the plan's fix relies on.

`6. Bash`
```
mkdir -p /tmp/dl && cd /tmp/dl && curl -sL -o schema.graphql https://docs.github.com/public/fpt/schema.docs.graphql; ls -la schema.graphql; grep -n -i "ProjectV2View" schema.graphql | grep -i -E "mutation|input|update|create|delete" | head; grep -n -E "^\s+(create|update|delete)ProjectV2" schema.graphql | head -30
```

> -rw-r--r-- 1 runner runner 1558210 Oct  8 22:48 schema.graphql
> 9225:Autogenerated input type of CreateProjectV2View
> 9227:input CreateProjectV2ViewInput {
> 9236:  configuration: ProjectV2ViewConfigurationInput
> 9255:Autogenerated return type of CreateProjectV2View.
> 9257:type CreateProjectV2ViewPayload {
> 11217:Autogenerated input type of DeleteProjectV2View
> 11219:input DeleteProjectV2ViewInput {
> 11232:Autogenerated return type of DeleteProjectV2View.
> 11234:type DeleteProjectV2ViewPayload {
> 28101:  createProjectV2View(
> 28061:  createProjectV2(
> 28071:  createProjectV2Field(
> 28081:  createProjectV2IssueField(
> 28091:  createProjectV2StatusUpdate(
> 28101:  createProjectV2View(
> 28404:  deleteProjectV2(
> 28414:  deleteProjectV2Field(
> 28424:  deleteProjectV2Item(
> 28434:  deleteProjectV2StatusUpdate(
> 28444:  deleteProjectV2View(
> 28454:  deleteProjectV2Workflow(
> 29930:  updateProjectV2(
> 29940:  updateProjectV2Collaborators(
> 29950:  updateProjectV2DraftIssue(
> 29960:  updateProjectV2Field(
> 29971:  updateProjectV2ItemFieldValue(
> 29981:  updateProjectV2ItemPosition(
> 29991:  updateProjectV2StatusUpdate(
> 30001:  updateProjectV2View(
> Shell cwd was reset to /home/runner/work/dokima/dokima

`7. Bash`
```
cd /tmp/dl; sed -n 29995,30012p schema.graphql; grep -n "input UpdateProjectV2ViewInput" -A 40 schema.graphql; grep -n "^type ProjectV2View " -A 80 schema.graphql | grep -n -E "filter|id:|name:"
```

> input: UpdateProjectV2StatusUpdateInput!
>   ): UpdateProjectV2StatusUpdatePayload @docsCategory(name: "projects")
> 
>   """
>   Updates an existing view in a project.
>   """
>   updateProjectV2View(
>     """
>     Parameters for UpdateProjectV2View
>     """
>     input: UpdateProjectV2ViewInput!
>   ): UpdateProjectV2ViewPayload @docsCategory(name: "projects")
> 
>   """
>   Update a pull request
>   """
>   updatePullRequest(
>     """
> 71170:input UpdateProjectV2ViewInput {
> 71171-  """
> 71172-  A unique identifier for the client performing the mutation.
> 71173-  """
> 71174-  clientMutationId: String
> 71175-
> 71176-  """
> 71177-  The new configuration for the view.
> 71178-  """
> 71179-  configuration: ProjectV2ViewConfigurationInput
> 71180-
> 71181-  """
> 71182-  The new filter for the view.
> 71183-  """
> 71184-  filter: String
> 71185-
> 71186-  """
> 71187-  The new layout for the view.
> 71188-  """
> 71189-  layout: ProjectV2ViewLayout
> 71190-
> 71191-  """
> 71192-  The new name for the view.
> 71193-  """
> 71194-  name: String
> 71195-
> 71196-  """
> 71197-  The ID of the view to update.
> 71198-  """
> 71199-  viewId: ID! @possibleTypes(concreteTypes: ["ProjectV2View"])
> 71200-}
> 71201-
> 71202-"""
> 71203-Autogenerated return type of UpdateProjectV2View.
> 71204-"""
> 71205-type UpdateProjectV2ViewPayload {
> 71206-  """
> 71207-  A unique identifier for the client performing the mutation.
> 71208-  """
> 71209-  clientMutationId: String
> 71210-
> 1:43654:type ProjectV2View implements Node @docsCategory(name: "projects") {
> 51:43704-  The project view's filt

**Agent:** The mutation exists in GitHub's schema (`updateProjectV2View`, with `viewId` and `filter`). Now running the tests.

`8. Bash`
```
cd /home/runner/work/dokima/dokima; python -m pytest -q tests/test_autopilot_board.py 2>&1 | grep -E "FAILED|passed|failed|Error" | head -30
```

> E       AssertionError: 210.4: switching autopilot on added [{'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'}], not one Autopilot table view filtered to label:autopilot is:open
> tests/test_autopilot_board.py:380: AssertionError
> E       AssertionError: 210.4: the Autopilot view is {'id': 'PVTV_1', 'name': 'Autopilot', 'layout': 'TABLE_LAYOUT', 'filter': 'label:autopilot'}
> tests/test_autopilot_board.py:714: AssertionError
> E       AssertionError: 210.4: the top of the tree added {'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'}, not the Autopilot table view filtered to label:autopilot is:open
> tests/test_autopilot_board.py:801: AssertionError
> E       AssertionError: 278.1: switching autopilot on sent [('POST', 'orgs/dokima-dev/projectsV2/1/views', {'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'})], not one Autopilot table view filtered to label:autopilot is:open
> tests/test_autopilot_board.py:850: AssertionError
> E       AssertionError: 278.2: the old Autopilot view (PVTV_1, label:autopilot) was changed by [], not one update to label:autopilot is:open
> tests/test_autopilot_board.py:865: AssertionError
> E       AssertionError: 278.2: two switches on sent updates [] and creates [], not one fix to label:autopilot is:open
> tests/test_autopilot_board.py:883: AssertionError
> E       AssertionError: 278.2: after switching #57 on, the Autopilot views are [{'name': 'Autopilot', 'layout': 'table', 'filter': 'label:autopilot'}]
> tests/te

**Agent:** All eight new or changed tests fail today for the right reason: the filter is still `label:autopilot`. I found one gap in the faked GitHub; writing the hand-back now.

`9. Bash`
```
cd /home/runner/work/dokima/dokima; sed -n 495,512p tests/test_autopilot_board.py; grep -n "Autopilot view\|label:autopilot" AGENTS.md
```

> "labels": {"nodes": [{"name": l} for l in sorted(self.labels.get(n, set()))]}}
>         if kind == "issue" and parent:
>             up = self.parents.get(n)
>             node["parent"] = self.item_node("issue", up, parent=False) if up else None
>         return node
> 
>     def q(self, query, **v):
>         """Answer one GraphQL call the way GitHub would."""
>         text = " ".join(query.split())
>         values = [str(x) for x in v.values()]
>         if "organization" in text:
>             return {"organization": {"projectV2": {"id": "P", "fields": {"nodes": [
>                 {"id": "S", "name": "Status", "options": [{"id": "s-" + o, "name": o} for o in ("Backlog", "Plan", "Work", "Review", "Done")]},
>                 {"id": "W", "name": "Action", "options": [{"id": "w-you", "name": "Needs you"}, {"id": "w-auto", "name": "Autopilot"}]}]},
>                 "views": {"nodes": [dict(x) for x in (self.before if self.stale_views else self.views)]}}}}
>         if "updateProjectV2View" in text:
>             view_id = v.get("viewId") or v.get("v") or next((x for x in values if x.startswith("PVTV_")), None) \
>                 or re.search(r'viewId:\s*"([^"]+)"', text).group(1)
> 79:- One Autopilot view, a table filtered to `label:autopilot`, lists everything on autopilot. Code adds it the first time a tree goes on autopilot, from the board run of the tree's top issue only, and a refused view fails that run naming it. The Autopilot option of the Action field is a one-time step on the board, like Needs y

`10. Bash`
```
mkdir -p /tmp/dokima-out; cat > /tmp/dokima-out/review.json <<'EOF'
{
 "previous_step": {
  "did": [
   "The planner wrote two criteria: a new Autopilot view is filtered to label:autopilot is:open, and an existing view still filtered to label:autopilot is changed to that filter.",
   "It added five tests and updated three older view tests to the new filter."
  ],
  "decided": [
   "The existing view is fixed the next time a tree goes on autopilot, through GitHub's updateProjectV2View.",
   "A refused fix still sets the pills and labels, then fails the board run naming the Autopilot view."
  ],
  "open": [
   "It asks the owner whether fixing the existing view at the next /autopilot start is soon enough, or whether it should be fixed straight after this merges."
  ]
 },
 "verdict": "block",
 "summary": "The plan covers both asks and its tests fail today for the right reason, but the faked GitHub hands back every view's id and filter even when the board never asks for them, so code that doesn't read the old filter from GitHub would pass the tests and fail on the real board.",
 "blockers": [
  {
   "id": "B1",
   "criterion": "278.2",
   "test": "tests/test_autopilot_board.py::test_the_existing_autopilot_view_is_fixed_to_open_items_only",
   "problem": "The fix depends on reading each view's id and filter from GitHub. On real GitHub, a query returns only the fields it asks for. The faked GitHub returns id, name, layout and filter for every view whatever the query asks. Code that keeps today's query (views{nodes{name}}) and then reads the id or filter would pass every 278.2 and 278.3 test, but on the real board it would get no id or filter. The existing view would then never be fixed, or the run would crash.",
   "evidence": "tests/test_autopilot_board.py:509 answers every organization query with `[dict(x) for x in self.views]` (all keys) without looking at which fields the query names; dokima/board.py:138 today asks only `nodes{name}`. GitHub's schema (docs.github.com/
```

> (Bash completed with no output)

**Agent:** I blocked the plan for #278 and sent it back to the planner over one test gap. Both checks on my review passed.

**What's right:** Both of your asks map to a criterion: 278.1 for "only open issues and pull requests" and 278.2 for "the existing view is fixed too". I checked GitHub's GraphQL schema, and the plan's fix is possible: GitHub can change an existing view's filter (`updateProjectV2View`, which takes the view's id and a new filter). I ran `tests/test_autopilot_board.py`. All five new tests and the three older ones updated for the new filter fail today because the filter is still `label:autopilot`, which is the right reason. The other 17 pass.

**Blocker B1 (criterion 278.2):** Real GitHub only returns the view fields a query asks for. The faked GitHub in the tests hands back every view's id and filter whatever the query asks (`tests/test_autopilot_board.py:509`). Today the board asks only for view names (`dokima/board.py:138`). A worker who never added the id and filter to that query would pass every test, but on the real board the old view would never be fixed, or the run would crash. The fix is for the fake to return only the fields the query names.

**Your question, not accepted:** The planner assumed the existing view gets fixed the next time any tree goes on autopilot, not straight after merge. You said "The existing view is fixed too, not only new ones." but not when. Until someone next switches a tree on, the view keeps listing merged and closed items, so this stops for you on autopilot.

**Note for the worker:** `AGENTS.md:79` still describes the view as filtered to `label:autopilot`. It's in the plan's scope and needs updating.

The review is in `/tmp/dokima-out/review.json`.
