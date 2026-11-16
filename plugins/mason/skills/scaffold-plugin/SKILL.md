---
name: scaffold-plugin
description: >-
  Trigger for new plugin requests. Given a plugin ID and purpose, builds the smallest v5 plugin that delivers it: manifest, one entry skill, only the agents that need their own context, hooks for must-hold rules, and validates the result.
version: 3.0.0
---

# Mason — Scaffold Plugin

<capability>
Makes the v5 plugin shape the easy one to produce. Delegates to `scaffolder`. The scaffold should pass `mason/audit-plugin` on the first run without manual fixes.
</capability>

<design>
Decide these before generating, and state each choice in the report:
- **Agents:** none by default. Add one only where a fresh context must not share the worker's reasoning, one disputed claim needs settling, a bulk read-only sweep should stay out of the worker's context, or a hidden oracle must stay hidden (ADR 018). Never for a role or a stage. Adding an agent is the owner's decision: raise it as a decision card with a recommendation.
- **Entry:** one skill named for the plugin id. Distinct modes become one-line alias skills that start it, as `wisp`'s `fix` and `build` do; split into independent skills only for genuinely independent intents.
- **Handoffs:** no mandatory gate chain and no stage documents. Define a schema only where code or a hook consumes the artifact.
- **Prompts:** outcome, constraints and evidence bar. Number steps only where order changes correctness.
- **Must-hold rules:** a hook or a project check, not prose. The pattern: `wisp:verifier` returns a `verdict@3` that the handback hook validates, and a Stop hook asks once for the `Not verified:` list. Codex has neither hook, so its skill states the rule.
- **Language and house rules:** a pack in `plugins/wisp-packs` that a repo adopts with a `Packs:` line in `AGENTS.md`, or a reference loaded on demand. Not an agent or a plugin per language.
- **Harnesses:** Claude Code, Codex and Antigravity are all kept; Codex gets its own tree under `harnesses/codex/plugins/<id>/`.
</design>

<agents>
| Agent | Model / Effort | Delegate when |
| :--- | :--- | :--- |
| **scaffolder** | sonnet / medium | A new plugin needs its directory generated from an ID and a purpose. |
</agents>

<references>
`shared/constitution.md`, `shared/agent-best-practices.md`, `shared/harness-authoring.md` when the plugin ships to Codex or Antigravity
</references>

<finish>
Produces `plugin.json`, `README.md`, `CHANGELOG.md`, `skills/<id>/SKILL.md`, the agent files the design justifies and the `shared` symlink. Run `just claude-manifests-sync`, `just marketplace-sync` and `just check`, judged by exit code, then `mason/audit-plugin`. Report what was not run. Do not commit, install or publish unless asked.
</finish>
