---
description: Prepare and execute a release — changelog, version bump, release branch, merge into main, and tag
argument-hint: Version number (e.g. 1.2.0)
---

Release version: $ARGUMENTS

# Release

You are the orchestrator of a release. Coordinate a team to produce a clean release branch, updated changelog, version bump, and a tagged commit in `main` — following GitFlow as defined in `git-conventions.md`.

## Phase 1: Prepare

**Goal**: Confirm the release scope and readiness before spinning up the team

**Actions**:
1. Confirm the version number with the user (semantic versioning: major.minor.patch).
2. Launch an `Explore` agent to list all commits merged to `develop` since the last release tag.
3. Present the release scope to the user. Ask them to confirm all intended work is included and the release is ready to proceed.

## Phase 2: Assemble the Team

**Goal**: Create the release team

**Actions**:
1. Use `TeamCreate` with `team_name: "release-<version>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — owns the changelog.
   - `name: "ci-cd-engineer"`, `subagent_type: "ci-cd-engineer"` — verifies CI is green and the release pipeline is ready.
   - `name: "sre"`, `subagent_type: "sre"` — only if the release contains operational changes (new endpoints, schema migrations, infrastructure updates) — verifies observability, runbooks, and rollback plan.
3. Create tasks in the team task list using `TaskCreate` for: changelog update, release-readiness check, and release branch preparation.

## Phase 3: Release Branch

**Goal**: Create the release branch

**Actions**:
1. Create the release branch from `develop` using the git MCP server. Branch naming follows `git-conventions.md` (i.e. `release/<version>`).
2. Notify the team of the branch name via `SendMessage`.

## Phase 3.5: Release Readiness Check

**Goal**: Confirm CI, observability, and rollback are ready before tagging

**Actions**:
1. Assign the readiness task to `ci-cd-engineer` via `TaskUpdate`. They verify: CI is green on `develop`, the release workflow is wired correctly, and any manual approval gates are unblocked.
2. If `sre` is in the team, assign a parallel task: confirm runbooks exist for new services/endpoints, alerts are wired, and a written rollback plan exists for any infrastructure or schema changes.
3. Surface readiness issues to the user. Do **not** proceed to changelog/merge until the user accepts any open issues.

## Phase 4: Changelog & Version

**Goal**: Update changelog and version references

**Actions**:
1. Assign the changelog task to `technical-writer` via `TaskUpdate`. Send the list of commits and the target version via `SendMessage`.
2. The `technical-writer` will: update `CHANGELOG.md` with all changes since the last release grouped by type, and update any version references in code, manifests, or docs.
3. When the agent reports back, present the changelog to the user for review and approval.
4. Iterate via `SendMessage` if adjustments are needed.
5. Once approved, commit: `chore(release): prepare release <version>`.

## Phase 5: Shutdown the Team

**Goal**: Clean up the team before the merge steps

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.

## Phase 6: Merge & Tag

**Goal**: Merge into `main` and `develop`, then tag — confirm with user before each step

**Actions**:
1. Confirm with the user before merging.
2. Merge `release/<version>` into `main` using the git MCP server.
3. Tag the commit on `main` with `<version>` using the git MCP server.
4. Merge `release/<version>` back into `develop`.
5. Summarize the release and confirm the tag.
