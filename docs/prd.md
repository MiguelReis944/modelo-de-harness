# Requisitos do produto

## Problema e pessoas usuárias

Times que querem organizar vários repositórios e agentes precisam de um ponto de
partida replicável, sem importar o conteúdo privado de outro harness.

## Escopo atual

Este repositório é um template público do harness: fornece CLI, skills, agentes, MCP,
hooks, CI, vault operacional e projeções para um novo harness com `workspace/` vazio.

## Requisitos

- Permitir adotar o template e sincronizar as fontes para Claude Code e Codex.
- Adicionar projetos como submodules e criar a documentação canônica inicial.
- Manter o template sem projetos, segredos ou conhecimento privado do harness de origem.
- Permitir sincronizar caminhos compartilhados do harness oficial por allowlist revisável.

## Critérios de aceitação e evidências

README, `AGENTS.md`, `bin/harness`, `.github/scripts/sync-upstream.sh` e os caminhos
versionados devem explicar e executar o fluxo sem depender de um checkout privado.

## Fora de escopo

O template não importa submodules, `workspace.yaml` preenchido, vault curado ou
referências pessoais do harness oficial. A sincronização não substitui README, AGENTS,
workflows e vault operacional mantidos localmente.
