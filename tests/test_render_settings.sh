#!/usr/bin/env bash
# render_settings.py: sobrescreve os eventos declarados em hooks.json, preserva o resto.
set -euo pipefail
cd "$(dirname "$0")/.."

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cat > "$tmp/hooks.json" << 'JSON'
{
  "hooks": {
    "SessionStart": [
      {"matcher": "startup", "hooks": [{"type": "command", "command": "new-hook"}]}
    ]
  }
}
JSON

cat > "$tmp/settings.json" << 'JSON'
{
  "permissions": {"allow": ["Bash(git *)"]},
  "hooks": {
    "SessionStart": [
      {"matcher": "startup", "hooks": [{"type": "command", "command": "old-hook"}]}
    ],
    "PreToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "other-event"}]}
    ]
  }
}
JSON

python3 bin/render_settings.py "$tmp/hooks.json" "$tmp/settings.json"

cat > "$tmp/check.py" << 'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
assert d["permissions"] == {"allow": ["Bash(git *)"]}, "deve preservar chaves nao relacionadas"
assert d["hooks"]["SessionStart"][0]["hooks"][0]["command"] == "new-hook", "fonte canonica deve sobrescrever evento declarado"
assert d["hooks"]["PreToolUse"][0]["hooks"][0]["command"] == "other-event", "deve preservar evento nao declarado na fonte canonica"
print("render_settings.py: merge de hooks correto (sobrescreve declarado, preserva o resto)")
PY

python3 "$tmp/check.py" "$tmp/settings.json"
