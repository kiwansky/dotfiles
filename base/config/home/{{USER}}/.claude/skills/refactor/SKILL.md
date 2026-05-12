---
name: refactor
description: Plan and execute a scoped refactor — risk-assessed, with a safety net of tests written first, on a refactor/ branch
argument-hint: Path, module, or short description of what to refactor
disable-model-invocation: true
user-invocable: true
---

Refactor: $ARGUMENTS

# Refactor

You are the orchestrator of a scoped refactoring effort. The goal is to improve internal structure **without changing observable behavior** — and to do it safely. Branch and commit conventions follow `git-conventions.md`.

A refactor is *not* a feature, a bug fix, or a redesign. If the work changes behavior, it should be `/implement` instead. If it changes architecture meaningfully, run `/design` first.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Frame the Refactor

**Goal**: Establish what we're changing and why, before changing anything

**Actions**:
1. Identify the scope: file, module, package, or cross-cutting concern (e.g. "extract a payment domain"). Be specific.
2. Identify the **trigger**: why now?
   - Code is hard to test → tests will get easier after
   - Repeated bugs cluster here → reduces error surface
   - About to add a feature that requires changes here → enables the feature
   - Code-review finding marked as deferred → addressing tech debt
   - Other (be honest — "I don't like the style" is rarely a good enough trigger)
3. State the success criteria explicitly:
   - **Behavior preserved**: existing tests still pass; observable behavior unchanged.
   - **Specific structural improvement**: what gets simpler, smaller, more cohesive, or more testable.
   - **No scope creep**: enumerate what's *not* part of this refactor.

## Phase 2: Branch Setup

**Actions**:
1. Use the **git MCP server** to create or check out `refactor/<scope-slug>` from `develop` per `git-conventions.md`.
2. Refactors get their own branch — they should not be bundled with feature work, because reviewers can't tell behavior change from structural change in a mixed PR.

## Phase 3: Assemble the Team

**Actions**:
1. Use `TeamCreate` with `team_name: "refactor-<slug>"`.
2. Spawn:
   - `name: "software-architect"`, `subagent_type: "software-architect"` — plans the refactor.
   - `name: "software-engineer"`, `subagent_type: "software-engineer"` — executes.
   - `name: "test-engineer"`, `subagent_type: "test-engineer"` — builds the safety net.
3. **Conditionally include**:
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — if the refactor touches the data layer (queries, repos, migrations).
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — if the refactor touches auth, crypto, or other security-sensitive code paths.

## Phase 4: Plan the Refactor

**Goal**: Decide the *small steps* before changing code

**Actions**:
1. Assign the planning task to `software-architect`. They produce a plan covering:
   - **Current state** — observed structure, smells (long methods, large classes, feature envy, primitive obsession, data clumps, etc.).
   - **Target state** — what the structure looks like after.
   - **Sequenced steps** — small, behavior-preserving transformations (rename, extract, inline, move, replace conditional with polymorphism, etc.). Each step ships independently green.
   - **Risk assessment** — which steps are risky? What is the rollback for each?
   - **Out of scope** — explicit list of things they noticed but won't touch.
2. The architect references `clean-code-principles.md` and `pragmatism-principles.md` — strict cleanup is right when uncertainty is low; pragmatism is right when uncertainty is high. Surface tension explicitly.
3. Present the plan to the user. Iterate via `SendMessage`. **Confirm scope before any code changes.**

## Phase 5: Build the Safety Net

**Goal**: Capture current behavior in tests *before* changing anything

**Actions**:
1. Assign the safety-net task to `test-engineer`. They will:
   - Audit existing test coverage of the refactor scope.
   - Add **characterization tests** that pin down current observable behavior — including quirks. The goal is "tests that fail if I accidentally change behavior," not "tests that prove correctness."
   - Prefer integration-level tests for behavior pinning; reach for unit tests when the seam is clean.
   - Run the new tests against the unchanged code — they all pass.
2. Commit the safety-net tests *before* any structural changes: `test(<scope>): add characterization tests for refactor [#<issue-id>]`.
3. **The refactor does not start until the safety net is green.**

## Phase 6: Execute Step-by-Step

**Goal**: Apply the planned transformations one at a time

**Actions**:
1. Assign execution to `software-engineer`. For each planned step:
   - Apply the single transformation
   - Run the full test suite (safety net + existing)
   - **Tests must stay green between steps.** If a test fails, the refactor stepped across a behavior boundary — back out and re-plan.
   - Commit per step with `refactor(<scope>): <step description> [#<issue-id>]`. Small commits make review and bisect cheap.
2. The architect, database-engineer, and security-engineer (if in the team) review at intermediate milestones. They surface concerns to the engineer via `SendMessage`.
3. If the engineer discovers the original plan was wrong, **stop and re-plan** with the architect rather than freelancing.

## Phase 7: Review the Diff

**Goal**: Verify behavior is preserved and the structural improvement landed

**Actions**:
1. Run the full test suite one more time. All green, no flakes.
2. Diff vs. `develop`: scan for accidental behavior changes (default values, validation rules, error messages, log lines, public signatures). The reviewer's mantra during a refactor: "what could a user notice?"
3. Spawn two `code-reviewer` agents via `Agent` for an explicit pre-PR pass, each with a distinct lens:
   - `name: "reviewer-bugs"`, `subagent_type: "code-reviewer"` — bug-detection lens, hunts for accidental behavior change (default values, validation, error messages, log lines, public signatures).
   - `name: "reviewer-architecture"`, `subagent_type: "code-reviewer"` — architecture lens, confirms the structural goal landed, no scope creep, no new layering violations.

   Together they confirm:
   - No observable behavior change visible in the diff
   - Structural goal achieved
   - No scope creep
4. Iterate via `SendMessage` until the reviewer signs off.

## Phase 8: Commit & Open PR

**Actions**:
1. Push the branch. Open a PR back to `develop` via the GitHub MCP server.
2. PR description must state: scope, trigger, success criteria, what is *not* in scope, and how the safety net protects against regressions.
3. Recommend `/review` to the user for the formal review cycle.

## Phase 9: Shutdown & Summary

**Actions**:
1. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
2. Summarize:
   - Steps applied (count)
   - Tests added (count, pyramid level)
   - Lines added/removed
   - Behavior delta (should be: "none, by design")
3. Suggest `/review` to land the change.
