---
name: feature-api
description: >-
  Optional Stage 3 API/interface contract for one FEATURE. Writes AI_CONTEXT/<FEATURE>_API.md plus
  <FEATURE>_API.contract.yaml only when the feature contract says API work is needed.
---

# /feature-api \<FEATURE\> — Conditional interface planning

## Purpose

Define interface behavior for a feature only when required. This stage is controlled by `<FEATURE>.contract.yaml` delivery flags so simple internal features can skip API design entirely.

## When to invoke

- Run when `delivery.needs_api: true`.
- Skip when `delivery.needs_api: false`.
- Re-run when behavior, integration, or compatibility needs change.

## Inputs

- **Required:** `AI_CONTEXT/<FEATURE>.contract.yaml`.
- **Required when planning:** `AI_CONTEXT/SPEC.md`.
- **Optional:** `AI_CONTEXT/<FEATURE>_DB.contract.yaml` (if DB-backed APIs), `AI_CONTEXT/SYSTEM_HLD.contract.yaml`, `AI_CONTEXT/<FEATURE>_DESIGN.md`.
- **Forbidden:** Requiring DB contract when `needs_db: false` and API can be described independently.

## Workflow

1. Validate feature contract and inspect `delivery.needs_api`.
2. If `needs_api: false`, stop after a short skip note (no output files by default).
3. If `needs_api: true`, define operations, auth/authz expectations, error model, and compatibility notes.
4. Emit markdown + YAML outputs with concise traces to feature criteria.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_API.md` | Created or replaced | Emitted only when `needs_api: true` |
| `AI_CONTEXT/<FEATURE>_API.contract.yaml` | Created or replaced | Emitted only when `needs_api: true` |

If downstream tooling requires a placeholder on skip, allow a minimal stub with `style.protocol: in_process`; default is no API artifacts when skipped.

## `<FEATURE>_API.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_api
feature_id: "<FEATURE>"
feature_contract_path: AI_CONTEXT/<FEATURE>.contract.yaml
spec_path: AI_CONTEXT/SPEC.md
feature_db_contract_path: AI_CONTEXT/<FEATURE>_DB.contract.yaml

summary: "<one sentence>"
style: {}
  # protocol: rest | grpc | graphql | cli | in_process | event | TBD
operations: []
compatibility: []
open_questions: []
assumptions: []
```

## Context budget

- Read feature contract in full first.
- Read DB contract only if relevant for API payloads.

## Failure handling

- Missing feature contract → stop and suggest `/feature-design <FEATURE>`.
- `needs_api: true` but no clear behaviors → emit focused `open_questions`, do not invent endpoints.

## Forbidden

- Generating implementation code or massive OpenAPI dumps.
- Editing upstream contracts.

## Quality bar (self-check before finishing)

- [ ] Skip behavior obeys `delivery.needs_api`.
- [ ] When emitted, operations are traceable to feature behaviors/criteria.
