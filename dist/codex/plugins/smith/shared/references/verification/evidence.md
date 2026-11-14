# Verification Evidence

Choose evidence from the changed risk and the workspace's available capabilities. Do not run every method by default.

## Method selection

- Examples: bounded behavior with clear representative cases.
- Property or fuzz testing: parsers, combinatorial inputs, state transitions, graph logic, or round trips. Name the generated domain and a meaningful oracle or invariant; a no-panic check alone rarely proves behavior.
- Mutation or deliberate fault: show that tests distinguish an important wrong implementation from the intended one.
- Boundary testing: exercise the contract implicated by the change, feeding real producer output to the real consumer where a format crosses it; a missing key fails instead of defaulting. Name any mocked segment and why the remaining boundary is sufficient. A test double accepts only what the real tool accepts and applies the logic it stands in for.
- Environment testing: exercise only environment assumptions that can change the outcome, such as runtime version, PATH, working directory, build tags, packaging, or CI configuration. Run what CI runs, from a clean state, before reporting a change verified; a narrower local check is a coverage gap. A failure seen in only one environment, or only sometimes, is a defect until a cause is shown, including on the main branch.
- Declared requirements: compare what the change declares (peer ranges, engines, minimum versions, pins) with what the code now needs, and exercise the declared minimum.
- Generated output: exercise generated files such as workflows, templates, and configs the way their consumer receives them; matching golden bytes does not show they work.

Prefer project-configured commands and installed tools. A missing optional tool is a coverage gap, not permission to install it or fabricate a result.

## Language-service evidence

Language-server diagnostics and symbol queries are supporting boundary evidence only when the report records the backend identity/version, negotiated capability, and document or workspace version/content identity. A response for stale content, an unadvertised capability, or an unknown backend cannot support a pass.

Prefer the repository's compiler, type-checker, test, or other project-configured command for terminal correctness evidence. Language-service feedback is especially useful for targeted semantic checks and editor-only behavior, but protocol silence does not prove correctness and many servers degrade unresolved states without a wire-level confidence field.

Run diagnostics after a coherent mutation or subsystem batch, not mechanically after every individual edit. Related edits may intentionally create a transient invalid state; verify at the nearest boundary where the changed behavior is expected to be coherent. If only language-service evidence is available, record that limitation as a coverage gap.

## Evidence quality

Record the claim, actual command or inspection, observed result, and remaining gap. Report a claim as done only after reading its result: a check still running is pending, and another agent's or worker's summary is a lead, not evidence. A filter, limit, or skip that drops inputs reports how many and why, so "could not check" differs from "checked, nothing found". A measurement uses the consumer's configuration, times only the measured work, and states its sample size. Generated tests also record the generator and oracle. External state records an immutable identity and observation time when it affects the decision.

A test discriminates behavior when a controlled mutation, deliberate fault, isolated prior revision, or equivalent evidence makes it fail for the relevant wrong behavior and pass for the corrected behavior. Do not modify shared worktrees or user state merely to manufacture a red run.

Structure is not behavior. A type, export, file-layout or schema-shape check does not show that changed logic works: run the changed code on representative and edge inputs taken from the criterion or the reported defect, and compare what it returns with what the criterion says. For a visual or interactive change, inspect the built page where a browser is available (computed styles, accessibility tree, contrast, target size); passing markup tests do not show the page renders correctly.

Before completion, every started verification task has a terminal result that was read, or is explicitly excluded from the verified scope.
