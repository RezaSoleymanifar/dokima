# Writing issues

In Dokima, a task is a GitHub issue. A good issue says what you want and how anyone could tell it's done. Everything downstream, the plan, the tests and the final verdict, is measured against it.

## The three fields

1. **Title:** the outcome, written as a sentence you could check.
   *Good:* "Exported CSVs include a header row." *Vague:* "Fix export."
2. **Goals and checks** (required): a checklist. Each goal has the checks that prove it nested underneath. A goal is done when all of its checks are done.
3. **Where to look** (optional): file paths, one per line, so the agent doesn't have to rediscover them.

## Example

**Title:** Exported CSVs include a header row

**Goals and checks**

```markdown
- [ ] Goal: exported files are readable by spreadsheet apps
  - [ ] the first line of every export lists the column names
  - [ ] column names match the field names shown in the app
- [ ] Goal: existing imports keep working
  - [ ] importing a file with a header row skips that row
```

**Where to look**

```
src/export/csv.py
src/import/csv.py
```

## What makes a good check

A check is something a test or a person could confirm without judgment calls.

| Instead of | Write |
| --- | --- |
| "Export is faster" | "Exporting 10,000 rows takes under 2 seconds" |
| "Errors are handled" | "A missing file shows 'File not found' and exits with code 1" |
| "Clean up the code" | Leave it out, or split it into its own issue |

If a check can't be verified, the planner will say so and propose a rewrite instead of guessing. *Planned.*

## Big issues

If an issue holds more than one deliverable, split it into sub-issues. The parent keeps the goals and closes itself when all of its children close. The planner may propose a split; nothing is created until you approve it. *Planned.*

## Shortcuts

- Blank issues are allowed. You can jot down an idea now and add goals and checks later; nothing runs until they're there.
- Issues created through the website, the API or an agent are held to the same standard.
