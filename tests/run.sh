#!/usr/bin/env bash
# Roda todos os tests/test_*.sh e reporta um resumo. Uso: bash tests/run.sh
set -euo pipefail
cd "$(dirname "$0")/.."

pass=0
fail=0

for t in tests/test_*.sh; do
  name="$(basename "$t")"
  if bash "$t"; then
    echo "PASS $name"
    pass=$((pass + 1))
  else
    echo "FAIL $name"
    fail=$((fail + 1))
  fi
done

echo ""
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
