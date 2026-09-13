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

# JSON encoding vai pro python (json.dumps) em vez de escape manual em bash, que não
# cobre corretamente todos os caracteres de controle/unicode.
if [ -f "$SKILL_FILE" ]; then
  cat "$SKILL_FILE"
else
  echo "Error reading using-superpowers skill at ${SKILL_FILE}"
fi | python3 - << 'PY'
import json
import sys

sys.stdout.reconfigure(newline="\n")
content = sys.stdin.read()
session_context = (
    "<EXTREMELY_IMPORTANT>\n"
    "You have superpowers.\n\n"
    "**Below is the full content of the 'using-superpowers' skill - your "
    "introduction to using skills. For all other skills, use the Skill "
    "tool:**\n\n"
    f"{content}\n"
    "</EXTREMELY_IMPORTANT>"
)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": session_context,
    }
}, ensure_ascii=False))
PY

exit 0
