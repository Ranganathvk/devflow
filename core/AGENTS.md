# Framework agent harness (canonical)

This is the **canonical** agent harness for the `devflow` framework. It applies to any coding agent or AGENTS.md-respecting tool (Codex, Claude Code, Cursor, Windsurf, Copilot, and future compatible agents) that has been attached to a repo via the installer.

> **Do not hand-edit derived copies.** Files such as `.cursor/AGENTS.md`, `.claude/AGENTS.md`, etc. are materialized from this file by the installer/sync described under `adapters/<agent>/`. Edit **here** and re-sync.

## Philosophy

- **Files over chat.** Durable intent and state live in the repo; conversation is for execution and clarification.
- **Small surface area.** Keep root orchestration minimal; put repeatable workflows in modular `SKILL.md` files under `core/skills/`.
- **One direction of truth.** Do not duplicate specs in chat — update the canonical file instead.
- **No mega prompts.** Split work into bounded skills; prefer small orchestrated workflows over monolithic skills.
- **Vertical implementation.** Deliver one feature end-to-end before broadening; no horizontal "all DB then all APIs then all UI" passes.
- **Human code ownership.** Every implementation path includes review and snapshot; fix blockers in-editor and re-run `/review`. Optional `/debug` and `/learn` for deeper loops.

## Source of truth (read order)

Agents reading this harness must consult these inputs in order before acting on a non-trivial task:

| Order | Path | Role |
|-------|------|------|
| 1 | The `AGENTS.md` materialized for the current agent (this file's content) | Harness rules, read order, rotation policy |
| 2 | `AI_CONTEXT/SPEC.md` | What we are building — **high-level product intent only** (goals, boundary, requirements); not technical or low-level design (that lives in HLD/LLD) |
| 3 | `AI_CONTEXT/PROJECT_STATE.md` (when present) | Where we are now — decisions, active work, blockers |
| 4 | The relevant `SKILL.md` for the requested slash command, if any | Bounded workflow module |

If `AI_CONTEXT/SPEC.md` is unfilled or placeholder-heavy, align with the human via `/grillme` or `/understand` (attach `@AI_CONTEXT/SPEC.md`) before any large change. Same for `PROJECT_STATE.md`.

## Dev Loop (single workflow)

One workflow for all projects. **Optional prelude** skills depend on repo state. Full doc: [docs/DEV_LOOP.md](../docs/DEV_LOOP.md).

### Optional prelude (pick what you need)

| Skill | When |
|-------|------|
| `/grillme` | Spec is thin, fuzzy, or needs interview-driven refinement |
| `/understand` | Existing codebase — orientation + SPEC delta + blast radius |
| `/system-hld` | System shape needed before slicing |
| `/slice` | Large scope — feature catalog before per-feature work |

### Core loop (per feature)

```text
/design <FEATURE> → /tdd <FEATURE> → /tasksplit <FEATURE>
→ /implement-next → /review → /snapshot
```

`/design` asks what to build, classifies delivery (`needs_db`, `needs_api`, `needs_tasks`), and emits DB/API artifacts when needed — no separate `/feature-*` commands.

Repeat `/implement-next` → `/review` → `/snapshot` until the task queue is empty.

### Other commands

- `/implement <FEATURE>` or `/implement <TASK_ID>` — explicit invoke (lite path)
- `/debug`, `/learn` — optional post-review depth

### Suggested routes

| Route | Typical sequence |
|-------|------------------|
| Lite | `/slice` → `/design` → `/implement <FEATURE>` when `needs_tasks: false` |
| Standard | prelude as needed → `/design` → `/tdd` → `/tasksplit` → implement loop |
| Compliance-heavy | standard + `/tasksplit` → `/implement <TASK_ID>` per chunk + `/learn` |

Existing-repo safe-change principles: [docs/DELTA_PRINCIPLES.md](../docs/DELTA_PRINCIPLES.md).

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

All workflow contracts use **`workflow_profile: devflow`** unless marked legacy deprecated.

| Human doc | Machine contract |
|-----------|------------------|
| `AI_CONTEXT/PROJECT_OVERVIEW.md` | `AI_CONTEXT/PROJECT_OVERVIEW.contract.yaml` |
| `AI_CONTEXT/CONVENTIONS.md` | `AI_CONTEXT/CONVENTIONS.contract.yaml` |
| *(orientation rollup)* | `AI_CONTEXT/UNDERSTAND.contract.yaml` |
| `AI_CONTEXT/SYSTEM_HLD.md` | `AI_CONTEXT/SYSTEM_HLD.contract.yaml` |
| `AI_CONTEXT/FEATURE_SLICES.md` | `AI_CONTEXT/FEATURE_SLICES.contract.yaml` |
| `<FEATURE>_DESIGN.md` | `<FEATURE>.contract.yaml` |
| `<FEATURE>_DB.md` | `<FEATURE>_DB.contract.yaml` *(when `needs_db`)* |
| `<FEATURE>_API.md` | `<FEATURE>_API.contract.yaml` *(when `needs_api`)* |
| `<FEATURE>_TDD.md` | `<FEATURE>_TDD.contract.yaml` |
| `<FEATURE>_TASKS.md` | `<FEATURE>_TASKS.contract.yaml` |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` | `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` |
| *(verification checkpoint; prose optional)* | `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` |
| `AI_CONTEXT/LEARNINGS.md` (append-only sections) | `AI_CONTEXT/<FEATURE>_C<n>_LEARN.contract.yaml` |

Contracts are stability-critical. Downstream skills consume contracts, not prose.

Conditional artifacts (`_DB*`, `_API*`, `_TDD*`, `_TASKS*`) emit only when applicable; record skips in `<FEATURE>.contract.yaml` via `delivery` flags.

## Skill discovery

- Canonical skills live under `core/skills/<name>/SKILL.md`.
- Agent-specific paths (e.g. `.cursor/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`) are **derived** by the installer. See `adapters/<agent>/` for each tool's discovery convention.
- To add a skill: author it under `core/skills/`, then re-sync.
- **Deprecated slash commands** (`/feature-*`, `/plan-feature`) remain as redirect stubs only — do not extend.

## Hooks (allowed responsibilities)

Hooks may **only** summarize, generate contracts, checkpoint state, or trim context. Hooks **must not** bloat context, inject unbounded narrative, or duplicate skill logic.

## Forbidden in agent sessions

- Generating large unbounded code in one shot (violates "no mega prompts" and "vertical implementation").
- Horizontal whole-system passes (all DB → all APIs → all UI) — work one vertical feature at a time.
- Editing derived `AGENTS.md` / `SKILL.md` mirrors instead of the canonical source under `core/`.
- Treating chat history as durable state — update files instead.
- Marking `AI_CONTEXT/SPEC.md` "approved" — the human owns that.
- Invoking deprecated `/feature-*` skills for new work — use `/design`.

---

*Extend this harness with additional `core/` docs only when a pattern repeats across efforts.*
