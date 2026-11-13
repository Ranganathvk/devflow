---
name: review
description: >-
  Optional bounded checklist review after implementation. Reports findings in chat by default;
  invoke /review <TASK_ID> save to persist a review report and contract. Does not gate the task queue.
---

# /review — Optional post-change review

## Purpose

Review one task-sized change set against its task scope, acceptance criteria, tests, and repository conventions. **Chat is the default output.** Do not create files unless the human explicitly asks to save the review (for example, `/review AUTH:C1 save`).

This skill does not mark tasks `done`, approve its own work as final, or rewrite application code. Humans own merge quality; use a third-party review skill if preferred.

## When to invoke

- `/review <TASK_ID>` — review and report findings in chat.
- `/review <TASK_ID> save` — review and persist a report pair.
- `/review` — resolve the task id using the rules below.
- Do not review unrelated tasks in one run or run before a concrete diff/file list exists.
- For security-only review, use `/security-review`.

## Inputs

- **Required:** Resolved `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`, or explicit paths plus human waiver for ad-hoc (`ADHOC:1` only if authorized).
- **Required:** `{context_dir}/SPEC.md` — read Design principles, Implementation rules, and Human code ownership.
- **Required:** Concrete change set from `git diff`, `git show`, PR, or paths supplied by the human.
- **Optional:** Tasks, TDD, legacy plan contracts, and `PROJECT_STATE.md` for scope and traceability.
- **Forbidden:** Treating chat as the diff or inventing files reviewed.

## Resolve TASK_ID

1. `current_task` on `*_TASKS.contract.yaml` (or legacy `*_PLAN.contract.yaml`) if set.
2. Else the most recently `done` task on an approved tasks contract (if several features match, ask).
3. Else `PROJECT_STATE.md` / the user's message.
4. Else stop and ask for `/review <TASK_ID>`; do not demand `/implement`.

## Workflow

1. Resolve the task id and parse feature/task number.
2. Resolve the concrete change set; if ambiguous, stop with one focused question.
3. Check scope against the task contract; flag violations as blocking.
4. Review correctness against task/TDD, tests for new behavior, error paths, conventions, secrets/logging, migration safety, and drive-by changes.
5. Classify findings as blocking or non-blocking; note explicit deferrals.
6. Report a concise findings table in chat, ordered by severity, with file/line and rationale. If no findings, state what was checked and any limitations.
7. **Only when save was explicitly requested:** write `{context_dir}/<FEATURE>_C<n>_REVIEW.md` and `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml` from the same review result. Otherwise, write no files.

If blocking findings exist, explain the fix path and offer to review again after changes. If clear, mention `/implement` only when the queue has pending tasks.

## Saved contract shape

Use this only in save mode:

```yaml
contract_version: "1"
artifact: task_review
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
review_basename: "<FEATURE>_C<n>"
plan_contract_path: "{context_dir}/<FEATURE>_PLAN.contract.yaml" # null if unused
agent_checklist_completed: true
agent_ready_for_signoff: false # true only with zero blocking findings
findings: []
deferred: []
resolved_findings: []
human_signoff: pending # pending | approved | rejected
human_signoff_notes: ""
```

## Context budget and failure handling

- Read the task row and relevant `TC-*` cases; inspect only the concrete diff and necessary surrounding code.
- No diff/files → stop and ask how to obtain the change set.
- Scope mismatch → report as blocking; save only if requested.
- Never change task status or block the implement queue.

## Quality bar

- [ ] Findings are grounded in the actual diff and ordered by severity.
- [ ] Scope, tests, error paths, security-sensitive changes, and migration safety were considered.
- [ ] No files were created unless persistence was requested.
- [ ] Chat states blocking/non-blocking findings and next action.
