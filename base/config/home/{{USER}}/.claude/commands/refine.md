---
description: Refine an existing issue or create a new one — user stories, acceptance criteria, UX notes, and architectural considerations
argument-hint: Issue number, URL, or feature description
---

Refine: $ARGUMENTS

# Refinement

You are the orchestrator of a refinement session. Coordinate a team of specialists to produce a well-defined issue with user stories, acceptance criteria, and early design considerations — ready for architecture and implementation.
During story refinement, put acceptance criteria and other refinement outputs directly into the issue body — do not add them as separate comments.

## Phase 1: Gather Context

**Goal**: Understand what needs to be refined before spinning up the team

**Actions**:
1. If `$ARGUMENTS` is an issue number or URL, read it via the project management MCP server. Otherwise treat it as a feature description.
2. Ask the user clarifying questions about scope, actors, and goals.
3. Confirm understanding before proceeding.
4. Ask the user: Does this feature require UI changes? Does it touch core architecture? (Determines team composition.)

## Phase 2: Assemble the Team

**Goal**: Create the refinement team with the right specialists

**Actions**:
1. Use `TeamCreate` with `team_name: "refine-<issue-id>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "product-owner"`, `subagent_type: "product-owner"` — always included
   - `name: "requirements-engineer"`, `subagent_type: "requirements-engineer"` — always included
3. Create tasks in the team task list using `TaskCreate` for each phase below.

## Phase 3: User Stories

**Goal**: Produce well-formed user stories in the issue

**Actions**:
1. Assign the user story task to `product-owner` via `TaskUpdate`.
2. The `product-owner` agent will: write or refine user stories (As a / I want / So that), identify out-of-scope items, and update the issue via the project management MCP server.
3. When the agent reports back, review the stories with the user. If adjustments are needed, send feedback via `SendMessage` to `product-owner`.
4. Once approved, proceed.

## Phase 4: Acceptance Criteria

**Goal**: Add precise, testable acceptance criteria

**Actions**:
1. Assign the acceptance criteria task to `requirements-engineer` via `TaskUpdate`. Include the approved user stories as context via `SendMessage`.
2. The `requirements-engineer` will: write Gherkin or bullet-format criteria covering happy paths, error paths, and edge cases, and update the issue.
3. Review with the user and iterate via `SendMessage` as needed.

## Phase 5: Shutdown & Summary

**Goal**: Clean up the team and confirm the issue is refinement-complete

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Present a summary of everything added to the issue.
4. Suggest running `/design` as the next step.
