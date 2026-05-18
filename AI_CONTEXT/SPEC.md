# Product specification — agentic-dev-os

## Summary

**agentic-dev-os** is a **public, production-quality, reusable AI engineering workflow framework** (not a customer application). It targets multiple coding agents and AGENTS.md-style tools (Codex, Claude Code, Cursor, Windsurf, Copilot, and future compatible agents) through a shared **core** plus thin **adapters**.

**Scope decision (agreed):** This repository’s authoritative product is **the framework only**. A prior draft in this file described a separate **post-deploy DevOps AI agent** product; that content is **superseded** and is **out of scope** for this repo unless reintroduced as an explicit, separate effort elsewhere.

## Product boundary

- **In scope:** Skills, templates, contracts, hooks, adapters, installer, examples, and documentation that enforce deterministic, bounded workflows across projects.
- **Out of scope (v1 of this SPEC):** Shipping a hosted or vertical “application” (SaaS, control plane product) as the deliverable of this framework repo.

## Core goal

Provide a **deterministic AI engineering operating system** that mitigates:

- Giant uncontrolled code generation  
- Context window overload and mega prompts  
- Architecture drift and horizontal “plan everything” passes  
- Markdown explosion and unreviewed AI output

The framework **enforces** disciplined workflows; the **human** remains architect, reviewer, decision maker, and code owner. **AI** acts as a bounded pair engineer and workflow executor.

## Design principles (locked)

1. **No mega prompts** — Split work into **bounded skills**; prefer small orchestrated workflows over monolithic skills.
2. **Vertical implementation only** — One feature end-to-end (not all DB, then all APIs, then all UI).
3. **Human code ownership** — Every implementation path includes **review → test → debug → snapshot** (and related stages in the locked workflow below).
4. **Context rotation** — Broad phases use broad context; deep work uses **narrow, surgical** context; avoid unbounded chat history as the source of truth.
5. **Separate questions / research / design** — Do not mix speculative design with objective repo inspection. Preferred order is **Questions → Research → Design → Implementation**, but these are **optional modules per feature** (not a mandatory chain for every slice).
6. **Contract-based handoff** — Major artifacts emit a **human-readable doc** and a **machine-readable compact contract** (`.yaml`); downstream steps consume **contracts**, not giant prior docs.
7. **Short design docs** — Feature design docs stay **compact** (order of **~200 lines max** per doc).

## Locked workflow (slash commands)

**Stage 1 — Spec alignment**

- `/grillme`

**Stage 2 — System shape**

- `/system-hld`  
- `/slice`

**Stage 3 — Per vertical feature** (repeat per feature, e.g. `AUTH`)

Stage 3 is a **toolkit**. Commands are **pick-what-you-need** per feature; they are not a forced waterfall.

- `/feature-questions <FEATURE>` *(optional quality gate)*  
- `/feature-research <FEATURE>` *(optional evidence pass)*  
- `/feature-design <FEATURE>` *(recommended for non-trivial features; can also set delivery flags)*  
- `/feature-db <FEATURE>` *(only when the feature needs persistence)*  
- `/feature-api <FEATURE>` *(only when the feature needs an interface contract)*  
- `/tdd <FEATURE>` *(optional planning depth; recommended when risk is non-trivial)*  
- `/tasksplit <FEATURE>` *(optional; use when chunking into `FEATURE:Cn` tasks helps execution)*  
- `/implement <FEATURE>` *(lite direct path)* or `/implement <TASK_ID>` *(task-based path)*  
- `/review <TASK_OR_FEATURE>` → `/debug <TASK_OR_FEATURE>` → `/snapshot <TASK_OR_FEATURE>` → `/learn <TASK_OR_FEATURE>`

**Illustration (full path):** `AUTH` can run questions → research → design → db → api → tdd → tasksplit → e.g. `AUTH:C1` → review → debug → snapshot.

**Illustration (lite path):** `AUTH` can run slice context + minimal design flags, then go directly to `/implement AUTH` when DB/API/tasksplit are not required.

## Repository layout (target)

```text
agentic-dev-os/
  core/
    skills/
    templates/
    contracts/
    hooks/
    AGENTS.md
  adapters/
    codex/
    cursor/
    claude/
    windsurf/
    copilot/
  installer/
  examples/
```

- `**core/**` — Universal logic (skills, templates, contracts, hooks, `AGENTS.md`).  
- `**adapters/**` — Thin compatibility wrappers per agent/tooling.  
- `**installer/**` — Bootstrap so consumers attach the framework to **any** repo with minimal copy/paste.  
- `**examples/`** — Example usage.

### Authoritative skills (v1, agreed)

- **Canonical definitions** live only under `**core/skills/`**. Skill behavior and prose are **edited there**.  
- **Agent-specific skill directories** (for example `.cursor/skills/`) are **derived**: the **installer** or a documented **sync** step materializes them from `core/skills/` (copy, render, or equivalent). They are **not** a parallel source of truth to maintain by hand.  
- `**adapters/<agent>/`** describe how that agent **discovers** skills after sync (paths, naming, invocation conventions).

### Authoritative AGENTS.md (v1, agreed)

- **Canonical** framework agent guidance lives only in `**core/AGENTS.md`**. Edits happen there.  
- **Per-agent `AGENTS.md`** files (for example `**.cursor/AGENTS.md**`) are **derived** by the same **installer/sync** story as skills: they are **not** a second authoritative copy to drift independently.  
- `**adapters/<agent>/`** document where each tool expects `AGENTS.md` on disk after sync and any filename quirks.

### Authoritative templates, contracts, hooks (v1, agreed)

- `**core/templates/**` — **Canonical** boilerplate and doc templates. Any agent-local copies (for example under `.cursor/`) are **derived** via installer/sync, not a parallel edited source.  
- `**core/contracts/`** — **Canonical** contract **schemas**, **reference shapes**, and framework-owned samples that skills and tooling depend on. This is **not** the same path family as **per-project emitted** `*.contract.yaml` artifacts (for example `AUTH.contract.yaml`); those are **workflow outputs** in the consumer repo and are governed by the artifact pattern + installer layout, but **framework definitions** still originate in `core/contracts/`.  
- `**core/hooks/`** — **Canonical** hook scripts or manifests (summarize, contract emit, checkpoint, trim). Agent-specific hook registration paths are **derived** via installer/sync.  
- **Rule:** For all of the above, **edit in `core/`**; **installer/sync** materializes agent-specific locations documented under `**adapters/<agent>/`**.

## Skill design rules

Each skill is **modular and reusable** and defines at minimum:

- Purpose; when to invoke  
- Required inputs; forbidden inputs  
- Exact workflow steps; expected outputs  
- Files mutated; context budget guidance; failure handling

Do **not** author giant monolithic skills.

## Artifact pattern

Major workflows emit **paired** artifacts:


| Human doc             | Machine contract           |
| --------------------- | -------------------------- |
| e.g. `SYSTEM_HLD.md`  | `SYSTEM_HLD.contract.yaml` |
| e.g. `AUTH_DESIGN.md` | `AUTH.contract.yaml`       |
| e.g. `AUTH_DB.md`     | `AUTH_DB.contract.yaml`    |
| e.g. `AUTH_API.md`    | `AUTH_API.contract.yaml`   |


## Context strategy

Downstream skills must **not** require loading entire prior narrative outputs.

- **Good:** e.g. `feature-db` consumes `AI_CONTEXT/SPEC.md`, `SYSTEM_HLD.contract.yaml`, and `FEATURE.contract.yaml`.  
- **Bad:** `feature-db` consumes full HLD prose, full design history, or giant chat context.

## Implementation rules

- `**/implement`** — Exactly **one bounded task**; no unrelated files; no speculative abstractions; obey architecture rules; **stop** after bounded completion.  
- `**/tasksplit`** — Produces **dependency-ordered** task units (e.g. `AUTH:C1`, `AUTH:C2`, `AUTH:C3`).

## Subagents and hooks

Subagents (e.g. HLD, slice, risk, research) are allowed where they reduce risk or specialize work. **Hooks** must only: summarize, generate contracts, checkpoint state, trim context — **never** to bloat context.

## Reuse and installer

The framework must be **reusable across projects** with **low duplication**; the **installer/bootstrap** story is a first-class requirement so teams attach the framework **cleanly** to arbitrary repos.

### Consumer repository layout (v1, agreed)

- **Attached repos** use a **fixed** top-level folder `**AI_CONTEXT/`** for **human-owned durable context** (at minimum `**AI_CONTEXT/SPEC.md`**; optional companions such as `**AI_CONTEXT/PROJECT_STATE.md**` when skills reference them).  
- The **installer** creates `**AI_CONTEXT/`** when missing and may seed starter files; skills and templates **default** to paths under `**AI_CONTEXT/`** so handoffs stay predictable.  
- **Per-project emitted** artifacts (for example `*.contract.yaml`, feature design stubs) use locations **defined by the emitting skills** — often under `**AI_CONTEXT/`** or a documented subfolder — **TBD per skill**, but the **stable anchor name** remains `**AI_CONTEXT/`** at the **consumer repo root**.

### Durable SPEC path (v1, agreed)

- The **only authoritative product specification** in an attached repo (including this framework repo when dogfooding) is `**AI_CONTEXT/SPEC.md`**. Skills that require “the SPEC” **read and update this path** unless a skill explicitly documents a rare, scoped exception.  
- **No root-level `spec.md` (agreed):** This framework repo **does not** keep a second spec-shaped file at the repository root. `**README.md`** is the **primary** entry for humans and **must** link to `**AI_CONTEXT/SPEC.md`** for the full product specification. Any historical root `**spec.md**` is **removed** once that link exists (same rule for other attached repos that adopt this framework: avoid duplicate root specs).

## Bootstrap sequence (agreed first increment)

Build **incrementally**; do not generate the entire framework in one shot. Initial milestone:

1. Repo skeleton matching the layout above (as applicable).
2. `core/AGENTS.md`.
3. First foundational templates.
4. **Stop and wait** for the next guided increment.

## Success criteria (v1 framework)

- A new team can follow the **locked workflow** using repo-local skills/contracts without mega-prompts or horizontal whole-system planning.  
- **Vertical** feature delivery is the default path; artifacts and contracts are **consumable** by the next stage without re-loading full chat.  
- **Adapters** allow the same core behaviors to be invoked from **more than one** supported agent class without forking core logic.

## Known tricky parts

- Keeping skills **small** yet **composable** without exploding the number of files.  
- **Contract schema** stability so downstream automation does not churn unnecessarily.  
- **Installer** ergonomics across OSes and agent products without brittle paths.

## Open items (TBD in implementation)

- Exact contract YAML schemas per artifact type.  
- Which slash commands are implemented first after bootstrap.  
- Adapter surface per tool (Cursor vs Windsurf vs Copilot, etc.).

---

*Version:* framework SPEC; DevOps-agent draft superseded (**A — Framework only**); authoritative `**core/`** tree with agent-local mirrors **derived** via installer/sync (**A** ×3); consumer `**AI_CONTEXT/`** anchor (**A**); durable SPEC **only** `**AI_CONTEXT/SPEC.md`**; **no root `spec.md`** — `**README.md**` links here (**A**, 2026-05-13).