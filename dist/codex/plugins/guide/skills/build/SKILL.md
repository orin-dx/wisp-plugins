---
name: build
description: Build a feature, choosing the path by risk. Use for "build this" or "implement this spec".
---

# Guide: build

Say "Mode: build" and the path chosen, and why. Shared components, public interfaces, data, security and anything other code depends on: `scribe:draft-spec` (or `muse:component` for UI), then `scribe:gate-spec`, `navigator:plan` and `smith:implement`. Contained work: `smith:implement` with a brief stating the outcome, the checks that prove it and the invariants. If the outcome is not clear yet, offer `guide:explore` or `guide:spike` first. Say what done means and how it is checked before building.
