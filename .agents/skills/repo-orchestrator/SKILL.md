---
name: repo-orchestrator
description: Monta o contexto antes de qualquer execução num repo da workspace. Use SEMPRE no início de uma tarefa de código — identifica o repo pelo workspace.yaml, carrega a página dele no vault, e puxa PRs/issues recentes (GitHub).
allowed-tools: [read, grep, glob, exec]
triggers:
  user: ["/contexto", "/orquestrar"]
  model: ["comecar tarefa", "antes de implementar", "montar contexto do repo"]
---
# repo-orchestrator

## Quando usar
No começo de toda tarefa de implementação, antes de ler/escrever código de produto num
projeto dentro de `workspace/`.

## Passos
1. Descubra o repo atual (diretório em `workspace/<nome>`) e leia sua entrada em
   `workspace.yaml` (name, domain, type, summary) pra saber o que ele é.
2. Carregue o contexto do projeto: `vault/team/projetos/<repo>.md` (se existir) e
   `vault/team/regras-de-negocio.md` / `vault/team/glossario.md` pra regras que atravessam
   projetos.
3. Leia o `AGENTS.md` do próprio projeto (cada repo em `workspace/` pode ter o seu, com
   convenções específicas — isso tem prioridade sobre qualquer suposição genérica).
4. Se o MCP do GitHub estiver habilitado, puxe PRs/issues recentes do repo.
5. Sintetize um **contexto escopado** (só o necessário pra tarefa — não despeje o vault
   inteiro nem o AGENTS.md inteiro do projeto).
6. Proponha um plano e **pare pra gate humano** antes de alterar código, se a mudança for
   não-trivial.

## Lembrete sobre submodules
Este harness usa git submodules em `workspace/`. Commits de código de um projeto vão pro
remoto **daquele projeto**, nunca pro remoto do harness. Depois de commitar dentro de um
submodule, atualize o ponteiro no harness (`git add workspace/<repo> && git commit`). Veja
[AGENTS.md](../../../AGENTS.md) na raiz.

## Saída
Um resumo curto: o que é o repo, convenções relevantes do AGENTS.md dele, regras do vault
aplicáveis, PRs/issues recentes, e o plano.
