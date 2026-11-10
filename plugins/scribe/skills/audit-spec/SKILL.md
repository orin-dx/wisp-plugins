---
name: audit-spec
description: >-
  Use this, not a freehand review, whenever a spec's quality is reviewed: "review this spec", "is this spec complete?", "audit this spec", "what is missing from this spec". Adversarially checks a spec@1 on its own terms for untestable criteria, ambiguity, missing error cases and scope overlap; returns issues with rewritten fixes.
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
