# Claude Code Guidelines

## General Behavior

Ask clarifying questions when needed — including from sub-agents.

## Conventions

@~/.claude/shared/git-conventions.md
@~/.claude/shared/project-conventions.md
@~/.claude/shared/software-development-process.md

## Sub-Agent Delegation

Always delegate to the matching sub-agent listed in `shared/software-development-process.md`. If no sub-agent exists for a role the task needs, recommend creating one before proceeding.

## Engineering Principles

Loaded on demand by the relevant agents. See `~/.claude/shared/` for: `clean-code-principles`, `pragmatism-principles`, `security-principles`, `observability-standards`, `accessibility-standards`, `agent-memory-system`.

## Phase Approval

Every multi-phase skill MUST enforce the gate in `~/.claude/shared/approval-beat.md` before advancing between phases and before suggesting any next command.
