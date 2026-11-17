# Conventional Commits Reference

**Format:** `<type>(<scope>): <description>`

Types: `feat` `fix` `docs` `style` `refactor` `test` `chore` `perf` `ci` `build` `revert`

Breaking change: append `!` after type/scope, or add `BREAKING CHANGE:` footer.

## Rules

- Subject line: imperative mood, no period, under 72 characters
- Body (optional): explain the *why*, not the what. Do not artificially wrap lines — one paragraph per line, let the terminal/renderer soft-wrap.
- Footer: `BREAKING CHANGE: <description>`, `Fixes #123`, `Refs #456`
- Scope is optional; when used, it names the module or component
- Match the repository you are in: use the scopes and subject style in its recent history or commit configuration. The scope table below applies only to this repository.
- Put a limit, constraint, or tradeoff a future reader of the log needs in the body, not in a scratchpad.

## Examples

```
feat(courier): add changeset generation skill

fix(wisp): pass the verifier's blockers to the retry

docs(shared): add conventional-commits reference

refactor(wisp): extract workspace detection into recon subagent

feat!: rename guard to wisp

BREAKING CHANGE: plugin ID changed from guard to wisp.
Update marketplace.json and skill trigger references.
```

## Commit Message Body

The body answers: why was this change needed? What problem does it solve?

Don't describe what the code does (the diff shows that). Write what a reviewer needs to understand the intent.

## Voice

Use active voice and imperative mood. Name the technical outcome in the subject and explain only the non-obvious reason in the body. Remove adjectives that stand in for mechanism or evidence. Full standard: `shared/references/authoring/voice.md`.

## Scope Conventions (this repo)

| Scope | Covers |
|---|---|
| `wisp` | wisp plugin, skills and subagents |
| `wisp-packs` | wisp-packs plugin and packs |
| `courier` | courier plugin and subagents |
| `mason` | mason plugin and subagents |
| `muse` | muse plugin and subagents |
| `shared` | shared schemas, references, agent-best-practices |
