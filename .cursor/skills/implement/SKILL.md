---
name: implement
description: >-
  Execute one bounded implementation unit either as /implement <TASK_ID> (task-based) or
  /implement <FEATURE> (lite direct path). Uses contracts when present and keeps scope tight.
---

# /implement \<TASK_ID | FEATURE\> — Bounded execution

## Purpose

Implement one bounded chunk without waterfall coupling:

- **Task mode:** `/implement <FEATURE>:C<n>` consumes `<FEATURE>_TASKS.contract.yaml`.
- **Lite mode:** `/implement <FEATURE>` uses slices + feature contract flags to implement directly when tasksplit is skipped.

This skill mutates code/tests but must not silently expand scope.

## When to invoke

- `/implement <TASK_ID>` when a task backlog exists and a single chunk is ready.
- `/implement <FEATURE>` when the feature is in lite path (`delivery.needs_tasks: false`) or the human explicitly wants direct implementation.
- One invocation must cover exactly one task ID or one feature ID.

## Inputs

- **Required (both modes):** `artifacts/SPEC.md`, `artifacts/FEATURE_SLICES.contract.yaml`.
- **Required (task mode):** `artifacts/<FEATURE>_TASKS.contract.yaml`.
- **Optional (both):** `artifacts/<FEATURE>.contract.yaml`, `artifacts/<FEATURE>_TDD.contract.yaml`, `artifacts/SYSTEM_HLD.contract.yaml`, `artifacts/PROJECT_STATE.md`.
- **Forbidden:** Inventing requirements from chat history alone.

## Workflow

1. Parse argument:
   - If matches `^([A-Z][A-Z0-9_]{1,31}):C[1-9][0-9]*$` -> task mode.
   - If matches `^[A-Z][A-Z0-9_]{1,31}$` -> lite mode.
   - Otherwise stop with format hint.
2. Validate feature existence in `FEATURE_SLICES.contract.yaml`.
3. **Task mode:** load matching task row, enforce `depends_on`, and scope-lock to that row.
4. **Lite mode:** use feature slice `in_scope` + optional feature contract delivery flags to define a small implementation boundary; if `needs_tasks: true`, ask for confirmation before bypassing tasksplit.
5. Implement smallest change set required to satisfy scoped behavior.
6. Run relevant checks/tests for touched area.
7. Reply with changed paths, check results, and suggested next `/review <TASK_OR_FEATURE>`.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| Source and test files | As required | Only files justified by selected task/slice scope |
| `artifacts/PROJECT_STATE.md` | Optional append | Only if file exists or user requested tracking |

Do not edit upstream planning contracts in this skill.

## Context budget

- Prefer contract-first reads.
- In lite mode, avoid loading full stage artifacts unless needed to remove ambiguity.

## Failure handling

- Invalid id pattern -> stop with accepted formats.
- Missing task contract in task mode -> suggest `/tasksplit <FEATURE>`.
- Scope mismatch (requested work exceeds task/slice) -> stop and request split or scope decision.

## Forbidden

- Multiple tasks/features in one run.
- Drive-by refactors outside scoped files.
- Rewriting planning contracts to fit code changes.

## Quality bar (self-check before finishing)

- [ ] Exactly one bounded unit executed.
- [ ] Changes map to task scope or feature slice scope.
- [ ] Tests/checks run and summarized.
