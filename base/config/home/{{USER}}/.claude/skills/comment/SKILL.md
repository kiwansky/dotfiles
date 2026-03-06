---
name: comment
description: Use this when commenting on a pull requests on github.
---

Each comment must contain the name of the agent (the first letter needs to be uppercase) like in this examples:
  - [**<Agent>**] <Comment>

Comments that are tied to a specific part of the code should be added to this specific lines of codes in the pull request.

Comments that are on a broader scale should be documented in the pull request overview.

To create comments use:

```bash
gh pr review --commment $ARGUMENTS
```