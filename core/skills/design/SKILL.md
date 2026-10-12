---
name: design
description: >-
  Design a feature in one bounded investigation-and-synthesis pass. Bundles safe impact analysis,
  research, design, and conditional DB/API contracts; stops for material human decisions and final
  design approval. Invoke /design FEATURE, /design "description", or /design to ask for intent.
---

# /design [<FEATURE> | "description"] [approved]

## Purpose

Turn confirmed feature intent into a reviewable design and a machine-readable feature contract with the fewest useful interactions. Perform related read-only analysis together; do not require a separate invocation for each mechanical stage.

Downstream: `/tdd <FEATURE>` → `/tasksplit <FEATURE>` → `/implement`.

This skill never edits application source or invokes downstream skills.

## Invocation

- `/design`: ask what feature/change to design if intent is not already clear from SPEC or the user message.
- `/design "add OTP login"`: propose a feature ID and begin.
- `/design OTP_LOGIN`: create or resume the draft.
- `/design OTP_LOGIN approved`: explicitly approve the currently presented complete design, if no blocking questions remain.
- If a feature contract already exists, resume it; do not overwrite approved decisions or silently reset status.

## Inputs

- Required: `{context_dir}/SPEC.md`.
- Brownfield required: `{context_dir}/<FEATURE>_PLAN.contract.yaml` with `ready_for_design: true` and `approval.status: approved`. If missing or unapproved, stop and suggest `/understand <FEATURE>`.
- Optional: `{context_dir}/FEATURE_SLICES.contract.yaml`, `{context_dir}/SYSTEM_HLD.contract.yaml`.
- Required for repository impact analysis: consumer repo access.
- Do not treat unbounded chat as a spec or invent unconfirmed product behavior.

## Operating model

One invocation may complete multiple safe, related steps:

1. **Load and validate** SPEC, approved brownfield plan (if applicable), slices/HLD, and any existing feature contract.
2. **Investigate** the relevant code path read-only. Trace entry point, owner, dependencies, patterns, tests, and relevant configuration. Normally inspect no more than 12 source/config/test files; expand only with a concrete reason.
3. **Synthesize** the behavior, scope, acceptance criteria, delivery flags, design choice, failure paths, observability, security, compatibility, migration/deployment concerns, and operational risks relevant to this feature.
4. **Classify** `needs_db`, `needs_api`, and `needs_tasks` with rationale.
5. **Persist** the feature design and contract; emit DB/API contracts only when applicable.
6. **Review boundary:** if a material product, architecture, compatibility, security, or migration decision needs human input, ask one focused question and stop. Otherwise present the coherent design for explicit approval.

Do not stop after an individual search or mechanical analysis category. Stop when human knowledge/approval is required, evidence is unavailable, a blocking risk cannot be resolved safely, or the design is ready for review.

## Delivery classification

Infer from confirmed intent, SPEC, brownfield evidence, and system context. Record rationale in `delivery.notes`.

| Flag | True when | False when |
|---|---|---|
| `needs_db` | Persistence, entities, schema, or migrations change | No durable data/store impact |
| `needs_api` | HTTP/RPC/events/CLI interface or external integration changes | Internal-only change without interface impact |
| `needs_tasks` | Scope is non-trivial and benefits from an approved task queue | A single bounded vertical slice is safe and reviewable |

Do not guess when uncertainty materially changes the design. Ask one targeted question and preserve the rest of the analysis as draft.

## Approval and resume semantics

- Initial invocation should complete the safe investigation/design work possible from available evidence and produce a coherent draft, not just create a skeleton.
- If one material decision is unresolved, record it in `open_questions[]`, keep `design_status: draft`, ask one focused question, and stop. Resume with `/design <FEATURE>`.
- When all blocking questions are resolved, show the design summary, key evidence, acceptance criteria, delivery flags, risks, and artifacts. Ask for explicit whole-design approval.
- `/design <FEATURE> approved` approves the **entire currently presented draft**, not a stage. Only accept it when no blocking questions or blocking compatibility risks remain.
- Any material scope/design change after approval resets `design_status: draft` and requires approval again.
- Set `design_status: approved` only after explicit human approval. `/tdd` must refuse otherwise.

## Output artifacts

| Path | Default |
|---|---|
| `{context_dir}/<FEATURE>.contract.yaml` | Always; canonical structured feature state and approval |
| `{context_dir}/<FEATURE>_DESIGN.md` | Always; human-reviewable design rationale and evidence |
| `{context_dir}/<FEATURE>_DB.contract.yaml` | Only when `delivery.needs_db: true` |
| `{context_dir}/<FEATURE>_API.contract.yaml` | Only when `delivery.needs_api: true` |
| `{context_dir}/<FEATURE>_DB.md` | Optional when separate data-design review materially helps or requested |
| `{context_dir}/<FEATURE>_API.md` | Optional when separate interface-design review materially helps or requested |

Contracts are the downstream handoff. Optional DB/API Markdown is a readable view, not an independently maintained source of truth. Record why conditional outputs were skipped through `delivery` flags; do not create empty placeholder documents.

## Feature contract shape

```yaml
contract_version: "1"
artifact: feature
workflow_profile: devflow
feature_id: "<FEATURE>"
title: "<short title>"
design_status: draft # draft | approved
approved_at: null
spec_path: "{context_dir}/SPEC.md"
feature_plan_contract_path: null
feature_slices_contract_path: null

summary: "<problem and intended outcome>"
in_scope: []
out_of_scope: []
acceptance_criteria:
  # - id: AC-001
  #   given_when_then: "Given ... When ... Then ..."
design:
  approach: "<chosen approach and rationale>"
  components: []
  evidence_paths: []
  alternatives: []
  failure_modes: []
  observability: []
  security: []
  compatibility: []
  migration_and_deployment: []
delivery:
  delivery_profile: lite # lite | standard | heavy
  needs_db: false
  needs_api: false
  needs_tasks: false
  notes: "<rationale for classification>"
depends_on: []
open_questions: []
risks: []
assumptions: []
```

## Conditional DB contract

Write only when `needs_db: true`.

```yaml
contract_version: "1"
artifact: feature_db
feature_id: "<FEATURE>"
feature_contract_path: "{context_dir}/<FEATURE>.contract.yaml"
summary: "<one sentence>"
persistence:
  primary_store: sql # sql | document | kv | file | none | TBD
entities: []
relationships: []
migrations: []
consistency_and_transactions: []
backfill_and_rollback: []
open_questions: []
```

## Conditional API contract

Write only when `needs_api: true`.

```yaml
contract_version: "1"
artifact: feature_api
feature_id: "<FEATURE>"
feature_contract_path: "{context_dir}/<FEATURE>.contract.yaml"
summary: "<one sentence>"
style:
  protocol: rest # rest | grpc | graphql | cli | in_process | event | TBD
operations: []
auth_and_authorization: []
validation_and_errors: []
compatibility: []
observability: []
open_questions: []
```

## Failure handling

- Missing SPEC: seed from template or suggest `/grillme`; do not fabricate product intent.
- Missing/unapproved brownfield plan: stop and suggest `/understand <FEATURE>`.
- No repository access: make only clearly labeled assumptions, provide one compact targeted evidence request, and keep the design draft.
- Conflicting evidence: record the conflict and ask if it changes a material decision.
- Blocking compatibility/security/migration risk: do not mark design approved until resolved or explicitly re-scoped by the human.
- Missing acceptance criteria: ask a focused question; do not proceed to `/tdd`.

## Forbidden

- One invocation per mechanical design stage.
- Treating stage approvals as a substitute for whole-design approval.
- Setting `design_status: approved` without explicit human approval.
- Emitting DB/API artifacts when the matching delivery flag is false.
- Creating duplicate Markdown contracts by default for DB/API details.
- Editing application source or invoking `/tdd`, `/tasksplit`, or `/implement` in this invocation.
- Running whole-repository scans or generating architecture dumps.

## Quality bar

- [ ] Safe impact analysis and related research are batched into one invocation.
- [ ] Product intent and every material decision are confirmed or explicitly left blocking.
- [ ] Repository claims cite inspected paths; no unsupported behavior claims.
- [ ] Acceptance criteria, delivery flags, and conditional contracts agree.
- [ ] Security, failure paths, observability, compatibility, and migration are considered where relevant.
- [ ] Final approval applies to the coherent complete draft; downstream TDD remains blocked until approved.
