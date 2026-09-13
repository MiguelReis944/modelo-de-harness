# Instruções para agentes de IA neste repositório

Este repositório é um **harness**: um repositório guarda-chuva que não contém
código de aplicação diretamente. Cada pasta dentro de `workspace/` é um
**git submodule** — ou seja, um repositório Git independente, com seu próprio
remoto no GitHub, clonado dentro do harness.

A lista de projetos registrados está em [workspace.yaml](workspace.yaml).

## Regras importantes ao editar arquivos dentro de `workspace/<projeto>/`

- Cada `workspace/<projeto>/` tem seu **próprio histórico Git e remoto**.
  Commits feitos ali devem ser enviados (`git push`) para o repositório
  daquele projeto, nunca para o repositório do harness.
- Depois de commitar dentro de um submodule, o harness vai marcar esse
  submodule como "modified" (o ponteiro de commit mudou). Para atualizar o
  harness para apontar para o novo commit, é preciso rodar, na raiz do
  harness:
  ```
  git add workspace/<projeto>
  git commit -m "bump <projeto> para <commit>"
  ```
- Nunca rode `git commit` na raiz do harness esperando que isso comite
  mudanças de código dentro de um submodule — mudanças de conteúdo de um
  submodule só são commitadas dentro dele mesmo.

## Topologia

```
catalog/   biblioteca de skills — versionada, não carregada direto
mcp/       lista canônica de MCP servers (mcp/servers.json)
agents/    perfis de sub-agentes (orquestrador, revisor)
vault/     conhecimento: team/ (curado) + projects/ (LLM Wiki — ver vault/AGENTS.md)
hooks/     hooks do Claude Code (ex: injeta using-superpowers a cada SessionStart)
.claude/   projeção gerada por `bin/harness sync` (não editar direto)
bin/       a CLI `harness`
```

`catalog/`, `mcp/`, `agents/`, `vault/` e `hooks/` são a fonte de verdade. `.claude/`,
`CLAUDE.md` e `.mcp.json` são **gerados** por `bin/harness sync` (estão no `.gitignore`).
Depois de editar uma skill em `catalog/skills/`, um agente em `agents/` ou um hook em
`hooks/`, rode `bin/harness sync` de novo — a projeção é cópia, não symlink, porque criar
symlink no Windows exige Modo Desenvolvedor ou privilégio de admin.

**Hook ativo:** `hooks/session-start.sh` injeta o conteúdo da skill `using-superpowers`
como contexto a cada início/clear/compact de sessão (`SessionStart`), replicando o
mecanismo do `obra/superpowers` original — só que lendo de `catalog/skills/` deste repo
em vez de `${CLAUDE_PLUGIN_ROOT}` (não é distribuído como plugin aqui). Isso força a
checagem "existe skill pra isso?" antes de qualquer resposta, em toda sessão aberta
nesta pasta.

## Adicionando um novo projeto

Use `bin/harness new-project <nome> <url>` (faz `git submodule add` e adiciona a entrada
em `workspace.yaml`).

## Comandos da CLI (`bin/harness`)
- `sync` — projeta `catalog/`, `agents/` e `mcp/servers.json` pra `.claude/`, `CLAUDE.md`
  e `.mcp.json`
- `doctor` — confere binário do Claude Code, skills/agentes ativos, status dos
  submodules e MCP
- `skills` — lista catálogo vs. ativo (`harness.config.yaml`)
- `new-project <nome> <url>` — adiciona um repo como submodule em `workspace/`
- `update-projects` — atualiza todos os submodules pro commit mais recente do remoto
