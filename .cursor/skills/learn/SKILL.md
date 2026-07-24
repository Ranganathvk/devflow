---
name: learn
description: >-
  After /snapshot <TASK_ID>, distills durable lessons into artifacts/LEARNINGS.md (append)
  and optionally artifacts/<FEATURE>_C<n>_LEARN.contract.yaml for automation. Closes the
  implement → review → debug → snapshot loop for knowledge retention.
---

# /learn — Durable lessons after a verified task

## Purpose

Turn a **completed, snapshotted** task into **compact, reusable knowledge** for the team and future agents: what worked, what surprised us, what to avoid, and which contracts or tests to trust next time. Keeps **`artifacts/`** as the durable source of truth per framework rules.

## When to invoke

- `/learn <TASK_ID>` — immediately after `/snapshot <TASK_ID>` produced `artifacts/<FEATURE>_C<n>_SNAPSHOT.contract.yaml`.
- `/learn <TASK_ID>` — when revisiting an older snapshot to backfill lessons (human-directed).
- Do **not** invoke before a snapshot exists **unless** the human explicitly requests **“lessons without snapshot”** for a cancelled/aborted task — then set `learn_kind: aborted` in the contract and skip verification claims.
- Do **not** dump raw logs into `LEARNINGS.md` — summarize.

## Inputs

- **Required:** `<TASK_ID>` matching `^[A-Z][A-Z0-9_]{1,31}:C[1-9][0-9]*$`.
- **Required:** `artifacts/<FEATURE>_C<n>_SNAPSHOT.contract.yaml` when `learn_kind: complete` (default).
- **Optional:** `artifacts/<FEATURE>_C<n>_REVIEW.contract.yaml` — findings / deferred items worth carrying forward.
- **Optional:** `artifacts/<FEATURE>_TASKS.contract.yaml` — task `title` / `risk` for indexing.
- **Optional:** `artifacts/SPEC.md` — only if lessons propose SPEC-level process changes (then list SPEC sections to edit separately; do not silently rewrite SPEC unless human asked).
- **Forbidden:** Invention of incidents not supported by snapshot/review/implement artifacts.

## Workflow

1. **Parse** `<TASK_ID>` → `<FEATURE>`, `C<n>`, `basename = "<FEATURE>_C<n>"`.
2. **Load** snapshot contract. If missing and not in **aborted** mode → **stop**; run `/snapshot` first.
3. **Extract** 3–7 bullet lessons (max): patterns, pitfalls, test gaps closed, contract ambiguities discovered, operational commands worth standardizing.
4. **Append** to `artifacts/LEARNINGS.md`:
   - Create the file with a one-line header if missing: `# Project learnings (append-only, newest at bottom)` (or match existing file style if present).
   - New section: `## <YYYY-MM-DD> — <TASK_ID> (<FEATURE> C<n>)` followed by bullets + optional **“Follow-ups”** sub-list (SPEC edits, new TC-* ideas) **without** implementing them here.
5. **Write** `artifacts/<FEATURE>_C<n>_LEARN.contract.yaml` using the **YAML shape** below (keeps machine consumers independent of prose layout).
6. **Chat reply (brief):** Path to learnings + contract, top 1–2 lessons, suggested next task from backlog if applicable.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `artifacts/LEARNINGS.md` | Created or appended | New dated section; avoid bloat |
| `artifacts/<FEATURE>_C<n>_LEARN.contract.yaml` | Created or replaced | Small YAML |

No other files written or edited.

## `<FEATURE>_C<n>_LEARN.contract.yaml` shape

```yaml
contract_version: "1"
artifact: task_learn
task_id: "<FEATURE>:C<n>"
feature_id: "<FEATURE>"
learn_kind: complete | aborted

snapshot_contract_path: "artifacts/<FEATURE>_C<n>_SNAPSHOT.contract.yaml"  # null if aborted

lessons: []
  # - id: "L-001"
  #   summary: "<one line>"
  #   category: process | test | design | ops | other

follow_ups: []
  # - summary: "<proposed next action>"
  #   owner: human | agent
```

## Context budget

- Read in full: snapshot contract; optional review contract summary fields only.
- Do **not** re-read entire task/TDD prose.

## Failure handling

- **Snapshot missing** → Stop (unless aborted mode with human confirmation).
- **LEARNINGS.md huge** → Append only; suggest human archive old sections if > ~500 lines.

## Forbidden

- Deleting or rewriting prior dated sections in `LEARNINGS.md` (append-only discipline).
- Claiming lessons not grounded in artifacts.

## Quality bar (self-check before finishing)

- [ ] Dated section exists in `LEARNINGS.md` for this `<TASK_ID>`.
- [ ] Learn contract lists the same lessons as the prose (IDs optional but consistent).
- [ ] No verification claims when `learn_kind: aborted`.
