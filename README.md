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
- Infra DB config (asyncpg): `src/infrastructure/database/asyncpg.py`
- Infra SQL (referência): `src/infrastructure/database/sql/tables.sql` (não é necessário executar manualmente)

Dependências (principais):

- `litestar`, `litestar-asyncpg`, `bcrypt`, `pyjwt`, `python-dotenv`, `dependency-injector`.

Setup

1) .env

```
KEY=secret
DSN=postgresql://user:password@host:port/db
ACCESS_TOKEN_SALT=xYzDeV@0000
JWT_ALG=HS256
ASYNC_PG_MIN_SIZE=4
ASYNC_PG_MAX_SIZE=16
CSRF_SECRET=secret
CORS_ALLOW_ORIGINS=*
CORS_ALLOW_METHODS=GET,POST,DELETE,PUT,PATCH,OPTIONS
CORS_ALLOW_HEADERS=Origin,Content-Type,X-CSRFToken,X-Access-Token
CORS_ALLOW_CREDENTIALS=true
GZIP_LEVEL=9
RATE_LIMIT_UNIT=second
RATE_LIMIT_RATE=10
RATE_LIMIT_EXCLUDE=/schema
CHANNELS=notifications
CHANNELS_CREATE_WS=true
```

2) Banco (PostgreSQL)

- Criar usuário e banco (psql):

```sql
-- conectar como superusuário (ex.: postgres)
CREATE ROLE app_user WITH LOGIN PASSWORD 'app_password';
CREATE DATABASE app_db OWNER app_user;
GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;
```

- Ativar extensão necessária no banco:

```sql
-- dentro do banco app_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

- Atualizar a `DSN` no `.env` para o banco criado:

```
DSN=postgresql://app_user:app_password@localhost:5432/app_db
```

- Criação automática de tabelas: ao iniciar a API, as tabelas são criadas automaticamente.

- Opcional (Docker): subir um Postgres rapidamente:

```bash
docker run --name pg \
  -e POSTGRES_USER=app_user \
  -e POSTGRES_PASSWORD=app_password \
  -e POSTGRES_DB=app_db \
  -p 5432:5432 -d postgres:16
# não é necessário rodar SQL manualmente; ao iniciar a API as tabelas serão criadas
```

3) Configurações

- Classe de configuração: `src/core/config/settings.py` expõe `settings.key` e `settings.dsn` (carregados do `.env`).


Como iniciar (Poetry)

- Instalar Poetry:

```bash
# Linux / macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

- Instalar dependências do projeto:

```bash
poetry install
```

- Plugin de shell do Poetry:

```bash
poetry self add poetry-plugin-shell
```

- Entrar no ambiente virtual do projeto:

```bash
poetry shell
```

- Configurar pre-commit:

```bash
pre-commit install --config pre-commit.yaml
```

- Iniciar a API (uvicorn):

```bash
uvicorn app:app --reload
```

Exemplos de rotas úteis:

- `POST /users/register` — cadastro de usuário
- `POST /users/auth` — autenticação (retorna token JWT)
- `POST /teams/players` — cria time e jogadores (autenticado)
- `GET /teams/players` — lista times e jogadores (autenticado)
- `GET /auth/data` — dados do usuário autenticado

OpenAPI

- `http://localhost:port/schema/redoc`
