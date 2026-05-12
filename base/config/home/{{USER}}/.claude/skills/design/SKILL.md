---
name: design
description: Design the architecture, API spec, and documentation for an issue
argument-hint: Issue number or URL
disable-model-invocation: true
user-invocable: true
---

Design the solution for: $ARGUMENTS

# Design

You are the orchestrator of a design session. Coordinate a team of specialists to produce a documented architecture, optional API specification, and updated project documentation — ready for implementation.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Gather Context

**Goal**: Understand the issue and existing architecture before spinning up the team

**Actions**:
1. Read the issue via the project management MCP server (user stories and acceptance criteria).
2. Launch an `Explore` agent to understand the existing architecture in `/docs/` and relevant areas of the codebase.
3. Ask the user clarifying questions about constraints, tech stack preferences, or existing decisions.
4. Ask the user: Does this feature require a new or updated API? (Determines team composition.)

## Phase 2: Assemble the Team

**Goal**: Create the design team

**Actions**:
1. Use `TeamCreate` with `team_name: "design-<issue-id>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "software-architect"`, `subagent_type: "software-architect"` — always included.
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — always included.
   - `name: "api-designer"`, `subagent_type: "api-designer"` — only if an API is required.
   - `name: "ui-ux-engineer"`, `subagent_type: "ui-ux-engineer"` — only if a frontend / user-facing UI is required.
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — only if non-trivial schema design or query work is involved.
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — only if the design touches authentication, authorization, secrets, crypto, or restricted data classifications.
   - `name: "accessibility-specialist"`, `subagent_type: "accessibility-specialist"` — only if the design includes complex custom widgets or has formal accessibility-conformance obligations beyond the default WCAG 2.1 AA baseline that `ui-ux-engineer` already covers.
3. Create tasks in the team task list using `TaskCreate` for each phase below.

## Phase 3: Branch Setup

**Goal**: Ensure all design artifacts are produced on the same branch that `/implement` will continue on

**Actions**:
1. Assign the branch setup task to `software-architect` via `TaskUpdate`. Send the issue ID and a brief description via `SendMessage` so they can create the feature branch from `develop` (or check it out if it already exists). Branch naming follows `git-conventions.md`.
2. Wait for confirmation that the branch is created and checked out.
3. All subsequent phases (architecture, API, UI/UX, data, security, docs) commit to this branch.

## Phase 4: Architecture Design

**Goal**: Design and document the architectural approach

**Actions**:
1. Assign the architecture task to `software-architect` via `TaskUpdate`. Send the issue details, codebase exploration findings, and user-confirmed constraints via `SendMessage`.
2. The `software-architect` will: design the approach, produce an ADR in `/docs/adr/`, and document the architecture in `/docs/architecture`.
3. When the agent reports back, present the architecture to the user. Discuss trade-offs.
4. If adjustments are needed, send feedback via `SendMessage` to `software-architect` and iterate.
5. Confirm the chosen approach with the user.

## Phase 4.5: Data Design (if applicable)

**Goal**: Design the data layer — schemas, migrations, and query patterns

**Actions**:
1. If `database-engineer` is in the team: assign the data-design task and send the approved architecture and acceptance criteria as context via `SendMessage`.
2. The `database-engineer` will: design the schema, document access patterns, justify indexes and constraints, and produce a migration plan if existing data is affected — saved to `/docs/data/<feature>.md`.
3. Present the data design to the user. Iterate via `SendMessage` as needed. For changes touching large existing tables, surface the online-migration plan explicitly.
4. Confirm with the user.

## Phase 5: API Specification (if applicable)

**Goal**: Design and document the API contract

**Actions**:
1. If `api-designer` is in the team: assign the API spec task and send the approved architecture and (if applicable) data design as context via `SendMessage`.
2. The `api-designer` will: produce an OpenAPI 3.x spec in `/api/` and report back with a summary of design decisions.
3. Present the API spec to the user. Iterate via `SendMessage` as needed.
4. Confirm the spec with the user.

## Phase 6: UI/UX Design (if applicable)

**Goal**: Design and document the user interface and experience

**Actions**:
1. If `ui-ux-engineer` is in the team: assign the UI/UX task and send the approved architecture, API spec (if any), and acceptance criteria as context via `SendMessage`.
2. The `ui-ux-engineer` will: produce user flows, screen specs, component contracts, interaction states, responsive behavior, and accessibility notes (WCAG 2.1 AA baseline) — documented in `/docs/design/`.
3. Present the design to the user. Iterate via `SendMessage` as needed.
4. Confirm the design with the user.

## Phase 6.5: Accessibility Deep-Dive (if applicable)

**Goal**: Specialist review for complex inclusive patterns or formal conformance obligations

**Actions**:
1. If `accessibility-specialist` is in the team: assign the a11y deep-dive task with the approved UI/UX design as context.
2. The specialist will: audit any custom widgets against WAI-ARIA APG, define focus management and live announcements explicitly, and document patterns in `/docs/accessibility/patterns/`.
3. Iterate via `SendMessage`. Confirm with the user.

## Phase 6.7: Security Design Review (if applicable)

**Goal**: Validate the design against security and threat-modelling concerns before code is written

**Actions**:
1. If `security-engineer` is in the team: assign the design-review task with the approved architecture, API spec, and data design as context.
2. The `security-engineer` will: produce a STRIDE-based threat model in `/docs/security/threat-models/<feature>.md`, flag authorization gaps, secret-handling decisions, and any design-level risks. Issues raised here are cheaper to fix than at code-review time.
3. Iterate with the architect (and api-designer / database-engineer if their decisions are affected) via `SendMessage` until the design is acceptable.
4. Confirm with the user.

## Phase 7: Documentation Review

**Goal**: Ensure all design artifacts are clear and consistent

**Actions**:
1. Assign the documentation task to `technical-writer` via `TaskUpdate`. Send links to all produced artifacts (ADR, architecture doc, API spec, UI/UX design) via `SendMessage`.
2. The `technical-writer` will: review for clarity and consistency, and update the README if the design introduces new concepts.
3. Present documentation changes to the user for review.

## Phase 8: Shutdown & Summary

**Goal**: Clean up the team and confirm design is approved

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize all design artifacts produced (ADRs, API spec, docs).
4. Confirm with the user that the design is approved.
5. Suggest running `/implement` as the next step.
