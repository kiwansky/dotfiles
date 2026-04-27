---
description: Generate or refresh contributor onboarding docs — CONTRIBUTING.md, dev-setup, testing, code-of-conduct, README onboarding section
argument-hint: Optional scope (e.g. "frontend", "all", or "fix gaps")
---

Onboarding docs: $ARGUMENTS

# Onboarding

You are the orchestrator of a contributor-onboarding documentation pass. The goal is that a new contributor can clone the repo, get to a productive local environment, run tests, and submit a PR — without needing to ask anyone. Branch and commit conventions follow `git-conventions.md`.

## Phase 1: Inventory & Gap Analysis

**Goal**: Identify what onboarding docs already exist and what's missing

**Actions**:
1. Launch an `Explore` agent to inventory:
   - `README.md` — does it have an onboarding section?
   - `CONTRIBUTING.md` — exists? Up to date?
   - `CODE_OF_CONDUCT.md`, `LICENSE`, `SECURITY.md`
   - `/docs/dev/` or similar (setup, architecture-for-newcomers, glossary)
   - Editor configs (`.editorconfig`, `.vscode/settings.json`, `.idea/`)
   - Local-dev tooling (`docker-compose.yml`, devcontainer config, Makefile, justfile, scripts)
   - Test entry points
2. Extract from the codebase the actual setup steps (don't trust outdated docs):
   - Required runtimes and versions (`.nvmrc`, `.python-version`, `go.mod`, `package.json` `engines`)
   - System dependencies (Postgres, Redis, etc.)
   - Environment variables (look at `.env.example`)
   - Build commands (from package.json scripts, Makefile, etc.)
3. Surface the gap list to the user. Confirm scope.

## Phase 2: Branch Setup

**Actions**:
1. Use the **git MCP server** to create or check out `chore/onboarding-<date>` from `develop` per `git-conventions.md`.

## Phase 3: Assemble the Team

**Actions**:
1. Use `TeamCreate` with `team_name: "onboard-<date>"`.
2. Spawn:
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — primary author
3. **Conditionally** spawn for review of their domains:
   - `name: "ci-cd-engineer"`, `subagent_type: "ci-cd-engineer"` — verifies the documented setup actually matches what CI does
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — reviews `SECURITY.md` and any disclosure / vulnerability-reporting docs

## Phase 4: Author the Onboarding Set

**Goal**: Produce a complete, accurate set of onboarding docs

**Actions**:
1. Assign authoring to `technical-writer`. Send the inventory and gap list. Ensure they cover:

   ### `README.md` onboarding section
   - One-paragraph product description
   - Quickstart (5 commands or fewer to get something running)
   - Link to fuller setup in `/docs/dev/setup.md` or `CONTRIBUTING.md`

   ### `CONTRIBUTING.md`
   - How to set up a dev environment (or link to `/docs/dev/setup.md`)
   - How to run tests (link to `/docs/dev/testing.md` if extensive)
   - Branching strategy (reference `git-conventions.md`)
   - Commit conventions (reference `git-conventions.md`)
   - PR process (reference `/review` flow if applicable)
   - Code style (reference linters; don't restate rules)
   - How to file a bug or feature request

   ### `/docs/dev/setup.md`
   - Required system tools and versions
   - Step-by-step: clone → install → configure env → run → verify
   - Common errors and fixes
   - How to run a subset of the system locally

   ### `/docs/dev/testing.md`
   - How to run unit / integration / E2E tests
   - How to run a single test
   - How to run tests with coverage
   - How to debug a flaky test

   ### `SECURITY.md`
   - Supported versions
   - How to report a vulnerability (responsibly disclose)
   - Expected response times

   ### `CODE_OF_CONDUCT.md`
   - Use a recognized template (Contributor Covenant 2.1) unless the project has an established alternative

2. The writer must **verify each command actually works** by running it (or having the user run it) before publishing. Onboarding docs that are wrong are worse than missing.

## Phase 5: Validation

**Goal**: Prove a fresh-clone path works end-to-end

**Actions**:
1. Have `ci-cd-engineer` cross-check the documented setup steps against the CI configuration. Differences are bugs in either the docs or CI.
2. If feasible, run the documented setup in a clean environment (Docker container, fresh worktree, devcontainer) and confirm it produces a running app.
3. Iterate via `SendMessage` until validated.

## Phase 6: Commit & Summary

**Actions**:
1. Commit per file in logical groups: `docs(onboarding): add CONTRIBUTING.md`, `docs(dev): add setup guide`, etc.
2. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
3. Push the branch.
4. Summarize:
   - Files created or updated
   - Validation results
   - Recommended follow-ups (e.g. add a CI job that builds the docs, schedule a quarterly `/onboard` refresh)
5. Suggest opening a PR via `/review` when the user is ready to merge.
