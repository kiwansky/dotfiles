---
name: branch
description: Use this when interacting with git branches.
---

Each branch needs to follow the naming patterns, depending on what kind of work is done in this branch:
    - feat/<Issue>_<Description>: Feature branch
    - fix/<Issue>_<Description>: Bug fix branch
    - refactor/<Issue>_<Description>: Refactoring branch
    - chore/<Issue>_<Description>: Maintenance branch

To create a new branch use:

```bash
git branch $ARGUMENTS
```