---
name: tdd
description: >-
  Build a compact test-case contract from approved feature acceptance criteria. The contract is
  the default durable output; a Markdown test plan is optional. Invoke /tdd FEATURE before /tasksplit.
---

# /tdd <FEATURE> — Test cases

## Purpose

Map acceptance criteria from `<FEATURE>.contract.yaml` into a compact `TC-*` matrix before task splitting and implementation. Downstream skills consume the YAML contract, so **write that contract by default and show the matrix in chat**. Create a Markdown test-plan document only when the human requests it or the case matrix is complex enough to benefit from separate review.

## When to invoke

- `/tdd <FEATURE>` — after `/design <FEATURE>` has `design_status: approved`.
- Recommended when `delivery.needs_tasks: true` or the feature has meaningful risk.
- Skip only when the human agrees tests are trivial; record the rationale in feature assumptions or `PROJECT_STATE.md`.
- Do not invoke before design approval.

## Inputs

- **Required:** `artifacts/<FEATURE>.contract.yaml` with `design_status: approved`.
- **Optional:** `artifacts/<FEATURE>_DB.contract.yaml`, `<FEATURE>_API.contract.yaml` when applicable.
- **Optional:** `artifacts/SPEC.md`, `artifacts/SYSTEM_HLD.contract.yaml`.
- **Forbidden:** Implementing tests or product code.

## Workflow

1. Validate the feature contract and design approval; otherwise stop.
2. Read delivery flags and `acceptance_criteria[]`.
3. Build `cases[]` with stable ids (`TC-001`, …), each linked to one or more `AC-*` or a clearly stated assumption.
4. Write `artifacts/<FEATURE>_TDD.contract.yaml` with `workflow_profile: devflow`.
5. Show a concise test-case table in chat, including traceability to acceptance criteria.
6. If requested, write `artifacts/<FEATURE>_TDD.md` as a readable projection of the contract; do not maintain conflicting copies of case definitions.
7. Suggest `/tasksplit <FEATURE>` when a queue is needed; for a genuinely lite slice, `/implement <FEATURE>` may be used without a queue.

## Contract shape

```yaml
contract_version: "1"
artifact: feature_tdd
workflow_profile: devflow
feature_id: "<FEATURE>"
feature_contract_path: "artifacts/<FEATURE>.contract.yaml"
feature_db_contract_path: "artifacts/<FEATURE>_DB.contract.yaml"
feature_api_contract_path: "artifacts/<FEATURE>_API.contract.yaml"
summary: "<one sentence>"
cases: []
order: []
open_questions: []
assumptions: []
```

## Failure handling

- Missing/unapproved feature contract → stop; complete and approve `/design <FEATURE>`.
- No acceptance criteria → stop and request a design refresh; do not invent requirements.
- Missing DB/API contracts despite applicable delivery flags → flag the inconsistency before continuing.

## Forbidden

- Code changes; editing SPEC/slices/HLD contracts.
- Generating a Markdown file by default when the contract and chat matrix are sufficient.

## Quality bar

- [ ] Every case traces to an acceptance criterion or explicit assumption.
- [ ] Cases cover relevant happy paths, edge cases, and failure behavior.
- [ ] Contract is valid and downstream-readable.
- [ ] Chat suggests the appropriate next command.
