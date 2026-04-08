# Claude Code Guidelines

## General Behavior

Ask clarifying questions when needed. Also sub-agents and agent teams should ask clarifying questions when needed.

## Git Branching

Use **GitFlow** branching strategy. Always include the issue ID in the branch name.

### Branch Types and Patterns

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

---

## Git Commits

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

---

## Sub-Agent Delegation

**Always delegate tasks to the matching sub-agent.** Do not perform tasks yourself that belong to a defined sub-agent role.

| Task | Sub-Agent |
|------|-----------|
| Creating/refining user stories, backlog management | `product-owner` |
| Defining and documenting acceptance criteria | `requirements-engineer` |
| Architectural design and documentation | `software-architect` |
| API specification design | `api-designer` |
| UI/UX design | `ui-ux-engineer` |
| Implementation | `software-engineer` |
| Writing tests, acceptance test coverage | `test-engineer` |
| CI/CD pipeline setup and adjustments | `ci-cd-engineer` |
| Documentation consistency and README updates | `technical-writer` |
| Code review | `code-reviewer` |
| Planning implementation approach | `Plan` |
| Codebase exploration | `Explore` |

If a task requires a role that has no matching sub-agent, **recommend creating a custom sub-agent** for that specific role before proceeding.

---

## Software Development Skills

The development process is implemented as slash commands. Use them in sequence or independently:

| Skill | Command | Purpose |
|-------|---------|---------|
| User Story | `/story` | Create or update a user story in the issue tracker |
| Refinement | `/refine` | Full refinement: user stories, acceptance criteria, early UX/arch notes |
| Design | `/design` | Architecture, ADRs, API spec, and documentation |
| Implementation | `/implement` | Code + tests following architecture and acceptance criteria |
| Testing | `/test` | Focused test-writing or test-review pass on existing code |
| Review | `/review` | Full review cycle: PR creation, code review, address findings |
| CI/CD | `/cicd` | Set up or update the CI/CD pipeline |
| Documentation | `/document` | Audit and update project documentation |
| Release | `/release` | Prepare a release: changelog, version bump, merge, tag |
| Spike | `/spike` | Time-boxed investigation for uncertain areas |

**Typical flow**: `/story` → `/refine` → `/design` → `/implement` → `/review` → `/document`

---

## MCP Server Usage

- **Git operations** (branching, commits, log, status, etc.): Use the **git MCP server**.
- **GitHub operations** (issues, PRs, reviews, labels, etc.): Use the **GitHub MCP server**.
