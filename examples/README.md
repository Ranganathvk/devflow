# examples/

Illustrative consumer setups for **devflow**. Examples are **not** authoritative — always follow `core/` and [artifacts/SPEC.md](../artifacts/SPEC.md).

## Planned examples

| Example | Shows |
|---------|--------|
| `minimal-auth/` *(planned)* | Lite path: `/slice` → `/design AUTH` → `/implement AUTH` |
| `full-auth/` *(planned)* | Full path with db, api, tdd, tasksplit, and review loop |

Until examples land, use [docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md) with your own `artifacts/SPEC.md`.

## Dogfooding

This framework repository **is** a consumer: `artifacts/SPEC.md` describes the framework itself. Cursor skills under `.cursor/skills/` are synced from `core/skills/` via `installer/sync-cursor.ps1`.
