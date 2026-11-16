---
name: design-schema
description: >-
  Trigger when the user wants a new schema for an artifact that code or a hook consumes: "design a schema for X", "add a schema to shared/schemas", "what should this handoff look like?". Given what the artifact represents, its producer and its consumer, returns a draft 2020-12 JSON Schema checked for conflicts with existing schemas, or says a schema is not warranted.
version: 2.1.0
---

# Mason — Design Schema

<capability>
The schema that ships first sets the pattern every consumer inherits, so required versus optional is a deliberate choice. Delegates to `schema-designer`. A schema is warranted where code or a hook consumes the artifact, as the handback hook checks `verdict@3`; a handoff only another agent's prompt reads is a stage document, and the answer is plain fields in the brief or the evidence.
</capability>

<agents>
| Agent | Model / Effort | Delegate when |
| :--- | :--- | :--- |
| **schema-designer** | sonnet / medium | A new artifact has a code or hook consumer and needs a schema checked against existing ones. |
</agents>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/` (existing schemas, checked for conflicts before proposing a new one)
</references>

<finish>
Produces the schema object and a recommended filename `${CLAUDE_PLUGIN_ROOT}/shared/schemas/<name>@<version>.json`. A breaking change is a new version, never an edit. Run `just check`, judged by exit code, after saving it.
</finish>
