---
description: Write or review tests for existing code following the test pyramid
argument-hint: File path, module name, or issue number
---

Write or review tests for: $ARGUMENTS

# Test Writing

You are coordinating a focused test-writing or test-review pass. The goal is a well-balanced test suite that gives meaningful confidence in the code.

## Phase 1: Understand the Code Under Test

**Goal**: Understand what needs to be tested and what already exists

**Actions**:
1. Launch an `Explore` agent to:
   - Locate the code to be tested
   - Find any existing tests and assess the current pyramid balance (unit / integration / E2E ratio)
   - Identify the test framework in use
2. Ask the user what coverage gaps to prioritize.

## Phase 2: Write Tests

**Goal**: Produce tests at the appropriate pyramid levels

**Actions**:
1. Launch a `test-engineer` agent to:
   - Write missing unit tests (mock external dependencies, test one thing per test)
   - Write integration tests for component interactions
   - Write acceptance tests for any acceptance criteria in related issues
   - Follow FIRST principles: Fast, Independent, Repeatable, Self-validating, Timely
2. Confirm all tests pass.
3. Commit: `test(<scope>): <description> [#<issue-id>]`.

## Phase 3: Summary

**Goal**: Report test coverage improvements

**Actions**:
1. Summarize what was tested and at which pyramid level.
2. Note any remaining gaps for the user's awareness.
