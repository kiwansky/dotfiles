---
description: Quickly create or update a user story in the issue tracker
argument-hint: Feature idea, problem description, or existing issue number
---

Create or refine user story: $ARGUMENTS

# User Story

You are coordinating the creation or refinement of a user story. The goal is a well-formed issue in the tracker with a clear persona, goal, and initial scope — without the full refinement ceremony.

## Phase 1: Understand the Need

**Goal**: Understand the feature or problem to address

**Actions**:
1. If `$ARGUMENTS` is an issue number, read it via the GitHub MCP server.
2. Ask the user clarifying questions:
   - Who is the target user/persona?
   - What problem does this solve?
   - What does success look like?
   - What are the known constraints?

## Phase 2: Author the Story

**Goal**: Produce a well-formed user story

**Actions**:
1. Launch a `product-owner` agent to:
   - Write the user story ("As a / I want / So that")
   - Define out-of-scope items
   - Add acceptance criteria placeholders
   - Create or update the issue via the GitHub MCP server
2. Present the story to the user and discuss.

## Phase 3: Summary

**Goal**: Confirm the story is ready

**Actions**:
1. Confirm the issue is updated.
2. Suggest running `/refine` to add detailed acceptance criteria and design considerations.
