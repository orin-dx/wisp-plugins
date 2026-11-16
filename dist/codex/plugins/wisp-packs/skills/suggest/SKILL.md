---
name: suggest
description: Recommend which house packs fit a repo and where to point to them. Use for "which packs should this repo use". Edits nothing.
---

# Packs: suggest

Recommend and point; edit nothing.

1. Read the first line of each pack in this plugin's `packs/` directory; it says when the pack applies.
2. Look for evidence of fit in the repo: manifests (`Cargo.toml`, `package.json`, `tsconfig.json`), lint and format configs, the justfile or CI, and nested `AGENTS.md` files (monorepo packages).
3. For each pack that fits, give the evidence (the file that shows it), the exact line to add (for example `Packs: rust-house`) and where: the root `AGENTS.md` for the whole repo, or the nested `AGENTS.md` of the package where only that part applies. Say what the pack would change in how work here is done.
4. Skip a pack when the evidence is thin and say so. Note packs the repo already declares and rules it already states that a pack repeats.
