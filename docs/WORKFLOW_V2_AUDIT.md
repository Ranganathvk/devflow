# DevFlow workflow V2 — Phase 1 audit and baseline

**Status:** Phase 1 complete (static audit); runtime evaluation is not yet available.  
**Audit date:** 2026-10-12  
**Audited branch:** `main` at `7175a32bb37628b9a6a99216ee68cea20e4bd605`  
**Scope:** Workflow behavior, artifact creation, source-of-truth rules, generated mirrors, and evaluation readiness. This document records findings and proposed measurements; it does not change workflow behavior.

## Executive summary

DevFlow already has useful foundations: canonical skills under `core/`, a shared contract handoff model, explicit approval gates, bounded implementation, and generated agent mirrors. The main friction is the cumulative workflow cost, not any single file:

1. Human-readable and machine-readable artifacts are paired by default across most stages, even when a narrative document adds little beyond the contract.
2. `/design` is a seven-stage state machine with per-stage stops and approvals; this conflicts with descriptions that imply a bundled/incremental design workflow.
3. `/understand` is large and includes both a strict one-action rule and guidance to run multiple autonomous iterations in one invocation.
4. Optional workflows (`/review`, `/security-review`, `/learn`) also persist artifact pairs, increasing the default file footprint when used.
5. There is no checked-in workflow evaluation suite or dedicated test directory visible in the repository tree, so there is no repeatable baseline for quality, interaction count, artifacts, or cost.

**Recommendation:** Do not rewrite all skills at once. First agree on the artifact policy and a small representative evaluation set. Then reduce artifact creation and simplify `/understand` / `/design` in small, measurable changes.

## Repository snapshot

Source of truth is `core/`; generated copies live under agent-specific directories. The repository tree at the audited commit contained:

| Inventory | Static baseline |
|---|---:|
| Repository tree entries | 232 |
| Canonical skill definitions under `core/skills/` | 14 |
| Entries under generated `.cursor/`, `.claude/`, and `.github/skills/` trees | 106 |
| Dedicated test/evaluation paths found by name | 0 |
| Snapshot skill in canonical `core/skills/` | Not found |
| Workflow CI configuration | `.github/workflows/blank.yml` only |

These are repository-tree counts, not runtime measurements. The generated mirrors should continue to be regenerated from canonical sources rather than edited independently. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Findings and evidence

### F1 — Artifact policy makes file creation the default

The canonical harness describes paired human-readable and machine-readable artifacts as the pattern for major workflows. The product spec also calls for pairs. Current skill contracts implement that rule consistently, but it is too broad for optional or low-value outputs.

| Workflow | Current declared outputs | Static artifact count |
|---|---|---:|
| `/understand FEATURE` | `FEATURE_PLAN.md`, `FEATURE_PLAN.contract.yaml`, `UNDERSTAND.contract.yaml` | 3 |
| `/design FEATURE` | `FEATURE_DESIGN.md`, `FEATURE.contract.yaml` | 2 |
| `/design` with DB design | Above + `FEATURE_DB.md` + contract | +2 |
| `/design` with API design | Above + `FEATURE_API.md` + contract | +2 |
| `/tdd FEATURE` | `FEATURE_TDD.md` + contract | 2 |
| `/tasksplit FEATURE` | `FEATURE_TASKS.md` + contract | 2 |
| `/review TASK_ID` | Per-task review Markdown + contract | 2 |
| `/security-review` | Security review Markdown + contract | 2 |
| `/learn TASK_ID` | Append to shared `LEARNINGS.md` + per-task contract | 2 writes |

A typical understand → design → TDD → task split path therefore declares **9 artifacts before implementation** (3 + 2 + 2 + 2), or **11** if a review pair is also created. DB/API design adds two files for each applicable area. This is a policy-derived count, not a claim that every run always creates every file.

**Risk:** Repeated facts can drift between Markdown and YAML if both are edited as independent sources. Conversely, removing all Markdown would hurt human review and make product intent harder to maintain.

**Direction to validate:** One source of truth per fact. Keep human-owned product intent in `SPEC.md`; retain narrative documents when they materially improve review or reasoning; prefer compact structured contracts for machine handoffs; make derived summaries and optional reports ephemeral unless a later workflow consumes them.

### F2 — `/design` has a high interaction floor and conflicting descriptions

Evidence: [`core/skills/design/SKILL.md`](../core/skills/design/SKILL.md), [`docs/DEV_LOOP.md`](DEV_LOOP.md), and [`README.md`](../README.md).

- The skill enumerates seven stages: clarify, impact, research, design, DB, API, compatibility.
- Its workflow says to run exactly one next pending stage per invocation and stop after stages that produce content.
- The same skill's description says “incremental or bundled,” while the actual stage workflow is explicitly one stage per invocation.
- The docs present the core loop compactly, which understates the number of approval/continuation turns a staged design can require.

**Risk:** Repeated orchestration consumes time and context even for straightforward changes; approval gates can become ceremony rather than risk controls.

**Direction to validate:** Execute multiple safe, evidence-backed stages in one invocation. Stop for unresolved product decisions, material architecture choices, compatibility blockers, or approval of a coherent reviewable design—not after every mechanical stage. Preserve explicit approval before downstream test planning/implementation.

### F3 — `/understand` has internal tension and a large instruction surface

Evidence: [`core/skills/understand/SKILL.md`](../core/skills/understand/SKILL.md).

- The skill is 462 lines / approximately 15.7k characters.
- The core loop says exactly one question **or** one search per turn, never both or many.
- Another loop rule says to run multiple iterations in one invocation when the agent can act autonomously.
- It requires PLAN Markdown, PLAN YAML, and an UNDERSTAND rollup contract to be persisted/refreshed throughout the loop.

These rules can be reconciled if “one action per iteration” is intended, but the current wording makes it easy for an agent to stop too early or interpret each iteration as a separate user turn.

**Direction to validate:** Make the unit of work explicit: several bounded read-only searches and synthesis steps are allowed in one invocation; ask only when a decision requires human knowledge; persist the smallest useful state; never scan the whole repository or generate architecture dumps.

### F4 — Optional workflows have durable-output costs

Evidence: [`review`](../core/skills/review/SKILL.md), [`security-review`](../core/skills/security-review/SKILL.md), and [`learn`](../core/skills/learn/SKILL.md).

- `/review` is optional but writes two per-task files.
- `/security-review` writes a Markdown report and a YAML contract.
- `/learn` appends to `LEARNINGS.md` and writes a per-task contract.
- No canonical `snapshot` skill was found in `core/skills/` at the audited commit; any prior snapshot behavior should be located before modifying it.

**Direction to validate:** Keep review output in chat by default. Persist only when requested or when a downstream workflow genuinely consumes the record. Security review may need durable records in regulated workflows, so keep that behavior configurable rather than removing it globally.

### F5 — Contract definitions are not centralized consistently

Evidence: [`core/contracts/`](../core/contracts/README.md) and individual skill files.

The contract directory currently contains reference shapes for feature plan, feature tasks, understand, and security review. Other contracts (feature, TDD, DB, API, system HLD, slices, review, learn) are described inline in their skills. This splits schema guidance across files and can make it harder to understand which structures are stability-critical.

**Direction to validate:** Do not centralize every YAML example by default. Move a shape to `core/contracts/` when it is shared across skills, validated by tooling, or needs explicit versioning. Keep one-off illustrative examples close to the skill.

### F6 — Static workflow behavior lacks an automated regression baseline

The checked-in tree has no dedicated test/evaluation directory or test-named paths, and the only workflow under `.github/workflows/` is `blank.yml`. This audit cannot run agent workflows end-to-end through all supported IDEs from repository inspection alone.

**Risk:** Simplification could accidentally weaken scope control, approval semantics, evidence grounding, or bounded implementation without a reliable way to detect it.

**Direction:** Add a lightweight, version-controlled evaluation set before broad prompt edits. Use fixed scenarios and score outputs against observable criteria; do not make model-specific token or turn targets hard correctness requirements.

## Artifact policy proposal for Phase 2

This is a proposed direction to evaluate, not a behavior change in Phase 1.

| Artifact | Proposed default |
|---|---|
| `SPEC.md` | Human-owned durable product intent; never replace with generated YAML |
| `PROJECT_STATE.md` | Durable project/session state when useful |
| `FEATURE.contract.yaml` | Canonical structured feature state, acceptance criteria, delivery flags, and approval state |
| `FEATURE_PLAN.md` | Keep only when brownfield evidence and rationale materially help a human; avoid duplicating contract fields |
| `FEATURE_DESIGN.md` | Keep when the design needs human review; concise, generated from or synchronized with the canonical facts |
| `FEATURE_TDD.md` | Optional human-readable test plan; contract or concise chat matrix can be enough for small features |
| `FEATURE_TASKS.md` | Optional task summary; task queue contract remains necessary when `/implement` consumes it |
| DB/API docs | Conditional, only when the design is substantial enough to benefit from separate review |
| Review/snapshot reports | Ephemeral/chat output by default; persist on request or when consumed downstream |
| Security review / learnings | Keep durable mode available where auditability or accumulated learning is valuable |

**Invariant:** There must be one authoritative representation for each fact. If Markdown is human-editable and YAML is consumed downstream, define the synchronization rule; do not silently maintain two independent sources of truth.

## Baseline evaluation plan

The repository does not yet contain these evaluations. Phase 2 should add a small fixture-based set and record results before and after each behavior change.

| Scenario | What it exercises | Must remain true |
|---|---|---|
| Greenfield, clear small feature | `/design` → implementation | No unnecessary interrogation or DB/API docs; explicit scope and acceptance criteria |
| Brownfield, known pattern | `/understand` → `/design` | Evidence paths cite real files; targeted investigation; no whole-repo summary |
| Brownfield, ambiguous product rule | Human clarification | Ask a focused question; do not invent product behavior |
| Feature with DB and API changes | Conditional design outputs | Migration/compatibility risks surfaced; only relevant artifacts created |
| Multi-task feature | TDD/task queue/implement | Acceptance criteria trace to tests/tasks; dependencies respected; one bounded task per implement run |
| Risky compatibility change | Approval gates | Blocking risk prevents approval/implementation until resolved |
| Optional review | Review output | Findings are actionable; no durable files unless required/requested |
| Multiple agent adapters | Sync/materialization | Canonical core changes propagate; generated copies do not drift |

### Measurements to record

For each scenario, capture:

1. **Correctness:** acceptance criteria covered, evidence paths valid, no invented requirements, gate semantics preserved.
2. **Interaction cost:** user questions, approval turns, total skill invocations.
3. **Artifact cost:** files created, bytes written, duplicated facts, orphaned artifacts.
4. **Execution cost:** tool calls and model tokens/cost where the agent runtime exposes them.
5. **Operational quality:** failed commands, malformed contracts, stale mirrors, or state that cannot be resumed after context rotation.
6. **Safety:** scope violations, premature approval, multi-task implementation, or unsupported claims.

Use the same prompts, repository fixture, and scoring rubric before and after changes. Report quality regressions separately from cost improvements; a lower file/turn count is not a win if evidence or approval quality drops.

## Phase 1 exit criteria

- [x] Canonical skills and generated mirrors identified.
- [x] Current artifact producers and default output counts inventoried.
- [x] Conflicting/ambiguous workflow instructions recorded with file evidence.
- [x] Runtime-evaluation gap stated explicitly; no runtime claims fabricated.
- [x] Phase 2 priorities and representative scenarios defined.
- [ ] Baseline agent runs collected in a real supported IDE/runtime (manual follow-up; not available from static repository audit alone).

## Recommended implementation order

1. Agree on the artifact policy and implement output minimization in the optional/reporting paths first.
2. Simplify `/understand` so a single invocation can complete multiple safe investigation actions while stopping for human-only decisions.
3. Simplify `/design` around meaningful decision/approval boundaries rather than one invocation per mechanical stage.
4. Reconcile TDD/task splitting defaults with the lite route; keep one bounded task per `/implement`.
5. Add contract validation and generated-mirror drift checks where practical.
6. Run the evaluation set after each slice and regenerate agent mirrors from `core/`.

## Scope boundaries and risks

- Do not remove human approval for material design or task-scope decisions.
- Do not change the one-task-per-`/implement` constraint.
- Do not add a vector database, graph index, MCP dependency, or new infrastructure just to improve workflow context.
- Do not make YAML the universal source of truth for human-owned product intent.
- Do not hand-edit `.cursor/`, `.claude/`, or `.github/skills/`; synchronize generated mirrors from canonical sources.
- Avoid a broad all-skills rewrite. Keep changes small enough to evaluate and revert independently.


## Phase 2 implementation update — artifact reduction

**Status:** Implemented on the Phase 1 working branch; generated mirrors updated from canonical sources.

- `/review <TASK_ID>` now reports findings in chat and creates no files by default. Use `/review <TASK_ID> save` to persist the review report and contract.
- `/tdd <FEATURE>` now writes the TDD contract by default and reports the test matrix in chat. Markdown is optional and derived from the contract.
- `/tasksplit <FEATURE>` now writes the task queue contract by default and reports the queue in chat. Markdown is optional and derived from the contract.
- `core/AGENTS.md`, the product spec, and the dev-loop docs now state that contracts are durable machine handoffs and Markdown is created when it adds distinct value or is requested.
- Human approval gates remain unchanged. `/implement` remains bounded to one task per invocation. Security-review and learnings retain durable-output behavior.

### Expected artifact reduction

For a typical `/understand` → `/design` → `/tdd` → `/tasksplit` path, default declared artifacts fall from 9 to **7**: understand's three artifacts, design's two, and one contract each for TDD and tasksplit. A default review adds **0** files; an explicitly saved review adds two. This is a policy-derived count; actual runtime behavior still needs IDE validation.

### Validation still required

- [x] Canonical skills and policy updated.
- [x] Generated Cursor, Claude, and GitHub skill mirrors updated from canonical text.
- [ ] Execute representative workflows in a supported agent runtime and verify file counts, contract validity, approval semantics, and output quality.
