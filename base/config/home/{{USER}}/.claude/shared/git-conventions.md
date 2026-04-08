# Git Conventions

## Branching Strategy (GitFlow)

Always use **GitFlow** branching. Always include the issue ID in the branch name.

| Branch | Branched From | Merged Back Into | Naming Pattern |
|--------|--------------|-----------------|----------------|
| `main` | — | — | `main` |
| `develop` | `main` | — | `develop` |
| `feature` | `develop` | `develop` | `feature/<issue-id>-<short-description>` |
| `bugfix` | `develop` | `develop` | `bugfix/<issue-id>-<short-description>` |
| `release` | `develop` | `main` + `develop` | `release/<version>` |
| `hotfix` | `main` | `main` + `develop` | `hotfix/<issue-id>-<short-description>` |

**Examples:**
- `feature/42-add-user-authentication`
- `bugfix/87-fix-token-expiry`
- `hotfix/99-critical-login-crash`
- `release/1.3.0`

### Rules
- Never commit directly to `main` or `develop`.
- Release branches are version-named, not issue-named (but may reference a milestone).
- After merging a release or hotfix into `main`, tag the commit with the version.
- Use semantic versioning.
- Each issue that is worked on needs to have its own pull request.
- Always ensure your changes are committed and pushed when you are done.

## Commit Conventions

Make **small, logically grouped commits**. Each commit should represent a single coherent change. Reference the issue ID in every commit message.

### Conventional Commit Format

```
<type>(<scope>): <short description> [#<issue-id>]

[optional body]

[optional footer]
```

### Commit Types

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructuring, no behavior change |
| `test` | Adding or updating tests |
| `chore` | Build process, dependency updates |
| `ci` | CI/CD pipeline changes |
| `perf` | Performance improvement |

**Examples:**
- `feat(auth): add JWT refresh token support [#42]`
- `fix(api): handle null response from payment gateway [#87]`
- `test(auth): add acceptance tests for login flow [#42]`
- `ci: add deployment step for staging environment [#55]`

### Rules
- Keep commits small and focused — one logical change per commit.
- Always reference the issue ID using `[#<issue-id>]` at the end of the subject line.
- Write the subject in the imperative mood ("add", not "added" or "adds").
- Limit the subject line to 72 characters.
- Never append `Co-Authored` information to commit messages.

## MCP Server Usage

- **Git operations** (branching, commits, log, status, etc.): Use the **git MCP server**.
- **GitHub operations** (issues, PRs, reviews, labels, etc.): Use the **GitHub MCP server**.
