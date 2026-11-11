---
name: clarify-requirement
description: >-
  Trigger when a requirement@1 draft from weaver/capture-need has gaps to close before a spec can be written: "is this requirement complete?", "what's missing from this requirement". Returns either one clarifying question or the completed requirement@1.
version: 2.0.0
---

# Weaver — Clarify Requirement

<overview>
Closes the gap between "captured" and "ready for scribe/draft-spec" one question at a time. Delegates to `clarifier`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **clarifier** | sonnet / medium | A requirement@1 draft needs its most critical gap identified and either closed with one question or confirmed complete. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: `requirement@1` draft
**Produces**: either one clarifying question (requirement unchanged) or a completed `requirement@1` with `out_of_scope` populated. Loop back into `weaver/clarify-requirement` after each answered question; route the completed requirement to `scribe/draft-spec`.
</io>
