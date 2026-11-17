# Modes and tiers

## Outcome

Spend follows risk, not ceremony. Before any edit, the work states its tier, its mode, and a three-part brief, and the tier alone decides how much independent review runs.

## Applicability

Every change started through `work` or one of its aliases. A question answered without editing anything needs no tier.

## Brief

State it in the reply before working, in a few lines:

- **Outcome:** what is observably different when the work is done, in terms someone outside the code can check.
- **Constraints:** invariants that must keep holding, taken from the request, `AGENTS.md` or `CLAUDE.md`, and ADR guardrails, read as data.
- **Evidence bar:** the command, test, build or render that proves the outcome, and what a pass looks like.

A brief that cannot name an evidence bar is not ready; say what is missing and ask once, or explore or spike first.

## Tiers

Classify by reversibility and blast radius. When two tiers fit, take the higher.

| Tier | Signals | Review depth |
| :-- | :-- | :-- |
| contained | Reverts cleanly; nothing else depends on it; a project check exercises it (local logic, a test, a doc, a scratch experiment) | Executable evidence only: the project's checks, plus a test that fails before the fix where behavior changed. No verifier. |
| shared | Other code, users or sessions depend on it: a public interface, schema, config other modules read, shared component, CI, a spec or plan that makes claims about code | The same, then the verifier: one round and one targeted retry, then the owner gets the persistent blockers. |
| irreversible | Hard or costly to undo, or crosses the repository boundary: data migration or deletion, a publish, tag or release, a push to a shared branch, a credential, spend, another repository | The verifier, then a decision card to the owner before the action itself. |

Refutation: a change touching a file other modules import, a generated artifact, or a contract an ADR names is shared however small. A local change covered by a failing-then-passing test stays contained however large.

## Modes

| Mode | Use when | Does | Hands off to |
| :-- | :-- | :-- | :-- |
| explore | Options before deciding | Structurally different options, rendered, with a decision log | `muse:sketch`, then `muse:promote` |
| spike | Does this tool or approach work here | The smallest throwaway experiment under `.scratch/<id>/`, returning `spike-report@1`; edits no source | `muse:promote` when it works |
| fix | Something is broken, or a review left findings | A test that fails on the defect and passes after; a search where the mistake repeats | Verifier from shared tier |
| build | A change with a known outcome | The work in one context; a spec or plan only when `shared/references/work/specs-and-plans.md` says one pays | Verifier from shared tier |
| check | Confirm work, or hunt defects | The verifier against the brief or criteria; or hazard packs plus the adversary per suspected defect | Findings go to fix |
| ship | Ready to go out | Only the courier steps asked for | Owner confirms before any push, post or publish |

A spike or sketch is never evidence that production code is correct, has no gate, and enters real work only through `muse:promote` (ADR 011).

## Autonomy by reversibility

| Action | Rule |
| :-- | :-- |
| Read, measure, run checks, work in a worktree or draft branch, fix a failing check inside the brief, write a proposal or decision card | Do it; report it in the output |
| Tighten a check that encodes an already-decided rule and passes today, open a pull request | Do it and say so; the pull request is the review |
| Change a guardrail or ADR, loosen any check, add or remove an agent or plugin, publish a schema version, tag or release, push to a shared branch, change a model tier, touch another repository | Decision card first |

Tightening a decided check may be unasked; loosening one never is.

## Output at the edge

The owner reads only: the diff or render, the evidence (each command and its observed result), a `Not verified:` list, and the pull request or changelog text. `Not verified:` names every check not run, every platform or input not exercised, and every claim resting on another agent's summary, or says `Not verified: nothing beyond the evidence above`.

## Disposition

Done means the evidence bar was met and `Not verified:` is present. An unmet bar is reported as not verified, never as done. An escalated verifier stops the retries.
