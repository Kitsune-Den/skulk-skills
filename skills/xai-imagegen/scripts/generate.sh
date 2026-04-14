#!/usr/bin/env bash
# xAI Image Generation — generate an image from a text prompt
# Usage: ./generate.sh "your prompt here" [output_path]
# Requires: XAI_API_KEY env var or ~/.config/xai/credentials.json

set -euo pipefail

PROMPT="${1:?Usage: generate.sh \"prompt\" [output_path]}"
OUTPUT="${2:-/tmp/xai-generated-$(date +%s).jpg}"

# Resolve API key
if [ -z "${XAI_API_KEY:-}" ]; then
  CRED_FILE="$HOME/.config/xai/credentials.json"
  if [ -f "$CRED_FILE" ]; then
    XAI_API_KEY=$(jq -r '.api_key' "$CRED_FILE")
  else
    echo "ERROR: No XAI_API_KEY env var and no $CRED_FILE found." >&2
    echo "Get your key at https://console.x.ai" >&2
    exit 1
  fi
fi

# Generate image
RESPONSE=$(curl -s -X POST "https://api.x.ai/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d "{
    \"model\": \"grok-imagine-image\",
    \"prompt\": $(echo "$PROMPT" | jq -Rs .)
  }")

# Extract URL
URL=$(echo "$RESPONSE" | jq -r '.data[0].url // empty')

if [ -z "$URL" ]; then
  echo "ERROR: Image generation failed." >&2
  echo "$RESPONSE" | jq '.' >&2
  exit 1
fi

# Download (URLs are temporary)
curl -s -o "$OUTPUT" "$URL"
echo "$OUTPUT"
