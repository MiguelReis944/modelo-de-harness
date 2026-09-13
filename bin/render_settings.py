#!/usr/bin/env python3
"""Merge hooks/hooks.json into .claude/settings.json, preserving whatever else is
already in settings.json (never overwrites the whole file).
Uso: render_settings.py <hooks.json> <settings.json>"""
import json, sys, os

def main():
    hooks_path, settings_path = sys.argv[1], sys.argv[2]

    with open(hooks_path, encoding="utf-8") as f:
        hooks_cfg = json.load(f)

    settings = {}
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                settings = json.loads(content)

    settings.setdefault("hooks", {})
    for event, matchers in hooks_cfg.get("hooks", {}).items():
        settings["hooks"][event] = matchers  # canonical source wins for events it declares

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    main()
