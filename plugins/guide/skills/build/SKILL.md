---
name: build
description: >-
  Use for a new feature or a change other work depends on: "build this", "add this feature", "implement this spec", "let's do this for real". Picks the path by risk: a gated spec and plan for shared or production work, a brief straight to `smith:implement` for contained work.
version: 1.0.0
---

# Guide — Build

Say "Mode: build" and which path you chose, and why.

- Shared components, public interfaces, data, security and anything other code depends on: `scribe:draft-spec` (or `muse:component` for UI), then `scribe:gate-spec`, then `navigator:plan`, then `smith:implement`.
- Contained work with a clear outcome: `smith:implement` with a brief stating the outcome, the checks that prove it, and the invariants that must hold.

If the outcome is not clear yet, offer `/guide:explore` or `/guide:spike` first. Say what "done" means and how it will be checked before building.
