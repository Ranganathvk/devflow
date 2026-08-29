# False-positive filters

Adapted from Anthropic [`/security-review`](https://github.com/anthropics/claude-code-security-review/blob/main/.claude/commands/security-review.md). Apply after the semantic pass. Drop any finding that matches.

## Hard exclusions

1. Denial of service, rate limiting, resource exhaustion, ReDoS, memory/CPU exhaustion.
2. Secrets already on disk and otherwise gated (env files gitignored). **Do** report **new** hardcoded secrets/tokens in the change set.
3. Missing hardening, missing audit logs, missing rate limits.
4. Theoretical race conditions or timing attacks.
5. Outdated third-party libraries (dependency CVE scanners own this).
6. Memory-safety issues in memory-safe languages (Rust, Go, Java, C#, managed JS/Python).
7. Files that are only tests, fixtures, or docs (including markdown).
8. Log spoofing; unsanitized user text in logs is not a finding unless it leaks secrets or PII.
9. SSRF that only controls the URL **path** (host/protocol must be attacker-controlled).
10. User content in AI prompts; regex injection.
11. Client-side JS/TS missing auth checks (server must enforce).
12. Env vars and CLI flags treated as trusted.
13. UUIDs treated as unguessable.
14. Open redirects, tabnabbing, XS-Leaks, prototype pollution — only if extremely high confidence.
15. React/Angular XSS unless `dangerouslySetInnerHTML`, `bypassSecurityTrustHtml`, or equivalent unsafe sink.
16. GitHub Actions / notebooks — only with a concrete untrusted-input path.
17. Command injection in shell scripts unless untrusted input clearly reaches the shell.

## Confidence

- Report only **≥ 0.8** (clear pattern + known exploit method).
- MEDIUM only when the issue is obvious and concrete.
- Prefer missing a theoretical issue over a noisy report.

## Signal check (each remaining finding)

1. Concrete attack path from this diff?
2. Real risk vs style / defense-in-depth?
3. Specific `file:line` and a fix the human can apply?
4. Would a security engineer raise this on the PR?
