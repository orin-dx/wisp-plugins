---
name: audit-spec
description: >-
  Trigger when the user asks to review a spec's quality: "review this spec", "is this spec complete?", "audit this spec". Adversarially reviews a spec@1 on its own terms and returns a structured issue list with rewritten suggested fixes.
version: 2.0.0
---

# Scribe — Audit Spec

<overview>
Checks whether a spec, taken on its own terms, is complete, unambiguous, and implementable without a single clarifying question — a different question from `scribe/verify-spec`'s "does it trace back to the requirement?". Delegates to `auditor`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | A spec@1 needs adversarial quality review before it enters `scribe/gate-spec`. |
</dispatch>

<references>
`shared/schemas/spec@1.json`
</references>

<io>
**Consumes**: `spec@1`
**Produces**: issues array (criterion_id, type, description, suggested_fix per issue) plus an overall pass/fail verdict on spec quality (not the binding gate verdict — that's `scribe/gate-spec`). Route to `scribe/gate-spec`.
</io>
