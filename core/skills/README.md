# core/skills/

Canonical home of all framework skills. Each skill is a folder containing at least a `SKILL.md` (front-matter + workflow prose) and any helper assets.

## Authoring rules (from `AI_CONTEXT/SPEC.md`)

- Skills are **modular and reusable** — small, bounded, composable.
- Each `SKILL.md` defines: purpose, when to invoke, required/forbidden inputs, exact workflow steps, expected outputs, files mutated, context budget, failure handling.
- **No mega-skills.** Prefer orchestration of small skills over a monolith.
- Use the template at `core/templates/SKILL.template.md` to bootstrap a new skill.

## Implemented skills (canonical)

| Skill | Path |
|-------|------|
| `/grillme` | `core/skills/grillme/SKILL.md` |
| `/system-hld` | `core/skills/system-hld/SKILL.md` |
| `/slice` | `core/skills/slice/SKILL.md` |
| `/feature-questions <FEATURE>` | `core/skills/feature-questions/SKILL.md` |
| `/feature-research <FEATURE>` | `core/skills/feature-research/SKILL.md` |
| `/feature-design <FEATURE>` | `core/skills/feature-design/SKILL.md` |
| `/feature-db <FEATURE>` | `core/skills/feature-db/SKILL.md` |
| `/feature-api <FEATURE>` | `core/skills/feature-api/SKILL.md` |
| `/tdd <FEATURE>` | `core/skills/tdd/SKILL.md` |
| `/tasksplit <FEATURE>` | `core/skills/tasksplit/SKILL.md` |
| `/implement <TASK_ID \| FEATURE>` | `core/skills/implement/SKILL.md` |
| `/review <TASK_ID>` | `core/skills/review/SKILL.md` |
| `/debug <TASK_ID>` | `core/skills/debug/SKILL.md` |
| `/snapshot <TASK_ID>` | `core/skills/snapshot/SKILL.md` |
| `/learn <TASK_ID>` | `core/skills/learn/SKILL.md` |

## Derived locations

Skills under this folder are materialized to per-agent locations (for example `.cursor/skills/<name>/SKILL.md`) by the installer; see `adapters/<agent>/` for the discovery convention each tool uses.
