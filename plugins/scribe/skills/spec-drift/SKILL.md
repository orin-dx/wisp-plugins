---
name: spec-drift
description: >-
  Use when asked whether implemented code still matches its spec, weeks or months later: "check spec drift", "does the code still match this spec?", "has this spec drifted?". Given spec_file_path and a workspace root, reports each criterion as covered, uncovered or drifted. On-demand diagnostic, not a gate.
version: 2.0.0
---

# Scribe — Spec Drift

<overview>
Ongoing maintenance health check: does the code still do what the spec says, independent of whether it passed the gate once. When a prior changeset's `criteria_evidence` is available, its file/line pointers are a starting point, never a claim to trust — every pointer gets re-read and re-verified, since code moves. Delegates to `drift-checker`.
</overview>

<dispatch>
| Agent | Model / Effort | Delegate When |
| :--- | :--- | :--- |
| **drift-checker** | sonnet / medium | A spec's `spec_file_path` plus a workspace root need checking for whether the current code still implements every acceptance criterion. |
</dispatch>

<references>
`${CLAUDE_PLUGIN_ROOT}/shared/schemas/spec@1.json`

Keep command output and scripts out of the thread as `${CLAUDE_PLUGIN_ROOT}/shared/references/tooling/context.md` says.
</references>

<io>
**Consumes**: `spec_file_path`, workspace root, optionally prior `criteria_evidence`
**Produces**: drift report — covered / uncovered / drifted arrays plus a summary. Not routed anywhere automatically; a human or caller decides whether drift warrants a `scribe/correct-spec` cycle.
</io>
