---
name: tasksplit
description: >-
  Optional Stage 3 task decomposition for FEATURE. Writes AI_CONTEXT/<FEATURE>_TASKS.md plus
  <FEATURE>_TASKS.contract.yaml when task chunking is needed before implementation.
---

# /tasksplit \<FEATURE\> — Optional task decomposition

## Purpose

Create bounded `FEATURE:Cn` units when phased execution helps. This stage is optional and controlled by `delivery.needs_tasks` in the feature contract.

## When to invoke

- Run when `delivery.needs_tasks: true`.
- Skip when `delivery.needs_tasks: false` and implement directly with `/implement <FEATURE>`.
- Re-run when test plan or scope changed substantially.

## Inputs

- **Required:** `AI_CONTEXT/<FEATURE>.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>_TDD.contract.yaml`.
- **Optional:** `AI_CONTEXT/SPEC.md`.
- **Forbidden:** Requiring TDD contract for lite features where tasksplit is intentionally disabled.

## Workflow

1. Validate feature contract and check `delivery.needs_tasks`.
2. If `needs_tasks: false`, stop with a short skip note and suggest `/implement <FEATURE>`.
3. If `needs_tasks: true`, build bounded `FEATURE:Cn` tasks with explicit `depends_on`.
4. Use TDD cases when available; otherwise derive tasks from acceptance criteria.
5. Emit markdown + YAML outputs and suggest first task ID.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_TASKS.md` | Created or replaced | Emitted only when `needs_tasks: true` |
| `AI_CONTEXT/<FEATURE>_TASKS.contract.yaml` | Created or replaced | Emitted only when `needs_tasks: true` |

No other files written or edited.

## `<FEATURE>_TASKS.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_tasks
feature_id: "<FEATURE>"
feature_contract_path: AI_CONTEXT/<FEATURE>.contract.yaml
tdd_contract_path: AI_CONTEXT/<FEATURE>_TDD.contract.yaml

summary: "<one sentence>"
tasks: []
ordered_sequence: []
open_questions: []
assumptions: []
```

## Context budget

- Read feature contract first.
- Read TDD only when available and useful.

## Failure handling

- Missing feature contract → stop and suggest `/feature-design <FEATURE>`.
- `needs_tasks: true` with no basis for chunking → emit focused `open_questions`.

## Forbidden

- Implementing code/tests in this skill.
- Editing upstream contracts.

## Quality bar (self-check before finishing)

- [ ] IDs and dependency order are valid when tasks are emitted.
- [ ] Skip behavior follows `delivery.needs_tasks`.
