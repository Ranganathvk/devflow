# core/

**Canonical** framework logic. Edits to skills, templates, contracts, hooks, and the framework-wide `AGENTS.md` happen **here only**.

Agent-specific locations (for example `.cursor/`, `.claude/`, `.codex/`, `.windsurf/`) are **derived** from this tree by the installer/sync described under `adapters/<agent>/`. Do not hand-edit derived copies; they will drift.

## Subtrees

| Path | Purpose |
|------|---------|
| `core/skills/` | Canonical `SKILL.md` modules (one bounded skill per folder). |
| `core/templates/` | Canonical boilerplate and doc templates (SPEC, PROJECT_STATE, SKILL, design stubs). |
| `core/contracts/` | Canonical contract **schemas** and reference shapes. Not the same as per-project emitted `*.contract.yaml` workflow outputs. |
| `core/hooks/` | Canonical hook scripts / manifests (summarize, contract-emit, checkpoint, trim). |
| `core/AGENTS.md` | Canonical framework agent guidance. |

See `artifacts/SPEC.md` for the full design contract.
