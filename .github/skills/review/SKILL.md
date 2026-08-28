---
name: review
description: >-
  Optional bounded checklist review after implementation. Invoke as /review <TASK_ID> or
  /review (last done task, or current_task if still in_progress). Does not gate the task queue.
  Prefer a third-party review skill if the human already uses one.
---

# /review — Optional post-change review

## Purpose

Optional **file-backed checklist** for a single task-sized change set. The default loop does **not** require this skill — humans may review in editor, PR, or a **third-party** skill (e.g. Ponytail). This skill does **not** mark tasks `done` (implement already did).

The agent **does not** “approve” its own work as final: it records **checklist results** and **findings**. Blocking issues are fixed outside this skill (editor or `/implement`), then `/review` may be re-run.

This skill **does not** rewrite application code except typos in review docs if the human asks.

## When to invoke

- **Optional** after `/implement` when the human wants a Devflow review artifact.
- `/review <TASK_ID>` — preferred (queue may already have `current_task: null`).
- `/review` — resolve id (see **Resolve TASK_ID**).
- Do **not** invoke for multiple unrelated tasks in one run.
- Do **not** invoke before there is a **concrete** diff or file list (git diff, PR, or paths).
- Do **not** tell the human they must `/review` before `/implement`.
- For a security-only scan of the working tree, use `/security-review` instead.

## Inputs

- **Required:** Resolved `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$` **or** explicit paths + human waiver for ad-hoc (`ADHOC:1` only if authorized).
- **Required:** `artifacts/SPEC.md` — read **Design principles**, **Implementation rules**, and **Human code ownership** (minimum).
- **Required:** Change set — `git diff` / `git show` / or the files the human listed.
- **Optional:** `artifacts/<FEATURE>_TASKS.contract.yaml` — task row + TDD cases.
- **Optional (legacy plan):** `artifacts/<FEATURE>_PLAN.contract.yaml`.
- **Optional:** `artifacts/<FEATURE>_TDD.contract.yaml`.
- **Optional:** `artifacts/PROJECT_STATE.md`.
- **Forbidden:** Treating chat as the diff. Inventing files “reviewed” that are not in the change set.

## Resolve TASK_ID (when argument omitted)

1. `current_task` on `*_TASKS.contract.yaml` (or legacy `*_PLAN.contract.yaml`) if set.
2. Else the **most recently `done`** task on an approved tasks contract (one feature → use it; several features → ask).
3. Else `PROJECT_STATE.md` / user message.
4. Else **stop** and ask for `/review <TASK_ID>` — do not demand `/implement`.

## Workflow

1. **Resolve** `<TASK_ID>`.
2. **Parse** `feature_id` + `C<n>`; `review_basename = "<FEATURE>_C<n>"`.
3. **Resolve** change set; if ambiguous, **stop** with one question.
4. **Scope check** against task row; flag violations as `blocking`.
5. **Checklist:** correctness vs task/TDD, tests for new behavior, error paths, conventions, secrets/logging, migration safety, no drive-by refactors. Record pass / fail / not_applicable.
6. **Classify:** `blocking` or `non_blocking` (`deferred[]` for explicit deferrals).
7. **Write** `artifacts/<FEATURE>_C<n>_REVIEW.md` (target ≤ **~120** lines) and `artifacts/<FEATURE>_C<n>_REVIEW.contract.yaml`.
8. **Chat:** paths, blocking vs non-blocking. If blocking: fix then re-`/review`. If clear: continue with **`/implement`** if the queue has pending tasks.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `artifacts/<FEATURE>_C<n>_REVIEW.md` | Created or replaced | Human checklist |
| `artifacts/<FEATURE>_C<n>_REVIEW.contract.yaml` | Created or replaced | Small YAML |

No other files written or edited. Do **not** change task `status` on the tasks contract.

## `<FEATURE>_C<n>_REVIEW.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_review
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
review_basename: "<FEATURE>_C<n>"
plan_contract_path: artifacts/<FEATURE>_PLAN.contract.yaml  # null if unused

agent_checklist_completed: true
agent_ready_for_signoff: false  # true only if zero blocking findings

findings: []
deferred: []
resolved_findings: []

human_signoff: pending  # pending | approved | rejected
human_signoff_notes: ""
```

## Context budget

- Read in full: SPEC required sections; one task row; needed `TC-*` rows.
- Diff/stat only for the change set.

## Failure handling

- **Missing TASK_ID** → ask once for `<TASK_ID>`.
- **No diff / no files** → stop; ask how to obtain the change set.
- **Scope mismatch** → still write review with blocking `scope_mismatch` unless human confirms ad-hoc.

## Forbidden

- Silent approval without a checklist.
- Editing implementation source (use `/implement` or the editor).
- Blocking the implement queue.
- Rewriting plan/tasks status fields.

## Quality bar

- [ ] Review pair exists for one `review_basename`.
- [ ] Chat names next **optional** step (`/implement` or stop).
