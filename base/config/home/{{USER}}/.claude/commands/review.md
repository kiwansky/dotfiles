---
description: Run the full review cycle — create PR, code review, address findings, re-review until consensus
argument-hint: PR number, branch name, or issue number
---

Review: $ARGUMENTS

# Review Cycle

You are the orchestrator of a review cycle. Coordinate four specialized reviewers and a software engineer to produce a thoroughly reviewed, approved PR with all findings resolved.

## Phase 1: Gather Context

**Goal**: Ensure a PR exists and understand its scope

**Actions**:
1. If `$ARGUMENTS` is a PR number, read it via the GitHub MCP server.
2. If a branch or issue is provided, check for an existing open PR via the GitHub MCP server.
3. If no PR exists, create one now using the GitHub MCP server: feature branch → `develop`.
4. Summarize the changes to the user.

## Phase 2: Assemble the Team

**Goal**: Create the review team

**Actions**:
1. Use `TeamCreate` with `team_name: "review-<pr-number>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "reviewer-bugs"`, `subagent_type: "code-reviewer"` — focus: **bug detection** (logic errors, edge cases, null dereferences, incorrect assumptions, off-by-one errors)
   - `name: "reviewer-quality"`, `subagent_type: "code-reviewer"` — focus: **code quality** (Clean Code, SOLID, KISS compliance, naming, complexity, duplication, readability)
   - `name: "reviewer-security"`, `subagent_type: "code-reviewer"` — focus: **security** (OWASP Top 10, injection, auth/authz, secrets in code, input validation, dependency vulnerabilities)
   - `name: "reviewer-architecture"`, `subagent_type: "code-reviewer"` — focus: **architectural alignment** (does the implementation match the agreed design, ADRs, layer boundaries, module responsibilities, no unplanned dependencies)
   - `name: "software-engineer"`, `subagent_type: "software-engineer"`
3. Create tasks in the team task list using `TaskCreate` for: initial review (×4), address findings, and re-review (×4).

## Phase 3: Code Review

**Goal**: Identify all issues in the implementation across four specialized dimensions

**Actions**:
1. Send the PR number and repository details to all four reviewers **in parallel** via `SendMessage`. Each reviewer's message must include their specific focus area and instruction to post findings as PR review comments via the GitHub MCP server.
2. Wait for all four reviewers to report back.
3. Consolidate the findings by focus area and present the combined review summary to the user.

## Phase 4: Address Findings

**Goal**: Resolve review issues one at a time

**Actions**:
1. Assign the findings task to `software-engineer` via `TaskUpdate`. Send the consolidated list of open findings (grouped by focus area) via `SendMessage` with clear instruction to address issues **one at a time**, discussing each with you (the orchestrator) before making changes.
2. After the engineer proposes a fix for each finding, discuss it with the user and relay approval or feedback via `SendMessage`.
3. After each finding is addressed, the engineer commits the change and replies to the review comment referencing the commit.
4. Repeat until all agreed-upon findings are resolved.

## Phase 5: Re-Review

**Goal**: Verify all findings are resolved and no new issues introduced

**Actions**:
1. Send all four reviewers a re-review request **in parallel** via `SendMessage`, notifying them that all findings have been addressed.
2. Each reviewer will: re-check their previously open issues, verify resolution, mark them resolved on the PR, and flag any new issues within their focus area.
3. Wait for all four reviewers to report back.
4. If any new issues are found, return to Phase 4 with the new findings.

## Phase 6: Shutdown & Summary

**Goal**: Clean up the team and confirm the PR is approved

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate (all four reviewers and the software engineer).
2. Call `TeamDelete` once all teammates have shut down.
3. Confirm with the user that all issues are resolved.
4. Ask the user whether to merge the PR into `develop`. If yes, merge via the GitHub MCP server.
