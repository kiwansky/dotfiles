---
description: Facilitate an extensive product vision exercise with the product-manager — documented under /docs/product/ on a vision/ branch
argument-hint: Optional vision topic or scope (e.g. "2026-2028 platform strategy")
---

Product vision: $ARGUMENTS

# Product Vision

You are the orchestrator of a product-vision session. Coordinate a small team led by the `product-manager` agent to produce an extensive, well-structured product vision — captured as durable documentation under `/docs/product/` on a dedicated `vision/` branch.

This command is for **strategic** work (mission, vision, positioning, target customer, business model, north-star, strategic roadmap). For tactical refinement (stories, acceptance criteria, sprint backlog), use `/refine` instead.

## Phase 1: Gather Context

**Goal**: Understand the scope and inputs before assembling the team

**Actions**:
1. If `$ARGUMENTS` is provided, treat it as the vision topic / scope. Otherwise, ask the user what the vision should cover.
2. Ask the user clarifying questions:
   - **Time horizon** (1, 3, or 5 years)?
   - **Audience** (internal team, leadership, board/investors, customers)?
   - **Scope** (whole company, a single product line, a feature area)?
   - **Existing inputs** (customer research, analytics, competitive intel, prior strategy docs) — and where to find them?
   - **Constraints** (business model, regulatory, platform dependencies, non-negotiables)?
3. Launch an `Explore` agent to read any existing material in `/docs/`, especially `/docs/product/`, `/docs/architecture/`, and the project README, so the vision is grounded in current reality.
4. Confirm the brief with the user before proceeding.

## Phase 2: Branch Setup

**Goal**: Isolate vision work on a dedicated branch so it can iterate without disturbing in-flight feature work

**Actions**:
1. Determine a short kebab-case slug for the vision (e.g. `2026-2028-platform-strategy`, `payments-expansion`, `q3-repositioning`). Confirm the slug with the user.
2. Use the **git MCP server** to:
   - Ensure the working tree is clean (warn the user and stop if it isn't).
   - Check out `develop` and pull the latest.
   - Create and check out the vision branch from `develop`. Branch naming follows `git-conventions.md` (i.e. `vision/<slug>`). If the branch already exists, check it out instead.
3. Ensure `/docs/product/` exists. If it doesn't, create it with a placeholder `README.md` describing what lives in this directory.
4. Confirm the branch and directory are ready before assembling the team.

## Phase 3: Assemble the Team

**Goal**: Spin up the vision team

**Actions**:
1. Use `TeamCreate` with `team_name: "vision-<slug>"`.
2. Spawn teammates via the `Agent` tool with the `team_name` and a `name` for each:
   - `name: "product-manager"`, `subagent_type: "product-manager"` — always included, leads the session
   - `name: "ui-ux-engineer"`, `subagent_type: "ui-ux-engineer"` — included when the vision has meaningful UX or experience implications
   - `name: "software-architect"`, `subagent_type: "software-architect"` — included when the vision has material technical-feasibility or platform implications
   - `name: "technical-writer"`, `subagent_type: "technical-writer"` — always included, owns documentation polish
3. Create tasks in the team task list using `TaskCreate` for each phase below.

## Phase 4: Discovery & Framing

**Goal**: Establish the strategic context before drafting the vision

**Actions**:
1. Assign the discovery task to `product-manager` via `TaskUpdate`. Send the user's brief, exploration findings, and constraints via `SendMessage`.
2. The `product-manager` will produce, in `/docs/product/discovery.md`:
   - Target customer / ICP with named segments and jobs-to-be-done
   - Problem statement and opportunity sizing (with assumptions flagged)
   - Competitive landscape (direct, indirect, and "do nothing" baseline)
   - Market trends and inflection points relevant to the horizon
   - Open questions and the cheapest experiments to answer them
3. Discuss the discovery output with the user. Iterate via `SendMessage` until the framing is solid — vision built on shaky framing is worthless.

## Phase 5: Vision Draft

**Goal**: Produce the core vision document

**Actions**:
1. Assign the vision-drafting task to `product-manager` via `TaskUpdate`. Send the approved discovery findings as context via `SendMessage`.
2. The `product-manager` will produce `/docs/product/vision.md` covering, at minimum:
   - **Mission** (decade-scale)
   - **Vision** (3–5 year future state, concrete and falsifiable)
   - **Target Customer / ICP**
   - **Problem & Opportunity**
   - **Value Proposition**
   - **Positioning Statement** (Geoffrey Moore template)
   - **Strategic Pillars** (3–5 themes)
   - **North-Star Metric** plus supporting input metrics
   - **Business Model** (pricing, monetization, channel)
   - **Strategic Roadmap** — Now / Next / Later, mapped to pillars (not features or dates)
   - **Risks & Load-Bearing Assumptions** with validation plan
   - **Non-Goals** — what is explicitly out of scope
3. Present the draft to the user. Iterate via `SendMessage` — vision documents almost always need 2–3 passes. Steel-man alternatives, stress-test assumptions, and tighten the language.

## Phase 6: Experience & Feasibility Review (if applicable)

**Goal**: Validate the vision against UX and technical reality

**Actions**:
1. If `ui-ux-engineer` is in the team: assign a review task with the vision draft. The agent produces `/docs/product/experience-implications.md` outlining what the vision means for users, key flows, and design principles to uphold.
2. If `software-architect` is in the team: assign a review task with the vision draft. The agent produces `/docs/product/feasibility-notes.md` outlining technical implications, platform investments required, and feasibility risks per strategic pillar.
3. Bring findings back to the `product-manager` via `SendMessage`. Update `vision.md` if the reviews surface material risks or new non-goals.
4. Confirm the revised vision with the user.

## Phase 7: Narrative & Communication Artifacts

**Goal**: Produce the artifacts that make the vision usable beyond this room

**Actions**:
1. Assign the narrative task to `product-manager`. Produce in `/docs/product/`:
   - `narrative.md` — a 1–2 page strategic narrative ("press release from the future" or executive memo style)
   - `one-pager.md` — a single-page summary suitable for all-hands or board
   - `faq.md` — anticipated questions and crisp answers (objections, "why now?", "why not X?")
2. Iterate with the user via `SendMessage` until the narrative is sharp.

## Phase 8: Documentation Review

**Goal**: Polish for clarity, consistency, and longevity

**Actions**:
1. Assign the doc-review task to `technical-writer`. Send links to all artifacts in `/docs/product/`.
2. The `technical-writer` will: review for clarity, consistency, voice, and structure; ensure `/docs/product/README.md` indexes all artifacts with one-line descriptions; cross-check that terminology is used consistently across documents.
3. Present documentation changes for user review.

## Phase 9: Commit & Push

**Goal**: Persist the vision on the branch

**Actions**:
1. Use the **git MCP server** to commit the documentation in logically grouped commits (e.g. one per artifact), each following the project's conventional-commit format. Since vision work isn't tied to an issue ID, use the slug as the scope (e.g. `docs(vision): add discovery findings`). If the user wants an issue ID, ask first.
2. Push the `vision/<slug>` branch to the remote.
3. Do **not** open a pull request automatically — vision documents typically iterate over weeks. Mention to the user that `/review` can be used later to open and run the PR cycle when the vision is ready to merge into `develop`.

## Phase 10: Shutdown & Summary

**Goal**: Clean up and hand off

**Actions**:
1. Send `{type: "shutdown_request"}` via `SendMessage` to each active teammate.
2. Call `TeamDelete` once all teammates have shut down.
3. Summarize for the user:
   - Branch name and where it lives
   - All artifacts produced under `/docs/product/`
   - Open assumptions / experiments still to run
   - Suggested next steps (validate top assumptions, share narrative with stakeholders, run `/refine` on the first pillar to break it into deliverable work, run `/review` when ready to merge)
