---
name: fix
description: >-
  Use for a bug, a list of review findings or a small change: "fix this", "address these findings", "this is broken", "make this change". Starts the `smith:implement` fix path, so the change gets a test that fails on the original bug, a review and an exit check.
version: 1.0.0
---

# Guide — Fix

Say "Mode: fix." Invoke the `smith:implement` skill with a fix brief: the claim to fix, the invariants that must keep holding, and where the same mistake may repeat.

A change of a line or two with an obvious cause can be done directly: add a test that fails on the original bug, run the project's checks, and say that the full path was skipped and why.
