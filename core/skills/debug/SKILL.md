---
name: debug
description: >-
  Legacy/advanced: minimal fixes after /review blocking findings. Default loop: fix in editor and
  re-run /review. Invoke as /debug <TASK_ID> when automated fix pass is desired.
---

# /debug — Surgical fix pass for a reviewed task

## Purpose

Close the loop between **`/review`** and a **green verification** state by fixing **defects** (test failures, checklist blockers, obvious regressions) **inside the same task boundary**. This skill **mutates production and test code** — but only when justified by documented findings or failing output, not new scope.

## When to invoke

- `/debug <TASK_ID>` — when review contract lists `blocking` findings and/or tests fail for that task.
- `/debug` — **Simple Dev Loop:** resolve `<TASK_ID>` from `current_task` on `<FEATURE>_PLAN.contract.yaml` (same rules as `/review`).
- Do **not** invoke without a **specific** defect source (review findings, CI log, or repro steps) — gather that first.
- Do **not** use `/debug` to start new features; if scope grows, stop and suggest `/design` refresh (Simple Dev Loop) or `/tasksplit` (legacy).

## Inputs

- **Required:** Resolved `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required:** `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml` for that task (create via `/review` first **or** human provides equivalent pasted findings — if missing, run `/review` first unless human explicitly waived with a pasted defect list).
- **Required:** `{context_dir}/SPEC.md` — **Implementation rules** and **Design principles** (minimum).
- **Optional (legacy):** `{context_dir}/<FEATURE>_PLAN.contract.yaml` — task row when deprecated plan queue used.
- **Optional:** `{context_dir}/<FEATURE>_TASKS.contract.yaml` — task row for scope.
- **Optional:** Plan `test_cases[]` or `<FEATURE>_TDD.contract.yaml` for failing `TC-*`.
- **Forbidden:** Expanding task scope. “Fixing” upstream contracts to match wrong code without human direction. Unbounded refactors.

## Resolve TASK_ID (when argument omitted)

Same algorithm as `/review`: read `current_task` from `*_TASKS.contract.yaml` first; legacy `*_PLAN.contract.yaml` fallback.

## Workflow

1. **Resolve** `<TASK_ID>` from argument or plan `current_task`.
2. **Parse** → `<FEATURE>`, `C<n>`, `review_basename = "<FEATURE>_C<n>"`.
3. **Load** `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml`. If missing and human did not supply a defect list → **stop**; suggest `/review` first.
4. **Triage:** Map each `blocking` finding and each test failure to concrete code locations. If anything requires **out-of-scope** files per task `scope_out` (plan) or `scope.out` (legacy), **stop** with one escalation note — do not silently expand.
5. **Fix:** Apply the **smallest** edits that resolve blocking issues; prefer tests that encode the intended behavior from `implements_cases` / `TC-*`.
6. **Verify:** Run the same test/lint command the repo uses for this area (or full suite if that is the norm). Iterate **only** within scope until green or blocked.
7. **Update review artifact:** Patch `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml`:
   - Append resolved finding IDs under `resolved_findings: []` (stable id per finding) **or** remove/adjust findings if the schema uses resolution fields — maintain `contract_version: "1"`.
   - Set `agent_ready_for_signoff` to `true` only if no remaining `blocking` findings.
   - Add `last_debug_pass: "<ISO8601 date>"` (optional key) for traceability.
8. **Append** a short **“Debug log”** section to `{context_dir}/<FEATURE>_C<n>_REVIEW.md` (≤ ~40 lines): what changed, commands run, results.
9. **Chat reply (brief):** Files touched, commands + results, remaining blockers (if any). Suggest **`/review`** or **`/review <TASK_ID>`** if another pass is needed, else **human sign-off** then **`/snapshot`**.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| Source and test files | As needed | Only within task `scope.in` and defect-driven |
| `{context_dir}/<FEATURE>_C<n>_REVIEW.contract.yaml` | Patched | Resolution + readiness flags |
| `{context_dir}/<FEATURE>_C<n>_REVIEW.md` | Appended section | Debug log |

Do **not** edit `<FEATURE>_TASKS.contract.yaml` or other upstream contracts unless the human explicitly asked to amend the plan.

## Context budget

- Read in full: review contract; task row; SPEC minimum sections.
- Read partial: only failing stack traces / diff hunks referenced by findings.

## Failure handling

- **Defect not reproducible** → Stop after one isolation attempt; list hypotheses and data needed.
- **Scope insufficient** → Stop; propose `/design` refresh (Simple Dev Loop) or `/tasksplit` (legacy), or human approval to widen scope.
- **Flaky tests** → Document in review `non_blocking` with `deferred` reason; do not merge “lucky green.”

## Forbidden

- Feature creep or new APIs not required by the defect.
- Dropping findings without code/test evidence of resolution.
- Editing `human_signoff` — human only (unless the human’s message explicitly sets it).

## Quality bar (self-check before finishing)

- [ ] Every addressed `blocking` finding maps to a code/test change or a documented unblocker.
- [ ] Verification command(s) stated in chat with outcome.
- [ ] Review contract reflects current blocking count.
