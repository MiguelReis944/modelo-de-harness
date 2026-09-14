#!/usr/bin/env bash
# hooks/session-start.sh: o additionalContext precisa conter o texto REAL da skill
# using-superpowers, não só as bordas <EXTREMELY_IMPORTANT>...</EXTREMELY_IMPORTANT>.
# Regressão real: um pipe combinado com heredoc no mesmo stdin (`cmd | python3 - <<'PY'`)
# fazia o heredoc vencer e sys.stdin.read() no python voltar vazio (SC2259) — o hook
# emitia JSON valido mas com o conteudo do skill ausente, silenciosamente.
set -euo pipefail
cd "$(dirname "$0")/.."

out="$(bash hooks/session-start.sh)"

python3 -c "
import json, sys
d = json.loads(sys.argv[1])
ctx = d['hookSpecificOutput']['additionalContext']
assert len(ctx) > 1000, f'additionalContext suspeitosamente curto: {len(ctx)} chars'
assert 'Red Flags' in ctx, 'conteudo real do using-superpowers ausente (Red Flags nao encontrado)'
assert 'brainstorming' in ctx, 'conteudo real do using-superpowers ausente (brainstorming nao encontrado)'
print('session-start.sh: additionalContext tem', len(ctx), 'chars com conteudo real do skill')
" "$out"
