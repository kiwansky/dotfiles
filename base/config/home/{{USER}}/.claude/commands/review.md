---
description: Run the full review cycle — create PR, multi-lens code review, address findings, re-review until consensus
argument-hint: PR number, branch name, or issue number
---

Review: $ARGUMENTS

# Review Cycle

You are the orchestrator of a review cycle. Coordinate specialized reviewers and a software engineer to produce a thoroughly reviewed, approved PR with all findings resolved.

Branch and PR conventions follow `git-conventions.md`.

## Phase 1: Gather Context

**Goal**: Ensure a PR exists and understand its scope

**Actions**:
1. If `$ARGUMENTS` is a PR number, read it via the GitHub MCP server.
2. If a branch or issue is provided, check for an existing open PR via the GitHub MCP server.
3. If no PR exists, create one now using the GitHub MCP server: feature branch → `develop`.
4. Detect what's in scope: pure code? schema migration? new endpoint? UI change? infrastructure? This drives team composition in Phase 2.
5. Summarize the changes to the user.

## Phase 2: Assemble the Team

**Goal**: Create the review team, scaled to the change

**Actions**:
1. Use `TeamCreate` with `team_name: "review-<pr-number>"`.
2. **Always include** these reviewers via the `Agent` tool with the `team_name` and a `name`:
   - `name: "reviewer-bugs"`, `subagent_type: "code-reviewer"` — focus: **bug detection** (logic errors, edge cases, null dereferences, incorrect assumptions, off-by-one errors, race conditions).
   - `name: "reviewer-quality"`, `subagent_type: "code-reviewer"` — focus: **code quality** (Clean Code, SOLID, KISS compliance, naming, complexity, duplication, readability).
   - `name: "reviewer-architecture"`, `subagent_type: "code-reviewer"` — focus: **architectural alignment** (does the implementation match the agreed design, ADRs, layer boundaries, module responsibilities, no unplanned dependencies).
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — dedicated security reviewer (replaces the prior `reviewer-security` lens — a specialist runs deeper).
   - `name: "software-engineer"`, `subagent_type: "software-engineer"` — addresses findings.
3. **Conditionally include**:
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — if the PR touches schema, migrations, or queries.
   - `name: "accessibility-specialist"`, `subagent_type: "accessibility-specialist"` — if the PR touches user-facing UI.
   - `name: "sre"`, `subagent_type: "sre"` — if the PR touches production-critical paths, observability, or operational behavior.
4. Create tasks in the team task list using `TaskCreate` for: initial review (one per reviewer), address findings, and re-review.

## Phase 3: Code Review

**Goal**: Identify all issues across all relevant lenses

**Actions**:
1. Send the PR number and repository details to all reviewers **in parallel** via `SendMessage`. Each reviewer's message must include their specific focus area and instruction to post findings as PR review comments via the GitHub MCP server.
2. Wait for all reviewers to report back.
3. Consolidate findings by focus area. **Deduplicate** issues raised by multiple reviewers — count once, attribute to all who raised it.
4. Present the combined review summary to the user.

## Phase 4: Triage & Disagreement Resolution

**Goal**: Decide which findings to act on before the engineer starts fixing

**Actions**:
1. Group findings by **severity**: Critical (must fix before merge), Major (should fix), Minor (nice-to-have).
2. Identify **conflicting recommendations** — e.g. one reviewer says "extract to helper", another says "leave inline". Conflicts get explicit resolution:
   - Re-broadcast the disagreement via `SendMessage` to the conflicting reviewers, asking each to acknowledge the trade-off and pick a side, or defer to the user.
   - If they remain split, the user (orchestrator-facing) is the arbiter. Surface the trade-off clearly: "Reviewer A wants X because Y; Reviewer B wants Z because W; you decide."
   - The `software-architect` may be brought in via `Agent` for a tiebreak when the disagreement is structural.
3. Present the triaged list (Critical / Major / Minor / Deferred / Disputed) to the user. The user confirms which findings are in-scope for this PR before the engineer touches anything.

## Phase 5: Address Findings

**Goal**: Resolve in-scope findings

**Actions**:
1. Assign the findings task to `software-engineer` via `TaskUpdate`. Send the user-confirmed list of open findings via `SendMessage` with clear instruction to address issues **one at a time**, discussing each with you (the orchestrator) before making changes.
2. After the engineer proposes a fix for each finding, discuss it with the user and relay approval or feedback via `SendMessage`.
3. After each finding is addressed, the engineer commits the change and replies to the review comment referencing the commit. Commit follows `git-conventions.md`.
4. Repeat until all agreed-upon findings are resolved.

## Phase 6: Re-Review

**Goal**: Verify all findings are resolved and no new issues introduced

**Actions**:
1. Send all reviewers a re-review request **in parallel** via `SendMessage`, notifying them that all findings have been addressed.
2. Each reviewer will: re-check their previously open issues, verify resolution, mark them resolved on the PR, and flag any new issues within their focus area.
3. Wait for all reviewers to report back.
4. If any new issues are found, return to Phase 4 with the new findings.

## Phase 7: Shutdown & Summary

**Goal**: Clean up the team and decide on merge

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Confirm with the user that all in-scope issues are resolved.
4. Ask the user whether to merge the PR into `develop`. If yes, merge via the GitHub MCP server. Otherwise hand back to the user.
5. Suggest `/document` if the change introduced new concepts, or `/release` if this completes a release-ready batch of work.
