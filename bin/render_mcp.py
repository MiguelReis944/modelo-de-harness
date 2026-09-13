#!/usr/bin/env python3
"""Renderiza mcp/servers.json no formato do Claude Code (.mcp.json).
Uso: render_mcp.py <servers.json>
Emite { "mcpServers": { ... } } em stdout, só com servers enabled."""
import json, sys

def main():
    path = sys.argv[1]
    with open(path) as f:
        data = json.load(f)
    out = {"mcpServers": {}}
    for name, s in data.get("servers", {}).items():
        if not s.get("enabled", False):
            continue
        transport = s.get("transport", "stdio")
        if transport == "stdio":
            entry = {"type": "stdio", "command": s["command"], "args": s.get("args", [])}
            if s.get("env"):
                entry["env"] = s["env"]
        else:  # http / streamable http
            entry = {"type": "http", "url": s["url"]}
        out["mcpServers"][name] = entry
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
