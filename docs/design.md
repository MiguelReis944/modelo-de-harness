# Design de interação

## Jornadas de uso

Uma pessoa clona o template com submodules, roda `sync`, confere `doctor` e adiciona
projetos informando nome e URL. Para cada projeto, a CLI cria a documentação e mostra
os checkpoints separados.

## Interação e comportamento

`sync` relata cada projeção; `doctor` aponta ausências; `skills` mostra catálogo e
ativação; `new-project` valida o nome, preserva manifesto YAML válido e informa a ordem
dos commits. O vault oferece ingest, query, lint, cross-link, context e bridge.

## Linguagem visual

Não há superfície visual de produto. O design é de CLI e documentação: mensagens devem
ser copiáveis, seguras para nomes com espaços e claras sobre o repositório que recebe
cada mudança.
