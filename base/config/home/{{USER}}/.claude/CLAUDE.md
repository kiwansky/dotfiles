# Claude Code Guidelines

## General Behavior

Ask clarifying questions when needed. Sub-agents and agent teams should also ask clarifying questions when needed.

## Conventions

@~/.claude/shared/git-conventions.md
@~/.claude/shared/project-conventions.md
@~/.claude/shared/software-development-process.md

## Engineering Principles (referenced by sub-agents)

These are loaded by the relevant agents directly. Listed here for awareness:

- `shared/clean-code-principles.md` — Clean Code, SOLID, KISS
- `shared/pragmatism-principles.md` — YAGNI, when to *not* apply Clean Code strictly
- `shared/security-principles.md` — STRIDE, OWASP Top 10, secrets, auth, crypto
- `shared/observability-standards.md` — Logs, metrics, traces, SLOs, alerts, runbooks, postmortems
- `shared/accessibility-standards.md` — WCAG 2.1 AA baseline, ARIA, assistive-tech testing
- `shared/agent-memory-system.md` — Persistent memory shared across all agents

---

## Sub-Agent Delegation

**Always delegate tasks to the matching sub-agent.** Do not perform tasks yourself that belong to a defined sub-agent role.

| Task | Sub-Agent |
|------|-----------|
| Product vision, strategy, positioning, roadmap | `product-manager` |
| User stories, backlog management, acceptance-criteria placeholders | `product-owner` |
| Detailed acceptance criteria (Gherkin / SMART / INVEST) | `requirements-engineer` |
| Architectural design and ADRs | `software-architect` |
| API specification design | `api-designer` |
| Database schema, migrations, query performance | `database-engineer` |
| UI/UX design (wireframes, flows, baseline a11y) | `ui-ux-engineer` |
| Accessibility audits and complex inclusive patterns | `accessibility-specialist` |
| Implementation | `software-engineer` |
| Tests (writing, reviewing, pyramid balance) | `test-engineer` |
| CI/CD pipelines, build, deploy automation | `ci-cd-engineer` |
| Site reliability, observability, alerts, runbooks, postmortems | `sre` |
| Application security, threat modelling, dependency CVEs | `security-engineer` |
| Code review (bugs, quality, architecture lenses) | `code-reviewer` |
| Documentation, README, ADR write-up, user-facing copy | `technical-writer` |
| Planning implementation approach | `Plan` (built-in) |
| Codebase exploration and search | `Explore` (built-in) |

If a task requires a role that has no matching sub-agent, **recommend creating a custom sub-agent** for that specific role before proceeding.

---

## Slash Commands

The development pipeline is implemented as slash commands. Each command orchestrates a team of sub-agents and produces specific artifacts.

### Strategy
| Command | Purpose |
|---------|---------|
| `/product-vision` | Produce a 3–5 year product vision, narrative, and supporting artifacts under `/docs/product/`, on a `vision/` branch |
| `/discovery` | Lightweight problem validation for a single feature/opportunity — produces a build / build-small / postpone / drop recommendation |
| `/roadmap` | Build or refresh a Now / Next / Later roadmap tied to vision and strategic pillars |

### Definition
| Command | Purpose |
|---------|---------|
| `/story` | Quickly create or update a user story (placeholder ACs) in the issue tracker |
| `/refine` | Full refinement: stories, detailed acceptance criteria, early UX/arch notes |
| `/triage` | Triage incoming bugs/issues — reproduce, classify severity, label, route to next command |

### Design
| Command | Purpose |
|---------|---------|
| `/design` | Architecture, ADRs, API spec, data design, UI/UX, security threat model, on the feature branch |
| `/spike` | Time-boxed investigation for uncertain areas — produces a recommendation, not code |

### Build
| Command | Purpose |
|---------|---------|
| `/implement` | Code + tests following architecture and acceptance criteria |
| `/test` | Focused test-writing or review pass with pyramid-balance check |
| `/refactor` | Scoped, risk-assessed refactor on a `refactor/` branch with a safety-net of characterization tests |

### Validate
| Command | Purpose |
|---------|---------|
| `/review` | Multi-lens PR review (bugs, quality, architecture, security, plus database / a11y / sre as needed), with explicit disagreement resolution |
| `/security-review` | Built-in: security review of pending changes on the current branch |

### Operate
| Command | Purpose |
|---------|---------|
| `/cicd` | Set up or update the CI/CD pipeline — assess, design, implement, validate |
| `/document` | Audit and update project documentation, structured by Diátaxis |
| `/onboard` | Generate or refresh contributor onboarding docs (CONTRIBUTING, setup, testing, security) |
| `/audit-deps` | Dependency audit — CVEs, drift, licenses — with prioritized upgrade plan |
| `/release` | Prepare a release: readiness check, changelog, version bump, merge, tag |
| `/postmortem` | Blameless incident postmortem with action items in the tracker |

### Typical flows

- **New feature**: `/story` → `/refine` → `/design` → `/implement` → `/test` → `/review` → `/document` → `/release`
- **Strategic initiative**: `/product-vision` → `/roadmap` → `/refine` (per pillar) → standard feature flow
- **Risky idea**: `/discovery` → (build / drop) → standard feature flow if proceeding
- **Bug**: `/triage` → `/refine` → `/implement` → `/test` → `/review` → `/release` (hotfix if critical)
- **Incident**: `/postmortem` → `/refine` (per action item) → standard feature flow per item
- **Investigation**: `/spike` → `/refine` (informed by spike) → standard feature flow
- **Cleanup**: `/refactor` (preserves behavior) → `/review`

The full pipeline diagram and phase-by-phase ownership lives in `shared/software-development-process.md`.
