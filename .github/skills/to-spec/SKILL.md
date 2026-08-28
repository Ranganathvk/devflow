---
name: to-spec
description: >-
  Synthesize a product SPEC from a requirements document (or attached notes) —
  no interview. Writes artifacts/SPEC.md at high-level product intent.
  Invoke /to-spec with a path or @-attached doc. Inspired by mattpocock/skills
  engineering/to-spec. Prefer /grillme when the source is thin or needs Q&A.
disable-model-invocation: true
---

# /to-spec — Document → SPEC (no interview)

## Purpose

Turn an existing **requirements / project document** into the canonical product
spec at `artifacts/SPEC.md`. Do **not** interview the user — synthesize what
the document (and optional repo context) already say.

Inspired by [mattpocock/skills `to-spec`](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md):
synthesis over grilling; extensive user-facing coverage; explicit out-of-scope.

**Devflow adaptations:**

| Matt Pocock `to-spec` | This skill |
|-----------------------|------------|
| Conversation → issue tracker | Document → `artifacts/SPEC.md` |
| PRD with implementation & testing decisions | Product-intent SPEC (HLD/LLD hold how) |
| `ready-for-agent` triage label | Human owns SPEC; next is `/grillme` or `/system-hld` |

## When to invoke

| Invocation | Behavior |
|------------|----------|
| `/to-spec <path>` | Read that file as the source document |
| `/to-spec` with `@`-attached doc | Use the attachment as the source |
| `/to-spec` with pasted requirements | Use the paste as the source for this session; persist only into SPEC |

**Prefer this skill when:** a requirements doc, PRD draft, brief, or stakeholder
notes already exist and need to become durable SPEC.

**Prefer `/grillme spec` when:** the source is thin, contradictory, or the human
wants interview-driven refinement.

**Do not:** implement code, run `/design` / `/tdd`, mark SPEC approved, or invent
scope absent from the source document.

## Inputs

- **Required:** Source document — path, `@`-attachment, or pasted text with
  project requirements / product intent.
- **Optional:** Existing `artifacts/SPEC.md` (merge carefully — see below),
  `artifacts/PROJECT_STATE.md`, domain glossary / ADRs in-repo.
- **Forbidden:** Unbounded chat history as sole source of truth; fabricating
  requirements the document does not support.

## SPEC abstraction (mandatory)

`artifacts/SPEC.md` is **high-level product intent only** — same bar as
`core/templates/SPEC.template.md`.

| In SPEC | Not in SPEC |
|---------|-------------|
| Who, problem, boundary, v1 scope | Logical containers, module handoffs → HLD |
| Requirements & principles (technology-agnostic) | Frameworks, languages, APIs, schemas |
| Success criteria, product-level risks | Algorithms, deployment, class design |
| User stories as product behaviour | File paths, code snippets |

If the source document includes stack/API/schema detail, capture the **product
implication** (or an open item) in SPEC; do **not** copy implementation prose
forward. Note deferred mechanics for a later `/grillme hld` or `/system-hld`.

## Process

1. **Resolve source.** Identify the document. If none is provided, ask **once**
   for a path or paste — then stop until you have it. Do not invent a brief.

2. **Read source in full.** Extract: problem, users/actors, goals, in/out of
   scope, requirements, constraints, success criteria, risks, open questions.
   Mark gaps as **Open items**, not guesses.

3. **Orient to the repo (lightweight).** If you have not already: skim layout,
   glossary, and any ADRs that touch this area. Reuse project vocabulary. Do
   not start a full `/understand` unless the human asks.

4. **Sketch product seams (intent level).** Before writing SPEC, state briefly:
   - Product boundary (in vs out)
   - Primary actors
   - Highest-level behaviour seams implied by the doc (prefer few; ideal is one
     clear product surface)

   Check that these match the human’s expectations. If they disagree, adjust
   from their correction — still no interview loop beyond that confirmation.

5. **Write `artifacts/SPEC.md`** using the **output template** below.
   - Replace an existing SPEC only when the human asked to regenerate, or when
     SPEC is empty / placeholder-heavy.
   - If SPEC already has substantive locked decisions, **merge**: preserve
     locked principles and explicit human decisions; update sections grounded
     in the new document; list conflicts under Open items.

6. **Chat reply (brief):** path written, source used, open-item count, and
   suggested next step (`/grillme spec` if thin, else `/system-hld` or
   `/understand` for existing repos).

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `artifacts/SPEC.md` | Created or replaced/merged | Product-intent SPEC only |

Do **not** write HLD/LLD, contracts, or issue-tracker tickets from this skill.

## Output template

Follow `core/templates/SPEC.template.md` section order. Fill from the source
document; omit empty fluff, keep Open items honest.

```markdown
# Product specification — <PROJECT_NAME>

> Canonical product specification. Sources: <document path or “pasted brief”>.

## Abstraction level (mandatory)

SPEC = high-level product intent only — what and why, not how to build it.

## Summary

One paragraph: what is being built, for whom, and why now.

## Problem statement

The problem from the user’s / stakeholder’s perspective (from the source doc).

## Solution

The intended solution from the user’s perspective (product behaviour, not stack).

## Product boundary

- **In scope:** …
- **Out of scope (v1):** …

## Core goal

What problem this product solves (~4–6 bullets).

## Design principles (locked)

Numbered principles specific enough to reject a later design. Only include
principles the source supports or that are already locked in an existing SPEC.

## User stories

A **long, numbered** list covering the feature/product aspects in the source.
Format:

1. As a <actor>, I want <capability>, so that <benefit>

Derive extensively from the document; do not invent actors or benefits the
source does not support. If the source is sparse, write fewer stories and list
gaps under Open items — do not pad.

## Functional requirements

| ID | Requirement | Notes |
|----|-------------|-------|
| REQ-FR-001 | … | … |

Prefer testable, technology-agnostic statements. Map user stories to FR ids
where helpful.

## Non-functional requirements / constraints

| ID | Requirement | Notes |
|----|-------------|-------|
| REQ-NFR-001 | … | … |
| REQ-CON-001 | … | … |

## Success criteria (v1)

Measurable conditions that mean v1 is done.

## Known tricky parts

Risks and intent-level ambiguities from the source.

## Open items (TBD)

Unresolved decisions. Name **what** is open and **when** it must resolve
(e.g. before `/system-hld`, before `/design <FEATURE>`).

## Further notes

Anything else from the source that belongs at product intent — including
implementation or testing hints deferred to HLD/LLD (one-line pointers only).

---

*Version:* synthesized via `/to-spec` from <source>; refine via `/grillme` if needed.
```

### Mapping from Matt-style sections

| Matt section | Where it lands here |
|--------------|---------------------|
| Problem Statement | `## Problem statement` |
| Solution | `## Solution` |
| User Stories | `## User stories` (+ FR table) |
| Implementation Decisions | Open items / Further notes as **deferrals** — not SPEC body detail |
| Testing Decisions | Open items pointing to `/tdd` later — not test plans in SPEC |
| Out of Scope | Product boundary → Out of scope |
| Further Notes | `## Further notes` |

## Quality bar

- Ground every requirement in the source (or an explicit Open item).
- Prefer the source’s vocabulary and the repo’s glossary over new jargon.
- Extensive user stories when the document is rich; honest gaps when it is not.
- No file paths or code in SPEC (exception: none — keep intent-only).
- Do not mark SPEC approved.

## Next steps (suggest, do not auto-run)

| After `/to-spec` | Suggest |
|------------------|---------|
| SPEC still thin or disputed | `/grillme spec` |
| Existing codebase | `/understand` |
| SPEC concrete enough | `/system-hld` → `/slice` |
| Single clear feature | `/design <FEATURE>` |
