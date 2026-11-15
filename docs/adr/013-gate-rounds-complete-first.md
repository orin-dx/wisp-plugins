# ADR-013: Exit gates list the complete blocker set in round one and cite only known blockers on a retry

**Status:** Accepted
**Date:** 2026-11-10

## Decision

- Each exit gate (`muse`, `scribe`, `smith`, `sentinel`, `ranger`) states two rules in `<output>`. Round one (`retry_count` 0 or absent) lists the complete blocker set. A retry cites only prior blockers that remain unresolved, or regressions the fix introduced; any other new issue is a `coverage_gaps` entry with `blocking: false`.
- A blocker names the criterion or section in `criterion`, cites evidence (quoted text or a location) in `finding`, and states the exact change required. Wording or style issues are notes.
- The drafters feeding a spec gate (`muse:drafter`, `scribe:drafter`) check their draft against the checklist in `shared/references/verification/gate-readiness.md`, the one home for checklist and blocker wording.
- `shared/hooks/validate-handback.py` also denies a blocker or coverage gap whose text is only whitespace, and checks nothing else about blocker content.

Gates stay default-fail and adversarial; `verdict@3` is unchanged.

## Why

Every audited spec failed its first gate and blocker counts did not fall between rounds: a later round found what an earlier one could have, or a fix broke something, and each round re-reads the whole artifact. A program cannot judge round discipline (ADR 012 covers schema and cap), so it is a gate prompt rule plus a drafter self-check.

## Rejected

- **A `verdict@4` with a `regression` or `prior_blocker_id` field:** `verdict@3` already expresses the rule through `blockers` and `coverage_gaps`, new schema versions are costly (ADR 004), and the hook could not use the field because a retry is a new subagent with no stored prior verdict.
- **Hook checks for a `location`, minimum length or quote:** `escalation_required` and `missing_mutation_gate` blockers have no location, and each wrongful denial costs a turn.
- **A lenient gate on retries:** the rule does not drop findings, it records them as non-blocking gaps the orchestrator sees.
- **The rule in the shared constitution:** the constitution is byte-identical in every agent (ADR 006) and the rule applies only to gates.

## Consequences

Expected: fewer rounds and tokens per gated spec with the same defects caught. A defect missed in round one can now pass as a non-blocking gap on a retry, so the gap list needs a reader, and the gate-calling skills must carry `retry_count` and the prior blockers into the retry input.

Revisit when paired runs show round counts do not fall, or when the hook must tell fix-induced blockers from late-found ones.

**Enforced by:** `tests/test_handback_validator.py` (blank text), `tests/test_agent_structure.py` and `tests/test_prompt_alignment.py` (agent shape). The round rules are prompt rules.

**Evidence:** `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 013.
