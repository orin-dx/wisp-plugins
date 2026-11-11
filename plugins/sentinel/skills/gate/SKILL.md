---
name: gate
description: >-
  Use this, not freehand checking, whenever an artifact must be verified before the next stage: "verify this", "is this done?", "check this spec/plan/requirement/PR", "does this meet the criteria?", "gate this", and before starting implementation, shipping or opening a PR. Not for Q&A, code explanation or exploration. Returns verdict@3: cleared, or blockers.
version: 1.3.0
---

# Sentinel Gate Skill

<overview>
Sentinel is a cross-cutting verification gate. It runs whenever a stage artifact — requirement, spec, plan, implementation, or PR — must be confirmed against its criteria before the next stage begins. It does not generate artifacts; it only judges them.
</overview>

---

<three_stage_flow>

| Stage | Agent | Model | Effort | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| 1 — Recon | `recon` | haiku | low | Inventory the artifact: type, location, criteria list, source files to read. No judgment. |
| 2 — Verify | `verifier` | sonnet | medium | Cross-reference each criterion against the source files. Classify as verified, failed, or unverifiable. Neutral — reports evidence only. |
| 3 — Exit Gate | `exit-gate` | opus | high | Produce the final verdict. Pass only if all criteria are verified with no unresolved failures. On fail, return specific actionable blockers. On a retry, pass the gate `retry_count` and the previous round's blockers so it applies the round rules. |

</three_stage_flow>

---

<axiom_protocol>

The protocol input is: `artifact_type`, `artifact_path`, `criteria` (explicit or derived from linked spec).

The protocol output is `verdict@3`: a scoped pass or fail with blockers, coverage gaps, pending checks, and a short summary.

</axiom_protocol>

---

<framework_references>
- [Verdict Schema](../../../../shared/schemas/verdict@3.json)
- [Context hygiene](../../../../shared/references/tooling/context.md) — keep command output and scripts out of the thread when running checks.
</framework_references>
