# ADR-013: Exit gates list the complete blocker set in round one and cite only known blockers on a retry

**Status:** Accepted
**Date:** 2026-11-10

## Decision

Each exit gate (`muse`, `scribe`, `smith`, `sentinel`, `ranger`) lists every blocker in round one and cites only known blockers on a retry; gates stay default-fail and adversarial, and `verdict@3` is unchanged.

- **Round one:** `retry_count` 0 or absent lists the complete blocker set.
- **Retry:** cites only prior blockers that remain unresolved, or regressions the fix introduced; any other new issue is a `coverage_gaps` entry with `blocking: false`.
- **Blocker shape:** it names the criterion or section in `criterion`, cites evidence (quoted text or a location) in `finding`, and states the exact change required. Wording or style issues are notes.
- **Drafters:** `muse:drafter` and `scribe:drafter` check their draft against the checklist in `shared/references/verification/gate-readiness.md`, the one home for checklist and blocker wording.
- **Hook:** `shared/hooks/validate-handback.py` also denies a blocker or coverage gap whose text is only whitespace, and checks nothing else about blocker content.

## Why

- **Rounds did not converge:** every audited spec failed its first gate and blocker counts did not fall between rounds.
- **Late findings and fix breakage:** a later round found what an earlier one could have, or a fix broke something, and each round re-reads the whole artifact.
- **A program cannot judge round discipline:** ADR 012 covers schema and cap, so this is a gate prompt rule plus a drafter self-check.

## Rejected

- **A `verdict@4` with a `regression` or `prior_blocker_id` field:** because `verdict@3` already expresses the rule through `blockers` and `coverage_gaps`, new schema versions are costly (ADR 004), and the hook could not use the field since a retry is a new subagent with no stored prior verdict.
- **Hook checks for a `location`, minimum length or quote:** because `escalation_required` and `missing_mutation_gate` blockers have no location, and each wrongful denial costs a turn.
- **A lenient gate on retries:** because the rule does not drop findings, it records them as non-blocking gaps the orchestrator sees.
- **The rule in the shared constitution:** because the constitution is byte-identical in every agent (ADR 006) and the rule applies only to gates.

## Consequences

- **Now true:** fewer rounds and tokens per gated spec, expected with the same defects caught.
- **Risk:** a defect missed in round one can now pass as a non-blocking gap on a retry, so the gap list needs a reader.
- **Cost:** the gate-calling skills must carry `retry_count` and the prior blockers into the retry input.
- **Revisit when:** paired runs show round counts do not fall, or the hook must tell fix-induced blockers from late-found ones.

## Evidence

- **Enforced by:** `tests/test_handback_validator.py` (blank text), `tests/test_agent_structure.py` and `tests/test_prompt_alignment.py` (agent shape). The round rules are prompt rules.
- `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 013.
