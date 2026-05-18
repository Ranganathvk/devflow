# examples/

Illustrative consumer setups for **agentic-dev-os**. Examples are **not** authoritative — always follow `core/` and [AI_CONTEXT/SPEC.md](../AI_CONTEXT/SPEC.md).

## Planned examples

| Example | Shows |
|---------|--------|
| `minimal-auth/` *(planned)* | Lite path: `/slice` → `/feature-design AUTH` → `/implement AUTH` |
| `full-auth/` *(planned)* | Full path with db, api, tdd, tasksplit, and review loop |

Until examples land, use [docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md) with your own `AI_CONTEXT/SPEC.md`.

## Dogfooding

This framework repository **is** a consumer: `AI_CONTEXT/SPEC.md` describes the framework itself. Cursor skills under `.cursor/skills/` are synced from `core/skills/` via `installer/sync-cursor.ps1`.
