---
description: Design the architecture, API spec, and documentation for an issue
argument-hint: Issue number or URL
---

Design the solution for: $ARGUMENTS

# Design

You are the orchestrator of a design session. Coordinate a team of specialists to produce a documented architecture, optional API specification, and updated project documentation — ready for implementation.

## Phase 1: Gather Context

**Goal**: Understand the issue and existing architecture before spinning up the team

**Actions**:
1. Read the issue via the GitHub MCP server (user stories and acceptance criteria).
2. Launch an `Explore` agent to understand the existing architecture in `/docs/` and relevant areas of the codebase.
3. Ask the user clarifying questions about constraints, tech stack preferences, or existing decisions.
4. Ask the user: Does this feature require a new or updated API? (Determines team composition.)

## Phase 2: Assemble the Team

**Goal**: Create the design team

**Actions**:
1. Use `TeamCreate` with `team_name: "design-<issue-id>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "software-architect"`, `subagent_type: "software-architect"` — always included
   - `name: "api-designer"`, `subagent_type: "api-designer"` — only if an API is required
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — always included
3. Create tasks in the team task list using `TaskCreate` for each phase below.

## Phase 3: Architecture Design

**Goal**: Design and document the architectural approach

**Actions**:
1. Assign the architecture task to `software-architect` via `TaskUpdate`. Send the issue details, codebase exploration findings, and user-confirmed constraints via `SendMessage`.
2. The `software-architect` will: design the approach, produce an ADR in `/docs/adr/`, and document the architecture in `/docs/`.
3. When the agent reports back, present the architecture to the user. Discuss trade-offs.
4. If adjustments are needed, send feedback via `SendMessage` to `software-architect` and iterate.
5. Confirm the chosen approach with the user.

## Phase 4: API Specification (if applicable)

**Goal**: Design and document the API contract

**Actions**:
1. If `api-designer` is in the team: assign the API spec task and send the approved architecture as context via `SendMessage`.
2. The `api-designer` will: produce an OpenAPI 3.x spec in `/api/` and report back with a summary of design decisions.
3. Present the API spec to the user. Iterate via `SendMessage` as needed.
4. Confirm the spec with the user.

## Phase 5: Documentation Review

**Goal**: Ensure all design artifacts are clear and consistent

**Actions**:
1. Assign the documentation task to `technical-writer` via `TaskUpdate`. Send links to all produced artifacts (ADR, architecture doc, API spec) via `SendMessage`.
2. The `technical-writer` will: review for clarity and consistency, and update the README if the design introduces new concepts.
3. Present documentation changes to the user for review.

## Phase 6: Shutdown & Summary

**Goal**: Clean up the team and confirm design is approved

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize all design artifacts produced (ADRs, API spec, docs).
4. Confirm with the user that the design is approved.
5. Suggest running `/implement` as the next step.
