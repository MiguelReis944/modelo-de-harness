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
# cobre corretamente todos os caracteres de controle/unicode. O caminho do arquivo
# viaja por argv, não por pipe: `cmd | python3 - <<'PY'` combina um pipe com um
# heredoc no mesmo stdin — o heredoc vence (fornece o código-fonte do script) e
# `sys.stdin.read()` dentro dele lê string vazia (SC2259), então o conteúdo do skill
# nunca chegava ao additionalContext.
python3 - "$SKILL_FILE" << 'PY'
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", newline="\n")
skill_path = sys.argv[1]
try:
    with open(skill_path, encoding="utf-8") as f:
        content = f.read()
except OSError as e:
    content = f"Error reading using-superpowers skill at {skill_path}: {e}"

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
