---
name: feature-db
description: >-
  Optional Stage 3 data contract for one FEATURE. Writes AI_CONTEXT/<FEATURE>_DB.md plus
  <FEATURE>_DB.contract.yaml only when the feature contract says DB work is needed.
---

# /feature-db \<FEATURE\> — Conditional data planning

## Purpose

Define persistence intent for a feature when storage design is required. This stage is conditional and controlled by `<FEATURE>.contract.yaml` delivery flags.

## When to invoke

- Run when `delivery.needs_db: true` in `AI_CONTEXT/<FEATURE>.contract.yaml`.
- Skip when `delivery.needs_db: false` (intentional no-DB feature).
- Re-run when data assumptions change.

## Inputs

- **Required:** `AI_CONTEXT/<FEATURE>.contract.yaml`.
- **Required when planning:** `AI_CONTEXT/SPEC.md`.
- **Optional:** `AI_CONTEXT/SYSTEM_HLD.contract.yaml`, `AI_CONTEXT/<FEATURE>_DESIGN.md`.
- **Forbidden:** Inferring DB scope not present in feature contract or SPEC.

## Workflow

1. Validate feature contract and read `delivery.needs_db`.
2. If `needs_db: false`, stop after a short chat note: DB stage intentionally skipped (no files written by default).
3. If `needs_db: true`, produce concise DB design and contract.
4. Keep outputs bounded and traceable to feature behaviors/acceptance criteria.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_DB.md` | Created or replaced | Emitted only when `needs_db: true` |
| `AI_CONTEXT/<FEATURE>_DB.contract.yaml` | Created or replaced | Emitted only when `needs_db: true` |

If downstream tooling requires a path even when DB is skipped, a stub contract is allowed with `persistence.primary_store: none`; default behavior is to omit DB artifacts when skipped.

## `<FEATURE>_DB.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_db
feature_id: "<FEATURE>"
feature_contract_path: AI_CONTEXT/<FEATURE>.contract.yaml
spec_path: AI_CONTEXT/SPEC.md
system_hld_contract_path: AI_CONTEXT/SYSTEM_HLD.contract.yaml

summary: "<one sentence>"
persistence: {}
  # primary_store: sql | document | kv | file | none | TBD
entities: []
relationships: []
migrations: []
open_questions: []
assumptions: []
```

## Context budget

- Read feature contract in full first.
- Read SPEC/HLD only if `needs_db: true`.

## Failure handling

- Missing feature contract → stop and suggest `/feature-design <FEATURE>`.
- `needs_db: true` but no usable data intent → emit open questions, do not invent schema.

## Forbidden

- Editing implementation code or migrations in this skill.
- Editing upstream feature contract.

## Quality bar (self-check before finishing)

- [ ] Skip behavior obeys `delivery.needs_db`.
- [ ] When emitted, DB contract is traceable and compact.
