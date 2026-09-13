# Regras cross-projeto

> Os projetos deste harness são independentes entre si — não compartilham domínio de
> negócio. Regras específicas de cada um vivem na página do projeto em
> [projetos/](projetos/), não aqui.

## Convenções que valem pra qualquer projeto neste harness
- Nunca commitar segredo/credencial — usar `.env` (gitignored) ou `*.example`.
- Cada projeto em `workspace/` é um git submodule: commit e push vão para o remoto
  **daquele projeto**, nunca para o remoto do harness. Ver [AGENTS.md](../../AGENTS.md).
- Antes de mudar algo não-trivial, ler o `AGENTS.md`/`README.md` do próprio projeto — ele
  tem prioridade sobre qualquer suposição genérica feita aqui.
