---
name: prepare-harness
description: Pré-configura o harness para clone-and-go. Use no primeiro setup (clone novo da máquina) — checa pré-requisitos, inicializa os submodules de workspace/ e projeta a config de MCP.
allowed-tools: [read, grep, glob, exec]
triggers:
  user: ["/prepare-harness", "/preparar-harness"]
  model: ["preparar o harness", "primeiro setup do harness", "inicializar os submodules"]
---
# prepare-harness

> Este harness usa **git submodules** em `workspace/` (não clones soltos) — cada projeto é
> registrado em `.gitmodules` e listado em `workspace.yaml`.

## Quando usar
- Logo após clonar este harness numa máquina nova.
- Quando algum submodule esperado está vazio (pasta existe mas sem conteúdo).
- Depois de adicionar um novo projeto com `bin/add-project.sh`.

## O que faz
1. Valida pré-requisitos do ambiente (`git`, acesso aos repositórios listados).
2. Inicializa/atualiza todos os submodules:
   ```bash
   git submodule update --init --recursive
   ```
3. Projeta a config de MCP gerando `.mcp.json` a partir de `mcp/servers.json` (só os
   servers `enabled`), via `bin/harness sync`.
4. Confere que `workspace.yaml` e `.gitmodules` estão consistentes (mesma lista de projetos).

## Como executar
```bash
git submodule update --init --recursive
./bin/harness sync
./bin/harness doctor
```

## Pré-requisitos
- `git` instalado.
- Acesso aos repositórios listados em `.gitmodules` (chave SSH ou credencial HTTPS).
- `python3` — usado pelo renderer de MCP (`bin/render_mcp.py`).

## Notas sobre MCP
- Fonte canônica: `mcp/servers.json` (marque `enabled: true/false`). Credenciais/tokens
  ficam **locais** (env / `*.local.json`), nunca no repo.
- O Claude Code lê MCP project-scope de `.mcp.json` na raiz. Se editar `mcp/servers.json`
  com a sessão já aberta, rode `./bin/harness sync` e reinicie a sessão (ou `/mcp`).

## Saída
Resumo: quais submodules foram inicializados/atualizados, quais MCP servers ficaram no
`.mcp.json`, e quaisquer falhas de acesso.
