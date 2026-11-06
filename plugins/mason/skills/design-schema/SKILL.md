---
name: design-schema
description: >-
  Trigger when the user wants a new inter-agent artifact schema: "design a schema for X", "add a new schema to shared/schemas", "what should this handoff look like?". Given what the artifact represents, its producer, and its consumer, returns a draft 2020-12 JSON Schema checked for conflicts with existing schemas.
version: 2.0.0
---

# Mason — Design Schema

<overview>
The schema that ships first sets the pattern every consumer inherits — required vs. optional has to be a deliberate choice. Delegates to `schema-designer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **schema-designer** | sonnet / medium | A new inter-agent artifact needs a JSON Schema designed and checked against existing schemas for conflicts. |
</dispatch>

<references>
`shared/schemas/` (existing schemas, checked for conflicts before proposing a new one)
</references>

<io>
**Consumes**: artifact description, producer, consumer(s)
**Produces**: JSON Schema object plus a recommended filename (`shared/schemas/<name>@<version>.json`).
</io>
