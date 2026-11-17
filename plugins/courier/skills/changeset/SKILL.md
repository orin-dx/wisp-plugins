---
name: changeset
description: >-
  Use this, not freehand text, whenever a changeset, changelog entry or release note is written or edited: "add a changeset", "write the changeset for PR 12", "update the changelog", "what should the release note say". Turns a diff into layered changeset@3 entries, one per user-visible outcome, or recommends none. Pass the criteria_evidence along when the work produced it.
version: 3.0.0
---

# Courier — Changeset

<overview>
A changeset is the changelog entry, written once at authoring time and later aggregated — not rewritten — into a release. `changeset-analyzer` decides what a consumer upgrading, scripting or setting up needs to know, works at the level of user-visible outcomes rather than pull requests, and writes each entry as a lead line plus bullets or audience sections when there is more to say. It can update an existing unreleased entry or recommend that none is needed. No length cap applies; detail follows what the reader needs. Delegates entirely to `changeset-analyzer`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **changeset-analyzer** | sonnet / medium | A git diff needs structured `changeset@3` entries, an update to an existing entry, or a recommendation that none is needed. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/references/delivery/changesets.md` — changeset format, disposition, the Semver table (including CLI and serialized-file rows), entry shape, and the voice standard for this artifact.
</references>

<io>
**Consumes**: git diff (a single PR's, or a larger backlog/catch-up diff since the last release), optionally a linked `spec@1`, optionally the aggregated `criteria_evidence` the implementation produced
**Produces**: one or more `changeset@3` entries conforming to `${CLAUDE_PLUGIN_ROOT}/shared/schemas/changeset@3.json` — one per user-visible outcome, never one entry bundling unrelated outcomes together. Route to `courier/pr` or `courier/release` depending on the next stage. When the repository keeps changesets as files (for example `.changeset/*.md`, written by `changeset add` or a project CLI such as `callisto add`), save each `new` or `update-existing` entry in that format with the package and the bump from `semver_impact`, using the repository's tool when it has one. A repository whose release PR aggregates changesets does not need `courier/release`.
</io>
