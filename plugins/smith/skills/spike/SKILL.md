---
name: spike
description: >-
  Activate when the user wants to know whether a tool, library or approach works before committing to it: "does this work in our stack", "try it out", "spike this", "quick prototype to check", "can we use X here". Runs the smallest throwaway experiment that answers one question and returns a spike-report@1 with what was observed, what was verified and what was not. Non-binding by design — no plan, no spec, no mutation or review, no exit gate, no tests required. Do not activate for production changes; use implement for those.
version: 1.0.0
---

# Smith — Spike Skill

<capability>
A spike answers one question by trying it. It is the fast path for finding out whether a library renders in the stack, an API behaves as documented, or an approach is feasible, before anyone writes a spec or a plan. It skips the implementation pipeline on purpose: no recon baseline gate, no plan, no mutation testing, no review, no exit gate. What it keeps is honesty: the report says what was observed, what was verified and what was not. Open the reply with "Mode: spike. Nothing here is binding."
</capability>

<references>
`shared/references/architecture/modes.md`, `shared/schemas/spike-report@1.json`
</references>

<io>
**Consumes**: one question in free text, optionally a `requirement@1` or an `option-set@1` for context
**Produces**: a `spike-report@1` (`fidelity: spike`), with the throwaway code under a scratch directory (default `.scratch/<id>/`)
</io>

<report_shape>
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
</report_shape>

<spike_cycle>
1. **State the mode, the question and the signal.** Begin your first message with exactly: "Mode: spike. Nothing here is binding." One question, and what would count as an answer (it renders, it returns the documented shape, it completes within a stated time). If the work is a production change, say `smith/implement` fits and let the user choose.
2. **Design the smallest experiment** that could answer it, in the target stack where possible, with the versions the project uses. Prefer a few lines to a structure.
3. **Run it in scratch.** Write only under the scratch directory; never edit existing source, configuration or lockfiles. Installing a dependency belongs to the scratch directory too; say if the experiment needs one the project does not have.
4. **Observe and record.** Keep the real output and errors. Run the smoke check the question implies: it ran, it produced the expected result, it failed in this specific way. Do not write a test suite unless the user asks.
5. **Separate what you verified from what you did not.** `verified` holds only what the experiment demonstrated; `unverified` names what it left unchecked (other platforms, scale, accessibility, server rendering, edge cases). A conclusion of `works` needs at least one verified item. Use `partly`, `fails` or `inconclusive` when that is what happened.
6. **Report and stop.** Return the `spike-report@1`. Say whether the scratch code will be discarded or kept for reference, never extended in place. Offer the next step: promote the result through `muse/promote`, run another spike, or drop it. End with one line naming what was skipped: "Skipped by design: plan, spec, mutation, review and exit gate."
</spike_cycle>

<rules>
- A spike is never evidence that production code is correct and never counts toward a gate.
- Do not claim a result you did not observe. If a check could not run, it is `unverified`.
- Keep the scratch code out of the build: do not import it from source, and do not commit it unless the user asks.
</rules>
