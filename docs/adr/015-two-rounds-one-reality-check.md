# ADR-015: Gates get two rounds and one check against reality per draft

**Status:** Accepted
**Date:** 2026-11-14

## Decision

- **Two rounds.** Every exit gate and the plan challenger get one retry. After the second failing round, or when a blocker repeats unchanged, the gate returns fail with an `escalation_required` blocker and a human decides with the persistent blockers. For exit gates the hook enforces it: a fail at `retry_count` 1 must carry `escalation_required`, and any later report must be an escalated fail (it allowed three retries, per ADR 012). The challenger's limit is in its prompt only (its output is not `verdict@3`).
- **One check per draft, against reality.** Spec drafters self-check and the exit gate judges. The auditor, verifier and architecture audit run when asked, when other work shares the spec, or when it crosses a module boundary. Spec gates check every claim, criterion or citation against the code, configuration, build or spec it refers to; an issue tied to no source or testability defect is a note, not a blocker.
- **Scoped watchers.** The implementation reviewer runs once per batch with one repeat. Mutation is skipped, recorded as `unavailable` with a reason, when a batch changes no executable logic.

## Why

Review earns its cost in first-round, independent checks against code or a build, which caught real defects before code existed. Later rounds were mostly wording churn or agents working around structural tests. The auditor and gate reviewed the same draft, so the gate re-found what the auditor found. Per-commit review caught no logic bug, and mutation ran on modules with no executable logic.

## Rejected

- **Keep a cap of three:** the useful catches came in rounds one and two; the long loops cost most and caught least.
- **Remove the independent gate:** the first-round independent check produced every documented catch.
- **Cap at one round:** one targeted retry fixes most first-round blockers cheaply.

## Consequences

Fewer, more useful rounds, and decisions reach the user earlier with the persistent blockers stated. A defect only a third round would have caught now reaches a human instead of an agent; ADR 013's round-one completeness keeps that rare. The optional checks may miss a cross-spec conflict on a spec that proves shared; the gate's check against sources is the guard. Logic bugs, which no reviewer caught, need behavior checks, not more rounds.

Revisit when paired fix-task sequences (`docs/evaluation-runbook.md`) show a defect that only a third round or the dropped auditor step would have caught.

**Evidence:** `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "Evidence review and ADR 015" and "ADR evidence", ADR 015 (catch-rate counts are approximate).
