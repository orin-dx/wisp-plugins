---
name: spike
description: Run the smallest throwaway experiment that answers whether a tool, library or approach works, and report what was observed, verified and left unchecked. Use before committing to a technical choice. Non-binding: no plan, no spec, no review, no gate, no tests required.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Find out whether it works

Open with "Mode: spike. Nothing here is binding." A spike answers one question by trying it, and skips the implementation pipeline on purpose. If the work is a production change, say the implementation skill fits and let the user choose. Read `shared/references/architecture/modes.md` for the mode rules and `shared/references/tooling/context.md` for keeping command output small.

## Inputs

- One question in free text, optionally a `requirement@1` or an `option-set@1` for context.

## Workflow

1. State the question and what would count as an answer (it renders, it returns the documented shape, it finishes within a stated time).
2. Design the smallest experiment that could answer it, in the target stack where possible, with the versions the project uses.
3. Run it under a scratch directory (default `.scratch/<id>/`). Never edit existing source, configuration or lockfiles; a dependency the project lacks is installed in scratch, and say so.
4. Observe and record the real output and errors. Run the smoke check the question implies; do not write a test suite unless the user asks.
5. Separate what was verified from what was not. `verified` holds only what the experiment demonstrated; `unverified` names what it left unchecked (other platforms, scale, accessibility, server rendering, edge cases). A conclusion of `works` needs at least one verified item; otherwise use `partly`, `fails` or `inconclusive`.
6. Return a `spike-report@1` conforming to `shared/schemas/spike-report@1.json` with `fidelity` set to `spike`. Say whether the scratch code is discarded or kept for reference, never extended in place. Offer to promote the result, run another spike, or drop it, and end with one line: "Skipped by design: plan, spec, mutation, review and exit gate."

## Report shape

```json
{
  "id": "SPIKE-001",
  "question": "string",
  "approach": "string",
  "environment": "string",
  "scratch_path": ".scratch/SPIKE-001/",
  "observed": ["string"],
  "verified": ["string"],
  "unverified": ["string"],
  "conclusion": "partly",
  "followups": ["string"],
  "fidelity": "spike",
  "reasoning": "string"
}
```

Follow it exactly, because the report is checked against `spike-report@1`. Required: `id` (`SPIKE-` and three or more digits), `question`, `approach`, `observed` (at least one), `verified`, `unverified`, `conclusion` (`works`, `partly`, `fails` or `inconclusive`; `works` needs at least one `verified` item), `fidelity` (always `spike`) and `reasoning`. No other fields are allowed.

## Decisions and stopping

A spike is never evidence that production code is correct and never counts toward a gate. Claim only what was observed; a check that could not run is `unverified`. Keep scratch code out of the build and uncommitted unless the user asks. This skill has a complete single-agent path and needs no delegation.
