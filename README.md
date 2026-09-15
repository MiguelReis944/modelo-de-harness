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

## Cinco skills de React (`react-doctor` + `react-scan`)

| Skill | Fonte | Pra que serve |
|---|---|---|
| `react-doctor` | [`millionco/react-doctor`](https://github.com/millionco/react-doctor) | Roda `npx react-doctor@latest` — scanner determinístico de state/effects, performance, arquitetura, segurança, acessibilidade. Score 0-100 |
| `improve-react` | mesmo repo | Read-only: lê o scan do react-doctor, prioriza por leverage real, escreve planos de implementação pra outro agente executar — nunca edita código |
| `improve-threejs` | mesmo repo | Mesma lógica pra Three.js/React Three Fiber (frame-loop, GPU leaks, scene-graph) |
| `performance` | mesmo repo | Diagnóstico de performance runtime via trace do DevTools + outlines de render ao vivo |
| `animation-best-practices` | [`aidenybai/react-scan`](https://github.com/aidenybai/react-scan) | Checklist de animação CSS/UI — hover, transição, flicker |

Ambos os repos são do mesmo autor/organização — Aiden Bai (`millionco`), também criador do
`million.js`; conta e organização verificadas antes de vendorizar. `react-scan` é o
predecessor do `react-doctor` (o próprio README dele recomenda migrar), por isso só o skill
secundário (`animation-best-practices`) veio de lá — o resto do valor de `react-scan` é como
dependência **no projeto** (`npm install -D react-scan`), não como skill do harness.

**Ressalva sobre `react-doctor` (o skill principal)**: o fluxo `/doctor` busca um
"playbook canônico" em tempo real (`curl https://www.react.doctor/prompts/...`) em vez de
seguir instruções versionadas neste repo — diferente de todo o resto do catálogo, que é
100% estático. O domínio é do próprio autor da ferramenta, não terceiro, mas é a mesma
classe de risco que `owasp-security` cataloga em "ASI04: Agentic Supply Chain
Vulnerabilities" (seguir instrução de fonte externa não fixada). Mantido por decisão
explícita do usuário. Os outros 3 skills (`improve-react`, `improve-threejs`,
`performance`) são 100% locais — dependem só do CLI, sem fetch remoto.

## MCP `playwright` (oficial da Microsoft)

Vem de [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp), pinado em
`@playwright/mcp@0.0.81`. **Nota do próprio fabricante**: o README oficial recomenda o
[`microsoft/playwright-cli`](https://github.com/microsoft/playwright-cli) (CLI + skills) em
vez do MCP especificamente pra coding agents — é mais eficiente em tokens porque evita
carregar schemas de tool e árvores de acessibilidade verbosas no contexto. Adicionado mesmo
assim por decisão explícita do usuário; se algum projeto do `workspace/` for web, já existe
`webapp-testing` (Playwright) e o Browser pane nativo do Claude Code, então há alguma
sobreposição de propósito.

## `ponytail` — modo "dev preguiçoso" sempre ativo

Diferente de todo o resto do catálogo, `ponytail` não ativa sob demanda por descrição —
ele se injeta em **toda resposta de código**, via hook, até ser desligado. A regra é uma
escada YAGNI: antes de escrever código novo, pare no primeiro degrau que resolver —
"isso já existe na codebase?", "a stdlib resolve?", "uma dependência já instalada
resolve?", "cabe numa linha?" — e só then escreva o mínimo necessário. Simplificação
deliberada que corta uma esquina real (lock global, scan O(n²)) é permitida, mas exige um
comentário `ponytail:` nomeando o teto e o caminho de upgrade — não é "esconder a
dívida", é rastreá-la.

Vem de [`dietrichgebert/ponytail`](https://github.com/dietrichgebert/ponytail) (MIT).
**Ressalva que não dá pra pular**: o repositório tem 138 mil estrelas contra 341
*watchers* e um dono com ~2 mil seguidores — uma proporção fora do padrão normal, sinal
de manipulação de estrelas (farm/compra). Isso não prova conteúdo malicioso, mas invalida
"popularidade" como sinal de confiança aqui. A decisão de vendorizar foi baseada em ler o
conteúdo inteiro (o `SKILL.md` principal, os 5 sub-skills, e os ~600 linhas de hooks JS)
antes de qualquer cópia — nada de rede, telemetria ou coleta de dados; os hooks só leem/
escrevem um arquivo de estado local.

**Como foi adaptado**: o pacote original é um plugin multi-agente (Cursor, Codex,
Copilot, Windsurf...) com ~15 arquivos de infraestrutura que este harness não usa. Só
vendorizamos a parte de Claude Code:

- `catalog/skills/ponytail{,-audit,-debt,-gain,-help,-review}/` — os 6 skills (o
  principal + 5 auxiliares: `ponytail-review` audita um diff, `ponytail-audit` audita o
  repo inteiro, `ponytail-debt` coleta os comentários `ponytail:` num ledger, `ponytail-
  gain`/`ponytail-help` são referência).
- `hooks/ponytail/` — os scripts Node que injetam o ruleset (`ponytail-activate.js` no
  `SessionStart`, `ponytail-subagent.js` no `SubagentStart` — sem isso sub-agentes
  disparados por Task rodam sem o modo, `ponytail-mode-tracker.js` no `UserPromptSubmit`,
  que lê comandos `/ponytail <nível>`). Uma única linha foi ajustada
  (`ponytail-instructions.js`): o caminho do `SKILL.md`, que no pacote original é
  `hooks/../skills/ponytail/SKILL.md` e aqui vira `hooks/../../catalog/skills/ponytail/SKILL.md`,
  para bater com a estrutura deste harness.

**Uso**: `/ponytail lite|full|ultra|off` troca o nível a qualquer momento; "stop ponytail"
ou "normal mode" desliga. **full** é o padrão. O estado persiste em `~/.claude/
.ponytail-active` — por usuário na máquina, não por repositório, então vale pra todo
projeto que você abrir com Claude Code, não só os deste harness.

## Sete skills de `mattpocock/skills`

[`mattpocock/skills`](https://github.com/mattpocock/skills) (MIT) é mantido por Matt
Pocock — criador do curso "Total TypeScript", ex-Vercel, ~45 mil seguidores, ~60 mil
assinantes da newsletter, listado no marketplace oficial do Claude Code. Sem red flags;
conferido skill a skill antes de vendorizar.

| Skill | Pra que serve |
|---|---|
| `git-guardrails-claude-code` | Hooks que **bloqueiam de verdade** `git push`, `reset --hard`, `clean`, `branch -D` etc. antes de executar — reforça em código o que hoje só existe como instrução textual |
| `setup-pre-commit` | Configura Husky + lint-staged (Prettier) + typecheck + tests em pre-commit num repo |
| `writing-for-agents` | Como escrever documentos PARA agentes — usar ao criar/editar skills, `AGENTS.md` ou `CLAUDE.md` |
| `handoff` | Compacta a conversa atual num documento de handoff pra outro agente/sessão continuar |
| `resolving-merge-conflicts` | Resolver um merge/rebase com conflito em andamento |
| `domain-modeling` | Constrói/afia o modelo de domínio de um projeto — `CONTEXT.md`, ADRs |
| `code-review-standards-spec` | Revisão em duas dimensões (Standards: segue convenção do repo? / Spec: entrega o que foi pedido?) rodando em sub-agentes paralelos |

`code-review-standards-spec` foi **renomeado** — o original se chama só `code-review`, que
colide com o skill nativo do Claude Code (`/code-review`, outra coisa). Diretório e
`name:` no frontmatter foram ajustados; resto do conteúdo é o original.

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
