# Product specification — <PROJECT_NAME>

> **This is the canonical product specification for this repo.** Skills that say "the SPEC" read and update **this file**. Keep it short, concrete, and decision-oriented. Replace every `<…>` placeholder before merging.

## Summary

One paragraph: what is being built, for whom, and why now. Frame it as a product, not a tech stack.

## Product boundary

- **In scope:** Bullet list — what this effort delivers.
- **Out of scope (v1):** Bullet list — explicit non-goals that act as hard boundaries downstream.

## Core goal

What problem this product solves and what disciplined behaviour it enforces. Keep to ~4–6 bullets.

## Design principles (locked)

Numbered list of locked principles. Each principle should be specific enough to reject a design later (not just "be good"). Examples:

1. **<Principle name>** — <one-sentence implication>.
2. **<Principle name>** — <one-sentence implication>.

## Functional requirements

Numbered or `REQ-FR-###`-keyed list. Each requirement is a single, testable statement.

| ID | Requirement | Notes |
|----|-------------|-------|
| REQ-FR-001 | … | … |
| REQ-FR-002 | … | … |

## Non-functional requirements / constraints

| ID | Requirement | Notes |
|----|-------------|-------|
| REQ-NFR-001 | … | … |
| REQ-CON-001 | … | … |

## Success criteria (v1)

Bullet list — measurable conditions that mean v1 is done. Avoid vague adjectives ("fast", "great UX") without a target.

## Known tricky parts

Bullets — risks, integrations that may bite, areas where decisions are likely to churn.

## Open items (TBD in implementation)

Bullets — explicitly deferred decisions. Each open item should name **what** is unresolved and **when** it must be resolved (e.g. before `/architect`, before `/feature-design AUTH`).

---

*Version:* initial draft; refine via `/grillme` before invoking `/architect`.
