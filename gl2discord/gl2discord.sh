#!/usr/bin/env bash
# GitLens to Discord notification script
# Usage: ./gl2discord.sh CHANNEL_ID TITLE [BODY] [COLOR]
#
# LLM Directive: This script sends notifications from GitLens/VS Code to Discord.
# Extend to support:
# - Different embed formats
# - File attachments
# - Interactive buttons
set -euo pipefail

CHANNEL_ID="$1"
TITLE="$2"
BODY="${3:-}"
COLOR="${4:-0x2f81f7}"

if [[ -z "${DISCORD_TOKEN:-}" ]]; then
    echo "Error: DISCORD_TOKEN environment variable not set" >&2
    exit 1
fi

curl -sS -H "Authorization: Bot $DISCORD_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -d "$(jq -n --arg t "$TITLE" --arg b "$BODY" --argjson c "$COLOR" \
        '{embeds:[{title:$t, description:$b, color:$c}]}')"
