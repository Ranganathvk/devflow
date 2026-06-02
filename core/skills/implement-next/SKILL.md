---
name: implement-next
description: >-
  Execute the next pending task from an approved FEATURE_TASKS queue.
  Legacy *_PLAN.contract.yaml is deprecated. Sets current_task, bounded implementation, then /review.
  Invoke as /implement-next or /implement-next FEATURE.
---

# /implement-next [\<FEATURE\>] — Next task execution

## Purpose

Pop **one** task from an **approved** `AI_CONTEXT/<FEATURE>_TASKS.contract.yaml` queue and implement with minimal blast radius.

Updates `current_task` on the tasks contract; `/snapshot` marks `done`.

## When to invoke

- After **`tasks_status: approved`** and **`design_status: approved`** on the feature contract.
- Do **not** invoke while `current_task` is `in_progress` — finish `/review` → `/snapshot` first.
- One task per invocation.

## Queue discovery (no `<FEATURE>` argument)

1. Collect `*_TASKS.contract.yaml` with `tasks_status: approved`.
2. **Legacy:** `*_PLAN.contract.yaml` with `plan_status: approved` — supported but deprecated; prefer `/design` → `/tdd` → `/tasksplit`.
3. **0** → stop: run `/design` → `/tdd` → `/tasksplit` → approve tasks.
4. **1** → use its `feature_id`.
5. **>1** → stop; pass `/implement-next <FEATURE>`.

## Workflow

1. **Resolve** `<FEATURE>` from argument or discovery.
2. **Load** `*_TASKS.contract.yaml` and `AI_CONTEXT/<FEATURE>.contract.yaml`.
3. **Gates:** `tasks_status: approved`; `design_status: approved`; when `design_stages.compat.blocking` present it must not be true.
4. **In-flight gate:** if `current_task` with task `in_progress` → stop; `/review` → `/snapshot` first.
5. **Select next task:** `pending` + `depends_on` satisfied; use `ordered_sequence` when present.
6. **Bind:** set `current_task`, task `in_progress`.
7. **Scope-lock** from task row; load `CONVENTIONS.contract.yaml` when present.
8. **Implement** per feature contract + SPEC **Current change** when relevant.
9. **Run checks** for touched area.
10. **STOP** → suggest **`/review`**.

## Output artifacts

| Path | Change |
|------|--------|
| Source and test files | As required |
| `*_TASKS.contract.yaml` | `current_task` + `in_progress` |
| `PROJECT_STATE.md` | Optional append |

## Failure handling

- Missing approval → stop with which gate failed.
- Empty queue → `/tasksplit <FEATURE>`.
- Scope creep → `/design <FEATURE>` refresh.

## Forbidden

- Multiple tasks per run; marking `done` (snapshot); `/review` in same invocation.

## Quality bar

- [ ] One task; `current_task` saved; chat → `/review`.

## Loop position

```text
/design → approve → /tdd → /tasksplit → approve → implement-next → review → snapshot
```
