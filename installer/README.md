# installer/

Bootstrap and sync utilities for attaching **devflow** to consumer repositories and keeping agent mirrors up to date.

## Scripts

| Script | Purpose |
|--------|---------|
| [`install.ps1`](install.ps1) | Copy `core/`, `adapters/`, seed `artifacts/`, sync Cursor skills into a **target repo** |
| [`sync-cursor.ps1`](sync-cursor.ps1) | Copy `core/AGENTS.md` + `core/skills/*` → `.cursor/` (Windows) |
| [`sync-cursor.sh`](sync-cursor.sh) | Same as above (macOS / Linux) |

## Install into your project

```powershell
# Windows — run from your application repo
C:\path\to\devflow\installer\install.ps1 -TargetPath C:\path\to\your-app
```

Parameters:

- **`-TargetPath`** (required) — root of the consumer repository  
- **`-Agent`** — currently only `cursor` (default)

## Sync after editing core/

When working **in this framework repo** (or after changing skills in an installed copy):

```powershell
.\installer\sync-cursor.ps1
```

```bash
chmod +x installer/sync-cursor.sh
./installer/sync-cursor.sh
```

Optional **`-RepoRoot`** (PowerShell) points at a different repo root when syncing an installed copy.

## What install does

1. Copies `core/` and `adapters/` into the target repo (if not already present from a submodule/copy).
2. Creates the context directory (default `artifacts/`) and seeds `devflow.context.yaml`, `SPEC.md`, and `PROJECT_STATE.md` from `core/templates/` when missing.
3. Materializes `.cursor/AGENTS.md` and `.cursor/skills/<name>/SKILL.md` from canonical `core/`.

Installer outputs are **derived** — never edit them as a second source of truth.

See [docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md) for the full workflow after install.
