# Reestruturação Arquitetural - src/app

Este documento resume as principais mudanças realizadas para alinhar a arquitetura de `src/app` com `src/fullstack`, mantendo o uso do AsyncPG e apenas o essencial.

## Principais Mudanças Realizadas

### 1. Configurações (config/)
- **base.py**: Configurações essenciais (DatabaseSettings, AppSettings)
- **app.py**: Configurações do Litestar (CORS, CSRF, Logging, AsyncPG)
- **_utils.py**: Utilitário simples para variáveis de ambiente
- **constants.py**: Apenas constantes realmente utilizadas

### 2. Dependency Injection (lib/deps.py)
- `provide_db_connection` para injeção de conexão AsyncPG
- `provide_current_user` para usuário atual
- Aliases de tipos essenciais

### 3. Repository Pattern
- Repositories específicos para cada domínio
- Apenas métodos utilizados pelos serviços
- Sem classe base abstrata (YAGNI)

### 4. Domain Layer Restructuring

#### Users Domain
- **repository.py**: `UserRepository` com métodos essenciais
- **session_repository.py**: `SessionRepository` para autenticação
- **schemas.py**: Schemas específicos (Create, Read, Login)
- **services.py**: Lógica de negócio usando repositories
- **controllers.py**: Endpoints com validações
- **deps.py**: Injeção de dependências

#### Teams Domain  
- **repository.py**: `TeamRepository` e `PlayerRepository`
- **schemas.py**: Schemas estruturados
- **services.py**: Operações de times com transações
- **controllers.py**: CRUD com tratamento de erros
- **deps.py**: Injeção de dependências

### 5. DTOs (lib/dto.py)
- Apenas `APIResponse` para respostas consistentes
- Removidas DTOs não utilizadas

### 6. Server Configuration (server/core.py)
- Sistema de dependências essencial
- Configuração simplificada

## Benefícios da Simplificação

### 1. YAGNI (You Aren't Gonna Need It)
- Removidas funcionalidades não utilizadas
- Código mais limpo e focado
- Manutenibilidade melhorada

### 2. Separação Clara
- **Repositories**: Apenas métodos usados nos serviços
- **Services**: Lógica de negócio essencial
- **Controllers**: Manipulação HTTP necessária
- **Schemas**: Validação específica por uso

### 3. Configuração Essencial
- Apenas configurações realmente utilizadas
- Variáveis de ambiente simplificadas
- Menos complexidade desnecessária

### 4. AsyncPG Otimizado
- Mantém performance do AsyncPG
- Repositories específicos para cada necessidade
- Pool de conexões configurável

## Compatibilidade

A reestruturação mantém:
- ✅ Todas as funcionalidades existentes
- ✅ AsyncPG como driver de banco
- ✅ Schema de banco atual
- ✅ APIs existentes
- ✅ Lógica de negócio essencial

## Arquitetura Resultante

```
src/app/
├── config/
│   ├── _utils.py          # Utilitário para env vars
│   ├── base.py            # Configurações essenciais
│   ├── app.py             # Configuração Litestar
│   └── constants.py       # Constantes utilizadas
├── lib/
│   ├── deps.py            # Dependency injection
│   ├── dto.py             # Response patterns
│   └── exceptions.py      # Exception handlers
├── domain/
│   ├── users/
│   │   ├── repository.py     # User data access
│   │   ├── session_repository.py # Session data access
│   │   ├── schemas.py        # User schemas
│   │   ├── services.py       # User business logic
│   │   ├── controllers.py    # User endpoints
│   │   └── deps.py          # User dependencies
│   └── teams/
│       ├── repository.py     # Team/Player data access
│       ├── schemas.py        # Team schemas
│       ├── services.py       # Team business logic
│       ├── controllers.py    # Team endpoints
│       └── deps.py          # Team dependencies
└── server/
    ├── core.py            # Application core
    ├── lifespan.py        # Lifecycle events
    └── plugins.py         # Litestar plugins
```

A arquitetura agora é mais simples, focada e mantém apenas o essencial para o funcionamento do projeto.
