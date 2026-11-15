# ADR-011: Exploration modes are non-binding and enter the pipeline only through promote

**Status:** Accepted
**Date:** 2026-10-20

## Decision

Add exploration modes beside the gated pipeline, not inside it.

- `muse/sketch` produces an `option-set@1`: three structurally different options per round (cap five), each with a status and reason, rendered locally, with an append-only decision log.
- `smith/spike` produces a `spike-report@1`: a throwaway experiment on whether an approach works.
- `muse/promote` turns a chosen option or working spike into a `requirement@1`. It is the only route from an exploration artifact into a gated stage.
- Modes are non-binding: no gate, spec or test requirement. They write only to scratch and the artifact, mark it `fidelity: sketch` or `spike`, stop before implementing, and are never evidence for a gate.
- Divergent generation is a new cognitive mode with its own agent (`muse/explorer`, per ADR 003); judging the options stays with the user.
- Rules live in `shared/references/architecture/modes.md`; the skill is the entry point and its agents are internal.

## Why

The gated path earns its cost on stable contracts, not on an idea nobody has seen. In the audited projects specs described behavior but not appearance and were rewritten after renders. Ideation ran outside the plugins, in forks and general-purpose agents, at more token cost than all the gates, with decisions lost between sessions; the plugin skills were almost never invoked. Vercel's product-design skill and Anthropic's guidance (exploratory work may skip planning) point the same way.

## Rejected

- **Loosen the existing gates:** they earn their cost on stable contracts, and loosening them for all weakens the cases that need them.
- **A light flag on each skill:** one skill would carry two contracts, and orchestrators skip skills they find heavy.
- **A new plugin for exploration:** deferred; `muse` owns UI and design and `AGENTS.md` allows several skills per plugin. The schema is UI-neutral so sketching can move out if used beyond UI work.
- **Leave exploration ad hoc:** it produced the largest token cost, lost decisions and unreviewed visual defects.

## Consequences

Early work has a light path and a stated way back into the gate. Risks: an exploration artifact mistaken for a spec, or the light path used where the gated one is needed; the `fidelity` marker, promote-only rule, the full-pipeline list in `modes.md` and the skipped-gates note address them. Each new skill and agent needs a Codex counterpart, and the new schemas are immutable (ADR 004).

Revisit when evaluation (`docs/evaluation-methodology.md`) shows the light path is chosen where the gated one is needed, or raises later defects.

**Evidence:** `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 011.
