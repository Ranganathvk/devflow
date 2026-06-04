---
name: grillme
description: >-
  Interview using human-provided SPEC as input; generate HLD and/or LLD only when asked.
  One question at a time. Invoke /grillme hld, /grillme lld FEATURE, or /grillme spec when
  refining intent. Supports delta mode.
---

# /grillme — Grill from SPEC → HLD and/or LLD

## Purpose

The **human provides SPEC** (product intent). This skill **interviews** to close gaps and writes **only what the human asked to generate**:

| Output (when requested) | Write target | SPEC role |
|-------------------------|--------------|-----------|
| **HLD only** | `SYSTEM_HLD.md` + `SYSTEM_HLD.contract.yaml` | Read-only baseline |
| **LLD only** | `<FEATURE>_DESIGN.md` + `<FEATURE>.contract.yaml` | Read-only baseline |
| **SPEC refinement** | `AI_CONTEXT/SPEC.md` | Active write target |

Typical flow: attach or maintain **`AI_CONTEXT/SPEC.md`**, then **`/grillme hld`** or **`/grillme lld <FEATURE>`** — no SPEC rewriting unless the human explicitly wants spec refinement.

## SPEC abstraction (high-level only)

`AI_CONTEXT/SPEC.md` holds **product / high-level intent** — the same bar as `core/templates/SPEC.template.md` § Abstraction level.

| In SPEC | Not in SPEC (use HLD or LLD) |
|---------|------------------------------|
| Who, what problem, boundary, v1 scope | Logical containers, system context, major module handoffs → **HLD** |
| Requirements & principles (technology-agnostic) | Frameworks, languages, libraries, repo layout |
| Success criteria, compliance/regime at product level | API paths, payloads, auth mechanism detail, DB schemas |
| Intent-level risks & open questions | Algorithms, deployment, CI/CD, class design |

**All modes:** When reading SPEC, treat any existing technical/low-level prose as **legacy** — do not copy it forward; offer to move it to HLD/LLD in a separate session.

**`grill_target: spec`:** Ask **product-level** questions only (boundary, behaviour, rules, NFRs without stack). If the human answers with implementation detail, respond with a **product-level** rewrite for SPEC **or** defer: *“Record that in HLD/LLD — should I continue SPEC at intent level?”* Do not merge stack/API/schema text into SPEC.

**`grill_target: hld` / `lld`:** Technical and low-level detail belongs in the **active output artifact**, not SPEC.

## Behavioral contract (verbatim)

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time.
>
> When a question has fixed choices (A/B/C, pick-one), present them **radio-style**: one short question line, then each option on **its own line** with a bold letter label and a brief title, plus a short clarification if needed — never one dense paragraph of “(A) … (B) … (C)?”.
>
> If a question can be answered by exploring the codebase, explore the codebase instead.

**Scope note:** In **incremental / delta** mode, grill only the **new/changed idea** and its dependencies in the **active output artifact** — not unrelated settled HLD/LLD/SPEC content.

## SPEC as input (default)

1. **Required input:** `AI_CONTEXT/SPEC.md` — read in full before any question or write. Treat it as **given intent** unless the session target is **`spec`** refinement.
2. **Human may also** `@`-attach SPEC in chat or paste a delta; use that for the session, but the **durable** SPEC is still `AI_CONTEXT/SPEC.md`. Persist chat-only SPEC text **only** when `grill_target: spec` or the human asks to save it to the file.
3. **HLD-only / LLD-only:** Do **not** expand or rewrite SPEC to “fill in” design detail. Record unresolved intent gaps in the **HLD/LLD** artifact (`Open questions`, contract `open_questions`) and ask the human — or suggest a separate **`/grillme spec`** session if intent itself is wrong.
4. **Intent-level contradiction** (answer conflicts SPEC): Ask **one** resolution question — update SPEC **only** if the human chooses to change intent; otherwise narrow the HLD/LLD decision to stay consistent with SPEC.

## When to invoke

| Invocation | Behavior |
|------------|----------|
| `/grillme hld` or “HLD only”, “only system HLD” | `grill_target: hld` — SPEC read-only; write `SYSTEM_HLD*` only |
| `/grillme lld <FEATURE>` or “LLD only for …” | `grill_target: lld` — SPEC read-only; write `<FEATURE>_DESIGN*` only |
| `/grillme spec` or “refine SPEC”, thin/disputed spec | `grill_target: spec` — write `SPEC.md` only |
| `/grillme` (no target) | After reading SPEC, ask **one** output question (HLD vs LLD vs SPEC) — see gate below |
| `/grillme delta` | Incremental pass on the active output artifact |
| Before `/system-hld` | Optional interview-first: `/grillme hld` then `/system-hld` if you want less automation |
| Before `/design <FEATURE>` | `/grillme lld <FEATURE>` for extended clarify grilling |

Do **not** implement code, run `/tdd`, or mark artifacts approved.

## Output gate (only when target unclear)

**Skip** when slash args or the human message already fixes the output (`hld`, `lld`, `spec`, “only HLD”, “only LLD”, feature name).

**Otherwise**, first message after reading SPEC — **one** question, no edits:

```markdown
**Question:** You provided SPEC as input. What should this session generate?

- **A — System HLD only** — Interview system shape; write `SYSTEM_HLD.md` (+ contract). SPEC stays as-is.
- **B — Feature LLD only** — Interview one feature; write `<FEATURE>_DESIGN.md` (+ contract). SPEC stays as-is.
- **C — SPEC refinement** — Interview and update `SPEC.md` (use when intent is still thin or disputed).

**Recommended:** … (e.g. solid SPEC, no HLD yet → A; named feature → B; placeholder SPEC → C)
```

**Pre-specified (skip gate):**

| Human says | `grill_target` |
|------------|----------------|
| `/grillme hld`, HLD only, system shape | `hld` |
| `/grillme lld`, LLD only, feature design | `lld` |
| `/grillme lld AUTH_LOGIN` | `lld` + `AUTH_LOGIN` |
| `/grillme spec`, refine SPEC | `spec` |

### Follow-up gate — LLD only

If `grill_target: lld` and `feature_id` is unknown: **one** question to confirm `feature_id` (propose from SPEC / slices). Create `<FEATURE>_DESIGN.md` + contract skeleton **after** confirmation.

## Inputs

| Input | Role |
|-------|------|
| `AI_CONTEXT/SPEC.md` | **Always required** — human-provided intent; full read every turn |
| `SYSTEM_HLD*` | Read when `grill_target: hld` and files exist |
| `<FEATURE>_DESIGN*` + contract | Read when `grill_target: lld` and files exist |
| `FEATURE_SLICES.contract.yaml`, `SYSTEM_HLD.contract.yaml` | Optional context for LLD/HLD |
| `PROJECT_STATE.md`, harness | Optional session constraints |

**Forbidden:** Chat history as source of truth; inventing scope not in SPEC or human answers.

## Workflows

Pick **baseline** vs **incremental** from the **active output artifact** (HLD, LLD, or SPEC when refining spec).

### Baseline

1. Read SPEC + active artifact for `grill_target`.
2. Build decision tree **for that output only** (HLD structure from SPEC; LLD feature shape from SPEC + HLD contract if present).
3. **Per turn** until done.
4. Session end: summary, open items, handoff (`/slice`, `/design <FEATURE>`, etc.).

### Incremental (`/grillme delta`, pivot, new idea)

1. Read SPEC (baseline) + active artifact.
2. Extract delta; impact **only** the output artifact (+ SPEC **only** if `grill_target: spec` or human changes intent).
3. **Human gate:** first reply after delta — no edits (except verbatim insert); restate delta; **one** question.
4. **Per turn** until subgraph done.

### Per turn (all targets)

- **One question** + recommended answer; radio layout for pick-one.
- **Codebase-first** for factual repo questions.
- After reply → merge into **active output artifact only**.
- **`grill_target: hld`:** compact HLD (≤ ~200 lines target); unknowns → open questions — not SPEC prose.
- **`grill_target: lld`:** clarify/intent/design sections + contract fields; no `/design` stages (`impact`, `db`, `api`, …).
- **`grill_target: spec`:** update SPEC only — **high-level product content** per § SPEC abstraction; never add HLD/LLD-grade detail.

## Output artifacts

| `grill_target` | May edit | SPEC |
|----------------|----------|------|
| `hld` | `SYSTEM_HLD.md`, `SYSTEM_HLD.contract.yaml` | **Read-only** (exception: human explicitly revises intent → one resolution, then optional SPEC edit) |
| `lld` | `<FEATURE>_DESIGN.md`, `<FEATURE>.contract.yaml` | **Read-only** (same exception) |
| `spec` | `AI_CONTEXT/SPEC.md` | Active target |

No application code or other feature artifacts.

## Question format

Stem + stacked **A / B / C** options + **Recommended** — for output gate, feature gate, and substantive questions.

## Context budget

- **Every turn:** `AI_CONTEXT/SPEC.md` in full.
- **When active:** HLD or LLD artifact + contract; prefer contracts over long prose when sufficient.

## Failure handling

- **SPEC missing** — Stop; human must provide or create `AI_CONTEXT/SPEC.md` (e.g. from `core/templates/SPEC.template.md`) before HLD/LLD grilling.
- **HLD only but SPEC cannot bound structure** — One question: add minimal intent via `/grillme spec` vs proceed with explicit TBDs in HLD — do not invent product scope in SPEC silently.
- **LLD only vs approved design conflict** — One resolution (replace / narrow / defer).
- **Vague delta** — One clarifying question before writes.

## Forbidden

- Multiple questions per message.
- **HLD/LLD sessions:** editing SPEC for design detail, “helpful” spec expansion, or silent requirement invention.
- Editing artifacts outside `grill_target`.
- Inventing unconfirmed scope.
- Marking artifacts approved.
- Full-tree replay in incremental mode without invalidation or **full re-grill**.
- Bulk inference without per-knot Q&A.
- Running full `/design` pipeline inside `/grillme lld`.
- **SPEC writes:** frameworks, APIs, schemas, file/module structure, deployment/ops detail, or other low-level design (belongs in HLD/LLD).
- **SPEC spec-mode questions** that presuppose a tech stack when product intent is enough.

## Quality bar

- [ ] SPEC read as input; output target (HLD / LLD / spec) confirmed before substantive grilling.
- [ ] Any SPEC edit stays high-level product intent (no technical/low-level leakage).
- [ ] HLD-only and LLD-only sessions did not rewrite SPEC unless human explicitly changed intent.
- [ ] Every substantive output change maps to a human answer (or verbatim exception).
- [ ] Session end: what was generated, what remains open, next command.
