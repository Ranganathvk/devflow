---
name: learn
description: >-
  Optional. After a task is done on the TASKS contract, distills durable lessons into
  {context_dir}/LEARNINGS.md (append) and optionally a LEARN contract. /review artifacts
  are optional inputs.
---

# /learn — Durable lessons after a completed task

## Purpose

Turn a **completed** task (status `done` on the tasks contract) into **compact, reusable knowledge**. Keeps **`{context_dir}/`** as the durable source of truth.

`/review` artifacts are optional inputs.

## When to invoke

- `/learn <TASK_ID>` — after `/implement` marked the task `done`.
- `/learn <TASK_ID>` — backfill from an older completed task (human-directed).
- Aborted work: human requests **“lessons without a completed task”** → `learn_kind: aborted`; skip verification claims.
- Do **not** dump raw logs into `LEARNINGS.md`.

## Inputs

- **Required:** `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required (complete):** matching task row `status: done` on `{context_dir}/<FEATURE>_TASKS.contract.yaml` (legacy plan `done` acceptable).
- **Optional:** `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml`.
- **Optional:** `{context_dir}/SPEC.md` if lessons propose process changes (list sections; do not silently rewrite SPEC).
- **Forbidden:** Inventing incidents not supported by implement/review/task artifacts.

## Workflow

1. **Parse** `<TASK_ID>` → `<FEATURE>`, `C<n>`.
2. **Load** tasks (or legacy plan) row. If not `done` and not aborted → **stop**; finish implement first.
3. **Extract** 3–7 bullet lessons (max).
4. **Append** `{context_dir}/LEARNINGS.md` (`## <YYYY-MM-DD> — <TASK_ID>`).
5. **Write** `{context_dir}/<FEATURE>_C<n>_LEARN.contract.yaml`.
6. **Chat:** paths, top 1–2 lessons, optional `/implement`.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `{context_dir}/LEARNINGS.md` | Created or appended | Dated section |
| `{context_dir}/<FEATURE>_C<n>_LEARN.contract.yaml` | Created or replaced | Small YAML |

## `<FEATURE>_C<n>_LEARN.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_learn
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
learn_kind: complete | aborted

tasks_contract_path: "{context_dir}/<FEATURE>_TASKS.contract.yaml"
review_contract_path: null  # set if review YAML exists

lessons: []
follow_ups: []
```

## Context budget

- Task row; optional review summary fields. Do not re-read all TDD prose.

## Failure handling

- **Task not done** → stop unless aborted mode.
- **LEARNINGS.md huge** → append only; suggest archive if > ~500 lines.

## Forbidden

- Rewriting prior dated LEARNINGS sections.
- Claiming lessons not grounded in artifacts.
- Requiring a review artifact.

## Quality bar

- [ ] Dated LEARNINGS section for this `<TASK_ID>`.
- [ ] Contract matches prose lessons.
