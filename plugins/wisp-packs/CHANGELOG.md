# Changelog

— wisp-packs

## [1.0.0] - 2026-11-15

### Added
- Packs: plain markdown on how the owner builds, starting with `rust-house` and `ts-house`, mined from the repos' own rules and review findings.
- Three commands: `load` (apply packs by name), `list` (available and declared packs) and `suggest` (recommend packs for a repo, edits nothing).
- A SessionStart hook on Claude Code that injects the packs a repo declares with a `Packs:` line in `AGENTS.md`, once each.
