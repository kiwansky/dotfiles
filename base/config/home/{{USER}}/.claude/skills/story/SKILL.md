---
name: story
description: Quickly create or update a user story in the issue tracker
argument-hint: Feature idea, problem description, or existing issue number
disable-model-invocation: true
user-invocable: true
---

Create or refine user story: $ARGUMENTS

# User Story

You are coordinating the creation or refinement of a user story. The goal is a well-formed issue in the tracker with a clear persona, goal, and initial scope — without the full refinement ceremony.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Understand the Need

**Goal**: Understand the feature or problem to address

**Actions**:
1. If `$ARGUMENTS` is an issue number, read it via the project management MCP server.
2. Ask the user clarifying questions:
   - Who is the target user/persona?
   - What problem does this solve?
   - What does success look like?
   - What are the known constraints?

## Phase 2: Author the Story

**Goal**: Produce a well-formed user story

**Actions**:
1. Launch a `product-owner` agent. The agent will:
   - Write the user story in the "As a [persona] / I want [capability] / So that [value]" format
   - Define out-of-scope items
   - Add acceptance criteria *placeholders* (the detailed criteria belong in `/refine`, not here)
   - Apply standard labels per `project-conventions.md` — at minimum `story`, plus any cross-cutting labels (e.g. `frontend`, `api`, `tech-debt`, `bug`)
   - Suggest a milestone if one applies
   - Create or update the issue via the GitHub MCP server
2. Present the story to the user and discuss. Iterate via `SendMessage` if the persona, scope, or value statement needs sharpening.

## Phase 3: Summary

**Goal**: Confirm the story is ready and point to the next step

**Actions**:
1. Confirm the issue is updated. Print the issue number and URL.
2. Suggest the next step in the pipeline:
   - **`/refine`** to add detailed acceptance criteria, UX notes, and architectural considerations (most common next step).
   - **`/spike`** if the story has unresolved technical uncertainty before refinement makes sense.
   - **`/discovery`** if the story is more "we think we should build X" than "we know X solves a real problem" — validate the problem first.
