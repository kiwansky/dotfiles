# Software Development Process

A canonical, command-driven development pipeline. Each phase has a matching slash command and a clear handoff to the next.

## The Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Vision   │──▶│ Discovery│──▶│ Roadmap  │──▶│ Refine   │──▶│ Design   │──▶│ Implement│
│ /vision  │   │/discovery│   │/roadmap  │   │/refine   │   │/design   │   │/implement│
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                                                  │
┌──────────┐   ┌──────────┐   ┌──────────┐                                       │
│ Release  │◀──│  Review  │◀──│   Test   │◀──────────────────────────────────────┘
│ /release │   │ /review  │   │  /test   │
└──────────┘   └──────────┘   └──────────┘
```

## Phases

Each phase has an owner (lead agent), inputs, outputs, and a successor command.

### Phase 0 — Strategy
Establish *why* and *for whom*. Long-horizon work that may run for weeks.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| Vision | `/product-vision` | `product-manager` | `/docs/product/vision.md` + supporting artifacts | `vision/<slug>` |
| Discovery | `/discovery` | `product-manager` | `/docs/product/discovery/<topic>.md` | `vision/<slug>` or `discovery/<slug>` |
| Roadmap | `/roadmap` | `product-manager` + `software-architect` | `/docs/product/roadmap.md` | `vision/<slug>` |

### Phase 1 — Definition
Translate strategy into executable units of work.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| Story | `/story` | `product-owner` | GitHub Issue with user story | none (issue tracker) |
| Refine | `/refine` | `product-owner` + `requirements-engineer` | Issue body with stories + acceptance criteria | none |

### Phase 2 — Design
Decide *how* before building.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| Design | `/design` | `software-architect` (+ `api-designer`, `ui-ux-engineer`, `database-engineer` as needed) | ADR, architecture doc, API spec, UI/UX spec | `feature/<issue-id>-<slug>` |
| Spike | `/spike` | `software-architect` | `/docs/spikes/<topic>.md` (recommendation, not code) | `spike/<topic>` |

### Phase 3 — Build
Write the code and the tests.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| Implement | `/implement` | `software-engineer` | Code + tests on the design branch | `feature/<issue-id>-<slug>` |
| Test | `/test` | `test-engineer` | New/updated tests | same branch |
| Refactor | `/refactor` | `software-architect` (plan) + `software-engineer` (execute) | Refactored code on a dedicated branch | `refactor/<scope>` |

### Phase 4 — Validate
Independent quality gates before merge.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| Review | `/review` | `code-reviewer` × 4 lenses + `security-engineer` + `software-engineer` | PR with all findings addressed | feature branch → PR to `develop` |
| Security review | `/security-review` (built-in) | `security-engineer` | Security review report | same |

### Phase 5 — Operate
Ship, monitor, learn.

| Phase | Command | Lead Agent | Output | Branch |
|-------|---------|-----------|--------|--------|
| CI/CD | `/cicd` | `ci-cd-engineer` | Pipeline updates | feature branch |
| Release | `/release` | `technical-writer` (changelog) + `ci-cd-engineer` | Tagged release on `main` | `release/<version>` |
| Documentation | `/document` | `technical-writer` | README, `/docs/*` updates | feature branch |
| Triage | `/triage` | `product-owner` + `code-reviewer` | Labelled, prioritised issues | none |
| Postmortem | `/postmortem` | `sre` + `technical-writer` | `/docs/postmortems/<date>-<slug>.md` | `postmortem/<slug>` |
| Audit dependencies | `/audit-deps` | `ci-cd-engineer` + `security-engineer` | `/docs/audits/deps-<date>.md` + upgrade plan | `chore/audit-deps-<date>` |
| Onboarding docs | `/onboard` | `technical-writer` | CONTRIBUTING.md, dev-setup, etc. | `chore/onboarding-<date>` |

## Handoff Rules

- **Each command should end with a suggested next command.** This keeps the pipeline visible.
- **Branch continuity**: `/design` and `/implement` use the *same* feature branch — design artifacts and code ship together.
- **Branch isolation**: `vision/`, `spike/`, `refactor/`, `postmortem/`, `chore/` work happens on their own branches and is merged independently.
- **One issue, one PR.** A feature branch terminates in exactly one PR back to `develop`.
- **Never commit to `main` or `develop` directly.** See `git-conventions.md`.

## Choosing the Right Command

| Situation | Command |
|-----------|---------|
| "Where should the product be in 3 years?" | `/product-vision` |
| "Should we build feature X?" (validate before committing) | `/discovery` |
| "What are we doing this quarter?" | `/roadmap` |
| "Quick — capture this idea as a story" | `/story` |
| "Make this story implementation-ready" | `/refine` |
| "I'm not sure technically how to do this" | `/spike` |
| "Plan the technical approach" | `/design` |
| "Build it" | `/implement` |
| "Add tests to existing code" | `/test` |
| "Clean up this code" | `/refactor` |
| "Open and run a PR review" | `/review` |
| "Audit security on the current branch" | `/security-review` |
| "Audit dependencies for vulnerabilities or drift" | `/audit-deps` |
| "Set up or update the CI/CD pipeline" | `/cicd` |
| "Update the docs to match reality" | `/document` |
| "Help a new contributor get set up" | `/onboard` |
| "Cut a release" | `/release` |
| "Triage incoming bugs" | `/triage` |
| "Write a postmortem for this incident" | `/postmortem` |

## Command Composition

Most non-trivial work flows through multiple commands. Common chains:

- **New feature**: `/story` → `/refine` → `/design` → `/implement` → `/test` → `/review` → `/document` → `/release`
- **Strategic initiative**: `/product-vision` → `/roadmap` → `/refine` (per pillar) → … (then standard feature flow)
- **Bug**: `/triage` → `/refine` → `/implement` → `/test` → `/review` → `/release` (hotfix if critical)
- **Incident**: `/postmortem` → `/refine` (action items) → standard feature flow per item
- **Investigation**: `/spike` → `/refine` (informed by spike) → standard feature flow
