# ADR-015: Gates get two rounds and one check against reality per draft

**Status:** Accepted
**Date:** 2026-11-14

## Context

Three independent reads of the evidence (documented evaluations, session token data across five projects, and what reviewers actually caught) agreed on where review earns its cost. First-round, independent checks against code or a build caught real defects: a spec criterion pointing attestation at the wrong commit, an `init` that writes a config the loader rejects, a plan diagnostic that could never fire, padding that computed to zero in the built page. Later rounds were mostly wording churn or agents working around structural tests: one implementation gate ran 14 rounds after calling the code correct in round 3, one plan ran 29 challenge rounds, and one spec ran 13 gate rounds with blockers returning after clean rounds. The auditor and the exit gate reviewed the same draft, so the gate re-found what the auditor found. Reviewers ran per commit with no logic bug caught, and mutation ran on modules with no executable logic.

The details are in `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md` (evidence review section). Part of the reviewer catch-rate report was reconstructed from notes, so its exact counts are approximate; the direction is supported by the gate-round records and session data independently.

## Decision

- **Two rounds.** Every exit gate and the plan challenger get one retry. After the second failing round, or when a blocker repeats unchanged, the gate returns fail with an `escalation_required` blocker and the decision goes to a human with the persistent blockers. The hook enforces `retry_count` above 1 (it enforced 3, per ADR 012).
- **One check per draft, against reality.** Spec drafters self-check and the exit gate judges. The auditor, verifier and architecture audit run when asked, when a spec is shared by other work, or when it crosses a module boundary. Spec gates check every claim, criterion or citation against the code, configuration, build or spec it refers to; an issue that cannot be tied to a source or to a testability defect is a note, not a blocker.
- **Scoped watchers.** The implementation reviewer runs once per batch and gets one repeat. Mutation is skipped, and recorded as `unavailable` with a reason, when a batch changes no executable logic.

## Options considered

- **Keep a cap of three.** Rejected: the useful catches came in rounds one and two; the long loops cost the most and caught the least.
- **Remove the independent gate.** Rejected: the first-round independent check produced every documented catch before code existed.
- **Cap at one round.** Rejected: one targeted retry fixes most first-round blockers and is cheap.

## Consequences

Fewer, more useful rounds, and more decisions reach the user earlier, with the persistent blockers stated. A defect that only a third round would have caught now reaches a human instead of an agent; ADR 013's round-one completeness rule is what keeps that rare. The optional checks may miss a cross-spec conflict on a spec that turns out to be shared; the gate's own check against sources is the guard. Not yet addressed: logic bugs, which no reviewer caught in the evidence, need behavior checks (next change). Measure the effect with the paired fix-task sequences in `docs/evaluation-runbook.md`.
