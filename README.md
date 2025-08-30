## Litestar Asyncpg API (Clean Architecture)

Camadas e responsabilidades:

- Domain: entidades (`msgspec.Struct`) e contratos (interfaces de repositório).
- Application: casos de uso (classes `@dataclass`) orquestrando regras de negócio.
- Infrastructure: repositórios `asyncpg` que acessam o banco.
- Presentation: rotas e controladores, middlewares, canais e eventos do Litestar.

Principais caminhos:

- Domain entities: `src/domain/entities/*.py`
- Repository interfaces: `src/domain/interfaces/*.py`
- Use cases: `src/application/use_cases/*.py`
- Repositories impl.: `src/infrastructure/repositories/*.py`
- Controllers: `src/presentation/controllers/*.py`
- Routes: `src/presentation/routes/*.py`
- Middlewares / Channels / Events: `src/presentation/middlewares|channels|events`

Dependências (principais):

- `litestar`, `litestar-asyncpg`, `bcrypt`, `pyjwt`, `python-dotenv`, `dependency-injector`.

Setup

1) .env

```
KEY=secret
DSN=postgresql://user:password@host:port/db
```

2) Banco

```sql
-- criar o banco antes de executar a aplicação
create database db;
```

3) Rodar o servidor

```bash
litestar run
```

Exemplos de rotas úteis:

- `POST /users/register` — cadastro de usuário
- `POST /users/auth` — autenticação (retorna token JWT)
- `POST /teams/players` — cria time e jogadores (autenticado)
- `GET /teams/players` — lista times e jogadores (autenticado)
- `GET /auth/data` — dados do usuário autenticado

OpenAPI

- `http://localhost:port/schema/redoc`
