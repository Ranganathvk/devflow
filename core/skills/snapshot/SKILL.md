---
name: snapshot
description: >-
  After review sign-off and green verification, records a compact checkpoint for <TASK_ID>:
  AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml plus a one-line append to PROJECT_STATE.md
  when that file exists. Feeds /learn.
---

# /snapshot — Verified checkpoint for a task

## Purpose

Capture a **durable, machine-readable checkpoint** that a task’s change set was **reviewed** and **verified** (tests or agreed checks), so later sessions and `/learn` do not depend on chat history. This skill is **not** a git replacement — it records **workflow metadata** and pointers for humans and downstream automation.

## When to invoke

- `/snapshot <TASK_ID>` — after **`/review`** artifacts exist, **human_signoff** is `approved` in `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` **or** the human’s latest message explicitly approves merge for this task, **and** verification commands have **passed** (or human explicitly waived tests with a one-line reason recorded in the snapshot contract).
- Do **not** snapshot with failing tests unless the human explicitly instructed waiver and the waiver is recorded in the snapshot YAML under `verification.waiver`.
- Do **not** snapshot multiple tasks in one invocation.

## Inputs

- **Required:** `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required:** `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` — confirm `human_signoff: approved` **or** copy explicit human approval from chat into `verification.approval_source: chat` (human message paraphrase ≤ 200 chars).
- **Required:** `AI_CONTEXT/SPEC.md` — skim **Human code ownership** (minimum).
- **Optional:** `git rev-parse HEAD` (or equivalent) for `git_head`.
- **Optional:** `AI_CONTEXT/PROJECT_STATE.md` — append one-line summary when present.
- **Forbidden:** Fabricating green test results.

## Workflow

1. **Parse** `<TASK_ID>` → `<FEATURE>`, `C<n>`, `basename = "<FEATURE>_C<n>"`.
2. **Verify gate:** If `human_signoff` is not `approved` and no explicit chat approval was given → **stop**; point to `/review` completion steps.
3. **Record verification:** Capture commands run and outcome (`passed` / `waived`). If waived, require `verification.waiver.reason` and `verification.waiver.approver_note` from human input.
4. **Write** `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` using the **YAML shape** below.
5. **Link back:** Update `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` field `linked_snapshot_path` to the snapshot path (relative to repo root as `AI_CONTEXT/...`).
6. **PROJECT_STATE:** If `AI_CONTEXT/PROJECT_STATE.md` exists, append one dated line: ``- [snapshot] `<TASK_ID>` verified (`<basename>_SNAPSHOT.contract.yaml`)`` — do **not** create the file solely for this line unless the human asked to start `PROJECT_STATE.md`.
7. **Chat reply (brief):** Snapshot path, verification summary, suggested **`/learn <TASK_ID>`**.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `AI_CONTEXT/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` | Created or replaced | Small YAML |
| `AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml` | Patch `linked_snapshot_path` only | Optional if field already set correctly |
| `AI_CONTEXT/PROJECT_STATE.md` | Optional one-line append | Only if file already exists |

No source code edits in this skill.

## `<FEATURE>_C<n>_SNAPSHOT.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_snapshot
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
snapshot_basename: "<FEATURE>_C<n>"

captured_at: "<ISO8601>"

git_head: "<sha-or-unknown>"

review_contract_path: "AI_CONTEXT/<FEATURE>_C<n>_REVIEW.contract.yaml"
human_signoff: approved

verification:
  status: passed | waived
  commands: []     # e.g. ["pnpm test", "pnpm lint"]
  waiver: null     # or { reason: "...", approver_note: "..." }

notes: ""   # optional short human/agent context for /learn
```

## Context budget

- Read in full: review contract; optional PROJECT_STATE tail.
- Do **not** load full chat — only explicit human approval text if using `approval_source: chat`.

## Failure handling

- **Tests not run and no waiver** → Stop; suggest running tests or documenting waiver.
- **Review contract shows blocking findings** → Stop; suggest `/debug` then `/review`.

## Forbidden

- Claiming verification without commands or waiver documented.
- Editing implementation files.

## Quality bar (self-check before finishing)

- [ ] Snapshot YAML exists and references the review artifact.
- [ ] `verification.status` matches actual outcome or documented waiver.
- [ ] Chat suggests `/learn <TASK_ID>`.
