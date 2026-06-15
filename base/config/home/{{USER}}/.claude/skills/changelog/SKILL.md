---
name: changelog
description: Generate or update a changelog entry from commits since the last release/tag. Use when the user asks to update the changelog, write release notes, or summarize what changed since the last version.
---

# Changelog

Turn the commit history since the last release into a changelog entry.

## Steps

1. Find the reference point: the latest tag (`git describe --tags --abbrev=0`) or, if the project is untagged, ask what range to cover.
2. Collect the commits since then: `git log <ref>..HEAD --oneline --no-merges`. Read individual commits where the summary alone isn't clear.
3. Locate the existing changelog (`CHANGELOG.md` or equivalent) and match its established format exactly — section names, heading levels, link style. If none exists, use the Keep a Changelog format (`Added` / `Changed` / `Fixed` / `Removed` / `Deprecated` / `Security`).
4. Map Conventional Commit types onto the sections (`feat` → Added, `fix` → Fixed, etc.). Write entries for the reader, not the committer: describe user-visible impact, not internal mechanics. Drop pure noise (`chore`, CI tweaks) unless user-relevant.
5. Where commits reference items in the project's issue tracker, carry those references into the entries using the changelog's existing linking style.
6. Add the entry under an `Unreleased` heading unless the user names a version. Don't invent version numbers — if a version bump is needed, ask which one.
7. Show the resulting entry. Commit only if asked.

## Rules

- Never rewrite published changelog sections for past releases; only append or extend `Unreleased`/the named version.
- If the commit history is too vague to write meaningful entries, say so and list the commits that need clarification instead of padding with guesses.
