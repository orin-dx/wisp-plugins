---
name: list
description: List the available house packs and the ones this repo declares. Use for "what packs are there" or "which packs does this repo use". Read-only.
---

# Packs: list

Edit nothing.

1. Available: every `*.md` file in this plugin's `packs/` directory, with its name and its first line (when it applies).
2. Declared: every line starting `Packs:` in `AGENTS.md` at the repo root and in nested `AGENTS.md` files under the working directory, with the file each came from.
3. Gaps: declared names with no pack file, and available packs the repo does not declare.

Output a short table: pack, applies when, declared where (or "not declared").
