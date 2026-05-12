---
name: plan-implementation
description: Produce a step-by-step implementation plan for an issue — files to touch, work-stream split, risks, recommended team — without writing any code. Hard human-in-the-loop gate before /implement.
argument-hint: Issue number or URL
disable-model-invocation: true
user-invocable: true
---

Plan implementation for: $ARGUMENTS

# Plan Implementation

You are the orchestrator of an implementation-planning session. The goal is a clear, written plan — files to touch, work-stream split, risks, recommended team — that the user reviews and approves **before any code is written**. This is the deliberate human-in-the-loop gate between `/design` and `/implement`.

The plan is persisted on the feature branch at `/docs/implementation-plans/<issue-id>.md` and linked from the GitHub issue, so `/implement` can read it without re-planning.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Gather Context

**Goal**: Fully understand what needs to be built before planning

**Actions**:
1. Read the issue via the project management MCP server (user stories, acceptance criteria, and any early UX/arch notes from `/refine`).
2. Launch an `Explore` agent to gather:
   - Relevant areas of the codebase, existing patterns, and conventions
   - Design artifacts produced by `/design`: ADRs in `/docs/adr/`, architecture doc in `/docs/architecture/`, API spec in `/api/`, UI/UX in `/docs/design/`, data design in `/docs/data/`, threat model in `/docs/security/threat-models/` — whichever exist for this feature
   - Existing test coverage in the affected paths
3. Ask the user any remaining clarifying questions about scope, constraints, or trade-offs the design didn't resolve.
4. Confirm understanding with the user before proceeding.

## Phase 2: Branch Setup

**Goal**: Ensure the plan lands on the same branch `/implement` will use

**Actions**:
1. Use the **git MCP server** to check out the feature branch if it already exists (e.g. created by `/design`), or create it from `develop` otherwise per `git-conventions.md` (i.e. `feature/<issue-id>-<slug>`).
2. Ensure `/docs/implementation-plans/` exists.

## Phase 3: Produce the Plan

**Goal**: A step-by-step, code-free implementation plan with a recommended team composition

**Actions**:
1. Launch a `Plan` agent with the gathered context. Ask it to produce:
   - **Step-by-step implementation plan** — files to touch, order of changes, critical trade-offs, risks to watch.
   - **Work-stream split** — whether the work cleanly splits into independent areas (frontend vs. backend, service A vs. service B, infrastructure vs. application). For each area: scope, files/directories owned, dependencies on other areas, and the order in which areas must land. If the work is single-stream, say so explicitly.
   - **Recommended team for `/implement`** — number and naming of `software-engineer` agents, plus which specialists should join: `database-engineer`, `security-engineer`, `accessibility-specialist`, `site-reliability-engineer`, `test-engineer`. Justify each inclusion in one line.
   - **Acceptance-criteria coverage map** — which plan step satisfies which acceptance criterion.
2. Iterate with the `Plan` agent until the plan is solid. Present interim drafts to the user for input.

## Phase 4: Persist the Plan

**Goal**: Save the plan where `/implement` will read it

**Actions**:
1. Save the plan to `/docs/implementation-plans/<issue-id>.md` on the feature branch. Use this structure:
   ```
   ## Implementation Plan — Issue #<issue-id>

   **Status**: Draft
   **Branch**: feature/<issue-id>-<slug>
   **Design artifacts**: [links to ADRs, API spec, UI/UX, data design, threat model]

   ### Scope
   ### Acceptance-criteria coverage
   ### Work-stream split
   ### Step-by-step plan (per area)
   ### Risks and trade-offs
   ### Recommended team for /implement
   ### Out of scope
   ```
2. Commit: `docs(plan): implementation plan for #<issue-id>`.
3. Push the branch via the git MCP server.
4. Post a comment on the GitHub issue linking to the plan file and summarizing: scope, work-stream split, top 3 risks, recommended team.

## Phase 5: Approval Gate

**Goal**: Hard human-in-the-loop gate before any code is written

**Actions**:
1. Present the plan summary to the user: scope, split, top 3 risks, files to be touched, recommended team.
2. **STOP.** The plan does not become an implementation. The user must explicitly run `/implement <issue-id>` to proceed with code. This separation is the point of this skill.
3. If the user requests changes, iterate via the `Plan` agent, update the plan file, re-commit, and re-link the issue comment.
4. Once approved, flip the file header from `Status: Draft` to `Status: Approved`, commit the status change, and suggest running `/implement <issue-id>` as the next step.
