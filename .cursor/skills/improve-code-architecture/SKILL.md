---
name: improve-code-architecture
description: >-
  Scan a codebase for deepening opportunities, present them as a markdown report in chat, then
  grill through whichever candidate the human picks. Invoke /improve-code-architecture for
  brownfield architecture friction, shallow modules, or testability seams. Does not implement code.
disable-model-invocation: true
---

# /improve-code-architecture — Deepen shallow modules

## Purpose

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is **testability**, **locality**, and **AI-navigability** without starting implementation.

This command is informed by the project's domain language and a fixed architecture vocabulary (§ Architecture vocabulary). Use those terms exactly in every suggestion — do not drift into "component," "service," "API," or "boundary."

## When to invoke

| Invocation | When |
|------------|------|
| `/improve-code-architecture` | Brownfield repo; recurring change pain; hard-to-test areas; modules that sprawl across paths |
| `/improve-code-architecture <path or subsystem>` | Human named a direction — scope to that area; skip hot-spot inference |
| After `/understand` | Optional depth pass when blast radius or conventions reveal structural friction |
| Before large `/design` | Optional — clarify seams before feature LLD |

Do **not** invoke for greenfield-only repos with no application code. Do **not** implement refactors inside this skill — hand off to `/design` → `/tasksplit` → `/implement-next` after grilling.

## Context root

Do **not** assume the folder is named `AI_CONTEXT`. Resolve **`<context-root>`** — the directory where this repo keeps harness artifacts (`SPEC.md`, contracts, HLD/LLD) — before reading inputs or writing grilling updates.

**Resolution order:**

1. **Harness read-order** — path named in the materialized `AGENTS.md` (or equivalent harness) for SPEC / project state.
2. **Human hint** — `@`-attached SPEC, or an explicit path in the message.
3. **Discover** — locate the product `SPEC.md` (same tree as `PROJECT_STATE.md` and/or `*.contract.yaml` from prior skills). Prefer the directory contracts reference via `spec_path` or sibling `*_contract.yaml` paths.
4. **Ambiguous** — ask **one** question: which directory is `<context-root>`?

Use `<context-root>/…` in all paths below. If the human renames the folder mid-session, follow the new path.

## Inputs

| Input | Role |
|-------|------|
| `<context-root>/SPEC.md` | Domain vocabulary and product boundary — read in full |
| `<context-root>/PROJECT_STATE.md` | Prior decisions, active work — read when present |
| `<context-root>/CONVENTIONS.contract.yaml` | Naming and layout evidence — prefer over rescanning |
| `<context-root>/PROJECT_OVERVIEW.contract.yaml` | Module boundaries guess — optional |
| `docs/adr/*.md` | Recorded decisions — do not re-litigate without real friction |
| Consumer repo tree | Exploration target |

**Forbidden:** Treating chat as durable state (update `<context-root>/` only in grilling phase); writing the review into the repo; proposing concrete interfaces before the human picks a candidate; horizontal "refactor everything" passes.

## Architecture vocabulary

Use **exactly** these terms (adapted from module-depth design practice):

| Term | Meaning |
|------|---------|
| **module** | A unit of code with one outward **interface** and hidden **implementation** |
| **interface** | What callers depend on — the test surface |
| **implementation** | Everything behind the interface |
| **depth** | Interface much smaller than implementation (deep) vs nearly equal (shallow) |
| **seam** | Substitutable edge between modules |
| **adapter** | Code that sits on a seam (IO, clock, ID generator, HTTP client) |
| **leverage** | One interface change affects many call sites safely |
| **locality** | Related behavior lives in one module; bugs concentrate where tests aim |

**Principles:**

- **Deletion test:** Would deleting this module concentrate complexity, or just move it? "Concentrates" signals a good deepening target.
- **Interface is the test surface:** Tests should exercise the module through its interface, not scattered helpers.
- **One adapter = hypothetical seam; two adapters = real seam** (e.g. prod HTTP + in-memory fake).

**Never substitute:** component/service/unit (for module) · API/signature (for interface) · boundary (for seam) · layer/wrapper (when you mean module).

## Workflow

### 1 — Explore

**Scope before you scan — YAGNI.** Deepening pays off where future changes concentrate. Decide *where* to look before you look:

- **Human named a direction** (path, subsystem, pain point) → take it; skip hot-spot inference below.
- **Otherwise** — walk commit history (`git log --oneline -40` or similar) for hot spots; prioritize paths that keep changing. If changes are scattered, widen the net.

**Read first:** `<context-root>/SPEC.md` (domain names for seams), `<context-root>/PROJECT_STATE.md`, ADRs under `docs/adr/` in the scoped area.

Use the **Task** tool with `subagent_type=Explore` (or direct search when narrow) to walk the codebase. Explore organically; note friction:

- Understanding one concept requires bouncing between many small modules
- Modules are **shallow** — interface nearly as complex as implementation
- Pure functions extracted for tests, but bugs hide in call patterns (**no locality**)
- Tightly coupled modules **leak** across seams
- Untested or hard-to-test areas through the current interface

Apply the **deletion test** to suspected shallow modules.

### 2 — Present candidates (markdown report)

Post the review **in chat** as markdown — do not write report files to the repo or temp directory.

Target **≤ ~150 lines** total. Structure:

| Section | Content |
|---------|---------|
| Header | Repo name, scope, date |
| Each candidate | Title + strength; Files; Problem; Solution; Wins (glossary bullets); Before/After (Mermaid or ASCII); optional ADR blockquote |
| Top recommendation | One candidate + one sentence why |

Example candidate skeleton (Mermaid blocks are separate fenced blocks in the chat reply, not nested):

    ### 1. Collapse Order intake — **Strong**
    **Files:** `src/orders/intake.ts`, …
    **Problem:** …
    **Solution:** …
    **Wins:** locality / leverage / tests bullets
    **Before:** (mermaid flowchart or bullet hop list)
    **After:** (mermaid flowchart or bullet hop list)

Per candidate include:

- **Files** — involved paths/modules
- **Problem** — why current architecture causes friction
- **Solution** — plain English deepening (no concrete interface signatures yet)
- **Wins** — bullets using glossary terms (locality, leverage, interface, seam)
- **Before / After** — optional Mermaid `flowchart` or `sequenceDiagram` when a graph helps; otherwise a short ASCII sketch or bullet list of module hops
- **Recommendation strength** — `Strong` | `Worth exploring` | `Speculative`

**Domain language:** Use SPEC vocabulary (e.g. "Order intake module" if SPEC defines Order) — not internal handler class names alone.

**ADR conflicts:** If a candidate contradicts `docs/adr/*`, surface only when friction warrants reopening. Use a blockquote callout: *"contradicts ADR-0007 — worth reopening because…"*

**Tone:** Plain English, no hedging. Do not write *"easier to maintain"* or *"cleaner code"* — name gains in glossary terms.

After the report, ask **one** question:

```markdown
**Question:** Which deepening candidate should we explore?

(list candidate titles as A / B / C … with one-line summaries)

**Recommended:** … (anchor to Top recommendation)
```

Do **not** propose interfaces yet.

### 3 — Grilling loop (after human picks)

Run [grillme](../grillme/SKILL.md) **behavior** for the chosen candidate — one question per turn, recommended answers, radio-style options for pick-one:

| Scope of deepening | Handoff |
|--------------------|---------|
| System-wide seam / container shape | `/grillme hld` — update `<context-root>/SYSTEM_HLD*` only |
| Single feature or bounded subsystem | `/grillme lld <FEATURE>` — update `<context-root>/<FEATURE>_DESIGN*` only |
| Product boundary or domain term unclear | `/grillme spec` — high-level SPEC only |

Walk the decision tree: constraints, dependencies, shape of the deepened module, what sits behind the seam, which tests survive.

**Inline side effects as decisions crystallize:**

- **New domain term not in SPEC?** Add to `<context-root>/SPEC.md` at product level only (no stack/API detail).
- **Sharpening a fuzzy term?** Update `<context-root>/SPEC.md` or `<context-root>/PROJECT_STATE.md` in the same turn.
- **Human rejects with a load-bearing reason?** Offer: *"Record this in `<context-root>/PROJECT_STATE.md` or `docs/adr/` so future reviews don't re-suggest it?"* Skip ephemeral reasons ("not now").
- **Alternative interface shapes?** Explore two options in parallel (design-it-twice) before committing — still one question per turn when presenting to the human.

**Session end handoff** (no code):

```text
Deepening decisions captured in <artifact paths>.

Next:
  /slice              — if the deepening implies new feature boundaries
  /design <FEATURE>   — per-feature LLD for the chosen deepening
  /understand         — refresh blast radius before implementation
  /tasksplit → /implement-next — when design is approved
```

## Output artifacts

| Phase | Output | Location |
|-------|--------|----------|
| Explore + report | Markdown review | Chat only |
| Grilling | HLD, LLD, SPEC, or PROJECT_STATE updates | `<context-root>/` per grillme rules |
| Optional rejection record | ADR or PROJECT_STATE decision | `docs/adr/` or `<context-root>/PROJECT_STATE.md` |

No application source edits inside this skill.

## Forbidden

- Writing the review or scratch analysis into the repo (chat-only until grilling updates `<context-root>/`)
- Multiple substantive questions per message (grilling phase)
- Implementing refactors or marking design artifacts approved
- Drifting off the architecture vocabulary
- Re-litigating every ADR theoretically forbidden by an old decision
- Bulk interface design before the human picks a candidate

## Quality bar

- [ ] `<context-root>` resolved before reads or writes
- [ ] Scope chosen deliberately (human direction or commit hot spots)
- [ ] SPEC read; domain terms used in candidate titles and prose
- [ ] Each candidate passes deletion-test reasoning
- [ ] Markdown report posted in chat; ≤ ~150 lines
- [ ] Glossary terms used consistently; no "cleaner code" hand-waving
- [ ] Grilling is one-question-at-a-time with recommended answers
- [ ] Session ends with explicit next command (`/design`, `/slice`, etc.)
