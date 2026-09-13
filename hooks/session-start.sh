#!/usr/bin/env bash
# SessionStart hook: injects the using-superpowers skill content as context on every
# session start/clear/compact, replicating obra/superpowers' own hooks/session-start.
# Adapted for this harness: no CLAUDE_PLUGIN_ROOT (not distributed as a plugin) — the
# skill lives in this repo's own catalog/, resolved relative to the repo root.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$ROOT" ]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi
SKILL_FILE="${ROOT}/catalog/skills/using-superpowers/SKILL.md"

using_superpowers_content=$(cat "$SKILL_FILE" 2>&1 || echo "Error reading using-superpowers skill at ${SKILL_FILE}")

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

using_superpowers_escaped=$(escape_for_json "$using_superpowers_content")
session_context="<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n**Below is the full content of the 'using-superpowers' skill - your introduction to using skills. For all other skills, use the Skill tool:**\n\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"

printf '{\n  "hookSpecificOutput": {\n    "hookEventName": "SessionStart",\n    "additionalContext": "%s"\n  }\n}\n' "$session_context"

exit 0
