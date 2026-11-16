---
name: release
description: >-
  Trigger when the user asks to cut a release or summarize what's in one: "cut a release", "what's in this release", "generate release notes". Aggregates changeset@3 entries since the last release into a release-artifact@3, carrying layered summaries through unedited.
version: 4.0.0
---

# Courier — Release

<overview>
A release is an aggregation of changesets already written correctly at authoring time. This skill does not re-narrate anything: it filters, groups and computes the version bump, which is deterministic, so it runs in the primary agent and has no subagent.
</overview>

<dispatch>
None. This skill runs in the primary agent. Do not delegate it.
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/delivery/changesets.md` — the Semver Decision Guide (machine-enforced through each changeset's `semver_impact`) and the Release Notes Generation format.
</references>

<io>
**Consumes**: list of `changeset@3` entries, the prior released version, a release date
**Produces**: `release-artifact@3` conforming to `${CLAUDE_PLUGIN_ROOT}/shared/schemas/release-artifact@3.json`.
</io>

<workflow>
1. **Collect.** Gather every `changeset@3` entry since the prior release (from `.changeset/`, the changelog's unreleased section, or the entries the user supplies) and read the prior released version from the repository's version source, not from memory. If the prior version or the entries cannot be found, ask; do not guess a version.
2. **Filter.** Drop each entry with `consumer_impact: internal-only` and each with `disposition: none`. If nothing remains, say there is nothing to release and stop.
3. **Compute the version.** Apply `max(semver_impact)` across the remaining entries to the prior version, with major above minor above patch above none. Never choose the version by what sounds right. If every remaining entry is `none`, report that no bump is warranted.
4. **Aggregate.** Carry each entry's `summary`, `consumer_impact`, `semver_impact`, `linked_requirement`, `pr_url` and `commits` through unedited, and collect every entry's `breaking_changes` into the top-level `breaking_changes` array. Never rewrite a summary: `changeset-analyzer` wrote it at the detail its impact earns, and an edit here drifts from what it verified.
5. **Return the `release-artifact@3`** with the version, the date, the included entries and the breaking changes. Put the prior version, which entry set the bump and the formatted release notes in `reasoning`. Check the result against the schema before returning it.
6. **Stop.** Tagging, publishing and pushing are separate actions the user confirms; do not run them from here.
</workflow>

<rules>
- An `internal-only` entry never appears in the output.
- The bump is never lower than the highest `semver_impact` among the included entries.
- A summary is carried through exactly as written.
</rules>
