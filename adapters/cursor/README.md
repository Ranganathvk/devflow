# Cursor adapter

How **agentic-dev-os** materializes on disk for [Cursor](https://cursor.com) (Desktop, IDE, CLI, Cloud Agents).

## Materialized paths

| Canonical source | Cursor path | Role |
|------------------|-------------|------|
| `core/AGENTS.md` | `.cursor/AGENTS.md` | Agent harness — read first |
| `core/skills/<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` | Slash-command skills |
| `core/hooks/` *(future)* | `.cursor/hooks/hooks.json` | Summarize, contract-emit, checkpoint, trim |
| `core/templates/` | *(via installer into `AI_CONTEXT/`)* | Consumer spec templates |

Run [`installer/sync-cursor.ps1`](../../installer/sync-cursor.ps1) (or `.sh`) after any change under `core/`.

## Discovery

- Cursor loads skills from **`.cursor/skills/<name>/SKILL.md`** with YAML front matter (`name`, `description`).
- Invoke in chat with **`/<name>`** (e.g. `/understand "add OTP"`, `/design OTP_LOGIN`, `/implement-next`).
- **Brownfield default:** [docs/BROWNFIELD_DEV_LOOP.md](../../docs/BROWNFIELD_DEV_LOOP.md) — same shape as greenfield after `/understand`.
- The agent should follow **`core/AGENTS.md`** content (mirrored to `.cursor/AGENTS.md`).

## Consumer repo layout

After [`install.ps1`](../../installer/install.ps1):

```text
your-app/
├── AI_CONTEXT/
│   ├── SPEC.md              # Your product spec
│   └── PROJECT_STATE.md     # Living status
├── core/                    # Canonical framework (from install)
├── adapters/
└── .cursor/
    ├── AGENTS.md
    └── skills/
```

## Rules for agents

- **Edit `core/skills/`**, not `.cursor/skills/` — then re-sync.
- Read `AI_CONTEXT/SPEC.md` before non-trivial work.
- Downstream skills consume `*.contract.yaml`, not full prior markdown.

See [docs/GETTING_STARTED.md](../../docs/GETTING_STARTED.md) and [core/AGENTS.md](../../core/AGENTS.md).
