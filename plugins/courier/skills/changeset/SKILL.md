---
name: changeset
description: >-
  Use this, not freehand text, whenever a changeset, changelog entry or release note is written or edited: "add a changeset", "write the changeset for PR 12", "update the changelog", "what should the release note say". Turns a diff into layered changeset@3 entries, one per user-visible outcome, or recommends none. Pass smith's criteria_evidence along when the change came via smith.
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
`shared/references/delivery/changesets.md` — changeset format, disposition, the Semver table (including CLI and serialized-file rows), entry shape, and the voice standard for this artifact.
</references>

<io>
**Consumes**: git diff (a single PR's, or a larger backlog/catch-up diff since the last release), optionally a linked `spec@1`, optionally smith's aggregated `criteria_evidence`
**Produces**: one or more `changeset@3` entries conforming to `shared/schemas/changeset@3.json` — one per user-visible outcome, never one entry bundling unrelated outcomes together. Route to `courier/pr` or `courier/release` depending on the next stage.
</io>
