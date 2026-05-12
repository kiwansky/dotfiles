---
name: implement
description: Implement an issue from an approved implementation plan — assemble the team, verify the branch, write code. Requires a plan from /plan-implementation.
argument-hint: Issue number or URL
disable-model-invocation: true
user-invocable: true
---

Implement: $ARGUMENTS

# Implementation

You are the orchestrator of an implementation session. Coordinate one or more software engineers to deliver working code that fulfills the architecture and acceptance criteria, **following an approved implementation plan produced by `/plan-implementation`**. When tests should be written alongside the implementation (TDD, regression-prone areas, thin existing coverage), include a `test-engineer` on the team; otherwise a focused testing pass via `/test` follows implementation.

If no approved plan exists for this issue, stop and instruct the user to run `/plan-implementation <issue-id>` first.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Verify the Plan

**Goal**: Confirm an approved plan exists and is still valid

**Actions**:
1. Locate the implementation plan at `/docs/implementation-plans/<issue-id>.md` on the feature branch (`feature/<issue-id>-<slug>`).
2. If the file is missing or marked `Status: Draft`, **stop**. Instruct the user to run `/plan-implementation <issue-id>` first, or to approve the existing draft.
3. Read the plan and the linked design artifacts. Re-read the issue to confirm nothing has changed that invalidates the plan.
4. Present a one-paragraph summary of the plan (scope, work-stream split, recommended team) to the user and confirm it's still the intent before assembling the team. If the user wants material changes, return them to `/plan-implementation`.

## Phase 2: Assemble the Team

**Goal**: Create the implementation team per the plan's recommended composition

**Actions**:
1. Use `TeamCreate` with `team_name: "implement-<issue-id>"`.
2. Spawn one `software-engineer` per area identified in the plan, each primed to its specific scope. Use descriptive names so messages are routable. Examples:
   - Single-stream work: `name: "software-engineer"`, `subagent_type: "software-engineer"`.
   - Frontend + backend split: `name: "software-engineer-frontend"` and `name: "software-engineer-backend"`, both `subagent_type: "software-engineer"`.
   - Service split: `name: "software-engineer-<service>"` per service, all `subagent_type: "software-engineer"`.
3. **Include specialists per the plan's recommendation**:
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — for schema changes, migrations, or query work.
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — for auth, crypto, secrets, or other security-sensitive paths.
   - `name: "accessibility-specialist"`, `subagent_type: "accessibility-specialist"` — for non-trivial UI work, especially custom widgets.
   - `name: "site-reliability-engineer"`, `subagent_type: "site-reliability-engineer"` — when the change introduces new operational surface (new endpoint, background worker, scheduled job, observability hooks).
   - `name: "test-engineer"`, `subagent_type: "test-engineer"` — when tests should be written alongside the implementation rather than deferred to `/test` (TDD, regression-prone areas, thin existing coverage).
4. When spawning each teammate, include their area, owned paths, dependencies on other areas, and a pointer to the plan file (`/docs/implementation-plans/<issue-id>.md`) in the spawn prompt so they start primed to their slice.
5. Create tasks in the team task list using `TaskCreate` for: branch verification and one implementation task per area.

## Phase 3: Branch Verification

**Goal**: Confirm everyone is on the correct branch before any code is written

**Actions**:
1. Assign the branch-verification task to one engineer via `TaskUpdate`. Send the issue ID via `SendMessage` so they can verify the feature branch is checked out (it should already exist from `/plan-implementation`). If for any reason the branch is missing, create it from `develop` per `git-conventions.md`.
2. Wait for confirmation before any engineer starts work.

## Phase 4: Implementation

**Goal**: Implement the solution following the agreed plan and architecture

**Actions**:
1. For each engineer in the team, assign their area's implementation task via `TaskUpdate`. Send via `SendMessage`: their area scope and owned paths, the approved implementation plan (`/docs/implementation-plans/<issue-id>.md`), the issue details, architecture docs location (`/docs/`), API spec location (`/api/`), and UI/UX design location (`/docs/design/`) if relevant.
2. Engineers run **in parallel** when their areas don't conflict. If areas have ordering dependencies (e.g. backend contract before frontend integration), gate later engineers on the earlier one's completion.
3. Each engineer implements following the plan and applying Clean Code, SOLID, and KISS principles, committing in small logical units to the shared branch. If `test-engineer` is in the team, they work in lock-step with each engineer — tests land in the same commits as the code they cover, not as a trailing batch.
4. Present progress to the user at natural milestones as agents report back. If two engineers risk touching the same files, broker the boundary explicitly via `SendMessage`.
5. Discuss implementation decisions and trade-offs with the user as they arise. Relay decisions to the relevant engineer(s) via `SendMessage`. **If the plan needs to change materially, pause, return to `/plan-implementation` to update the plan, and re-confirm before continuing.**

## Phase 5: Shutdown & Summary

**Goal**: Clean up the team and confirm implementation is complete

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize what was implemented per area and which acceptance criteria are covered (per the plan's coverage map).
4. Suggest running `/test` next to add test coverage (if `test-engineer` wasn't on the team), then `/review` once tests are in place.
