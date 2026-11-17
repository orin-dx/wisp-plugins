---
name: scaffold-plugin
description: >-
  Trigger for new plugin requests. Given a plugin ID and purpose, generates the manifest, skill, agents, shared linkage, routing, and any needed schemas, and validates the result.
version: 2.2.0
---

# Mason — Scaffold Plugin

<overview>
Makes the correct plugin structure the easy one to produce. Delegates to `scaffolder`. The scaffold should pass `mason/audit-plugin` on the first run without manual fixes.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **scaffolder** | sonnet / medium | A new plugin needs a complete, installable directory generated from an ID and description. |
</dispatch>

<references>
`shared/constitution.md`, `shared/agent-best-practices.md`, `shared/harness-authoring.md` when the plugin will ship to more than one harness
</references>

<io>
**Consumes**: plugin ID, description of what it should do
**Produces**: `plugin.json`, `skills/<id>/SKILL.md`, one stub agent file per declared agent, `shared` symlink. Run `mason/audit-plugin` against the result to confirm conformance.
</io>
