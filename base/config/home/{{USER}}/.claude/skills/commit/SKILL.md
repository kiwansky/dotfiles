---
name: commit
description: Use this when committing changes to a git repository.
---

Each commit message must start with one of those prefixes:
  - feat:*: For commits related to features
  - fix:*: For commits related to bug fixes
  - test:*: For commits related to testing
  - refactor:*: For commits related to refactorings
  - chore:*: For commits related to maintenance tasks

Each commit message must contain the name of the agent (the first letter needs to be uppercase) like in this examples:
  - feat: [<AgentName>] <Message>
  - test: [<AgentName>] <Message>

Each commit must be signed, never bypass commit signing.

To do commits use git.

Never append Co-Authored-By: post-fix to any commit.

To commit use:

```bash
git commit $ARGUMENTS
```