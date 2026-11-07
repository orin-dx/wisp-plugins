# Review and slop learnings, and a plugin cost audit

Evaluation date: 2026-11-02, updated 2026-11-06. Status: the first change set is implemented on this branch (see Implementation status); the rest is proposal. No plugin version or schema changed.

## Principle

Spend tokens only where they change an outcome. Two costs, kept apart:

- **Runtime cost** is paid in every session that enables the plugins: agent and skill descriptions, agent bodies, loaded references.
- **Authoring cost** is paid by maintainers: the constitution, `CONTRIBUTING.md`, tests, scripts, the Codex build. `shared/constitution.md` is not loaded by agents. They carry only the 5-line embedded block, identical in all 44 agents (verified).

Cuts must not remove the checks that catch real failures. Every item below has file evidence. Items marked **verified** were re-checked against source after the full-read lanes reported.

## Implementation status

Implemented in seven signed commits on `worktree-review-slop-evaluation`, in the order of the work plan. `just check` passes (56 tests).

| Workstream | Commit | What changed |
|---|---|---|
| 0 Baseline and fixtures | `fcfe974c` | Ten replay fixtures from real misses (`tests/fixtures/behavioral/fix-pass-misses.json`) |
| 1 Truth repair | `d24be9e0` | A3 to A7 fixed; A2 softened (claim now says no runtime validator runs); source wiring now runs in `just check` and CI |
| 2 Verification content | `720add75` | D2 and D3 and the Part 1 additions in the three owner references; a test ties each rule to one owner |
| 3 Fix-pass path | `36bfd751` | D1 light `smith` entry (Claude and Codex skills); D8 project invariants defined once in the workspace conventions reference; `ranger` adversary sweep replaced |
| 4 Gates | `50bdcf1b` | A1: `muse` gate on `verdict@3` (nothing references `verdict@1` now); claim-evidence rule in the `smith` and `sentinel` gates; fix-pass criteria in the `smith` gate |
| 5 Hazards | `381c14ea` | D7: script, workflow and template hazard reference, routed from implementation review |
| 6 Prompt weight | `18e52d5d` | Description text 41,217 to 20,100 characters (agents 26,683 to 11,465; skills 14,534 to 8,635), identity fields unchanged; repeated rules and history narration removed; 294 lines deleted against 116 added |
| 7 Guards | this commit | `tests/test_prompt_alignment.py`: identical constitution block in all 44 agents, description length caps, gate tier matches the constitution, no retired verdict version referenced |

### Deliberately not done

- **C7, shared gate mechanics:** skipped. A shared reference would add a load to every gate call for less text than the inline rules cost.
- **B6, Go and Python hazard regexes:** deferred. Removing them changes scanner recall, which needs measuring first.
- **Schema work (A2 validator, A8, B2 retire, B3 unused fields, R3 `reasoning`):** deferred to one coordinated change, since schemas are immutable, the authoring hook blocks deletes, and `dist/codex` copies them.
- **Release versions and CHANGELOG entries:** left for you. Every plugin changed. Suggested: `smith` minor (fix pass), `muse` minor or major (its produced verdict moves from `verdict@1` to `verdict@3`, a consumer-visible contract change), the rest patch.
- **R2 (constitution block cache sharing), R3, C4 (planner exact code):** still to be measured; no change made. The identical-block rule is now at least tested.
- **R4 hooks:** chose to keep the two scripts and correct the docs, not wire or delete them.
- **C10:** superseded by D8 and implemented.
- **D4:** verified, no change needed; the `smith` gate already fails when the mutation gate neither ran nor was reported unavailable.
- **Untouched:** C1, C5, C6, D5, D6, D9, D10, B9, B10.

## Measuring the effect

The test is real work, not a replay harness. Baseline taken 2026-11-06, before this change set is used:

| Measure | Baseline |
|---|---|
| Subagent tokens in Callisto, Caliper and Monokl sessions | plugin agents 44.6M (26%), other subagents 124.2M (74%). One long session on the pre-rename names (`canon`, `lambda`, `vector`) inflates the plugin share. |
| `smith` reviewer, mutator and exit gate runs on fix work | effectively none; `smith:implementer` ran 21 times in one session, `ranger` adversary, scanner and recon in one |
| Entire findings | 256 on 242 changes (111 open, 112 resolved, 33 dismissed); 65 changes have findings, median 3 per change with findings; class mix in Part 1 |

Re-measure after about 20 changes or two weeks of use of the new path (the sample is small and noisy, so read `paired-analysis.py`'s power warning before trusting a difference):

```
python3 tools/transcript-metrics.py agents --match 'Projects-(callisto|caliper|monokl)'
python3 tools/transcript-metrics.py skills --match 'Projects-(callisto|caliper|monokl)'
python3 tools/entire-findings.py pull --project gh/orin-dx --repos caliper callisto monokl --out findings-<date>.json
python3 tools/entire-findings.py summary findings-<before>.json findings-<after>.json
```

What would show it worked: the `smith` reviewer, mutator and gate run on fix work; plugin agents take a larger share of subagent tokens; the weak-test, doc-claim, copied-value, harness and release classes shrink as a share of findings; tokens per fix do not rise sharply. What would show it did not: the controls still never run (then the entry point or the project instructions are the problem), or the class mix is unchanged.

Adoption lever, for each project's `AGENTS.md` (Callisto found its repo instructions did not mention the plugins; using them was a personal memory rule). Replace the placeholder with the project's own CI-equivalent command:

```
## Fixes and review findings

Fix review findings, bugs, and diff-sized changes with the smith fix pass (`smith:implement`), not ad hoc agents.

- State each claim to fix, the invariants that must hold, and the sites to search for the changed symbol.
- Give every fix a regression test that fails on the pre-fix source.
- Verify with the command CI runs, from a clean state: `<ci-equivalent command>`.
- Report each claim with the command that proves it. A check still running is pending.
```

CI-equivalent command per project (from each justfile; confirm before relying on it):

| Project | Command | Parity |
|---|---|---|
| Monokl | `just ci` (lint, test, doc-check, deny, machete, typos, zizmor, changesets, coverage 90) | its justfile says it is everything the CI jobs run; the release path is not rehearsed |
| Callisto | `just ci` | Callisto's own analysis says it is a strict subset of GitHub CI (CI also runs machete, features-boundary, check-api, per-crate coverage, a `--locked` check, MSRV, artifact preflight and two contract scripts); its next step is a `verify` command equal to CI, which should replace this entry |
| Caliper | `just ci` (lint, test, deny, typos, zizmor, doc-check, machete, semver, msrv, coverage 90) | parity with the CI workflow not checked; its analysis proposes a clean-room verify command |

## How this was produced

- **Review and slop learnings:** all Entire trail findings for `orin-dx/caliper`, `orin-dx/callisto` and `orin-dx/monokl`, pulled 2026-11-06 (242 changes; **256 findings**: 111 open, 112 resolved, 33 dismissed). An earlier pull on 2026-11-02 saw only 37; 220 of the 256 were created on 2026-11-03. Each finding was classified from its text and disposition by three read-only agents. Also the Caliper and Monokl sessions' own root-cause write-ups (pasted by the user, not re-verified here) and session learnings from Caliper `ad4b3461` and Callisto `01a16130`, `01a0e02c`, `01a0e02f-*`, `a33915af`, `15c732d1`. Transcripts (126 sessions, 71 MB) were harvested but not read in bulk. Entire has only three Monokl sessions; the sweep and eval session is not checkpointed yet.
- **Plugin audit:** seven read-only lanes each fully read their files with no sampling: weaver, vanguard and scribe; muse, navigator, smith and sentinel; ranger, courier and mason; the constitution and all references; all 31 schemas with every consumer; docs, ADRs, tests and tooling; the Codex harness build. Not fully read: `dist/` (sampled and diffed against sources) and CHANGELOG bodies (headings only).
- Limits: three projects by one author; no lane ran the plugins, so tier suggestions are judgments, not measurements; the finding classification is a model judgment from the finding text alone (see Part 4 caveats).

## Part 1: What review findings show

The first 37-finding sample (13 logic, 7 weak tests, 5 duplication, 4 harness, 4 docs) was an early snapshot. The full 256 agree on the shape and show a larger documentation class. Counts, classified by defect type:

| Class | Count | Share |
|---|---:|---:|
| Logic bug or edge case | 72 | 28% |
| Doc, comment or report states what code does not do | 57 | 22% |
| Duplicated or hand-copied value, helper, list | 29 | 11% |
| Test cannot fail, asserts too little, path untested | 24 | 9% |
| Dead code, unused parameter, scope creep | 18 | 7% |
| Harness or CI differs from the real consumer | 12 | 4% |
| Release or CI configuration | 12 | 4% |
| Swallowed error, silent fallback | 10 | 3% |
| String key, forged shape, declared versus required | 10 | 3% |
| Order, race, shared fixture | 8 | 3% |
| Other (incl. one security) | 4 | 2% |

Entire's reviewer is precise: of 33 dismissals, 17 were already fixed at HEAD or in a follow-up, 7 other, and only 4 were factually wrong and 2 premise errors (6 of 256, 2%).

Proposed additions, one or two lines each in existing reference files, each backed by at least ten findings:

1. Specific assertions: a test for a specified error asserts that error; a stub applies the logic it replaces (verification evidence reference).
2. Single source: reuse an existing helper, string or list before adding one (implementation-review reference).
3. Harness fidelity: measurements use the consumer's configuration and time only the measured work (verification evidence reference).
4. Claims match code: comments state current behavior; heuristics are labeled (comments reference).

Item 4 now has the strongest evidence of the four: 57 findings (22%), 44 of which had no independent control that would have caught them. Both the Caliper and Monokl write-ups independently propose "a claim cites the command that proves it", which is the same rule from the author side.

Held back until Part 4's decisions are made: a judge/consolidation step, an `entire` CLI dependency, a constitution change for briefs. Failure-as-absence hazards for `ranger` now have a second source (10 swallowed-error findings plus the Caliper and Callisto write-ups) but remain a small class. The 14-class sweep from the Callisto prompt is a good one-off audit script, not a plugin default.

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

## Part 3: Fit to current models and guidance

Sources: the prompt-audit and model-migration guidance bundled with the Claude API skill (Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5), and a Claude Code docs lookup (skills, sub-agents, hooks, plugin evals, prompt caching). The docs lookup is secondhand and its page claims were not re-fetched. The guidance's own rule applies to this audit: cut specific outdated instructions, not length; context and the reasons behind constraints are never cruft; "an audit that finds nothing should change nothing".

### What the plugins already get right (measured)

Zero hits for the classic dated patterns across all agents, skills and references: no "think step by step" or scratchpad tags, no "think harder/less", no tool-use discouragement, no "be thorough / do not be lazy", no update suppressors, no anti-formatting rules, no CRITICAL/IMPORTANT caps, no retired model names. Emphasis is light (31 NEVER, 4 MUST, 0 ALWAYS in about 23,000 words). Skill descriptions are within the documented 1,536-character cap (max 824, median 497). 37 of 44 backstories give the reason behind a constraint, which is context and stays. The problem is structure and volume, not shouting, so a rewrite campaign is not justified.

### Confirmed by the guidance

- **B1 descriptions:** trim enumerations of trigger phrases to intent categories; keep when-to-use and when-not-to-use, because routing text may carry calibrated urgency and skills under-trigger. Validate with `/skill-doctor` and `claude plugin eval` instead of guessing.
- **C4 planner exact code:** the guidance says prompts and skills written for earlier models are often too prescriptive for current ones and reduce output quality; A/B with the scaffolding removed. Keep exact scripts only for fragile operations. Run the A/B through `mason:evaluate` or `claude plugin eval` before changing the planner.
- **C1, C6, C5, C7:** the audit's architecture group names two defects directly. An LLM executor for a deterministic plan belongs in code (`release-summarizer`, `review-preprocessor`, `estimator`). Specialist agents with near-duplicate prompts that differ in a filter should be one agent taking the distinction as input (muse versus scribe; the repeated gate mechanics).
- **A2 validator and A6/A7:** instructions nothing enforces carry little signal; enforce in code what code can enforce.
- **Part 1 additions:** do not invent wording. Anthropic publishes tested snippets for exactly these failures, so adopt them in `smith` and the gates: audit each progress claim against a tool result from this session; run a real check that exercises the change before reporting it done (a syntax-only check does not count); do not add features, refactors or abstractions beyond the task. The guidance also reports that separate fresh-context verifiers outperform self-critique, which supports keeping independent gates and verifiers (section D).

### Changed by the guidance

| # | Item | Revised view |
|---|---|---|
| R1 | Tier changes (C2, C3) | Low value. Per-million-token prices: Haiku 5.5 0.10 in / 0.50 out, Sonnet 5.5 2 / 10, Opus 5.5 4 / 20, Fable 5.1 10 / 50. Opus costs 2x Sonnet, so moving a gate down saves little; the levers are fewer calls, Haiku for mechanical work, and Opus instead of Fable for `arch-auditor` check mode (2.5x). The guidance says to measure the most capable model at lower effort before keeping a multi-model cascade, because caches are model-scoped. Do not churn tiers without an eval. Two cheap fixes: use the `fable` alias instead of the pinned `claude-fable-5-1` in the two agents that pin it; consider Haiku recon at medium effort, since a recon miss silently narrows everything downstream. |
| R2 | Byte-identical constitution block | The stated reason is prompt-cache sharing across agents. The block is about 323 tokens, below the 512-token minimum cacheable prefix on current models, and per the docs lookup the cache key includes model, speed and effort and subagents build their own caches (tools also render first and differ per agent). Cross-agent sharing therefore looks unsupported; repeated calls to the same agent cache regardless. Verify with the cache-read ratio in `/usage` before acting. If confirmed, drop the byte-identity invariant, keep the trust-boundary and report-concern rules, and let the other three (trained defaults) go. Needs an ADR 006 amendment. |
| R3 | The `reasoning` scratchpad | New and potentially the largest item. 44 agents tell the model to fill it, 30 show it in their output example, 12 schemas require it, and it is discarded. The audit guidance names a reasoning, thinking or trace field in JSON output as an item to remove: thinking is native (always on in Opus 5.5 and Fable 5.1), output tokens cost five times input, and on Fable 5.1, Opus 5.5 and Sonnet 5.5 instructing reasoning reproduction may trigger a `reasoning_extraction` refusal that fallback does not retry. Our field asks for scratchpad notes, not reproduced thinking, so the refusal risk is unmeasured. Medium confidence. Test on the gates first; if outputs hold, make the field optional in new schema versions and drop the instruction. Needs a constitution change and schema versions. |
| R4 | Hooks (A6) | Claude Code plugins can ship hooks (a hooks file or the manifest, with the plugin-root variable). The two scripts inject one language's hazard file at subagent start (an if/elif chain, so polyglot repos get one). Agents already load references themselves. Default recommendation is delete the scripts and fix the docs, not wire them. |
| R5 | EARS and SHALL density | 191 SHALL and 186 rule lines in `<output>` sections. Contract rules (retry caps, schema pins, ordering that protocols require) should stay exact. For judgment rules, prefer a sentence with its reason; do this opportunistically while editing a plugin, not as a campaign. |
| R6 | Mason overlap | `claude plugin validate` (manifest, paths), `claude plugin eval` (graders, baseline versus no plugin) and `/skill-doctor` (usage, cost per skill) now exist first-party. Check what `mason:evaluate`, its runner and adjudicator, and the manifest scripts add beyond them before maintaining both. The hidden-oracle adjudication may still earn its place. |

Smaller notes: effort changes now preserve the prompt cache on Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1, so per-agent effort needs no consolidation; subagent caches default to a 5-minute lifetime and the docs lookup reports an environment variable for 1 hour, relevant only to pipelines that call gates minutes apart; the skill count is 30, not 33.

## Part 4: Where the failings happened

Corpus: the 256 findings from Part 1, classified by origin (earliest stage that could have prevented the defect), by the independent control that would plausibly have caught it first, and by the cheapest mechanical guard that would stop the class returning. Judged from the finding text and disposition alone, by model; treat shares as indicative.

| | Result |
|---|---|
| Origin | code 65%, author claimed or documented without proof 13%, test authoring 11%, CI or release config 5%, spec 1%, brief 1% |
| Catcher | no control except an adversarial human read 45%; sibling-site search 23%; fail-on-original-bug or mutation 10%; mechanical lint 9%; clean-room run equal to CI 4%; real-producer contract test 4%; language hazard check 3% |
| Guard | a regression test 44%, a lint 13%, a CI matrix or rehearsal 3%, a schema or contract validator 2%, none 36% |

- 139 findings (54%) fall in classes that controls the plugins already define would plausibly catch: sibling search (60), mutation (26), clean-room (11), contract (10), hazards (7), plus lint (25). 163 (64%) have a mechanical guard.
- Findings cluster. 21 changes with five or more findings hold 160 (63%); eight hold 85 (33%). The largest are Caliper's type-parameter scope work (changes 132, 142, 143: 39 findings), where each fix left a sibling site with the same defect, and 4 of 15 findings on change 132 were stale reports already fixed at HEAD.
- Each project has a different signature. Caliper: resolver logic and sibling chains (67 of 189 are logic). Callisto: tests that cannot fail (9 of 35) and release. Monokl: doc claims that contradict code (12 of 32).
- Only 3 findings are high severity: the `.2.28` target suffix that would break both Linux builds, committed pending-snapshot files, and a fake `git` in a test harness that diverged from the real call.

### Agreement with the projects' own root causes

The Caliper, Monokl and Callisto write-ups (Caliper and Monokl pasted; Callisto read from its `ANALYSIS-2026-11` plan; none re-verified) name the same causes independently. Callisto adds: fakes checked against the code and never against the real tool, "our own repo is the only consumer we test", pins and lists with no owner or expiry, and a repo whose own instructions say nothing about verification parity, sibling sweeps or the plugins. The corpus supports most of them:

| Root cause named by the authors | What the 256 findings show |
|---|---|
| Fixes are local, verification is narrow, siblings stay | Sibling search is the single largest independent catcher (23%); the scope-chain changes are the clearest case |
| Green is easy to fake | 24 weak-test findings, 20 of them catchable by a fail-on-original-bug check |
| Plausible claims cascade; summaries of summaries | 57 doc-claim findings (22%); 34 findings across all classes originate in a claim stated without proof |
| Local green, CI red | 24 harness and release findings; the three high-severity items |
| Boundaries are weakly typed | 10 boundary findings, half catchable by a contract test |
| Review sees only diffs; specs outran code; briefs lacked invariants | Not testable here: a diff reviewer cannot see briefs or specs, so spec and brief origins (2%) are undercounted. The corpus neither confirms nor refutes these. |

### What this means for the plugins

1. **The controls exist; the path to them does not.** All three write-ups say they ran general-purpose agents with hand-written briefs and never invoked the reviewer, mutator or exit gate; Callisto adds that using the plugins is a personal memory rule and its repo instructions do not mention them. Verified cause: the `smith` skill consumes only `plan@1` or `spec@1`. A request like "fix these review findings" or "make this change" has no entry, so the spec-and-plan ceremony gets skipped and the controls with it. The mutation gate is also "when available and relevant", so it can be skipped by design. Adding more controls would repeat the pattern; a light entry point addresses it.
2. **Caliper's verification gaps look real.** `evidence.md` mentions CI configuration only as an environment assumption. It says nothing about running exactly what CI runs in a clean state, declared versus required ranges (peer ranges, engines, pins), or treating an intermittent failure as a defect until a cause is shown. Each is one line.
3. **The author-side rule matches the reviewer-side finding.** Both write-ups propose a worker report where each claim names its proving command, says "pending" while checks run, and lists the sites searched for the changed symbol. That is the Part 1 claims rule, from the other direction, and it is the same as Anthropic's tested progress-claim snippet.
4. **Courier format mismatch is reported twice and partly verified.** The shared changesets reference defines grouped Breaking Changes, New Features and Bug Fixes headings, but as the release-note shape; `changeset@2` is structured JSON. Caliper and Callisto both report that their `.changeset/` files are flat markdown and that a mapping step is needed. Neither tried it.
5. **Callisto adds gaps the other two did not name.**
   - **Language coverage:** the hazard packs cover Rust, TypeScript, JavaScript, Python and Go (verified from the hazard files). Shell, workflow YAML, generated templates and `jq`, a large share of Callisto's findings, are a tolerated coverage gap by design, because the constitution says an unsupported target is recorded as a gap. The corpus has 12 release-configuration findings, and the E170 failure that blocked Monokl 0.3.0 came from a generated workflow.
   - **Test doubles:** the plugins ask to name the mocked segment but not to validate the double against the real tool's argument grammar. The corpus agrees: a fake `git` that diverged from the real refspec (the one Callisto high-severity item), and stubs that accept any flag or ignore the filter they stand in for.
   - **Generated output seen by the consumer:** the matrix template was never exercised the way a downstream repo's `actions/checkout` produces it. Caliper and Monokl independently ask for a release rehearsal.
   - **External state that expires:** retired runner labels, floating tool versions. `ranger` correctly carries uncertainty as `plausible`, which never blocks, so a retired label would be softened too.
6. **A seed for project knowledge already exists.** All three projects propose an invariants map (each repo invariant and what enforces it). The `ranger` adversary already reads `CLAUDE.md` and `AGENTS.md` for invariants once per session, and the constitution allows extracting only invariant descriptions from workspace docs under its trust rule. That mechanism could be defined once in the workspace conventions reference and used by the `smith` reviewer too, instead of a new project-specific file type. Earlier I proposed removing that sweep (C10); this changes the recommendation to keep and generalize it.
7. **Monokl's full read of this repo agrees with the audit and adds one real gap.** Independently it found that the plugin repo has its own failure classes (the constitution contradicts its CLI reference, versions drift, a schema cites a missing path, an agent emits a verdict its schema forbids, the docs name a remediator that does not exist), which are items A1, A3 and A4. It says to fix that drift before adding rules, which the suggested order already does. It also reports, and I verified:
   - **Outcome versus baseline has no stage.** Monokl lost to `rg` on its own eval (about 20 of 36 tasks found cleanly against 34 for `rg`, at about 6x the tokens) after a large design effort, and no check compared the product with anything. `requirement@1` `done_when` is an array of free-text strings with no baseline or measure field, and `mason:evaluate` covers plugins only. This is the goal-level failure that review findings cannot show, since reviewers see diffs.
   - **Dismissals do not persist.** `candidate-assessment@1` can mark a candidate `dismissed` with free-text refutation evidence, but `finding-report@2` carries only `confirmed` and `plausible`, so dismissed items are dropped and nothing carries over between runs.
   - **Courier cannot feed Callisto as is.** `changeset@2` has no package, order or format field, and `release-artifact@2` has no notes field (notes sit in the discarded `reasoning`). Same as D6.
   - **Mason has one behavioral fixture and no committed workspace to run it against.** The evaluate skill points at the fixtures directory, which holds a single JSON file.
   - Of its six proposed additions (outcome versus baseline, change completeness, conservation and visibility, claim provenance, regression discrimination with real inputs, release and requirement rehearsal), five map onto controls that exist or onto D2 and D3; only outcome versus baseline is a new stage.
8. **Keep the plugins generic.** The projects propose a swap test (would the line hold for a Go CLI?) and a prescription test (does it order steps where order does not matter?). Both are cheap and fit the constitution's reference rules. Project facts such as the gate command, contract sites and platform floors belong in each repo's own docs.

### Decisions

| # | Proposal | Cost and risk |
|---|---|---|
| D1 | Give `smith` a light entry: accept a finding list or a diff-sized task, with a brief of the claim to fix, invariants that must hold and sites to search; run implementer, reviewer (both sibling modes, fail-on-original-bug test) and exit gate with a clean-room check; no spec or plan. | Medium: a change to the skill's consumes contract and the implementer input. Highest leverage because it makes the existing controls usable on the commonest task. |
| D2 | Add five one-line verification rules to the evidence reference: run what CI runs in a clean state; compare declared requirements with actual use; an intermittent failure is a defect until a cause is shown; validate a test double against the real tool's argument grammar; exercise generated output the way its consumer will. Add a sixth from Monokl: a filter or limit that drops inputs reports how many (conservation), so "could not check" differs from "checked, nothing found". | Small. Backed by 24 harness and release findings, 10 silent-failure findings and all three write-ups. |
| D3 | Add a "claims cite their proving command" rule for implementer and gate reports, using Anthropic's tested wording. | Small. Backed by 57 doc-claim findings. |
| D4 | Treat a skipped mutation or discrimination check as a coverage gap that the gate must carry, not an optional step. The exit gate already fails when the mutator neither ran nor reported unavailable, so this may already hold; confirm before changing. | Small, verify first. |
| D5 | A source-neutral finding record with reason codes (by-design, factually-wrong, already-fixed, duplicate, nit), proposed by the Monokl session. Entire does retain findings on merged changes (151 of 256 sit on 48 merged changes), so the premise that they vanish on merge is not supported. A snapshot script that records dispositions would still make dismissals labelled data. | Small as a script; do not build adapters or a schema until the data justifies them. |
| D6 | Fix courier's changeset output to the consumer's format, or make the format an input. Reported by Caliper and Callisto. | Needs a look at the courier changeset skill. |
| D7 | One hazard reference for shell, CI workflows and generated templates, in the existing Signal/Confirm/Refute shape, covering: errexit disabled by `\|\|`, soft failure in scripts, unpinned or drifting action and tool versions, retired runner labels, a generated file never checked as its consumer receives it. Build its fixtures from the real misses (E170, the fake `git` refspec, the invalid attestation flag, the `.2.28` suffix). | Medium: one new reference file plus loader wiring. Justified because it closes a gap the constitution tolerates, with three projects' misses as fixtures. Apply the swap test first: would each line hold for a Go CLI. |
| D8 | Define the repo-side invariants file once in the workspace conventions reference and let the `smith` recon and reviewer read it under the existing trust rule, as the `ranger` adversary already does. Replaces removing that sweep (C10). | Small to medium. Resolves the three projects' request for an invariants map without a new schema. |
| D9 | Make a product-goal requirement carry a measurable outcome with a named baseline and method, without a new stage: have `weaver:clarifier` ask for it when `done_when` states an outcome ("better than", "faster", "finds more"), keep it as a `done_when` convention, and let the `sentinel` gate treat an outcome with no run against its baseline as `pending_checks`. | Small: one clarifier question and a gate rule. It targets the one failure the findings cannot show: a large build that never beat the thing it replaces. A baseline-comparison stage would be a larger change; do not start there. |
| D10 | Persist dismissals: let `finding-report@2`'s successor carry `dismissed` items with a reason code (by-design, factually-wrong, already-fixed, duplicate, nit) so a rerun does not re-raise them and the labels can be mined. Merges with D5. | Schema bump. Defer until the D5 snapshot script shows dismissal rates worth acting on. |

## Suggested order

1. A1 to A7 (defects and false text): small, no judgment calls.
2. D2 and D3 with the Part 1 additions: small reference edits backed by the full corpus, each paired with a B-item deletion so net text shrinks.
3. D1 (light `smith` entry) and D8 (repo invariants file): decide and design; they are the main structural changes this analysis supports. Then D7 (shell, CI and template hazards) with fixtures from the three projects' real misses.
4. B1 (descriptions), validated with `claude plugin eval` and `/skill-doctor`.
5. B2 with C8: retire dead schemas and add a real validator.
6. Measure before deciding: the cache-read ratio (R2), gate outputs without the `reasoning` field (R3), planner without exact code (C4).
7. B3 to B10, then decide the remaining C-items one at a time.

## Open decisions

- Approve A and B as a first batch, split by plugin so each can be reviewed.
- Answer C1 to C10 you care about; the rest can wait.
- Whether to re-run a final read after the first batch lands.
