---
name: audit-backlog
description: >-
  Trigger when the user asks about overall backlog health: "what's in the backlog", "audit the backlog", "what requirements are missing coverage". Cross-references all open requirement@1 objects against specs and implementation. Returns per-requirement status with evidence and a structured summary.
version: 2.0.0
---

# Weaver — Audit Backlog

<overview>
The full-backlog version of `weaver/connect-requirement` — same agent, wider scope. Use this before planning to prevent duplicate or redundant work across the whole open backlog, not just one requirement.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **auditor** | sonnet / medium | All open requirement@1 objects need cross-referencing against specs and implementation for coverage and duplicates. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: all open `requirement@1` objects, workspace access
**Produces**: audit report — per-requirement status/evidence/duplicate_of, plus a backlog health summary. Read-only; does not modify any files.
</io>
