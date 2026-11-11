---
name: promote
description: >-
  Use when a chosen sketch option or a spike that worked should become real work: "promote this option", "let's build option B", "turn the chosen design into a requirement", "that spike worked, make it a feature". Turns an option-set@1 or spike-report@1 into a requirement@1 with the decision, render and what was not verified. The only route from exploration into the gated stages; it does not build, spec or plan.
version: 1.0.0
---

# Muse — Promote Skill

<overview>
Turns a decision made while exploring into a requirement the gated pipeline can accept. A sketch or a spike is non-binding and never counts as evidence for a gate; this skill is how its result crosses over. It keeps the reason for the decision, the render the owner approved and the list of what was not verified, so the next stage starts from facts and not from a lost conversation. It runs in the primary agent and has no gate of its own; the requirement is gated by the stage that consumes it.
</overview>

<dispatch>
None. This skill runs in the primary agent. Do not delegate it.
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/architecture/modes.md`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/option-set@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/spike-report@1.json`, `${CLAUDE_PLUGIN_ROOT}/shared/schemas/requirement@1.json`
</references>

<io>
**Consumes**: an `option-set@1` with an option whose `status` is `chosen`, or a `spike-report@1` whose `conclusion` is `works` or `partly`
**Produces**: a `requirement@1`, written where the repository keeps requirements (a file, or the issue tracker the project uses), with the sketch or spike recorded in `linked_issues`
</io>

<requirement_shape>
Follow this shape exactly, because the requirement is checked against `requirement@1`: `id` (for example `REQ-001`), `statement`, `stakeholder`, `why`, `done_when` (at least one item), and optionally `out_of_scope`, `priority` (`critical`, `high`, `medium` or `low`), `linked_issues` and `reasoning`. No other fields are allowed, so the sketch reference, approved render and verified lists go in `linked_issues` and `done_when`, not in new fields.
</requirement_shape>

<workflow>
1. **Check there is something to promote.** A sketch needs a chosen option; if none is chosen, ask the user to choose or offer another round. A spike with `fails` or `inconclusive` is not promoted; report what it showed and what would answer the question. Do not promote on your own preference.
2. **Draft the `requirement@1`.**
   - `statement`: what to build, in one sentence, from the chosen option's summary.
   - `stakeholder`: the brief's audience.
   - `why`: the brief's problem and the reason recorded for the decision.
   - `done_when`: conditions a person can check from outside, derived from the chosen option's structure and render, for example "At 390px the navigation opens as a full-height sheet". Include one criterion that the built result matches the approved render at its recorded location in layout and hierarchy, reviewed by the owner. Mark any condition that rests on an unverified assumption, and carry the unverified items forward as conditions to confirm.
   - `out_of_scope`: the brief's non-goals, plus each rejected and parked option by name with its reason.
   - `linked_issues`: the sketch or spike and option (for example `SKETCH-001/OPT-rail`), the path of the artifact, and the approved render.
3. **Keep the log honest.** Make sure the sketch is `decided` and its `decisions` include the choice; for a spike, copy its `verified` and `unverified` lists. Do not rewrite earlier entries.
4. **Do not carry code over.** The scratch builds are throwaway. Say they will be discarded or rebuilt through a planned implementation, not extended in place.
5. **Name the next stage and stop.** For a component with behavior and accessibility to pin down, `muse/component`; for other work, `scribe/draft-spec`; if the requirement has gaps, `weaver/clarify-requirement`. Do not start it. End with one line naming what this skill skipped: "Skipped by design: a gate on the sketch; the requirement is gated by the next stage."
</workflow>

<rules>
- A requirement written here is a draft until the next stage accepts it; do not describe it as approved.
- Every `done_when` item must be testable from outside the implementation. "Looks good" is not one; "matches the approved render" is a human review and is labeled so.
- Preserve the decision reasons exactly; do not paraphrase a rejection into something softer.
</rules>
