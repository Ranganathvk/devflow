# core/skills/

Canonical home of all framework skills. Each skill is a folder containing at least a `SKILL.md` (front-matter + workflow prose) and any helper assets.

## Authoring rules (from `{context_dir}/SPEC.md`)

- Skills are **modular and reusable** — small, bounded, composable.
- Each `SKILL.md` defines: purpose, when to invoke, required/forbidden inputs, exact workflow steps, expected outputs, files mutated, context budget, failure handling.
- **No mega-skills** at the dev-facing layer — orchestrators hide internal stages.
- Use the template at `core/templates/SKILL.template.md` to bootstrap a new skill.

## Dev Loop — [DEV_LOOP.md](../../docs/DEV_LOOP.md)

### Optional prelude

| Skill | Path |
|-------|------|
| `/grillme` | `core/skills/grillme/SKILL.md` |
| `/understand [change]` | `core/skills/understand/SKILL.md` |
| `/system-hld` | `core/skills/system-hld/SKILL.md` |
| `/slice` | `core/skills/slice/SKILL.md` |

### Core loop (per feature)

| Skill | Path |
|-------|------|
| `/design <FEATURE>` | `core/skills/design/SKILL.md` |
| `/tdd <FEATURE>` | `core/skills/tdd/SKILL.md` |
| `/tasksplit <FEATURE>` | `core/skills/tasksplit/SKILL.md` |
| `/implement-next [FEATURE]` | `core/skills/implement-next/SKILL.md` |
| `/review [TASK_ID]` | `core/skills/review/SKILL.md` |
| `/snapshot [TASK_ID]` | `core/skills/snapshot/SKILL.md` |
| `/plan-feature`, `/feature-*` | Deprecated → `/design` |

### Advanced / partial

| Skill | Path |
|-------|------|
| `/workspace-scan`, `/convention-detect` | Orientation partial (prefer `/understand`) |
| `/implement <TASK_ID \| FEATURE>` | Explicit task invoke |
| `/debug`, `/learn` | Optional |

## Derived locations

Skills under this folder are materialized to per-agent locations (for example `.cursor/skills/<name>/SKILL.md`) by the installer; see `adapters/<agent>/` for the discovery convention each tool uses.
