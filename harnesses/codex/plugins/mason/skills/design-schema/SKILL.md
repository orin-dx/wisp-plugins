---
name: design-schema
description: Design a versioned shared JSON Schema for an artifact that code or a hook consumes. Use when a workflow needs a durable producer-consumer contract or an existing contract must evolve.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Design the boundary before the prompt

Model the artifact's consumers, producers, durable evidence, and failure modes before deciding on fields. A schema exists to make handoffs stable across models and harnesses, not to serialize every thought.

A schema is warranted where code or a hook consumes the artifact, as the handback validator checks `verdict@3`. A handoff only another agent's prompt reads is a stage document: recommend plain fields in the brief or the evidence and write no schema.

## Discovery

1. Read the relevant existing files in `shared/schemas/` and identify the nearest compatible contract.
2. Name the producer, every consumer, lifecycle point, and whether the artifact is persisted.
3. Separate required decision data from optional evidence, from the non-consumed `reasoning` scratchpad.
4. Decide whether the change is compatible. Breaking changes require a new `<name>@<N+1>.json`; never mutate an existing version's contract.

## Schema requirements

Create a Draft 2020-12 schema at `shared/schemas/<name>@<version>.json` with:

- `$id` matching its versioned filename stem.
- A title and field descriptions that explain consumer use.
- Explicit `required` fields and `additionalProperties: false` at every closed object boundary.
- A `reasoning` string for producer scratchpad when the artifact is structured output.
- Precise enums, arrays, and nested shapes where consumers depend on them.

## Validation and output

Validate representative valid and invalid examples against the draft, and run `just check`, judged by exit code. Report the producer/consumer map, compatibility decision, filename, validation evidence, and prompt sites that must cite the exact relative schema path.

## Team use

This is a tightly coupled design: the schema author owns the compatibility decision and the draft. Complete it yourself. To pressure-test consumer assumptions in a fresh context, read `agent-roles/README.md` and use the `adversary` card; without subagents, re-read the draft against each consumer in a separate pass.
