# ADR-017: Agent bodies drop the `<backstory>` section

**Status:** Accepted
**Date:** 2026-11-14
**Amends:** ADR-001 and ADR-006, which listed `<backstory>` as a required section. The rest of both stands: no `<role>` body section, no `success_criteria` checklist, a byte-identical `<constitution>`.

## Decision

Every agent body defines four sections in order: `<constitution>`, `<goal>`, `<judgment>`, `<output>`, plus the optional `<load_first>` after `<constitution>`. All `<backstory>` blocks are removed.

A backstory fact that appears nowhere else in the agent becomes a plain sentence in `<judgment>`; persona narrative is not kept. One agent needed this: `weaver:intake` now states that `why` names the pain behind the request, not a restatement of the feature.

`<role>` and `success_criteria` stay out, the frontmatter `role:` remains routing metadata, and EARS stays confined to `<constitution>` and `<output>` (ADR 002, ADR 006).

## Why

ADR 001 chose an experiential backstory over a role label on the premise that it shapes judgment; the premise was never measured. A backstory is a persona paragraph that costs tokens in every prompt, can pull in role behavior, and almost always only restated the failure mode `<judgment>` already names. A paired ablation on three agents found no measurable difference in catches, size or cost. The seeded defects were easy, so every run hit the ceiling: it shows no measurable effect, not that there is none.

## Rejected

- **Keep the backstories:** no measured benefit, a token cost in every prompt and a risk of role play; removal is the cheaper default.
- **Remove them from the three tested agents only:** leaves two structures to author and audit, with no reason to expect the others differ.
- **Re-run on harder defects first:** a measured loss is the evidence that should reopen this, and waiting costs tokens in every run.

## Consequences

Each prompt is one paragraph shorter and the authoring rule has one fewer part. The incident behind a failure mode is no longer in the file (history keeps it), and a real effect on harder tasks or other models would be missed.

To restore one, write a new ADR that supersedes this one, name the agents and the measured difference, and restore the section only for them, between `<constitution>` (and `<load_first>`) and `<goal>`. Update `PARTS` in `tests/test_agent_structure.py`, the structure rule in `shared/constitution.md`, and the docs and mason agents that state the structure.

Revisit when a measurement shows a loss without the backstory: seeded defects hard enough not to saturate, more agents and models, and more than five runs per condition (`docs/evaluation-runbook.md`).

**Enforced by:** `tests/test_agent_structure.py` (four parts in order, no `<backstory>` or `<role>` section, byte-identical constitution).

**Evidence:** `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "ADR evidence", ADR 017.
