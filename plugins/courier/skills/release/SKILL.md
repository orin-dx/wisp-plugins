---
name: release
description: >-
  Trigger when the user asks to cut a release or summarize what's in one: "cut a release", "what's in this release", "generate release notes". Aggregates changeset@3 entries since the last release into a release-artifact@3, carrying layered summaries through unedited.
version: 3.0.0
---

# Courier — Release

<overview>
A release is an aggregation of changesets already written correctly at authoring time — this skill does not re-narrate anything, it groups and computes the version bump. Delegates entirely to `release-summarizer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **release-summarizer** | sonnet / medium | A set of `changeset@3` entries needs aggregating into a `release-artifact@3` with a computed version bump. |
</dispatch>

<references>
`shared/references/delivery/changesets.md` — the Semver Decision Guide (now machine-enforced via each changeset's `semver_impact`) and Release Notes Generation format.
</references>

<io>
**Consumes**: list of `changeset@3` entries, the prior released version, a release date
**Produces**: `release-artifact@3` conforming to `shared/schemas/release-artifact@3.json`.
</io>
