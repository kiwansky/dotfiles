#!/bin/bash
set -euo pipefail

CLAUDE_JSON="$HOME/.claude.json"

ATLASSIAN_MCP='{
  "command": "uvx",
  "args": [
    "mcp-atlassian"
  ],
  "env": {
    "CONFLUENCE_URL": "{CONFLUENCE_URL}",
    "CONFLUENCE_PERSONAL_TOKEN": "{CONFLUENCE_API_TOKEN}",
    "JIRA_URL": "{JIRA_URL}",
    "JIRA_PERSONAL_TOKEN": "{JIRA_API_TOKEN}"
  }
}'

# Ensure ~/.claude.json and mcpServers key exist (base hook creates these,
# but guard in case this hook runs standalone)
if [ ! -f "$CLAUDE_JSON" ]; then
  echo '{}' > "$CLAUDE_JSON"
fi

if ! jq -e '.mcpServers' "$CLAUDE_JSON" > /dev/null 2>&1; then
  tmp=$(mktemp)
  jq '.mcpServers = {}' "$CLAUDE_JSON" > "$tmp" && mv "$tmp" "$CLAUDE_JSON"
fi

# Add atlassian MCP server if not already matching
current_atlassian=$(jq -c '.mcpServers.atlassian // empty' "$CLAUDE_JSON")
expected_atlassian=$(echo "$ATLASSIAN_MCP" | jq -c '.')
if [ "$current_atlassian" != "$expected_atlassian" ]; then
  tmp=$(mktemp)
  jq --argjson val "$expected_atlassian" '.mcpServers.atlassian = $val' "$CLAUDE_JSON" > "$tmp" && mv "$tmp" "$CLAUDE_JSON"
  echo "Added/updated mcpServers.atlassian in $CLAUDE_JSON"
else
  echo "mcpServers.atlassian already up to date in $CLAUDE_JSON"
fi
