# S2: AI agents in design-system / front-end workflows (researched 2026-10-17)

Source quality: [P]=primary/first-party, [S]=secondary/well-sourced aggregator, [M]=marketing/third-party.
Best single index: Kaelig Deloumeau-Prigent, "State of AI in Design Systems" (July 2026, CC-BY, audits public repos) [S, repo-derived]: https://state-of-ai-in-design-systems.netlify.app/llms.txt (21 systems; does NOT cover Netflix, Duolingo, Linear, Stripe, Notion, Encore).

## IBM Carbon
- Remote MCP server mcp.carbondesignsystem.com/mcp, 4 tools (docs_search, code_search, get_charts, labs_search), IBMid OAuth, closed source. Docs: https://carbondesignsystem.com/developing/carbon-mcp/onboarding-and-setup/ [P]
- carbon-builder agent skill (24KB, 12 lazy-loaded reference docs, hard rule "never generate Carbon code from training knowledge alone") [S via report]: https://state-of-ai-in-design-systems.netlify.app/systems/carbon-design-system
- Hand-curated llms.txt (carbondesignsystem.com/llms.txt); root AGENTS.md of 69 lines used as a router ("as short as possible. More length = more tokens"), per-package AGENTS.md; Bob triage bot prompt versioned in .github/prompts/bob-bug-triage.md [S]
- Works in IBM Bob, Cursor, Claude Code, VS Code Copilot. "Carbon for AI: Scaling New Ways of Working" (Medium/carbondesign) exists but returned 403; unread.
- Verification: nothing public beyond MCP-first rule. Nothing found on IBM Design Studio internal use.

## Spotify Encore
- MCP server exposing rules/tokens/component specs; machine-readable docs; 3-layer architecture (foundation / style / behavior; headless on React Aria + Base UI). Speakers Victoria Tholerus, Aleksander Djordjevic. [S: Into Design Systems writeup of talk] https://www.intodesignsystems.com/blog/how-spotify-design-system-ai-ready
- Test framework scoring AI output vs real Encore components: lint errors, similarity scores, visual output (strongest verification pattern found). Claims 220k+ style uses, 93% dev satisfaction (via https://www.intodesignsystems.com/blog/design-system-not-ready-for-ai-agents) [S]. No first-party Spotify Engineering post found.

## GitHub Primer
- @primer/mcp (20 tools; lint_css tool described as "REQUIRED FINAL STEP"), @primer/brand-mcp (8 tools), Storybook MCP at localhost:6006/mcp, 52 Figma Code Connect files, .github/copilot-instructions.md + 5 path-scoped instructions (component-review backed by ADRs) + 7 skills + 2 custom agents (modular-ds-implementer/reviewer), gh-aw issue-triage with capped safe-outputs. No llms.txt/AGENTS.md in primer/react; AGENTS.md in primer/primitives with mandatory lint/format/test/build. [S, links to primary repos] https://state-of-ai-in-design-systems.netlify.app/systems/primer-github ; docs https://primer.style/product/getting-started/foundations/mcp/ [P]
- Trust tiers: agents restricted to issue creation (Jan Six, via Into Design Systems).
- GitHub Spark (GitHub Next): NL->app exploration tool; no public detail found on its design-system use. Exploration tool, not hardening.

## Microsoft Fluent UI
- AGENTS.md ("source of truth, not existing code", 5 never-violate rules), CLAUDE.md redirect, 9 skills mirrored in .agents/skills & .claude/skills incl. /visual-test (per-component Storybook + Playwright screenshots) and /lint-check (fix, re-run, repeat); skills use disable-model-invocation (human-triggered); copilot-setup-steps.yml. Internal React MCP exists, unreleased (discussion #35732). Blazor MCP public. [S] https://state-of-ai-in-design-systems.netlify.app/systems/fluent-ui-microsoft ; primary: https://github.com/microsoft/fluentui/discussions/35732

## Salesforce SLDS
- Knowledge shipped as npm skills (@salesforce/afv-skills: slds-apply, slds-validate, slds2-migrate) + @salesforce/mcp lwc-experts tools + @salesforce-ux/slds-linter closing a deterministic validate loop. Starter kit: AGENTS.md routing, .builderrules 5-step checklist, CLAUDE.md one-line import. Figma->LWC MCP tool (beta). No llms.txt. 
- Primary: https://developer.salesforce.com/docs/platform/slds-linter/guide/get-started-linter-AI-skills.html ; https://developer.salesforce.com/docs/platform/lwc/guide/mcp-design.html ; https://developer.salesforce.com/blogs/2025/10/vibe-code-lightning-web-components-with-salesforce-dx-mcp ; summary [S] https://state-of-ai-in-design-systems.netlify.app/systems/salesforce-slds

## Adobe Spectrum
- React Spectrum S2: llms.txt + .md twin per page + "Copy for LLM"; @react-spectrum/mcp; 3 skills at /.well-known/skills (build, spectrum-audit with deterministic severity-weighted rubric, v3->S2 migrate); agent context GENERATED from docs source at deploy. Named prohibitions (no Tailwind/shadcn, no UNSAFE_*). Compile-time `style` macro as a verifier. [P] https://react-spectrum.adobe.com/ai ; [S] https://state-of-ai-in-design-systems.netlify.app/systems/react-spectrum-s2
- Spectrum Design Data (tokens + component schemas, Rust core, CLI/wasm/MCP): https://opensource.adobe.com/spectrum-design-data/ai/ [P]. Firefly: marketing only, skipped.

## Netflix Hawkins
- Public: 2022-era Hawkins blog (https://netflixtechblog.com/hawkins-diving-into-the-reasoning-behind-our-design-system-964a7357547) predates agents. Only AI evidence is job postings: "Hawkins Consumer ... evolving into a design intelligence layer", "centralize agentic context that Commerce, Games, and Member extend from", encode voice/tone as machine-readable rules. https://jobs.intodesignsystems.com/jobs/netflix-systems-designer-design-foundations-1pp919 [job post = weak signal]. No engineering post, MCP, or repo found.

## Figma
- use_figma tool lets agents write to canvas bound to design system; /figma-use skill + custom markdown skills encode team conventions; says Figma teams use it internally but gives no detail. https://www.figma.com/blog/the-figma-canvas-is-now-open-to-agents/ [P/marketing-ish]
- MCP + Code Connect + variable code syntax + annotations + "design system rules generation" (scan codebase -> rules file). https://www.figma.com/blog/design-systems-ai-mcp/ [P]

## Anthropic
- Product Design team: feed Figma to Claude Code in autonomous write/test/iterate loop; GitHub Actions PR comments; use Claude to map error states/edge cases in design phase. https://claude.com/blog/how-anthropic-teams-use-claude-code [P]; research: https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic [P]
- Claude Design (Anthropic Labs): builds a design system by reading codebase + design files, "a dozen directions" exploration, handoff bundle to Claude Code. https://www.anthropic.com/news/claude-design-anthropic-labs [P, product announcement]. Internal verification details not public.

## Pinterest, Intuit, Duolingo, Linear, Stripe, Notion
- Pinterest: public MCP ecosystem post is about data/infra tools (Presto, Spark, Airflow), registry + auth; nothing on Gestalt. https://medium.com/pinterest-engineering/building-an-mcp-ecosystem-at-pinterest-d881eb4c16f1 [P]
- Intuit, Duolingo: nothing public found.
- Linear/Stripe/Notion: only third-party "DESIGN.md" extractions (designmd.directory, open-design, better-design); not first-party. Useful as a pattern only.

## Cross-cutting patterns
- Indeed (Diana Wolosin): JSON over Markdown in MCP = ~80% fewer tokens, 4,300 prototypes in 4 months [S via https://www.intodesignsystems.com/blog/design-system-not-ready-for-ai-agents].
- Brad Frost three-layer: always-on rules -> MCP on-demand -> AGENTS.md orchestration.
