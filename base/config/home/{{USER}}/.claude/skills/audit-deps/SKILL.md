---
name: audit-deps
description: Audit dependencies for vulnerabilities, drift, and license issues — produce a prioritized upgrade plan
argument-hint: Optional scope (e.g. "frontend only", "production deps", or path to a specific package)
disable-model-invocation: true
user-invocable: true
---

Dependency audit: $ARGUMENTS

# Audit Dependencies

You are the orchestrator of a dependency audit. The goal is a clear, prioritized list of dependencies to upgrade, replace, or accept-with-rationale — saved as a written audit and converted into trackable issues. Branch and commit conventions follow `git-conventions.md`.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Inventory

**Goal**: Build a complete picture of what we depend on

**Actions**:
1. Launch an `Explore` agent to find all dependency manifests:
   - Node: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - Python: `pyproject.toml`, `requirements*.txt`, `Pipfile.lock`, `uv.lock`, `poetry.lock`
   - Go: `go.mod`, `go.sum`
   - Rust: `Cargo.toml`, `Cargo.lock`
   - Ruby: `Gemfile`, `Gemfile.lock`
   - Java/Kotlin: `pom.xml`, `build.gradle`, `gradle.lockfile`
   - Docker base images: `Dockerfile`, `docker-compose.yml`
   - Terraform / CloudFormation modules and providers
   - GitHub Actions used in workflows (treat actions as deps too)
2. Note for each ecosystem:
   - Direct vs. transitive dep counts
   - Lockfile present and committed?
   - Pinning strategy (exact / caret / tilde / loose)
3. Surface the inventory to the user.

## Phase 2: Branch Setup

**Actions**:
1. Use the **git MCP server** to create or check out `chore/audit-deps-<YYYY-MM-DD>` from `develop` per `git-conventions.md`.

## Phase 3: Assemble the Team

**Actions**:
1. Use `TeamCreate` with `team_name: "audit-deps-<date>"`.
2. Spawn:
   - `name: "ci-cd-engineer"`, `subagent_type: "ci-cd-engineer"` — runs scanners, evaluates upgrade impact on CI
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — assesses CVE severity and exploit context
3. **Conditionally include**:
   - `name: "test-engineer"`, `subagent_type: "test-engineer"` — when the audit is likely to produce risky upgrades (major-version bumps in production paths, or upgrades where regression risk is high) — assesses whether existing test coverage is adequate to catch breakage from the recommended upgrades.

## Phase 4: Scan

**Goal**: Get the data — CVEs, outdated versions, license risks

**Actions**:
1. Assign the scan task to `ci-cd-engineer`. They run platform-appropriate scanners:
   - Node: `npm audit`, `yarn audit`, or `pnpm audit`
   - Python: `pip-audit`, `safety`
   - Go: `govulncheck`
   - Rust: `cargo audit`
   - Ruby: `bundler-audit`
   - Generic: `osv-scanner`, `trivy fs`
   - Container images: `trivy image` or equivalent
   - Secrets in deps: `gitleaks` on transitive code (rare but catches malicious additions)
   - GitHub Actions: review pinned vs. floating versions
2. Collect outputs into a structured form: package, current version, latest, CVE IDs, severity, exploit availability.
3. Run a license scan if licensing matters for this project (e.g. `license-checker` for Node, `pip-licenses` for Python, `go-licenses` for Go).

## Phase 5: Triage

**Goal**: Convert raw scanner output into prioritised actions

**Actions**:
1. Assign triage to `security-engineer`. They classify each finding:
   - **Patch now** — actively exploited or critical CVE in production-path dependency
   - **Patch this sprint** — high-severity CVE, even if mitigation isn't urgent
   - **Plan upgrade** — outdated by major version, or medium CVE
   - **Track only** — minor drift, no CVE
   - **Replace** — unmaintained or single-maintainer dependency in security-sensitive path
   - **Accept** — explicit decision to defer with documented reason and renewal date
2. For each finding, the `security-engineer` notes:
   - Exploit context (is the vulnerable code path actually called from this codebase?)
   - Upgrade effort estimate (patch / minor / major)
   - Breaking-change risk
3. The `ci-cd-engineer` flags any upgrade that would also require CI/runtime changes (Node version bump, Python version bump, etc.).
4. If `test-engineer` is in the team: for each "Patch now" and "Plan upgrade" finding, they audit test coverage on the affected code paths and flag any upgrade where coverage is too thin to catch regressions. Add the test-readiness verdict as a column in the per-finding rows of the audit doc.

## Phase 6: Author the Audit Document

**Goal**: Produce `/docs/audits/deps-<YYYY-MM-DD>.md`

**Actions**:
1. Structure:
   ```
   ## Dependency Audit — YYYY-MM-DD

   **Scope**: [ecosystems audited]
   **Tooling**: [scanners used]

   ### Summary
   - Total deps: direct / transitive
   - Findings by severity: critical / high / medium / low
   - Findings by action: patch now / this sprint / plan / track / replace / accept

   ### Patch now
   | Package | Current | Latest | CVE | Severity | Exploit context | Effort |

   ### Patch this sprint
   ...

   ### Plan upgrade
   ...

   ### Replace
   ...

   ### Accept (with rationale and renewal date)
   ...

   ### Licensing notes
   ...
   ```
2. Have the `technical-writer` polish if the audit will be shared widely (optional — depends on audience).

## Phase 7: Generate Issues

**Goal**: Convert the audit into trackable work

**Actions**:
1. For each "Patch now" and "Patch this sprint" item, create a GitHub issue via the MCP server:
   - Title: `[deps] Upgrade <package> to <version> (CVE-<id>)`
   - Labels: `dependencies`, `security` if CVE-driven, severity label
   - Milestone: appropriate sprint or release
   - Body: link to audit, CVE details, exploit context, upgrade notes
2. For "Replace" items, create a longer-running issue with `tech-debt` label.
3. Add issue numbers back to the audit table.

## Phase 8: Commit & Summary

**Actions**:
1. Commit the audit doc: `docs(audit): dependency audit YYYY-MM-DD`.
2. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
3. Push the branch.
4. Summarize:
   - Counts by action category
   - Highest-priority issues created (issue numbers)
   - Suggested cadence: schedule via `/loop` or calendar to repeat (quarterly is a sensible default)
5. Suggest `/refine` then `/implement` for the highest-priority upgrades.
