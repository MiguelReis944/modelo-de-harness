# Regras do projeto

## Invariantes

- `workspace.yaml` permanece com `projects: []` em uma instalação nova.
- Caminhos sincronizados pelo upstream são infraestrutura compartilhada e podem ser
  substituídos na próxima sincronização.
- O template público não recebe segredos, dados pessoais, projetos privados ou páginas
  curadas do harness de origem.

## Restrições

O upstream só pode copiar os caminhos explicitamente permitidos em
`.github/scripts/sync-upstream.sh`. README, AGENTS, workflows e vault operacional são
mantidos separadamente.

## Regras de trabalho

Leia README e AGENTS antes de editar. Faça mudanças de infraestrutura no harness
oficial quando elas precisarem ser propagadas; depois sincronize e revise o diff local.
Faça o commit do projeto novo dentro do submodule antes do commit do template.
