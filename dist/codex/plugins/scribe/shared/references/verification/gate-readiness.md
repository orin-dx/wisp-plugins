# Gate Readiness

What an exit gate checks and how it words a blocker, so the producer can check the same things before submitting. Every first gate in the audited projects failed, and blocker counts rose and fell across rounds (SPEC-001: 18, 5, 6, 0, 0, 2, 0, 6, 2, 3, 2, 8, 3). The cause was incomplete first rounds and issues found late, not a lenient gate.

## Blocker shape

A blocker is one defect that stops the artifact from passing. It carries:

- `criterion`: the criterion id, section, or named check it fails.
- `finding`: the evidence, as a quoted phrase or a location, and the exact change that resolves it. A producer must be able to apply it without a follow-up question.
- `location`: the file, line, field path, or criterion id, when one exists.

A wording-only or style-only issue is a note in `verdict_summary` or a non-blocking `coverage_gaps` entry, never a blocker. Merge blockers that need the same change into one entry that lists every location.

## Rounds

- Round one (`retry_count` 0 or absent): run every check in full and list the complete blocker set. A gate that stops at the first few defects forces extra rounds.
- Retry (`retry_count` above 0): cite only blockers the prior round listed that remain unresolved, or regressions the fix introduced. Record any other newly noticed issue as a `coverage_gaps` entry with `blocking: false`.
- The producer fixes the whole prior blocker set in one pass and rechecks sibling criteria for the same defect before resubmitting.

## Spec checklist

The `muse` and `scribe` gates judge a `spec@1` on these checks. The drafter runs each one against its own draft before returning it and fixes every miss.

1. Every acceptance criterion is a falsifiable proposition: two developers watching the same observable behavior reach the same verdict. No "accessible", "gracefully", "appropriate", "fast", or "as expected" without a measurable condition.
2. No TBD, "to be decided", "if needed", or open question appears in any field. An unknown goes in `non_goals` or `reasoning`.
3. Every error path and invalid input or prop combination is its own criterion with `is_error_case: true`: nil, empty, malformed, out of range, wrong order, and unsupported combination.
4. Every `non_goals` entry exists, and every behavior the requirement names has a criterion or a matching non-goal.
5. Scope fits one planning cycle. If it needs more, split it and say where.
6. `api_surface` signatures match live source when the spec names existing code.
7. `acceptance_criteria` ids are unique and every criterion states one condition and one observation.

Component specs (`muse`) add these checks:

8. Every interactive state the props or requirement imply (default, hover, focus, active, disabled, loading, error, empty) has a criterion or an explicit non-goal.
9. Accessibility is stated as testable behavior: role, accessible name, focus order, keyboard operation, and any live-region or state announcement.
10. Each invalid prop combination is an error-case criterion naming the combination and the observable result.

## Use

Before returning, list each check that the draft fails, fix it, and recheck that fixes did not break a neighboring criterion. Do not add criteria beyond what the requirement and the checks call for.
