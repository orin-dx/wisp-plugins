---
name: capture-need
description: >-
  Trigger when the user describes a raw need in free text: "we need X", "the problem is Y", "users are asking for Z". Converts unstructured text into a requirement@1 draft without asking clarifying questions.
version: 2.0.0
---

# Weaver — Capture Need

<overview>
The entry point for turning a raw idea or pain point into something a spec can be drafted from. Delegates to `intake`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **intake** | sonnet / medium | A free-text need statement needs converting into a requirement@1 draft. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: free-text need statement
**Produces**: `requirement@1` draft (fields that couldn't be inferred are omitted, noted in `reasoning`). Route to `weaver/clarify-requirement` to close gaps before `scribe/draft-spec`.
</io>
