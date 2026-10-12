---
name: tasksplit
description: >-
  Build an approved-gated FEATURE:Cn task queue for /implement. The YAML task contract is the
  default durable output; a Markdown task summary is optional. Invoke /tasksplit FEATURE before queued implementation.
---

# /tasksplit <FEATURE> — Task queue

## Purpose

Create bounded `FEATURE:Cn` units for `/implement`, with explicit scope, dependencies, and traceability to test cases. **The tasks contract is the source of truth.** Report the task table in chat; do not create a duplicate Markdown file unless requested.

## When to invoke

- `/tasksplit <FEATURE>` — after approved design and normally after `/tdd <FEATURE>` (TDD may be skipped with explicit human waiver).
- When `delivery.needs_tasks: true`, create a dependency-ordered queue before queued `/implement`.
- When `needs_tasks: false`, prefer the lite `/implement <FEATURE>` path; create a single `FEATURE:C1` only when queue consistency or traceability is useful.
- Re-run when scope or TDD changes materially.

## Inputs

- **Required:** `artifacts/<FEATURE>.contract.yaml` with `design_status: approved`.
- **Optional:** `artifacts/<FEATURE>_TDD.contract.yaml`.
- **Optional:** `artifacts/FEATURE_SLICES.contract.yaml` for scope boundaries.
- **Forbidden:** Implementing code in this skill.

## Workflow

1. Validate the feature contract and design approval.
2. Read `delivery.needs_tasks` and slice `in_scope` / `out_of_scope`.
3. Build a dependency-ordered `tasks[]` list (typically 3–8 tasks for non-trivial work; fewer when appropriate).
4. Each task must include `id`, `status: pending`, `summary`, `depends_on`, `scope_in`, `scope_out`, and `implements_cases` where test cases exist.
5. Write `artifacts/<FEATURE>_TASKS.contract.yaml` with `tasks_status: draft` and `current_task: null`.
6. Show the task table and rationale in chat. **Stop for explicit human approval**; do not set `tasks_status: approved` without it.
7. If requested, write `artifacts/<FEATURE>_TASKS.md` as a readable projection of the contract.

## Contract shape

```yaml
contract_version: "1"
artifact: feature_tasks
workflow_profile: devflow
feature_id: "<FEATURE>"
tasks_status: draft
current_task: null
feature_contract_path: "artifacts/<FEATURE>.contract.yaml"
tdd_contract_path: "artifacts/<FEATURE>_TDD.contract.yaml"
summary: "<one sentence>"
tasks: []
ordered_sequence: []
open_questions: []
assumptions: []
```

## Approval semantics

- `tasks_status: approved` — only after explicit human approval; required before queued `/implement`.

## Failure handling

- Missing feature contract → stop; `/design <FEATURE>`.
- No safe chunking basis → record an open question and ask; do not emit an empty queue.
- Invalid dependency or scope overlap → fix the plan before requesting approval.

## Forbidden

- Approving tasks without human approval.
- Implementing code in the same invocation.
- Treating optional Markdown as a second task-state source.

## Quality bar

- [ ] IDs are valid and dependencies are acyclic.
- [ ] Task scopes are bounded, ordered, and traceable to acceptance criteria/test cases where available.
- [ ] The chat response clearly states the approval gate before queued `/implement`.
