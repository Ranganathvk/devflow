---
name: security-review
description: >-
  Security review of uncommitted changes (default) or the current branch, in the
  style of Anthropic /security-review and Cursor /review-security. Combines a
  high-confidence semantic pass with any project-local linters or SAST already
  present (CodeQL, ESLint, Ruff, Bandit, Semgrep, gitleaks). Invoke as
  /security-review, /security-review branch, or when the human asks to scan
  pending changes for vulnerabilities, injection, auth gaps, or secrets.
---

# /security-review — Uncommitted-change security scan

## Purpose

Catch **newly introduced, high-confidence** security issues before commit. Complements — does not replace — CI SAST (CodeQL, Semgrep) and linters.

Related (do not copy as-is):

- Anthropic [claude-code-security-review](https://github.com/anthropics/claude-code-security-review) `/security-review` (branch / PR diff)
- Cursor built-in `/review-security` (Security Review subagent; default **branch** changes)

This skill is the Devflow counterpart: **uncommitted** by default, file-backed, multi-agent (do **not** require Cursor's subagent).

`/review` remains the optional task checklist. This skill is security-only and does **not** gate `/implement`.

## When to invoke

- `/security-review` — staged + unstaged + untracked vs `HEAD`.
- `/security-review branch` — commits + dirty tree vs merge-base with the default remote branch (Anthropic / Cursor default).
- `/security-review <TASK_ID>` — same uncommitted scope; stamp `task_id` on the contract when a queue id is known.
- Natural language: "security review", "scan for vulns", "CodeQL-style check", "review my uncommitted changes for secrets".
- Do **not** invoke for general quality / style review (`/review` or a third-party review skill).
- Do **not** invent a whole-repo audit unless the human explicitly asks.

## Path resolution

All workflow paths use **`{context_dir}/`**. Resolve per `core/AGENTS.md` (`DEVFLOW_CONTEXT_DIR` → `devflow.context.yaml` → default `artifacts`).

## Inputs

- **Required:** Git working tree (repo root).
- **Required:** Change set — resolve in workflow step 1. Never treat chat as the diff.
- **Optional:** `{context_dir}/SPEC.md` — only **Human code ownership** / compliance notes if present.
- **Optional:** Project tool configs (`.github/workflows/*codeql*`, `codeql*.yml`, `ruff.toml`, `eslint.config.*`, `.semgrep.yml`, `.pre-commit-config.yaml`, `pyproject.toml`).
- **Forbidden:** Whole-repo history; generating exploit PoCs or payloads; installing scanners.

## Workflow

1. **Resolve scope**
   - Default / omitted / `uncommitted`:
     - `git status --porcelain`
     - `git diff HEAD` (staged + unstaged)
     - `git ls-files --others --exclude-standard` — **read** each untracked source file (skip binaries, lockfiles, generated assets)
   - `branch`: `git diff --name-only` and `git diff --merge-base` against `origin/HEAD` (or `main` / `master` if no `origin/HEAD`)
   - Empty change set → **stop**. One sentence: nothing to review.

2. **Tool pass (optional, cheap, already-present only)**
   - Detect tools from configs + `PATH`. Run **scoped to changed files** when a one-shot command exists.
   - Candidates: Ruff, ESLint/Biome, Bandit, Semgrep, gitleaks / detect-secrets, project `lint` script.
   - **CodeQL:** run only if the `codeql` CLI is on `PATH` **and** a pre-existing database is present. Do **not** `codeql database create`.
   - Never install packages or CLIs. Skip missing tools; record `tools_skipped`.
   - Treat tool output as **signals** to confirm or dismiss — not automatic findings.

3. **Semantic pass** (Anthropic methodology)
   - Context: existing sanitization, auth, and validation patterns in the repo (search only files that the diff touches or clearly calls).
   - Compare new code to those patterns. Trace user input → sinks.
   - Categories: injection (SQL / command / template / NoSQL / XXE / path), authn/authz bypass, session/JWT flaws, XSS (unsafe sinks only), insecure deserialization / `eval`, new hardcoded secrets in the **diff**, weak crypto, sensitive data in logs.
   - Report only issues **introduced by this change set**, confidence **≥ 0.8**, HIGH or MEDIUM. See [references/filters.md](references/filters.md).
   - Describe impact in prose. **No exploit code, PoCs, or payloads.**

4. **Write** `{context_dir}/SECURITY_REVIEW.md` (replace, ≤ **~120** lines) and `{context_dir}/SECURITY_REVIEW.contract.yaml`.
5. **Chat:** compact table — Severity | Location (`file:line`) | Finding — highest severity first. Then artifact paths. Do **not** fix unless the human asks.

## Output artifacts

| Path | Change | Notes |
|------|--------|-------|
| `{context_dir}/SECURITY_REVIEW.md` | Created or replaced | Human report |
| `{context_dir}/SECURITY_REVIEW.contract.yaml` | Created or replaced | Small YAML |

No other files written or edited. Do **not** change task `status`.

## `{context_dir}/SECURITY_REVIEW.md` shape

```markdown
# Security review

- Scope: uncommitted | branch
- Files: <n>
- Tools run: <list or none>
- Tools skipped: <list or none>

| Severity | Location | Category | Finding |
|----------|----------|----------|---------|
| HIGH | path:line | sql_injection | … |

## Notes
<one short paragraph, or "No high-confidence findings.">
```

## `{context_dir}/SECURITY_REVIEW.contract.yaml` shape

```yaml
contract_version: "1"
artifact: security_review
workflow_profile: devflow
scope: uncommitted  # or branch
task_id: null       # set if /security-review <TASK_ID>
reviewed_at: "2026-01-01"
files_reviewed: []
tools_run: []
tools_skipped: []
findings: []        # {severity, confidence, category, location, summary}
finding_count: 0
```

Reference schema: `core/contracts/security_review.contract.yaml`.

## Context budget

- Diff/stat + untracked source files in the change set.
- Surrounding callers/callees only as needed to confirm a sink.
- Do not load full HLD, TDD, or unrelated features.

## Failure handling

- **No diff / no untracked source** → stop; do not write empty praise.
- **Tool missing or fails** → skip; continue semantic pass; list in `tools_skipped`.
- **Huge diff (> ~40 files or clearly multi-feature)** → still review, but say the scan is coarse; suggest `/security-review` again on a smaller set or `branch` after split.

## Forbidden

- Editing application source.
- Writing exploits, PoCs, or attack scripts.
- Reporting pre-existing issues outside the change set.
- Installing CodeQL / Semgrep / linters.
- Whole-repo `codeql database create`.
- Style, tests-missing, or architecture nits (use `/review`).
- Blocking the implement queue.

## Quality bar

- [ ] Change set resolved from git, not chat.
- [ ] Filters applied; no speculative / DOS / docs-only noise.
- [ ] Artifact pair exists and matches the chat table.
- [ ] Chat names next **optional** step (fix in editor, `/review`, or stop).
