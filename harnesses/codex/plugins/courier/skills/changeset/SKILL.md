---
name: changeset
description: Classify verified changes and write one layered changeset per user-visible outcome, update an existing entry, or recommend none. Use whenever a changeset, changelog entry or release note is written or edited, instead of freehand text.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Record release intent at authoring time

Read the actual diff and any available implementation evidence before writing a changeset. A changeset is the durable consumer-facing statement that release aggregation consumes later; do not re-derive its intent from a vague summary.

## Workflow

1. Inspect the diff and group files by user-visible outcome, not by pull request or commit.
2. Read `shared/references/delivery/changesets.md` before choosing `consumer_impact` or `semver_impact`.
3. For each topic, connect changed behavior to the linked requirement, spec, plan, or exact criteria evidence when available.
4. Produce one object per outcome conforming to `shared/schemas/changeset@3.json`. Write `summary` as Markdown with no length target: a lead line stating the value, then bullets or audience sections when the reader needs more (what changed for them, why it helps, what to do). State limits the reader will hit in the summary. Set `disposition` to `update-existing` (and name `updates`) when an unreleased entry already covers the outcome, or to `none` when no consumer sees the change.
5. Validate required fields, especially `files_changed` and `acceptance_criteria_met`, against observed evidence.

## Classification rules

- Use `internal-only` only when a consumer cannot observe any behavior, API, configuration, or operational change.
- Use the largest required semver impact for the topic; do not dilute a breaking change because it is bundled with a smaller feature.
- Preserve uncertainty in `reasoning`; do not invent evidence or line numbers.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` only for non-overlapping diff-topic inventory and keep the final changeset classification with the primary agent.

When independent diff topics exist and agent teams are available, delegate topic classification by non-overlapping file groups. Merge only after checking that the groups are genuinely independent and each object validates. Otherwise work through the topics yourself.

## Output

Return the structured `changeset@3` object or objects and a short human-readable summary. Do not write, commit, or publish files unless the user asks for that action.
