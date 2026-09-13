# harness vault — Knowledge Base

> Este vault é uma base de conhecimento LLM-maintained seguindo o padrão LLM Wiki.
> O LLM escreve e mantém o conteúdo do wiki; você cura fontes (drop de arquivo em `raw/`)
> e direciona a análise.

## Structure

```
vault/
├── AGENTS.md           ← você está aqui (contrato operacional do vault)
├── _meta/
│   ├── skills/         ← 8 skills operacionais (leia antes de cada operação)
│   │   ├── ingest.md, query.md, lint.md, cross-link.md, status.md, export.md
│   │   ├── context.md  ← gerador do arquivo-bússola (_context.md)
│   │   └── bridge.md   ← conector código ↔ KB
│   └── taxonomy.md     ← vocabulário controlado (tags, entity types, relation types)
├── projects/           ← um sub-wiki por projeto de workspace/
│   └── <project>/
│       ├── _context.md ← bússola auto-gerada (25-35 linhas, leia PRIMEIRO)
│       ├── raw/         ← fontes imutáveis (domínio seu — drop de arquivo aqui)
│       ├── wiki/        ← conhecimento compilado (concepts/, entities/, sources/)
│       ├── output/      ← artefatos gerados (relatórios, slides, etc.)
│       ├── index.md     ← catálogo do projeto
│       └── log.md       ← timeline do projeto
├── team/                ← conhecimento curado cross-projeto (regras, glossário, resumo por repo)
├── index.md             ← porta de entrada (MOC)
├── llms.txt             ← índice plano pra ingestão por agente
└── log.md               ← timeline global de atividade
```

> `team/`, `index.md` e `llms.txt` são a base curada pré-existente do harness — as
> operações do LLM Wiki vivem em `projects/` e nunca sobrescrevem esse conteúdo. Use
> `team/` como fonte extra ao fazer ingest/query.

## Rules

1. **Nunca modifique arquivos em `raw/`** — fontes são imutáveis, domínio do humano.
2. **Sempre atualize `index.md` e `log.md`** após qualquer operação que mude o wiki.
3. **Use `[[wikilinks]]`** para referências internas — o Obsidian resolve automaticamente
   (e funciona como texto normal em qualquer outro viewer de markdown).
4. **Adicione YAML frontmatter** a toda página de wiki que criar:
   ```yaml
   ---
   title: Page Title
   type: concept | entity | source-summary | comparison | analysis
   tags: [from taxonomy.md]
   sources: [list of source files this page draws from]
   confidence: high | medium | low
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   ---
   ```
5. **Siga `_meta/taxonomy.md`** para entity types, tags e relation types — sugira
   adições, não invente em silêncio.
6. **Sinalize contradições explicitamente** — nova informação que conflita com página
   existente: anote as duas com fonte e adicione relação `[contradicts]`.
7. **Um conceito por página** — divida páginas que cobrem múltiplos tópicos distintos.
8. **Leia `_context.md` primeiro** — ao entrar num projeto pela primeira vez na sessão,
   leia o `_context.md` dele antes de mergulhar nas páginas do wiki.
9. **Use relações tipadas** — toda página deveria ter uma seção `## Relations` com
   entradas como `- [depends_on] [[Target Page]]`, usando tipos de `_meta/taxonomy.md`.

## Projects

| Project | Domain | Description |
|---------|--------|-------------|
| _(nenhum projeto ainda — use a skill `bridge` pra conectar um de `workspace/`)_ | | |

## Operations

Este vault tem 8 skills operacionais em `_meta/skills/`. Leia o arquivo da skill
relevante antes de executar qualquer operação.

| Operação | Skill | Quando usar |
|----------|-------|-------------|
| **Ingest** | `_meta/skills/ingest.md` | Você dropa uma fonte em `raw/` e pede pra processar |
| **Query** | `_meta/skills/query.md` | Você faz uma pergunta sobre a base de conhecimento |
| **Lint** | `_meta/skills/lint.md` | Health check, ou após grandes lotes de ingestão |
| **Cross-link** | `_meta/skills/cross-link.md` | Após ingest, ou pra melhorar conexões |
| **Status** | `_meta/skills/status.md` | O que foi ingerido, o que mudou, o que está pendente |
| **Export** | `_meta/skills/export.md` | Quer artefatos: reports, slides, timelines, glossários |
| **Context** | `_meta/skills/context.md` | Auto-disparado após ingest/lint; ou manual pra atualizar a bússola |
| **Bridge** | `_meta/skills/bridge.md` | Conectar um projeto de `workspace/` a este vault |

### Workflow: sessão típica
1. Você dropa fonte(s) em `projects/<nome>/raw/`
2. **Ingest** — lê e processa cada fonte → cria/atualiza páginas com relações tipadas
3. **Cross-link** — varre menções não-linkadas → insere `[[wikilinks]]` e `## Relations`
4. **Context** — regenera `_context.md` (disparado pelo ingest)
5. **Status** — reporta o que foi feito

### Workflow: integração com código
1. **Bridge** — conecta um projeto em `workspace/<nome>` a `vault/projects/<nome>` (setup único)
2. Ao codar: leia `_context.md` → páginas de wiki relevantes pra decisões/regras do projeto
3. Após mudança que afeta uma decisão documentada: atualize a página de entidade correspondente

## Domain Context

Projetos pessoais de engenharia de software, independentes entre si. Ênfase em
**ingest** (specs, decisões, notas de arquitetura) e **lint** (consistência conforme o
vault cresce). Fontes curadas já disponíveis: `team/regras-de-negocio.md`,
`team/glossario.md`, `team/projetos/`.
