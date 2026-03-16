#!/bin/bash
set -euo pipefail

CLAUDE_JSON="$HOME/.claude.json"

GITHUB_MCP='{
  "type": "http",
  "url": "https://api.githubcopilot.com/mcp",
  "headers": {
    "Authorization": "Bearer {GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}'

GIT_MCP='{
  "type": "stdio",
  "command": "npx",
  "args": ["@cyanheads/git-mcp-server@latest"],
  "env": {
    "MCP_TRANSPORT_TYPE": "stdio",
    "MCP_LOG_LEVEL": "info",
    "LOGS_DIR": "~/Source/logs/git-mcp-server/",
    "GIT_USERNAME": "Keven - Yannic Iwansky",
    "GIT_EMAIL": "keven.iwansky@gmail.com",
    "GIT_SIGN_COMMITS": "true"
  }
}'

# Create ~/.claude.json with empty object if it does not exist
if [ ! -f "$CLAUDE_JSON" ]; then
  echo '{}' > "$CLAUDE_JSON"
fi

# Ensure mcpServers key exists
if ! jq -e '.mcpServers' "$CLAUDE_JSON" > /dev/null 2>&1; then
  tmp=$(mktemp)
  jq '.mcpServers = {}' "$CLAUDE_JSON" > "$tmp" && mv "$tmp" "$CLAUDE_JSON"
fi

# Add github MCP server if not already matching (ignore Authorization header in comparison)
current_github=$(jq -c 'del(.mcpServers.github.headers.Authorization) | .mcpServers.github // empty' "$CLAUDE_JSON")
expected_github=$(echo "$GITHUB_MCP" | jq -c 'del(.headers.Authorization)')
if [ "$current_github" != "$expected_github" ]; then
  tmp=$(mktemp)
  full_github=$(echo "$GITHUB_MCP" | jq -c '.')
  jq --argjson val "$full_github" '.mcpServers.github = $val' "$CLAUDE_JSON" > "$tmp" && mv "$tmp" "$CLAUDE_JSON"
  echo "Added/updated mcpServers.github in $CLAUDE_JSON"
else
  echo "mcpServers.github already up to date in $CLAUDE_JSON"
fi

# Add git MCP server if not already matching
current_git=$(jq -c '.mcpServers.git // empty' "$CLAUDE_JSON")
expected_git=$(echo "$GIT_MCP" | jq -c '.')
if [ "$current_git" != "$expected_git" ]; then
  tmp=$(mktemp)
  jq --argjson val "$expected_git" '.mcpServers.git = $val' "$CLAUDE_JSON" > "$tmp" && mv "$tmp" "$CLAUDE_JSON"
  echo "Added/updated mcpServers.git in $CLAUDE_JSON"
else
  echo "mcpServers.git already up to date in $CLAUDE_JSON"
fi
