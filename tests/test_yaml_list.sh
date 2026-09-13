#!/usr/bin/env bash
# bin/yaml_list.py: itens simples, entre aspas (com '#' dentro), e comentario inline real.
set -euo pipefail
cd "$(dirname "$0")/.."

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cat > "$tmp/config.yaml" << 'YAML'
name: harness

active_skills:
  - plain-item
  - "quoted item with # not a comment"
  - item-with-trailing-comment  # this is a real comment
  - 'single-quoted'

active_agents:
  - agent-one

other_key: value
YAML

got_skills="$(python3 bin/yaml_list.py active_skills "$tmp/config.yaml")"
expected_skills=$'plain-item\nquoted item with # not a comment\nitem-with-trailing-comment\nsingle-quoted'
if [ "$got_skills" != "$expected_skills" ]; then
  echo "MISMATCH active_skills:"
  echo "got:  [$got_skills]"
  echo "want: [$expected_skills]"
  exit 1
fi

got_agents="$(python3 bin/yaml_list.py active_agents "$tmp/config.yaml")"
[ "$got_agents" = "agent-one" ] || { echo "MISMATCH active_agents: got [$got_agents]"; exit 1; }

echo "yaml_list.py: aspas com '#' interno, comentario inline real, multiplas chaves - ok"
