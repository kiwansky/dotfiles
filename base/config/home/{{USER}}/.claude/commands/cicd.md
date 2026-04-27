---
description: Set up or update the CI/CD pipeline — assess current state, design, implement, and validate
argument-hint: Optional scope (e.g. "add Docker build", "set up canary deploy", "fix flaky integration job")
---

CI/CD work: $ARGUMENTS

# CI/CD Pipeline

You are the orchestrator of CI/CD pipeline work. The goal is a reliable, well-designed pipeline that enforces quality gates, automates delivery, and stays maintainable. Branch and commit conventions follow `git-conventions.md`.

## Phase 1: Assess Current State

**Goal**: Understand the existing pipeline and what needs to change

**Actions**:
1. Launch an `Explore` agent to inventory existing CI/CD configuration:
   - Workflow files (`.github/workflows/`, `Jenkinsfile`, `gitlab-ci.yml`, `.circleci/config.yml`, `azure-pipelines.yml`)
   - Build/test entry points (Makefile, package.json scripts, Bazel, etc.)
   - Deployment manifests (Dockerfile, Helm charts, Kustomize, Terraform, serverless configs)
   - Quality-gate tools (linters, formatters, coverage tools, scanners)
   - Existing secrets/auth setup (OIDC, secret manager, environments)
2. Run a quick health check using the Explore findings:
   - Are pipelines structured (build → test → scan → deploy) or ad-hoc?
   - Are there obvious smells: hardcoded secrets, broad permissions, no caching, no parallelization, no failure notifications?
   - Are there flaky jobs visible from recent runs?
3. Ask the user the right questions only — skip what you can infer:
   - Deployment target (cloud provider, K8s, serverless, on-prem)
   - Required quality gates (test types, coverage threshold, lint, type-check, SBOM, security scan)
   - Environments (dev / staging / prod) and promotion model
   - Specific pain points or requirements driving this change
   - Constraints: budget, runner self-hosted vs. managed, compliance/SOC2 needs
4. Summarize current state, gaps, and proposed scope of work to the user. Confirm before proceeding.

## Phase 2: Branch Setup

**Goal**: Work on the right branch

**Actions**:
1. Determine the branch type (per `git-conventions.md`):
   - Issue-driven change → `feature/<issue-id>-<slug>` or `bugfix/<issue-id>-<slug>` from `develop`.
   - Standalone CI/CD work without an issue → `chore/cicd-<slug>` from `develop`.
2. Use the **git MCP server** to create or check out the branch.

## Phase 3: Design

**Goal**: Decide the pipeline shape before changing files

**Actions**:
1. Launch a `ci-cd-engineer` agent. Send the assessment, gaps, and constraints via `SendMessage`.
2. The `ci-cd-engineer` will produce a written design covering:
   - Stages and their order (build → test → scan → package → deploy)
   - Triggers (push, PR, tag, schedule, manual)
   - Caching strategy (deps, Docker layers, test results)
   - Parallelization opportunities and dependencies
   - Quality gates and pass/fail criteria
   - Secret-handling pattern (OIDC where supported, secret manager otherwise)
   - Deployment strategy (rolling / blue-green / canary)
   - Rollback path
   - Notifications and observability of the pipeline itself
3. **Conditionally bring in** `security-engineer` via `Agent` if the pipeline touches secrets, signing, or supply-chain integrity (SBOM, signed artifacts) — they review the design before implementation.
4. Present the design to the user. Confirm before implementation.

## Phase 4: Implement

**Goal**: Apply the agreed design

**Actions**:
1. The `ci-cd-engineer` writes the configuration files following the design. Constraints:
   - Least-privilege credentials. No hardcoded secrets.
   - Idempotent and re-runnable jobs.
   - Meaningful stage and job names.
   - Timeouts on every step.
   - Artifact versioning traceable to commits.
2. Block PRs that fail quality gates (branch protection rules + required checks).
3. Where applicable, add a job that runs the full pipeline against a sample PR to validate end-to-end before merging the change itself.

## Phase 5: Validate

**Goal**: Prove the pipeline works before merging

**Actions**:
1. Push the branch and trigger the pipeline (push, PR, or workflow_dispatch).
2. Confirm:
   - All jobs run as designed
   - Quality gates fire correctly on a known-bad input (intentionally break a test or lint locally)
   - Caching reduces build time on second run
   - Failure notifications reach the intended channel
3. If anything fails, iterate via `SendMessage` to `ci-cd-engineer` until green.

## Phase 6: Commit & Document

**Goal**: Land the change cleanly with the necessary docs

**Actions**:
1. Commit using the conventional format: `ci: <description> [#<issue-id>]` (or `chore(cicd): <description>` if no issue).
2. Update or create `/docs/cicd/README.md` with: pipeline overview, where to find each workflow, how to run it locally, troubleshooting common failures.
3. If new secrets were added, document the rotation procedure (without leaking the secret values).

## Phase 7: Shutdown & Summary

**Actions**:
1. Send `{type: "shutdown_request"}` to the `ci-cd-engineer` (and `security-engineer` if used). Call `TeamDelete` if a team was created.
2. Summarize: what changed, what was validated, where the docs live, suggested next steps (e.g. `/audit-deps` for dependency scanning, `/document` for broader doc updates).
