# Decision cards

## Outcome

The owner decides only what changes scope or cannot be undone, in under a minute per decision, and the answer survives the session.

## Applicability

Raise a card when the answer changes scope, behavior other work depends on, or cost the owner carries, or when the next action is irreversible (`shared/references/work/modes.md`, Tiers and Autonomy). Everything else proceeds on a stated assumption: write `Assumption: <the answer the work proceeds on>` in the reply and keep going.

No trigger, no card. A preference question, a naming choice, or a step the repository already answers is not a card.

## Shape

```text
Decision: <the question, one line>
Why now: <the trigger and its evidence: a file, a failing check, a cost>
Options:
  A. <option> — cost, risk, reversibility
  B. <structurally different option> — cost, risk, reversibility
Recommendation: <A or B>, confidence <high | medium | low>, because <reason>
Default if unanswered: <what happens, and when>
Expires: <the point after which the card is withdrawn or the default applies>
```

- **Options differ in structure,** not in a parameter of one idea. If only one real option exists, say so and ask for a yes or no.
- **What would change the answer:** one line, when a fact the owner may know would flip the recommendation.
- **Irreversible actions have no default that acts.** The default for a publish, push, deletion or migration is to wait.

## Limits

- At most three open cards at once; batch them in one message, most consequential first.
- Do not repeat a card the owner already answered; fold the answer in.
- Do not ask before reading what the repository says: `AGENTS.md`, ADR guardrails and existing specs answer many questions.

## Encode the answer

A decision that lives only in a chat or in memory is lost. When the owner answers:

- A rule for every session goes in `AGENTS.md`, or becomes a check (a hook, a test, a lint) when a machine can decide it.
- An architectural choice that passes both gates in `shared/references/architecture/decision-records.md` gets a decision record.
- A scope answer goes in the brief, the spec's `scope`, or the pull request body, wherever the next reader acts on it.

## Refutation

A card is wrong when the repository already decides the question, when the answer would not change what is built, or when it hides a recommendation the agent could act on reversibly. Proceed on an assumption instead and list it in the output.

## Disposition

- Answered: encode it and continue.
- Unanswered by expiry: apply the stated default, or keep waiting for an irreversible action, and say which.
- Declined: record the decision as declined with the reason, so it is not raised again without new evidence.
