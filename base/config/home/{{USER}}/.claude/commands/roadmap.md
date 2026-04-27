---
description: Build or refresh a horizon-based roadmap (Now / Next / Later) tied to product vision and strategic pillars
argument-hint: Optional time horizon or scope (e.g. "Q3 2026", "platform pillar")
---

Roadmap: $ARGUMENTS

# Roadmap

You are the orchestrator of roadmap planning. The goal is a **horizon-based** roadmap (Now / Next / Later — *not* a Gantt chart) that ties day-to-day work to the product vision and strategic pillars. A roadmap is a *bet*, not a *promise* — communicate it as such.

Roadmap planning sits between `/product-vision` (3–5 year direction) and `/refine` (a specific story made implementation-ready). Run it quarterly or whenever priorities shift materially.

## Phase 1: Establish Inputs

**Goal**: Pull together everything the roadmap should be derived from

**Actions**:
1. Locate the latest vision and pillars:
   - `/docs/product/vision.md` (and `narrative.md`, `roadmap.md` if present)
   - Any in-flight `/discovery` results in `/docs/product/discovery/`
2. Pull current state of the work:
   - Open issues by label (especially `epic`, `story`)
   - Active milestones
   - In-flight feature branches (via the git MCP server)
3. Ask the user:
   - **Time horizon** — typically the next 1–4 quarters; confirm.
   - **Capacity** — engineering headcount available, expected leave / freezes.
   - **Hard constraints** — fixed delivery dates, regulatory deadlines, dependencies on other teams.
   - **Stakeholder asks** — what has been promised to whom?
   - **Operational debt** — known reliability / security / dependency hotspots that should be invested in.

## Phase 2: Branch Setup

**Actions**:
1. Use the **git MCP server** to create or check out `vision/roadmap-<period>` from `develop` (e.g. `vision/roadmap-2026-q3`). Roadmap work is treated as vision-adjacent.
2. Ensure `/docs/product/` exists.

## Phase 3: Assemble the Team

**Actions**:
1. Use `TeamCreate` with `team_name: "roadmap-<period>"`.
2. Spawn:
   - `name: "product-manager"`, `subagent_type: "product-manager"` — leads, balances strategic value.
   - `name: "software-architect"`, `subagent_type: "software-architect"` — sanity-checks feasibility, sequencing, technical dependencies.
   - `name: "sre"`, `subagent_type: "sre"` — surfaces operational debt that should be on the roadmap.
   - `name: "security-engineer"`, `subagent_type: "security-engineer"` — surfaces security debt that should be on the roadmap.

## Phase 4: Themes & Bets

**Goal**: Map possible work to strategic pillars, not features

**Actions**:
1. Assign the theme task to `product-manager`. They will:
   - Map open issues, in-flight work, and discovery outputs to the strategic pillars from `vision.md`.
   - Identify themes ("expand into X", "reduce time-to-first-value", "improve reliability of Y") rather than feature lists.
   - For each theme, identify the **bet**: what we believe, what's at stake, and how we'd know it worked.
2. The `sre` and `security-engineer` contribute non-product themes (reliability, dependency hygiene, threat-model gaps) — these go on the roadmap too.
3. The `software-architect` flags themes whose technical sequencing locks ordering (e.g. "we can't do B until A").

## Phase 5: Prioritize into Now / Next / Later

**Goal**: Use a defensible framework, not gut feel

**Actions**:
1. Apply RICE (Reach × Impact × Confidence ÷ Effort) **or** MoSCoW **or** Value-vs-Effort, depending on the user's preference. Default to RICE.
2. Have the `product-manager` produce a ranked list with explicit scores and reasoning.
3. Slot themes into:
   - **Now** — committed for the current quarter / period. Has clear scope, clear owner, and clear success measure.
   - **Next** — likely the following period. Less defined; on deck.
   - **Later** — known but deliberately deferred. Captured to avoid losing context, not to commit.
4. **Capacity check**: total Now must fit the available capacity from Phase 1, with ~20% buffer for in-flight bugs and operational work.
5. **Sequencing check**: from the architect — does the Now order respect technical dependencies?

## Phase 6: Author the Roadmap Document

**Goal**: Produce `/docs/product/roadmap.md`

**Actions**:
1. Structure:
   ```
   ## Roadmap — <period>

   **Status**: Draft / Approved
   **Last updated**: YYYY-MM-DD
   **Capacity assumed**: <headcount, FTE, weeks>
   **Vision link**: /docs/product/vision.md

   ### Now (committed this period)
   For each item: theme, bet, success measure, owner, target end date, linked epic/issue.

   ### Next (likely next period)
   ### Later (deferred, captured for context)
   ### Explicit non-goals
   ### Assumptions & risks
   ### Capacity model
   ### Out-of-scope discussions
   ```
2. Tone: communicate as bets and intentions, not commitments. Use phrases like "we believe" and "we plan to" — not "we will."
3. Iterate with the user via `SendMessage`. Roadmaps almost always get pushback; surface trade-offs instead of arguing.

## Phase 7: Wire to the Issue Tracker

**Actions**:
1. For each Now item, ensure there's an `epic` issue in GitHub:
   - Title and description match the roadmap item
   - Labels: `epic`, plus relevant area labels per `project-conventions.md`
   - Milestone: matches the period
   - Sub-issues: if known, linked via `sub_issue_write`
2. Add a top-level comment on each epic linking to the roadmap.
3. Anything in **Later** stays in the doc only — don't pollute the tracker with speculative epics.

## Phase 8: Commit & Summary

**Actions**:
1. Commit: `docs(roadmap): publish roadmap for <period>`.
2. Push the branch via the git MCP server.
3. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
4. Summarize:
   - Now / Next / Later breakdown with counts
   - Top 3 risks from the Assumptions & risks section
   - Suggested cadence for refresh (typically quarterly)
5. Suggest `/refine` for each Now epic to break it into stories with acceptance criteria.
