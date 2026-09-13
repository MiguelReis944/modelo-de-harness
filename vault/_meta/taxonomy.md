# Taxonomia

Vocabulário controlado do vault. Sugira adições, não invente em silêncio.
Domínio: **engineering** (projetos pessoais de software — arquitetura, decisões, incidentes).

## Entity Types
- `service` — módulos, APIs, serviços internos de um projeto
- `pattern` — padrões de design, decisões arquiteturais
- `incident` — bugs, comportamentos inesperados, post-mortems
- `dependency` — bibliotecas, frameworks, serviços externos
- `adr` — registro de decisão arquitetural

## Relation Types
- `depends_on` — precisa de outra entidade pra funcionar
- `implements` — realiza um padrão, spec ou ADR
- `extends` — constrói em cima de / adiciona a outra entidade
- `contradicts` — conflita com outra afirmação ou página (sinalizar pra resolução)
- `related_to` — associação geral (só quando nenhum tipo específico se aplica)
- `part_of` — componente ou subconjunto de uma entidade maior
- `used_by` — consumido ou referenciado por outra entidade
- `supersedes` — substitui uma versão ou decisão anterior
- `calls` — invocação entre serviços/módulos ou chamada de API
- `deploys_to` — roda num alvo de infraestrutura específico

## Tags
- `#status/active` `#status/deprecated` `#status/planned`
- `#severity/critical` `#severity/high` `#severity/medium` `#severity/low`
- `#source-type/code` `#source-type/doc` `#source-type/incident` `#source-type/adr`
