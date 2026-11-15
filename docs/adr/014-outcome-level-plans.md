# ADR-014: Plans state outcomes and contracts; code appears only where logic is non-obvious or a wrong shape is costly

**Status:** Accepted
**Date:** 2026-11-10
**Supersedes:** the exact-code-for-every-task clause of ADR-009. Its implementer-latitude and compilation-boundary sizing clauses stand.

## Decision

Plans state each task as an outcome and a contract, and carry implementation code only where logic is non-obvious or a wrong shape is costly to undo.

- **Task content:** `planner` writes an outcome, exact file paths, the approach, signatures or interfaces with error behavior, proving tests with inputs and asserted results, the verification command, the commit message and `covers_criteria`.
- **Where code appears:** ordering or concurrency, numeric or parsing edges, security checks, wire or on-disk formats, result-only algorithms, and signatures other tasks depend on. Routine code gets the outcome and the signature.
- **Challenger:** flags full bodies for routine logic as `over-specified` and a missing outcome, signature, assertion or command as `under-specified`; it no longer treats absent code as a defect. Its other checks are unchanged.
- **No schema change:** `plan@1` stays as published (ADR 004), the shape lives in `steps` strings, and every consumer (`smith`, `estimator`, `sentinel`, `weaver`) already reads free-text steps.
- **ADR-009:** stays Accepted for implementer latitude and compilation-boundary sizing; its guardrail (do not size tasks by clock time) is unchanged.

## Why

- **Code for every task did not pay:** ADR-009 required it though the implementer may reshape it, so `planner` wrote every body, `challenger` policed it and `implementer` was told not to copy it.
- **Size and prescription hurt:** very large plans stalled agents, and Anthropic's guidance says over-prescription hurts current models.
- **The guardrail is scope, not bodies:** what ADR-009 wanted is the plan's scope (files, signatures, tests, criteria).
- **The schema already fits:** `plan@1` requires only `id`, `title`, `files`, `steps` and `commit_message`, and `additionalProperties` is false, so the rest of a task lives in `steps`.

## Rejected

- **Keep exact code for every task:** because it is the cost this record cuts, and ADR-009 already made it non-binding.
- **Drop code entirely:** because a wrong wire format, parsing edge or cross-task signature is costly and cheap to prevent.
- **A per-run plan mode:** because it doubles the planner and challenger surface to test; the per-task rule covers both ends.
- **A `plan@2` with outcome, signature and test fields:** because `steps` carries the content and every consumer and fixture would have to move.
- **Edit the `plan@1` field descriptions that mention exact code:** because a published schema is not edited in place (ADR-004); they are stale but harmless.

## Consequences

- **Now true:** plans are smaller.
- **Risk:** a weaker-model implementer invents a wrong shape where only a signature was given.
- **Risk:** a code-free plan is harder for `challenger` to falsify.
- **Risk:** the rule for when code is warranted is a judgment call.
- **Revisit when:** consumers need outcome, signature or test fields programmatically (`plan@2`), or implementers do measurably worse from outcome-level plans.

## Evidence

- **Enforced by:** `tests/test_navigator_plan.py` (planner and challenger rules, unchanged schema, a new-shape plan validates against `plan@1`).
- `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "Outcome-level plans" and "ADR evidence", ADR 014.
