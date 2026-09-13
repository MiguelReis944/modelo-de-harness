# Activity Log

Registro append-only de operações do LLM Wiki neste vault.

## [2026-09-13] setup | obsidian-brain instalado
- Instalada a camada de esquema: `AGENTS.md`, `_meta/skills/` (8 skills), `_meta/taxonomy.md` (domínio engineering)
- Base curada pré-existente preservada: `team/`, `index.md`, `llms.txt`

## [2026-09-13] conectado ao app Obsidian
- Vault aberto manualmente no Obsidian (File > Open folder as vault) apontando pra
  `vault/` desta pasta.
- **Nota pra não repetir o erro**: `obsidian://open?path=...` via linha de comando tem um
  bug de encoding no Windows com caminho acentuado (`programação` vira `programaÃ§Ã£o`,
  UTF-8 lido como Latin-1) — ele abre o vault errado em silêncio. Nem o URI nem passar o
  caminho como argumento de CLI funcionaram. **Abrir manualmente pela UI é o caminho
  confiável** nesta máquina.
