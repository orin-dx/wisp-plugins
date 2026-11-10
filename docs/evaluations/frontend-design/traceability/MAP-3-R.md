# MAP-3-R: traceability of R1-R4 findings to WP-xx

Tags: [P] primary/fetched, [S] secondary/snippet, [U] unverified, [I] inference/lesson (author's or mine). Where a source file gave its own tag it is kept; elsewhere tags are assigned from the file's stated confidence. "DISPOSITION" = evidence-based decision not to build, with reason. WP-3xx are new (see end).

## R1 (design-md-uspec)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| R1-01 | DESIGN.md introduced by Google Labs with Stitch March 2026 relaunch; draft spec open-sourced April 2026, Apache-2.0, alpha (github.com/google-labs-code/design.md) | S | WP-31, WP-313 | Alpha status = re-verify before pinning; record as-of date |
| R1-02 | Format = Markdown + YAML front matter: version, name, description, tokens (colors, typography, rounded, spacing, components) | S | WP-31 | Compat is the plan; field list must be verified against repo (WP-90) |
| R1-03 | `{path.to.token}` reference syntax; CSS colors (hex/oklch), dimensions | S | WP-30, WP-31 | Same syntax adopted in spec@2 token refs |
| R1-04 | Fixed body section order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts; prose = rationale | S | WP-31 | Section-order conformance not stated in WP-31; WP-301 |
| R1-05 | CLI `npx @google/design.md lint, diff, export` | S | WP-31 | WP-31 says "optional CLI"; `diff` subcommand use for drift not mentioned; WP-73/301 |
| R1-06 | Export targets: json-tailwind, css-tailwind, dtcg | S | WP-31 | Export-to-DTCG interchange not planned: WP-301 |
| R1-07 | 11 lint rules: broken refs, missing primary, WCAG AA contrast, orphan tokens, section order, unknown keys (only 6 named in source) | S | WP-31, WP-42 | Full 11 not enumerated; verify via WP-90 |
| R1-08 | Consumption = file in repo root; Claude Code/Cursor/Gemini CLI/Antigravity just read it, no special protocol | S | WP-71, WP-31 | Router pointer in AGENTS.md handles it |
| R1-09 | Unverified: first-party per-agent integration docs for DESIGN.md | U | WP-90 | Already listed in WP-90 |
| R1-10 | VoltAgent/awesome-design-md: MIT, 84 brands, community 9-section variant (adds Responsive, Agent Prompt Guide, component states); ships preview.html catalogs | S | WP-31, WP-302 | Use as format exemplars only; preview.html catalog idea feeds WP-12 |
| R1-11 | Awesome-design-md values scraped from public CSS, so inferred not authoritative | S | WP-302 | UNMAPPED before; WP-302 provenance tag (inferred vs authoritative) plus license/brand-IP caution |
| R1-12 | Critique: "openness is the beginning of interoperability, not proof"; format still early | S | WP-31, WP-313 | Keep Wisp intent files DESIGN.md-compatible, not DESIGN.md-dependent |
| R1-13 | Uber uSpec: blog uber.com/.../automate-design-specs, docs.uspec.design, repo redongreen/uSpec | S | WP-90 | Primary read still pending |
| R1-14 | uSpec repo is NOT an Uber-org repo; license NOT verified | U | WP-90, WP-302 | Do not vendor or copy text until license checked |
| R1-15 | uSpec direction Figma -> spec (reverse of DESIGN.md) | S | WP-35, WP-32 | Informs design-source adapter direction |
| R1-16 | uSpec input: Figma component link or "uSpec Extract" plugin producing _base.json, plus optional human context (states, platform behavior) | S | WP-35, WP-32 | Facts file ~ _base.json analogue |
| R1-17 | uSpec agents: Cursor (blog); Cursor/Claude Code/Codex (docs) | S | WP-70 | Blog vs docs differ (see Contradictions) |
| R1-18 | uSpec layer 1: skills as instruction files with platform a11y reference tables (VoiceOver/TalkBack/ARIA) so agent selects documented APIs | S | WP-33 | Covered; "never from memory" rule |
| R1-19 | uSpec layer 2: Figma Console MCP (Southleft, OSS, local WebSocket) crawls component tree, variants, variables, tokens | S | WP-35, WP-303 | Console MCP vs official MCP distinction recorded in WP-303; local WebSocket = untrusted-input surface WP-317 |
| R1-20 | uSpec layer 3: LLM only for semantic judgment (a11y semantics, token mapping, slot composition) | S | WP-32, WP-64 | Deterministic-first principle; WP-32 |
| R1-21 | uSpec layer 4: programmatic rendering into Figma from library templates (anatomy markers, tables) | S | WP-34 (partial) | Write-to-Figma DISPOSITION: not adopted (R2 says write beta/pricing unstable); WP-34 renders in repo/HTML instead |
| R1-22 | uSpec outputs: anatomy, API, properties, color annotation (token per state), structure (dimensions/spacing/density), screen reader (3 platforms), motion | S | WP-30, WP-33, WP-316 | Per-state token annotation -> spec@2; motion -> WP-316 |
| R1-23 | uSpec motion section derived from After Effects | S | WP-316 | DISPOSITION for AE: not adopted (tool-specific); motion spec itself WP-316 |
| R1-24 | "Component.MD": canonical schema-valid JSON contract + concise Markdown guide, rendered back to Figma by create-* skills | S | WP-34 | Dual JSON+readable format matches WP-34 |
| R1-25 | uSpec stack: 7 implementations (UIKit, SwiftUI, Android XML/Compose, React, Go, SDUI) | S | WP-33 | DISPOSITION: native mobile not targeted by this evaluation; keep platform API tables extensible |
| R1-26 | uSpec roadmap: drift detection, code-to-spec | S | WP-73 | Confirms drift is open industry problem |
| R1-27 | uSpec local-only processing | S | WP-317 | Privacy posture noted; no action beyond trust handling |
| R1-28 | Key lesson: visual intent stays in source of truth; text contract derived by deterministic extraction, LLM for semantics only | I | WP-32, WP-30 | Core design principle |
| R1-29 | Figma MCP "design system rules" skill generates CLAUDE.md / AGENTS.md / .cursor/rules/figma-design-system.mdc | P/S | WP-35, WP-71 | Rules-file generator covered; per-harness paths list |
| R1-30 | Rules files are lightweight prose; visual intent fetched from Figma at implement time | S | WP-35 | Matches metadata-first |
| R1-31 | W3C DTCG first stable format 2025.10 (Oct 28 2025): JSON, themes, Display P3/Oklch, aliases | S | WP-301 | Token interchange format choice not in any WP: WP-301 |
| R1-32 | DTCG is rigid and machine-checkable but atomic only; no composition or intent | S | WP-31 | Justifies prose intent layer alongside tokens |
| R1-33 | Storybook MCP tools: docs-list, docs-show, get-storybook-story-instructions, test-run; component manifests (props, stories, JSDoc, tests) | S | WP-35, WP-74, WP-46 | Tool names differ from R4 (`run-story-tests`) -> Contradictions |
| R1-34 | Stories = executable examples (visual intent as rendered states) | I | WP-30, WP-46 | Story id as visual reference in spec@2 |
| R1-35 | Storybook MCP visual regression exposure unverified | U | WP-90 | Verify against docs |
| R1-36 | Spec Kit (GitHub, MIT, ~142k stars): constitution/specify/plan/tasks; also bug-fix and idea-assessment entry points; text-first, no visual model | S | WP-18, WP-310 | Entry-point variety supports mode router; star count perishable |
| R1-37 | Kiro: requirements/design/tasks; design agent claims browser-verified UI loop (vendor source) | U | WP-90, WP-41 | Vendor claim; verify before citing |
| R1-38 | OpenSpec: delta-based change specs, ~250 vs ~800 lines per change (Augment roundup, secondary) | S | WP-14, WP-310 | Number unverified; delta approach in WP-14 |
| R1-39 | Common complaint: specs drift and do not self-update | S | WP-73 | Drift extension |
| R1-40 | dsh-ui-spec plugin: deterministic geometry/palette measurement plus optional vision model (low-confidence source) | S | WP-32 | Measured-geometry facts file |
| R1-41 | Lesson 1: split lightweight human-authored design-intent file from falsifiable spec@1; intent = prose and reference, not testable | I | WP-31, WP-30 | Core |
| R1-42 | Lesson 2: criteria reference tokens/intent by name and visual reference (Figma node, story id, screenshot path); visual evidence is attachment/oracle not proposition | I | WP-30, WP-41 | Core |
| R1-43 | Lesson 3: exploratory mode = DESIGN.md + references, no gate; promote to spec only for behavior/a11y once stable | I | WP-10, WP-11, WP-14 | Core |
| R1-44 | Lesson 3b: deterministic extraction should feed the LLM, not the reverse | I | WP-32 | Core |
| R1-45 | Lesson 4: token lint (contrast, broken refs) cheap and deterministic | I | WP-42, WP-31 | Covered |
| R1-46 | Lesson 4b: screenshot diff for visual claims, flagged as coverage gap when no tooling | I | WP-40, WP-41 | Covered |
| R1-47 | Lesson 5: both Uber and OpenSpec critics name drift unsolved; extend spec-drift to intent files | I | WP-73 | Covered |
| R1-48 | Lesson 6: treat scraped/community DESIGN.md as inferred | I | WP-302 | New WP |
| R1-49 | Unverified: uSpec license/ownership; DESIGN.md agent docs; Storybook visual exposure; Kiro UI claims; several facts from LLM-summarised fetches | U | WP-90 | Add each as explicit WP-90 checklist item |
| R1-50 | Third-party design-file / DESIGN.md / MCP output may carry injected instructions (not stated in source; implied by consuming scraped/community files) | I | WP-317 | UNMAPPED before; new WP-317 |

## R2 (figma)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| R2-01 | Official Figma MCP read tools: get_design_context (React+Tailwind default, customizable), get_metadata (sparse XML), get_screenshot, get_variable_defs, download_assets (remote only), get_motion_context, get_figjam | P | WP-35, WP-303 | Tool inventory reference doc WP-303 (perishable) |
| R2-02 | Write tools: use_figma (skills figma-use, -figjam, -slides, figma-spec), generate_figma_design (remote), create_new_file, upload_assets, generate_diagram, html_to_figma, generate_image, send_code_to_figma | P | WP-303 | DISPOSITION: write-to-canvas not adopted (beta, pricing changing, nondeterministic) |
| R2-03 | Design-system/Code Connect tools: get_libraries, search_design_system (remote), get_code_connect_map, add_code_connect_map, get_code_connect_suggestions, get_context_for_code_connect, send_code_connect_mappings | P | WP-35, WP-303 | Wisp analogue = reuse check (WP-35) |
| R2-04 | Also generative plugins, shaders, Weave tools; MCP prompt create_design_system_rules | P | WP-35 | Rules generator |
| R2-05 | Remote https://mcp.figma.com/mcp (recommended) vs desktop http://127.0.0.1:3845/mcp (org/enterprise) | P | WP-303 | Capability-detect both endpoints |
| R2-06 | get_variable_defs availability: search summary says desktop-only, official table says not remote-only | U | WP-90 | Conflict flagged; verify in table before relying |
| R2-07 | Guide: rules files are "onboarding notes" | P | WP-35, WP-71 | Short-router stance consistent |
| R2-08 | Guide: structure Figma with components, variables, semantic names, Auto Layout, annotations | P | WP-35 | Design-source readiness checklist; WP-303 |
| R2-09 | Guide: break large selections up | P | WP-303 | Scan-first rule |
| R2-10 | Limits: Starter plan ~6 calls/month; paid seats per-minute REST Tier 1 limits | P | WP-303 | Budget awareness; optional-adapter justification |
| R2-11 | Failure causes: poor file structure, vague prompts, oversized selections, not triggering the right tool | P | WP-303 | |
| R2-12 | Write to canvas: use_figma builds with real components/variables/auto layout; 9 example skills (/figma-generate-library, /apply-design-system) | P | WP-303 | Not adopted (see R2-02) |
| R2-13 | Write-to-canvas free in beta, later usage-based; nondeterministic; roadmap images/custom fonts | P | WP-35, WP-303 | Basis for "never depend" |
| R2-14 | Code to canvas: generate_figma_design captures running browser UI as FLAT layers, no library connection | P | WP-303 | Lossy; do not use as design-system artifact |
| R2-15 | Code to canvas auto-binds variables if target has library; paid plans (Starter+), edit access | P | WP-303 | |
| R2-16 | Code Connect: without it agent fabricates components (Coinbase stepper from progress bars) | P | WP-35, WP-312 | Reuse-before-create inventory is Wisp's CC analogue |
| R2-17 | Code Connect median: quality +1 (2->3 on 1-4 Likert), tokens -29.5%, duration -19.6%; scales with coverage | P | WP-35, WP-03 | Vendor-sourced; use as hypothesis for WP-60/WP-03 measurement, not as claim |
| R2-18 | Search snippet quoted different Coinbase numbers 11.5%/22.3%/22.5% | U | WP-90 | Contradiction with R2-17 |
| R2-19 | Code Connect needs ongoing manual maintenance (ByteByteGo) | S | WP-72, WP-73 | Maintenance cost motivates drift check |
| R2-20 | Code Connect UI beta/GA mapping via GitHub; GA date unverified | U | WP-90 | |
| R2-21 | Figma Make: prompt-to-app (React+TS+Tailwind+Vite), zip export, GitHub push, open PR (secondary, partly marketing) | S | WP-313 | Landscape record only; DISPOSITION: no integration, depth unverified |
| R2-22 | Make depth unverified | U | WP-90 | |
| R2-23 | Token pipeline: Figma variables -> DTCG JSON -> Style Dictionary -> CSS | S | WP-301 | Interchange/pipeline note |
| R2-24 | Tokens Studio bidirectional git sync | S | WP-301 | Note only |
| R2-25 | Token pipeline details unverified | U | WP-90 | |
| R2-26 | LogRocket: screenshots alone drift | S | WP-35, WP-307 | Tension with R4 screenshot loops (Contradictions) |
| R2-27 | LogRocket: messy layers hurt output | S | WP-35, WP-303 | Source readiness |
| R2-28 | LogRocket: without CC agent regenerates components | S | WP-312 | |
| R2-29 | LogRocket: output needed manual import/responsive fixes | S | WP-19, WP-42 | Responsive probes |
| R2-30 | LogRocket: exported token JSON helped | S | WP-301, WP-32 | Token facts file |
| R2-31 | ByteByteGo: 25k default MCP response cap | S | WP-303 | Verify number (WP-90) |
| R2-32 | ByteByteGo: scan first (get_metadata) then zoom into node | S | WP-35, WP-303 | In WP-35 |
| R2-33 | ByteByteGo: each handoff is lossy (logic/state lost both directions) | S | WP-30, WP-19 | Supports spec for behavior, visual by reference |
| R2-34 | ByteByteGo: capture walks DOM computed styles | S | WP-47 | Computed-style query layer |
| R2-35 | ByteByteGo: agent tools vary | S | WP-70, WP-303 | Capability detection |
| R2-36 | hipsquare: Figma MCP + Playwright screenshot loop; ~50% time reduction on component sets (self-reported, small) | S | WP-03, WP-41 | Hypothesis only; do not cite as evidence |
| R2-37 | Design Systems Collective: token tax of roundtripping (403; snippet only) | U | WP-90 | Read when accessible |
| R2-38 | Code-first loop: implement -> screenshot -> diff list -> fix (Medium x2, mowgli.ai; snippets) | S | WP-41, WP-17 | Matches R4 loop |
| R2-39 | Code-first Medium/mowgli sources not read | U | WP-90 | |
| R2-40 | Community skills: figma-implement-design, figma-use, southleft/figma-console-mcp-skills, tempad-dev figma-design-to-code | S | WP-35, WP-313 | Reference/exemplars; license unchecked (WP-302) |
| R2-41 | Inference: design reference as optional typed artifact with tokens/components/states | I | WP-35 | |
| R2-42 | Inference: visual evidence (screenshot + a11y snapshot) as generic oracle, not Figma-specific | I | WP-41 | |
| R2-43 | Inference: token/component mapping check (tokens used vs hardcoded; component reuse = CC analogue) | I | WP-42, WP-35, WP-312 | |
| R2-44 | Inference: drift check for visual | I | WP-73 | Visual-drift specifics (screenshot baseline age) not stated in WP-73; add |
| R2-45 | Inference: rules-file generation | I | WP-35, WP-71 | |
| R2-46 | design-source@1 kind: figma/screenshot/html/description/none normalized to {tokens, components, states, reference_images} | I | WP-35 | Needs schema work per AGENTS.md schema-first |
| R2-47 | Figma adapter uses MCP if present; else browser screenshot loop against spec criteria; capability-detect, never require | I | WP-35, WP-40 | |
| R2-48 | Keep context cost low: metadata-first, per-node fetch | I | WP-35, WP-66 | |
| R2-49 | Treat Figma output as reference not truth (over-literal, absolute layout) | I | WP-35, WP-303 | Normalization guidance in WP-303 |
| R2-50 | Do not depend on write-to-canvas (beta, pricing changing) | I | WP-35 | DISPOSITION recorded |
| R2-51 | Figma "agent tools" vs Make vs MCP skills proliferate quickly; claims perishable | I | WP-313 | As-of dating |

## R3 (ai-design-tools)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| R3-01 | Overall confidence medium: web-search summaries plus two fetches; vendor/blog reviews | U | WP-90, WP-313 | |
| R3-02 | Tempo, Relume, Uizard, Bolt variant behavior unverified beyond one-liners | U | WP-90 | DISPOSITION: not relied on |
| R3-03 | Claude Design options via chat ("show me 2-3 alternative layouts"); first generation is a starting point (support.claude.com/.../14604416) | P/S | WP-11 | Default ~3 options |
| R3-04 | Claude Design steering: chat for structure, inline canvas comments, direct canvas edit, sliders | S | WP-315 | Annotation intake UNMAPPED before; WP-315 |
| R3-05 | Claude Design ingests design system from GitHub repo, design files, uploads, or local codebase; each becomes an artifact reusable in Claude Code | S | WP-32, WP-31 | Ingest-repo = ground-truth extraction |
| R3-06 | Claude Design self-checks output against the system | S | WP-17, WP-42 | Token/system conformance check |
| R3-07 | Settings > Design Systems "Migrate team design systems" action | S | WP-313 | Landscape note only |
| R3-08 | Export formats .zip, PDF, PPTX, HTML, Canva; send-to v0, Lovable, Replit, Netlify, Miro | S | WP-304 | DISPOSITION: export breadth not needed; handoff bundle content is |
| R3-09 | "Hand off to Claude Code": bundle of design files, chat, README with paste-able prompt | S | WP-304, WP-14 | Bundle format |
| R3-10 | Third-party says bundle holds component structure spec, tokens, layout hierarchy, assets (claudefa.st); not first-party | U | WP-90 | Verify against claude.com/product/design |
| R3-11 | Claude Design explore-then-harden: no version history "yet"; workaround "save what we have and try a completely different approach" | S | WP-11, WP-13 | Option files replace missing history |
| R3-12 | Failure: inline comments sometimes vanish | S | WP-315 | Persist feedback in files |
| R3-13 | Failure: multi-person editing unreliable | S | WP-315 | DISPOSITION: single-author sketch; multi-user out of scope |
| R3-14 | Failure: PCWorld reportedly used 80% of a Pro weekly quota on three variations | S | WP-305, WP-11 | Cost cap/telemetry; number unverified |
| R3-15 | Failure: outputs drift by revision 4-5; fix = fresh anchoring prompt, not stacked corrections | S | WP-11, WP-306 | WP-11 re-derives anchor each round; trigger/threshold missing: WP-306 |
| R3-16 | Failure: design-system copies drift from real system; some advise pasting tokens/specs into prompt | S | WP-73, WP-32 | Read tokens live, not a copy |
| R3-17 | Failure: output "safe/template-y" (the-designengineer.com) | S | WP-16 | Anti-slop |
| R3-18 | Failure: annotations only visible by hovering | S | WP-315 | UI-specific; DISPOSITION: not applicable to file-based feedback |
| R3-19 | Stitch: "Ideate" for exploration and "Flash" for fast generation; both generate multiple alternatives | S | WP-11 | Two speed modes: quick vs thorough sketch? note |
| R3-20 | Stitch Mar 2026: infinite canvas mixing images, code, UI | S | WP-12 | Option board |
| R3-21 | Stitch design agent remembers project history | S | WP-13 | Memory = decision log analogue |
| R3-22 | Stitch voice and instant prototypes (auto-generated missing screens) | S | WP-313 | DISPOSITION: voice not relevant; auto-generated screens risk premature fidelity |
| R3-23 | Stitch MCP server for Claude Code and Cursor | S | WP-35, WP-313 | Possible design-source kind; unverified |
| R3-24 | Stitch handoff: paste into Figma as layered Auto Layout; HTML/CSS/Tailwind export | S | WP-35 | |
| R3-25 | Stitch framework export (Vue, Angular, Flutter, SwiftUI) claimed by one source only | U | WP-90 | |
| R3-26 | Positioning: ideate in Stitch, finish in Figma, build in code | S | WP-18 | Staged-fidelity model supports mode router |
| R3-27 | v0 Design Mode: visual edit panel; Design Systems 2.0 uses shadcn registry to pass tokens/components | S | WP-12, WP-74 | Registry as design-system lookup |
| R3-28 | v0 output for same prompt shifts per imported system -> brand/theme comparison feasible | S | WP-12 | |
| R3-29 | v0 since Mar 2026 infers design system automatically; Design Mode instability reports | S | WP-313 | |
| R3-30 | v0 output is React code, handoff is code; variant/branching UX not verified | U | WP-90 | |
| R3-31 | Figma Make kits combine React package/Figma library with guidelines so prototypes use production components | S | WP-32, WP-31 | |
| R3-32 | Figma agent claims "explore multiple directions" with real components/tokens (marketing) | U | WP-16 | |
| R3-33 | Make forum failures: changes confirmed but not applied, instructions ignored, stuck builds | S | WP-13, WP-19 | "Recorded but not applied" detection in WP-13 |
| R3-34 | Users request branching/version control for Make | S | WP-11, WP-13 | Validates option-ID design |
| R3-35 | Magic Patterns: infinite canvas, duplicate component and prompt for parallel variations (e.g. four headers side by side) using own tokens/components | S | WP-12, WP-16 | Closest to option board |
| R3-36 | Subframe: canvas plus coding agent; layers map to HTML/React; components with props/slots/variants sync to codebase | S | WP-313 | Variant generation unverified; no action |
| R3-37 | Lovable Visual Edits and Bolt Visual Edits (Bolt stacks changes, batches to model) | S | WP-315 | Batched feedback pattern |
| R3-38 | Lovable/Bolt are full-app builders, not divergent-exploration tools | S | WP-313 | DISPOSITION: not exploration references |
| R3-39 | Builder.io Visual Copilot/Fusion maps Figma to code using your components; modes visual/interactive/code; hardening focus | S | WP-35, WP-312 | |
| R3-40 | Uizard (acquired by Miro 2024): sketch-to-wireframe scanner, Autodesigner | S | WP-314 | Wireframe option type |
| R3-41 | Relume recommended for marketing sites, sitemap/wireframes | U | WP-314 | |
| R3-42 | Tempo: nothing found | U | WP-313 | DISPOSITION: no evidence, no action |
| R3-43 | Pattern 1: parallel variants (duplicate or ask for N) | S | WP-11 | |
| R3-44 | Pattern 2: option board on infinite canvas | S | WP-12 | |
| R3-45 | Pattern 3: annotate-and-iterate with chat fallback | S | WP-315 | |
| R3-46 | Pattern 4: direct manipulation/sliders for fine tuning | S | WP-16 (taste dials) | Sliders ~ taste dials; direct manipulation DISPOSITION: needs GUI, not feasible in plugin |
| R3-47 | Pattern 5: design-system grounding via registry, kit, ingested repo | S | WP-31, WP-32, WP-74 | |
| R3-48 | Pattern 6: branching history weak/absent; Claude no history; Stitch memory | S | WP-13 | |
| R3-49 | Decision logs not a feature anywhere found; chat transcript is implicit log, bundled into Claude Code handoff | S | WP-13, WP-304 | Differentiator; also includes transcript in bundle (privacy/size note) |
| R3-50 | Pattern 7: handoff = export bundle, code, or MCP | S | WP-304, WP-14 | |
| R3-51 | Failure: variants burn quota fast | S | WP-305 | |
| R3-52 | Failure: drift over iterations; re-anchor | S | WP-306 | |
| R3-53 | Failure: lost/invisible comments | S | WP-315 | |
| R3-54 | Failure: no history so cannot return to earlier option | S | WP-11, WP-13 | |
| R3-55 | Failure: design-system copy staleness | S | WP-73 | |
| R3-56 | Failure: generic safe aesthetics; options converge instead of diverging | S | WP-16, WP-306 | Divergence check missing in WP-16 |
| R3-57 | Failure: instructions ignored or unapplied | S | WP-13, WP-50 | |
| R3-58 | Failure: premature fidelity; production-looking code blurs sketch and spec | S | WP-11 | Low-fidelity marker |
| R3-59 | Lesson: options as first-class files with stable ID `sketch/<topic>/opt-A` | I | WP-11 | |
| R3-60 | Lesson: render option x brand/theme matrix from tokens | I | WP-12 | |
| R3-61 | Lesson: allow TBDs, no gates; status open/parked/chosen/rejected with one-line reason = decision log | I | WP-11, WP-13 | |
| R3-62 | Lesson: re-derive from anchor brief each round; keep brief in sketch file | I | WP-11 | |
| R3-63 | Lesson: cap default options ~3 for cost | I | WP-11, WP-305 | Conflict with WP-16 "~4 directions" (see Contradictions) |
| R3-64 | Lesson: promote path chosen option -> muse spec, TBDs resolved or moved to non_goals, behaviors to testable criteria | I | WP-14 | |
| R3-65 | Lesson: sketch carries `decision_ref` matching arch-model/ADR conventions | I | WP-14, WP-13 | |
| R3-66 | Lesson: handoff bundle = chosen option + tokens + decision log together | I | WP-304 | |
| R3-67 | Lesson: keep sketches visibly low-fidelity or watermarked | I | WP-11 | |

## R4 (verification-hardening)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| R4-01 | Anthropic: "Give Claude a way to verify its work"; "looks done" is the only signal without a runnable check | P | WP-40, WP-41 | Core justification |
| R4-02 | UI example: paste design, screenshot result, compare, list differences, fix | P | WP-17, WP-41 | |
| R4-03 | Wants evidence (screenshot, command output) not assertion | P | WP-41, WP-50 | |
| R4-04 | Stop hook as deterministic gate | P | WP-308 | UNMAPPED before; WP-308 |
| R4-05 | Fresh-context verification subagent: the agent doing the work is not the one grading | P | WP-17, WP-55 | Already Wisp's shape (R4 item 9.8) |
| R4-06 | Reviewers prompted for gaps over-report; restrict to correctness/stated requirements | P | WP-50 | Tension with WP-50 "report all then filter" (Contradictions) |
| R4-07 | Failure pattern "trust-then-verify gap... if you can't verify it, don't ship" | P | WP-40 | |
| R4-08 | Plan mode adds overhead; "if you could describe the diff in one sentence, skip the plan" | P | WP-309 | UNMAPPED before; fast path |
| R4-09 | Sometimes skip planning because task is exploratory | P | WP-10, WP-18 | |
| R4-10 | Interview -> SPEC.md -> fresh session to execute | P | WP-66, WP-71 | Consistent with fresh-context; no new item |
| R4-11 | Best specs self-contained, state out of scope, end with end-to-end verification step | P | WP-30, WP-34 | spec@2 should require final E2E verification criterion |
| R4-12 | Playwright MCP: accessibility snapshot cheaper than screenshots (~1/4 tokens claimed); hybrid | S | WP-307 | UNMAPPED before; modality policy; token claim verify |
| R4-13 | Screenshot catches blank regions, CSS collisions, narrow-viewport breaks, contrast, overflow, wrong data bound | S | WP-41, WP-17 | |
| R4-14 | GitHub Copilot coding agent has Playwright MCP preconfigured | S | WP-70 | Landscape fact; no action |
| R4-15 | Chrome DevTools for agents: screenshots, console, lighthouse_audit (a11y/SEO/best-practices, mobile/desktop, navigation/snapshot) vs localhost or file:// | S | WP-41, WP-42, WP-47 | SEO check -> WP-82; verify tool names (WP-90) |
| R4-16 | Cursor browser tool + Design Mode hands agent selected element code, applied CSS, layout, screenshots | S | WP-47, WP-41 | Visual evidence as harness artifact |
| R4-17 | Anthropic frontend-design plugin steers against generic AI slop; aesthetic direction up front | S | WP-16 | Read plugin source as prior art (WP-90) |
| R4-18 | Storybook MCP (addon-mcp, Storybook 10.3+): Development, Docs, Testing toolsets; `run-story-tests` returns a11y violations; self-healing loop | P | WP-35, WP-46, WP-45 | Version pin 10.3+ |
| R4-19 | Storybook docs toolset needs components manifest (not all frameworks) | P | WP-35, WP-74 | Capability detection |
| R4-20 | "Agents require explicit instructions to avoid hallucinating undocumented properties" | P | WP-33, WP-32 | Never-from-memory rule extends to props |
| R4-21 | Chromatic hosted visual diffs + Storybook MCP | S | WP-45 | |
| R4-22 | Percy AI Visual Review Agent filters false positives | S | WP-45 | Vendor claim |
| R4-23 | Lost Pixel OSS: Playwright screenshots of stories/pages, baselines in repo, GitHub Action | S | WP-45 | Fits git-native baselines |
| R4-24 | Regression tools confirm "unchanged" not "correct"; first-time agent output has no baseline; human or rubric must approve baseline | U | WP-41, WP-45 | Rubric-based first approval not in WP-41: add (WP-17 rubric) |
| R4-25 | Deque: axe-core fully covers ~57% of issues by volume (2,000+ audits, 13k pages) | S | WP-42 | Number verify; verdict wording "automated-only" |
| R4-26 | Practical a11y pattern: axe via Storybook addon/Playwright, Lighthouse via DevTools MCP | S | WP-42, WP-46 | |
| R4-27 | Explicit probes: computed contrast, target size >=24px (WCAG 2.2 SC 2.5.8), keyboard-driven focus order | U | WP-42 | 24px threshold not fetched; verify (WP-90) |
| R4-28 | Absence of axe violations is not evidence of accessibility; gate reports "automated-only" scope | I | WP-42, WP-40 | |
| R4-29 | Stylelint (stylelint-declaration-strict-value) fails raw hex/rgb/hsl outside token sheet | S | WP-42 | |
| R4-30 | AI hardcodes resolved value instead of semantic token | S | WP-42 | |
| R4-31 | Atlassian token usage guide; "State of AI in Design Systems" coercion techniques (not read) | S/U | WP-90, WP-31 | Read techniques page |
| R4-32 | Lint (static) plus render (visual) both needed; lint can pass while render wrong | I | WP-42, WP-41 | |
| R4-33 | Hardening consensus: keep UI/product shape, rebuild foundations | S | WP-19 | |
| R4-34 | First step characterization tests pinning behavior, then refactor, then harden auth/data/integrations | S | WP-19 | Auth/data/integration hardening beyond UI: partial; DISPOSITION: ranger/smith general paths cover |
| R4-35 | Common failures: interface wired only to local state, calls to nonexistent endpoints, saves that do not persist | S | WP-318 | UNMAPPED before; wiring-truth probe |
| R4-36 | "Vibe-prototype is your PRD, not your first product version" | S | WP-14 | |
| R4-37 | Code-first suits uncertain outcomes; "specification emerges from lessons learned" | S | WP-10, WP-14 | |
| R4-38 | Prototype-to-spec has no strong primary source; blog-level | U | WP-90, WP-14 | Treat WP-14 as hypothesis; test with WP-60 |
| R4-39 | Fowler/Böckeler: Kiro made small bug into 4 user stories / 16 acceptance criteria ("sledgehammer to crack a nut") | P | WP-310, WP-309 | Proportionality |
| R4-40 | Spec Kit output repetitive "with each other and with the code"; review fatigue | P | WP-310 | |
| R4-41 | Agents "frequently" ignore instructions or overreach | P | WP-64, WP-50 | |
| R4-42 | Tessl showed non-determinism even from detailed specs | P | WP-311 | Variance measurement |
| R4-43 | Spec-as-source risks MDD inflexibility and non-determinism | P | WP-62 | DISPOSITION: Wisp keeps spec as contract, not source of generation |
| R4-44 | Unclear functional vs technical boundary in specs | P | WP-30, WP-310 | spec@2 section separation |
| R4-45 | Nothing checks code matches spec; research step catalogued classes then agent regenerated duplicates | S | WP-73, WP-312 | Drift check exists (spec-drift); duplicate-creation via WP-312 |
| R4-46 | HN practitioner: specs drift; duplication and contradictions | S | WP-52, WP-73 | |
| R4-47 | Kiro-style specs treated as launch docs that drift once generation starts | S | WP-73 | |
| R4-48 | OpenSpec: current specs/ separate from changes/ deltas; brownfield-first; per-change scope reduces churn | S | WP-14, WP-30 | Tension with R1-39 |
| R4-49 | Specs help: multi-file, uncertain approach, well-bounded checkable behavior | I | WP-309, WP-18 | Router criteria |
| R4-50 | Specs hurt: small changes, visual/taste-driven work, moving design | I | WP-309, WP-10, WP-30 | Core rationale for explore mode |
| R4-51 | No first-party UI-SDD write-ups from Shopify/Airbnb/Uber/Atlassian/Vercel found; flag absent | U | WP-90 | DISPOSITION: do not infer their practice |
| R4-52 | Worktrees give file isolation; "merge conflicts" vs "intent conflicts" (clean merge, wrong combined behavior) | S | WP-55 | |
| R4-53 | Collision hotspots: routing tables, config, component registries (also tokens, shared primitives, global CSS) | S | WP-55 | |
| R4-54 | Assign explicit file ownership; sequence tasks sharing files; merge one branch at a time | S | WP-55 | |
| R4-55 | 3-5 agents practical ceiling | S | WP-55 | Contradicts Anthropic /batch 5-30 (see Contradictions) |
| R4-56 | Anthropic: worktrees, /batch (5-30 subagents each in worktree), Writer/Reviewer fresh-context pattern | P | WP-55, WP-70 | |
| R4-57 | Intent conflicts on UI appear only when rendered together; need post-merge render check | U | WP-55, WP-41 | |
| R4-58 | AI UI review checklists: invented round numbers (99.9%, 50%) | S | WP-43 | |
| R4-59 | Placeholder names (Acme, John Doe) | S | WP-43 | |
| R4-60 | Invented testimonials/ratings | S | WP-43 | |
| R4-61 | Missing loading/empty/error/permission states | S | WP-19, WP-33 | Permission state: add to hardening checklist and muse state list (muse already has empty/loading/error, not permission): WP-19 note |
| R4-62 | Unlabeled icon buttons | S | WP-42, WP-17 | axe covers partly |
| R4-63 | Buttons that submit forms by accident | S | WP-17, WP-46 | Needs interaction test; WP-46 |
| R4-64 | Rule: every finding carries evidence plus location (quoted value, where it lives) | S | WP-43, WP-50 | |
| R4-65 | Mechanizable: extract visible DOM text via Playwright, diff vs source-of-truth copy file, flag numerals, proper nouns, untraceable claims | I | WP-43 | |
| R4-66 | Failure 1: gates judge text, never render; add render-evidence artifact required for UI scope; "not rendered" = coverage gap never pass | I | WP-40, WP-41 | |
| R4-67 | Failure 2: spec churn; add explore mode (throwaway, no spec/gate, time/scope boxed) then spec from prototype, prototype as visual oracle | I | WP-10, WP-11, WP-14 | Time/scope box: WP-11 has none; add timebox in WP-11 |
| R4-68 | OpenSpec-style deltas rather than rewriting whole specs; skip pipeline for one-sentence diffs | I | WP-14, WP-309 | |
| R4-69 | Failure 3: taste criteria reference visual oracle (approved screenshot/story baseline) not adjectives | I | WP-30, WP-41, WP-45 | |
| R4-70 | Failure 4: content-provenance check | I | WP-43 | |
| R4-71 | Failure 5: stylelint strict-value in smith plus render check of computed values | I | WP-42, WP-46 | |
| R4-72 | Failure 6: axe + keyboard + contrast + target-size; verdict says automated coverage partial (~57%) | I | WP-42 | |
| R4-73 | Failure 7: file-ownership in plan; single-writer for shared tokens; integrated render after merge | I | WP-55 | |
| R4-74 | Failure 8: independent evidence-bearing verifier matches Wisp adversary/exit-gate shape but lacks rendering tools | I | WP-40, WP-17 | Tool access for agents (rendering) must be in Codex counterparts (WP-70) |
| R4-75 | Gaps: most Playwright/Chromatic/Percy/Lost Pixel/parallel claims from summaries, not opened | U | WP-90 | |
| R4-76 | Gap: WCAG 2.2 target-size threshold not fetched | U | WP-90 | Duplicate of R4-27 |
| R4-77 | Gap: no primary sources for big-company agentic front-end practices | U | WP-90 | Duplicate of R4-51 |
| R4-78 | Gap: prototype-to-spec lacks primary source | U | WP-90 | Duplicate of R4-38 |

Row counts: R1 50, R2 51, R3 67, R4 78 = 246.

## (1) CONTRADICTIONS between sources (and with the WP draft)

1. Code Connect numbers: R2 blog median (quality +1, tokens -29.5%, duration -19.6%) vs search snippet Coinbase 11.5%/22.3%/22.5% (R2-17 vs R2-18). Different cohorts/sources; do not quote either without opening the Figma blog.
2. get_variable_defs: desktop-only (search summary) vs not remote-only (official table) (R2-06). Prefer the official table; verify.
3. Storybook MCP tool names: R1 lists docs-list/docs-show/get-storybook-story-instructions/test-run; R4 lists toolsets with `run-story-tests` (R1-33 vs R4-18). One may be an older/LLM-summarised name set; check docs/ai/mcp/overview.
4. Screenshots: R2-26 says screenshots alone drift and need structured data; R4 recommends screenshot loops as the check. Resolve: screenshots are evidence of rendering only, specification must come from tokens/structure (R1 lesson 2) plus a11y tree (R4-12).
5. Parallel ceiling: 3-5 agents practical (R4-55) vs Anthropic /batch 5-30 subagents (R4-56). The latter is capability, the former is practitioner advice for merge-safety; WP-55's "3-5" needs qualification.
6. Reviewer scope: Anthropic says over-prompted reviewers over-report, restrict to correctness (R4-06); WP-50 says scanners report all with confidence then filter separately. Compatible only if the filter stage is separate and cheap; test in WP-60.
7. Option count: R3 lesson says cap ~3 (R3-63); WP-16 says propose ~4 directions. Pick one default (suggest 3 for options within a direction, 4 only for first direction-commit) and justify in the ADR.
8. Spec drift: R1-39 says OpenSpec specs drift and do not self-update; R4-48 says OpenSpec per-change deltas reduce churn. Both can hold (reduces churn, does not solve drift).
9. uSpec agents: blog says Cursor; docs say Cursor/Claude Code/Codex (R1-17).
10. R3-49 "decision logs are not a feature anywhere" vs R3-21 Stitch agent remembers project history and R3-09 handoff bundle includes chat. Memory exists; structured, status-bearing logs not found. Absence-of-evidence claim, weak.
11. Kiro: vendor claims browser-verified UI loop (R1-37) vs Fowler review finding over-specification and no code-vs-spec check (R4-39, R4-45). Not directly contradictory; vendor claim is unverified.
12. WP-30 "no TBD in spec" vs R3 "allow TBDs" in sketch: consistent only if sketch and spec are strictly separate artifacts; enforce by schema (sketch not a spec@N).
13. R3-13 multi-person editing unreliable vs Wisp's file-based multi-agent model: not a contradiction, but note single-author assumption.

## (2) CLAIMS TO VERIFY before acting (and how)

| Claim | Rows | How to verify |
|---|---|---|
| DESIGN.md front-matter fields, 8-section order, 11 lint rules, export targets, alpha status | R1-02..07 | Read github.com/google-labs-code/design.md README/spec; run `npx @google/design.md lint` on a sample in a scratch dir |
| Per-agent DESIGN.md integration docs | R1-09 | Search Claude Code/Cursor/Gemini CLI docs; likely none: record "no protocol" |
| uSpec license/ownership/architecture | R1-13,14,49 | Read repo LICENSE, org, docs.uspec.design llms.txt, Uber blog |
| awesome-design-md scrape provenance and license | R1-10,11 | Read repo README/LICENSE; check brand-asset terms |
| DTCG 2025.10 stable status and features | R1-31 | Read designtokens.org spec and W3C announcement |
| Storybook MCP tool names, 10.3+ version, visual regression exposure, manifest framework support | R1-33,35, R4-18,19 | storybook.js.org/docs/ai/mcp/overview; try in a scratch Storybook |
| Kiro browser-verified UI loop | R1-37 | Kiro docs and a trial; treat as vendor claim otherwise |
| OpenSpec ~250 vs ~800 lines | R1-38 | Read Augment article and OpenSpec repo; sample real change folders |
| Figma get_variable_defs remote vs desktop | R2-06 | Tools-and-prompts table plus a remote-endpoint call if a seat is available |
| Figma 25k response cap, Starter ~6 calls/month, Tier 1 limits | R2-10,31 | Figma developer docs rate-limit pages; mcp-server-guide |
| Code Connect effect sizes and Coinbase numbers | R2-17,18 | Open figma.com/blog/the-benefits-of-code-connect-in-mcp; check sample size and who measured |
| Code Connect GA date | R2-20 | Figma release notes |
| Figma write beta pricing | R2-13 | Figma pricing/blog; re-check at adapter build time |
| Roundtripping token tax article | R2-37 | Retry fetch via alternate route or archive |
| hipsquare 50% | R2-36 | Open article; treat n as small; replicate only within WP-03/WP-60 |
| Claude Design handoff bundle contents, quota burn, drift at revision 4-5 | R3-10,14,15 | Read claude.com/product/design and support article; reproduce in a scratch session if access; PCWorld original |
| Stitch framework export; Stitch MCP | R3-23,25 | Stitch docs; one source only so far |
| Tempo/Relume/Uizard/Subframe/v0 branching | R3-02,30,36,41 | Product docs; otherwise leave as DISPOSITION no-action |
| Playwright a11y snapshot ~1/4 tokens | R4-12 | Measure on own pages (feeds WP-307, WP-03) |
| Chrome DevTools lighthouse_audit tool and parameters | R4-15 | developer.chrome.com/docs/devtools/agents (open page, currently snippet) |
| Deque 57% | R4-25 | Open deque.com study; note by-volume vs by-criteria |
| WCAG 2.2 SC 2.5.8 24px target size | R4-27 | W3C WCAG 2.2 text (minimum 24x24 CSS px with exceptions) |
| Percy AI review agent false-positive filtering; Chromatic/Lost Pixel features | R4-21..23 | Vendor docs; only matters if WP-45 names tools |
| Anthropic frontend-design plugin behavior | R4-17 | Read plugin SKILL in anthropics/claude-code repo |
| Fowler SDD article quotes (Kiro 4 stories/16 criteria) | R4-39..45 | Already [P]; spot-check quotes against page |
| Parallel-agent advice (3-5 ceiling, intent conflicts) | R4-52..57 | Blogs only; validate with own measurement in WP-55 pilot |
| Big-company practices absent | R4-51 | Targeted search of engineering blogs; otherwise leave absent |
| Anthropic best-practices doc quotes (Stop hook, fresh-context verifier) | R4-04..06 | [P] but re-open before quoting in an ADR |

## (3) PROPOSED NEW WPs (deduplicated)

- WP-301 Design-token interchange policy: adopt W3C DTCG (2025.10) as the canonical JSON token format referenced by spec@2 and exportable from the design-intent file; map DESIGN.md `export dtcg`, Style Dictionary and Tokens Studio paths; require DESIGN.md section-order and lint-rule parity notes. Target: <refs>/design/tokens.md, WP-30/31 schemas.
- WP-302 Provenance and licensing of design-intent inputs: tag every intent fact authoritative vs inferred (scraped/community DESIGN.md, screenshot-measured); record third-party license before vendoring examples (uSpec unverified, awesome-design-md scraped). Target: design-intent schema field plus vanguard guidance.
- WP-303 Figma MCP operational reference: tool inventory with as-of date, remote vs desktop endpoints, rate/plan limits, 25k cap, metadata-first procedure, flat-layer limits of code-to-canvas, treat output as reference not truth, Console MCP distinction. Target: <refs>/tooling/figma-mcp.md (loaded only by the adapter agent).
- WP-304 Chosen-option handoff bundle: format combining chosen sketch option, tokens, decision log, visual oracle, and README prompt (Claude Design analogue) consumed by `promote`. Target: muse promote skill plus schema.
- WP-305 Exploration cost telemetry and budget: record tokens/time per sketch round, default option cap, warn at budget; fed by WP-03. Target: muse sketch SKILL.md plus mason:evaluate metrics.
- WP-306 Option divergence and re-anchoring protocol: check that options differ on declared axes (not just cosmetic), trigger fresh anchoring after N revisions (R3 cites 4-5) rather than stacking corrections. Target: muse sketch agent judgment plus reference.
- WP-307 Browser-evidence modality policy: a11y-tree/DOM text first for structure and copy, screenshots for visual claims, Lighthouse/axe JSON for audits; token-cost measured on own pages. Target: <refs>/verification/browser-evidence.md.
- WP-308 Hook-based deterministic enforcement: use Stop/pre-commit hooks to run render evidence, token lint and copy check so completion cannot be claimed without a signal. Target: harnesses/ docs plus smith recipe; Codex counterpart.
- WP-309 Small-change fast path: routing rule that skips spec/plan for one-sentence diffs and visual tweaks, with explicit criteria and an audit trail. Target: sentinel/navigator routing and muse mode router (WP-18).
- WP-310 Spec proportionality and de-duplication: ceiling on criteria per change size, no criteria that restate code, functional vs technical split; counters Kiro 4 stories/16 criteria and Spec Kit repetition. Target: shared/constitution.md amendment (with WP-50) plus scribe/muse auditors.
- WP-311 Run-to-run variance measurement: repeat same spec N times, compare outputs, to quantify non-determinism (Tessl finding). Target: mason:evaluate (extends WP-60).
- WP-312 Reuse-before-create inventory: recon emits an inventory of existing components/abstractions/tokens; implementer and reviewer must cite reuse or justify new (Code Connect analogue, duplicate regeneration). Target: smith/muse recon, workspace-manifest@2.
- WP-313 Tool landscape reference with as-of dates and re-verify triggers: records Claude Design, Stitch, v0, Make, Magic Patterns, Kiro, Spec Kit, OpenSpec, awesome-design-md, with explicit "no integration" dispositions. Target: docs/ (not runtime-loaded) or <refs>/design/landscape.md.
- WP-314 Wireframe/IA option type for sketch: sitemap/wireframe-level options before visual options (Uizard, Relume). Target: muse sketch.
- WP-315 Annotation and feedback intake: element-anchored comments persisted in files, batched per round (Bolt stacked edits), so feedback is never lost. Target: muse sketch references.
- WP-316 Motion spec and verification: motion tokens, timing, prefers-reduced-motion criteria in spec@2; probes in WP-42 (uSpec motion, Figma get_motion_context). Target: muse drafter/auditor, shared references.
- WP-317 Untrusted design-source content: design files, DESIGN.md, MCP and scraped content are data, never instructions; sanitization and confirmation rules for write actions. Target: shared/constitution.md plus adapter agent.
- WP-318 Wiring-truth probe for hardening: verify UI actions hit existing endpoints, persist, and survive reload (vibe-code failures); extends WP-19. Target: smith UI verification recipe.
