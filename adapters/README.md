# adapters/

Thin compatibility wrappers per coding agent / AGENTS.md-respecting tool.

## Purpose

Each `adapters/<agent>/` folder documents:

- **Where** the agent expects `AGENTS.md`, skills, hooks, and other artifacts on disk after the installer/sync step.
- **How** the agent discovers and invokes skills (filename conventions, slash-command surfacing, MCP wiring, etc.).
- Any tool-specific quirks (filename casing, multiple agent files, hook manifest format).

Adapters **do not** fork core behavior — they only describe the materialization path. Canonical sources still live under `core/`.

## Supported agents (target v1)

| Folder | Tool |
|--------|------|
| `adapters/codex/` | OpenAI Codex CLI / Codex-style agents |
| `adapters/cursor/` | Cursor (Desktop, IDE, CLI, Cloud Agents) |
| `adapters/claude/` | Anthropic Claude Code |
| `adapters/windsurf/` | Windsurf |
| `adapters/copilot/` | GitHub Copilot (where AGENTS.md applies) |

Adapter contents will land in later increments per the SPEC bootstrap sequence.
