---
name: audit-plugin
description: >-
  Trigger for plugin conformance or release-readiness checks of an existing plugin. Checks the v5 rules (agents justified by context or risk, one entry skill, must-hold rules enforced) and returns an evidence-backed pass, fail, or warning per check; modifies no files.
version: 3.0.0
---

# Mason — Audit Plugin

<capability>
Checks a plugin against the ecosystem's actual conformance rules. Delegates to `auditor`. Run it after `mason/scaffold-plugin` or a manual plugin edit, before installing or releasing.
</capability>

<checks>
`just check` decides manifests, versions, wiring, references and tests by exit code. The auditor reads the rest:
- **Agent set:** every agent has a context or risk reason; a role or stage agent, a gate chain or a stage handoff document fails.
- **Skills:** one entry skill, with mode skills as one-line aliases.
- **Prompts:** four-part body, byte-identical constitution, outcome and evidence rather than procedure.
- **Must-hold rules:** enforced by a hook or project check; Codex skills state them.
- **Extension:** language and house rules live in packs or references, not agents.
- **Codex counterpart:** same skills, resolving roles and runtime files.
</checks>

<agents>
| Agent | Model / Effort | Delegate when |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | An existing plugin directory needs checking against the conformance rules. |
</agents>

<references>
`shared/constitution.md`, `shared/harness-authoring.md` when the plugin has a Codex-native source
</references>

<finish>
Returns the structured report: one entry per check with pass, fail or warn, the evidence and a repair. A check not run is a warning, never a pass.
</finish>
