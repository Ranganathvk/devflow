---
name: design
description: >-
  Per-feature design for brownfield and greenfield. Brownfield: orchestrates clarify/impact/research/
  design/compat stages in AI_CONTEXT/<FEATURE>_DESIGN.md with chat approval gates. Greenfield:
  questions/research/feature-design/db/api after /slice. Invoke /design FEATURE or /design "description".
  Stops for approval before /tdd.
---

# /design \<FEATURE\> | /design "\<description\>" [approved]

## Purpose

**One command** for feature design on both workflows. Produces `AI_CONTEXT/<FEATURE>_DESIGN.md` and `<FEATURE>.contract.yaml` with `design_status` and stage gates.

| Profile | When | Gates |
|---------|------|-------|
| **Brownfield** | Existing repo; after `/understand` | One internal stage per invocation; **wait for chat approval** between stages |
| **Greenfield** | After `/slice` | Runs bundled stages; single design approval at end |

Downstream: **`/tdd <FEATURE>`** → **`/tasksplit <FEATURE>`** → **`/implement-next`**.

## Profile detection

1. If `FEATURE_SLICES.contract.yaml` exists **and** `<FEATURE>` is in slices **and** `SYSTEM_HLD.contract.yaml` exists → **greenfield**.
2. Else → **brownfield** (requires `UNDERSTAND.contract.yaml` or overview + conventions).

## When to invoke

| Invocation | When |
|------------|------|
| `/design "add OTP login"` | Brownfield: derive `feature_id`, start at stage **clarify** |
| `/design OTP_LOGIN` | Continue brownfield (next stage if previous approved) |
| `/design OTP_LOGIN approved` | Approve awaiting stage, run **one** next stage |
| `/design AUTH` | Greenfield: after `/slice` |

- Do **not** implement code.
- Do **not** skip design approval before `/tdd`.

## Inputs

### Brownfield

- **Required:** `AI_CONTEXT/CONVENTIONS.contract.yaml`
- **Required:** `AI_CONTEXT/SPEC.md` (incl. **Current change** when present)
- **Required:** `UNDERSTAND.contract.yaml` or `PROJECT_OVERVIEW.contract.yaml`
- **Required:** Consumer repo (impact/research)
- **Optional:** `FEATURE_SLICES.contract.yaml` — scope boundary when `/slice` ran

### Greenfield

- **Required:** `AI_CONTEXT/SPEC.md`
- **Required:** `FEATURE_SLICES.contract.yaml` — row for `<FEATURE>`
- **Required:** `AI_CONTEXT/SYSTEM_HLD.contract.yaml`

## Brownfield — internal stages (one per invocation)

| # | Stage | `_DESIGN.md` section | Notes |
|---|-------|----------------------|-------|
| 1 | `clarify` | § Questions | From change + SPEC |
| 2 | `impact` | § Impact | Evidence paths only |
| 3 | `research` | § Research | ≤12 files; read-only explore |
| 4 | `design` | § Design (delta) | Fills `delivery` on feature contract |
| 5 | `compat` | § Compatibility | `blocking` flag |

After stage 5 approved → set **`design_status: approved`** only on explicit whole-design approval (same chat or follow-up).

**Do not** run TDD/tasksplit inside `/design` on brownfield — use `/tdd` and `/tasksplit` (same as greenfield).

### Brownfield workflow

**A — New (`/design "description"`)**

1. Parse `feature_id`, `title`; abort if `<FEATURE>.contract.yaml` exists with in-progress stages — use `/design <FEATURE>`.
2. Load brownfield inputs; missing orientation → `/understand`.
3. Create `<FEATURE>_DESIGN.md` (skeleton below), `<FEATURE>.contract.yaml` (`workflow_profile: brownfield_dev_loop`, `design_status: draft`, `awaiting_approval: clarify`, all stages `pending`).
4. Run **clarify** only → `awaiting_approval: clarify`, stage `draft`.
5. **STOP** — [stage stop message](#stage-stop-message).

**B — Continue (`/design <FEATURE>` or `… approved`)**

1. Load feature contract + DESIGN.md.
2. If `awaiting_approval` set and no `approved` in message → **STOP** (remind section to read).
3. On `approved`: mark stage `approved`, clear `awaiting_approval`.
4. If all five stages `approved` and `design_status` still `draft` → prompt whole-design approval; **STOP** unless message explicitly approves design.
5. Else run **exactly one** next `pending` stage → set `awaiting_approval`, **STOP**.

### Greenfield workflow

1. Validate `<FEATURE>` in `FEATURE_SLICES.contract.yaml`.
2. Run stages per table (questions → research → feature-design → conditional db/api) using linked skills.
3. Set `workflow_profile: greenfield_dev_loop`, `design_status: draft`.
4. **STOP** — approve design, then `/tdd <FEATURE>`.

## Stage stop message (brownfield)

```text
Design stage complete: <STAGE> — read AI_CONTEXT/<FEATURE>_DESIGN.md § "<section>".

Edit the file for corrections. When satisfied, reply approved or:
  /design <FEATURE> approved

Then: /tdd <FEATURE> → /tasksplit <FEATURE> → /implement-next (after each approval gate).
```

## Output artifacts

| Path | Profile |
|------|---------|
| `AI_CONTEXT/<FEATURE>_DESIGN.md` | Both |
| `AI_CONTEXT/<FEATURE>.contract.yaml` | Both |
| `AI_CONTEXT/<FEATURE>_QUESTIONS.*` | Greenfield optional |
| `AI_CONTEXT/<FEATURE>_RESEARCH.*` | Greenfield optional |
| `AI_CONTEXT/<FEATURE>_DB.*` / `_API.*` | Greenfield conditional |

No application source edits.

## `<FEATURE>.contract.yaml` (brownfield)

```yaml
contract_version: "1"
artifact: feature
feature_id: "<FEATURE>"
workflow_profile: brownfield_dev_loop
design_status: draft
awaiting_approval: clarify
title: "<description>"

spec_path: AI_CONTEXT/SPEC.md
understand_contract_path: AI_CONTEXT/UNDERSTAND.contract.yaml
conventions_contract_path: AI_CONTEXT/CONVENTIONS.contract.yaml
feature_slices_contract_path: null

design_stages:
  clarify: { status: draft, approved_at: null }
  impact: { status: pending, approved_at: null }
  research: { status: pending, approved_at: null }
  design: { status: pending, approved_at: null }
  compat: { status: pending, approved_at: null, blocking: false }

delivery:
  delivery_profile: lite
  needs_db: false
  needs_api: false
  needs_tasks: true

depends_on: []
in_scope: []
out_of_scope: []
acceptance_criteria: []
open_questions: []
```

Greenfield: same as before with `workflow_profile: greenfield_dev_loop` and `design_status: draft` (no `design_stages` required).

## Approval semantics

| Gate | Rule |
|------|------|
| Brownfield stage | `approved` in chat while `awaiting_approval` matches |
| `design_status: approved` | All brownfield stages `approved` + explicit human OK |
| `/tdd` | Refuses if `design_status` not `approved` |

## Failure handling

- **Brownfield: no orientation** → `/understand`.
- **Greenfield: missing slice/HLD** → `/slice` or `/system-hld`.
- **Unknown FEATURE (greenfield)** → list valid IDs.
- **Compat `blocking: true`** → do not approve design until resolved.

## Forbidden

- More than one brownfield stage per invocation (except `approved` → one next stage).
- `design_status: approved` without explicit human approval.
- `/tdd`, `/tasksplit`, `/implement-next` in same invocation.
- Brownfield: requiring `SYSTEM_HLD` or `FEATURE_SLICES`.

## Deprecated

**`/plan-feature`** — use **`/design`** (same artifacts pattern, aligned with greenfield). See [plan-feature](../plan-feature/SKILL.md).

## Quality bar

- [ ] Correct `workflow_profile` set.
- [ ] Brownfield: one stage written; chat names file + section.
- [ ] Greenfield: `delivery` block populated; skip documented.
