---
name: review
description: >-
  After /implement-next or /implement <TASK_ID>, runs a bounded checklist review and writes
  REVIEW artifacts. Invoke as /review <TASK_ID> or /review (uses current_task from PLAN or TASKS contract).
  Simple Dev Loop: fix blockers in editor or chat, re-run /review, then /snapshot after sign-off.
  Legacy: /debug available for automated fix pass before snapshot.
---

# /review — Bounded post-change review

## Purpose

Provide a **repeatable, file-backed review** for a single task-sized change set so the human stays the owner of merge decisions. The agent **does not** “approve” its own work as final: it records **checklist results**, **findings**, and **machine-readable** status for `/snapshot` (and optionally `/learn`). **Simple Dev Loop:** does not use `/debug` — blocking issues are fixed outside this skill, then `/review` is re-run. This skill **does not** rewrite application code except typos in review docs if the human asks.

## When to invoke

- `/review <TASK_ID>` — immediately after `/implement-next` or `/implement <TASK_ID>` (or when the human points at a ready change set tied to that ID).
- `/review` — resolve `<TASK_ID>` from `current_task` on an approved **plan** or **tasks** contract (see **Resolve TASK_ID**). If null, **stop** and run `/implement-next`.
- `/review` — **legacy:** only when `PROJECT_STATE.md` or the user message clearly names the active `<TASK_ID>`; otherwise stop with one question.
- Do **not** invoke for multiple unrelated tasks in one run — one review = one `<TASK_ID>` or one explicitly bounded file list (then encode a synthetic `task_id` in the contract as `ADHOC:1` only if the human authorized ad-hoc review).
- Do **not** invoke before there is a **concrete** diff or file list to review (git diff, PR, or paths).

## Inputs

- **Required:** Resolved `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$` **or** explicit paths + human waiver for ad-hoc (see Purpose).
- **Required:** `AI_CONTEXT/SPEC.md` — read **Design principles**, **Implementation rules**, and **Human code ownership** (minimum).
- **Required:** Change set — `git diff` / `git show` / or the files the human listed as in-scope for this review.
- **Optional (brownfield):** `AI_CONTEXT/<FEATURE>_PLAN.contract.yaml` — task row + `test_cases[]`.
- **Optional (greenfield):** `AI_CONTEXT/<FEATURE>_TASKS.contract.yaml` — task row + TDD cases.
- **Optional:** `AI_CONTEXT/<FEATURE>_TDD.contract.yaml` — narrow `cases[]` when not using plan `test_cases[]`.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md` — branch, constraints, or “what was supposed to be done.”
- **Forbidden:** Treating chat as the diff. Inventing files “reviewed” that are not in the change set. Approving work without listing evidence (commands run, files read).

## Resolve TASK_ID (when argument omitted)

1. Find contracts with non-null `current_task`:
   - `*_PLAN.contract.yaml` (`workflow_profile: simple_dev_loop`)
   - `*_TASKS.contract.yaml` (`workflow_profile: greenfield_dev_loop`)
2. **One match** → use `current_task`.
3. **Multiple** → stop; ask for `/review <TASK_ID>`.
4. **None** → `PROJECT_STATE.md` / user message; else stop.

## Workflow

1. **Resolve** `<TASK_ID>` from argument or **Resolve TASK_ID** above.
2. **Parse** into `feature_id` (`<FEATURE>`) and chunk `C<n>`. Derive **safe basename** `review_basename = "<FEATURE>_C<n>"` (filename-safe; mirrors `AUTH:C1` → `AUTH_C1`).
3. **Resolve** change set: prefer repository diff against merge base or last commit; if ambiguous, **stop** with one question.
4. **Scope check:** Load task row from plan `tasks[]` or greenfield `tasks[]`. Confirm edits align with `scope_in` and `implements_cases`; flag **violations** as `blocking`.
5. **Checklist (systematic):** Cover at minimum: correctness vs task/TDD IDs, tests present for new behavior, error paths, naming/style match (`CONVENTIONS.contract.yaml` when present), secrets/logging, migration safety if applicable, and “no drive-by refactors.” Record each item as **pass / fail / not_applicable** with a one-line note in the human doc.
6. **Classify findings:** Each issue is `blocking` (must fix before sign-off) or `non_blocking` (may defer with explicit reason in `deferred[]`).
7. **Write** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` (target ≤ **~120** lines): summary, checklist table, findings, open questions for the human, **sign-off block** (human fills).
8. **Write** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` using the **YAML shape** below. Set `plan_contract_path` when plan exists. Set `agent_ready_for_signoff` to `true` only if there are **zero** `blocking` findings.
9. **Chat reply (brief):** Paths written, blocking vs non-blocking counts. If **blocking:** fix code/tests (editor or chat), then **`/review`** again — do **not** suggest `/debug` on Simple Dev Loop. If clear: human sign-off then **`/snapshot`**.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` | Created or replaced | Human checklist + sign-off block |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` | Created or replaced | Machine handoff; small YAML |

No other files written or edited.

## `<FEATURE>_C<n>_REVIEW.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_review
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
review_basename: "<FEATURE>_C<n>"
plan_contract_path: AI_CONTEXT/<FEATURE>_PLAN.contract.yaml  # null if legacy tasksplit only

agent_checklist_completed: true
agent_ready_for_signoff: false  # true only if zero blocking findings

findings:
  # - id: "RV-001"
  #   severity: blocking | non_blocking
  #   summary: "<short>"
  #   paths: []   # optional

deferred: []   # non_blocking items explicitly deferred with reason

resolved_findings: []  # RV-* ids fixed in /debug — append only; do not delete history

human_signoff: pending  # pending | approved | rejected — human updates when ready
human_signoff_notes: ""

linked_snapshot_path: null  # filled by /snapshot when run

last_debug_pass: null  # optional ISO8601 — set by /debug
```

## Context budget

- Read in full: `SPEC.md` (required sections); the single task row when present; only the `TC-*` rows needed from TDD contract.
- Read via diff/stat: the change set only — not the whole repo.

## Failure handling

- **Missing TASK_ID and no `current_task` on plan contract** → Stop; ask for `<TASK_ID>` once or run `/implement-next`.
- **No diff / no files** → Stop; ask how to obtain the change set.
- **Cannot map changes to task scope** → Still write review with `findings` noting **scope_mismatch** as blocking unless human confirms ad-hoc scope.

## Forbidden

- Silent approval without documented checklist.
- Editing implementation source files (this is `/debug` / `/implement`).
- Rewriting plan or tasks contracts to match code (except `linked_snapshot_path` / review fields).

## Quality bar (self-check before finishing)

- [ ] Both `*_REVIEW.md` and `*_REVIEW.contract.yaml` exist for one `review_basename`.
- [ ] Every `blocking` finding has a clear fix path (re-review; no `/debug` on Simple Dev Loop).
- [ ] Chat states the suggested next slash command.
