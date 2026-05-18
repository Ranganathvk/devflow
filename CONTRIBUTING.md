# Contributing

Thank you for helping improve **agentic-dev-os**. This repo is a **framework** (skills, contracts, templates, adapters)—not an application product.

## Where to edit

| Change | Edit here | Do not edit |
|--------|-----------|-------------|
| Skill workflow / prose | `core/skills/<name>/SKILL.md` | `.cursor/skills/` (derived) |
| Agent harness rules | `core/AGENTS.md` | `.cursor/AGENTS.md` (derived) |
| Doc templates | `core/templates/` | — |
| Contract schemas | `core/contracts/` | — |
| Cursor discovery notes | `adapters/cursor/README.md` | — |
| Product spec for **this** framework | `AI_CONTEXT/SPEC.md` | — |

After changing `core/`, run:

```powershell
.\installer\sync-cursor.ps1
```

```bash
chmod +x installer/sync-cursor.sh && ./installer/sync-cursor.sh
```

Commit both `core/` and the updated `.cursor/` mirror so Cursor users get changes without running sync.

## Skill design rules

From [AI_CONTEXT/SPEC.md](AI_CONTEXT/SPEC.md):

- **Small and bounded** — no mega-skills; compose orchestration instead.
- **Explicit I/O** — required inputs, forbidden inputs, exact outputs, files mutated.
- **Contract handoffs** — major stages emit paired human doc + `*.contract.yaml`.
- **Context budget** — downstream skills consume contracts + SPEC, not full prior narratives.

Use [core/templates/SKILL.template.md](core/templates/SKILL.template.md) for new skills.

## Pull request checklist

- [ ] Edits are under `core/` (or docs/adapters/installer as appropriate)
- [ ] `sync-cursor` run if skills or `core/AGENTS.md` changed
- [ ] No secrets, API keys, or `.env` files
- [ ] Skill remains ≤ ~200 lines of prose where applicable (per framework principle)
- [ ] README or GETTING_STARTED updated if user-facing behavior changed

## Reporting issues

Open a GitHub issue with:

- Agent/tool (Cursor, Claude Code, etc.)
- Slash command invoked
- Expected vs actual behavior
- Whether `AI_CONTEXT/SPEC.md` and relevant `*.contract.yaml` exist

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
