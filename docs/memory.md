# Memória do projeto

## Fatos e decisões

- O template público começa com workspace vazio e `projects: []`.
- A direção de sincronização é harness oficial commitado → template; alterações locais
  no template em caminhos compartilhados podem ser sobrescritas.
- O conteúdo privado do vault e projetos reais não deve entrar neste repositório.

## Armadilhas conhecidas

Não editar projeções geradas diretamente. Depois de uma sincronização upstream, revise
o índice e os caminhos permitidos antes do checkpoint; o template não é o lugar para
registrar decisões de produto dos projetos hospedados.
