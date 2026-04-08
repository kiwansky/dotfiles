---
description: Review, update, and ensure consistency of project documentation
argument-hint: Optional scope (e.g. README, architecture, API docs) or issue number
---

Update documentation: $ARGUMENTS

# Documentation

You are coordinating a documentation review and update pass. The goal is accurate, consistent, and complete documentation across the project.

## Phase 1: Audit

**Goal**: Identify documentation gaps and inconsistencies

**Actions**:
1. Launch a `technical-writer` agent to:
   - Review all existing documentation (`/docs/`, `README.md`, `/api/`)
   - Check for inconsistencies, outdated content, and missing sections
   - Verify each concern is documented in its own dedicated file
   - Produce a prioritized list of issues found
2. Present findings to the user and agree on what to address.

## Phase 2: Update

**Goal**: Fix identified documentation issues

**Actions**:
1. Launch a `technical-writer` agent to:
   - Fix inconsistencies and outdated content
   - Fill documentation gaps
   - Ensure the README is up to date
2. Present changes to the user for review.

## Phase 3: Summary

**Goal**: Confirm documentation is up to date

**Actions**:
1. Summarize all documentation changes made.
2. Commit: `docs: update documentation [#<issue-id>]`.
