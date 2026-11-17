# ADR-008: Drop mandatory write-test-first ordering in smith

**Status:** Accepted
**Date:** 2026-09-01

## Decision

`smith`'s `implementer` and `navigator`'s `planner` no longer require a failing test before implementation; `mutator` verifies test quality instead.

- **Implementer cycle:** read the criteria, design the approach, write the implementation, write tests proving each `covers_criteria` criterion, run the full suite, commit.
- **Planner tasks:** a task states a brief implementation approach, decided first, then the exact implementation and the exact tests. It no longer carries "a failing test written before any implementation code" or "expected failure output", and the order of implementation and tests is not mandated.
- **Test quality:** `mutator`'s mutation gate is unchanged; a surviving mutant is the signal that a test does not check what it claims, whichever was written first.
- **Unchanged:** `mutator`, `reviewer` and `exit-gate`.
- **Bug repair keeps red-green:** reproducing the failure before fixing it stays the practice (`shared/agent-best-practices.md`, "Repair"), because proving the bug is real is a causal reason that does not apply to fresh feature work.
- **ADR 003:** this narrows its "minimum change + red-green verification" for `implementer`'s fresh implementation only; 003 is left as written.

## Why

- **The red phase is a human aid:** its stated value, confidence and discipline, is psychological and does not obviously transfer to an agent.
- **Comparison found no benefit:** Birgitta Böckeler's controlled comparison of TDD and non-TDD agent workflows (martinfowler.com, "TDD inside the agent loop — theater or actual value?") found no quality difference under blind model judging and no meaningful difference in mutation scores, at several times the tokens for TDD.
- **TDD fights up-front design:** TDD runs let the design emerge from locally minimal steps and land on whatever shape the first test fixed; non-TDD runs designed architecture, types, edge cases and contracts before any code or test.
- **The gate was doing the work:** `mutator` already ran after every task regardless of write order.

## Rejected

- **Keep strict test-first for every task:** because it cost several times the tokens with no measured gain in quality or regression catching, and it pushed design onto the first test.

## Consequences

- **Now true:** lower token cost per task, and the approach is chosen before a test can lock it in.
- **Cost:** the safety net rests wholly on mutation testing. Where a workspace has no mutation tool, `mutator` records a coverage gap instead of blocking (existing behavior), so test-quality assurance is weaker there than under strict TDD. This is an accepted tradeoff.
- **Limit:** the basis is one practitioner's comparison, not this ecosystem's own agents.
- **Revisit when:** this repo's own tasks show a different result, decided by measuring, not argument.

## Evidence

- The Böckeler article above; the change is commit `25d87a73`. This repo has run no controlled comparison of its own.
