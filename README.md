# harness

Repositório guarda-chuva que organiza múltiplos projetos independentes, cada um mantendo
seu próprio repositório Git no GitHub, via **git submodules** — com uma fonte canônica de
skills, MCP servers e perfis de sub-agente para o Claude Code, inspirado no padrão do
[fintech-harness](https://github.com/LucaPinheiro/fintech-harness).

## Estrutura

```
harness/
├── .github/workflows/ci.yml  # valida JSON, shellcheck, sync/doctor e testes a cada push/PR
├── .gitmodules           # gerado pelo git, mapeia cada submodule ao seu remoto
├── harness.config.yaml   # perfil ativo: quais skills/agentes ligar
├── workspace.yaml        # manifesto dos projetos (domain/type/summary)
├── AGENTS.md             # contrato do agente (lido também como CLAUDE.md, gerado)
├── bin/
│   ├── harness            # CLI: sync | doctor | skills | new-project | update-projects
│   ├── yaml_list.py        # parser da lista YAML de harness.config.yaml (sem awk)
│   ├── render_mcp.py       # mcp/servers.json -> .mcp.json
│   └── render_settings.py  # hooks/hooks.json -> .claude/settings.json (merge)
├── tests/                 # testes de bin/*.py, sem dependências externas (bash tests/run.sh)
├── catalog/skills/        # biblioteca de skills (Agent Skills / SKILL.md)
├── agents/                # perfis de sub-agente (orquestrador, revisor)
├── mcp/servers.json       # MCP servers canônicos (GitHub, context7, ...)
├── vault/                 # conhecimento cross-projeto + 1 página por repo
└── workspace/             # cada subpasta é um submodule (repo próprio)
    ├── projeto-a/
    ├── projeto-b/
    └── ...
```

`catalog/`, `agents/`, `mcp/` e `vault/` são a **fonte de verdade**, versionada. `.claude/`,
`CLAUDE.md` e `.mcp.json` são **gerados** por `bin/harness sync` (estão no `.gitignore`) —
depois de editar uma skill ou agente, rode `sync` de novo pra propagar.

## Como funciona um git submodule

Um submodule é uma referência do harness a um **commit específico** de outro repositório.
O harness não guarda o código do projeto-filho — guarda apenas a URL (`.gitmodules`) e
qual commit está "ativo" (ponteiro no índice do Git, modo `160000`).

Cada projeto dentro de `workspace/` continua sendo um repositório 100% independente, com
seu próprio histórico e remoto. Commits e pushes dentro de `workspace/<projeto>`, por
exemplo, vão para o remoto daquele projeto, nunca para o repositório do harness.

## Setup (primeira vez / máquina nova)

```bash
git clone --recurse-submodules <url-do-seu-fork-ou-harness>
cd harness
./bin/harness sync     # gera CLAUDE.md, .claude/skills, .claude/agents, .mcp.json
./bin/harness doctor    # checagem
claude                  # abra o Claude Code na raiz (ou em workspace/<projeto>)
```

Se já clonou sem `--recurse-submodules`: `git submodule update --init --recursive`.

## Comandos (`bin/harness`)

- `sync` — projeta `catalog/`, `agents/` e `mcp/servers.json` pra `.claude/`, `CLAUDE.md`
  e `.mcp.json`
- `doctor` — confere binário do Claude Code, skills/agentes ativos, status dos submodules
  e MCP servers
- `skills` — lista catálogo completo vs. o conjunto ativo (`harness.config.yaml`)
- `new-project <nome> <url>` — adiciona um repo como submodule em `workspace/`
- `update-projects` — atualiza todos os submodules pro commit mais recente do remoto

## Testes e CI

`tests/` cobre os scripts em `bin/` (sem framework, sem dependência externa):

```bash
bash tests/run.sh
```

O `.github/workflows/ci.yml` roda isso a cada push/PR na `main`, mais validação de JSON
(`mcp/servers.json`, `hooks/hooks.json`), `shellcheck` em `bin/harness` e
`hooks/session-start.sh`, e um `sync` + `doctor` completos — garante que a projeção pro
Claude Code não quebra silenciosamente.

## Fluxo do dia a dia

### Trabalhar em um projeto existente

Entre na pasta do projeto e trabalhe normalmente — é um repositório Git comum:

```bash
cd workspace/<projeto>
git add .
git commit -m "minha mudança"
git push
```

Depois de commitar dentro do submodule, o harness marca essa pasta como modificada
(o ponteiro de commit mudou). Para fixar a nova versão no harness:

```bash
cd ../..
git add workspace/<projeto>
git commit -m "bump <projeto>"
```

### Adicionar um novo projeto

```bash
bin/harness new-project novo-projeto https://github.com/<seu-usuario>/novo-projeto.git
```

Depois, preencha `domain`/`type`/`summary` da entrada em [workspace.yaml](workspace.yaml)
e crie a página correspondente em `vault/team/projetos/<nome>.md`, e commite.

## Skills ativas (`catalog/skills/`)

A maior parte do catálogo é o **[Superpowers](https://github.com/obra/superpowers)**
(Jesse Vincent/obra) vendorizado diretamente da fonte — não uma cópia adaptada. É um
sistema coeso: `using-superpowers` é o "manual" que ensina quando puxar cada skill;
`brainstorming` classifica a tarefa (spike/bounded/architectural) e escala o processo
de acordo; `writing-plans` → `executing-plans`/`subagent-driven-development` levam do
plano à implementação com checkpoints de revisão; `finishing-a-development-branch`
fecha o ciclo.

| Skill | Pra que serve |
|---|---|
| `using-superpowers` | regra de entrada: antes de qualquer resposta, checar se alguma skill se aplica |
| `repo-orchestrator` | monta contexto (workspace.yaml + vault + AGENTS.md do projeto) antes de codar |
| `prepare-harness` | inicializa os submodules e projeta MCP num setup novo |
| `brainstorming` | classifica a tarefa e transforma ideia em design aprovado + doc `.md` **antes** de codar |
| `writing-plans` / `executing-plans` | planejar e executar tarefas multi-etapa com checkpoints de revisão |
| `subagent-driven-development` | executa um plano despachando um subagente implementador por tarefa, com revisão a cada uma |
| `dispatching-parallel-agents` | despacha agentes em paralelo pra falhas/tarefas independentes |
| `test-driven-development` | escrever teste antes da implementação |
| `systematic-debugging` | investigação metódica antes de propor correção |
| `docker-compose` | padrões de orquestração local |
| `verification-before-completion` | exige rodar e conferir antes de alegar "pronto" |
| `using-git-worktrees` | isolar trabalho de feature em worktree separado |
| `requesting-code-review` / `receiving-code-review` | pedir revisão e tratar feedback com rigor técnico |
| `finishing-a-development-branch` | fecha o ciclo: merge, PR, manter ou descartar |
| `writing-skills` | criar/editar skills novas seguindo o método TDD (RED-GREEN-REFACTOR aplicado a documentação) |
| `obsidian-brain` | monta/estende o `vault/` como base de conhecimento LLM-maintained (padrão Obsidian) |
| `github-actions` | CI/CD seguro (permissions mínimas, actions pinadas por SHA, OIDC) pros workflows dos repos em `workspace/` |
| `frontend-design` | design visual distinto e deliberado — evita "cara de IA" (gradiente roxo, Inter, cards genéricos) |
| `webapp-testing` | toolkit oficial de testes web com Playwright (screenshot, log de console, descoberta de elemento) |
| `mcp-builder` | guia pra construir servidor MCP (Python/FastMCP ou Node/TS) — expor um projeto como ferramenta do Claude Code |
| `skill-creator` | criar/empacotar/avaliar skills novas (scripts de validação e benchmark) |

`frontend-design`, `webapp-testing`, `mcp-builder` e `skill-creator` vêm oficialmente do
repositório [`anthropics/skills`](https://github.com/anthropics/skills) — mesma fonte das
skills nativas do Claude Code (docx, pdf, pptx...).

O catálogo completo pode crescer sem tudo ficar ativo — `active_skills` em
`harness.config.yaml` é o conjunto realmente carregado, pra não estourar a janela de
contexto. Hoje as 23 skills do catálogo estão todas ativas; se a janela de contexto
apertar, desative alguma removendo a entrada correspondente e rodando `sync` de novo.

**Hook de enforcement instalado:** `hooks/session-start.sh` (declarado em
`hooks/hooks.json`, projetado por `bin/harness sync` para `.claude/settings.json`)
injeta o conteúdo inteiro da skill `using-superpowers` como contexto a cada início,
`/clear` ou compactação de sessão — igual ao mecanismo do `obra/superpowers` original,
só que lendo de `catalog/skills/` deste repo em vez de `${CLAUDE_PLUGIN_ROOT}` (aqui não
é distribuído como plugin). Isso faz a checagem "existe skill pra isso?" valer pra toda
sessão aberta nesta pasta, não só quando alguém lembra de invocar a skill manualmente.

## Sub-agentes (`agents/`)

- **orquestrador** — ponto de entrada, não escreve código de produto direto, identifica o
  repo e monta contexto (roda `repo-orchestrator`).
- **revisor** — revisa diff antes de PR (lógica, segurança, convenções do projeto), sempre
  termina em `APPROVE` ou `REQUEST_CHANGES`.

## Vault — base de conhecimento (padrão Obsidian)

`vault/` segue o padrão **LLM Wiki**: você joga fontes soltas em
`vault/projects/<nome>/raw/` (specs, decisões, notas) e pede pro agente processar — ele
lê, sintetiza e mantém páginas de wiki interligadas (`[[wikilinks]]`) em
`vault/projects/<nome>/wiki/`. `vault/AGENTS.md` é o contrato inteiro; 8 operações vivem
em `vault/_meta/skills/`:

| Operação | Quando usar |
|---|---|
| `ingest` | processar uma fonte nova dropada em `raw/` |
| `query` | perguntar algo — a resposta vem do wiki, não é reinventada |
| `cross-link` | conectar menções soltas com `[[wikilinks]]` e relações tipadas |
| `lint` | health check — links quebrados, páginas órfãs, contradições |
| `status` | dashboard: o que foi ingerido, o que está pendente |
| `export` | gerar relatório/slide/timeline/glossário a partir do wiki |
| `context` | regenera a "bússola" (`_context.md`) de cada projeto — ~1000 tokens de orientação rápida |
| `bridge` | conecta um projeto de `workspace/` ao `vault/` (cria `.claude/kb-link.md` no projeto) |

Como o vault é só markdown, ele funciona igual sem o app Obsidian instalado — mas se você
abrir a pasta `vault/` no Obsidian, ganha grafo de conexões e busca visual de graça.

A skill `bridge` cria o esqueleto em `vault/projects/<nome>/` na primeira vez que você
conecta um projeto de `workspace/` ao vault. Pra começar: jogue um arquivo em
`vault/projects/<nome>/raw/` e peça "faz o ingest desse arquivo".

## Por que não colocar tudo num repositório só?

Se todos os projetos vivessem dentro do repositório do harness sem submodules, o Git do
harness tentaria versionar os arquivos deles junto — impossível cada um ter seu próprio
histórico/remote/PRs separados. Submodules resolvem isso: o harness só guarda uma "foto"
(ponteiro de commit) de cada projeto, e cada projeto continua sendo commitado e publicado
no seu próprio repositório.
