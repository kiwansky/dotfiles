---
name: pr
description: Push the current branch (with confirmation) and open a change request (pull request / merge request) with a structured description. Use when the user asks to create a PR, MR, or change request, or to "open a pull request".
---

# Change Request (PR / MR)

Publish the current branch and open a change request on the project's code hosting platform.

## Determine the platform

Resolve the platform and tooling from, in order: the project's CLAUDE.md, project memory, then `git remote -v`. Use the matching CLI or MCP tools (e.g. `gh` for GitHub, `glab` for GitLab). If the platform or tooling is unclear, ask.

## Steps

1. Verify the state: current branch (never the default branch — create one if needed), all intended changes committed, working tree clean.
2. Run the project's tests and lint/build before publishing. If they fail, report the failures and stop — don't open a change request on a red build.
3. Review what the change request will contain: `git log` and `git diff` against the target branch.
4. **Ask for confirmation before pushing.** Pushing is never done silently.
5. Create the change request with:
   - **Title**: Conventional Commit style summary of the overall change.
   - **Summary**: what changed and why, 2–4 sentences.
   - **Changes**: bullet list of the notable changes.
   - **Test plan**: how the change was verified (commands run, manual checks).
   - A reference to the related item in the project's issue tracker, if one exists, using that tracker's linking convention.
6. Return the URL of the created change request.

## Rules

- Match any change request template the repository defines (e.g. in `.github/`, `.gitlab/`, or `docs/`) — the template wins over the structure above.
- Target the repository's default integration branch unless told otherwise.
- Never force-push without explicit approval.
