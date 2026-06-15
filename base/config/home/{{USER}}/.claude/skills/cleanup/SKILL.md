---
name: cleanup
description: Deliberate, scoped refactoring pass — the dedicated home for cleanups deferred by the "no drive-by refactors" rule. Use when the user asks to clean up, refactor, or modernize a file, module, or a list of previously noted cleanup candidates.
---

# Cleanup

Apply refactors deliberately, in their own pass, instead of mixing them into feature work.

## Steps

1. Establish the scope: the files/modules to clean up, or the list of cleanup candidates noted in earlier work. If no scope is given, ask rather than sweeping the whole codebase.
2. Confirm a safety net exists: the affected code should be covered by tests. If coverage is missing for code about to be restructured, say so and offer to add characterization tests first.
3. Collect candidate cleanups by reading the scope: duplication to deduplicate, dead code, misleading names, over-complex constructs, outdated idioms. Stay behavior-preserving — anything that changes behavior is a feature/fix, not a cleanup.
4. Present the candidates as a short list (what, where, why it's worth it) and get approval before changing anything.
5. Apply the approved cleanups one logical change at a time, running the tests after each. Match the codebase's existing style — cleanup means more consistent, not more clever.
6. Verify the full test suite and lint/build are green.
7. Commit as separate `refactor:`/`chore:` commits, one per logical cleanup — never mixed with behavior changes.

## Rules

- Behavior-preserving only. If a cleanup reveals an actual bug, report it separately instead of silently fixing it mid-refactor.
- Don't expand scope mid-pass; new candidates found along the way go on the list for a future pass.
- Skip cleanups whose churn outweighs their benefit — say why instead of doing them anyway.
