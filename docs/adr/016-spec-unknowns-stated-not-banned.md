# ADR-016: Specs state unknowns as assumptions or owner decisions instead of banning them

**Status:** Accepted
**Date:** 2026-11-14

## Decision

A spec states each unknown in `scope` as an assumption or an owner decision, one per line after the coverage statement; it does not ban unknowns.

- **Line forms:** `Assumption: <the answer the work proceeds on>`, or `Open decision: <question>; options: <A | B>; affects: <criterion ids or scope>`. The convention and gate disposition live in `shared/references/verification/gate-readiness.md` (Unknowns).
- **Drafters:** write unknowns that way and never leave a TBD in a criterion or move an unknown into `non_goals` or `reasoning`.
- **Skills:** put each open decision to the user before gating and redraft with the answer, folded into the spec with the line deleted.
- **Gates fail:** an unknown that leaves a criterion untestable; an `Open decision:` line (blocker criterion `owner_decision`, routed to the user, not the drafter); and an `Assumption:` that changes scope, dependent behavior or cost.
- **Gates pass:** a stated assumption is otherwise not a blocker unless the requirement or code it rests on contradicts it (the claim check of ADR 015).
- **No schema change:** `spec@1` is unchanged (ADR 004).
- **Relation to ADR 013:** this replaces the second item of the checklist ADR 013 created; ADR 013's round rules and ADR 015's round limit stand.

## Why

- **The ban caused churn:** the blanket TBD ban is a human "definition of ready"; it caused first-round failures and churn (ADR 015).
- **It hid unknowns:** it moved unknowns where no later stage sees them. `non_goals` reads as an exclusion, so an unknown there is a silent scope cut, and `reasoning` is never forwarded (ADR 004).
- **Agents need less:** every unknown visible, and resolved, stated as an assumption, or put to the owner when it changes scope, shared behavior or cost.

## Rejected

- **Keep the blanket ban:** because of first-round failures and churn, and unknowns hidden in fields that mean something else.
- **A `spec@2` with `assumptions` and `open_decisions` arrays:** because `spec@1` is named across most authored files, Codex skills and fixtures, and every consumer already reads `scope`.
- **`non_goals`:** because it means "excluded", so an unknown reads as a decision not to build.
- **`reasoning`:** because it is a scratchpad that is never forwarded.
- **Criterion text or `rationale`:** because a criterion states one condition and observation, `rationale` belongs to `judgment_call` criteria, and a spec-wide assumption has no single criterion.
- **`purpose`:** because it says why the spec exists, not what it rests on.
- **Open decisions only in conversation:** because conversation is compressed and lost, and the drafter returns only the spec, the one place the skill and gate both see.

## Consequences

- **Now true:** unimportant unknowns stop failing gates, and important decisions reach the user before planning.
- **Now true:** an implementer who finds an assumption false reports a `spec_contradiction`.
- **Risk:** no schema enforces a line prefix in free text, and a drafter can still label a scope change an assumption; the gate's `Assumption:` rule is the guard.
- **Revisit when:** a stage must process assumptions programmatically (a `spec@2`, for example a drift check re-testing each one), or gate rounds per spec do not fall.

## Evidence

- **Enforced by:** the `spec@1` schema (both lines fit it). The convention and the gate disposition are prompt rules; no test pins their wording.
- `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 016.
