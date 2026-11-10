# ADR-014: Plans state outcomes and contracts; code appears only where logic is non-obvious or a wrong shape is costly

**Status:** Accepted
**Date:** 2026-11-10
**Supersedes:** the exact-code-for-every-task clause of ADR-009. Its implementer-latitude and compilation-boundary sizing clauses stand.

## Context

ADR-009 made the plan's exact implementation code a baseline the implementer may reshape, and kept the plan fully concrete so `challenger` has something to review. The baseline was still required for every task, so `planner` wrote a body for every function, `challenger` policed it, and `implementer` was told not to copy it. The planner prompt was the second-largest agent file.

Three observations argue against writing code for every task. Plans of 60 to 130 KB stalled agents in the audited projects (`docs/evaluations/frontend-design/ARCHITECTURE-REVIEW.md`, assumption 10). Anthropic's guidance says instructions written for earlier models are often too prescriptive for current ones and reduce output quality, and its own planner stays at high-level design. And a body the implementer is told it may discard buys little: the guardrail ADR-009 wanted is the plan's scope (files, signatures, tests, criteria), which does not need the body.

`plan@1` does not require code. A task requires `id`, `title`, `files`, `steps` (an array of strings), and `commit_message`; "exact code" appears only in a field description, and `additionalProperties` is false, so every part of a task other than those fields lives in `steps` strings.

## Decision

`planner` writes each task as an outcome, exact file paths, the approach, signatures or interfaces with error behavior, proving tests with inputs and asserted results, the verification command, the commit message and `covers_criteria`. It adds implementation code only where the logic is non-obvious or a wrong shape would be costly to undo: ordering or concurrency rules, numeric or parsing edge cases, security checks, wire or on-disk formats, algorithms the spec states only by result, and signatures other tasks depend on. Routine code gets the outcome and the signature.

`challenger` flags full bodies for routine logic as `over-specified`, and treats a missing outcome, signature, assertion or command as `under-specified`. It no longer treats absent code as a defect. Its checks for missing work, ordering, criterion coverage and sibling interfaces are unchanged.

No schema change. `plan@1` stays as published (ADR-004). The shape lives in `steps` strings, and every consumer that reads a plan (`smith`, `estimator`, `sentinel`, `weaver`) already handles free-text steps.

## Options considered

- **Keep exact code for every task.** Rejected: it is the cost this record exists to cut, and ADR-009 already made the code non-binding.
- **Drop code entirely.** Rejected: a wrong shape in a wire format, a parsing edge or a cross-task signature is costly and cheap to prevent, and weaker implementers lose a guardrail.
- **A plan mode (outcome-level or full-code) chosen per run.** Rejected: it doubles the planner and challenger surface to test, and a per-task rule already covers both ends.
- **A `plan@2` with explicit outcome, signature and test fields.** Rejected for now: the existing `steps` array carries the content, and a new version would need every consumer and the pipeline fixtures to move. Revisit if consumers need to read the fields programmatically.
- **Edit the `plan@1` field descriptions that mention exact code.** Rejected: a published schema is not edited in place (ADR-004). The descriptions are stale but harmless.

## Consequences

Plans are smaller. One run on a six-criterion fixture produced a plan 43% smaller in characters with every criterion still covered (see `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`). Whether implementers do better or worse with outcome-level plans is untested. The risks are that an implementer in a weaker model invents a wrong shape where the plan gave only a signature, and that a plan with no code is harder for `challenger` to falsify. The rule for when code is warranted is a judgment call the planner can get wrong in either direction.

ADR-009 stays Accepted as to implementer latitude and compilation-boundary sizing; only its requirement that every task carry the exact code is superseded. Its guardrail (do not size tasks by clock time) is unchanged.

**Enforced by:** `tests/test_navigator_plan.py` checks the planner and challenger rules, the unchanged schema, and that a plan in the new shape validates against `plan@1`.
