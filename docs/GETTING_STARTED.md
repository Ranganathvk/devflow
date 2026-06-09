# Getting started

This guide walks through using **devflow** in a real project with **Cursor**. Other agents follow the same `core/` sources; adapter notes live under `adapters/<agent>/`.

## What you get

- **Bounded skills** (`/grillme`, `/system-hld`, `/implement`, …) instead of mega-prompts
- **Vertical feature delivery** — one slice end-to-end, not "all DB then all APIs"
- **Contract handoffs** — compact `*.contract.yaml` files downstream skills consume
- **Human ownership** — review → snapshot on every task; optional `/debug` and `/learn`

Full product definition: [artifacts/SPEC.md](../artifacts/SPEC.md).

## Dev Loop (cheat sheet)

```text
Optional prelude: /grillme | /understand | /system-hld | /slice

Core loop: /design FEATURE → /tdd → /tasksplit → /implement-next → /review → /snapshot
```

Full guide: **[DEV_LOOP.md](DEV_LOOP.md)**.

## Option A — Use this framework repo as a template

1. **Clone** this repository (or use it as a GitHub template).
2. Open the repo in **Cursor**. Skills are under `.cursor/skills/` (synced from `core/skills/`).
3. Replace placeholders in `artifacts/SPEC.md`, or start with **`/grillme`**.
4. Run the Dev Loop stage by stage.

## Option B — Attach to an existing repository

From PowerShell (Windows):

```powershell
git clone https://github.com/YOUR_ORG/devflow.git
cd your-existing-app
..\devflow\installer\install.ps1 -TargetPath .
```

From bash (macOS / Linux):

```bash
git clone https://github.com/YOUR_ORG/devflow.git
cd your-existing-app
chmod +x ../devflow/installer/install.sh
../devflow/installer/install.sh .
```

The installer copies `core/` and `adapters/`, seeds `artifacts/`, and syncs to `.cursor/`.

Or use the CLI:

```powershell
devflow-ai cursor install --scope repo
devflow-ai claude install --scope repo
devflow-ai copilot install --scope repo
```

### Context directory (custom name)

Workflow files live under a **context directory** at the repo root (default **`artifacts/`**).

**Recommended — one command (repo install):**

```powershell
cd C:\path\to\your-app
devflow-ai cursor install --scope repo --context-dir my-workflow
```

That writes `devflow.context.yaml`, creates `my-workflow/SPEC.md`, and syncs skills with `my-workflow/…` paths materialized in `.cursor/skills/`.

**Other ways to set the folder name:**

| Method | When to use |
|--------|-------------|
| `--context-dir my-workflow` on `devflow <agent> install` | Easiest; sets manifest + install in one step |
| `devflow.context.yaml` with `context_dir: my-workflow` | Commit the name in repo; then run install without `-c` |
| `DEVFLOW_CONTEXT_DIR=my-workflow` env var | CI or shell profile; overrides manifest |

**Then install skills** (if you did not use the CLI above):

```powershell
devflow-ai cursor install --scope repo      # this project
devflow-ai cursor install --scope global    # all Cursor projects (keeps {context_dir} token)
```

Canonical skills under `core/skills/` use **`{context_dir}/`**; repo install **materializes** it to your folder in agent mirrors.

Then run **`/understand`** when working in an existing repo, or **`/grillme`** when shaping spec from scratch.

## Optional per-feature modules

| Command | When |
|---------|------|
| `/implement <TASK_ID>` | Explicit task invoke |
| `/debug`, `/learn` | Optional after review |

All design work (questions, research, DB, API classification) runs inside **`/design`**.

**Lite path:** `/slice` → minimal `/design` → `/implement <FEATURE>` → review loop.

## Key folders after install

| Path | Purpose |
|------|---------|
| `devflow.context.yaml` | Context directory name for this repo |
| `artifacts/SPEC.md` | Your product spec (default context dir) |
| `artifacts/PROJECT_STATE.md` | Status, decisions, blockers |
| `artifacts/*.contract.yaml` | Machine-readable handoffs |
| `core/skills/` | Canonical skills (**edit here**) |
| `.cursor/skills/` | Cursor mirror (**run sync**) |
| `core/AGENTS.md` | Agent harness rules |

## Sync after editing skills

```powershell
.\installer\sync-cursor.ps1
```

```bash
./installer/sync-cursor.sh
```

## Tips

1. **Keep SPEC decisive** — `/grillme` aligns intent, not endless brainstorming.
2. **One feature at a time** — pick a slice, then run the core loop for that `FEATURE`.
3. **Trust contracts** — downstream skills read `*.contract.yaml`.
4. **Never skip review** — humans own merge quality via `/review` and tests.

## Next reads

- [DEV_LOOP.md](DEV_LOOP.md)
- [DELTA_PRINCIPLES.md](DELTA_PRINCIPLES.md)
- [core/AGENTS.md](../core/AGENTS.md)
- [adapters/cursor/README.md](../adapters/cursor/README.md)
