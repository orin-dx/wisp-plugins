---
name: ship
description: >-
  Use when work is ready to go out: "ship this", "commit and open a PR", "write the changeset", "cut a release". Starts the courier skills for the commit message, changeset, pull request or release notes, in the repository's own conventions.
version: 1.0.0
---

# Guide — Ship

Say "Mode: ship." Use only the steps the user asked for, in this order: `courier:changeset` first when the repository uses changesets and the change is user-visible (so the file is part of the commit), then `courier:commit` for the commit message, then `courier:pr` for the pull request title and body (Entire opens the PR from the branch's trail), `courier:release` for release notes. Confirm before anything is pushed, posted or published.
