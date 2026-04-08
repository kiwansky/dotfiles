---
description: Set up or update the CI/CD pipeline for the project
argument-hint: Optional scope or specific pipeline change needed
---

Set up or update CI/CD: $ARGUMENTS

# CI/CD Pipeline

You are coordinating CI/CD pipeline work. The goal is a reliable, well-designed pipeline that enforces quality gates and automates delivery.

## Phase 1: Assess Current State

**Goal**: Understand the existing pipeline and what needs to change

**Actions**:
1. Launch an `Explore` agent to inspect existing CI/CD configuration files (e.g., `.github/workflows/`, `Jenkinsfile`, `gitlab-ci.yml`).
2. Ask the user:
   - What is the deployment target (cloud provider, container platform, etc.)?
   - What quality gates are required (tests, linting, coverage thresholds)?
   - What environments exist (dev, staging, production)?
   - Are there specific pain points or requirements driving this change?
3. Summarize the current state and proposed scope of work with the user.

## Phase 2: Design & Implement

**Goal**: Implement the pipeline changes

**Actions**:
1. Launch a `ci-cd-engineer` agent to:
   - Design the pipeline following best practices (fail fast, shift left, parallelization, idempotency)
   - Implement the configuration with quality gates, security scanning, and secret management
   - Follow the principle of least privilege for all credentials
   - Block pull requests if quality gates are not satisfied
2. Present the proposed pipeline to the user. Discuss design decisions and trade-offs.
3. Confirm with the user before committing.

## Phase 3: Commit & Summary

**Goal**: Commit the changes and document them

**Actions**:
1. Commit pipeline changes: `ci: <description> [#<issue-id>]`.
2. Summarize what was implemented and suggest validation steps.
