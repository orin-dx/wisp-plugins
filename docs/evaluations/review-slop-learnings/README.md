# Review and slop learnings, and a plugin cost audit

Evaluation date: 2026-11-02. Status: proposal, nothing implemented. No plugin version, schema or constitution text changed.

## Principle

Spend tokens only where they change an outcome. Two costs, kept apart:

- **Runtime cost** is paid in every session that enables the plugins: agent and skill descriptions, agent bodies, loaded references.
- **Authoring cost** is paid by maintainers: the constitution, `CONTRIBUTING.md`, tests, scripts, the Codex build. `shared/constitution.md` is not loaded by agents. They carry only the 5-line embedded block, identical in all 44 agents (verified).

Cuts must not remove the checks that catch real failures. Every item below has file evidence. Items marked **verified** were re-checked against source after the full-read lanes reported.

## How this was produced

- **Review and slop learnings:** all Entire trail findings for `orin-dx/caliper` and `orin-dx/callisto` (167 changes; 37 findings: 19 open, 18 resolved), plus session learnings from Caliper `ad4b3461` and Callisto `01a16130`, `01a0e02c`, `01a0e02f-*`, `a33915af`, `15c732d1`. Transcripts (126 sessions, 71 MB) were harvested but not read in bulk.
- **Plugin audit:** seven read-only lanes each fully read their files with no sampling: weaver, vanguard and scribe; muse, navigator, smith and sentinel; ranger, courier and mason; the constitution and all references; all 31 schemas with every consumer; docs, ADRs, tests and tooling; the Codex harness build. Not fully read: `dist/` (sampled and diffed against sources) and CHANGELOG bodies (headings only).
- Limits: two projects by one author; Entire's reviewer had false positives (4 Caliper findings were already fixed and still show open); no lane ran the plugins, so tier suggestions are judgments, not measurements.

## Part 1: What review findings show

37 findings: 13 logic bugs, 7 tests that cannot fail or leave a path untested, 5 duplication or hardcoded values, 4 harness-versus-consumer mismatches, 4 docs or comments that misstate behavior, 2 dead code, 2 swallowed errors or bent contracts. Logic bugs are found by reading each change independently; no rule prevents them. The Caliper agent did not consult the review output until the user relayed it.

Proposed additions, one or two lines each in existing reference files, each backed by at least four findings:

1. Specific assertions: a test for a specified error asserts that error; a stub applies the logic it replaces (verification evidence reference).
2. Single source: reuse an existing helper, string or list before adding one (implementation-review reference).
3. Harness fidelity: measurements use the consumer's configuration and time only the measured work (verification evidence reference).
4. Claims match code: comments state current behavior; heuristics are labeled (comments reference).

Held back for lack of a second source: failure-as-absence hazards for `ranger`, a docs-versus-code checker, a judge/consolidation step, an `entire` CLI dependency, a constitution change for briefs. The 14-class sweep from the Callisto prompt is a good one-off audit script, not a plugin default.

## Part 2: Plugin audit

### A. Defects: fix regardless of taste

| # | Finding | Evidence |
|---|---|---|
| A1 | `muse` exit-gate emits verdict `"escalate"`, but `verdict@1` allows only pass or fail. Muse is the only `verdict@1` producer, and every other gate uses `verdict@3`. **Verified.** | muse exit-gate output section; verdict@1 schema |
| A2 | ARCHITECTURE says each produced artifact "validates before downstream consumption" and ADR 004 says "validated at wiring time". Nothing validates: CI runs `jq .` (parse only), the one validator is hand-rolled in a test, runs on 5 fixtures, and supports no `$ref`, `oneOf`, `anyOf` or `pattern`. No schema library appears anywhere. **Verified.** | ARCHITECTURE.md, ADR 004, `tests/test_cross_harness_artifacts.py` |
| A3 | Prompts and docs that say false things: the vanguard research skill says recon loads search heuristics that do not exist (**verified**); the vanguard README says the synthesizer "resolves contradictions" while the agent is told never to pick a side; `weaver` `capture-need` names the wrong owner for `out_of_scope`; the weaver auditor advertises a connect mode with no logic; the sentinel README promises escalation to a higher-effort model on retry 2 that no agent implements; the navigator README draws a changeset-to-PR edge that does not exist (**verified**: neither the PR agent nor the PR skill mentions changesets). | files named |
| A4 | Constitution contradicts its own ecosystem: it says standard exit gates are sonnet/medium while all five run opus/high (**verified**); it mandates modern CLI tools while `tooling/cli.md` says repository-native commands win; it caps loops at 2 rounds and never mentions the 3-retry gate rule five gate files repeat; best-practices says "all 38" agents and names a remediator that does not exist; there are 44 agents. | constitution; best-practices |
| A5 | `docs/pipeline-walkthrough.md` shows `requirement@1` with fields the schema does not have (`success_conditions`); with `additionalProperties:false` it would not validate. **Verified.** `AGENTS.md` and `CONTRIBUTING.md` give conflicting author formats. | files named |
| A6 | Documented as active but wired nowhere: the two scripts in `shared/hooks` (**verified**: referenced nowhere outside themselves); `shared/scripts/validate-wiring.sh` is listed as a gate in ARCHITECTURE and run by neither the justfile nor CI. | ARCHITECTURE; justfile |
| A7 | Constitution plan-persistence rules (`plan_file_path`, `plan_file_unset`) appear in the navigator skill and no agent (**verified**), though the rule says any agent consuming a plan reads that path. | constitution; navigator skill |
| A8 | `navigator:challenger` and `scribe:auditor` drive retry loops on a binding shape that has no schema. Other inline-JSON agents are fine without one. | schemas lane |

### B. Prune: low risk, measurable

| # | Item | Size or evidence |
|---|---|---|
| B1 | **Descriptions are the largest runtime cost.** Agent descriptions total 26,688 characters across 44 agents (average 607; five exceed 1,000); skill descriptions add about 14,500. Both lists enter every session with the plugins enabled, roughly 10,000 tokens. Many restate inputs, outputs and classification rules the body already has. Cut each to a one- or two-sentence routing description. **Verified counts.** | frontmatter of all agents and skills |
| B2 | Schema files nothing references: `verdict@2`, `finding-report@1`, `implementation-review@1`, `mutation-report@1`, `harness-evaluation@1`, `arch-model@1`, `arch-spec@1` (prose mentions only), `codex-adaptation@1`. **Verified zero references.** `verdict@1` is live (muse) until A1 is fixed. Deleting needs a retired-schema mechanism, because the authoring hook blocks deletes and `dist/codex` copies them. | schemas lane |
| B3 | Output fields with no consumer: vanguard recon `external_keywords`, `existing_implementations`, `scope`; risk-assessor `overall_risk`; scribe verifier `supported` array; arch-auditor `model_updates_suggested` and `last_built_from`; ranger recon `capabilities`, `baseline`, `workspace_state`; about 15 schema fields (for example `spec@1` `judgment_call`, `release-artifact@2` `pr_url` and `migration_guide`, four `harness-evaluation@2` metrics). `reasoning` is required in 13 of 31 schemas and read by nothing. | lanes; schemas lane |
| B4 | Repeated text within a plugin: `scribe:auditor` states its `boundary-round-trip` check in five places; `drift-checker` states three rules two to four times each; ranger exit-gate states "plausible is not a blocker" four times; `challenger` has two check types for the same condition; `smith` exit-gate mirrors seven of eight judgment bullets as output rules. | lanes |
| B5 | Prose that narrates history in runtime prompts: "previously undocumented", "new for this split", an ADR-008 backstory in the planner, a find-and-replace artifact ("vanguard back to the requirement"). | lanes |
| B6 | Hazard references for Go and Python carry nine `rg` regexes each (including `return nil`, `default:`) that match almost every function; Rust and TypeScript use Signal/Confirm/Refute without regexes, as the constitution asks. Each match is judged by one opus adversary call. | hazards |
| B7 | The language-to-file routing table is copied six times; best-practices sections restate constitution rules; README and ARCHITECTURE share byte-identical diagrams (**verified**: 2 identical blocks); the authoring rules are restated in four files. | lanes |
| B8 | Tests and scripts that cannot fail or duplicate another check: substring checks on skill prose in the smith integration test; brand and logo text pins; README-prose pins in the Codex evaluation test; the skills-doc check (regex on README table shape); the reference-size cap (largest file is 95 lines, cap is 120); a dead mermaid wrapper script; byte-equality checked three or four times across the Codex builder and tests. | tooling lanes |
| B9 | Codex build trims: derive the Codex manifest version from `plugin.json` (a fifth manual version edit per bump); replace backup and rollback machinery with a temp-dir swap; drop the nested `dist` marketplace manifest; fold the eight five-line role cards into one README (200 of 240 generated files are copies and 46% of bytes duplicate another file). | Codex lane |
| B10 | Version appears in six places per plugin; adding one agent takes about eight hand edits. A single source in `plugin.json` would remove the sync work and `check-versions.sh`'s reason to exist. | tooling lanes |

### C. Decisions for you: real tradeoffs

| # | Question | Case for / against |
|---|---|---|
| C1 | `muse` is three agents that are near-copies of scribe's drafter, auditor and exit-gate plus a UI-state and accessibility checklist. Fold into scribe as a reference loaded by the same agents? | For: removes ~160 lines of copied text and a plugin. Against: plugin removal touches marketplace, Codex dist and install docs; muse recently gained exploration modes. |
| C2 | `sentinel:exit-gate` runs opus/high but maps a verifier report to a verdict without re-reading evidence (smith's gate re-derives from code). Lower the tier, or make it re-check passes? Its recon, on haiku, fixes the criteria list, so a recon miss silently narrows the gate. | Constitution reserves opus for terminal verdicts. |
| C3 | `scribe:arch-auditor` runs on the fable tier in check mode, which the constitution says to reserve for single bounded tasks, never gates or per-finding loops. Build mode on fable, check mode lower? | Risk: weaker model misses boundary conflicts. |
| C4 | `navigator:planner` writes exact implementation code that `smith:implementer` is told not to copy, and `challenger` polices. Require criteria, signatures and test assertions, with full code only for non-obvious logic? | ADR 009 kept the concreteness on purpose. Weaker implementers lose guardrails. |
| C5 | `navigator:estimator`: an opt-in mode with no pipeline consumer and output that contradicts ADR 009's "clock time has no meaning for an agent". Remove? | Users may invoke "estimate". |
| C6 | `courier:review-preprocessor` re-serializes the caller's inputs and generates only a diff summary; `courier:release-summarizer` is deterministic (filter, max semver, concatenate) on sonnet/medium and puts its only consumer-facing text in the discarded `reasoning` field. Script them? | Release notes field needs a schema version. |
| C7 | The five exit gates repeat the retry-above-3 and pending-checks-means-fail rules. Move the shared mechanics into the `verdict@3` schema description or one reference and keep domain checks per gate? | Low risk; the agents stay. |
| C8 | Add a real schema validator to CI (A2), or soften the claims? | A validator is the one new piece of machinery this audit supports: it makes the claim true and addresses "tests that cannot fail". Cost is a dev dependency. |
| C9 | Whether to build `dist/codex` in CI instead of committing. | Do not, until it is verified that `codex plugin marketplace add` can pin a ref. The root manifest points at `./dist/codex/plugins/...`. |
| C10 | `ranger:adversary` runs a "constitution sweep once per session" while running once per candidate, with no output slot for the result. Remove or make an opt-in step? | Untested behavior. |

### D. Keep: earns its place

- The identical 5-line `<constitution>` block, for prompt-cache sharing (ADR 006).
- Default-fail gates and the "plausible is not evidence" and "absence of counter-evidence is not verified" rules.
- Independent re-derivation of siblings in `smith` and `ranger` exit gates; `ranger` adversary refute-first stance; `boundary-tracer` for T7.
- `implementation-review@2`, `mutation-report@2`, `verdict@3`: cross-field rules that catch false approvals, exercised by fixtures.
- Trust-boundary, lossy-context and uncommitted-is-not-persisted rules; "a named tool alone is not evidence".
- The Rust and TypeScript hazard format, the changeset semver table, the hidden-oracle evaluation split.
- The Codex build tool and its tests, `check-versions.sh`, reference-integrity test, the schema-immutability hook.
- `dist/codex` committed, until C9 is resolved.

## Suggested order

1. A1 to A7 (defects and false text): small, no judgment calls.
2. B1 (descriptions): largest runtime saving; do per plugin.
3. B2 and C8 together: retire dead schemas and add a real validator.
4. Part 1 additions, each paired with a B-item deletion so net text shrinks.
5. B3 to B10, then decide C-items one at a time.

## Open decisions

- Approve A and B as a first batch, split by plugin so each can be reviewed.
- Answer C1 to C10 you care about; the rest can wait.
- Whether to re-run a final read after the first batch lands.
