---
name: understand
description: >-
  Brownfield phase 0: repo orientation (workspace-scan + convention-detect) and optional SPEC delta
  refinement. Human provides AI_CONTEXT/SPEC.md (edit or @-attach in chat); agent grill-updates
  that file with blast-radius analysis. Invoke /understand before /design.
---

# /understand — attach `AI_CONTEXT/SPEC.md`

## Purpose

**One command** for brownfield onboarding and intent alignment:

1. **Orientation** — how the repo is laid out and how code is written (when artifacts are missing or stale).
2. **Spec delta** — read **`AI_CONTEXT/SPEC.md`** (human must edit the file or attach `@AI_CONTEXT/SPEC.md` in chat). Refine it grill-style (one question at a time, recommended answers) and record **blast radius** under **Current change**. Do not treat a short slash-command phrase as the spec — the **file** is authoritative.

Downstream: **`/design <FEATURE>`** (same command name as greenfield).

## When to invoke

| Invocation | When |
|------------|------|
| `/understand` | First time on repo, or refresh overview/conventions |
| `/understand` + `@AI_CONTEXT/SPEC.md` | Orientation (if needed) + SPEC delta from the attached/edited file |
| `/understand` (SPEC already has **Current change**) | SPEC-only pass when overview/conventions already exist |

- Do **not** use for greenfield product shaping from scratch — use `/grillme`.
- Do **not** implement features — use `/design` → `/tdd` → `/tasksplit` → `/implement-next`.

## Inputs

- **Required (orientation):** Consumer repository tree.
- **Required (spec delta):** `AI_CONTEXT/SPEC.md` — human-edited or attached in chat; create from `core/templates/SPEC.template.md` if missing.
- **Optional:** One-line hint in the message (feature name only) — must not replace content in `SPEC.md`.
- **Optional:** Existing overview/conventions — refresh only when human requests.
- **Forbidden:** Unbounded chat as requirements; whole-repo dumps; editing application source.

## Workflow

### 1 — Orientation (when needed)

Run when `PROJECT_OVERVIEW.contract.yaml` or `CONVENTIONS.contract.yaml` is missing, stale, or human asked for refresh:

1. Ensure `AI_CONTEXT/` exists.
2. **Stage A** — [workspace-scan](../workspace-scan/SKILL.md) steps 2–7 → `PROJECT_OVERVIEW.*`
3. **Stage B** — [convention-detect](../convention-detect/SKILL.md) steps 1–7 → `CONVENTIONS.*`
4. Write `AI_CONTEXT/UNDERSTAND.contract.yaml` rollup (shape below).

If both artifacts already exist and the invocation is **spec-delta only**, set `stages.workspace_scan` / `convention_detect` to `skipped` in rollup and do not rescan unless human requested refresh.

### 2 — Spec delta (when change description provided)

Follow [grillme](../grillme/SKILL.md) **Workflow B (incremental)** for the human’s change:

- One question per turn with **recommended** answer (radio-style options when fixed choices).
- **No silent writes** — merge into `SPEC.md` only after each answered question (verbatim-insert exception per grillme).
- Explore the codebase when a question is factual (paths, existing auth flow, etc.).

Additionally for brownfield:

1. Maintain or create section **`## Current change`** in `SPEC.md` with:
   - **Intent** — one paragraph from human input
   - **Blast radius** — evidence-backed bullets: modules/paths, APIs, data, config, tests, integrations, deploy risk (use IDE search; no invented paths)
   - **Open questions** — numbered list tied to the change
2. Update blast radius as answers land; shrink uncertainty; do not redesign the whole product spec unrelated to the change.

**STOP after spec-delta work** (when no `/design` in same invocation):

```text
SPEC updated for current change. Review: AI_CONTEXT/SPEC.md (sections Current change, …)

When intent is clear enough, derive a feature ID and run:
  /slice          (optional — if the change is large)
  /design <FEATURE>
```

### 3 — Finish

1. Cross-check rollup paths and merged `open_gaps`.
2. **STOP.** Reply: artifacts written, 3-bullet repo summary (if orientation ran), SPEC/blast-radius summary (if delta ran), next command (`/design <FEATURE>` or `/slice`).

Do **not** run `/design`, `/tdd`, or `/implement-next` in the same invocation.

## Output artifacts

| Path | When |
|------|------|
| `AI_CONTEXT/PROJECT_OVERVIEW.md` | Orientation |
| `AI_CONTEXT/PROJECT_OVERVIEW.contract.yaml` | Orientation |
| `AI_CONTEXT/CONVENTIONS.md` | Orientation |
| `AI_CONTEXT/CONVENTIONS.contract.yaml` | Orientation |
| `AI_CONTEXT/UNDERSTAND.contract.yaml` | Always refresh rollup |
| `AI_CONTEXT/SPEC.md` | Spec delta mode only |

## `UNDERSTAND.contract.yaml` shape

```yaml
contract_version: "1"
artifact: understand
workflow_profile: brownfield_dev_loop
completed_at: "YYYY-MM-DD"

project_overview_contract_path: AI_CONTEXT/PROJECT_OVERVIEW.contract.yaml
conventions_contract_path: AI_CONTEXT/CONVENTIONS.contract.yaml
spec_path: AI_CONTEXT/SPEC.md

summary: "<stack + style + current change one-liner if any>"

stages:
  workspace_scan: complete | skipped
  convention_detect: complete | skipped
  spec_delta: complete | skipped

current_change_summary: null   # short string when spec delta ran

open_gaps: []

downstream_skills:
  - slice
  - design
```

## Failure handling

- **Spec delta without SPEC file** — seed template, then grill.
- **Orientation blocked** — minimal overview + gaps; spec delta may still run if conventions sample is possible.
- **Change too vague** — ask one clarifying question; do not invent blast radius.

## Forbidden

- Feature design, TDD, tasksplit, implementation, review.
- Replacing `/grillme` on empty greenfield products.
- Chaining `/design` in the same run.

## Quality bar

- [ ] Rollup exists; orientation artifacts present or skip documented.
- [ ] Spec delta: `Current change` + blast radius cite evidence or `open_questions`.
- [ ] Chat ends with STOP + `/design <FEATURE>` (not `/plan-feature`).

## Advanced

| Need | Use |
|------|-----|
| Layout only | `/workspace-scan` |
| Conventions only | `/convention-detect` |
| Full product spec (greenfield) | `/grillme` |
