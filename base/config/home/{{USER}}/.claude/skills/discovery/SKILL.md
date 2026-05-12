---
name: discovery
description: Validate a single feature or opportunity before committing — jobs-to-be-done, competitive scan, problem framing, and an explicit go/no-go recommendation
argument-hint: Feature idea, opportunity description, or issue number
disable-model-invocation: true
user-invocable: true
---

Discovery: $ARGUMENTS

# Discovery

You are the orchestrator of a lightweight discovery exercise. The goal is to *validate the problem* — not the solution — before the team commits engineering effort. This is the cheaper, faster cousin of `/product-vision`: a single feature/opportunity, days not weeks. Output: a written recommendation to **build / build small / postpone / drop**.

Discovery sits between `/story` (capture an idea) and `/refine` (make it implementation-ready). It is optional but highly recommended for ambitious or ambiguous work.

## Approval Gates

@~/.claude/shared/approval-beat.md

This gate applies at **every phase boundary in this skill** — not just the final one. Each phase ends with present → STOP → confirm before advancing.

## Phase 1: Frame the Question

**Goal**: Establish what we are validating, in plain language

**Actions**:
1. If `$ARGUMENTS` is an issue number, read it via the GitHub MCP server.
2. Ask the user:
   - **What is the proposed feature or opportunity?**
   - **Who is it for?** (Specific user / segment, not "users.")
   - **What problem do we believe it solves?** (Stated as a customer problem, not a feature.)
   - **What's our level of conviction?** (Have we talked to customers? Read tickets? Just a hypothesis?)
   - **What's the cost of being wrong?** (Cheap experiment vs. major bet.)
   - **Time-box.** A discovery exercise should fit in days, not weeks. Confirm a ceiling.
3. Restate the discovery question in one sentence: "Is [problem] real and important enough for [segment] to justify building [proposed solution]?" Get the user to agree to the framing.

## Phase 2: Branch Setup

**Actions**:
1. Use the **git MCP server** to create or check out `discovery/<slug>` from `develop` (or work on the existing issue's feature branch if discovery is a sub-step of a larger initiative).
2. Ensure `/docs/product/discovery/` exists.

## Phase 3: Assemble the Team

**Actions**:
1. Use `TeamCreate` with `team_name: "discovery-<slug>"`.
2. Spawn:
   - `name: "product-manager"`, `subagent_type: "product-manager"` — leads.
   - `name: "ui-ux-engineer"`, `subagent_type: "ui-ux-engineer"` — only if UX implications are central to the validation.
   - `name: "software-architect"`, `subagent_type: "software-architect"` — only if technical feasibility is uncertain (otherwise skip — discovery is about the *problem*, not the solution).

## Phase 4: Investigate

**Goal**: Gather signal — fast — on whether the problem is real

**Actions**:
1. Assign the investigation task to `product-manager`. Ask them to produce, in `/docs/product/discovery/<slug>.md`:

   ### Customer evidence
   - Existing customer signals: support tickets, sales notes, user research transcripts, churn reasons, NPS comments — point to specific sources, not "we think customers want this."
   - Quantify where possible (X% of churn cites this problem; Y open tickets tagged Z).
   - Mark unknowns as unknowns. **Never invent customer data.**

   ### Jobs-to-be-done framing
   - What job is the customer hiring this feature to do?
   - What are they hiring *today* (workaround, competitor, manual process)?
   - What triggers the switch?

   ### Competitive scan
   - Direct competitors: do they offer this? How well?
   - Indirect: what else fills the same job?
   - "Do nothing" baseline: what happens if we don't build this?

   ### Sizing (rough)
   - How many customers / segments are affected?
   - Revenue or retention impact, even rough.

   ### Riskiest assumptions
   - What 2–3 things must be true for this to work?
   - For each, the **cheapest experiment** that would falsify it.

2. Iterate via `SendMessage`. Push back on weak signal — "we think customers will love this" is not evidence.

## Phase 5: Recommendation

**Goal**: Make an explicit call

**Actions**:
1. The `product-manager` produces a recommendation:
   - **Build** — strong signal, validated assumptions, clear scope.
   - **Build small** — proceed with a smaller scope or experiment to validate the riskiest assumption first.
   - **Postpone** — problem is real but not currently the top priority; document and revisit.
   - **Drop** — problem is not real, not important enough, or solved adequately by alternatives.
2. The recommendation must include:
   - The chosen disposition
   - The reasoning (1–2 paragraphs)
   - Top 3 risks if proceeding
   - The next step (which command to run, or specifically what to do)
3. Present to the user. Iterate. The user has final say on disposition.

## Phase 6: Document & Route

**Actions**:
1. Finalize `/docs/product/discovery/<slug>.md` with the disposition recorded.
2. Update or create the GitHub issue:
   - Add the discovery doc as a comment or link
   - Apply labels: `discovery-complete`, plus disposition (`build`, `build-small`, `postponed`, `dropped`)
   - For `postponed` or `dropped`: close the issue with `state_reason: "not_planned"` and rationale in the closing comment
3. If the disposition is `build` or `build-small`: update the issue body with the validated problem statement and JTBD, then suggest `/refine` next.
4. If `build-small`: scope down explicitly in the issue body — what is the minimum experiment that would validate the next assumption?

## Phase 7: Commit & Summary

**Actions**:
1. Commit per conventional-commit format: `docs(discovery): <slug> <disposition>`.
2. Push the branch via the git MCP server.
3. Send `{type: "shutdown_request"}` to all teammates. Call `TeamDelete`.
4. Summarize the disposition, the riskiest assumption, and the recommended next command.
