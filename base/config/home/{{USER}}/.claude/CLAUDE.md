# Claude Code Guidelines

## General Behavior

Ask clarifying questions when needed. Also sub-agents and agent teams should ask clarifying questions when needed.

## Git and Project Conventions

@/home/kyi/.claude/shared/git-conventions.md
@/home/kyi/.claude/shared/project-conventions.md

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

