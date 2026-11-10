# Wisp Plugins inventory and UI/design-fit evaluation
Repo: /Users/gabe/Projects/wisp-plugins (marketplace v4.4.5). Read-only research; paths relative to repo root.

## 1. What the set is
Ten plugins forming a spec-driven, schema-handoff software lifecycle (README.md, ARCHITECTURE.md). Central thesis: criteria live on disk as typed JSON (shared/schemas/*.json), agents are split by cognitive mode (haiku enumerate / sonnet analyze / opus binding judgment), every artifact is gated by default-fail verdicts. Everything is text/JSON/code-reading; no plugin has a visual, browser, or generative-design mode.

Flow: weaver(requirement@1) -> vanguard(research-report@1) -> scribe(spec@1) | muse(spec@1) -> navigator(plan@1) -> smith(code + implementation-review@2 + verdict@3) -> courier(changeset@2, release-artifact@2). Sentinel and ranger attach as cross-cutting verifiers; mason maintains plugins.

## 2. Per-plugin inventory
- weaver 3.0.3 (plugins/weaver): intake -> clarifier -> auditor/prioritizer. Skills capture-need, clarify-requirement, prioritize-backlog, connect-requirement, audit-backlog. Produces requirement@1 (id, statement, stakeholder, why, done_when[], out_of_scope[], priority). Text-only.
- vanguard 2.0.2: recon -> reader -> synthesizer -> risk-assessor. One skill `research`. requirement@1 -> research-report@1 (findings tagged confirmed/likely/assumed, recommendation + confidence). Maps internal sources and external keywords; this is the only "explore options" stage, but it is evidence-gathering and converges on one falsifiable recommendation, not divergent ideation.
- scribe 3.4.0: drafter, verifier, auditor, exit-gate, drift-checker, arch-auditor, architect. Eight skills (draft-spec, verify-spec, audit-spec, gate-spec, correct-spec, spec-drift, audit-architecture, architect). requirement@1 (+research) -> spec@1; also arch-model@2 / arch-audit@1; turns ranger finding-report@2 / smith implementation-review@2 into structural spec@1.
- muse 1.0.1: drafter (sonnet), auditor (sonnet), exit-gate (opus). One skill `component` (plugins/muse/skills/component/SKILL.md). Consumes requirement@1 or free-text design intent; produces the same spec@1 as scribe plus verdict@1 (note verdict@1, whereas scribe/smith/sentinel/ranger use verdict@3). Drafter/auditor loop capped at 2, exit gate up to 3 retries then escalate.
- navigator 2.3.2: planner, challenger, estimator. spec@1 -> plan@1 (tasks with exact file paths, exact baseline code, tests, verification command, commit message, covers_criteria; every criterion must be covered). Max 2 challenger rounds.
- smith 2.4.5: recon (haiku, workspace-manifest@1, baseline must pass), implementer (one batch -> implementation-result@1 with criteria_evidence), mutator (mutation-report@2), reviewer (implementation-review@2, sibling/defect-family search, can route needs_architecture to scribe:architect), exit-gate (verdict@3). Optional Wisp CLI implementation-context@1.
- sentinel 2.1.2: recon (haiku) -> verifier (sonnet) -> exit-gate (opus) over ANY artifact (requirement, spec, plan, implementation, PR); verified only on positive evidence; 3 retries; verdict@3. Evidence is by reading artifact and source files.
- ranger 3.2.3: recon (live-file trace), scanner, boundary-tracer (T7/T10 only), adversary (refutation-first), exit-gate. Languages: Rust, TS/JS, Python, Go. Hazard taxonomies T1-T10 (shared/references/hazards/*.md). Output finding-report@2.
- courier 3.0.3: commit-analyzer, pr-narrator, review-preprocessor, changeset-analyzer, release-summarizer. Skills commit, pr, changeset, receive-feedback, post-review, release.
- mason 3.2.2: scaffolder, auditor, schema-designer, evaluation-runner, evaluation-adjudicator. Plugin authoring / conformance / behavioral evaluation. Meta; irrelevant to product UI work.

Shared governance: shared/constitution.md (EARS constraints; byte-identical constitution block in every agent), shared/agent-best-practices.md, debugging-laws.md, docs/adr/*.

## 3. (a) Front-end / UI / design-system implementation

### Explicitly covered
- Component spec authoring: plugins/muse/agents/drafter.md. Goal names props + valid domains, variants, every state (default, hover, focus, active, disabled, loading, error, empty), and a11y criteria: role, name, focus order, keyboard operability, live-region/state-announcement. Judgment forces criteria falsifiable from "rendered markup, computed accessibility role/name, focus behavior, emitted events". Invalid prop combinations -> is_error_case: true.
- Muse auditor and exit-gate (plugins/muse/agents/auditor.md, exit-gate.md) fail specs lacking any implied state or a11y criterion; gate explicitly refuses "accessibility details can be finalized during implementation".
- Design-system grounding, single mention: drafter.md says that for api_surface against an existing component family / design-system convention, inspect live source or design-system reference and verify prop names/types (also an EARS rule in <output>). Drafter description lists "design-system tokens" and "mockup description" as optional inputs. This is verification of prop names, not token/theming/visual-spec modelling.
- Muse scope statement (plugins/muse/README.md, plugin.json): "Audits the spec, not the implementation".

### Covered only incidentally (generic machinery that happens to apply to UI code)
- Smith (plugins/smith/**): language-agnostic implement/mutate/review/gate. TypeScript verification reference (shared/references/verification/typescript.md) lists Vitest/Jest/Bun/Node tests, type-check, Stryker, fast-check, bundle/package build, "process or network boundary - integration harness". Nothing on component tests, Testing Library, DOM, jsdom, browser runners.
- shared/constitution.md:202 requires verification at the nearest executable boundary including "render", or a recorded coverage gap; ARCHITECTURE.md:137 repeats it; shared/schemas/field-survival-map@1.json enumerates boundary_type "render". In practice "render" is a label in a taxonomy, with no procedure or tooling behind it. A UI change could legitimately pass by recording "render boundary unexercised" as a coverage gap.
- shared/references/verification/evidence.md: "Environment testing ... runtime version, PATH, build tags, packaging, CI" - no browser/viewport/theme/locale environment.
- Ranger TS hazards (T1-T6, T8, T9; T7/T10 boundary) are runtime-correctness hazards: assertion bypass, floating promises, nullish state, prototype keys, closed-variant fallthrough, intent dropped, failure swallowed. They overlap UI code only generically (e.g. T9 exhaustive variants could cover component variants; T7 could cover props dropped before the DOM).
- shared/references/architecture/typescript.md mentions "UI state" owner for async writes; boundary-values.md gives TS sum-type guidance. Useful for state modelling in components; not UI-specific.
- Navigator plan@1 requires exact implementation code and exact tests per criterion; fine for React/Vue logic, but a plan cannot encode "looks right" because tests must be mechanical.
- scribe:audit-architecture / arch-model@2 module-boundary checks apply to a UI codebase's layering (components vs. data) generically.

### Structurally missing by design
1. No visual verification of any kind. grep across plugins/ and shared/ for playwright, screenshot, storybook, visual regression, chromium, axe, e2e, jsdom, WCAG, contrast, responsive, viewport, CSS, design token returns nothing outside muse's one "design-system tokens" mention. workspace-manifest@1 capability kinds are a closed enum: build, test, type_check, lint, mutation, property, fuzz, race, integration, boundary. There is no e2e / browser / visual / a11y kind, so recon cannot even record that Playwright or Storybook exists; smith would treat it as a generic "test" or ignore it.
2. Spec model is text-only. spec@1 (shared/schemas/spec@1.json) = purpose, scope, non_goals, api_surface[{name, signature, description, error_conditions}], acceptance_criteria[{id, criterion, is_error_case, judgment_call, rationale}], additionalProperties false. No fields for design tokens, layout/breakpoints, visual references (mockup/Figma links), assets, motion, theming, i18n/copy. The only escape hatch is judgment_call:true criteria "requiring human judgment", which Sentinel/exit-gates cannot evaluate. The drafter judgment explicitly rejects "looks disabled" style criteria (semantic-model leakage), so visual intent is pushed OUT of the spec rather than captured.
3. Observable behavior is defined as DOM/ARIA/focus/events. Nothing about computed style, pixel output, spacing, color contrast, responsive behavior, reduced-motion, dark mode, or cross-browser. A muse spec can pass the binding gate with zero criteria about how the component looks.
4. Muse misdirects a11y code scanning. plugins/muse/README.md, SKILL.md, plugin.json, and top-level docs state "see ranger's accessibility hazard taxonomy for code-level scanning". There is no such taxonomy: grep "accessib" in plugins/ranger and shared/references yields nothing; ranger hazards are T1-T10 listed above (introduced with the muse rename commit a859e2f, never implemented). This is a documentation defect, and means no plugin checks implemented a11y at all (no axe, no ARIA lint, no keyboard walk). Treat as the most concrete finding.
5. No design-system awareness beyond the single "verify prop names" rule. No token inventory, no theme/Tailwind/CSS-in-JS capability detection, no reuse-vs-new-component check (scribe's arch-model@2 canonical-abstractions concept could host this but is generic and code-structure oriented).
6. Smith's acceptance loop is test-pass + mutation-survival + sibling review. Mutation testing (Stryker) is meaningless for CSS/markup-only changes; "deliberate fault" fallback is behavioral. UI work with no logic gets weak discrimination evidence. No "run the app and look" step; the built-in `run` skill/Playwright MCP are outside the plugin set.
7. Sentinel verifies by reading artifact + source files; "unverifiable" bucket is where visual criteria would land, and exit-gate separates "coverage gaps" from blockers, so UI work can clear with visual coverage gaps.
8. Spec-drift/gate for UI: scribe:spec-drift checks code vs criteria textually; cannot detect visual drift.

Net: the set supports UI work as "logic + semantics + a11y-spec" very well on paper, and as "pixel/UX/design-system fidelity" not at all. Muse is the only UI-aware plugin and it stops at the spec.

## 4. (b) Design ideation (visual directions, brand, layout, copy, prototypes, critique)

### Explicitly covered
- Essentially nothing. Nearest explicit items:
  - muse drafter accepts "design references (mockup description, existing component family, design-system tokens)" as input (plugins/muse/agents/drafter.md description) - consumes a finished design, does not create one.
  - vanguard (plugins/vanguard/skills/research/SKILL.md) answers "what are the options for Z" / "prior art on Y" - option survey with evidence and a single recommendation; could be pointed at design patterns, but its sources are specs, docs, manifests, codebase, and external keywords; no visual or competitive-UI sourcing.
  - muse auditor is described as "design review" in the README mermaid ("Auditor: design review"), but the checks are spec completeness (states, a11y, scope overlap, ambiguity), not design critique.

### Incidental
- weaver capture-need/clarify-requirement can structure a design brief into requirement@1 (stakeholder, why, done_when), forcing testable done_when. Good for turning a vague design ask into criteria; hostile to exploratory briefs, since the clarifier asks exactly one question and demands testability.
- vanguard risk-assessor surfaces risks of an approach neutrally; applicable to e.g. "risk of adopting design system X".
- shared/references/authoring/diagrams.md ("Orin Visual Standard") and shared/references/authoring/voice.md are internal authoring standards (Mermaid palette, document voice) for this repo's docs, not product design/copy guidance. assets/brand + ADR 010 are the plugin family's own brand. Do not mistake them for a design capability.
- courier pr-narrator/changeset write copy, but only technical release prose under voice.md rules.

### Structurally missing by design
1. No divergent mode. The whole architecture is convergence: default-fail gates, "no TBDs anywhere" (muse/scribe), testable-proposition-only criteria, circuit breakers capping revision at 2 rounds, adversarial reviewers. Unknowns must be pushed into non_goals/reasoning. A spec cannot hold open options, alternates, or a moodboard; the reasoning field is explicitly "never forwarded downstream".
2. No artifact type for a design direction, style tile, brand brief, layout/wireframe, prototype, copy deck, or critique. Schemas list (shared/schemas/) contains requirement, research-report, spec, plan, verdict, review/finding/mutation/changeset/release/arch/eval artifacts; none is a design artifact. Adding one would need mason:design-schema, and the constitution requires schema-first handoffs.
3. No generation agents with a visual output channel: no HTML/Figma/Storybook/prototype producer, no screenshot ingestion or rendering for critique; agents are told to use abstract tool language, but none lists browser/image tools. No visual critique rubric (hierarchy, contrast, rhythm, consistency), no brand voice/copy review beyond repo-internal voice.md.
4. No user-research or taste-eliciting loop; weaver's intake explicitly "without asking clarifying questions", clarifier limited to one question per invocation.
5. Model-tier policy (haiku enumerate, sonnet analyze, opus binding judgment) has no slot for a "generative/exploratory" cognitive mode; constitution requires agents organized by cognitive mode, so ideation would be a new mode requiring a constitution amendment or an extension of how modes are enumerated (shared/constitution.md, ARCHITECTURE.md ~L241).
6. Human-in-the-loop is only escalation after failed retries (muse exit-gate "escalate"), not a design-review checkpoint.

Net: the set has no ideation capability; a design-ideation phase would have to live outside the plugins, with muse/weaver as the downstream funnel that converts a chosen direction into requirement@1 and spec@1.

## 5. Accuracy notes / gotchas
- Muse's cross-reference to a ranger a11y taxonomy is false in the current repo (see 3.4).
- muse emits verdict@1 while the rest of the ecosystem is on verdict@3 (shared/schemas has verdict@1, @2, @3); muse/README says "produced by exit-gate only; verdict@1". Version skew; may matter for sentinel routing.
- Codex harness has a counterpart: harnesses/codex/plugins/muse/skills/component/SKILL.md (Codex is authored separately; AGENTS.md section 4: generated files must not be edited).
- AGENTS.md rule: any change requires cross-harness review, constitution byte-identity, schema-first, `just check`. Adding a UI/design plugin or a spec@2 means mason scaffold + schema design + marketplace.json + Codex source + `just marketplace-sync`.
- Smith README documents its own "Capability Gaps" (shared/README) as precedent for honest gap docs.

## 6. Rigidity vs. exploratory/sketch work (added per user lens)

### Per-plugin: is there a lightweight entry point?
- weaver: capture-need is light (free text -> requirement@1 with no questions; omits unknowns), but done_when must be testable and clarifier/audit-backlog push toward complete requirement@1. Lightest path in the set; still produces a formal artifact.
- vanguard: one fixed pipeline (recon->reader->synthesizer->risk-assessor); README says "One skill, one pipeline - not a menu of modes". Not skippable internally; README allows skipping vanguard entirely (weaver -> scribe directly, plugins/weaver/README.md:117).
- scribe: eight skills; draft-spec is the entry, then verify/audit/audit-architecture/gate-spec before planning. Every path ends at a binding default-fail gate. No "draft only, don't gate" mode except calling draft-spec alone (README-level, not a documented sketch).
- muse: single skill `component`; plugins/muse/skills/component/SKILL.md circuit_breaker: drafter->auditor capped at 2, exit gate up to 3 retries then human. Spec is "persisted to disk only after exit-gate passes".
- navigator: plan@1 requires exact code, tests per criterion, every criterion covered, challenger review (max 2 rounds), no TBDs.
- smith: actually the loosest build entry. Accepts spec@1 with no plan (plugins/smith/README.md:14, skills/implement/SKILL.md io), but still runs recon (baseline must pass; stop on failing baseline - agents/recon.md), mutator, reviewer, exit-gate per batch; "Do not activate for explanation-only requests". No spike/prototype/throwaway mode; no path without a spec or plan.
- sentinel: gate only; explicitly not for "exploratory research ... where no artifact boundary is being crossed" (skills/gate/SKILL.md:24). It is opt-in, so it is skippable by simply not invoking it.
- ranger: has narrower paths (verify one candidate, targeted scan; README L40-46) but is audit, not building.
- courier: commit/pr/changeset individually invokable; post-review needs explicit confirmation. Shipping, not exploring.
- mason: scaffolding/audit of plugins only.

Bottom line: every build-side path assumes a requirement/spec/plan artifact exists or will be created, and ends in an independent verdict. The only flexible edges are (1) invoking an individual skill by itself, (2) not installing/invoking the gates, (3) spec_file_path/plan_file_path absence degrading gracefully (constitution L116, L126, "graceful degradation, not a hard block"). None of these is a designed sketch mode; they are escape hatches by omission.

### Rigidity language (citations)
- shared/constitution.md L104-106: re-submit to exit-gate after fail; producing agent SHALL address only blockers. L112: on exit-gate pass the orchestrator SHALL write spec to docs/specs/<id>.json, commit, set spec_file_path. L154: amended plan SHALL pass through challenger, "amendment is not exempt from adversarial review". L162: review loops capped at 2 rounds. L166: gate re-evaluation scope. L202: verification at nearest executable boundary or recorded gap. L228: strict spec text rules. Model tiers L47-50: terminal binding verdicts on opus/high (cost/latency for every gate).
- Default-fail gates: plugins/muse/agents/exit-gate.md ("default disposition is fail"; "Conditional passing ... is a fail"; escalate after retry_count>3); scribe exit-gate and plugins/sentinel/skills/gate/SKILL.md L50 (3 retries then escalate, "do not loop indefinitely"); sentinel verifier "verified only on positive evidence".
- "No TBDs anywhere" in muse/scribe/navigator skills and agents: unknowns must be moved to non_goals/reasoning, so an unfinished idea cannot exist as a valid artifact.
- Smith: recon "WHEN the baseline fails, THE SYSTEM SHALL stop before implementation"; implementer "no shortcuts"; status spec_contradiction halts remaining work (skills/implement/SKILL.md recovery); mutator + reviewer mandatory before exit-gate ("only approved reviews reach exit-gate"). ADR 008 (docs/adr/008-drop-test-first-ordering.md) removed test-first ORDER but not the requirement that tests discriminate via mutation or deliberate fault; so "tests-first" is not literally mandated, "tests proven" is.
- AGENTS.md/CONTRIBUTING: schema-first handoffs, additionalProperties:false, so a malformed output "halts the pipeline" (README Design Principles).

### What is NOT forced
- No plugin hooks or enforcement mechanism makes gates mandatory at runtime; skills trigger on user phrasing. A user can simply not call muse/scribe/navigator/sentinel and just code. The rigidity is in what the plugins do once invoked, plus the implied lifecycle (README: "one direction, no side-taps"), not in blocking ordinary coding.

### What a "sketch mode" would need
1. A declared mode on artifacts (e.g. status: sketch|spec, or a sketch-note@1 / idea@1 schema) that permits TBDs, open questions, alternates, and is never gated; spec@1 requires non_goals>=1 and acceptance_criteria>=1 so it cannot carry a sketch.
2. A smith "spike" skill: skip plan/spec/mutator/reviewer/exit-gate; baseline failure downgraded to warning; output = run instructions + what was and was NOT verified (reuse the existing coverage-gap vocabulary); no commit by default (already default, commit_authorized).
3. Visual feedback tooling in capability enum (browser/screenshot/dev-server kind) so the loop is "change, render, look"; workspace-manifest@1 capability kind enum is closed today.
4. A divergent/generative cognitive mode (haiku/sonnet, no adversary) in the constitution tier model, producing N alternatives, plus a cheap "pick/promote" step that converts a chosen sketch into weaver capture-need -> muse/scribe (promotion path), with sentinel gate applied only at promotion.
5. Lighter validation of tools/ideas: a "does it work" smoke-check recipe (run tool, capture output) recorded as evidence without criteria, i.e. verdict@3 "scoped pass" semantics already allow narrow scope; a sketch verdict could reuse it with scope: "smoke only".
6. Constitution amendment: circuit-breaker/default-fail rules (L104-166) scoped to artifacts with status != sketch; mason scaffold + audit conformance, Codex counterpart skills, marketplace.json registration.
