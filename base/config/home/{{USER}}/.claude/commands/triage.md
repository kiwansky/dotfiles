---
description: Triage incoming bugs or new issues — reproduce, classify severity, label, link related, and route to the right next command
argument-hint: Issue number, URL, or bug description
---

Triage: $ARGUMENTS

# Triage

You are the orchestrator of an issue triage. The goal is a labelled, prioritised, routed issue with enough context that the next person picking it up can act immediately. Conventions follow `project-conventions.md` and `git-conventions.md`.

## Phase 1: Read the Report

**Goal**: Get the facts straight before classifying

**Actions**:
1. If `$ARGUMENTS` is an issue number or URL, read it via the GitHub MCP server. Otherwise treat it as a fresh bug description and prepare to create a new issue.
2. Identify whether this is:
   - **Bug** — something broken vs. expected behavior
   - **Regression** — was working, now isn't
   - **Feature request** — not a bug; route to `/story` or `/discovery`
   - **Question / support** — close with a pointer
   - **Duplicate** — link and close
3. Note what's already in the report: reproduction steps, environment, logs, screenshots, expected vs. actual.

## Phase 2: Reproduce or Investigate

**Goal**: Verify the issue is real and gather enough signal to classify

**Actions**:
1. Spawn a `code-reviewer` via `Agent` for root-cause hunch (they read code with the bug-detection lens).
2. Launch an `Explore` agent **in parallel** to find:
   - Recently touched files in the affected area (last 30 days of `git log`)
   - Existing related issues (search by keyword via GitHub MCP)
   - Existing tests that should have caught this
3. If the issue is reproducible from the report, attempt reproduction. If not, ask the reporter (via comment on the issue) for the missing inputs and pause.
4. Surface findings: probable area of code, related issues, missing tests, suspected commits.

## Phase 3: Classify

**Goal**: Apply consistent labels, severity, and ownership

**Actions**:
1. **Severity** (label one):
   - `sev/critical` — production down, data loss, security breach in progress
   - `sev/high` — major feature broken for many users, no good workaround
   - `sev/medium` — feature broken with workaround, or affecting some users
   - `sev/low` — minor, cosmetic, or rarely-hit
2. **Type** (label one): `bug` / `regression` / `tech-debt` / `support`. Use `regression` if the bisect implicates a recent commit.
3. **Area labels**: apply per `project-conventions.md` (`frontend`, `api`, `data`, etc.).
4. **Stakeholders**: if the bug touches a domain owner (security, data, accessibility), tag the relevant agent's "owner" label.
5. **Milestone**: assign if there's an obvious release destination.
6. **Assignee**: leave unassigned unless the user has a specific person in mind.
7. Use the GitHub MCP server (`issue_write`) to apply all labels and milestone in one call.

## Phase 4: Disposition

**Goal**: Route the issue to the next step

**Actions**:
1. If duplicate: close as `duplicate` with `duplicate_of`, comment linking to the canonical issue.
2. If feature request masquerading as a bug: relabel and suggest `/story` or `/discovery`.
3. If unclear/needs reporter: leave open, comment with the specific information requested, label `needs-info`.
4. If actionable bug: stay open, decide on next command:
   - **`sev/critical`** → recommend hotfix flow: `/refine` then `/implement` on a `hotfix/` branch (per `git-conventions.md`), with `/security-review` if security-relevant.
   - **`sev/high` / `sev/medium`** → recommend `/refine` for the next sprint.
   - **`sev/low`** → leave on backlog with milestone.
5. Add a triage summary comment on the issue: severity rationale, suspected area of code, related issues, recommended next command.

## Phase 5: Summary

**Actions**:
1. Print: issue number, severity, labels, milestone, recommended next step.
2. If multiple bugs were triaged in one session, summarize the batch with a small severity breakdown.
