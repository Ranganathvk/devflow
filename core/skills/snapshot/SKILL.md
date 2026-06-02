---
name: snapshot
description: >-
  Simple Dev Loop: after /review sign-off and green verification, checkpoints the task and marks it
  done on FEATURE_PLAN.contract.yaml. Invoke as /snapshot or /snapshot TASK_ID. Next: /implement-next
  if more tasks remain. Does not use /debug.
---

# /snapshot [\<TASK_ID\>] — Verified checkpoint (Simple Dev Loop)

## Purpose

Close one plan task after human review:

1. Record verification in `*_SNAPSHOT.contract.yaml`
2. Link snapshot to the review artifact
3. Mark the task **`done`** and clear **`current_task`** on `<FEATURE>_PLAN.contract.yaml`

This skill is **not** a git replacement. It does **not** fix code — resolve blockers before snapshot (fix in editor or chat, then re-run `/review`).

## When to invoke

- `/snapshot` — **Simple Dev Loop (default):** resolve `<TASK_ID>` from `current_task` on `AI_CONTEXT/<FEATURE>_PLAN.contract.yaml`.
- `/snapshot <TASK_ID>` — explicit task (e.g. after legacy or multi-plan workflows).
- After **`/review`** artifacts exist for that task.
- After **`human_signoff: approved`** in the review contract **or** explicit human approval in chat.
- After verification **passed** (or documented waiver in snapshot YAML).
- Do **not** snapshot with unresolved **blocking** review findings.
- Do **not** snapshot multiple tasks in one invocation.

## Inputs

- **Required:** Resolved `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required:** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` with zero `blocking` findings (or `agent_ready_for_signoff: true`).
- **Required:** `AI_CONTEXT/SPEC.md` — skim **Human code ownership** (minimum).
- **Required (Simple Dev Loop):** `AI_CONTEXT/<FEATURE>_PLAN.contract.yaml` — patch task queue on success.
- **Optional:** `git rev-parse HEAD` for `git_head`.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md` — one-line append when present.
- **Forbidden:** Fabricating green test results; snapshot while review shows blockers.

## Resolve TASK_ID (when argument omitted)

1. Find `*_PLAN.contract.yaml` or `*_TASKS.contract.yaml` with non-null `current_task`.
2. **One match** → use `current_task`.
3. **Multiple** → stop; ask for `/snapshot <TASK_ID>`.
4. **None** → stop; run `/implement-next` then `/review` first.

## Workflow

1. **Resolve** `<TASK_ID>` from argument or plan `current_task`.
2. **Parse** → `<FEATURE>`, `C<n>`, `basename = "<FEATURE>_C<n>"`.
3. **Load** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml`.
4. **Gate — blockers:** If any finding has `severity: blocking` or `agent_ready_for_signoff: false` with open blockers → **stop**. Tell human: fix code/tests, re-run **`/review`** (Simple Dev Loop does not use `/debug`).
5. **Gate — sign-off:** If `human_signoff` is not `approved` and no explicit chat approval → **stop**; complete `/review` sign-off steps.
6. **Gate — verification:** Run or confirm tests/checks for the task scope. Record commands and outcome. If failing and no human waiver → **stop**.
7. **Write** `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` (YAML shape below).
8. **Link back:** Set `linked_snapshot_path` on the review contract.
9. **Queue update:** Patch plan or tasks contract:
   - Matching `tasks[].id` → `status: done`
   - `current_task: null`
10. **PROJECT_STATE:** If `AI_CONTEXT/PROJECT_STATE.md` exists, append: ``- [snapshot] `<TASK_ID>` verified``.
11. **STOP.** Chat reply: snapshot path, verification summary, pending task count. If pending tasks → **`/implement-next`**. If queue empty → feature plan complete. `/learn` is optional (advanced).

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` | Created or replaced | Checkpoint |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` | Patch `linked_snapshot_path` | |
| `AI_CONTEXT/<FEATURE>_PLAN.contract.yaml` | Patched | `done` + `current_task: null` |
| `AI_CONTEXT/PROJECT_STATE.md` | Optional append | If file exists |

No application source edits in this skill.

## `<FEATURE>_C<n>_SNAPSHOT.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_snapshot
workflow_profile: devflow
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
snapshot_basename: "<FEATURE>_C<n>"

captured_at: "<ISO8601>"
git_head: "<sha-or-unknown>"

review_contract_path: AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml
plan_contract_path: AI_CONTEXT/<FEATURE>_PLAN.contract.yaml

human_signoff: approved

verification:
  status: passed | waived
  commands: []
  approval_source: contract | chat
  waiver: null

pending_tasks_after: 0
notes: ""
```

## Failure handling

- **No review contract** → stop; run `/review` first.
- **Blocking findings** → stop; fix and re-run `/review`.
- **Tests not run and no waiver** → stop; run tests or document waiver.
- **Plan contract missing** (simple loop) → still write snapshot; warn that queue was not updated.

## Forbidden

- `/debug` in the same or prior chained invocation for this task.
- Marking task `done` while review blockers remain.
- Editing implementation files.

## Quality bar (self-check before finishing)

- [ ] Zero blocking findings at snapshot time.
- [ ] Plan contract shows task `done` and `current_task: null` when plan exists.
- [ ] Chat states `/implement-next` or plan complete.

## Legacy

Legacy flows without a tasks queue may set `plan_contract_path` and skip queue update step 9.
