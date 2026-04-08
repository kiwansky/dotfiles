## Git Workflow (Strictly Enforced)

### Branching: Git Flow

The project follows Git Flow with the following branch structure:

| Branch | Purpose | Branches from | Merges into |
|---|---|---|---|
| `main` | Production releases only — always tagged | `release/` or `hotfix/` | — |
| `dev` | Integration branch — base for all development | — | `main` (via `release/`) |
| `feat/<issue-number>-<description>` | New feature work | `dev` | `dev` |
| `fix/<issue-number>-<description>` | Bug fix | `dev` | `dev` |
| `refactor/<description>` | Refactoring without behavior change | `dev` | `dev` |
| `chore/<description>` | Maintenance, config, dependencies | `dev` | `dev` |
| `release/<version>` | Release stabilization | `dev` | `dev` + `main` (tagged) |
| `hotfix/<issue-number>-<description>` | Critical production fix | `main` | `main` (tagged) + `dev` |

Rules:
- Always branch feature/fix/refactor/chore work from `dev`, never from `main`.
- Never commit directly to `main` or `dev`.
- `main` is always in a releasable state and every merge to it is tagged with a semantic version.

### Commits: Conventional Commits
Every commit message MUST be prefixed with one of:
- `feat:` — New feature or functionality
- `fix:` — Bug fix
- `chore:` — Maintenance tasks, dependency updates, configuration
- `refactor:` — Code restructuring without behavior change
- `doc:` — Documentation changes

Commit messages must be concise, descriptive, and written in imperative mood (e.g., `feat: add JWT token validation middleware`).

Rules:
- All commits MUST be GPG-signed. Never skip signing or use `--no-gpg-sign`.

### Commit Strategy
- **Small, logically grouped commits**: Each commit should represent one logical change. Do NOT bundle unrelated changes into a single commit.
- Group related file changes together (e.g., a new service class and its unit tests in one commit).
- Typical commit sequence for a feature:
  1. `feat: add <domain model/interface>`
  2. `feat: implement <service/logic>`
  3. `feat: add unit tests for <service/logic>`
  4. `refactor: extract <shared utility>` (if applicable)
  5. `doc: update <relevant documentation>` (if applicable)

### Pull Policy
- Always ensure the latest changes are pulled from remote before starting work.

### Push Policy
- Always ensure ALL work is committed and pushed before reporting completion.
- Verify with `mcp__git__git_status` that the working directory is clean.
- Verify with `mcp__git__git_log` that commits are properly formatted.

## Tool Requirements (Strictly Enforced)

- **Git operations**: Always use Git MCP tools (`mcp__git__git_*`) — never `git` CLI commands via Bash.
- **GitHub operations**: Always use GitHub MCP tools (`mcp__github__*`) — never the `gh` CLI.
- **Local-only projects**: Do not create GitHub repositories, issues, or any remote resources for projects that are explicitly local-only. Only set up GitHub when remote hosting, collaboration, or issue tracking is explicitly required.
