#!/usr/bin/env bash
# render_mcp.py: filtra servers "enabled" e renderiza stdio/http corretamente.
set -euo pipefail
cd "$(dirname "$0")/.."

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cat > "$tmp/servers.json" << 'JSON'
{
  "servers": {
    "enabled-stdio": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "pkg@1.0.0"],
      "env": {"FOO": "${FOO}"},
      "enabled": true
    },
    "enabled-http": {
      "transport": "http",
      "url": "https://example.com/mcp",
      "enabled": true
    },
    "disabled": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "other"],
      "enabled": false
    }
  }
}
JSON

python3 bin/render_mcp.py "$tmp/servers.json" > "$tmp/out.json"

cat > "$tmp/check.py" << 'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
servers = d["mcpServers"]
assert set(servers.keys()) == {"enabled-stdio", "enabled-http"}, servers.keys()
assert servers["enabled-stdio"]["type"] == "stdio"
assert servers["enabled-stdio"]["args"] == ["-y", "pkg@1.0.0"]
assert servers["enabled-stdio"]["env"] == {"FOO": "${FOO}"}
assert servers["enabled-http"]["type"] == "http"
assert servers["enabled-http"]["url"] == "https://example.com/mcp"
print("render_mcp.py: filtra disabled, renderiza stdio+http corretamente")
PY

python3 "$tmp/check.py" "$tmp/out.json"
