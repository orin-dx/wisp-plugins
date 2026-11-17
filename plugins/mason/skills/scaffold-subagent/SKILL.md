---
name: scaffold-subagent
description: >-
  Trigger when the request names an agent task and tier for an existing plugin, not a new plugin. Creates only the agent file and reports the routing the plugin needs.
version: 2.1.0
---

# Mason — Scaffold Subagent

<overview>
The narrower sibling of `mason/scaffold-plugin`: one agent file for a plugin that already exists, not a full plugin directory. Delegates to `scaffolder` in its single-subagent mode.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **scaffolder** (single-subagent mode) | sonnet / medium | An existing plugin needs exactly one new conformant agent file for a given task and tier. |
</dispatch>

<references>
`shared/agent-best-practices.md`
</references>

<io>
**Consumes**: target plugin ID, task description, model/effort tier
**Produces**: one agent file at `plugins/<id>/agents/<role>.md`. Does not touch `plugin.json` or `SKILL.md` — if the new agent should be dispatched from a skill, that wiring is a separate manual step.
</io>
