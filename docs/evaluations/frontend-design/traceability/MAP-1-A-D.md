# MAP-1: traceability of A-plugin-inventory.md and D-outcomes.md to WP-draft.md

Conventions. Evidence tag: neither source used [P]/[S]/[U]/[F]/[I] tags, so A rows carry `repo-grep` (the author's own repo reads/greps, line cites unverified by me) and D rows carry `repo-grep` meaning consumer-repo (~/projects/pages) docs/commits as cited by the author. "(partial)" means the WP covers only part; the gap is stated in the note. DISPOSITION means no work item, with evidence-based reason. UNMAPPED rows point to a WP-1xx in section 3.

## Table A (A-plugin-inventory.md)

| ID | finding | evidence | mapped WP | note |
|---|---|---|---|---|
| A-01 | No plugin has a visual, browser, or generative-design mode; everything is text/JSON/code-reading | repo-grep | WP-12, WP-17, WP-40, WP-41 | Umbrella finding; components split into rows below |
| A-02 | vanguard is the only "explore options" stage but is evidence-gathering converging on one falsifiable recommendation, not divergent ideation | repo-grep | WP-10, WP-11, WP-21 | WP-21 must keep convergent research distinct from divergent sketch (WP-11) |
| A-03 | POSITIVE: muse drafter names props, variants, all 8 states, a11y criteria (role, name, focus order, keyboard, live-region), falsifiable via rendered markup/role/focus/events | repo-grep | WP-30 | Preserve; WP-30 says "keep falsifiable criteria" |
| A-04 | POSITIVE: muse auditor and exit-gate fail specs missing any implied state or a11y criterion; gate refuses "a11y can be finalized during implementation" | repo-grep | WP-30, WP-50 | Preserve when amending gate hygiene (WP-50) |
| A-05 | Design-system grounding is a single rule: verify prop names/types against live source; no token/theming/visual modelling | repo-grep | WP-30, WP-31, WP-32, WP-35 | |
| A-06 | muse scope statement "Audits the spec, not the implementation" so nothing downstream checks the rendered component | repo-grep | WP-41, WP-42 | WP-41/42 cover implementation evidence; docs scope text in muse README/plugin.json must be updated (add to WP-01) |
| A-07 | smith TS verification reference lists Vitest/Jest/Stryker/fast-check/build only; nothing on Testing Library, DOM, jsdom, browser runners | repo-grep | WP-46 | Edit shared/references/verification/typescript.md |
| A-08 | constitution.md:202 requires verification at nearest executable boundary incl. "render" or a recorded gap; "render" is a label with no procedure; UI change can pass via coverage gap | repo-grep | WP-40, WP-41 | Also field-survival-map@1 boundary_type "render"; WP-40 states "unrendered UI is a gap, never a pass" |
| A-09 | verification/evidence.md "Environment testing" lacks browser/viewport/theme/locale | repo-grep | WP-41 (partial) | Missing: explicit edit to evidence.md environment list; fold into WP-41 |
| A-10 | ranger TS hazards T1-T10 overlap UI only generically (T9 exhaustive variants for component variants; T7 props dropped before DOM) | repo-grep | UNMAPPED | WP-44 is a11y only. Propose WP-101 |
| A-11 | architecture/typescript.md "UI state" owner and boundary-values.md sum-type guidance help component state modelling but are not UI-specific | repo-grep | UNMAPPED | Propose WP-102 |
| A-12 | navigator plan@1 requires mechanical tests per criterion; a plan cannot encode "looks right" | repo-grep | UNMAPPED | WP-30 covers spec@2 only; plan has no render-evidence task kind. Propose WP-103 |
| A-13 | scribe:audit-architecture / arch-model@2 boundary checks apply generically to UI layering | repo-grep | WP-35 (partial), WP-81 | Missing: arch-model canonical-abstraction use for component reuse (see A-26) |
| A-14 | Claim: grep for playwright, screenshot, storybook, visual regression, chromium, axe, e2e, jsdom, WCAG, contrast, responsive, viewport, CSS, design token across plugins/ and shared/ returns nothing except one muse "design-system tokens" mention | repo-grep | WP-05 | Unverified by me; likely false for "contrast"/"CSS"/"responsive" given diagrams.md "Orin Visual Standard"; re-run (section 2) |
| A-15 | workspace-manifest@1 capability kinds are a closed enum (build,test,type_check,lint,mutation,property,fuzz,race,integration,boundary); no e2e/browser/visual/a11y | repo-grep | WP-40 | Needs schema bump (@2) and recon updates in smith AND ranger |
| A-16 | recon cannot record that Playwright/Storybook exists; smith would treat as generic test or ignore | repo-grep | WP-40 | D-39/D-42 show these exist but were manual: capability needs a "ci vs manual" attribute (contradiction C-3) |
| A-17 | spec@1 has no fields for tokens, layout/breakpoints, visual refs, assets, motion, theming, i18n/copy (additionalProperties false) | repo-grep | WP-30 | Also WP-31 for design-intent file |
| A-18 | judgment_call:true criteria require human judgment that Sentinel/exit-gates cannot evaluate | repo-grep | WP-34 (partial) | Missing: gate behaviour for judgment_call criteria (accept human approval evidence artifact) |
| A-19 | drafter judgment rejects "looks disabled"-style criteria as semantic-model leakage, pushing visual intent OUT of the spec | repo-grep | WP-30 (partial) | Missing: rewrite of drafter/auditor judgment to admit render-reference criteria while avoiding D-33 brittleness; see WP-106 |
| A-20 | Observable behavior defined only as DOM/ARIA/focus/events: nothing on computed style, pixels, spacing, contrast, responsive, reduced-motion, dark mode, cross-browser | repo-grep | WP-30, WP-42 | |
| A-21 | A muse spec can pass the binding gate with zero criteria on how the component looks | repo-grep | WP-30 (partial) | Missing: exit-gate condition requiring visual-reference or explicit "no visual intent" statement |
| A-22 | MOST CONCRETE: muse README, SKILL.md, plugin.json and top-level docs point to a "ranger accessibility hazard taxonomy" that does not exist (ranger has T1-T10 only) | repo-grep | WP-01, WP-44 | Verify by grep "accessib" in plugins/ranger and shared/references |
| A-23 | Consequence: no plugin checks implemented a11y at all (no axe, ARIA lint, keyboard walk) | repo-grep | WP-42, WP-44 | |
| A-24 | Claim: the dangling reference was introduced by muse rename commit a859e2f and never implemented | repo-grep | WP-05 | Verify with git log -S (section 2) |
| A-25 | No token inventory, theme/Tailwind/CSS-in-JS capability detection, or reuse-vs-new-component check | repo-grep | WP-31, WP-32, WP-35 | |
| A-26 | scribe arch-model@2 canonical-abstractions concept could host reuse-vs-new check but is generic and code-structure oriented | repo-grep | WP-35 (partial) | Missing: extension of arch-model@2 with component/token canon (spec'd in WP-31/32 facts file) |
| A-27 | Mutation testing (Stryker) is meaningless for CSS/markup-only changes; deliberate-fault fallback is behavioral; UI without logic gets weak discrimination evidence | repo-grep | WP-46 | See also C-8 (mutation cannot detect a wrong oracle) |
| A-28 | No "run the app and look" step; built-in `run` skill and Playwright MCP are outside the plugin set | repo-grep | WP-12, WP-41 | Decide whether plugins may name browser tools abstractly (constitution abstract-tool rule) |
| A-29 | sentinel verifies by reading; visual criteria land in "unverifiable"; exit-gate separates coverage gaps from blockers so UI work can clear with visual gaps | repo-grep | WP-40, WP-50 | |
| A-30 | scribe:spec-drift checks code vs criteria textually and cannot detect visual drift | repo-grep | WP-73, WP-41 | WP-73 extends drift to intent files; visual drift needs baseline comparison from WP-41/45 |
| A-31 | Net: set supports UI as logic+semantics+a11y-spec, not pixel/UX/design-system fidelity; muse stops at the spec | repo-grep | WP-40, WP-41, WP-30 | Summary of A-15..A-30 |
| A-32 | muse drafter accepts design references (mockup description, component family, tokens) as input: consumes a finished design, does not create one | repo-grep | WP-11, WP-31 | |
| A-33 | vanguard sources are specs/docs/manifests/codebase/external keywords: no visual or competitive-UI sourcing | repo-grep | WP-21 | |
| A-34 | muse README mermaid labels auditor "design review" but checks are spec completeness, not design critique | repo-grep | WP-01 (partial), WP-17 | WP-01 as written covers only the ranger reference; add label correction. Real critique = WP-17 |
| A-35 | weaver capture-need/clarify can structure a design brief into requirement@1 but clarifier (one question, demands testable done_when) is hostile to exploratory briefs | repo-grep | UNMAPPED | WP-18 routes modes but weaver has no exploratory intake. Propose WP-104 |
| A-36 | vanguard risk-assessor surfaces risks neutrally; usable for "risk of adopting design system X" | repo-grep | WP-21 | Positive; document the use in vanguard README |
| A-37 | shared/references/authoring/diagrams.md and voice.md are internal repo authoring standards, not product design/copy guidance; do not mistake for capability | repo-grep | WP-20 | Warning: do not reuse voice.md for product copy; WP-20 needs its own reference |
| A-38 | courier pr-narrator/changeset write only technical release prose | repo-grep | WP-20 | Disposition: courier not a copy tool; confirm WP-20 is a new agent |
| A-39 | No divergent mode: default-fail gates, no TBDs, testable-only criteria, 2-round caps force convergence; reasoning field never forwarded downstream | repo-grep | WP-10, WP-11, WP-61 | WP-61 touches reasoning field naming/forwarding |
| A-40 | No artifact type for design direction, style tile, brand brief, wireframe, prototype, copy deck, critique; new schemas need mason:design-schema and schema-first | repo-grep | WP-11, WP-17, WP-20, WP-31 | Each WP must list its schema (@1) before the agent |
| A-41 | No generation agents with a visual output channel; no screenshot ingestion; no agent lists browser/image tools; no critique rubric (hierarchy, contrast, rhythm, consistency) | repo-grep | WP-12, WP-17 | |
| A-42 | No brand-voice/copy review beyond repo-internal voice.md | repo-grep | WP-20 | |
| A-43 | No user-research or taste-eliciting loop; weaver intake asks no questions, clarifier one question | repo-grep | WP-16 (partial), WP-13 | WP-16 covers pick-from-directions; missing: preference/taste capture feeding decision log (WP-13) |
| A-44 | Model-tier policy has no slot for a generative/exploratory mode; needs constitution amendment (ARCHITECTURE.md ~L241) | repo-grep | WP-10, WP-63 | |
| A-45 | Human-in-the-loop exists only as escalation after failed retries, not as a design-review checkpoint | repo-grep | WP-18, WP-34, WP-51 | |
| A-46 | Net: ideation must live outside the plugins; muse/weaver are the downstream funnel (chosen direction -> requirement@1 -> spec@1) | repo-grep | WP-14 | |
| A-47 | muse emits verdict@1 while others use verdict@3 (verdict@1,@2,@3 all exist); "may matter for sentinel routing" | repo-grep | WP-02 | Routing impact is speculation; verify (section 2) |
| A-48 | Codex counterpart exists at harnesses/codex/plugins/muse/skills/component/SKILL.md, authored separately; generated files must not be edited | repo-grep | WP-70 | |
| A-49 | AGENTS.md rules: cross-harness review, constitution byte-identity, schema-first, just check; new plugin/spec@2 needs mason scaffold + schema design + marketplace.json + Codex source + just marketplace-sync | repo-grep | WP-70 | Constraint on every WP that adds an agent or schema; add a WP-wide acceptance rule |
| A-50 | Precedent: smith README documents "Capability Gaps" (shared/README) as honest gap docs | repo-grep | WP-40 | Reuse vocabulary for "unrendered" gaps |
| A-51 | weaver capture-need is the lightest path (no questions, omits unknowns) but still yields formal requirement@1 with testable done_when | repo-grep | WP-18 | |
| A-52 | vanguard is one fixed pipeline ("not a menu of modes"), not skippable internally | repo-grep | WP-18, WP-21 | Missing: a lighter design-research variant or documented skip; vanguard README states the opposite |
| A-53 | weaver -> scribe directly (skip vanguard) allowed per plugins/weaver/README.md:117 | repo-grep | WP-18 | Line cite to verify |
| A-54 | scribe has no documented "draft only, don't gate" sketch mode beyond calling draft-spec alone | repo-grep | WP-11, WP-18 | |
| A-55 | muse: single skill, circuit breaker (2 drafter/auditor, exit gate up to 3 then human); spec persisted only after exit-gate passes | repo-grep | WP-18, WP-51 | |
| A-56 | navigator plan@1 requires exact code, tests per criterion, all criteria covered, challenger (max 2), no TBDs: no sketch path | repo-grep | WP-18 | |
| A-57 | smith is the loosest build entry (spec without plan) but still recon, mutator, reviewer, exit-gate per batch; no spike/prototype/throwaway mode; nothing without a spec or plan | repo-grep | WP-15 | |
| A-58 | sentinel is gate-only, explicitly not for exploratory work (skills/gate/SKILL.md:24), opt-in | repo-grep | WP-18 | Line cite to verify |
| A-59 | ranger has narrower paths (verify one candidate, targeted scan) but is audit not building | repo-grep | DISPOSITION: no WP | Not an exploration tool; relevance only via WP-44/WP-101 |
| A-60 | courier skills individually invokable; post-review needs explicit confirmation; shipping not exploring | repo-grep | DISPOSITION: no WP | Evidence: skills list in A; no exploratory role |
| A-61 | mason is plugin authoring only, irrelevant to product UI work | repo-grep | DISPOSITION: no WP (used as tool by WP-70, WP-60) | mason:evaluate is the harness for WP-60 and WP-109 |
| A-62 | Bottom line: every build path assumes an artifact and ends in an independent verdict; flexible edges are escape hatches by omission (single skill, not installing gates, graceful degradation constitution L116/L126) | repo-grep | WP-18 | |
| A-63 | Rigidity rules (constitution L104-106 resubmit; L162 loops capped 2; L166 re-eval scope) apply once invoked | repo-grep | WP-10, WP-50 | Scope circuit-breaker rules to status != sketch (see A-82) |
| A-64 | Constitution L112: on pass the orchestrator SHALL write spec to docs/specs/<id>.json, commit, set spec_file_path | repo-grep | WP-14 | Promotion must be the path that triggers this write |
| A-65 | Constitution L154: amended plan must pass challenger; amendment not exempt | repo-grep | WP-58 | |
| A-66 | Review loops capped at 2 rounds | repo-grep | WP-51 | |
| A-67 | Model tiers L47-50: terminal binding verdicts on opus/high, so cost/latency on every gate | repo-grep | WP-63, WP-91 | WP-91 measures it |
| A-68 | Default-fail: muse exit-gate "conditional passing is a fail", escalate after retry_count>3; scribe exit-gate; sentinel verified only on positive evidence | repo-grep | WP-50, WP-51 | See C-1 on retry-cap enforcement |
| A-69 | Sentinel gate L50: 3 retries then escalate, "do not loop indefinitely" | repo-grep | WP-51 | Line cite to verify |
| A-70 | "No TBDs anywhere" in muse/scribe/navigator: an unfinished idea cannot exist as a valid artifact; unknowns forced into non_goals/reasoning | repo-grep | WP-11, WP-30 | WP-30 keeps no-TBD in spec; WP-11 allows TBD in sketch |
| A-71 | smith: recon stops on failing baseline; implementer "no shortcuts"; spec_contradiction halts remaining work; only approved reviews reach exit-gate | repo-grep | WP-15, WP-56 | Spike must downgrade baseline failure to a warning |
| A-72 | ADR 008 removed test-first ORDER but not discrimination via mutation or deliberate fault ("tests proven" not "tests first") | repo-grep | WP-15, WP-46 | Read ADR 008 before WP-15/46 to avoid contradicting it |
| A-73 | Schema-first/additionalProperties:false means a malformed output halts the pipeline | repo-grep | WP-10, WP-54 | Non-binding sketch artifacts need a lenient schema; WP-54 stall handling |
| A-74 | NOT forced: no hooks make gates mandatory; skills trigger on phrasing; user can ignore plugins; rigidity is only once invoked plus implied lifecycle ("one direction, no side-taps") | repo-grep | WP-18 | Implication: new exploration modes can be additive without removing gates |
| A-75 | Sketch need 1: declared mode on artifacts (status sketch/spec or sketch-note@1/idea@1) permitting TBDs/alternates, never gated; spec@1 requires non_goals>=1 and criteria>=1 so cannot carry a sketch | repo-grep | WP-11, WP-30 | |
| A-76 | Sketch need 2: smith spike skill (skip plan/spec/mutator/reviewer/exit-gate; baseline failure -> warning; output = run instructions + verified/not-verified; no commit by default) | repo-grep | WP-15 | |
| A-77 | Sketch need 3: browser/screenshot/dev-server capability kind so loop is change-render-look | repo-grep | WP-40, WP-12 | |
| A-78 | Sketch need 4: divergent cognitive mode (haiku/sonnet, no adversary) producing N alternatives plus cheap pick/promote converting to capture-need -> muse/scribe, sentinel only at promotion | repo-grep | WP-10, WP-11, WP-14, WP-63 | |
| A-79 | Sketch need 5: smoke-check recipe recorded as evidence without criteria; verdict@3 "scoped pass" could carry scope "smoke only" | repo-grep | WP-15 | Assumes verdict@3 scope semantics; verify (section 2) |
| A-80 | Sketch need 6: constitution amendment scoping circuit-breaker/default-fail (L104-166) to status != sketch; mason scaffold + audit, Codex counterparts, marketplace.json | repo-grep | WP-10, WP-70 | |
| A-81 | Inventory header facts: marketplace v4.4.5; plugin versions (weaver 3.0.3, vanguard 2.0.2, scribe 3.4.0, muse 1.0.1, navigator 2.3.2, smith 2.4.5, sentinel 2.1.2, ranger 3.2.3, courier 3.0.3, mason 3.2.2) | repo-grep | WP-05 | Versions drift; recheck before baseline (git is at 9c39614) |
| A-82 | Many line-number citations (constitution L47-50,104-166,202,228; ARCHITECTURE L137,L241; weaver README:117; smith README:14; sentinel L24,L50) | repo-grep | WP-05 | Line cites rot; re-resolve before quoting in ADRs |
| A-83 | smith has optional Wisp CLI implementation-context@1 | repo-grep | WP-47, WP-74 | Existing integration point for UI query/lookup layer |
| A-84 | muse model tiers: drafter sonnet, auditor sonnet, exit-gate opus (README table) | repo-grep | WP-63 | Included in tier re-check |

## Table D (D-outcomes.md)

| ID | finding | evidence | mapped WP | note |
|---|---|---|---|---|
| D-01 | Scope: ~/projects/orin-dx-site holds only brand/ HTML artifacts and .bak files (no git, no docs); all named docs live in ~/projects/pages/docs | repo-grep | WP-90 | Provenance limit: outcomes evidence is from one consumer repo plus one brand folder |
| D-02 | 538 commits 30 Sep-16 Oct 2026; 479 with Claude-Session trailer; 460 with Entire-Checkpoint | repo-grep | WP-03 | Transcript source for the baseline metrics; verify counts via git log |
| D-03 | Plugin-driven work: SPEC-001..013 (spec@1 + verdict files), PLAN-001/003/004/005 + challenger files, SPEC-002 rules checker; verdicts verdict@1-style | repo-grep | WP-02, WP-03 | Suggests muse verdict@1 volume; confirm which verdicts were muse vs scribe |
| D-04 | Everything after 13 Oct was ad hoc; strands/landing/Tools/Principles/brand-page rebuild (SPEC-014/015/016, ~110 commits, 14 Oct) shipped without a gate | repo-grep | WP-18, WP-11, WP-14 | Evidence that the pipeline was abandoned for exploratory work: demand for sketch/spike/promote modes |
| D-05 | Commit 0ea8be77: specs drafted "before the work moved to an exploratory build. They are not approved scope." | repo-grep | WP-14, WP-82 | Promotion gap; also stale-spec cleanup |
| D-06 | SPEC-015-audit.json is an overall:fail never resolved | repo-grep | WP-51, WP-82 | Silent abandonment of a failed verdict; WP-51 requires declared overrides |
| D-07 | 16 Oct a11y audit, case-study rewrite, copy reviews, ship-readiness were all ad hoc | repo-grep | WP-42, WP-43, WP-20, WP-111 | These are the productive ad hoc moves to productize |
| D-08 | Design-system base-layer docs (design-system-rules/coverage/api, proposals/*) are owner+Claude prose, not plugin artifacts, but SPEC-005..012 derive from them | repo-grep | WP-31 | Design-intent file would give these a typed home |
| D-09 | Defect 1: specs and code drifted (nav sheet, rails; SPEC-001/003a/003c/PLAN-004; props vs DOM, 768 vs 1280); found by human review not drift-checker; fixed via SPEC-013 (ef3dcf26) | repo-grep | WP-73, WP-58, WP-36 | Drift-checker was available but not triggered: need trigger policy (pre-merge/scheduled); WP-73 only extends scope |
| D-10 | Defect 2: 760px boundary (c77778b1): code narrow at 760, frame thresholds parked at 761, SPEC-013 AC-004/021 said 760 wide; 8px band; 296 nav-fixture tests pinned the wrong value | repo-grep | WP-32 (partial), WP-52, WP-46 | Missing: independence of test oracle from implementation constants (WP-107) |
| D-11 | Defect 3: brand page shipped "NaN%" glass opacity and rails width 1104 vs 1304 (05844c28); only a crawl for "NaN" caught it | repo-grep | WP-42 (partial) | Missing: rendered-text scan for NaN/undefined/[object Object] (WP-105) |
| D-12 | Defect 4: token conversion left bare parentheses instead of calc(); browsers dropped masks; hard cuts at phone width (a04ddca3); no visual test existed | repo-grep | WP-42, WP-41, WP-45 | Token lint plus screenshot at phone width would catch; see C-9 on "no visual test existed" vs "deleted 12 Oct" |
| D-13 | Defect 5: strand marks stretched 32x36 from square source and 2px low; family/loop cards; phone opener empty band (0a9018ca, cdb331d7); found by human review | repo-grep | WP-17, WP-41 | Needs aspect-ratio/geometry probe (WP-42) as well as critique |
| D-14 | Defect 6: focus rings clipped/wrong shape or side (bf6b44d6, a0af8700, ef5cc2a7, 88490112, ad42137f, e23aae76); focus not returned after sheet close (12d82f79, 98ae9acc) | repo-grep | WP-42, WP-41, WP-33 | Focus-return behaviour belongs in APG reference (WP-33) and keyboard walk probe |
| D-15 | Focus ring colour changed to blue (2c81bd88) because it clashed; many focus changes are owner design decisions not bugs, yet SPEC-001/005/007 had "passed" focus criteria first | repo-grep | WP-13, WP-03 | Defect vs design-decision classification needed in WP-03; decisions into log (WP-13) |
| D-16 | Defect 7: 32/40/48 control scale and 44px touch target retrofitted 13 Oct (e23aae76) | repo-grep | WP-42 | Target-size probe |
| D-17 | 16 Oct audit still found: colour-card labels 2.9-4.3:1 (opacity 0.7), CV contact icons overlapping, work filters 43px wide (ab5a7e4a), Orin controls under 44, small text on ramp colours below 4.5:1 (b8faa0a5) | repo-grep | WP-42, WP-41 | |
| D-18 | Two banner landmarks on techworx brand page; CV toolbar outside main (1d61cb60); h1 outside main on document-template pages (known issue in docs/plans/accessibility-manual-pass.md) | repo-grep | WP-42 | Landmark probe is already in WP-42 |
| D-19 | Contrast and target size were found by the first real automated suite, 4 days after base specs "all passed" | repo-grep | WP-42, WP-45, WP-80 | |
| D-20 | Review 3 Oct F1: nav toggle labelled Preview/Outline with Cmd+Y flipping theme (Blocker/High found only after build) | repo-grep | WP-82 | Consumer fix list; behaviour was a naming/shortcut defect catchable by spec audit? treat as evidence for WP-33 keyboard map |
| D-21 | Logo cap regression AC-112/113/017 caught only by manual baseline `just e2e` (4 failures) | repo-grep | WP-45, WP-80 | CI placement |
| D-22 | F3: CV print .cvpage.cvpage.cvpage, 67 !important, 40 hex | repo-grep | WP-42, WP-81 | Token lint (hardcoded values, !important count) |
| D-23 | F4 --radius-md removed so corners square; F5 PostRow gap 5 emitted 5px not 24px; F6 hero padding emitted 96px; Orin Button 14/400 not 16/600; TileGrid 2 cols on phones with lone cards | repo-grep | WP-42, WP-41, WP-81 | Token-key to computed-style resolution check; TileGrid lone card is layout critique (WP-17) |
| D-24 | Token-key mistakes "already did twice" (two numbering schemes) | repo-grep | WP-32, WP-31 | Facts file of real token keys consumed by drafter/planner |
| D-25 | Most review-3-Oct items are still "pending verification", not verified-fixed | repo-grep | WP-82, WP-90 | Status unknown; verify before citing as open |
| D-26 | Copy: case studies misattribute (H1 wrong image as Chosen; H2 "88% I chose" contradicted by transcript; H4 AI research credited to owner); "two views" stale; claims dropped from hero (BRA-7) | repo-grep | WP-43, WP-20, WP-82 | |
| D-27 | No spec criterion covers truthfulness; only human/model fact-check caught copy errors | repo-grep | WP-43, WP-30 | WP-30 needs a provenance/source field on copy criteria |
| D-28 | Docs links to docs.orin-dx.com pointed to an empty site | repo-grep | UNMAPPED | WP-04 covers plugin docs only. Propose WP-105/WP-111 (crawl link checker); consumer fix WP-82 |
| D-29 | SEO/meta checked only by ship-readiness crawl; docs stub lacks description/lang; /writing/ builds "0 posts" and is unlinked; seo-geo worktree exists with no spec | repo-grep | UNMAPPED | Propose WP-111 (ship-readiness recipe); consumer follow-up WP-82 |
| D-30 | Gates judge spec on its own terms; found zero rendered-outcome defects; no step renders anything | repo-grep | WP-40, WP-41 | |
| D-31 | POSITIVE with cost: gate blockers (contradictions between ACs, missing states, wording e.g. "AC-044 label role holds only for techworx") were valuable; SPEC-001 needed 13 verdict files, SPEC-005 retry_count 6, SPEC-002b hit the 3-retry escalation | repo-grep | WP-50, WP-51, WP-91 | retry_count 6 exceeds cap 3: see C-1; blocker-type typology in WP-03 |
| D-32 | Specs over-specified at the wrong level: SPEC-013 has 39 ACs of paragraph length with exact px, route-interception recipes, "Replaces SPEC-001 AC-056" chains; SPEC-001 had 120+ ACs; they read as CSS assertions | repo-grep | UNMAPPED | WP-36 caps size; no rule stops CSS-mirroring criteria. Propose WP-106 |
| D-33 | Owner deleted 384 of 1116 tests (34%) on 12-13 Oct (testing-prune-plan), incl 28/33 in site-nav-css.test.ts, because they pinned values not behaviour | repo-grep | WP-45 (partial), WP-46 | Missing: spec-side prevention (WP-106). Tension with WP-42 computed-style checks (C-4) |
| D-34 | Real visual risks (contrast, reflow, forced colours, target size) were parked in deferred-accessibility-tests.md and only rebuilt as one suite on 16 Oct (9dfe58e4, e9d921e9), which immediately found failures | repo-grep | WP-42, WP-80 | Forced-colours probe is not in WP-42 list; add |
| D-35 | Spec/design thrash: SPEC-004..012 gated pass 11 Oct then "revised for design decisions" in one batch 12 Oct (6fb08ba3, f8896db5, 1faebc1c) | repo-grep | UNMAPPED | WP-11/13 reduce cause; no WP on re-gating revised specs (revisions may have bypassed gate; unknown). Propose WP-108 |
| D-36 | Visual decisions (focus ring side, brass depth, frosted ground, sheet corners) made after gating via drawn pages (d72d7458 "ui-examples-open"); muse specs encoded states/ARIA not visual intent | repo-grep | WP-12, WP-30, WP-31 | Strongest evidence for sketch-before-spec ordering |
| D-37 | SPEC-006..012 passed at retry 0 on 11 Oct, 8 specs in one day, each revised next day for 5+ owner decisions: author infers "good drafts or low adversarial pressure" | repo-grep | WP-03, WP-60, WP-91 | Inference not proven; check verdict blockers/notes per spec |
| D-38 | Verification infra exists: Vitest ~1100 tests pre-prune, AC-id references in ~100 test files (e.g. apps/site-e2e/e2e/nav-sheet.spec.ts) | repo-grep | WP-03, WP-45 | Positive: AC-id traceability convention to keep in plans |
| D-39 | nav-fixture Playwright suite 296 passing; Firefox absent | repo-grep | WP-45, WP-80 | Browser matrix in render-evidence |
| D-40 | site-e2e 19 spec files on real built sites; Storybook ~one line per component, SiteNav had no story at 3 Oct; axe in six Vitest files plus 16 Oct audit | repo-grep | WP-80, WP-45, WP-46 | |
| D-41 | AC-ids tie nav/chapter/breadcrumb specs to tests; SPEC-014..016 work has none; 16 Oct audit is tied to WCAG success criteria not spec ACs | repo-grep | WP-30, WP-41, WP-42 | Render-evidence should record AC id or WCAG SC for each finding |
| D-42 | Playwright suites are `runInCI: false` / "manual; not part of ci" (justfile lines 60-66; review 11 Oct headline 5; review 3 Oct testing gaps) | repo-grep | WP-80, WP-45 | |
| D-43 | Zero toHaveScreenshot (grep 0); no Storybook build/visual in CI; no JS size budget (271 KB hydrated) | repo-grep | WP-45, WP-80, WP-42 | Budget in WP-42 |
| D-44 | packages/rules is a README only; SPEC-002 rules checker never ported | repo-grep | WP-81 | |
| D-45 | The missing enforcement layer (review 11 Oct) is exactly what would have caught NaN, calc() breakage, hex/px/!important | repo-grep | WP-42 | |
| D-46 | Owner policy 13 Oct "we test behaviour, visual testing comes later" is right about brittleness but nothing replaced it until 16 Oct | repo-grep | WP-45 | Policy design: behaviour-vs-CSS split with explicit visual layer |
| D-47 | decisions-status.md (13 Oct) opens "after two decisions turned out to be recorded but not applied" | repo-grep | WP-13, WP-82 | |
| D-48 | design-system-coverage lists MenuSheet "removed; NavSheet built" while review 11 Oct still describes MenuSheet; docs stale within a day (8cebb61b "four stale tests"; commits correcting stale thresholds) | repo-grep | WP-73 | |
| D-49 | Duplicates: packages/orin and packages/twx both carry button, button-link, code-block, command-line, hero, icon, margin-note, view-toggle | repo-grep | WP-81 | |
| D-50 | packages/foundations/src/ui AND packages/components/src both carry button, button-link, field, sheet-ish components; 23 app files import foundations/ui | repo-grep | WP-81 | |
| D-51 | Five theme-toggle copies were the stated target; 40 files in apps/orin-dx and techworx still call css() (policy: recipes only); 13 `brand === ...` branches in shared code | repo-grep | WP-81 | Evidence for WP-35 reuse-vs-new check |
| D-52 | Spec numbering collisions: SPEC-002/a/b/c, SPEC-003/a/b/c, PLAN-003 vs PLAN-004 superseded; "Replaces SPEC-001 AC-xxx" chains obscure the live contract | repo-grep | UNMAPPED | WP-36 mentions supersession handling only. Propose WP-110 |
| D-53 | POSITIVE: plugin work reliably produced consistent, testable, well-challenged spec text and plans for interaction/ARIA/geometry | repo-grep | WP-30 | Preserve; do not weaken gates |
| D-54 | Every visible-quality defect (NaN, masks, stretched marks, phone openers, contrast/targets, landmarks, copy truth) was found by human look, post-hoc audit, or new suite | repo-grep | UNMAPPED | Use these as a regression corpus for the new stages. Propose WP-109 |
| D-55 | The best-defended area (nav) is also where the owner deleted the most tests as too brittle | repo-grep | WP-45, WP-106 | Over-defence signal |
| D-56 | Late strong results came from two ad hoc moves: whole-site crawl/axe/target/reflow audit (16 Oct) and independent fact-check/review docs | repo-grep | WP-42, WP-43, WP-17 | Productize both |
| D-57 | Missing stage: rendered-outcome check (screenshots at 320/375/760/1440, both themes and brands, contrast/target/reflow probe, copy-vs-source) in CI and referenced from spec criteria | repo-grep | WP-41, WP-42, WP-43, WP-45, WP-30 | Viewport list is consumer-specific; WP-12 matrix should be configurable |
| D-58 | Citation list includes commit 61c05725 and docs not discussed in the body | repo-grep | WP-90 | Unreferenced citation; verify what it supports |
| D-59 | Brand page defect (NaN) occurred on the page about the design system itself | repo-grep | WP-42 | Part of D-11; kept as signal that design-system pages need render checks |
| D-60 | Spec/plan artifacts carry drift risk even for plan: PLAN-003 vs PLAN-004 superseded; nav fixtures' 296 tests encoded wrong constant | repo-grep | WP-58 | Plan amendment when spec changes |

## 1. CONTRADICTIONS

C-1. A: muse exit-gate escalates after retry_count>3 / "up to 3 retries then human"; Sentinel "3 retries then escalate". D: SPEC-005 reached retry_count 6 and SPEC-001 needed 13 verdict files. Either the cap is not enforced, retry counting resets per drafter loop, or humans overrode silently. Supports WP-51; needs transcript check.
C-2. A says only muse emits verdict@1 (others verdict@3). D calls consumer verdicts "verdict@1-style" with artifact_type spec@1 for SPEC-001..013 (including ones possibly gated by scribe). Need to check which gate produced them before concluding on verdict@1 impact (WP-02).
C-3. A-15/A-16 say recon cannot record browser/Storybook capability; D shows Playwright, Storybook, axe existed in the consumer but ran manual / `runInCI:false`. Adding a capability kind (WP-40) is insufficient: recording must capture "exists, but not in CI/manual".
C-4. TENSION between A and D recommendations: A (and WP-30/WP-42) pushes computed-style and visual criteria into specs; D shows CSS-mirroring criteria (exact px, 39 AC paragraphs) were over-specified and 34% of tests then deleted as brittle. Visual references must be oracles at the render layer, not pinned values (WP-106).
C-5. A-19 says drafter judgment rejects "looks disabled" criteria; D-32 shows specs full of exact-px CSS assertions ("logo capped 64px", "column gap 8px"). Either specs were hand-edited past the drafter rule, the rule only blocks vague visual language not numeric, or A misread. Read drafter.md judgment and SPEC-013 history.
C-6. Within D: D-12 says "No visual test existed; deleted 12 Oct" (self-contradictory), and D-33 says the CSS tests were deleted 12-13 Oct while D-19 says base specs "all passed" 4 days before 16 Oct (=12 Oct) although SPEC-004..012 passed 11 Oct and were revised 12 Oct.
C-7. D-37 interprets retry-0 passes as possibly "low adversarial pressure", while D-31 shows other specs needed 6-13 rounds. Same gate, opposite signals; unresolved inference.
C-8. A-27 values mutation survival as discrimination evidence; D-10 shows 296 tests pinned the wrong constant. Mutation testing cannot detect a wrong oracle, so A's reliance on it overstates verification for spec/code disagreements.
C-9. WP-draft WP-56 asserts smith reviewer/mutator/exit-gate/recon and sentinel were "never used in either project"; neither A nor D states this (D shows scribe/muse/navigator-style spec/plan/gate use; says nothing on smith). Source is another file; keep WP-56 conditional until verified.
C-10. A-14 (grep returns nothing for CSS, contrast, responsive, viewport) vs A-37 (diagrams.md "Orin Visual Standard" palette) and the existence of voice.md/assets/brand: those files plausibly contain such words. The "nothing" claim is probably overstated.
C-11. A-74 says gates are not mandatory at runtime (skippable) while D-04/D-05 show that the pipeline was in fact abandoned after 13 Oct: consistent, but it means rigidity was not the blocking factor; absence of sketch/spike modes plus cost was. WP-10/WP-18 should be justified by D-04, not by A's rigidity argument alone.

## 2. CLAIMS TO VERIFY BEFORE ACTING

1. Dangling ranger a11y taxonomy (A-22, A-24): `rg -n -i "accessib" plugins/ranger shared/references/hazards`; `rg -n "accessibility hazard" plugins shared docs`; `git log -S"accessibility hazard" --oneline -- plugins/muse` to confirm a859e2f.
2. "grep returns nothing" (A-14): `rg -n -i "playwright|screenshot|storybook|axe|jsdom|wcag|contrast|viewport|responsive|design token" plugins shared docs`, diff against A's claim.
3. muse verdict@1 vs verdict@3 (A-47): `rg -n "verdict@" plugins/*/agents plugins/*/skills shared/schemas`; read sentinel routing for an artifact_type/verdict version switch. Also open consumer docs/specs/*verdict*.json `$schema`/artifact_type to settle C-2.
4. verdict@3 "scoped pass" semantics (A-79): read shared/schemas/verdict@3.json and sentinel exit-gate.md for a scope field.
5. Line citations (A-82): resolve each against HEAD 9c39614 (`sed -n` on constitution.md, ARCHITECTURE.md, weaver/README.md, smith/README.md, sentinel/skills/gate/SKILL.md).
6. Versions (A-81): `jq` over marketplace.json and each plugin.json.
7. Codex muse path (A-48): `ls harnesses/codex/plugins/muse/skills/component/SKILL.md`.
8. Retry-cap behaviour (C-1): count verdict files and retry_count fields in ~/projects/pages/docs/specs; read muse exit-gate.md retry logic.
9. D counts: `git log --oneline | wc -l` (538), trailer greps for Claude-Session (479) and Entire-Checkpoint (460); `git show --stat` for commits 0ea8be77, c77778b1, 05844c28, a04ddca3, 61c05725.
10. testing-prune-plan numbers (D-33): read docs/proposals/testing-prune-plan.md; 384/1116 = 34.4% arithmetic holds; confirm 28/33 in site-nav-css.test.ts.
11. 760/761/768 band (D-10): read SPEC-013 AC-004/021 and the c77778b1 diff; the "8px band" arithmetic is not self-evident from 760 vs 761.
12. justfile lines 60-66 `runInCI:false`, toHaveScreenshot grep 0, 271 KB budget (D-42/43): `rg toHaveScreenshot`, read justfile, check build output size.
13. Review-3-Oct items "pending verification" (D-25): re-run the specific checks; do not cite as open defects without that.
14. Retry-0 interpretation (D-37): read the verdict JSONs for SPEC-006..012 for blocker/notes and gate timestamps.
15. Whether SPEC-004..012 revisions of 12 Oct were re-gated (D-35): check for new verdict files after 6fb08ba3/f8896db5/1faebc1c.
16. Claim "owner-driven decisions rather than plain bugs" (D-15): requires reading decisions-status.md and the cited commit messages.
17. Docs link docs.orin-dx.com empty (D-28): curl the URL now (state may have changed).
18. Existence of drift-checker runs (D-09): look for any scribe:spec-drift output in consumer repo; the claim "not found by drift-checker" assumes it was never run.

## 3. PROPOSED NEW WPs (group WP-1xx for MAP-1)

- WP-101 ranger TSX/CSS hazard applicability notes: add UI sections to shared/references/hazards/typescript*.md (T7 props dropped before DOM, T9 exhaustive variants, focus-return as failure-swallowed); complements WP-44. Maps A-10.
- WP-102 UI state-modelling reference: <refs>/architecture/ui-state.md (or section in architecture/typescript.md) on state owners, sum types for component states, loading/error/empty; loaded by muse drafter. Maps A-11.
- WP-103 plan@2 render-evidence task kind: navigator planner/challenger and shared/schemas/plan@2 allow a task verification of type render-evidence (screenshot/probe reference) so "looks right" criteria are mechanically attached; depends on WP-30/WP-41. Maps A-12.
- WP-104 weaver exploratory intake: requirement status exploratory (or brief@1) with optional done_when and clarifier bypass; plugins/weaver capture-need and clarify-requirement; route in WP-18. Maps A-35, A-43 (partial).
- WP-105 Rendered-text and link crawl probe: in render-evidence/WP-42, scan for NaN, undefined, [object Object], empty or dead links (docs.orin-dx.com case), missing lang/description; shared/references/verification (ui checks) and a smith/sentinel recipe. Maps D-11, D-28.
- WP-106 Criterion-level brittleness guard: muse drafter/auditor judgment and shared/references/spec rules that route visual facts to token/render-oracle references instead of pinned px/hex ACs; AC size caps by criterion; behaviour-vs-value test policy. Maps D-32, D-33, D-55, C-4, A-19.
- WP-107 Oracle independence rule: smith implementer/reviewer (and navigator challenger) must derive thresholds and expected values from the spec or token source, never from the implementation constant; add to shared/references/verification/evidence.md; complements mutation (C-8). Maps D-10.
- WP-108 Design-decision revision loop: scribe:correct-spec / muse correction mode extended to batch design-decision revisions with revision_note and mandatory re-gate; detect gated specs modified after pass (hash mismatch). Maps D-35.
- WP-109 Defect-corpus replay fixtures: mason:evaluate fixtures built from D-11..D-27 defect classes (NaN, calc() dropped, 760 band, stretched mark, focus clip, landmarks, copy misattribution) with hidden oracles to test whether the new render/copy checks catch them; plugin mason, feeds WP-60. Maps D-54, D-56.
- WP-110 Live-contract view and spec ID scheme: scribe tooling/convention to resolve "Replaces AC-xxx" chains and a/b/c suffixes into a single current view plus supersession status; shared/schemas/spec@2 supersedes fields (WP-30) and scribe spec-drift report. Maps D-52, D-09.
- WP-111 Ship-readiness recipe: sentinel/courier checklist (crawl, SEO/meta, link integrity, size budget, landmark/lang, copy provenance) producing a verdict@3 scoped to the checks run; plugins/sentinel or courier release. Maps D-29, D-43, D-28.
- WP-112 (addition to WP-42, not new plugin file) forced-colours/contrast-mode and reduced-motion probes; D-34 lists forced colours as a parked risk not in WP-42's current list.
