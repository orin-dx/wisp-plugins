---
name: list
description: >-
  Use to see which packs exist and which this repo uses: "what packs are there", "list packs", "which packs does this repo declare". Lists the plugin's packs with the line each opens with, and the `Packs:` lines found in AGENTS.md files under the working directory. Read-only.
version: 1.0.0
allowed-tools: Read, Grep, Glob
---

# Packs: list

Use your file reading and search tools. Edit nothing.

1. Available: every `*.md` file in `${CLAUDE_PLUGIN_ROOT}/packs/`. Show its name and its first line (when it applies).
2. Declared: every line starting `Packs:` in `AGENTS.md` at the repo root and in nested `AGENTS.md` files under the working directory, with the file each came from.
3. Report the gap: declared names with no pack file, and available packs the repo does not declare.

Output a short table: pack, applies when, declared where (or "not declared").
