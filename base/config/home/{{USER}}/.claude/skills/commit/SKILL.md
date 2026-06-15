---
name: commit
description: Group the current changes into small atomic commits with Conventional Commit messages. Use when the user asks to commit, says "commit this", or wants the working tree turned into clean commits.
---

# Commit

Turn the current working tree changes into one or more atomic commits.

## Steps

1. Inspect the state: `git status` and `git diff` (plus `git diff --staged` if anything is staged). Read enough of the changes to understand what they do — never commit blind.
2. Check recent history (`git log --oneline -10`) to match the repository's existing message conventions if they deviate from the defaults below.
3. Group the changes into logical units — one logical change per commit. If unrelated changes are mixed in one file, use `git add -p` style staging to separate them. Never use `git add -A` blindly.
4. For each group, stage the files and commit with a Conventional Commit message:
   - Format: `<type>(<optional scope>): <imperative summary>`
   - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`, `build`
   - Summary ≤ 72 chars, lowercase, no trailing period. Add a body only when the why isn't obvious from the diff.
   - If the work relates to an item in the project's issue tracker, reference it using that tracker's convention (resolve the tracker from the project's CLAUDE.md or project memory).
5. Verify with `git log --oneline` and `git status` that everything intended is committed and nothing unintended is.

## Rules

- Never push. Pushing requires a separate, explicit request.
- Never commit files that look like secrets, credentials, or local config (.env, keys). Flag them instead.
- If the changes can't be cleanly separated, ask the user how to split them rather than guessing.
- Do not amend or rewrite existing commits unless explicitly asked.
