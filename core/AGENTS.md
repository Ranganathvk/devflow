# Framework agent harness (canonical)

This is the **canonical** agent harness for the `agentic-dev-os` framework. It applies to any coding agent or AGENTS.md-respecting tool (Codex, Claude Code, Cursor, Windsurf, Copilot, and future compatible agents) that has been attached to a repo via the installer.

> **Do not hand-edit derived copies.** Files such as `.cursor/AGENTS.md`, `.claude/AGENTS.md`, etc. are materialized from this file by the installer/sync described under `adapters/<agent>/`. Edit **here** and re-sync.

## Philosophy

- **Files over chat.** Durable intent and state live in the repo; conversation is for execution and clarification.
- **Small surface area.** Keep root orchestration minimal; put repeatable workflows in modular `SKILL.md` files under `core/skills/`.
- **One direction of truth.** Do not duplicate specs in chat — update the canonical file instead.
- **No mega prompts.** Split work into bounded skills; prefer small orchestrated workflows over monolithic skills.
- **Vertical implementation.** Deliver one feature end-to-end before broadening; no horizontal "all DB then all APIs then all UI" passes.
- **Human code ownership.** Every implementation path must include review → test → debug → snapshot. AI is a bounded pair engineer, not an autonomous owner.

## Source of truth (read order)

Agents reading this harness must consult these inputs in order before acting on a non-trivial task:

| Order | Path | Role |
|-------|------|------|
| 1 | The `AGENTS.md` materialized for the current agent (this file's content) | Harness rules, read order, rotation policy |
| 2 | `AI_CONTEXT/SPEC.md` | What we are building — goals, constraints, success criteria |
| 3 | `AI_CONTEXT/PROJECT_STATE.md` (when present) | Where we are now — decisions, active work, blockers |
| 4 | The relevant `SKILL.md` for the requested slash command, if any | Bounded workflow module |

If `AI_CONTEXT/SPEC.md` is unfilled or placeholder-heavy, treat it as a prompt to align with the human (via `/grillme`) before any large change. Same for `PROJECT_STATE.md`.

## Locked workflow (slash commands)

The framework standardizes the following workflow. Skills implementing each stage live under `core/skills/`.

**Stage 1 — Spec alignment**

- `/grillme` — interview-driven refinement of `AI_CONTEXT/SPEC.md`.

**Stage 2 — System shape**

- `/system-hld` — compact system HLD plus `SYSTEM_HLD.contract.yaml` under `AI_CONTEXT/` (see `core/skills/system-hld/SKILL.md`).
- `/slice` — vertical feature decomposition plus `FEATURE_SLICES.contract.yaml` for Stage 3 (see `core/skills/slice/SKILL.md`).

**Stage 3 — Per vertical feature** (repeat per feature, e.g. `AUTH`)

Stage 3 is an **optional routing toolkit**, not a required waterfall. Use only the depth needed for the current feature.

- `/feature-questions <FEATURE>` — optional clarification gate.
- `/feature-research <FEATURE>` — optional evidence pass.
- `/feature-design <FEATURE>` — feature contract + delivery flags (`delivery_profile`, `needs_db`, `needs_api`, `needs_tasks`).
- `/feature-db <FEATURE>` — run only when `needs_db: true`.
- `/feature-api <FEATURE>` — run only when `needs_api: true`.
- `/tdd <FEATURE>` — optional test-planning depth.
- `/tasksplit <FEATURE>` — optional task chunking when `needs_tasks: true`.
- `/implement <FEATURE>` — lite direct implementation path.
- `/implement <TASK_ID>` — task-based path for one bounded chunk (e.g. `AUTH:C1`).
- `/review <TASK_OR_FEATURE>` → `/debug <TASK_OR_FEATURE>` → `/snapshot <TASK_OR_FEATURE>` → `/learn <TASK_OR_FEATURE>` — post-implementation verification loop.

Suggested routes:

| Route | Typical sequence |
|-------|------------------|
| Lite | `slice` → `feature-design` (minimal contract flags) → `implement <FEATURE>` |
| Standard | `feature-questions` → `feature-research` → `feature-design` → conditional db/api → optional `tdd` → `implement` |
| Compliance-heavy | standard + `tdd` + `tasksplit` → `implement <TASK_ID>` for each chunk |

Stage 3 skills through `/learn` are implemented under `core/skills/` (see `core/skills/README.md`).

## Default session command order

1. Read this harness.
2. Read `AI_CONTEXT/SPEC.md` for goals, constraints, and success criteria.
3. Read `AI_CONTEXT/PROJECT_STATE.md` (if present) for decisions, active work, and blockers.
4. If the user invoked a `/<command>`, read the matching `SKILL.md` and follow it literally.
5. Execute the task; update `AI_CONTEXT/PROJECT_STATE.md` when completion or material facts change.
6. Only then propose follow-ups — prefer updating files over long summaries.

## Context rotation

- **Rotate out.** Once a slice of work is done, capture outcomes, decisions, and next steps in `AI_CONTEXT/PROJECT_STATE.md`; avoid relying on thread history for facts.
- **Rotate in.** After compaction or a new session, re-read the sources above before continuing — do not assume the transcript is complete.
- **SPEC vs state.** `AI_CONTEXT/SPEC.md` changes rarely (intent). `AI_CONTEXT/PROJECT_STATE.md` changes often (progress). Keep that separation.
- **Downstream skills must not reload entire prior narratives.** They consume `AI_CONTEXT/SPEC.md` plus the relevant compact `*.contract.yaml`, not full HLD prose or full chat history.

## Artifact pattern

Major workflows emit **paired** artifacts: a human-readable doc and a machine-readable compact contract.

| Human doc | Machine contract |
|-----------|------------------|
| `AI_CONTEXT/SYSTEM_HLD.md` | `AI_CONTEXT/SYSTEM_HLD.contract.yaml` |
| `AI_CONTEXT/FEATURE_SLICES.md` | `AI_CONTEXT/FEATURE_SLICES.contract.yaml` |
| `<FEATURE>_DESIGN.md` | `<FEATURE>.contract.yaml` |
| `<FEATURE>_DB.md` | `<FEATURE>_DB.contract.yaml` |
| `<FEATURE>_API.md` | `<FEATURE>_API.contract.yaml` |
| `<FEATURE>_QUESTIONS.md` | `<FEATURE>_QUESTIONS.contract.yaml` |
| `<FEATURE>_RESEARCH.md` | `<FEATURE>_RESEARCH.contract.yaml` |
| `<FEATURE>_TDD.md` | `<FEATURE>_TDD.contract.yaml` |
| `<FEATURE>_TASKS.md` | `<FEATURE>_TASKS.contract.yaml` |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` | `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` |
| *(verification checkpoint; prose optional)* | `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` |
| `AI_CONTEXT/LEARNINGS.md` (append-only sections) | `AI_CONTEXT/<FEATURE>_C<n>_LEARN.contract.yaml` |

Contracts are stability-critical. Downstream skills consume contracts, not prose.

`<FEATURE>_DB*`, `<FEATURE>_API*`, `<FEATURE>_TDD*`, and `<FEATURE>_TASKS*` are **conditional artifacts**. Emit them only when applicable for the feature; record intentional skips in `<FEATURE>.contract.yaml` via `delivery` flags.

## Skill discovery

- Canonical skills live under `core/skills/<name>/SKILL.md`.
- Agent-specific paths (e.g. `.cursor/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`) are **derived** by the installer. See `adapters/<agent>/` for each tool's discovery convention.
- To add a skill: author it under `core/skills/`, then re-sync.

## Hooks (allowed responsibilities)

Hooks may **only** summarize, generate contracts, checkpoint state, or trim context. Hooks **must not** bloat context, inject unbounded narrative, or duplicate skill logic.

## Forbidden in agent sessions

- Generating large unbounded code in one shot (violates "no mega prompts" and "vertical implementation").
- Horizontal whole-system passes (all DB → all APIs → all UI) — work one vertical feature at a time.
- Editing derived `AGENTS.md` / `SKILL.md` mirrors instead of the canonical source under `core/`.
- Treating chat history as durable state — update files instead.
- Marking `AI_CONTEXT/SPEC.md` "approved" — the human owns that.

---

*Extend this harness with additional `core/` docs only when a pattern repeats across efforts.*
