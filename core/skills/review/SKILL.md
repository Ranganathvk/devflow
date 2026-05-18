---
name: review
description: >-
  After /implement <TASK_ID> (or a focused change set), runs a bounded checklist review and
  writes AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md plus paired REVIEW.contract.yaml. Hand off to
  /debug if fixes are needed, else /snapshot after human sign-off and green tests.
---

# /review — Bounded post-change review

## Purpose

Provide a **repeatable, file-backed review** for a single task-sized change set so the human stays the owner of merge decisions. The agent **does not** “approve” its own work as final: it records **checklist results**, **findings**, and **machine-readable** status for `/debug`, `/snapshot`, and `/learn`. This skill **does not** rewrite application code except typos in review docs if the human asks.

## When to invoke

- `/review <TASK_ID>` — immediately after `/implement <TASK_ID>` (or when the human points at a ready change set tied to that ID).
- `/review` — only when `AI_CONTEXT/PROJECT_STATE.md` (or the user message) clearly names the active `<TASK_ID>` and changed paths; otherwise **stop** with one question asking for `<TASK_ID>` or an explicit file list.
- Do **not** invoke for multiple unrelated tasks in one run — one review = one `<TASK_ID>` or one explicitly bounded file list (then encode a synthetic `task_id` in the contract as `ADHOC:1` only if the human authorized ad-hoc review).
- Do **not** invoke before there is a **concrete** diff or file list to review (git diff, PR, or paths).

## Inputs

- **Required:** `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$` **or** explicit paths + human waiver for ad-hoc (see Purpose).
- **Required:** `AI_CONTEXT/SPEC.md` — read **Design principles**, **Implementation rules**, and **Human code ownership** (minimum).
- **Required:** Change set — `git diff` / `git show` / or the files the human listed as in-scope for this review.
- **Optional:** `AI_CONTEXT/<FEATURE>_TASKS.contract.yaml` — the single `tasks[]` row for `<TASK_ID>` (`<FEATURE>` parsed from the ID) for `scope.in` / `implements_cases` cross-check.
- **Optional:** `AI_CONTEXT/<FEATURE>_TDD.contract.yaml` — narrow read: only `cases[]` rows for `TC-*` listed on the task row.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md` — branch, constraints, or “what was supposed to be done.”
- **Forbidden:** Treating chat as the diff. Inventing files “reviewed” that are not in the change set. Approving work without listing evidence (commands run, files read).

## Workflow

1. **Parse** `<TASK_ID>` into `feature_id` (`<FEATURE>`) and chunk `C<n>`. Derive **safe basename** `review_basename = "<FEATURE>_C<n>"` (filename-safe; mirrors `AUTH:C1` → `AUTH_C1`).
2. **Resolve** change set: prefer repository diff against merge base or last commit; if ambiguous, **stop** with one question.
3. **Scope check:** If `<FEATURE>_TASKS.contract.yaml` exists, confirm edits align with that task’s `scope.in` / `implements_cases`; flag **violations** as `blocking` findings.
4. **Checklist (systematic):** Cover at minimum: correctness vs task/TDD IDs, tests present for new behavior, error paths, naming/style match, secrets/logging, migration safety if applicable, and “no drive-by refactors.” Record each item as **pass / fail / not_applicable** with a one-line note in the human doc.
5. **Classify findings:** Each issue is `blocking` (must fix before sign-off) or `non_blocking` (may defer with explicit reason in `deferred[]`).
6. **Write** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.md` (target ≤ **~120** lines): summary, checklist table, findings, open questions for the human, **sign-off block** (human fills).
7. **Write** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` using the **YAML shape** below. Set `agent_ready_for_signoff` to `true` only if there are **zero** `blocking` findings.
8. **Chat reply (brief):** Paths written, blocking vs non-blocking counts, suggested next step: **`/debug <TASK_ID>`** if blocking findings or failing tests were observed; else remind human to sign off in the `.md` and run tests, then **`/snapshot <TASK_ID>`**.

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

- **Missing TASK_ID and no unambiguous state** → Stop; ask for `<TASK_ID>` once.
- **No diff / no files** → Stop; ask how to obtain the change set.
- **Cannot map changes to task scope** → Still write review with `findings` noting **scope_mismatch** as blocking unless human confirms ad-hoc scope.

## Forbidden

- Silent approval without documented checklist.
- Editing implementation source files (this is `/debug` / `/implement`).
- Rewriting `<FEATURE>_TASKS.contract.yaml` or upstream contracts to match code.

## Quality bar (self-check before finishing)

- [ ] Both `*_REVIEW.md` and `*_REVIEW.contract.yaml` exist for one `review_basename`.
- [ ] Every `blocking` finding has a clear next action for `/debug`.
- [ ] Chat states the suggested next slash command.
