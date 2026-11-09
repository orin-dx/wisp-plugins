# Pipeline Walkthrough

A concrete example tracing one feature request through the full lifecycle pipeline. The scenario: *"requests to our upstream API sometimes hang forever — we need configurable timeouts."*

This walkthrough shows what each handoff carries, why typed contracts matter, and how the ranger audit loop feeds back into the design stage.

---

## The Scenario

A backend team files an issue: requests to an upstream service occasionally stall with no response. The fix is adding a configurable timeout to the HTTP client. Simple enough — but the most common implementation mistake is capturing the timeout in a config struct and never passing it to the actual HTTP call. The hazard has a name: **T7 (Write-Only Fields / Intent-Capture-to-Execution Discard)**.

This walkthrough shows how the pipeline catches that bug before it ships, and how ranger's finding feeds back into a structural spec rather than a one-off patch.

---

## Stage 1 — weaver: Need

The user invokes the `weaver` skill. `intake` (sonnet/medium) converts free text into a structured requirement. `clarifier` asks one targeted question if the success condition is ambiguous. `auditor` (sonnet/medium) checks for testability.

**Output: `requirement@1`**

*Shape: see the schema named above in `shared/schemas/`; `tests/fixtures/cross-harness/lifecycle.json` holds a validated example chain.*

`reasoning` is a private scratchpad. It is never forwarded to the next stage.

---

## Stage 2 — vanguard: Research

`vanguard` receives `requirement@1`. `recon` (haiku/low) builds a workspace manifest. `reader` (sonnet/medium) reads relevant source files. `risk-assessor` (sonnet/medium) identifies what could go wrong. `synthesizer` (sonnet/medium) produces the research report.

**Output: `research-report@1`**

*Shape: see the schema named above in `shared/schemas/`.*

---

## Stage 3 — scribe: Spec

`drafter` (sonnet/medium) turns the requirement and research report into a testable spec. `verifier` (sonnet/medium) checks every acceptance criterion against the source artifacts — not the codebase. `auditor` (sonnet/medium) hunts vague language. `exit-gate` (opus/high) issues a binding pass or fail.

**Output: `spec@1`**

*Shape: see the schema named above in `shared/schemas/`.*

Notice `ac-1` directly addresses the T7 risk `vanguard` found: the spec requires the field to *reach the builder call site*, not just exist in the struct. This is the enforcement the research recommended.

---

## Stage 4 — navigator: Plan

`planner` (sonnet/medium) decomposes the spec into sequenced tasks, each with an implementation approach, exact code, and the tests proving its criteria. `estimator` (sonnet/medium) adds sizing. `challenger` (sonnet/medium) pressure-tests the sequence for hidden dependencies.

**Output: `plan@1`** (abridged)

*Shape: see the schema named above in `shared/schemas/`.*

---

## Stage 5 — smith: Code

`recon` (haiku/low) reads the manifest from `plan@1`. `implementer` (sonnet/medium) executes each task — design the approach, write the implementation, write comprehensive tests proving the task's criteria, confirm the suite passes. `mutator` (sonnet/medium) runs cargo-mutants after each task to verify the tests would actually catch a wrong implementation.

**Mutation gate: mutator catches the T7 bug**

**The mutation gate catches a slot-swap bug the unit test missed.**

- `implementer` inverts the condition — mapping `read_timeout_ms` to the connection slot instead of `connect_timeout_ms`
- The unit test passes because it checks the Duration value, not which builder slot it went into
- The surviving mutant is the specific code path that was never killed — `mutator` returns a precision test targeting exactly that slot assignment

**Output: `mutation-report@2`**

*Shape: see the schema named above in `shared/schemas/`.*

`mutator` re-invokes `implementer` with the precision test. The implementer fixes the slot assignment and both tests pass. `exit-gate` confirms the mutation evidence and later issues `verdict@3`.

---

## Stage 6 — ranger: Audit (cross-cutting)

**`ranger` runs independently of the main pipeline — typically before a release.**

- `recon` (haiku/low) — builds the workspace manifest: live files, dead files, language detection
- `scanner` (sonnet/medium) — searches hazard-taxonomy candidate signals across all live files without adjudicating them

For this codebase, the scanner surfaces a T7 candidate: an `AccessConfig` struct whose `private_registry` field is captured from user config but never reaches the publish command.

`boundary-tracer` (sonnet/medium) is dispatched because T7 was found. It traces every field in `AccessConfig` to determine which reach the execution boundary.

**Output: `field-survival-map@1`**

*Shape: see the schema named above in `shared/schemas/`.*

`adversary` (opus/high) confirms the finding is real — user-specified registry is silently overridden by the hardcoded default. Ranger groups it with related instances before remediation.

**Output: `finding-report@2`** (abridged)

*Shape: see the schema named above in `shared/schemas/`.*

---

## The Ranger → Scribe Loop

**`architect` designs a structural fix — not a patch.**

- A patch would add `private_registry` to the existing `publish()` parameter list — it would fix this one field but leave the narrow type intact, ready to silently drop the next field that gets added
- The structural fix widens the parameter type to accept the full `AccessConfig` directly, eliminating the class of bug rather than the instance

`architect` receives `finding-report@2` and specifies this correction.

**Output: `spec@1` (structural)**

*Shape: see the schema named above in `shared/schemas/`.*

This spec re-enters the pipeline at `navigator` for planning, then `smith` for implementation. The fix is structural — the next field added to `AccessConfig` reaches the subprocess automatically.

---

## What This Demonstrates

| Principle | Where it appeared |
| :--- | :--- |
| **Schema-driven handoffs** | Each stage received a typed document. `synthesizer` couldn't omit the risk finding without schema validation failing. |
| **EARS output contracts** | `spec@1` ac-1 is an EARS statement — it makes the T7 risk machine-checkable, not advisory. |
| **Cognitive mode separation** | `scanner` found T7 candidates without filtering. `boundary-tracer` traced field survival. `adversary` verdicted. Three agents, three modes, none contaminating the others. |
| **Mutation gate** | `mutator` caught the slot-swap bug that unit tests missed. The precision test it generated became part of the permanent test suite. |
| **Ranger → scribe loop** | The finding didn't produce a patch. `architect` designed a structural fix that makes the whole class of bug a compile error. |
