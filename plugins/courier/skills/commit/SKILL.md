---
name: commit
description: >-
  Use this, not a hand-written message, whenever a commit is about to be made or a commit message written: "commit this", "write a commit message", "commit the staged changes". Reads the staged diff and returns a conventional commit message that explains why.
version: 2.0.1
---

# Courier — Commit

<overview>
Reads the staged git diff and the repository's recent commit history, and produces a conventional commit message in that repository's style. Delegates entirely to `commit-analyzer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **commit-analyzer** | haiku / low | Staged changes are ready and need a conventional commit message. |
</dispatch>

<references>
`shared/references/delivery/commits.md` — type/scope conventions, commit message rules, and the voice standard for this artifact.
</references>

<io>
**Consumes**: staged git diff
**Produces**: conventional commit message. The skill runs `git commit` after the user confirms the message — committing is a local, reversible action per this repo's standing action-safety guidance, but still surface the message for confirmation before running it.
</io>
