# Brownfield Dev Loop

Same **command shape** as [GREENFIELD_DEV_LOOP.md](GREENFIELD_DEV_LOOP.md), adapted for **existing codebases**. One shared execution path: `/implement-next` → `/review` → `/snapshot`.

```text
# Edit or attach AI_CONTEXT/SPEC.md first, then:
/understand                          # reads & updates SPEC.md (not chat-only text)
/slice                               # optional — only when the change is large
/design <FEATURE>                    # plan stages; stop each turn for approval in chat
/tdd <FEATURE>
/tasksplit <FEATURE>
/implement-next
/review
/snapshot
```

## Commands

| Command | Purpose |
|---------|---------|
| `/understand` | Phase 0: `PROJECT_OVERVIEW` + `CONVENTIONS` + rollup |
| `/understand` | Phase 0 + grill-style refinement of **`AI_CONTEXT/SPEC.md`** (attach `@AI_CONTEXT/SPEC.md` in chat) |
| `/slice` | Optional — split a large change into feature IDs (no `SYSTEM_HLD` required) |
| `/design <FEATURE>` | Per-feature design (internal plan stages); **wait for approval in chat** between stages |
| `/design <FEATURE> approved` | Approve current design stage and run the next |
| `/tdd <FEATURE>` | Test cases `TC-*` after `design_status: approved` |
| `/tasksplit <FEATURE>` | Task queue `FEATURE:Cn` after TDD (or waiver) |
| `/implement-next` | Next approved task |
| `/review` / `/snapshot` | Human-owned verification |

## Approval gates

1. **Design (per stage)** — After each `/design` stage, read `AI_CONTEXT/<FEATURE>_DESIGN.md` (named section), edit, then reply **`approved`** or `/design <FEATURE> approved`.
2. **Design (whole)** — When all design stages are approved, set `design_status: approved` on `<FEATURE>.contract.yaml`.
3. **Tasks** — Approve `tasks_status` on `<FEATURE>_TASKS.contract.yaml` before `/implement-next`.
4. **Task** — Approve review before `/snapshot` (same as greenfield).

## Artifacts

| Phase | Files |
|-------|--------|
| Orientation | `PROJECT_OVERVIEW.*`, `CONVENTIONS.*`, `UNDERSTAND.contract.yaml` |
| Intent | `AI_CONTEXT/SPEC.md` (includes blast radius for current change when using `/understand <change>`) |
| Optional catalog | `FEATURE_SLICES.*` |
| Feature | `<FEATURE>_DESIGN.md`, `<FEATURE>.contract.yaml` |
| Tests / queue | `<FEATURE>_TDD.*`, `<FEATURE>_TASKS.*` |
| Per task | `<FEATURE>_C<n>_REVIEW.*`, `<FEATURE>_C<n>_SNAPSHOT.*` |

## vs Greenfield

| | Brownfield | Greenfield |
|---|------------|------------|
| Spec | `/understand` + existing `SPEC.md` | `/grillme` |
| Architecture | Repo conventions (no `/system-hld` gate) | `/system-hld` |
| Slice | Optional | Required after HLD |
| Design inputs | `SPEC` + `UNDERSTAND` + `CONVENTIONS` | `SPEC` + `FEATURE_SLICES` + `SYSTEM_HLD` |

Principles (short): [BROWNFIELD_PRINCIPLES.md](BROWNFIELD_PRINCIPLES.md). Deprecated: `/plan-feature` → use `/design`.
