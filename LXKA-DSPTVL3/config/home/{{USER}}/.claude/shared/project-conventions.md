# Project Management Conventions

## Project Management Tool

The project management tool is **Jira** (via the **Atlassian MCP server**). Use `mcp__atlassian__jira_*` tools for all issue-related operations.

> To switch PM tools, update this file.

## Issue Hierarchy

| Level | Issue Type | Purpose |
|-------|-----------|---------|
| Epic | `Epic` | Large body of work spanning multiple sprints |
| Story | `Story` | User-facing feature ("As a... I want... So that...") |
| Task | `Task` | Technical or non-user-facing work |
| Bug | `Bug` | Defect in existing functionality |
| Subtask | `Subtask` | Breakdown of a Story, Task, or Bug |

### Rules
- Never assume the project key — always ask the user or read it from context.
- Issue keys follow the pattern `PROJ-123` (uppercase project key + number).
- Link Stories/Tasks/Bugs to their parent Epic using `jira_link_to_epic`.
- Create Subtasks with `issue_type: "Subtask"` and `additional_fields: {"parent": "PROJ-123"}`.

## Issue Lifecycle

Always check available transitions before changing status:

1. **Get transitions**: `jira_get_transitions` — returns valid next states for the issue.
2. **Transition**: `jira_transition_issue` with the `transition_id` from step 1.

Never hardcode transition IDs — they vary per project and workflow.

## Searching (JQL)

Use `jira_search` with JQL queries. Common patterns:

| Goal | JQL |
|------|-----|
| Issues in a project | `project = PROJ` |
| Open issues assigned to me | `assignee = currentUser() AND status != Done` |
| Issues in an Epic | `parent = PROJ-123` |
| Recently updated | `project = PROJ AND updated >= -7d` |
| By label | `project = PROJ AND labels = "frontend"` |
| By sprint | `sprint in openSprints()` |
| Unresolved bugs | `project = PROJ AND issuetype = Bug AND resolution = Unresolved` |

## Writing to Issues

- Use **Markdown** for `description` and `comment` fields — the MCP server handles conversion.
- Structure user stories in the description using the format from the `product-owner` agent.
- Add acceptance criteria, design notes, and updates as **comments** (`jira_add_comment`), not by overwriting the description.
- Use **labels** for cross-cutting concerns (e.g., `frontend`, `api`, `tech-debt`).

## Sprint & Board Management

| Action | Tool |
|--------|------|
| Find boards | `jira_get_agile_boards` |
| List sprints | `jira_get_sprints_from_board` |
| Sprint issues | `jira_get_sprint_issues` |
| Add issues to sprint | `jira_add_issues_to_sprint` |
| Create sprint | `jira_create_sprint` |

## Issue Links

Use `jira_create_issue_link` for relationships between issues:

| Relationship | When to use |
|-------------|-------------|
| `Blocks` | Issue A must be resolved before B can start |
| `Relates to` | Issues are related but not dependent |
| `Duplicate` | Issues describe the same problem |

Use `jira_get_link_types` to discover available link types in the project.

## Development Info

Use `jira_get_issue_development_info` to check linked PRs, branches, and commits for an issue. This is useful during `/review` to verify code is linked to the right issue.

## MCP Server Usage

- **Issue tracking** (issues, epics, sprints, boards, JQL search): Use the **Atlassian MCP server** (`mcp__atlassian__jira_*`).
