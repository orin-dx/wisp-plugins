---
name: audit
description: >-
  Use this, not a freehand code review, whenever code is hunted for bugs or vulnerabilities, a suspected bug needs proof, or a fix needs checking: "find bugs in this", "audit this for security issues", "is this really a bug", "did that fix resolve the finding". Rust, TypeScript, JavaScript, Python, Go. Refutes candidates, groups defect families, returns finding-report@2 and verdict@3.
version: 2.4.0
---

# Ranger — Cross-Language Bug Hunting

## Modes

- Full sweep: scan every hazard taxonomy.
- Targeted scan: scan the named category.
- Candidate verification: send the supplied candidate directly to adversary.
- Post-remediation check: run exit-gate against prior findings.

## Pipeline

```text
workspace → recon → scanner → [boundary-tracer] → adversary → finding-report@2 → exit-gate
```

1. `recon` records live files, entry points, languages, capabilities, workspace state, and workflow provenance in `workspace-manifest@1`.
2. `scanner` loads the matching hazard reference and emits `candidate@1` without judgment.
3. `boundary-tracer` produces `field-survival-map@1` for T7 and T10 candidates.
4. `adversary` emits `candidate-assessment@1` for one candidate. It confirms only a reachable failing scenario; external uncertainty produces `plausible`.
5. The caller aggregates findings and their families into `finding-report@2`.
6. After remediation, `exit-gate` independently derives sibling candidates and verifies current code with project-native evidence. It emits `verdict@3`.

## Defect-family route

Treat confirmed findings with the same root cause, domain responsibility, or failure state as one possible defect family. Search beyond copied syntax: equivalent behavior may use different names, control flow, or language.

When a family suggests a missing concept, state, operation, boundary, abstraction, invariant, or enforcement mechanism, pass the complete `finding-report@2` to `scribe:architect` before remediation. Local or unrelated findings remain ordinary remediation work.

## Verification depth

Choose evidence by risk, not language ritual. Use the project-native test, mutation, property, fuzz, race, integration, or boundary tools that can discriminate the suspected defect. A property or fuzz check needs a meaningful generator and oracle. Record unsupported or impractical checks as coverage gaps; do not imply coverage. Keep command output and scripts out of the thread as `shared/references/tooling/context.md` says.

## Dispatch

| Agent | Mode | Tier | Input → output |
| :--- | :--- | :--- | :--- |
| `recon` | Enumeration | haiku / low | workspace → `workspace-manifest@1` |
| `scanner` | Pattern matching | sonnet / medium | manifest → `candidate@1` |
| `boundary-tracer` | Data-flow tracing | sonnet / medium | T7/T10 candidate → `field-survival-map@1` |
| `adversary` | Adversarial judgment | opus / high | one candidate → `candidate-assessment@1` |
| `exit-gate` | Binding verification | opus / high | `finding-report@2` → `verdict@3` |

## Contracts

- Candidates: `shared/schemas/candidate@1.json`
- Candidate assessment: `shared/schemas/candidate-assessment@1.json`
- Workspace: `shared/schemas/workspace-manifest@1.json`
- Boundary evidence: `shared/schemas/field-survival-map@1.json`
- Findings: `shared/schemas/finding-report@2.json`
- Exit verdict: `shared/schemas/verdict@3.json`

Plausible findings pass to `flagged_for_review`; they never become remediation blockers without confirmation.
