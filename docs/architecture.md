# Arquitetura atual

## Componentes e limites

`bin/` implementa a CLI; `catalog/` contém skills; `agents/` perfis; `mcp/` servidores;
`hooks/` automações; `vault/_meta/` operações da base; `templates/project-docs/` e
`bin/project_docs.py` padronizam novos projetos; `workspace/` começa vazio.

## Fluxos de dados e controle

`sync-upstream.sh` copia somente a allowlist a partir de uma referência Git do harness
oficial. `bin/harness sync` gera projeções locais. `new-project` adiciona um submodule,
cria documentos e atualiza o manifesto; `doctor` verifica a instalação.

## Interfaces

As interfaces são Bash, Python padrão, YAML, Markdown, Git submodules e os arquivos
gerados pelo sync. O template não exige um backend ou uma aplicação de produto.

## Decisões técnicas vigentes

O template mantém uma cópia própria do helper e dos seis templates para funcionar antes
do primeiro sync upstream. A allowlist inclui `templates/` para manter as cópias alinhadas.
