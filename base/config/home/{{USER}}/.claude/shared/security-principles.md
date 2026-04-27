# Security Principles

Practical security guidance for software engineers, code reviewers, and the dedicated `security-engineer` agent. Apply proportionally to risk: a payments path needs every control; a CLI dev-tool does not.

## Threat Modelling Heuristic — STRIDE

For any non-trivial change, ask whether it enables:

- **S**poofing — can an attacker pretend to be someone they aren't?
- **T**ampering — can an attacker modify data in transit or at rest?
- **R**epudiation — can an action be performed without an audit trail?
- **I**nformation disclosure — can secrets, PII, or business data leak?
- **D**enial of service — can an attacker exhaust resources?
- **E**levation of privilege — can a low-privilege user do high-privilege things?

If yes to any, document the mitigation in the design.

## OWASP Top 10 (2021) — Always Check

1. **Broken access control** — every endpoint must check authorisation, not just authentication. Default-deny.
2. **Cryptographic failures** — never invent crypto. Use platform primitives. TLS in transit, AES-GCM or libsodium at rest.
3. **Injection** — parametrize SQL, escape shell, validate and encode for context. Never concatenate user input into queries or commands.
4. **Insecure design** — threat-model first, code second.
5. **Security misconfiguration** — secure defaults, minimal surface area, latest patches.
6. **Vulnerable / outdated components** — track CVEs, run `/audit-deps` regularly.
7. **Identification and authentication failures** — proper session management, MFA where appropriate, rate-limit auth endpoints.
8. **Software and data integrity failures** — signed artifacts, integrity checks, no untrusted deserialization.
9. **Security logging and monitoring failures** — log auth events, log sensitive actions, alert on anomalies.
10. **Server-side request forgery (SSRF)** — validate URLs, allowlist destinations, block metadata endpoints.

## Secrets

- **Never commit secrets to source control.** If one slips in, rotate immediately — `git history rewrite` does not invalidate the leak.
- Use the platform's secret manager (AWS Secrets Manager, GCP Secret Manager, Vault, sealed-secrets).
- `.env.example` files: yes. `.env` files with real values: never.
- Pre-commit hooks (e.g. `gitleaks`, `trufflehog`) should block commits with secrets.

## Authentication & Authorization

- Authentication answers "who are you?" Authorization answers "are you allowed?"
- **Authorize at the resource boundary, not the route.** Check every access against the actor and the resource together.
- Prefer short-lived tokens with refresh over long-lived sessions.
- Token storage: HttpOnly + Secure cookies for browsers; OS keychain for native apps; never in localStorage.
- Time-constant comparisons for tokens, signatures, and password hashes.

## Input Validation

- Validate at the system boundary (untrusted input enters the system).
- Validate **type, range, format, and length**.
- Allowlist > denylist when feasible.
- Output encoding is context-specific: HTML, attribute, JS, URL, CSS, SQL — each has its own rules.

## Data Protection

- Classify data: public / internal / confidential / restricted.
- Restricted data (PII, payment, health) gets encryption at rest, encryption in transit, audit logging, and minimal access.
- Pseudonymize or anonymize for analytics.
- **Don't log PII or secrets.** Redact at the logger, not at the call site.

## Dependencies

- Pin dependency versions; use lockfiles.
- Run vulnerability scanners (Snyk, Dependabot, `pip-audit`, `npm audit`, `govulncheck`) in CI.
- Patch criticals within hours, highs within days.
- Avoid abandoned or single-maintainer dependencies for security-sensitive code.
- Verify integrity of third-party artifacts (signatures, checksums, SBOM).

## Cryptography

- Use vetted libraries (libsodium, BoringSSL, platform crypto APIs).
- Never roll your own crypto, hash function, or random source.
- For passwords: argon2id (preferred) or bcrypt. Never MD5, SHA-1, or unsalted SHA-256.
- Use cryptographically-secure RNG (`/dev/urandom`, `crypto.randomBytes`, etc.) for tokens and IDs — never `rand()` or `Math.random()`.

## Logging & Monitoring

- Log security-relevant events: auth success/failure, permission denials, admin actions, config changes.
- Include correlation IDs to trace a request across services.
- Alert on anomalies: unusual auth patterns, brute-force, sudden privilege escalation.
- Retain logs long enough to investigate incidents (often 90+ days).

## Code Review Red Flags

- String concatenation building SQL, shell commands, or HTML
- `eval`, `exec`, `pickle.loads`, `yaml.load` (use `yaml.safe_load`), `Object.fromEntries(req.body)` patterns
- Disabled TLS verification (`verify=False`, `rejectUnauthorized: false`)
- Hardcoded secrets, API keys, connection strings
- Custom authentication or authorization logic where a framework primitive exists
- Password or token comparisons with `==` instead of constant-time compare
- Untrusted deserialization
- File path manipulation accepting user input without canonicalization
- Open redirects (user-controlled `Location` header)
- Missing CSRF protection on state-changing endpoints
- Missing rate limits on auth, password reset, or expensive endpoints

## Quick Quality Bar for Security-Sensitive Code

- [ ] Threat-modelled with STRIDE
- [ ] Inputs validated at the boundary
- [ ] Outputs encoded for their context
- [ ] Secrets in a secret manager, not in code
- [ ] Authentication and authorization both enforced
- [ ] Cryptography uses platform primitives
- [ ] Logs cover security-relevant events without leaking secrets
- [ ] Dependencies are scanned and current
- [ ] Tests cover at least one negative authorization case
