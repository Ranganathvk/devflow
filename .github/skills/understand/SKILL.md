---
name: understand
description: >-
  Bounded brownfield investigation before design. Performs several targeted read-only searches
  per invocation, persists one feature-plan contract, and asks only for decisions that require
  human knowledge. Invoke /understand, /understand FEATURE, or /understand "description".
---

# /understand [<FEATURE> | "description"]

## Purpose

Gather only the codebase context needed to design a bounded change. Investigate the change path, cite repository evidence, record meaningful risks and unknowns, then stop for human input or approval. This is not a whole-repository survey.

Downstream: `/design <FEATURE>`.

## Invocation

- `/understand`: ask what change to investigate only when no intent is available from the message or SPEC.
- `/understand <FEATURE>`: resume from the existing feature-plan contract.
- `/understand "add OTP login"`: derive a proposed feature ID and investigate the supplied intent.
- Use for brownfield changes. For empty-spec greenfield work, use `/grillme` or `/design` as appropriate.
- Never implement or chain `/design`, `/tdd`, `/tasksplit`, or `/implement` in this invocation.

## Inputs and bounds

- Required: consumer repository access for targeted searches, if available.
- Optional: `artifacts/SPEC.md` and `PROJECT_STATE.md`.
- Resume state: `artifacts/<FEATURE>_PLAN.contract.yaml`; read it first.
- Read only files relevant to the feature path. Normally inspect no more than 12 source/config/test files in one invocation; expand only with a concrete reason.
- Do not dump the repository tree, scan every module, generate architecture docs/knowledge graphs, edit application source, or invent paths.

## Operating model

**One invocation may perform multiple bounded read-only investigation steps.** The unit of control is a meaningful decision boundary, not an individual search.

1. **Assess:** read the existing plan contract (if any), SPEC, and relevant state.
2. **Investigate:** run several focused searches and inspect relevant files. Follow entry points to the owning component, one or more analogous patterns, critical dependencies, and applicable tests/configuration.
3. **Synthesize:** record evidence-backed findings, scope, constraints, risks, and unresolved questions.
4. **Persist:** update the feature-plan contract once the investigation batch has meaningful results or before stopping.
5. **Transition:** ask one focused human question and stop if blocked; otherwise continue investigation if a material gap remains; when ready, present the summary and request approval.

Do not stop merely because one search or a mechanical category is complete. Do stop when the next step requires product intent, a business rule, a material scope/architecture decision, human-provided repository evidence, or approval.

## Investigation strategy

Prioritize in this order, but cover related items together when the same evidence answers several questions:

1. **Intent:** problem and business goal confirmed by the human or authoritative SPEC.
2. **Entry path:** handler, endpoint, job, CLI, event, or caller that initiates the change.
3. **Ownership:** responsible module/service and its evidence path.
4. **Scope:** explicit in-scope and out-of-scope boundaries.
5. **Dependencies:** important integrations, persistence, configuration, and call paths.
6. **Existing patterns:** a comparable implementation, or a documented search that found none.
7. **Constraints and risks:** compatibility, security, performance, migration, deployment, operational failure modes.
8. **Open questions:** resolve blocking uncertainties; retain non-blocking questions with explicit rationale.

Use the cheapest search that can answer the question. Search symbols, route names, types, configuration keys, imports/callers, tests, and migration names. Inspect the smallest useful file set and cite paths for every repository-derived claim. A path is evidence of location, not proof that a behavior works; inspect the relevant implementation/test where needed.

If tools are available, execute searches and inspect files directly. If repo access is unavailable, emit one compact search request for the human to run and stop. Never claim a search was performed when it was not.

## Human questions and approvals

- Ask only when the answer requires human knowledge or changes product behavior, scope, compatibility policy, or another material decision.
- Ask **one focused question at a time**, with a recommended answer when defensible.
- Do not ask the human to locate code that the agent can search itself.
- If a human answer is required, persist current findings and the question, then stop. Resume with `/understand <FEATURE>`.
- When investigation is ready, summarize the proposed intent, scope, key evidence, patterns, constraints, risks, and non-blocking unknowns in chat. Ask for explicit approval.
- Set `ready_for_design: true` and `understand_status: ready` only after explicit human approval. Do not treat silence or a generated report as approval.

## Ready-for-design criteria

All must hold before asking for final approval:

- Problem statement and business goal are human-confirmed or grounded in the authoritative SPEC.
- Domain and responsible components are evidence-backed.
- In-scope and out-of-scope boundaries are explicit.
- Each material in-scope component has an evidence path, or a clearly identified blocking unknown.
- At least one analogous pattern is cited, or a targeted search and its “none found” result are recorded.
- Material dependencies, constraints, and risks are captured, or their absence is explicitly justified.
- No unresolved blocking questions remain.

A failed or empty search is not evidence that a component does not exist. Record the attempted search and try a different symbol/entry path before concluding “none found.”

## Durable output

**Default: one file** in the consumer repository: `artifacts/<FEATURE>_PLAN.contract.yaml`. This contract is the resumable investigation state and the handoff consumed by `/design`.

Do not create `UNDERSTAND.contract.yaml`: it only duplicated pointers to the feature plan. Do not create `<FEATURE>_PLAN.md` by default. Create that Markdown view only when the human asks for it or the evidence/rationale is substantial enough that a separate review document materially helps. If created, derive it from the contract and avoid independently maintained copies of facts.

### Feature-plan contract shape

```yaml
contract_version: "1"
artifact: feature_plan
workflow_profile: devflow
feature_id: "<FEATURE>"
title: "<short title>"
understand_status: draft # draft | ready
updated_at: "YYYY-MM-DD"
ready_for_design: false

intent:
  problem_statement: "<human-confirmed or SPEC-grounded>"
  business_goal: "<human-confirmed or SPEC-grounded>"
summary: "<concise current understanding>"

scope:
  in_scope: []
  out_of_scope: []

domains: []
components: []
evidence_paths:
  # - path: "src/..."
  #   role: "entry | service | repository | config | test | migration | other"
  #   claim: "What this path demonstrates"

patterns:
  # - id: PAT-001
  #   summary: "Reusable behavior"
  #   evidence_paths: ["src/..."]

dependencies: []
constraints:
  # - id: CON-001
  #   category: compat | security | performance | deploy | migration | other
  #   summary: "Constraint"
  #   blocking: false
risks: []
open_questions:
  # - id: Q-001
  #   question: "Question"
  #   blocking: true
  #   why_blocking: "Decision affected"

assumptions: []
searches:
  # - query: "symbol or search intent"
  #   result: "What was found, including none found"
  #   evidence_paths: ["src/..."]

approval:
  status: pending # pending | approved
  approved_at: null
  notes: ""
downstream_skills:
  - design
```

## Failure handling

- Missing or vague intent: ask one focused question; do not invent product behavior.
- No repository access: persist known intent, provide one targeted search request, and stop.
- Search yields nothing: record the query/result and try a different entry path before declaring no pattern found.
- Conflicting evidence: record the conflict and ask only if it changes the next safe step.
- Existing approved plan with changed requirements: mark approval pending and explain which facts changed.

## Forbidden

- Whole-repository summaries, unbounded scans, or architecture documentation dumps.
- Requiring a separate user turn for each search.
- Creating a Markdown plan and rollup contract by default.
- Claiming `ready_for_design` without explicit human approval.
- Implementing code or invoking downstream skills.

## Quality bar

- [ ] Several safe searches are batched when they answer related questions.
- [ ] Every codebase claim has a real evidence path.
- [ ] The investigation is bounded and focused on the requested change.
- [ ] Human questions are necessary, focused, and not answerable by repository search.
- [ ] One durable contract is updated before stopping.
- [ ] Approval and blocking unknowns are represented explicitly.
