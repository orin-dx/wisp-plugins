# R4: Verifying and hardening agent-built front-end work (researched 2026-10-17)

Confidence tags: [P] primary/vendor doc fetched; [S] secondary summary from search snippet only (not opened); [U] unverified/inferred.

## 1. Visual verification loops
- Anthropic Claude Code best practices [P]: "Give Claude a way to verify its work"; "Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal." Example for UI: paste a design, "take a screenshot of the result and compare it to the original. list differences and fix them". Wants evidence (screenshot, command output) not assertion. Also: Stop hook as deterministic gate; a fresh-context verification subagent so "the agent doing the work isn't the one grading it"; reviewers prompted for gaps over-report, so restrict to correctness/stated requirements. Failure pattern named: "trust-then-verify gap... If you can't verify it, don't ship it." https://code.claude.com/docs/en/best-practices
- Same doc on explore vs plan [P]: plan mode adds overhead; "If you could describe the diff in one sentence, skip the plan"; "Sometimes you should skip planning ... because the task is exploratory." Suggests an interview -> SPEC.md -> fresh session to execute; best specs are self-contained, state out of scope, and "end with an end-to-end verification step".
- Playwright MCP [S]: accessibility-snapshot (text) is cheaper than screenshots (~1/4 tokens claimed); hybrid use. Screenshot catches blank regions, CSS collisions, narrow-viewport breaks, contrast, overflow, wrong data bound. https://playwright.dev/docs/getting-started-mcp ; https://qaskills.sh/blog/claude-code-screenshot-frontend-verification-mcp ; https://codex.danielvaughan.com/2026/08/14/codex-cli-playwright-mcp-browser-automation-accessibility-snapshots-testing/ (GitHub Copilot coding agent has Playwright MCP preconfigured [S]).
- Chrome DevTools for agents [S, official domain, snippet only]: agents verify via screenshots, console, and a `lighthouse_audit` tool (a11y/SEO/best-practices, mobile/desktop, navigation/snapshot) against localhost or file://. https://developer.chrome.com/docs/devtools/agents ; https://developer.chrome.com/docs/devtools/agents/use-cases/lighthouse-audit
- Cursor [S]: browser tool + Design Mode that hands the agent selected element code, applied CSS, layout, screenshots; lesson: visual evidence as a first-class harness artifact. https://cursor.com/docs/agent/tools/browser ; https://cursor.com/changelog/design-mode-improvements
- Anthropic frontend-design plugin [S]: steers against generic "AI slop" aesthetics (aesthetic direction up front). https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

## 2. Storybook / visual regression
- Storybook MCP (addon-mcp, Storybook 10.3+) [P]: Development toolset (story previews, interaction tests), Docs toolset (component manifest, props), Testing toolset (`run-story-tests` returns results incl. a11y violations; "self-healing loop"). Caveats: docs toolset needs a components manifest (not all frameworks); "Agents require explicit instructions to avoid hallucinating undocumented properties". https://storybook.js.org/docs/ai/mcp/overview
- Chromatic (Storybook team, hosted visual diffs + Storybook MCP), Percy (AI Visual Review Agent filters false positives), Lost Pixel (OSS, Playwright screenshots of stories/pages, baselines in repo, GitHub Action) [S]. https://www.augmentcode.com/guides/visual-regression-testing-ai-generated-uis ; https://momentic.ai/blog/best-visual-regression-testing-tools ; https://percy.io/blog/ai-visual-testing-tools
- Key limitation [U/inferred, consistent with sources]: regression tools diff against a baseline; they confirm "unchanged", not "correct". First-time agent output has no baseline, so a human or a rubric must approve the baseline.

## 3. Automated a11y
- Deque study: axe-core fully covers ~57% of issues by volume (2,000+ audits, 13k pages); remainder needs manual/guided testing [S, official Deque]. https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues
- Practical pattern: axe via Storybook a11y addon / Playwright, Lighthouse via DevTools MCP, plus explicit probes (computed contrast, target size >=24px per WCAG 2.2 SC 2.5.8 [U: not fetched], focus order via keyboard-driven Playwright run). Absence of axe violations is not evidence of accessibility; gate should report "automated-only" scope.

## 4. Design-token linting
- Stylelint (e.g. stylelint-declaration-strict-value) fails raw hex/rgb/hsl outside the token sheet; AI "hardcodes the resolved value instead of referencing the semantic token" [S]. https://medium.com/@barshaya97_76274/design-tokens-enforcement-977310b2788e ; https://www.alwaystwisted.com/articles/where-to-lint-design-tokens ; Atlassian token usage guide https://atlassian.design/tokens/use-tokens-in-code/ [S]; "State of AI in Design Systems" coercion techniques https://state-of-ai-in-design-systems.netlify.app/techniques [S, not read].
- Pattern: lint (static) + render (visual) are both needed; lint passes can still render wrong.

## 5. Vibe coding -> production hardening
- Consensus [S]: keep UI/product shape, rebuild foundations; first step is characterization tests pinning current behavior, then refactor, then harden auth/data/integrations. Common failures: interfaces wired only to local state, calls to nonexistent endpoints, saves that don't persist. https://wavect.io/software-development-guide/vibe-coded-prototype-to-production/ ; https://addjam.com/blog/2026-01-12/from-vibe-code-to-production/ ; https://www.vibengineer.io/blog/vibe-coded-prototype-to-production
- "Vibe-prototype is your PRD, not your first product version" (Product School/Reforge-style prototype-first) [S]. https://productschool.com/blog/artificial-intelligence/ai-prototyping ; https://www.reforge.com/blog/ai-prototyping-product-development
- Spec-first vs code-first: code-first suits uncertain outcomes; "the specification emerges from lessons learned" [S]. https://www.kinde.com/learn/ai-for-software-engineering/best-practice/spec-first-vs-code-first-in-ai-development/

## 6. Spec-driven development in practice
- Böckeler / Martin Fowler site, Kiro, Spec Kit, Tessl [P via fetch of sdd-3-tools]: Kiro turned a small bug into 4 user stories / 16 acceptance criteria ("sledgehammer to crack a nut"); Spec Kit produced repetitive markdown "repetitive with each other and with the code", review fatigue ("I'd rather review code than all these markdown files"); agents "frequently" ignore instructions or overreach; Tessl showed non-determinism even from detailed specs; spec-as-source risks MDD's "inflexibility and non-determinism"; unclear functional vs technical boundary. https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- Nothing checks code matches spec; research step catalogued classes then agent regenerated duplicates [S via search summary of same article].
- Drift: HN practitioner "specs keep drifting ... duplication and contradictions"; Kiro-style specs treated as launch docs that drift once generation starts [S]. OpenSpec: current specs/ separated from changes/ deltas, brownfield-first, per-change scope reduces churn [S]. https://github.com/Fission-AI/OpenSpec ; https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md ; https://www.augmentcode.com/guides/spec-driven-development-brownfield-codebases ; https://zenn.dev/cbmrham/articles/202601-spec-driven-development-skepticism?locale=en
- When specs help: multi-file, uncertain-approach, well-bounded behavior with checkable outcomes (Anthropic: self-contained, out-of-scope listed, end-to-end verification). When they hurt: small changes, visual/taste-driven work where the "truth" is a rendered artifact, moving design.
- Not found: first-party UI-specific SDD write-ups from Shopify/Airbnb/Uber/Atlassian/Vercel on agentic front-end verification. Search returned only Vercel/Shopify commerce-integration material (irrelevant) and Atlassian's token docs. Flag as UNVERIFIED/absent rather than inferring their practice.

## 7. Parallel agents on shared UI
- Worktrees give file isolation; "merge conflicts" vs "intent conflicts" (clean merge, wrong combined behavior) [S]. Collision hotspots: routing tables, config, component registries (and by extension token files, shared primitives, global CSS). Assign explicit file ownership; sequence tasks that share files; merge one branch at a time; 3-5 agents practical ceiling. https://www.mindstudio.ai/blog/git-worktrees-parallel-ai-coding-agents ; https://addyosmani.com/blog/code-agent-orchestra/ ; https://auravcs.com/learn/run-multiple-coding-agents-in-parallel
- Anthropic: worktrees, /batch (5-30 subagents each in a worktree), Writer/Reviewer fresh-context pattern [P].
- Inference [U]: intent conflicts on UI show up only when rendered together (spacing, z-index, duplicated primitives); needs a post-merge render check, not per-branch checks.

## 8. Copy / content truth
- AI UI review checklists [S]: invented round numbers (99.9%, 50%), placeholder names (Acme, John Doe), invented testimonials/ratings, missing loading/empty/error/permission states, unlabeled icon buttons, buttons that submit forms by accident. Rule: every finding carries evidence + location (quoted value, where it lives). https://21st.dev/blog/ai-generated-ui-review-checklist ; https://dev.to/janarthanan_soundararajan/what-to-check-when-reviewing-ai-generated-ui-h28 ; https://floneo.co/blog/why-beautiful-ai-generated-uis-still-fail
- Mechanizable: extract all visible text from the rendered DOM (Playwright), diff against a source-of-truth copy file/requirement, flag numerals, proper nouns, and claims not traceable to a source.

## 9. Failure modes mapped to Wisp (spec -> plan -> implement -> gate, no render, no explore)
1. Self-consistency gates never render: spec-gate/plan-challenger/exit-gate judge text. Anthropic's own guidance says the check must return a signal from the running artifact (screenshot, Lighthouse, story tests). Add a "render evidence" artifact (screenshots at defined viewports/themes/states, axe/Lighthouse JSON, console errors) required by the implementation gate for UI scope; gate reports "not rendered" as a coverage gap, never pass.
2. Spec churn when design moves: add an explicit explore mode (throwaway prototype, no spec, no gate, time/scope boxed), whose output is a prototype + decision notes; then "spec from prototype" (characterize observable behavior, tokens, states), keeping the prototype as the visual oracle. Use OpenSpec-style change deltas rather than rewriting whole specs; skip the pipeline for one-sentence diffs.
3. Spec criteria for taste-based UI should reference a visual oracle (approved screenshot/Storybook story baseline) rather than prose adjectives; regression tools (Chromatic/Lost Pixel/Playwright toHaveScreenshot) then lock it after human approval.
4. Copy truth: add a content-provenance check (rendered text vs source copy; flag invented stats/testimonials/placeholders).
5. Token compliance: lint (stylelint strict-value) as deterministic check in smith verification; render check for effective computed values.
6. A11y: run axe + keyboard + contrast + target-size probes; verdict wording must say automated coverage is partial (~57% per Deque).
7. Parallel agents: file-ownership declared in plan; shared primitives/token files single-writer; integrated render check after merge (intent conflicts).
8. Independent verifier with fresh context, evidence-bearing, scoped to correctness (Anthropic), already matches Wisp's adversary/exit-gate shape but lacks rendering tools.

## Unverified / gaps
- Most Playwright/Chromatic/Percy/Lost Pixel/parallel-agent claims are from search summaries, not opened pages.
- WCAG 2.2 target-size threshold not fetched.
- No primary sources found for Shopify/Airbnb/Uber/Atlassian/Vercel agentic front-end verification practices.
- Prototype-to-spec has no strong primary source; evidence is blog-level.
