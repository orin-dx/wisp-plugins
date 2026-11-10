---
name: promote
description: Turn a chosen sketch option, or a spike that worked, into a requirement that carries the decision, the approved render and what was and was not verified. Use when exploration should become real work. It does not build, spec or plan.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Carry a decision across into the gated pipeline

A sketch or a spike is non-binding and never counts as evidence for a gate. This is the only route from one into a gated stage. It runs in the primary agent and has no gate of its own; the requirement is gated by the stage that consumes it. Read `shared/references/architecture/modes.md` for the mode rules.

## Inputs

- An `option-set@1` (`shared/schemas/option-set@1.json`) with an option whose `status` is `chosen`, or a `spike-report@1` (`shared/schemas/spike-report@1.json`) whose `conclusion` is `works` or `partly`.

## Workflow

1. Confirm there is something to promote. A sketch needs a chosen option; if none is chosen, ask the user to choose or offer another round. A spike that `fails` or is `inconclusive` is not promoted: report what it showed and what would answer the question. Never promote on your own preference.
2. Draft a `requirement@1` conforming to `shared/schemas/requirement@1.json`.
   - `statement`: what to build, in one sentence, from the chosen option's summary.
   - `stakeholder`: the brief's audience. `why`: the brief's problem and the recorded reason for the decision.
   - `done_when`: conditions checkable from outside, derived from the option's structure and render. Include one that the built result matches the approved render at its recorded location in layout and hierarchy, reviewed by the owner, and label it as a human review. Mark any condition that rests on an unverified assumption and carry the unverified items forward as conditions to confirm.
   - `out_of_scope`: the brief's non-goals plus each rejected and parked option by name with its reason.
   - `linked_issues`: the sketch or spike and option (for example `SKETCH-001/OPT-rail`), the artifact path and the approved render.
3. Make sure the sketch is `decided` and its `decisions` include the choice; for a spike, copy its `verified` and `unverified` lists. Do not rewrite earlier entries.
4. Say the scratch builds are throwaway: they are discarded or rebuilt through a planned implementation, never extended in place.
5. Name the next stage and stop: `component` for a component whose behavior and accessibility must be pinned down, a specification skill for other work, or requirement clarification if the requirement has gaps. End with one line: "Skipped by design: a gate on the sketch; the requirement is gated by the next stage."

## Requirement shape

Follow this shape exactly, because the requirement is checked against `requirement@1`: `id` (for example `REQ-001`), `statement`, `stakeholder`, `why`, `done_when` (at least one item), and optionally `out_of_scope`, `priority` (`critical`, `high`, `medium` or `low`), `linked_issues` and `reasoning`. No other fields are allowed, so the sketch reference, approved render and verified lists go in `linked_issues` and `done_when`, not in new fields.

## Decisions and stopping

A requirement written here is a draft until the next stage accepts it. Every `done_when` item must be testable from outside the implementation; "looks good" is not one. Preserve the decision reasons exactly. Do not delegate this skill.
