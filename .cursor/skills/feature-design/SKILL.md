---
name: feature-design
description: >-
  Stage 3: compact per-feature design and routing contract for FEATURE. Writes
  AI_CONTEXT/<FEATURE>_DESIGN.md plus AI_CONTEXT/<FEATURE>.contract.yaml. Invoke as
  /feature-design <FEATURE> for partial refresh. Greenfield Dev Loop: prefer /design <FEATURE>.
---

# /feature-design \<FEATURE\> — Compact design + delivery routing

## Purpose

Produce a short per-feature design and the authoritative feature contract (`<FEATURE>.contract.yaml`) used by downstream skills **and** routing. This skill supports both:

- **Full design path** (questions/research inputs available).
- **Lite bootstrap path** (start from SPEC + slices only, then encode deliberate skips).

The contract carries explicit `delivery` flags so later skills know whether DB/API/tasksplit artifacts are expected or intentionally skipped.

## When to invoke

- `/feature-design <FEATURE>` — after `/slice`; use whenever you need a stable feature contract before implementation.
- Recommended after `/feature-research` for non-trivial features, but **not required**.
- Re-run when scope, risks, or delivery mode changes.
- Do **not** replace `/system-hld` — this is per-feature only.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md` — read in full.
- **Required:** `AI_CONTEXT/FEATURE_SLICES.contract.yaml` — feature row for `<FEATURE>`.
- **Optional:** `AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>_RESEARCH.contract.yaml`.
- **Optional:** `AI_CONTEXT/SYSTEM_HLD.contract.yaml`, `AI_CONTEXT/PROJECT_STATE.md`.
- **Forbidden:** Unbounded chat as source of truth.

## Workflow

1. Validate `<FEATURE>` and confirm presence in `FEATURE_SLICES.contract.yaml`.
2. Synthesize outcomes, constraints, acceptance criteria, and behavior from available inputs.
3. Choose and encode delivery routing:
   - `delivery_profile`: `lite` | `standard` | `heavy`.
   - `needs_db`, `needs_api`, `needs_tasks`: explicit booleans.
4. Write `AI_CONTEXT/<FEATURE>_DESIGN.md` (target ≤ ~200 lines) with sections:
   - Document control + input coverage (which optional inputs were absent).
   - Outcomes and scope.
   - Behaviors / flows.
   - Data and integration intent (high level only).
   - Open questions and assumptions.
5. Write `AI_CONTEXT/<FEATURE>.contract.yaml` using shape below.
6. Cross-check:
   - `depends_on` aligns to slices.
   - Every acceptance criterion traces to SPEC/slices or an explicit assumption.
   - Delivery flags are internally consistent (`needs_api: false` means API artifact is optional).
7. Chat reply: paths written, selected delivery profile, numbered open questions, and recommended next command based on flags.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_DESIGN.md` | Created or replaced | ≤ ~200 lines target |
| `AI_CONTEXT/<FEATURE>.contract.yaml` | Created or replaced | Primary feature + routing contract |

No other files written or edited.

## `<FEATURE>.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature
feature_id: "<FEATURE>"
spec_path: AI_CONTEXT/SPEC.md
feature_slices_contract_path: AI_CONTEXT/FEATURE_SLICES.contract.yaml
questions_contract_path: AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml
research_contract_path: AI_CONTEXT/<FEATURE>_RESEARCH.contract.yaml

summary: "<one paragraph outcome>"

delivery:
  delivery_profile: lite | standard | heavy
  needs_db: true
  needs_api: true
  needs_tasks: true
  notes: "<why this routing was chosen>"

depends_on: []        # other feature IDs — should match slices
in_scope: []
out_of_scope: []

acceptance_criteria: []
  # - id: AC-001
  #   given_when_then: "<short>"
  #   traces_to: []  # SPEC heading / slice trace / SYS-REQ-*

behaviors: []
  # - id: BEH-001
  #   name: "<verb phrase>"
  #   description: "<one or two sentences>"

data_intent: []
integrations: []
non_functional: []

open_questions: []
assumptions: []
```

## Skip semantics for downstream stages

- If `delivery.needs_db: false`, skip `/feature-db`; no DB artifacts are required.
- If `delivery.needs_api: false`, skip `/feature-api`; no API artifacts are required.
- If `delivery.needs_tasks: false`, skip `/tasksplit` and use `/implement <FEATURE>` lite path.
- If any flag is `true`, that stage is expected before corresponding deep path implementation.

## Context budget

- Read in full: SPEC and slices contract.
- Read optional contracts only when present; missing optional inputs are acceptable and must be reflected in `assumptions` / `open_questions`.

## Failure handling

- **Missing SPEC or slices contract** → Stop with precise missing path.
- **Feature absent from slices** → Stop and suggest `/slice` refresh.
- **Conflicting optional inputs** → Prefer SPEC + slices; record conflict in `assumptions`.

## Forbidden

- Emitting DB/API/tasksplit contracts from this skill.
- Editing SPEC/slices/system contracts.
- More than two output files.

## Quality bar (self-check before finishing)

- [ ] YAML parses; `feature_id` consistent across filenames.
- [ ] `delivery` block is present and fully populated.
- [ ] Acceptance criteria and delivery flags are traceable to available inputs.
