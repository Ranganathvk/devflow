---
name: feature-questions
description: >-
  Optional Stage 3 quality gate: capture decision questions for one FEATURE as
  AI_CONTEXT/<FEATURE>_QUESTIONS.md plus <FEATURE>_QUESTIONS.contract.yaml.
  Invoke as /feature-questions <FEATURE> when ambiguity is high.
---

# /feature-questions \<FEATURE\> — Optional decision clarifier

## Purpose

Capture open decisions and assumptions for one feature in a compact Q&A contract. This skill is optional and can be skipped for straightforward features that are ready for design or direct implementation.

For usability, this skill should work like a lightweight `/grillme` for one feature: ask clearly, suggest a recommendation, and leave an explicit place for the human to answer.

## When to invoke

- Use when a feature has unresolved product or behavior ambiguity.
- Use before design when stakeholder alignment is the main risk.
- Skip when the feature is simple and SPEC + slices already settle behavior.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md`.
- **Required:** `AI_CONTEXT/FEATURE_SLICES.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>.contract.yaml` (refresh mode), `AI_CONTEXT/PROJECT_STATE.md`.
- **Forbidden:** Chat-only assumptions with no trace to SPEC or slices.

## Workflow

1. Validate `<FEATURE>` format and slice membership.
2. Build a bounded list of key questions (target ≤ 12) with recommended answers.
3. Mark already-settled questions as `resolved_in_spec` when evidence exists.
4. Write `AI_CONTEXT/<FEATURE>_QUESTIONS.md` with a question table that includes a dedicated answer field for the human:

   | ID | Question | Recommended answer | User answer | Status |
   |----|----------|--------------------|-------------|--------|
   | FQ-001 | ... | ... | `[fill]` | open |

   - `User answer` is where the human records the decision (in file) or can answer in chat and then the file is updated.
5. Write `AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml` using the schema below.
6. Reply with open question count and recommended next command (`/feature-research`, `/feature-design`, or direct `/implement` for lite path).

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_QUESTIONS.md` | Created or replaced | Optional artifact |
| `AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml` | Created or replaced | Optional handoff |

No other files written or edited.

## `<FEATURE>_QUESTIONS.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_questions
feature_id: "<FEATURE>"
spec_path: AI_CONTEXT/SPEC.md
feature_slices_contract_path: AI_CONTEXT/FEATURE_SLICES.contract.yaml

summary: "<one sentence>"
questions: []
  # - id: FQ-001
  #   stem: "<question>"
  #   blocks: "<what it blocks>"
  #   recommended_answer: "<recommendation>"
  #   user_answer: null  # filled after human response
  #   traces_to: []
  #   status: open | resolved_in_spec | deferred

open_questions: []
assumptions: []
```

## Context budget

- Read SPEC and slices contract in full.
- Avoid codebase exploration in this skill (research stage handles factual repo checks).

## Failure handling

- Missing slices contract or unknown feature ID → stop and suggest `/slice`.
- Thin SPEC → emit concise contract with `open_questions` instead of guessing.

## Forbidden

- Writing design, DB, API, TDD, tasksplit, or implementation artifacts.

## Quality bar (self-check before finishing)

- [ ] IDs are unique and dependency-ordered.
- [ ] Each question traces to SPEC/slices or explicit assumption.
