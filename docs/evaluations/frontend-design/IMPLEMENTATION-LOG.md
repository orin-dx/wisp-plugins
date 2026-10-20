# Wave 0 implementation log

Status as of 2026-10-20 on branch `worktree-frontend-design-evaluation`. Five of the Wave 0 work packages in `CATALOG.md` are started or done. Nothing is released: no plugin version, changelog or tag changed (see "Release bookkeeping").

| WP | Status | What changed | Verified by |
| :-- | :-- | :-- | :-- |
| WP-617 Codex model ids | Done | `harnesses/codex/agent-roles/README.md` names `gpt-6-luna`, `gpt-6.1-sol` and `gpt-6-astra` (the selectable models on the Codex models page, 2026-10-20), notes that effort labels are relative and the tiers are unevaluated; generated `dist/codex` copies regenerated | `just marketplace-check`; no `gpt-5.6` or `terra` left in `dist`, `harnesses` or `.agents` |
| WP-620 Claude manifests | Done | `tools/sync-claude-manifests.py` generates `plugins/<id>/.claude-plugin/plugin.json` (name, version, description, author) from each `plugin.json`, with `--check`; `just claude-manifests` is in `just check` and CI; `just claude-validate` runs `claude plugin validate --strict` on every plugin and the marketplace | `just claude-validate`: 10 plugins and the marketplace pass `--strict`, and validation now reads each manifest (before, the directory form checked nothing) |
| WP-622 AGY and root marketplace | Partly done | Removed the dead `$schema` URL (404) from the root `marketplace.json`; nothing in tests, scripts or CI read it | `just check` |
| WP-624 Hook validator spike | Done as a spike | `tools/validate-handback.py`, a `PreToolUse` hook on `SubagentHandback` that checks exit-gate handbacks against their verdict schema, denies with the errors, caps denials at 3 per agent, and fails open; not registered by any plugin | `tests/test_handback_validator.py` (11 tests) and `verification/scripts/handback-conformance.py` over 45 recorded verdicts |
| WP-625 Reasoning-wording lint | Done | `tests/test_reasoning_wording.py` fails on text that demands reproduced reasoning (verbatim, step-by-step, chain of thought), with one documented exception for the immutable `requirement@1` schema | Passes; fails when the probe's demand is planted in an agent file |

## What the work found

- **`claude plugin validate plugins/<id>` was a false pass** because the manifests sit at the plugin root. With the generated `.claude-plugin/plugin.json` it validates the manifest, and the repo-only keys (`id`, `consumes`, `produces`) stay in `plugin.json` where Claude Code ignores them.
- **Recorded gate verdicts nearly all conform to their schemas.** 33 of 45 conform; all 12 violations are `verdict_summary` over 300 characters (`VERIFY-3.md` section 5). A hook would have asked for one trim on about 27% of handbacks.
- **`muse` gates emit `verdict@3`-shaped output** (35 of 45) while `muse` documents `verdict@1`. WP-02 should migrate `muse` before the hook is enabled for it; until then the validator accepts either.
- **A bug in the validator was found only by real data:** a schema property with a list of types (`["string", "null"]`). It is fixed and has a regression test.
- **The `requirement@1` schema describes `reasoning` as "chain-of-thought during capture".** It is immutable (ADR 004), agents reach it through a file read and not a prompt, so the lint carries a documented exception; a future `requirement@2` should use the "private scratchpad" wording.

## Open items from this work

- The README documents AGY installs through the community `agy-plugins-cli`. Fetched source snippets suggest that tool discovers plugins as top-level repository directories, which would not find plugins under `plugins/`. This is unverified; test an install in an isolated environment before changing the README (WP-622, WP-621).
- The installed plugins use `shared -> ../../shared` symlinks and the Claude marketplace installs from the `plugins/<id>` subdirectory (`git-subdir`). Whether the symlink resolves after install is untested (WP-621).
- The hook is a spike: it needs a plugin `hooks/hooks.json` registration, a decision on how it is distributed (the tool lives outside any plugin directory), and a check against a live gate agent in auto mode before WP-602 builds on it.
- Hook behavior on Claude Code 2.1.292: `onFailure: "block"` needs 2.1.295, so a crashing hook does not block (the validator fails open by design).

## Change record (shared/harness-authoring.md)

```text
Classification: Codex workflow (role-card resource), distribution (generated bundle), shared identity (Claude manifest generation, root marketplace)
Counterpart reviewed: plugins/*/plugin.json, .claude-plugin/marketplace.json, harnesses/codex/agent-roles/README.md, shared/harness-authoring.md, docs/codex-marketplace-release-policy.md
Intent preserved: role boundaries and the delegation packet are unchanged; only model ids and a freshness note changed. Plugin identity (id, version, author, consumes, produces) is unchanged and still authoritative in plugins/<id>/plugin.json.
Intentional divergence: Claude Code reads .claude-plugin/plugin.json, so a generated minimal manifest sits beside the repo manifest; Codex tiers were re-chosen by position (luna, sol, astra) and are explicitly unevaluated.
Codex role impact: model ids in all ten materialized agent-roles/README.md files; no skill changes.
Verification: just check; just claude-validate; python3 -m unittest discover -s tests; scripts under docs/evaluations/frontend-design/verification/scripts
```

## Release bookkeeping not done

The repo's contribution checklist asks for a plugin version bump, a plugin changelog entry and a matching marketplace entry when a plugin's behavior changes, and the version check compares all of them. These changes touch every plugin's packaged files (the Codex role README, a new Claude manifest), so a release would bump all ten plugins and the ecosystem version together. That is a release decision, so no version, changelog or tag was changed. Until then `just versions` passes because nothing it compares moved, and the generated Claude manifests copy whatever version `plugin.json` has.
