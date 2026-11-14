---
name: draft-spec
description: >-
  Use this, not a freehand spec, whenever a spec is written or drafted: "spec this out", "draft a spec", "write a spec for this requirement", "write the acceptance criteria". Turns a requirement@1 and optional research-report@1 into a spec@1 with scope, non_goals, api_surface and testable criteria; error cases carry is_error_case: true. Unknowns are stated as assumptions or owner decisions.
version: 2.0.0
---

# Scribe — Draft Spec

<overview>
Turns a requirement (and optional research report) into a spec a developer could implement without asking a single clarifying question. Delegates to `drafter`. The drafter checks its own draft, then `scribe/gate-spec` decides pass or fail. `scribe/verify-spec`, `scribe/audit-spec` and `scribe/audit-architecture` run on request, or when the spec is shared by other work or crosses a module boundary.

Unknowns are expected. The drafter states each in `scope` as an `Assumption:` line or, when the answer changes scope, behavior other work depends on, or cost, an `Open decision:` line. Put every open decision to the user before gating and redraft with the answers.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** | sonnet / medium | A requirement@1 (plus optional research-report@1) needs a first spec@1 draft. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/spec@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: `requirement@1`, optionally `research-report@1`
**Produces**: `spec@1` draft (no disk write yet — that happens after `scribe/gate-spec` passes). Route to `scribe/gate-spec` once no `Open decision:` line remains, or first to an optional check above when one applies.
</io>
