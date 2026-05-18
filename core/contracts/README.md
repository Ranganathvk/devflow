# core/contracts/

Canonical contract **schemas** and reference shapes used by framework skills and tooling.

## Scope (from `AI_CONTEXT/SPEC.md`)

- This folder holds **framework-owned** definitions: schemas, reference shapes, and example skeletons that downstream skills consume.
- It is **not** the same as the per-project emitted artifacts produced by workflows (for example `AUTH.contract.yaml`, `SYSTEM_HLD.contract.yaml`). Those workflow outputs land in the consumer repo under paths defined by the emitting skill — typically inside `AI_CONTEXT/` or a documented subfolder.

## Stability

Contract schemas are stability-critical: downstream automation depends on them, and churn here forces churn across every consuming skill. Treat schema changes as breaking unless explicitly additive.

Schemas will be added in later increments per the SPEC bootstrap sequence.
