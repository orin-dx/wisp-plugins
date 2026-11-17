# R3: AI-native design ideation tools (researched 2026-10-17)

Confidence: web-search summaries plus two page fetches. Many sources are vendor or blog reviews, so treat as medium confidence. Tempo, Relume, Uizard and Bolt variant behavior are UNVERIFIED beyond one-line descriptions.

## Per-tool

### Claude Design (Anthropic)
- Options: ask in chat ("show me 2-3 alternative layouts"). The first generation is a starting point. Source: https://support.claude.com/en/articles/14604416-get-started-with-claude-design
- Steering: chat for structural change, inline comments on canvas elements, direct canvas editing (drag, resize, align), sliders for precision (https://uxpilot.ai/blogs/claude-design-review).
- Design system: ingests from a GitHub repo, design files, uploads, or a local codebase. Each system becomes an artifact reusable in Claude Code. It self-checks output against the system. Settings > Design Systems has a "Migrate team design systems" action.
- Handoff: export as .zip, PDF, PPTX, HTML, or Canva. Send-to integrations include v0, Lovable, Replit, Netlify, Miro and others. "Hand off to Claude Code" produces a bundle of design files, chat and a README with a paste-able prompt. A third-party description says the bundle holds a component structure spec, tokens used, layout hierarchy and assets (https://claudefa.st/blog/guide/mechanics/claude-design-handoff). That description is not first-party, so treat it as UNVERIFIED in detail. See also https://claude.com/product/design
- Explore then harden: no version history "yet". The workaround is to tell Claude "save what we have and try a completely different approach".
- Reported failures:
  - Inline comments sometimes vanish.
  - Multi-person editing is unreliable.
  - Weekly usage burn: PCWorld reportedly used 80% of a Pro week building three variations (https://uxpilot.ai/blogs/claude-design-review, https://flowstep.ai/blog/claude-design-review/).
  - Outputs drift by revision 4-5. Recovery is a fresh anchoring prompt, not stacked corrections.
  - Design-system copies drift out of sync with the real system. Some reviewers advise pasting tokens and specs into the prompt instead.
  - Output is "safe/template-y" (https://the-designengineer.com/insights/claude-design-review-is-it-worth-it/).
  - Annotations can only be seen by hovering over the chat comments.

### Google Stitch
- "Ideate" mode is for early exploration and "Flash" is fast generation. Both generate multiple alternatives (https://uithings.com/what-is-google-stitch).
- The March 2026 update added an infinite canvas mixing images, code and UI, a design agent that remembers project history, voice, and instant prototypes (auto-generated missing screens). It also added an MCP server for Claude Code and Cursor (https://sfailabs.com/guides/google-stitch-vs-figma).
- Handoff: paste into Figma as layered Auto Layout; HTML/CSS/Tailwind export. Framework export (Vue, Angular, Flutter, SwiftUI) is claimed by one source only: UNVERIFIED (https://vibecoding.app/blog/google-stitch-review).
- Positioning: ideate in Stitch, finish in Figma, then build in code.

### v0 (Vercel)
- Design Mode is a visual editing panel. Design Systems 2.0 uses a shadcn registry to pass tokens and components to v0. Output for the same prompt shifts per imported system, which is relevant to brand/theme comparison (https://v0.app/docs/design-systems).
- Since March 2026, v0 infers the design system automatically instead of manual selection. Design Mode has reported instability (https://community.vercel.com/t/design-mode-changes-where-do-i-select-the-design-system/36398.md).
- Output is React code, so handoff is the code itself. Variant/branching UX: not verified.

### Figma Make / Figma AI
- Make kits combine a React package or Figma library with guidelines, so prototypes use production components (https://www.figma.com/blog/introducing-make-kits-and-make-attachments/).
- The Figma agent claims to generate "explore multiple directions" variations using real components and tokens (https://www.figma.com/solutions/ai-design-iteration-generator/, marketing copy).
- Forum failure reports: changes confirmed but not applied, instructions ignored, stuck builds. Users have requested branching/version control for Make (https://forum.figma.com/suggest-a-feature-11/figma-make-structured-version-control-iteration-branching-for-ai-workflows-51303, https://forum.figma.com/report-a-problem-6/figma-make-not-following-even-simple-instructions-updates-not-occurring-46762).

### Magic Patterns
- Infinite canvas. You duplicate a component and prompt for parallel variations, such as four headers in different styles compared side by side. It uses your own tokens and component library (https://www.developersdigest.tech/blog/magic-patterns). This is the closest match to the option-board pattern.

### Subframe
- Canvas plus coding agent. Layers map to HTML/React. Components with props, slots and variants sync to the codebase (https://uxmagic.ai/blog/magic-patterns-alternatives). Variant generation for ideation: UNVERIFIED.

### Lovable, Bolt
- Both are full-app builders. Both have click-to-edit layers: Lovable Visual Edits (https://lovable.dev/blog/introducing-visual-edits), and Bolt Visual Edits, which stacks changes and sends them to the model in one batch (https://bolt.new/blog/visual-edits).
- Neither is primarily a divergent-exploration tool.

### Builder.io Visual Copilot / Fusion
- Maps Figma designs to code using your components. Modes are visual, interactive and code (https://builder.io/blog/builder-visual-editor-v2). Focus is hardening, not ideation.

### Uizard, Relume, Tempo
- Uizard (acquired by Miro in 2024): sketch-to-wireframe scanner and Autodesigner (https://uxmagic.ai/blog/magic-patterns-alternatives). Relume is recommended for marketing sites and sitemap/wireframes. Tempo: nothing found. All three are UNVERIFIED.

## Common ideation interaction patterns
1. Parallel variants: duplicate or ask for N options (Magic Patterns, Stitch Ideate, Figma agent, Claude chat).
2. Option board: an infinite canvas where options sit side by side (Stitch, Magic Patterns, Claude canvas).
3. Annotate-and-iterate: pin comments on elements, with a chat fallback for structural changes (Claude, Bolt batched edits).
4. Direct manipulation or sliders for fine tuning (Claude, v0 Design Mode, Lovable, Bolt).
5. Design-system grounding via a registry, kit or ingested repo (v0, Make kits, Claude, Magic Patterns).
6. Branching history is weak or absent. Claude has no version history and Make users request branching. Stitch's agent keeps project memory. Decision logs are essentially not a feature anywhere I found; the chat transcript serves as an implicit log, and it is bundled into the Claude Code handoff.
7. Handoff means an export bundle, code, or MCP.

## Failure modes users report
- Cost: variants burn quota fast.
- Drift over iterations; the fix is a re-anchoring prompt.
- Lost or invisible comments.
- No history, so you cannot return to an earlier option.
- Design-system drift or copies going stale.
- Generic "safe" aesthetics, and options that converge instead of diverging.
- Instructions ignored or unapplied.
- Premature fidelity: ideation tools output production-looking code, which blurs sketch and spec.

## Lessons for Wisp sketch mode
- Make options first-class files, not chat turns. Use a stable ID per option, such as `sketch/<topic>/opt-A`, so there is a durable history even though the tools lack one.
- Render the matrix (option x brand/theme) from tokens. v0 shows per-design-system rendering is feasible and valuable.
- Allow TBDs and use no gates. Mark each option's status (open, parked, chosen, rejected) with a one-line reason. That is the decision log, which no tool provides.
- Prevent drift. Re-derive from an anchor brief on each round, and keep the brief in the sketch file.
- Keep cost visible: cap the default option count at about 3, because tools burn quota on variants.
- Promote path: the chosen option becomes a muse component spec, with TBDs resolved or moved to non_goals and behaviors turned into testable criteria. The sketch carries a `decision_ref`, which matches the existing arch-model and ADR conventions. Handoff bundle idea (Claude Design): ship the chosen option, tokens and the decision log together.
- Keep sketch artifacts visibly low-fidelity, or watermarked, so nobody mistakes them for a spec.
