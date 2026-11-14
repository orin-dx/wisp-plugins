# ADR-016: Specs state unknowns as assumptions or owner decisions instead of banning them

**Status:** Accepted
**Date:** 2026-11-14

## Context

The spec drafters and exit gates (`scribe`, `muse`) failed a spec for any TBD "regardless of how minor", and the gate-readiness checklist sent every unknown to `non_goals` or `reasoning`. That is a human "definition of ready": everything decided before work starts. In the audited projects every spec failed its first gate, later rounds were mostly wording churn (ADR 015), and the owner rewrote gated specs the day after seeing renders (ADR 011). The ban did not remove unknowns; it moved them where no later stage sees them. `non_goals` reads as an exclusion, so an unknown parked there becomes a silent scope cut, and `reasoning` is never forwarded (ADR 004), so an unknown parked there disappears.

What agents need is narrower: every unknown visible, and each one either resolved, stated as an assumption the work proceeds on, or put to the owner when it changes scope, behavior other work depends on, or cost.

## Decision

- A spec states each unknown in `scope`, one per line after the coverage statement: `Assumption: <the answer the work proceeds on>`, or `Open decision: <question>; options: <A | B>; affects: <criterion ids or scope>`. The convention and the gate disposition live in `shared/references/verification/gate-readiness.md` (Unknowns).
- The drafters write unknowns that way and never leave a TBD in a criterion or move an unknown into `non_goals` or `reasoning`. The skills put each open decision to the user before gating and redraft with the answer, which is folded into the spec and the line deleted.
- The gates fail an unknown that leaves a criterion untestable, an `Open decision:` line (blocker criterion `owner_decision`, routed to the user rather than the drafter), and an `Assumption:` that actually changes scope, dependent behavior or cost. A stated assumption is not a blocker unless the requirement or code it rests on contradicts it, which is the ordinary claim check of ADR 015.
- `spec@1` is unchanged (ADR 004). This replaces the second item of the spec checklist ADR 013 created; the round rules of ADR 013 and the round limit of ADR 015 are unchanged.

## Options considered

- **Keep the blanket ban.** Rejected: it produced first-round failures and churn without making unknowns go away, and it hid them in fields that mean something else.
- **A `spec@2` with `assumptions` and `open_decisions` arrays.** Rejected for now: `spec@1` is named in more than 70 authored files across seven plugins, the Codex skills and the pipeline fixtures, and every consumer already reads `scope`. Revisit when a stage needs to process assumptions programmatically, for example a drift check that re-tests each assumption.
- **`non_goals`.** Rejected: it means "excluded", so an unknown there reads as a decision not to build.
- **`reasoning`.** Rejected: it is a scratchpad that is never forwarded.
- **Criterion text or `rationale`.** Rejected: a criterion states one condition and one observation, `rationale` belongs to `judgment_call` criteria, and a spec-wide assumption has no single criterion.
- **`purpose`.** Rejected: it says why the spec exists, not what it covers or rests on.
- **Leave open decisions out of the spec and only in conversation.** Rejected: conversation context is compressed and lost; the drafter returns only the spec, so the spec is the one place the skill and the gate both see.

## Consequences

Fewer first-round failures for unknowns that do not matter, and decisions that do matter reach the user before planning instead of after a render. Planners and implementers read the assumptions in `scope` and can see what the work rests on; an implementer who finds an assumption false reports a `spec_contradiction` on the criteria that depend on it. Costs: the convention is a line prefix in a free-text field, so no schema enforces it, and a drafter can still label a scope change an assumption; the gate's `Assumption:` rule is the guard. Whether rounds and rewrites fall is not yet measured; compare gate rounds per spec before and after with `docs/evaluation-runbook.md`.

**Enforced by:** `tests/test_spec_unknowns.py` (a `spec@1` carries both lines without a schema change; the drafters, gates and skills in both harnesses use the convention and no longer ban every TBD) and `tests/test_verification_rules.py` (one owning reference). The gate disposition itself is a prompt rule.
