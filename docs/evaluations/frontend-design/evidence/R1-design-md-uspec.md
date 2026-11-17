# R1: Design intent in agent-readable files (researched 2026-10-17)

## DESIGN.md
- Introduced by Google Labs with Stitch's March 2026 relaunch; draft spec open-sourced April 2026 (Apache-2.0, alpha). https://www.designwhine.com/what-the-hell-is-google-stitchs-design-md/ ; https://github.com/google-labs-code/design.md
- Format: Markdown + YAML front matter. Front matter: version, name, description, tokens (colors, typography, rounded, spacing, components); `{path.to.token}` references; CSS colors (hex/oklch), dimensions. Body: fixed ## section order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts (prose = rationale/visual intent).
- CLI `npx @google/design.md lint | diff | export` (export: json-tailwind, css-tailwind, dtcg). 11 lint rules: broken refs, missing primary, WCAG AA contrast, orphan tokens, section order, unknown keys.
- Consumption: dropped in repo root; agents (Claude Code, Cursor, Gemini CLI, Antigravity) just read it as a file. No special protocol (secondary sources: https://mindwiredai.com/2026/04/23/design-md-is-now-open-source-googles-new-file-format-that-makes-ai-build-your-brand-correctly/). Unverified: any first-party per-agent integration docs.
- Public examples: https://github.com/VoltAgent/awesome-design-md (MIT; 84 brands; community variant with 9 sections: Visual Theme & Atmosphere, Color roles, Typography, Component Stylings with states, Layout, Depth, Do/Don't, Responsive, Agent Prompt Guide; ships preview.html catalogs). Values scraped from public CSS, so they are inferred, not authoritative.
- Critique: "openness is the beginning of interoperability, not proof of it"; still early.

## Uber uSpec
- Uber blog: https://www.uber.com/us/en/blog/automate-design-specs/ ; docs https://docs.uspec.design/ ; repo https://github.com/redongreen/uSpec (found via docs llms.txt; NOT an Uber-org repo; license NOT verified).
- Direction is Figma -> spec, the reverse of DESIGN.md. Input: Figma component (link, or newer "uSpec Extract" Figma plugin producing _base.json) + optional human context (states, platform behavior). Agents: Cursor (blog), Cursor/Claude Code/Codex (docs).
- Architecture: (1) agent skills = instruction files with platform a11y reference tables (VoiceOver/TalkBack/ARIA) so the agent selects from documented APIs rather than guessing; (2) Figma Console MCP (Southleft, open source, local WebSocket) crawls component tree, variants, variables, tokens; (3) LLM does semantic judgment (a11y semantics, token mapping, slot composition); (4) programmatic rendering into Figma from library templates (anatomy markers, tables).
- Outputs: spec pages in Figma: anatomy, API, properties, color annotation (token per state), structure (dimensions/spacing/density), screen reader (3 platforms), motion (from After Effects). Docs also describe "Component.MD": canonical schema-valid JSON contract + concise Markdown implementation guide, rendered back to Figma by optional create-* skills. Stack: 7 implementations (UIKit, SwiftUI, Android XML/Compose, React, Go, SDUI).
- Roadmap per Uber: drift detection, code-to-spec. Local-only processing.
- Key lesson: visual intent stays in Figma (source of truth); the text contract is derived from it by deterministic extraction, with LLM only for semantics.

## Other approaches
- Figma MCP "design system rules" skill: generates CLAUDE.md / AGENTS.md / .cursor/rules/figma-design-system.mdc encoding conventions (tokens, component reuse, layout). Lightweight, prose rules; visual intent comes from Figma frames via MCP at implement time. https://developers.figma.com/docs/figma-mcp-server/skill-create-design-system-rules
- W3C DTCG tokens: first stable format 2025.10 (Oct 28 2025), JSON, themes, Display P3/Oklch, aliases. Rigid and machine-checkable, but only atomic values, no composition or intent. https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/ ; https://www.designtokens.org/
- Storybook MCP: component manifests (props types, stories, JSDoc, tests) exposed via tools docs-list, docs-show, get-storybook-story-instructions, test-run. Stories are executable examples (visual intent as rendered states); fetched docs did not say how visual regression is exposed (unverified). https://storybook.js.org/docs/ai
- Spec Kit (GitHub, MIT, ~142k stars): constitution/specify/plan/tasks pipeline, also bug-fix and idea-assessment entry points; text-first, no native visual model. https://github.com/github/spec-kit . Kiro: requirements/design/tasks; Kiro design agent claims browser-verified UI loop (vendor-ish source, unverified). OpenSpec: light delta-based change specs (~250 vs ~800 lines per change, per Augment roundup, secondary); common complaint: specs drift and don't self-update. https://codemyspec.com/blog/kiro-vs-openspec
- Screenshot->spec tools (dsh-ui-spec plugin): deterministic geometry/palette measurement plus optional vision model. https://open-design.ai/plugins/dsh-ui-spec/ (low-confidence source).

## Lessons for Wisp (spec@1 text-only, too rigid for exploration)
1. Split artifacts: a lightweight, human-authored design-intent file (DESIGN.md-style: tokens in front matter + prose rationale, Do/Don't) separate from the falsifiable behavior spec@1. Intent is prose-and-reference, not testable criteria.
2. Let spec@1 criteria reference tokens/intent by name ({token.path}) and by visual reference (Figma node, Storybook story id, screenshot path) instead of describing pixels in text. Visual evidence is an attachment/oracle, not a proposition.
3. Tiering: exploratory mode = DESIGN.md + references, no gate; promote to spec@1 only for behavior/a11y once stable. uSpec's extract-then-compile pattern shows deterministic extraction should feed the LLM, not the reverse.
4. Verification: tokens lint (contrast, broken refs) is cheap and deterministic (design.md lint); stories as executable examples; screenshot diff for visual claims, flagged as coverage gap when no tooling.
5. Drift: both Uber and OpenSpec critics name drift as the unsolved problem; Wisp already has spec-drift, extend it to design-intent files.
6. Treat scraped/community DESIGN.md as inferred, not authoritative.

## Could not verify
uSpec license; whether uSpec repo is officially Uber-owned; exact DESIGN.md per-agent integration docs; Storybook visual-test exposure via MCP; Kiro UI claims. Several facts come from LLM-summarized page fetches.
