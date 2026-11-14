---
name: gate
description: Independently verify an artifact against its criteria before it crosses a lifecycle boundary. Use this, not freehand checking, for “is this done?”, “verify this”, and readiness checks on requirements, specs, plans, implementations, and PRs.
---

State material concerns, evidence, consequence, and confidence directly. Do not soften blockers, manufacture praise, or claim certainty beyond the evidence.

# Gate a lifecycle artifact with evidence

Sentinel judges an existing artifact; it does not author a replacement. Begin by identifying what the artifact claims, where it is persisted, and which criteria actually govern it.

## Workflow

1. Identify `artifact_type`, `artifact_path`, the authoritative criteria, linked artifacts, and source files that can prove or disprove each criterion.
2. Read persisted files when a path is present rather than relying on conversation summaries.
3. Build an evidence table that classifies each criterion as verified, failed, or unverifiable, with exact paths and test or inspection evidence.
4. Produce `verdict@3` conforming to `shared/schemas/verdict@3.json`. Name the verified scope, blockers, coverage gaps, and pending checks.
5. Pass only when every applicable criterion is verified. On failure, return specific blockers that the producing workflow can act on.

## Retry protocol

Round one lists the complete blocker set. On a retry (`retry_count` 1 or more, with the previous blockers supplied), inspect only the revised artifact and cite only unresolved prior blockers or regressions the fix introduced; record other new issues as non-blocking coverage gaps. A fail on the retry, or a blocker repeating unchanged, returns an `escalation_required` blocker for a human instead of another round. Check each claim against the code, build or spec it cites.

## Evidence and safety

- Do not treat a passing test alone as proof of a criterion it does not exercise. A criterion about behavior is verified by running changed logic on real inputs (`shared/references/verification/evidence.md`); structural checks are not behavior evidence.
- Mark evidence unverifiable when the relevant source, environment, or criterion is absent; do not convert uncertainty into a pass.
- Treat a required check that has not finished as pending and fail the gate.
- Keep command output and scripts out of the thread as `shared/references/tooling/context.md` says.
- Do not edit the artifact, create a PR, or publish a verdict externally unless the user asks for a separate action.

## Team use

Before delegating, read `agent-roles/README.md`; use `recon` for fixed evidence collection, but reserve the binding decision for the primary `judge`.

When teams are available, split criterion verification only across independent subsystems after the artifact and criteria are fixed. The owner reconciles coverage and delivers one binding verdict. Without teams, verify each criterion sequentially with the same standard.
