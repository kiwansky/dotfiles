---
name: explain
description: Explain a file, module, or subsystem — purpose, structure, data flow, entry points. Use when the user asks "how does X work", "explain this code/module", or wants to get oriented in an unfamiliar part of a codebase.
---

# Explain

Build an accurate mental model of a piece of code and convey it concisely.

## Steps

1. Pin down the target. If the user named a concept rather than a path, locate it first (search broadly; consider an Explore agent for large codebases).
2. Read the code itself — entry points, key types, and the main control/data flow. Follow imports and call sites enough to see how the piece connects to the rest of the system. Don't explain from file names or comments alone.
3. Structure the explanation:
   - **Purpose** — what problem this code solves, in one or two sentences.
   - **Entry points** — where execution enters, referenced as `file:line` so they're clickable.
   - **How it works** — the main flow, narrated at the level of design decisions, not line-by-line.
   - **Connections** — what it depends on and what depends on it.
   - **Gotchas** — non-obvious behavior, invariants, or surprising coupling actually observed in the code.
4. Match depth to the question: a quick "what does this function do" gets a paragraph; "explain this subsystem" gets the full structure above.

## Rules

- Read-only: never modify code during an explanation.
- Distinguish facts from inference: what the code does vs. what it appears intended to do.
- If something can't be determined from the code (e.g. runtime config, external services), say so instead of speculating.
