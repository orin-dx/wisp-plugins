# R2: Figma + coding agents (researched 2026-10-17)

## Official MCP server (verified via fetch)
- Tools ref: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
  - Read: get_design_context (React+Tailwind default, customizable via prompt), get_metadata (sparse XML outline), get_screenshot, get_variable_defs, download_assets (remote only), get_motion_context, get_figjam
  - Write: use_figma (skills figma-use, -figjam, -slides, figma-spec), generate_figma_design (remote), create_new_file, upload_assets, generate_diagram, html_to_figma, generate_image, send_code_to_figma
  - Design system / Code Connect: get_libraries, search_design_system (remote), get_code_connect_map, add_code_connect_map, get_code_connect_suggestions, get_context_for_code_connect, send_code_connect_mappings
  - Also generative plugins, shaders, Weave tools. MCP prompt: create_design_system_rules (generates agent rules file for stack/design system).
- Remote https://mcp.figma.com/mcp (recommended) vs desktop http://127.0.0.1:3845/mcp (org/enterprise) - https://github.com/figma/mcp-server-guide
  - UNVERIFIED/CONFLICT: a search summary said get_variable_defs is desktop-only; the official table says not remote-only. Check before relying.
- Guide guidance: rules files = "onboarding notes", structure Figma w/ components, variables, semantic names, Auto Layout, annotations; break large selections up; Starter plan ~6 calls/month, paid seats per-minute REST Tier 1 limits. Failures: poor file structure, vague prompts, oversized selections, not triggering right tool. https://github.com/figma/mcp-server-guide
- Write to canvas: https://www.figma.com/blog/the-figma-canvas-is-now-open-to-agents/ ; use_figma builds with real components/variables/auto layout; skills = markdown instruction sets (9 examples e.g. /figma-generate-library, /apply-design-system); free in beta, later usage-based; nondeterministic; roadmap: images, custom fonts.
- Code to canvas: https://developers.figma.com/docs/figma-mcp-server/code-to-canvas/ ; generate_figma_design captures running browser UI as FLAT layers, no library connection; auto-binds matching variables if target file has library; paid plans (Starter+), edit access.

## Code Connect
- https://www.figma.com/blog/the-benefits-of-code-connect-in-mcp/ : without it agent fabricates components (Coinbase: stepper from progress bars). Median with CC: quality +1 (2->3 on 1-4 Likert), tokens -29.5%, duration -19.6%; scales with coverage. (A search snippet quoted different Coinbase numbers 11.5%/22.3%/22.5% - unverified, different source.)
- Needs ongoing manual maintenance (ByteByteGo). CC UI beta/GA mapping via GitHub (forum + secondary source; unverified GA date).

## Figma Make
- Prompt-to-app (React+TS+Tailwind+Vite), zip export, GitHub push, can connect codebase and open PR (secondary sources, partly marketing): https://www.figma.com/solutions/ai-engineering-handoff-tool/ ; https://www.banani.co/blog/figma-make-tutorial . Unverified depth.

## Tokens
- Pipeline: Figma variables -> DTCG JSON -> Style Dictionary -> CSS; Tokens Studio for bidirectional git sync (secondary: https://atomize.tools/blog/figma-design-tokens-vibe-coding/). Unverified in detail.

## Write-ups
- LogRocket https://blog.logrocket.com/ux-design/design-to-code-with-figma-mcp/ : screenshots alone drift; messy layers hurt; no CC => regenerates components; output needed manual import/responsive fixes; exported token JSON helped.
- ByteByteGo https://blog.bytebytego.com/p/figma-design-to-code-code-to-design : 25k default MCP response cap; scan-first (get_metadata) then zoom in; each handoff lossy (logic/state lost both ways); capture walks DOM computed styles; agent tools vary.
- hipsquare https://blog.hipsquare.io/posts/2026-05-10-figma-playwright-mcp : Figma MCP + Playwright screenshot loop; claims ~50% time reduction on component sets (self-reported, small).
- Design Systems Collective (403 on fetch; snippet only) https://www.designsystemscollective.com/the-hidden-cost-of-figma-mcp-roundtripping-and-the-sustainable-model-i-use-instead-142d8e782a51 : token tax of roundtripping. UNVERIFIED content.
- Code-first: https://medium.com/@garimasadhnani/stop-making-figma-prototypes-how-i-build-live-ui-with-claude-code-and-mcps-fd5379f9072e ; https://medium.com/@karthikmulugu/i-let-claude-design-my-entire-website-using-shadcn-magic-ui-and-playwright-mcp-heres-what-ad24860b705b ; https://mowgli.ai/blog/claude-code-ui-design-workflow (snippets only, not read). Loop: implement -> screenshot -> diff list -> fix.
- Community skills: figma/mcp-server-guide figma-implement-design (https://claudemarketplaces.com/skills/figma/mcp-server-guide/figma-implement-design), figma-use, southleft/figma-console-mcp-skills (https://github.com/southleft/figma-console-mcp-skills), tempad-dev figma-design-to-code.

## Wisp implications (my inference)
Integration points: (1) muse spec inputs: design reference as an optional typed artifact (design-source) w/ tokens/components/states; (2) smith verification: visual evidence step (screenshot + a11y snapshot) as a generic oracle, not Figma-specific; (3) token/component mapping check (tokens used vs hardcoded; existing component reuse = Code Connect analogue); (4) drift check (spec-drift for visual); (5) rules file generation.
Figma-optional: define design-source@1 with `kind: figma|screenshot|html|description|none`, normalize to {tokens, components, states, reference_images}. Figma adapter uses MCP if present; otherwise browser-screenshot loop against spec criteria. Capability-detect MCP tools, never require. Keep context cost low: metadata-first, per-node fetch. Treat Figma output as reference not truth (over-literal, absolute layout). Don't depend on write-to-canvas (beta, pricing changing).
