# Claude Code adapter

How **devflow** materializes on disk for [Claude Code](https://code.claude.com).

## Materialized paths

| Canonical source | Claude Code path | Role |
|------------------|------------------|------|
| `core/AGENTS.md` | `.claude/AGENTS.md` | Agent harness |
| `core/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | Slash-command skills |
| *(generated on install)* | `CLAUDE.md` | Points at `@.claude/AGENTS.md` when missing |

### User-level (global)

| Canonical source | Path | Role |
|------------------|------|------|
| `core/AGENTS.md` | `~/.claude/AGENTS.md` | Harness across all projects |
| `core/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` | Skills across all projects |

## Install

```bash
devflow-ai claude install
devflow-ai claude install --scope repo -p /path/to/your-app
devflow-ai claude install --scope global
```

## Discovery

- Claude Code loads skills from **`.claude/skills/<name>/SKILL.md`** (project) or **`~/.claude/skills/`** (user).
- Invoke in chat with **`/<name>`** (e.g. `/understand`, `/design AUTH`).
- **Dev Loop:** [docs/DEV_LOOP.md](../../docs/DEV_LOOP.md)

## Rules

- **Edit `core/skills/`**, not `.claude/skills/` — then re-run `devflow-ai claude install`.
- Read `artifacts/SPEC.md` before non-trivial work.

See [docs/GETTING_STARTED.md](../../docs/GETTING_STARTED.md) and [core/AGENTS.md](../../core/AGENTS.md).
