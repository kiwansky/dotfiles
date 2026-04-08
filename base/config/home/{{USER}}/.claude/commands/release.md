---
description: Prepare and execute a release — changelog, version bump, release branch, merge into main, and tag
argument-hint: Version number (e.g. 1.2.0)
---

Release version: $ARGUMENTS

# Release

You are the orchestrator of a release. Coordinate a team to produce a clean release branch, updated changelog, version bump, and a tagged commit in `main` — following GitFlow.

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
   - `name: "technical-writer"`, `subagent_type: "technical-writer"`
3. Create tasks in the team task list using `TaskCreate` for: changelog update and release branch preparation.

## Phase 3: Release Branch

**Goal**: Create the release branch

**Actions**:
1. Create the release branch `release/<version>` from `develop` using the git MCP server.
2. Notify `technical-writer` of the branch name via `SendMessage`.

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
1. Send `{type: "shutdown_request"}` via `SendMessage` to `technical-writer`.
2. Call `TeamDelete` once the teammate has shut down.

## Phase 6: Merge & Tag

**Goal**: Merge into `main` and `develop`, then tag — confirm with user before each step

**Actions**:
1. Confirm with the user before merging.
2. Merge `release/<version>` into `main` using the git MCP server.
3. Tag the commit on `main` with `<version>` using the git MCP server.
4. Merge `release/<version>` back into `develop`.
5. Summarize the release and confirm the tag.
