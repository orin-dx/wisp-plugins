---
name: scaffold-subagent
description: Add one conformant agent prompt to an existing source plugin, after testing that it needs its own context or risk tier. Use when the user asks to add an agent without changing the plugin's unrelated routes.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Add one agent only if it earns its place

Inspect the target plugin's manifest, entry skill and existing agent prompts first. This skill changes the source-plugin agent surface; it does not assume the same prompt belongs in the Codex adaptation.

## Test first

Ask whether the primary agent could do the work in its own context, with a skill section, a hook, a pack or a reference. If it can, say so and create nothing. An agent is justified only by a fresh context that must not share the worker's reasoning, one disputed claim, a bulk read-only sweep, or a hidden oracle (ADR 018). Adding an agent is the owner's decision: bring it as a decision card with a recommendation. If the role overlaps an existing agent, report the overlap and propose reuse.

## Workflow

- Confirm the responsibility, input, output and tier (haiku/low enumeration, sonnet/medium drafting and analysis, opus/high independent judgment).
- Read an existing source agent and copy its `<constitution>` byte-for-byte.
- Author `<goal>`, `<judgment>` and `<output>` in that order, with one direct rule per item and the evidence bar the agent must meet. Add one `<load_first>` block only when the agent needs a phase-specific reference.
- Cite `shared/schemas/<name>@<version>.json` for structured output that code or a hook consumes, or create that schema first. A handoff only another prompt reads is plain text.
- Update the manifest and the entry skill's routing only when the agent must be reachable.
- Run `just claude-manifests-sync` and `just check`, and judge each by exit code.

## Boundaries

- Do not alter unrelated agents, skills, or the Codex-native tree to make the source prompt fit.
- Do not create a generic role prompt. Define the agent's actual evidence and judgment boundary.

## Team use

This is a tightly coupled edit. Complete it yourself; do not request an agent team.
