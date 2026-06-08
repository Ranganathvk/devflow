---
name: <skill-slug>
description: >-
  One-or-two sentence description. State **what** the skill does and **when** to invoke it.
  Keep it scannable — agents read this to decide whether to use the skill.
---

# /<skill-slug> — <short human title>

## Purpose

2–4 sentences. What problem does this skill solve? What disciplined outcome does it guarantee? Mention the canonical inputs and outputs at a high level.

## When to invoke

- `/` <command> — <primary trigger>.
- <secondary trigger>.
- Do **not** invoke when <explicit anti-trigger>.

## Path resolution

All workflow paths use **`{context_dir}/`** (not a hardcoded folder name). Before step 1, resolve `{context_dir}` per `core/AGENTS.md` (env `DEVFLOW_CONTEXT_DIR` → `devflow.context.yaml` → default `artifacts`).

## Inputs

- **Required:** Paths the skill must read in full before starting.
- **Optional:** Paths that enrich the work if present.
- **Forbidden:** Inputs the skill must **not** read or rely on (e.g. unbounded chat history).

## Workflow

Numbered, exact steps. Each step is small and verifiable. Example shape:

1. Read inputs.
2. <Bounded action> — including the **smallest** set of files the skill is allowed to touch.
3. <Bounded action>.
4. Cross-check: list invariants the skill must verify before finishing.
5. Reply briefly in chat: paths written, gaps that need human input, suggested next skill.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `<path>` | Created / replaced / appended | <constraint, e.g. "≤200 lines"> |

No other files written or edited.

## Context budget

State expected context size: which files are read in full, which are read partially (with line ranges), and which are **not** read. The skill must fit comfortably below the agent's working context window.

## Failure handling

What to do when:

- A required input is missing → <e.g. ask one targeted question; do not invent>.
- An invariant fails → <e.g. stop and report; do not patch silently>.
- The skill would exceed its bounded scope → <e.g. propose a follow-up skill invocation>.

## Forbidden

- Mega-output (the skill must stay bounded).
- Editing files outside the **Output artifacts** table.
- Inventing scope the human or SPEC has not confirmed.
- Re-doing work already captured in upstream contracts.

## Quality bar (self-check before finishing)

- [ ] All outputs in the table above exist and pass their per-row constraints.
- [ ] No file outside the table was written.
- [ ] Gaps / open questions surfaced in chat (numbered list), not buried in prose.
