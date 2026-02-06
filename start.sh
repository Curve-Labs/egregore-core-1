#!/bin/bash
cd "$(dirname "$0")"

missing=()
command -v git    >/dev/null || missing+=("git — https://git-scm.com")
command -v claude >/dev/null || missing+=("claude — npm install -g @anthropic-ai/claude-code")
command -v jq     >/dev/null || missing+=("jq — brew install jq")

if [ ${#missing[@]} -gt 0 ]; then
  echo "Missing prerequisites:"
  for m in "${missing[@]}"; do echo "  ✗ $m"; done
  exit 1
fi

exec claude "hello"
