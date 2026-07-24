---
name: tasksplit
description: >-
  Task queue FEATURE:Cn after /tdd. Writes FEATURE_TASKS.md and contract with tasks_status draft
  until approved. Invoke /tasksplit FEATURE before /implement-next.
---

# /tasksplit \<FEATURE\> — Task queue

## Purpose

Create bounded `FEATURE:Cn` units for `/implement-next`, with `scope_in`, `depends_on`, and `implements_cases` linked to TDD.

## When to invoke

- `/tasksplit <FEATURE>` — after `/tdd <FEATURE>` (or after approved `/design` when TDD skipped with human waiver).
- When `delivery.needs_tasks: true` on feature contract — **required** before implement-next.
- When `needs_tasks: false` — emit **one** task `FEATURE:C1` covering full slice scope for queue consistency.
- Re-run when scope or TDD changes materially.

## Inputs

- **Required:** `{context_dir}/<FEATURE>.contract.yaml` with `design_status: approved`.
- **Optional:** `{context_dir}/<FEATURE>_TDD.contract.yaml`.
- **Optional:** `{context_dir}/FEATURE_SLICES.contract.yaml` — slice row for scope boundaries.
- **Forbidden:** Implementing code in this skill.

## Workflow

1. Validate feature contract; gate on `design_status: approved`.
2. Read `delivery.needs_tasks` and slice `in_scope` / `out_of_scope`.
3. Build `tasks[]` (typically 3–8; single `C1` when lite).
4. Each task: `id`, `status: pending`, `summary`, `depends_on`, `scope_in`, `scope_out`, `implements_cases`.
5. Write `{context_dir}/<FEATURE>_TASKS.md` and `{context_dir}/<FEATURE>_TASKS.contract.yaml` with `tasks_status: draft`, `current_task: null`, `workflow_profile: devflow`.
6. **STOP.** Chat reply: task table, explicit **approve tasks then `/implement-next <FEATURE>`**. Do **not** set `tasks_status: approved` without human approval.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `{context_dir}/<FEATURE>_TASKS.md` | Created or replaced | |
| `{context_dir}/<FEATURE>_TASKS.contract.yaml` | Created or replaced | Queue for implement-next |

## `<FEATURE>_TASKS.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_tasks
workflow_profile: devflow
feature_id: "<FEATURE>"
tasks_status: draft
current_task: null
feature_contract_path: {context_dir}/<FEATURE>.contract.yaml
tdd_contract_path: {context_dir}/<FEATURE>_TDD.contract.yaml

summary: "<one sentence>"
tasks: []
  # - id: AUTH:C1
  #   status: pending
  #   summary: "..."
  #   depends_on: []
  #   scope_in: []
  #   scope_out: []
  #   implements_cases: [TC-001]

ordered_sequence: []
open_questions: []
assumptions: []
```

## Approval semantics

- **`tasks_status: approved`** — only after explicit human approval; required before `/implement-next`.

## Failure handling

- Missing feature contract → stop; `/design <FEATURE>`.
- `needs_tasks: true` with no chunking basis → `open_questions`; do not emit empty queue.

## Forbidden

- `tasks_status: approved` without human approval.
- Implementation in same invocation.

## Quality bar (self-check before finishing)

- [ ] Valid IDs and acyclic `depends_on`.
- [ ] Chat states approval gate before `/implement-next`.
