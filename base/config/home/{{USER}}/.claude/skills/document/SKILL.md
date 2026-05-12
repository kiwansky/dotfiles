---
name: document
description: Audit and update project documentation — README, /docs/*, API docs, ADRs — for accuracy, consistency, and Diátaxis coverage
argument-hint: Optional scope (e.g. "README", "architecture", "API docs", or issue number)
disable-model-invocation: true
user-invocable: true
---

Update documentation: $ARGUMENTS

# Documentation

You are the orchestrator of a documentation review and update pass. The goal is documentation that is accurate, consistent, useful, and structured along the **Diátaxis** dimensions (tutorial / how-to / reference / explanation). Branch and commit conventions follow `git-conventions.md`.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Inventory & Audit

**Goal**: Build a clear picture of what exists, what's missing, and what's stale

**Actions**:
1. Launch an `Explore` agent to inventory documentation:
   - Top-level: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `CODE_OF_CONDUCT.md`
   - `/docs/` tree (architecture, ADRs, design, runbooks, postmortems, security, accessibility, data, etc.)
   - `/api/` (OpenAPI specs, schema definitions)
   - Inline code documentation (godoc, JSDoc, docstrings) — sample, not exhaustive
   - Generated docs (build output, Storybook, mkdocs, Sphinx, etc.)
2. Spawn a `technical-writer` via `Agent`. Send the inventory and ask for an audit covering:
   - **Accuracy**: claims that don't match the current code
   - **Coverage**: missing categories — installation, usage, contributing, architecture, deployment, troubleshooting, security, accessibility, observability
   - **Consistency**: terminology, voice, formatting drift across files
   - **Structure**: does each doc fit a Diátaxis category, or is it a hybrid muddle?
   - **Discoverability**: is the README a reliable index? Are docs easy to find from where they're needed?
3. The writer produces a prioritized findings list (Critical / Major / Minor) with file references.
4. Present findings to the user. Agree on which findings are in-scope for this pass.

## Phase 2: Branch Setup

**Actions**:
1. Determine the branch (per `git-conventions.md`):
   - Tied to an issue → `feature/<issue-id>-<slug>` or relevant existing feature branch
   - Standalone documentation pass → `chore/docs-<slug>` from `develop`
2. Use the **git MCP server** to create or check out the branch.

## Phase 3: Update

**Goal**: Fix in-scope findings

**Actions**:
1. Assign the update task to `technical-writer` via `TaskUpdate`. Send the agreed findings list.
2. The writer will:
   - Update existing docs in place where appropriate
   - Move docs into the right Diátaxis bucket if structurally wrong
   - Create missing docs (README sections, runbooks, ADRs, etc.)
   - Maintain a single source of truth — link rather than duplicate
   - Update the README index if structure changes
3. For domain-specific updates, bring in the relevant specialist via `Agent`:
   - **Architecture / ADR** updates: `software-architect` reviews
   - **API reference** updates: `api-designer` reviews
   - **Security docs / threat models**: `security-engineer` reviews
   - **Runbooks / SLOs / observability docs**: `site-reliability-engineer` reviews
   - **Accessibility patterns**: `accessibility-specialist` reviews
   - **Data / schema docs**: `database-engineer` reviews
4. Present changes to the user for review. Iterate via `SendMessage` as needed.

## Phase 4: Consistency Pass

**Goal**: Make sure the corpus reads like one product, not ten

**Actions**:
1. The `technical-writer` does a final pass:
   - Terminology check (use a single term per concept)
   - Voice and tense consistency
   - Heading levels and formatting consistency
   - Cross-link verification (no broken links, no orphaned docs)
   - Code block language tags applied consistently
2. Confirm with the user.

## Phase 5: Commit & Summary

**Actions**:
1. Commit in logical groups (per topic) following conventional-commit format: `docs(<scope>): <description> [#<issue-id>]`. Examples: `docs(readme): add observability section`, `docs(adr): record decision to drop service-X`.
2. Send `{type: "shutdown_request"}` to all teammates and call `TeamDelete` if a team was created.
3. Summarize what changed, by category, and suggest follow-ups (e.g. `/onboard` if contributor docs are now ready, `/release` if these belong in the next changelog entry).
