# agentic-dev-os

A **public, reusable AI engineering workflow framework** for coding agents (Cursor, Claude Code, Codex, Windsurf, Copilot, and compatible tools). It replaces mega-prompts with **bounded skills**, **vertical feature delivery**, and **contract-based handoffs** so humans stay architects and code owners.

> This repository ships the **framework only** — not a sample SaaS or application. Attach it to any project and drive work through slash-command skills.

**Full specification:** [AI_CONTEXT/SPEC.md](AI_CONTEXT/SPEC.md)  
**Step-by-step guide:** [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

## Why use it

| Problem | How this framework helps |
|---------|---------------------------|
| Giant uncontrolled codegen | `/implement` is one bounded task per invocation |
| Context window overload | Skills consume compact `*.contract.yaml`, not full prior docs |
| Architecture drift | `/system-hld` + `/slice` lock system shape before feature work |
| Markdown explosion | Short design docs (~200 lines) + machine contracts |
| “Plan everything horizontally” | Vertical slices only — one `FEATURE` end-to-end |

## Quick start (Cursor)

1. **Clone** this repo and open it in Cursor (skills are pre-synced under `.cursor/skills/`).
2. **Align the spec** — edit [AI_CONTEXT/SPEC.md](AI_CONTEXT/SPEC.md) or run **`/grillme`** in chat.
3. **Shape the system** — **`/system-hld`** then **`/slice`**.
4. **Deliver one feature** — e.g. **`/feature-design AUTH`** → **`/implement AUTH`** → **`/review`** → **`/debug`** → **`/snapshot`** → **`/learn`**.

To attach the framework to **your own** repository:

```powershell
# From your app repo (Windows)
path\to\agentic-dev-os\installer\install.ps1 -TargetPath .
```

See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for bash, lite vs full paths, and troubleshooting.

## Workflow overview

```text
Stage 1          Stage 2              Stage 3 (per FEATURE, pick what you need)
────────         ────────             ─────────────────────────────────────────
/grillme    →    /system-hld     →    /feature-questions  (optional)
                 /slice               /feature-research   (optional)
                                      /feature-design     (recommended)
                                      /feature-db         (if persistence)
                                      /feature-api        (if interfaces)
                                      /tdd                (optional)
                                      /tasksplit            (optional)
                                      /implement <FEATURE|TASK_ID>
                                      /review → /debug → /snapshot → /learn
```

Stage 3 is a **toolkit**, not a waterfall. Example lite path: `slice` → `feature-design` → `implement AUTH`.

## Slash commands

| Command | Purpose |
|---------|---------|
| `/grillme` | Interview-driven refinement of `AI_CONTEXT/SPEC.md` |
| `/system-hld` | System HLD + `SYSTEM_HLD.contract.yaml` |
| `/slice` | Vertical feature decomposition + `FEATURE_SLICES.contract.yaml` |
| `/feature-questions <FEATURE>` | Capture decision questions (optional) |
| `/feature-research <FEATURE>` | Objective codebase inspection (optional) |
| `/feature-design <FEATURE>` | Feature design + delivery flags |
| `/feature-db <FEATURE>` | Data contract (when needed) |
| `/feature-api <FEATURE>` | API contract (when needed) |
| `/tdd <FEATURE>` | Test plan contract (optional) |
| `/tasksplit <FEATURE>` | Task chunks e.g. `AUTH:C1` (optional) |
| `/implement <FEATURE\|TASK_ID>` | One bounded implementation unit |
| `/review` → `/debug` → `/snapshot` → `/learn` | Post-implementation loop |

Canonical skill sources: [`core/skills/`](core/skills/). Cursor mirrors: [`.cursor/skills/`](.cursor/skills/) (synced via installer).

## Repository map

```text
agentic-dev-os/
├── AI_CONTEXT/           # Durable product context (SPEC, PROJECT_STATE, emitted contracts)
├── core/
│   ├── AGENTS.md         # Canonical agent harness (edit here)
│   ├── skills/           # Canonical SKILL.md modules (edit here)
│   ├── templates/        # SPEC, PROJECT_STATE, SKILL templates
│   ├── contracts/        # Contract schemas and reference shapes
│   └── hooks/            # Hook manifests (summarize, checkpoint, trim)
├── adapters/             # Per-agent discovery paths (cursor, claude, codex, …)
├── installer/            # install.ps1, sync-cursor.ps1|.sh
├── examples/             # Example consumer walk-throughs (growing)
└── docs/                 # GETTING_STARTED and guides
```

**Rule:** Edit **`core/`** only. Run **`installer/sync-cursor.ps1`** (or `.sh`) to refresh `.cursor/`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Multi-agent support

| Agent | Adapter notes |
|-------|----------------|
| Cursor | [adapters/cursor/README.md](adapters/cursor/README.md) — `.cursor/AGENTS.md`, `.cursor/skills/` |
| Claude Code | [adapters/claude/README.md](adapters/claude/README.md) |
| Codex | [adapters/codex/README.md](adapters/codex/README.md) |
| Windsurf | [adapters/windsurf/README.md](adapters/windsurf/README.md) |
| Copilot | [adapters/copilot/README.md](adapters/copilot/README.md) |

Adapters document **where** each tool expects files after install; behavior lives in `core/`.

## Design principles

1. **No mega prompts** — small composable skills  
2. **Vertical implementation** — one feature end-to-end  
3. **Human code ownership** — review → test → debug → snapshot  
4. **Context rotation** — files over chat history  
5. **Separate questions / research / design**  
6. **Contract-based handoff** — human doc + `.yaml` contract  
7. **Short design docs** — compact markdown, rich contracts  

## Status

**v1 bootstrap** — skeleton, canonical skills, templates, Cursor sync, and installer are in place. Contract schemas, additional adapters, hooks automation, and `examples/` walk-throughs continue in later increments (see [AI_CONTEXT/SPEC.md](AI_CONTEXT/SPEC.md)).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Use issues and PRs on GitHub.

## License

[MIT](LICENSE) — use freely in personal and commercial projects.
