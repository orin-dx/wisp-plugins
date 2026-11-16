Applies when the repo has TypeScript packages or apps built with pnpm (a `tsconfig.json` and a `pnpm-workspace.yaml` or `package.json` scripts). The model knows TypeScript; this lists only where our repos differ from its defaults. Rules hold in both pages and caliper's TypeScript packages; the repo's own AGENTS.md wins where it differs. UI, design-token and brand rules are out of scope.

Each rule ends with what enforces it: `[lint]` a lint, format or type check, `[review]` nothing but review. Run only the checks the repo declares (justfile, package scripts, moon tasks, CI); say so when a check named here does not exist.

## Toolchain and gates

- The toolchain is pinned in `.prototools` (node, pnpm, and moon where used). Install and run through it; do not bump a pin without the owner. Use `pnpm`, not npm or yarn.
- A tool resolves paths from the directory it runs in. `pnpm --dir <package>` and `--filter` run from the package, so a relative path the user passed (a corpus root, an output directory) must be made absolute before the hand-off, and the oxlint Panda rules bind the config found from where oxlint runs. Run from the project root or through the repo's task runner (two caliper findings, one pages rule).
- A pnpm script whose name is also a pnpm command runs as `pnpm run <script>`: `pnpm ci` deletes `node_modules`, `pnpm run ci` runs the repo's script.
- Lint is oxlint with `correctness`, `suspicious`, `pedantic`, `perf` and `style` all at `error` (the same disabled-rule list in both repos; production code gets all of it). Fix the code. A rare inline disable names one rule and a reason (`// oxlint-disable-next-line <rule> -- <why>`); never a blanket disable or a config change to pass. Loosening `.oxlintrc.json` needs the owner. `[lint]`
- Format is oxfmt: `printWidth` 120, no semicolons, single quotes, `proseWrap: never`. Run the repo's format check, not Prettier. `[lint]`
- Types: `strict: true` stays on; do not weaken a compiler flag to make code pass. Type-only imports use `import type`. `tsc` is the typecheck and, in published packages, the build. `[lint]`
- Generated files (`styled-system/`, `binding.d.ts`, `dist/`) are never hand-edited or committed unless the repo already commits them; change the source or script and regenerate. They are already in the lint and format ignore lists.

## Types

- Model domain values and validated inputs with explicit types, including in tests and fixtures. Where the repo bans `any` and `unknown` (pages does; caliper's oracle tooling is the exception), do not author them or cast through them. `[review]`
- A string key that crosses a script, process or language boundary comes from one exported constant or type, never retyped: an oracle emitted `less precise` while a script read `less_precise` and silently recorded zero. A module copied between packages and kept equal by a test that diffs the text is one module with two importers.
- Public options and data shapes are typed interfaces with a doc comment that states the default and what happens when it is off. Prefer a union of string literals over a bare `string` or a boolean pair that can contradict (`skipHtmlProps` vs `htmlAttributes: 'none'` states which one wins).

## Tests

- `vitest`. Test behavior: results, state, thrown errors, events, ordering, accessibility semantics. Do not pin incidental detail (class names, pixel values, generated output) while a design is still changing. `[review]`
- Assert the exact value: `toStrictEqual`/`toBe` on the whole result, not `toBeDefined` or `toContain` on a piece. A test of "X exists" survives X holding wrong data. A test of a specified error asserts that error, and a test never reads the code under test as text.
- Prefer a test that makes a rule a check over prose: a vocabulary or contract that must stay closed gets one small test that fails when someone adds a new case. See the exemplar.
- A unit suite that mocks a boundary (the native binding, the network) is paired with at least one test through the real boundary; say which ran. Integration and browser suites run only when the repo says so (they may be manual).
- A fix gets a test that fails on the original bug. A function that mirrors a tested one gets a test asserting the same contract.

## Fixing and finishing

- Search for structurally identical code (same logic in another package or entry point) and fix siblings in the same change; record a sibling left alone where the repo records such things.
- Done means the repo's CI-equivalent recipe passes (for example its `ci` or `check` recipe), judged by exit code and never by grepping output. Scope to one package while iterating with the repo's own filter (`pnpm --filter <package> <script>` or `moon run <project>:<task>`), then run the whole gate before handoff. A check that has not run is reported as pending.
- Never hard-wrap Markdown or commit messages: one line per paragraph. A code comment states a non-obvious why only, with no history and no spec or plan IDs, and any file, section or command a comment or doc cites exists at this commit. When behavior changes, search docs, help text, comments and tests for the old claim.

## Exemplars

- A contract held by a small test: `packages/foundations/src/widthSteps.test.ts` (pages). It fails when a new `max-width` condition appears, and asserts exact key lists.
- Typed public options with documented defaults: `packages/vite-plugin/src/options.ts` (caliper).
- Lint and format config to match: `.oxlintrc.json` and `.oxfmtrc.json` at the root of either repo.
