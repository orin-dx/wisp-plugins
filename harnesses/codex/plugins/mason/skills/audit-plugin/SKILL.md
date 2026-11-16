---
name: audit-plugin
description: Audit a plugin against the repository's v5 authoring and packaging rules. Use when the user asks whether a plugin conforms, is installable, or is ready to release.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Audit a plugin from its declared contract

Inspect the named plugin and its declared harnesses rather than evaluating style in the abstract. For cross-harness work, read `shared/harness-authoring.md` and its change record first. Start from manifests and paths, then trace every declared route to its implementation and contract.

## Checks

Run `just check` and judge it by exit code; it decides manifests, versions, wiring, references and tests. Then read what no script decides:

- Agent set: each agent has a context or risk reason (a fresh context that must not share the worker's reasoning, one disputed claim, a bulk read-only sweep, a hidden oracle). A role or stage agent, a mandatory gate chain, or a stage handoff document fails.
- Skills: one entry skill, with mode skills as one-line aliases unless the intents are independent. Trigger discrimination and a concrete workflow, not a procedure where an outcome and evidence bar would do.
- Agent prompts: four-part body (constitution, optional load_first, goal, judgment, output), constitution byte-identical to another agent's, model and effort routing.
- Schemas: only where code or a hook consumes the artifact; versioned, with required `reasoning` and `additionalProperties: false`.
- Must-hold rules: enforced by a hook or project check; the Codex skill states the rule because Codex has no such hook.
- Extension: language and house rules live in packs or references, not agents or per-language plugins.
- Instruction economy: direct, atomic rules without repeated rationale or process narration. Length thresholds trigger review, not failure.
- Runtime references: concern-first paths, language filenames only for language-specific evidence, no human index on a runtime path, applicability and refutation stated for heuristics, complete coverage for every named language or platform.
- Verification evidence: claimed boundaries, semantic searches, generated inputs, mutable state, asynchronous completion and longitudinal comparisons carry their matching evidence; unrelated methods are optional.
- Codex: `.codex-plugin/plugin.json`, native skill directories, interface metadata, catalog runtime files, generated bundle parity, and no unresolved source symlinks in distributable output.

## Evidence standard

Return one row per check with status `pass`, `fail`, or `warn`, the observed path, consequence, confidence, and repair guidance. A check not run is a `warn`, never a `pass`. A missing file is a fail only when a manifest, contract, or required convention declares it. Do not call a plugin ready from filenames alone.

## Team use

An independent conformance reading is a legitimate context split. Read `agent-roles/README.md` and start a fresh subagent with the `reviewer` card, read-only, to read the plugin without your findings; the `recon` card may inventory a large surface. Reconcile the results yourself. Without subagents, do the reading as a separate pass and say it was not independent.

## Safety

This is read-only by default. Do not repair, regenerate, install, or publish a plugin unless the user asks for that follow-on work.
