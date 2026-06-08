---
name: tdd
description: >-
  Test plan for FEATURE after /design is approved. Writes FEATURE_TDD.md and FEATURE_TDD.contract.yaml.
  Invoke /tdd FEATURE before /tasksplit.
---

# /tdd \<FEATURE\> — Test plan

## Purpose

Map acceptance criteria from `<FEATURE>.contract.yaml` into a compact test matrix (`TC-*`) before task splitting and implementation.

## When to invoke

- `/tdd <FEATURE>` — after `/design <FEATURE>` with `design_status: approved` on `<FEATURE>.contract.yaml`.
- Recommended when `delivery.needs_tasks: true` or risk warrants explicit cases.
- Skip only when human agrees tests are trivial and records skip in `PROJECT_STATE.md` or feature assumptions.
- Do **not** invoke before design approval.

## Inputs

- **Required:** `{context_dir}/<FEATURE>.contract.yaml` with `design_status: approved`.
- **Optional:** `{context_dir}/<FEATURE>_DB.contract.yaml`, `<FEATURE>_API.contract.yaml` when delivery flags require them.
- **Optional:** `{context_dir}/SPEC.md`, `{context_dir}/SYSTEM_HLD.contract.yaml`.
- **Forbidden:** Implementing tests or product code in this skill.

## Workflow

1. Validate `<FEATURE>` and `design_status: approved` — else **stop**; complete `/design` approval first.
2. Read `delivery` flags and `acceptance_criteria[]`.
3. Build `cases[]` with ids `TC-001`, … linked to `AC-*`.
4. Write `{context_dir}/<FEATURE>_TDD.md` and `{context_dir}/<FEATURE>_TDD.contract.yaml` — set `workflow_profile: devflow`.
5. **STOP.** Suggest **`/tasksplit <FEATURE>`** when `needs_tasks: true`; else **`/tasksplit <FEATURE>`** still recommended for single-task queue, or **`/implement-next <FEATURE>`** only if tasksplit documents lite single task.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `{context_dir}/<FEATURE>_TDD.md` | Created or replaced | |
| `{context_dir}/<FEATURE>_TDD.contract.yaml` | Created or replaced | |

No other files written or edited.

## `<FEATURE>_TDD.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_tdd
workflow_profile: devflow
feature_id: "<FEATURE>"
feature_contract_path: {context_dir}/<FEATURE>.contract.yaml
feature_db_contract_path: {context_dir}/<FEATURE>_DB.contract.yaml
feature_api_contract_path: {context_dir}/<FEATURE>_API.contract.yaml

summary: "<one sentence>"
cases: []
order: []
open_questions: []
assumptions: []
```

## Failure handling

- Missing or unapproved feature contract → stop; `/design <FEATURE>` then approve.
- No acceptance criteria → stop; amend feature contract via `/design` refresh.

## Forbidden

- Code changes; editing SPEC/slices/HLD contracts.

## Quality bar (self-check before finishing)

- [ ] Every case traces to AC or explicit assumption.
- [ ] Chat suggests `/tasksplit <FEATURE>`.
