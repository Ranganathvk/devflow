---
name: tdd
description: >-
  Optional Stage 3 test-plan contract for FEATURE. Writes AI_CONTEXT/<FEATURE>_TDD.md plus
  <FEATURE>_TDD.contract.yaml when deeper test planning is needed before task splitting.
---

# /tdd \<FEATURE\> — Optional test design

## Purpose

Map feature acceptance criteria into a test matrix when explicit planning is useful. This stage is optional and can be skipped for lite features that go straight to implementation and review.

## When to invoke

- Use when risk or complexity justifies explicit test planning.
- Recommended before `/tasksplit` in standard/heavy routes.
- Skip on lightweight features or when tests are simpler to design directly during implementation.

## Inputs

- **Required:** `AI_CONTEXT/<FEATURE>.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>_DB.contract.yaml` (if `needs_db: true`).
- **Optional:** `AI_CONTEXT/<FEATURE>_API.contract.yaml` (if `needs_api: true`).
- **Optional:** `AI_CONTEXT/SPEC.md`, `AI_CONTEXT/SYSTEM_HLD.contract.yaml`.
- **Forbidden:** Assuming DB/API contracts must exist when feature delivery flags say they are not needed.

## Workflow

1. Validate feature contract and read `delivery` flags.
2. Build cases from acceptance criteria and available API/DB artifacts when relevant.
3. Emit compact markdown and YAML outputs.
4. Suggest `/tasksplit` only when `delivery.needs_tasks: true`; otherwise recommend direct `/implement <FEATURE>`.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_TDD.md` | Created or replaced | Optional artifact |
| `AI_CONTEXT/<FEATURE>_TDD.contract.yaml` | Created or replaced | Optional handoff |

No other files written or edited.

## `<FEATURE>_TDD.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_tdd
feature_id: "<FEATURE>"
feature_contract_path: AI_CONTEXT/<FEATURE>.contract.yaml
feature_db_contract_path: AI_CONTEXT/<FEATURE>_DB.contract.yaml
feature_api_contract_path: AI_CONTEXT/<FEATURE>_API.contract.yaml

summary: "<one sentence>"
cases: []
order: []
open_questions: []
assumptions: []
```

## Context budget

- Read feature contract first.
- Read DB/API contracts only if present and relevant.

## Failure handling

- Missing feature contract → stop and suggest `/feature-design <FEATURE>`.
- No acceptance criteria → stop and ask for contract correction.

## Forbidden

- Implementing tests or product code in this skill.

## Quality bar (self-check before finishing)

- [ ] Cases trace to acceptance criteria or explicit assumptions.
- [ ] Outputs remain concise and actionable.
