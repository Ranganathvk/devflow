# core/hooks/

Canonical hook scripts and manifests.

## Allowed responsibilities (from `artifacts/SPEC.md`)

Hooks may **only**:

- Summarize.
- Generate contracts.
- Checkpoint state.
- Trim context.

Hooks **must not** bloat context, inject unbounded narrative, or duplicate skill logic.

## Derived registration

Agent-specific registration paths (for example `.cursor/hooks/hooks.json`) are materialized by the installer; see `adapters/<agent>/` for each tool's expected layout.

Concrete hook scripts will land in later increments.
