# Writing issues

In Dokima, a task is a GitHub issue. A good issue says what you want and how anyone could tell it's done. Everything downstream, the plan, the tests and the final verdict, is measured against it.

## The three fields

1. **Title:** the outcome, written as a sentence you could check.
   *Good:* "Exported CSVs include a header row." *Vague:* "Fix export."
2. **Goals and criteria** (required): a list. Each goal has the criteria that prove it nested underneath. Each criterion has a "Verified by" line saying how it is checked. A goal is met once all of its criteria are met.
3. **Where to look** (optional): file paths, one per line, so the agent doesn't have to rediscover them.

## Example

**Title:** Exported CSVs include a header row

**Goals and criteria**

```markdown
- Goal: exported files are readable by spreadsheet apps
  - Criterion: the first line of every export lists the column names
    Verified by: a test that exports a file and reads its first line
  - Criterion: column names match the field names shown in the app
    Verified by: a test comparing the header to the app's field names
- Goal: existing imports keep working
  - Criterion: importing a file with a header row skips that row
    Verified by: a test that imports a file with a header row
```

**Where to look**

```
src/export/csv.py
src/import/csv.py
```

## What makes a good criterion

A criterion is something a test or a person could confirm without judgment calls.

| Instead of | Write |
| --- | --- |
| "Export is faster" | "Exporting 10,000 rows takes under 2 seconds" |
| "Errors are handled" | "A missing file shows 'File not found' and exits with code 1" |
| "Clean up the code" | Leave it out, or split it into its own issue |

If a criterion can't be verified, the planner will say so and propose a rewrite instead of guessing. *Planned.*

## Big issues

If an issue holds more than one deliverable, split it into sub-issues. The parent keeps the goals and closes itself when all of its children close. The planner may propose a split; nothing is created until you approve it. *Planned.*

## Approving the plan

When the planner has posted its plan, read it. Adding the `work` label approves the plan and starts the worker.

## Shortcuts

- Blank issues are allowed. You can jot down an idea now and add goals and criteria later; nothing runs until they're there.
- Issues created through the website, the API or an agent are held to the same standard.
