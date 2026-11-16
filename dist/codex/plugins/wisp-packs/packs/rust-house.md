Applies when the repo is a Rust workspace (a `Cargo.toml` with `[workspace]`). The model knows Rust; this lists only where our repos differ from its defaults. Rules hold in at least two of callisto, caliper and monokl; the repo's own AGENTS.md wins where it differs.

Each rule ends with what enforces it: `[lint]` a lint or CI job, `[type]` the shape of the types, `[review]` nothing but review. Treat `[review]` rules as the likeliest to have drifted and check them in the area you touch. Run only the checks the repo declares (justfile, CI); say so when a check named here does not exist.

## Failure handling

- No `unwrap()` outside tests. `expect`, `panic!`, `unreachable!` and `todo!` follow the repo's lint table: where it denies them, use `?`; where it allows `expect`, the message names the invariant that makes the failure impossible. `[lint]` `unwrap_used` and friends in `[workspace.lints.clippy]`, run with `-D warnings`.
- `unsafe_code` is forbidden or denied workspace-wide, and `unused_must_use`, `let_underscore_must_use` and `map_err_ignore` are denied. A crate opts in with `[lints] workspace = true`. `[lint]`
- Failures are typed enums (`thiserror`; `miette::Diagnostic` for user-facing errors, with a stable code and a fix). No `String` variant when a structured one is possible; compose with `#[from]`/`#[source]`. Public error enums are `#[non_exhaustive]`. `[review]`
- Never degrade silently: a skipped file, dropped item or defaulted value emits a diagnostic or a count. When one sibling of a family starts failing loudly, convert the rest in the same change. About 20 of 406 review findings in these repos are silent degradation (an over-size file skipped with no count; one lookup answering `null` where its siblings now error). `[review]`

## Types and API shape

- No `_` arm on a match over an enum this workspace owns; a compile error on a new variant is the point. Prefer `match` over `matches!` for the same reason. `[review]` (clippy cannot scope the lint to owned enums, so it is off.)
- Make the wrong thing unrepresentable before testing for it. Use the first rung that works: a type or private constructor; an exhaustive match; a lint already in the workspace table; one small test of observable behavior; nothing. Delete a check a type now covers before adding another. `[type]`
- Newtype where a bare type allows confusion; an enum instead of a `bool` parameter that hides intent; destructure structs explicitly so a new field is a compile error.
- `pub(crate)` for implementation modules, `pub` only for the consumer API. A new `pub` type derives `Debug`, implements `Display` when it appears in output and `Error` when it is a failure,; `#[must_use]` goes on functions whose result must not be dropped.
- Wire or don't define: a new abstraction or helper has a real call site in the same change, and a new shared helper migrates every call site or the rest are tracked. `[review]`
- Internal hot-path maps are `FxHashMap`/`FxHashSet`; anything serialized is a `BTreeMap` so output order is deterministic. Paths are `camino::Utf8Path` unless a path may not be UTF-8. (caliper and monokl state both; callisto uses `IndexMap` and `std::path`, so apply them only where the repo already does.) `[review]`
- Prefer a crate already in `Cargo.lock` over a hand-written grammar: `semver`, `thiserror`/`miette`, `clap` derive, `serde`, `insta`. A dependency is added to a crate only when its code uses it, and its version is pinned once in `[workspace.dependencies]`. `[lint]` `cargo machete`, `cargo deny` where declared.

## Tests

- Assert the exact value, not presence: `assert_eq!` over `contains`, `is_some` or "does not panic". A test of "X exists" survives X holding stale data. `[review]`
- A fix gets a test that fails on the original bug. A function that mirrors an already-tested one (watch mode beside batch mode, a second ecosystem beside the first) gets a test asserting the same contract: sibling paths are where coverage lapses.
- A test of a specified failure asserts that failure (the diagnostic code, the exit code), not only "it failed": any other failure would pass. A stub applies the logic it replaces (a fake `gh` that ignores `--jq` leaves the filter untested). A test never reads the code under test as text, and never mirrors the implementation's own constants back at it.
- Snapshots (`insta`): accept a change only after confirming the new output is correct, not merely different.
- Tests earn their place by covering a behavior, edge or error state, not a line. Do not scan source text for strings that code can expose directly. Do not keep hand-maintained lists that mirror code or config (error codes, command names, the crates a release script loops over, option keys): derive them from the type or the config that owns them, and state a fact in one place.
- Tests run with the repo's runner (`cargo nextest` plus doctests where declared). Coverage thresholds belong to the repo's recipe; never lower one to pass. `[lint]`

## Fixing a bug

- Search for structurally identical code (same algorithm in another file, ecosystem or mode) and fix siblings in the same change. A sibling left alone is recorded where the repo records such things: a changeset note, a tracked follow-up or a comment. Several copies of one logic become one implementation.
- Done means: the repo's CI-equivalent recipe passes, judged by exit code and never by grepping output (a compile error prints no "failed" line); docs, comments and tests describing the old behavior are updated or removed; a check that has not run is reported as pending.

## Comments and docs

- A code comment states only a non-obvious why. No history ("used to", "previously": the commit records it), no spec, criterion or plan IDs (specs change; say what the code guarantees). Fill to 120 columns (`rustfmt.toml`); rewriting a block counts as writing it, so re-fill and cut. A comment, doc, help text or report that claims what the code no longer does is the most common finding after logic bugs (95 of 406 findings mention one, by keyword). When behavior changes, search docs, help output, comments and tests for the old claim, and make sure any file, section or command a comment cites exists at this commit.
- Public items: first doc line is one third-person sentence ending in a period; link types by name; add `# Errors`, `# Panics` or `# Examples` only when they carry information.
- Read the matching ADR (`docs/adr/README.md`) before changing what it guards. Reversing one needs a new ADR the owner accepts.

## Cargo hazards

- Run one cargo command at a time: parallel builds serialize on `target/`'s lock. Scope while iterating with `-p <crate>`.
- A `Cargo.lock` diff means investigate, not `checkout` it away.
- `deny.toml` is the license, source and advisory policy: widening an allowlist or adding a skip needs the owner.

## Exemplars

- Error enum: `crates/monokl/src/error.rs` (monokl). User-facing diagnostics with codes and help: `crates/callisto-cli/src/error.rs` (callisto).
- A complete public type: `crates/core/src/types/diagnostic.rs` (caliper).
- An architecture test that enforces a boundary by script: `crates/callisto-graph/tests/architecture.rs` (callisto). Its own file says it is a coarse tripwire; prefer a type.
