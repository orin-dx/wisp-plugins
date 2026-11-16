# Verifier brief

## Outcome

An independent check whose independence is real: the verifier sees what the work claims and what changed, never how the worker reasoned, and tests each claim by running something.

## Applicability

The verifier runs for shared and irreversible work, and for a spec or plan that makes claims about code (`shared/references/work/modes.md`). It does not run for contained work with executable evidence; the project's checks and the stop hook cover that tier.

## What the caller passes

| Field | Content |
| :-- | :-- |
| Brief | Outcome, constraints and evidence bar, as stated before the work began |
| Tier | `shared` or `irreversible`, and why |
| Change | The diff range or base revision (`<base>..HEAD`, or the uncommitted tree), or the artifact path for a spec or plan |
| Evidence | Each claim the work makes, with the command run and the observed result |
| Not verified | The worker's own list |
| Round | `retry_count` (0 on the first round) and, on a retry, only the prior round's `blockers` |

## What the caller withholds

- The worker's reasoning, plan, scratch notes, transcript or conversation summary.
- Arguments for why a claim holds. A claim and its evidence are enough; persuasion is what fresh context exists to resist.
- Unrelated files or history. The verifier reads the repository itself.

## A brief the verifier can check

- Each outcome is observable: a command's output, a page state, a returned value, a file's contents.
- Each constraint names where it can break: a caller, a contract, a config reader.
- The evidence bar names a command or render, not "tests pass".

A brief that fails these is returned as a fail with a blocker on criterion `brief`. A vague brief brings back the old failure: padding, wording churn, and blockers that cannot be acted on.

## What the verifier does with it

- Treats the brief's outcomes and constraints as the criteria and the evidence list as leads, not proof.
- Runs the changed code on representative and edge inputs from the brief, the build, or a render, per `shared/references/verification/evidence.md`.
- Searches for the same mistake where it is likely to repeat: callers, siblings with the same responsibility, generated copies.
- Returns `verdict@3` with blockers that cite evidence and state the change required.

## Rounds

- Round one lists the complete blocker set.
- The worker fixes only those blockers, then resubmits with `retry_count` 1 and the prior blockers.
- A fail on the second round, or a blocker repeated unchanged, carries an `escalation_required` blocker. The caller stops and gives the owner the persistent blockers; there is no third round.
- An outcome claimed against a baseline ("faster than", "replaces", "matches") stays pending until a result shows both run the same way.

## Disputed findings

When the worker believes a blocker is wrong, or acting on a finding is costly, send that one finding to the adversary instead of arguing in a retry. A `dismissed` assessment with code evidence goes back to the verifier as evidence; `confirmed` or `plausible` stays a blocker or goes to the owner.

## Refutation

The check was not independent if the verifier received the worker's reasoning, if it passed on evidence it did not run or read, or if it ran in the worker's own context. Record any of these in the output's `Not verified:` list.

## Disposition

- Pass: report the verified scope; non-blocking gaps go in the `Not verified:` list.
- Fail, round one: fix the blockers and retry once.
- Escalated: stop; owner decides with the persistent blockers.
