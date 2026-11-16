---
name: scaffold-subagent
description: >-
  Trigger when the request names an agent task for an existing plugin, not a new plugin. Tests that the agent needs its own context or risk tier, then creates only the agent file and reports the routing the plugin needs.
version: 3.0.0
---

# Mason — Scaffold Subagent

<capability>
The narrower sibling of `mason/scaffold-plugin`: one agent file for a plugin that already exists. Delegates to `scaffolder` in its single-agent mode.
</capability>

<test>
First ask whether the primary agent could do the work in its own context, with a skill section, a hook, a pack or a reference. If it can, say so and create nothing. An agent is justified only by a fresh context that must not share the worker's reasoning, one disputed claim, a bulk read-only sweep, or a hidden oracle (ADR 018). Adding an agent is the owner's decision, so bring the choice as a decision card with a recommendation.
</test>

<agents>
| Agent | Model / Effort | Delegate when |
| :--- | :--- | :--- |
| **scaffolder** (single-agent mode) | sonnet / medium | The test passes and the owner wants the agent. |
</agents>

<references>
`shared/agent-best-practices.md`
</references>

<finish>
Produces one file at `plugins/<id>/agents/<role>.md` and leaves `plugin.json` and `SKILL.md` alone; the report names the routing the entry skill needs and the manifest entry to add. After wiring, run `just claude-manifests-sync` and `just check`, judged by exit code.
</finish>
