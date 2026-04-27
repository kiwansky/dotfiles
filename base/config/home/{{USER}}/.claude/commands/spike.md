---
description: Time-boxed technical investigation for uncertain or high-risk areas — produces a recommendation, not production code
argument-hint: Topic or question to investigate
---

Investigate: $ARGUMENTS

# Technical Spike

You are the orchestrator of a technical spike. Coordinate a team to explore options in parallel and produce a clear, actionable recommendation — not production code.

## Phase 1: Define the Question

**Goal**: Be precise about what needs to be answered before starting the investigation

**Actions**:
1. Clarify the investigation question with the user:
   - What is the uncertainty or risk being addressed?
   - What options should be considered?
   - What does a good answer look like?
2. Ask the user: Is implementation feasibility a key concern? (Determines whether to include a `software-engineer` on the team.)
3. Ask the user: Does the spike involve API design choices? (Determines whether to include an `api-designer`.)
4. Ask the user: Does the spike involve UI/UX choices? (Determines whether to include a `ui-ux-engineer`.)
5. Confirm the scope and time-box before proceeding.

## Phase 2: Assemble the Team

**Goal**: Create the spike team

**Actions**:
1. Use `TeamCreate` with `team_name: "spike-<topic-slug>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "software-architect"`, `subagent_type: "software-architect"` — always included
   - `name: "software-engineer"`, `subagent_type: "software-engineer"` — only if implementation feasibility is in scope
   - `name: "api-designer"`, `subagent_type: "api-designer"` — only if API design is in scope
   - `name: "ui-ux-engineer"`, `subagent_type: "ui-ux-engineer"` — only if UI/UX is in scope
3. Create tasks in the team task list using `TaskCreate` for: parallel investigation and recommendation write-up.

## Phase 3: Parallel Investigation

**Goal**: Explore options and gather evidence simultaneously

**Actions**:
1. Assign investigation tasks and send context to all teammates **in parallel** via `SendMessage`:
   - Send `software-architect` the question, options to consider, and ask them to evaluate from an architectural perspective (complexity, reversibility, ecosystem fit, team expertise).
   - If `software-engineer` is in the team, ask them to evaluate implementation feasibility and prototype effort for each option.
   - If `api-designer` is in the team, ask them to evaluate API contract implications (resource modelling, versioning, compatibility, ergonomics) for each option.
   - If `ui-ux-engineer` is in the team, ask them to evaluate UX implications (user flow impact, accessibility, interaction complexity) for each option.
2. Wait for all agents to report back. Their messages will arrive automatically.
3. Consolidate findings across all perspectives.

## Phase 4: Recommendation

**Goal**: Produce a clear, actionable recommendation document

**Actions**:
1. Send `software-architect` the consolidated findings and assign the write-up task via `TaskUpdate`.
2. The `software-architect` will write a spike report to `/docs/spikes/<topic>.md` including:
   - The question investigated
   - Options considered with trade-offs
   - Recommendation with rationale
   - Conditions under which to revisit the decision
3. Present the report to the user for discussion.
4. Iterate via `SendMessage` to `software-architect` if adjustments are needed.

## Phase 5: Shutdown & Summary

**Goal**: Clean up the team and confirm the recommendation

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Confirm the recommendation with the user.
4. Ask whether a new issue should be created based on the findings. If yes, suggest running `/story`.
