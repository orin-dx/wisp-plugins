---
name: scaffold-plugin
description: Create the smallest plugin that delivers a purpose. Use when the user asks to build or scaffold a plugin; derive structure from the repository constitution and validate the result before handoff.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Scaffold a v5 plugin

Start from the outcome the plugin gives its owner, then build the smallest plugin that delivers it. Do not create a folder of placeholders that leaves the next author to rediscover the contract.

## Design

Read `shared/constitution.md` first. Inspect the closest existing plugin (`plugins/wisp` is the reference for an entry skill with mode aliases), without copying a workflow merely because its layout looks similar. Decide, and state each choice in the report:

- **Agents:** none by default. Add one only where a fresh context must not share the worker's reasoning, one disputed claim needs settling, a bulk read-only sweep should stay out of the worker's context, or a hidden oracle must stay hidden (ADR 018). Never for a role or a stage. Adding an agent is the owner's decision: bring it as a decision card with a recommendation.
- **Entry:** one skill named for the plugin id. Distinct modes become one-line alias skills that start it. Split into independent skills only for genuinely independent intents.
- **Handoffs:** no mandatory gate chain and no stage documents. Define `shared/schemas/<name>@<version>.json` first, and only where code or a hook consumes the artifact.
- **Prompts:** the outcome, constraints and evidence bar. Number steps only where order changes correctness.
- **Must-hold rules:** a hook or a project check, not prose. The pattern is `wisp:verifier` with the handback validator and the Stop hook. Codex has neither hook, so a Codex skill states the rule itself.
- **Language and house rules:** a pack in `plugins/wisp-packs`, adopted by a `Packs:` line in `AGENTS.md`, or a reference loaded on demand. Not an agent or a plugin per language.
- **Evidence and references:** add verification rules only for the claims the plugin makes. Give each runtime reference its outcome, applicability, evidence and refutation, owned by a cognitive concern, with the language as filename only for language-specific evidence. Do not universalize one codebase's preference or omit a named language or platform.
- **Harnesses:** Claude Code, Codex and Antigravity are all kept. Read `shared/harness-authoring.md` when the plugin ships to more than one, and give Codex its own tree under `harnesses/codex/plugins/<id>/` rather than assuming Claude instructions are portable.

## Build

1. Create the source plugin: manifest, entry skill, README, changelog, `shared` symlink, and only the justified agents, each with the four sections: constitution (copied byte for byte from an existing agent), optional load_first, goal, judgment, output.
2. Create the Codex-native tree and its catalog entry when Codex is in scope.
3. Run `just claude-manifests-sync`, `just marketplace-sync` and `just check`, and judge each by exit code. Report any you did not run.

## Team use

This is tightly coupled work: complete it yourself. For a comparable-plugin inventory only, read `agent-roles/README.md` and use the `recon` card read-only; without subagents, do the inventory yourself.

## Output

Report created paths, the design choices above, schema producers and consumers, validation results, and any user decision still required. Do not register, install, publish, or commit the plugin unless the user explicitly requests each action.
