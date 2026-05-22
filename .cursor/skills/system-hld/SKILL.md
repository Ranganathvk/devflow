---
name: system-hld
description: >-
  Greenfield Dev Loop step 2: compact system HLD (SYSTEM_HLD.md + SYSTEM_HLD.contract.yaml).
  Invoke /system-hld after /grillme when SPEC is concrete enough. Next: /slice. Does not replace /design.
---

# /system-hld — System shape (HLD + contract)

## Purpose

Materialize **Stage 2 — System shape** from `AI_CONTEXT/SPEC.md`: a **short** human-readable high-level design and a **compact machine-readable contract** so later stages load **contracts**, not mega prose (per framework context strategy).

This skill is **bounded**: system boundaries, major logical pieces, interfaces at a summary level, traceability hooks, and explicit gaps. It does **not** implement features, write application code, or produce per-feature design contracts.

## When to invoke

- `/system-hld` — `AI_CONTEXT/SPEC.md` describes product boundary, goals, and enough structure to name major parts and handoffs.
- After `/grillme` when the spec is no longer placeholder-only.
- When `SYSTEM_HLD` artifacts are missing or **stale** after a meaningful SPEC change.
- Do **not** invoke on an empty or purely aspirational SPEC — run `/grillme` first.
- Do **not** use this skill for a single vertical feature’s deep design — use `/feature-design <FEATURE>` (and related feature skills) instead.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md` — read in full.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md`, `core/AGENTS.md` (or materialized harness) for repo role and constraints.
- **Forbidden:** Unbounded chat history as source of truth; inventing product scope absent from SPEC or confirmed human answers.

## Workflow

1. Read **required** inputs. Note SPEC version/footer if present (for document control).
2. Extract **only** what SPEC asserts: summary, boundary, principles, workflow stages, repo layout, artifact patterns, open items. Treat “TBD” and open items as **first-class outputs** (listed, not smoothed over).
3. **Normalize for traceability (lightweight):** If SPEC already uses stable IDs, reuse them. If not, assign **read-order** IDs for trace rows only inside `SYSTEM_HLD.md`’s traceability table (prefix `SYS-REQ-001` …) — do **not** edit `SPEC.md`.
4. Write `AI_CONTEXT/SYSTEM_HLD.md` using the **skeleton** in this file. Hard limits:
   - Prefer **≤ ~200 lines** total (per framework “short design docs” principle); if impossible, prioritize **contract completeness** and move overflow to **Open questions** bullets, not unbounded narrative.
   - Include **at least one** Mermaid diagram: **system context** (this product vs actors vs external systems). For purely non-hosted frameworks, “actors” may be humans, repos, and agent tools — still draw the boundary.
   - Include a **small** table of **logical containers / major modules** implied by SPEC (e.g. `core/`, `adapters/`, `installer/`, `examples/`, consumer `AI_CONTEXT/`). Technology **only** if SPEC names it; else `TBD`.
5. Write `AI_CONTEXT/SYSTEM_HLD.contract.yaml` using the **YAML shape** in this file. Values must be **SPEC-grounded**; unknowns = `null` or empty lists with an `open_questions` entry explaining the gap — **no fabrication**.
6. Cross-check:
   - Every **major** SPEC heading that implies structure (goals, boundary, layout, workflow, artifacts) is reflected in **either** the prose **or** the contract **or** both.
   - Contract keys are stable for downstream parsers (additive changes only when extending).
7. Chat reply (brief): paths written, whether `SYS-REQ-*` IDs were assigned, **numbered** list of gaps / assumptions needing human or `/grillme`, suggested next step (`/slice` or a feature stage).

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/SYSTEM_HLD.md` | Created or replaced | Compact HLD; ≤ ~200 lines target |
| `AI_CONTEXT/SYSTEM_HLD.contract.yaml` | Created or replaced | Machine handoff; shape below |

No other files written or edited (including **do not** edit `AI_CONTEXT/SPEC.md`, and **do not** write to `AI_CONTEXT/BLUEPRINT/` unless a future skill explicitly merges — this skill’s outputs are the SPEC-named pair only).

## `SYSTEM_HLD.md` skeleton

Use these section headings (omit subsections that SPEC gives nothing for, but keep section numbers stable where possible):

```markdown
# System high-level design

> Sources: AI_CONTEXT/SPEC.md …

## Document control

| Field | Value |
|-------|-------|
| SPEC reference | path + note |
| Revision | initial \| refreshed for … |

## 1. Problem & outcomes

## 2. Scope & non-goals

## 3. Stakeholders & actors

## 4. System context

<!-- Mermaid: context view -->

## 5. Logical structure (modules / containers)

Table: id, name, responsibility, notes/TBD

## 6. Key workflows (framework or product)

Short bullets tied to SPEC’s locked workflow or product flows — no duplicate of full slash encyclopedia.

## 7. Interfaces & integrations

Table or bullets — protocols only if SPEC says; else TBD.

## 8. Cross-cutting concerns

Map SPEC design principles (security, ownership, contracts, context strategy) to how the system honors them.

## 9. Risks, assumptions, open questions

## 10. Traceability (lightweight)

| ID | SPEC excerpt / heading | HLD § |
|----|------------------------|-------|
```

## `SYSTEM_HLD.contract.yaml` shape

Top-level keys (order flexible; preserve keys for tooling):

```yaml
contract_version: "1"
artifact: system_hld
spec_path: AI_CONTEXT/SPEC.md
summary: "<one paragraph, SPEC-grounded>"
product_boundary:
  in_scope: []
  out_of_scope: []
actors: []
  # - id: human_developer
  #   description: "..."

logical_containers: []
  # - id: core
  #   name: Framework core
  #   responsibility: "..."
  #   technology: null

artifact_conventions: []
  # Human + machine pairs this repo uses (from SPEC artifact pattern), as strings

downstream_skills: []
  # Next slash stages from SPEC, e.g. slice, feature-questions — strings only

integrations: []
  # - id: ...
  #   consumer: ...
  #   provider: ...
  #   protocol: null
  #   auth: null
  #   notes: "Assumption: ..."  # only if labeled as assumption in HLD prose

constraints: []
  # Short strings echoing locked principles / rules from SPEC

open_questions: []
  # Strings referencing SPEC TBDs or new gaps discovered while drafting

assumptions: []
  # id, statement, risk_if_wrong, confirm_via — only items labeled Assumption in prose
```

**Parsing note:** Use YAML **null** for unknown scalar fields; use empty arrays for unknown lists. Keep the file **small** (dozens of lines, not hundreds).

## Context budget

- Read in full: `AI_CONTEXT/SPEC.md`.
- Read in full only if needed: optional inputs.
- Do **not** load full prior HLD history from chat; if refreshing, read existing `SYSTEM_HLD.*` only to preserve intentional human edits **when** the human asks for a merge refresh — default is **replace** with SPEC-current content.

## Failure handling

- **`AI_CONTEXT/SPEC.md` missing** — Stop; direct the human to create it (e.g. from `core/templates/SPEC.template.md` when available) or supply an authoritative path; do not write HLD from guesswork.
- **SPEC too thin to bound structure** — Stop after one short message; recommend `/grillme` and list what is missing.
- **Conflict with existing `AI_CONTEXT/BLUEPRINT/*` from other workflows** — Do not edit those files; mention both locations in chat and recommend human reconciliation if titles overlap conceptually.

## Forbidden

- Editing `AI_CONTEXT/SPEC.md`.
- Implementation code, installer scripts, or adapter edits.
- Per-feature deep design (`AUTH_*`, etc.) — wrong stage.
- **Mega** HLD that downstream skills are expected to load in full — keep prose short; push structure to the contract.
- Vague traceability rows (“various sections”) without SPEC anchors.

## Quality bar (self-check before finishing)

- [ ] Both artifact paths exist and validate as UTF-8 text; YAML parses.
- [ ] Mermaid in `SYSTEM_HLD.md` renders logically (actors + system boundary).
- [ ] `SYSTEM_HLD.contract.yaml` is sufficient for a downstream skill to list **containers** and **constraints** without opening the markdown.
- [ ] Numbered chat list: gaps, assumptions, suggested next slash command.
