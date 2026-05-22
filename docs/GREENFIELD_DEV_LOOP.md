# Greenfield Dev Loop

Doc index: [README.md](README.md). Install: [GETTING_STARTED.md](GETTING_STARTED.md).

High-level commands for **new product** work from `AI_CONTEXT/SPEC.md` through vertical slices. Uses `FEATURE_SLICES`; shares execution/review with brownfield (`/implement-next`, `/review`, `/snapshot`).

```text
/grillme
/system-hld
/slice
/design AUTH
# approve design → then:
/tdd AUTH
/tasksplit AUTH
# approve tasks → then:
/implement-next
/review
/snapshot
/implement-next          # repeat per feature / per task
```

## High-level commands

| Command | Purpose |
|---------|---------|
| `/grillme` | Interview-fill and refine `AI_CONTEXT/SPEC.md` |
| `/system-hld` | System shape + `SYSTEM_HLD.contract.yaml` |
| `/slice` | Vertical feature catalog + `FEATURE_SLICES.contract.yaml` |
| `/design <FEATURE>` | Per-feature design (questions, research, design, db, api) |
| `/tdd <FEATURE>` | Test matrix `TC-*` from acceptance criteria |
| `/tasksplit <FEATURE>` | Task queue `FEATURE:Cn` for implementation |
| `/implement-next [FEATURE]` | Next approved task (greenfield or brownfield queue) |
| `/review` | Review `current_task` |
| `/snapshot` | Verify, mark task `done` |

## Approval gates

1. **Design** — After `/design <FEATURE>`, approve (`design_status: approved` on `<FEATURE>.contract.yaml`) before `/tdd`.
2. **Tasks** — After `/tasksplit <FEATURE>`, approve (`tasks_status: approved` on `<FEATURE>_TASKS.contract.yaml`) before `/implement-next`.

## Per-feature loop

Repeat for each feature ID from `FEATURE_SLICES` (respect `depends_on` order):

```text
/design AUTH
# approved
/tdd AUTH
/tasksplit AUTH
# approved
/implement-next AUTH
/review
/snapshot
```

## Lite feature path

When `/design` sets `delivery.needs_tasks: false`, `/tasksplit` still emits a **single** task `FEATURE:C1` for a consistent queue, or follow skill output for direct scope — see `/tasksplit` skill.

## Artifacts

| Phase | Key files |
|-------|-----------|
| Product | `SPEC.md`, `SYSTEM_HLD.*`, `FEATURE_SLICES.*` |
| Feature | `<FEATURE>_DESIGN.md`, `<FEATURE>.contract.yaml`, optional `_DB`, `_API`, `_QUESTIONS`, `_RESEARCH` |
| Tests / tasks | `<FEATURE>_TDD.*`, `<FEATURE>_TASKS.*` |
| Execution | `<FEATURE>_C<n>_REVIEW.*`, `<FEATURE>_C<n>_SNAPSHOT.*` |

## Advanced (not on cheat sheet)

- `/feature-questions`, `/feature-research`, `/feature-design`, … — partial stages (prefer `/design`)
- `/implement <TASK_ID>` — legacy explicit task invoke
- `/debug`, `/learn` — optional; not required on this loop

Brownfield counterpart: [BROWNFIELD_DEV_LOOP.md](BROWNFIELD_DEV_LOOP.md)
