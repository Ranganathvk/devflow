# Brownfield principles

Short rules for evolving **existing** codebases. The workflow is **[BROWNFIELD_DEV_LOOP.md](BROWNFIELD_DEV_LOOP.md)** — skills implement these principles; do not use one mega-prompt.

## Locked rules

1. **Respect the codebase** — extend existing patterns; no speculative rewrites without approval.
2. **Surgical context** — IDE/search tools; no whole-repo dumps.
3. **Small bounded steps** — one design stage, one task, one implementation unit at a time.
4. **Files over chat** — `AI_CONTEXT/SPEC.md`, `*_DESIGN.md`, contracts are durable state.
5. **Human approval gates** — after each `/design` stage and before `/tdd`, `/tasksplit`, `/implement-next`, `/snapshot`.
6. **Delta thinking** — smallest safe change; blast radius documented in SPEC **Current change**.
7. **Same command path as greenfield** — `/design` → `/tdd` → `/tasksplit` → implement loop (profile differs, commands do not).

## When stuck

Stop and explain: unclear requirements, compat risk, missing conventions, or blast radius too large. Do not guess.

## Historical note

The long step-by-step mega workflow was retired in favor of bounded skills. For detail see skill sources under `core/skills/` (especially `understand`, `design`, `implement-next`).
