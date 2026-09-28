# Taxonomia

Vocabulário controlado do vault. Sugira adições, não invente em silêncio.
Domínio: **engineering** (projetos pessoais de software — arquitetura, decisões, incidentes).

## Entity Types
- `service` — módulos, APIs, serviços internos de um projeto
- `pattern` — padrões de design, decisões arquiteturais
- `incident` — bugs, comportamentos inesperados, post-mortems
- `dependency` — bibliotecas, frameworks, serviços externos
- `adr` — registro de decisão arquitetural
- `certification` — certificado ou credencial obtida por pessoa
- `institution` — escola, empresa, organização, grupo
- `project` — produto ou repositório de software
- `person` — indivíduo (membro de equipe, contribuidor)
- `component` — parte de um serviço ou sistema maior
- `profile` — ativo público que representa a identidade profissional de uma pessoa

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
- `governs` — regra, conceito ou norma que determina o comportamento de uma entidade (ex.:
  uma lei ou um padrão de arquitetura `governs` o service que a implementa)

## Tags
- `#status/active` `#status/deprecated` `#status/planned` `#status/proposed` `#status/resolved`
- `#severity/critical` `#severity/high` `#severity/medium` `#severity/low`
- `#source-type/code` `#source-type/doc` `#source-type/incident` `#source-type/adr` `#source-type/spec` `#source-type/internal`
- `#confidence/high` `#confidence/medium` `#confidence/low`
