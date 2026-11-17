# Changelog

— wisp

## [1.0.1] - 2026-11-16

### Changed
- **Less to read per run:** `work` reads only `modes.md` and `conventions.md` up front and loads the other references when the path needs them, so a contained fix starts with about 1,400 fewer words of context.
- **Packs count as project invariants:** the packs a repo's `AGENTS.md` declares are read with its other invariants, and a pack never overrides a repo check.
- **Question-only turns:** with uncommitted changes, a turn that only answers a question can end with `Not verified: nothing changed this turn`.

## [1.0.0] - 2026-11-15

### Added
- One `work` skill that sizes a change as contained, shared or irreversible, states its outcome, constraints and evidence bar before any edit, and picks the mode and review depth. You are asked only for decisions that change scope or cannot be undone, as decision cards.
- Six commands that start it in a mode: `explore`, `spike`, `fix`, `build`, `check`, `ship`. Exploration hands off to `muse:sketch` and `muse:promote`; shipping to the courier skills.
- A fresh-context `verifier` for shared and irreversible work: it gets the brief, the change and the evidence list, never the worker's reasoning, and runs the code, build or render itself. Two rounds, then the persistent blockers come to you.
- An `adversary` that settles one disputed finding or claim, and a read-only `recon` for unfamiliar workspaces.
- A Stop hook: when changes are left uncommitted and the final message has no `Not verified:` line, it asks once for one.
- A Codex counterpart with the same seven skills; Codex has no Stop hook, so its skills state the `Not verified:` rule themselves.
