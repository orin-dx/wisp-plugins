# ADR-013: Exit gates list the complete blocker set in round one and cite only known blockers on a retry

**Status:** Accepted
**Date:** 2026-11-10

## Context

In two real projects every spec failed its first gate. Blocker counts per round did not fall: SPEC-001 went 18, 5, 6, 0, 0, 2, 0, 6, 2, 3, 2, 8, 3 across 13 rounds, and eight specs passed only at `retry_count` 4 to 9. The muse gates cost about 8.15 million tokens over 79 calls (`docs/evaluations/frontend-design/verification/VERIFY-3.md`, section 5; `CATALOG.md`, WP-50 and WP-212). A zero followed by a nonzero count means a later round found issues an earlier round could have found, or a fix broke something. Each extra round re-reads the whole artifact. ADR 012 already enforces schema conformance and the retry cap by hook, but not round discipline.

## Decision

- Each exit gate (`muse`, `scribe`, `smith`, `sentinel`, `ranger`) states two rules in its `<output>` section, worded the same in all five. In round one (`retry_count` 0 or absent) it lists the complete blocker set. On a retry it cites only blockers from the prior round that remain unresolved, or regressions the fix introduced; any other newly noticed issue is a `coverage_gaps` entry with `blocking: false`.
- A blocker names the criterion or section in `criterion`, cites evidence (quoted text or a location) in `finding`, and states the exact change required. A wording-only or style-only issue is a note, never a blocker.
- The drafters that feed a spec gate (`muse:drafter`, `scribe:drafter`) load `shared/references/verification/gate-readiness.md` and check their draft against its spec checklist before returning. The checklist and blocker wording live in that one reference.
- `shared/hooks/validate-handback.py` additionally denies a blocker or coverage gap whose text field is only whitespace. It checks nothing else about blocker content.

Gates stay default-fail and adversarial; no pass condition is relaxed. `verdict@3` is unchanged.

## Options considered

- **A `verdict@4` with a `regression` or `prior_blocker_id` field on each blocker.** Rejected for now: `verdict@3` already expresses the rule through `blockers` and `coverage_gaps`, and ADR 004 makes a new schema version costly. Revisit if WP-212 needs the hook to tell fix-induced blockers from late-found ones; today the hook cannot, because a retry is a new subagent with no stored prior verdict.
- **Hook checks that a blocker has a `location`, a minimum length, or a quote.** Rejected: an `escalation_required` or `missing_mutation_gate` blocker has no location, and a terse correct blocker would be denied. Each denial costs a turn. Only blank text is rejected.
- **Make the gate lenient on retries (accept anything not previously listed).** Rejected as stated; the rule does not drop findings, it records them as non-blocking gaps the orchestrator sees.
- **Put the rule in the shared constitution.** Rejected: the constitution block is copied byte for byte into every agent (ADR 006), so any change touches all 40 agents; the rule applies only to gates.

## Consequences

Expected: fewer rounds and fewer tokens per gated spec, with the same defects caught. Not yet measured; a live run (`docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`) confirms the hook fires and the gates run, not that rounds fall. Costs: a defect a gate misses in round one can now pass as a non-blocking gap on a retry, so the gap list needs a reader; and a gate can only tell a retry from round one if the orchestrator supplies `retry_count` and the prior blockers, which the skills do not yet pass. The skills track must carry the prior blockers into the retry input.

**Enforced by:** `tests/test_handback_validator.py` (blank text), `tests/test_agent_structure.py` and `tests/test_prompt_alignment.py` (agent shape). The round rules themselves are prompt rules.
