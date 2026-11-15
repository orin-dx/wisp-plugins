# Agent-native architecture: design it twice

Status: proposal for the owner, not a decision. No plugin, agent, skill or schema changes with this document, and it is not an ADR. If the measurement in section 5 supports a change, a record follows under [`shared/references/architecture/decision-records.md`](../../shared/references/architecture/decision-records.md), superseding what it reverses (ADR 001, 003 and 007 are the likely ones).

The question: the plugins mirror a human organization (role-named agents, handoff documents, sign-off gates). Agents are not a team of people, and models trained on human organizations reproduce that ceremony unless asked not to. What shape should the architecture take instead, and how do we find out?

Method: each option below is chosen by a different **unit of decomposition**, because the options must differ in structure, not in parameters. A splits by lifecycle stage and role. B splits by context and risk. C splits by what a machine can check.

## 1. Goal and constraints

**Goal for the owner.** Set direction once, and read only what matters: a brief and decision cards in; a diff or render, the evidence, a list of what was not verified, and the changelog or PR out. Spend scales with risk, not with ceremony. Must-hold rules are enforced, not requested.

**Goal for agents.** Work from outcome, constraints and an evidence bar rather than a procedure. Hold the full context of one change. Be checked by something a machine can run. Get independent review only where a confident mistake is costly or irreversible.

Constraints used in the comparison (C1 to C10):

- **C1, owner attention:** artifacts reach the owner only at the edges and at decisions that change direction.
- **C2, cost follows risk:** tokens, rounds and review depth scale with reversibility and blast radius.
- **C3, independent check where it pays:** fresh-context verification where a confident mistake is costly or irreversible.
- **C4, must-hold rules are deterministic:** hooks, tests, types and lints, not prompts.
- **C5, reached by default:** the right path runs without the model having to choose a skill.
- **C6, full context for the worker:** pieces that must be read together are joined (Ousterhout), without becoming one mega-agent.
- **C7, strategy is asked for:** the architecture contains the explicit step that asks "what should be structurally different", because models do not volunteer it.
- **C8, resident footprint:** always-loaded descriptions and plugins are a cost.
- **C9, migration cost and reversibility:** what existing records, schemas, tests and Codex counterparts must change.
- **C10, portability:** Claude Code and Antigravity share the authored tree, Codex has its own; hooks exist on each host but differ ([ARCHITECTURE.md](../../ARCHITECTURE.md) section 8).

**Evidence base shared by all three, and its limits.** One author, five projects, September to November 2026, single runs for nearly every pilot. Records: [Evidence review and ADR 015](../evaluations/frontend-design/IMPLEMENTATION-LOG.md#evidence-review-and-adr-015), [ADR evidence](../evaluations/frontend-design/IMPLEMENTATION-LOG.md#adr-evidence), [the architecture review](../evaluations/frontend-design/ARCHITECTURE-REVIEW.md), [the assumptions register](../architecture-assumptions.md) (rows 2, 7, 8, 9, 14 are the ones this touches).

- **Value came from first-round independent checks against code or a build.** Repeated rounds, duplicate review of one draft, per-commit review and mutation on logic-free code were waste. The catch-rate counts are approximate in part (reconstructed from an agent's notes).
- **"No reviewer caught a logic bug" is an absence in a sample, not a proof.** Humans found logic bugs (28% of human-found findings), so the gap is real, but the sample cannot say reviewers could never catch them.
- **77% of subagent tokens went to ad hoc forks and general-purpose agents.** Those are reported tokens, not a bill, and forks are not all waste; the figure says where work happened, not that it was wasteful.
- **Plugin agents mostly ran without their skills** (7 skill calls in 812 transcripts), so the checks inside skills mostly did not run ([unused agents](../evaluations/frontend-design/investigations/unused-agents.md)).
- **The cost figures from TokenEconomizer** (pruning unused tools was the largest saving; failed trajectories take about a third of spend) are the owner's citation. They were not re-read for this document and carry the `vendor-run` and `testimonial` cautions of [evidence quality](../evidence-quality.md) until they are.
- **No arm has been run against another.** Nothing here is a comparison of A, B and C; section 5 is how to get one.

## 2. Three structurally different architectures

### A. Today's plugins, trimmed

**Shape.** The lifecycle pipeline as it stands after [ADR 015](../adr/015-two-rounds-one-reality-check.md) and the routing guard: 11 plugins, 44 agents, 39 skills (counted in `plugins/` now). `guide` offers six intent commands that hand off to the existing skills. Further trimming that stays inside A: collapse the build-side chain (recon, implementer, mutator, reviewer, exit gate), make plugins opt-in per project instead of always loaded, delete agents the sessions never reached, and keep typed artifacts as handoffs.

**Who does what.** The model routes (through `guide`, the project's `AGENTS.md`, or typing a command). A skill orchestrates role-and-mode agents. Gates are default-fail with two rounds. A hook validates gate output and redirects direct agent calls to the skill ([ADR 012](../adr/012-gate-output-enforced-by-hook.md), [ARCHITECTURE.md](../../ARCHITECTURE.md) section 6).

**What humans see.** Requirement, research report, spec, plan, verdicts, review artifacts: written documents mid-pipeline, plus the final PR text.

**How checks work.** Independent gates on artifacts (spec, plan, implementation), default to fail, schema-checked, capped at two rounds; mutation and review per batch.

**What it removes.** Round 3 and beyond, the default auditor step, per-commit review, mutation on logic-free code, a prompt-only retry cap.

**Cost and risk.**

- Still the largest resident surface: agent and skill descriptions, 33 skills a person must pick between.
- Routing still depends on the model: the guard acts only on a direct agent call; a generic "review my fix" was handled with no skill or agent at all (log, "Routing: entry commands and the routing guard").
- Mid-pipeline artifacts and chained agents are exactly the handoff and ceremony pattern the principles argue against; each handoff loses context the next agent re-derives.
- Two source trees: 83 authored agent and skill files, plus the Codex counterparts, to keep consistent.

**Evidence for.** The first-round independent checks produced every documented catch (a criterion that pointed attestation at the wrong commit, an `init` writing a config the loader rejected, a plan diagnostic that could never fire, padding that computed to zero in the built page). When the component skill ran, the whole pipeline ran. SiteNav passed 478 end-to-end tests on a stable contract. The hook caps work where prompt caps did not (eight specs passed at `retry_count` 4 to 9). Lowest migration cost.

**Evidence against.** The same data says value sat in a few early independent checks, and the rest was ceremony. Where work happened, it was in forks and general-purpose agents, not in plugins. Anthropic's own guidance favors splitting by context over role (architecture review, row 2). Whether A's trimmed form is cheaper or better than not having it is untested.

### B. A deep core

**Shape.** Few deep modules instead of many shallow ones, split by context and risk:

- **One risk-aware work skill.** It classifies the change by reversibility and blast radius (contained, shared, irreversible), states the outcome, constraints and evidence bar, and picks the review depth. `explore` and `spike` stay as non-binding modes ([ADR 011](../adr/011-exploration-modes.md)). It subsumes `guide`'s six commands as modes, not as six skills.
- **One full-context worker.** Researches, decides the approach, implements and tests in one context. It may fork for wide read-only search, which is a context split, not a role split.
- **One independent verifier.** A fresh context that gets the brief, the diff and the evidence list, not the worker's reasoning, and checks claims against code, a build or a render. It returns the existing `verdict@3` or `finding-report@2`. It runs for shared or irreversible work and for artifacts that make claims about code (a spec, a plan); not for contained, executable-checked work. It is the one place the "first-round independent check" lives.
- **Edge artifacts.** In: a brief and decision cards. Out: diff or render, evidence, the not-verified list, changelog or PR (`changeset@3` and `pr` text carry over).
- **Specialization loaded on demand.** ranger's hazard packs, scribe's spec rules, courier's changeset guidance, the evidence and context references become references the worker or verifier loads when the work needs them ([ARCHITECTURE.md](../../ARCHITECTURE.md) section 1), not agents.

**Who does what.** The worker does the work; the verifier does the one thing that needs separate eyes; hooks and project checks enforce what must hold.

**What humans see.** Brief and decision cards in; diff or render, evidence, not-verified list and PR out. A spec exists only when the owner wants one to read or the work is a shared contract.

**How checks work.** Layered by tier. Contained: executable evidence only (tests, types, lints, build, render), enforced by a stop hook. Shared: the same plus the verifier, one round and one targeted retry, then escalation. Irreversible: the verifier plus an owner decision card before the action.

**What it removes.** Most of the pipeline plugins as stages (weaver, vanguard, scribe, navigator as separate steps), mandatory `spec@1` and `plan@1` handoffs, the build-side agent chain, per-plugin exit gates (five of them), and most of the 44 agents. A plausible end state is the work skill, a verifier, an adversary mode for refutation, a cheap recon fork, an explorer for sketches, and the references.

**Cost and risk.**

- Biggest migration: new skill and verifier, tests for 44 agents rewritten, Codex counterparts reauthored, plugin ids and ADR 001, 003 and 007 guardrails superseded, existing consumers of the pipeline plugins affected.
- One worker context grows on a long task; compaction can lose decisions. The split for that is by context (fork a sub-task), not by role.
- A single context can talk itself into a confident wrong answer. The verifier exists for that, but its independence rests on fresh context, which is untested here.
- The verifier is only as good as its brief; a vague brief puts the pipeline's old failure (padding, wording churn) back.
- Behavior and logic bugs are not solved by B alone: the verifier has to run the code against criteria ([`evidence.md`](../../shared/references/verification/evidence.md)), not read it.

**Evidence for.** The ad hoc forks that took 77% of subagent tokens are, in practice, full-context workers; B names and constrains what the owner already does. The two-line-bug live run used no skill or agent, and a direct fix with a failing-then-passing test was proportionate. First-round independent checks are kept. Anthropic's context-split guidance and Ousterhout both point this way.

**Evidence against.** No head-to-head exists. Forks were also the biggest cost, so B does not lower cost unless the worker is leaner than the forks were. Some first-round catches were on spec and plan artifacts, which B makes optional; whether the verifier catches the same defects in a brief or in code is unmeasured. The routing problem does not vanish: one entry skill must still be reached.

### C. One agent, hooks and executable evidence only

**Shape.** No plugin agents and no pipeline. One agent does the work with a short `AGENTS.md`. Everything that must hold is a deterministic check: a stop hook that blocks completion until the project's check command passes and the not-verified list is present; pre-tool hooks that stop pushes, releases and destructive actions without the owner; schemas and linters for any artifact. A decision card is a plain question the hook or the agent raises.

**Who does what.** The agent does everything, forks for search when it chooses. Machines judge. No LLM verifier.

**What humans see.** Brief in; diff or render, evidence, not-verified list, PR out. Decision cards at the irreversible edges.

**How checks work.** Only what a program can decide: tests, types, lints, build, render diff, schema validation, hooks. "The spec for agents is something a machine can check" taken literally.

**What it removes.** All agents and skills, nearly all resident description text, and the routing question (nothing to route to).

**Cost and risk.**

- A confident mistake with no executable oracle goes through. Quality is capped by the project's own checks; a repo with weak tests has weak C. If the agent writes its own checks, it grades itself.
- The documented catches were on claims in artifacts (a criterion against the wrong commit); a test only catches the equivalent bug if one exists and exercises it.
- Hooks are not uniform: Codex has fewer events and no plugin hooks under cloud orchestration, Antigravity uses `hooks.json`, and a hook that crashes does not block on the Claude Code version used for the checks (log, "What the work found" and its open items).
- It removes the repository's reason to exist as a product, which is a business decision, not an engineering one.

**Evidence for.** Prompt-only rules failed where a hook worked (the retry cap). The strongest waste findings (rounds, duplicate review, review on logic-free code) are removed by construction. The smallest resident footprint, which TokenEconomizer's largest saving points at. Routing failure cannot happen.

**Evidence against.** Value in the sessions came from independent first-round checks, which C drops. No evidence says tests alone catch what those checks caught. The architecture review cites agents claiming success despite failed checks (a stop hook answers that) and lenient self-grading, for which C has only the tests as a counter.

## 3. The strategic layer

Applies to B and to a trimmed A; C hosts it as a scheduled routine plus a skill. The point: the architecture should not rely on the agent noticing, unprompted, that its own structure is wrong. Models reproduce ceremony, so strategy is asked for explicitly and on a trigger.

**The loop.**

1. **Identify.** A trigger fires and a detector produces the evidence.
2. **Propose options (design it twice).** Two or three structurally different options, each with cost, risk, reversibility, evidence and what would change the answer. A second option that only changes a parameter of the first is rejected.
3. **Owner decides.** Through a decision card: the question, why now (the trigger and its evidence), the options, a recommendation with confidence, the default if the owner does not answer, and an expiry. At most three open cards per cycle; no trigger, no card.
4. **Encode.** The answer becomes a guardrail or a check (a hook, a test, a lint, a line in `AGENTS.md`), and a decision record only if it passes both gates in the decision-records guide. A decision that lives only in a chat or memory is lost; that was already observed.
5. **Deliver.** The change goes through the normal path for its risk tier.
6. **Monitor.** After delivery, measure the thing the change was meant to move and report it. A change that did not move it is reverted or re-proposed.

**Triggers.** Prefer ones a script can detect, with the agent interpreting rather than hunting.

- **Cadence:** a weekly or per-model-release pass over the [assumptions register](../architecture-assumptions.md) and the transcript metrics (`tools/transcript-metrics.py`).
- **Repeated fixes in one area:** the same file or module fixed three or more times in a window is a structural defect class, which is what `scribe:architect` was written for.
- **An assumption going stale:** a register row's "next check" comes due (a model generation, a host change, an ADR's `Revisit when`).
- **Duplicated work:** the same finding, spec section or prompt text derived twice, or two agents covering one concern.

**What the agent may do without asking, by reversibility.**

| Tier | Examples | Rule |
| :-- | :-- | :-- |
| Reversible, local, affects no one else | Read, measure, write a proposal or decision card, run checks, work in a worktree or draft branch, fix a failing check inside the brief | Do it and report in the output list |
| Reversible at small cost, inside the repository | Tighten a check that encodes an already-decided rule and passes today, update a register status with the evidence that moved it, open a PR | Do it and announce it; the PR is the review |
| Hard to reverse or crosses the boundary | Change a guardrail or ADR, loosen any check, add or remove an agent or plugin, publish a schema version, tag or release, push to a shared branch, change a model or effort tier that changes spend, touch another repository, raise an autonomy or budget limit | Owner decision card first |

Asymmetry worth keeping: tightening a check that encodes a decided rule may be unasked; loosening one never is.

**Guard against the layer becoming ceremony.** A card cap, an expiry, no card without a detector trigger, and a monitor step that retires the layer's own rules when they did not pay. The layer is itself an assumption to put in the register.

## 4. Comparison and recommendation

| Constraint | A. Plugins trimmed | B. Deep core | C. Single agent and hooks |
| :-- | :-- | :-- | :-- |
| C1 Owner sees only edges and decisions | Partly: spec, plan and verdict artifacts remain mid-pipeline | Meets by design | Meets; decision cards need a mechanism |
| C2 Cost follows risk | Partly: rounds capped, chains and gates still run by stage | Meets: risk picks the review depth | Meets, but only by omitting review |
| C3 Independent check where it pays | Meets (gates), but also where it does not | Meets, scoped by tier | Weak: executable oracles only |
| C4 Must-hold is deterministic | Partly: gate output and routing hooks only | Partly: needs the stop hook and project checks added | Meets by construction |
| C5 Reached by default | Partly: guard on direct agent calls; generic requests bypass | Partly: one entry, but still skill-invoked; far fewer choices | Meets: nothing to route |
| C6 Full context for the worker | Weak: chained agents, handoffs | Meets | Meets |
| C7 Strategy asked for | Partly: the layer can sit on top | Meets: work friction feeds the loop | Partly: needs a routine and a skill, so not "nothing" |
| C8 Resident footprint | Weak to partly: the 26 pipeline agents' descriptions alone are about 2.2k tokens after the last cut, plus 39 skills | Meets: a handful of descriptions | Best |
| C9 Migration and reversibility | Best: already in place | Weak: large rewrite, ADRs superseded; reversible if built beside A | Partly: deletion is easy, but removes the product |
| C10 Portability | Good: Codex counterparts exist, hooks Claude-only | Partly: Codex has a single-agent fallback already; verifier and hooks need counterparts | Weak: hook parity differs per host |
| Evidence today | Strongest for its first-round checks; none that it beats B or C | Direction supported by where work already happens; untested | Weakest on the catch side; strongest on waste |

**Observation.** B at its lowest risk tier is C. B adds three things to C: a risk router, a verifier that switches on above the contained tier, and references loaded on demand. So the real question is not B versus C but where the verifier switches on, and whether A's mid-pipeline stages add anything above that.

**Recommendation.** Treat B as the target and reach it from A without a rewrite.

1. **Do now, valid under all three** (no-regret): the stop hook and not-verified list; making plugins opt-in per project; collapsing the build-side chain in A; the strategic loop's detectors and decision-card format, which need none of the architecture decisions.
2. **Build B beside A, not over it**: one work skill and one verifier as a new plugin or project skill, leaving the existing plugins installed but off. Nothing is superseded until the measurement says so.
3. **Decide on the paired measurement** (section 5), with no-plugin as the control and as the C arm.

**Confidence.** High that the no-regret moves are right: each targets something observed (unenforced prompts, unrouted skills, resident text). Medium-low, about 55 to 60%, that B beats A on cost at equal or better quality: the direction fits the evidence but no arm has been compared, and the sample is one author and a few projects. Low that C alone suffices beyond contained work.

**What would change it.**

- **Toward C:** the bare arm ties B on hidden-test pass and later defects across contained tasks at lower tokens. Then B's contained tier is C, and the verifier applies only above it.
- **Toward A:** the B verifier misses first-round spec or plan defects that A's gates caught, or B's worker degrades on long tasks and the forks it needs re-create A's chain.
- **Toward a deeper rewrite:** B's worker cost per task is no lower than the forks it replaces, which says the cost is in the work and not the structure.
- **Against the whole direction:** a logic bug class that only a separate role caught, found in the paired data.

## 5. How to decide

The test is the paired fix-task sequence in [`docs/evaluation-runbook.md`](../evaluation-runbook.md), designed in [`docs/evaluation-methodology.md`](../evaluation-methodology.md). The runbook as it stands defines three task kinds (design ideation, spec gating, changeset and PR text); ADR 015 and the log cite "paired fix-task sequences" there, but no such kind is written yet. A fourth kind has to be added first (docs only, and the owner confirms it).

**Design.**

- **Arms (three, as methodology rule 1 requires).** Bare: no plugins, the same `AGENTS.md` and hooks (this is C). A: the current plugins, entering through `/guide:fix` and `/guide:build`. B: a prototype of the work skill and verifier.
- **Tasks.** Sequences of real fix tasks from one repository's backlog, run in order so rework in task 3 shows up as cost in task 4. Each task has a frozen brief, pre-written answers to clarifying questions, and hidden regression checks the agent cannot see (hidden-oracle style). Include logic-bug tasks on purpose, since that is the gap.
- **Fixed.** Model, effort, repository commit, permission mode, `CLAUDE.md` and memory. Randomized arm order, same-day pairs, a driver who is not the scorer.

**Metrics.**

- **Outcome:** hidden-check pass at acceptance; defects found in later tasks or by a blind reviewer within a week; whether the not-verified list was accurate (spot-check false claims).
- **Cost:** reported subagent tokens plus main-thread context characters (`tools/transcript-metrics.py agents` and `context`); the share of spend in abandoned or reverted attempts (the failed-trajectory third, on our own data).
- **Effort and rework:** prompts to acceptance, turns, retries, wall-clock.
- **Attention:** characters of artifacts the owner had to read; number of decision cards and minutes to answer.
- **Path:** for A, whether the intended skill ran; for B, whether the verifier switched on at the right tier; verifier blockers that led to a persisting change versus ones discarded.

**First small experiment, runnable next week.**

1. **Replay (free).** Classify the last 30 to 40 fix tasks across the five projects by risk tier (contained, shared, irreversible) from existing transcripts. This says how often a verifier would switch on at all, and whether most work is contained. It also bounds the experiment before spending anything.
2. **B-lite.** One prompt-only project skill (no repository change): classify risk, state outcome and evidence bar, do the work, and for shared work spawn one fresh-context verifier given only the brief, diff and evidence. A day to write.
3. **Run.** One sequence of 4 fix tasks, 3 arms, 1 run each (12 runs), then a second sequence if the first is clean (the wiring-check rung of the methodology ladder).
4. **Read it as a direction check.** Four pairs cannot reach significance (the exact Wilcoxon test needs six non-tied pairs); a consistent direction here only justifies the 8-pair, repeated run the runbook asks for. A null shows no large effect on those tasks, at that model and effort, nothing more. Tag it `small-sample` and `self-benchmark`.

**Pre-register before the first run** (proposals for the owner to confirm): B replaces A if it is at least about a quarter cheaper with the hidden-check pass no worse and defects later no worse in more than one task of eight; the bare arm is enough for contained work if it ties B on those; a worse hidden-check result outweighs any token saving.

The strategic layer is measured separately: cards raised, cards the owner accepted, owner minutes, whether an encoded check later fired, and whether the trigger condition recurred less.

## 6. Open questions for the owner

1. **Who is the user of the plugins?** If they are a marketplace product for others, A and B change what consumers install, and ADR 007's no-rename guardrail binds; if they are your personal harness, C and B are far cheaper to adopt.
2. **Claude first, or portable?** B and C lean on hooks and forks. Is Codex and Antigravity parity a hard requirement for the new core, or a later port with the single-agent fallback?
3. **Risk tiers per repository.** What counts as contained, shared and irreversible for the sites and for this repository? Is any push or publish always yours to approve?
4. **Decision cards.** What do you want to read, where (terminal, a rendered page), how many per week, and what is the default when you do not answer?
5. **Unattended loop.** May the strategic loop run on a schedule without you, within what budget, and with what it may open (draft PRs, proposals only)?
6. **The fix-task kind.** The runbook has no such kind yet. Confirm the design, the repository, and who scores (one author is the main weakness of every number above).
7. **Coverage gaps in the evidence.** The sessions say little about weaver, vanguard and courier beyond the changeset runs. Do you want those kept as they are while the build side is tested?
8. **Thresholds.** Is a quarter cheaper at equal quality the right bar to replace A, and is a worse hidden-check result an automatic loss?
9. **Supersession appetite.** If B wins, are you willing to supersede ADR 003 and amend 001 and 007, and retire plugins that consumers may use?
