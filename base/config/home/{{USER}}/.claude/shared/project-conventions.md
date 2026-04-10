# Project Management Conventions

## Project Management Tool

The project management tool is **GitHub Issues** (via the **GitHub MCP server**). Use `mcp__github__issue_*`, `mcp__github__search_issues`, and `mcp__github__list_issues` tools for all issue-related operations.

> To switch PM tools, update this file.

## Issue Structure

GitHub Issues uses a flat model with labels and sub-issues for hierarchy:

| Concept | GitHub Mechanism |
|---------|-----------------|
| Epic | Issue with `epic` label + sub-issues |
| Story | Issue with `story` label ("As a... I want... So that...") |
| Task | Issue with `task` label |
| Bug | Issue with `bug` label |
| Subtask | Sub-issue linked via `sub_issue_write` |

### Rules
- Every issue requires `owner` and `repo` — never assume these, ask the user or read from git remote.
- Issues are referenced by number (`#123`), not keys.
- Use **labels** to categorize issue types (`epic`, `story`, `task`, `bug`) and cross-cutting concerns (`frontend`, `api`, `tech-debt`).
- Link sub-issues to parent issues using `sub_issue_write` with `method: "add"`.
- Use `list_issue_types` to check if the repository/org supports typed issues before using the `type` field.

## Issue Lifecycle

GitHub Issues have two states: `open` and `closed`.

- **Close as completed**: `issue_write` with `state: "closed"`, `state_reason: "completed"`.
- **Close as not planned**: `issue_write` with `state: "closed"`, `state_reason: "not_planned"`.
- **Close as duplicate**: `issue_write` with `state: "closed"`, `state_reason: "duplicate"`, `duplicate_of: <issue_number>`.
- **Reopen**: `issue_write` with `state: "open"`.

## Searching Issues

Use `search_issues` with GitHub search syntax. Common patterns:

| Goal | Query |
|------|-------|
| Open issues in repo | `repo:owner/repo is:open` |
| By label | `repo:owner/repo label:bug is:open` |
| Assigned to me | `repo:owner/repo assignee:@me is:open` |
| By milestone | `repo:owner/repo milestone:"v1.0"` |
| Recently updated | `repo:owner/repo is:open sort:updated-desc` |
| By keyword | `repo:owner/repo "search term" in:title,body` |
| Unassigned bugs | `repo:owner/repo label:bug no:assignee is:open` |

Use `list_issues` for simpler filtered listing (by state, labels, since date).

## Writing to Issues

- Use **Markdown** for issue `body` and comment `body` fields.
- Structure user stories in the body using the format from the `product-owner` agent.
- Add acceptance criteria, design notes, and updates as **comments** (`add_issue_comment`), not by overwriting the body.
- Use **labels** liberally — they replace the role of components, priorities, and categories.
- Use **milestones** to group issues into releases or sprints.
- Use **assignees** to indicate ownership (supports multiple assignees).

## Milestones (Sprint / Release Tracking)

GitHub milestones serve as sprint or release containers:

- Group issues into a milestone to track progress toward a release or sprint goal.
- Milestones have a title, description, and optional due date.
- Use milestone filtering in `search_issues` to find all work for a given sprint/release.

## Issue Relationships

| Relationship | How to express |
|-------------|----------------|
| Parent / child | `sub_issue_write` with `method: "add"` |
| Duplicate | Close with `state_reason: "duplicate"` and `duplicate_of` |
| Related | Reference in a comment: "Related to #456" |
| Blocks | Note in comment: "Blocked by #789" (no native blocking) |

Use `issue_read` with `method: "get_sub_issues"` to list child issues.

## MCP Server Usage

- **Issue tracking** (issues, labels, milestones, sub-issues, search): Use the **GitHub MCP server** (`mcp__github__issue_*`, `mcp__github__search_issues`, `mcp__github__list_issues`).
