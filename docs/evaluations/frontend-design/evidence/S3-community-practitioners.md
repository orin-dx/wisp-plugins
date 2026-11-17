# S3 Community practitioners (researched 2026-10-17)
Confidence: moderate. Many items verified via repo READMEs fetched through a summarizing tool (not raw); star counts conflicted between sources.

## Primary sources (repo/official)
- State of AI in Design Systems, Kaelig Deloumeau-Prigent (Jul 2026, CC-BY): https://github.com/kaelig/state-of-ai-in-design-systems ; site https://state-of-ai-in-design-systems.netlify.app/systems/shadcn-ui . 20-21 OSS systems, ~200 affordances, 165 coercion techniques (prohibitions, tool-gating, validation loops, exemplar pairs). Headline claim: almost none ship llms.txt/Code Connect/agent instruction files; some "llms.txt" return 404/HTML shells (from search snippet; not independently verified).
- shadcn/ui: bundled MCP (`npx shadcn@latest mcp`), Agent Skill with Critical Rules + Incorrect/Correct pairs, curated llms.txt (https://ui.shadcn.com/llms.txt), CLI `info --json`/`add --dry-run`, eval suite for skill rules. Registry MCP announcement: https://x.com/shadcn/status/1917597228513853603
- Hallmark (Nutlope): https://github.com/Nutlope/hallmark - 21 themes, macrostructure selection, 57 slop-test gates, pre-emit self-critique; verbs build/audit/redesign/study. No screenshot QA documented.
- avoid-ai-design (funboy322): https://github.com/funboy322/avoid-ai-design - zero-dep scanner `detect.mjs`, 67 deterministic patterns, P0/P1/P2, JSON + exit codes for CI; names "second-order slop" (cream+terracotta, mono-chrome, numbered 01/02/03); generates DESIGN.md for multi-page consistency.
- taste-skill (Leonxlnx): https://github.com/Leonxlnx/taste-skill - 9 skills; dials DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY; brief inference, redesign-audit, pre-flight check; imagegen skill produces reference images only. Stars reported 46k vs 98k in different sources: unverified.
- Koomook/claude-frontend-skills: https://github.com/Koomook/claude-frontend-skills - single distinctive-frontend skill (typography extremes, cultural palettes, motion, backgrounds); derivative of Anthropic frontend-design.
- Anthropic frontend-design skill (baseline): 4 pre-CSS questions (purpose, tone, constraints, differentiation), commit to extreme direction, bans Inter/Roboto/Arial. Aggregator: https://agenticskills.io/skills/frontend-design (secondary).
- Matt Pocock skills: https://github.com/mattpocock/skills - `prototype` skill: throwaway HTML or multiple UI variations toggled from one route; sits between grill-me and TDD/PRD. Secondary: https://deepwiki.com/mattpocock/skills/3.5-prototyping (429'd; got info from repo fetch).
- Emil Kowalski design-engineering skill (animation easing/duration, fixed review format); Jakub Krehel Typography + Better Layout skills; aggregated at https://craftwork.design/skills (secondary index). https://note.com/ai_driven/n/n2f8718394117 (secondary deep dive).
- TechNickAI/ai-coding-config Design Reviewer agent: https://github.com/TechNickAI/ai-coding-config/pull/4/files - Playwright at 1440/768/375, hierarchy, a11y (WCAG AA contrast), severity-tiered findings in user-impact language with screenshots.
- Visual QA skills (marketplace listings, secondary): https://mcpmarket.com/tools/skills/visual-review-ui-inspection ; https://mcpmarket.com/tools/skills/visual-feedback-loop-eyes (capture -> propose -> confirm -> verify). Also https://github.com/undeadlist/claude-code-agents (visual diff + browser QA agents; not inspected).
- VoltAgent/awesome-design-md: https://github.com/voltagent/awesome-design-md - brand-modelled DESIGN.md files.

## Secondary
- Adpharm, "Claude Design without the AI slop look" (May 2026): https://www.theadpharm.com/insights/claude-design-without-the-ai-slop-look - aesthetic-family anchoring (mix two), DESIGN.md with 9 sections incl. explicit rejection clauses, Anthropic aesthetics-cookbook prompt fragment, Goal-Layout-Content-Constraints prompting, inline comments/"Tweaks" over re-prompting.
- DESIGN.md explainers: https://betterstack.com/community/guides/ai/design-md-ai/ ; https://dev.to/aws-builders/agentsmd-skillmd-designmd-how-ai-instructions-split-into-three-layers-d0g (AGENTS/SKILL/DESIGN layering). DESIGN.md originated with Google Stitch (per explainers).
- Parallel variants via worktrees: https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents ; https://understandingdata.com/posts/git-worktrees-parallel-dev/ (generic; not design-specific).
- Prototype-as-question: https://newsletter.thelongcommit.com/p/the-prototype-is-a-question-not-a ; Prove AI PDD series https://proveai.com/blog/prototype-driven-development-part-1-a-new-approach-to-building-software
- Roundup (X article, unread): https://x.com/MyWestLord/article/2068064010600108267

## Gaps / thin
- STYLE.md / brand.md as distinct intent files: nothing found; DESIGN.md is the de facto convention. Intent also lives in SKILL.md and CLAUDE.md rules (not found as documented practice).
- No source found describing an explicit "explore without specs, then backfill specs/tests and harden" lifecycle for design; closest is Pocock's prototype (throwaway-by-design) and prototype-driven-development essays.
- Option-board/variant-selection for design: only generic worktree posts and Pocock's single-route variants; no named design-engineer practitioner write-up verified.
- Visual QA agents are mostly marketplace listings; quality unverified. Rauno Freiberg: nothing found.
- Per-system claims (Radix, Material, Chakra, Ant, Mantine, Base UI, Spectrum, Primer) not individually verified; rely on Kaelig survey.
