---
name: feature-research
description: >-
  Optional Stage 3 objective inspection for one FEATURE. Writes AI_CONTEXT/<FEATURE>_RESEARCH.md
  plus <FEATURE>_RESEARCH.contract.yaml. Invoke as /feature-research <FEATURE> when codebase facts
  are needed before design or implementation.
---

# /feature-research \<FEATURE\> — Optional evidence pass

## Purpose

Produce evidence-backed findings about existing code, gaps, and constraints for one feature. This skill is optional: use it when uncertainty is factual (repo state), skip it when the feature is simple and low risk.

## When to invoke

- Use when implementation risk comes from unknown current code behavior.
- Use before design for non-trivial or legacy-heavy areas.
- Skip for straightforward greenfield/lite features when direct implementation is faster.

## Inputs

- **Required:** `AI_CONTEXT/SPEC.md`.
- **Required:** `AI_CONTEXT/FEATURE_SLICES.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml`.
- **Optional:** `AI_CONTEXT/<FEATURE>.contract.yaml` (refresh mode), `AI_CONTEXT/SYSTEM_HLD.contract.yaml`, `AI_CONTEXT/PROJECT_STATE.md`.
- **Forbidden:** Speculative claims without file evidence.

## Workflow

1. Validate `<FEATURE>` and slice membership.
2. Build a bounded research checklist from feature scope and any open questions.
3. Inspect repository evidence (paths/symbols) for each checklist item.
4. Record findings as `found`, `not_found`, `partial`, or `blocked`.
5. Write paired markdown + YAML outputs.
6. Suggest next step: `/feature-design`, `/implement <FEATURE>`, or both depending on risk.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_RESEARCH.md` | Created or replaced | Optional artifact |
| `AI_CONTEXT/<FEATURE>_RESEARCH.contract.yaml` | Created or replaced | Optional handoff |

No other files written or edited.

## `<FEATURE>_RESEARCH.contract.yaml` shape

```yaml
contract_version: "1"
artifact: feature_research
feature_id: "<FEATURE>"
spec_path: AI_CONTEXT/SPEC.md
feature_slices_contract_path: AI_CONTEXT/FEATURE_SLICES.contract.yaml
questions_contract_path: AI_CONTEXT/<FEATURE>_QUESTIONS.contract.yaml

summary: "<facts-only summary>"
findings: []
  # - id: FR-001
  #   topic: "<area>"
  #   result: found | not_found | partial | blocked
  #   evidence: []
  #   notes: "<short>"

implications_for_design: []
open_gaps: []
```

## Context budget

- Prefer targeted code reads driven by checklist; avoid broad unrelated scans.

## Failure handling

- Missing slices contract or unknown feature ID → stop and suggest `/slice`.
- Sparse repository evidence → keep results in `blocked` / `open_gaps` instead of guessing.

## Forbidden

- Writing design, DB, API, TDD, tasksplit, or implementation artifacts.

## Quality bar (self-check before finishing)

- [ ] Findings are evidence-backed.
- [ ] Output stays compact and factual.
