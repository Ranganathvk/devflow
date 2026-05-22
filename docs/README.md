# Documentation

Guides for using and extending **agentic-dev-os**.

## Start here

| Doc | Audience | Summary |
|-----|----------|---------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Everyone | Install, Cursor setup, workflow cheat sheets |
| [BROWNFIELD_DEV_LOOP.md](BROWNFIELD_DEV_LOOP.md) | Brownfield (existing repos) | Same command shape as greenfield (`/design` → `/tdd` → …) |
| [SIMPLE_DEV_LOOP.md](SIMPLE_DEV_LOOP.md) | Brownfield | Redirect to BROWNFIELD_DEV_LOOP |
| [GREENFIELD_DEV_LOOP.md](GREENFIELD_DEV_LOOP.md) | Greenfield (new products) | Spec → HLD → slice → design → implement |

## Reference

| Doc | Purpose |
|-----|---------|
| [BROWNFIELD_PRINCIPLES.md](BROWNFIELD_PRINCIPLES.md) | Locked operating principles for evolving existing codebases (skills implement these) |
| [../AI_CONTEXT/SPEC.md](../AI_CONTEXT/SPEC.md) | Framework product specification |
| [../core/AGENTS.md](../core/AGENTS.md) | Canonical agent harness rules |
| [../core/skills/README.md](../core/skills/README.md) | Skill catalog and paths |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | How to change the framework |
| [../installer/README.md](../installer/README.md) | Install and sync scripts |

## Choosing a workflow

```text
Existing codebase?  → BROWNFIELD_DEV_LOOP.md  (/understand → /design → /tdd → …)
New product?        → GREENFIELD_DEV_LOOP.md  (/grillme → /system-hld → …)
```

Both loops share **`/implement-next`**, **`/review`**, and **`/snapshot`** after plans or task queues are approved.
