---
name: audit-plugin
description: >-
  Trigger for plugin conformance or release-readiness checks of an existing plugin. Returns an evidence-backed pass, fail, or warning per check; modifies no files.
version: 2.2.0
---

# Mason — Audit Plugin

<overview>
Checks a plugin against the ecosystem's actual conformance rules — not vibes. Delegates to `auditor`. Run this after `mason/scaffold-plugin` or any manual plugin edit, before installing.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | An existing plugin directory needs checking against ecosystem conformance rules. |
</dispatch>

<references>
`shared/constitution.md`, `shared/harness-authoring.md` when the plugin has a Codex-native source
</references>

<io>
**Consumes**: plugin directory path
**Produces**: structured pass/fail/warn report, one entry per conformance check.
</io>
