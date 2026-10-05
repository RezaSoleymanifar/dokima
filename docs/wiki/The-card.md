# The card

Dokima's job is to move your attention from the work to the verification. The card is how it does that: every unit of work is reported the same way, twice.

The same card sits at the top of the issue and at the top of its PR, so you see one status in both places.

- **Before work starts:** each objective, its acceptance criteria, and how each check will be verified. Plus what is deliberately *not* checked.
- **After work ends:** each check marked passed or failed, with a link to the proof.

## Example

**Before**

```markdown
Objective: nothing reaches main unless tests pass
- ☐ A failing pull request can't merge. Verify: open one with a broken test, attempt the merge.
- ☐ A passing pull request can merge. Verify: fix the test, show it green and mergeable.

Not checked: whether the tests themselves are good.
```

**After**

```markdown
Objective: nothing reaches main unless tests pass
- ✅ A failing pull request can't merge. Proof: <link to the red test run and blocked merge>
- ✅ A passing pull request can merge. Proof: <link to the green test run>

Not checked: whether the tests themselves are good.
```

## Reading the card

Each criterion has a circle that shows GitHub's verdict on it. The words of the criterion link to the proof.

The Approve button means "approve the result to merge". It is for the finished work, not the plan; you approve the plan by adding the `work` label to the issue.

## What counts as proof

Proof is a link to GitHub's own record, so you never have to take the agent's word for it:

- a test run that went green or red,
- a pull request showing a merge was blocked,
- a setting as GitHub reports it back.

A commit is rarely proof on its own: it shows what changed, not that it works. Where there is no page to link, GitHub's exact response is quoted.

## Why you can trust it

Cards are not written by the AI. A script builds each card from the checks in the issue and from GitHub's record of which checks passed, and the workflow posts it. No session can skip a card, reword it, or report a pass that didn't happen. *Planned.*

## "Not checked"

Every card says what it does not cover. A green card means the listed checks passed, nothing more. Making the gaps visible is what lets you decide where to look yourself.
