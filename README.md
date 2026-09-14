# harness

Repositório guarda-chuva que organiza múltiplos projetos independentes, cada um mantendo
seu próprio repositório Git no GitHub, via **git submodules** — com uma fonte canônica de
skills, MCP servers e perfis de sub-agente para o Claude Code, inspirado no padrão do
[fintech-harness](https://github.com/LucaPinheiro/fintech-harness).

Este repositório é um **template**: vem com `workspace/` vazio (`projects: []` em
[workspace.yaml](workspace.yaml)) e todo o resto — skills, agentes, MCP, CI — pronto pra
uso. A ideia é você adotar ele como o harness dos *seus* projetos.

## Como usar

### 1. Adote o template

```bash
git clone --recurse-submodules <url-deste-repo-ou-do-seu-fork> meu-harness
cd meu-harness
```

Se for usar como base do seu próprio harness (não só experimentar), troque o remoto pro
seu repositório: `git remote set-url origin <seu-novo-remoto>` (ou recrie do zero com
`git init` se preferir não carregar o histórico deste template).

### 2. Rode o setup inicial

```bash
./bin/harness sync     # gera CLAUDE.md, .claude/skills, .claude/agents, .mcp.json
./bin/harness doctor    # checagem: binário do claude, skills/agentes, hooks, MCP
claude                  # abre o Claude Code na raiz do harness
```

### 3. Diga ao agente quais repositórios você vai trabalhar

Dentro do Claude Code, não precisa decorar comando nenhum — é só colar os links dos
repositórios que você quer gerenciar por aqui e pedir pra adicionar. Por exemplo:

> Adiciona esses repos ao workspace:
> https://github.com/seu-usuario/projeto-a
> https://github.com/seu-usuario/projeto-b

O agente, para cada link:

1. Roda `bin/harness new-project <nome> <url>` (`git submodule add` + registra a entrada
   em `workspace.yaml`).
2. Preenche `domain`/`type`/`summary` daquela entrada (pergunta se não conseguir inferir).
3. Roda `sync` de novo e commita as mudanças **com sua aprovação**.

Opcionalmente, peça pra ligar o projeto ao vault de conhecimento (skill `bridge` — ver
[Vault](#vault--base-de-conhecimento-padrão-obsidian) abaixo) se quiser que o agente
sintetize specs/decisões daquele repo em páginas de wiki interligadas.

A partir daí, qualquer tarefa que você pedir sobre um desses projetos passa pela skill
`repo-orchestrator`: o agente identifica em qual repo a tarefa se aplica, lê o
`workspace.yaml`, o `AGENTS.md` do projeto e o vault, e só então propõe um plano — sem
você precisar dizer "cd pra tal pasta" toda vez.

Prefere fazer manualmente em vez de pedir pro agente? O comando é o mesmo que ele roda:

```bash
bin/harness new-project <nome> <url>
```

Depois preencha `domain`/`type`/`summary` da entrada em [workspace.yaml](workspace.yaml)
e commite.

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

## Clonando numa máquina nova (harness já com projetos)

Depois que você já adotou o template e adicionou projetos (passo 1-3 acima), clonar em
outra máquina é só:

```bash
git clone --recurse-submodules <url-do-seu-harness>
cd meu-harness
./bin/harness sync
./bin/harness doctor
claude
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

Ver [Como usar](#como-usar) — na prática, é pedir pro agente ou rodar
`bin/harness new-project <nome> <url>` diretamente.

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
| `claude-api` | referência de API/SDK da Anthropic — model ids, pricing, streaming, tool use, MCP, caching; complementa `mcp-builder` |
| `discernment-nudge` | autocrítica antes de finalizar uma resposta substantiva (plano, estimativa, análise) — complementa `verification-before-completion` |
| `vercel-react-best-practices` | 70 regras de performance React/Next.js da engenharia da Vercel, priorizadas por impacto |
| `vercel-composition-patterns` | padrões de composição de componentes React (compound components, render props, context) |
| `web-design-guidelines` | audita UI contra o Web Interface Guidelines (acessibilidade, UX) — complementa `frontend-design` (que é sobre estética, não compliance) |
| `writing-guidelines` | revisão de prosa/docs contra um guia de estilo — útil pro vault e READMEs |
| `deploy-to-vercel` | deploy de app/site na Vercel (preview por padrão, produção só se pedido explicitamente) |
| `vercel-optimize` | auditoria de custo/performance de projetos na Vercel (Next.js, SvelteKit, Nuxt) — métricas antes de recomendação |
| `supabase` | Database, Auth, RLS, Storage, Edge Functions, `supabase-js`/`@supabase/ssr` em Next.js/React — debugging de erros Postgres/Auth/Storage |
| `supabase-postgres-best-practices` | guia de performance Postgres mantido pela Supabase — índices, queries lentas, connection exhaustion, RLS que mata performance |
| `cloudflare` | skill "roteador" da Cloudflare — carrega referência específica sob demanda (R2, KV, Workers, Queues...); cobre R2 via API S3-compatible, presigned URLs, CORS, multipart, limits/pricing do free tier |
| `owasp-security` | checklist OWASP Top 10:2025, ASVS 5.0 (níveis L1/L2/L3), LLM Top 10:2025 e Agentic AI Security (2026, ASI01-10) — padrões seguros por linguagem (20+) e uma seção anti-falso-positivo antes de reportar achado |

`frontend-design`, `webapp-testing`, `mcp-builder`, `skill-creator`, `claude-api` e
`discernment-nudge` vêm oficialmente do repositório
[`anthropics/skills`](https://github.com/anthropics/skills) — mesma fonte das skills
nativas do Claude Code (docx, pdf, pptx...). `vercel-react-best-practices`,
`vercel-composition-patterns`, `web-design-guidelines`, `writing-guidelines`,
`deploy-to-vercel` e `vercel-optimize` vêm de
[`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills) — relevantes
porque pelo menos um projeto real gerenciado por este tipo de harness costuma ser
Next.js/React deployado na Vercel. `supabase` e `supabase-postgres-best-practices` vêm de
[`supabase/agent-skills`](https://github.com/supabase/agent-skills) (oficial); `cloudflare`
vem de [`cloudflare/skills`](https://github.com/cloudflare/skills) (oficial) — juntos
cobrem o resto do stack gratuito típico (Postgres/Auth via Supabase, storage de objetos
via R2 S3-compatible).

`owasp-security` é a única exceção ao padrão "só fonte oficial do fabricante" — não existe
skill oficial da OWASP. Vem de [`agamm/claude-code-owasp`](https://github.com/agamm/claude-code-owasp)
(MIT, mantenedor individual, mas conteúdo lido e conferido linha a linha antes de vendorizar).
Complementa o `/security-review` nativo do Claude Code (que varre o diff atual) com
checklists e padrões de referência — e a seção de Agentic AI Security cobre riscos do
próprio harness (MCP servers, sub-agentes), não só dos projetos em `workspace/`.

O catálogo completo pode crescer sem tudo ficar ativo — `active_skills` em
`harness.config.yaml` é o conjunto realmente carregado, pra não estourar a janela de
contexto. Hoje todas as skills do catálogo estão ativas; se a janela de contexto
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
