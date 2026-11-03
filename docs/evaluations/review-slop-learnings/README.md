# Review and slop learnings: plugin improvements

Evaluation date: 2026-11-02. Status: proposal, nothing implemented. No plugin version, schema or constitution text changed.

## Evidence and limits

| Source | What it gave | Limit |
|---|---|---|
| Caliper "Road to v1 Alpha" (`ad4b3461`) | 22 Entire reviewer findings (7 runs, caliper/115, /117, /65), 71 findings distilled by the agent, user pushback | Findings fetched for 3 of 88 changes. Sweep claims are relayed, unverified. |
| Callisto sessions `01a16130` (adversarial review), `01a0e02c`, `01a0e02f-*` (research lanes), `a33915af`, `15c732d1` | Release-workflow and redaction defects, user pushback, adopted `AGENTS.md` rules | Codex sessions. Only selected turns of 40-140 MB transcripts read. |
| Plugin inventory of this repo | Current review, evidence and overclaim controls | Partial: not every agent file opened. |

- Callisto has no Entire review profile, so it has no Entire reviewer or judge output. Its "reviewer" evidence comes from a Codex adversarial review and workflow subagents. No "Callisto alpha" session exists.
- Entire's reviewer produced false positives: 4 caliper/65 findings were already fixed and still show as current. Findings need reproduction on current main before action.
- Entire findings carry no slop-versus-bug category.
- Evidence comes from two projects by one author. Patterns are plausible, not proven general.

## Pattern catalogue

Coverage = what the plugins do today.

| # | Pattern | Evidence | Coverage today |
|---|---|---|---|
| P1 | Test cannot fail: stub with hand-typed JSON, string-assertion generator tests, tests that `return` when a tool is missing, tests that run in no CI job | Callisto a33915af, E281, 01a0e02f; Caliper SWP-23 | `smith:mutator` checks discrimination, but nothing rejects stub-fed contract tests or skip-on-missing |
| P2 | Failure read as absence: failed lookup, unparsed history, or missing tool becomes "no problem" | Callisto 01a16130 (#290 guard), 01a0e02f-4ede; Caliper graceful degradation | `ranger` hazard packs do not name it |
| P3 | Projection taken for authority: green check on stale PR, manifest path, shortened ID | Callisto 01a16130 (#248: 12 checks green, 15 of 32 changesets) | None |
| P4 | Harness differs from the real consumer (config defaults, warm vs cold cache) | Caliper `checker_modes_session.mjs`, `provider.ts:69` | `mason:evaluate` covers plugin fixtures only |
| P5 | Producer-consumer boundary never crossed: `release-pr decide` output piped into `verify` fails; `less precise` vs `less_precise` key | Callisto E281; Caliper 01M6FC4227XS64CDFPTB1HT752 | `ranger:boundary-tracer` exists; contract-test requirement is missing |
| P6 | Hand-copied lists and string keys that drift (four credential lists, 2,000-entry allow-list) | Callisto 15c732d1; Caliper patterns 1, 2 | `smith:reviewer` sibling search is the closest control |
| P7 | Docs and specs written from intent: 10 of 30 doc claims false, ~14% of ~95 spec criteria false, `alias_expanded` stated as fact | Caliper sweeps; Callisto V1-REVIEW | `scribe:spec-drift` checks specs against code. Nothing checks README, changelog or docs claims. |
| P8 | Briefs name symbols that do not exist (`redact_native_output`, `ScopedKey`) | Callisto 15c732d1 | Constitution "API Grounding Invariant" covers `spec@1`, `arch-spec@1`, `plan@1` only, not implementer briefs or worker prompts |
| P9 | Premature "done": merged and green reported as published; worker numbers relayed as conclusions | Callisto a33915af; Caliper ("repeated worker numbers as conclusions") | `smith:exit-gate` and `sentinel` reject "implementer said so". Nothing requires an externally observed outcome (tagged, published). |
| P10 | Review output not consulted until the user relayed it | Caliper | None |
| P11 | Unrequested gates and over-engineering ("veneer", ~2,800 lines of gate scripts) | Caliper; Callisto "owner did not state it" | Nothing |
| P12 | Prose slop: filler, vague names ("Durable"), history comments, wordy changesets | Both | `shared/references/authoring/voice.md` and `comments.md` cover the writing. They rely on banned words. Review agents do not load them for non-comment slop. |
| P13 | Fix the symptom, not the family | Callisto 01a0e02c, a33915af | `smith:reviewer` sibling search and `scribe:architect` exist |

## Proposals

Ordered by value over effort. "Decision" marks anything that touches a constitution, schema or release version, which is yours to approve.

### A. Extend what exists

1. **`ranger` hazard pack: failure-as-absence and projection-as-authority** (P2, P3). Add two hazards under `shared/references/hazards/*`: an absent, unknown or failed check result must not count as "no finding"; a status, path or truncated ID must not stand in for the object it names. Candidates need a runtime construct to refute, as `adversary` already requires. Effort: small. Decision: none.
2. **`smith:reviewer` and `smith:mutator`: reject tests that cannot fail** (P1, P5). Add to `implementation-review.md` and `evidence.md`: contract tests must consume real producer output, not a stub; tests that skip silently on a missing tool fail under CI; a test must fail on the original defect. `mutator` records a stub-fed oracle as a coverage gap. Effort: small. Decision: none.
3. **`sentinel` and `smith:exit-gate`: externally observed outcome** (P9). For release, publish or deploy criteria, the evidence must be the observed outcome (tag exists, package resolves), not "merged and green". Unobserved becomes `pending_checks`, not pass. `verdict@3` already has the fields. Effort: small. Decision: none.
4. **`navigator:challenger` and constitution API grounding for briefs** (P8). Extend the invariant from specs and plans to any brief or worker prompt that names a function or type, and make `challenger` check named symbols against live code. Effort: small. Decision: constitution text change.
5. **`scribe:auditor` and `drift-checker`: claim grounding in docs** (P7). Allow `drift-checker` to take a docs file (README, changelog, ADR) as the claim source and report each claim as covered, uncovered or drifted. Effort: medium. Decision: none, if it stays within the existing `drift-report` shape; schema bump otherwise.

### B. New capability

6. **Slop review of workspace code** (P6, P7, P11, P12, P13). No agent owns this (see inventory). Recommended shape: a `smith:reviewer` reference pack (a new file beside `evidence.md` in `shared/references/verification/`), not a new agent, per ADR 003 keeping enumeration and judgment separate. The pack lists observable checks: duplicated helpers, hand-copied lists with no single source, history comments, comments restating signatures, dead code, unrequested gates, docs claims with no matching code. Each check requires a file and line. Effort: medium. Decision: none for the pack. A new agent would need ADR review.
7. **Judge-style consolidation of multiple reviewer reports** (P10, plus Entire false positives). Add a `sentinel` step that takes reviewer reports (Entire findings, `ranger` candidates, `smith` review), reproduces each on current code, deduplicates, and grades CONFIRMED or PLAUSIBLE, refuting before confirming. Caliper's worker brief already does this by hand. Effort: medium to large. Decision: new artifact schema (`findings-consolidation@1`) and routing.
8. **Review-output intake as a workflow step** (P10). `sentinel:gate` and `courier:pr` check for outstanding Entire review findings on the change before a pass. Needs an Entire reachability fallback, since `entire` calls failed under the sandbox here. Effort: small. Decision: whether plugins may call `entire` at all.

### C. Process for the plugin authors (not plugin code)

9. **Harness fidelity** (P4): `mason:evaluate` fixtures should copy the real consumer's config. Effort: small.
10. **Succinct-writing and owner-confirmation rules** (P11, P12): both projects' `AGENTS.md` already carry these. Lift them into `voice.md` as detection rules (empty claims, repetition, unrequested gates) rather than banned words, which the earlier voice-guide review flagged as the weak spot. Effort: small.

## Recommended first batch

Proposals 1, 2, 3 and 6 (pack only). Together they cover P1 to P3, P5 to P7, P9 to P13 without a schema or constitution change, and each is a reference edit with a focused test in `tests/`.

## Open decisions

- Constitution change for proposal 4.
- Whether to commission proposal 7 and its schema.
- Whether plugins may depend on the `entire` CLI (proposal 8).
- Whether to re-run this evaluation after pulling Entire findings for the 85 Caliper changes not checked here.
