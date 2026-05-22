# core/skills/

Canonical home of all framework skills. Each skill is a folder containing at least a `SKILL.md` (front-matter + workflow prose) and any helper assets.

## Authoring rules (from `AI_CONTEXT/SPEC.md`)

- Skills are **modular and reusable** — small, bounded, composable.
- Each `SKILL.md` defines: purpose, when to invoke, required/forbidden inputs, exact workflow steps, expected outputs, files mutated, context budget, failure handling.
- **No mega-skills** at the dev-facing layer — orchestrators hide internal stages.
- Use the template at `core/templates/SKILL.template.md` to bootstrap a new skill.

## Developer-facing loops

### Brownfield — [BROWNFIELD_DEV_LOOP.md](../../docs/BROWNFIELD_DEV_LOOP.md)

| Skill | Path |
|-------|------|
| `/understand [change]` | `core/skills/understand/SKILL.md` |
| `/slice` (optional) | `core/skills/slice/SKILL.md` |
| `/design <FEATURE>` | `core/skills/design/SKILL.md` |
| `/tdd <FEATURE>` | `core/skills/tdd/SKILL.md` |
| `/tasksplit <FEATURE>` | `core/skills/tasksplit/SKILL.md` |
| `/implement-next [FEATURE]` | `core/skills/implement-next/SKILL.md` |
| `/review [TASK_ID]` | `core/skills/review/SKILL.md` |
| `/snapshot [TASK_ID]` | `core/skills/snapshot/SKILL.md` |
| `/plan-feature` | deprecated → `design` |

### Greenfield — [GREENFIELD_DEV_LOOP.md](../../docs/GREENFIELD_DEV_LOOP.md)

| Skill | Path |
|-------|------|
| `/grillme` | `core/skills/grillme/SKILL.md` |
| `/system-hld` | `core/skills/system-hld/SKILL.md` |
| `/slice` | `core/skills/slice/SKILL.md` |
| `/design <FEATURE>` | `core/skills/design/SKILL.md` |
| `/tdd <FEATURE>` | `core/skills/tdd/SKILL.md` |
| `/tasksplit <FEATURE>` | `core/skills/tasksplit/SKILL.md` |
| `/implement-next [FEATURE]` | `core/skills/implement-next/SKILL.md` |
| `/review [TASK_ID]` | `core/skills/review/SKILL.md` |
| `/snapshot [TASK_ID]` | `core/skills/snapshot/SKILL.md` |

### Advanced / partial

| Skill | Path |
|-------|------|
| `/workspace-scan`, `/convention-detect` | Phase 0 partial (prefer `/understand`) |
| `/feature-questions`, `/feature-research`, `/feature-design`, `/feature-db`, `/feature-api` | Greenfield partial (prefer `/design`) |
| `/implement <TASK_ID \| FEATURE>` | Explicit task invoke |
| `/debug`, `/learn` | Optional legacy |

## Derived locations

Skills under this folder are materialized to per-agent locations (for example `.cursor/skills/<name>/SKILL.md`) by the installer; see `adapters/<agent>/` for the discovery convention each tool uses.
