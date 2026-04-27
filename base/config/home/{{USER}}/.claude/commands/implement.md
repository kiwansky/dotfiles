---
description: Implement an issue following its architecture and acceptance criteria
argument-hint: Issue number or URL
---

Implement: $ARGUMENTS

# Implementation

You are the orchestrator of an implementation session. Coordinate one or more software engineers to deliver working code that fulfills the architecture and acceptance criteria. Testing is handled by the dedicated `/test` command.

## Phase 1: Gather Context

**Goal**: Fully understand what needs to be built before writing any code

**Actions**:
1. Read the issue via the project management MCP server (user stories, acceptance criteria).
2. Launch an `Explore` agent to understand the relevant codebase, existing patterns, and architecture docs in `/docs/`.
3. Ask the user any remaining clarifying questions.
4. Confirm understanding with the user before proceeding.

## Phase 2: Plan Implementation

**Goal**: Produce a step-by-step implementation plan and identify separable work streams before any code is written

**Actions**:
1. Launch a `Plan` agent with the gathered context (issue details, acceptance criteria, codebase findings, architecture docs in `/docs/`, API spec in `/api/`, UI/UX design in `/docs/design/` if any) and ask it to produce a step-by-step implementation plan — including the files to touch, the order of changes, critical trade-offs, and risks to watch.
2. Identify whether the work splits cleanly into independent areas (e.g. frontend vs. backend, service A vs. service B, infrastructure vs. application). For each area, note: scope, files/directories owned, dependencies on other areas, and the order in which areas must land.
3. Present the plan and the proposed split (or single-stream approach) to the user. Discuss trade-offs and confirm.
4. Iterate with the `Plan` agent if adjustments are needed.
5. Confirm the final plan with the user before proceeding.

## Phase 3: Assemble the Team

**Goal**: Create the implementation team — one `software-engineer` per separable area, plus specialists where the work demands it

**Actions**:
1. Use `TeamCreate` with `team_name: "implement-<issue-id>"`.
2. Spawn one `software-engineer` per area identified in Phase 2, each primed to its specific scope. Use descriptive names so messages are routable. Examples:
   - Single-stream work: `name: "software-engineer"`, `subagent_type: "software-engineer"`.
   - Frontend + backend split: `name: "software-engineer-frontend"` and `name: "software-engineer-backend"`, both `subagent_type: "software-engineer"`.
   - Service split: `name: "software-engineer-<service>"` per service, all `subagent_type: "software-engineer"`.
3. **Conditionally include specialists** when the work touches their domain:
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — for schema changes, migrations, or query work.
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — for auth, crypto, secrets, or other security-sensitive paths.
   - `name: "accessibility-specialist"`, `subagent_type: "accessibility-specialist"` — for non-trivial UI work, especially custom widgets.
   - `name: "sre"`, `subagent_type: "sre"` — when the change introduces new operational surface (new endpoint, background worker, scheduled job, observability hooks).
4. When spawning each teammate, include their area, owned paths, and dependencies on other areas in the spawn prompt so they start primed to their slice.
5. Create tasks in the team task list using `TaskCreate` for: branch setup and one implementation task per area.

## Phase 4: Branch Setup

**Goal**: Work on the correct branch

**Actions**:
1. Assign the branch setup task to one engineer (any of the spawned engineers — pick one) via `TaskUpdate`. Send the issue ID and a brief description via `SendMessage` so they can check out the feature branch if it already exists (e.g. created by `/design`), or create it from `develop` otherwise. Branch naming follows `git-conventions.md`.
2. Wait for confirmation that the branch is checked out before any other engineer starts work on the same checkout.

## Phase 5: Implementation

**Goal**: Implement the solution following the agreed plan and architecture

**Actions**:
1. For each engineer in the team, assign their area's implementation task via `TaskUpdate`. Send via `SendMessage`: their area scope and owned paths, the approved implementation plan, the issue details, architecture docs location (`/docs/`), API spec location (`/api/`), and UI/UX design location (`/docs/design/`) if relevant.
2. Engineers run **in parallel** when their areas don't conflict. If areas have ordering dependencies (e.g. backend contract before frontend integration), gate later engineers on the earlier one's completion.
3. Each engineer implements following the plan and applying Clean Code, SOLID, and KISS principles, committing in small logical units to the shared branch.
4. Present progress to the user at natural milestones as agents report back. If two engineers risk touching the same files, broker the boundary explicitly via `SendMessage`.
5. Discuss implementation decisions and trade-offs with the user as they arise. Relay decisions to the relevant engineer(s) via `SendMessage`. If the plan needs to change materially, pause and re-align with the user before continuing.

## Phase 6: Shutdown & Summary

**Goal**: Clean up the team and confirm implementation is complete

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize what was implemented per area and which acceptance criteria are covered.
4. Suggest running `/test` next to add test coverage, then `/review` once tests are in place.
