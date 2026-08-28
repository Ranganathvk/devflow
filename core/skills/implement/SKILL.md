---
name: implement
description: >-
  Execute one bounded implementation unit. /implement (no args) or /implement FEATURE
  pops the next pending task from an approved TASKS queue. /implement TASK_ID does that
  task. /implement FEATURE is lite (whole feature) only when there is no approved task
  queue. Marks the task done on success. Review is optional.
---

# /implement [\<TASK_ID | FEATURE\>] — Bounded execution

## Purpose

Implement **one** bounded chunk.

| Invoke | Behavior |
|--------|----------|
| `/implement` | Next pending task on the **one** approved `*_TASKS.contract.yaml` |
| `/implement <FEATURE>:C<n>` | That task row |
| `/implement <FEATURE>` | Next pending task **if** an approved tasks queue exists; otherwise **lite** whole-feature implement |

On success in **task/queue** mode, mark the task **`done`** and set **`current_task: null`**. `/review` is optional.

## When to invoke

- After `tasks_status: approved` (and `design_status: approved`) when a queue exists.
- After `/design` with `needs_tasks: false` and no task queue — lite `/implement <FEATURE>`.
- One invocation = one task **or** one lite feature.

## Inputs

- **Required (all modes):** `{context_dir}/SPEC.md`.
- **Required (task/queue):** `{context_dir}/<FEATURE>_TASKS.contract.yaml` with `tasks_status: approved`.
- **Required (lite):** `{context_dir}/<FEATURE>.contract.yaml`.
- **Optional:** `{context_dir}/<FEATURE>_TDD.contract.yaml`, `{context_dir}/SYSTEM_HLD.contract.yaml`, `{context_dir}/FEATURE_SLICES.contract.yaml`, `{context_dir}/PROJECT_STATE.md`.
- **Forbidden:** Inventing requirements from chat history alone.

## Queue discovery (`/implement` with no argument)

1. Collect `*_TASKS.contract.yaml` with `tasks_status: approved`.
2. **0** → stop: `/design` → `/tdd` → `/tasksplit` (or `/implement <FEATURE>` lite if `needs_tasks: false`).
3. **1** → use that `feature_id`.
4. **>1** → stop; pass `/implement <FEATURE>` or `/implement <TASK_ID>`.

## Workflow

1. **Parse argument:**
   - None → queue-next (discovery above).
   - `^([A-Z][A-Z0-9_]{1,31}):C[1-9][0-9]*$` → **task mode**.
   - `^[A-Z][A-Z0-9_]{1,31}$` → if approved TASKS contract exists for that feature → **queue-next for FEATURE**; else **lite mode**.
   - Otherwise stop with format hint.
2. **Gates (task/queue):** `tasks_status: approved`; `design_status: approved`; `design_stages.compat.blocking` must not be true.
3. **In-flight:** if `current_task` is `in_progress` → **resume that task**. Do not wait for review.
4. **Else (queue-next):** pick `pending` with `depends_on` satisfied; use `ordered_sequence` when present.
5. **Task mode:** load the named row; enforce `depends_on`; scope-lock.
6. **Lite mode:** use `in_scope` / delivery flags from the feature contract (slice row if present); if `needs_tasks: true` and a queue exists, do **not** lite — use queue-next instead. If `needs_tasks: true` and no queue, stop and suggest `/tasksplit`.
7. Bind `current_task` + `in_progress` in task/queue modes.
8. Implement the smallest change set for that scope.
9. Run checks for the touched area. If they fail, leave `in_progress` and **stop**.
10. **Task/queue success:** `status: done`, `current_task: null`.
11. **Chat:** task/feature id, paths, checks, remaining pending count. If pending remain → **`/implement`** (or `/implement <FEATURE>`). Review is optional.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| Source and test files | As required | Scope-locked |
| `{context_dir}/<FEATURE>_TASKS.contract.yaml` | Task/queue | `done` + clear `current_task` on success |
| `{context_dir}/PROJECT_STATE.md` | Optional | If present or requested |

Do not edit design/TDD/slice contracts. Queue status fields on the tasks contract are allowed.

## Failure handling

- Missing approval → stop with which gate failed.
- Empty queue → feature complete or `/tasksplit`.
- Invalid id → accepted formats.
- Scope mismatch → stop; split or scope decision.
- Failed checks → leave `in_progress`; re-run `/implement` to resume.

## Forbidden

- Multiple tasks/features in one run.
- Drive-by refactors outside scoped files.

## Quality bar

- [ ] Exactly one bounded unit executed.
- [ ] Task/queue: task is `done` after green checks.
- [ ] Chat continues with `/implement` if pending tasks remain.
