# ADR-018: The core is one work skill and one verifier, split by context and risk

**Status:** Accepted
**Date:** 2026-11-15
**Supersedes:** ADR-003 (agents split by cognitive mode) and ADR-007 (a persona id for every lifecycle plugin), and ADR-001 in part: its premise that the ecosystem is many role agents, each owning one stage. Its agent section structure, with its later amendments, stands.

## Decision

Work is decomposed by context and risk, not by lifecycle stage, role or cognitive mode.

- **Plugins:** `wisp` is the core; `courier`, `muse` and `mason` keep their ids; `wisp-packs` holds optional specializations. The lifecycle plugins are retired and what they knew becomes references loaded on demand.
- **One entry:** the `work` skill states a brief (outcome, constraints, evidence bar), sizes the change as contained, shared or irreversible, and picks a mode. `explore`, `spike`, `fix`, `build`, `check` and `ship` are one-line aliases into it.
- **One worker:** the primary agent researches, implements and tests in one context; forking a read-only search is a context split, not a role.
- **One independent check:** `wisp:verifier` gets the brief, the change and the evidence, never the worker's reasoning, runs things itself, and returns `verdict@3` under the round rules of ADR 013 and ADR 015. It runs for shared and irreversible work and for specs or plans that make claims about code.
- **Two helpers:** `adversary` settles one disputed finding; `recon` inventories an unfamiliar workspace.
- **No mandatory stages:** a spec or plan is written only for a shared contract or when the owner wants one. The owner sees a brief and decision cards in; the diff or render, evidence, a `Not verified:` list and the pull request out.
- **Must-hold rules are hooks:** a Stop hook asks once for the `Not verified:` list when changes are left uncommitted; the handback validator checks the verifier's `verdict@3`. Codex skills state both rules, because Codex has neither hook.

## Why

- **Agents are not a team of people:** role agents and handoff documents reproduced ceremony, and each handoff lost context.
- **Value sat in early independent checks:** first-round checks against code or a build produced the documented catches; later rounds, duplicate reviews and per-stage gates mostly added cost.
- **The pipeline mostly did not run:** work happened in general-purpose forks that rarely reached the skills, so their checks rarely ran. One entry is easier to reach.
- **Cost should follow risk:** the tier sets review depth, so contained work pays for executable evidence only.

## Rejected

- **Trim the pipeline and keep its stages:** because chained agents and mid-pipeline artifacts are the handoff pattern the evidence argues against, with the largest resident footprint.
- **One agent with hooks and tests only:** because it drops the independent first-round check that produced the catches; it survives as the contained tier.
- **One agent per cognitive mode:** because splitting evidence-gathering from judgment split context more than it protected judgment; the verifier does both in one fresh context.

## Consequences

- **Now true:** a handful of descriptions instead of dozens, and one place where independent verification lives; ADRs 011 to 016 still apply.
- **Cost:** consumers of the retired plugins lose those ids and skills; a long task can grow one context past what compaction preserves (fork a sub-task; do not add a role).
- **Risk:** the verifier's independence rests on fresh context and a checkable brief; a vague brief brings back padding and churn, so the verifier fails a brief with no evidence bar.
- **Revisit when:** paired fix-task sequences (`docs/evaluation-runbook.md`) show the verifier missing defects the retired spec or plan gates caught, a logic-bug class only a separate role caught, or a bare arm tying this design on hidden checks at lower cost above the contained tier.

## Evidence

- **Enforced by:** `tests/test_wisp_core.py` (agent set, tiers, description caps, aliases, hook behavior and registration) and `shared/hooks/validate-handback.py` (routes `wisp:verifier` to `verdict@3`).
- `docs/design/agent-native-architecture.md` (architecture B and the strategic layer); `docs/evaluations/frontend-design/IMPLEMENTATION-LOG.md`, "Evidence review and ADR 015".
