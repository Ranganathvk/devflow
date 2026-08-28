# Architecture principles

## Overview

These principles translate `artifacts/SPEC.md` into durable design constraints for the DevOps AI Agent. They prioritize **customer control**, **explicit human approval for mutations**, **minimal trust of inbound webhooks**, and **safe handling of sensitive operational data** especially at the **LLM boundary**.

## Principles

| # | Principle | Implication | Anti-pattern |
|---|-----------|-------------|--------------|
| P1 | **Gated execution for mutations** | Cluster writes and Git pushes never run from autonomous inference alone; they require an authenticated **approver** confirmation (per change or approved playbook). | Auto-applying patches or merging PRs without an in-product approval step aligned to SPEC. |
| P2 | **Configured scope beats payload authority** | CD payloads only select among **administrator-defined mappings**; arbitrary fields do not directly designate cluster/namespace targets. | Trusting unvalidated webhook fields as live targeting inputs. |
| P3 | **Customer-operated control plane** | Backend, UI, PostgreSQL, and ingress live in the **customer’s** Kubernetes cluster on Helm; workload clusters are separate attachments. | Introducing a shared multi-tenant SaaS control plane in v1. |
| P4 | **Single-replica backend default (v1)** | Orchestration, session affinity, and real-time channels are designed around **one** API replica unless/until HA is explicitly in scope. | Assuming leader election or sticky-load-balancer behavior without documenting it. |
| P5 | **PostgreSQL as system of record** | Users, roles, configuration metadata, runs, and audit history persist in PostgreSQL; chart wires connectivity (managed or in-cluster). | Adding SQLite or ad hoc file stores for core state in v1. |
| P6 | **Secrets minimized at rest and in transit to vendors** | Cluster credentials, Git PATs, and LLM keys stored **encrypted at rest**; prompts to LLM pass through **redaction/minimization** (rules to be specified). | Echoing secret values into chat, audit blobs, or model prompts by default. |
| P7 | **Verification before remediation** | Deployment verification uses **read-only** Kubernetes observation within scope; pass/fail/partial answers cite evidence; fixes remain behind P1. | Conflating “checked version” with silently restarting workloads. |
| P8 | **Git change path via PR by default** | After approval, agent pushes a branch and opens/updates a PR; merge and CD follow normal repo governance. | Bypassing review/merge conventions without explicit product policy exception. |
| P9 | **Vendor-neutral CD integration** | Contract is documented generic JSON + auth; GitHub Actions samples are **examples**, not runtime coupling. | Hard dependency on GitHub-only APIs for activation. |
| P10 | **Observable enough to operate (v1)** | Operators rely on **structured application logs** to stdout/stderr for collection; advanced metrics/tracing deferred. | Requiring Prometheus or OTel as a v1 blocker without SPEC change. |
| P11 | **Explicit deferrals stay deferrals** | OIDC/SSO, HA backends, self-hosted LLM, Docker Compose installs, and SaaS control plane remain **out of v1** unless SPEC is updated. | Sneaking “small” SSO or HA paths into v1 without scope revision. |

## Decision criteria

When choosing between design options:

1. **Does it preserve approver gates for cluster and Git writes?** If not, reject or escalate SPEC change.
2. **Does it keep targeting derived from admin configuration rather than untrusted input?** Prefer mapping tables and presets.
3. **Does it respect customer data boundary** except where SPEC explicitly allows LLM egress? Prefer local aggregation and minimization.
4. **Does it stay within v1 topology** (Helm on K8s, single replica default, PostgreSQL)? Flag HA/metrics/alt-install as later milestones.
5. **Can post-incident review reconstruct approvals and actions?** Prefer append-rich audit events over silent side effects.

## Deferred / out of scope

Aligned with SPEC — not principles violations, but **non-goals for v1** unless SPEC is amended:

- OIDC / SSO and group-to-role mapping (post–v1 milestone).
- Horizontal scaling / HA for backend API workloads.
- Prometheus metrics, OpenTelemetry traces, `/metrics` scraping model.
- SQLite or non-PostgreSQL primary stores.
- Self-hosted LLM inference.
- Docker Compose, single-VM bundles, non-Kubernetes distribution.
- Vendor-hosted multi-tenant SaaS control plane.
- Automated cluster credential rotation UX (operator responsibility v1).

## Review checklist

- [ ] Aligns with SPEC constraints
- [ ] NFR coverage addressed or flagged (logging yes; metrics/tracing deferred; HA deferred)
- [ ] Assumptions labeled (e.g. standard K8s API client patterns for credentials; GitHub reference payloads non-binding)
