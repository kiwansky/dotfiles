---
description: Implement an issue following its architecture and acceptance criteria, including tests
argument-hint: Issue number or URL
---

Implement: $ARGUMENTS

# Implementation

You are the orchestrator of an implementation session. Coordinate a software engineer and test engineer to deliver working, tested code that fulfills all acceptance criteria.

## Phase 1: Gather Context

**Goal**: Fully understand what needs to be built before writing any code

**Actions**:
1. Read the issue via the GitHub MCP server (user stories, acceptance criteria).
2. Launch an `Explore` agent to understand the relevant codebase, existing patterns, and architecture docs in `/docs/`.
3. Ask the user any remaining clarifying questions.
4. Confirm understanding with the user before proceeding.

## Phase 2: Assemble the Team

**Goal**: Create the implementation team

**Actions**:
1. Use `TeamCreate` with `team_name: "implement-<issue-id>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "software-engineer"`, `subagent_type: "software-engineer"`
   - `name: "test-engineer"`, `subagent_type: "test-engineer"`
3. Create tasks in the team task list using `TaskCreate` for: branch setup, implementation, and tests.

## Phase 3: Branch Setup

**Goal**: Work on the correct branch

**Actions**:
1. Assign the branch setup task to `software-engineer` via `TaskUpdate`. Send the issue ID and a brief description via `SendMessage` so they can create `feature/<issue-id>-<short-description>` from `develop`.
2. Wait for confirmation that the branch is created.

## Phase 4: Implementation

**Goal**: Implement the solution following the agreed architecture

**Actions**:
1. Assign the implementation task to `software-engineer` via `TaskUpdate`. Send the issue details, architecture docs location (`/docs/`), and API spec location (`/api/`) via `SendMessage`.
2. The `software-engineer` will implement, applying Clean Code, SOLID, and KISS principles, committing in small logical units.
3. Present progress to the user at natural milestones (the agent will report back as it works).
4. Discuss implementation decisions and trade-offs with the user as they arise. Relay decisions back via `SendMessage`.

## Phase 5: Tests

**Goal**: Ensure the implementation is fully tested and all acceptance criteria are covered

**Actions**:
1. Once implementation is complete, assign the test task to `test-engineer` via `TaskUpdate`. Send the issue's acceptance criteria and the list of implemented files via `SendMessage`.
2. The `test-engineer` will: write unit, integration, and E2E tests following the test pyramid, and write acceptance tests for each acceptance criterion.
3. When the agent reports back, confirm all tests pass.

## Phase 6: Shutdown & Summary

**Goal**: Clean up the team and confirm implementation is complete

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize what was implemented and which acceptance criteria are covered.
4. Suggest running `/review` as the next step.
