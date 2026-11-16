# When a spec or plan is worth writing

## Outcome

A spec or plan exists only where a reader needs it: the owner wants to read the contract before code exists, or other work will be built against it. It is never a mandatory stage.

## Applicability

Build mode, before the work starts. Fix, spike and explore never need one.

## Write a spec when

- **Shared contract:** other code, teams or sessions will be built against the behavior (a public API, a schema, a shared component, a protocol).
- **The owner asks to read it** before code exists, or the brief has open decisions that a written contract would settle faster than a render.
- **A UI component** whose states and accessibility must not regress: write the `spec@1` in build mode, and use `muse:sketch` first when the look is undecided.

A spec follows `shared/schemas/spec@1.json` and the checklist and unknowns rules in `shared/references/verification/gate-readiness.md`: falsifiable criteria, error cases marked, unknowns stated as `Assumption:` or `Open decision:` lines in `scope` (ADR 016). It is persisted where `shared/references/workspace/conventions.md` says.

## Write a plan when

- **The work spans sessions** or several people or agents, so the order and the proving test for each outcome must survive compaction.
- **Several subsystems change together** and a wrong order would break the build between steps.

A plan follows `shared/schemas/plan@1.json`: tasks state outcomes, signatures and proving tests, with code only where the logic is non-obvious or a wrong shape is costly (ADR 014).

## Skip both when

- One context can hold the change, and the brief's evidence bar can be checked by running something.
- The outcome is not settled yet: explore or spike first, and promote the result.

## Checking one

A spec or plan makes claims about code (signatures, call sites, existing behavior), so it is shared tier: the verifier checks those claims against the live code with the artifact path as the change. Its rounds are the same two.

## Refutation

A spec written only because the work felt large, that nobody will read or build against, is ceremony. A plan whose tasks restate the diff adds nothing a reviewer needs. Either is a sign to delete it and keep the brief.

## Disposition

- Written: persist and commit it, and cite its path in the brief.
- Skipped: the brief is the contract; say so in the output.
