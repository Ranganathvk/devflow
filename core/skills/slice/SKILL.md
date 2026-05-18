---
name: slice
description: >-
  After /system-hld, decomposes the product into dependency-ordered vertical feature
  slices (stable FEATURE IDs) plus FEATURE_SLICES.contract.yaml for /feature-questions
  and later stages. Invoke as /slice; consumes SPEC + SYSTEM_HLD contract only.
---

# /slice — Vertical feature decomposition

## Purpose

Turn **system shape** into **implementable vertical slices**: a small set of named features (e.g. `AUTH`, `INSTALLER`) each owning an end-to-end cut of behavior, with explicit **dependencies**, **boundaries**, and **traceability** back to `SYSTEM_HLD` — without starting per-feature design, DB, or API work.

Outputs are **paired** artifacts under `AI_CONTEXT/` so Stage 3 skills load **contracts**, not mega prose (per framework context strategy).

## When to invoke

- `/slice` — immediately after `/system-hld` when `SYSTEM_HLD.contract.yaml` exists and SPEC + contract are concrete enough to name distinct vertical outcomes.
- When `FEATURE_SLICES` artifacts are **missing** or **stale** after a meaningful SPEC or `SYSTEM_HLD` change.
- Do **not** invoke before `/system-hld` (no contract → no slice).
- Do **not** invoke for **horizontal** decomposition (“all DB”, “all APIs”) — vertical end-to-end slices only.
- Do **not** replace `/feature-design`, `/feature-db`, or `/feature-api` — this skill only names and orders the **catalog** of features.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md` — read in full.
- **Required:** `AI_CONTEXT/SYSTEM_HLD.contract.yaml` — read in full (primary structural source).
- **Optional:** `AI_CONTEXT/SYSTEM_HLD.md` — read only if the contract has `null`/empty lists that block safe slicing; prefer closing gaps via `open_questions` over inventing scope.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md` for active feature focus or human notes.
- **Forbidden:** Unbounded chat history as source of truth; inventing features absent from SPEC or `SYSTEM_HLD`; reading full `SYSTEM_HLD.md` by default when the contract suffices.

## Workflow

1. Read **required** inputs. If `SYSTEM_HLD.contract.yaml` is missing or unparsable → **stop**; recommend `/system-hld`.
2. **Extract slicing signals** from SPEC + contract: `summary`, `product_boundary`, `logical_containers`, `constraints`, `downstream_skills`, `open_questions`, and any workflow/examples that imply user-visible capabilities.
3. **Propose vertical features** — each feature MUST:
   - Have a **stable ID**: `^[A-Z][A-Z0-9_]{1,31}$` (examples: `AUTH`, `CORE_SKILLS`, `INSTALLER`).
   - Represent **one vertical**: user- or operator-visible outcome, or a coherent framework increment that can flow through `/feature-questions` → `/implement` without “all layers everywhere.”
   - Declare **in_scope** bullets (what this slice owns) and **out_of_scope** bullets (explicit non-ownership to prevent horizontal blobs).
   - List **`depends_on`**: other feature IDs only (empty if none). Graph must be **acyclic**; order features **topologically** in outputs.
4. **Enforce framework rules from SPEC:** no mega-prompt-sized slices; prefer **fewer, larger** verticals over many micro-tasks unless SPEC already names fine-grained deliverables; respect **out_of_scope** / non-goals — do not create features for explicitly excluded product.
5. Write `AI_CONTEXT/FEATURE_SLICES.md` using the **skeleton** below. Hard limits:
   - Prefer **≤ ~200 lines** total; overflow → `Open questions` bullets, not narrative sprawl.
   - Include **one** Mermaid diagram: **feature dependency** (`flowchart` or `graph` showing IDs and `depends_on` edges) OR a table if a diagram would be noisy for ≤5 features.
6. Write `AI_CONTEXT/FEATURE_SLICES.contract.yaml` using the **YAML shape** below. Values **SPEC- and contract-grounded**; unknowns → `open_questions` strings, not fabrication.
7. **Cross-check:**
   - Every feature ID is unique; `depends_on` references only defined IDs; no cycles.
   - Every `logical_containers[].id` from `SYSTEM_HLD.contract.yaml` is **mapped** to at least one feature’s `primary_containers` **or** called out under top-level `open_questions` with rationale (do not leave orphan containers silently).
   - **Suggested_sequence** lists all feature IDs exactly once in valid dependency order.
8. Chat reply (brief): paths written, feature count, **numbered** open questions / assumptions, suggested next command (`/feature-questions <FIRST_FEATURE>` or human-picked feature).

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/FEATURE_SLICES.md` | Created or replaced | Compact; ≤ ~200 lines target |
| `AI_CONTEXT/FEATURE_SLICES.contract.yaml` | Created or replaced | Machine handoff; shape below |

No other files written or edited (including **do not** edit `AI_CONTEXT/SPEC.md`, `SYSTEM_HLD*`, or application code).

## `FEATURE_SLICES.md` skeleton

```markdown
# Feature slices (vertical plan)

> Sources: AI_CONTEXT/SPEC.md, AI_CONTEXT/SYSTEM_HLD.contract.yaml …

## Document control

| Field | Value |
|-------|-------|
| SPEC / HLD reference | … |
| Revision | initial \| refreshed for … |

## 1. Slicing principles

3–6 bullets: how vertical boundaries were chosen (SPEC quotes / contract anchors).

## 2. Feature catalog

| ID | Title | One-line outcome | Depends on |
|----|-------|------------------|------------|

## 3. Dependency view

<!-- Mermaid flowchart or dependency table -->

## 4. Traceability

| Feature ID | HLD / SPEC anchor |
|------------|-------------------|

## 5. Suggested implementation sequence

Ordered ID list (same as contract `suggested_sequence`) with one-line rationale each.

## 6. Open questions

Bullets — gaps that need `/grillme`, human pick, or next `/system-hld` refresh.
```

## `FEATURE_SLICES.contract.yaml` shape

Top-level keys (order flexible; preserve keys for tooling):

```yaml
contract_version: "1"
artifact: feature_slices
spec_path: AI_CONTEXT/SPEC.md
system_hld_contract_path: AI_CONTEXT/SYSTEM_HLD.contract.yaml
summary: "<one paragraph: how the product is sliced>"

suggested_sequence: []
  # Ordered feature IDs, dependency-respecting — e.g. [ "CORE", "ADAPTERS", "INSTALLER" ]

features: []
  # - id: AUTH
  #   title: "Human-readable title"
  #   outcome: "<one sentence user/operator outcome>"
  #   depends_on: []   # other feature IDs only
  #   primary_containers: []  # ids from SYSTEM_HLD.contract logical_containers
  #   in_scope: []
  #   out_of_scope: []
  #   traces_to: []  # strings: SYS-REQ-*, SPEC section names, or HLD notes

constraints_echo: []
  # Short strings copied or summarized from SYSTEM_HLD / SPEC that slices must obey

open_questions: []
assumptions: []
  # id, statement, risk_if_wrong, confirm_via — only if labeled in prose
```

**Parsing note:** YAML **null** for unknown scalars; empty arrays for absent lists. Keep the file **small** (typically well under 120 lines).

## Context budget

- Read in full: `AI_CONTEXT/SPEC.md`, `AI_CONTEXT/SYSTEM_HLD.contract.yaml`.
- Read `AI_CONTEXT/SYSTEM_HLD.md` only when required fields in the contract are empty and prose is needed to avoid invention.
- Do **not** load prior chat; when refreshing, read existing `FEATURE_SLICES.*` only if the human asked for a merge — default is **replace** with current inputs.

## Failure handling

- **`SYSTEM_HLD.contract.yaml` missing** — Stop; run `/system-hld` first.
- **SPEC or contract too thin** — Emit minimal YAML with `open_questions` explaining what is missing; keep markdown short; do **not** invent features to fill the page.
- **Cycle detected in dependencies** — Fix before writing: merge features or remove an edge; if unresolved, stop with one message listing the cycle.
- **Conflict with existing human-edited `FEATURE_SLICES.md`** — Default **replace**; if the human explicitly asked to preserve named sections, merge only those sections and note the merge in Document control.

## Forbidden

- Horizontal-only features (“Database layer”, “All APIs”) as the sole content of a slice.
- Editing `AI_CONTEXT/SPEC.md` or `SYSTEM_HLD*`.
- Per-feature design depth (schemas, endpoints, tickets) — wrong stage.
- More than **two** output files.
- **Mega** feature lists — if >12 features, consolidate with human-facing `open_questions` listing merge candidates (do not silently merge without noting tradeoff).

## Quality bar (self-check before finishing)

- [ ] YAML parses; `suggested_sequence` matches dependency order and includes every `features[].id`.
- [ ] Each feature’s `in_scope` / `out_of_scope` is concrete enough for `/feature-questions <FEATURE>` to start cold.
- [ ] Numbered chat list: open questions, suggested first `/feature-questions` target.
