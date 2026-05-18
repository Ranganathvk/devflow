# core/templates/

Canonical boilerplate and document templates consumed by skills, the installer, and humans starting a new effort.

## Conventions

- Files end in `.template.md` (or `.template.<ext>`) so consumers can copy + rename without ambiguity about authoritativeness.
- Templates **must** stay short and skimmable; per SPEC, feature design docs target ~200 lines max.
- Update templates here, not in derived agent-specific copies.

## Foundational templates (current)

| File | Used for |
|------|----------|
| `SPEC.template.md` | Seed for a new consumer repo's `AI_CONTEXT/SPEC.md`. |
| `PROJECT_STATE.template.md` | Seed for `AI_CONTEXT/PROJECT_STATE.md` (durable state). |
| `SKILL.template.md` | Skeleton for authoring a new skill under `core/skills/`. |

Additional templates (feature design, DB stub, API stub, contract starters) will land in later increments per the SPEC bootstrap sequence.
