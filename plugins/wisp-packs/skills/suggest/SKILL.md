---
name: suggest
description: >-
  Use to find out which packs fit a repo: "which packs should this repo use", "suggest packs", "set up packs here". Looks at the repo and recommends packs and where a `Packs:` line would go. Edits nothing; the owner decides.
version: 1.0.0
allowed-tools: Read, Grep, Glob
---

# Packs: suggest

Use your file reading and search tools. Edit nothing; recommend and point.

1. Read the available packs' first lines (`${CLAUDE_PLUGIN_ROOT}/packs/*.md`), which say when each applies.
2. Inspect the repo for evidence of fit: manifests (`Cargo.toml`, `package.json`, `tsconfig.json`), lint and format configs, the justfile or CI, and any nested `AGENTS.md` (monorepo packages).
3. For each pack that fits, state the evidence (the file that shows it) and the place to point to it: the root `AGENTS.md` for the whole repo, or the nested `AGENTS.md` of the package where only that part applies.
4. Show the exact line to add, for example `Packs: rust-house`, and say what the pack would change in how work here is done.
5. Skip a pack when the evidence is thin; say so rather than padding the list. Note any pack the repo already declares.

Existing repo rules win over a pack. If the repo already states a rule that a pack also states, mention the overlap and recommend the line only if the pack adds something.
