# GitHub Copilot adapter

How **devflow** materializes on disk for [GitHub Copilot](https://github.com/features/copilot) agent skills.

## Materialized paths

| Canonical source | Copilot path | Role |
|------------------|--------------|------|
| `core/AGENTS.md` | `AGENTS.md` (repo root) | Agent harness |
| `core/skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md` | Agent skills |

### User-level (global)

| Canonical source | Path | Role |
|------------------|------|------|
| `core/AGENTS.md` | `~/.copilot/AGENTS.md` | Harness across all projects |
| `core/skills/<name>/SKILL.md` | `~/.copilot/skills/<name>/SKILL.md` | Skills across all projects |

Copilot also reads `.claude/skills/` for backward compatibility; devflow uses the recommended `.github/skills/` layout.

## Install

```bash
devflow-ai copilot install
devflow-ai copilot install --scope repo -p /path/to/your-app
devflow-ai copilot install --scope global
```

## Discovery

- Copilot loads skills from **`.github/skills/<name>/SKILL.md`** (project) or **`~/.copilot/skills/`** (user).
- Skills are auto-invoked when relevant, or via **`/<name>`** in VS Code agent mode.
- **Dev Loop:** [docs/DEV_LOOP.md](../../docs/DEV_LOOP.md)

## Rules

- **Edit `core/skills/`**, not `.github/skills/` — then re-run `devflow-ai copilot install`.
- Read `artifacts/SPEC.md` before non-trivial work.

See [docs/GETTING_STARTED.md](../../docs/GETTING_STARTED.md) and [core/AGENTS.md](../../core/AGENTS.md).
