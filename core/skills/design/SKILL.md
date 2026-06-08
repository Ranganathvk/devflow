---
name: design
description: >-
  Per-feature design: asks what to build, classifies delivery (db/api/tasks), produces DESIGN +
  contract and conditional DB/API artifacts. Invoke /design FEATURE, /design "description", or
  /design (prompt for intent). Stops for approval before /tdd.
---

# /design [\<FEATURE\> | "\<description\>"] [approved]

## Purpose

**One command** for all feature design. The agent:

1. **Asks the human** what they want to design (when intent is unclear).
2. **Researches** the repo or slice context as needed.
3. **Classifies delivery** — sets `needs_db`, `needs_api`, `needs_tasks` from the feature shape (not from a separate skill chain).
4. **Designs accordingly** — core `_DESIGN.md` + `.contract.yaml`, plus `_DB.*` / `_API.*` only when classified.

Downstream: **`/tdd <FEATURE>`** → **`/tasksplit <FEATURE>`** → **`/implement-next`**.

## When to invoke

| Invocation | When |
|------------|------|
| `/design` | No feature yet — agent asks what you want to design |
| `/design "add OTP login"` | New feature from description; derive `feature_id`, start **clarify** |
| `/design OTP_LOGIN` | Continue next pending stage |
| `/design OTP_LOGIN approved` | Approve awaiting stage, run **one** next stage |

- Do **not** implement code in this skill.
- Do **not** skip whole-design approval before `/tdd`.
- **Deprecated:** `/feature-questions`, `/feature-research`, `/feature-design`, `/feature-db`, `/feature-api` → use **`/design`** only.

## Inputs

- **Required:** `{context_dir}/SPEC.md`
- **Required (existing repo):** `{context_dir}/CONVENTIONS.contract.yaml` and `{context_dir}/UNDERSTAND.contract.yaml` or `PROJECT_OVERVIEW.contract.yaml` — if missing, suggest `/understand` first
- **Optional:** `{context_dir}/FEATURE_SLICES.contract.yaml` — scope when `/slice` ran
- **Optional:** `{context_dir}/SYSTEM_HLD.contract.yaml`
- **Required for work:** Consumer repo when impact/research/db/api touch code
- **Forbidden:** Unbounded chat as spec; inventing scope the human has not confirmed

## Stages (one per invocation)

| # | Stage | `_DESIGN.md` section | Notes |
|---|-------|----------------------|-------|
| 1 | `clarify` | § Intent & questions | **Ask the human** what to design; one question per turn with **recommended** answer; derive `feature_id` + title |
| 2 | `impact` | § Impact | Evidence paths; skip as `skipped` if no repo (spec-only greenfield) |
| 3 | `research` | § Research | ≤12 files read-only; skip as `skipped` if trivial and cited in SPEC |
| 4 | `design` | § Design | Outcomes, ACs, behaviors; **classify `delivery`** (see below) |
| 5 | `db` | § Data | Emit `_DB.*` only when `needs_db: true`; else mark `skipped` |
| 6 | `api` | § API / interface | Emit `_API.*` only when `needs_api: true`; else mark `skipped` |
| 7 | `compat` | § Compatibility | `blocking` flag for existing-repo deltas |

After stage 7 approved → set **`design_status: approved`** only on explicit whole-design approval.

## Delivery classification (during `design` stage)

Infer from clarified intent + SPEC + slice/HLD — **state rationale** in `delivery.notes`:

| Flag | Set `true` when | Set `false` when |
|------|-----------------|------------------|
| `needs_db` | New/changed persistence, entities, migrations | Pure UI/config/docs/cli with no durable store |
| `needs_api` | HTTP/RPC/events/CLI surface, external integrations | Internal-only refactor, library module, docs-only |
| `needs_tasks` | Non-trivial scope; wants chunked `FEATURE:Cn` queue | Lite vertical slice; single bounded change |

When uncertain, **ask one targeted question** in clarify/design — do not default all flags to `true`.

## Workflow

**A — New (`/design` or `/design "description"`)**

1. If no description and no `<FEATURE>` → ask: *What feature or change do you want to design?* (recommended options from SPEC / slices if available). **STOP**.
2. Parse or propose `feature_id` (`^[A-Z][A-Z0-9_]{1,31}$`); abort if contract exists in progress — use `/design <FEATURE>`.
3. Load inputs; missing orientation on existing repo → `/understand`.
4. Create `<FEATURE>_DESIGN.md` (skeleton), `<FEATURE>.contract.yaml` (`workflow_profile: devflow`, `design_status: draft`, `awaiting_approval: clarify`, all stages `pending`).
5. Run **clarify** only — grill-style Q&A until intent is clear enough for impact/design.
6. **STOP** — [stage stop message](#stage-stop-message).

**B — Continue (`/design <FEATURE>` or `… approved`)**

1. Load feature contract + DESIGN.md.
2. If `awaiting_approval` set and no `approved` in message → **STOP** (remind section to read).
3. On `approved`: mark stage `approved`, clear `awaiting_approval`.
4. If all stages `approved` or `skipped` and `design_status` still `draft` → prompt whole-design approval; **STOP** unless explicit approve.
5. Run **exactly one** next `pending` stage:
   - **`db`:** if `needs_db` → write `_DB.md` + `_DB.contract.yaml`; else set stage `skipped`.
   - **`api`:** if `needs_api` → write `_API.md` + `_API.contract.yaml`; else set stage `skipped`.
6. Set `awaiting_approval` for stages that produced content; **STOP**.

## Stage stop message

```text
Design stage complete: <STAGE> — read {context_dir}/<FEATURE>_DESIGN.md § "<section>".

Edit for corrections. When satisfied, reply approved or:
  /design <FEATURE> approved

Delivery flags: needs_db=<bool> needs_api=<bool> needs_tasks=<bool>

Then: /tdd <FEATURE> → /tasksplit <FEATURE> → /implement-next (after design_status approved).
```

## Output artifacts

| Path | When |
|------|------|
| `{context_dir}/<FEATURE>_DESIGN.md` | Always (updated each stage) |
| `{context_dir}/<FEATURE>.contract.yaml` | Always |
| `{context_dir}/<FEATURE>_DB.md` + `_DB.contract.yaml` | `needs_db: true` (stage `db`) |
| `{context_dir}/<FEATURE>_API.md` + `_API.contract.yaml` | `needs_api: true` (stage `api`) |

No application source edits.

## `<FEATURE>.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature
feature_id: "<FEATURE>"
workflow_profile: devflow
design_status: draft
awaiting_approval: clarify
title: "<from clarify>"

spec_path: {context_dir}/SPEC.md
understand_contract_path: {context_dir}/UNDERSTAND.contract.yaml
conventions_contract_path: {context_dir}/CONVENTIONS.contract.yaml
feature_slices_contract_path: null

design_stages:
  clarify: { status: draft, approved_at: null }
  impact: { status: pending, approved_at: null }
  research: { status: pending, approved_at: null }
  design: { status: pending, approved_at: null }
  db: { status: pending, approved_at: null }
  api: { status: pending, approved_at: null }
  compat: { status: pending, approved_at: null, blocking: false }

delivery:
  delivery_profile: lite | standard | heavy
  needs_db: false
  needs_api: false
  needs_tasks: true
  notes: "<why flags were set>"

depends_on: []
in_scope: []
out_of_scope: []
acceptance_criteria: []
open_questions: []
```

## Conditional `_DB.contract.yaml` (minimal)

```yaml
contract_version: "1"
artifact: feature_db
feature_id: "<FEATURE>"
feature_contract_path: {context_dir}/<FEATURE>.contract.yaml
summary: "<one sentence>"
persistence: { primary_store: sql | document | kv | file | none | TBD }
entities: []
relationships: []
migrations: []
open_questions: []
```

## Conditional `_API.contract.yaml` (minimal)

```yaml
contract_version: "1"
artifact: feature_api
feature_id: "<FEATURE>"
feature_contract_path: {context_dir}/<FEATURE>.contract.yaml
summary: "<one sentence>"
style: { protocol: rest | grpc | graphql | cli | in_process | event | TBD }
operations: []
compatibility: []
open_questions: []
```

## Approval semantics

| Gate | Rule |
|------|------|
| Stage | `approved` in chat while `awaiting_approval` matches |
| `design_status: approved` | All stages `approved` or `skipped` + explicit human OK |
| `/tdd` | Refuses if `design_status` not `approved` |

## Failure handling

- **No SPEC** → seed from template or `/grillme`.
- **No orientation on existing repo** → `/understand`.
- **Unknown FEATURE in slices** → list valid IDs or `/slice`.
- **Compat `blocking: true`** → do not approve design until resolved.

## Forbidden

- More than one substantive stage per invocation (except auto-`skipped` for db/api when flag false).
- Invoking deprecated `/feature-*` skills in the same run.
- `/tdd`, `/tasksplit`, `/implement-next` in same invocation.

## Deprecated

- **`/plan-feature`** → `/design` ([plan-feature](../plan-feature/SKILL.md))
- **`/feature-questions`**, **`/feature-research`**, **`/feature-design`**, **`/feature-db`**, **`/feature-api`** → `/design`

## Quality bar

- [ ] Human was asked (clarify) when intent was ambiguous.
- [ ] `delivery` flags set with `notes` rationale.
- [ ] DB/API artifacts exist iff flags true; otherwise stages `skipped`.
- [ ] Chat names file, section, and next command.
