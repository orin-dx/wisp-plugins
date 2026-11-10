---
name: draft-spec
description: >-
  Use this, not a freehand spec, whenever a spec is written or drafted: "spec this out", "draft a spec", "write a spec for this requirement", "write the acceptance criteria". Turns a requirement@1 and optional research-report@1 into a spec@1 with scope, non_goals, api_surface and testable criteria; error cases carry is_error_case: true. No TBDs.
version: 2.0.0
---

# Scribe — Draft Spec

<overview>
Turns a requirement (and optional research report) into a spec a developer could implement without asking a single clarifying question. Delegates to `drafter`. The draft is not final — it feeds `scribe/verify-spec` and `scribe/audit-spec` before `scribe/gate-spec` decides pass or fail.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drafter** | sonnet / medium | A requirement@1 (plus optional research-report@1) needs a first spec@1 draft. |
</dispatch>

<references>
`shared/schemas/spec@1.json`, `shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: `requirement@1`, optionally `research-report@1`
**Produces**: `spec@1` draft (no disk write yet — that happens after `scribe/gate-spec` passes). Route to `scribe/verify-spec`.
</io>
