---
name: prioritize-backlog
description: >-
  Trigger when the user asks what to work on first from a set of requirements: "what should we prioritize", "rank the backlog", "what's most urgent". Given requirement@1 drafts, returns an ordered list with a rationale per requirement.
version: 2.0.0
---

# Weaver — Prioritize Backlog

<overview>
Turns a pile of "high priority" requirements into an actual order, with a rationale that survives being challenged. Delegates to `prioritizer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **prioritizer** | sonnet / medium | A set of requirement@1 drafts needs a ranked order before planning starts. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: list of `requirement@1` objects
**Produces**: ranked list — `{requirement_id, rank, rationale, depends_on}` per entry. Feeds which requirement goes to `scribe/draft-spec` next; does not modify the requirements themselves.
</io>
