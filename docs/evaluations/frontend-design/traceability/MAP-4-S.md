# MAP-4-S: traceability of S1, S2, S3 findings to work packages

Tags: [P] primary/first-party, [S] secondary/third-party/aggregator, [U] unverified or source unopened/403/conflicting, [I] researcher inference.
WP ids refer to WP-draft.md; WP-4xx are new proposals (section 3 of this file).

## S1 (Shopify / Airbnb / Vercel / Atlassian)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| S1-01 | Atlassian structured content: TypeScript schemas kept beside code for components, icons, tokens, lint rules, foundations; each covers usage, examples, props, content standards, a11y | [P] | WP-31, WP-74, WP-32 | Draft has small routed files; missing: schema-in-code (typed, co-located with source) as the canonical form that generates other formats. See WP-403 |
| S1-02 | Atlassian AI "skills" auto-update structured content and run evals and code-health checks | [P] | WP-72, WP-73 | WP-72 covers generate-from-source; missing: scheduled content-health/eval run on the intent files themselves (WP-73 is spec-drift only) |
| S1-03 | Atlassian claim: 4.9% more accurate code (own benchmarks) | [P] | WP-60, WP-402, WP-401 | Vendor self-benchmark; treat as direction only. Verify list C1 |
| S1-04 | Atlassian claim: 11% fewer errors | [P] | WP-402, WP-401 | Same caveat; baseline undefined in S1 |
| S1-05 | Atlassian claim: 34% faster | [P] | WP-402, WP-401 | Baseline unclear; do not compare with CLI-vs-MCP 8% |
| S1-06 | Atlassian claim: 16% fewer tokens | [P] | WP-402, WP-401 | Baseline unclear |
| S1-07 | Atlassian claim: 26% fewer tool calls | [P] | WP-402, WP-401 | Baseline unclear |
| S1-08 | Atlassian claim: 52% accuracy on queries (own benchmarks) | [P] | WP-402, WP-401 | Ambiguous (absolute accuracy on content queries); verify definition |
| S1-09 | Atlassian blog URLs: ai-at-work/teaching-ai-to-speak-our-design-language (2026-06-02) and ...building-the-context-engine-for-the-ai-era | [P] | WP-90 | Primary sources to be read in full by WP-90 |
| S1-10 | ADS MCP remote https://mcp.atlassian.com/v1/ads/public/mcp, local `npx -y @atlaskit/ads-mcp`: tokens, icons, components, primitives, a11y guidance | [P] | WP-74, WP-35 | Dual remote+local MCP deployment; WP-74 compares CLI vs MCP but not distribution mode. Capability-detect in WP-35 |
| S1-11 | https://atlassian.design/llms.txt published alongside MCP | [P] | WP-74, WP-440 | llms.txt validity checking missing, see WP-440 |
| S1-12 | Figma MCP + ADS MCP + Rovo Dev CLI homepage redesign demo (2026-02-23): reads Figma and repo conventions, plans, generates, runs tests, axe-core fixes, humans review | [P] | WP-35, WP-42, WP-46 | Pipeline shape equals muse->navigator->smith; axe fix loop is in WP-42; missing: human review checkpoint placement |
| S1-13 | Demo claim: 4-5 dev-days reduced to 20 min, 1,381 LOC; self-caveated on design-system maturity | [P] | WP-401, WP-03 | Marketing-grade; use only as caveat that maturity of source system gates value. Do not cite as benchmark |
| S1-14 | Atlassian CLI `npx @atlaskit/ads-cli search button`, 2026-09-16: same content usable from any shell, CI, agent | [P] | WP-74, WP-47 | WP-74 covers CLI vs MCP; missing: CLI is usable in CI as a gate (deterministic), see WP-411 |
| S1-15 | CLI vs MCP: 8% faster, 8% fewer tokens | [P] | WP-74, WP-402 | Small delta; benchmark used transcript analysis not only pass/fail (S1-16). Contradiction C2 with MCP-first stances |
| S1-16 | Atlassian CLI benchmark on real front-end tasks with transcript analysis (not just pass/fail) | [P] | WP-60, WP-03 | Supports WP-03 transcript metrics and WP-60 outcome grading; method worth copying |
| S1-17 | DESIGN.md test (2026-06-15): token frontmatter plus prose; file at atlassian.design/DESIGN.md | [P] | WP-31 | WP-31 adopts DESIGN.md-compatible format; the Atlassian result argues for limiting its role. See C1 |
| S1-18 | DESIGN.md login-screen task: ~7.21M tokens | [P] | WP-31, WP-402 | Highest cost of four arms; ~1.7x no-context |
| S1-19 | Same task: MCP 3.75M tokens | [P] | WP-74, WP-402 | Lowest cost arm |
| S1-20 | Same task: skill 4.43M tokens | [P] | WP-31, WP-402 | Skill cost more than no context (4.20M): skills are not free. Check quality outcome not given |
| S1-21 | Same task: no context 4.20M tokens | [P] | WP-402 | Baseline; shows context can cost more than it saves |
| S1-22 | DESIGN.md limits: all-at-once context, lossy compression (2.5 MB to 80 KB), agents recreate components rather than import | [P] | WP-31, WP-35, WP-42 | Component-recreation needs a detector (reuse check in WP-35/WP-42); loss on compression argues against monolith in WP-31 |
| S1-23 | Recommended DESIGN.md uses only: art direction, quick prototyping, customer theming, tool interop | [P] | WP-31, WP-12, WP-18 | Maps cleanly to exploration (sketch) vs production routing: DESIGN.md for sketch mode only; production uses lookup (WP-74). Make explicit in WP-31 |
| S1-24 | Atlassian authors say DESIGN.md results not conclusive | [P] | WP-401, WP-60 | Own n small; run our own paired test (WP-402) |
| S1-25 | Atlassian verification stack: lint rules in schema, axe-core, tests, human review, internal evals; no visual-regression detail found | [P] | WP-42, WP-45, WP-41 | Lint rules inside schema (lint as part of the content source) is a pattern: see WP-412. Visual regression gap = our WP-45 is ahead |
| S1-26 | Exploration (DESIGN.md/Figma Make) vs production (MCP/CLI plus real components) split | [I] | WP-18, WP-10 | Inference by researcher; consistent with S1-23. Do not cite as Atlassian statement |
| S1-27 | Vercel "Teaching agents product design" (2026-06-25, John Phamous): in-repo `product-design` skill | [P] | WP-31, WP-18, WP-67 | Primary template for several WPs; read in full under WP-90 |
| S1-28 | Root AGENTS.md says when to load skill; skill-local AGENTS.md sets load order and validation | [P] | WP-71 | Two-level AGENTS.md (router plus skill-local load order); WP-71 covers router only. Add skill-local AGENTS.md convention |
| S1-29 | References: product-judgment, interface-quality, resilience, copy, patterns, surfaces-{surface}.md | [P] | WP-31, WP-19, WP-20 | Reference taxonomy by concern; resilience maps to WP-19 harden; copy to WP-20; surfaces-per-surface files missing in WP-31 |
| S1-30 | Exemplars: PRs worth repeating and mistakes | [P] | WP-31 | Draft has "exemplar good/bad PRs". Missing: how exemplars are collected (WP-414) |
| S1-31 | `coverage-gaps.md` listing where no standard exists | [P] | WP-31, WP-40 | Draft names coverage-gaps file; add rule that agent must flag when working inside a listed gap and propose decision (WP-13). Also parallels "unrendered UI is a coverage gap" in WP-40 |
| S1-32 | Deterministic linters: no nested modals, accessible names on icon buttons | [P] | WP-42, WP-412 | Examples of rule-to-lint; need an explicit promotion ladder (WP-412) |
| S1-33 | Evals with before/after fixtures and hidden expected edits to test generalization to unseen UI | [P] | WP-67, WP-60 | Covered by WP-67 |
| S1-34 | SKILL.md resolves a mode first: shape (compare alternatives, no edits) | [P] | WP-18, WP-11 | Maps to sketch; WP-18 says exploration modes read-only or sketch-only |
| S1-35 | Mode: implement (smallest coherent change) | [P] | WP-18 | "Smallest coherent change" as implement-mode contract not in draft; add to WP-18 |
| S1-36 | Mode: review (findings, no edits unless asked) | [P] | WP-18, WP-17 | Covered |
| S1-37 | Mode: copy | [P] | WP-18, WP-20 | Covered |
| S1-38 | Mode: harden (fix state/resilience/a11y, keep direction) | [P] | WP-18, WP-19 | Covered by WP-19 |
| S1-39 | Contract: "never claim visual verification from code alone" | [P] | WP-40, WP-41 | WP-40 "unrendered UI is a coverage gap"; add as verbatim constitution rule, see WP-50. Conflicts with static slop scanners if mislabeled (C6) |
| S1-40 | Findings tiered P0-P3 with source and fix | [P] | WP-17, WP-53 | Cite source per finding (evidence) = WP-50 evidence-citing blockers |
| S1-41 | Decision authority order: user goals > verified evidence > repo guidance > accepted decisions > adjacent patterns > heuristics | [P] | WP-18, WP-13 | WP-18 only has "explicit authority labeling". Missing the ordered precedence list: see WP-413 |
| S1-42 | Weekly feedback collection from Slack/Figma/GitHub | [P] | WP-13 | Missing: harvesting mechanism and cadence, see WP-414 |
| S1-43 | Candidate rules stay pending until human accepts | [P] | WP-13 | Covered |
| S1-44 | Never promote one screenshot or comment into a universal rule (multi-source) | [P] | WP-13 | Covered; add minimum-evidence count threshold |
| S1-45 | Vercel design.md (2026-08-31): public brand guidance file plus vercel-brand.css primitives loaded by agents (v0, Codex, Claude) | [P] | WP-31, WP-35 | Pairing prose with executable CSS primitives; add to WP-31 |
| S1-46 | design.md includes anti-patterns ("generated-design patterns we never want") | [P] | WP-16, WP-31 | Covered (ban lists/rejection clauses) |
| S1-47 | design.md eval: 7 fixed scenarios, 200+ developer runs | [P] | WP-60, WP-67 | Design of fixed scenario suite; reuse shape |
| S1-48 | design.md eval: 39 vs 91 known failures (57% fewer), self-described far too small sample | [P] | WP-401, WP-60 | Arithmetic checks (52/91=57.1%). Contradicts Atlassian DESIGN.md result direction (C1) |
| S1-49 | Slack @design-agent captures real use | [P] | WP-414, WP-13 | Telemetry from real use feeds rule candidates; see WP-414 |
| S1-50 | v0 Design Systems 2.0 docs: ingests GitHub, npm, Storybook/docs, Figma, screenshots, ZIPs | [P] | WP-35, WP-32 | Multi-source ingestion list; WP-35 adapter is Figma/screenshot/html. Missing npm/Storybook/ZIP inputs |
| S1-51 | v0 produces a "skill" with `v0.json` (max 3 reference sources, starter app, distilled instructions) | [P] | WP-72, WP-31 | "Distill instructions from sources into skill" = WP-72 generation; cap of 3 sources is a context-economy rule worth testing |
| S1-52 | v0 builds and previews a starter app; user must approve before saving; updates re-validate | [P] | WP-34, WP-35 | Preview-and-approve gate for ingestion: see WP-418 |
| S1-53 | v0 DS 2.0 launch date conflicts (Feb 5 vs June 25 2026); no Vercel blog post found | [U] | WP-90 | Date unverified; do not cite date |
| S1-54 | Earlier: shadcn registry + MCP, 2025-08-22 vercel.com/blog/ai-powered-prototyping-with-design-systems | [P] | WP-35, WP-74 | Registry as lookup source; see S3 shadcn rows |
| S1-55 | Earlier: Figma/npm import in v0, 2025-01-27 vercel.com/blog/working-with-figma-and-custom-design-systems-in-v0 | [P] | WP-35 | Historical; low value |
| S1-56 | Not found: Vercel "design engineer" role essay or Geist-for-agents beyond design.md | [U] | none | Negative result; disposition: no action; record in WP-90 as searched |
| S1-57 | Shopify Polaris + Dev MCP: `npx -y @shopify/dev-mcp@latest` serves docs, GraphQL introspection, validation of generated code across Polaris web components surfaces | [P] | WP-74, WP-35 | "Validate generated code" tool inside MCP = verify loop; missing in WP-74: validation tool as lookup-interface feature (WP-411) |
| S1-58 | Polaris web components early access via env flag POLARIS_UNIFIED=true | [P] | WP-90 | Time-sensitive; may be stale; verify |
| S1-59 | Dev MCP exact tool names not listed in fetched page; no visual/a11y verification described | [U] | WP-90 | Open item |
| S1-60 | River (2026-05-28): Slack-native agent, public channels only | [P] | WP-55, WP-407 | Public-channel-only scoping is a trust-tier choice; see WP-407 |
| S1-61 | River stats: ~19 min / ~50 tool calls median session; 59,918 sessions and 3,536 coauthored merged PRs in 30 days | [P] | WP-03, WP-91 | Reference metrics for baseline (sessions, median tool calls); not design-specific |
| S1-62 | River: knowledge as files loaded on demand; learns from public transcripts into prompts/skills | [P] | WP-13, WP-72, WP-66 | Transcript-to-skill learning loop = WP-414 variant; human acceptance required (WP-13) |
| S1-63 | Shopify Dispatch security pipeline uses a different model for verification (not opened; via third party) | [U] | WP-63, WP-421 | Cross-model verification option: see WP-421. Verify source |
| S1-64 | Shopify Roast: deterministic plus AI steps, resumable (shopify.engineering/introducing-roast) | [P] | WP-66, WP-54 | Resumable mixed deterministic/LLM workflow; covered partially by WP-66 state files; resume semantics not in draft |
| S1-65 | software-factories.port.io/shopify summary of the three | [S] | WP-90 | Secondary only |
| S1-66 | Sidekick (2025-08-26): JIT instructions to avoid "Death by a Thousand Instructions" | [P] | WP-64, WP-71 | Maps to progressive context loading; make "JIT instruction injection" explicit in WP-64 |
| S1-67 | Sidekick: LLM judges calibrated to humans (kappa 0.02 to 0.61) | [P] | WP-60, WP-422 | Judge calibration step missing from WP-60: see WP-422 |
| S1-68 | Sidekick: merchant simulators | [P] | WP-60, WP-67 | User-simulator for eval; optional; note in WP-60 |
| S1-69 | Sidekick: reward-hacking lessons | [P] | WP-50, WP-60 | Agents gaming gates/evals; add to WP-50 (gate hygiene) and WP-60 |
| S1-70 | Tobi memo 2025-04-07: reflexive AI use, justify why AI cannot do it before headcount (via third party; original not opened) | [U] | none | Org policy, not workflow practice. Disposition: out of scope, no WP; evidence: no design/front-end mechanism |
| S1-71 | Nothing public on Shopify design rules files, visual verification, Hydrogen internal agent practice; Hydrogen claims only from T blogs | [U] | none | Negative result; disposition: do not cite Hydrogen claims |
| S1-72 | Airbnb: no first-party AI + DLS, design-to-code, Lottie agent material | [U] | none | Negative result; no WP |
| S1-73 | Airbnb Ghost Platform server-driven UI (2021) is pre-AI | [S] | none | Out of scope; disposition: not relevant to agent workflow |
| S1-74 | Airbnb DLS not public; "Airbnb DESIGN.md" sites (superdesign.dev, open-design.ai) are community reconstructions | [S] | WP-31 | Do not treat as Airbnb; related risk: third-party brand DESIGN.md lack provenance; see WP-401 |
| S1-75 | Airbnb LLM test migration harness: step-based state machine, per-file steps, injected context, validate/retry loops (Medium 403; via ByteByteGo) | [U] | WP-66, WP-54, WP-444 | Bulk migration pattern; see WP-444 migrate mode. Verify source |
| S1-76 | Conference-talk claims: 12+ internal MCP servers, 80% moved IDE to CLI agents, 64% of PRs involve agentic sessions; source dated "November 2026" (after today) | [U] | WP-401 | Unreliable date/attribution; do not use |
| S1-77 | Pattern 1: mode routing up front; exploration modes forbid edits; harden preserves direction | [I] | WP-18, WP-19 | Covered |
| S1-78 | Pattern 2: routed references plus exemplars plus coverage-gaps beat one big file | [I] | WP-31, WP-74 | Covered |
| S1-79 | Pattern 3: rules to deterministic lint where possible, rest as evals with hidden edits | [I] | WP-42, WP-67, WP-412 | Promotion ladder = WP-412 |
| S1-80 | Pattern 4: rule promotion requires human acceptance and multiple sources | [I] | WP-13 | Covered |
| S1-81 | Pattern 7: evidence mostly self-reported benchmarks with small samples | [I] | WP-401, WP-60 | Source-quality policy |

## S2 (Netflix / IBM / Spotify / Primer / Fluent / Salesforce / Adobe / others)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| S2-01 | Kaelig Deloumeau-Prigent "State of AI in Design Systems" (July 2026, CC-BY, 21 systems, audits public repos); llms.txt at state-of-ai-in-design-systems.netlify.app | [S] | WP-90, WP-409 | Best index; use as source for coercion catalog (WP-409). Count 20 vs 21 mismatch (C8) |
| S2-02 | Survey does not cover Netflix, Duolingo, Linear, Stripe, Notion, Encore | [S] | WP-90 | Coverage gap; Encore data comes from talk only |
| S2-03 | Carbon remote MCP mcp.carbondesignsystem.com/mcp | [P] | WP-74, WP-35 | MCP lookup precedent |
| S2-04 | Carbon MCP 4 tools: docs_search, code_search, get_charts, labs_search | [P] | WP-74 | Tool surface granularity (search-style, few tools) vs Primer 20 tools; see C5 |
| S2-05 | Carbon MCP needs IBMid OAuth; closed source | [P] | WP-74 | Auth on lookup layer; not reproducible; record as constraint |
| S2-06 | Carbon docs onboarding URL carbondesignsystem.com/developing/carbon-mcp/onboarding-and-setup/ | [P] | WP-90 | Read in full |
| S2-07 | carbon-builder agent skill: 24KB | [S] | WP-71, WP-36 | Size budget datum for skills |
| S2-08 | carbon-builder: 12 lazy-loaded reference docs | [S] | WP-33, WP-71 | Lazy-load pattern = load_first; covered |
| S2-09 | Hard rule "never generate Carbon code from training knowledge alone" | [S] | WP-33 | Covered by "never write from memory"; extend from a11y tables to component libraries (WP-33 scope is ARIA/keyboard only). See WP-409 |
| S2-10 | Carbon hand-curated llms.txt | [S] | WP-74, WP-440 | Hand-curated vs generated (Spectrum): see C7 |
| S2-11 | Carbon root AGENTS.md 69 lines used as router ("as short as possible. More length = more tokens") | [S] | WP-71 | Datum: router length; WP-71 says short router, ≤32 KiB; add line-count target |
| S2-12 | Carbon per-package AGENTS.md | [S] | WP-71 | Closest-file override; covered |
| S2-13 | Carbon "Bob" triage bot prompt versioned in .github/prompts/bob-bug-triage.md | [S] | WP-72, WP-407 | Prompts versioned in repo; triage-bot out of scope but pattern recorded |
| S2-14 | Carbon works in IBM Bob, Cursor, Claude Code, VS Code Copilot | [S] | WP-70, WP-71 | Cross-harness portability; covered by WP-70/71 |
| S2-15 | "Carbon for AI: Scaling New Ways of Working" (Medium) returned 403, unread | [U] | WP-90 | Open item |
| S2-16 | Carbon verification: nothing public beyond MCP-first rule; nothing on IBM Design Studio | [U] | none | Negative result; no WP |
| S2-17 | Spotify Encore MCP server exposes rules/tokens/component specs; machine-readable docs | [S] | WP-74 | Via talk writeup only (intodesignsystems.com/blog/how-spotify-design-system-ai-ready); no first-party post |
| S2-18 | Encore 3-layer architecture: foundation / style / behavior, headless on React Aria plus Base UI | [S] | WP-81, WP-74 | Informational for consumer repos; layering resembles Brad Frost layers (different thing). Low action |
| S2-19 | Encore speakers: Victoria Tholerus, Aleksander Djordjevic | [S] | none | Attribution only; no action |
| S2-20 | Spotify test framework scoring AI output vs real Encore components: lint errors, similarity scores, visual output | [S] | WP-60, WP-67, WP-405 | Strongest verification pattern found; scoring harness for design-system conformance missing: WP-405 |
| S2-21 | Spotify claims: 220k+ style uses, 93% dev satisfaction | [S] | WP-401 | Marketing-grade survey claims; do not cite. Verify list C9 |
| S2-22 | Primer @primer/mcp: 20 tools | [S] | WP-74 | Tool count differs from Carbon's 4 (C5) |
| S2-23 | Primer lint_css tool described as "REQUIRED FINAL STEP" | [S] | WP-42, WP-412, WP-50 | Mandatory-final-lint-in-tool-description (coercion by tool contract). Maps to deterministic checks; add "final lint step" rule to smith recipe (WP-46) |
| S2-24 | @primer/brand-mcp: 8 tools | [S] | WP-74 | Separate MCP per brand/product surface |
| S2-25 | Primer Storybook MCP at localhost:6006/mcp | [S] | WP-35, WP-46 | Storybook MCP capability-detect; covered by WP-35 |
| S2-26 | Primer: 52 Figma Code Connect files | [S] | WP-35 | Code Connect equivalent; covered |
| S2-27 | Primer .github/copilot-instructions.md plus 5 path-scoped instructions; component-review instructions backed by ADRs | [S] | WP-71, WP-13, WP-17 | Path-scoped instructions = closest-file override; ADR-backed review rules: review agent cites ADR for each rule (decision_ref). See WP-413. WP-17 lacks ADR-backed review |
| S2-28 | Primer 7 skills plus 2 custom agents (modular-ds-implementer, modular-ds-reviewer) | [S] | WP-72, WP-46 | Implementer/reviewer pair as DS-specific agents; smith equivalents exist |
| S2-29 | Primer gh-aw issue-triage with capped safe-outputs | [S] | WP-407, WP-55 | Capped outputs; see WP-407 |
| S2-30 | Primer: no llms.txt/AGENTS.md in primer/react; AGENTS.md in primer/primitives with mandatory lint/format/test/build | [S] | WP-71, WP-57 | Mandatory command list in AGENTS.md; interplay with pre-commit cost (WP-57) |
| S2-31 | Primer docs https://primer.style/product/getting-started/foundations/mcp/ | [P] | WP-90 | Read in full |
| S2-32 | Primer trust tiers: agents restricted to issue creation (Jan Six, via Into Design Systems) | [S] | WP-407, WP-51 | Trust-tier model missing: WP-407 |
| S2-33 | GitHub Spark (GitHub Next): NL to app exploration tool; no design-system detail | [U] | WP-10, WP-12 | Exploration tool category; no action beyond landscape note |
| S2-34 | Fluent AGENTS.md "source of truth, not existing code" | [S] | WP-71, WP-32 | Authority statement: docs override existing code (existing code may be wrong). Add to WP-413 precedence |
| S2-35 | Fluent AGENTS.md has 5 never-violate rules | [S] | WP-71, WP-409 | Prohibition list as coercion technique |
| S2-36 | Fluent CLAUDE.md is redirect to AGENTS.md | [S] | WP-71 | Covered (one-line CLAUDE.md importing AGENTS.md) |
| S2-37 | Fluent 9 skills mirrored in .agents/skills and .claude/skills | [S] | WP-70, WP-408 | Mirror dirs for cross-harness; WP-70 is harnesses/codex; see WP-408 |
| S2-38 | Fluent /visual-test skill: per-component Storybook plus Playwright screenshots | [S] | WP-41, WP-45, WP-46 | Per-component visual test as user-invoked skill; covered by WP-41/45 |
| S2-39 | Fluent /lint-check skill: fix, re-run, repeat | [S] | WP-42, WP-46 | Validation loop; covered |
| S2-40 | Fluent skills use disable-model-invocation (human-triggered) | [S] | WP-406 | Not in draft: policy on which skills are human-trigger-only (expensive visual tests). WP-406 |
| S2-41 | Fluent copilot-setup-steps.yml | [S] | WP-80, WP-70 | Environment bootstrap for agent runs (browsers/deps); add to WP-80 CI work |
| S2-42 | Fluent internal React MCP exists but unreleased (discussion #35732); Blazor MCP public | [S] | WP-90 | Primary: github.com/microsoft/fluentui/discussions/35732; verify |
| S2-43 | Salesforce knowledge shipped as npm skills: @salesforce/afv-skills (slds-apply, slds-validate, slds2-migrate) | [S] | WP-408, WP-444, WP-72 | npm distribution of skills; migrate skill: WP-444 |
| S2-44 | @salesforce/mcp lwc-experts tools | [S] | WP-74 | MCP expert tools; covered |
| S2-45 | @salesforce-ux/slds-linter closing a deterministic validate loop | [S] | WP-42, WP-412 | Linter-gate: skills produce, linter validates, loop until clean. Linter as gate input in workspace-manifest (WP-40 capability kinds lack "linter" for design system) |
| S2-46 | Salesforce starter kit: AGENTS.md routing | [S] | WP-71 | Covered |
| S2-47 | Salesforce .builderrules 5-step checklist | [S] | WP-71, WP-409 | Fixed ordered checklist file; ordered procedure in rules file |
| S2-48 | Salesforce CLAUDE.md one-line import | [S] | WP-71 | Covered |
| S2-49 | Salesforce Figma to LWC MCP tool (beta) | [S] | WP-35 | Figma adapter precedent |
| S2-50 | Salesforce has no llms.txt | [S] | WP-440 | Fact for survey; no action |
| S2-51 | Salesforce primary docs: slds-linter get-started-linter-AI-skills; lwc mcp-design; 2025/10 vibe-code LWC blog | [P] | WP-90 | Read in full |
| S2-52 | Adobe React Spectrum S2: llms.txt plus .md twin per page plus "Copy for LLM" | [P] | WP-74, WP-34 | Markdown twin per page: dual format (human + machine), maps to WP-34; add to WP-74 |
| S2-53 | @react-spectrum/mcp | [P] | WP-74 | Covered |
| S2-54 | Spectrum 3 skills at /.well-known/skills: build, spectrum-audit, v3 to S2 migrate | [P] | WP-408, WP-444 | Discovery URL convention: WP-408; migrate: WP-444 |
| S2-55 | spectrum-audit has deterministic severity-weighted rubric | [P] | WP-17, WP-42, WP-404 | Rubric as numeric deterministic score: WP-404; WP-17 has severity tiers but not weights |
| S2-56 | Spectrum agent context GENERATED from docs source at deploy | [P] | WP-72 | Covered (generate skills from source); see C7 on hand-curated vs generated |
| S2-57 | Spectrum named prohibitions: no Tailwind/shadcn, no UNSAFE_* | [P] | WP-16, WP-409 | Named-prohibition technique |
| S2-58 | Spectrum compile-time `style` macro acts as verifier | [P] | WP-42, WP-47 | Type/compile-time enforcement as verification in consumer; add to WP-42 recipe: prefer compile-time constraints |
| S2-59 | Spectrum Design Data: tokens plus component schemas, Rust core, CLI/wasm/MCP (opensource.adobe.com/spectrum-design-data/ai/) | [P] | WP-31, WP-74, WP-90 | One data core with multiple delivery adapters (CLI/wasm/MCP); supports WP-74 conclusion that facts file is canonical |
| S2-60 | Adobe Firefly marketing only, skipped | [S] | none | Out of scope |
| S2-61 | Netflix Hawkins blog (2022) predates agents | [P] | none | Not relevant |
| S2-62 | Netflix job postings: Hawkins Consumer "evolving into a design intelligence layer" | [S] | WP-31 | Weak signal (job post) |
| S2-63 | Netflix: "centralize agentic context that Commerce, Games, Member extend from" | [S] | WP-71, WP-31 | Layered inheritance of context (base + product extends); closest-file override covers it. Weak signal |
| S2-64 | Netflix: encode voice/tone as machine-readable rules | [S] | WP-20, WP-31 | Covered by copy/voice WP-20 |
| S2-65 | Netflix: no engineering post, MCP or repo | [U] | none | Negative result |
| S2-66 | Figma use_figma tool: agents write to canvas bound to design system | [P] | WP-35 | Write path to Figma out of scope for read-only adapter; record as future |
| S2-67 | Figma /figma-use skill and custom markdown skills encode team conventions; internal use claimed without detail | [P] | WP-35, WP-90 | Marketing-ish; detail missing |
| S2-68 | Figma MCP plus Code Connect plus variable code syntax plus annotations | [P] | WP-35 | Covered |
| S2-69 | Figma "design system rules generation" (scan codebase to rules file) | [P] | WP-35, WP-71 | Rules-file generator in WP-35; covered |
| S2-70 | Anthropic Product Design team: Figma to Claude Code autonomous write/test/iterate loop | [P] | WP-35, WP-60 | Covered; loop bounded by retry caps (WP-51) |
| S2-71 | Anthropic: GitHub Actions PR comments | [P] | WP-45, WP-80 | CI comment of visual evidence; fold into WP-41 |
| S2-72 | Anthropic: use Claude to map error states/edge cases in design phase | [P] | WP-19, WP-11 | State enumeration at sketch time; muse drafter already requires states; add to sketch checklist |
| S2-73 | Claude Design (Anthropic Labs): builds design system from codebase plus design files | [P] | WP-32, WP-35 | Ground-truth extraction; covered |
| S2-74 | Claude Design "a dozen directions" exploration | [P] | WP-16 | Draft says ~4 directions; dozen is breadth; note decision for default count (WP-11 says ~3) |
| S2-75 | Claude Design handoff bundle to Claude Code | [P] | WP-14, WP-30 | Promote/handoff artifact; covered by WP-14 |
| S2-76 | Claude Design internal verification not public | [U] | none | Negative result |
| S2-77 | Pinterest MCP ecosystem post: data/infra tools, registry plus auth; nothing on Gestalt | [P] | WP-74 | Registry+auth pattern for MCP governance; not design. Disposition: no WP |
| S2-78 | Intuit, Duolingo: nothing public | [U] | none | Negative |
| S2-79 | Linear/Stripe/Notion: only third-party DESIGN.md extractions (designmd.directory, open-design, better-design) | [S] | WP-31, WP-401 | Provenance risk; pattern only |
| S2-80 | Indeed (Diana Wolosin): JSON over Markdown in MCP, ~80% fewer tokens | [S] | WP-74, WP-402 | WP-74 lists "JSON over Markdown"; claim unverified (secondary). Conflicts with Spectrum .md twin (C3) |
| S2-81 | Indeed: 4,300 prototypes in 4 months | [S] | WP-12, WP-401 | Prototype volume; marketing-level; no action beyond WP-12 |
| S2-82 | Brad Frost three layers: always-on rules, MCP on demand, AGENTS.md orchestration | [S] | WP-71 | Draft WP-71 has three layers; compare with S3 AWS dev.to layering (AGENTS/SKILL/DESIGN): different decomposition (C4) |
| S2-83 | intodesignsystems.com/blog/design-system-not-ready-for-ai-agents source for Indeed, Spotify numbers | [S] | WP-90 | Read to verify claims |
| S2-84 | Source-quality legend [P]/[S]/[M] used by S2 | [I] | WP-401 | Adopt tagging scheme P/S/U/I in research-report convention |

## S3 (community practitioners)

| ID | finding | tag | mapped WP | note |
|---|---|---|---|---|
| S3-01 | Kaelig repo github.com/kaelig/state-of-ai-in-design-systems; site per-system pages (shadcn-ui) | [P] | WP-90, WP-409 | Primary dataset |
| S3-02 | Survey: 20-21 OSS systems | [P] | WP-401 | Count conflicts with S2 (21): minor |
| S3-03 | Survey: ~200 affordances | [P] | WP-409 | Catalog to mine for agent-facing affordances |
| S3-04 | Survey: 165 coercion techniques (prohibitions, tool-gating, validation loops, exemplar pairs) | [P] | WP-409, WP-16 | Mine the 165 into our reference; WP-16 only covers ban lists and rejection clauses |
| S3-05 | Headline: almost none ship llms.txt/Code Connect/agent instruction files; some llms.txt return 404/HTML shells (search snippet, unverified) | [U] | WP-440, WP-90 | Contradicts S2 (Carbon, Spectrum, shadcn ship llms.txt): C8 |
| S3-06 | shadcn/ui bundled MCP: `npx shadcn@latest mcp` | [P] | WP-74, WP-35 | Covered |
| S3-07 | shadcn Agent Skill with Critical Rules plus Incorrect/Correct pairs | [P] | WP-409, WP-67 | Incorrect/Correct pair format not in draft: WP-409 |
| S3-08 | shadcn curated llms.txt https://ui.shadcn.com/llms.txt | [P] | WP-74, WP-440 | Covered |
| S3-09 | shadcn CLI `info --json` | [P] | WP-411, WP-32 | Machine-readable project introspection for recon; WP-411 |
| S3-10 | shadcn CLI `add --dry-run` | [P] | WP-411 | Dry-run before write; WP-411 |
| S3-11 | shadcn eval suite for skill rules | [P] | WP-67, WP-60 | Covered; confirm structure (hidden edits?) under WP-90 |
| S3-12 | Registry MCP announcement x.com/shadcn/status/1917597228513853603 | [S] | WP-90 | Social post; low priority |
| S3-13 | Hallmark (Nutlope) github.com/Nutlope/hallmark: 21 themes | [P] | WP-16 | Theme library = named aesthetics; covered |
| S3-14 | Hallmark macrostructure selection | [P] | WP-16, WP-11 | Choose page macrostructure before styling; add to sketch step |
| S3-15 | Hallmark 57 slop-test gates | [P] | WP-16, WP-42 | Taxonomy of slop checks; compare with avoid-ai-design 67 patterns; dedupe under WP-409/WP-16 |
| S3-16 | Hallmark pre-emit self-critique | [P] | WP-16, WP-64 | Self-critique before output; Opus producers over-verification caution (WP-64) |
| S3-17 | Hallmark verbs build/audit/redesign/study | [P] | WP-18 | Verbs map to modes: build=implement, audit=review, redesign=sketch+promote, study=research. Add "study" |
| S3-18 | Hallmark: no screenshot QA documented | [P] | WP-40, WP-41 | Gap: slop gates are static; render evidence still needed (C6) |
| S3-19 | avoid-ai-design (funboy322): zero-dep scanner `detect.mjs` | [P] | WP-16, WP-42 | Deterministic slop scanner; zero-dependency property worth copying |
| S3-20 | avoid-ai-design: 67 deterministic patterns | [P] | WP-16, WP-42 | Source for the scanner pattern list |
| S3-21 | avoid-ai-design: P0/P1/P2 severities | [P] | WP-53, WP-16 | Different scale from P0-P3 (WP-53); align |
| S3-22 | avoid-ai-design: JSON output plus exit codes for CI | [P] | WP-42, WP-45 | Scanner contract as CI gate; covered |
| S3-23 | "second-order slop": cream plus terracotta, mono-chrome, numbered 01/02/03 | [P] | WP-16 | Covered (second-order slop patterns) |
| S3-24 | avoid-ai-design generates DESIGN.md for multi-page consistency | [P] | WP-31, WP-12 | Generated intent file to hold consistency across pages |
| S3-25 | taste-skill (Leonxlnx): 9 skills | [P] | WP-16, WP-18 | Skill decomposition |
| S3-26 | taste-skill dials DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY | [P] | WP-16 | Covered (taste dials) |
| S3-27 | taste-skill brief inference, redesign-audit, pre-flight check | [P] | WP-16, WP-18 | Brief inference matches anchor brief (WP-11) |
| S3-28 | taste-skill imagegen skill produces reference images only | [P] | WP-12, WP-16 | Boundary: generated images as references, not assets; add as rule in WP-12/WP-43 |
| S3-29 | taste-skill stars 46k vs 98k conflict | [U] | WP-401 | Do not cite popularity |
| S3-30 | Koomook/claude-frontend-skills: single distinctive-frontend skill (typography extremes, cultural palettes, motion, backgrounds), derivative of Anthropic frontend-design | [P] | WP-16 | Derivative; low value |
| S3-31 | Anthropic frontend-design skill baseline: 4 pre-CSS questions (purpose, tone, constraints, differentiation) | [S] | WP-11, WP-16 | Pre-CSS question set is a ready sketch intake; add to WP-11 |
| S3-32 | frontend-design: commit to extreme direction | [S] | WP-16 | Covered (direction-commit) |
| S3-33 | frontend-design bans Inter/Roboto/Arial | [S] | WP-16 | Ban list; also a common-slop precedent for "bans cause new default" second-order slop |
| S3-34 | agenticskills.io aggregator is secondary for frontend-design | [S] | WP-90 | Verify against Anthropic repo |
| S3-35 | Matt Pocock skills github.com/mattpocock/skills: `prototype` skill | [P] | WP-11, WP-14, WP-18 | Core model for sketch/promote; read in full |
| S3-36 | prototype: throwaway HTML or multiple UI variations toggled from one route | [P] | WP-12, WP-11 | Variant toggle in a single route: add to WP-12 (option matrix medium) |
| S3-37 | prototype sits between grill-me and TDD/PRD | [P] | WP-18, WP-14 | Pipeline position: interrogate then prototype then PRD/TDD. grill-me not mapped: WP-427 |
| S3-38 | deepwiki.com/mattpocock/skills/3.5-prototyping returned 429 | [U] | WP-90 | Unread; repo fetch used |
| S3-39 | Emil Kowalski design-engineering skill: animation easing/duration, fixed review format | [S] | WP-17, WP-16 | Fixed review format = output contract for design review; motion rules not in draft: WP-437 |
| S3-40 | Jakub Krehel Typography and Better Layout skills | [S] | WP-16, WP-17 | Domain-specific design skills (typography, layout); reference packs: WP-437 |
| S3-41 | craftwork.design/skills index (secondary); note.com deep dive | [S] | WP-90 | Secondary |
| S3-42 | TechNickAI ai-coding-config Design Reviewer agent (PR 4) | [P] | WP-17 | Primary model for WP-17 |
| S3-43 | Design Reviewer: Playwright at 1440/768/375 | [P] | WP-17, WP-12, WP-41 | Viewport defaults for matrix |
| S3-44 | Design Reviewer: hierarchy and WCAG AA contrast checks | [P] | WP-17, WP-42 | Covered |
| S3-45 | Design Reviewer: severity-tiered findings in user-impact language with screenshots | [P] | WP-17 | Covered |
| S3-46 | Visual QA skills marketplace listings (mcpmarket visual-review-ui-inspection, visual-feedback-loop-eyes) | [S] | WP-17 | Quality unverified |
| S3-47 | visual-feedback-loop: capture, propose, confirm, verify | [S] | WP-17, WP-19 | Four-step loop with human confirm; matches harden loop; add confirm step |
| S3-48 | undeadlist/claude-code-agents (visual diff plus browser QA agents; not inspected) | [U] | WP-90 | Inspect |
| S3-49 | VoltAgent/awesome-design-md: brand-modelled DESIGN.md files | [S] | WP-31, WP-401 | Third-party reconstructions, brand/provenance caution (as S1-74) |
| S3-50 | Adpharm (May 2026) "Claude Design without the AI slop look": aesthetic-family anchoring (mix two) | [S] | WP-16 | Covered in "named aesthetic"; add "blend two families" option |
| S3-51 | Adpharm: DESIGN.md with 9 sections incl. explicit rejection clauses | [S] | WP-31, WP-16 | Section layout; covered. 9-section list to read |
| S3-52 | Adpharm: Anthropic aesthetics-cookbook prompt fragment | [S] | WP-16, WP-90 | Locate primary source (Anthropic cookbook) |
| S3-53 | Adpharm: Goal-Layout-Content-Constraints prompting | [S] | WP-11 | Prompt template for sketch intake; add |
| S3-54 | Adpharm: inline comments/"Tweaks" over re-prompting | [S] | WP-11, WP-12 | Targeted per-element feedback (not whole re-prompt): missing in WP-11; note |
| S3-55 | betterstack.com DESIGN.md explainer | [S] | WP-31 | Low value |
| S3-56 | dev.to AWS builders: AGENTS.md / SKILL.md / DESIGN.md three layers | [S] | WP-71, WP-31 | Layering vs Brad Frost (C4) |
| S3-57 | DESIGN.md originated with Google Stitch (per explainers) | [U] | WP-90 | Verify origin and spec version |
| S3-58 | Parallel variants via git worktrees (developer.upsun.com; understandingdata.com), generic | [S] | WP-12, WP-55, WP-425 | Variant fan-out via worktrees: WP-425; conflicts with ceiling 3-5 (WP-55) if variants ≥ 4 |
| S3-59 | Prototype-as-question (thelongcommit newsletter) | [S] | WP-11, WP-14 | Framing: each prototype answers one question; add "question" field to option files |
| S3-60 | Prove AI Prototype-Driven Development series | [S] | WP-14 | Lifecycle for promote; read |
| S3-61 | Roundup X article x.com/MyWestLord (unread) | [U] | WP-90 | Unread |
| S3-62 | Gap: STYLE.md/brand.md as distinct intent files — nothing found; DESIGN.md de facto | [U] | WP-31 | Negative; keep DESIGN.md-compatible |
| S3-63 | Gap: no source for explore-without-specs then backfill specs/tests and harden lifecycle | [U] | WP-14, WP-19 | Our novelty; hence needs own evaluation (WP-60) |
| S3-64 | Gap: option-board/variant selection: no verified practitioner write-up | [U] | WP-12 | Our design; eval it |
| S3-65 | Gap: visual QA agents mostly marketplace listings; Rauno Freiberg nothing | [U] | WP-17 | Negative; do not rely |
| S3-66 | Per-system claims (Radix, Material, Chakra, Ant, Mantine, Base UI, Spectrum, Primer) not verified; rely on Kaelig survey | [U] | WP-90 | Verify before citing |
| S3-67 | Confidence moderate; repo READMEs fetched through summarizing tool, star counts conflict | [U] | WP-401, WP-90 | Re-fetch raw for items that drive design decisions |

## 1. CONTRADICTIONS

- C1 DESIGN.md value: Atlassian measured DESIGN.md as costliest arm (7.21M vs 3.75M MCP, 4.43M skill, 4.20M none) and component-recreating; Vercel reports 57% fewer failures with design.md (39 vs 91, tiny sample) and S3 treats DESIGN.md as de facto standard. Resolution candidate: different tasks (art direction/brand pages vs product UI components). Adopt as exploration/brand aid, not as component source (WP-31, WP-402).
- C2 CLI vs MCP: Atlassian CLI only 8% faster/8% fewer tokens than MCP; Carbon, Primer, Spotify, Salesforce, Spectrum are MCP-first. Not a real contradiction; deltas small. Do not pick on token savings alone.
- C3 JSON vs Markdown: Indeed claims JSON in MCP saves ~80% tokens; Adobe publishes .md twin per page and Atlassian/Carbon rely on Markdown/llms.txt. Different layers (tool payload vs docs page).
- C4 Layer models differ: Brad Frost (rules -> MCP -> AGENTS.md orchestration) vs dev.to (AGENTS.md / SKILL.md / DESIGN.md) vs Encore (foundation/style/behavior, which is code architecture) vs draft WP-71 "rules / lookup tool / AGENTS.md". Pick one explicitly.
- C5 Tool surface size: Carbon 4 tools vs Primer 20 + 8 tools; no evidence on which performs better.
- C6 "Never claim visual verification from code alone" (Vercel) vs static slop scanners (avoid-ai-design, Hallmark gates) that judge code. Scanners are pre-render checks and must not be reported as visual verification.
- C7 Generated context (Spectrum, deploy-time from source) vs hand-curated (Carbon llms.txt, Vercel exemplars, coverage-gaps). Draft WP-72 favors generation; judgment content (exemplars, gaps) cannot be generated.
- C8 Kaelig headline "almost none ship llms.txt" vs S2 report of Carbon, Spectrum, shadcn, Atlassian publishing llms.txt; system count 20 vs 21.
- C9 Self-reported effects use different baselines: Atlassian 34% faster/16% fewer tokens (skills vs ?) vs 8%/8% (CLI vs MCP); not additive.
- C10 Skills cost: Atlassian skill arm (4.43M) cost more than no context (4.20M) while draft assumes skills reduce cost.
- C11 Directions count: Claude Design "dozen"; draft WP-16 ~4; WP-11 ~3; Anthropic frontend-design: one extreme direction. Define default plus parameter.
- C12 Auto vs human invocation: Fluent sets disable-model-invocation; Vercel root AGENTS.md routes automatically. Choice depends on skill cost/side effects (WP-406).
- C13 Dates: v0 DS 2.0 (Feb 5 vs June 25 2026); Airbnb talk "November 2026" is in the future; taste-skill stars 46k vs 98k.
- C14 Severity scales: P0-P3 (Vercel, WP-53) vs P0-P2 (avoid-ai-design).
- C15 Variant fan-out via worktrees (S3) vs parallel-agent ceiling 3-5 (WP-55) and single-writer rule.

## 2. CLAIMS TO VERIFY before acting (and how)

1. Atlassian DESIGN.md token numbers (7.21M/3.75M/4.43M/4.20M; 2.5MB->80KB): read the 2026-06-15 post; check units, task, n, quality outcome per arm.
2. Atlassian 4.9%/11%/34%/16%/26%/52% and CLI 8%/8%: read both posts; identify baselines; treat as vendor benchmark.
3. Vercel 39 vs 91 failures, 7 scenarios, 200+ runs: read 2026-08-31 post; sample size caveat is theirs.
4. Indeed 80% token / 4,300 prototypes; Spotify 220k+/93%: fetch intodesignsystems.com articles and the talk; seek first-party.
5. Spotify test framework details: no first-party post; ask/lookup talk slides.
6. Kaelig counts (21 systems, ~200 affordances, 165 techniques) and the llms.txt 404 claim: clone repo, count from dataset, curl llms.txt URLs.
7. Primer tool counts (20/8), lint_css "REQUIRED FINAL STEP": inspect primer/react-mcp repos directly.
8. Fluent skills and disable-model-invocation: inspect microsoft/fluentui .agents/skills and discussion #35732.
9. Salesforce afv-skills and slds-linter: check npm and developer.salesforce.com pages.
10. Spectrum /.well-known/skills and rubric weights: fetch react-spectrum.adobe.com/ai and the skills.
11. Hallmark 21 themes/57 gates, avoid-ai-design 67 patterns, taste-skill star count: clone repos; run scanner on a sample.
12. Pocock prototype skill details: read repo SKILL.md raw.
13. TechNickAI Design Reviewer: read PR 4 diff.
14. Shopify Dispatch different-model verification; Airbnb harness; Airbnb 12+ MCP/80%/64%: unopened/403; fetch originals or discard.
15. v0 DS 2.0 launch date and v0.json max 3 sources: read v0.app/docs/design-systems-2.
16. DESIGN.md origin (Google Stitch) and spec version: read primary spec.
17. Carbon "never from training knowledge" rule and 24KB/12 refs: read skill file in Carbon repo.
18. Figma use_figma, Anthropic Claude Design details: product pages only; verify before depending.
19. Atlassian demo 4-5 days -> 20 min / 1,381 LOC: marketing; do not use as benchmark.
20. Shopify River stats: acceptable as reference; not design-specific.

## 3. PROPOSED NEW WPs (deduplicated)

- WP-401 Evidence-quality convention for research outputs: tag [P]/[S]/[U]/[I], flag vendor self-benchmarks, small n, conflicting dates/counts; add to vanguard research-report guidance (shared/references/research) and use in WP-90. Covers S1-03..08, S1-13, S1-76, S2-21, S2-84, S3-29, S3-67.
- WP-402 Design-context delivery benchmark: run own paired test of no-context vs skill vs MCP vs CLI vs DESIGN.md on our consumer repo tasks, measuring tokens, quality and component reuse; extend mason:evaluate (WP-60) with token-cost metric. Resolves C1, C2, C3, C10.
- WP-403 Typed schema-as-canonical source: one co-located structured source (TypeScript/JSON schema) for components/tokens/lint rules from which DESIGN.md, llms.txt, MCP and skills are generated; target shared/references/design plus muse docs; builds on WP-72/WP-74.
- WP-404 Deterministic weighted UI audit rubric (Spectrum spectrum-audit): severity-weighted scoring of a UI against explicit checks, numeric result; target muse (new audit-ui skill) or ranger hazard pack; complements WP-17/WP-42.
- WP-405 Design-system conformance scoring harness (Spotify): score generated UI against real components via lint errors, similarity and visual diff; target mason:evaluate fixtures plus shared/references/evaluation.
- WP-406 Human-trigger-only skill policy: criteria for flagging skills disable-model-invocation (costly visual tests, side effects) and how Codex counterpart expresses it; target shared/constitution.md plus mason:audit-plugin check.
- WP-407 Agent trust tiers and capped outputs: tiers by capability (read-only, issue-only, branch-write), capped safe-outputs, public-channel-only scoping (Primer, River); target shared/constitution.md and WP-55.
- WP-408 Skill distribution and discovery: npm packaging (@salesforce/afv-skills), /.well-known/skills URL, mirrored .agents/skills and .claude/skills; target docs/adr plus harnesses/codex (extends WP-70/72).
- WP-409 Coercion-technique reference: catalog from Kaelig 165 techniques (prohibitions, tool-gating, validation loops, exemplar pairs, Incorrect/Correct pairs, named prohibitions, fixed ordered checklists, never-from-memory rules) with when-to-use; target shared/references/prompting; feeds WP-16, WP-31, WP-64, WP-67.
- WP-411 Introspection and dry-run conventions: `info --json` and `add --dry-run` style capability for recon and implement (shadcn), validation tool in MCP (Shopify Dev MCP), final-lint-step rule (Primer); target smith:recon and shared/references/tooling/cli.md.
- WP-412 Rule promotion ladder: guidance text -> exemplar pair -> deterministic lint -> eval fixture, with human acceptance per step and multi-source threshold; target shared/references/design plus WP-13.
- WP-413 Authority and precedence order in constitution/router: user goals > verified evidence > repo guidance > accepted decisions > adjacent patterns > heuristics; docs over existing code (Fluent); ADR-backed review rules cite decision (Primer); target shared/constitution.md and muse/sentinel gates.
- WP-414 Feedback harvest loop: periodic collection of signals (PR comments, Slack, screenshots) into pending rule candidates, with real-use telemetry (Vercel @design-agent, River transcript learning); target shared/references/design plus WP-13.
- WP-418 Ingestion preview-and-approve: when extracting a design system or intent file (WP-32/35), build a starter preview and require human approval, re-validate on update, cap reference sources (v0); target muse.
- WP-421 Cross-model verification option: allow verifier/gate on a different model than producer (Shopify Dispatch); target mason:evaluate and shared constitution tier rules; verify source first.
- WP-422 Judge calibration step: calibrate LLM judges against human labels (Sidekick kappa 0.02 -> 0.61) before using them in evals or gates; target mason:evaluate.
- WP-425 Variant fan-out via worktrees: parallel option generation in isolated worktrees within the WP-55 ceiling, with merge/discard rules; target muse sketch skill and navigator parallel guidance.
- WP-427 Grill-before-sketch: structured interrogation step ahead of prototype (Pocock grill-me then prototype then PRD/TDD); target weaver:clarify-requirement/muse sketch intake; reconcile with one-question-per-invocation.
- WP-437 Motion and typography reference packs for design review: easing/duration rules (Emil Kowalski), typography and layout rules (Jakub Krehel), fixed review format; target shared/references/design plus WP-17.
- WP-440 Instruction-file validity linter: check llms.txt/AGENTS.md/MCP URLs resolve (not 404/HTML shell), line/size budgets (Carbon 69 lines, 32 KiB), no dangling references; extends WP-04.
- WP-444 Migrate mode: bulk, per-file stepwise migration (Salesforce slds2-migrate, Spectrum v3->S2, Airbnb test migration state machine) with validate/retry loops, resumable state; target smith (new skill) or router (WP-18).

Dispositions without WP (evidence-based): S1-56, S1-70, S1-71, S1-72, S1-73, S2-16, S2-19, S2-60, S2-61, S2-65, S2-76, S2-77, S2-78.
