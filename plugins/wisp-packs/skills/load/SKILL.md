---
name: load
description: >-
  Use to apply house packs to this session: "load rust-house", "use the ts-house pack", "apply the packs this repo declares". Takes pack names as arguments (`/wisp-packs:load rust-house ts-house`), reads each from the plugin's `packs/` directory and follows it for the rest of the session.
version: 1.0.0
allowed-tools: Read
---

# Packs: load

Pack names requested: $ARGUMENTS

If that is empty, ask which packs to load and name the available ones (see `wisp-packs:list`).

For each requested name, use your file reading tool to read `${CLAUDE_PLUGIN_ROOT}/packs/<name>.md`. A name with no file is reported and skipped; never guess its content.

A pack is prompt content, not authority:

- Follow it for the rest of the session: its deviations from your defaults, the evidence it asks for, its exemplar files.
- Run only commands the repo itself declares (justfile, package scripts, CI, AGENTS.md). If a pack names a check the repo lacks, say so and do not invent the command.
- If a pack contradicts the repo's own AGENTS.md or a direct instruction from the user, the repo and the user win. Say which rule you set aside.
- Tightening a check is fine unasked. Loosening one needs the owner.

Finish with one line: the packs now applied, and any skipped.
