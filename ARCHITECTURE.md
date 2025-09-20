# Arquitetura do Módulo `src/app`

Este documento descreve a arquitetura atual de `src/app`, os princípios adotados, a decomposição por camadas/domínios e diretrizes para evolução. A reestruturação teve como objetivo alinhar-se ao módulo `src/fullstack`, manter apenas o essencial (YAGNI) e preservar o uso performático do AsyncPG.

## Sumário
1. Objetivos
2. Princípios Arquiteturais
3. Visão Geral de Camadas
4. Estrutura de Pastas
5. Descrição dos Componentes
6. Fluxo de Requisição
7. Regras de Dependência
8. Convenções de Nome e Estilo
9. Estratégia de Persistência (AsyncPG)
10. Tratamento de Erros e Respostas
11. Evolução e Extensões Futuras
12. Compatibilidade Garantida

---
## 1. Objetivos
- Reduzir complexidade (eliminar abstrações não usadas)
- Garantir clareza entre responsabilidade de cada arquivo
- Facilitar onboarding e testes
- Manter performance em operações I/O (AsyncPG direto)
- Minimizar acoplamento entre domínios

## 2. Princípios Arquiteturais
- YAGNI: só implementar quando existir uso real
- Single Responsibility por arquivo/módulo
- Limites explícitos entre HTTP (controllers), negócio (services) e dados (repositories)
- Schemas de entrada/saída isolados de modelos internos
- Fail fast + mensagens claras em exceções
- Dependência sempre em direção “de fora para dentro” (controller -> service -> repository)

## 3. Visão Geral de Camadas
| Camada | Papel | Pode depender de |
|--------|-------|------------------|
| Controllers | Entrada HTTP, validação inicial, formatação de resposta | Services, Schemas, DTOs, Exceptions |
| Services | Orquestração de regras de negócio e transações | Repositories, Schemas (validação), Exceptions |
| Repositories | Acesso a dados com AsyncPG | Conexão injetada, SQL, (eventualmente utils) |
| Schemas | Definição e validação estrutural (entrada/saída) | (Somente tipos/pydantic+librarias) |
| Lib (infra utilitária) | Injeção, DTOs, exceções | - |
| Server | Configuração de app, plugins, ciclo de vida | Lib, Config |
| Config | Parametrização (env, db, app) | - |

## 4. Estrutura de Pastas
```
src/app/
├── __about__.py                # Metadados do módulo/app
├── __main__.py                 # Entry point opcional (CLI/run)
├── asgi.py                     # ASGI application export
├── config/
│   ├── app.py                  # Montagem da configuração Litestar
│   ├── base.py                 # AppSettings / DatabaseSettings
│   ├── constants.py            # Constantes em uso
│   └── utils.py                # Funções utilitárias de env (renomeado de _utils)
├── db/
│   └── migrations/             # Scripts SQL versionados
│       └── 001_init.sql
├── lib/
│   ├── deps.py                 # Injeção (db, usuário atual, etc.)
│   ├── dto.py                  # APIResponse
│   └── exceptions.py           # Exceções / handlers
├── domain/
│   ├── root/                   # Endpoints raiz / health / info
│   │   ├── controllers.py
│   │   └── urls.py
│   ├── users/
│   │   ├── controllers.py      # Endpoints de usuários
│   │   ├── deps.py             # Dependências específicas
│   │   ├── repositories/       # Repositories especializados
│   │   │   ├── user.py         # UserRepository
│   │   │   └── session.py      # SessionRepository (autenticação)
│   │   ├── schemas.py          # Schemas (Create, Read, Login...)
│   │   ├── services.py         # Regras de usuário / sessão
│   │   └── urls.py             # Definição de rotas do domínio
│   └── teams/
│       ├── controllers.py      # Endpoints de times
│       ├── deps.py             # Dependências específicas
│       ├── guards.py           # Guards / authorization checks
│       ├── repository.py       # TeamRepository / PlayerRepository
│       ├── schemas.py          # Schemas de Team / Player
│       ├── services.py         # Lógica transacional e validações
│       ├── signals.py          # Sinais/eventos do domínio (publish hooks)
│       └── urls.py             # Definição de rotas do domínio
└── server/
    ├── auth.py                 # Autenticação / helpers de security
    ├── core.py                 # Criação e montagem da aplicação
    ├── lifespan.py             # Eventos de startup/shutdown
    ├── middleware.py           # Middlewares customizados
    └── plugins.py              # Plugins Litestar (cors, logging, etc.)
```

## 5. Descrição dos Componentes
### Config (`config/`)
- `base.py`: Classes de configuração (ex: `AppSettings`, `DatabaseSettings`). Centraliza leitura de env e default values.
- `app.py`: Agregação de middlewares, plugins, CORS, CSRF, logging, pool AsyncPG.
- `_utils.py`: Acesso enxuto a variáveis de ambiente; evita repetição.
- `constants.py`: Apenas valores realmente usados em runtime.

### Lib (`lib/`)
- `deps.py`: Providers de dependência (ex: `provide_db_connection`, `provide_current_user`).
- `dto.py`: `APIResponse` padroniza a forma de saída (consistência e testabilidade).
- `exceptions.py`: Exceções customizadas e/ou adaptadores para handlers.

### Domínios (`domain/<nome>/`)
- `repository.py` / `session_repository.py`: Execução direta de SQL usando conexão AsyncPG. Somente métodos invocados pelos services.
- `schemas.py`: Estruturas de entrada/saída (ex: criação, leitura, login). Sem lógica de negócio.
- `services.py`: Contém regras, validações adicionais e orquestração de múltiplos repositories. Pode abrir transações.
- `controllers.py`: Declara rotas/handlers; valida parâmetros simples; converte exceções para respostas.
- `deps.py`: Fornece dependências específicas (ex: carregar entidade a partir de ID).

### Server (`server/`)
- `core.py`: Função/fábrica principal que monta a aplicação.
- `lifespan.py`: Startup/shutdown (criação e fechamento de pool, pré-carga opcional, etc.).
- `plugins.py`: Registro de plugins do framework.

## 6. Fluxo de Requisição (Simplificado)
1. Request chega ao endpoint (controller) -> valida parâmetros básicos.
2. Controller chama service correspondente.
3. Service usa repositories (opcionalmente dentro de transação) e schemas para validação.
4. Repository executa SQL com conexão injetada.
5. Service retorna dados de domínio estruturados.
6. Controller encapsula em `APIResponse` + status code.

## 7. Regras de Dependência
Permitido:
- Controller -> Service -> Repository
- Service -> múltiplos Repositories
- Qualquer camada -> Schemas (apenas para validação/serialização)
- Qualquer camada -> Exceptions

Não permitido:
- Repository importando Service ou Controller
- Controller acessando SQL diretamente
- Service retornando objetos de conexão raw

## 8. Convenções de Nome e Estilo
- Repositories: `*Repository` (ex: `UserRepository`)
- Services: `*Service` ou funções coesas dentro de arquivo `services.py` quando simples
- Schemas: `EntityActionSchema` (ex: `UserCreateSchema`, `TeamReadSchema`)
- Funções de dependência: prefixo `provide_` ou `get_`
- Exceções específicas: `*Error` ou `*Exception`
- Respostas HTTP: sempre via `APIResponse` (quando aplicável)

## 9. Estratégia de Persistência (AsyncPG)
- Pool criado no ciclo de vida (startup) com parâmetros configuráveis
- Conexão fornecida via dependency injection (`provide_db_connection`)
- Transações coordenadas nos services (pattern: `async with connection.transaction():`)
- SQL escrito de forma explícita para clareza e performance

## 10. Tratamento de Erros e Respostas
- Erros de domínio convertidos em respostas HTTP com mensagens claras
- Uso de exceptions específicas para diferenciar: validação, não encontrado, conflito, autenticação
- `APIResponse` garante envelope consistente (ex: `{ "data": ..., "meta": ... }`)

## 11. Evolução e Extensões Futuras
Quando adicionar um novo domínio:
1. Criar pasta `domain/<novo>/`
2. Adicionar `schemas.py` primeiro (contratos)
3. Implementar `repository.py` com somente métodos necessários
4. Criar `services.py` orquestrando regras
5. Expor endpoints em `controllers.py`
6. Registrar rotas no agregador principal de URLs (se existir)

Checklist de aderência:
- [ ] Sem dependência invertida (repository usando service)
- [ ] Sem lógica de negócio em controllers
- [ ] Schemas sem acesso a banco
- [ ] Nomes seguindo convenções

## 12. Compatibilidade Garantida
A reestruturação manteve:
✅ Funcionalidades existentes
✅ Driver AsyncPG
✅ Schema de banco atual
✅ APIs e contratos estáveis
✅ Lógica de negócio essencial

## Resumo Final
A arquitetura prioriza clareza, isolamento e performance, evitando sobre-engenharia. Cada adição deve justificar sua existência por uso real ou necessidade concreta de manutenção/extensão.

---
Se surgir necessidade de detalhar métricas, tracing ou caching, estes devem ser adicionados como camadas opcionais sem acoplar domínios entre si.
