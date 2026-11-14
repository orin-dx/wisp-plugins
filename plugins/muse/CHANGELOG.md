# Changelog

— muse

## [1.2.0] - 2026-11-14

### Changed
- The exit gate gets two rounds; after a second failing round, or a repeated blocker, the decision goes to you with the persistent blockers (ADR 015).
- The drafter self-checks and the gate judges; the auditor runs only when you ask, because it reviewed the same draft.
- The gate checks claims and citations against the code, build or spec they refer to; an issue it cannot tie to a source is a note.

## [1.1.0] - 2026-11-10

### Added
- `sketch` and `promote` skills and the `explorer` agent: non-binding exploration with three structurally different options per round, a decision log, and `promote` as the only route into the gated pipeline (ADR 011). New schema `option-set@1`.

### Changed
- The exit gate returns `verdict@3`; it was told to emit a verdict value no schema allows.
- The exit gate lists the complete blocker set in round one and, on a retry, only unresolved or newly introduced blockers; `drafter` self-checks against the same list (ADR 013).
- Output is checked by a hook before it reaches the caller (ADR 012).
- Skill descriptions lead with the request they serve. References load from the plugin root (`${CLAUDE_PLUGIN_ROOT}/shared/...`), so an agent finds them on the first read from any project.

### Fixed
- Removed a reference to a `ranger` accessibility skill that does not exist.

## [1.0.1] - 2026-09-09

### Changed
- Agents now report material concerns directly with evidence, consequence, and calibrated confidence.

## [1.0.0] - 2026-08-27

### Added
- Initial release. Component specification plugin: turns UI/design intent into unambiguous, testable component specs — props, variants, per-state behavior, and accessibility criteria as testable propositions, gated before planning. One skill (`component`), three subagents (`drafter`, `auditor`, `exit-gate`). Reuses `spec@1`/`verdict@1` — no new schema. Tenth plugin in the Wisp-branded ecosystem. See [ADR-007](../../docs/adr/007-wisp-persona-naming.md).
