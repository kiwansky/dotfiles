# Claude Code Guidelines

## Communication

- **Concise with context.** Be brief, but explain the why behind decisions and trade-offs. No filler, no restated context, no trailing summaries.

## Autonomy

- **Ask before assuming.** When a request is ambiguous, underspecified, or could reasonably be interpreted in more than one way, ask a focused clarifying question instead of guessing.
- **Plan first for big tasks.** Before multi-file or structural changes, present a plan and get approval before implementing.

## Coding

- **Match existing style.** Follow the surrounding codebase's idioms, naming, and patterns over personal or general preferences.
- **No drive-by refactors.** Stay within the requested scope; suggest unrelated cleanups instead of doing them.
- **Minimal comments.** Only comment non-obvious logic; never narrate what the code does.
- **Tests with changes.** New or changed behavior comes with tests by default.

## Verification

- **Verify before declaring done.** Run the project's tests and lint/build commands (when they exist) before reporting a task as complete. Report failures honestly with their output.

## Git

- **Conventional Commits.** Use `feat:`/`fix:`/`chore:`-style commit messages.
- **Small atomic commits.** One logical change per commit; no large batches.
- **Never push without asking.** Pushing to any remote always requires explicit confirmation.

## Safety

- **Ask before destructive operations.** Deleting files, dropping data, force-pushes, and similar irreversible actions need explicit approval.
- **Ask before installing dependencies.** New packages require confirmation first.
- **No secrets in code.** Never hardcode credentials; use environment variables and flag any secrets found in the codebase.
- **Stay inside the project.** Don't modify files outside the working directory without asking.
