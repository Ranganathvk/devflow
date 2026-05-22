---
name: plan-feature
description: >-
  DEPRECATED — use /design instead. Brownfield planning now uses /design with the same stage-wise
  approval gates and _DESIGN.md artifacts, aligned with the greenfield command path (/tdd, /tasksplit).
---

# /plan-feature — Deprecated

**Use `/design`** per [BROWNFIELD_DEV_LOOP.md](../../docs/BROWNFIELD_DEV_LOOP.md).

| Old | New |
|-----|-----|
| `/plan-feature "…"` | `/design "…"` |
| `/plan-feature <FEATURE> approved` | `/design <FEATURE> approved` |
| `<FEATURE>_PLAN.md` | `<FEATURE>_DESIGN.md` |
| `plan_status` on `*_PLAN.contract.yaml` | `design_status` on `<FEATURE>.contract.yaml` |
| `/implement-next` (plan queue) | `/tdd` → `/tasksplit` → `/implement-next` (tasks queue) |

This skill remains only so old slash invocations can be redirected. Do not extend.
