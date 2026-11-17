# ADR-007: Wisp persona naming — plugin ID rename

**Status:** Superseded; umbrella-brand clause by ADR-010 (the family is now **Wisp Plugins**; "Wisp" alone is the library), and the persona id for every lifecycle plugin by ADR-018 (the core is `wisp`; `courier`, `muse` and `mason` keep their ids)
**Date:** 2026-08-27
**Supersedes:** none — this is a naming/identity change, not a structural one. All prior ADRs (001-006) remain in force under the new plugin ids.

## Decision

Every plugin id is a persona, a character or craft-role archetype evocative of the plugin's function, and the literal action lives in the skill name as `persona:action` (for example `ranger:audit`, `sentinel:gate`).

- **Skill names:** the five single-skill plugins, whose skill name duplicated the plugin id, rename the skill to the literal action. The four multi-skill plugins keep their skill names and change only the id prefix.
- **A tenth plugin:** `muse`, a component-specification plugin (Design category, alongside `scribe`) added in the same change. It reuses `spec@1` and `verdict@1` unchanged.
- **Versioning:** each renamed plugin takes the next major version, the `feat!:` plus `BREAKING CHANGE: plugin ID changed` precedent in `shared/references/delivery/commits.md`.
- **Umbrella brand:** the original decision named the family "Wisp"; ADR-010 replaced that with Wisp Plugins.

| Old id | New id | Category | Skill |
| :--- | :--- | :--- | :--- |
| `graph` | `weaver` | Requirements | unchanged |
| `trace` | `vanguard` | Research | `research` (was `trace`) |
| `canon` | `scribe` | Design | unchanged |
| — | `muse` (new) | Design | `component` |
| `vector` | `navigator` | Planning | `plan` (was `vector`) |
| `lambda` | `smith` | Implementation | `implement` (was `lambda`) |
| `proof` | `ranger` | Verification | `audit` (was `proof`) |
| `axiom` | `sentinel` | Verification | `gate` (was `axiom`) |
| `delta` | `courier` | Shipping | unchanged |
| `basis` | `mason` | Meta | unchanged |

## Why

- **Abstract ids stopped cueing function:** `graph`, `trace`, `canon`, `vector`, `lambda`, `proof`, `axiom`, `delta` and `basis` mapped loosely to a domain concept, which worked for a handful of plugins. Past nine, nobody could tell `canon` from `axiom` from `basis` without a lookup, so skills were routed by table, not recall.
- **A persona is a memory hook:** a `ranger` hunts bugs, a `sentinel` guards a gate, a `smith` forges implementation, a `scribe` writes specs; the id is inferable instead of memorized.
- **The skill carries the literal action:** this avoids the collisions that literal plugin names hit, where `canon` and `muse` both want "spec-writer" and `axiom` collides with the exit-gate every plugin already names internally.

## Rejected

- **Keep the abstract nouns and add a lookup table to every doc:** because it treats the symptom, not the cause (the names carry no signal), and the table is one more thing to keep in sync.
- **Literal function names for plugin ids** (`spec-writer`, `bug-hunter`, `verifier`, `planner`): because several plugins do not compress to one literal word without collision, and a persona leaves the skill name free to carry the literal action.

## Consequences

- **Breaking:** the old ids in scripts, CI or muscle memory stop resolving, so `/plugin install <old-id>` and `<old-id>:<skill>` must change. The five single-skill plugins also renamed their skill, a second break for anyone calling `<old-id>/<old-id>` directly.
- **Unchanged:** schemas, agent behavior and pipeline logic. ADRs 001-006 still govern structure.
- **New scaffolds:** `mason:scaffolder` and `mason:auditor` default a single-skill plugin's skill name to the literal action, not the plugin id.

## Evidence

- Commit `a859e2f2`, which made the rename and the mapping above.
