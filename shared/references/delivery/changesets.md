# Changesets

## Outcome

Record one user-visible outcome in `changeset@3` so release tooling can preserve its meaning and calculate semver without reinterpreting prose. See `shared/schemas/changeset@3.json`.

## Consumer impact

| Value | Use when |
| :--- | :--- |
| `behavior-change` | Existing observable behavior changes for a consumer |
| `new-capability` | A consumer can do something new |
| `internal-only` | No behavior changes outside the repository |

`release-summarizer` omits `internal-only` entries from consumer release notes.

## Topic boundary

Use one changeset per user-visible outcome, not per pull request or commit. Use these signals in priority order:

1. A shared linked requirement, spec, or plan defines one scope.
2. The author explicitly identifies a coordinated delivery scope.
3. The live diff shows one part exists because of another.

Do not split one outcome by package or file count. Do not bundle changes that could ship independently merely because they share a branch. When the boundary remains uncertain, state the ambiguity in `reasoning` and prefer the split that preserves accurate impact classification.

Verify `consumer_impact`, `semver_impact`, changed files, tests, and criteria evidence against that outcome's own diff slice.

## Disposition

| `disposition` | Use when |
| :--- | :--- |
| `new` | A consumer-visible outcome has no unreleased entry yet |
| `update-existing` | The change extends an outcome an unreleased entry already describes; name it in `updates` and write the full updated entry |
| `none` | No consumer sees it, or it fixes something not yet released; `summary` says why |

## Semver

| Change | Impact |
| :--- | :--- |
| Documentation or self-description only | `none` |
| Internal refactor or test-only change | `none` |
| Bug fix in runtime agent or skill behavior | `patch` |
| New optional schema field | `minor` |
| New schema or skill | `minor` |
| New plugin | `minor` |
| New CLI flag, command, or option with a default that keeps current behavior | `minor` |
| Changed CLI output, exit code, or default that scripts or readers already depend on | `major` |
| New optional field in a serialized file or machine-readable output | `minor` |
| Removed, renamed, or newly required field in a serialized file or output | `major` |
| New serialized file or output format | `minor` |
| Removed or renamed schema field | `major`; create a new schema version |
| Renamed plugin ID or incompatible consumer behavior | `major` |

The release version is the highest `semver_impact` among included changesets. Classification comes from the structured field, not wording intensity.

## Breaking changes

Each breaking entry states:

- Old behavior.
- New behavior.
- Required consumer action.

Do not call an internal implementation change breaking unless it changes a supported consumer contract.

## Entry shape

The summary is Markdown with no length target. Lead with the value, then add depth only when the reader needs it.

- Lead line: what the reader can now do or what changed for them.
- Bullets: what they see and where, why it helps, and what to do.
- Audience sections (what you see, scripting, upgrading) when readers differ.
- Limits the reader will hit, stated in the entry, not in `reasoning`.

A one-line entry is correct when that is all there is. Name the visible thing (a link, a label, a flag, a field); vague verbs like "identifies" or "supports" fail.

Bad: `Adds an optional pr field to the preview file and links changes to PRs.` It names no visible thing, no reason, and no limit.

Good:

```markdown
Links each change in the release PR to the pull request that added it.

- Shown as `#123` next to the change, so you can open the review and discussion behind it.
- A changeset added without a pull request (a direct push) gets no link.
- For scripts: the `--emit-preview` file has an optional `pr` for each change.
```

## Voice

Lead with observable consumer impact. Include a reason when it changes understanding or action. Omit internal agent, file, and implementation detail unless the consumer must know it. State limitations and migration work directly. Full standard: `shared/references/authoring/voice.md`.

## Changeset, commit, and release note

| Artifact | Reader | Focus |
| :--- | :--- | :--- |
| Commit | Maintainer reading history | Technical outcome and non-obvious reason |
| Changeset | Package consumer and release tooling | Observable impact and semver |
| Release note | Consumer deciding whether or how to upgrade | Grouped impact and required action |

Write a changeset when a PR changes runtime behavior, adds a consumer capability, changes a model or effort tier, changes a shared schema, adds a skill or plugin, or changes a verification protocol. Skip documentation, reference-only, internal refactor, and test-only changes unless they alter runtime instructions consumed by an agent.

## Release shape

```markdown
## v2.0.0 (2026-08-04)

### Breaking Changes
- Old behavior → new behavior. Required action.

### New Features
- Consumer-visible capability.

### Bug Fixes
- Corrected consumer-visible behavior.
```
