---
name: test
description: Write or review tests — assess pyramid balance, fill the most valuable gaps, validate the suite is fast, deterministic, and meaningful
argument-hint: File path, module name, or issue number
disable-model-invocation: true
user-invocable: true
---

Write or review tests for: $ARGUMENTS

# Test Writing

You are the orchestrator of a focused test-writing or test-review pass. The goal is a well-balanced test suite that gives meaningful confidence in the code, runs fast, and isn't flaky. Branch and commit conventions follow `git-conventions.md`.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Understand the Code & Existing Coverage

**Goal**: Pinpoint where new tests will pay off most

**Actions**:
1. Launch an `Explore` agent to gather:
   - Code to be tested (file paths, public surface, key branches)
   - Existing tests for that code and adjacent modules
   - Test framework and testing utilities in use
   - Mocking patterns and test doubles already established
   - Pyramid balance signal (count of unit / integration / E2E in this area, runtime if available)
   - CI test commands and any coverage thresholds
2. Form a hypothesis about where tests are missing or weak. Common signals:
   - Untested error/branch paths
   - Inverted-pyramid hot spots (lots of E2E, no unit)
   - Slow or flaky integration suites
   - Logic without negative test cases (auth, validation)
3. Ask the user only the questions you can't answer from the code:
   - Are there specific behaviors or risks they want tested first?
   - Are flake or runtime issues more painful than coverage gaps right now?
   - Any non-functional tests needed (load, contract, fuzz)?
4. Confirm scope with the user before writing.

## Phase 2: Plan the Test Pass

**Goal**: Decide where each new test lives in the pyramid before writing

**Actions**:
1. Spawn a `test-engineer` via `Agent`. Send the Phase 1 findings.
2. The `test-engineer` will produce a short test plan:
   - Which scenarios to cover (happy path, error paths, edge cases)
   - At which pyramid level each scenario belongs (unit / integration / E2E / contract)
   - What to mock vs. what to use real
   - Estimated runtime impact
   - Any refactor needed before testing (a test that's painful to write usually means the code is wrong)
3. Present the plan to the user. Iterate via `SendMessage` if needed. Confirm.

## Phase 3: Branch Setup

**Actions**:
1. If tests are tied to an issue or feature branch in flight, work on that branch.
2. Otherwise create `chore/tests-<scope>` from `develop` per `git-conventions.md`.
3. Use the **git MCP server** to check out the branch.

## Phase 4: Write Tests

**Goal**: Produce tests that match the plan

**Actions**:
1. The `test-engineer` writes tests following:
   - **FIRST**: Fast, Independent, Repeatable, Self-validating, Timely
   - One reason to fail per test
   - No logic in tests (no loops/conditionals; tests are straight-line)
   - Black-box at higher pyramid levels, white-box at unit when justified
   - Descriptive names that communicate intent
   - Deterministic — no flakes from timing, random data, or shared state
2. Run the new tests locally. Confirm they pass and that mutating the code under test makes them fail (the "is this test useful?" sanity check).
3. Run the full suite to check no regressions in adjacent tests.
4. Measure runtime impact — flag any new test taking disproportionately long.

## Phase 5: Validate the Suite

**Goal**: Confirm the suite is healthy after the changes

**Actions**:
1. **Pyramid balance check**: present unit / integration / E2E counts and runtime before vs. after. Flag if the pass made the balance worse (e.g. added E2Es where unit would have done).
2. **Coverage signal**: report coverage delta if a coverage tool is wired. Coverage isn't the goal, but a drop is worth flagging.
3. **Flake check**: re-run the new tests at least once (preferably 5x) to surface non-determinism early.
4. Iterate via `SendMessage` until the suite is healthy.

## Phase 6: Commit & Summary

**Actions**:
1. Commit per conventional-commit format: `test(<scope>): <description> [#<issue-id>]`. Group commits by area when adding many tests.
2. Send `{type: "shutdown_request"}` to the `test-engineer`. Call `TeamDelete` if a team was created.
3. Summarize:
   - What was added (per pyramid level)
   - Pyramid balance before/after
   - Runtime delta
   - Remaining coverage gaps (if any) and whether they're worth a follow-up issue
4. Suggest next steps: `/review` if these tests are part of a PR ready for review; `/refactor` if testing surfaced design issues that warrant cleanup.
