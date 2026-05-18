---
name: debug
description: >-
  After /review surfaces blocking findings or tests fail, applies minimal fixes within the same
  task scope, re-runs checks, and updates the review contract status fields. Next: /review again
  or /snapshot when green and signed off.
---

# /debug — Surgical fix pass for a reviewed task

## Purpose

Close the loop between **`/review`** and a **green verification** state by fixing **defects** (test failures, checklist blockers, obvious regressions) **inside the same task boundary**. This skill **mutates production and test code** — but only when justified by documented findings or failing output, not new scope.

## When to invoke

- `/debug <TASK_ID>` — when `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` lists `blocking` findings and/or tests fail for that task’s change set.
- `/debug <TASK_ID>` — when the human pastes failing logs and points at the task ID.
- Do **not** invoke without a **specific** defect source (review findings, CI log, or repro steps) — gather that first.
- Do **not** use `/debug` to start new features; return to `/implement` / `/tasksplit` if scope grows.

## Inputs

- **Required:** `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required:** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` for that task (create via `/review` first **or** human provides equivalent pasted findings — if missing, run `/review <TASK_ID>` first unless human explicitly waived with a pasted defect list).
- **Required:** `AI_CONTEXT/SPEC.md` — **Implementation rules** and **Design principles** (minimum).
- **Optional:** `AI_CONTEXT/<FEATURE>_TASKS.contract.yaml` — task row for `scope.in` / `scope.out` / `implements_cases`.
- **Optional:** `AI_CONTEXT/<FEATURE>_TDD.contract.yaml` — narrow `cases[]` for failing `TC-*`.
- **Forbidden:** Expanding `scope.in`. “Fixing” upstream contracts to match wrong code without human direction. Unbounded refactors.

## Workflow

1. **Parse** `<TASK_ID>` → `<FEATURE>`, `C<n>`, `review_basename = "<FEATURE>_C<n>"`.
2. **Load** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml`. If missing and human did not supply a defect list → **stop**; suggest `/review <TASK_ID>` first.
3. **Triage:** Map each `blocking` finding and each test failure to concrete code locations. If anything requires **out-of-scope** files per task `scope.out`, **stop** with one escalation note — do not silently expand.
4. **Fix:** Apply the **smallest** edits that resolve blocking issues; prefer tests that encode the intended behavior from `implements_cases` / `TC-*`.
5. **Verify:** Run the same test/lint command the repo uses for this area (or full suite if that is the norm). Iterate **only** within scope until green or blocked.
6. **Update review artifact:** Patch `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml`:
   - Append resolved finding IDs under `resolved_findings: []` (stable id per finding) **or** remove/adjust findings if the schema uses resolution fields — maintain `contract_version: "1"`.
   - Set `agent_ready_for_signoff` to `true` only if no remaining `blocking` findings.
   - Add `last_debug_pass: "<ISO8601 date>"` (optional key) for traceability.
7. **Append** a short **“Debug log”** section to `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` (≤ ~40 lines): what changed, commands run, results.
8. **Chat reply (brief):** Files touched, commands + results, remaining blockers (if any). Suggest **`/review <TASK_ID>`** if another human/agent pass is needed, else **human sign-off** then **`/snapshot <TASK_ID>`**.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| Source and test files | As needed | Only within task `scope.in` and defect-driven |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` | Patched | Resolution + readiness flags |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` | Appended section | Debug log |

Do **not** edit `<FEATURE>_TASKS.contract.yaml` or other upstream contracts unless the human explicitly asked to amend the plan.

## Context budget

- Read in full: review contract; task row; SPEC minimum sections.
- Read partial: only failing stack traces / diff hunks referenced by findings.

## Failure handling

- **Defect not reproducible** → Stop after one isolation attempt; list hypotheses and data needed.
- **Scope insufficient** → Stop; propose new `/tasksplit` chunk or human approval to widen `scope.in`.
- **Flaky tests** → Document in review `non_blocking` with `deferred` reason; do not merge “lucky green.”

## Forbidden

- Feature creep or new APIs not required by the defect.
- Dropping findings without code/test evidence of resolution.
- Editing `human_signoff` — human only (unless the human’s message explicitly sets it).

## Quality bar (self-check before finishing)

- [ ] Every addressed `blocking` finding maps to a code/test change or a documented unblocker.
- [ ] Verification command(s) stated in chat with outcome.
- [ ] Review contract reflects current blocking count.
