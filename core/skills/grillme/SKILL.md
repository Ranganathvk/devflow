---
name: grillme
description: >-
  Interview-driven refinement of AI_CONTEXT/SPEC.md. Baseline vs incremental (/grillme delta):
  one question at a time, recommended answer, dependency-ordered. Invoke before architect or implementation.
---

# /grillme — SPEC stress-test and refinement

## Purpose

Reach **shared understanding** by grilling the plan: expose gaps, resolve dependencies between decisions in order, fold agreed intent into `AI_CONTEXT/SPEC.md`. Chat is the dialogue; the file is the durable record.

## Behavioral contract (verbatim)

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time.
>
> When a question has fixed choices (A/B/C, pick-one), present them **radio-style**: one short question line, then each option on **its own line** with a bold letter label and a brief title, plus a short clarification if needed — never one dense paragraph of “(A) … (B) … (C)?”.
>
> If a question can be answered by exploring the codebase, explore the codebase instead.

**Scope note:** In **Workflow B (incremental)**, satisfy this contract for **every aspect of the new/changed idea and its knock-on decisions**, not by re-interviewing unrelated parts of the plan already captured in SPEC.

## When to invoke

- `/grillme` — `SPEC.md` is thin, fuzzy, or disputed.
- Before `/architect` or implementation.
- After a large pivot to realign requirements.
- **`/grillme delta`** or “new idea on top of existing SPEC” — **incremental pass** only (see Workflow B); do **not** restart from question one unless the human asks for a **full re-grill**.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md` — read in full before starting.
- **Optional:** `core/AGENTS.md` (canonical framework harness when present), `AI_CONTEXT/PROJECT_STATE.md`, any materialized repo-local harness (e.g. `.cursor/AGENTS.md`) if it constrains how this session should behave.
- **Forbidden:** Unbounded chat history as the source of truth; inventing product scope not grounded in the human’s answers or existing SPEC text.

## Workflow

Pick **A** or **B** after reading `AI_CONTEXT/SPEC.md`. Default to **B** when the spec already has real content (non-placeholder goals, requirements, or decisions).

### A — Baseline (empty or placeholder-heavy SPEC, or human asks for **full re-grill**)

1. Read inputs. Build the **full decision tree**: branches and inter-dependencies.
2. Walk it dependency-first — same **Per turn** loop as below.
3. On session end: one-line summary of what changed and what branch is next.

### B — Incremental (**new idea**, pivot detail, or `/grillme delta`)

Goal: **update intelligently** — only reopen branches the new input touches; **do not** replay unrelated settled decisions from scratch.

1. Read `AI_CONTEXT/SPEC.md` end-to-end. Treat explicit, concrete statements as **baseline** unless contradicted.
2. From the human message (or a short clarifying question if the delta is vague), extract **the delta**: what changed or what’s newly proposed.
3. Compute **impact**: which SPEC sections/tables/rows must change or gain rows — include product-shaped headings when relevant (for example **Summary**, **Activation**, **Admin dashboard (v1)**, **Cluster access**, **Investigation scope**, **Deployment verification (v1)**, **Authorization**, **Functional requirements**, **Success criteria**, Risks, Open questions). Prefer touching the smallest set that stays internally consistent.
4. Build a **small subgraph**: only dependencies needed to integrate the delta (e.g. new integration → clarify ownership, SLA, security — not re-litigate unrelated UX unless linked).
5. **Reuse baseline:** skip questions already answered in SPEC with no conflict. **Invalidation:** if the new idea contradicts baseline, ask **one** resolution question at a time (replace vs narrow vs defer — map outcome into SPEC).
6. **Human gate (mandatory for B):** On the **first** assistant message after you understand the delta, **do not edit `SPEC.md`.** You may only: briefly restate the delta (2–4 bullets), then ask **one** question + recommendation (same layout as **Per turn**). This forces a human turn before any incremental write.
   - **Verbatim exception:** If the human supplied exact text and explicitly asked to insert it in a named section *verbatim*, you may apply **only** that block on that same message — then continue with **Per turn** for every further integration (no bulk “feature dump”).
7. **Per turn** (below) until the subgraph is done — **each** substantive change to requirements/wording follows **one** human answer (see **No silent writes**).
8. On session end: bullets — **Delta summary**, **Sections touched**, **Contradictions resolved** (if any).

### Per turn (shared by A and B)

- **No silent writes (especially B):** Do not expand/interpret a “new idea” into new goals, features, F-* rows, success criteria, or product prose **without** the human answering your latest question in this thread — unless **verbatim exception** above applies to that chunk only.
- **Codebase-first:** If the next item is purely factual about the repo (paths, filenames, existing harness layout) and **does not** change product intent, explore the codebase; report what you found; then either skip SPEC change or ask **one** question if the finding implies a spec decision.
- If product intent or prioritization is ambiguous → ask **one** dependency- or subgraph-respecting question with your **recommended answer** and one-sentence rationale.
- **Multiple-choice layout:** stem (`**Question:** …`), then `**A — Short label**` … End with `**Recommended:** …`.
- After human reply → merge **only** what that answer settled into `AI_CONTEXT/SPEC.md` in the same turn.

Repeat until done or only `[needs human]` stubs remain.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/SPEC.md` | Updated in-place as decisions land | Only file this skill may edit. |

No other files written or edited.

## Question format (multiple choice)

Use this shape whenever the human must pick one of a small set of options.

**Avoid** — single paragraph with inlined `(A) … (B) … (C)?` (hard to scan, unlike Plan-mode pick-one UI).

**Use** — stem + stacked options + recommendation:

```markdown
**Question:** For fixes, what is the binding rule?

- **A — Propose-only** — Read-only on cluster/Git; you apply every change.
- **B — Gated execution** — kubectl/Git only after your approval per change or per playbook.
- **C — Autonomous execution** — Agent may apply fixes without waiting for per-action approval.

**Recommended:** B — balances speed with safety for production paths.
```

Reply handling: accept `A` / `B` / `C`, the label (“gated”), or a short paraphrase; map it to the chosen option before updating SPEC.

## Context budget

- Read **in full:** `AI_CONTEXT/SPEC.md` (required every turn that advances the interview).
- Read **in full when present and relevant:** `AI_CONTEXT/PROJECT_STATE.md`, `core/AGENTS.md` (or materialized harness) — only to align session constraints; do not treat them as product SPEC.
- Do **not** load unrelated large docs, full blueprint folders, or prior chat dumps as substitutes for SPEC.

## Failure handling

- **`AI_CONTEXT/SPEC.md` missing** — Stop; tell the human to create it (e.g. from `core/templates/SPEC.template.md`) or provide the path they want treated as authoritative; do not invent a parallel spec file at repo root.
- **Delta is vague** — Ask **one** clarifying question before choosing Workflow A vs B or before editing SPEC (except Workflow B human-gate rules).
- **Answer contradicts an earlier settled line in SPEC** — Ask **one** resolution question (replace vs narrow vs defer); merge only after the human picks.

## Forbidden

- Multiple questions in one message.
- Editing anything other than `AI_CONTEXT/SPEC.md`.
- Inventing scope the human has not confirmed.
- Asking what codebase exploration already shows.
- Marking the spec "approved" — human owns that.
- **Full-tree replay in incremental mode** — do not re-ask branches already settled in SPEC unless invalidated by the new idea or the human requests **full re-grill**.
- **SPEC edits on the delta-discovery message** in Workflow B (first reply after “new idea”) except the narrow **verbatim exception**.
- **Bulk inference** — turning a vague delta into many new requirements or rewriting sections in one shot without Q&A per substantive knot.

## Quality bar (self-check before finishing)

- [ ] Every substantive SPEC change in this thread maps to a human answer (or verbatim exception).
- [ ] Only `AI_CONTEXT/SPEC.md` was edited among repo files.
- [ ] Session end summary includes what changed and what remains open (if anything).
