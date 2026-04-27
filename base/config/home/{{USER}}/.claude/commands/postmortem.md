---
description: Author a blameless postmortem for a production incident — timeline, root causes, action items — on a postmortem/ branch
argument-hint: Incident slug or short description (e.g. "2026-04-22-checkout-outage")
---

Postmortem: $ARGUMENTS

# Postmortem

You are the orchestrator of a blameless postmortem. The goal is a clear, written record that explains what happened, why, and what we will change — generating concrete action items in the issue tracker. Postmortems aim at *systems*, never at *people*.

## Phase 1: Frame the Incident

**Goal**: Establish what we're writing about before writing

**Actions**:
1. Confirm the incident with the user:
   - Date and time (UTC) the incident started and ended
   - User-visible impact (what broke, for whom, how badly)
   - Detection: how did we find out?
   - Mitigation: what stopped the bleeding?
2. Confirm a slug for the postmortem (e.g. `2026-04-22-checkout-outage`).
3. Confirm participants: who was on call, who joined, who can answer timeline questions.
4. Read related sources via the GitHub MCP server: any open issues, alerts that fired, related PRs deployed in the prior 24–48 hours.

## Phase 2: Branch Setup

**Goal**: Isolate postmortem authorship

**Actions**:
1. Use the **git MCP server** to create or check out the branch per `git-conventions.md` (i.e. `postmortem/<slug>`) from `develop`.
2. Ensure `/docs/postmortems/` exists. If not, create it with a `README.md` that indexes postmortems.

## Phase 3: Assemble the Team

**Goal**: Bring in the right specialists for the incident type

**Actions**:
1. Use `TeamCreate` with `team_name: "postmortem-<slug>"`.
2. **Always include**:
   - `name: "sre"`, `subagent_type: "sre"` — owns the postmortem.
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — polishes the narrative.
3. **Conditionally include based on the incident**:
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — if security incident or near-miss.
   - `name: "database-engineer"`, `subagent_type: "database-engineer"` — if data layer involved (locking, replication, migration, corruption).
   - `name: "ci-cd-engineer"`, `subagent_type: "ci-cd-engineer"` — if deploy pipeline contributed.
   - `name: "code-reviewer"`, `subagent_type: "code-reviewer"` — if a specific code defect is suspected.

## Phase 4: Build the Timeline

**Goal**: Get an honest, UTC-timestamped sequence of events

**Actions**:
1. Assign the timeline task to `sre`. Send the framing context.
2. The `sre` will collect:
   - Alert firings (with timestamps)
   - Detection time (when did a human first know?)
   - Status updates posted during the incident
   - Mitigations attempted, in order, with outcomes
   - Resolution: what fixed it
3. Iterate with the user — fill gaps from human memory while the incident is still recent. The timeline is the foundation; everything else builds on it.

## Phase 5: Identify Root Causes

**Goal**: Distinguish *direct* causes from *contributing* factors, without blaming individuals

**Actions**:
1. Apply the "Five Whys" (or similar) to walk from symptom to underlying cause.
2. Categorize causes:
   - **Direct**: the immediate trigger (deploy, config change, traffic spike)
   - **Contributing**: factors that made the impact worse or detection slower (missing alert, brittle dependency, no rollback)
   - **Systemic**: organizational or process factors (no runbook, single person knowledge, missing tests)
3. Where the conditional specialists are in the team (security, database, CI/CD, code-reviewer), have them review their domain.
4. **Blameless framing rule**: every cause is described as a system property. "The deploy proceeded despite an unhealthy canary signal" — not "Alice deployed despite the canary."

## Phase 6: Draft the Postmortem

**Goal**: Produce the document at `/docs/postmortems/<slug>.md`

**Actions**:
1. Assign drafting to `sre`. Use the structure from `observability-standards.md`:
   ```
   ## [Incident title]

   **Status**: Resolved
   **Date**: YYYY-MM-DD
   **Duration**: HH:MM
   **Author(s)**:

   ### Summary
   ### Impact
   ### Detection
   ### Timeline (UTC)
   ### Root cause(s)
     - Direct
     - Contributing
     - Systemic
   ### What went well
   ### What went poorly
   ### Action items
   | # | Action | Owner | Due | Issue |
   ### Lessons learned
   ```
2. The `technical-writer` does a clarity and tone pass.
3. Present the draft to the user. Iterate via `SendMessage`. Postmortems often need 2–3 passes for honesty and clarity.

## Phase 7: Generate Action Items

**Goal**: Convert the postmortem into tracked work

**Actions**:
1. For each action item, create a GitHub issue via the MCP server with:
   - Title prefixed `[postmortem]`
   - Body: link to the postmortem, the specific item, and the rationale
   - Labels: `postmortem`, plus area labels (per `project-conventions.md`) and severity if applicable
   - Milestone: next sprint or release as appropriate
   - Assignee: per the team's process (often left unassigned for the team to pick up)
2. Update the action items table in the postmortem with the issue numbers.
3. **Verify each action item is concrete and dated.** "Improve monitoring" is not an action item; "Add p99-latency burn-rate alert on /checkout, by 2026-05-15" is.

## Phase 8: Commit & Publish

**Actions**:
1. Commit the postmortem and supporting docs. Follow conventional-commit format: `docs(postmortem): add <slug>`.
2. Push the branch via the git MCP server.
3. Ask the user whether to open a PR back to `develop` now or leave the branch open for review/edits.

## Phase 9: Shutdown & Summary

**Actions**:
1. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
2. Summarize:
   - Postmortem location
   - Action items created (with counts by severity/type)
   - Suggested follow-ups (e.g. `/refine` per action item before implementation)
3. Schedule (via `/loop` or user calendar) a 30-day check-in on action item progress.
