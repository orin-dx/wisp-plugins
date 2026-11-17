---
name: pr
description: >-
  Use this, not freehand text, whenever a pull request is opened or its title or description written or updated: "open a PR", "create a pull request", "write the PR description". Produces a PR title and body from the diff and any linked spec or requirement, then hands them to the branch's Entire trail, which opens the PR.
version: 2.0.2
---

# Courier — PR

<overview>
Produces a PR title and body from a diff plus optional linked spec/requirement, following the repository's pull request template when it has one, then opens the PR. Delegates the narrative to `pr-narrator`; opening the PR is a visible external action and always requires explicit confirmation before the `gh pr create` call fires.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **pr-narrator** | sonnet / medium | A PR needs a title and body a reviewer with zero context can act on. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/delivery/github.md` — outcome-led PR structure, observed verification, risk disclosure, review voice, labels, and `gh` commands.
</references>

<io>
**Consumes**: git diff, optionally linked `spec@1` or `requirement@1`
**Produces**: opened PR (title, body, labels). By default, push the branch and create or link its Entire trail (`entire trail create`); Entire opens the pull request from the trail, so return the title and body for it. Open a PR with `gh pr create` only when the repository's instructions say agents open them, and only after the user confirms the title and body.
</io>
