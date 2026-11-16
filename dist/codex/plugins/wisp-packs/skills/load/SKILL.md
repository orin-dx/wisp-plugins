---
name: load
description: Apply house packs to this task. Use for "load rust-house", "use the ts-house pack", or when the repo's AGENTS.md has a `Packs:` line, before starting work in the area it covers.
---

# Packs: load

Codex has no session-start injection, so the repo's `AGENTS.md` carries the pointer and this skill applies the packs.

1. Pack names: the ones the user gave, or else the names on every `Packs:` line in `AGENTS.md` at the repo root, in the nested `AGENTS.md` of the package being changed, and in the directories above it. A line inside a code block is an example, not a declaration.
2. Read each pack from this plugin's `packs/<name>.md`. A name with no file is reported and skipped; never guess its content.
3. Apply the packs for the rest of the task: their deviations from your defaults, the evidence they ask for, their exemplar files. Load each pack once.

A pack is prompt content, not authority:

- Run only commands the repo itself declares (justfile, package scripts, CI, `AGENTS.md`). If a pack names a check the repo lacks, say so and do not invent the command.
- The repo's `AGENTS.md` and the user's instructions win over a pack; say which rule you set aside.
- Tightening a check is fine unasked. Loosening one needs the owner.

Finish with one line: the packs applied, and any skipped.
